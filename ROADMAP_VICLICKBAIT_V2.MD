# ROADMAP V2: Hoàn thiện đề tài NCKH ViClickbait

## 0. Mục tiêu của roadmap V2

Roadmap V2 chỉ tập trung vào những việc còn lại để đưa đề tài NCKH về trạng thái hoàn chỉnh, chỉn chu và có thể bảo vệ được trước phản biện.

Luận điểm trung tâm cần giữ xuyên suốt:

> Trong phát hiện clickbait tiếng Việt, kết quả trên random split chưa đủ để kết luận mô hình tốt. Một benchmark chặt chẽ cần kiểm tra khả năng khái quát theo nguồn/chủ đề/thời gian, kiểm soát shortcut/leakage và phân tích lỗi để hiểu mô hình dựa vào dấu hiệu nào.

Định vị đề tài nên dùng:

> Phát hiện clickbait tiếng Việt có khả năng khái quát theo miền và giải thích được trên bộ dữ liệu ViClickbait-2025.

Tên tiếng Anh gợi ý:

> Robust and Explainable Benchmarking for Vietnamese Clickbait Detection on ViClickbait-2025.

## 1. Trạng thái hiện tại

### Đã có nền tốt

- Research framing: problem statement, research gap, RQ, contribution statement.
- EDA: schema, missing values, label/source/category/time distribution, title/lead features, duplicate/near-duplicate audit.
- Split protocol: random stratified, k-fold, leave-one-source-out, category-held-out, temporal chronological.
- Traditional ML benchmark: rule baselines, TF-IDF word/char/word+char, Logistic Regression, Linear SVM, Naive Bayes, Random Forest.
- Domain robustness: source-held-out và category-held-out.
- Error analysis: 100 lỗi được annotate, cân bằng 50 FP/50 FN.
- Explainability truyền thống: Logistic Regression feature cues.
- Ablation: title vs title+lead, word vs char, lexical features, masked source cues.

### Còn thiếu để "all done"

- Duplicate/group leakage chưa được kiểm soát trong split cuối.
- Chưa có group-aware split và sensitivity analysis sau khi xử lý duplicate.
- Chưa có leakage/shortcut baselines source-only/category-only/surface-only.
- Chưa có kết quả model trên temporal split.
- Chưa có README/requirements/reproducibility checklist.
- Thuyết minh hiện còn over-claim BiLSTM/PhoBERT/XLM-R so với output thật.
- Phase 7 ablation cần giảm một số kết luận mạnh.
- Chưa có report/paper skeleton cuối để gom toàn bộ kết quả thành câu chuyện nghiên cứu mạch lạc.

## 2. Nguyên tắc hoàn thiện

- Không dùng Accuracy làm metric chính.
- Không dùng `source`, `category`, `publish_datetime` làm feature của mô hình chính.
- Không claim mô hình tổng quát cho toàn bộ báo chí tiếng Việt.
- Không hứa BiLSTM/PhoBERT/XLM-R nếu chưa có output thật.
- Không diễn giải feature coefficient là nguyên nhân; chỉ gọi là lexical association.
- Temporal split chỉ báo cáo exploratory nếu dữ liệu lệch mạnh theo thời gian.
- Mỗi kết luận cần gắn với một bảng, file output hoặc case study cụ thể.

## 3. Phase V2.1 - Duplicate Leakage Control

### Mục tiêu

Kiểm soát rủi ro duplicate leakage trước khi chốt benchmark cuối.

Kiểm tra hiện tại cho thấy:

- 46 nhóm tiêu đề trùng sau chuẩn hóa đơn giản.
- 23 nhóm tiêu đề trùng rơi qua nhiều split trong random split.
- 41 nhóm tiêu đề trùng xuất hiện ở nhiều nguồn báo.
- 8 nhóm tiêu đề trùng có nhãn khác nhau.

### Việc cần làm

