# Roadmap NCKH: Benchmark, Domain Generalization và Explainability cho Vietnamese Clickbait Detection

## 0. Phạm vi đề tài

### Tên đề tài gợi ý

**Phát hiện clickbait tiếng Việt có khả năng khái quát theo miền và giải thích được trên bộ dữ liệu ViClickbait-2025**

### Hướng nghiên cứu

Đề tài không chỉ dừng lại ở việc benchmark nhiều mô hình. Contribution chính là:

1. Xây dựng benchmark có hệ thống cho bài toán phát hiện clickbait tiếng Việt.
2. Đánh giá khả năng khái quát của mô hình theo nguồn báo, chủ đề và thời gian.
3. Phân tích khả năng giải thích của mô hình thông qua đặc trưng ngôn ngữ và lỗi dự đoán.

### CÂU HỎI NGHIÊN CỨU

**RQ1.** Các nhóm mô hình traditional ML, deep learning và pretrained language models khác nhau như thế nào trên ViClickbait-2025?

**RQ2.** Mô hình có thật sự học đặc trưng clickbait, hay chủ yếu học bias theo nguồn báo, chủ đề, độ dài tiêu đề và phong cách biên tập?

**RQ3.** Những dấu hiệu ngôn ngữ nào ảnh hưởng nhiều nhất đến quyết định clickbait/non-clickbait của mô hình?

**RQ4.** Khi đánh giá trên source unseen hoặc temporal split, hiệu năng có giảm đáng kể so với random split không?

### Phạm vi không làm

- Không mở rộng thành bài toán multimodal nếu chưa có thời gian xử lý thumbnail và license ảnh.
- Không tập trung vào việc đề xuất kiến trúc deep learning quá phức tạp.
- Không dùng accuracy làm metric chính.
- Không dùng metadata như `source`, `category`, `publish_datetime` làm feature chính nếu chưa có thí nghiệm kiểm soát leakage.
- Không claim mô hình có thể tổng quát cho toàn bộ báo chí tiếng Việt nếu chỉ đánh giá trên ViClickbait-2025.

---

## Phase 1. Đọc tài liệu và xác định research framing

### Mục tiêu

Chốt bài toán nghiên cứu, khoảng trống học thuật và cách trình bày contribution sao cho vượt qua một bài benchmark bình thường.

### Việc cần làm

- Đọc kỹ bài nền ViClickbait-2025:
  - Dataset size: 3,414 headline.
  - Label: clickbait / non-clickbait.
  - Clickbait ratio: khoảng 31.2%.
  - Nguồn: 8 nền tảng tin tức Việt Nam.
  - Chủ đề: 13 news categories.
  - Thời gian: 2023-2025.
  - Annotation: 3 annotator, Cohen's Kappa = 0.822.
  - License: CC BY 4.0.
- Đọc thêm các nhóm tài liệu:
  - Clickbait detection với traditional ML.
  - Clickbait detection với pretrained language models.
  - Domain generalization trong text classification.
  - Explainability trong NLP classification.
  - Vietnamese NLP và Vietnamese pretrained language models.
- Viết 1 trang problem statement:
  - Vì sao clickbait tiếng Việt đáng quan tâm?
  - ViClickbait-2025 đã giải quyết phần nào?
  - Khoảng trống còn lại là benchmark nghiêm túc, robustness và explainability.

### Output cần có

- File note literature review ngắn gọn.
- Danh sách paper liên quan.
- 3-4 research questions đã chốt.
- Draft contribution statement.

### Tiêu chí hoàn thành

- Giải thích được vì sao đề tài không chỉ là "chạy model lấy điểm".
- Chốt được thông điệp trung tâm: **random split có thể làm benchmark quá lạc quan; cần đánh giá source/domain robustness và phân tích lỗi dự đoán**.

---

## Phase 2. Dataset audit và EDA

### Mục tiêu

