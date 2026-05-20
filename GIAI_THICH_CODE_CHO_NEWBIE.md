# Giải thích code hiện tại cho newbie

## 1. Nội dung này đang nói về điều gì?

Repo này đang xây dựng một đề tài NCKH về **phát hiện tiêu đề clickbait tiếng Việt** trên bộ dữ liệu **ViClickbait-2025**.

Nói đơn giản: nhóm không chỉ muốn hỏi "mô hình nào dự đoán đúng nhất?", mà còn muốn hỏi thêm:

- Mô hình có thật sự học dấu hiệu clickbait không?
- Hay mô hình chỉ học "đường tắt" như nguồn báo, chủ đề, độ dài tiêu đề?
- Nếu đem mô hình sang nguồn báo hoặc chủ đề khác, điểm có giảm không?
- Khi mô hình sai, nó thường sai vì loại tiêu đề nào?

Những gì repo hiện đã làm có thể chia thành các phần:

- **Phase 1:** xác định vấn đề nghiên cứu, khoảng trống, câu hỏi nghiên cứu.
- **Phase 2:** phân tích dữ liệu và kiểm tra rủi ro dữ liệu.
- **Phase 3:** tạo các cách chia dữ liệu để đánh giá công bằng.
- **Phase 4:** chạy benchmark bằng các mô hình học máy truyền thống.
- **Phase 5:** phân tích robustness, lỗi dự đoán và lexical cues.
- **Phase 6:** tổng hợp bảng kết quả sẵn sàng đưa vào báo cáo.
- **Phase 7:** làm ablation để xem thành phần nào giúp mô hình tốt hơn.
- **Sprint 1 V2:** kiểm soát duplicate leakage bằng group-aware split và rerun benchmark.

## 2. Diễn giải lại bằng ngôn ngữ đơn giản

### Dịch nghĩa câu chữ

Repo này đang thử nhiều cách để máy tính phân biệt một tiêu đề báo là **clickbait** hay **non-clickbait**. Đầu vào chính là tiêu đề bài báo. Đầu ra là nhãn `1` cho clickbait và `0` cho non-clickbait.

### Giải thích bản chất

Đề tài không dừng ở việc "ném dữ liệu vào model rồi lấy điểm". Repo đang cố làm một benchmark có tính nghiên cứu hơn bằng cách:

1. Kiểm tra dữ liệu trước khi train.
2. Chia dữ liệu theo nhiều cách để tránh kết luận quá dễ.
3. Chạy các baseline đơn giản và mô hình học máy truyền thống.
4. So sánh model trên random split và domain-held-out split.
5. Phân tích vì sao model sai.
6. Kiểm tra model có học shortcut không.
7. Kiểm tra duplicate có làm benchmark bị lạc quan không.

Ví dụ rất đơn giản:

Nếu nhiều tiêu đề từ Kênh14 là clickbait và nhiều tiêu đề từ VnExpress là non-clickbait, mô hình có thể chỉ học "thấy văn phong giống Kênh14 thì đoán clickbait", thay vì thật sự hiểu dấu hiệu clickbait. Repo này đang cố phát hiện và kiểm soát rủi ro đó.

## 3. Giải thích các thuật ngữ / khái niệm khó

### Clickbait

Clickbait là tiêu đề được viết để kích thích người đọc bấm vào, thường bằng cách gây tò mò, phóng đại, che giấu thông tin chính hoặc dùng từ gây sốc.

Ví dụ:

- "Cô gái này làm một điều khiến ai cũng bất ngờ"
- "Sự thật phía sau hành động của nam ca sĩ khiến dân mạng sốc"

### ViClickbait-2025

Đây là bộ dữ liệu tiếng Việt dùng trong đề tài. Mỗi mẫu thường có tiêu đề, đoạn lead, nguồn báo, chủ đề, thời gian đăng và nhãn clickbait/non-clickbait.

Trong repo hiện tại, file feature chính là:

- `output/phase2/viclickbait_eda_features.csv`

### EDA

EDA là viết tắt của **Exploratory Data Analysis**, nghĩa là phân tích dữ liệu ban đầu.

Trong repo, EDA dùng để xem:

- Có bao nhiêu mẫu?
- Tỷ lệ clickbait là bao nhiêu?
- Nguồn báo nào có nhiều clickbait?
- Chủ đề nào dễ có clickbait?
- Tiêu đề clickbait có dài hơn không?
- Có duplicate hoặc near-duplicate không?

### Benchmark

