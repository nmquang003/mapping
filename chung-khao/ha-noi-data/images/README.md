# Ảnh minh họa Hà Nội

Tạo qua API Ban tổ chức; model `gpt-image-2.5-sunburst`. Không lưu key trong thư mục này.

Ảnh không có tham chiếu tư liệu, cần kiểm tra trước khi xuất bản. Gắn caption “Minh họa do AI tạo; không phải ảnh tư liệu”.

## Tệp

- `prompts/`: prompt đầy đủ từng địa danh.
- `output/imagegen/`: ảnh gốc PNG.
- `generated/`: bản WebP 1536×864 dùng cho web.
- `manifest.json`: kết quả sinh ảnh, đường dẫn, alt và liên kết place_id.
- `contact-sheet.jpg`: bảng xem nhanh ảnh đã tạo.

## Prompt

### Hồ Hoàn Kiếm

[ho-hoan-kiem.txt](prompts/ho-hoan-kiem.txt)

Nguồn nội dung: S04, S05 trong database địa phương. Chi tiết hình ảnh là minh họa, chưa xác minh từng cấu kiện kiến trúc.

### Phố cổ Hà Nội

[pho-co-ha-noi.txt](prompts/pho-co-ha-noi.txt)

Nguồn nội dung: S03, S04 trong database địa phương. Chi tiết hình ảnh là minh họa, chưa xác minh từng cấu kiện kiến trúc.

### Văn Miếu – Quốc Tử Giám

[van-mieu-quoc-tu-giam.txt](prompts/van-mieu-quoc-tu-giam.txt)

Nguồn nội dung: S03 trong database địa phương. Chi tiết hình ảnh là minh họa, chưa xác minh từng cấu kiện kiến trúc.

### Hoàng thành Thăng Long

[hoang-thanh-thang-long.txt](prompts/hoang-thanh-thang-long.txt)

Nguồn nội dung: S03, S06, S07 trong database địa phương. Chi tiết hình ảnh là minh họa, chưa xác minh từng cấu kiện kiến trúc.

### Lăng Chủ tịch Hồ Chí Minh

[lang-chu-tich-ho-chi-minh.txt](prompts/lang-chu-tich-ho-chi-minh.txt)

Nguồn nội dung: S03, S05 trong database địa phương. Chi tiết hình ảnh là minh họa, chưa xác minh từng cấu kiện kiến trúc.

### Nhà hát Lớn Hà Nội

[nha-hat-lon-ha-noi.txt](prompts/nha-hat-lon-ha-noi.txt)

Nguồn nội dung: S04, S05 trong database địa phương. Chi tiết hình ảnh là minh họa, chưa xác minh từng cấu kiện kiến trúc.

### Bảo tàng Dân tộc học Việt Nam

[bao-tang-dan-toc-hoc.txt](prompts/bao-tang-dan-toc-hoc.txt)

Nguồn nội dung: S05 trong database địa phương. Chi tiết hình ảnh là minh họa, chưa xác minh từng cấu kiện kiến trúc.

### Nhà thờ Lớn Hà Nội

[nha-tho-lon-ha-noi.txt](prompts/nha-tho-lon-ha-noi.txt)

Nguồn nội dung: S04, S05 trong database địa phương. Chi tiết hình ảnh là minh họa, chưa xác minh từng cấu kiện kiến trúc.
