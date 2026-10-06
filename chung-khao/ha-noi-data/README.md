# Bộ dữ liệu giới thiệu Hà Nội

Ngày đọc nguồn: 06/10/2026.

Sổ tay giới thiệu tổng quan Hà Nội và 8 địa danh tuyển chọn: Hồ Hoàn Kiếm, Phố cổ Hà Nội, Văn Miếu – Quốc Tử Giám, Hoàng thành Thăng Long, Lăng Chủ tịch Hồ Chí Minh, Nhà hát Lớn Hà Nội, Bảo tàng Dân tộc học Việt Nam, Nhà thờ Lớn Hà Nội. Không bao phủ mọi địa danh trong địa phương.

Đây là bộ dữ liệu khởi đầu, không phải dữ liệu đầy đủ hoặc cập nhật trực tiếp. `source_checked` nghĩa là đã đọc nội dung nguồn, không phải mọi dữ kiện được xác minh độc lập.

## Tệp dữ liệu

- `seed.json`: dữ liệu gốc, có thể nạp vào web hoặc chuyển sang hệ quản trị khác.
- `ha_noi.sqlite`: database SQLite có bảng entities, places, knowledge, sources và liên kết nguồn.
- `sources.csv`: danh mục liên kết nguồn, mở được trong công cụ bảng tính.
- `build_database.py`: tạo lại SQLite, CSV và tài liệu từ JSON bằng Python chuẩn.

Chạy lại: `python3 build_database.py` trong thư mục này. Chỉ sửa seed.json; SQLite là tệp sinh ra.

## Nội dung tổng quan có thể sử dụng

### Thủ đô qua những lớp di sản

Hà Nội được giới thiệu qua di tích hoàng thành, truyền thống học tập, phố cổ, không gian hồ và bảo tàng. Bộ hồ sơ này tập trung vào tám điểm tuyển chọn, không phải danh bạ đầy đủ mọi địa danh thủ đô.

