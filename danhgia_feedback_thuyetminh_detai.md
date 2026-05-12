# Đánh giá và feedback cho `thuyetminh_detai.md`

## 1. Kết luận tổng quan

File `thuyetminh_detai.md` đã có khung thuyết minh tương đối đầy đủ: có tên đề tài, lý do chọn đề tài, mục tiêu, nội dung, kế hoạch, kết quả dự kiến và tài liệu tham khảo. Về hướng nghiên cứu, bài toán phát hiện clickbait tiếng Việt trên ViClickbait-2025 có thể phát triển thành đề tài NCKH sinh viên, đặc biệt vì repo hiện tại không chỉ có benchmark cơ bản mà còn có EDA, thiết kế split, đánh giá theo miền, phân tích lỗi, phân tích đặc trưng và ablation.

Tuy nhiên, bản thuyết minh hiện tại chưa bám sát tốt nhất vào những gì repo đã làm. Điểm lệch lớn nhất là thuyết minh đang đặt trọng tâm vào việc huấn luyện 4 mô hình gồm SVM, BiLSTM, PhoBERT và XLM-RoBERTa, trong khi repo hiện tại thể hiện rõ phần đã làm mạnh nhất là traditional ML với TF-IDF, Logistic Regression, Linear SVM, Naive Bayes, Random Forest, k-fold, source/category-held-out, manual error taxonomy, lexical cue analysis và ablation. Ngược lại, các phần BiLSTM, PhoBERT, XLM-RoBERTa, HuggingFace fine-tuning, AdamW, Early Stopping, Grid Search và đo latency/parameter count chưa thấy bằng chứng implementation trong repo.

Nếu nộp theo hướng hiện tại, đề tài vẫn có thể được xem là NCKH, nhưng dễ bị phản biện là "benchmark nhiều mô hình" hơn là một nghiên cứu có câu hỏi rõ. Nếu chỉnh lại trọng tâm thành "benchmark có kiểm soát robustness/domain generalization và explainability cho phát hiện clickbait tiếng Việt", đề tài sẽ chặt hơn, bám repo hơn và có đóng góp học thuật rõ hơn.

## 2. Bằng chứng từ repo hiện tại

### 2.1. Những phần đã có bằng chứng đã làm

Repo hiện có các artefact sau:

| Nhóm công việc | Bằng chứng trong repo | Nhận xét |
|---|---|---|
| EDA và audit dữ liệu | `output/phase2/viclickbait_phase2_checklist.csv`, `output/phase2/viclickbait_eda_features.csv` | Đã kiểm tra schema, missing values, duplicate, near-duplicate, label/source/category/time distribution, surface cues, lead paragraph, lexical features. |
| Split protocol | `PHASE3_EXPERIMENTAL_PROTOCOL.md`, `output/phase3/split_summary.csv` | Đã có random stratified 70/10/20, 5-fold, leave-one-source-out, category-held-out, temporal chronological split. |
| Traditional ML benchmark | `ViClickBait_Phase4.ipynb`, `output/phase4/random_split_results.csv`, `output/phase4/phase4_summary.md` | Đã chạy TF-IDF với Logistic Regression, Linear SVM, Naive Bayes, Random Forest và rule baselines. |
| K-fold summary | `output/phase6/paper_table_kfold_summary.csv` | Có mean/std qua 5 fold cho các baseline truyền thống. |
| Domain robustness | `output/phase5/domain_drop_summary.csv`, `output/phase6/paper_table_domain_robustness.csv` | Có source-held-out và category-held-out; đây là điểm mạnh về mặt nghiên cứu. |
| Error analysis | `output/phase6/paper_table_error_taxonomy.csv`, `output/phase6/paper_discussion_points.md` | Đã annotate 100 lỗi và phân nhóm FP/FN. |
| Explainability bằng feature cues | `output/phase4/feature_importance_logreg.csv`, `output/phase6/paper_table_feature_cues.csv` | Có phân tích hệ số Logistic Regression như lexical association, không nên diễn giải là quan hệ nhân quả. |
| Ablation | `ViClickBait_Phase7.ipynb`, `output/phase7/phase7_ablation_insights.md` | Có title-only, title+lead, char TF-IDF, word+char, lexical features, masked source cues. |

Một số kết quả pilot có thể dùng làm bằng chứng khả thi nếu form cho phép nhắc đến kết quả ban đầu:

