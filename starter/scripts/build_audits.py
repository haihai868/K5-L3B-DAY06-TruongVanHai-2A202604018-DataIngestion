import json
import os

# 1. Coherence Audit
coherence_data = [
    {
        "pos": 1, "page": 1, "target": "Điều 1: Phạm vi điều chỉnh",
        "score_A": 1, "reason_A": "Cửa sổ 500 ký tự cắt ngang giữa Khoản 2 Điều 1, thiếu phần quy định về đơn vị áp dụng ở Khoản 3.",
        "score_B": 2, "reason_B": "Giữ trọn vẹn toàn bộ Điều 1 với cả 3 khoản trong cùng một khối ngữ cảnh.",
        "score_C": 2, "reason_C": "Cùng chunk với B, giữ trọn vẹn cấu trúc Điều 1."
    },
    {
        "pos": 2, "page": 3, "target": "Điều 4: Hình thức dạy học & định nghĩa tín chỉ",
        "score_A": 1, "reason_A": "Cắt ngang phần giải thích giờ tín chỉ thực hành và tự học.",
        "score_B": 2, "reason_B": "Bao quát trọn vẹn Điều 4 từ Khoản 1 đến Khoản 3.",
        "score_C": 2, "reason_C": "Cùng chunk với B, trọn vẹn ngữ nghĩa."
    },
    {
        "pos": 3, "page": 10, "target": "Điều 11: Cấu trúc chương trình đào tạo",
        "score_A": 1, "reason_A": "Bị cắt đứt ở khối kiến thức giáo dục chuyên nghiệp, mất các định nghĩa phụ.",
        "score_B": 2, "reason_B": "Khối đoạn hoàn chỉnh, nêu đầy đủ cấu trúc khối kiến thức chung và chuyên nghiệp.",
        "score_C": 2, "reason_C": "Giống B, trọn vẹn ý nghĩa."
    },
    {
        "pos": 4, "page": 14, "target": "Điều 17: Thời gian tối đa hoàn thành khóa học",
        "score_A": 1, "reason_A": "Bị chia tách giữa Điều 16 và đầu Điều 17, câu văn bị ngắt đoạn.",
        "score_B": 2, "reason_B": "Tách riêng từng điều khoản độc lập, Điều 17 có đầy đủ chủ thể và thời hạn quy định.",
        "score_C": 2, "reason_C": "Giống B, rõ ràng mạch lạc."
    },
    {
        "pos": 5, "page": 17, "target": "Điều 21: Khối lượng tín chỉ đăng ký học kỳ",
        "score_A": 1, "reason_A": "Bị cắt ở giữa đoạn quy định tín chỉ tối thiểu và tối đa (2/3 và 3/2).",
        "score_B": 2, "reason_B": "Bao trọn vẹn Khoản 1 Điều 21 với đầy đủ cả cận dưới và cận trên.",
        "score_C": 2, "reason_C": "Giống B, câu từ nguyên vẹn."
    },
    {
        "pos": 6, "page": 23, "target": "Điều 26: Học cùng lúc hai chương trình",
        "score_A": 1, "reason_A": "Bị cắt ngang ở điểm c điều kiện điểm số 2.5 và 2.0.",
        "score_B": 2, "reason_B": "Chứa trọn vẹn điều kiện học cùng lúc 2 chương trình đào tạo.",
        "score_C": 2, "reason_C": "Giống B."
    },
    {
        "pos": 7, "page": 31, "target": "Điều 32: Điểm thưởng nghiên cứu khoa học",
        "score_A": 2, "reason_A": "May mắn rơi trọn trong một cửa sổ 500 ký tự.",
        "score_B": 2, "reason_B": "Khối đoạn hoàn chỉnh về mục đích và nguyên tắc tính điểm thưởng NCKH.",
        "score_C": 2, "reason_C": "Giống B."
    },
    {
        "pos": 8, "page": 34, "target": "Điều 34: Trách nhiệm của cố vấn học tập",
        "score_A": 1, "reason_A": "Bị cắt dở giữa điểm a và b về trách nhiệm của giáo viên chủ nhiệm / cố vấn.",
        "score_B": 2, "reason_B": "Khối đoạn chứa đầy đủ các điểm a, b, c, d về trách nhiệm cố vấn học tập.",
        "score_C": 2, "reason_C": "Giống B."
    },
    {
        "pos": 9, "page": 45, "target": "Điều 43: Bảng quy đổi điểm chữ sang thang 4.0",
        "score_A": 1, "reason_A": "Bảng quy đổi bị ngắt giữa chừng, mất các điểm D+, D và F.",
        "score_B": 2, "reason_B": "Bảng điểm quy đổi từ A+ đến F được giữ nguyên vẹn cùng công thức tính GPA.",
        "score_C": 2, "reason_C": "Giống B."
    },
    {
        "pos": 10, "page": 48, "target": "Điều 46: Điều kiện công nhận tốt nghiệp",
        "score_A": 2, "reason_A": "Đoạn liệt kê điều kiện tốt nghiệp nằm trọn trong chunk.",
        "score_B": 2, "reason_B": "Toàn bộ các điều kiện từ a đến h của Điều 46 được bao hàm đầy đủ.",
        "score_C": 2, "reason_C": "Giống B."
    }
]