1. Tạo duplicate group cho exact/normalized duplicate.
2. Xuất danh sách duplicate groups.
3. Audit các nhóm duplicate:
   - cùng nhãn hay khác nhãn;
   - cùng source hay khác source;
   - đang rơi vào cùng split hay nhiều split.
4. Tạo random split mới theo group-aware stratification.
5. Kiểm tra không có group nào rơi đồng thời vào train/validation/test.
6. Rerun traditional ML benchmark trên split mới.
7. So sánh kết quả split cũ và group-aware split.

### Output cần có

- `output/phase2/duplicate_title_groups.csv`
- `output/phase3/random_group_stratified_70_10_20.csv`
- `output/phase3/split_leakage_audit.json`
- `output/phase4_groupaware/random_split_results.csv`
- `output/phase4_groupaware/phase4_summary.md`
- `output/phase4_groupaware/groupaware_vs_original_comparison.csv`

### Tiêu chí hoàn thành

- Không có duplicate group xuất hiện ở nhiều split trong split mới.
- Có bảng kết quả benchmark sau group-aware split.
- Có bảng so sánh Macro-F1, Clickbait F1, Balanced Accuracy giữa split cũ và split mới.
- Có đoạn thảo luận trong report: duplicate leakage có/không làm kết quả random split lạc quan hơn.

## 4. Phase V2.2 - Shortcut / Leakage Baselines

### Mục tiêu

Định lượng mức độ dataset có thể chứa shortcut theo source, category và surface features.

### Baseline cần chạy

Các baseline này chỉ dùng cho phân tích leakage, không dùng làm mô hình chính:

- `source_only_logreg`
- `category_only_logreg`
- `source_category_logreg`
- `surface_features_logreg`
- `source_category_surface_logreg`

Surface features có thể gồm:

- `title_char_len`
- `title_word_len`
- `title_n_question`
- `title_n_exclaim`
- `title_n_number`
- `title_n_cb_keywords`
- `title_n_ambiguous_cues`
- `title_n_curiosity_gap_cues`
- `title_starts_with_num`
- `title_has_superlative`
- `title_has_quote`
- `lead_char_len`
- `lead_word_len`

### Output cần có

- `output/phase8_leakage/leakage_random_split_results.csv`
- `output/phase8_leakage/leakage_groupaware_results.csv` nếu đã có group-aware split.
- `output/phase8_leakage/leakage_summary.md`

### Tiêu chí hoàn thành

- Có bảng metric cho từng shortcut baseline.
- Có nhận xét baseline nào đáng lo nhất.
- Có kết luận rõ: metadata/surface feature chỉ dùng để audit bias, không dùng trong mô hình chính.
- Trả lời được RQ: mô hình có thể học shortcut theo source/category/surface style không?

## 5. Phase V2.3 - Temporal Baseline

### Mục tiêu

Chạy kết quả mô hình trên temporal split để hoàn thiện phần robustness theo thời gian.

### Mô hình tối thiểu

- `keyword_heuristic`
- `tfidf_word_logreg`
- `tfidf_word_svm`

### Lưu ý diễn giải

Temporal split phải được viết là exploratory vì `temporal_split_note.json` cho thấy dữ liệu lệch mạnh về năm 2025 và có 31 mẫu thiếu datetime.

### Output cần có

- `output/phase8_temporal/temporal_results.csv`
- `output/phase8_temporal/temporal_summary.md`

### Tiêu chí hoàn thành

- Có Macro-F1, Clickbait Precision, Clickbait Recall, Clickbait F1, Balanced Accuracy.
- Có so sánh với random split.
- Có limitation rõ: temporal chưa đủ cân bằng để kết luận mạnh về drift theo thời gian.

## 6. Phase V2.4 - Refresh Benchmark Tables

### Mục tiêu

Gom lại các bảng paper-ready cuối cùng sau khi có duplicate control, leakage baseline và temporal baseline.

### Bảng cần có

- Random benchmark gốc.
- Group-aware benchmark.
- K-fold summary.
- Source-held-out robustness.
- Category-held-out robustness.
- Temporal exploratory results.
- Leakage/shortcut baselines.
- Ablation results.
- Error taxonomy.
- Lexical cues.
- Case studies.