| Kết quả | Giá trị hiện có |
|---|---:|
| Best random split model | `tfidf_word_logreg` |
| Random split Macro-F1 | 0.7259 |
| Random split Clickbait F1 | 0.6429 |
| Best k-fold model | `tfidf_word_char_logreg` |
| K-fold Macro-F1 mean | 0.7464 ± 0.0048 |
| Hardest source-held-out | `VnExpress`, Macro-F1 0.6288, Clickbait F1 0.4444 |
| Hardest category-held-out | `Giải trí & Showbiz`, Macro-F1 0.5708 |
| Error counts on random test | TN 360, TP 153, FP 110, FN 60 |

### 2.2. Những phần chưa thấy bằng chứng đã làm

Các nội dung sau đang xuất hiện trong thuyết minh nhưng chưa thấy bằng chứng implementation hoặc output tương ứng:

| Nội dung trong thuyết minh | Vị trí | Trạng thái theo repo | Rủi ro khi nộp | Gợi ý chỉnh |
|---|---:|---|---|---|
| BiLSTM là một trong 4 mô hình sẽ cài đặt/fine-tune | Dòng 56, 62, 70, 86, 113 | Chưa thấy notebook/script huấn luyện BiLSTM. | Dễ bị xem là hứa quá phạm vi hoặc ghi trước phần chưa làm. | Chuyển thành "mô hình mở rộng nếu điều kiện tính toán cho phép", hoặc bỏ khỏi mục tiêu chính. |
| PhoBERT và XLM-RoBERTa fine-tuning | Dòng 56, 60, 62, 70, 87, 115-117 | Chưa thấy `transformers`, `AutoModel`, `Trainer`, checkpoint hoặc output PLM. | Đây là over-claim lớn nhất nếu đề tài được hỏi "đã làm đến đâu". | Nếu muốn giữ, cần viết là nhánh mở rộng có điều kiện; nếu bám repo hiện tại, nên bỏ khỏi kết quả bắt buộc. |
| Grid Search cho SVM | Dòng 85 | Chưa thấy bằng chứng `GridSearchCV`; repo dùng cấu hình baseline cố định theo protocol. | Người đọc có thể hỏi grid search ở đâu, tune trên split nào. | Viết lại thành "thiết lập cấu hình có kiểm soát và so sánh word/char n-gram". |
| VnCoreNLP/PyVi và stop-word removal | Dòng 77 | EDA có import `underthesea.word_tokenize`, nhưng pipeline benchmark hiện tại dựa trên TF-IDF word/char và lowercase; chưa thấy VnCoreNLP/PyVi/stop-word pipeline là thành phần chính. | Có thể bị xem là liệt kê công cụ cho đủ, không gắn với code thật. | Viết lại là "khảo sát các lựa chọn tiền xử lý; baseline chính dùng title gốc với lowercase và n-gram để tránh làm mất tín hiệu clickbait". |
| AdamW, Early Stopping, Validation Loss | Dòng 87 | Chưa thấy PLM/deep learning training loop. | Chưa có căn cứ trong repo. | Chỉ giữ nếu bổ sung notebook fine-tune thật. |
| Số tham số, thời gian huấn luyện, độ trễ suy luận | Dòng 71, 93 | Chưa thấy bảng đo compute/latency/parameter count. | Khó bảo vệ khi hội đồng yêu cầu số liệu. | Ghi là tiêu chí bổ sung dự kiến, hoặc thay bằng tiêu chí đã có: Macro-F1, Clickbait F1, Balanced Accuracy, PR-AUC, ROC-AUC, robustness drop. |
| "Huấn luyện thành công 4 mô hình đạt trạng thái hội tụ, không bị quá khớp" | Dòng 88 | Chưa có 4 mô hình, chưa có learning curve/checkpoint. | Câu này hứa chắc thành công, trái tinh thần hướng dẫn. | Viết lại là "thử nghiệm các mô hình trong phạm vi tính toán cho phép; báo cáo cả trường hợp mô hình không cải thiện hoặc có dấu hiệu overfit". |

## 3. Đánh giá nội dung

### 3.1. Mức độ bám sát những gì đã làm

Bản thuyết minh bám đúng ở các điểm sau:

- Bài toán phát hiện tiêu đề clickbait tiếng Việt trên ViClickbait-2025 là đúng với repo.
- Dataset size 3.414, 8 nguồn, 13 chủ đề, Cohen's Kappa 0.822 khớp với framing/roadmap trong repo; tuy nhiên vẫn cần trích dẫn tài liệu gốc rõ hơn.
- Hướng benchmark là đúng.
- TF-IDF + SVM/Logistic Regression là đúng với artefact hiện tại.
- EDA theo label/source/category/title length là đúng.
- Error analysis là đúng và repo còn làm tốt hơn phần thuyết minh đang mô tả.

