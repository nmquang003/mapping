Nguồn: https://docs.thucchien.ai/docs/round-2/user-guide/google-search-grounding

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* [Hướng dẫn sử dụng API](00-overview.md)
* Tìm kiếm web (Google Search grounding)

# Tìm kiếm web (Google Search grounding)



Mặc định, model chỉ biết thông tin đến thời điểm được huấn luyện. Bật **tìm kiếm web** thì model tự tạo truy vấn, tìm trên Internet rồi trả lời dựa trên kết quả mới nhất, kèm danh sách nguồn. Tính năng này hợp với câu hỏi về tin tức, giá cả, lịch thi đấu hay số liệu mới.

| Nhóm model | Cách bật | Endpoint |
| --- | --- | --- |
| Gemini (Gemini Enterprise Agent Platform (trước đây là Vertex AI)) | `tools=[{"googleSearch": {}}]` | `POST /chat/completions` |
| OpenAI (`gpt-5.6-*`, `gpt-6*`, `o3`, `o4-mini`) | `tools=[{"type": "web_search"}]` | `POST /responses` |
| DeepSeek | Không hỗ trợ | — |

Chi phí

Mỗi lượt tìm kiếm tốn khoảng **$0.01–$0.035**, đắt hơn hàng chục lần một câu hỏi thường. Chi phí này trừ thẳng vào budget của key. Chỉ bật khi thật sự cần thông tin mới. Xem [bảng giá](08-google-search-grounding.md#b%E1%BA%A3ng-gi%C3%A1).

## Gemini: Google Search grounding[​](08-google-search-grounding.md#gemini-google-search-grounding "Direct link to Gemini: Google Search grounding")

**Model hỗ trợ:** tất cả model Gemini sinh văn bản, gồm `gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemini-3.1-pro-preview`, `gemini-2.5-pro` và `gemini-2.5-flash`.

Thêm tool `googleSearch` vào request. Model tự quyết định có cần tìm kiếm hay không, và có thể chạy nhiều truy vấn trong một request.

* Python (openai)
* curl

```
from openai import OpenAI

client = OpenAI(
  api_key="<your_api_key>",
  base_url="https://api.thucchien.ai"
)

response = client.chat.completions.create(
  model="gemini-3.5-flash-lite",
  messages=[{"role": "user", "content": "Tỷ giá USD/VND hôm nay là bao nhiêu?"}],
  tools=[{"googleSearch": {}}],
)

print(response.choices[0].message.content)

# Thông tin tìm kiếm: truy vấn đã chạy và nguồn tham khảo
grounding = response.model_extra.get("vertex_ai_grounding_metadata") or []
for meta in grounding:
  print("Truy vấn:", meta.get("webSearchQueries"))
  for chunk in meta.get("groundingChunks", []):
      print("-", chunk["web"]["title"], chunk["web"]["uri"])
```

```
curl https://api.thucchien.ai/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_api_key>" \
-d '{
  "model": "gemini-3.5-flash-lite",
  "messages": [{"role": "user", "content": "Tỷ giá USD/VND hôm nay là bao nhiêu?"}],
  "tools": [{"googleSearch": {}}]
}'
```

Response giữ nguyên chuẩn OpenAI và có thêm trường `vertex_ai_grounding_metadata` (một list). Mỗi phần tử gồm:

| Trường | Ý nghĩa |
| --- | --- |
| `webSearchQueries` | Các truy vấn model đã chạy. Mỗi truy vấn tính phí riêng với Gemini 3.x. |
| `groundingChunks` | Nguồn tham khảo (`web.title`, `web.uri`). `uri` là link chuyển hướng qua Google. |
| `groundingSupports` | Đoạn nào trong câu trả lời được nguồn nào hỗ trợ. |
| `searchEntryPoint` | HTML gợi ý tìm kiếm của Google (Search Suggestions). |

Quy định hiển thị của Google

Nếu hiển thị câu trả lời có grounding cho người dùng cuối (ví dụ trong sản phẩm demo), Google yêu cầu hiển thị kèm **Search Suggestions** lấy từ `searchEntryPoint.renderedContent`. Chi tiết xem [tài liệu Grounding with Google Search](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/grounding-with-google-search).

note

Tham số `web_search_options` (kiểu OpenAI) chỉ hoạt động với một số model Gemini. Với `gemini-2.5-flash` và model OpenAI, tham số này bị bỏ qua và model trả lời mà không tìm kiếm. Hãy dùng `tools=[{"googleSearch": {}}]` như trên.

## OpenAI: web search qua Responses API[​](08-google-search-grounding.md#openai-web-search-qua-responses-api "Direct link to OpenAI: web search qua Responses API")

Model OpenAI chỉ tìm kiếm web qua endpoint **`/responses`**, không qua `/chat/completions`.

**Model hỗ trợ:** `gpt-5.6-*`, `gpt-6-*`, `gpt-6.1-sol`, `o3`, `o4-mini`.

* Python (openai)
* curl

```
from openai import OpenAI

client = OpenAI(
  api_key="<your_api_key>",
  base_url="https://api.thucchien.ai"
)

response = client.responses.create(
  model="gpt-6-luna",
  input="Tỷ giá USD/VND hôm nay là bao nhiêu?",
  tools=[{"type": "web_search"}],
)

# Câu trả lời đã kèm link nguồn dạng markdown
print(response.output_text)
```

```
curl https://api.thucchien.ai/responses \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_api_key>" \
-d '{
  "model": "gpt-6-luna",
  "input": "Tỷ giá USD/VND hôm nay là bao nhiêu?",
  "tools": [{"type": "web_search"}]
}'
```

Trong `response.output`, mỗi lần tìm kiếm là một phần tử `web_search_call`. Câu trả lời nằm trong phần tử `message`, và nguồn nằm trong `content[].annotations`.

## Bảng giá[​](08-google-search-grounding.md#bảng-giá "Direct link to Bảng giá")

Ngoài tiền token như bình thường, gateway tính thêm phí tìm kiếm:

| Model | Phí tìm kiếm | Đơn vị tính |
| --- | --- | --- |
| Gemini 3.x (`gemini-3.x-*`, `gemini-3.1-pro-preview`) | $0.014 | mỗi **truy vấn** (một request thường chạy 1–3 truy vấn) |
| `gemini-2.5-pro`, `gemini-2.5-flash` | $0.035 | mỗi **request** có dùng tìm kiếm |
| OpenAI (`/responses` + `web_search`) | $0.01 | mỗi lần gọi `web_search` |

Chi phí thực tế đo được trên gateway là khoảng $0.028–$0.058 cho mỗi câu hỏi có tìm kiếm. Kết quả tìm kiếm được đưa vào input của model, nên số token input cũng tăng theo.

## Mẹo[​](08-google-search-grounding.md#mẹo "Direct link to Mẹo")

* Chỉ bật tìm kiếm cho câu hỏi cần thông tin mới. Với kiến thức phổ thông, gọi model bình thường vừa rẻ vừa nhanh hơn.
* Nên ghi rõ ngày trong câu hỏi (ví dụ "hôm nay 28/9/2026") để model tìm đúng thời điểm.
* Model rẻ như `gemini-3.1-flash-lite` cho kết quả tìm kiếm không thua model lớn trong phần lớn câu hỏi tra cứu.

## Tham khảo[​](08-google-search-grounding.md#tham-khảo "Direct link to Tham khảo")

* [Grounding with Google Search — Agent Platform](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/grounding-with-google-search)
* [Bảng giá Agent Platform (mục Grounding)](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing)
* [Web search — OpenAI](https://platform.openai.com/docs/guides/tools-web-search)
* [Web search — LiteLLM](https://docs.litellm.ai/docs/completion/web_search)