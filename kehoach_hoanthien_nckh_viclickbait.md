# Kế hoạch hoàn thiện đề tài NCKH ViClickbait

## 1. Định vị lại đề tài

Sau khi đối chiếu `ROADMAP_VICLICKBAIT.md`, các phase plan và các output hiện có, hướng mạnh nhất của đề tài không phải là "chạy nhiều mô hình nhất có thể". Hướng mạnh hơn, chặt hơn và bám sát repo hơn là:

> Xây dựng một benchmark có khả năng tái lập cho phát hiện clickbait tiếng Việt, đồng thời kiểm tra khả năng khái quát theo nguồn/chủ đề/thời gian và giải thích lỗi dự đoán bằng các dấu hiệu ngôn ngữ.

Tên đề tài nên ưu tiên:

> Phát hiện clickbait tiếng Việt có khả năng khái quát theo miền và giải thích được trên bộ dữ liệu ViClickbait-2025

Tên tiếng Anh:

> Robust and Explainable Benchmarking for Vietnamese Clickbait Detection on ViClickbait-2025

Nếu cần giữ tên hiện tại trong form, nên thêm rõ cụm "khả năng khái quát theo miền" và "phân tích lỗi/giải thích mô hình" vào B1, B2.1 và B2.2.

## 2. Trạng thái hiện tại theo roadmap

| Hạng mục | Trạng thái | Nhận xét |
|---|---|---|
| Research framing | Đã có nền tốt | `PHASE1_RESEARCH_FRAMING.md` đã nêu problem statement, research gap, RQ và thesis. Cần bổ sung citation chính thức. |
| EDA và data audit | Đã làm khá đầy đủ | Phase 2 có checklist, feature table, source/category/time analysis. Cần xuất riêng duplicate groups để dùng trong báo cáo và split. |
| Experimental protocol | Đã có split files | Có random, k-fold, source-held-out, category-held-out, temporal. Nhưng cần xử lý duplicate/group leakage trước khi xem split là final. |
| Traditional ML benchmark | Đã làm tốt | Có rule baseline, TF-IDF word/char/word+char, Logistic Regression, Linear SVM, Naive Bayes, Random Forest. |
| Domain robustness | Đã làm tốt với source/category | Có domain drop và robustness tables. Temporal chưa có kết quả model, chỉ có split/note. |
| Error analysis | Đã làm tốt | Có 100 dòng annotation, cân bằng 50 FP/50 FN, taxonomy hoàn tất. |
| Explainability truyền thống | Đã có | Có feature importance/lexical cues từ Logistic Regression. Cần diễn giải là association, không phải causal explanation. |
| Ablation | Đã có hướng tốt | Có title vs title+lead, word/char, lexical features, masked source cues. Cần viết kết luận thận trọng hơn. |
| FastText/Deep Learning/PLM | Chưa có bằng chứng implementation | Không nên để BiLSTM/PhoBERT/XLM-R là kết quả bắt buộc trong thuyết minh hiện tại. |
| Reproducibility | Còn yếu | Repo hiện chủ yếu là notebook/output; thiếu script tái lập, requirements, README chạy lại, experiment manifest. |

## 3. Phát hiện quan trọng cần xử lý

### 3.1. Duplicate leakage có thể ảnh hưởng benchmark

Kiểm tra nhanh trên `output/phase2/viclickbait_eda_features.csv` và `output/phase3/random_stratified_70_10_20.csv` cho thấy:

- 46 nhóm tiêu đề trùng sau chuẩn hóa đơn giản.
- 23 nhóm tiêu đề trùng rơi qua nhiều split trong random split.
- 41 nhóm tiêu đề trùng xuất hiện ở nhiều nguồn báo khác nhau.
- 8 nhóm tiêu đề trùng có nhãn khác nhau.

Điều này không phá hỏng toàn bộ đề tài, nhưng nếu không xử lý hoặc không báo cáo, hội đồng có thể hỏi về leakage. Đây là điểm nên sửa trước khi chốt kết quả cuối cùng.

Hướng xử lý:

