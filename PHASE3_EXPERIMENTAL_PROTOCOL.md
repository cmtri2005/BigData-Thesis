# Phase 3: Experimental Protocol cho ViClickbait-2025

## 1. Mục tiêu

Phase 3 chuẩn hóa cách chia dữ liệu và cách đánh giá trước khi benchmark mô hình. Mục tiêu là tránh cherry-picking, giảm rủi ro leakage và tạo protocol đủ rõ để người khác có thể chạy lại.

Input chính:

- `output/phase2/viclickbait_eda_features.csv`

Output chính sau khi chạy script:

- `output/phase3/random_stratified_70_10_20.csv`
- `output/phase3/stratified_kfold_5.csv`
- `output/phase3/leave_one_source_out.csv`
- `output/phase3/category_heldout.csv`
- `output/phase3/temporal_chronological_70_10_20.csv`
- `output/phase3/split_summary.csv`
- `output/phase3/metrics_config.json`

Script tạo output:

```bash
python phase3_create_splits.py
```

## 2. Nhận xét từ Phase 2

Phase 2 đã đủ điều kiện để sang Phase 3:

- Dataset giữ đủ 3,414 mẫu headline.
- Label distribution: 1,065 clickbait và 2,349 non-clickbait.
- Class imbalance ở mức vừa phải, khoảng 31.2% clickbait.
- `source` có bias rõ:
  - Kênh14: 76.92% clickbait.
  - SaoStar: 65.03% clickbait.
  - VnExpress: 14.47% clickbait.
  - Báo Mới: 20.25% clickbait.
- `category` có bias rõ:
  - Giải trí & Showbiz: 70.59% clickbait.
  - Sức khỏe & Đời sống: 57.02% clickbait.
  - Tin tức tổng hợp: 4.06% clickbait.
- Temporal distribution lệch mạnh về năm 2025, nên temporal split chỉ nên xem là exploratory nếu không có thêm dữ liệu cân bằng theo thời gian.

Kết luận: random split là cần thiết nhưng không đủ. Benchmark chính nên báo cáo thêm source-held-out và category-held-out để tránh kết luận quá lạc quan.

## 3. Split Protocol

### 3.1. Random Stratified Split

File output:

- `output/phase3/random_stratified_70_10_20.csv`

Tỷ lệ:

- Train: 70%.
- Validation: 10%.
- Test: 20%.

Nguyên tắc:

- Stratify theo `label`.
- Fixed seed: `42`.
- Dùng làm split chính để so sánh baseline.
- Không tune hyperparameter trên test set.

Vai trò:

- Benchmark chính cho traditional ML, FastText, deep learning và pretrained language models.

### 3.2. Stratified 5-Fold Cross Validation

File output:

- `output/phase3/stratified_kfold_5.csv`

Nguyên tắc:

- 5 fold.
- Stratify theo `label`.
- Fixed seed: `42`.
- Cột `fold` cho biết fold validation.
- Khi chạy fold `k`, dùng `fold == k` làm validation/test fold và `fold != k` làm train.

Vai trò:

- Kiểm tra độ ổn định trên dataset nhỏ.
- Ưu tiên dùng cho traditional ML và FastText.
- Với pretrained models, có thể thay bằng multi-seed trên random split nếu compute hạn chế.

### 3.3. Leave-One-Source-Out

File output:

- `output/phase3/leave_one_source_out.csv`

Nguyên tắc:

- Mỗi lần giữ một `source` làm test.
- Train trên tất cả source còn lại.
- Không dùng `source` làm feature input trong mô hình chính.

Vai trò:

- Kiểm tra domain generalization theo nguồn báo.
- Đây là split quan trọng nhất để trả lời câu hỏi: mô hình học clickbait thật hay học publisher/source bias?

### 3.4. Category-Held-Out

File output:

- `output/phase3/category_heldout.csv`

Nguyên tắc:

- Chỉ dùng category có ít nhất 100 mẫu.
- Mỗi lần giữ một category đủ mẫu làm test.
- Train trên các category còn lại.
- Không dùng `category` làm feature input trong mô hình chính.

Vai trò:

- Kiểm tra khả năng khái quát theo chủ đề.
- Đặc biệt quan trọng vì Phase 2 cho thấy category như `Giải trí & Showbiz`, `Sức khỏe & Đời sống`, `Tin tức tổng hợp` có clickbait rate lệch mạnh.

### 3.5. Temporal Chronological Split

File output:

- `output/phase3/temporal_chronological_70_10_20.csv`

Nguyên tắc:

- Chỉ split các mẫu parse được `publish_dt`.
- Sắp xếp theo thời gian.
- 70% cũ nhất: train.
- 10% tiếp theo: validation.
- 20% mới nhất: test.
- Mẫu thiếu thời gian được gán `excluded_missing_datetime`.

Vai trò:

- Kiểm tra robustness theo thời gian.
- Vì Phase 2 cho thấy dữ liệu lệch mạnh về 2025, kết quả temporal split cần được báo cáo như exploratory, không nên diễn giải quá mạnh.

## 4. Metric Protocol

Metric chính:

- Macro-F1.

Metric bắt buộc:

- Precision cho class clickbait.
- Recall cho class clickbait.
- F1 cho class clickbait.
- Weighted-F1.
- Balanced accuracy.
- Confusion matrix.

Metric nên có:

- ROC-AUC nếu model trả được probability hoặc decision score.
- PR-AUC vì clickbait là class thiểu số.
- Mean ± std qua nhiều seed hoặc nhiều fold.

Không dùng một mình:

- Accuracy.

## 5. Quy tắc chống leakage

Không dùng các cột sau làm feature chính trong benchmark headline-only:

- `source`
- `category`
- `publish_datetime`
- `publish_dt`
- `source_encoded`
- `category_encoded`
- `source_cb_rate_diagnostic`
- `category_cb_rate_diagnostic`

Các cột này chỉ dùng cho:

- Audit bias.
- Source/category/temporal split.
- Leakage-control baseline nếu cần chứng minh shortcut.

Feature input chính:

- `title`

Feature input phụ cho ablation:

- `title + lead_paragraph`
- `title + MODEL_SAFE_FEATS`
- `title + lead_paragraph + MODEL_SAFE_FEATS`

## 6. Cách dùng trong Phase 4

Với random split:

```python
split_df = pd.read_csv('output/phase3/random_stratified_70_10_20.csv')
train_ids = split_df.loc[split_df['split'] == 'train', 'id']
val_ids = split_df.loc[split_df['split'] == 'validation', 'id']
test_ids = split_df.loc[split_df['split'] == 'test', 'id']
```

Với 5-fold:

```python
fold_df = pd.read_csv('output/phase3/stratified_kfold_5.csv')
fold = 0
train_ids = fold_df.loc[fold_df['fold'] != fold, 'id']
val_ids = fold_df.loc[fold_df['fold'] == fold, 'id']
```

Với leave-one-source-out:

```python
source_df = pd.read_csv('output/phase3/leave_one_source_out.csv')
heldout = 'VnExpress'
run_df = source_df[source_df['heldout_source'] == heldout]
train_ids = run_df.loc[run_df['split'] == 'train', 'id']
test_ids = run_df.loc[run_df['split'] == 'test', 'id']
```

## 7. Output hoàn thành Phase 3

Phase 3 được xem là hoàn thành khi có:

- [ ] Random stratified split.
- [ ] Stratified 5-fold split.
- [ ] Leave-one-source-out split.
- [ ] Category-held-out split.
- [ ] Temporal chronological split.
- [ ] Split summary.
- [ ] Metrics config.
- [ ] Protocol document.

Sau Phase 3, có thể chuyển sang Phase 4: benchmark baseline.