Hiểu rõ dataset trước khi train model, phát hiện các bias có thể ảnh hưởng đến benchmark.

### Việc cần làm

- Kiểm tra schema:
  - `id`
  - `url`
  - `title`
  - `lead_paragraph`
  - `category`
  - `publish_datetime`
  - `source`
  - `thumbnail_url`
  - `label`
- Thống kê label distribution:
  - Số lượng clickbait.
  - Số lượng non-clickbait.
  - Tỷ lệ class imbalance.
- Thống kê theo `source`:
  - Mỗi source có bao nhiêu mẫu?
  - Tỷ lệ clickbait theo source.
  - Source nào có nguy cơ tạo shortcut cho model?
- Thống kê theo `category`:
  - Số mẫu mỗi category.
  - Tỷ lệ clickbait mỗi category.
  - Category nào quá ít mẫu để đánh giá riêng?
- Thống kê theo thời gian:
  - Số mẫu theo năm/tháng.
  - Tỷ lệ clickbait theo năm/tháng.
  - Có đủ mẫu cho temporal split hay không?
- Phân tích tiêu đề:
  - Độ dài ký tự.
  - Số token/word.
  - Tỷ lệ có dấu hỏi.
  - Tỷ lệ có dấu chấm than.
  - Tỷ lệ có số đếm/listicle.
  - Tỷ lệ chứa đại từ mơ hồ: "này", "kia", "người này", "điều này", "bất ngờ", "sốc".
- Kiểm tra duplicate và near-duplicate:
  - Normalize title.
  - Exact duplicate.
  - Fuzzy duplicate.
  - Mẫu cùng URL hoặc cùng tiêu đề nhưng khác label.

### Output cần có

- Bảng thống kê label/source/category/time.
- Biểu đồ:
  - Label distribution.
  - Clickbait ratio by source.
  - Clickbait ratio by category.
  - Title length by label.
  - Temporal distribution.
- Danh sách rủi ro dataset:
  - Class imbalance.
  - Source bias.
  - Category bias.
  - Temporal bias.
  - Duplicate leakage.

### Tiêu chí hoàn thành

- Biết rõ dataset có những bias nào.
- Có cơ sở để thiết kế split và metric phù hợp.
- Có thể viết mục "Dataset Analysis" trong paper.

---

## Phase 3. Thiết kế experimental protocol

### Mục tiêu

Chốt protocol đánh giá trước khi train model để tránh cherry-picking và tránh benchmark thiếu công bằng.

### Split cần có

#### 3.1. Random stratified split

- Mục đích: benchmark cơ bản.
- Gợi ý:
  - Train: 70%.
  - Validation: 10%.
  - Test: 20%.
  - Stratify theo label.
- Lưu ý:
  - Duplicate và near-duplicate phải được xử lý trước khi split.
  - Báo cáo kết quả trung bình qua nhiều seed.

#### 3.2. K-fold cross validation

- Mục đích: ổn định kết quả trên dataset nhỏ.
- Gợi ý:
  - 5-fold stratified CV.
  - Dùng cho traditional ML và FastText.
  - Nếu compute hạn chế, pretrained models có thể chạy 3 seed trên fixed split thay vì full CV.

#### 3.3. Leave-one-source-out evaluation

- Mục đích: kiểm tra domain generalization theo nguồn báo.
- Cách làm:
  - Mỗi lần giữ 1 source làm test.
  - Train trên các source còn lại.
  - Lặp lại cho tất cả source đủ mẫu.
- Lưu ý:
  - Nếu source quá ít mẫu, có thể gom vào "small sources" hoặc chỉ báo cáo như exploratory result.

#### 3.4. Category-held-out evaluation

- Mục đích: kiểm tra khả năng tổng quát theo chủ đề.
- Cách làm:
  - Giữ một số category đủ mẫu làm test.
  - Train trên category còn lại.
- Chỉ nên áp dụng cho category có số mẫu đủ lớn.

