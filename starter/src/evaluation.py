"""Evaluate retrieved evidence and compute Hit@1, Hit@3, and summary metrics."""
from typing import Any
import unicodedata


def is_chunk_hit(gold_page: int, gold_evidence: str, hit: dict[str, Any]) -> bool:
    """A chunk is a HIT if it matches the gold page and contains the gold evidence."""
    hit_page = hit.get("metadata", {}).get("page")
    if hit_page != gold_page:
        return False
        
    chunk_text = hit.get("text", "")
    norm_chunk = " ".join(unicodedata.normalize("NFC", chunk_text).split())
    norm_gold = " ".join(unicodedata.normalize("NFC", gold_evidence).split())
    
    # Check if exact evidence or a significant portion (first 50 chars) is in chunk
    if norm_gold in norm_chunk:
        return True
    
    # In case gold evidence is slightly longer than chunk or split at boundary
    if len(norm_gold) > 60:
        sub_gold = norm_gold[:60]
        if sub_gold in norm_chunk:
            return True
            
    return False


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    """Check source/page and gold evidence match for top-3 hits, recording hit@1 and hit@3."""
    gold_page = question["gold_page"]
    gold_evidence = question["gold_evidence"]
    
    hit_details = []
    has_hit_at_1 = False
    has_hit_at_3 = False
    
    for rank, h in enumerate(hits, start=1):
        is_hit = is_chunk_hit(gold_page, gold_evidence, h)
        if rank == 1 and is_hit:
            has_hit_at_1 = True
        if is_hit:
            has_hit_at_3 = True
            
        hit_details.append({
            "rank": rank,
            "chunk_id": h.get("chunk_id"),
            "score": h.get("score"),
            "page": h.get("metadata", {}).get("page"),
            "is_hit": is_hit,
            "metadata": h.get("metadata"),
            "text_snippet": h.get("text", "")[:120] + "..."
        })
        
    return {
        "question_id": question["id"],
        "split": question["split"],
        "question": question["question"],
        "gold_page": gold_page,
        "gold_evidence": gold_evidence,
        "filter": question.get("filter"),
        "hit_at_1": has_hit_at_1,
        "hit_at_3": has_hit_at_3,
        "hits": hit_details
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate Hit@1 and Evidence Hit@3 by split (dev / test)."""
    dev_traces = [t for t in traces if t["split"] == "dev"]
    test_traces = [t for t in traces if t["split"] == "test"]
    
    def calc_split_metrics(sub_traces: list[dict[str, Any]]) -> dict[str, Any]:
        total = len(sub_traces)
        if total == 0:
            return {"total": 0, "hit1_count": 0, "hit1_rate": 0.0, "hit3_count": 0, "hit3_rate": 0.0}
        h1 = sum(1 for t in sub_traces if t["hit_at_1"])
        h3 = sum(1 for t in sub_traces if t["hit_at_3"])
        return {
            "total": total,
            "hit1_count": h1,
            "hit1_rate": round(h1 / total, 4),
            "hit3_count": h3,
            "hit3_rate": round(h3 / total, 4)
        }
        
    return {
        "overall": calc_split_metrics(traces),
        "dev": calc_split_metrics(dev_traces),
        "test": calc_split_metrics(test_traces)
    }