avg_coherence_A = round(sum(x["score_A"] for x in coherence_data) / len(coherence_data), 2)
avg_coherence_B = round(sum(x["score_B"] for x in coherence_data) / len(coherence_data), 2)
avg_coherence_C = round(sum(x["score_C"] for x in coherence_data) / len(coherence_data), 2)

coherence_summary = {
    "avg_score": {
        "A": avg_coherence_A,
        "B": avg_coherence_B,
        "C": avg_coherence_C
    },
    "details": coherence_data
}

with open("results/coherence_audit.json", "w", encoding="utf-8") as f:
    json.dump(coherence_summary, f, ensure_ascii=False, indent=2)

# 2. Grounding Audit on 5 Test Questions
grounding_data = [
    {
        "qid": "q16", "topic": "Hạ một bậc tốt nghiệp",
        "score_A": 2, "reason_A": "Chunk Top-1 chứa đầy đủ điều kiện kỷ luật và tỷ lệ học lại > 5%.",
        "score_B": 2, "reason_B": "Chunk Top-1 chứa đầy đủ điều kiện hạ bậc tốt nghiệp trọn vẹn.",
        "score_C": 2, "reason_C": "Chunk Top-1 chứa trọn vẹn, và Top-3 100% thuộc Chương VIII loại bỏ hoàn toàn nhiễu."
    },
    {
        "qid": "q17", "topic": "Điểm TBC tích lũy tốt nghiệp",
        "score_A": 1, "reason_A": "Top-1 nói về hạng tốt nghiệp, đến Top-3 mới có mức điểm 2.00 để tốt nghiệp.",
        "score_B": 1, "reason_B": "Top-1 nói về xếp loại bằng, Top-3 mới chứa câu quy định điểm tích lũy 2.00.",
        "score_C": 1, "reason_C": "Top-1 nói về xếp loại bằng, Top-3 chứa câu quy định điểm tích lũy 2.00."
    },
    {
        "qid": "q18", "topic": "Thời hạn hoàn thành chuẩn ngoại ngữ",
        "score_A": 2, "reason_A": "Top-1 chứa đầy đủ quy định thời hạn 3 năm cho sinh viên hoàn thành điều kiện.",
        "score_B": 2, "reason_B": "Top-1 chứa trọn vẹn quy định thời hạn 3 năm kèm đối tượng áp dụng.",
        "score_C": 2, "reason_C": "Top-1 chứa trọn vẹn quy định thời hạn 3 năm kèm đối tượng áp dụng."
    },
    {
        "qid": "q19", "topic": "Số lần cấp bản chính bằng tốt nghiệp",
        "score_A": 2, "reason_A": "Top-1 chứa câu khẳng định bản chính chỉ cấp 1 lần, không cấp lại.",
        "score_B": 2, "reason_B": "Top-1 chứa nguyên vẹn Khoản 4 Điều 47 quy định chỉ cấp 1 lần.",
        "score_C": 2, "reason_C": "Top-1 chứa nguyên vẹn Khoản 4 Điều 47 quy định chỉ cấp 1 lần."
    },
    {
        "qid": "q20", "topic": "Kỳ xét tốt nghiệp định kỳ",
        "score_A": 1, "reason_A": "Top-1 nói về thành phần chủ tịch hội đồng xét tốt nghiệp, Top-3 mới có 4 lần/năm.",
        "score_B": 2, "reason_B": "Top-1 chứa trọn vẹn Khoản 1 Điều 47 với định kỳ 4 lần/năm (tháng 3, 6-7, 9, 12).",
        "score_C": 2, "reason_C": "Top-1 chứa trọn vẹn Khoản 1 Điều 47 với định kỳ 4 lần/năm (tháng 3, 6-7, 9, 12)."
    }
]

avg_grounding_A = round(sum(x["score_A"] for x in grounding_data) / len(grounding_data), 2)
avg_grounding_B = round(sum(x["score_B"] for x in grounding_data) / len(grounding_data), 2)
avg_grounding_C = round(sum(x["score_C"] for x in grounding_data) / len(grounding_data), 2)

grounding_summary = {
    "avg_score": {
        "A": avg_grounding_A,
        "B": avg_grounding_B,
        "C": avg_grounding_C
    },
    "score_distribution": {
        "A": {"0": 0, "1": 2, "2": 3},
        "B": {"0": 0, "1": 1, "2": 4},
        "C": {"0": 0, "1": 1, "2": 4}
    },
    "details": grounding_data
}

with open("results/grounding_audit.json", "w", encoding="utf-8") as f:
    json.dump(grounding_summary, f, ensure_ascii=False, indent=2)

# 3. Metadata Audit
metadata_summary = {
    "records_audited": 15,
    "strategy_A": {
        "valid_metadata_count": "15/15",
        "valid_metadata_rate": 1.0,
        "filter_compliance": "N/A"
    },
    "strategy_B": {
        "valid_metadata_count": "15/15",
        "valid_metadata_rate": 1.0,
        "filter_compliance": "N/A"
    },
    "strategy_C": {
        "valid_metadata_count": "15/15",
        "valid_metadata_rate": 1.0,
        "filter_compliance": "1/1 (100% trên câu có filter q16, cả 3 chunk đều thuộc Chương VIII)"
    }
}

with open("results/metadata_audit.json", "w", encoding="utf-8") as f:
    json.dump(metadata_summary, f, ensure_ascii=False, indent=2)

print("Saved all audit files to results/")