### Output cần có

- `output/final_tables/table_random_benchmark.csv`
- `output/final_tables/table_groupaware_benchmark.csv`
- `output/final_tables/table_kfold_summary.csv`
- `output/final_tables/table_domain_robustness.csv`
- `output/final_tables/table_temporal_results.csv`
- `output/final_tables/table_leakage_baselines.csv`
- `output/final_tables/table_ablation.csv`
- `output/final_tables/table_error_taxonomy.csv`
- `output/final_tables/table_feature_cues.csv`
- `output/final_tables/case_studies.csv`
- `output/final_tables/final_discussion_points.md`

### Tiêu chí hoàn thành

- Mỗi bảng có tên cột sạch, dễ đưa vào báo cáo.
- Bảng chính không đặt Accuracy làm metric đầu tiên.
- Có `final_discussion_points.md` trả lời trực tiếp từng RQ.

## 7. Phase V2.5 - Chỉnh thuyết minh đề tài

### Mục tiêu

Làm `thuyetminh_detai.md` khớp với repo thật và roadmap cuối.

### Việc cần sửa

1. Chỉnh tên/định vị đề tài theo hướng robust + explainable benchmark.
2. Hạ BiLSTM/PhoBERT/XLM-R xuống nhánh mở rộng hoặc future work.
3. Thêm source/category/temporal robustness vào contribution chính.
4. Thêm leakage/shortcut analysis vào phương pháp.
5. Điền phần "Phân chia dữ liệu" đang bỏ trống.
6. Đổi metric chính thành Macro-F1 và Clickbait F1.
7. Thêm kế hoạch B nếu không đủ GPU hoặc mô hình mở rộng không cải thiện.
8. Chuyển kế hoạch B2.3 thành bảng có thành viên phụ trách.
9. Bổ sung kết quả dự kiến:
   - split protocol;
   - benchmark tables;
   - robustness tables;
   - leakage baselines;
   - error taxonomy;
   - lexical cues;
   - reproducibility package.
10. Bổ sung citation nội dòng và sửa B4 theo IEEE.

### Output cần có

- `thuyetminh_detai.md` được chỉnh.
- Có thể thêm `thuyetminh_detai_revised.md` nếu muốn giữ bản gốc.

### Tiêu chí hoàn thành

- Không còn câu hứa chắc "huấn luyện thành công 4 mô hình" nếu chưa có output.
- Không còn claim "tối ưu nhất" hoặc "tiên tiến nhất" không có căn cứ.
- Mỗi phương pháp được giải thích bằng lý do cụ thể.
- B3 khớp với B2.1.
- Nội dung bám sát artefact thật trong repo.

## 8. Phase V2.6 - Chỉnh Phase 7 Ablation Narrative

### Mục tiêu

Giữ giá trị của ablation nhưng giảm claim quá mạnh.

### Việc cần sửa

1. Thêm Clickbait F1 trung bình cho source-held-out nếu có dữ liệu.
2. Bổ sung per-source variance hoặc source khó nhất.
3. Không viết model "hiểu ngữ nghĩa" với TF-IDF + Logistic Regression.
4. Viết masked source cues theo hướng "gợi ý" thay vì "chứng minh chắc".
5. Nêu rõ lexical features cải thiện Macro-F1 source-held-out nhưng không nhất thiết cải thiện mọi metric.

### Output cần có

- `output/phase7/phase7_ablation_insights.md` cập nhật.
- Nếu cần, thêm `output/phase7/phase7_ablation_summary_for_report.md`.

### Tiêu chí hoàn thành

- Kết luận thận trọng, đúng dữ liệu.
- Không claim robust toàn diện.
- Ablation trả lời được: input/context/feature nào giúp generalization hơn.

## 9. Phase V2.7 - Report / Paper Skeleton

### Mục tiêu

Tạo khung báo cáo cuối để gom toàn bộ kết quả thành một câu chuyện nghiên cứu.

