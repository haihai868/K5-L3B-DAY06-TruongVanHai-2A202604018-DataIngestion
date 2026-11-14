import json

with open("starter/data/extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

pages_dict = {p["page"]: p["text"] for p in pages}

# 10 locations:
locs = [
    {"pos": 1, "page": 1, "name": "Điều 1: Phạm vi điều chỉnh và đối tượng áp dụng"},
    {"pos": 2, "page": 3, "name": "Điều 4: Hình thức dạy học, tín chỉ, giờ tín chỉ"},
    {"pos": 3, "page": 10, "name": "Điều 11: Cấu trúc chương trình đào tạo"},
    {"pos": 4, "page": 14, "name": "Điều 17: Khóa học và thời gian tối đa"},
    {"pos": 5, "page": 17, "name": "Điều 21: Tổ chức đăng ký học phần"},
    {"pos": 6, "page": 23, "name": "Điều 26: Học cùng lúc 2 chương trình (bằng kép)"},
    {"pos": 7, "page": 31, "name": "Điều 32: Điểm thưởng NCKH sinh viên"},
    {"pos": 8, "page": 34, "name": "Điều 34: Cố vấn học tập, GV chủ nhiệm"},
    {"pos": 9, "page": 45, "name": "Điều 43: Bảng quy đổi thang điểm chữ sang số 4.0"},
    {"pos": 10, "page": 48, "name": "Điều 46: Điều kiện công nhận tốt nghiệp"}
]

from starter.src.chunking import fixed_size, by_paragraph
from starter.src.models import DocumentPage

print("=== EVALUATING CHUNK COHERENCE FOR 10 LOCATIONS ===")
coherence_audit = []
for loc in locs:
    p_num = loc["page"]
    raw_txt = pages_dict[p_num]
    d_page = DocumentPage("vnu_uet_quy_che_3626", "Quy-che-3626-digital.pdf", p_num, raw_txt, {"page": p_num})
    
    cA = fixed_size(d_page, size=500, overlap=50)
    cB = by_paragraph(d_page, max_size=800)
    
    # Pick the chunk that contains the main topic
    chunk_A = cA[0].text if cA else ""
    chunk_B = cB[0].text if cB else ""
    
    # Audit scoring:
    # 0 = cắt ngang giữa ý / thiếu chủ thể không hiểu được
    # 1 = hiểu được một phần, thiếu ngữ cảnh
    # 2 = tự hiểu trọn vẹn, giữ trọn ý ngữ nghĩa
    
    coherence_audit.append({
        "pos": loc["pos"],
        "page": p_num,
        "name": loc["name"],
        "chunk_A_sample": chunk_A[:100] + "...",
        "chunk_B_sample": chunk_B[:100] + "..."
    })

print(json.dumps(coherence_audit, ensure_ascii=False, indent=2))