1. Tạo `output/phase2/duplicate_title_groups.csv`.
2. Gán `duplicate_group_id` cho exact/normalized duplicate.
3. Tạo lại random split theo group-aware stratification, đảm bảo cùng group không rơi vào cả train và test.
4. Với near-duplicate, nếu chưa muốn loại bỏ hết, ít nhất tạo sensitivity analysis:
   - benchmark cũ;
   - benchmark sau khi loại/group duplicate;
   - so sánh Macro-F1 và Clickbait F1.
5. Với các nhóm trùng nhưng khác nhãn, đưa vào mục data limitation hoặc label ambiguity.

### 3.2. Temporal split mới có split, chưa có kết quả model

Roadmap đặt RQ về temporal robustness, Phase 3 đã tạo `temporal_chronological_70_10_20.csv`, nhưng output hiện tại chưa có bảng kết quả temporal tương ứng.

Vì `temporal_split_note.json` ghi rõ dữ liệu lệch mạnh về một năm, temporal nên được báo cáo là exploratory. Tuy vậy, chạy baseline chính trên temporal split sẽ giúp đề tài hoàn thiện hơn.

Hướng xử lý:

- Chạy `tfidf_word_logreg`, `tfidf_word_svm` trên temporal split.
- Báo cáo Macro-F1, Clickbait F1, Balanced Accuracy.
- Không diễn giải quá mạnh; chỉ nói đây là kiểm tra bổ sung do phân bố thời gian chưa cân bằng.

### 3.3. Leakage/shortcut baseline còn thiếu

Roadmap có mục source-only, category-only, surface-feature-only baseline. Repo hiện có heuristic và surface profile, nhưng chưa thấy bảng baseline riêng chỉ dùng metadata/surface features để định lượng shortcut.

Hướng xử lý:

- Random split:
  - `source_only_logreg`
  - `category_only_logreg`
  - `source_category_logreg`
  - `surface_features_logreg`
  - `source_category_surface_logreg`
- Không dùng các model này làm mô hình chính. Chỉ dùng để chứng minh dữ liệu có domain shortcut.
- Nếu source/category-only đạt điểm đáng kể, discussion sẽ mạnh hơn: random split dễ lạc quan vì metadata/style có tính dự báo.

### 3.4. Phase 7 kết luận đang hơi mạnh

`phase7_ablation_insights.md` có kết luận như "mô hình thực sự học được cú pháp và ngữ nghĩa" hoặc "robust, không dễ bị bẻ gãy". Với model TF-IDF + Logistic Regression, nên viết thận trọng hơn:

- Không nên nói mô hình "hiểu ngữ nghĩa" theo nghĩa sâu.
- Nên nói "kết quả gợi ý rằng mô hình không chỉ phụ thuộc vào một nhóm source-heavy cues đã mask".
- Mức giảm Macro-F1 từ 0.711 xuống 0.693 khi mask source cues là đáng chú ý nhưng chưa đủ để kết luận mô hình robust toàn diện.

Gợi ý sửa:

> Kết quả masked source cues cho thấy một phần hiệu năng của mô hình phụ thuộc vào các từ/cụm từ đặc thù, nhưng mức suy giảm chưa đủ lớn để xem đây là nguồn tín hiệu duy nhất. Điều này gợi ý mô hình còn khai thác thêm các n-gram và đặc trưng bề mặt khác của tiêu đề clickbait.

## 4. Hướng chỉnh sửa thuyết minh

### 4.1. Chỉnh tên và đóng góp

Nên chuyển đóng góp từ:

> Huấn luyện và so sánh SVM, BiLSTM, PhoBERT, XLM-RoBERTa.

sang:

> Xây dựng benchmark có khả năng tái lập, đánh giá robustness theo source/category/time và phân tích lỗi/lexical cues.

Lý do: đây là phần đã có artefact rõ trong repo và có giá trị nghiên cứu hơn so với chỉ liệt kê nhiều kiến trúc.

### 4.2. Chỉnh research questions

RQ đề xuất:

1. Các baseline TF-IDF + học máy truyền thống đạt hiệu năng như thế nào trên ViClickbait-2025 khi đánh giá bằng Macro-F1 và Clickbait F1?
2. Hiệu năng thay đổi ra sao khi chuyển từ random split sang source-held-out, category-held-out và temporal split?
3. Dataset có tồn tại shortcut theo source/category/surface features không, và các shortcut này ảnh hưởng thế nào đến cách diễn giải benchmark?
4. Các lỗi false positive/false negative thường thuộc nhóm nào, và lexical cues nào có liên hệ mạnh với dự đoán clickbait/non-clickbait?

Nếu muốn giữ PLM:

> RQ mở rộng: Một mô hình tiền huấn luyện tiếng Việt/đa ngữ có cải thiện đáng kể so với baseline truyền thống không, trong điều kiện tính toán cho phép?

### 4.3. Chỉnh mục tiêu

Mục tiêu nên viết theo sản phẩm kiểm chứng được:

1. Xây dựng EDA và data audit cho ViClickbait-2025, bao gồm kiểm tra phân bố nhãn, nguồn, chủ đề, thời gian và duplicate/near-duplicate.
2. Thiết kế protocol đánh giá gồm random stratified split, 5-fold, leave-one-source-out, category-held-out và temporal split dạng exploratory.
3. Huấn luyện các baseline truyền thống dựa trên TF-IDF word/char n-gram và các mô hình Logistic Regression, Linear SVM, Naive Bayes, Random Forest.
4. Đánh giá robustness bằng cách so sánh random split với source/category/temporal held-out.
5. Phân tích lỗi và lexical cues để giải thích xu hướng dự đoán của mô hình.
6. Thử nghiệm mở rộng với FastText hoặc một PLM nếu đủ thời gian/tài nguyên, nhưng không xem là kết quả bắt buộc.

### 4.4. Chỉnh phương pháp

Mỗi lựa chọn phương pháp nên có lý do cụ thể:

- Macro-F1: phù hợp vì clickbait chỉ chiếm khoảng 31%, Accuracy có thể che giấu lỗi ở lớp clickbait.
- Source-held-out: kiểm tra mô hình có hoạt động trên nguồn báo chưa thấy hay chỉ học phong cách biên tập.
- Category-held-out: kiểm tra mô hình có phụ thuộc vào chủ đề, vì clickbait rate khác nhau mạnh giữa category.
- Temporal split: kiểm tra sơ bộ khả năng ổn định theo thời gian, nhưng chỉ báo cáo exploratory do phân bố thời gian lệch.
- Word/char TF-IDF: word n-gram nắm cụm từ, char n-gram hỗ trợ biến thể chính tả và tiếng Việt có dấu.
- Logistic Regression/Linear SVM: baseline mạnh cho sparse text và có thể phân tích trọng số đặc trưng.
- Error taxonomy: giúp biến bảng metric thành nhận xét nghiên cứu về loại tiêu đề mà mô hình hay nhầm.

### 4.5. Chỉnh kết quả dự kiến

B3 nên có các sản phẩm sau:

1. Báo cáo tổng kết đề tài.
2. Bộ notebook/source code tái lập EDA, split, benchmark, robustness, error analysis và ablation.
3. Bộ split protocol, gồm group-aware random split nếu đã xử lý duplicate.
4. Bảng benchmark random/k-fold.
5. Bảng robustness source/category/temporal.
6. Bảng leakage/shortcut baseline.
7. Bảng error taxonomy, case studies và lexical cues.
8. Phụ lục limitations và reproducibility checklist.

## 5. Backlog implement tiếp theo

### P0 - Việc nên làm ngay

#### P0.1. Tạo duplicate/group-aware split

Mục tiêu:

- Loại hoặc kiểm soát duplicate leakage trước khi chốt kết quả.

Output nên có:

- `output/phase2/duplicate_title_groups.csv`
- `output/phase3/random_group_stratified_70_10_20.csv`
- `output/phase3/split_leakage_audit.json`
- `output/phase4_groupaware/random_split_results.csv`
- `output/phase4_groupaware/phase4_summary.md`

