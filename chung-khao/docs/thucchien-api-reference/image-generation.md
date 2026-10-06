Nguồn: https://docs.thucchien.ai/docs/round-2/api-reference/image-generation

Tải lúc: 2026-10-05T09:03:17.854876+07:00

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* [Tham chiếu API](https://docs.thucchien.ai/docs/api-reference)
* Sinh hình ảnh

# Sinh hình ảnh (Image Generation)

## POST `/images/generations`[​](https://docs.thucchien.ai/docs/round-2/api-reference/image-generation#-imagesgenerations "Direct link to -imagesgenerations")

Tạo một hoặc nhiều hình ảnh dựa trên mô tả văn bản (prompt).

Phương pháp thay thế

Ngoài endpoint này, bạn cũng có thể tạo ảnh bằng cách sử dụng các mô hình đa phương thức thông qua endpoint [`/chat/completions`](https://docs.thucchien.ai/docs/round-2/api-reference/image-generation-chat).

Tham khảo

Chi tiết đầy đủ các tham số, tham khảo [tài liệu LiteLLM API](https://docs.litellm.ai/docs/image_generation)

### Cấu trúc yêu cầu (Request Body)[​](https://docs.thucchien.ai/docs/round-2/api-reference/image-generation#cấu-trúc-yêu-cầu-request-body "Direct link to Cấu trúc yêu cầu (Request Body)")

`prompt`stringRequired

Mô tả chi tiết về hình ảnh cần tạo.

`model`stringRequired

Mô hình Nano Banana (Gemini Image) sẽ sử dụng để tạo ảnh. Tên alias và ID gốc gọi cùng một model:

* `nano-banana-2` = `gemini-3.1-flash-image`
* `nano-banana-2-lite` = `gemini-3.1-flash-lite-image`: rẻ và nhanh nhất
* `nano-banana-pro` = `gemini-3-pro-image`: chất lượng cao nhất
* `nano-banana` = `gemini-2.5-flash-image`: Google ngừng hỗ trợ từ 02/10/2026

`n`integer

Số lượng hình ảnh cần tạo. Chỉ hỗ trợ `1`; cần nhiều ảnh thì gửi nhiều request.

`aspect_ratio`string

Tỷ lệ khung hình của ảnh. Có thể là `1:1`, `3:4`, `4:3`, `16:9`, `9:16`. Mặc định `1:1`. Tham số `size` không có tác dụng, hãy dùng `aspect_ratio`.

---

### Cấu trúc Phản hồi (Response Body)[​](https://docs.thucchien.ai/docs/round-2/api-reference/image-generation#cấu-trúc-phản-hồi-response-body "Direct link to Cấu trúc Phản hồi (Response Body)")

API sẽ trả về một đối tượng JSON chứa danh sách các hình ảnh được tạo.

#### Đối tượng `ImageResponse`[​](https://docs.thucchien.ai/docs/round-2/api-reference/image-generation#đối-tượng-imageresponse "Direct link to đối-tượng-imageresponse")

`created`integer

Thời gian Unix timestamp của thời điểm yêu cầu được tạo.

`data`array

Một danh sách các đối tượng hình ảnh được tạo.

`b64_json`string

Dữ liệu hình ảnh được mã hóa dưới dạng Base64.

`revised_prompt`string

Prompt đã được tinh chỉnh bởi mô hình để tạo ra hình ảnh tốt hơn (nếu có).

curlPython (openai)Python (requests)Python (litellm)

```
curl https://api.thucchien.ai/images/generations \



-H "Content-Type: application/json" \



-H "Authorization: Bearer " \



-d '{



"model": "nano-banana-2nano-banana-2-litenano-banana-progemini-3.1-flash-imagegemini-3.1-flash-lite-imagegemini-3-pro-imagegemini-2.5-flash-image",



"prompt": " a digital render of a massive skyscraper, modern, grand, epic with a beautiful sunset in the background ",



"aspect_ratio": "1:13:44:316:99:16"



}'
```

Example Response

```
{
  "created": 1759806089,
  "data": [
    {
      "b64_json": "iVBORw0KGgoAAAANSUhEUgAABAAAAAQACAIAAADwf7zUAAAgAE... [TRUNCATED]",
      "revised_prompt": "A photorealistic image of an astronaut in a full s... [TRUNCATED] ...th is visible as a small blue dot in the distance."
    }
  ]
}
```