Bản thuyết minh chưa bám sát ở các điểm quan trọng:

- Chưa đưa domain robustness thành đóng góp trung tâm, dù repo đã có source-held-out, category-held-out, robustness drop và ablation.
- Chưa đưa explainability/error taxonomy thành đóng góp trung tâm, dù repo đã có lexical cues, feature importance và annotation 100 lỗi.
- Đang nhấn mạnh BiLSTM/PhoBERT/XLM-RoBERTa trong khi repo hiện chưa có bằng chứng triển khai.
- Chưa nhấn mạnh vấn đề leakage/shortcut learning, dù đây là điểm mạnh nhất để biến đề tài từ "chạy model" thành NCKH.
- Chưa nêu rõ metric chính là Macro-F1 trong bối cảnh class imbalance; vẫn liệt kê Accuracy ngang hàng với các metric khác.

Đánh giá ngắn: bản thuyết minh hiện tại bám đúng "bài toán", nhưng chưa bám đúng "đóng góp thật" của repo.

### 3.2. Có bịa hoặc ghi phần chưa làm không?

Nếu hiểu thuyết minh là bản đề xuất việc sẽ làm trong tương lai, các phần BiLSTM/PhoBERT/XLM-RoBERTa chưa phải là "bịa" tuyệt đối. Nhưng nếu người đọc đối chiếu với repo hiện tại, các phần đó đang là "chưa có bằng chứng". Vì vậy nên dùng ngôn ngữ có điều kiện hoặc đưa chúng xuống phần mở rộng.

Các câu có rủi ro cao:

- "tiên tiến nhất như PhoBERT và XLM-RoBERTa": không nên viết "tiên tiến nhất" nếu chưa có căn cứ so sánh cập nhật.
- "cài đặt và tinh chỉnh thành công": nên tránh hứa chắc thành công.
- "đề xuất giải pháp công nghệ tối ưu nhất": không nên dùng "tối ưu nhất" vì đề tài chỉ đánh giá trên một bộ dữ liệu và một số protocol.
- "đối mặt triệt để với bài toán này": quá mạnh so với phạm vi 3.414 tiêu đề.
- "vẫn chưa có một nghiên cứu đánh giá tổng thể nào": đây là claim học thuật cần citation/literature search; nếu chưa có bằng chứng, nên viết thận trọng hơn.

Gợi ý thay thế:

> Trong phạm vi đề tài, nhóm tập trung xây dựng một benchmark có khả năng tái lập cho phát hiện clickbait tiếng Việt trên ViClickbait-2025. Ngoài random split, đề tài đánh giá thêm source-held-out và category-held-out nhằm kiểm tra mức độ suy giảm hiệu năng khi mô hình gặp nguồn báo hoặc chủ đề chưa xuất hiện trong huấn luyện. Cách thiết kế này giúp phân biệt kết quả phân loại thông thường với khả năng khái quát theo miền.

### 3.3. Với nội dung hiện tại, có đúng là đề tài NCKH chưa?

Có, nhưng cần chỉnh trọng tâm.

Nếu giữ như hiện tại, đề tài có xu hướng là một bài benchmark kỹ thuật: chạy nhiều mô hình, so sánh điểm số, chọn mô hình tốt nhất. Hướng này vẫn có giá trị thực nghiệm, nhưng đóng góp nghiên cứu chưa sắc vì câu hỏi "mô hình nào tốt hơn" khá phổ biến.

Nếu viết lại theo repo đang có, đề tài có chất NCKH rõ hơn:

- Câu hỏi nghiên cứu không chỉ là mô hình nào cao điểm nhất, mà là mô hình có khái quát được qua nguồn báo/chủ đề không.
- Protocol có random split, k-fold, source-held-out, category-held-out nên kiểm soát được benchmark lạc quan.
- Error taxonomy và lexical cues giúp giải thích vì sao mô hình đúng/sai, không dừng ở bảng điểm.
- Ablation title/lead/char/lexical/source-cue giúp kiểm tra thành phần nào đóng góp vào khả năng khái quát.

Tên đề tài nên cân nhắc đổi để phản ánh đóng góp thật:

> ĐÁNH GIÁ KHẢ NĂNG KHÁI QUÁT THEO MIỀN VÀ GIẢI THÍCH MÔ HÌNH TRONG BÀI TOÁN PHÁT HIỆN TIÊU ĐỀ CLICKBAIT TIẾNG VIỆT

