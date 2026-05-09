# Phase 4 Implementation Plan: Benchmark Baseline cho ViClickbait-2025

## 1. Mục tiêu Phase 4

Phase 4 triển khai benchmark baseline đầu tiên sau khi đã có split chuẩn ở Phase 3.

Mục tiêu không phải chạy thật nhiều mô hình ngay từ đầu, mà là xây một pipeline benchmark có thể tái lập, công bằng và đủ chắc để mở rộng sang Deep Learning / PhoBERT ở các phase sau.

Phase 4 tập trung vào:

1. Simple baselines.
2. TF-IDF + Traditional ML.
3. Evaluation chuẩn theo `metrics_config.json`.
4. Export kết quả để phục vụ paper và error analysis.

## 2. Input và Output

### Input

Từ Phase 2:

- `output/phase2/viclickbait_eda_features.csv`

Từ Phase 3:

- `output/phase3/random_stratified_70_10_20.csv`
- `output/phase3/stratified_kfold_5.csv`
- `output/phase3/leave_one_source_out.csv`
- `output/phase3/category_heldout.csv`
- `output/phase3/metrics_config.json`

### Output

Tạo thư mục:

- `output/phase4/`

Các file dự kiến:

- `output/phase4/random_split_results.csv`
- `output/phase4/kfold_results.csv`
- `output/phase4/source_heldout_results.csv`
- `output/phase4/category_heldout_results.csv`
- `output/phase4/all_results.csv`
- `output/phase4/confusion_matrices.json`
- `output/phase4/predictions_random_split.csv`
- `output/phase4/best_traditional_model_predictions.csv`
- `output/phase4/feature_importance_logreg.csv`
- `output/phase4/phase4_summary.md`

## 3. Notebook cần tạo

Tạo notebook:

- `ViClickbait_Phase4_Benchmark.ipynb`
Path Colab mặc định:

```python
PHASE2_PATH = Path('/content/output/phase2/viclickbait_eda_features.csv')
PHASE3_DIR = Path('/content/output/phase3')
PHASE4_DIR = Path('/content/output/phase4')
```


## 4. Phạm vi mô hình Phase 4

### 4.1. Simple baselines

Các baseline bắt buộc:

1. Majority class baseline.
2. Random stratified baseline.
3. Length-based heuristic.
4. Keyword-based heuristic.

Mục đích:

- Kiểm tra model ML có thật sự vượt qua rule đơn giản không.
- Tạo mốc thấp nhất cho benchmark.
- Hỗ trợ explainability vì clickbait có nhiều cue bề mặt.

### 4.2. Traditional ML baselines

Các model cần chạy:

1. TF-IDF word n-gram + Logistic Regression.
2. TF-IDF char n-gram + Logistic Regression.
3. TF-IDF word+char n-gram + Logistic Regression.
4. TF-IDF word n-gram + Linear SVM.
5. TF-IDF char n-gram + Linear SVM.
6. TF-IDF word+char n-gram + Linear SVM.
7. TF-IDF word n-gram + Multinomial Naive Bayes.
8. TF-IDF word n-gram + Random Forest.

Khuyến nghị:

- Logistic Regression và Linear SVM là baseline chính.
- Random Forest chỉ là baseline phụ vì thường không mạnh trên sparse text.
- Char n-gram quan trọng với tiếng Việt vì có dấu, biến thể chính tả và tên riêng.

### 4.3. Chưa làm trong Phase 4

Không implement trong Phase 4:

- CNN.
- BiLSTM.
- Attention-BiLSTM.
- FastText.
- PhoBERT.
- XLM-RoBERTa.
- viBERT.
- LLM prompting.

Lý do:

- Phase 4 cần chốt pipeline benchmark truyền thống trước.
- Deep Learning / PLM nên là Phase 5 để tránh notebook quá dài và khó debug.

## 5. Text Representation

### 5.1. Text input chính

Input chính:

- `title`

Đây là setting headline-only và là setting benchmark chính.

### 5.2. Input phụ cho ablation

Có thể thêm sau khi baseline chính chạy ổn:

- `title + lead_paragraph`

Trong Phase 4, nếu thời gian hạn chế, chỉ cần chuẩn bị function tạo text này nhưng chưa bắt buộc chạy toàn bộ.

### 5.3. Không dùng làm feature chính

Không dùng các cột sau trong model chính:

- `source`
- `category`
- `publish_datetime`
- `publish_dt`
- `source_encoded`
- `category_encoded`
- `source_cb_rate_diagnostic`
- `category_cb_rate_diagnostic`

Lý do:

- Các cột này có nguy cơ tạo shortcut/leakage.
- Chúng chỉ dùng để split và phân tích domain generalization.

## 6. TF-IDF Config

### 6.1. Word-level TF-IDF

Gợi ý:

```python
TfidfVectorizer(
    analyzer='word',
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    lowercase=True
)
```

### 6.2. Char-level TF-IDF

Gợi ý:

```python
TfidfVectorizer(
    analyzer='char_wb',
    ngram_range=(3, 5),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    lowercase=True
)
```

### 6.3. Word + char

Dùng `FeatureUnion` hoặc `ColumnTransformer` để nối word TF-IDF và char TF-IDF.

Gợi ý:

```python
FeatureUnion([
    ('word', word_vectorizer),
    ('char', char_vectorizer)
])
```

## 7. Model Config

### 7.1. Logistic Regression

Gợi ý:

```python
LogisticRegression(
    max_iter=2000,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
```

Vai trò:

- Baseline mạnh.
- Có thể dùng coefficient để explainability.

### 7.2. Linear SVM

Gợi ý:

```python
LinearSVC(
    class_weight='balanced',
    random_state=42
)
```

Vai trò:

- Baseline mạnh cho text classification.
- Không có probability mặc định, nhưng có `decision_function`.

### 7.3. Multinomial Naive Bayes

Gợi ý:

```python
MultinomialNB()
```

Vai trò:

- Baseline đơn giản, nhanh.
- Chạy tốt với TF-IDF/count features trong nhiều bài text classification.

### 7.4. Random Forest

Gợi ý:

```python
RandomForestClassifier(
    n_estimators=300,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
```

Vai trò:

- Baseline phụ.
- Không kỳ vọng tốt hơn Linear SVM/LogReg trên sparse TF-IDF.

## 8. Evaluation Metrics

Metric chính:

- Macro-F1.

Metric bắt buộc:

- Accuracy.
- Balanced accuracy.
- Macro-F1.
- Weighted-F1.
- Precision cho clickbait.
- Recall cho clickbait.
- F1 cho clickbait.
- ROC-AUC nếu model có probability hoặc decision score.
- PR-AUC nếu model có probability hoặc decision score.
- Confusion matrix.

Lưu ý:

- Accuracy chỉ báo cáo tham khảo, không dùng làm metric chính.
- Với dataset lệch lớp, recall và F1 cho clickbait quan trọng hơn accuracy.

## 9. Evaluation Protocol

### 9.1. Random split benchmark

Input:

- `random_stratified_70_10_20.csv`

Cách chạy:

1. Train trên split `train`.
2. Tune threshold/hyperparameter nếu cần trên `validation`.
3. Report final score trên `test`.

Trong Phase 4:

- Không tune phức tạp.
- Dùng validation để kiểm tra sanity.
- Test result là bảng benchmark chính.

### 9.2. Stratified k-fold

Input:

- `stratified_kfold_5.csv`

Cách chạy:

1. Với mỗi fold `k`, dùng fold `k` làm validation/test fold.
2. Train trên các fold còn lại.
3. Báo cáo mean ± std.

Ưu tiên chạy:

- Simple baselines.
- Logistic Regression.
- Linear SVM.
- Naive Bayes.

Random Forest có thể bỏ khỏi k-fold nếu quá chậm.

### 9.3. Leave-one-source-out

Input:

- `leave_one_source_out.csv`

Cách chạy:

1. Với mỗi `heldout_source`, train trên các source khác.
2. Test trên source được giữ lại.
3. Báo cáo Macro-F1 và F1-clickbait theo source.

Model nên chạy:

- Best Logistic Regression.
- Best Linear SVM.

Không cần chạy toàn bộ model để tiết kiệm thời gian.

### 9.4. Category-held-out

Input:

- `category_heldout.csv`

Cách chạy:

1. Với mỗi `heldout_category`, train trên category còn lại.
2. Test trên category được giữ lại.
3. Báo cáo Macro-F1 và F1-clickbait theo category.

Model nên chạy:

- Best Logistic Regression.
- Best Linear SVM.

## 10. Code Structure trong Notebook

