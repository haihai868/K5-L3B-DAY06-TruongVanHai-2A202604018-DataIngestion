# Báo cáo cá nhân — Day 6

## Dữ liệu và pipeline
- **Chủ đề, nguồn/quyền, số trang và quy tắc tính trang**:
  - Chủ đề: Quy chế đào tạo đại học tại Đại học Quốc gia Hà Nội ban hành kèm theo Quyết định số 3626/QĐ-ĐHQGHN ngày 21 tháng 10 năm 2022 của Giám đốc ĐHQGHN.
  - Nguồn & quyền: Công khai chính thức trên Cổng thông tin Đào tạo UET - ĐHQGHN ([uet.vnu.edu.vn](https://uet.vnu.edu.vn/wp-content/uploads/2022/12/Quy-ch%E1%BA%BF-%C4%90T%C4%90H-3626.pdf)) và Cổng văn bản USSH - ĐHQGHN ([ussh.vnu.edu.vn](https://ussh.vnu.edu.vn/vi/van-ban/detail/Quy-che-dao-tao-dai-hoc-tai-Dai-hoc-Quoc-gia-Ha-Noi-Ap-dung-tu-khoa-QH-2022-X-19452/)). Văn bản quy phạm nội bộ có giá trị áp dụng công khai cho sinh viên, giảng viên và các đơn vị đào tạo trực thuộc.
  - Số trang & quy tắc tính trang: Tổng số 52 trang vật lý, 52 trang nội dung hữu ích (9 chương, 51 điều, 95.029 ký tự). Quy tắc tính: Văn bản là quyết định quy chế được số hóa liên tục, không có trang bìa hay phụ lục riêng; 100% các trang đều chứa các điều khoản pháp lý quy định trực tiếp về đào tạo nên đều được tính hợp lệ (> 30 trang theo yêu cầu).
- **Chuẩn hóa, lỗi và giới hạn**:
  - Sử dụng thư viện `pypdf` đọc trích xuất văn bản số hóa, áp dụng `unicodedata.normalize("NFC")` để đồng nhất dấu tiếng Việt.
  - Xóa bỏ ký tự điều khiển lạ, chuẩn hóa các khoảng trắng thừa, giữ lại ngắt dòng tự nhiên và ranh giới đoạn văn `\n\n`.
  - Lỗi phát hiện: File gốc trên website UET là file scan ảnh (19MB, không có text layer); giải pháp khắc phục là sử dụng bản số hóa văn bản chính thức của ĐHQGHN có text layer selectable (`starter/data/Quy-che-3626-digital.pdf`), đảm bảo không có trang bị mất chữ hay lỗi OCR.
- **Embedding model/provider/version/số chiều, vector store/version, metric, lệnh chạy và chi phí**:
  - Embedding Model: `paraphrase-multilingual-MiniLM-L12-v2` qua `sentence-transformers 6.3.0`, 384 dimensions, chạy offline cục bộ trên CPU.
  - Vector Store: `ChromaDB 1.5.8` (sử dụng `PersistentClient` tại `starter/data/chroma_db`).
  - Metric tìm kiếm: Cosine similarity (`hnsw:space: cosine`).
  - Lệnh chạy: `python -m starter.src.run`.
  - Chi phí: 0.00 USD (chạy hoàn toàn local, không phát sinh chi phí API).
- **Metadata bắt buộc, trường lọc bổ sung, nguồn giá trị và lý do chọn**:
  - Metadata bắt buộc: `document_id` ("vnu_uet_quy_che_3626"), `source` ("Quy-che-3626-digital.pdf"), `page` (1 đến 52).
  - Trường lọc bổ sung: `chapter` ("Chương I" đến "Chương IX") và `category` (phân loại chủ đề tương ứng). Nguồn giá trị được ánh xạ chính xác từ mục lục phân chia cấu trúc 9 chương của quy chế.
  - Lý do chọn: Văn bản quy chế có các từ khóa trùng lặp giữa các chương (ví dụ: điều kiện học phần ở Chương III vs điều kiện tốt nghiệp ở Chương VIII). Trường `chapter` giúp thu hẹp không gian tìm kiếm, loại trừ các điều khoản gây nhiễu ngoài phạm vi câu hỏi.

## Cấu hình và benchmark
- **A / B / C (tham số cụ thể, khác biệt duy nhất B–C)**:
  - Strategy A: Cắt theo kích thước cố định (Fixed-size: `size = 500`, `overlap = 50` ký tự), lưu metadata `source`, `page`, `chapter`. Không áp dụng filter khi tìm kiếm. Tổng số: 225 chunks.
  - Strategy B: Cắt theo cấu trúc đoạn văn / điều khoản (Paragraph-based: nhóm đoạn tự nhiên `max_size = 800` ký tự, `overlap = 0`), giữ nguyên metadata như A. Không áp dụng filter khi tìm kiếm. Tổng số: 195 chunks.
  - Strategy C: Sử dụng cùng tập chunk và index vector như Strategy B (195 chunks). Điểm khác biệt duy nhất: Bật tính năng Metadata Filtering theo `chapter` khi câu hỏi có cung cấp điều kiện lọc.
- **≥20 câu: phân chia ≥15 dev / ≥5 test, câu metadata filter và cách kiểm chứng evidence**:
  - Bộ câu hỏi gồm 20 câu: 15 câu Dev (`q01`–`q15`) và 5 câu Test (`q16`–`q20`).
  - Có 3 câu kiểm tra metadata filter: `q04` (Dev - Chương III), `q08` (Dev - Chương V), `q16` (Test - Chương VIII).
  - Kiểm chứng evidence: 100% bằng chứng (`gold_evidence`) được trích nguyên văn từ bản text sau chuẩn hóa tại đúng `gold_page`, đã được script tự động xác thực đối chiếu chính xác từng ký tự.
- **Tiêu chí chọn chiến lược đã chốt trước khi xem test**:
  - Tiêu chí 1: Retrieval Accuracy (ưu tiên Hit@3, sau đó Hit@1) trên tập Dev.
  - Tiêu chí 2: Chunk Coherence (tính mạch lạc của chunk ngữ nghĩa /2).
  - Tiêu chí 3: Khả năng loại bỏ kết quả gây nhiễu của Metadata Filtering và Grounding quality.
  - Tiêu chí 4: Hiệu quả tài nguyên (số lượng chunk và thời gian xử lý).

## Kết quả
| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Thời gian | Chi phí |
|---|---|---|---|---|---|---|
| A | dev | 6/15 (40.0%) | 9/15 (60.0%) | 225 | 30.66s | 0.00$ |
| A | test | 3/5 (60.0%) | 5/5 (100.0%) | 225 | 30.66s | 0.00$ |
| B | dev | 8/15 (53.3%) | 11/15 (73.3%) | 195 | 40.59s | 0.00$ |
| B | test | 4/5 (80.0%) | 5/5 (100.0%) | 195 | 40.59s | 0.00$ |
| C | dev | 8/15 (53.3%) | 11/15 (73.3%) | 195 | 40.59s | 0.00$ |
| C | test | 4/5 (80.0%) | 5/5 (100.0%) | 195 | 40.59s | 0.00$ |

| Strategy | Coherence trung bình /2 (n) | Metadata đủ và đúng (n/N) | Filter tuân thủ (n/N hoặc N/A) | Grounding 0/1/2 (số câu) và trung bình /2 |
|---|---|---|---|---|
| A | 1.20 (10 vị trí) | 15/15 (100%) | N/A | 0: 0, 1: 2, 2: 3 (TB: 1.60/2) |
| B | 2.00 (10 vị trí) | 15/15 (100%) | N/A | 0: 0, 1: 1, 2: 4 (TB: 1.80/2) |
| C | 2.00 (10 vị trí) | 15/15 (100%) | 1/1 (100%) | 0: 0, 1: 1, 2: 4 (TB: 1.80/2) |

**Đường dẫn trace, nhãn thủ công và cách chọn mẫu**:
- Trace files: [results/trace_strategy_A.json](../../results/trace_strategy_A.json), [results/trace_strategy_B.json](../../results/trace_strategy_B.json), [results/trace_strategy_C.json](../../results/trace_strategy_C.json).
- Tóm tắt metrics: [results/summary_metrics.json](../../results/summary_metrics.json).
- Nhật ký thực nghiệm: [artifacts/experiment_log.csv](../../artifacts/experiment_log.csv).
- Nhãn thủ công Coherence (10 vị trí nguồn tại các Điều 1, 4, 11, 17, 21, 26, 32, 34, 43, 46): [results/coherence_audit.json](../../results/coherence_audit.json).
- Nhãn thủ công Grounding & Metadata (5 câu test `q16`–`q20`): [results/grounding_audit.json](../../results/grounding_audit.json), [results/metadata_audit.json](../../results/metadata_audit.json).

## Phân tích và kết luận
- **So sánh A–B và B–C; 2 ví dụ sai có ID câu và nguồn**:
  - *So sánh A–B (Tác động của Chunking)*: Strategy B vượt trội rõ rệt so với A trên cả Dev và Test. Dev Hit@3 tăng từ 60.0% (9/15) lên 73.3% (11/15), Dev Hit@1 tăng từ 40.0% lên 53.3%. Test Hit@1 tăng từ 60.0% (3/5) lên 80.0% (4/5). Điểm Coherence tăng từ 1.20 lên 2.00 tuyệt đối do Strategy B giữ trọn vẹn ngữ cảnh từng điều khoản quy chế, tránh hiện tượng câu từ bị xé lẻ giữa chừng của fixed-size window.
  - *So sánh B–C (Tác động của Metadata Filter)*: Strategy C giữ nguyên accuracy cao của B nhưng cải thiện độ sạch ngữ cảnh. Tại câu test `q16` (hỏi về hạ một bậc tốt nghiệp, có filter `Chương VIII`), Strategy B đưa 1 chunk ngoại lai từ Trang 27 (Chương III - Kế hoạch đào tạo) vào Top 2, trong khi Strategy C với metadata filter đã loại bỏ hoàn toàn các điều khoản không liên quan, giúp 100% cả 3/3 chunk trả về đều thuộc Trang 49 (Chương VIII).
  - *Ví dụ sai 1 (`q01`, Dev, Trang 3)*: Câu hỏi định nghĩa "Một tín chỉ tương đương bao nhiêu giờ tín chỉ?". Strategy A thất bại ở Top-1 do cửa sổ 500 ký tự cắt đúng ranh giới Khoản 2 Điều 4, làm đứt đoạn liên kết giữa "tín chỉ" và "15 giờ tín chỉ", khiến embedding trả về nhầm đoạn thực hành ở trang 4. Strategy B xử lý trọn vẹn Điều 4 nên đạt Top-1 hit chính xác.
  - *Ví dụ sai 2 (`q17`, Test, Trang 48)*: Câu hỏi "Điểm trung bình chung tích lũy tối thiểu để tốt nghiệp?". Cả 3 chiến lược đều xếp đoạn xếp hạng tốt nghiệp (Trang 49) lên Rank 1 và Rank 2, trong khi quy định điều kiện tốt nghiệp $\ge 2.00$ (Trang 48 Điều 46) chỉ xuất hiện ở Rank 3. Nguyên nhân là từ khóa "điểm trung bình chung tích lũy" xuất hiện với tần suất dày đặc hơn ở bảng phân hạng Xuất sắc/Giỏi/Khá tại Trang 49, tạo ra độ tương đồng ngữ nghĩa cao hơn một chút so với đoạn quy định điều kiện.
- **Chiến lược chọn, đánh đổi, điều kiện áp dụng**:
  - *Chiến lược được chọn*: **Strategy C** (Paragraph chunking kết hợp Metadata Filtering).
  - *Đánh đổi*: Strategy C đòi hỏi hệ thống ingest phải bóc tách được metadata có cấu trúc (chương, mục) từ tài liệu và ứng dụng phía người dùng cần cung cấp ngữ cảnh lọc. Tuy nhiên, nó mang lại độ tin cậy và triệt tiêu hallucination tốt nhất cho RAG.
  - *Điều kiện áp dụng*: Áp dụng tối ưu cho các tài liệu có cấu trúc điều/khoản/chương rõ ràng như quy chế đào tạo, văn bản pháp luật, tài liệu kỹ thuật có phân mục API.
- **Hạn chế của dữ liệu, nhãn, test nhỏ, đo thời gian/chi phí**:
  - Tập test gồm 5 câu là kích thước mẫu tương đối nhỏ, chỉ mang tính chất phát hiện và minh họa lỗi đại diện chứ chưa đủ để đưa ra kết luận thống kê quy mô lớn.
  - Việc chấm thủ công coherence và grounding do tác giả thực hiện có thể tiềm ẩn sai lệch chủ quan (author bias).
  - Thời gian ingest và retrieval đo trên CPU máy cá nhân có độ trễ phụ thuộc vào tài nguyên phần cứng tại thời điểm chạy.
- **Nếu làm lại hoặc mở rộng, cải tiến gì?**:
  - Bổ sung **Hybrid Retrieval**: Kết hợp BM25 (từ khóa chính xác như số hiệu văn bản, thang điểm số cụ thể) với Dense Semantic Embedding để cải thiện các câu hỏi như `q17`.
  - Mở rộng phân cấp metadata: Chia nhỏ trường lọc xuống cấp độ `Article` (Từng điều khoản) và `Audience` (Sinh viên chính quy / Bằng kép / Liên thông) để tối ưu hóa khả năng truy vấn chuyên sâu.