Nguồn: [S03: Hanoi: six heritage sites](https://vietnam.travel/things-to-do/hanoi-six-heritage-sites); [S05: 11 must-see attractions in Ha Noi](https://vietnam.travel/things-to-do/11-must-see-attractions-ha-noi); [S07: Thư ngỏ – Hoàng thành Thăng Long](https://hoangthanhthanglong.vn/thu-ngo/)

### Hồ và không gian đô thị

Hồ Hoàn Kiếm là một điểm nhận diện trong khu vực trung tâm, gắn với đền Ngọc Sơn, cầu Thê Húc và không gian phố cổ lân cận. Nguồn tuyến đi bộ còn giới thiệu sông Hồng, cầu Long Biên và khu vực Trúc Bạch như ngữ cảnh đô thị; các điểm này chưa có hồ sơ riêng.

Nguồn: [S04: 3 walking tours of Hanoi](https://vietnam.travel/things-to-do/3-walking-tours-hanoi); [S05: 11 must-see attractions in Ha Noi](https://vietnam.travel/things-to-do/11-must-see-attractions-ha-noi)

### Hoàng thành và truyền thống giáo dục

Hoàng thành Thăng Long lưu giữ nhiều lớp dấu tích qua các triều đại và được UNESCO ghi danh năm 2010. Văn Miếu có mốc xây dựng năm 1070; Quốc Tử Giám có mốc năm 1076 theo bài giới thiệu di sản. Các mốc này có thể dùng cho dòng thời gian học tập.

Nguồn: [S03: Hanoi: six heritage sites](https://vietnam.travel/things-to-do/hanoi-six-heritage-sites); [S07: Thư ngỏ – Hoàng thành Thăng Long](https://hoangthanhthanglong.vn/thu-ngo/)

### Phố nghề, di tích và bảo tàng

Tên nhiều phố cổ bắt đầu bằng Hàng, gợi lại các hoạt động nghề và buôn bán như Hàng Bạc, Hàng Mã, Hàng Đường. Bảo tàng Dân tộc học giới thiệu đời sống văn hóa của các cộng đồng dân tộc Việt Nam; Lăng Chủ tịch Hồ Chí Minh là không gian tưởng niệm cần cách ứng xử trang nghiêm.

Nguồn: [S03: Hanoi: six heritage sites](https://vietnam.travel/things-to-do/hanoi-six-heritage-sites); [S05: 11 must-see attractions in Ha Noi](https://vietnam.travel/things-to-do/11-must-see-attractions-ha-noi)

### Tên món ăn để khám phá

Nguồn tuyến đi bộ giới thiệu phở, cà phê trứng, phở cuốn và phở chiên phồng trong trải nghiệm Hà Nội. Database hiện lưu tên món và bối cảnh giới thiệu; chưa xác nhận công thức, quán ăn, nguồn gốc độc quyền hoặc mức giá.

Nguồn: [S04: 3 walking tours of Hanoi](https://vietnam.travel/things-to-do/3-walking-tours-hanoi)

### Khám phá theo tuyến chủ đề

Có thể xây dựng trải nghiệm lựa chọn giữa di sản hoàng thành, lịch sử giáo dục, phố nghề và văn hóa bảo tàng. Nguồn đã có tuyến đi bộ tham khảo; khi đưa vào web, đội cần đối chiếu lối vào, lịch hoạt động, khoảng cách và điều kiện thực tế trước khi hướng dẫn người dùng.

Nguồn: [S03: Hanoi: six heritage sites](https://vietnam.travel/things-to-do/hanoi-six-heritage-sites); [S04: 3 walking tours of Hanoi](https://vietnam.travel/things-to-do/3-walking-tours-hanoi); [S05: 11 must-see attractions in Ha Noi](https://vietnam.travel/things-to-do/11-must-see-attractions-ha-noi); [S07: Thư ngỏ – Hoàng thành Thăng Long](https://hoangthanhthanglong.vn/thu-ngo/)

## Hồ sơ địa danh

### Hồ Hoàn Kiếm

Không gian hồ ở trung tâm đô thị, gắn với đền Ngọc Sơn và cầu Thê Húc trong bài giới thiệu điểm đến Hà Nội.

Điểm nổi bật: Không gian ven hồ; Đền Ngọc Sơn; Cầu Thê Húc.

Nguồn: [S04: 3 walking tours of Hanoi](https://vietnam.travel/things-to-do/3-walking-tours-hanoi); [S05: 11 must-see attractions in Ha Noi](https://vietnam.travel/things-to-do/11-must-see-attractions-ha-noi)

Ghi chú dữ liệu: Không dùng nhân vật truyền thuyết bị nhầm trong bài nguồn. Chưa có lịch phố đi bộ hiện hành hoặc thông tin vé đền.

### Phố cổ Hà Nội

Khu phố gắn với thương mại và nghề truyền thống, thể hiện qua những tên phố bắt đầu bằng Hàng.

Điểm nổi bật: Tên phố gắn với nghề; Hàng Bạc; Hàng Mã và Hàng Đường.

Nguồn: [S03: Hanoi: six heritage sites](https://vietnam.travel/things-to-do/hanoi-six-heritage-sites); [S04: 3 walking tours of Hanoi](https://vietnam.travel/things-to-do/3-walking-tours-hanoi)

Ghi chú dữ liệu: Hồ sơ nội dung đã có nguồn; địa chỉ hành chính chi tiết, tọa độ, giá và giờ hiện hành chưa xác nhận.

### Văn Miếu – Quốc Tử Giám

Di tích gắn với truyền thống học tập và khoa cử, có hệ thống bia tiến sĩ được bài giới thiệu di sản nhắc tới.

Điểm nổi bật: Truyền thống giáo dục; Bia tiến sĩ; Mốc 1070 và 1076.

Nguồn: [S03: Hanoi: six heritage sites](https://vietnam.travel/things-to-do/hanoi-six-heritage-sites)

Ghi chú dữ liệu: Chưa đọc nguồn quản lý trực tiếp về vé, giờ và địa chỉ mới; không dùng giá cũ từ bài du lịch tổng hợp.

### Hoàng thành Thăng Long

Khu di sản phản ánh nhiều lớp lịch sử kinh đô, với dấu tích kiến trúc và khảo cổ qua các thời kỳ.

Điểm nổi bật: Di sản UNESCO năm 2010; Các lớp khảo cổ; Lịch sử kinh đô.

Nguồn: [S03: Hanoi: six heritage sites](https://vietnam.travel/things-to-do/hanoi-six-heritage-sites); [S06: Giới thiệu Hoàng thành Thăng Long](https://hoangthanhthanglong.vn/gioi-thieu/); [S07: Thư ngỏ – Hoàng thành Thăng Long](https://hoangthanhthanglong.vn/thu-ngo/)

Ghi chú dữ liệu: Hồ sơ nội dung đã có nguồn; địa chỉ hành chính chi tiết, tọa độ, giá và giờ hiện hành chưa xác nhận.

### Lăng Chủ tịch Hồ Chí Minh

Không gian tưởng niệm Chủ tịch Hồ Chí Minh được nguồn du lịch Hà Nội giới thiệu.

Điểm nổi bật: Không gian tưởng niệm; Ứng xử trang nghiêm.

Nguồn: [S03: Hanoi: six heritage sites](https://vietnam.travel/things-to-do/hanoi-six-heritage-sites); [S05: 11 must-see attractions in Ha Noi](https://vietnam.travel/things-to-do/11-must-see-attractions-ha-noi)

Ghi chú dữ liệu: Chưa xác nhận lịch viếng, thời gian bảo trì hoặc điều kiện tham quan hiện hành; loại giá vé trong bài tổng hợp.

### Nhà hát Lớn Hà Nội

Công trình kiến trúc và địa điểm biểu diễn được các bài du lịch giới thiệu trong khu vực trung tâm Hà Nội.

Điểm nổi bật: Kiến trúc; Nghệ thuật biểu diễn.

Nguồn: [S04: 3 walking tours of Hanoi](https://vietnam.travel/things-to-do/3-walking-tours-hanoi); [S05: 11 must-see attractions in Ha Noi](https://vietnam.travel/things-to-do/11-must-see-attractions-ha-noi)

Ghi chú dữ liệu: Không suy ra luôn có tour nội thất hoặc biểu diễn; lịch chương trình cần nguồn đơn vị vận hành.

### Bảo tàng Dân tộc học Việt Nam

Bảo tàng giới thiệu đời sống và văn hóa của các cộng đồng dân tộc Việt Nam.

Điểm nổi bật: Văn hóa các cộng đồng; Trưng bày hiện vật và không gian kiến trúc.

Nguồn: [S05: 11 must-see attractions in Ha Noi](https://vietnam.travel/things-to-do/11-must-see-attractions-ha-noi)

Ghi chú dữ liệu: Không dùng cách gọi 54 dân tộc thiểu số trong bài tiếng Anh; chưa xác nhận giờ, vé và nội dung triển lãm hiện hành.

### Nhà thờ Lớn Hà Nội

Công trình Công giáo được nguồn du lịch nhắc tới qua kiến trúc Gothic và vị trí trong tuyến khám phá trung tâm.

Điểm nổi bật: Kiến trúc Gothic; Không gian sinh hoạt tôn giáo.

Nguồn: [S04: 3 walking tours of Hanoi](https://vietnam.travel/things-to-do/3-walking-tours-hanoi); [S05: 11 must-see attractions in Ha Noi](https://vietnam.travel/things-to-do/11-must-see-attractions-ha-noi)

Ghi chú dữ liệu: Chưa có lịch thánh lễ hoặc quy định vào bên trong; không tự coi giờ mở cửa trên bài du lịch là lịch hiện hành.

## Lịch tham khảo, chưa xác nhận hiện hành

Không hiển thị các mục này như giá hoặc lịch hôm nay. Ngày đọc nguồn khác ngày có hiệu lực.

| Điểm | Nội dung | Giá trị theo nguồn | Ngày nguồn hiển thị |
|---|---|---|---|
| Hoàng thành Thăng Long | Giờ tham quan trên header website quản lý | 08:00–17:00 hằng ngày  | Không hiển thị |

## Lưu ý khi tích hợp chatbot

- Trả lời bằng tiếng Việt, chỉ sử dụng hồ sơ và dữ kiện thuộc database đang chọn.
- Với địa danh chưa có hồ sơ, nói: Địa danh này chưa có trong sổ tay; không lấy kiến thức mô hình để bù.
- Với câu hỏi ngoài phạm vi địa phương đang chọn, đề nghị chuyển sang database tương ứng nếu hệ thống đã nạp; không tự trả lời địa phương khác.
- Chỉ khẳng định dữ kiện từ chatbot_knowledge; mỗi câu trả lời phải có source_ids hoặc URL thực sự hỗ trợ nội dung.
- Giữ mốc thời gian của dated_reference; không gọi số liệu theo nghị quyết là số liệu mới nhất.
- needs_review và not_checked không được dùng làm căn cứ khẳng định. Không suy diễn từ tên hoặc tiêu đề nguồn.
- Đối với giá vé, lịch tàu, giờ mở cửa, đặt vé, thời tiết và tình trạng đường: nếu chưa xác nhận hiện hành, nói chưa có dữ liệu hiện hành trong sổ tay.
- Tọa độ null không được tự suy ra; không dùng dữ liệu này để dẫn đường chính xác.
- Không coi source_checked là chứng nhận đúng tuyệt đối; khi có mâu thuẫn, nêu chưa chắc và chuyển mục sang needs_review.

View `chatbot_knowledge` chỉ lọc nội dung theo trạng thái, chưa thực hiện tìm kiếm hoặc kiểm soát câu trả lời. Backend vẫn phải lọc phạm vi câu hỏi, lấy nguồn, kiểm tra trích dẫn và xử lý thiếu dữ liệu.

Ví dụ truy vấn nguồn cho một dữ kiện:

```sql
SELECT k.text, k.status, k.time_basis, s.title, s.url
FROM chatbot_knowledge k
JOIN knowledge_sources ks ON ks.knowledge_id = k.id
JOIN sources s ON s.id = ks.source_id
WHERE k.entity_id = 'ho-hoan-kiem';
```

## Các khoảng trống cần bổ sung

- Chưa có bộ giá vé hiện hành, chi phí ăn ở, lịch vận chuyển hoặc dịch vụ đặt vé đã xác nhận.
- Chưa đối chiếu tọa độ từng địa danh và ranh giới hành chính để đặt marker/map3D; latitude và longitude để null.
- Chưa có đầy đủ địa chỉ xã/phường mới của từng điểm; chỉ điền địa chỉ khi nguồn trực tiếp nêu.
- Chưa có ảnh AI, âm thanh thuyết minh hoặc mô hình 3D; đây là database nội dung.
- Bộ hồ sơ tuyển chọn không bao phủ mọi địa danh, lễ hội, cộng đồng và món ăn của địa phương.

## Danh mục nguồn

### S01 · Chi tiết 34 đơn vị hành chính cấp tỉnh

[Báo Điện tử Chính phủ](https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm) · Trạng thái: `source_checked`.

Dùng để xác định Hà Nội không sáp nhập cấp tỉnh trong đợt năm 2025; không suy ra địa chỉ chi tiết.

### S02 · Nghị quyết 1656/NQ-UBTVQH15 về sắp xếp cấp xã Hà Nội

[Thông tấn xã Việt Nam](https://nvsk.vnanet.vn/toan-van-nghi-quyet-so-1656-nq-ubtvqh15-sap-xep-cac-don-vi-hanh-chinh-cap-xa-cua-thanh-pho-ha-noi-nam-2025-1-172085.vna) · Trạng thái: `source_checked`.

Đã đọc phần mở đầu và văn bản về sắp xếp năm 2025. Không thấy ngày đăng riêng; ngày 16/06/2025 là ngày nghị quyết.

### S03 · Hanoi: six heritage sites

[Vietnam Tourism – Cục Du lịch Quốc gia Việt Nam](https://vietnam.travel/things-to-do/hanoi-six-heritage-sites) · Trạng thái: `source_checked`.

Dùng cho tổng quan di tích, mốc Văn Miếu, Quốc Tử Giám và phố cổ. Loại chi tiết truyền thuyết và niên đại chưa đối chiếu thêm.

### S04 · 3 walking tours of Hanoi

[Vietnam Tourism – Cục Du lịch Quốc gia Việt Nam](https://vietnam.travel/things-to-do/3-walking-tours-hanoi) · Trạng thái: `source_checked`.

Dùng cho địa danh và tên món ăn; không lấy mô tả nguyên liệu phở cuốn trong bài. Tuyến đi bộ không được coi là hướng dẫn an toàn hay lịch hoạt động hiện hành.

### S05 · 11 must-see attractions in Ha Noi

[Vietnam Tourism – Cục Du lịch Quốc gia Việt Nam](https://vietnam.travel/things-to-do/11-must-see-attractions-ha-noi) · Trạng thái: `source_checked`.

Bài có chi tiết cần biên tập: nhầm vua xây chùa Một Cột, nhầm nhân vật truyền thuyết trả gươm; cách gọi 54 ethnic minorities không chính xác; giá và giờ không có mốc rõ. Đã loại các chi tiết này, chỉ lấy mô tả địa danh có căn cứ.

### S06 · Giới thiệu Hoàng thành Thăng Long

[Trung tâm Bảo tồn di sản Thăng Long – Hà Nội](https://hoangthanhthanglong.vn/gioi-thieu/) · Trạng thái: `source_checked`.

Website quản lý trực tiếp; đã đọc địa chỉ footer và giờ 8:00–17:00 trên header. Chưa kiểm tra hiệu lực lịch đối với ngày cụ thể. Đường dẫn đặt vé chưa được kiểm tra nên không đưa vào database.

### S07 · Thư ngỏ – Hoàng thành Thăng Long

[Trung tâm Bảo tồn di sản Thăng Long – Hà Nội](https://hoangthanhthanglong.vn/thu-ngo/) · Trạng thái: `source_checked`.

Nguồn quản lý nêu khai quật khảo cổ năm 2002 và UNESCO năm 2010; dùng đối chiếu lịch sử và di sản.

## Nguyên tắc biên tập

- Diễn đạt lại bằng tiếng Việt; hiển thị nguồn cạnh dữ kiện. Không sao chép toàn bộ bài hay tự sử dụng ảnh có bản quyền.
- Tên tỉnh, xã, phường và số liệu phải đi kèm thời điểm. Không dùng địa chỉ huyện trong bài cũ như địa chỉ hành chính hiện hành.
- Không tự sinh tọa độ, giá vé, lịch vận chuyển, giờ mở cửa, đường dẫn đặt vé hoặc số liệu dân số hiện tại.
- Tôn trọng tín ngưỡng và đời sống cộng đồng; truyền thuyết cần gắn nhãn truyền thuyết, không kể như sự kiện lịch sử.
- Ảnh do AI tạo phải gắn nhãn minh họa AI; không dùng ảnh tái dựng làm bằng chứng về kiến trúc hay nghi lễ thực tế.
- Các ý tưởng tương tác và gợi ý hành trình là biên tập của đội, không phải dữ kiện của nguồn hoặc cam kết dịch vụ.
