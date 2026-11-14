import json
from datetime import datetime

with open("starter/data/extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

manifest = {
    "source_id": "vnu_uet_quy_che_3626",
    "title": "Quy chế đào tạo đại học tại Đại học Quốc gia Hà Nội (Ban hành kèm theo Quyết định số 3626/QĐ-ĐHQGHN ngày 21 tháng 10 năm 2022 của Giám đốc Đại học Quốc gia Hà Nội)",
    "source_path_or_url": "https://uet.vnu.edu.vn/wp-content/uploads/2022/12/Quy-ch%E1%BA%BF-%C4%90T%C4%90H-3626.pdf (Official scan) & https://ussh.vnu.edu.vn/vi/van-ban/detail/Quy-che-dao-tao-dai-hoc-tai-Dai-hoc-Quoc-gia-Ha-Noi-Ap-dung-tu-khoa-QH-2022-X-19452/ (Digital selectable text)",
    "license_or_permission": "Công khai (Văn bản quy phạm nội bộ của ĐHQGHN, áp dụng công khai cho cán bộ, giảng viên và sinh viên)",
    "accessed_at": "2026-11-14",
    "effective_date": "2022-10-21 (Áp dụng từ khóa QH-2022-X)",
    "total_pages_physical": 52,
    "total_content_pages": 52,
    "page_counting_rule": "Toàn bộ 52 trang văn bản số hóa đều chứa nội dung quy định pháp lý (9 chương, 51 điều), không có trang bìa hay trang trắng độc lập. Tất cả 52 trang đều hợp lệ tính vào corpus (> 30 trang theo yêu cầu).",
    "total_characters": sum(p["char_count"] for p in pages),
    "pages": [
        {"page_id": p["page"], "char_count": p["char_count"]} for p in pages
    ],
    "structure": {
        "Chương I": {"title": "Những quy định chung", "pages": "1-9", "articles": "Điều 1 - 10", "category": "Quy_dinh_chung"},
        "Chương II": {"title": "Chương trình đào tạo", "pages": "10-13", "articles": "Điều 11 - 15", "category": "Chuong_trinh_dao_tao"},
        "Chương III": {"title": "Kế hoạch và tổ chức đào tạo", "pages": "14-29", "articles": "Điều 16 - 29", "category": "To_chuc_dao_tao"},
        "Chương IV": {"title": "Nghiên cứu khoa học của sinh viên", "pages": "30-31", "articles": "Điều 30 - 32", "category": "Nghien_cuu_khoa_hoc"},
        "Chương V": {"title": "Giảng viên, giáo viên chủ nhiệm, cố vấn học tập", "pages": "32-34", "articles": "Điều 33 - 34", "category": "Giang_vien_Co_van"},
        "Chương VI": {"title": "Nghĩa vụ và quyền lợi của sinh viên", "pages": "35-37", "articles": "Điều 35 - 36", "category": "Quyen_va_nghia_vu_sinh_vien"},
        "Chương VII": {"title": "Kiểm tra, thi và đánh giá kết quả học tập", "pages": "38-46", "articles": "Điều 37 - 44", "category": "Kiem_tra_danh_gia"},
        "Chương VIII": {"title": "Công nhận tốt nghiệp", "pages": "47-49", "articles": "Điều 45 - 47", "category": "Tot_nghiep"},
        "Chương IX": {"title": "Điều khoản thi hành", "pages": "50-52", "articles": "Điều 48 - 51", "category": "Dieu_khoan_thi_hanh"}
    }
}

with open("data/manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("Saved data/manifest.json")

# Export benchmark to markdown
with open("benchmark/benchmark.json", "r", encoding="utf-8") as f:
    b_data = json.load(f)

md_out = ["# Benchmark Dataset: Quy chế đào tạo ĐH ĐHQGHN (3626/QĐ-ĐHQGHN)\n"]
md_out.append(f"**Tổng số câu**: {len(b_data)} (Dev: {sum(1 for x in b_data if x['split']=='dev')}, Test: {sum(1 for x in b_data if x['split']=='test')})\n")
md_out.append("| ID | Split | Câu hỏi | Trang Gold | Metadata Filter | Tóm tắt đáp án |")
md_out.append("|---|---|---|---|---|---|")
for q in b_data:
    flt_str = f"`{json.dumps(q['filter'])}`" if q['filter'] else "None"
    ans_short = q['gold_answer'].replace("\n", " ")
    if len(ans_short) > 60:
        ans_short = ans_short[:57] + "..."
    q_short = q['question'].replace("\n", " ")
    md_out.append(f"| {q['id']} | {q['split']} | {q_short} | Trang {q['gold_page']} | {flt_str} | {ans_short} |")

md_out.append("\n## Chi tiết Gold Evidence từng câu\n")
for q in b_data:
    md_out.append(f"### [{q['id']}] ({q['split'].upper()}) Trang {q['gold_page']}")
    md_out.append(f"- **Câu hỏi**: {q['question']}")
    md_out.append(f"- **Đáp án**: {q['gold_answer']}")
    md_out.append(f"- **Filter**: `{q['filter']}`")
    md_out.append(f"- **Gold Evidence**: > {q['gold_evidence']}\n")

with open("benchmark/benchmark.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_out))

print("Saved benchmark/benchmark.md")

