# Bộ dữ liệu giới thiệu Lào Cai

Ngày đọc nguồn: 06/10/2026.

Sổ tay giới thiệu tổng quan Lào Cai và 7 địa danh tuyển chọn: Sa Pa, Fansipan, Chợ Bắc Hà, Mù Cang Chải, Đèo Khau Phạ, Hồ Thác Bà, Làng Ngòi Tu. Không bao phủ mọi địa danh trong địa phương.

Đây là bộ dữ liệu khởi đầu, không phải dữ liệu đầy đủ hoặc cập nhật trực tiếp. `source_checked` nghĩa là đã đọc nội dung nguồn, không phải mọi dữ kiện được xác minh độc lập.

## Tệp dữ liệu

- `seed.json`: dữ liệu gốc, có thể nạp vào web hoặc chuyển sang hệ quản trị khác.
- `lao_cai.sqlite`: database SQLite có bảng entities, places, knowledge, sources và liên kết nguồn.
- `sources.csv`: danh mục liên kết nguồn, mở được trong công cụ bảng tính.
- `build_database.py`: tạo lại SQLite, CSV và tài liệu từ JSON bằng Python chuẩn.

Chạy lại: `python3 build_database.py` trong thư mục này. Chỉ sửa seed.json; SQLite là tệp sinh ra.

## Nội dung tổng quan có thể sử dụng

### Lào Cai sau sắp xếp năm 2025

Tỉnh Lào Cai hiện được giới thiệu theo phạm vi sau sắp xếp từ Lào Cai và Yên Bái trước đây. Vì vậy, sổ tay lựa chọn cả nhóm Sa Pa, Fansipan, Bắc Hà và nhóm Mù Cang Chải, Khau Phạ, hồ Thác Bà, Ngòi Tu. Tên tỉnh Yên Bái trong nguồn du lịch cũ được chú thích theo thời điểm.