#### 3.5. Temporal split

- Mục đích: kiểm tra robustness theo thời gian.
- Cách làm gợi ý:
  - Train trên dữ liệu cũ hơn.
  - Test trên dữ liệu mới hơn.
- Lưu ý:
  - Nếu 2023 quá ít mẫu, có thể dùng split theo tháng/quý thay vì theo năm.

### Metrics cần báo cáo

Metric chính:

- Macro-F1.

Metric bắt buộc:

- Precision cho clickbait.
- Recall cho clickbait.
- F1 cho clickbait.
- Weighted-F1.
- Balanced accuracy.
- Confusion matrix.

Metric nên có:

- ROC-AUC.
- PR-AUC.
- Mean và standard deviation qua nhiều seed.

Metric không nên dùng một mình:

- Accuracy.

### Nguyên tắc công bằng khi so sánh

- Tất cả model dùng cùng split.
- Cùng preprocessing đầu vào, trừ khi model yêu cầu khác.
- Không tune hyperparameter trên test set.
- Chỉ dùng validation set để chọn threshold và hyperparameter.
- Báo cáo compute setup:
  - CPU/GPU.
  - Số seed.
  - Batch size.
  - Max sequence length.
  - Learning rate.
  - Epoch.

### Output cần có

- File mô tả experimental protocol.
- Script tạo split có seed cố định.
- Bảng mapping split: train/validation/test.
- Danh sách metric và cách tính.

### Tiêu chí hoàn thành

- Nếu người khác chạy lại, họ có thể tạo đúng split và metric.
- Không còn thay đổi protocol sau khi đã thấy kết quả test.

---

## Phase 4. Xây dựng benchmark baseline

### Mục tiêu

Có bảng kết quả baseline đủ rộng, gồm từ đơn giản đến mạnh, để làm nền cho các phần domain generalization và explainability.

### Nhóm 1. Simple baselines

Cần có:

- Majority class baseline.
- Random stratified baseline.
- Length-based heuristic:
  - Ví dụ: title dài hơn threshold thì clickbait.
- Keyword heuristic:
  - Dựa vào từ/cụm từ như "bất ngờ", "sốc", "không ngờ", "người này", "điều này", "sự thật", "lý do".

Vai trò:

- Cho thấy model ML có vượt qua heuristic đơn giản hay không.
- Hỗ trợ explainability vì clickbait có nhiều dấu hiệu bề mặt.

### Nhóm 2. Traditional ML

Cần có:

- TF-IDF word n-gram + Logistic Regression.
- TF-IDF word/char n-gram + Linear SVM.
- TF-IDF + Naive Bayes.
- TF-IDF + Random Forest.

Khuyến nghị:

- Linear SVM và Logistic Regression là baseline mạnh hơn Random Forest trên sparse text.
- Cần thử cả word n-gram và char n-gram vì tiếng Việt có dấu, tách từ và biến thể chính tả.

### Nhóm 3. FastText

Cần có:

- FastText supervised classifier.
- So sánh với TF-IDF và deep learning.

Lý do:

- FastText rẻ, nhanh, mạnh trên dataset nhỏ.
- Là baseline thực dụng cho low-resource Vietnamese text classification.

### Nhóm 4. Deep Learning

Cần có nếu đủ thời gian:

- CNN.
- BiLSTM.
- Attention-BiLSTM.

Lưu ý:

- Dataset nhỏ nên deep learning từ đầu dễ overfit.
- Nếu kết quả kém pretrained models là bình thường.
- Cần dùng early stopping, dropout và validation loss.

### Nhóm 5. Pretrained Language Models

Cần có:

- PhoBERT-base.
- XLM-RoBERTa-base.
- viBERT hoặc một Vietnamese BERT tương đương.

Có thể thêm nếu đủ GPU:

- PhoBERT-large.

Lưu ý:

