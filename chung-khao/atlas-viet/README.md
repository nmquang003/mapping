# Atlas Việt — Sổ tay điện tử Dư địa chí

Bản mẫu web tương tác dành cho bốn tỉnh/thành phố: Ninh Bình, Hà Nội, Quảng Ninh và Lào Cai.

## Chạy bản mẫu

Không cần cài thư viện frontend hoặc bước build. Từ thư mục này:

```sh
python3 -m http.server 4321 --bind 127.0.0.1 --directory dist
```

Mở http://127.0.0.1:4321/. Cần máy chủ HTTP để tải GeoJSON; không mở `index.html` bằng `file://`.

## Chạy chatbot RAG

Đặt `THUCCHIEN_API_KEY` hoặc `AITC_API_KEY` trong môi trường backend, rồi chạy từ thư mục này:

```sh
python3 rag/server.py serve --port 4322
```

Mở http://127.0.0.1:4322/. Lần đầu tạo embedding qua API BTC; những lần sau dùng lại chỉ mục nếu dữ liệu không đổi. [Model, luồng truy xuất và kiểm tra](rag/README.md).

## Đã triển khai

- Chatbot RAG tiếng Việt: embedding 142 tư liệu từ bốn SQLite, truy xuất theo địa phương/địa danh, kiểm tra căn cứ, dẫn nguồn từng câu và từ chối ngoài phạm vi/thiếu dữ liệu.

- Bản đồ SVG từ dữ liệu ranh giới 34 tỉnh/thành; làm nổi bật bốn tỉnh/thành phố trong phạm vi.
- Hình học tham khảo quần đảo Hoàng Sa, Trường Sa; bản đồ không biểu diễn đường biên biển.
- Phóng to, thu nhỏ, kéo bản đồ và chuyển nhanh tới bốn tỉnh/thành phố.
- Popup bản đồ địa phương với bốn địa danh, dấu mốc, thẻ giới thiệu và liên kết trang chi tiết.
- Bốn trang riêng bằng hash URL, hỗ trợ tải lại trực tiếp. Đường dẫn `ha-long` và `sa-pa` cũ chuyển sang `quang-ninh` và `lao-cai`; sổ tay đã lưu cũng được chuyển đổi.
- Popup hiển thị ranh giới toàn tỉnh/thành phố. Hạ Long là địa danh thuộc Quảng Ninh; Sa Pa và Mù Cang Chải thuộc phạm vi Lào Cai trên bản đồ 34 tỉnh/thành phố. Nội dung vẫn là một nhóm địa danh khởi đầu, chưa phải tư liệu đầy đủ về toàn tỉnh.
- Các tab Địa lý – Tổng quan, Địa danh, Du lịch online, Lịch sử, Văn hóa – Ẩm thực, Nguồn tham khảo.
- Du lịch online nhúng tour AirPano chính thức: 5 cảnh Hà Nội, 9 cảnh Hạ Long thuộc Quảng Ninh; chọn cảnh khởi đầu, thử lại, dừng tour và toàn màn hình. Chỉ tải iframe khi bấm bắt đầu; rời tab sẽ đóng tour. Ninh Bình và Lào Cai hiển thị trạng thái chưa có dữ liệu phù hợp.
- Lưu tỉnh/thành phố bằng localStorage, sổ tay đã lưu và thông báo ngoài phạm vi.
- Bố cục máy tính/điện thoại; modal dùng bàn phím và Escape; các tab dùng phím mũi tên.
- Font và ảnh giao diện phục vụ từ thư mục local. Tour AirPano cần Internet và có thể phát âm thanh khi bắt đầu.

## Nội dung đang biên soạn

Nội dung ngắn được đánh dấu là bản mẫu. Tọa độ địa danh là vị trí tham khảo gần đúng, chưa đối chiếu từng điểm với tài liệu chính thức. Không dùng cho đo đạc, địa chính hoặc dẫn đường.

Ảnh hiện tại là ảnh thực tế có nguồn và giấy phép, **chưa phải ảnh AI**. Chatbot **RAG đã kết nối API BTC** qua backend Python, truy xuất bốn database có nguồn. Xem [hướng dẫn RAG](rag/README.md).

Trước khi nộp: đối chiếu ranh giới, tọa độ, nội dung và mốc dữ liệu; bổ sung hình minh họa AI bằng API BTC và tiếp tục đánh giá chatbot tiếng Việt trả lời từ kho tư liệu có dẫn nguồn.

## Cấu trúc

