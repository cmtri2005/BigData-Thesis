# Phase 1: Research Framing cho ViClickbait-2025

## 1. Tên đề tài đề xuất

**Phát hiện clickbait tiếng Việt có khả năng khái quát theo miền và giải thích được trên bộ dữ liệu ViClickbait-2025**

Tên tiếng Anh có thể dùng trong paper:

**Robust and Explainable Benchmarking for Vietnamese Clickbait Detection on ViClickbait-2025**

## 2. Problem Statement

Clickbait là hiện tượng tiêu đề được thiết kế để kích thích người đọc nhấp vào bài viết bằng cách tạo tò mò, gây sốc, che giấu thông tin quan trọng hoặc phóng đại nội dung. Trong bối cảnh báo chí số và mạng xã hội, clickbait làm suy giảm chất lượng tiếp nhận thông tin, ảnh hưởng đến niềm tin của độc giả và có thể góp phần lan truyền thông tin kém chất lượng.

Với tiếng Việt, bài toán clickbait detection còn thiếu các benchmark công khai, nhất quán và có khả năng tái lập. Sự xuất hiện của bộ dữ liệu **ViClickbait-2025** tạo nền tảng quan trọng để đánh giá các mô hình phát hiện clickbait trên tiêu đề báo tiếng Việt. Tuy nhiên, nếu chỉ đánh giá bằng random train/test split, kết quả có thể quá lạc quan vì mô hình có thể học các shortcut như nguồn báo, chủ đề, phong cách biên tập hoặc độ dài tiêu đề thay vì học bản chất clickbait.

Do đó, đề tài này không chỉ benchmark nhiều nhóm mô hình, mà còn đánh giá khả năng khái quát theo miền và phân tích khả năng giải thích của mô hình. Trọng tâm nghiên cứu là kiểm tra xem mô hình có thật sự nhận diện được các dấu hiệu clickbait tiếng Việt hay chỉ tận dụng các bias có sẵn trong dữ liệu.

## 3. Research Gap

Các nghiên cứu clickbait detection thường tập trung vào việc cải thiện điểm số phân loại trên một tập test cố định. Với tiếng Việt, khoảng trống nghiên cứu còn rõ hơn vì số lượng dataset công khai và benchmark có hệ thống còn hạn chế.

Các khoảng trống chính mà đề tài hướng đến:

1. **Thiếu benchmark hệ thống cho tiếng Việt**: Chưa có so sánh nhất quán giữa traditional ML, deep learning và pretrained language models trên ViClickbait-2025.
2. **Thiếu đánh giá robustness/domain generalization**: Random split không kiểm tra được mô hình có hoạt động tốt trên nguồn báo, chủ đề hoặc thời gian chưa thấy trong train hay không.
3. **Thiếu phân tích shortcut và leakage**: Source, category, title length hoặc các cue bề mặt có thể khiến mô hình đạt điểm cao mà không thật sự hiểu clickbait.
4. **Thiếu explainability và error analysis**: Chưa rõ mô hình dựa vào từ/cụm từ nào để ra quyết định, và lỗi sai thường thuộc nhóm nào.

## 4. Research Questions

**RQ1.** Các nhóm mô hình traditional ML, deep learning và pretrained language models khác nhau như thế nào trên ViClickbait-2025?

**RQ2.** Hiệu năng của mô hình thay đổi như thế nào khi chuyển từ random split sang source-held-out, category-held-out hoặc temporal split?

**RQ3.** Mô hình có đang học đặc trưng clickbait thật sự, hay đang tận dụng bias theo nguồn báo, chủ đề, độ dài tiêu đề và phong cách biên tập?

**RQ4.** Những đặc trưng ngôn ngữ nào có liên hệ mạnh với clickbait tiếng Việt, và chúng giải thích được các lỗi false positive/false negative đến mức nào?

## 5. Contribution Statement

Đề tài dự kiến có 4 đóng góp chính:

1. **Benchmark có hệ thống**: So sánh các nhóm mô hình từ heuristic baseline, TF-IDF + traditional ML, FastText, deep learning đến pretrained language models trên ViClickbait-2025.
2. **Evaluation protocol nghiêm túc hơn random split**: Bổ sung k-fold hoặc multi-seed evaluation, leave-one-source-out, category-held-out và temporal robustness nếu dữ liệu cho phép.
3. **Shortcut và domain-bias analysis**: Kiểm tra mô hình có bị ảnh hưởng bởi source/category/temporal bias hay không thông qua các baseline chỉ dùng metadata và phân tích performance drop.
4. **Explainability và error analysis**: Phân tích lexical cues, feature importance, explanation examples và taxonomy lỗi để hiểu vì sao mô hình đúng/sai.