Benchmark là một bộ thí nghiệm chuẩn để so sánh nhiều mô hình trên cùng dữ liệu, cùng split và cùng metric.

Trong repo, benchmark chính nằm ở Phase 4 và output như:

- `output/phase4/random_split_results.csv`
- `output/phase4/kfold_results.csv`
- `output/phase4/source_heldout_results.csv`
- `output/phase4/category_heldout_results.csv`

### Baseline

Baseline là mốc so sánh cơ bản. Nếu mô hình phức tạp không vượt baseline thì mô hình đó chưa thuyết phục.

Repo có các baseline như:

- Majority class: luôn đoán lớp nhiều nhất.
- Random stratified: đoán ngẫu nhiên theo tỷ lệ nhãn.
- Length heuristic: dựa vào độ dài tiêu đề.
- Keyword heuristic: dựa vào từ khóa như "bất ngờ", "sốc", "lý do".
- TF-IDF + Logistic Regression/SVM/Naive Bayes/Random Forest.

### TF-IDF

TF-IDF là cách biến văn bản thành số. Nó cho biết một từ hoặc cụm từ quan trọng đến mức nào trong văn bản.

Ví dụ: nếu từ "bất ngờ" xuất hiện nhiều trong tiêu đề clickbait nhưng không xuất hiện nhiều trong tiêu đề thường, TF-IDF có thể giúp model chú ý đến từ đó.

### Logistic Regression

Đây là mô hình học máy dùng để phân loại. Trong repo, Logistic Regression mạnh vì:

- chạy nhanh;
- hợp với dữ liệu văn bản dạng TF-IDF;
- có hệ số để xem từ nào nghiêng về clickbait hoặc non-clickbait.

### Linear SVM

SVM là mô hình phân loại cố tìm đường ranh giới giữa hai lớp. Với văn bản TF-IDF, Linear SVM thường là baseline mạnh.

### Random Forest và Naive Bayes

Random Forest là mô hình gồm nhiều cây quyết định. Naive Bayes là mô hình xác suất đơn giản. Trong repo, hai mô hình này dùng làm baseline phụ để so sánh.

### Random split

Random split là chia dữ liệu ngẫu nhiên thành train/validation/test. Repo dùng tỷ lệ 70/10/20.

Rủi ro: nếu các tiêu đề giống nhau hoặc cùng phong cách nguồn báo rơi vào cả train và test, điểm có thể cao hơn thực tế.

### K-fold

K-fold chia dữ liệu thành nhiều phần. Mỗi lần dùng một phần để test/validation, các phần còn lại để train. Repo dùng 5-fold để xem kết quả có ổn định không.

### Source-held-out

Source-held-out nghĩa là giữ lại một nguồn báo làm test, train trên các nguồn còn lại.

Ví dụ: train trên 7 nguồn, test riêng trên VnExpress.

Mục đích: kiểm tra model có dùng được trên nguồn báo chưa từng thấy không.

### Category-held-out

Category-held-out nghĩa là giữ lại một chủ đề làm test, train trên các chủ đề còn lại.

Ví dụ: train trên các chủ đề khác, test trên "Giải trí & Showbiz".

Mục đích: kiểm tra model có bị phụ thuộc vào chủ đề không.

### Temporal split

Temporal split là chia theo thời gian: dữ liệu cũ để train, dữ liệu mới để test.

Trong repo, temporal split chỉ nên xem là exploratory vì dữ liệu lệch mạnh về năm 2025.

### Leakage

Leakage là khi thông tin từ test vô tình lọt vào train hoặc model học một tín hiệu không nên dùng.

Ví dụ: cùng một tiêu đề xuất hiện ở train và test. Khi đó model không thật sự tổng quát, nó có thể chỉ "nhớ lại" tiêu đề đã thấy.

### Duplicate leakage

Duplicate leakage là leakage do tiêu đề trùng hoặc gần trùng rơi vào nhiều split.

Sprint 1 V2 đã xử lý phần này bằng:

- `output/phase2/duplicate_title_groups.csv`
- `output/phase3/random_group_stratified_70_10_20.csv`
- `output/phase3/split_leakage_audit.json`
- `output/phase4_groupaware/random_split_results.csv`

Kết quả quan trọng: số nhóm duplicate rơi qua nhiều split giảm từ `24` xuống `0`.

### Group-aware split

Group-aware split là cách chia dữ liệu sao cho các mẫu cùng một nhóm duplicate luôn nằm trong cùng một split.

Ví dụ: nếu hai bài có tiêu đề gần như giống nhau, cả hai phải cùng ở train hoặc cùng ở test, không được tách ra hai bên.

