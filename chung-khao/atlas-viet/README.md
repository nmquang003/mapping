# Atlas Việt — Sổ tay điện tử Dư địa chí

Bản mẫu web tương tác dành cho bốn tỉnh/thành phố: Ninh Bình, Hà Nội, Quảng Ninh và Lào Cai.

## Chạy bản mẫu

Không cần cài thư viện frontend hoặc bước build. Từ thư mục này:

```sh
python3 -m http.server 4321 --bind 127.0.0.1 --directory dist
```

Mở http://127.0.0.1:4321/. Cần máy chủ HTTP để tải GeoJSON; không mở `index.html` bằng `file://`.

## Chạy chatbot RAG

Để test tạm bằng OpenRouter, giữ `OPENROUTER_API_KEY` trong `.env` ở thư mục gốc repository và chạy `python3 run.py --no-browser` từ `atlas-viet/`, rồi mở http://127.0.0.1:4322/. Atlas trò chuyện như hướng dẫn viên du lịch, gợi ý trải nghiệm từ tư liệu có nguồn. [Cấu hình OpenRouter và chuyển lại BTC](rag/README.md#test-với-openrouter).

Khung chat hiển thị ảnh minh họa theo địa danh đang giới thiệu, lấy từ bộ ảnh AI local. Bấm ảnh để xem lớn; thử câu “Cho mình xem ảnh minh họa Tràng An”. Giao diện hỗ trợ mở rộng trên máy tính, gợi ý câu hỏi, nguồn tham khảo đánh số và bố cục điện thoại.

Có gói bàn giao ở `release/atlas-viet-rag.zip`; xem [hướng dẫn chạy độc lập](rag/README.md).

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
- Bong bóng cạnh nút Hỏi Atlas khi rê chuột lên 34 tỉnh/thành, dấu mốc hoặc thẻ địa phương; lời chào và gợi ý luân phiên hoàn toàn offline, không gọi API. Mỗi lần hover chọn ngẫu nhiên một câu khác câu vừa hiện, kèm icon; bong bóng chỉ hiện câu chat. Bốn địa phương có câu gợi ý riêng; các địa phương còn lại hiện lời chào và thông báo đang chuẩn bị sổ tay. Chỉnh câu soạn sẵn trong `dist/province-hints.js`.
- Popup bản đồ địa phương với bốn địa danh, dấu mốc, thẻ giới thiệu và liên kết trang chi tiết.
- Bốn trang riêng bằng hash URL, hỗ trợ tải lại trực tiếp. Đường dẫn `ha-long` và `sa-pa` cũ chuyển sang `quang-ninh` và `lao-cai`; sổ tay đã lưu cũng được chuyển đổi.
- Popup hiển thị ranh giới toàn tỉnh/thành phố. Hạ Long là địa danh thuộc Quảng Ninh; Sa Pa và Mù Cang Chải thuộc phạm vi Lào Cai trên bản đồ 34 tỉnh/thành phố. Nội dung vẫn là một nhóm địa danh khởi đầu, chưa phải tư liệu đầy đủ về toàn tỉnh.
- Các tab Địa lý – Tổng quan, Địa danh, Bộ ảnh AI, Du lịch online, Lịch sử, Văn hóa – Ẩm thực, Nguồn tham khảo.
- Du lịch online dùng trình xem Pannellum local: 8 cảnh Ninh Bình, 5 cảnh Hà Nội, 9 cảnh Hạ Long thuộc Quảng Ninh; kéo nhìn quanh, zoom, chuyển cảnh qua danh sách hoặc hotspot, thử lại/dừng và toàn màn hình. Chỉ tải ảnh khi bấm bắt đầu; rời tab giải phóng viewer. Lào Cai chưa có ảnh panorama phù hợp.
- Sổ tay cá nhân tại `#/so-tay`: lưu/bỏ lưu địa phương, ghi chú tự lưu, trạng thái đã khám phá, tìm kiếm không dấu, lọc, sắp xếp và tải bản văn bản. Dữ liệu giữ trong localStorage của trình duyệt; chưa đồng bộ tài khoản.
- Mồi ba mục Ninh Bình, Hà Nội, Lào Cai kèm ghi chú và trạng thái khi nâng cấp sổ tay trống lần đầu. Giữ nguyên danh sách người dùng đã lưu; cờ mồi riêng ngăn dữ liệu mẫu quay lại sau khi bỏ lưu hết. Ghi chú được giữ khi bỏ lưu để có thể đọc lại khi lưu địa phương lần nữa.
- Bố cục máy tính/điện thoại; modal dùng bàn phím và Escape; các tab dùng phím mũi tên.
- Font, thư viện Pannellum và ảnh panorama phục vụ cùng website; trình xem không gọi AirPano hoặc CDN. Nhạc nền không lời tự tổng hợp được phục vụ local, mặc định 25%, có bật/tắt và chỉnh âm lượng.

