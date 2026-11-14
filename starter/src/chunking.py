"""Implement fixed-size and structure-aware chunking."""
from .models import Chunk, DocumentPage


def fixed_size(page: DocumentPage, size: int = 500, overlap: int = 50) -> list[Chunk]:
    """Split text into overlapping windows and retain page metadata."""
    text = page.text
    if not text:
        return []
    
    chunks: list[Chunk] = []
    step = size - overlap
    if step <= 0:
        step = size
        
    start = 0
    idx = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + size, text_len)
        chunk_text = text[start:end].strip()
        
        if chunk_text:
            chunk_id = f"A_p{page.page}_{idx:03d}"
            c_meta = dict(page.metadata)
            c_meta.update({
                "strategy": "A_fixed",
                "start_char": start,
                "end_char": end,
                "chunk_len": len(chunk_text)
            })
            chunks.append(Chunk(
                chunk_id=chunk_id,
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=chunk_text,
                metadata=c_meta
            ))
            idx += 1
            
        if end >= text_len:
            break
        start += step
        
    return chunks


def by_paragraph(page: DocumentPage, max_size: int = 800) -> list[Chunk]:
    """Group paragraphs / structure blocks, split oversized blocks and retain metadata."""
    text = page.text
    if not text:
        return []
    
    # Split by double newline first, or lines starting with Article/bullet point
    raw_paragraphs = text.split("\n\n")
    paragraphs: list[str] = []
    for p in raw_paragraphs:
        p_clean = p.strip()
        if p_clean:
            paragraphs.append(p_clean)
            
    chunks: list[Chunk] = []
    curr_text = ""
    idx = 0
    
    for p in paragraphs:
        if len(p) > max_size:
            # If current accumulated text is not empty, flush it
            if curr_text:
                chunk_id = f"B_p{page.page}_{idx:03d}"
                c_meta = dict(page.metadata)
                c_meta.update({"strategy": "B_paragraph", "chunk_len": len(curr_text)})
                chunks.append(Chunk(
                    chunk_id=chunk_id,
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=curr_text,
                    metadata=c_meta
                ))
                idx += 1
                curr_text = ""
            
            # Split oversized paragraph by sentences or fixed window
            sub_start = 0
            while sub_start < len(p):
                sub_end = min(sub_start + max_size, len(p))
                sub_text = p[sub_start:sub_end].strip()
                if sub_text:
                    chunk_id = f"B_p{page.page}_{idx:03d}"
                    c_meta = dict(page.metadata)
                    c_meta.update({"strategy": "B_paragraph", "chunk_len": len(sub_text)})
                    chunks.append(Chunk(
                        chunk_id=chunk_id,
                        document_id=page.document_id,
                        source=page.source,
                        page=page.page,
                        text=sub_text,
                        metadata=c_meta
                    ))
                    idx += 1
                sub_start = sub_end
        else:
            if curr_text and len(curr_text) + len(p) + 2 > max_size:
                # Flush
                chunk_id = f"B_p{page.page}_{idx:03d}"
                c_meta = dict(page.metadata)
                c_meta.update({"strategy": "B_paragraph", "chunk_len": len(curr_text)})
                chunks.append(Chunk(
                    chunk_id=chunk_id,
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=curr_text,
                    metadata=c_meta
                ))
                idx += 1
                curr_text = p
            else:
                if curr_text:
                    curr_text += "\n\n" + p
                else:
                    curr_text = p
                    
    if curr_text:
        chunk_id = f"B_p{page.page}_{idx:03d}"
        c_meta = dict(page.metadata)
        c_meta.update({"strategy": "B_paragraph", "chunk_len": len(curr_text)})
        chunks.append(Chunk(
            chunk_id=chunk_id,
            document_id=page.document_id,
            source=page.source,
            page=page.page,
            text=curr_text,
            metadata=c_meta
        ))
        
    return chunks
