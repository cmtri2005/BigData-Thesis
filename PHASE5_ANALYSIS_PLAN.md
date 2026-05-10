# Phase 5 Implementation Plan: Domain Robustness, Error Analysis và Explainability cho ViClickbait-2025

## 1. Mục tiêu Phase 5

Phase 5 không thêm mô hình mới. Mục tiêu là biến kết quả benchmark ở Phase 4 thành phân tích nghiên cứu có thể đưa vào báo cáo NCKH.

Phase này tập trung vào 4 câu hỏi:

1. Mô hình tốt nhất trên random split có thật sự ổn định không?
2. Hiệu năng giảm như thế nào khi đánh giá theo source/category held-out?
3. Mô hình sai ở những nhóm tiêu đề nào?
4. Các lexical cue mà mô hình học được có khớp với đặc trưng clickbait tiếng Việt không?

Đây là phase quan trọng để đề tài không chỉ là "chạy benchmark", mà có thêm giá trị phân tích về robustness và explainability.

## 2. Input và Output

### Input

Từ Phase 2:

- `output/phase2/viclickbait_eda_features.csv`

Từ Phase 3:

- `output/phase3/random_stratified_70_10_20.csv`
- `output/phase3/leave_one_source_out.csv`
- `output/phase3/category_heldout.csv`

Từ Phase 4:

- `output/phase4/random_split_results.csv`
- `output/phase4/kfold_results.csv`
- `output/phase4/source_heldout_results.csv`
- `output/phase4/category_heldout_results.csv`
- `output/phase4/all_results.csv`
- `output/phase4/best_traditional_model_predictions.csv`
- `output/phase4/predictions_random_split.csv`
- `output/phase4/feature_importance_logreg.csv`
- `output/phase4/confusion_matrices.json`

### Output

Tạo thư mục:

- `output/phase5/`

Các file cần tạo:

- `output/phase5/phase5_data_audit.json`
- `output/phase5/random_split_leaderboard.csv`
- `output/phase5/kfold_summary.csv`
- `output/phase5/domain_drop_summary.csv`
- `output/phase5/source_robustness_summary.csv`
- `output/phase5/category_robustness_summary.csv`
- `output/phase5/best_model_error_table.csv`
- `output/phase5/error_profile_by_source.csv`
- `output/phase5/error_profile_by_category.csv`
- `output/phase5/error_profile_by_surface_features.csv`
- `output/phase5/manual_error_annotation_template.csv`
- `output/phase5/manual_error_taxonomy_guide.md`
- `output/phase5/feature_cue_summary.csv`
- `output/phase5/case_study_candidates.csv`
- `output/phase5/phase5_summary.md`

Nếu có vẽ hình:

- `output/phase5/figures/random_split_macro_f1.png`
- `output/phase5/figures/domain_drop_by_source.png`
- `output/phase5/figures/domain_drop_by_category.png`
- `output/phase5/figures/best_model_confusion_matrix.png`
- `output/phase5/figures/top_clickbait_features.png`
- `output/phase5/figures/top_non_clickbait_features.png`

## 3. Notebook cần tạo

Tạo notebook:

- `ViClickBait_Phase5_Analysis.ipynb`

Path Colab mặc định:

```python
PHASE2_PATH = Path('/content/output/phase2/viclickbait_eda_features.csv')
PHASE3_DIR = Path('/content/output/phase3')
PHASE4_DIR = Path('/content/output/phase4')
PHASE5_DIR = Path('/content/output/phase5')
```

Nên giữ fallback local như Phase 4 để notebook vẫn chạy được trong repo.

## 4. Phạm vi Phase 5

### Làm trong Phase 5