- Fine-tune nhiều seed.
- Báo cáo variance.
- Tránh kết luận quá mạnh nếu chênh lệch nhỏ.

### Output cần có

- Bảng benchmark trên random split.
- Bảng benchmark trên k-fold hoặc multi-seed.
- Confusion matrix cho 3 model đại diện:
  - Best traditional ML.
  - Best lightweight model.
  - Best pretrained model.

### Tiêu chí hoàn thành

- Có tối thiểu 8-10 baseline hợp lý.
- Có kết quả ổn định qua seed.
- Biết model nào là main model cho các phase sau.

---

## Phase 5. Domain generalization evaluation

### Mục tiêu

Kiểm tra model có học clickbait thật hay chỉ học shortcut theo source/category/time.

### Thí nghiệm 1. Leave-one-source-out

Cần làm:

- Chọn các model đại diện:
  - Logistic Regression hoặc Linear SVM.
  - FastText.
  - PhoBERT-base.
  - XLM-RoBERTa-base.
- Mỗi lần giữ 1 source làm test.
- Train trên các source còn lại.
- Báo cáo Macro-F1 và clickbait F1 cho từng source.

Cần phân tích:

- Source nào khó nhất?
- Source nào làm model giảm mạnh nhất?
- Model nào robust hơn khi gặp source mới?
- Nếu model tốt trên random split nhưng kém trên source-held-out, đó là bằng chứng source bias.

### Thí nghiệm 2. Category-held-out

Cần làm:

- Chọn category đủ mẫu.
- Giữ từng category làm test.
- Train trên category còn lại.

Cần phân tích:

- Clickbait trong giải trí, đời sống, thể thao, chính trị có khác nhau không?
- Model có fail khi gặp chủ đề ít có trong train không?

### Thí nghiệm 3. Temporal robustness

Cần làm:

- Sắp xếp data theo `publish_datetime`.
- Train trên khoảng thời gian cũ.
- Test trên khoảng thời gian mới.

Cần phân tích:

- Hiệu năng có giảm theo thời gian không?
- Clickbait cue có thay đổi theo năm/tháng không?

### Thí nghiệm 4. Feature leakage check

Cần làm:

- Train model chỉ dùng `source`.
- Train model chỉ dùng `category`.
- Train model chỉ dùng title length và surface features.
- So sánh với model dùng `title`.

Ý nghĩa:

- Nếu `source-only` hoặc `category-only` đạt điểm cao bất thường, dataset có domain shortcut mạnh.
- Đây là điểm research rất quan trọng cho bài NCKH.

### Output cần có

- Bảng leave-one-source-out.
- Bảng category-held-out.
- Bảng temporal split.
- Bảng leakage/shortcut analysis.
- Đồ thị drop performance:
  - Random split vs source-held-out.
  - Random split vs temporal split.

### Tiêu chí hoàn thành

- Chứng minh được random split có thể không phản ánh đầy đủ khả năng generalization.
- Có insight rõ về bias theo source/category/time.
- Có nội dung đủ mạnh cho phần "Domain Generalization Analysis" trong paper.

---

## Phase 6. Explainability và error analysis

### Mục tiêu

Giải thích mô hình dựa vào dấu hiệu nào và lỗi sai thường xảy ra ở đâu.

### 6.1. Lexical feature analysis

Tạo bộ đặc trưng thủ công:

- Title length.
- Word count.
- Character count.
- Có dấu hỏi hay không.
- Có dấu chấm than hay không.
- Có số đếm hay không.
- Có listicle pattern hay không.
- Có từ cảm xúc/gây sốc hay không.
- Có đại từ mơ hồ hay không.
- Có cụm gây curiosity gap hay không.
- Độ tương đồng giữa `title` và `lead_paragraph` nếu có.

Phân tích:

- Đặc trưng nào phân biệt clickbait/non-clickbait tốt?
- Đặc trưng nào chỉ mạnh trong một số source?
- Đặc trưng nào gây false positive?

