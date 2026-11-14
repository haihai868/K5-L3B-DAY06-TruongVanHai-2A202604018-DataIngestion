import json

benchmark_questions = [
  {
    "id": "q01",
    "split": "dev",
    "question": "Một tín chỉ trong chương trình đào tạo được tính tương đương với bao nhiêu giờ tín chỉ?",
    "gold_answer": "Một tín chỉ là đại lượng xác định khối lượng kiến thức, kỹ năng mà sinh viên tích lũy được từ học phần trong 15 giờ tín chỉ.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 3,
    "gold_evidence": "Tín chỉ là đại lượng xác định khối lượng kiến thức, kỹ năng mà sinh viên tích lũy được từ học phần trong 15 giờ tín chỉ.",
    "filter": None
  },
  {
    "id": "q02",
    "split": "dev",
    "question": "Thời gian tối đa để sinh viên hoàn thành khoá học đối với mỗi hình thức đào tạo được quy định như thế nào?",
    "gold_answer": "Thời gian tối đa để sinh viên hoàn thành khoá học không vượt quá 2 lần thời gian theo kế hoạch học tập chuẩn toàn khoá.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 14,
    "gold_evidence": "Thời gian tối đa để sinh viên hoàn thành khoá học không vượt quá 2 lần thời gian theo kế hoạch học tập chuẩn toàn khoá đối với mỗi hình thức đào tạo.",
    "filter": None
  },
  {
    "id": "q03",
    "split": "dev",
    "question": "Trong mỗi học kỳ chính, khối lượng tín chỉ đăng ký học tối thiểu và tối đa theo kế hoạch học tập chuẩn là bao nhiêu?",
    "gold_answer": "Khối lượng đăng ký tối thiểu không ít hơn 2/3 và tối đa không vượt quá 3/2 khối lượng trung bình một học kỳ theo kế hoạch học tập chuẩn.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 17,
    "gold_evidence": "khối lượng đăng ký tối thiểu không ít hơn 2/3 khối lượng trung bình một học kỳ theo kế hoạch học tập chuẩn; khối lượng tối đa không vượt quá 3/2 khối lượng trung bình một học kỳ the o kế hoạch học tập chuẩn",
    "filter": None
  },
  {
    "id": "q04",
    "split": "dev",
    "question": "Sinh viên được chấp nhận rút bớt học phần đã đăng ký và được trả lại học phí trong khoảng thời gian nào?",
    "gold_answer": "Việc rút bớt học phần chỉ được chấp nhận trong 2 tuần kể từ đầu học kỳ chính, 1 tuần kể từ đầu học kỳ phụ và được trả lại học phí.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 21,
    "gold_evidence": "Việc rút bớt học phần chỉ được chấp nhận trong 2 tuần kể từ đầu học kỳ chính, 1 tuần kể từ đầu học kỳ phụ và được trả lại học phí.",
    "filter": {"chapter": "Chương III"}
  },
  {
    "id": "q05",
    "split": "dev",
    "question": "Điều kiện về điểm trung bình chung tích lũy để sinh viên được đăng ký học chương trình đào tạo thứ hai là gì?",
    "gold_answer": "Điểm trung bình chung tất cả các học phần tính từ đầu khóa học đạt từ 2,5 trở lên (và đáp ứng ngưỡng đảm bảo chất lượng đầu vào), hoặc đạt từ 2,0 trở lên (và đáp ứng điều kiện trúng tuyển chương trình thứ hai trong năm tuyển sinh).",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 23,
    "gold_evidence": "học lực tính theo điểm trung bình chung tất cả các học phần tính từ đầu khóa học đến thời điểm đăng ký học chương trình đào tạo thứ hai đạt từ 2,5 trở lên",
    "filter": None
  },
  {
    "id": "q06",
    "split": "dev",
    "question": "Sinh viên hoàn thành năm học thứ mấy thì được xem xét chuyển sang học ngành học khác?",
    "gold_answer": "Sinh viên hoàn thành năm học thứ nhất được xem xét chuyển sang học một ngành học khác nếu đáp ứng đủ các điều kiện.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 28,
    "gold_evidence": "Sinh viên hoàn thành năm học thứ nhất được xem xét chuyển sang học một        ngành học khác nếu đáp ứng đầy đủ các điều kiện sau:",
    "filter": None
  },
  {
    "id": "q07",
    "split": "dev",
    "question": "Điểm thưởng thành tích nghiên cứu khoa học của sinh viên có được dùng để xếp loại học lực hoặc xác định hạng tốt nghiệp không?",
    "gold_answer": "Không, điểm thưởng chỉ dùng để làm căn cứ xét học bổng, xét chuyển tiếp vào học ở bậc sau đại học và các quyền lợi khác, không dùng để xếp loại học lực hoặc xác định hạng tốt nghiệp.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 31,
    "gold_evidence": "không dùng để xếp loại học lực hoặc xác định hạng tốt nghiệp.",
    "filter": None
  },
  {
    "id": "q08",
    "split": "dev",
    "question": "Giáo viên chủ nhiệm, cố vấn học tập có trách nhiệm gì đối với kế hoạch học tập của sinh viên?",
    "gold_answer": "Nắm vững chương trình đào tạo, hướng dẫn sinh viên xây dựng kế hoạch học tập, lựa chọn đăng ký học phần phù hợp với năng lực, nguyện vọng và điều kiện của từng sinh viên.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 34,
    "gold_evidence": "Nắm vững chương trình đào tạo, hướng dẫn sinh viên xây dựng kế hoạch học tập, lựa chọn đăng ký học phần phù hợp với năng lực, nguyện vọng và điều kiện của từng sinh viên;",
    "filter": {"chapter": "Chương V"}
  },
  {
    "id": "q09",
    "split": "dev",
    "question": "Đối với các học phần bắt buộc trong chương trình đào tạo, nếu bị điểm F sinh viên phải xử lý thế nào?",
    "gold_answer": "Đối với các học phần bắt buộc, nếu bị điểm F, sinh viên phải đăng ký học lại học phần đó.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 19,
    "gold_evidence": "Đối với các học phần bắt buộc, nếu bị điểm F, sinh viên phải đăng ký học lại học phần đó;",
    "filter": None
  },
  {
    "id": "q10",
    "split": "dev",
    "question": "Theo thang điểm 4, mức điểm chữ B được quy đổi tương ứng với bao nhiêu điểm số?",
    "gold_answer": "Mức điểm chữ B tương ứng với 3,0.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 45,
    "gold_evidence": "B  tương ứng với  3,0",
    "filter": None
  },
  {
    "id": "q11",
    "split": "dev",
    "question": "Sinh viên bị cảnh báo học vụ khi tổng số tín chỉ của các học phần bị điểm F tồn đọng quá bao nhiêu tín chỉ?",
    "gold_answer": "Tổng số tín chỉ của các học phần bị điểm F còn tồn đọng tính từ đầu khoá học đến thời điểm xét đã quá 24 tín chỉ.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 46,
    "gold_evidence": "Tổng số tín chỉ của các học phần bị điểm F còn tồn đọng tính từ đầu khoá học đến thời điểm xét đã quá 24 tín chỉ",
    "filter": None
  },
  {
    "id": "q12",
    "split": "dev",
    "question": "Sinh viên không đăng ký học bao nhiêu học kỳ liên tiếp thì bị buộc thôi học?",
    "gold_answer": "Không đăng ký học 2 học kỳ liên tiếp.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 47,
    "gold_evidence": "Không đăng ký học 2 học kỳ liên tiếp;",
    "filter": None
  },
  {
    "id": "q13",
    "split": "dev",
    "question": "Để xếp loại học lực Giỏi sau mỗi học kỳ, điểm trung bình chung học kỳ của sinh viên cần đạt trong khoảng nào?",
    "gold_answer": "Giỏi: Điểm trung bình chung học kỳ từ 3,20 đến 3,59.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 47,
    "gold_evidence": "Giỏi:   Điểm trung bình chung học kỳ từ 3,20 đến 3,59",
    "filter": None
  },
  {
    "id": "q14",
    "split": "dev",
    "question": "Học phần khóa luận, đồ án tốt nghiệp có thời lượng quy định cụ thể là bao nhiêu tín chỉ?",
    "gold_answer": "Khóa luận, đồ án tốt nghiệp có thời lượng từ 5 đến 10 tín chỉ.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 4,
    "gold_evidence": "Khóa luận, đồ án tốt nghiệp là học phần thuộc khối kiến thức bắt buộc, có thời lượng từ 5 đến 10 tín chỉ được quy định cụ thể trong chương trình đào tạo;",
    "filter": None
  },
  {
    "id": "q15",
    "split": "dev",
    "question": "Sinh viên vi phạm kỷ luật ở lần thứ mấy vì lý do thi hộ hoặc nhờ người thi hộ thì bị buộc thôi học?",
    "gold_answer": "Bị kỷ luật lần thứ hai vì lý do thi hộ hoặc nhờ người thi hộ.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 47,
    "gold_evidence": "Bị kỷ luật lần thứ hai vì lý do thi hộ hoặc nhờ người thi hộ theo quy định tại điểm d, khoản 4, Điều 35 của Quy chế này",
    "filter": None
  },
  {
    "id": "q16",
    "split": "test",
    "question": "Sinh viên có kết quả học tập toàn khóa đạt hạng xuất sắc hoặc giỏi sẽ bị hạ một hạng tốt nghiệp trong những trường hợp nào?",
    "gold_answer": "Bị hạ một hạng nếu bị kỷ luật từ mức cảnh cáo trở lên trong thời gian học hoặc khối lượng của các học phần phải học lại vượt quá 5% so với tổng số tín chỉ quy định cho toàn chương trình.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 49,
    "gold_evidence": "Những sinh viên có kết quả học tập toàn khóa đạt hạng xuất sắc hoặc giỏi, hạng tốt nghiệp sẽ bị hạ một hạng nếu bị kỷ luật từ mức cảnh cáo trở lên trong thời gian học hoặc khối lượng của các học phần phải học lại vượt quá 5% so với tổng số tín chỉ quy định cho toàn chương trình.",
    "filter": {"chapter": "Chương VIII"}
  },
  {
    "id": "q17",
    "split": "test",
    "question": "Điểm trung bình chung tích lũy của khóa học tối thiểu để sinh viên chương trình đào tạo chuẩn được xét công nhận tốt nghiệp là bao nhiêu?",
    "gold_answer": "Điểm trung bình chung tích lũy của khóa học đạt từ 2,00 trở lên (đối với chương trình tài năng, chất lượng cao đạt từ 2,50 trở lên).",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 48,
    "gold_evidence": "Điểm trung bình chung tích lũy của khóa học đạt từ 2,00 trở lên. Đối với chương trình đào tạo tài năng, chất lượng cao đạt từ  2,50 trở lên;",
    "filter": None
  },
  {
    "id": "q18",
    "split": "test",
    "question": "Sinh viên chưa đạt chuẩn đầu ra ngoại ngữ nhưng đã hết thời gian tối đa được phép học được trở về trường hoàn thành trong thời hạn bao lâu?",
    "gold_answer": "Trong thời hạn 3 năm tính từ ngày phải ngừng học, được trở về đơn vị đào tạo hoàn thành các điều kiện còn thiếu và đề nghị xét công nhận tốt nghiệp.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 49,
    "gold_evidence": "trong thời hạn 3 năm tính từ ngày phải ngừng học, được trở về đơn vị đào tạo hoàn thành các điều kiện còn thiếu và đề nghị xét công nhận tốt nghiệp.",
    "filter": None
  },
  {
    "id": "q19",
    "split": "test",
    "question": "Bản chính bằng tốt nghiệp đại học được cấp bao nhiêu lần?",
    "gold_answer": "Bản chính bằng tốt nghiệp chỉ cấp một lần, không cấp lại.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 49,
    "gold_evidence": "Bản chính bằng tốt nghiệp chỉ cấp một lần, không cấp lại.",
    "filter": None
  },
  {
    "id": "q20",
    "split": "test",
    "question": "Hội đồng xét tốt nghiệp cho sinh viên hoàn thành chương trình đào tạo được tổ chức định kỳ mỗi năm mấy lần và vào những tháng nào?",
    "gold_answer": "Định kỳ mỗi năm 4 lần, vào các tháng 3, tháng 6 và tháng 7, tháng 9, tháng 12.",
    "gold_source": "Quy-che-3626-digital.pdf",
    "gold_page": 48,
    "gold_evidence": "Định kỳ mỗi năm 4 lần (tháng 3, tháng 6 và tháng 7, tháng 9,  tháng 12), thủ trưởng đơn vị đào tạo ra quyết định thành lập Hội đồng xét tốt nghiệp cho sinh viên đã hoàn thành chương trình đào tạo c ủa đơn vị.",
    "filter": None
  }
]

with open("starter/data/extracted_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)
pages_dict = {p["page"]: p["text"] for p in pages}

all_passed = True
for q in benchmark_questions:
    page_num = q["gold_page"]
    page_text = pages_dict.get(page_num, "")
    evidence = q["gold_evidence"]
    if evidence in page_text:
        print(f"[{q['id']}] PASS: verified on Page {page_num}")
    else:
        print(f"[{q['id']}] FAIL: evidence NOT found in Page {page_num}!")
        all_passed = False

if all_passed:
    print("\nALL 20 BENCHMARK QUESTIONS VERIFIED SUCCESSFULLY 100%!")
    import os
    os.makedirs("benchmark", exist_ok=True)
    with open("benchmark/benchmark.json", "w", encoding="utf-8") as f:
        json.dump(benchmark_questions, f, ensure_ascii=False, indent=2)
    print("Saved to benchmark/benchmark.json")