1. Kiểm tra tính đầy đủ của output Phase 4.
2. Tổng hợp bảng benchmark chính.
3. Phân tích domain generalization theo source/category.
4. Tạo bảng lỗi của best model trên random test.
5. Phân tích false positive và false negative theo source/category/surface features.
6. Tạo taxonomy guide cho manual error analysis.
7. Chọn mẫu lỗi tiêu biểu để đọc thủ công.
8. Tổng hợp lexical feature importance từ Logistic Regression.
9. Xuất summary để đưa vào báo cáo.

### Không làm trong Phase 5

Không làm:

- Fine-tune PhoBERT.
- Fine-tune XLM-R.
- CNN/BiLSTM.
- LLM prompting.
- SHAP/LIME đầy đủ.
- Huấn luyện lại toàn bộ benchmark.

Lý do:

- Phase 5 phải tập trung vào phân tích kết quả đã có.
- Các mô hình mới nên để Phase 6 hoặc một nhánh mở rộng riêng nếu còn thời gian.

## 5. Thiết kế phân tích

### 5.1. Phase 4 output audit

Cần kiểm tra:

- Có đủ tất cả file Phase 4 không.
- Số dòng của từng file có đúng kỳ vọng không.
- `best_traditional_model_predictions.csv` có đúng số mẫu test không.
- Các `id` trong prediction join được với `viclickbait_eda_features.csv` không.
- Không có duplicate `id` trong test prediction.
- `y_true`, `y_pred` chỉ gồm `{0, 1}`.
- `feature_importance_logreg.csv` có đủ 100 cue clickbait và 100 cue non-clickbait không.

Output:

- `phase5_data_audit.json`

Nếu audit fail, notebook phải raise error rõ ràng.

### 5.2. Benchmark synthesis

Từ `random_split_results.csv`, tạo leaderboard chỉ cho test split.

Cần báo cáo:

- Model name.
- Accuracy.
- Balanced accuracy.
- Macro-F1.
- Clickbait precision.
- Clickbait recall.
- Clickbait F1.
- ROC-AUC.
- PR-AUC.

Sắp xếp theo:

1. Macro-F1.
2. Clickbait F1.

Output:

- `random_split_leaderboard.csv`

Từ `kfold_results.csv`, tạo bảng mean/std theo model.

Output:

- `kfold_summary.csv`

Điểm cần nhấn mạnh trong báo cáo:

- Accuracy của majority baseline cao nhưng clickbait F1 bằng 0.
- Keyword heuristic tương đối mạnh nhưng không đủ recall.
- Logistic Regression/SVM là baseline chính đáng tin hơn Naive Bayes/Random Forest.

### 5.3. Domain robustness analysis

Từ:

- `random_split_results.csv`
- `source_heldout_results.csv`
- `category_heldout_results.csv`

Tính:

- `macro_f1_drop = random_test_macro_f1 - heldout_macro_f1`
- `clickbait_f1_drop = random_test_clickbait_f1 - heldout_clickbait_f1`
- `balanced_accuracy_drop = random_test_balanced_accuracy - heldout_balanced_accuracy`

Làm riêng cho:

- Best Logistic Regression.
- Best Linear SVM.

Output:

- `domain_drop_summary.csv`
- `source_robustness_summary.csv`
- `category_robustness_summary.csv`

Cần phân tích:

- Source nào khó nhất.
- Category nào khó nhất.
- Drop theo source có yếu hơn hay mạnh hơn drop theo category.
- Có trường hợp accuracy cao nhưng clickbait F1 thấp không.

Các case đã thấy từ Phase 4 cần kiểm tra lại:

- `VnExpress` là source khó với clickbait F1 thấp.
- `Giải trí & Showbiz`, `Quốc tế`, `Tin tức tổng hợp` là các category đáng phân tích sâu.
- `Tin tức tổng hợp` có thể có accuracy cao nhưng clickbait F1 thấp, cho thấy class imbalance/domain skew.

### 5.4. Best model error table

Merge:

- `best_traditional_model_predictions.csv`
- `output/phase2/viclickbait_eda_features.csv`

Tạo cột:

- `is_correct`
- `error_type`
  - `TP`: true clickbait, predict clickbait.
  - `TN`: true non-clickbait, predict non-clickbait.
  - `FP`: true non-clickbait, predict clickbait.
  - `FN`: true clickbait, predict non-clickbait.
- `confidence`
  - Nếu `y_score` là probability: dùng trực tiếp.
  - Nếu `y_score` là decision score: chuẩn hóa tương đối hoặc dùng absolute margin.
- `confidence_error_rank`

Output:

- `best_model_error_table.csv`

Cột nên giữ:

- `id`
- `title`
- `lead_paragraph`
- `source`
- `category`
- `label`
- `y_true`
- `y_pred`
- `y_score`
- `error_type`
- `is_correct`
- `title_char_len`
- `title_word_count`
- `title_n_question`
- `title_n_exclamation`
- `title_n_cb_keywords`
- `title_n_curiosity_gap_cues`

### 5.5. Error profile by source/category

Từ `best_model_error_table.csv`, tạo bảng theo source/category.

Mỗi bảng cần có:

- `n_samples`
- `n_clickbait`
- `n_non_clickbait`
- `accuracy`
- `macro_f1`
- `clickbait_precision`
- `clickbait_recall`
- `clickbait_f1`
- `false_positive_count`
- `false_negative_count`
- `false_positive_rate`
- `false_negative_rate`
- `dominant_error_type`

Output:

- `error_profile_by_source.csv`
- `error_profile_by_category.csv`

Mục tiêu:

- Chỉ ra model sai không đều giữa các domain.
- Tìm domain cần đưa vào case study.
- Tạo luận điểm cho phần domain generalization.

### 5.6. Error profile by surface features

Chia tiêu đề theo các nhóm:

- Length bin:
  - `very_short`
  - `short`
  - `medium`
  - `long`
  - `very_long`
- Có dấu hỏi:
  - `has_question`
  - `no_question`
- Có từ khóa clickbait:
  - `has_clickbait_keyword`
  - `no_clickbait_keyword`
- Có curiosity gap cue:
  - `has_curiosity_gap`
  - `no_curiosity_gap`
- Có số:
  - `has_number`
  - `no_number`

Với mỗi nhóm, tính:

- Accuracy.
- Macro-F1.
- Clickbait F1.
- FP/FN count.
- FP/FN rate.

Output:

- `error_profile_by_surface_features.csv`

Mục tiêu:

- Kiểm tra model có phụ thuộc quá mạnh vào cue bề mặt không.
- Tìm các lỗi kiểu: tiêu đề có từ gây tò mò nhưng không clickbait, hoặc clickbait tinh vi không có keyword.

### 5.7. Manual error taxonomy

Tạo file hướng dẫn taxonomy:

- `manual_error_taxonomy_guide.md`

Taxonomy đề xuất:

#### False Positive

- `FP_emotional_but_informative`: Có từ cảm xúc/gây chú ý nhưng tiêu đề vẫn thông tin.
- `FP_question_but_legitimate`: Có dạng câu hỏi nhưng không tạo curiosity gap sai lệch.
- `FP_entertainment_style_bias`: Tin giải trí/showbiz có style hấp dẫn nhưng không clickbait.
- `FP_source_style_bias`: Model có vẻ bị ảnh hưởng bởi source/style.
- `FP_short_ambiguous_title`: Tiêu đề ngắn hoặc thiếu ngữ cảnh làm model đoán sai.

#### False Negative

- `FN_subtle_curiosity_gap`: Clickbait tinh vi, không có keyword rõ.
- `FN_neutral_surface_form`: Bề mặt giống tin thường nhưng vẫn che giấu thông tin quan trọng.
- `FN_requires_lead_context`: Cần lead/article context mới thấy clickbait.
- `FN_entity_context_needed`: Cần hiểu entity/sự kiện để nhận ra câu nhử.
- `FN_domain_specific_clickbait`: Clickbait đặc thù theo domain/category.