### 6.2. Explainability cho traditional ML

Dùng:

- Coefficient của Logistic Regression.
- Feature weight của Linear SVM.

Cần báo cáo:

- Top n-gram đẩy về clickbait.
- Top n-gram đẩy về non-clickbait.
- So sánh với guideline annotation.

### 6.3. Explainability cho pretrained models

Có thể dùng:

- SHAP.
- LIME.
- Integrated Gradients.
- Attention visualization chỉ nên dùng phụ, không nên claim attention là explanation đầy đủ.

Cần chọn:

- 20-30 mẫu đúng.
- 20-30 mẫu sai.
- Bao gồm cả clickbait và non-clickbait.
- Bao gồm nhiều source/category.

Cần phân tích:

- Token/cụm từ nào làm model quyết định clickbait?
- Model có quá phụ thuộc vào từ gây sốc không?
- Model có bỏ qua ngữ cảnh trong lead paragraph không?
- Model có nhầm tin giải trí hợp lệ thành clickbait không?

### 6.4. Error taxonomy

Phân nhóm lỗi sai thành các loại:

- False positive do từ cảm xúc nhưng tiêu đề vẫn thông tin.
- False positive do source/category bias.
- False positive do tiêu đề dài.
- False negative do clickbait tinh vi, không có từ khóa rõ.
- False negative do cần ngữ cảnh bài viết mới thấy curiosity gap.
- Lỗi do ambiguous label.
- Lỗi do entity/context thiếu thông tin.

### 6.5. Manual error analysis

Cần làm:

- Lấy 100 mẫu sai của model chính.
- Chia đều:
  - 50 false positive.
  - 50 false negative.
- Gán nhãn lỗi bằng taxonomy.
- Báo cáo tỷ lệ từng nhóm lỗi.

### Output cần có

- Bảng top lexical cues.
- Bảng feature importance.
- Ví dụ explanation của model.
- Bảng error taxonomy.
- 5-10 case study tiêu biểu.

### Tiêu chí hoàn thành

- Giải thích được vì sao model đúng/sai.
- Có insight ngôn ngữ tiếng Việt, không chỉ có bảng metric.
- Có phần "Explainability and Error Analysis" đủ thuyết phục.

---

## Phase 7. Ablation study

### Mục tiêu

Kiểm tra thành phần nào thật sự có đóng góp vào hiệu năng và khả năng generalization.

### Ablation cần làm

#### 7.1. Title-only vs title + lead paragraph

- Model A: chỉ dùng `title`.
- Model B: dùng `title` + `lead_paragraph`.
- Câu hỏi:
  - Lead paragraph có giúp phát hiện curiosity gap không?
  - Hay làm model nhiễu hơn và overfit hơn?

#### 7.2. TF-IDF word vs char vs word+char

- Model A: word n-gram.
- Model B: char n-gram.
- Model C: word + char n-gram.
- Câu hỏi:
  - Char n-gram có hữu ích với tiếng Việt không?

#### 7.3. Pretrained model vs pretrained + lexical features

- Model A: PhoBERT-base.
- Model B: PhoBERT-base + lexical features.
- Câu hỏi:
  - Lexical cues có giúp model robust hơn trên source-held-out không?

#### 7.4. Without source-heavy cues

- Loại hoặc mask một số từ/cụm từ quá đặc thù của source nếu phát hiện source bias.
- Câu hỏi:
  - Performance giảm bao nhiêu?
  - Model có đang dựa vào style của một vài nguồn báo không?

### Output cần có

- Bảng ablation trên random split.
- Bảng ablation trên source-held-out.
- Nhận xét thành phần nào giúp generalization.

### Tiêu chí hoàn thành

- Không chỉ nói model nào tốt hơn, mà biết vì sao tốt hơn.
- Có bằng chứng về vai trò của title, lead paragraph và lexical features.

---

## Phase 8. Tổng hợp kết quả và viết paper

