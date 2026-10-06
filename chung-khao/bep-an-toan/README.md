# Bếp An Toàn — Giải cứu hội chợ trường

Game hành động 2D tiếng Việt cho học sinh cấp 2. Chơi đơn trong trình duyệt, không tài khoản, không backend, không khóa API, không thư viện runtime. Tranh mở đầu và bộ sprite nhân vật, trạm bếp, thực phẩm tạo bằng ImageGen. Canvas hiển thị sprite, ghép map và vẽ hiệu ứng/trạng thái.

## Chạy ngay

Cần Node.js có hỗ trợ ES modules và `node:test` (khuyến nghị Node.js 22 trở lên).

```sh
cd chung-khao/bep-an-toan
npm run dev
```

Mở http://127.0.0.1:5173. Không cần `npm install` vì không có dependency. `PORT=8080 npm run dev` để đổi cổng. Không mở trực tiếp `index.html` bằng file:// vì game dùng module JavaScript.

## Điều khiển

- WASD / phím mũi tên: di chuyển.
- E hoặc Space: thao tác tại trạm gần nhất.
- H: nhờ Nam vệ sinh dụng cụ; hồi chiêu 25 giây.
- Escape: tạm dừng. Game tự tạm dừng khi mất focus hoặc chuyển tab.
- Chuột / cảm ứng: bấm vào trạm để tìm đường, rồi bấm nút tương tác. Thiết bị cảm ứng có thêm các nút hướng.

## Game có gì?

Ba chương hoàn chỉnh, 2:30–3:30 phút mỗi ca, mở khóa theo kết quả:

1. **Gian hàng đầu tiên:** gà nướng, rửa tay, nhiệt kế.
2. **Bữa trưa rộn ràng:** thêm salad, bàn riêng, sự cố nguồn nước.
3. **Giải cứu hội chợ:** thêm trái cây, biến thể bố trí, tủ lạnh mất điện.

Đơn hàng và thời điểm sự cố thay đổi theo seed. Sau màn có thể chơi lượt mới hoặc lặp cùng seed. Chế độ thư giãn tăng thời gian chờ khách. Tiến độ và số sao lưu tại localStorage trên trình duyệt hiện tại (không đồng bộ thiết bị).

Mỗi món giữ trạng thái sơ chế, nhiễm chéo, xác nhận nhiệt độ và thời gian bảo quản mô phỏng. Món không an toàn bị giữ ở quầy; người chơi giảm uy tín và nhận giải thích. Các trạm có va chạm; điều hướng bằng chuột dùng tìm đường qua ô lưới. Có âm thanh tổng hợp, bật/tắt tùy chọn.

Công thức:

- Gà: tủ gà → bàn sống → đặt lên bếp → rửa tay → đo nhiệt độ đạt 74°C → lấy món → quầy.
- Salad / trái cây: kho → rửa bằng nước an toàn → bàn rau sạch → quầy.
- Dụng cụ: tay trống + bàn → vệ sinh; hoặc H nhờ Nam. Không rửa gà sống.
- Sự cố nước: kích hoạt trạm nước dự phòng. Sự cố điện: khôi phục cầu dao, kiểm tra tủ và thay lô bị ảnh hưởng.

Đạt mục tiêu và còn uy tín để qua chương. 2 sao khi tối đa 1 lỗi, 3 sao khi không lỗi và phục vụ vượt mục tiêu ít nhất 2 món.

## Nội dung giáo dục

Dựa trên [WHO Five Keys to Safer Food](https://www.who.int/publications/i/item/9789241594639) và [CDC Food Safety](https://www.cdc.gov/food-safety/prevention/index.html). Sổ tay trong game dẫn nguồn và giải thích các mốc ngoài đời.

Thời gian game được tăng tốc: rửa tay 2 giây, nấu 10 giây, thanh bảo quản 50 giây và sự cố tủ lạnh 25 giây **không phải hướng dẫn ngoài đời**. Ngoài đời rửa tay ít nhất 20 giây; gà cần nhiệt độ bên trong ít nhất khoảng 74°C; bảo quản lạnh khoảng 4°C hoặc thấp hơn; tham khảo nguồn cho giới hạn thời gian, nhiệt độ và từng loại thực phẩm. Mô phỏng nhiễm chéo được đơn giản hóa và ưu tiên phòng ngừa. Game không mô phỏng chẩn đoán bệnh.

## Kiểm tra và build

```sh
npm test
npm run build
```

Build tạo `dist/` chứa chỉ tài nguyên công khai của game. Test kiểm tra luật nhiễm chéo, đo nhiệt độ, bảo quản, công thức, kết quả, mở khóa, tạm dừng, khôi phục sự cố và đường đi ở các bố cục.

## Deploy lên Vercel

Đã có `vercel.json`. Khi import repository trong Vercel:

- **Root Directory:** `chung-khao/bep-an-toan`
- **Framework Preset:** Other
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Environment Variables:** không cần

Nếu đưa riêng thư mục game sang repository mới, Root Directory để mặc định. Chỉ cần publish nội dung game, không đưa `.env` hoặc các thư mục khác của repository vào bản triển khai.

Sau deploy, kiểm tra trang chủ, mở chương 1, lấy gà, phục vụ một món và reload để kiểm tra tiến độ. Tài liệu: [Vercel Git deployments](https://vercel.com/docs/git), [Project Configuration](https://vercel.com/docs/project-configuration).

## Cấu trúc

- `index.html`: giao diện, điều khiển và dialog.
- `style.css`: thiết kế responsive; font Google Fonts có fallback system nếu offline.
- `game.js`: vòng lặp, input, vẽ, va chạm, tìm đường, âm thanh, UI và chiến dịch.
- `rules.js`: luật thực phẩm, màn chơi và bộ random theo seed.
- `assets/cover.png`: tranh hội chợ AI.
- `tests/`: kiểm tra logic và luồng gameplay bằng Node.js.
- `server.mjs` / `build.mjs`: server local và đóng gói website tĩnh.

Bản này là một game nhỏ hoàn chỉnh với ba chương, không có multiplayer, dashboard giáo viên hoặc nội dung do AI sinh trực tiếp khi chơi.

## Bộ hình ảnh v2

Dùng `create-game-assets` và `imagegen`: 16 pose nhân vật (Linh/Nam × 4 hướng × đứng/đi), 12 prop và 6 icon thực phẩm. Sprite atlas nhân vật có 2 pose mỗi hướng kết hợp nhún theo thời gian; cầm món và thao tác dùng overlay/hiệu ứng trong code, không phải bộ animation từng hành động đầy đủ.

`assets/sprites/` là ảnh chuẩn hóa dùng trong game. `art/source/` giữ nguyên ảnh sinh và thông tin nguồn. `art/art-direction.md` ghi phong cách/kích thước; `art/asset-manifest.json` ghi nguồn và kiểm tra; `art/previews/` chứa bảng xem. `art/normalize_assets.py` cắt/căn/đổi kích thước bằng Pillow. Không cần chạy các script này khi chơi hoặc deploy.

Nếu ảnh tải lỗi, renderer dùng hình Canvas dự phòng. Toàn bộ vị trí trạm và luật va chạm được giữ nguyên.