#### General/Ambiguous

- `AMB_borderline_label`: Nhãn khó, ranh giới clickbait/non-clickbait không rõ.
- `DATA_quality_issue`: Lỗi dữ liệu, title thiếu, duplicate, encoding, metadata bất thường.
- `OTHER`: Không thuộc nhóm trên.

### 5.8. Manual annotation template

Chọn mẫu lỗi từ `best_model_error_table.csv`.

Ưu tiên:

- 50 false positive.
- 50 false negative.
- Đa dạng source.
- Đa dạng category.
- Ưu tiên lỗi model tự tin sai:
  - FP có `y_score` cao.
  - FN có `y_score` thấp.

Nếu số lỗi không đủ cân bằng, lấy toàn bộ nhóm nhỏ hơn và bù bằng nhóm còn lại.

Output:

- `manual_error_annotation_template.csv`

Cột cần có:

- `id`
- `title`
- `lead_paragraph`
- `source`
- `category`
- `y_true`
- `y_pred`
- `y_score`
- `error_type`
- `suggested_priority`
- `taxonomy_label`
- `annotator_note`
- `is_case_study_candidate`

Lưu ý:

- `taxonomy_label`, `annotator_note`, `is_case_study_candidate` để trống cho người nghiên cứu điền thủ công.
- Không nên tự động gán taxonomy cuối cùng nếu chưa đọc mẫu.

### 5.9. Feature cue summary

Từ:

- `feature_importance_logreg.csv`

Tạo bảng:

- Top clickbait cues.
- Top non-clickbait cues.
- Nhóm cue thủ công:
  - `question/curiosity`
  - `surprise/emotion`
  - `vague_reference`
  - `official/news`
  - `entity/event`
  - `other`

Output:

- `feature_cue_summary.csv`

Cần phân tích:

- Cue nào hợp lý với clickbait tiếng Việt.
- Cue nào có nguy cơ là shortcut.
- Cue nào xuất hiện ở non-clickbait và phản ánh phong cách tin chính thống.

Không claim rằng coefficient là giải thích nhân quả. Chỉ viết là lexical association learned by the model.

### 5.10. Case study candidates

Tạo file:

- `case_study_candidates.csv`

Chọn:

- 5 false positive tiêu biểu.
- 5 false negative tiêu biểu.
- 5 correct clickbait tiêu biểu.
- 5 correct non-clickbait tiêu biểu.

Mỗi case nên có:

- `id`
- `title`
- `source`
- `category`
- `y_true`
- `y_pred`
- `y_score`
- `case_group`
- `why_selected`
- `analysis_note`

`analysis_note` có thể để trống để viết thủ công sau.

Mục tiêu:

- Chuẩn bị cho phần qualitative analysis trong báo cáo.

## 6. Code structure trong notebook

Notebook `ViClickBait_Phase5_Analysis.ipynb` nên có các section:

1. Import và config path.
2. Load Phase 2/3/4 outputs.
3. Audit output Phase 4.
4. Benchmark synthesis.
5. Domain robustness analysis.
6. Best model error table.
7. Error profile by source/category.
8. Error profile by surface features.
9. Feature cue summary.
10. Manual taxonomy guide.
11. Manual annotation template.
12. Case study candidate selection.
13. Export outputs.
14. Phase 5 summary.

## 7. Các function chính cần implement

### 7.1. `audit_phase4_outputs`

Input:

- Paths của Phase 2/3/4.

Output:

- Dict audit.
- Raise error nếu thiếu file hoặc join lỗi.

### 7.2. `make_random_split_leaderboard`

Input:

- `random_split_results.csv`

Output:

- Test leaderboard sorted by Macro-F1.

### 7.3. `summarize_kfold`

Input:

- `kfold_results.csv`

Output:

- Mean/std theo model.

