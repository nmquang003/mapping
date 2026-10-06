# Database Dư địa chí: Ninh Bình, Hà Nội, Lào Cai, Quảng Ninh

Ngày đọc nguồn: **06/10/2026**. Bốn bộ dữ liệu tiếng Việt có cùng cấu trúc SQLite, dùng trực tiếp cho web hoặc làm dữ liệu truy xuất cho chatbot.

Điểm vào cho ứng dụng: [data-catalog.json](data-catalog.json). Manifest chứa mã địa phương, tên hiển thị, đường dẫn JSON/SQLite, số bản ghi và thông tin media. Mọi đường dẫn trong manifest được tính từ thư mục `chung-khao/`; ứng dụng không cần tự đoán tên file database.

| Bộ dữ liệu | Hồ sơ địa danh | Dữ kiện | Tổng quan | Bản ghi nguồn | Lịch tham khảo |
|---|---:|---:|---:|---:|---:|
| Ninh Bình | 7 | 26 | 6 | 18 | 8 |
| Quảng Ninh | 7 | 20 | 6 | 6 | 1 |
| Hà Nội | 8 | 22 | 6 | 7 | 1 |
| Lào Cai | 7 | 21 | 6 | 5 | 1 |

Tổng cộng **29 hồ sơ địa danh, 89 dữ kiện và 36 bản ghi nguồn**, tương ứng 34 URL khác nhau trong bốn database. Các nguồn dùng chung vẫn có ID cục bộ trong từng bộ dữ liệu. `source_checked` nghĩa là đã đọc nội dung nguồn, chưa phải xác minh độc lập mọi dữ kiện.

## Mở dữ liệu

| Địa phương | Tài liệu và nguồn | JSON để nạp vào web | SQLite |
|---|---|---|---|
| Quảng Ninh | [README](quang-ninh-data/README.md) · [Nguồn CSV](quang-ninh-data/sources.csv) | [seed.json](quang-ninh-data/seed.json) | [quang_ninh.sqlite](quang-ninh-data/quang_ninh.sqlite) |
| Hà Nội | [README](ha-noi-data/README.md) · [Nguồn CSV](ha-noi-data/sources.csv) | [seed.json](ha-noi-data/seed.json) | [ha_noi.sqlite](ha-noi-data/ha_noi.sqlite) |
| Lào Cai | [README](lao-cai-data/README.md) · [Nguồn CSV](lao-cai-data/sources.csv) | [seed.json](lao-cai-data/seed.json) | [lao_cai.sqlite](lao-cai-data/lao_cai.sqlite) |
| Ninh Bình | [README](ninh-binh-data/README.md) · [Nguồn CSV](ninh-binh-data/sources.csv) | [seed.json](ninh-binh-data/seed.json) | [ninh_binh.sqlite](ninh-binh-data/ninh_binh.sqlite) |

Giữ các bộ dưới `chung-khao/<địa-phương>-data/` để nằm cạnh sản phẩm vòng chung khảo và giữ đường dẫn tương đối ổn định. Không cần dịch vụ database ngoài để bắt đầu: frontend có thể nạp `seed.json` được phục vụ qua HTTP; backend mở SQLite ở chế độ chỉ đọc.

Ví dụ backend Python chạy từ thư mục gốc repo:

```python
import json
import sqlite3
from pathlib import Path

data_root = Path("chung-khao").resolve()
catalog = json.loads((data_root / "data-catalog.json").read_text(encoding="utf-8"))
dataset = next(item for item in catalog["datasets"] if item["id"] == "ninh-binh")
database_path = data_root / dataset["paths"]["sqlite"]
connection = sqlite3.connect(database_path.as_uri() + "?mode=ro", uri=True)
try:
    places = connection.execute("SELECT id, summary FROM places").fetchall()
finally:
    connection.close()
```

## Ảnh và prompt Ninh Bình

