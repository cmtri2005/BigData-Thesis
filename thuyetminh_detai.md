THUYẾT MINH
ĐỀ TÀI KHOA HỌC VÀ CÔNG NGHỆ CẤP SINH VIÊN 2026

THÔNG TIN CHUNG

A1. Tên đề tài

Tên tiếng Việt (IN HOA): ĐÁNH GIÁ VÀ SO SÁNH HIỆU NĂNG CÁC MÔ HÌNH HỌC MÁY TRONG BÀI TOÁN PHÁT HIỆN TIÊU ĐỀ CLICKBAIT TIẾNG VIỆT
Tên tiếng Anh (IN HOA): BENCHMARKING MACHINE LEARNING MODELS FOR VIETNAMESE CLICKBAIT HEADLINE DETECTION

A2. Thời gian thực hiện 
 ..06.. tháng (kể từ khi được duyệt).

A3. Tổng kinh phí
(Lưu ý tính nhất quán giữa mục này và mục B8. Tổng hợp kinh phí đề nghị cấp)

Tổng kinh phí: …6.. triệu đồng, gồm
 Kinh phí từ Trường Đại học Công nghệ Thông tin: ..6.. triệu đồng

A4. Chủ nhiệm
Họ và tên: Nguyễn Minh Trí	.
Ngày, tháng, năm sinh: 25/10/2005	. Giới tính (Nam/Nữ): Nam	.
Số CMND: 079205009939	; Ngày cấp: 05/08/2022	; Nơi cấp: TPHCM	.
Mã số sinh viên:  23521643	.
Số điện thoại liên lạc: 0924165845	.
Đơn vị (Khoa): Hệ thống thông tin	.
Số tài khoản: 8802475201	Ngân hàng: BIDV
A5. Thành viên đề tài 

TT
Họ tên 
MSSV
Khoa
1
Cao Minh Trí
23521635
Hệ thống thông tin
2
Nguyễn Minh Trí 
23521643
Hệ thống thông tin




MÔ TẢ NGHIÊN CỨU

B1. Giới thiệu về đề tài

Trong kỷ nguyên truyền thông số và sự bùng nổ của mạng xã hội, "Clickbait" (Mồi nhử nhấp chuột) đã trở thành một vấn nạn nhức nhối trên không gian mạng. Nhằm cạnh tranh khốc liệt để giành giật sự chú ý (attention economy) và tối đa hóa doanh thu quảng cáo, nhiều tòa soạn và nền tảng nội dung thường lạm dụng các thủ thuật ngôn từ: sử dụng tiêu đề giật gân, mập mờ, phóng đại, hoặc cố tình che giấu thông tin cốt lõi (curiosity gap). Điều này không chỉ gây lãng phí thời gian, mang lại trải nghiệm tiêu cực cho độc giả, mà về lâu dài còn làm xói mòn nghiêm trọng niềm tin của công chúng vào nền báo chí chính thống, đồng thời tạo môi trường dung túng cho tin giả (fake news) lan truyền. Do đó, việc xây dựng các hệ thống Trí tuệ Nhân tạo (AI) tự động phát hiện và cảnh báo clickbait đang là một hướng nghiên cứu cấp thiết trên toàn cầu.