Tiêu chí hoàn thành:

- Không có duplicate group nào xuất hiện đồng thời ở train/validation/test.
- Có bảng so sánh kết quả trước và sau khi group-aware split.
- Nếu điểm giảm, dùng như một insight về leakage sensitivity.

#### P0.2. Viết README tái lập

Repo hiện đã có nhiều output tốt nhưng thiếu hướng dẫn chạy lại. Cần thêm:

- `README.md`
- `requirements.txt` hoặc `environment.yml`
- `REPRODUCIBILITY.md`

Nội dung tối thiểu:

- Dữ liệu đầu vào nằm ở đâu.
- Thứ tự chạy notebook/phase.
- Python version và package chính.
- Seed cố định.
- Output kỳ vọng của từng phase.
- Cảnh báo temporal split exploratory.
- Cảnh báo không dùng metadata làm feature chính.

#### P0.3. Chỉnh thuyết minh để không over-claim PLM/BiLSTM

Trong `thuyetminh_detai.md`:

- Đưa BiLSTM/PhoBERT/XLM-R xuống nhánh mở rộng hoặc future work.
- Không viết "huấn luyện thành công" nếu chưa có output.
- Không viết "tối ưu nhất"; dùng "phù hợp nhất trong phạm vi protocol".
- Thêm source/category robustness vào contribution chính.

### P1 - Việc làm để đề tài chặt hơn

#### P1.1. Implement leakage/shortcut baselines

Output nên có:

- `output/phase8_leakage/leakage_random_split_results.csv`
- `output/phase8_leakage/leakage_summary.md`

Các baseline:

- Source-only.
- Category-only.
- Source + category.
- Surface features only.
- Source + category + surface features.

Ý nghĩa trong báo cáo:

- Nếu các baseline này đạt điểm không thấp, có bằng chứng rằng dataset chứa shortcut theo metadata/style.
- Kết quả này trực tiếp trả lời RQ3.

#### P1.2. Chạy temporal baseline

Output nên có:

- `output/phase8_temporal/temporal_results.csv`
- `output/phase8_temporal/temporal_summary.md`

Mô hình tối thiểu:

- `tfidf_word_logreg`
- `tfidf_word_svm`
- `keyword_heuristic`

Cách viết:

- Không xem temporal là kết luận chính.
- Dùng như kiểm tra bổ sung vì dữ liệu lệch theo thời gian.

#### P1.3. Rà lại Phase 7 ablation

Output nên cập nhật:

- `output/phase7/phase7_ablation_insights.md`

Việc cần chỉnh:

- Thêm Clickbait F1 trung bình cho source-held-out, không chỉ Macro-F1.
- Bổ sung per-source variance hoặc bảng source khó nhất.
- Giảm các claim như "mô hình hiểu ngữ nghĩa".
- Nêu rõ lexical features cải thiện Macro-F1 nhưng Clickbait F1 random split có thể không tăng tương ứng.

#### P1.4. Tạo report skeleton

Nên tạo:

- `report_outline.md`
- hoặc `paper_draft.md`

Cấu trúc:

1. Introduction.
2. Related Work.
3. Dataset and EDA.
4. Methodology.
5. Experimental Protocol.
6. Results.
7. Robustness Analysis.
8. Error Analysis and Lexical Cues.
9. Ablation.
10. Limitations.
11. Conclusion.

### P2 - Việc nên làm nếu còn thời gian

#### P2.1. FastText baseline

FastText là baseline hợp lý hơn BiLSTM nếu muốn thêm một mô hình "nhẹ nhưng khác TF-IDF".

Lý do:

- Nhanh.
- Thực dụng cho text classification.
- Có giá trị so sánh giữa bag-of-subwords và TF-IDF.

Chỉ nên làm nếu môi trường cài đặt ổn. Nếu mất nhiều thời gian vì dependency, bỏ qua và ghi future work.

#### P2.2. Một PLM duy nhất

Nếu có GPU/Colab, chỉ nên chọn một:

- PhoBERT-base nếu muốn nhấn mạnh tiếng Việt.
- XLM-RoBERTa-base nếu muốn mô hình đa ngữ dễ chạy tokenizer hơn trong một số setting.

Protocol tối thiểu:

- Random split 3 seed hoặc 1 seed nếu compute hạn chế nhưng phải ghi limitation.
- Không cần full source-held-out cho PLM nếu compute quá lớn.
- Báo cáo training config: batch size, learning rate, max length, epoch, seed, hardware.

Không nên làm BiLSTM nếu thời gian ngắn. Với dataset 3.414 mẫu, BiLSTM từ đầu dễ overfit và giá trị nghiên cứu thấp hơn leakage/temporal/group-aware split.

#### P2.3. Bootstrap confidence interval

Nếu muốn tăng độ học thuật:

- Bootstrap test predictions để lấy 95% CI cho Macro-F1/Clickbait F1.
- Dùng cho best model vs runner-up, hoặc random split vs group-aware split.

Không bắt buộc cho NCKH sinh viên, nhưng làm được thì báo cáo chặt hơn.

## 6. Thứ tự triển khai khuyến nghị

### Sprint 1: Làm benchmark sạch hơn

1. Tạo duplicate groups.
2. Tạo group-aware random split.
3. Rerun traditional ML baseline trên group-aware split.
4. So sánh kết quả cũ/mới.

### Sprint 2: Đóng lỗ hổng trong roadmap

1. Chạy leakage/shortcut baselines.
2. Chạy temporal baseline dạng exploratory.
3. Cập nhật phase summaries.

### Sprint 3: Chỉnh narrative

1. Chỉnh `thuyetminh_detai.md`.
2. Chỉnh `phase7_ablation_insights.md` để giảm claim mạnh.
3. Tạo `paper_draft.md` hoặc `report_outline.md`.
4. Thêm limitations rõ ràng.

### Sprint 4: Reproducibility

1. Tạo README/requirements.
2. Gom các notebook theo thứ tự chạy.
3. Nếu có thời gian, tách utility thành script.
4. Tạo checklist "run from scratch".

### Sprint 5: Optional extension

1. Chạy FastText hoặc một PLM.
2. Nếu không chạy được, đưa vào future work thay vì cố nhét vào kết quả chính.

## 7. Definition of Done cho đề tài

Đề tài có thể xem là hoàn chỉnh khi có đủ:

- Thuyết minh không hứa các mô hình chưa làm.
- Research questions khớp với output thật.
- EDA có data risk và duplicate/near-duplicate audit.
- Split final có kiểm soát duplicate leakage hoặc có sensitivity analysis.
- Benchmark chính có random/k-fold.
- Robustness có source/category và temporal exploratory.
- Có leakage/shortcut baselines.
- Có error taxonomy 100 mẫu và case studies.
- Có lexical cue analysis.
- Có ablation và kết luận thận trọng.
- Có limitations rõ.
- Có README/requirements để người khác chạy lại.

## 8. Những thứ không nên ưu tiên

- Không nên mở rộng multimodal thumbnail.
- Không nên cố làm nhiều deep learning model từ đầu.
- Không nên biến PLM thành lời hứa bắt buộc nếu chưa có GPU và output.
- Không nên claim mô hình tổng quát cho toàn bộ báo chí tiếng Việt.
- Không nên dùng Accuracy làm metric chính.
- Không nên dùng `source`, `category`, `publish_datetime` làm feature của mô hình chính.

## 9. Câu chuyện nghiên cứu nên chốt

Luận điểm trung tâm:

> Với phát hiện clickbait tiếng Việt, kết quả trên random split chưa đủ để kết luận mô hình tốt. Một benchmark chặt chẽ cần kiểm tra domain shift theo nguồn/chủ đề/thời gian, kiểm soát shortcut/leakage và phân tích lỗi để hiểu mô hình dựa vào dấu hiệu nào.

Câu chuyện này khớp với roadmap, khớp với repo hiện tại và đủ sức thành một đề tài NCKH sinh viên chỉn chu.