### Macro-F1

Macro-F1 là metric tính F1 cho từng lớp rồi lấy trung bình. Nó quan trọng khi dữ liệu lệch lớp.

Trong đề tài này, clickbait khoảng 31%, nên Accuracy không đủ để đánh giá.

### Clickbait F1

Clickbait F1 đo riêng khả năng nhận diện lớp clickbait. Đây là metric rất quan trọng vì mục tiêu chính là bắt được clickbait.

### Balanced Accuracy

Balanced Accuracy là Accuracy được cân bằng giữa hai lớp. Nó hữu ích khi số lượng clickbait và non-clickbait không đều.

### FP, FN, TP, TN

- TP: clickbait thật, model đoán clickbait.
- TN: non-clickbait thật, model đoán non-clickbait.
- FP: non-clickbait thật, model đoán nhầm là clickbait.
- FN: clickbait thật, model bỏ sót.

### Error analysis

Error analysis là đọc các mẫu model sai để hiểu vì sao sai.

Repo đã annotate 100 lỗi:

- 50 false positive;
- 50 false negative.

### Lexical cues

Lexical cues là các dấu hiệu từ vựng mà model có thể dùng.

Ví dụ:

- "nào", "sao", "bất ngờ", "gì" có thể nghiêng về clickbait.
- Một số từ hành chính hoặc tin chính thống có thể nghiêng về non-clickbait.

Lưu ý: đây là liên hệ thống kê, không phải nguyên nhân tuyệt đối.

### Ablation

Ablation là thử thêm hoặc bớt một thành phần để xem nó có tác dụng không.

Repo đã thử:

- chỉ title vs title + lead paragraph;
- word TF-IDF vs char TF-IDF vs word+char;
- TF-IDF vs TF-IDF + lexical features;
- mask source-heavy cues.

## 4. Logic của đoạn này là gì?

Logic nghiên cứu của repo đi theo hướng sau:

1. Trước hết phải hiểu dữ liệu.
2. Sau đó phải chia dữ liệu cho công bằng.
3. Tiếp theo mới train và so sánh mô hình.
4. Nhưng điểm trên random split chưa đủ, nên cần kiểm tra source-held-out và category-held-out.
5. Nếu model giảm điểm khi đổi nguồn/chủ đề, nghĩa là random split có thể đang quá lạc quan.
6. Muốn hiểu model hơn, cần phân tích lỗi và lexical cues.
7. Muốn benchmark sạch hơn, cần kiểm soát duplicate leakage bằng group-aware split.

Nói cách khác, repo đang lập luận:

> Một mô hình tốt không chỉ là mô hình có điểm cao trên random split. Mô hình tốt phải được kiểm tra xem có khái quát qua domain mới không, có bị shortcut không, và khi sai thì sai vì lý do gì.

## 5. Tác giả muốn chứng minh hoặc nhấn mạnh điều gì?

Ý chính muốn truyền đạt là:

1. Với bài toán clickbait tiếng Việt, random split là cần thiết nhưng chưa đủ.
2. Dataset có thể có bias theo nguồn báo, chủ đề, thời gian và duplicate.
3. Benchmark chặt chẽ phải kiểm tra robustness, leakage và lỗi dự đoán.
4. Traditional ML như TF-IDF + Logistic Regression vẫn là baseline mạnh, dễ giải thích và đáng dùng.
5. Phân tích lỗi và lexical cues làm đề tài có giá trị nghiên cứu hơn việc chỉ báo cáo bảng điểm.

## 6. Ví dụ minh họa để dễ hiểu hơn

Giả sử bạn học thuộc đề trước khi kiểm tra. Nếu đề thi thật có câu giống hệt đề đã học, điểm của bạn cao chưa chắc vì bạn hiểu bài, có thể vì bạn đã thấy câu đó rồi.

Trong machine learning cũng vậy:

- Nếu tiêu đề gần giống nhau xuất hiện ở cả train và test, model có thể đạt điểm cao vì "nhớ" dữ liệu.
- Group-aware split giống như yêu cầu: các câu hỏi giống nhau phải nằm cùng một bên, không được để một câu ở phần học và một câu ở phần kiểm tra.

Một ví dụ khác:

Nếu một lớp có 70 bạn mặc áo trắng và 30 bạn mặc áo xanh, một người luôn đoán "áo trắng" sẽ có Accuracy 70%. Nhưng người đó hoàn toàn không nhận ra áo xanh. Vì vậy repo không dùng Accuracy làm metric chính, mà dùng Macro-F1 và Clickbait F1.

