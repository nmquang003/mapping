# Bộ dữ liệu giới thiệu Ninh Bình

Ngày đọc nguồn: 06/10/2026.

Sổ tay giới thiệu tổng quan tỉnh Ninh Bình và 7 địa danh tuyển chọn: Tràng An, Hoa Lư, Tam Cốc – Bích Động, Cúc Phương, Bái Đính, Phát Diệm, Hang Múa. Không bao phủ mọi địa danh trong tỉnh.

Đây là bộ dữ liệu khởi đầu, không phải dữ liệu đầy đủ hoặc cập nhật trực tiếp. `source_checked` nghĩa là đã đọc nội dung nguồn, không phải mọi dữ kiện được xác minh độc lập.

## Tệp dữ liệu

- `seed.json`: dữ liệu gốc, có thể nạp vào web hoặc chuyển sang hệ quản trị khác.
- `ninh_binh.sqlite`: database SQLite có bảng entities, places, knowledge, sources và liên kết nguồn.
- `sources.csv`: danh mục liên kết nguồn, mở được trong công cụ bảng tính.
- `build_database.py`: tạo lại SQLite, CSV và tài liệu từ JSON bằng Python chuẩn.

Chạy lại: `python3 build_database.py` trong thư mục này. Chỉ sửa seed.json; SQLite là tệp sinh ra.

## Nội dung tổng quan có thể sử dụng

### Tổng quan

Ninh Bình là điểm đến kết hợp cảnh quan núi đá vôi, sông nước và di sản lịch sử. Khu vực Hoa Lư, Tràng An và Tam Cốc – Bích Động giúp người xem tìm hiểu mối liên hệ giữa địa hình tự nhiên, dấu tích kinh đô và đời sống địa phương. Phạm vi tỉnh hiện nay đã mở rộng sau sắp xếp năm 2025; các hồ sơ trong bản sổ tay này là những địa danh tuyển chọn.