## 6. Literature Review Notes

### 6.1. Clickbait Detection

Nhóm nghiên cứu này tập trung vào việc phân loại tiêu đề hoặc bài viết thành clickbait và non-clickbait. Các hướng phổ biến gồm:

- Dùng đặc trưng bề mặt: độ dài tiêu đề, dấu câu, số đếm, từ gây tò mò, từ cảm xúc.
- Dùng TF-IDF/n-gram với Logistic Regression, SVM hoặc Naive Bayes.
- Dùng neural models như CNN, LSTM, BiLSTM và attention.
- Dùng pretrained language models để học biểu diễn ngữ cảnh tốt hơn.

Điểm cần rút ra cho đề tài: clickbait không chỉ là bài toán classification, mà còn liên quan đến curiosity gap, ambiguity, sensationalism và mismatch giữa title với nội dung bài.

### 6.2. Vietnamese Text Classification

Tiếng Việt có đặc thù về dấu, từ ghép, tách từ và cách viết tên riêng. Vì vậy, benchmark nên thử cả:

- Word n-gram.
- Character n-gram.
- Tokenization tiếng Việt nếu dùng mô hình cần tách từ.
- Pretrained models phù hợp tiếng Việt như PhoBERT hoặc các Vietnamese BERT variants.

Điểm cần rút ra cho đề tài: không nên chỉ dùng một kiểu preprocessing. Cần so sánh word-level và char-level features để tránh kết luận lệch do lựa chọn biểu diễn văn bản.

### 6.3. Pretrained Language Models

PhoBERT, XLM-RoBERTa và các biến thể BERT tiếng Việt thường mạnh trong classification vì tận dụng tri thức ngôn ngữ học được từ pretraining. Tuy nhiên, với dataset nhỏ, mô hình lớn có thể overfit hoặc học shortcut.

Điểm cần rút ra cho đề tài: pretrained models nên được đánh giá bằng nhiều seed và domain-held-out split, không chỉ random split.

### 6.4. Domain Generalization

Domain generalization trong text classification kiểm tra mô hình có hoạt động tốt khi test domain khác train domain hay không. Trong ViClickbait-2025, domain có thể được hiểu là:

- Nguồn báo (`source`).
- Chủ đề (`category`).
- Thời gian xuất bản (`publish_datetime`).

Điểm cần rút ra cho đề tài: nếu mô hình giảm mạnh khi test trên source chưa thấy, random split có thể đang đánh giá quá lạc quan.

### 6.5. Explainability

Explainability giúp trả lời câu hỏi mô hình dựa vào dấu hiệu nào để dự đoán clickbait. Với traditional ML, có thể dùng hệ số Logistic Regression hoặc feature weights của Linear SVM. Với pretrained models, có thể dùng SHAP, LIME hoặc Integrated Gradients.

Điểm cần rút ra cho đề tài: explanation không chỉ để minh họa, mà phải hỗ trợ error analysis và phát hiện shortcut.

## 7. Phạm vi thực nghiệm phù hợp NCKH cấp trường

### Nên làm

- EDA chi tiết theo label/source/category/time.
- Benchmark các baseline chính: heuristic, TF-IDF + ML, FastText, PhoBERT, XLM-R.
- Source-held-out evaluation.
- Leakage check với source-only/category-only/surface-feature-only baseline.
- Lexical feature analysis.
- Manual error analysis khoảng 100 mẫu sai.

### Có thể làm nếu đủ thời gian

- Category-held-out evaluation.
- Temporal split theo chronological order.
- SHAP/LIME cho một số case study.
- Ablation title-only vs title + lead paragraph.

### Không nên mở rộng trong scope hiện tại

- Multimodal clickbait detection.
- LLM reasoning quy mô lớn.
- Dataset expansion lớn.
- Kiến trúc deep learning phức tạp mới.

## 8. Thesis chính của bài nghiên cứu

**Trong phát hiện clickbait tiếng Việt, điểm số trên random split không đủ để kết luận mô hình tốt. Một benchmark nghiêm túc cần đánh giá thêm khả năng khái quát theo nguồn báo/chủ đề/thời gian và cần phân tích mô hình dựa vào những dấu hiệu nào để ra quyết định.**

## 9. Output Phase 1

- [x] Problem statement.
- [x] Research gap.
- [x] 4 research questions.
- [x] Contribution statement.
- [x] Literature review notes theo nhóm chủ đề.
- [x] Scope phù hợp NCKH cấp trường.
- [x] Thesis chính của đề tài.