Tên tiếng Anh gợi ý:

> DOMAIN-ROBUST AND EXPLAINABLE BENCHMARKING FOR VIETNAMESE CLICKBAIT HEADLINE DETECTION

Nếu vẫn muốn giữ tên hiện tại, nên bổ sung cụm "khả năng khái quát" vào B1/B2 để hội đồng thấy đề tài không chỉ là so sánh mô hình.

## 4. Đối chiếu với `huongdan_viet_thuyetminh.md`

### 4.1. B1. Giới thiệu đề tài

Yêu cầu của hướng dẫn: nêu khái quát đề tài, tổng quan tình hình hiện tại, khoảng trống nghiên cứu và đóng góp/tính mới.

Mức độ phù hợp hiện tại: đạt một phần.

Điểm tốt:

- Mở bài có bối cảnh và lý do chọn đề tài.
- Có nêu dataset ViClickbait-2025 và khoảng trống benchmark.
- Có dẫn nhập đến hướng tiếp cận của nhóm.

Điểm cần sửa:

- Đoạn mở đầu dùng nhiều từ mạnh: "vấn nạn nhức nhối", "xói mòn nghiêm trọng", "dung túng cho tin giả", "cấp thiết trên toàn cầu". Văn phong này tạo cảm giác diễn thuyết hơn là thuyết minh học thuật. Có thể giữ tinh thần cấp thiết nhưng giảm cường độ.
- Tổng quan nghiên cứu chưa có trích dẫn nội dòng. B4 có tài liệu, nhưng B1 chưa chỉ rõ claim nào dựa vào nguồn nào.
- Research gap đang viết là "chưa có benchmark tổng thể" nhưng chưa chứng minh bằng khảo sát tài liệu. Cần viết thận trọng hoặc bổ sung citation.
- Đóng góp chưa phản ánh phần repo đã làm tốt: robustness, source/category bias, leakage, error taxonomy, lexical cue, ablation.

Gợi ý chỉnh B1:

> Các kết quả trên random train/test split có thể đánh giá quá lạc quan nếu dữ liệu huấn luyện và kiểm thử chia sẻ cùng nguồn báo, chủ đề hoặc phong cách biên tập. Vì vậy, ngoài việc xây dựng baseline phân loại bằng TF-IDF và các mô hình học máy truyền thống, đề tài đặt trọng tâm vào kiểm tra khả năng khái quát theo nguồn và chủ đề, đồng thời phân tích các dấu hiệu ngôn ngữ khiến mô hình dự đoán đúng hoặc sai.

### 4.2. B2.1. Mục tiêu

Yêu cầu của hướng dẫn: mục tiêu cụ thể, đo đếm được, vừa đủ rộng để có không gian điều chỉnh.

Mức độ phù hợp hiện tại: cần chỉnh.

Vấn đề:

- Mục tiêu "cài đặt và tinh chỉnh thành công SVM, BiLSTM, PhoBERT, XLM-RoBERTa" quá chắc và quá rộng so với repo hiện tại.
- Chưa có mục tiêu về source-held-out/category-held-out, dù đây là điểm nghiên cứu tốt nhất.
- Chưa có mục tiêu về phân tích lỗi và giải thích mô hình.
- Chưa nêu Macro-F1 là metric chính, trong khi repo đã xác định Accuracy không nên là metric chính.

Gợi ý viết lại B2.1:

1. Xây dựng quy trình thực nghiệm có khả năng tái lập cho bài toán phát hiện tiêu đề clickbait tiếng Việt trên ViClickbait-2025, bao gồm EDA, kiểm tra rủi ro dữ liệu, tạo split và cấu hình metric.
2. Huấn luyện và so sánh các baseline phát hiện clickbait dựa trên TF-IDF word/char n-gram kết hợp với các mô hình học máy truyền thống như Logistic Regression, Linear SVM, Naive Bayes và Random Forest.
3. Đánh giá hiệu năng không chỉ trên random split mà còn trên k-fold, source-held-out và category-held-out để kiểm tra khả năng khái quát theo miền.
4. Phân tích lỗi dự đoán và các lexical cues của mô hình nhằm nhận diện những dấu hiệu ngôn ngữ có liên hệ với clickbait tiếng Việt.
5. Nếu điều kiện tính toán cho phép, thử nghiệm thêm một mô hình tiền huấn luyện tiếng Việt hoặc đa ngữ để làm đối chứng mở rộng, nhưng không xem đây là kết quả bắt buộc của đề tài.

