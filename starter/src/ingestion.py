"""Read and normalize source data."""
from pathlib import Path
import unicodedata
import re
import pypdf
from .models import DocumentPage


def get_chapter_for_page(page_num: int) -> tuple[str, str]:
    """Map page number to chapter and category."""
    if 1 <= page_num <= 9:
        return "Chương I", "Quy_dinh_chung"
    elif 10 <= page_num <= 13:
        return "Chương II", "Chuong_trinh_dao_tao"
    elif 14 <= page_num <= 29:
        return "Chương III", "To_chuc_dao_tao"
    elif 30 <= page_num <= 31:
        return "Chương IV", "Nghien_cuu_khoa_hoc"
    elif 32 <= page_num <= 34:
        return "Chương V", "Giang_vien_Co_van"
    elif 35 <= page_num <= 37:
        return "Chương VI", "Quyen_va_nghia_vu_sinh_vien"
    elif 38 <= page_num <= 46:
        return "Chương VII", "Kiem_tra_danh_gia"
    elif 47 <= page_num <= 49:
        return "Chương VIII", "Tot_nghiep"
    elif 50 <= page_num <= 52:
        return "Chương IX", "Dieu_khoan_thi_hanh"
    return "Chương I", "Quy_dinh_chung"


def normalize_text(text: str) -> str:
    """Normalize Unicode (NFC) and whitespace without discarding useful structure."""
    if not text:
        return ""
    # NFC normalization for Vietnamese accents
    text = unicodedata.normalize("NFC", text)
    # Remove control characters except newlines
    text = re.sub(r'[\r\t\f\v]', ' ', text)
    # Replace non-breaking spaces
    text = text.replace('\xa0', ' ')
    # Clean multiple spaces within lines
    lines = [re.sub(r'[ ]+', ' ', line).strip() for line in text.split('\n')]
    # Remove completely empty lines at extremities
    cleaned_text = '\n'.join(lines)
    # Collapse 3+ newlines to 2 newlines
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text).strip()
    return cleaned_text


def load_pdf(path: Path, document_id: str = "vnu_uet_quy_che_3626", source: str = "Quy-che-3626-digital.pdf") -> list[DocumentPage]:
    """Extract each physical page; keep its page number, source, and chapter metadata."""
    reader = pypdf.PdfReader(str(path))
    pages: list[DocumentPage] = []
    
    for idx, raw_page in enumerate(reader.pages):
        page_num = idx + 1
        raw_text = raw_page.extract_text() or ""
        norm_text = normalize_text(raw_text)
        
        chapter, category = get_chapter_for_page(page_num)
        doc_page = DocumentPage(
            document_id=document_id,
            source=source,
            page=page_num,
            text=norm_text,
            metadata={
                "chapter": chapter,
                "category": category,
                "char_count": len(norm_text)
            }
        )
        pages.append(doc_page)
    
    return pages
