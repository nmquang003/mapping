# AI Thực Chiến — Generative Studio

Giao diện Gradio local gọi gateway BTC, làm việc theo project và lưu output bền vững. Không cần chỉnh curl hoặc Python để sử dụng.

## Chạy trên macOS / Linux

Tại thư mục gốc repo:

```bash
bash chung-khao/generative-studio/run.sh --open
```

Lần đầu script tạo môi trường Python tại `local/studio-venv/` và cài dependencies. Cần Python 3.12 trở lên (đã kiểm tra trên Python 3.13). Giao diện: http://127.0.0.1:7860. Nếu cổng bận: `--port 7861`. Dừng bằng Ctrl+C trong terminal chạy server.

Cài thủ công / Windows:

```bash
python -m venv local/studio-venv
# Windows: local\studio-venv\Scripts\python.exe thay cho đường dẫn Python bên dưới
local/studio-venv/bin/python -m pip install -r chung-khao/generative-studio/requirements.txt
local/studio-venv/bin/python chung-khao/generative-studio/app.py
```

## Kết nối

Mở **Kết nối API & nơi lưu dữ liệu**, nhập key gọi model do BTC cấp. Key dùng trong phiên không được ghi vào project hay localStorage. Hoặc tạo `.env` riêng cho app từ `.env.example` rồi tự điền `STUDIO_API_KEY`. App đọc cả `.env` ở gốc repo và `.env` trong thư mục app (ưu tiên file app). Không dùng `AI_LOG_API_KEY`: đó là token hệ thống logging, không phải key gọi model.

**Kiểm tra kết nối** gọi `GET /models`, không tạo nội dung. Danh sách chọn model phản ánh tài liệu BTC đã tải; endpoint /models xác minh kết nối, không tự thay đổi catalog. Khả năng/quyền thực tế phụ thuộc key. Không commit `.env`.

## Làm việc

1. Tạo hoặc chọn project.
2. Chọn tab, model, input và tham số, nhấn tạo.
3. Xem output ở cột phải; kết quả được lưu tự động vào lịch sử.
4. Chọn lần tạo trong thư viện để xem lại. Có thể đổi tên, thêm tags, đánh dấu ★, tải file hoặc ZIP.
5. **Dùng lại prompt & tham số** phục hồi form; lần tạo tiếp theo liên kết với bản gốc. Đổi project sẽ xóa liên kết này.
6. Chuyển văn bản sang giọng nói/prompt ảnh, hoặc ảnh sang video/chỉnh sửa local bằng các nút cạnh output.

### Các tác vụ

- **Ảnh:** Nano Banana chuẩn hoặc chat; OpenAI size/quality. Một request chuẩn tạo một ảnh. Không dùng alias Nano Banana đã ngừng hỗ trợ. Tạo lại là thao tác chủ động của người dùng. Chế độ chat không gửi tham số tỷ lệ khung hình.
- **Văn bản:** nội dung trước đó, system prompt, token budget, reasoning OpenAI và thinking DeepSeek. Tìm kiếm web đi qua `/responses` cho OpenAI và `googleSearch` cho Gemini. Nguồn và Search Suggestions được hiển thị. Output văn bản có thể sửa rồi lưu thành phiên bản mới.
- **Video:** text-to-video hoặc ảnh khởi đầu; thời lượng 4/6/8 giây, 720p/1080p tùy model. Lưu video_id ngay khi API trả về; tự poll mỗi 10 giây trong khi mở trang có key, hoặc kiểm tra thủ công. Sau khi restart, mở lại project và nhập key để tiếp tục kiểm tra/tải. Có thể nhập video_id đã biết để khôi phục. Tắt theo dõi không hủy video hoặc hoàn tiền. Chi phí ước tính dựa trên tài liệu, không phải số dư budget.
- **Giọng nói:** chọn giọng theo Gemini/OpenAI, nghe và tải audio.
- **Phiên âm:** upload hoặc microphone; lưu transcript và sửa trực tiếp. Microphone cần quyền trình duyệt.
- **Embedding:** mỗi dòng một đoạn, xuất JSON và bảng cosine similarity. Gemini Embedding 2 gọi riêng từng dòng; giữ kết quả từng bước nếu bị lỗi giữa chừng.
- **Kiểm duyệt:** kết quả JSON của `omni-moderation-latest`.
- **Sửa ảnh local:** crop/resize bằng trình editor, lưu bản mới. Không gọi API chỉnh sửa ảnh/inpainting chưa được BTC xác nhận.

## Dữ liệu

Mặc định `local/generative-studio/` (repo đã ignore `/local`). Có thể thay bằng biến `STUDIO_DATA_DIR` trỏ đến đường dẫn tuyệt đối.

```text
studio.sqlite                 # project, lịch sử, tags, trạng thái
projects/<project-id>/
  inputs/
  runs/<timestamp-kind-id>/
    request.json              # tham số, không chứa Authorization
    metadata.json             # nguồn, parent, trạng thái, cost nếu API báo
    response.json             # response/usage; ảnh base64 lớn không lưu lặp
    input.*                   # bản sao file đầu vào, nếu có
    output.*                  # PNG / MP4 / MP3 / WAV / TXT / JSON
  exports/*.zip
cache/                        # cache hiển thị Gradio
```

Output không bị ghi đè. SQLite và file thật giữ lịch sử sau khi đóng trình duyệt. ZIP chứa các run, prompt/tham số, metadata và file output/input; không chứa API key hoặc database. Sao lưu toàn bộ thư mục dữ liệu khi app đã dừng. App dành cho làm việc local; không có phân quyền người dùng hay đăng nhập cho triển khai nhiều người.

## Lỗi và chi phí

App giới hạn tối đa 3 request mạng cùng lúc trong process, hàng đợi tối đa 32; không đảm bảo quota toàn đội khi có công cụ khác gọi gateway. Lỗi 429 phân biệt hết budget và rate limit. Không tự retry POST: timeout có thể xảy ra sau khi BTC đã nhận tác vụ. Run đang chạy khi ứng dụng dừng được đánh dấu `uncertain` khi khởi động lại. Run `uncertain` cần kiểm tra trước khi chủ động tạo lại. Video có ID vẫn retry được GET/tải mà không tạo video mới. Chi phí chỉ cộng các header `x-litellm-response-cost` có nhận được; thiếu header được ghi là chưa biết, không coi là miễn phí. Key chỉ gửi tới HTTPS `api.thucchien.ai`.

## Kiểm tra

```bash
local/studio-venv/bin/python -m pip install pytest
cd chung-khao/generative-studio
../../local/studio-venv/bin/python -m pytest -q
```

Tests dùng HTTP mock; không gọi model thật hoặc tiêu budget. Bao phủ payload riêng theo model, ảnh base64, multipart, video resume, timeout không retry, storage/export, phiên bản local và xây dựng UI. Cần thử bằng key BTC để xác nhận tương thích gateway thực tế; chưa có lần tạo sinh thật trong quá trình phát triển.

Nguồn cấu hình: `../docs/thucchien-user-guide/` và `../docs/thucchien-api-reference/image-generation.md`. Catalog chỉnh tại `studio/models.json`. Hướng dẫn Gradio: https://www.gradio.app/docs/gradio/blocks và https://www.gradio.app/guides/file-access.