### 4.3. B2.2. Nội dung và phương pháp nghiên cứu

Yêu cầu của hướng dẫn: chia thành nội dung nhỏ, mỗi nội dung có mô tả, phương pháp và kết quả dự kiến; tránh quá chung hoặc quá chi tiết cứng.

Mức độ phù hợp hiện tại: có cấu trúc đúng nhưng nội dung cần tái cân bằng.

Nội dung 1 hiện tại:

- Có khảo sát lý thuyết, nhưng đang liệt kê quá nhiều nhóm mô hình.
- Nên bổ sung research questions rõ hơn: random split có lạc quan không, mô hình có học source/category bias không, lexical cues nào ảnh hưởng dự đoán.

Nội dung 2 hiện tại:

- EDA phù hợp với repo.
- Phần tiền xử lý cần sửa vì pipeline hiện tại không chứng minh VnCoreNLP/PyVi/stop-word là thành phần chính.
- Mục "Phân chia dữ liệu:" đang bị bỏ trống. Đây là lỗi nội dung rõ ràng và nên bổ sung ngay.

Gợi ý bổ sung cho "Phân chia dữ liệu":

> Phân chia dữ liệu theo nhiều protocol gồm random stratified 70/10/20, stratified 5-fold, leave-one-source-out và category-held-out. Random split dùng để đo hiệu năng in-domain; k-fold dùng để kiểm tra độ ổn định trên bộ dữ liệu nhỏ; source/category-held-out dùng để đánh giá khả năng khái quát khi mô hình gặp nguồn báo hoặc chủ đề chưa xuất hiện trong huấn luyện. Các cột `source`, `category` và `publish_datetime` không được dùng làm feature chính để hạn chế shortcut learning.

Nội dung 3 hiện tại:

- Nên đổi từ "4 mô hình đại diện cho 3 thế hệ" sang "baseline truyền thống có kiểm soát, kèm nhánh mở rộng nếu đủ tài nguyên".
- Nếu giữ PhoBERT/XLM-RoBERTa, phải có kế hoạch B: dùng model truyền thống làm kết quả chính, PLM là đối chứng nếu đủ GPU/thời gian.

Nội dung 4 hiện tại:

- Đúng hướng nhưng nên thêm domain robustness, error taxonomy, lexical cue analysis và ablation.
- Không nên hứa "xác định mô hình tối ưu nhất"; nên viết là "xác định cấu hình có kết quả tốt nhất trong phạm vi dữ liệu và protocol của đề tài".

### 4.4. B2.3. Kế hoạch nghiên cứu

Yêu cầu của hướng dẫn: nên có bảng gồm nội dung nghiên cứu, thời gian và thành viên thực hiện.

Mức độ phù hợp hiện tại: chưa đạt hình thức khuyến nghị.

Vấn đề:

- Đang liệt kê dạng văn bản, chưa phải bảng.
- Thiếu cột thành viên thực hiện, trong khi nhóm có 2 thành viên.
- Tổng thời lượng đang là 20 tuần, trong khi A2 ghi 6 tháng. Cần giải thích 4 tuần còn lại là buffer, hoàn thiện báo cáo, phản biện nội bộ hoặc dự phòng compute.
- Kế hoạch đang phân bổ 8 tuần cho BiLSTM/PhoBERT/XLM-RoBERTa, nhưng repo hiện chưa có phần này. Nếu không chắc triển khai, nên chuyển thành nhánh mở rộng.

Gợi ý cấu trúc kế hoạch:

| Nội dung | Thời gian | Người phụ trách | Sản phẩm kiểm chứng |
|---|---:|---|---|
| Khảo sát tài liệu, chốt research questions | 3-4 tuần | Cần bổ sung | Problem statement, related work matrix |
| EDA, audit dữ liệu, kiểm tra leakage | 4 tuần | Cần bổ sung | EDA tables, duplicate/near-duplicate report |
| Thiết kế split và metric protocol | 2 tuần | Cần bổ sung | Split files, metrics config |
| Benchmark traditional ML | 4 tuần | Cần bổ sung | Random/k-fold/source/category results |
| Error analysis, lexical cues, ablation | 4 tuần | Cần bổ sung | Error taxonomy, feature cues, ablation tables |
| Hoàn thiện báo cáo và slide | 3-4 tuần | Cần bổ sung | Báo cáo, slide, appendix |

