# Phase 6 Implementation Plan: Manual Error Analysis và Paper Synthesis

## 1. Mục tiêu Phase 6

Phase 6 biến các bảng phân tích từ Phase 5 thành nội dung gần với báo cáo/paper.

Phase này không huấn luyện mô hình mới. Trọng tâm là:

1. Kiểm tra trạng thái annotate thủ công.
2. Tổng hợp taxonomy nếu đã annotate.
3. Tạo bảng case study tiêu biểu.
4. Tạo các bảng paper-ready cho benchmark, robustness và explainability.
5. Sinh file summary để dùng trong phần Results/Discussion.

## 2. Input

Từ Phase 5:

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
- `output/phase5/feature_cue_summary.csv`
- `output/phase5/case_study_candidates.csv`

Nếu đã annotate xong, có thể thêm một trong các file:

- `output/phase6/manual_error_annotation_completed.csv`
- `output/phase5/manual_error_annotation_completed.csv`
- hoặc cập nhật trực tiếp `output/phase5/manual_error_annotation_template.csv`

## 3. Output

Tạo thư mục:

- `output/phase6/`

Các file cần tạo:

- `phase6_annotation_audit.json`
- `paper_table_random_benchmark.csv`
- `paper_table_kfold_summary.csv`
- `paper_table_domain_robustness.csv`
- `paper_table_error_profile.csv`
- `paper_table_feature_cues.csv`
- `paper_table_error_taxonomy.csv`
- `paper_case_studies.csv`
- `paper_discussion_points.md`
- `phase6_summary.md`

## 4. Notebook

Tạo notebook:

- `ViClickBait_Phase6_Report.ipynb`

Path Colab mặc định:

```python
PHASE5_DIR = Path('/content/output/phase5')
PHASE6_DIR = Path('/content/output/phase6')
```

Fallback local:

```python
PHASE5_DIR = Path('output/phase5')
PHASE6_DIR = Path('output/phase6')
```

## 5. Logic chính

### 5.1. Annotation audit

Kiểm tra:

- Tổng số dòng annotation.
- Số dòng FP/FN.
- Số dòng đã điền `taxonomy_label`.
- Số dòng đã điền `annotator_note`.
- Số case study được đánh dấu.
- Annotation completion rate.

Nếu chưa annotate, notebook vẫn chạy và xuất summary với trạng thái `needs_manual_annotation`.

### 5.2. Paper-ready benchmark tables

Tạo bảng gọn hơn cho báo cáo:

- Model.
- Macro-F1.
- Clickbait Precision.
- Clickbait Recall.
- Clickbait F1.
- ROC-AUC.
- PR-AUC.

Không ưu tiên Accuracy trong bảng chính.

### 5.3. Domain robustness table

Lấy các held-out case khó nhất theo:

- `macro_f1_drop`
- `clickbait_f1_drop`
- `macro_f1` thấp

Tách source và category.

### 5.4. Error profile table

Gộp source/category/surface-feature profile thành bảng chọn lọc:

- Group.
- N.
- Macro-F1.
- Clickbait F1.
- FP count.
- FN count.
- Dominant error type.

### 5.5. Error taxonomy table

Nếu đã annotate:

- Count và percentage theo taxonomy.
- Tách theo FP/FN.
- Tạo bảng `paper_table_error_taxonomy.csv`.

Nếu chưa annotate:

- Tạo bảng rỗng có schema đúng.
- Ghi rõ trong summary rằng cần annotate thủ công trước khi viết phần taxonomy.

### 5.6. Case studies

Ưu tiên lấy:

- Các dòng có `is_case_study_candidate = 1`.
- Nếu chưa có, lấy từ `case_study_candidates.csv`.
- Nếu chưa annotate, giữ `analysis_note` trống để viết thủ công.

## 6. Tiêu chí hoàn thành

Phase 6 hoàn thành khi:

- Notebook chạy không lỗi.
- Có audit annotation.
- Có các bảng paper-ready.
- Có summary rõ phần nào đã sẵn sàng, phần nào còn cần annotate.
- Có file discussion points để dùng khi viết báo cáo.