Nguồn: [S01: Chi tiết 34 đơn vị hành chính cấp tỉnh](https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm); [S03: Sapa](https://vietnam.travel/places-to-go/northern-vietnam/sapa); [S04: 4 things you will love about Mu Cang Chai](https://vietnam.travel/things-to-do/4-things-youll-love-about-mu-cang-chai); [S05: Thac Ba Lake: the emerald of Yen Bai](https://vietnam.travel/things-to-do/thac-ba-lake-emerald-yen-bai)

### Núi, ruộng bậc thang và hồ

Sa Pa được nguồn du lịch giới thiệu với thung lũng, núi và ruộng bậc thang; Mù Cang Chải nổi bật với cảnh quan ruộng trên sườn núi. Khau Phạ là đèo trong khu vực Mù Cang Chải – Tú Lệ. Hồ Thác Bà là hồ nhân tạo hình thành cùng công trình thủy điện Thác Bà.

Nguồn: [S03: Sapa](https://vietnam.travel/places-to-go/northern-vietnam/sapa); [S04: 4 things you will love about Mu Cang Chai](https://vietnam.travel/things-to-do/4-things-youll-love-about-mu-cang-chai); [S05: Thac Ba Lake: the emerald of Yen Bai](https://vietnam.travel/things-to-do/thac-ba-lake-emerald-yen-bai)

### Đọc lịch sử qua cảnh quan sinh kế

Bộ dữ liệu hiện có căn cứ cho lịch sử hành chính năm 2025 và mối liên hệ hồ Thác Bà với công trình thủy điện. Ruộng bậc thang được giới thiệu như cảnh quan nông nghiệp và sinh kế. Chưa có đủ nguồn để lập niên biểu lịch sử toàn tỉnh hoặc khẳng định niên đại từng làng.

Nguồn: [S01: Chi tiết 34 đơn vị hành chính cấp tỉnh](https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm); [S04: 4 things you will love about Mu Cang Chai](https://vietnam.travel/things-to-do/4-things-youll-love-about-mu-cang-chai); [S05: Thac Ba Lake: the emerald of Yen Bai](https://vietnam.travel/things-to-do/thac-ba-lake-emerald-yen-bai)

### Đời sống cộng đồng và nghề thủ công

Nguồn Mù Cang Chải giới thiệu văn hóa dệt của người Mông; bài hồ Thác Bà giới thiệu Ngòi Tu với nhà sàn, nghề đan và sinh hoạt cộng đồng Dao. Các mô tả gắn với cộng đồng trong bài, không được khái quát thành phong tục của mọi cư dân Lào Cai.

Nguồn: [S04: 4 things you will love about Mu Cang Chai](https://vietnam.travel/things-to-do/4-things-youll-love-about-mu-cang-chai); [S05: Thac Ba Lake: the emerald of Yen Bai](https://vietnam.travel/things-to-do/thac-ba-lake-emerald-yen-bai)

### Ẩm thực trong trải nghiệm cộng đồng

Bài hồ Thác Bà nhắc cơm lam và món gà nấu măng chua trong trải nghiệm địa phương. Đây là tên món theo nguồn, chưa phải công thức, thực đơn, giá hoặc chỉ dẫn về cơ sở phục vụ. Dữ liệu ẩm thực Sa Pa và Bắc Hà cần bổ sung nguồn chuyên biệt.

Nguồn: [S05: Thac Ba Lake: the emerald of Yen Bai](https://vietnam.travel/things-to-do/thac-ba-lake-emerald-yen-bai)

### Đi bộ, chợ phiên và du lịch hồ

Nguồn Sa Pa giới thiệu đi bộ khám phá làng và chợ Bắc Hà; nguồn Mù Cang Chải giới thiệu đường đi qua ruộng bậc thang, gợi ý hướng dẫn viên địa phương. Hồ Thác Bà và Ngòi Tu bổ sung trải nghiệm cảnh quan hồ và lưu trú cộng đồng. Lịch chợ, tour, đường đi và điều kiện thời tiết cần xác nhận cho chuyến thực tế.

Nguồn: [S03: Sapa](https://vietnam.travel/places-to-go/northern-vietnam/sapa); [S04: 4 things you will love about Mu Cang Chai](https://vietnam.travel/things-to-do/4-things-youll-love-about-mu-cang-chai); [S05: Thac Ba Lake: the emerald of Yen Bai](https://vietnam.travel/things-to-do/thac-ba-lake-emerald-yen-bai)

## Hồ sơ địa danh

### Sa Pa

Điểm đến vùng núi với thung lũng, ruộng bậc thang và những tuyến khám phá làng được nguồn du lịch giới thiệu.

Điểm nổi bật: Thung lũng và ruộng bậc thang; Cát Cát và Tả Phìn theo nguồn; Đi bộ khám phá.

Nguồn: [S03: Sapa](https://vietnam.travel/places-to-go/northern-vietnam/sapa)

Ghi chú dữ liệu: Hồ sơ dùng Sa Pa như điểm đến du lịch rộng hơn một phường; không tự gán mọi làng cho phường Sa Pa mới.

### Fansipan

Đỉnh núi được nguồn Sa Pa giới thiệu như điểm ngắm cảnh núi và trải nghiệm lên cao.

Điểm nổi bật: Cảnh quan núi; Trải nghiệm cáp treo theo nguồn.

Nguồn: [S03: Sapa](https://vietnam.travel/places-to-go/northern-vietnam/sapa)

Ghi chú dữ liệu: Chưa đối chiếu độ cao hiện hành, tuyến leo, điều kiện hoạt động cáp treo hoặc giá vé; không nhập các con số từ bài tổng hợp.

### Chợ Bắc Hà

Chợ phiên được nguồn du lịch Sa Pa giới thiệu như điểm khám phá sinh hoạt và giao thương địa phương.

Điểm nổi bật: Chợ phiên; Sinh hoạt địa phương.

Nguồn: [S03: Sapa](https://vietnam.travel/places-to-go/northern-vietnam/sapa)

Ghi chú dữ liệu: Nguồn ghi chợ Chủ nhật, nhưng chưa xác nhận lịch hoạt động ngày cụ thể, địa chỉ mới và thay đổi vào dịp lễ.

### Mù Cang Chải

Cảnh quan ruộng bậc thang gắn với canh tác, làng và văn hóa người Mông theo nguồn du lịch.

Điểm nổi bật: Ruộng bậc thang; Mâm Xôi; La Pán Tẩn.

Nguồn: [S04: 4 things you will love about Mu Cang Chai](https://vietnam.travel/things-to-do/4-things-youll-love-about-mu-cang-chai); [S01: Chi tiết 34 đơn vị hành chính cấp tỉnh](https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm)

Ghi chú dữ liệu: Nguồn du lịch dùng Yên Bái trước sắp xếp; database dùng phạm vi tỉnh Lào Cai mới. Chưa xác nhận mùa lúa năm cụ thể.

### Đèo Khau Phạ

Đèo trong khu vực Mù Cang Chải – Tú Lệ, được bài du lịch giới thiệu với cảnh quan thung lũng và ruộng.

Điểm nổi bật: Cảnh quan đèo; Khu vực Tú Lệ.

Nguồn: [S04: 4 things you will love about Mu Cang Chai](https://vietnam.travel/things-to-do/4-things-youll-love-about-mu-cang-chai); [S01: Chi tiết 34 đơn vị hành chính cấp tỉnh](https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm)

Ghi chú dữ liệu: Chưa kiểm tra tình trạng đường, điểm dừng an toàn hoặc dịch vụ dù lượn; không dùng hồ sơ làm hướng dẫn giao thông.

### Hồ Thác Bà

Hồ hình thành cùng công trình thủy điện Thác Bà, được nguồn du lịch giới thiệu qua mặt nước, đảo và cảnh quan ven hồ.

Điểm nổi bật: Cảnh quan mặt nước và đảo; Mối liên hệ với thủy điện; Trải nghiệm thuyền theo nguồn.

Nguồn: [S05: Thac Ba Lake: the emerald of Yen Bai](https://vietnam.travel/things-to-do/thac-ba-lake-emerald-yen-bai); [S01: Chi tiết 34 đơn vị hành chính cấp tỉnh](https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm)

Ghi chú dữ liệu: Nguồn dùng tỉnh Yên Bái cũ; chưa xác nhận bến thuyền, giờ, giá, ranh giới mặt hồ hoặc số đảo hiện hành.

### Làng Ngòi Tu

Điểm du lịch cộng đồng ở khu vực hồ Thác Bà, được nguồn giới thiệu qua nhà sàn, nghề thủ công và đời sống cộng đồng Dao.

Điểm nổi bật: Nhà sàn; Nghề đan; Trải nghiệm cộng đồng.

Nguồn: [S05: Thac Ba Lake: the emerald of Yen Bai](https://vietnam.travel/things-to-do/thac-ba-lake-emerald-yen-bai); [S01: Chi tiết 34 đơn vị hành chính cấp tỉnh](https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm)

Ghi chú dữ liệu: Không khái quát nghi lễ hoặc phong tục cho mọi người Dao; cần xin phép cộng đồng trước khi ghi hình, tái hiện nghi lễ hoặc tạo hình minh họa chi tiết.

## Lịch tham khảo, chưa xác nhận hiện hành

Không hiển thị các mục này như giá hoặc lịch hôm nay. Ngày đọc nguồn khác ngày có hiệu lực.

| Điểm | Nội dung | Giá trị theo nguồn | Ngày nguồn hiển thị |
|---|---|---|---|
| Chợ Bắc Hà | Ngày chợ phiên theo trang Sa Pa | Chủ nhật  | Không hiển thị |

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
WHERE k.entity_id = 'sa-pa';
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

Dân số và diện tích Lào Cai là số liệu phục vụ sắp xếp năm 2025; không gọi là số liệu mới nhất năm 2026.

### S02 · Nghị quyết 1673/NQ-UBTVQH15 về sắp xếp cấp xã Lào Cai

[Báo Điện tử Chính phủ](https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-quyet-so-1673-nq-ubtvqh15-sap-xep-cac-dvhc-cap-xa-cua-tinh-lao-cai-nam-2025-119250616214156071.htm) · Trạng thái: `source_checked`.

Nghị quyết ngày 16/06/2025; chính quyền xã/phường mới hoạt động từ 01/07/2025. Không suy ra địa chỉ điểm đến từ tên huyện cũ.

### S03 · Sapa

[Vietnam Tourism – Cục Du lịch Quốc gia Việt Nam](https://vietnam.travel/places-to-go/northern-vietnam/sapa) · Trạng thái: `source_checked`.

Dùng cảnh quan, địa danh và chợ phiên; loại chiều cao Fansipan, thời gian cáp treo và thời gian di chuyển chưa đối chiếu. Mùa vụ và thời tiết là tham khảo, không phải dự báo.

### S04 · 4 things you will love about Mu Cang Chai

[Vietnam Tourism – Cục Du lịch Quốc gia Việt Nam](https://vietnam.travel/things-to-do/4-things-youll-love-about-mu-cang-chai) · Trạng thái: `source_checked`.

Nguồn dùng địa danh tỉnh Yên Bái trước sắp xếp. Dùng mô tả cảnh quan và văn hóa; không dùng số giờ chạy xe hay lịch mùa vụ như cam kết hiện hành.

### S05 · Thac Ba Lake: the emerald of Yen Bai

[Vietnam Tourism – Cục Du lịch Quốc gia Việt Nam](https://vietnam.travel/things-to-do/thac-ba-lake-emerald-yen-bai) · Trạng thái: `source_checked`.

Nguồn dùng Yên Bái và huyện Yên Bình/Lục Yên trước sắp xếp. Đã ánh xạ phạm vi tỉnh qua S01; loại xếp hạng hồ, số đảo và diện tích chưa đối chiếu; không khuyến nghị món cá sống.

## Nguyên tắc biên tập

- Diễn đạt lại bằng tiếng Việt; hiển thị nguồn cạnh dữ kiện. Không sao chép toàn bộ bài hay tự sử dụng ảnh có bản quyền.
- Tên tỉnh, xã, phường và số liệu phải đi kèm thời điểm. Không dùng địa chỉ huyện trong bài cũ như địa chỉ hành chính hiện hành.
- Không tự sinh tọa độ, giá vé, lịch vận chuyển, giờ mở cửa, đường dẫn đặt vé hoặc số liệu dân số hiện tại.
- Tôn trọng tín ngưỡng và đời sống cộng đồng; truyền thuyết cần gắn nhãn truyền thuyết, không kể như sự kiện lịch sử.
- Ảnh do AI tạo phải gắn nhãn minh họa AI; không dùng ảnh tái dựng làm bằng chứng về kiến trúc hay nghi lễ thực tế.
- Các ý tưởng tương tác và gợi ý hành trình là biên tập của đội, không phải dữ kiện của nguồn hoặc cam kết dịch vụ.