### 4.5. B3. Kết quả dự kiến

Yêu cầu của hướng dẫn: kết quả dự kiến khớp với mục tiêu, định lượng được, chứng minh được.

Mức độ phù hợp hiện tại: đạt một phần.

Điểm tốt:

- Có số lượng báo cáo, source code, bảng benchmark.

Điểm cần sửa:

- "fine-tune 4 loại mô hình" chưa khớp repo hiện tại.
- Chưa liệt kê các sản phẩm nghiên cứu mạnh hơn: protocol split, bảng robustness, taxonomy lỗi, bảng lexical cues, ablation.
- Chưa nêu rõ báo cáo sẽ có phụ lục thực nghiệm để tái lập.

Gợi ý viết lại B3:

1. Một báo cáo tổng kết đề tài trình bày cơ sở lý thuyết, phân tích dữ liệu, quy trình thực nghiệm, kết quả benchmark, phân tích robustness và phân tích lỗi.
2. Một bộ notebook/source code có khả năng tái lập các bước EDA, tạo split, huấn luyện baseline, đánh giá metric và xuất bảng kết quả.
3. Một bộ split và metric protocol gồm random stratified, stratified k-fold, source-held-out và category-held-out.
4. Một bảng benchmark cho các mô hình baseline truyền thống, báo cáo Macro-F1, Clickbait F1, Balanced Accuracy, ROC-AUC/PR-AUC nếu có.
5. Một bộ phân tích lỗi và lexical cues gồm taxonomy lỗi, case studies và bảng đặc trưng có liên hệ với dự đoán clickbait/non-clickbait.
6. Một nhánh thử nghiệm mở rộng với mô hình tiền huấn luyện nếu điều kiện tính toán cho phép.

### 4.6. B4. Tài liệu tham khảo

Yêu cầu của hướng dẫn: chỉ nêu tài liệu đã trích dẫn trong thuyết minh, dùng chuẩn IEEE, tối đa 5 tài liệu.

Mức độ phù hợp hiện tại: cần chỉnh.

Vấn đề:

- B1/B2 chưa có citation nội dòng, nhưng B4 đã có 3 tài liệu.
- Tài liệu [1] đang có thông tin placeholder như `vol. XX`; cần bổ sung thông tin chính thức hoặc đánh dấu là cần xác minh.
- Nếu nói "chưa có benchmark tổng thể", cần có tài liệu khảo sát hoặc các paper liên quan để chứng minh khoảng trống.
- Cần đảm bảo các tài liệu trong B4 đều được nhắc đến trong B1/B2.

Phần cần bạn bổ sung:

- DOI/link chính thức của ViClickbait-2025.
- 1-2 paper về clickbait detection hoặc Vietnamese text classification để làm nền cho gap.
- Nếu giữ PhoBERT/XLM-RoBERTa, cần citation chính xác cho cả hai.
- Nếu bỏ PLM khỏi mục tiêu chính, có thể vẫn giữ PhoBERT/XLM-RoBERTa như tài liệu nền, nhưng không nên để chúng chiếm trọng tâm.

## 5. Feedback về phong cách viết

### 5.1. Điểm mạnh

- Bố cục dễ theo dõi, có đủ các phần chính của form.
- Ngôn ngữ nhìn chung trôi chảy, có ý thức dùng thuật ngữ đúng lĩnh vực.
- B1 tạo được cảm giác đề tài có ý nghĩa xã hội và kỹ thuật.
- B2.2 có cấu trúc "mô tả - phương pháp - kết quả dự kiến", khớp với hướng dẫn.

### 5.2. Vấn đề phong cách

Văn phong hiện tại hơi "lớn tiếng" so với thuyết minh học thuật. Các cụm sau nên giảm cường độ hoặc thay bằng diễn đạt có căn cứ hơn:

| Cụm hiện tại | Vấn đề | Gợi ý thay |
|---|---|---|
| "vấn nạn nhức nhối" | Cảm xúc mạnh, giống báo chí hơn học thuật. | "một hiện tượng đáng chú ý trong truyền thông số" |
| "xói mòn nghiêm trọng niềm tin" | Claim xã hội lớn, cần citation. | "có thể ảnh hưởng đến trải nghiệm và mức độ tin cậy của độc giả" |
| "đối mặt triệt để với bài toán này" | Quá tuyệt đối. | "tạo điều kiện khảo sát bài toán trong phạm vi dữ liệu công khai" |
| "bước ngoặt" | Cường điệu nếu chưa có nguồn chứng minh. | "nguồn dữ liệu có giá trị cho nghiên cứu tiếng Việt" |
| "tiên tiến nhất" | Dễ sai theo thời điểm. | "các mô hình tiền huấn luyện phổ biến trong NLP tiếng Việt/đa ngữ" |
| "khẳng định sức mạnh" | Mang màu sắc quảng bá. | "so sánh điểm mạnh và giới hạn" |
| "tối ưu nhất" | Không thể khẳng định ngoài phạm vi thí nghiệm. | "phù hợp nhất trong phạm vi dữ liệu và protocol của đề tài" |
| "không bị quá khớp" | Hứa chắc kết quả. | "theo dõi và báo cáo dấu hiệu quá khớp nếu xuất hiện" |

### 5.3. Cách giải thích phương pháp nên chặt hơn

Không nên chỉ viết "phương pháp này phù hợp với đề tài". Mỗi lựa chọn cần có lý do ngắn, gắn với rủi ro hoặc câu hỏi nghiên cứu.

Ví dụ nên viết:

- Dùng Macro-F1 làm metric chính vì tập dữ liệu có tỷ lệ clickbait khoảng 31%, nên Accuracy có thể che khuất khả năng nhận diện lớp clickbait.
- Dùng source-held-out vì random split có thể để cùng phong cách biên tập xuất hiện ở cả train và test, làm kết quả lạc quan hơn thực tế.
- Dùng category-held-out vì clickbait rate khác nhau đáng kể giữa chủ đề; mô hình có thể học chủ đề thay vì dấu hiệu clickbait.
- Dùng char n-gram vì tiếng Việt có dấu, tên riêng và biến thể chính tả; char-level feature giúp giảm phụ thuộc vào tách từ.
- Dùng Logistic Regression/Linear SVM vì đây là baseline mạnh cho văn bản sparse TF-IDF và cho phép phân tích trọng số đặc trưng ở mức từ/cụm từ.
- Dùng error taxonomy vì bảng điểm không cho biết loại tiêu đề nào khiến mô hình sai; taxonomy giúp biến kết quả benchmark thành nhận xét nghiên cứu.

### 5.4. Chỗ cần đánh dấu thiếu thông tin

Các phần nên thêm nhãn "Cần bổ sung" trong bản thuyết minh hoặc trong quá trình hoàn thiện:

- Cần bổ sung citation chính thức cho ViClickbait-2025.
- Cần bổ sung danh sách paper khảo sát/công trình liên quan để chứng minh research gap.
- Cần bổ sung vai trò từng thành viên trong kế hoạch 6 tháng.
- Cần bổ sung cơ sở dự toán kinh phí 6 triệu nếu form có mục B8.
- Cần bổ sung môi trường tính toán nếu vẫn giữ PLM/fine-tuning.
- Cần bổ sung phương án dự phòng nếu không đủ GPU hoặc mô hình deep learning không cải thiện.
- Cần bổ sung quy tắc không dùng `source`, `category`, `publish_datetime` làm feature chính để tránh leakage.

## 6. Đề xuất chỉnh trọng tâm thuyết minh

### 6.1. Phiên bản trọng tâm nên dùng

Thay vì:

> So sánh SVM, BiLSTM, PhoBERT, XLM-RoBERTa để tìm mô hình tốt nhất.

Nên chuyển thành:

> Xây dựng một benchmark có khả năng tái lập cho phát hiện clickbait tiếng Việt, trong đó hiệu năng được đánh giá không chỉ bằng random split mà còn bằng các kịch bản kiểm tra khả năng khái quát theo nguồn báo và chủ đề. Đề tài đồng thời phân tích lỗi và dấu hiệu ngôn ngữ để làm rõ mô hình học đặc trưng clickbait hay học các shortcut từ dữ liệu.

Lý do: cách viết này khớp với artefact hiện có trong repo, có câu hỏi nghiên cứu rõ, và tránh hứa các mô hình chưa triển khai.

### 6.2. Cấu trúc 4 nội dung nên sửa

Nội dung 1: Khảo sát bài toán và xác định câu hỏi nghiên cứu.

- Khảo sát clickbait detection, Vietnamese text classification, benchmark và domain generalization.
- Chốt câu hỏi: random split có lạc quan không, source/category bias ảnh hưởng ra sao, lexical cues nào liên hệ với clickbait.
- Kết quả: problem statement, research questions, related-work matrix.

Nội dung 2: EDA, audit dữ liệu và thiết kế protocol.

