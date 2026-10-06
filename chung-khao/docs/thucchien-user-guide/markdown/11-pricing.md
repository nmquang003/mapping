Nguồn: https://docs.thucchien.ai/docs/round-2/user-guide/pricing

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* [Hướng dẫn sử dụng API](00-overview.md)
* Bảng giá model

# Bảng giá model

Giá tính bằng **USD**, là mức gateway dùng để trừ budget của key. `/1M` nghĩa là trên 1 triệu token. Bạn xem chi phí từng request trong header `x-litellm-response-cost` hoặc trên trang quản lý key.

Tiết kiệm budget

* Chọn model nhỏ trước (`gemini-3.1-flash-lite`, `gpt-6-luna`, `deepseek-flash`…), chỉ nâng lên model lớn khi cần.
* Model reasoning tính cả token suy nghĩ vào output. Giảm bằng `reasoning_effort="none"`/`"low"` (OpenAI) hoặc tắt thinking (DeepSeek), xem [Model OpenAI và DeepSeek](10-openai-deepseek.md).
* Phần input lặp lại giữa các request (system prompt dài) được tính giá **cached input** rẻ hơn khoảng 10 lần.

## Sinh văn bản[​](11-pricing.md#sinh-văn-bản "Direct link to Sinh văn bản")

| Model | Nhà cung cấp | Input /1M | Cached input /1M | Output /1M | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| `deepseek-flash` | DeepSeek | $0.3 | $0.006 | $1.2 | model DeepSeek-V4.1-Flash, thay cho tên cũ `deepseek-v4-flash` ([DeepSeek](https://api-docs.deepseek.com/quick_start/pricing/)) |
| `deepseek-v4-pro` | DeepSeek | $1.32 | $0.044 | $3.96 |  |
| `gpt-5.6-luna` | OpenAI | $0.2 | $0.02 | $1.2 |  |
| `gpt-5.6-sol` | OpenAI | $4 | $0.4 | $20 |  |
| `gpt-5.6-terra` | OpenAI | $2 | $0.2 | $12 |  |
| `gpt-6-astra` | OpenAI | $10 | $1 | $50 |  |
| `gpt-6-luna` | OpenAI | $0.1 | $0.01 | $0.5 |  |
| `gpt-6-sol` | OpenAI | $2 | $0.2 | $10 |  |
| `gpt-6.1-sol` | OpenAI | $2 | $0.1 | $10 |  |
| `o3` | OpenAI | $2 | $0.5 | $8 |  |
| `o4-mini` | OpenAI | $1.1 | $0.275 | $4.4 |  |
| `gemini-2.5-flash` | Agent Platform | $0.3 | $0.03 | $2.5 | audio in $1 |
| `gemini-2.5-pro` | Agent Platform | $1.25 | $0.125 | $10 | >200k token: in $2.5 / out $15 |
| `gemini-3.1-flash-lite` | Agent Platform | $0.25 | $0.025 | $1.5 | audio in $0.5 |
| `gemini-3.1-pro-preview` | Agent Platform | $2 | $0.2 | $12 | >200k token: in $4 / out $18 |
| `gemini-3.5-flash` | Agent Platform | $1.5 | $0.15 | $9 |  |
| `gemini-3.5-flash-lite` | Agent Platform | $0.3 | $0.03 | $2.5 |  |
| `gemini-3.6-flash` | Agent Platform | $0.75 | $0.075 | $3.75 |  |
| `gemini-3.7-flash` | Agent Platform | $0.75 | $0.075 | $3.75 |  |
| `gemini-3.8-flash` | Agent Platform | $0.75 | $0.075 | $3.75 |  |

## Tạo ảnh[​](11-pricing.md#tạo-ảnh "Direct link to Tạo ảnh")

Model Gemini tính theo **ảnh output** (giá/ảnh ở độ phân giải mặc định 1K). Model `gpt-image-*` tính theo **image token** — chi phí 1 ảnh phụ thuộc kích thước và `quality` (low rẻ nhất).

| Model | Nhà cung cấp | Text input /1M | Image input /1M | Output text /1M | Output image token /1M | Giá / ảnh |
| --- | --- | --- | --- | --- | --- | --- |
| `gpt-image-2.5-flare` | OpenAI | $5 | $8 |  | $30 |  |
| `gpt-image-2.5-sunburst` | OpenAI | $5 | $8 |  | $30 |  |
| `gemini-2.5-flash-image` | Agent Platform | $0.3 |  | $2.5 | $30 | $0.039 |
| `gemini-3-pro-image` | Agent Platform | $2 |  | $12 | $120 | $0.134 |
| `gemini-3.1-flash-image` | Agent Platform | $0.5 |  | $3 | $60 | $0.0672 |
| `gemini-3.1-flash-lite-image` | Agent Platform | $0.25 |  | $1.5 | $30 | $0.0336 |
| `nano-banana` (= `gemini-2.5-flash-image`) | Agent Platform | $0.3 |  | $2.5 | $30 | $0.039 |
| `nano-banana-2` (= `gemini-3.1-flash-image`) | Agent Platform | $0.5 |  | $3 | $60 | $0.0672 |
| `nano-banana-2-lite` (= `gemini-3.1-flash-lite-image`) | Agent Platform | $0.25 |  | $1.5 | $30 | $0.0336 |
| `nano-banana-pro` (= `gemini-3-pro-image`) | Agent Platform | $2 |  | $12 | $120 | $0.134 |

## Tạo video[​](11-pricing.md#tạo-video "Direct link to Tạo video")

| Model | Nhà cung cấp | 720p / giây | 1080p / giây | 4K / giây | Ví dụ 8 giây 720p |
| --- | --- | --- | --- | --- | --- |
| `veo-3.1-fast-generate-001` | Agent Platform | $0.1 | $0.12 | $0.3 | $0.8 |
| `veo-3.1-generate-001` | Agent Platform | $0.4 | = 720p | $0.6 | $3.2 |
| `veo-3.1-lite-generate-001` | Agent Platform | $0.05 | $0.08 | — | $0.4 |

## Text-to-speech[​](11-pricing.md#text-to-speech "Direct link to Text-to-speech")

| Model | Nhà cung cấp | Text input /1M token | Audio output /1M token | Khác |
| --- | --- | --- | --- | --- |
| `gpt-4o-mini-tts` | OpenAI | $0.6 | $12 | ≈ $0.015 / phút audio |
| `gemini-2.5-flash-preview-tts` | Agent Platform | $0.5 | $10 |  |
| `gemini-2.5-pro-preview-tts` | Agent Platform | $1 | $20 |  |
| `gemini-3.1-flash-tts-preview` | Agent Platform | $1 | $20 |  |

## Speech-to-text[​](11-pricing.md#speech-to-text "Direct link to Speech-to-text")

| Model | Nhà cung cấp | Audio input | Text output /1M | ≈ / phút audio |
| --- | --- | --- | --- | --- |
| `gpt-4o-mini-transcribe` | OpenAI | $0.000050 / giây | $5 | $0.003 |
| `gpt-4o-transcribe` | OpenAI | $0.000100 / giây | $10 | $0.006 |
| `gpt-transcribe` | OpenAI | $0.000075 / giây |  | $0.0045 |
| `whisper-1` | OpenAI | $0.000100 / giây |  | $0.006 |
| `gemini-3.5-transcribe-preview` | Agent Platform | $2 /1M token | $12 | ~$0.0038 |

## Embedding & moderation[​](11-pricing.md#embedding--moderation "Direct link to Embedding & moderation")

| Model | Nhà cung cấp | Loại | Input /1M |
| --- | --- | --- | --- |
| `gemini-embedding-001` | Agent Platform | embedding | $0.15 |
| `gemini-embedding-2` | Agent Platform | embedding | $0.2 |
| `text-embedding-005` | Agent Platform | embedding | $0.1 |
| `text-multilingual-embedding-002` | Agent Platform | embedding | $0.1 |
| `text-embedding-3-large` | OpenAI | embedding | $0.13 |
| `text-embedding-3-small` | OpenAI | embedding | $0.02 |
| `omni-moderation-latest` | OpenAI | moderation | miễn phí |

## Tìm kiếm web (grounding)[​](11-pricing.md#tìm-kiếm-web-grounding "Direct link to Tìm kiếm web (grounding)")

Tính **thêm** vào tiền token, xem hướng dẫn ở [Tìm kiếm web](08-google-search-grounding.md).

| Model | Phí tìm kiếm | Đơn vị tính |
| --- | --- | --- |
| Gemini 3.x (`gemini-3.x-*`, `gemini-3.1-pro-preview`) | $0.014 | mỗi truy vấn tìm kiếm |
| `gemini-2.5-pro`, `gemini-2.5-flash` | $0.035 | mỗi request có dùng tìm kiếm |
| OpenAI (`/responses` + `web_search`) | $0.01 | mỗi lần gọi `web_search` |

## Lưu ý[​](11-pricing.md#lưu-ý "Direct link to Lưu ý")

* "Agent Platform" là Gemini Enterprise Agent Platform của Google Cloud, tên mới của Vertex AI.
* Model reasoning (`gpt-5.6-*`, `gpt-6*`, `o3`, `o4-mini`, `gemini-3.x`, `deepseek-*`) tính cả token suy nghĩ vào output, nên chi phí thực thường cao hơn độ dài câu trả lời nhìn thấy.
* `gemini-3.5-transcribe-preview` tính theo audio token (khoảng 32 token/giây), nên cột "/ phút" là ước tính.
* Giá gốc của nhà cung cấp: [Gemini Enterprise Agent Platform (trước đây là Vertex AI)](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing), [OpenAI](https://platform.openai.com/docs/pricing), [DeepSeek](https://api-docs.deepseek.com/quick_start/pricing).