### Output cần có

- `report_outline.md`
- hoặc `paper_draft.md`

### Cấu trúc đề xuất

1. Introduction.
2. Related Work.
3. Dataset and Exploratory Analysis.
4. Experimental Protocol.
5. Baseline Models.
6. Random and K-fold Benchmark.
7. Domain Robustness Analysis.
8. Temporal Robustness Exploratory Study.
9. Shortcut and Leakage Analysis.
10. Error Analysis and Lexical Cues.
11. Ablation Study.
12. Discussion.
13. Limitations.
14. Conclusion.

### Nội dung bắt buộc trong Discussion

- Random split cho biết gì và không cho biết gì.
- Source/category-held-out làm lộ rủi ro domain shift như thế nào.
- Duplicate/group-aware split ảnh hưởng benchmark ra sao.
- Metadata/surface shortcut có mạnh không.
- Mô hình hay mắc FP/FN ở nhóm tiêu đề nào.
- Lexical cues nào liên hệ với clickbait tiếng Việt.
- Vì sao không claim tổng quát cho toàn bộ báo chí tiếng Việt.

### Tiêu chí hoàn thành

- Mỗi RQ có một đoạn trả lời.
- Mỗi contribution có output chứng minh.
- Limitations được viết thẳng thắn.
- Không có bảng nào chỉ báo cáo Accuracy.

## 10. Phase V2.8 - Reproducibility Package

### Mục tiêu

Đảm bảo người khác có thể hiểu và chạy lại pipeline.

### File cần tạo

- `README.md`
- `requirements.txt` hoặc `environment.yml`
- `REPRODUCIBILITY.md`
- `EXPERIMENT_MANIFEST.md`

### README cần có

- Mục tiêu đề tài.
- Cấu trúc repo.
- Thứ tự chạy phase.
- Dữ liệu đầu vào.
- Output chính.
- Cách đọc kết quả.
- Cảnh báo privacy nếu repo có thông tin cá nhân.

### REPRODUCIBILITY cần có

- Python version.
- Package chính.
- Random seed.
- Hardware nếu có.
- Cách tạo split.
- Cách rerun benchmark.
- Cách kiểm tra output.
- Những kết quả nào là exploratory.

### Tiêu chí hoàn thành

- Người khác nhìn repo biết chạy file nào trước.
- Không phụ thuộc vào trí nhớ của người làm đề tài.
- Có checklist để kiểm tra output sau khi chạy.

## 11. Phase V2.9 - Optional Extension

### Chỉ làm nếu còn thời gian

Ưu tiên optional theo thứ tự:

1. FastText baseline.
2. Một PLM duy nhất: PhoBERT-base hoặc XLM-RoBERTa-base.
3. Bootstrap confidence interval.

### Không nên ưu tiên

- BiLSTM từ đầu.
- Nhiều PLM cùng lúc.
- Multimodal thumbnail.
- LLM prompting.
- Dataset expansion lớn.

### Điều kiện để đưa optional vào báo cáo chính

- Có notebook/script chạy lại được.
- Có training config.
- Có output metric đầy đủ.
- Có limitation nếu chỉ chạy 1 seed.
- Không làm yếu câu chuyện chính robustness + explainability.

Nếu optional chưa đủ chắc, đưa vào Future Work.

## 12. Thứ tự thực hiện khuyến nghị

### Sprint 1 - Làm benchmark sạch hơn

- [x] Tạo duplicate groups.
- [x] Audit duplicate leakage.
- [x] Tạo group-aware random split.
- [x] Rerun benchmark truyền thống trên group-aware split.
- [x] Viết comparison summary.

### Sprint 2 - Đóng lỗ hổng robustness/shortcut

- [ ] Chạy leakage/shortcut baselines.
- [ ] Chạy temporal baseline.
- [ ] Refresh final tables.
- [ ] Viết discussion points theo RQ.

### Sprint 3 - Chỉnh narrative và thuyết minh