Nguồn: [S01: Chi tiết 34 đơn vị hành chính cấp tỉnh](https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm); [S03: Ninh Bình](https://vietnam.travel/vi/places-to-go/northern-vietnam/ninh-binh); [S04: Quần thể Danh thắng Tràng An – Bảo tàng địa chất ngoài trời](https://dulichninhbinh.com.vn/item/3021); [S05: Cố đô Hoa Lư](https://dulichninhbinh.com.vn/item/3020); [S06: Khám phá vẻ đẹp non nước hữu tình tại Khu du lịch Tam Cốc – Bích Động](https://dulichninhbinh.com.vn/item/3116)

### Địa lý và cảnh quan

Nét nổi bật ở khu vực Tràng An – Tam Cốc là núi đá vôi, thung lũng, hang động và dòng nước. Tại Tam Cốc, sông Ngô Đồng đi qua ba hang và những cánh đồng. Cúc Phương bổ sung góc nhìn về hệ sinh thái rừng; vùng Kim Sơn gắn với bãi bồi ven biển và nghề cói.

Nguồn: [S04: Quần thể Danh thắng Tràng An – Bảo tàng địa chất ngoài trời](https://dulichninhbinh.com.vn/item/3021); [S06: Khám phá vẻ đẹp non nước hữu tình tại Khu du lịch Tam Cốc – Bích Động](https://dulichninhbinh.com.vn/item/3116); [S07: Vườn quốc gia Cúc Phương](https://dulichninhbinh.com.vn/item/3018); [S13: Nghề cói Kim Sơn: Làng nghề truyền thống bên bãi bồi ven biển](https://dulichninhbinh.com.vn/item/3663)

### Lịch sử và di sản

Hoa Lư gắn với việc Đinh Bộ Lĩnh lên ngôi năm 968 và lịch sử các triều Đinh, Tiền Lê, đầu thời Lý. Năm 1010, Lý Thái Tổ dời đô về Thăng Long. Những đền thờ vua Đinh Tiên Hoàng và vua Lê Đại Hành là các điểm tiêu biểu để tìm hiểu ký ức lịch sử của vùng đất này.

Nguồn: [S05: Cố đô Hoa Lư](https://dulichninhbinh.com.vn/item/3020)

### Văn hóa và làng nghề

Lễ hội Hoa Lư tưởng nhớ các vị vua và tiền nhân, có các nghi thức như rước nước, rước kiệu và dâng hương. Thêu ren Văn Lâm và nghề cói Kim Sơn thể hiện kỹ năng thủ công được gìn giữ qua nhiều thế hệ. Bái Đính và Phát Diệm là những góc tiếp cận khác nhau về kiến trúc tôn giáo của địa phương.

Nguồn: [S08: Chùa Bái Đính](https://dulichninhbinh.com.vn/item/3015); [S09: Nhà thờ đá Phát Diệm](https://dulichninhbinh.com.vn/item/3014); [S11: Lễ hội Hoa Lư – Nơi lưu giữ nét đẹp truyền thống nghìn năm](https://dulichninhbinh.com.vn/item/3359); [S12: Làng nghề thêu ren Văn Lâm tinh hoa thủ công Ninh Bình](https://dulichninhbinh.com.vn/item/3684); [S13: Nghề cói Kim Sơn: Làng nghề truyền thống bên bãi bồi ven biển](https://dulichninhbinh.com.vn/item/3663)

### Ẩm thực địa phương

Các món được nguồn du lịch địa phương giới thiệu gồm cơm cháy, thịt dê, mắm tép Gia Viễn và nem chua Yên Mạc. Mắm tép gắn với nguyên liệu thủy sản nước ngọt và cách chế biến truyền thống; nem chua Yên Mạc là sản phẩm ẩm thực gắn với địa danh cùng tên.

Nguồn: [S14: Mắm tép Gia Viễn, đậm đà hương vị quê hương](https://dulichninhbinh.com.vn/item/3719); [S15: Nem chua Yên Mạc – Tinh hoa ẩm thực truyền thống của Ninh Bình](https://dulichninhbinh.com.vn/item/3718)

### Thông tin tham quan

Người xem có thể khám phá cảnh quan bằng thuyền ở Tràng An và Tam Cốc, tìm hiểu lịch sử tại Hoa Lư, quan sát cảnh quan từ Hang Múa hoặc tìm hiểu thiên nhiên tại Cúc Phương. Giờ mở cửa, lịch tuyến, giá vé và điều kiện tiếp cận phải được kiểm tra theo thông báo hiện hành của đơn vị quản lý trước chuyến đi.

Nguồn: [S03: Ninh Bình](https://vietnam.travel/vi/places-to-go/northern-vietnam/ninh-binh); [S04: Quần thể Danh thắng Tràng An – Bảo tàng địa chất ngoài trời](https://dulichninhbinh.com.vn/item/3021); [S05: Cố đô Hoa Lư](https://dulichninhbinh.com.vn/item/3020); [S06: Khám phá vẻ đẹp non nước hữu tình tại Khu du lịch Tam Cốc – Bích Động](https://dulichninhbinh.com.vn/item/3116); [S07: Vườn quốc gia Cúc Phương](https://dulichninhbinh.com.vn/item/3018); [S10: Hang Múa – kỳ quan thiên nhiên hùng vĩ của Ninh Bình](https://dulichninhbinh.com.vn/item/3007); [S16: Website Vườn quốc gia Cúc Phương](https://vuonquocgiacucphuong.vn/vi/)

## Hồ sơ địa danh

### Quần thể danh thắng Tràng An

Cảnh quan núi đá vôi, thung lũng và hang động hòa cùng dấu tích lịch sử, văn hóa. Nguồn du lịch địa phương giới thiệu Tràng An là Di sản Văn hóa và Thiên nhiên thế giới.

Điểm nổi bật: Cảnh quan karst và hệ thống hang động; Trải nghiệm thuyền ở khu du lịch sinh thái; Sự kết hợp giữa thiên nhiên và di sản văn hóa.

Nguồn: [S04: Quần thể Danh thắng Tràng An – Bảo tàng địa chất ngoài trời](https://dulichninhbinh.com.vn/item/3021)

Ghi chú dữ liệu: Phân biệt toàn quần thể di sản với bến thuyền/khu du lịch sinh thái. Chưa đối chiếu ranh giới UNESCO và địa chỉ cổng vào.

### Cố đô Hoa Lư

Hoa Lư là kinh đô gắn với các triều Đinh, Tiền Lê và đầu thời Lý. Các đền thờ vua Đinh Tiên Hoàng và vua Lê Đại Hành là điểm tìm hiểu lịch sử tiêu biểu.

Điểm nổi bật: Mốc năm 968; Mốc dời đô năm 1010; Đền vua Đinh và đền vua Lê.

Nguồn: [S05: Cố đô Hoa Lư](https://dulichninhbinh.com.vn/item/3020)

Ghi chú dữ liệu: Địa chỉ cuối bài S05 còn ghi xã Trường Yên, thành phố Hoa Lư; dùng phần đầu bài và căn cứ sắp xếp ở S02. Không nhầm cố đô với khu du lịch Phố cổ Hoa Lư.

### Tam Cốc – Bích Động

Tam Cốc gắn với sông Ngô Đồng và ba hang xuyên núi đá vôi. Bích Động là quần thể chùa và động theo địa thế núi, gồm chùa Hạ, Trung và Thượng.

Điểm nổi bật: Hang Cả, Hang Hai, Hang Ba; Cảnh quan sông Ngô Đồng và đồng lúa; Chùa Hạ, Trung, Thượng ở Bích Động.

Nguồn: [S06: Khám phá vẻ đẹp non nước hữu tình tại Khu du lịch Tam Cốc – Bích Động](https://dulichninhbinh.com.vn/item/3116)

Ghi chú dữ liệu: Chưa xác minh địa chỉ và cổng vào từng điểm. Không đồng nhất giá thuyền Tam Cốc với thông tin tham quan chùa Bích Động.

### Vườn quốc gia Cúc Phương

Vườn quốc gia có cảnh quan rừng mưa nhiệt đới và các hoạt động nghiên cứu, cứu hộ, bảo tồn động vật. Nguồn địa phương giới thiệu đây là vườn quốc gia đầu tiên của Việt Nam.

Điểm nổi bật: Hệ sinh thái rừng; Đa dạng sinh học; Giáo dục môi trường và cứu hộ động vật.

Nguồn: [S07: Vườn quốc gia Cúc Phương](https://dulichninhbinh.com.vn/item/3018); [S16: Website Vườn quốc gia Cúc Phương](https://vuonquocgiacucphuong.vn/vi/)

Ghi chú dữ liệu: Vườn liên tỉnh. S07 ghi địa chỉ xã Phú Long, S16 còn ghi xã Cúc Phương/huyện Nho Quan; chưa xác nhận cổng đón khách. Quy định phương tiện vùng lõi có thay đổi được thông báo từ 1/9/2026.

### Chùa Bái Đính

Quần thể có khu chùa cổ, khu chùa mới và các hạng mục kiến trúc Phật giáo. Nội dung giới thiệu tập trung vào không gian kiến trúc và giá trị văn hóa.

Điểm nổi bật: Khu chùa cổ và chùa mới; Hành lang La Hán; Các điện thờ và bảo tháp.

Nguồn: [S08: Chùa Bái Đính](https://dulichninhbinh.com.vn/item/3015)

Ghi chú dữ liệu: Không khẳng định hiệu quả cầu may/chữa bệnh hoặc kỷ lục chưa kiểm chứng. Phân biệt vé dịch vụ xe điện với vé vào toàn bộ quần thể.

### Nhà thờ đá Phát Diệm

Quần thể kiến trúc Công giáo kết hợp hình thức nhà thờ với các nét kiến trúc truyền thống Việt Nam, sử dụng đá và gỗ. Theo nguồn địa phương, công trình được xây dựng trong giai đoạn 1875–1898.

Điểm nổi bật: Kiến trúc đá và gỗ; Phương đình; Giao thoa hình thức kiến trúc.

Nguồn: [S09: Nhà thờ đá Phát Diệm](https://dulichninhbinh.com.vn/item/3014)

Ghi chú dữ liệu: Chưa xác minh giờ đón khách, lịch nghi lễ hay quy định chụp ảnh hiện hành.

### Hang Múa

Điểm khám phá cảnh quan với đường bậc đá lên núi và tầm nhìn xuống vùng sông nước, đồng ruộng. Nguồn địa phương mô tả đường lên gần 500 bậc.

Điểm nổi bật: Đường bậc đá lên núi; Ngắm cảnh quan từ trên cao; Câu chuyện dân gian về tên gọi.

Nguồn: [S10: Hang Múa – kỳ quan thiên nhiên hùng vĩ của Ninh Bình](https://dulichninhbinh.com.vn/item/3007)

Ghi chú dữ liệu: Tên thôn được ghi khác nhau ngay trong S10 và địa chỉ phường chưa đối chiếu. Không coi câu chuyện dân gian về tên gọi là sự kiện lịch sử đã xác thực.

## Giá và lịch tham khảo, chưa xác nhận hiện hành

Không hiển thị các mục này như giá hoặc lịch hôm nay. Ngày đọc nguồn khác ngày có hiệu lực.

| Điểm | Nội dung | Giá trị theo nguồn | Ngày nguồn hiển thị |
|---|---|---|---|
| Quần thể danh thắng Tràng An | Vé người cao trên 1,3 m | 300000 VND/người | 2025-03-27 |
| Cố đô Hoa Lư | Vé người lớn | 20000 VND/người | 2025-03-27 |
| Vườn quốc gia Cúc Phương | Vé tham quan người lớn | 60000 VND/người | 2025-03-27 |
| Hang Múa | Vé tham quan | 100000 VND/người | 2025-03-24 |
| Chùa Bái Đính | Xe điện khứ hồi người lớn | 150000 VND/người | 2025-03-26 |
| Tam Cốc – Bích Động | Thời lượng chuyến thuyền theo mô tả nguồn | 2 giờ, khoảng | 2025-06-26 |
| Tam Cốc – Bích Động | Mùa lúa chín theo mô tả nguồn | Tháng 5–6  | 2025-06-26 |
| Ninh Bình | Thời gian thường niên Lễ hội Hoa Lư theo nguồn | Ngày 9–11 tháng Ba âm lịch  | 2025-09-24 |

## Lưu ý khi tích hợp chatbot

- Chỉ trả lời trong phạm vi scope và các hồ sơ đã có dữ liệu.
- Dùng facts có trạng thái source_checked hoặc dated_reference; với dated_reference phải nêu mốc khi có ý nghĩa.
- Các trường có status needs_review hoặc not_checked không được dùng để khẳng định sự thật.
- dated_practical_info không là giá/lịch hiện hành. Nếu hỏi hôm nay, nói chưa có xác nhận hiện hành; chỉ đưa giá tham khảo khi nêu rõ giới hạn và nguồn.
- Chỉ dẫn nguồn thực sự đi kèm dữ kiện; không dẫn S17 hoặc S18 như đã đọc để hỗ trợ câu trả lời.
- Nếu không đủ dữ liệu, nói chưa có trong sổ tay hoặc chưa được kiểm chứng, không suy đoán.
- Khi hỏi Nghệ An hoặc địa danh chưa có hồ sơ, thông báo ngoài phạm vi nội dung hiện có.
- Trả lời bằng tiếng Việt, ưu tiên ngắn gọn và cho phép người dùng mở nguồn.

View `chatbot_knowledge` chỉ lọc nội dung theo trạng thái, chưa thực hiện tìm kiếm hoặc kiểm soát câu trả lời. Backend vẫn phải lọc phạm vi câu hỏi, lấy nguồn, kiểm tra trích dẫn và xử lý thiếu dữ liệu.

Ví dụ truy vấn nguồn cho một dữ kiện:

```sql
SELECT k.text, k.status, k.time_basis, s.title, s.url
FROM chatbot_knowledge k
JOIN knowledge_sources ks ON ks.knowledge_id = k.id
JOIN sources s ON s.id = ks.source_id
WHERE k.entity_id = 'hoa-lu';
```

## Các khoảng trống cần bổ sung

- Đọc trực tiếp hồ sơ UNESCO để bổ sung năm ghi danh, tiêu chí, diện tích vùng lõi/vùng đệm.
- Xác nhận địa chỉ và tọa độ cổng vào của từng điểm, nhất là Tràng An, Hang Múa và Cúc Phương.
- Xác nhận giá vé, giờ mở cửa, tuyến thuyền và điều kiện miễn giảm hiện hành từ đơn vị vận hành.
- Đọc đầy đủ quy định phương tiện vùng lõi Cúc Phương áp dụng từ 1/9/2026.
- Bổ sung nguồn khí hậu, địa hình, số liệu thống kê và kinh tế phù hợp phạm vi tỉnh hiện hành.
- Bổ sung hồ sơ thuộc khu vực Hà Nam và Nam Định trước đây nếu mở rộng nội dung toàn tỉnh.
- Kiểm tra quyền sử dụng dữ liệu bản đồ và media trước khi tích hợp vào sản phẩm.
- Chưa xác minh URL bán vé; không bật nút đặt vé dựa trên suy đoán.

## Danh mục nguồn

### S01 · Chi tiết 34 đơn vị hành chính cấp tỉnh

[Báo Điện tử Chính phủ](https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm) · Trạng thái: `source_checked`.

Bài dẫn Nghị quyết 202/2025/QH15. Số liệu diện tích và dân số là số liệu phục vụ sắp xếp năm 2025.

### S02 · Nghị quyết 1674/NQ-UBTVQH15 về sắp xếp đơn vị hành chính cấp xã Ninh Bình

[Báo Điện tử Chính phủ](https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-quyet-so-1674-nq-ubtvqh15-sap-xep-cac-dvhc-cap-xa-cua-tinh-ninh-binh-nam-2025-119250616203223135.htm) · Trạng thái: `source_checked`.

Nghị quyết thông qua ngày 16/6/2025; dùng làm căn cứ tên xã, phường theo đợt sắp xếp này.

### S03 · Ninh Bình

[Vietnam Tourism – Cục Du lịch Quốc gia Việt Nam](https://vietnam.travel/vi/places-to-go/northern-vietnam/ninh-binh) · Trạng thái: `source_checked`.

Trang ghi bản dịch được AI tạo. Chỉ lấy nội dung tổng quát; không dùng các kỷ lục, mùa vụ hay lịch vận chuyển như thông tin hiện hành chưa đối chiếu.

### S04 · Quần thể Danh thắng Tràng An – Bảo tàng địa chất ngoài trời

[Trung tâm Thông tin Xúc tiến Du lịch – Sở Du lịch Ninh Bình](https://dulichninhbinh.com.vn/item/3021) · Trạng thái: `source_checked`.

Ngày trang hiển thị không bảo đảm mọi chi tiết nội dung vẫn nguyên bản tại ngày đó. Không lấy diện tích tổng quần thể làm diện tích vùng lõi UNESCO.

### S05 · Cố đô Hoa Lư

[Trung tâm Thông tin Xúc tiến Du lịch – Sở Du lịch Ninh Bình](https://dulichninhbinh.com.vn/item/3020) · Trạng thái: `source_checked`.

Bài trộn địa chỉ mới trong phần đầu và địa chỉ cũ ở cuối. Giá vé cần xác nhận lại.

### S06 · Khám phá vẻ đẹp non nước hữu tình tại Khu du lịch Tam Cốc – Bích Động

[Trung tâm Thông tin Xúc tiến Du lịch – Sở Du lịch Ninh Bình](https://dulichninhbinh.com.vn/item/3116) · Trạng thái: `source_checked`.

Thời lượng thuyền và mùa lúa là mô tả tham khảo; điều kiện thực tế có thể thay đổi.

### S07 · Vườn quốc gia Cúc Phương

[Trung tâm Thông tin Xúc tiến Du lịch – Sở Du lịch Ninh Bình](https://dulichninhbinh.com.vn/item/3018) · Trạng thái: `source_checked`.

Nội dung hiện đọc nêu Ninh Bình, Phú Thọ, Thanh Hóa; địa chỉ cuối bài khác website vườn. Không tự suy ra cổng vào từ địa chỉ này.

### S08 · Chùa Bái Đính

[Trung tâm Thông tin Xúc tiến Du lịch – Sở Du lịch Ninh Bình](https://dulichninhbinh.com.vn/item/3015) · Trạng thái: `source_checked`.

Không đưa các tuyên bố kỷ lục vào dữ liệu đã duyệt khi chưa đọc xác nhận riêng.

### S09 · Nhà thờ đá Phát Diệm

[Trung tâm Thông tin Xúc tiến Du lịch – Sở Du lịch Ninh Bình](https://dulichninhbinh.com.vn/item/3014) · Trạng thái: `source_checked`.

Dùng mô tả kiến trúc và khoảng thời gian xây dựng theo bài; xã Phát Diệm đối chiếu S02.

### S10 · Hang Múa – kỳ quan thiên nhiên hùng vĩ của Ninh Bình

[Trung tâm Thông tin Xúc tiến Du lịch – Sở Du lịch Ninh Bình](https://dulichninhbinh.com.vn/item/3007) · Trạng thái: `source_checked`.

Nguồn ghi phường Hoa Lư; chưa xác nhận lại địa chỉ. Câu chuyện nguồn gốc tên gọi được ghi là câu chuyện dân gian.

### S11 · Lễ hội Hoa Lư – Nơi lưu giữ nét đẹp truyền thống nghìn năm

[Trung tâm Thông tin Xúc tiến Du lịch – Sở Du lịch Ninh Bình](https://dulichninhbinh.com.vn/item/3359) · Trạng thái: `source_checked`.

Lịch thường niên không thay thế thông báo tổ chức của từng năm.

### S12 · Làng nghề thêu ren Văn Lâm tinh hoa thủ công Ninh Bình

[Trung tâm Thông tin Xúc tiến Du lịch – Sở Du lịch Ninh Bình](https://dulichninhbinh.com.vn/item/3684) · Trạng thái: `source_checked`.

Giới thiệu nghề; chưa xác nhận cơ sở nào có tour trải nghiệm đang mở.

### S13 · Nghề cói Kim Sơn: Làng nghề truyền thống bên bãi bồi ven biển

[Trung tâm Thông tin Xúc tiến Du lịch – Sở Du lịch Ninh Bình](https://dulichninhbinh.com.vn/item/3663) · Trạng thái: `source_checked`.

Kim Sơn ở đây là vùng văn hóa/nghề, không gán mọi cơ sở nghề vào xã Kim Sơn hiện hành.

### S14 · Mắm tép Gia Viễn, đậm đà hương vị quê hương

[Trung tâm Thông tin Xúc tiến Du lịch – Sở Du lịch Ninh Bình](https://dulichninhbinh.com.vn/item/3719) · Trạng thái: `source_checked`.

Thông tin văn hóa ẩm thực, không phải hướng dẫn bảo đảm an toàn thực phẩm.

### S15 · Nem chua Yên Mạc – Tinh hoa ẩm thực truyền thống của Ninh Bình

[Trung tâm Thông tin Xúc tiến Du lịch – Sở Du lịch Ninh Bình](https://dulichninhbinh.com.vn/item/3718) · Trạng thái: `source_checked`.

Bài cũng nhắc cơm cháy và thịt dê là đặc sản Ninh Bình; chưa xác minh giá hoặc cửa hàng.

### S16 · Website Vườn quốc gia Cúc Phương

[Vườn quốc gia Cúc Phương](https://vuonquocgiacucphuong.vn/vi/) · Trạng thái: `source_checked`.

Đã đọc trang chủ. Có thông báo quy định phương tiện vào vùng lõi áp dụng từ 1/9/2026; chưa đọc đầy đủ quy định, không tự diễn giải điều kiện.

### S17 · Trang An Landscape Complex

[UNESCO World Heritage Centre](https://whc.unesco.org/en/list/1438/) · Trạng thái: `not_checked`.

Bị chặn ở bước kiểm tra bảo mật khi truy cập. Giữ làm nguồn ưu tiên bổ sung; không dùng như đã đọc trực tiếp trong lần này.

### S18 · Bản đồ hành chính Việt Nam

[Hạ tầng dữ liệu không gian địa lý quốc gia](https://vnsdi.mae.gov.vn/bandohanhchinh/) · Trạng thái: `not_checked`.

Nguồn do đề thi cung cấp; chưa kiểm tra dữ liệu hoặc quyền tái sử dụng trong lần này.

## Nguyên tắc biên tập

- Diễn đạt lại bằng tiếng Việt; giữ nguồn cạnh thông tin, không sao chép nguyên bài.
- Không gán số liệu Ninh Bình trước sắp xếp cho toàn tỉnh sau sắp xếp.
- Số liệu dân số năm 2025 phải ghi mốc, không gọi là dân số hiện tại năm 2026.
- Không tự sinh tọa độ, giờ mở cửa, URL đặt vé, lịch vận chuyển hoặc số lượng loài.
- Tôn trọng tín ngưỡng, không khẳng định tác dụng cầu may, chữa bệnh hoặc bình phẩm niềm tin.
- Hình AI phải ghi rõ là minh họa; hình phục dựng không được trình bày như ảnh tư liệu.
- Truyền thuyết và câu chuyện dân gian phải có nhãn riêng, không hòa vào dữ kiện lịch sử.
- Quyền đọc thông tin công khai không mặc nhiên cho phép dùng lại ảnh, bản đồ, video hoặc tour 360.
