Nguồn: https://docs.thucchien.ai/docs/round-2/user-guide/openai-deepseek

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* [Hướng dẫn sử dụng API](00-overview.md)
* Model OpenAI và DeepSeek

# Model OpenAI và DeepSeek



Ngoài Gemini, gateway còn cung cấp model của **OpenAI** và **DeepSeek**. Cách gọi y hệt các trang trước: cùng `base_url="https://api.thucchien.ai"`, cùng API key, chỉ cần đổi `model`.

## Danh sách model[​](10-openai-deepseek.md#danh-sách-model "Direct link to Danh sách model")

| Tác vụ | Model | Endpoint |
| --- | --- | --- |
| Sinh văn bản (reasoning) | `gpt-6.1-sol`, `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `o3`, `o4-mini` | `/chat/completions`, `/responses` |
| Sinh văn bản (DeepSeek) | `deepseek-flash`, `deepseek-v4-pro` | `/chat/completions` |
| Tạo ảnh | `gpt-image-2.5-flare`, `gpt-image-2.5-sunburst` | `/images/generations` |
| Text-to-speech | `gpt-4o-mini-tts` | `/audio/speech` |
| Speech-to-text | `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `gpt-transcribe`, `whisper-1` | `/audio/transcriptions` |
| Embedding | `text-embedding-3-small` (1536 chiều), `text-embedding-3-large` (3072 chiều). Embedding của Gemini xem ở [Embedding](09-embeddings.md) | `/embeddings` |
| Kiểm duyệt nội dung | `omni-moderation-latest` (miễn phí) | `/moderations` |

Giá từng model xem ở [Bảng giá model](11-pricing.md).

## OpenAI[​](10-openai-deepseek.md#openai "Direct link to OpenAI")

### Model reasoning (`gpt-5.6-*`, `gpt-6*`, `o3`, `o4-mini`)[​](10-openai-deepseek.md#model-reasoning-gpt-56--gpt-6-o3-o4-mini "Direct link to model-reasoning-gpt-56--gpt-6-o3-o4-mini")

Mọi model sinh văn bản của OpenAI trên gateway đều là model reasoning. Model reasoning "suy nghĩ" trước khi trả lời. Token suy nghĩ không hiển thị nhưng **vẫn tính tiền như output** và **vẫn tính vào giới hạn độ dài**.

* **Dùng `max_completion_tokens` thay cho `max_tokens`.** Mọi model `gpt-6*` (`gpt-6.1-sol`, `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`) báo lỗi 400 nếu gửi `max_tokens`:

  ```
  Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.
  ```

  `gpt-5.6-*`, `o3`, `o4-mini` vẫn nhận `max_tokens`, nhưng dùng `max_completion_tokens` cho mọi model là an toàn nhất. Với `/responses`, tham số tương ứng là `max_output_tokens`.
* **Đừng đặt `max_completion_tokens` quá nhỏ.** Ví dụ với giới hạn 50 token, model có thể dùng hết 50 token để suy nghĩ và trả về `content` **rỗng**. Nên để trống, hoặc đặt từ vài nghìn trở lên.
* **`temperature`, `top_p` không có tác dụng.** Gateway tự bỏ các tham số này thay vì báo lỗi.

### Mức suy nghĩ (`reasoning_effort`)[​](10-openai-deepseek.md#mức-suy-nghĩ-reasoning_effort "Direct link to mức-suy-nghĩ-reasoning_effort")

`reasoning_effort` quyết định model suy nghĩ bao lâu trước khi trả lời. Mức cao trả lời tốt hơn với bài khó nhưng chậm hơn và tốn nhiều token output hơn. Mặc định là `medium`.

* `/chat/completions`: gửi `reasoning_effort="low"`.
* `/responses`: gửi `reasoning={"effort": "low"}`.

Mức mỗi model nhận (kiểm tra qua `/responses`):