- [ ] Chỉnh `thuyetminh_detai.md`.
- [ ] Chỉnh `phase7_ablation_insights.md`.
- [ ] Tạo `report_outline.md` hoặc `paper_draft.md`.
- [ ] Viết limitations rõ ràng.

### Sprint 4 - Reproducibility

- [ ] Tạo `README.md`.
- [ ] Tạo `requirements.txt` hoặc `environment.yml`.
- [ ] Tạo `REPRODUCIBILITY.md`.
- [ ] Tạo `EXPERIMENT_MANIFEST.md`.

### Sprint 5 - Optional

- [ ] FastText baseline nếu dependency ổn.
- [ ] Một PLM duy nhất nếu có GPU.
- [ ] Bootstrap CI nếu còn thời gian.

## 13. Checklist "All Done"

### Nội dung nghiên cứu

- [ ] Research questions cuối cùng đã chốt.
- [ ] Thuyết minh khớp với output thật.
- [ ] Related work có citation chính thức.
- [ ] Contribution không chỉ là chạy model.

### Dữ liệu

- [ ] EDA đầy đủ.
- [ ] Duplicate groups được xuất file.
- [ ] Duplicate leakage được audit.
- [ ] Label/source/category/time bias được mô tả.
- [ ] Temporal limitation được ghi rõ.

### Protocol

- [ ] Random split.
- [ ] Group-aware random split.
- [ ] K-fold.
- [ ] Source-held-out.
- [ ] Category-held-out.
- [ ] Temporal exploratory split.
- [ ] Metric config.
- [ ] Không tune trên test set.

### Models

- [ ] Majority baseline.
- [ ] Random baseline.
- [ ] Keyword heuristic.
- [ ] Length heuristic.
- [ ] TF-IDF + Logistic Regression.
- [ ] TF-IDF + Linear SVM.
- [ ] TF-IDF + Naive Bayes.
- [ ] TF-IDF + Random Forest.
- [ ] Optional FastText/PLM chỉ nếu có output thật.

### Robustness

- [ ] Source-held-out results.
- [ ] Category-held-out results.
- [ ] Temporal exploratory results.
- [ ] Random vs held-out drop analysis.
- [ ] Group-aware sensitivity analysis.

### Leakage / Shortcut

- [ ] Source-only baseline.
- [ ] Category-only baseline.
- [ ] Source+category baseline.
- [ ] Surface-only baseline.
- [ ] Shortcut summary.

### Explainability / Error Analysis

- [ ] Feature cues.
- [ ] Error taxonomy.
- [ ] 50 FP + 50 FN annotated.
- [ ] Case studies.
- [ ] Coefficient được diễn giải là association.

### Ablation

- [ ] Title vs title+lead.
- [ ] Word vs char vs word+char.
- [ ] TF-IDF vs TF-IDF + lexical features.
- [ ] Masked source cues.
- [ ] Kết luận thận trọng.

### Report

- [ ] Paper/report skeleton.
- [ ] Final tables.
- [ ] Discussion trả lời từng RQ.
- [ ] Limitations.
- [ ] Conclusion.

### Reproducibility

- [ ] README.
- [ ] Requirements/environment.
- [ ] Reproducibility guide.
- [ ] Experiment manifest.
- [ ] Output paths rõ ràng.

## 14. Definition of Done

Đề tài được xem là "all done" khi:

1. Có thuyết minh không over-claim và bám sát repo.
2. Có benchmark chính đủ tái lập.
3. Có kiểm soát hoặc phân tích duplicate leakage.
4. Có robustness theo source/category và temporal exploratory.
5. Có leakage/shortcut baseline để trả lời RQ về bias.
6. Có error taxonomy và lexical cue analysis.
7. Có ablation trả lời thành phần nào giúp generalization.
8. Có limitations thẳng thắn.
9. Có README/reproducibility để người khác chạy lại.
10. Có report/paper skeleton gom toàn bộ kết quả thành một câu chuyện nghiên cứu thống nhất.
