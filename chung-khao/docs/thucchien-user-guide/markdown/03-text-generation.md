Nguồn: https://docs.thucchien.ai/docs/round-2/user-guide/text-generation

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* [Hướng dẫn sử dụng API](00-overview.md)
* Sinh văn bản (Text Generation)

# Sinh văn bản (Text Generation)



Các mô hình sinh văn bản cho phép bạn thực hiện nhiều tác vụ như trả lời câu hỏi, viết nội dung, tóm tắt văn bản, và nhiều hơn nữa. API này tuân theo chuẩn của OpenAI, vì vậy bạn có thể sử dụng các thư viện client của OpenAI một cách trực tiếp.

**Các model được hỗ trợ** (Gemini Enterprise Agent Platform (trước đây là Vertex AI)):

* `gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.6-flash`, `gemini-3.5-flash`
* `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`
* `gemini-3.1-pro-preview`
* `gemini-2.5-pro`, `gemini-2.5-flash`

**Model OpenAI và DeepSeek** cũng gọi được qua endpoint này, ví dụ `gpt-6-luna`, `gpt-6.1-sol`, `deepseek-flash`. Danh sách đầy đủ và các lưu ý riêng (reasoning, thinking) xem ở [Model OpenAI và DeepSeek](10-openai-deepseek.md). Cần thông tin mới trên Internet? Xem [Tìm kiếm web](08-google-search-grounding.md).

Tham khảo API chi tiết

Để xem danh sách đầy đủ các tham số request, response và các ví dụ chi tiết, vui lòng truy cập trang [**Tham chiếu API: Sinh văn bản**](https://docs.thucchien.ai/docs/round-2/api-reference/text-generation).

## Ví dụ nhanh[​](03-text-generation.md#ví-dụ-nhanh "Direct link to Ví dụ nhanh")

Dưới đây là một ví dụ nhanh sử dụng thư viện `openai` trong Python, là cách tiếp cận được khuyến khích vì sự tiện lợi và quen thuộc.

```
from openai import OpenAI

# --- Cấu hình ---
# Thay <your_api_key> bằng API key của bạn
client = OpenAI(
  api_key="<your_api_key>",
  base_url="https://api.thucchien.ai"
)

# --- Thực thi ---
response = client.chat.completions.create(
  model="gemini-2.5-pro", # Chọn model bạn muốn
  messages=[
      {
          "role": "user",
          "content": "Explain the concept of API gateway in simple terms."
      }
  ]
)

print(response.choices[0].message.content)
```