Tuy nhiên, đối với bài toán phân tích ngôn ngữ tự nhiên (NLP) cho tiếng Việt, các hướng nghiên cứu hiện tại thường vấp phải rào cản rất lớn về dữ liệu. Tiếng Việt có tính đặc thù cao với cấu trúc từ ghép phức tạp, hiện tượng đồng âm khác nghĩa và việc báo chí mạng thường xuyên sử dụng từ lóng, lối nói ẩn dụ, châm biếm. Để AI hiểu được các "mồi nhử" này, chúng ta cần những bộ dữ liệu cực lớn và được gán nhãn cực kỳ tỉ mỉ. Cho đến nay, vẫn thiếu vắng các bộ dữ liệu tiếng Việt chuẩn hóa, đa dạng chủ đề và có độ tin cậy cao. Trong bối cảnh đó, sự ra đời của bộ dữ liệu ViClickbait-2025 mang ý nghĩa bước ngoặt. Với 3.414 tiêu đề được thu thập công phu từ 8 nền tảng tin tức lớn (VnExpress, BaoMoi, Kenh14, SaoStar...) trải rộng trên 13 chủ đề, và đặc biệt đạt độ đồng thuận của chuyên gia rất cao (Cohen's Kappa = 0.822), ViClickbait-2025 đã cung cấp một nguồn tài nguyên quý giá để đối mặt triệt để với bài toán này.

Mặc dù đã có tài nguyên dữ liệu chất lượng cao, hiện tại vẫn đang tồn tại một khoảng trống nghiên cứu thực nghiệm (Empirical Gap) rất lớn. Cụ thể, do ViClickbait-2025 là một bộ dữ liệu hoàn toàn mới, vẫn chưa có một nghiên cứu đánh giá tổng thể (benchmark) nào được thực hiện để khảo sát tường tận mức độ hiệu quả của các thế hệ mô hình học máy khác nhau trên bộ dữ liệu này. Chúng ta chưa có đánh giá định lượng để trả lời cho các câu hỏi: Liệu một mô hình học máy cổ điển nhẹ nhàng có đủ sức nhận diện clickbait tiếng Việt, hay bắt buộc phải cần đến các kiến trúc mô hình ngôn ngữ khổng lồ? Sự đánh đổi (trade-off) giữa độ chính xác dự đoán, tốc độ suy luận (inference time) và tài nguyên tính toán giữa các mô hình này ra sao?

Nhằm lấp đầy khoảng trống nghiên cứu trên, đề tài "Đánh giá và so sánh hiệu năng các mô hình học máy trong bài toán phát hiện tiêu đề Clickbait tiếng Việt" được đề xuất thực hiện. Đề tài sẽ tiến hành xây dựng một pipeline chuẩn hóa, huấn luyện và so sánh một hệ sinh thái các mô hình đại diện cho 3 kỷ nguyên công nghệ NLP: từ phương pháp học máy thống kê cổ điển (TF-IDF kết hợp SVM), các mô hình Deep Learning xử lý chuỗi (BiLSTM), cho đến các Mô hình ngôn ngữ tiền huấn luyện (Pre-trained Language Models) tiên tiến nhất như PhoBERT và XLM-RoBERTa. Việc thiết lập một benchmark toàn diện và đa chiều không chỉ giúp khẳng định sức mạnh của từng kiến trúc mô hình, mà còn cung cấp một hệ quy chiếu khách quan. Từ đó, nhóm nghiên cứu sẽ đề xuất giải pháp công nghệ tối ưu nhất, cân bằng giữa hiệu suất và chi phí tài nguyên, mở ra tiềm năng ứng dụng thực tế tích hợp vào các nền tảng tổng hợp tin tức hoặc tiện ích trình duyệt cho độc giả Việt Nam.

B2. Mục tiêu, nội dung, kế hoạch nghiên cứu
B2.1 Mục tiêu 
Tìm hiểu sâu về các kiến trúc mô hình học sâu và mô hình ngôn ngữ tiền huấn luyện (PhoBERT, XLM-RoBERTa) ứng dụng trong bài toán phân loại văn bản (Text Classification).
Xây dựng quy trình xử lý ngôn ngữ tự nhiên chuẩn (NLP Pipeline) áp dụng riêng cho văn bản báo chí tiếng Việt từ dataset ViClickbait-2025.
Cài đặt và tinh chỉnh (fine-tune) thành công các mô hình: SVM, BiLSTM, PhoBERT, XLM-RoBERTa trên cùng một bộ dữ liệu.
Đo lường, đánh giá và lập bảng đối sánh (Benchmark) hiệu năng của các mô hình dựa trên các độ đo chuẩn (Accuracy, Precision, Recall, F1-Score).

B2.2 Nội dung và phương pháp nghiên cứu
Nội dung 1: Khảo sát hiện trạng và định hình cơ sở lý thuyết.
Mô tả: Nghiên cứu bức tranh tổng quan về bài toán phát hiện Clickbait trên các nền tảng báo chí, đặc biệt đi sâu vào các đặc điểm từ vựng, ngữ pháp và ngữ nghĩa mang tính đặc thù của tiếng Việt. Đồng thời, tìm hiểu và hệ thống hóa cơ sở lý thuyết của các nhóm thuật toán phân loại văn bản (Text Classification) sẽ được sử dụng để benchmark, trải dài từ học máy truyền thống, mạng nơ-ron sâu (Deep Learning) cho đến các mô hình ngôn ngữ lớn (Large/Pre-trained Language Models).
Phương pháp nghiên cứu:
Khảo sát tài liệu: Thu thập, đọc và phân tích các bài báo khoa học uy tín (tập trung vào các công bố từ 2020 đến nay) về lĩnh vực Xử lý ngôn ngữ tự nhiên (NLP) và nhận diện tin giả/clickbait. Rút ra các giới hạn, ưu/nhược điểm của các nghiên cứu trước để làm nổi bật tính cấp thiết của việc xây dựng benchmark trên dataset ViClickbait-2025.
Nghiên cứu cơ sở toán học và cơ chế hoạt động của thuật toán: Phân tích ba nhóm mô hình cốt lõi: nhóm học máy cổ điển (TF-IDF kết hợp SVM); nhóm Deep Learning (kỹ thuật nhúng từ Word Embedding kết hợp mạng xử lý chuỗi BiLSTM); và nhóm mô hình tiền huấn luyện tiên tiến PLMs (kiến trúc Transformer, cơ chế Self-Attention làm nền tảng cho PhoBERT và XLM-RoBERTa).
Xác định các chỉ số đo lường hiệu năng: ìm hiểu và lựa chọn các độ đo phù hợp cho bài toán phân loại nhị phân. Cụ thể, thiết lập danh sách các tiêu chí đánh giá bao gồm: Accuracy, Precision, Recall, F1-Score. Bổ sung thêm tiêu chí đánh giá về tài nguyên hệ thống như thời gian huấn luyện và độ trễ suy luận để đảm bảo tính thực tiễn khi triển khai.
Kết quả dự kiến: Nắm vững cơ sở lý thuyết toán học và luồng xử lý dữ liệu của các thuật toán. Hoàn thành chương Tổng quan tài liệu, bao gồm một bảng ma trận đối sánh các nghiên cứu trước đây. Xây dựng và phác thảo thành công sơ đồ kiến trúc tổng thể cho toàn bộ hệ thống thử nghiệm sẽ được lập trình trong các giai đoạn tiếp theo.
Nội dung 2: Khai phá dữ liệu (EDA) và Tiền xử lý (Preprocessing)
Mô tả: Khám phá các đặc trưng thống kê của bộ dữ liệu ViClickbait-2025 nhằm thấu hiểu cấu trúc văn bản, từ đó thiết kế quy trình (pipeline) làm sạch và chuẩn hóa đặc thù cho ngôn ngữ tiếng Việt trước khi đưa vào huấn luyện mô hình.
Phương pháp nghiên cứu:
Khai phá dữ liệu (EDA): Dùng các thư viện Python (Pandas, Seaborn) để thống kê và trực quan hóa tỷ lệ phân bố nhãn, tần suất xuất hiện của 13 chủ đề báo chí. Đặc biệt, tiến hành phân tích độ dài chuỗi (sequence length) của các tiêu đề – đây là thông số sống còn để cấu hình siêu tham số max_length cho các mô hình Transformer sau này.
Tiền xử lý văn bản: Thực hiện tuần tự các bước: (1) Chuẩn hóa Unicode tiếng Việt và chuyển đổi chữ thường; (2) Lọc nhiễu (dùng Regex để xóa URL, số, ký tự đặc biệt); (3) Tách từ (Word Tokenization) bằng công cụ chuyên dụng như VnCoreNLP hoặc PyVi để gắn kết các âm tiết tiếng Việt thành từ có nghĩa; (4) Loại bỏ các từ dừng (stop-words) dựa trên từ điển chuẩn.
Phân chia dữ liệu: 
Kết quả dự kiến: Bộ dữ liệu sạch, giảm thiểu nhiễu từ vựng. Đưa ra được các biểu đồ EDA trực quan. Tập dữ liệu được phân chia chuẩn xác, định dạng sẵn sàng để tiếp tục các bước tiếp theo.


Nội dung 3: Cài đặt và Huấn luyện các mô hình
Mô tả: Lập trình hiện thực hóa 4 mô hình đại diện cho 3 thế hệ công nghệ xử lý ngôn ngữ tự nhiên, nhằm xây dựng các hệ thống cơ sở (baselines) vững chắc cho bài toán phân loại tiêu đề Clickbait. 
Phương pháp nghiên cứu:
Nhóm cổ điển (TF-IDF + SVM):  Chuyển đổi văn bản đã tiền xử lý thành các vector không gian bằng TF-IDF (thử nghiệm với các n-gram khác nhau). Tiến hành huấn luyện thuật toán SVM và áp dụng kỹ thuật Grid Search để tìm kiếm tổ hợp siêu tham số tối ưu. 
Nhóm Deep Learning (BiLSTM): Thiết kế kiến trúc mạng nơ-ron bằng framework TensorFlow hoặc Keras/PyTorch. Khởi tạo lớp nhúng từ (Word Embedding như Word2Vec/FastText), truyền qua các lớp BiLSTM ẩn để trích xuất đặc trưng ngữ cảnh hai chiều. Áp dụng kỹ thuật Dropout để tránh học vẹt và dùng hàm kích hoạt Sigmoid ở lớp đầu ra cho tác vụ phân loại nhị phân. 
Nhóm PLMs (PhoBERT, XLM-RoBERTa): Sử dụng thư viện HuggingFace Transformers để tải trọng số tiền huấn luyện (pre-trained weights) và khởi tạo cấu trúc mô hình phân loại chuỗi (Sequence Classification). Quá trình tinh chỉnh (Fine-tuning) sử dụng thuật toán tối ưu AdamW, kết hợp với cơ chế dừng sớm (Early Stopping) dựa trên hàm mất mát (Validation Loss) để lưu lại trạng thái tốt nhất của mô hình. 
Kết quả dự kiến: Pipeline huấn luyện hoàn chỉnh. Huấn luyện thành công 4 mô hình đạt trạng thái hội tụ (không bị quá khớp); xuất và lưu trữ được các điểm kiểm tra trọng số tốt nhất (best model checkpoints) cùng đồ thị lịch sử huấn luyện (training logs) để chuyển sang bước đánh giá cuối cùng. 
Nội dung 4: Kiểm thử, đo đạc hiệu năng và phân tích Benchmark
Mô tả: Đánh giá độc lập hiệu năng của các mô hình đã được tinh chỉnh trên tập dữ liệu kiểm thử (Test set), nhằm thiết lập một hệ quy chiếu (Benchmark) toàn diện và xác định kiến trúc tối ưu nhất cho bài toán phát hiện Clickbait tiếng Việt.
Phương pháp nghiên cứu: 
Đo lường hiệu năng cốt lõi: Chạy quá trình suy luận (inference) bằng các điểm kiểm tra mô hình tốt nhất trên tập Test. Tính toán và trích xuất các độ đo chuẩn phân loại: Accuracy, Precision, Recall, và F1-Score. Trực quan hóa kết quả phân loại thông qua Ma trận nhầm lẫn. 
Phân tích đánh đổi (Trade-off Analysis): Lập bảng đối sánh đa chiều để cân nhắc sự đánh đổi giữa hiệu suất dự đoán và chi phí hệ thống. Các tiêu chí tài nguyên bao gồm: số lượng tham số của mô hình, thời gian huấn luyện, và đặc biệt là độ trễ suy luận để đánh giá khả năng triển khai thực tế trên các hệ thống tin tức có lưu lượng cao. 
Phân tích lỗi (Error Analysis): Khảo sát chuyên sâu các mẫu tiêu đề bị mô hình dự đoán sai (False Positives và False Negatives). Phân tích nguyên nhân cốt lõi (ví dụ: do câu mang tính châm biếm, chứa từ lóng mới, hoặc cấu trúc ngữ pháp phức tạp) nhằm vạch ra giới hạn của từng thuật toán. 
Kết quả dự kiến: Bảng số liệu Benchmark toàn diện kèm biểu đồ đối sánh trực quan; đưa ra phân tích sâu sắc về hành vi học của các mô hình đối với ngôn ngữ báo chí tiếng Việt; xác định và đề xuất được mô hình cân bằng nhất giữa độ chính xác và tốc độ xử lý; hoàn thiện toàn bộ báo cáo nghiên cứu khoa học. 
B2.3 Kế hoạch nghiên cứu.
Nội dung nghiên cứu
Thời gian
1. Khảo sát hiện trạng và định hình cơ sở lý thuyết 
4 tuần
1.1. Tìm hiểu lý thuyết về bài toán Clickbait, các thuật toán SVM, BiLSTM 
Tuần 1-2
1.2. Tìm hiểu sâu về kiến trúc Transformer, PhoBERT và XLM-RoBERTa 
Tuần 3-4
2. Khai phá dữ liệu và Tiền xử lý 
4 tuần
2.1. Tải dataset ViClickbait-2025, thống kê và phân tích dữ liệu (EDA) 
Tuần 1-2
2.2. Viết các hàm tiền xử lý (làm sạch, tách từ tiếng Việt) và phân chia tập dữ liệu 
Tuần 3-4
3. Cài đặt và Huấn luyện các mô hình 
8 tuần 
3.1. Cài đặt và huấn luyện Baseline: TF-IDF + SVM, nhúng Word2Vec + BiLSTM 
Tuần 1-3
3.2. Cài đặt pipeline HuggingFace, fine-tune mô hình PhoBERT 
Tuần 4-6
3.3. Fine-tune mô hình đa ngữ XLM-RoBERTa và tinh chỉnh siêu tham số 
Tuần 7-8
4. Kiểm thử, đo đạc hiệu năng và phân tích kết quả, viết báo cáo
4 tuần
4.1. Đánh giá mô hình trên tập Test, vẽ Confusion Matrix, trích xuất metrics 
Tuần 1-2
4.2. Phân tích kết quả Benchmark, thực hiện phân tích lỗi (Error Analysis) 
Tuần 3
4.3. Viết báo cáo tổng kết, chuẩn bị slide thuyết trình 
Tuần 4


B3. Kết quả dự kiến

Một (01) báo cáo tổng kết đề tài chi tiết, trình bày cơ sở lý thuyết, các bước xử lý và phân tích chuyên sâu về dữ liệu báo chí tiếng Việt. 
Một (01) bộ mã nguồn (Source code) hoàn chỉnh (có thể đóng gói dạng Jupyter Notebook/Python scripts), chứa toàn bộ pipeline từ tiền xử lý đến fine-tune 4 loại mô hình. 
Một (01) bảng Benchmark toàn diện đánh giá hiệu năng phát hiện Clickbait trên bộ dữ liệu ViClickbait-2025, tạo tiền đề tham khảo cho các nghiên cứu NLP trong tương lai. 

B4. Tài liệu tham khảo

[1] Tác giả bài báo ViClickbait (2025), "ViClickbait-2025: A Comprehensive Dataset for Vietnamese Clickbait Detection," Data in Brief, vol. XX, 2025. 
[2] D. Q. Nguyen and A. T. Nguyen, "PhoBERT: Pre-trained language models for Vietnamese," Findings of the Association for Computational Linguistics: EMNLP 2020, pp. 1037-1042, 2020. 
[3] A. Conneau et al., "Unsupervised Cross-lingual Representation Learning at Scale," Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pp. 8440-8451, 2020. 