## Nội dung đang biên soạn

Nội dung ngắn được đánh dấu là bản mẫu. Tọa độ địa danh là vị trí tham khảo gần đúng, chưa đối chiếu từng điểm với tài liệu chính thức. Không dùng cho đo đạc, địa chính hoặc dẫn đường.

Ảnh AI đã được nối vào thẻ điểm đến, banner trang chi tiết và các địa danh có ảnh tương ứng. Tab **Bộ ảnh AI** hiển thị ảnh tuyển chọn theo Hà Nội, Quảng Ninh và Lào Cai; bấm ảnh để xem lớn, giới thiệu địa danh và nguồn. Bộ ảnh Quảng Ninh/Lào Cai rộng hơn các dấu mốc Hạ Long/Sa Pa trên bản đồ. Ảnh có nhãn minh họa, không phải ảnh tư liệu. Ninh Bình hiện dùng ảnh thực tế có nguồn vì chưa có ảnh AI hoàn tất trong thư mục đầu vào.

Chatbot **RAG sử dụng API BTC** qua backend Python, truy xuất bốn database có nguồn. Cần chạy backend để sử dụng chatbot; trạng thái kết nối hiển thị trong khung trợ lý. Xem [hướng dẫn RAG](rag/README.md).

Trước khi nộp: đối chiếu ranh giới, tọa độ, nội dung và mốc dữ liệu; kiểm tra chi tiết ảnh AI, bổ sung ảnh còn thiếu và chatbot tiếng Việt chỉ trả lời từ kho tri thức đã duyệt, có dẫn nguồn.

## Đồng bộ ảnh mới

Sau khi script tạo ảnh hoàn thành thêm các địa danh, chạy từ thư mục `atlas-viet`:

```sh
python3 scripts/sync_ai_images.py
```

Script đọc `../<địa-phương>-data/images/generation-plan.json`, chỉ lấy WebP đã tồn tại, copy vào `dist/assets/ai/<địa-phương>/` và xuất `dist/assets/ai-images.json` với tên, alt, caption, place_id và nguồn nội dung. Không gọi API hoặc đọc key. Tải lại web sau khi đồng bộ. Toàn bộ tài nguyên cần để triển khai nằm trong `dist/`.

Các ảnh chưa tạo không sinh đường dẫn lỗi. Khi chưa có ảnh AI, banner vẫn dùng ảnh thực tế và giữ trích dẫn tương ứng. Nhãn nguồn nội dung địa danh không phải chứng nhận mọi chi tiết trong ảnh AI đúng thực tế.

## Cấu trúc

- `dist/index.html`: khung trang, modal và khung trợ lý.
- `dist/styles.css`: theme giấy ngà, xanh rừng, vàng đồng; bố cục responsive.
- `dist/app.js`: dữ liệu nội dung ngắn, phép chiếu bản đồ, điều hướng và tương tác.
- `dist/assets/vietnam-provinces.geojson`: dữ liệu ranh giới đã giản lược để hiển thị.
- `dist/assets/credits.json`: tác giả, nguồn, giấy phép và thay đổi đối với ảnh.
- `scripts/prepare_assets.py`: tái tạo tài nguyên từ nguồn công khai đã ghim phiên bản.
- `scripts/check_ui.py`: kiểm tra luồng thực trên Chromium và tạo ảnh QA ở `.qa/`.
- `scripts/check_notebook.py`: kiểm tra dữ liệu mẫu, ghi chú/trạng thái, tìm kiếm/lọc/sắp xếp, xuất văn bản, bỏ lưu, tải lại, chuyển đổi dữ liệu cũ và bố cục máy tính/điện thoại.
- `scripts/sync_ai_images.py`: đồng bộ ảnh đã tạo và xuất danh mục media cho web.
- `scripts/check_tours.py`: kiểm tra 22 cảnh ảnh thực local, hotspot đồng bộ, tải khi bắt đầu, toàn màn hình, thử lại/dừng, dọn viewer, mobile, lỗi ảnh và không có request bên thứ ba. Đặt `ATLAS_TEST_URL` nếu kiểm tra port hoặc deployment khác.

## Tour du lịch online

