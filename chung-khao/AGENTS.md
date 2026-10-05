# AGENTS.md — chung-khao/

Hướng dẫn cho AI coding agent (Claude Code, Codex, Cursor, Gemini, Antigravity...) khi làm việc trong thư mục vòng chung khảo của đội AIvenger (`AITC-481`).

## Quy tắc chung của repo

- Mọi code của vòng này nằm dưới `chung-khao/`. **Không sửa / xoá** cấu trúc thư mục do BTC tạo, không sửa `README.md` ở root.
- **Không commit secret:** API key, `.env`, token. `.env` và `.venv/` đã có trong `.gitignore`. Key đọc từ biến môi trường.
- **AI log là tự động** (xem `.agents/rules/ai-log-hook.md`):
  - KHÔNG chạy `scripts/log_antigravity.py` hay `scripts/log_manual.py` sau mỗi task.
  - KHÔNG sửa / xoá file trong `.ai-log/`.
  - Nếu pre-push hook lỗi: báo user, KHÔNG bypass bằng `--no-verify`.
- Hỏi user trước khi commit, push hay tạo nhánh.

## UI_testing/ — AITC Playground (Gradio)

Một file app: `UI_testing/demo.py`. Dependency quản lý bằng uv (`pyproject.toml`, `uv.lock`). Yêu cầu Gradio >= 6.

```bash
cd chung-khao/UI_testing
uv run demo.py                                          # chạy app
GRADIO_SERVER_PORT=7899 uv run demo.py                  # port khác, tránh đụng app user đang chạy ở 7860
uv run python -c "import demo"                          # kiểm tra build UI
AITC_BASE_URL=http://127.0.0.1:8765 uv run python ...   # trỏ sang server giả để test request
```

Khi kiểm tra, **đừng kill process trên port 7860**: thường là app user đang mở. Dùng port khác.

### Cấu trúc demo.py

- **Specs ở đầu file:** `IMAGE_SPECS` (kind google/openai, sizes, max_refs), `VIDEO_MODELS`, `VIDEO_SIZE`, `TTS_MODELS`, voice lists, `STT_MODELS`. Thêm model mới thì sửa ở đây trước.
- **Helper:**
  - `_call()` gọi HTTP và raise `gr.Error` kèm body khi lỗi.
  - `_parse_extra()` đọc ô raw JSON.
  - `_debug()` dựng nội dung panel Request / Response, rút gọn base64 bằng `_redact()`.
  - `_form()` encode field cho multipart.
- **Mỗi tab có 3 phần:** hàm xử lý (`gen_image`, `gen_video` là generator để stream status khi poll, `gen_tts`, `run_stt`), hàm `on_*_model` ẩn/hiện option theo model, và khối UI trong `with gr.Blocks()`.
- **Output chuẩn của mỗi hàm xử lý:** `(kết quả, status markdown, debug json)`.

### Quy ước gateway

- Base URL `https://api.thucchien.ai`. Theo docs BTC:
  - Image và audio dùng path không có `/v1`: `/images/generations`, `/audio/speech`, `/audio/transcriptions`.
  - Video và chat dùng path có `/v1`: `/v1/videos`, `/v1/chat/completions`.
- Auth bằng `Authorization: Bearer <key>`.
- **Quy tắc auto:** chỉ field có trong docs BTC mới được gửi mặc định.
  - Option ngoài docs có label *not in BTC docs* và mặc định `AUTO` / rỗng.
  - Dùng `_put(body, key, value)` để bỏ qua giá trị `AUTO`, rỗng hoặc `None`.
  - Thêm option mới cũng làm theo quy tắc này.
  - Sau khi sửa, kiểm tra request mặc định của từng tab vẫn khớp ví dụ trong docs BTC, bằng server giả và panel debug.
- Gateway là LiteLLM. Tham số ngoài docs BTC được gửi theo format của model gốc. Phần này **chưa kiểm chứng**, và docs BTC ghi gateway có thể tự bỏ tham số không hỗ trợ mà không báo lỗi. Vì vậy:
  - Giữ ô raw JSON và panel Request / Response ở mọi tab.
  - Không nuốt lỗi. Hiện nguyên văn response lỗi cho user.
  - Ghi rõ "chưa kiểm chứng" khi báo cáo cho user về các tham số này.
- Ảnh tham chiếu:
  - Nano Banana: `/v1/chat/completions` với các part `image_url` (data URI) và `image_config`.
  - gpt-image: `/images/edits` multipart, field `image[]`.
  - Veo: first frame qua `input_reference` (multipart, đúng như docs). `lastFrame` và `referenceImages` dùng format Veo `{"bytesBase64Encoded", "mimeType"}`.

### Lưu ý Gradio 6 (đã gặp thực tế)

- `css=` và `theme=` truyền vào `launch()`, không truyền vào `gr.Blocks()`.
- `gr.Textbox(show_copy_button=...)` không còn. Dùng `buttons=["copy"]`.
- `elem_classes` trên `gr.Column` không xuất hiện trong DOM của app này. Panel card dùng `elem_id="panel-N"` và CSS `[id^="panel-"]`.
- Ô ảnh tham chiếu dùng `gr.Gallery(interactive=True)` có sẵn:
  - Upload thêm sẽ cộng dồn, có nút X trên từng ảnh, bấm vào ảnh thì phóng to.
  - Value là list `(path, caption)`. Dùng `_paths()` để lấy đường dẫn.
  - Thumbnail nhỏ được style bằng CSS `.ref-thumbs`.
- Đổi layout hay CSS xong thì kiểm tra bằng screenshot (Playwright headless), không đoán DOM:
  `uv run --with playwright python <script>` (chromium đã cài ở `~/Library/Caches/ms-playwright`).