## 7. Những chỗ sinh viên dễ nhầm

### Nhầm 1: Accuracy cao nghĩa là model tốt

Sai. Nếu dữ liệu lệch lớp, Accuracy có thể cao dù model bỏ sót clickbait.

### Nhầm 2: Random split là đủ

Chưa đủ. Random split có thể trộn cùng nguồn báo, cùng chủ đề hoặc tiêu đề trùng vào train và test.

### Nhầm 3: Feature importance là nguyên nhân

Không hẳn. Nếu Logistic Regression cho thấy từ "bất ngờ" nghiêng về clickbait, điều đó chỉ nói đây là dấu hiệu thống kê trong dữ liệu, không chứng minh mọi tiêu đề có "bất ngờ" đều là clickbait.

### Nhầm 4: Model học được "ngữ nghĩa sâu"

Với TF-IDF + Logistic Regression/SVM, model chủ yếu học pattern từ vựng và n-gram. Không nên nói model thật sự hiểu ngữ nghĩa như con người.

### Nhầm 5: Càng nhiều model càng học thuật

Không đúng. Một đề tài ít model nhưng protocol chặt, kiểm soát leakage, có error analysis và limitation rõ vẫn thuyết phục hơn chạy nhiều model nhưng thiếu kiểm soát.

### Nhầm 6: Dùng source/category làm feature chính là tốt vì tăng điểm

Không nên. Source/category có thể tạo shortcut. Trong đề tài này, source/category nên dùng để audit bias và tạo held-out split, không dùng làm input chính.

### Nhầm 7: Temporal split có thể kết luận mạnh

Chưa chắc. Vì dữ liệu lệch về năm 2025, temporal split chỉ nên là phân tích bổ sung.

## 8. Nếu phải nói lại bằng lời của sinh viên, có thể nói như thế nào?

Em có thể nói như sau:

> Repo này xây dựng một benchmark cho bài toán phát hiện clickbait tiếng Việt trên ViClickbait-2025. Nhóm bắt đầu bằng việc phân tích dữ liệu để xem phân bố nhãn, nguồn báo, chủ đề, thời gian và duplicate. Sau đó nhóm tạo nhiều cách chia dữ liệu như random split, k-fold, source-held-out và category-held-out để đánh giá mô hình công bằng hơn. Các mô hình chính hiện tại là TF-IDF kết hợp Logistic Regression, SVM, Naive Bayes và Random Forest. Ngoài điểm số, repo còn phân tích lỗi, lexical cues và ablation để hiểu model đang học dấu hiệu nào. Gần đây nhóm đã thêm group-aware split để kiểm soát duplicate leakage, giúp benchmark sạch hơn trước khi viết báo cáo cuối.

Nếu nói ngắn hơn:

> Em không chỉ chạy model lấy điểm. Em kiểm tra dữ liệu, tạo split chống leakage, benchmark baseline, đánh giá model trên domain mới, rồi phân tích lỗi để hiểu mô hình sai ở đâu và dựa vào dấu hiệu nào.

## 9. Tóm tắt ngắn trong 3-5 câu

Repo hiện tại đang xây dựng một benchmark phát hiện clickbait tiếng Việt trên ViClickbait-2025. Điểm mạnh của đề tài là không chỉ dùng random split, mà còn kiểm tra source-held-out, category-held-out, error analysis, lexical cues và ablation. Sprint 1 V2 đã bổ sung group-aware split để kiểm soát duplicate leakage, đưa số nhóm duplicate rơi qua nhiều split từ `24` xuống `0`. Các mô hình chính hiện tại là baseline truyền thống dựa trên TF-IDF và Logistic Regression/SVM. Khi viết báo cáo, nên nhấn mạnh robustness, leakage control và explainability hơn là hứa chạy nhiều mô hình deep learning chưa có output.

## Ghi chú về ngữ cảnh còn thiếu

Để hiểu trọn vẹn repo, người đọc mới nên xem thêm:

- `ROADMAP_VICLICKBAIT_V2.MD` để biết việc nào đã làm và việc nào còn lại.
- `PHASE1_RESEARCH_FRAMING.md` để hiểu câu hỏi nghiên cứu.
- `PHASE3_EXPERIMENTAL_PROTOCOL.md` để hiểu cách chia dữ liệu.
- `output/phase4/phase4_summary.md` và `output/phase4_groupaware/phase4_summary.md` để xem benchmark.
- `output/phase6/paper_discussion_points.md` để xem các luận điểm đưa vào báo cáo.