[Thư viện ảnh Ninh Bình](ninh-binh-data/images/README.md) hiện có **8 ảnh tham chiếu và 8 prompt**, kèm [nguồn, tác giả và giấy phép](ninh-binh-data/images/references.json). Chưa có ảnh AI đầu ra; ứng dụng cần kiểm tra trạng thái trong manifest trước khi dùng đường dẫn ảnh dự kiến. Bộ Tam Cốc – Bích Động có hai prompt riêng nhưng dùng chung mã địa danh `tam-coc-bich-dong`.

## Nội dung tuyển chọn

- **Ninh Bình:** Tràng An, Cố đô Hoa Lư, Tam Cốc – Bích Động, Cúc Phương, Bái Đính, Phát Diệm, Hang Múa.
- **Quảng Ninh:** Vịnh Hạ Long, vịnh Bái Tử Long, Cô Tô, đảo Thanh Lân, Quan Lạn, Yên Tử, Bảo tàng – Thư viện Quảng Ninh. Hồ sơ Bái Tử Long hiện giới hạn ở quan hệ địa lý với Quan Lạn; hồ sơ bảo tàng chủ yếu có chức năng giáo dục và lưu giữ di sản.
- **Hà Nội:** Hồ Hoàn Kiếm, phố cổ, Văn Miếu – Quốc Tử Giám, Hoàng thành Thăng Long, Lăng Chủ tịch Hồ Chí Minh, Nhà hát Lớn, Bảo tàng Dân tộc học Việt Nam, Nhà thờ Lớn.
- **Lào Cai:** Sa Pa, Fansipan, chợ Bắc Hà, Mù Cang Chải, đèo Khau Phạ, hồ Thác Bà, làng Ngòi Tu.

Mỗi database có sáu mục tổng quan: tổng quan và phạm vi, địa lý, lịch sử, văn hóa, ẩm thực, trải nghiệm. Độ sâu phụ thuộc nguồn đã đọc; mục lịch sử Lào Cai hiện chỉ có lịch sử hành chính và ngữ cảnh thủy điện, chưa có niên biểu toàn tỉnh.

## Phạm vi hành chính và thời điểm

- **Quảng Ninh:** bài đăng Chính phủ ngày 03/09/2026 dẫn Nghị quyết 36/2026/QH16, thành lập thành phố Quảng Ninh từ toàn bộ tỉnh Quảng Ninh, hiệu lực 01/09/2026. Metadata ghi loại đơn vị `city`. Nguồn du lịch cũ có tên tỉnh được chú thích theo thời điểm.
- **Hà Nội:** không sáp nhập cấp tỉnh trong đợt năm 2025; số 126 đơn vị cấp xã, gồm 51 phường và 75 xã, có mốc nghị quyết năm 2025.
- **Lào Cai:** phạm vi sau sắp xếp năm 2025 gồm Lào Cai và Yên Bái trước đây. Mù Cang Chải, Khau Phạ, Thác Bà, Ngòi Tu trong nguồn cũ được ánh xạ vào tỉnh Lào Cai bằng nguồn hành chính. Diện tích 13.256,92 km² và dân số 1.778.785 là số liệu phục vụ sắp xếp năm 2025, không được gọi là số liệu mới nhất năm 2026.

Tên trường `scope.province_id` và `scope.province_name` được giữ để tương thích schema Ninh Bình; đây là khóa địa phương cấp tỉnh, bao gồm thành phố. Dùng `scope.administrative_type` để hiển thị đúng loại đơn vị trong ba bộ mới.

## Cấu trúc SQLite và cách lấy nguồn

`entities` lưu địa phương và địa danh; `places` lưu hồ sơ; `knowledge` lưu mục tổng quan, dữ kiện và lịch tham khảo; `sources` lưu URL và thời điểm đọc. `knowledge_sources` và `place_sources` liên kết nội dung với nguồn.