| Model | `none` | `low` / `medium` / `high` | `xhigh` / `max` |
| --- | --- | --- | --- |
| `gpt-6-sol`, `gpt-6-luna`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna` | ✅ | ✅ | ✅ |
| `gpt-6.1-sol`, `gpt-6-astra` | ❌ | ✅ | ✅ |
| `o3`, `o4-mini` | ❌ | ✅ | ❌ |

* `none` tắt hẳn suy nghĩ, vừa nhanh vừa rẻ với câu hỏi đơn giản (phân loại, trích xuất, viết lại…).
* **Không model nào nhận `minimal`.**
* Gửi mức model không hỗ trợ qua `/responses` sẽ bị lỗi 400 `Unsupported value: '...' is not supported with the '<model>' model`. Qua `/chat/completions` request vẫn thành công nhưng mức đó **có thể bị bỏ qua mà không báo lỗi**, nên hãy chọn mức trong bảng trên.
* Số token suy nghĩ đã dùng nằm ở `usage.completion_tokens_details.reasoning_tokens` (`/chat/completions`) hoặc `usage.output_tokens_details.reasoning_tokens` (`/responses`).

```
from openai import OpenAI

client = OpenAI(api_key="<your_api_key>", base_url="https://api.thucchien.ai")

response = client.chat.completions.create(
  model="gpt-6-luna",
  messages=[{"role": "user", "content": "Tóm tắt luật chơi cờ tướng trong 3 câu."}],
  reasoning_effort="low",
  max_completion_tokens=4000,
)

print(response.choices[0].message.content)
print(response.usage.completion_tokens_details.reasoning_tokens, "token suy nghĩ")
```

Cùng yêu cầu qua Responses API:

```
response = client.responses.create(
  model="gpt-6-luna",
  input="Tóm tắt luật chơi cờ tướng trong 3 câu.",
  reasoning={"effort": "low"},
  max_output_tokens=4000,
)

print(response.output_text)
print(response.usage.output_tokens_details.reasoning_tokens, "token suy nghĩ")
```

### Tạo ảnh (`gpt-image-*`)[​](10-openai-deepseek.md#tạo-ảnh-gpt-image- "Direct link to tạo-ảnh-gpt-image-")

Gọi `/images/generations` như [trang Tạo ảnh](04-image-generation.md). Khác với Nano Banana:

* Chọn kích thước bằng `size` (`1024x1024`, `1536x1024`, `1024x1536`) và chất lượng bằng `quality` (`low`, `medium`, `high`). `quality="low"` rẻ nhất.
* Giá tính theo image token, nên phụ thuộc `size` và `quality`. Ảnh `gpt-image-2.5-flare` 1024×1024 `low` tốn khoảng $0.006.
* Ảnh trả về dạng base64 trong `data[0].b64_json`.

```
import base64
from openai import OpenAI

client = OpenAI(api_key="<your_api_key>", base_url="https://api.thucchien.ai")

result = client.images.generate(
  model="gpt-image-2.5-flare",
  prompt="Một chú mèo đội nón lá, phong cách tranh Đông Hồ",
  size="1024x1024",
  quality="low",
)

with open("cat.png", "wb") as f:
  f.write(base64.b64decode(result.data[0].b64_json))
```

### Âm thanh[​](10-openai-deepseek.md#âm-thanh "Direct link to Âm thanh")

* **Text-to-speech**: `gpt-4o-mini-tts` dùng giọng của OpenAI (`alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`…), không dùng giọng Gemini như `Kore`. File trả về là `mp3`.
* **Speech-to-text**: gọi giống [trang Speech-to-Text](07-speech-to-text.md). Riêng `gpt-transcribe` **bắt buộc** gửi `response_format="json"`, nếu không sẽ lỗi 400.

```
with open("speech.mp3", "rb") as audio_file:
  transcript = client.audio.transcriptions.create(
      model="gpt-transcribe",
      file=audio_file,
      response_format="json",
  )
print(transcript.text)
```

### Embedding và kiểm duyệt[​](10-openai-deepseek.md#embedding-và-kiểm-duyệt "Direct link to Embedding và kiểm duyệt")

```
emb = client.embeddings.create(model="text-embedding-3-small", input=["xin chào", "tạm biệt"])
print(len(emb.data[0].embedding))  # 1536