Notebook `ViClickbait_Phase4_Benchmark.ipynb` nên có các section:

1. Config và import.
2. Load Phase 2 features và Phase 3 splits.
3. Utility functions:
   - `get_split_data`
   - `evaluate_predictions`
   - `get_scores`
   - `save_confusion_matrix`
4. Simple baselines.
5. TF-IDF vectorizer builders.
6. Model builders.
7. Random split benchmark.
8. K-fold benchmark.
9. Source-held-out benchmark.
10. Category-held-out benchmark.
11. Feature importance cho Logistic Regression.
12. Export results.
13. Phase 4 summary.

## 11. Các function chính cần implement

### 11.1. `evaluate_model`

Input:

- model pipeline.
- train dataframe.
- test dataframe.
- text column.
- label column.
- model name.
- protocol name.

Output:

- dict metrics.
- prediction dataframe.
- confusion matrix.

### 11.2. `compute_metrics`

Tính:

- accuracy.
- balanced accuracy.
- macro_f1.
- weighted_f1.
- clickbait_precision.
- clickbait_recall.
- clickbait_f1.
- roc_auc nếu có score.
- pr_auc nếu có score.
- confusion matrix.

### 11.3. `build_pipeline`

Input:

- vectorizer type: `word`, `char`, `word_char`.
- classifier type: `logreg`, `svm`, `nb`, `rf`.

Output:

- sklearn pipeline.

### 11.4. `run_random_split_benchmark`

Chạy toàn bộ simple baselines và traditional ML trên random split.

### 11.5. `run_kfold_benchmark`

Chạy một subset model trên 5-fold và export mean ± std.

### 11.6. `run_source_heldout`

Chạy best model trên leave-one-source-out.

### 11.7. `run_category_heldout`

Chạy best model trên category-held-out.

## 12. Feature Importance / Explainability nhẹ trong Phase 4

Chỉ làm cho Logistic Regression.

Output:

- Top n-gram hướng clickbait.
- Top n-gram hướng non-clickbait.

File:

- `output/phase4/feature_importance_logreg.csv`

Mục đích:

- Chuẩn bị cho Phase 6 explainability.
- Cho thấy các lexical cues model học được.

## 13. Kiểm tra chất lượng sau khi chạy

Sau khi chạy Phase 4, cần kiểm tra:

- Random split có đủ 3 split train/validation/test không?
- Label distribution trong mỗi split có hợp lý không?
- Majority baseline có accuracy cao nhưng macro-F1 thấp không?
- Logistic Regression / Linear SVM có vượt heuristic baseline không?
- K-fold mean/std có ổn định không?
- Source-held-out có drop mạnh ở source nào không?
- Category-held-out có drop mạnh ở category nào không?
- Confusion matrix có cho thấy model bỏ sót clickbait nhiều không?

## 14. Kết quả mong đợi

Kỳ vọng thực tế:

- Traditional ML mạnh nhất có thể là Linear SVM hoặc Logistic Regression với char/word+char TF-IDF.
- Accuracy có thể tương đối cao do non-clickbait chiếm đa số.
- Macro-F1 và F1-clickbait mới là chỉ số đáng tin hơn.
- Source-held-out sẽ giảm rõ so với random split nếu source bias mạnh.
- Category-held-out sẽ khó ở các category có tỷ lệ clickbait quá lệch như `Giải trí & Showbiz`, `Sức khỏe & Đời sống`, `Tin tức tổng hợp`.

## 15. Tiêu chí hoàn thành Phase 4

Phase 4 hoàn thành khi có:

- [ ] Notebook `ViClickbait_Phase4_Benchmark.ipynb`.
- [ ] Random split benchmark results.
- [ ] K-fold benchmark results.
- [ ] Source-held-out results.
- [ ] Category-held-out results.
- [ ] Confusion matrices.
- [ ] Prediction file cho random split.
- [ ] Feature importance cho Logistic Regression.
- [ ] Summary file `phase4_summary.md`.

## 16. Không làm trong Phase 4

Không làm:

- Fine-tune PhoBERT.
- Fine-tune XLM-R.
- CNN/BiLSTM.
- LLM prompting.
- Ensemble.
- Full SHAP/LIME/Integrated Gradients.

Các phần này nên tách sang phase sau để notebook Phase 4 gọn, dễ debug và có kết quả baseline rõ ràng.
