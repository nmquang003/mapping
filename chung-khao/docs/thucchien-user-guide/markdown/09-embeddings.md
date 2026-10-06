Nguồn: https://docs.thucchien.ai/docs/round-2/user-guide/embeddings

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* [Hướng dẫn sử dụng API](00-overview.md)
* Embedding

# Embedding



Embedding biến một đoạn văn bản thành một vector số, dùng cho tìm kiếm ngữ nghĩa, RAG, phân cụm hay so sánh độ giống nhau giữa các câu. Gọi qua endpoint `/embeddings`, cùng `base_url` và API key như các trang trước.

## Danh sách model[​](09-embeddings.md#danh-sách-model "Direct link to Danh sách model")

| Model | Nhà cung cấp | Số chiều | Ngôn ngữ | Giá input /1M token |
| --- | --- | --- | --- | --- |
| `gemini-embedding-001` | Agent Platform | 3072 | đa ngôn ngữ, có tiếng Việt | $0.15 |
| `gemini-embedding-2` | Agent Platform | 3072 | đa ngôn ngữ, có tiếng Việt | $0.2 |
| `text-multilingual-embedding-002` | Agent Platform | 768 | đa ngôn ngữ, có tiếng Việt | $0.1 |
| `text-embedding-005` | Agent Platform | 768 | chủ yếu tiếng Anh | $0.1 |
| `text-embedding-3-small` | OpenAI | 1536 | đa ngôn ngữ | $0.02 |
| `text-embedding-3-large` | OpenAI | 3072 | đa ngôn ngữ | $0.13 |

"Agent Platform" là Gemini Enterprise Agent Platform (trước đây là Vertex AI) của Google Cloud.

`gemini-embedding-2`: mỗi request một đoạn văn bản

Với `gemini-embedding-2`, nếu `input` là danh sách nhiều đoạn, gateway chỉ trả về **một** vector. Hãy gửi mỗi đoạn trong một request riêng. Các model còn lại nhận được danh sách nhiều đoạn trong một request.

Vector từ các model khác nhau không so sánh được với nhau. Hãy dùng cùng một model cho cả lúc lập chỉ mục và lúc truy vấn.

## Ví dụ[​](09-embeddings.md#ví-dụ "Direct link to Ví dụ")

```
from openai import OpenAI

client = OpenAI(api_key="<your_api_key>", base_url="https://api.thucchien.ai")

emb = client.embeddings.create(
  model="gemini-embedding-001",
  input=["Hà Nội là thủ đô của Việt Nam", "Thủ đô Việt Nam là thành phố nào?"],
)

print(len(emb.data), len(emb.data[0].embedding))  # 2 3072
```

```
curl https://api.thucchien.ai/embeddings \
-H "Authorization: Bearer <your_api_key>" \
-H "Content-Type: application/json" \
-d '{"model": "text-multilingual-embedding-002", "input": "xin chào"}'
```

## Tham khảo[​](09-embeddings.md#tham-khảo "Direct link to Tham khảo")

* [Text embeddings — Gemini Enterprise Agent Platform](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings)
* [Embeddings — OpenAI](https://platform.openai.com/docs/guides/embeddings)
* [Bảng giá model](11-pricing.md)