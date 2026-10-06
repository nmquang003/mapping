# Tạo ảnh địa danh song song qua API Ban tổ chức

Script: `generate_regional_images.py`. Đã chuẩn bị **22 prompt**: Quảng Ninh 7, Hà Nội 8, Lào Cai 7. Mỗi ảnh gắn với `place_id` của database địa phương.

## Chạy

Chạy từ thư mục gốc repository:

```bash
chung-khao/UI_testing/.venv/bin/python chung-khao/generate_regional_images.py --workers 3
```

Hoặc dùng đường dẫn tuyệt đối, không phụ thuộc thư mục terminal:

```bash
/Users/vuongminh/Documents/AI/AI_THUC_CHIEN/aitc2026-team-481-aivenger/chung-khao/UI_testing/.venv/bin/python /Users/vuongminh/Documents/AI/AI_THUC_CHIEN/aitc2026-team-481-aivenger/chung-khao/generate_regional_images.py --workers 3
```

Script sử dụng `requests` và Pillow đã có trong `.venv`. Không cần OpenAI SDK hoặc python-dotenv. Script chỉ đọc `GATEWAY_KEY` trong `.env` ở gốc repository, không thực thi nội dung `.env`, không ghi key vào prompt, ảnh hoặc manifest. Endpoint cố định: `https://api.thucchien.ai/images/generations`.

Model `gpt-image-2.5-sunburst`, chất lượng `high`, kích thước yêu cầu `1536x1024`. Chạy tối đa 3 yêu cầu đồng thời. Thứ tự xen kẽ ba địa phương để yêu cầu đầu tiên của mỗi địa phương được chạy song song.

Tạo lại prompt mà không gọi API:

```bash
chung-khao/UI_testing/.venv/bin/python chung-khao/generate_regional_images.py --prepare-only
```

## Chạy riêng Ninh Bình

```bash
chung-khao/UI_testing/.venv/bin/python chung-khao/generate_regional_images.py --regions ninh-binh --workers 3
```

Lệnh này chỉ chạy 8 ảnh Ninh Bình: Tràng An, Tam Cốc, Bích Động, Hoa Lư, Cúc Phương, Bái Đính, Phát Diệm, Hang Múa. Sử dụng prompt và ảnh tham chiếu sẵn có, gửi multipart tới `/images/edits` để giữ đặc trưng địa danh. Tự đọc `GATEWAY_KEY` từ `.env` gốc dự án. Không tạo lại ảnh của ba địa phương khác.

Sau khi tạo xong, đưa ảnh lên web và tải lại trang:

```bash
python3 chung-khao/atlas-viet/scripts/sync_ai_images.py
```

Ảnh Ninh Bình được lưu tại `chung-khao/ninh-binh-data/images/output/imagegen/` (PNG gốc) và `chung-khao/ninh-binh-data/images/generated/` (WebP).

## Nơi lưu các bộ ảnh

- [Quảng Ninh: prompt và mô tả ảnh](quang-ninh-data/images/README.md).
- [Hà Nội: prompt và mô tả ảnh](ha-noi-data/images/README.md).
- [Lào Cai: prompt và mô tả ảnh](lao-cai-data/images/README.md).

Trong mỗi thư mục `images/`:

- `prompts/<place_id>.txt`: prompt đầy đủ.
- `generation-plan.json`: kế hoạch, model và danh sách địa danh.
- `output/imagegen/<place_id>.png`: ảnh gốc sau khi API trả kết quả.
- `generated/<place_id>.webp`: bản 16:9, 1536×864, dùng cho web.
- `manifest.json`: trạng thái kết quả, tên, alt, caption, place_id và nguồn nội dung.
- `contact-sheet.jpg`: bảng xem nhanh khi đã có ảnh.

## Xử lý lỗi và chạy tiếp

Ảnh gốc đã tồn tại và mở được sẽ được dùng lại, không gọi API tạo lại. Script không tự thử lại yêu cầu POST đã lỗi; timeout có thể xảy ra sau khi API đã nhận yêu cầu. Lỗi kết nối, quyền truy cập, giới hạn tốc độ hoặc budget sẽ dừng gửi các ảnh tiếp theo. Trước khi chủ động chạy lại sau timeout, cần kiểm tra trạng thái/budget tại gateway để tránh tạo trùng.

## Nhãn và kiểm tra ảnh

Gắn caption: **“Minh họa do AI tạo; không phải ảnh tư liệu.”** Các ảnh được tạo từ prompt, không dùng ảnh tham chiếu. `source_ids` chỉ dẫn nguồn nội dung địa danh, không chứng minh mọi chi tiết trong hình được AI tạo.

Mọi ảnh mặc định có `visual_status: pending_visual_review`. Cần kiểm tra nhận diện công trình, tỷ lệ, mái, hình dáng núi, con người và phần crop trước khi xuất bản. Các chi tiết mùa lúa, ánh sáng và mây là lựa chọn minh họa, không phải thông tin thời tiết hoặc mùa vụ hiện tại.

## Trạng thái lần chạy trong Codex

Đã chạy script bằng `.venv` được chỉ định. Ba yêu cầu đầu tiên lỗi kết nối trong sandbox; kết quả **0/22 ảnh**. Bước xin quyền mạng ngoài sandbox không được thực thi vì hệ thống xét duyệt tự động lỗi `403`, model `codex-auto-review` không khả dụng. Đây là lỗi hệ thống xét duyệt, chưa phải kết luận API sinh ảnh hoặc `GATEWAY_KEY` không hợp lệ. Chưa kiểm tra được chi phí hoặc trạng thái model sinh ảnh trên gateway.
