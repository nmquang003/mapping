# Ảnh minh họa Ninh Bình

## Trạng thái

Đã chuẩn bị 8 ảnh thật từ Wikimedia Commons làm tham chiếu, kiểm tra trực quan và lưu 8 prompt riêng. **Chưa tạo ảnh AI, chưa gửi yêu cầu tính phí đến GPT Image.**

Ngày chuẩn bị: 06/10/2026. Bước chuẩn bị OpenAI SDK bị chặn vì cơ chế duyệt quyền tự động trả 403: model `codex-auto-review` không khả dụng. Đây là lỗi của cơ chế duyệt quyền, chưa phải phản hồi từ model tạo ảnh.

## Tệp

- `references.json`: nguồn ảnh tham chiếu, tác giả, giấy phép, URL và kết quả kiểm tra.
- `references/*.jpg`: 8 ảnh tham chiếu; không phải ảnh AI đầu ra.
- `references/contact-sheet.jpg`: bản xem nhanh 8 ảnh tham chiếu.
- `prompts/*.txt`: 8 prompt đầy đủ, mỗi ảnh một địa điểm.
- `generation-plan.json`: cấu hình và ánh xạ mã địa điểm cho web/chatbot.
- `output/imagegen/*.png`: đường dẫn dự kiến cho ảnh gốc do API tạo, hiện chưa có.
- `generated/*.webp`: đường dẫn dự kiến cho ảnh web 16:9 đã kiểm tra, hiện chưa có.

## Cấu hình đã chọn

- CLI dự phòng của skill imagegen; không dùng công cụ image_gen tích hợp vì phiên này không có công cụ đó.
- API: `https://api.thucchien.ai`.
- Model: `gpt-image-2.5-sunburst`, thuộc dòng GPT Image người dùng đã chọn. Chưa kiểm chứng khả năng truy cập model bằng key hiện tại.
- Chất lượng: `high`; mỗi ảnh kèm một ảnh tham chiếu, dùng lệnh `edit` của CLI để gửi ảnh đầu vào.
- Dự kiến chạy 8 lệnh CLI độc lập song song. `generate-batch` không có trường ảnh tham chiếu nên không dùng cho bộ này.
- Kích thước tài liệu gateway có hỗ trợ: `1536x1024`. Dự kiến cắt thành `1536x864` (16:9), giữ toàn bộ chủ thể chính, không phóng lớn để giả độ phân giải. Cần kiểm tra từng ảnh sau khi cắt.
- Key đọc từ biến `GATEWAY_KEY` trong `.env` ở thư mục gốc. Khi chạy CLI, chỉ ánh xạ biến này thành `OPENAI_API_KEY` trong bộ nhớ tiến trình và đặt `OPENAI_BASE_URL` về gateway; không ghi key vào nội dung ảnh, manifest hoặc câu lệnh có giá trị key.

## Khi xuất bản

Gắn nhãn bên ngoài ảnh: **Ảnh minh họa tạo bằng AI**. Giữ thông tin nguồn và giấy phép ảnh tham chiếu bên cạnh ảnh phát sinh nếu áp dụng; các ảnh CC BY/CC BY-SA có điều kiện ghi công và điều kiện giấy phép riêng. Ảnh Tràng An không được dùng thay Tam Cốc; Cố đô Hoa Lư không phải Phố cổ Hoa Lư. Cảnh lúa chín Tam Cốc là lựa chọn minh họa theo mùa, không thể hiện điều kiện hiện tại.

Ảnh AI dù có tham chiếu vẫn cần kiểm tra kiến trúc và địa hình trước khi quảng bá như một địa điểm cụ thể.
