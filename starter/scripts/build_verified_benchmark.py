import json
import unicodedata
import os

with open("starter/data/extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

# Normalize all pages to NFC
for p in pages:
    p["text"] = unicodedata.normalize("NFC", p["text"])
    p["flat_text"] = " ".join(p["text"].split())

pages_dict = {p["page"]: p for p in pages}

items = [
  (
    "q01", "dev",
    "Một tín chỉ trong chương trình đào tạo được tính tương đương với bao nhiêu giờ tín chỉ?",
    "Một tín chỉ là đại lượng xác định khối lượng kiến thức, kỹ năng mà sinh viên tích lũy được từ học phần trong 15 giờ tín chỉ.",
    3,
    "Tín chỉ là đại lượng xác định khối lượng kiến thức",
    "trong 15 giờ tín chỉ.",
    None
  ),
  (
    "q02", "dev",
    "Thời gian tối đa để sinh viên hoàn thành khoá học đối với mỗi hình thức đào tạo được quy định như thế nào?",
    "Thời gian tối đa để sinh viên hoàn thành khoá học không vượt quá 2 lần thời gian theo kế hoạch học tập chuẩn toàn khoá đối với mỗi hình thức đào tạo.",
    14,
    "Thời gian tối đa để sinh viên hoàn thành khoá học không vượt quá 2",
    "đối với mỗi hình thức đào tạo.",
    None
  ),
  (
    "q03", "dev",
    "Trong mỗi học kỳ chính, khối lượng tín chỉ đăng ký học tối thiểu và tối đa theo kế hoạch học tập chuẩn là bao nhiêu?",
    "Khối lượng đăng ký tối thiểu không ít hơn 2/3 khối lượng trung bình một học kỳ và khối lượng tối đa không vượt quá 3/2 khối lượng trung bình một học kỳ theo kế hoạch học tập chuẩn.",
    17,
    "khối lượng đăng ký tối thiểu không ít hơn 2/3",
    "kế hoạch học tập chuẩn",
    None
  ),
  (
    "q04", "dev",
    "Sinh viên được chấp nhận rút bớt học phần đã đăng ký và được trả lại học phí trong khoảng thời gian nào?",
    "Việc rút bớt học phần chỉ được chấp nhận trong 2 tuần kể từ đầu học kỳ chính, 1 tuần kể từ đầu học kỳ phụ và được trả lại học phí.",
    21,
    "Việc rút bớt học phần chỉ được chấp nhận trong 2 tuần kể từ đầu học kỳ chính,",
    "và được trả lại học phí.",
    {"chapter": "Chương III"}
  ),
  (
    "q05", "dev",
    "Điều kiện về điểm trung bình chung tích lũy để sinh viên được đăng ký học chương trình đào tạo thứ hai là gì?",
    "Điểm trung bình chung tất cả các học phần tính từ đầu khóa học đến thời điểm đăng ký đạt từ 2,5 trở lên (hoặc đạt từ 2,0 trở lên nếu đáp ứng điều kiện trúng tuyển chương trình thứ hai trong năm tuyển sinh).",
    23,
    "Điểm trung bình chung tất cả các học phần tính từ đầu khóa học đến thời điểm đăng ký học chương trình đào tạo thứ hai đạt từ 2,5 trở lên",
    "trong năm tuyển sinh;",
    None
  ),
  (
    "q06", "dev",
    "Sinh viên hoàn thành năm học thứ mấy thì được xem xét chuyển sang học ngành học khác?",
    "Sinh viên hoàn thành năm học thứ nhất được xem xét chuyển sang học một ngành học khác nếu đáp ứng đủ các điều kiện.",
    28,
    "Sinh viên hoàn thành năm học thứ nhất được xem xét chuyển sang học",
    "ngành học khác nếu đáp ứng",
    None
  ),
  (
    "q07", "dev",
    "Điểm thưởng thành tích nghiên cứu khoa học của sinh viên có được dùng để xếp loại học lực hoặc xác định hạng tốt nghiệp không?",
    "Không, điểm thưởng chỉ dùng để làm căn cứ xét học bổng, xét chuyển tiếp vào học ở bậc sau đại học và các quyền lợi khác, không dùng để xếp loại học lực hoặc xác định hạng tốt nghiệp.",
    31,
    "không dùng để xếp loại học lực",
    "xác định hạng tốt nghiệp.",
    None
  ),
  (
    "q08", "dev",
    "Giáo viên chủ nhiệm, cố vấn học tập có trách nhiệm gì đối với kế hoạch học tập của sinh viên?",
    "Nắm vững chương trình đào tạo, hướng dẫn sinh viên xây dựng kế hoạch học tập, lựa chọn đăng ký học phần phù hợp với điều kiện học tập của sinh viên và mục tiêu, yêu cầu của chương trình đào tạo.",
    34,
    "Nắm vững chương trình đào tạo, hướng dẫn sinh viên xây dựng kế hoạch học tập,",
    "yêu cầu của chương trình đào tạo;",
    {"chapter": "Chương V"}
  ),
  (
    "q09", "dev",
    "Đối với các học phần bắt buộc trong chương trình đào tạo, nếu bị điểm F sinh viên phải xử lý thế nào?",
    "Đối với các học phần bắt buộc, nếu bị điểm F, sinh viên phải đăng ký học lại học phần đó.",
    19,
    "Đối với các học phần bắt buộc, nếu bị điểm F,",
    "học lại học phần đó;",
    None
  ),
  (
    "q10", "dev",
    "Theo thang điểm 4, mức điểm chữ B được quy đổi tương ứng với bao nhiêu điểm số?",
    "Mức điểm chữ B tương ứng với 3,0.",
    45,
    "B tương ứng với 3,0",
    "B tương ứng với 3,0",
    None
  ),
  (
    "q11", "dev",
    "Sinh viên bị cảnh báo học vụ khi tổng số tín chỉ của các học phần bị điểm F tồn đọng quá bao nhiêu tín chỉ?",
    "Tổng số tín chỉ của các học phần bị điểm F còn tồn đọng tính từ đầu khoá học đến thời điểm xét đã quá 24 tín chỉ.",
    46,
    "Tổng số tín chỉ của các học phần bị điểm F còn tồn đọng",
    "đã quá 24 tín chỉ",
    None
  ),
  (
    "q12", "dev",
    "Sinh viên không đăng ký học bao nhiêu học kỳ liên tiếp thì bị buộc thôi học?",
    "Không đăng ký học 2 học kỳ liên tiếp.",
    47,
    "Không đăng ký học 2 học kỳ",
    "liên tiếp;",
    None
  ),
  (
    "q13", "dev",
    "Để xếp loại học lực Giỏi sau mỗi học kỳ, điểm trung bình chung học kỳ của sinh viên cần đạt trong khoảng nào?",
    "Giỏi: Điểm trung bình chung học kỳ từ 3,20 đến 3,59.",
    47,
    "Giỏi:",
    "từ 3,20 đến 3,59",
    None
  ),
  (
    "q14", "dev",
    "Học phần khóa luận, đồ án tốt nghiệp có thời lượng quy định cụ thể là bao nhiêu tín chỉ?",
    "Khóa luận, đồ án tốt nghiệp có thời lượng từ 5 đến 10 tín chỉ.",
    4,
    "Khóa luận, đồ án tốt nghiệp là học phần thuộc khối kiến thức bắt buộc,",
    "từ 5 đến 10 tín chỉ",
    None
  ),
  (
    "q15", "dev",
    "Sinh viên vi phạm kỷ luật ở lần thứ mấy vì lý do thi hộ hoặc nhờ người thi hộ thì bị buộc thôi học?",
    "Bị kỷ luật lần thứ hai vì lý do thi hộ hoặc nhờ người thi hộ.",
    47,
    "Bị kỷ luật lần thứ hai vì lý do thi hộ hoặc nhờ người thi hộ",
    "xóa tên khỏi danh sách sinh viên",
    None
  ),
  (
    "q16", "test",
    "Sinh viên có kết quả học tập toàn khóa đạt hạng xuất sắc hoặc giỏi sẽ bị hạ một hạng tốt nghiệp trong những trường hợp nào?",
    "Bị hạ một hạng nếu bị kỷ luật từ mức cảnh cáo trở lên trong thời gian học hoặc khối lượng của các học phần phải học lại vượt quá 5% so với tổng số tín chỉ quy định cho toàn chương trình.",
    49,
    "Những sinh viên có kết quả học tập toàn khóa đạt hạng xuất sắc hoặc giỏi,",
    "quy định cho toàn chương trình.",
    {"chapter": "Chương VIII"}
  ),
  (
    "q17", "test",
    "Điểm trung bình chung tích lũy của khóa học tối thiểu để sinh viên chương trình đào tạo chuẩn được xét công nhận tốt nghiệp là bao nhiêu?",
    "Điểm trung bình chung tích lũy của khóa học đạt từ 2,00 trở lên (đối với chương trình tài năng, chất lượng cao đạt từ 2,50 trở lên).",
    48,
    "Điểm trung bình chung tích lũy của khóa học đạt từ 2,00 trở lên.",
    "đạt từ 2,50 trở lên;",
    None
  ),
  (
    "q18", "test",
    "Sinh viên chưa đạt chuẩn đầu ra ngoại ngữ nhưng đã hết thời gian tối đa được phép học được trở về trường hoàn thành trong thời hạn bao lâu?",
    "Trong thời hạn 3 năm tính từ ngày phải ngừng học, được trở về đơn vị đào tạo hoàn thành các điều kiện còn thiếu và đề nghị xét công nhận tốt nghiệp.",
    49,
    "trong thời hạn 3 năm tính từ ngày phải ngừng học,",
    "đề nghị xét công nhận tốt nghiệp.",
    None
  ),
  (
    "q19", "test",
    "Bản chính bằng tốt nghiệp đại học được cấp bao nhiêu lần?",
    "Bản chính bằng tốt nghiệp chỉ cấp một lần, không cấp lại.",
    49,
    "Bản chính bằng tốt nghiệp chỉ cấp một lần,",
    "không cấp lại.",
    None
  ),
  (
    "q20", "test",
    "Hội đồng xét tốt nghiệp cho sinh viên hoàn thành chương trình đào tạo được tổ chức định kỳ mỗi năm mấy lần và vào những tháng nào?",
    "Định kỳ mỗi năm 4 lần, vào các tháng 3, tháng 6 và tháng 7, tháng 9, tháng 12.",
    48,
    "Định kỳ mỗi năm 4 lần (tháng 3, tháng 6 và tháng 7, tháng 9,",
    "hoàn thành chương trình đào tạo",
    None
  )
]

verified_list = []
for qid, split, question, answer, page_num, key_start, key_end, flt in items:
    p_obj = pages_dict[page_num]
    flat = p_obj["flat_text"]
    flat_start = " ".join(unicodedata.normalize("NFC", key_start).split())
    flat_end = " ".join(unicodedata.normalize("NFC", key_end).split())
    
    idx_s = flat.find(flat_start)
    if idx_s == -1:
        print(f"FAILED start on {qid} (Page {page_num}): {flat_start}")
        continue
    idx_e = flat.find(flat_end, idx_s)
    if idx_e == -1:
        print(f"FAILED end on {qid} (Page {page_num}): {flat_end}")
        continue
    
    exact_evidence = flat[idx_s:idx_e + len(flat_end)]
    verified_list.append({
        "id": qid,
        "split": split,
        "question": question,
        "gold_answer": answer,
        "gold_source": "Quy-che-3626-digital.pdf",
        "gold_page": page_num,
        "gold_evidence": exact_evidence,
        "filter": flt
    })
    print(f"[{qid}] Verified: {exact_evidence[:60]}... ({len(exact_evidence)} chars)")

print(f"\nTotal verified: {len(verified_list)} / {len(items)}")
if len(verified_list) == 20:
    os.makedirs("benchmark", exist_ok=True)
    with open("benchmark/benchmark.json", "w", encoding="utf-8") as f:
        json.dump(verified_list, f, ensure_ascii=False, indent=2)
    print("SUCCESS: Saved benchmark/benchmark.json with 20 questions!")
