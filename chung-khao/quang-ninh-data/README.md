# Bộ dữ liệu giới thiệu Quảng Ninh

Ngày đọc nguồn: 06/10/2026.

Sổ tay giới thiệu tổng quan Quảng Ninh và 7 địa danh tuyển chọn: Vịnh Hạ Long, Vịnh Bái Tử Long, Cô Tô, Đảo Thanh Lân, Quan Lạn, Yên Tử, Bảo tàng – Thư viện Quảng Ninh. Không bao phủ mọi địa danh trong địa phương.

Đây là bộ dữ liệu khởi đầu, không phải dữ liệu đầy đủ hoặc cập nhật trực tiếp. `source_checked` nghĩa là đã đọc nội dung nguồn, không phải mọi dữ kiện được xác minh độc lập.

## Tệp dữ liệu

- `seed.json`: dữ liệu gốc, có thể nạp vào web hoặc chuyển sang hệ quản trị khác.
- `quang_ninh.sqlite`: database SQLite có bảng entities, places, knowledge, sources và liên kết nguồn.
- `sources.csv`: danh mục liên kết nguồn, mở được trong công cụ bảng tính.
- `build_database.py`: tạo lại SQLite, CSV và tài liệu từ JSON bằng Python chuẩn.

Chạy lại: `python3 build_database.py` trong thư mục này. Chỉ sửa seed.json; SQLite là tệp sinh ra.

## Nội dung tổng quan có thể sử dụng

### Quảng Ninh trong phạm vi sổ tay

Sổ tay tập trung vào cảnh quan biển đảo, di tích Yên Tử và bảo tàng địa phương. Theo Nghị quyết 36/2026/QH16, thành phố Quảng Ninh được thành lập từ toàn bộ tỉnh Quảng Ninh, có hiệu lực từ 01/09/2026. Các bài du lịch cũ dùng tên tỉnh được giữ nguyên tên nguồn và chú thích thời điểm.