View `chatbot_knowledge` chỉ chứa mục tổng quan và dữ kiện có trạng thái `source_checked` hoặc `dated_reference`. Lịch tham khảo chưa xác nhận hiện hành bị loại khỏi view này. Bộ dữ liệu chưa có hệ thống tìm kiếm, embedding, AI API hoặc bộ kiểm soát câu trả lời tự động.

```sql
SELECT k.id, k.text, k.status, k.time_basis, s.id AS source_id,
       s.title, s.publisher, s.url, s.accessed_on
FROM chatbot_knowledge k
JOIN knowledge_sources ks ON ks.knowledge_id = k.id
JOIN sources s ON s.id = ks.source_id
WHERE k.entity_id = 'yen-tu';
```

Đổi `entity_id` theo địa danh trong database đang chọn. Chọn database trước khi tìm kiếm; backend phải kiểm tra phạm vi câu hỏi và chỉ gửi cho AI nội dung được truy xuất cùng nguồn. Khi không có căn cứ, trả lời “Chưa có thông tin này trong sổ tay”.

ID nguồn `S01`, dữ kiện `F01` và tổng quan `O01` là ID cục bộ của từng database. Nếu nhập chung một database, cần dùng khóa ghép `(province_id, id)` hoặc thêm tiền tố địa phương; không gộp trực tiếp các bảng rồi ghi đè ID.

## Dữ liệu còn thiếu và cách hiển thị

Chưa xác nhận giá vé hiện hành, chi phí ăn ở, lịch tàu/xe, đường dẫn đặt vé, tọa độ và tình trạng hoạt động từng ngày. Các trường chưa có căn cứ để `null`; web nên hiển thị “Chưa có dữ liệu đã xác nhận” và không đặt marker tùy ý.

Ba lịch tham khảo đã tách riêng: lễ hội Yên Tử, giờ trên website Hoàng thành, ngày chợ Bắc Hà. Tất cả có `publish_as_current: false`; chưa dùng như lịch hôm nay.

Nội dung văn hóa không được biến thành lời hứa cầu may hoặc khái quát phong tục cho mọi cộng đồng. Khi tạo ảnh AI, gắn nhãn “Minh họa do AI tạo”; ảnh minh họa không phải ảnh tư liệu hoặc bằng chứng lịch sử.

## Tạo lại database

Trong từng thư mục, sửa `seed.json`, sau đó chạy `python3 build_database.py`. Script dùng Python chuẩn để tạo SQLite, CSV và README; kiểm tra ID, tham chiếu nguồn, khóa ngoại và tính toàn vẹn. SQLite là tệp sinh ra, JSON là dữ liệu gốc.

## Một số nguồn web tiêu biểu

- [Nghị quyết thành lập thành phố Quảng Ninh](https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-quyet-so-36-2026-qh16-thanh-lap-thanh-pho-quang-ninh-tu-1-9-2026-119260903082603583.htm).
- [Yên Tử – Cổng thông tin Quảng Ninh](https://www.quangninh.gov.vn/Trang/ChiTietBVGioiThieu.aspx?bvid=530).
- [Hoàng thành Thăng Long – cơ quan quản lý](https://hoangthanhthanglong.vn/thu-ngo/).
- [Nghị quyết sắp xếp Hà Nội – TTXVN](https://nvsk.vnanet.vn/toan-van-nghi-quyet-so-1656-nq-ubtvqh15-sap-xep-cac-don-vi-hanh-chinh-cap-xa-cua-thanh-pho-ha-noi-nam-2025-1-172085.vna).
- [Sa Pa – Vietnam Tourism](https://vietnam.travel/places-to-go/northern-vietnam/sapa).
- [Hồ Thác Bà – Vietnam Tourism](https://vietnam.travel/things-to-do/thac-ba-lake-emerald-yen-bai).

Danh mục đầy đủ, ghi chú hạn chế của từng nguồn và dữ kiện được dẫn từ nguồn nằm trong README và sources.csv tương ứng.