### Mục tiêu

Biến toàn bộ thí nghiệm thành một câu chuyện nghiên cứu mạch lạc.

### Cấu trúc paper gợi ý

#### 1. Introduction

Cần nói rõ:

- Clickbait tiếng Việt là bài toán quan trọng.
- ViClickbait-2025 mở ra cơ hội benchmark công khai.
- Benchmark random split chưa đủ để đánh giá model.
- Đề tài này đánh giá cả performance, robustness và explainability.

Contribution:

1. Benchmark nhiều nhóm mô hình trên ViClickbait-2025.
2. Thiết kế evaluation protocol gồm random split, cross-validation, source-held-out, category-held-out và temporal split.
3. Phân tích shortcut/bias theo source, category và surface features.
4. Thực hiện explainability và error analysis để rút ra đặc trưng clickbait tiếng Việt.

#### 2. Related Work

Cần gồm:

- Clickbait detection.
- Vietnamese text classification.
- Pretrained Vietnamese language models.
- Domain generalization trong NLP.
- Explainable NLP classification.

#### 3. Dataset and Exploratory Analysis

Cần có:

- Mô tả ViClickbait-2025.
- Label distribution.
- Source/category/time distribution.
- Duplicate check.
- Risk analysis.

#### 4. Methodology

Cần có:

- Preprocessing.
- Baseline models.
- Pretrained models.
- Lexical features.
- Split protocol.
- Metrics.

#### 5. Experimental Results

Cần có:

- Random split benchmark.
- K-fold hoặc multi-seed results.
- Source-held-out results.
- Category-held-out results.
- Temporal results.
- Ablation.

#### 6. Explainability and Error Analysis

Cần có:

- Top cues.
- Explanation examples.
- Error taxonomy.
- Case studies.

#### 7. Discussion

Cần trả lời:

- Model nào tốt nhất trên random split?
- Model nào robust nhất trên domain shift?
- Dấu hiệu nào của clickbait tiếng Việt quan trọng?
- Random split có đánh giá quá lạc quan không?
- Dataset có những bias nào?

#### 8. Limitations

Cần thẳng thắn:

- Dataset nhỏ.
- Chỉ có 8 source.
- Temporal distribution lệch.
- Clickbait là subjective label.
- Chưa xử lý multimodal.
- Chưa có external test set mới.

#### 9. Conclusion

Cần kết luận:

- Benchmark pretrained models đạt kết quả cao.
- Tuy nhiên hiệu năng giảm khi test trên source/category/time unseen.
- Explainability cho thấy model vừa học cue clickbait, vừa bị ảnh hưởng bởi source/style bias.
- Cần evaluation protocol nghiêm túc hơn cho clickbait tiếng Việt.

### Bảng/figure cần có trong paper

- Table 1: Dataset statistics.
- Figure 1: Label distribution.
- Figure 2: Clickbait ratio by source.
- Figure 3: Clickbait ratio by category.
- Table 2: Model benchmark on random split.
- Table 3: K-fold or multi-seed results.
- Table 4: Leave-one-source-out results.
- Table 5: Temporal/category-held-out results.
- Table 6: Ablation study.
- Table 7: Error taxonomy.
- Figure 4: Performance drop under domain shift.
- Figure 5: Example explanations.

### Tiêu chí hoàn thành

- Paper có một thesis rõ: **mô hình cần được đánh giá về robustness và explainability, không chỉ điểm random split**.
- Kết quả không chỉ là bảng benchmark.
- Có discussion thẳng thắn về bias và limitation.

---

## Phase 9. Timeline đề xuất

### Tuần 1

- Đọc bài nền và related work.
- Chốt research questions.
- Audit dataset và EDA.
- Tạo split protocol.

### Tuần 2

- Implement preprocessing.
- Chạy simple baselines.
- Chạy TF-IDF + ML models.
- Chạy FastText.

### Tuần 3