- `dist/index.html`: khung trang, modal và khung trợ lý.
- `dist/styles.css`: theme giấy ngà, xanh rừng, vàng đồng; bố cục responsive.
- `dist/app.js`: dữ liệu nội dung ngắn, phép chiếu bản đồ, điều hướng và tương tác.
- `dist/assets/vietnam-provinces.geojson`: dữ liệu ranh giới đã giản lược để hiển thị.
- `dist/assets/credits.json`: tác giả, nguồn, giấy phép và thay đổi đối với ảnh.
- `scripts/prepare_assets.py`: tái tạo tài nguyên từ nguồn công khai đã ghim phiên bản.
- `scripts/check_ui.py`: kiểm tra luồng thực trên Chromium và tạo ảnh QA ở `.qa/`.
- `scripts/check_tours.py`: kiểm tra giao diện chủ với phản hồi iframe giả lập để xác minh tải khi bắt đầu, chọn cảnh, thử lại/dừng, dọn iframe và responsive. Khả năng tải ảnh thực bên trong tour phụ thuộc AirPano.

## Tour du lịch online

Tour dùng mã nhúng do AirPano cung cấp, với ghi công `Courtesy of www.AirPano.com` và liên kết nguồn. Tên cảnh tiếng Việt dựa trên cấu hình tour gốc; thứ tự cảnh giữ nguyên vì tham số `startscene` dùng chỉ số từ 0. Quảng Ninh chỉ có tour khu vực Hạ Long, chưa có tour Yên Tử hoặc Cô Tô.

Danh sách ngoài khung chọn **cảnh khởi đầu**. Người dùng vẫn chuyển được cảnh bên trong tour; do iframe khác origin, web không đồng bộ lựa chọn bên ngoài theo thao tác trong AirPano và không xác nhận được ảnh 360° bên trong đã tải thành công. Nút thử lại và liên kết nguồn luôn có khi tour mở. Ninh Bình chưa nhúng trang nguồn có iframe bất thường; ảnh panorama nguồn chưa tải được.

Dữ liệu tải về trong `data/360-tours/` vẫn là bản lưu riêng, chưa được phục vụ công khai cùng website. Không sao chép runtime hoặc ảnh AirPano vào `dist/` trong phiên bản nhúng này.

## Nguồn bản đồ

1. [Thang Le Quoc — Vietnamese Provinces Database](https://github.com/thanglequoc/vietnamese-provinces-database), bản chụp `geojson_11Mar2026`, revision `8b78ba5118715e1fa81769286724db79346abf52`. Nguồn dữ liệu gốc được dự án ghi là `sapnhap.bando.com.vn`. Giấy phép mã nguồn MIT nằm trong `data/GIS-REPOSITORY-LICENSE.txt`; quyền dữ liệu nền theo điều kiện nguồn gốc, không mặc định MIT áp dụng cho bản đồ nền.
2. [Nguyễn Duy Liêm — Free-GIS-Data](https://github.com/nguyenduy1133/Free-GIS-Data), chỉ lấy các thành phần ngoài khơi có ghi chú Hoàng Sa và Trường Sa. README cho phép sử dụng công cộng miễn phí và yêu cầu trích dẫn. Revision được ghi trong `vietnam-provinces.geojson`.
3. Nguồn đối chiếu: [Bản đồ hành chính Việt Nam](https://vnsdi.mae.gov.vn/bandohanhchinh/) và [Bản đồ sáp nhập](https://sapnhap.bando.com.vn/).

Dữ liệu cộng đồng không được trình bày như dữ liệu đã được cơ quan nhà nước xác nhận cho bản mẫu này.

## Ảnh và font

- Tràng An: Benjamin Smith / Wikimedia Commons — CC BY-SA 4.0.
- Hồ Hoàn Kiếm: Tranhuutukkt / Wikimedia Commons — CC BY-SA 4.0.
- Panorama Hạ Long: Isderion / Wikimedia Commons — CC BY-SA 3.0 DE.
- Ruộng bậc thang Sa Pa: Eerin25 / Wikimedia Commons — CC0 1.0.

Liên kết nguồn và giấy phép có trong `credits.json` và giao diện. Ảnh được thu nhỏ tối đa 1600px; CSS cắt khung hiển thị. Giữ giấy phép tương ứng cho các bản ảnh này.

Be Vietnam Pro và Playfair Display được phân phối theo SIL Open Font License; bản giấy phép đi kèm trong `dist/assets/fonts/`.

## Kiểm tra

Khởi động máy chủ HTTP như trên, sau đó:

```sh
node --check dist/app.js
uv run --no-project --with playwright python scripts/check_ui.py
uv run --no-project --with playwright python scripts/check_tours.py
```

Cần Chromium của Playwright có sẵn để chạy kiểm tra UI. Script kiểm tra 34 vùng, bốn luồng bản đồ → popup → trang riêng, tất cả tab, deep link, lưu sổ tay, vùng ngoài phạm vi và bố cục điện thoại.

## Xuất bản

`dist/` là thư mục website tĩnh có thể triển khai. Bản mẫu ban đầu đã được commit/push; bản cập nhật phạm vi chưa xuất bản lên Sites. Tuân theo quy định trong `../AGENTS.md` khi commit/push tiếp.
