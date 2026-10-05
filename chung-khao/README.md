# Vòng chung khảo

Thư mục nộp bài / làm việc cho đội **AIvenger** (`AITC-481`).

## Hướng dẫn

- Đặt toàn bộ source, tài liệu, demo liên quan **Vòng chung khảo** trong thư mục `chung-khao/` này.
- Có thể tạo nhánh riêng theo quy ước đội, nhưng **nội dung vòng này** phải nằm dưới `chung-khao/`.
- Không đẩy secret (API key, `.env`, password) lên repo.

```
chung-khao/
├── README.md          ← file này
├── AGENTS.md          ← hướng dẫn cho AI agent (Claude Code, Codex, Cursor...)
└── UI_testing/        ← Gradio playground gọi API của BTC
    ├── demo.py
    ├── pyproject.toml
    └── uv.lock
```

## UI_testing — AITC Playground

App Gradio để thử nhanh các model chung của BTC qua gateway `https://api.thucchien.ai`. Giao diện kiểu fal.ai: option bên trái, kết quả bên phải.

| Tab | Endpoint | Model |
|---|---|---|
| Image | `/images/generations`, `/v1/chat/completions` (khi có ảnh ref, Nano Banana), `/images/edits` (khi có ảnh ref, gpt-image) | `nano-banana-2`, `nano-banana-2-lite`, `nano-banana-pro`, `nano-banana`, `gpt-image-2.5-flare`, `gpt-image-2.5-sunburst` |
| Video | `/v1/videos` (tạo → poll → tải về) | `veo-3.1-lite/fast/generate-001` |
| Text to Speech | `/audio/speech` | `gemini-*-tts`, `gpt-4o-mini-tts` |
| Speech to Text | `/audio/transcriptions` | `gemini-3.5-transcribe-preview`, `gpt-4o(-mini)-transcribe`, `gpt-transcribe`, `whisper-1` |

Tab thứ 5, **API snippets**, không gọi API: chọn model (17 model) và vài option theo docs là ra code **cURL**, **Python requests** và **OpenAI SDK** để copy, kèm ghi chú (định dạng response, giới hạn, cảnh báo). Code lấy theo các ví dụ trong docs BTC (cùng URL, cùng `base_url` cho từng ví dụ SDK), chỉ chứa field có trong docs, key luôn là `<your_api_key>`.

### Chạy

Cần [uv](https://docs.astral.sh/uv/).

```bash
cd chung-khao/UI_testing
export AITC_API_KEY="<key BTC cấp>"
uv run demo.py            # mở http://127.0.0.1:7860
```

Nếu không set biến môi trường, có thể dán key vào ô **API key** trên giao diện.

| Biến môi trường | Mặc định | Ý nghĩa |
|---|---|---|
| `AITC_API_KEY` | (trống) | API key của BTC |
| `AITC_BASE_URL` | `https://api.thucchien.ai` | Base URL của gateway |
| `GRADIO_SERVER_PORT` | `7860` | Port của app |

### Tính năng

- **Ảnh tham chiếu nhiều ảnh:** kéo thả hoặc upload nhiều ảnh, upload thêm sẽ cộng dồn, bấm vào ảnh để xem lớn, bấm X để xoá. Giới hạn: Nano Banana 14 ảnh (`nano-banana` 3), gpt-image 16, Veo 3.
- **Option theo model gốc:** aspect ratio và resolution (512/1K/2K/4K) cho Nano Banana; size/quality/background/format cho gpt-image; negative prompt, resolution 720p/1080p/4k, bật/tắt audio, seed, first/last frame cho Veo; voice, style, speed, format cho TTS; language, prompt, response format, timestamp cho STT.
- **Ô "Advanced: raw parameters (JSON)":** merge thẳng vào request body, dùng để gửi field mà UI chưa có.
- **Panel "Request / Response":** xem request đã gửi và response gateway trả về (base64 được rút gọn).
- **Ước tính chi phí video** theo bảng giá trong docs BTC.

### Lưu ý

- **Mặc định chỉ gửi field có trong docs BTC.** Mỗi option không có trong docs được đánh dấu *not in BTC docs* trên UI. Giá trị mặc định của chúng là `auto` (hoặc để trống, `1.0` với speed, `0` với temperature), nghĩa là **không gửi** field đó. Ở mặc định, request khớp đúng ví dụ trong docs BTC.
- Các tham số ngoài docs BTC (ảnh ref cho ảnh, `image_size`, `background`, `output_format`, `generateAudio`, `negativePrompt`, `seed`, `lastFrame`, `referenceImages`, `instructions`, `speed`, `language`...) gửi theo format của model gốc và **chưa được kiểm chứng với gateway**. Docs BTC ghi gateway có thể **tự bỏ tham số không hỗ trợ mà không báo lỗi**, nên request trả 200 chưa chắc tham số đã có tác dụng. Hãy kiểm tra kết quả.
- `gpt-transcribe` luôn gửi `response_format=json`, vì docs BTC bắt buộc.
- Veo bắt buộc 8 giây khi dùng 1080p, 4k, ảnh ref hoặc last frame. App tự đặt 8 giây và ghi chú trong status.
- Gateway chỉ trả 1 ảnh mỗi request (`n=1`). "Number of images" gửi nhiều request song song.

Tài liệu BTC: [Giới thiệu](https://docs.thucchien.ai/docs/round-2/user-guide/introduction) · [Image](https://docs.thucchien.ai/docs/round-2/user-guide/image-generation) · [Video (Veo 3)](https://docs.thucchien.ai/docs/round-2/user-guide/video-generation-veo3) · [TTS](https://docs.thucchien.ai/docs/round-2/user-guide/text-to-speech) · [STT](https://docs.thucchien.ai/docs/round-2/user-guide/speech-to-text)