### 7.4. `compute_domain_drop`

Input:

- Random split test results.
- Source-held-out/category-held-out results.

Output:

- Drop table theo model/domain.

### 7.5. `build_best_model_error_table`

Input:

- Best model predictions.
- Phase 2 feature table.

Output:

- Row-level error table.

### 7.6. `classification_metrics_by_group`

Input:

- Error table.
- Group column: `source`, `category`, `length_bin`, `has_question`, ...

Output:

- Metrics và FP/FN counts theo group.

### 7.7. `select_manual_error_samples`

Input:

- Error table.
- Target FP/FN count.

Output:

- Manual annotation template.

### 7.8. `summarize_feature_cues`

Input:

- Feature importance table.

Output:

- Grouped cue summary.

## 8. Metrics cần dùng trong Phase 5

Metric chính:

- Macro-F1.
- Clickbait F1.

Metric phụ:

- Accuracy.
- Balanced accuracy.
- Clickbait precision.
- Clickbait recall.
- FP count.
- FN count.
- FP rate.
- FN rate.

Không dùng accuracy làm kết luận chính.

## 9. Expected findings cần kiểm tra

Từ Phase 4, các finding ban đầu:

1. Best random split model là `tfidf_word_logreg`.
2. `tfidf_word_char_logreg` có k-fold mean Macro-F1 tốt nhất nhưng không vượt rõ trên random test.
3. Majority baseline có accuracy khá cao nhưng clickbait F1 bằng 0.
4. Keyword heuristic có precision tương đối nhưng recall thấp.
5. `VnExpress` là source khó, đặc biệt ở clickbait F1.
6. Category-held-out drop rõ hơn source-held-out.
7. `Giải trí & Showbiz`, `Quốc tế`, `Tin tức tổng hợp` là các category cần phân tích sâu.
8. Feature importance cho thấy model học nhiều cue kiểu `nào`, `sao`, `bất ngờ`, `không`, nhưng cũng có cue non-clickbait kiểu `báo`, `công`, `bộ`, `thủ tướng`.

Phase 5 phải kiểm chứng các finding này bằng bảng và mẫu lỗi cụ thể.

## 10. Paper-ready outputs

Sau Phase 5, có thể đưa vào báo cáo các bảng:

- Table: Random split benchmark leaderboard.
- Table: K-fold stability summary.
- Table: Domain robustness drop by source.
- Table: Domain robustness drop by category.
- Table: Error profile by source.
- Table: Error profile by category.
- Table: Manual error taxonomy.
- Table: Representative error cases.
- Table: Top lexical cues learned by Logistic Regression.

Các đoạn discussion nên trả lời:

- Vì sao random split chưa đủ?
- Source/category nào làm model yếu đi?
- Mô hình đang dựa vào lexical cue nào?
- False positive và false negative thường đến từ đâu?
- Điều này nói gì về clickbait tiếng Việt?

## 11. Tiêu chí hoàn thành Phase 5

Phase 5 hoàn thành khi có:

- [ ] Notebook `ViClickBait_Phase5_Analysis.ipynb`.
- [ ] Audit Phase 4 output pass.
- [ ] Benchmark summary table.
- [ ] Domain drop summary.
- [ ] Error table của best model.
- [ ] Error profile theo source/category.
- [ ] Error profile theo surface features.
- [ ] Manual taxonomy guide.
- [ ] Manual annotation template.
- [ ] Feature cue summary.
- [ ] Case study candidates.
- [ ] `phase5_summary.md`.

## 12. Kết luận định hướng

Phase 5 là phase biến kết quả benchmark thành lập luận nghiên cứu.

Nếu Phase 4 trả lời "model nào tốt hơn", thì Phase 5 phải trả lời:
- Tốt hơn trong điều kiện nào?
- Yếu ở domain nào?
- Sai vì lý do gì?
- Mô hình học cue clickbait thật hay học shortcut bề mặt?