Tour dùng **Pannellum 2.5.6** (MIT, đóng gói trong `dist/vendor/pannellum/`) để hiển thị cubemap từ `dist/assets/360/`. Thứ tự mặt ảnh: front, right, back, left, up, down. Góc pitch được đổi dấu từ metadata krpano; yaw và FOV giữ theo cảnh nguồn. Desktop dùng ảnh `hi`, màn hình nhỏ dùng `mobile`.

Tên cảnh tiếng Việt, liên kết và ghi công `Courtesy of www.AirPano.com` hiển thị dưới trình xem. Hotspot nối các cảnh dựa trên metadata nguồn và đồng bộ với danh sách. Quảng Ninh hiện chỉ có tour Hạ Long, chưa có Yên Tử/Cô Tô. Nhạc nền `dist/assets/audio/peaceful-tour.mp3` là đoạn ambient 48 giây tự tổng hợp (không dùng sample bên thứ ba), phát lặp khi bắt đầu tour. Có bật/tắt và chỉnh âm lượng; chuyển cảnh hoặc thử lại giữ nhạc liên tục, dừng/rời tab sẽ giải phóng audio. Nếu trình duyệt chặn phát, nút Bật nhạc cho phép thử lại. Tái tạo bằng `scripts/generate_tour_music.py` với numpy và ffmpeg. Ninh Bình có 8 cảnh panorama từ Vietnam.travel (Hang Múa, Tam Cốc, Tràng An, Bái Đính); Lào Cai chưa có dữ liệu panorama.

Bản lưu gốc trong `data/360-tours/` được giữ nguyên, không chạy runtime nguồn. Ảnh và metadata cần cho bản local được sao chép vào `dist/`; không cần iframe hay CDN. User đã yêu cầu tự phục vụ lại ảnh và ghi nguồn; quyền phân phối lại ảnh AirPano vẫn chưa được xác minh độc lập, không mặc định quyền nhúng bao gồm quyền phân phối ảnh. Giấy phép MIT của Pannellum chỉ áp dụng cho thư viện.

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

## Bài viết và chú thích ảnh

Bốn bài địa phương gồm tổng quan, địa lý, lịch sử, văn hóa, ẩm thực và trải nghiệm; mục địa danh có đủ 29 hồ sơ. Nội dung dùng `seed.json` của từng địa phương, nguồn dẫn đặt dưới từng phần. Câu mở bài và phần biên tập nằm trong `scripts/build_articles.py`; dữ liệu web nằm ở `dist/assets/articles.json`.

Tạo lại nội dung và đồng bộ ảnh đã có:

```sh
python3 scripts/build_articles.py
python3 scripts/sync_ai_images.py
```

Web hiện có 29 ảnh AI, gồm 8 ảnh Ninh Bình, 7 Hà Nội, 7 Quảng Ninh và 7 Lào Cai. Caption ghi tên địa danh và “Minh họa do AI tạo; không phải ảnh tư liệu”. Ảnh thật có mô tả và ghi nguồn/tác giả; caption panorama 360° đổi theo cảnh đang chọn. Logo la bàn là hình trang trí của giao diện.

Kiểm tra bài viết, nguồn, ảnh và bố cục bằng `scripts/check_articles.cjs` (cần Playwright; `ATLAS_BASE_URL` mặc định `http://127.0.0.1:4321/`).

### Panorama Ninh Bình

Nguồn ảnh: Vietnam.travel — Ninh Binh in 360. Chỉ tải và kiểm tra JPEG panorama; không chạy runtime hoặc iframe nguồn. Tái tạo bằng `scripts/prepare_ninh_binh_tour.py` (Pillow). Ảnh gốc lưu riêng trong `data/360-tours/ninh-binh/media/`; bản public được thu nhỏ còn 4096×2048 cho desktop và 2048×1024 cho mobile để giảm bộ nhớ WebGL. Metadata gồm liên kết giữa 8 cảnh; tên cảnh được chuyển sang tiếng Việt. Trình xem hỗ trợ cả cubemap và equirectangular. Quyền phân phối ảnh nguồn chưa được xác minh độc lập; user đã yêu cầu tự phục vụ lại và ghi nguồn.

Popup từ bản đồ hiển thị ranh giới hành chính bên trái và tổng quan có ảnh AI, caption, nguồn dẫn bên phải. “Tìm hiểu chi tiết” mở Địa danh. Tab Địa lý – Tổng quan đã bỏ; URL cũ với `tab=tong-quan` mở Địa danh. Dữ liệu bản đồ hiện là ranh giới hành chính tham khảo, không có lớp thửa đất địa chính.