- Chạy PhoBERT, XLM-RoBERTa, viBERT.
- Chạy multi-seed.
- Tổng hợp benchmark random split.

### Tuần 4

- Chạy leave-one-source-out.
- Chạy category-held-out nếu đủ mẫu.
- Chạy temporal split nếu khả thi.
- Làm leakage check với source/category/length-only features.

### Tuần 5

- Làm lexical feature analysis.
- Làm explainability với Logistic Regression/SVM và PhoBERT.
- Làm manual error analysis 100 mẫu sai.
- Xây error taxonomy.

### Tuần 6

- Làm ablation study.
- Chốt bảng biểu.
- Viết bản thảo paper.
- Kiểm tra reproducibility.

### Tuần 7 nếu có

- Refine paper.
- Viết abstract, conclusion, limitation.
- Chuẩn bị slide báo cáo.
- Chuẩn bị repo/code/notebook để demo.

---

## Checklist tổng hợp

### Dataset

- [ ] Load dataset thành công.
- [ ] Kiểm tra schema.
- [ ] Kiểm tra missing values.
- [ ] Kiểm tra duplicate.
- [ ] Thống kê label/source/category/time.
- [ ] Tạo EDA figures.

### Experimental protocol

- [ ] Random stratified split.
- [ ] K-fold hoặc multi-seed setup.
- [ ] Leave-one-source-out split.
- [ ] Category-held-out split nếu khả thi.
- [ ] Temporal split nếu khả thi.
- [ ] Metric functions.
- [ ] Fixed random seeds.

### Models

- [ ] Majority baseline.
- [ ] Heuristic baseline.
- [ ] TF-IDF + Logistic Regression.
- [ ] TF-IDF + Linear SVM.
- [ ] TF-IDF + Naive Bayes.
- [ ] TF-IDF + Random Forest.
- [ ] FastText.
- [ ] CNN.
- [ ] BiLSTM.
- [ ] Attention-BiLSTM.
- [ ] PhoBERT-base.
- [ ] XLM-RoBERTa-base.
- [ ] viBERT.

### Domain generalization

- [ ] Leave-one-source-out results.
- [ ] Category-held-out results.
- [ ] Temporal split results.
- [ ] Source-only baseline.
- [ ] Category-only baseline.
- [ ] Length/surface-feature baseline.
- [ ] Performance drop analysis.

### Explainability

- [ ] Lexical feature analysis.
- [ ] Top n-gram weights.
- [ ] SHAP/LIME/Integrated Gradients examples.
- [ ] False positive analysis.
- [ ] False negative analysis.
- [ ] Error taxonomy.
- [ ] Case studies.

### Paper

- [ ] Introduction.
- [ ] Related work.
- [ ] Dataset analysis.
- [ ] Methodology.
- [ ] Results.
- [ ] Domain generalization analysis.
- [ ] Explainability and error analysis.
- [ ] Discussion.
- [ ] Limitations.
- [ ] Conclusion.

---

## Kết quả mong đợi

Nếu triển khai đúng, đề tài nên đạt được các kết quả sau:

1. Một benchmark có hệ thống cho Vietnamese clickbait detection trên ViClickbait-2025.
2. Bằng chứng về việc random split có thể cho kết quả lạc quan hơn domain-held-out split.
3. Phân tích rõ các bias theo source, category và temporal distribution.
4. Danh sách lexical cues đặc trưng của clickbait tiếng Việt.
5. Error taxonomy giúp giải thích vì sao model sai.
6. Một paper NCKH cấp trường có research value rõ ràng, không chỉ là báo cáo chạy model.

## Thông điệp chính của đề tài

**Trong phát hiện clickbait tiếng Việt, điểm số trên random split không đủ để kết luận mô hình tốt. Cần đánh giá thêm khả năng khái quát theo nguồn báo, chủ đề, thời gian và cần phân tích mô hình dựa vào dấu hiệu nào để ra quyết định.**