Nguồn: [S01: Nghị quyết 36/2026/QH16 thành lập thành phố Quảng Ninh](https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-quyet-so-36-2026-qh16-thanh-lap-thanh-pho-quang-ninh-tu-1-9-2026-119260903082603583.htm); [S02: Ha Long](https://vietnam.travel/places-to-go/northern-vietnam/ha-long); [S05: Khu di tích lịch sử và danh lam thắng cảnh Yên Tử](https://www.quangninh.gov.vn/Trang/ChiTietBVGioiThieu.aspx?bvid=530); [S06: Bảo tàng – Thư viện thành phố](https://www.quangninh.gov.vn/so/sovanhoathethao/trang/chitietbvgioithieu.aspx?bvid=84)

### Biển, đảo và cảnh quan núi

Hạ Long nổi bật với cảnh quan núi đá vôi giữa biển. Quan Lạn nằm trong vịnh Bái Tử Long; Cô Tô có bãi biển, bờ đá và đảo Thanh Lân. Yên Tử bổ sung cảnh quan núi rừng, tạo một tuyến chủ đề khác với du lịch biển đảo.

Nguồn: [S02: Ha Long](https://vietnam.travel/places-to-go/northern-vietnam/ha-long); [S03: Co To Island: pristine beauty of Northeast Vietnam](https://www.vietnam.travel/vi/things-to-do/co-island-pristine-beauty-northeast-vietnam); [S04: Discovering the beauty of Quan Lan Island](https://vietnamtourism.gov.vn/en/post/9785); [S05: Khu di tích lịch sử và danh lam thắng cảnh Yên Tử](https://www.quangninh.gov.vn/Trang/ChiTietBVGioiThieu.aspx?bvid=530)

### Lịch sử gắn với Yên Tử

Yên Tử gắn với Trần Nhân Tông và Thiền phái Trúc Lâm. Khu di tích được xếp hạng quốc gia đặc biệt năm 2012; năm 2025, phần Yên Tử thuộc quần thể di sản văn hóa thế giới liên địa phương Yên Tử – Vĩnh Nghiêm – Côn Sơn, Kiếp Bạc. Đây là hai mốc và hai phạm vi khác nhau.

Nguồn: [S05: Khu di tích lịch sử và danh lam thắng cảnh Yên Tử](https://www.quangninh.gov.vn/Trang/ChiTietBVGioiThieu.aspx?bvid=530)

### Tín ngưỡng và ký ức địa phương

Có thể giới thiệu kiến trúc chùa, am, tháp ở Yên Tử; cụm đình, đền, chùa tại Quan Lạn; và chức năng lưu giữ, giới thiệu di sản của Bảo tàng – Thư viện Quảng Ninh. Khi kể về hành hương, trình bày như sinh hoạt tín ngưỡng, không hứa hẹn cầu may.

Nguồn: [S04: Discovering the beauty of Quan Lan Island](https://vietnamtourism.gov.vn/en/post/9785); [S05: Khu di tích lịch sử và danh lam thắng cảnh Yên Tử](https://www.quangninh.gov.vn/Trang/ChiTietBVGioiThieu.aspx?bvid=530); [S06: Bảo tàng – Thư viện thành phố](https://www.quangninh.gov.vn/so/sovanhoathethao/trang/chitietbvgioithieu.aspx?bvid=84)

### Ẩm thực biển đảo

Bài giới thiệu Cô Tô nhắc các hải sản như mực, hàu, bề bề và sá sùng. Đây là danh mục nguyên liệu được nguồn du lịch giới thiệu, chưa phải danh sách món độc quyền của địa phương, nhà hàng khuyến nghị hoặc bảng giá.

Nguồn: [S03: Co To Island: pristine beauty of Northeast Vietnam](https://www.vietnam.travel/vi/things-to-do/co-island-pristine-beauty-northeast-vietnam)

### Trải nghiệm theo chủ đề

Nguồn du lịch giới thiệu ngắm cảnh vịnh bằng thuyền, chèo kayak tại Hạ Long, khám phá bãi biển và bờ đá ở Cô Tô, Quan Lạn; nguồn Yên Tử giới thiệu tuyến kiến trúc tôn giáo giữa núi rừng. Việc đặt tour, điều kiện hoạt động trên biển và lịch lễ hội từng năm cần nguồn vận hành hiện hành.

Nguồn: [S02: Ha Long](https://vietnam.travel/places-to-go/northern-vietnam/ha-long); [S03: Co To Island: pristine beauty of Northeast Vietnam](https://www.vietnam.travel/vi/things-to-do/co-island-pristine-beauty-northeast-vietnam); [S04: Discovering the beauty of Quan Lan Island](https://vietnamtourism.gov.vn/en/post/9785); [S05: Khu di tích lịch sử và danh lam thắng cảnh Yên Tử](https://www.quangninh.gov.vn/Trang/ChiTietBVGioiThieu.aspx?bvid=530)

## Hồ sơ địa danh

### Vịnh Hạ Long

Cảnh quan vịnh với núi đá vôi, đảo và hang động; phù hợp giới thiệu địa hình karst và trải nghiệm ngắm cảnh trên biển.

Điểm nổi bật: Núi đá vôi giữa biển; Hang động; Du thuyền và kayak theo nguồn du lịch.

Nguồn: [S02: Ha Long](https://vietnam.travel/places-to-go/northern-vietnam/ha-long)

Ghi chú dữ liệu: Không đồng nhất toàn khu du lịch Hạ Long với ranh giới di sản UNESCO. Không đưa Lan Hạ, Cát Bà vào phạm vi Quảng Ninh.

### Vịnh Bái Tử Long

Vịnh được nguồn giới thiệu Quan Lạn xác định là không gian biển nơi đảo Quan Lạn tọa lạc. Hồ sơ hiện tập trung vào mối liên hệ với Quan Lạn.

Điểm nổi bật: Không gian biển đảo; Quan Lạn.

Nguồn: [S04: Discovering the beauty of Quan Lan Island](https://vietnamtourism.gov.vn/en/post/9785)

Ghi chú dữ liệu: Nguồn năm 2015; chưa có khảo sát toàn vịnh, ranh giới, hệ sinh thái hoặc tour hiện hành.

### Cô Tô

Điểm đến biển đảo có bãi Hồng Vàn, Vàn Chảy và cảnh quan bờ đá Cầu Mỵ.

Điểm nổi bật: Bãi Hồng Vàn; Bãi Vàn Chảy; Bờ đá Cầu Mỵ.

Nguồn: [S03: Co To Island: pristine beauty of Northeast Vietnam](https://www.vietnam.travel/vi/things-to-do/co-island-pristine-beauty-northeast-vietnam)

Ghi chú dữ liệu: Hồ sơ nội dung đã có nguồn; địa chỉ hành chính chi tiết, tọa độ, giá và giờ hiện hành chưa xác nhận.

### Đảo Thanh Lân

Đảo thuộc khu vực Cô Tô, được nguồn du lịch giới thiệu với rừng và cảnh quan bờ đá.

Điểm nổi bật: Cảnh quan rừng; Bờ biển và đá.

Nguồn: [S03: Co To Island: pristine beauty of Northeast Vietnam](https://www.vietnam.travel/vi/things-to-do/co-island-pristine-beauty-northeast-vietnam)

Ghi chú dữ liệu: Hồ sơ nội dung đã có nguồn; địa chỉ hành chính chi tiết, tọa độ, giá và giờ hiện hành chưa xác nhận.

### Quan Lạn

Đảo trong vịnh Bái Tử Long, kết hợp bãi biển với cụm di tích đình, đền, chùa.

Điểm nổi bật: Bãi Quan Lạn; Sơn Hào và Minh Châu; Cụm di tích văn hóa.

Nguồn: [S04: Discovering the beauty of Quan Lan Island](https://vietnamtourism.gov.vn/en/post/9785)

Ghi chú dữ liệu: Bài năm 2015. Chưa xác nhận địa chỉ hành chính chi tiết, lịch tàu hoặc dịch vụ hiện hành.

### Yên Tử

Khu di tích và danh thắng gắn với Trần Nhân Tông, Thiền phái Trúc Lâm và hệ thống chùa, am, tháp giữa núi rừng.

Điểm nổi bật: Chùa Hoa Yên; Vườn tháp Huệ Quang; Chùa Đồng.

Nguồn: [S05: Khu di tích lịch sử và danh lam thắng cảnh Yên Tử](https://www.quangninh.gov.vn/Trang/ChiTietBVGioiThieu.aspx?bvid=530)

Ghi chú dữ liệu: Nguồn ngày 14/07/2025 nêu khu di tích phần lớn ở phường Yên Tử, một phần ở phường Hoàng Quế. Không coi toàn quần thể UNESCO liên địa phương nằm tại Quảng Ninh.

### Bảo tàng – Thư viện Quảng Ninh

Đơn vị lưu giữ, nghiên cứu, trưng bày và giới thiệu di sản, lịch sử, văn hóa, thiên nhiên, con người Quảng Ninh.

Điểm nổi bật: Di sản địa phương; Giáo dục lịch sử và văn hóa.

Nguồn: [S06: Bảo tàng – Thư viện thành phố](https://www.quangninh.gov.vn/so/sovanhoathethao/trang/chitietbvgioithieu.aspx?bvid=84)

Ghi chú dữ liệu: Nguồn đã đọc là hồ sơ chức năng đơn vị; chưa đủ căn cứ mô tả từng tầng trưng bày, kiến trúc, địa chỉ cổng vào hay vé.

## Lịch tham khảo, chưa xác nhận hiện hành

Không hiển thị các mục này như giá hoặc lịch hôm nay. Ngày đọc nguồn khác ngày có hiệu lực.

| Điểm | Nội dung | Giá trị theo nguồn | Ngày nguồn hiển thị |
|---|---|---|---|
| Yên Tử | Mốc lễ hội thường niên được bài nguồn nêu | Bắt đầu ngày 10 tháng Giêng âm lịch, kéo dài trong mùa xuân  | 2025-07-14 |

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
WHERE k.entity_id = 'vinh-ha-long';
```

## Các khoảng trống cần bổ sung

- Chưa có bộ giá vé hiện hành, chi phí ăn ở, lịch vận chuyển hoặc dịch vụ đặt vé đã xác nhận.
- Chưa đối chiếu tọa độ từng địa danh và ranh giới hành chính để đặt marker/map3D; latitude và longitude để null.
- Chưa có đầy đủ địa chỉ xã/phường mới của từng điểm; chỉ điền địa chỉ khi nguồn trực tiếp nêu.
- Chưa có ảnh AI, âm thanh thuyết minh hoặc mô hình 3D; đây là database nội dung.
- Bộ hồ sơ tuyển chọn không bao phủ mọi địa danh, lễ hội, cộng đồng và món ăn của địa phương.

## Danh mục nguồn

### S01 · Nghị quyết 36/2026/QH16 thành lập thành phố Quảng Ninh

[Báo Điện tử Chính phủ](https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-quyet-so-36-2026-qh16-thanh-lap-thanh-pho-quang-ninh-tu-1-9-2026-119260903082603583.htm) · Trạng thái: `source_checked`.

Nghị quyết thông qua ngày 24/08/2026, hiệu lực 01/09/2026; đọc trực tiếp nội dung Điều 1–3.

### S02 · Ha Long

[Vietnam Tourism – Cục Du lịch Quốc gia Việt Nam](https://vietnam.travel/places-to-go/northern-vietnam/ha-long) · Trạng thái: `source_checked`.

Chỉ lấy mô tả cảnh quan và trải nghiệm tổng quát. Nội dung có nhắc điểm ngoài Quảng Ninh; đã loại khỏi hồ sơ. Không lấy lịch hoặc thời gian vận chuyển làm thông tin hiện hành.

### S03 · Co To Island: pristine beauty of Northeast Vietnam

[Vietnam Tourism – Cục Du lịch Quốc gia Việt Nam](https://www.vietnam.travel/vi/things-to-do/co-island-pristine-beauty-northeast-vietnam) · Trạng thái: `source_checked`.

Trang tiếng Việt ghi bản dịch do AI tạo. Chỉ lấy mô tả địa danh tổng quát; loại số liệu, niên đại hải đăng và quy định hạn chế nhựa chưa đối chiếu.

### S04 · Discovering the beauty of Quan Lan Island

[Cục Du lịch Quốc gia Việt Nam – TITC](https://vietnamtourism.gov.vn/en/post/9785) · Trạng thái: `source_checked`.

Bài năm 2015 dùng địa danh huyện Vân Đồn trước sắp xếp. Không nhập số lượng phòng, cơ sở lưu trú, lịch tàu, giá hay thời gian chạy tàu như hiện hành.

### S05 · Khu di tích lịch sử và danh lam thắng cảnh Yên Tử

[Cổng thông tin điện tử Quảng Ninh](https://www.quangninh.gov.vn/Trang/ChiTietBVGioiThieu.aspx?bvid=530) · Trạng thái: `source_checked`.

Bài nêu địa giới phường sau sắp xếp và sự kiện UNESCO ngày 12/07/2025. Chỉ lấy phần di tích Quảng Ninh, không mở rộng hồ sơ sang Bắc Ninh hoặc Hải Phòng.

### S06 · Bảo tàng – Thư viện thành phố

[Sở Văn hóa, Thể thao và Du lịch Quảng Ninh](https://www.quangninh.gov.vn/so/sovanhoathethao/trang/chitietbvgioithieu.aspx?bvid=84) · Trạng thái: `source_checked`.

Nguồn về chức năng và nhiệm vụ đơn vị, không phải hướng dẫn trưng bày hoặc giá vé. Không nhập thông tin cá nhân cán bộ vào database du lịch.

## Nguyên tắc biên tập

- Diễn đạt lại bằng tiếng Việt; hiển thị nguồn cạnh dữ kiện. Không sao chép toàn bộ bài hay tự sử dụng ảnh có bản quyền.
- Tên tỉnh, xã, phường và số liệu phải đi kèm thời điểm. Không dùng địa chỉ huyện trong bài cũ như địa chỉ hành chính hiện hành.
- Không tự sinh tọa độ, giá vé, lịch vận chuyển, giờ mở cửa, đường dẫn đặt vé hoặc số liệu dân số hiện tại.
- Tôn trọng tín ngưỡng và đời sống cộng đồng; truyền thuyết cần gắn nhãn truyền thuyết, không kể như sự kiện lịch sử.
- Ảnh do AI tạo phải gắn nhãn minh họa AI; không dùng ảnh tái dựng làm bằng chứng về kiến trúc hay nghi lễ thực tế.
- Các ý tưởng tương tác và gợi ý hành trình là biên tập của đội, không phải dữ kiện của nguồn hoặc cam kết dịch vụ.
