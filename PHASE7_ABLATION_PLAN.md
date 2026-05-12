# Phase 7 Implementation Plan: Ablation Study cho ViClickbait-2025

## 1. Mục tiêu Phase 7

Phase 7 thực hiện các thí nghiệm ablation (cắt giảm hoặc thêm vào từng thành phần độc lập) để kiểm tra xem yếu tố nào thực sự đóng góp vào hiệu năng và khả năng khái quát (generalization) của mô hình phát hiện clickbait tiếng Việt.

Phase này tập trung vào 4 khía cạnh:
1. **Input Context:** Việc thêm đoạn sa-pô (`lead_paragraph`) vào tiêu đề (`title`) có giúp mô hình nhận diện clickbait tốt hơn hay làm tăng nhiễu?
2. **Text Representation:** So sánh hiệu quả của Word n-gram, Character n-gram và sự kết hợp của cả hai trong tiếng Việt.
3. **Lexical Features:** Đánh giá xem việc bổ sung các đặc trưng bề mặt (độ dài, số đếm, keyword) vào biểu diễn TF-IDF có giúp mô hình bền bỉ hơn khi chuyển tên miền (source shift) không.
4. **Source Bias:** Loại bỏ các từ khóa mang đậm tính đặc thù của nguồn báo (source-heavy cues) để đo lường mức độ phụ thuộc (bias) của mô hình vào phong cách của từng nhà xuất bản.

## 2. Input và Output

### Input
Từ Phase 2:
- `output/phase2/viclickbait_eda_features.csv` (chứa text, label và các lexical features)

Từ Phase 3:
- `output/phase3/random_stratified_70_10_20.csv`
- `output/phase3/leave_one_source_out.csv`

### Output
Tạo thư mục:
- `output/phase7/`

Các file kết quả:
- `output/phase7/ablation_random_split.csv`
- `output/phase7/ablation_source_heldout.csv`
- `output/phase7/phase7_summary.md`

## 3. Thiết kế Thí nghiệm Ablation

Mô hình cơ sở (Base Model) được chọn là **Logistic Regression** (do kết quả từ Phase 4/5 chỉ ra đây là mô hình hoạt động ổn định và có thể diễn giải được).

### 3.1. Title-only vs Title + Lead Paragraph
So sánh hiệu năng khi dùng:
- `title` (baseline)
- `title + " " + lead_paragraph`

### 3.2. TF-IDF Representation
So sánh 3 cách trích xuất đặc trưng văn bản:
- `Word TF-IDF` (1-2 grams)
- `Char WB TF-IDF` (3-5 grams)
- `Word + Char TF-IDF`

### 3.3. Base Model vs Base Model + Lexical Features
So sánh việc chỉ dùng nội dung text với việc bổ sung thêm các vector đặc trưng đếm được:
- `TF-IDF Word LogReg`
- `TF-IDF Word + Lexical Features LogReg` (Sử dụng FeatureUnion kết hợp TF-IDF với StandardScaler của các numeric features như độ dài, tỷ lệ số, keywords).

### 3.4. Without Source-heavy Cues
Xây dựng một bộ "source stop-words" tự động. 
- Tìm các từ (n-grams) có tỷ lệ xuất hiện chênh lệch cực kỳ lớn giữa các source (hoặc chỉ xuất hiện ở 1-2 source cụ thể mà mang trọng số LogReg cao).
- Mask/xóa các từ này khỏi text đầu vào.
- Train lại model và đánh giá xem F1-score có giảm mạnh không. Nếu không giảm hoặc giảm rất ít, mô hình thực sự học clickbait. Nếu giảm mạnh, mô hình đang học "đường tắt" (shortcut).

## 4. Kịch bản Đánh giá (Evaluation Protocol)

Mỗi mô hình trong các thiết lập Ablation trên sẽ được huấn luyện và đánh giá trên 2 tập:
1. **Random Stratified Split:** Lấy kết quả Test set để so sánh hiệu năng tối đa.
2. **Leave-One-Source-Out (LOSO) Split:** Tính Macro-F1 trung bình trên các tập test (khi source bị ẩn) để đánh giá khả năng Domain Generalization.

## 5. Cấu trúc Notebook

Notebook `ViClickBait_Phase7.ipynb` sẽ được xây dựng với các section:
1. Load dữ liệu và Utilities.
2. Chuẩn bị Pipelines cho các thí nghiệm.
3. Ablation 1: Input Context.
4. Ablation 2: Representation.
5. Ablation 3: Lexical Features.
6. Ablation 4: Source-heavy cues masking.
7. Run Experiments (Random Split & Source Held-out).
8. Export Results.
