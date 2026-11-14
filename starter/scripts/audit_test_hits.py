import json

# 1. Inspect chunks at the 10 fixed locations for Strategy A and Strategy B
# Locations:
# Pos 1: Trang 1 (Điều 1: Phạm vi điều chỉnh)
# Pos 2: Trang 3 (Điều 4: Hình thức dạy học, tín chỉ, giờ tín chỉ)
# Pos 3: Trang 10 (Điều 11: Cấu trúc chương trình đào tạo)
# Pos 4: Trang 14 (Điều 17: Khóa học và thời gian tối đa)
# Pos 5: Trang 17 (Điều 21: Tổ chức đăng ký học phần)
# Pos 6: Trang 23 (Điều 26: Học cùng lúc 2 chương trình)
# Pos 7: Trang 31 (Điều 32: Điểm thưởng NCKH)
# Pos 8: Trang 34 (Điều 34: Cố vấn học tập)
# Pos 9: Trang 45 (Điều 43: Thang điểm quy đổi 4.0)
# Pos 10: Trang 48 (Điều 46: Điều kiện tốt nghiệp)

target_pages = [1, 3, 10, 14, 17, 23, 31, 34, 45, 48]

with open("results/trace_strategy_A.json", "r", encoding="utf-8") as f:
    trace_A = json.load(f)
with open("results/trace_strategy_B.json", "r", encoding="utf-8") as f:
    trace_B = json.load(f)
with open("results/trace_strategy_C.json", "r", encoding="utf-8") as f:
    trace_C = json.load(f)

print("=== TEST QUESTIONS HITS (q16 - q20) ===")
for qid in ["q16", "q17", "q18", "q19", "q20"]:
    item_A = next(t for t in trace_A if t["question_id"] == qid)
    item_B = next(t for t in trace_B if t["question_id"] == qid)
    item_C = next(t for t in trace_C if t["question_id"] == qid)
    print(f"\n--- {qid}: {item_A['question']} (Gold Page: {item_A['gold_page']}) ---")
    print(f"Strategy A: Top-1 hit? {item_A['hit_at_1']}, Top-3 hit? {item_A['hit_at_3']}")
    for h in item_A["hits"]:
        print(f"  [A Rank {h['rank']}] Page {h['page']} (Hit: {h['is_hit']}): {h['text_snippet'][:80]}")
    print(f"Strategy B: Top-1 hit? {item_B['hit_at_1']}, Top-3 hit? {item_B['hit_at_3']}")
    for h in item_B["hits"]:
        print(f"  [B Rank {h['rank']}] Page {h['page']} (Hit: {h['is_hit']}): {h['text_snippet'][:80]}")
    print(f"Strategy C: Top-1 hit? {item_C['hit_at_1']}, Top-3 hit? {item_C['hit_at_3']}")
    for h in item_C["hits"]:
        print(f"  [C Rank {h['rank']}] Page {h['page']} (Hit: {h['is_hit']}): {h['text_snippet'][:80]}")