mod = client.moderations.create(model="omni-moderation-latest", input="nội dung cần kiểm tra")
print(mod.results[0].flagged)
```

## DeepSeek[​](10-openai-deepseek.md#deepseek "Direct link to DeepSeek")

| Model | Đặc điểm |
| --- | --- |
| `deepseek-flash` | Nhanh, rẻ. Hợp với phần lớn tác vụ văn bản. |
| `deepseek-v4-pro` | Mạnh hơn, giá gấp khoảng 4 lần. |

Tên model `deepseek-flash`

Hãy dùng `deepseek-flash` làm tên model. Theo DeepSeek, hai tên cũ `deepseek-v4-flash` và `deepseek-v4-flash-vision-exp` vẫn được API DeepSeek chấp nhận, nhưng các model tương ứng đã ngừng hoạt động: request gửi tới hai tên này do model DeepSeek-V4.1-Flash xử lý và tính theo giá Flash. Gateway không mở hai tên cũ này (trả lỗi `403`), chỉ gọi bằng `deepseek-flash`. Xem [bảng giá DeepSeek](https://api-docs.deepseek.com/quick_start/pricing/).

**Chế độ suy nghĩ (thinking) bật sẵn.** Phần suy nghĩ trả về riêng trong `message.reasoning_content`, còn câu trả lời vẫn nằm trong `message.content`. Token suy nghĩ tính tiền như output.

**Tắt thinking** khi không cần suy luận nhiều (phân loại, trích xuất, viết lại…). Chi phí giảm khoảng 10 lần:

```
from openai import OpenAI

client = OpenAI(api_key="<your_api_key>", base_url="https://api.thucchien.ai")

response = client.chat.completions.create(
  model="deepseek-flash",
  messages=[{"role": "user", "content": "Phân loại cảm xúc: 'Đồ ăn ngon, phục vụ chậm'"}],
  extra_body={"thinking": {"type": "disabled"}},  # bỏ dòng này để bật lại thinking
)

print(response.choices[0].message.content)
```

Khi bật thinking, đọc phần suy nghĩ như sau:

```
msg = response.choices[0].message
print(getattr(msg, "reasoning_content", None))  # quá trình suy nghĩ
print(msg.content)                              # câu trả lời
```

Lưu ý khác:

* **JSON mode**: `response_format={"type": "json_object"}` hoạt động. Trong prompt phải có chữ "JSON" và mô tả cấu trúc mong muốn.
* **Không hỗ trợ** ảnh đầu vào, tạo ảnh, âm thanh hay tìm kiếm web. Với các tác vụ này, hãy dùng Gemini hoặc OpenAI.
* DeepSeek giới hạn theo **số request đồng thời** trên toàn gateway, không theo từng đội. Đừng bắn hàng trăm request song song cùng lúc.

## Lưu ý chung[​](10-openai-deepseek.md#lưu-ý-chung "Direct link to Lưu ý chung")

* Model OpenAI và DeepSeek dùng chung một tài khoản cho tất cả các đội. Nếu nhận lỗi `429`, hãy chờ vài giây rồi thử lại (SDK `openai` tự thử lại 2 lần).
* Cần thông tin mới trên Internet? Xem [Tìm kiếm web](08-google-search-grounding.md).

## Tham khảo[​](10-openai-deepseek.md#tham-khảo "Direct link to Tham khảo")

* [Reasoning models — OpenAI](https://platform.openai.com/docs/guides/reasoning)
* [API reference: Chat Completions — OpenAI](https://platform.openai.com/docs/api-reference/chat/create) (`reasoning_effort`, `max_completion_tokens`)
* [API reference: Responses — OpenAI](https://platform.openai.com/docs/api-reference/responses/create) (`reasoning.effort`, `max_output_tokens`)
* [Reasoning content — LiteLLM](https://docs.litellm.ai/docs/reasoning_content) (cách gateway chuyển `reasoning_effort` tới từng nhà cung cấp)
* [Web search — OpenAI](https://platform.openai.com/docs/guides/tools-web-search)
* [Tài liệu API DeepSeek](https://api-docs.deepseek.com/)
* [Thinking mode — DeepSeek](https://api-docs.deepseek.com/guides/thinking_mode)
* [Models & Pricing — DeepSeek](https://api-docs.deepseek.com/quick_start/pricing/)