- Kiểm tra schema, missing values, duplicate/near-duplicate, label/source/category/time distribution.
- Tạo random split, k-fold, source-held-out, category-held-out.
- Kết quả: EDA tables, split files, metrics config.

Nội dung 3: Benchmark các mô hình baseline.

- Huấn luyện rule baselines và TF-IDF word/char n-gram với Logistic Regression, Linear SVM, Naive Bayes, Random Forest.
- Báo cáo Macro-F1, Clickbait F1, Balanced Accuracy, ROC-AUC/PR-AUC nếu có.
- Kết quả: leaderboard, k-fold summary, confusion matrix, prediction table.

Nội dung 4: Robustness, error analysis và explainability.

- So sánh random split với source/category-held-out.
- Phân tích FP/FN theo source, category, surface features.
- Tạo taxonomy lỗi và phân tích lexical cues từ Logistic Regression.
- Thực hiện ablation title-only, title+lead, char n-gram, lexical features, masked source cues.
- Kết quả: domain robustness table, error taxonomy, feature cues, ablation insights.

### 6.3. Phần PLM nên đặt ở đâu?

Nếu bạn chưa chắc có GPU/thời gian, không nên để PhoBERT/XLM-RoBERTa là mục tiêu bắt buộc. Có thể đặt trong phạm vi mở rộng:

> Trong trường hợp điều kiện tính toán cho phép, đề tài sẽ thử nghiệm thêm một mô hình tiền huấn luyện phù hợp với tiếng Việt hoặc đa ngữ để làm đối chứng với baseline truyền thống. Nếu kết quả mở rộng này chưa hoàn tất, benchmark truyền thống và phân tích robustness vẫn là kết quả chính của đề tài.

Cách viết này đúng với tinh thần hướng dẫn: không hứa chắc thành công và có kế hoạch B.

## 7. Checklist chỉnh sửa ưu tiên

| Mức ưu tiên | Việc cần sửa | Lý do |
|---|---|---|
| Cao | Bỏ hoặc hạ cấp BiLSTM/PhoBERT/XLM-RoBERTa khỏi mục tiêu bắt buộc | Chưa có bằng chứng code/output hiện tại. |
| Cao | Thêm source-held-out, category-held-out, robustness drop vào B1/B2 | Đây là đóng góp thật và mạnh nhất của repo. |
| Cao | Điền mục "Phân chia dữ liệu" ở dòng 78 | Hiện đang bỏ trống trong phần phương pháp. |
| Cao | Đổi metric chính thành Macro-F1, Clickbait F1; Accuracy chỉ là phụ | Khớp protocol và tránh sai lệch do class imbalance. |
| Cao | Thay các câu hứa chắc bằng câu có điều kiện | Khớp hướng dẫn thuyết minh. |
| Trung bình | Chuyển kế hoạch B2.3 thành bảng có cột thành viên | Hướng dẫn yêu cầu nếu nhóm có 2 thành viên. |
| Trung bình | Bổ sung sản phẩm dự kiến: split protocol, robustness table, error taxonomy, lexical cues | B3 hiện chưa phản ánh đầy đủ output thật. |
| Trung bình | Giảm văn phong cường điệu trong B1 | Tăng tính học thuật, giảm cảm giác AI/marketing. |
| Trung bình | Bổ sung citation nội dòng và sửa B4 theo IEEE | Tránh claim học thuật thiếu nguồn. |
| Thấp nhưng quan trọng | Cân nhắc không để thông tin cá nhân nhạy cảm trong repo public | A4 có thông tin định danh/tài khoản; nếu repo public thì rủi ro riêng tư. |

## 8. Đánh giá cuối

Điểm mạnh nhất của đề tài không nằm ở việc liệt kê nhiều mô hình, mà nằm ở chỗ repo đã xây được một protocol thực nghiệm có khả năng kiểm tra mô hình dưới nhiều điều kiện: random, k-fold, source-held-out, category-held-out, lỗi FP/FN, lexical cues và ablation. Đây là hướng đủ tốt cho NCKH sinh viên nếu thuyết minh viết đúng trọng tâm.

Điểm cần sửa lớn nhất là bỏ cảm giác "đề tài sẽ chạy mọi mô hình phổ biến" và thay bằng "đề tài kiểm tra nghiêm túc mức độ khái quát và khả năng giải thích của các baseline phát hiện clickbait tiếng Việt". Cách viết này vừa thật với repo, vừa có tính nghiên cứu, vừa khả thi hơn trong khung 6 tháng.

