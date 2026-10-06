Nguồn: https://docs.thucchien.ai/docs/round-2/user-guide/core-concepts

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* [Hướng dẫn sử dụng API](00-overview.md)
* Các khái niệm cốt lõi

# Các khái niệm cốt lõi



---

## 1. Giao diện API Hợp nhất & Tương thích OpenAI[​](02-core-concepts.md#1-giao-diện-api-hợp-nhất--tương-thích-openai "Direct link to 1. Giao diện API Hợp nhất & Tương thích OpenAI")

Thay vì phải làm việc với nhiều API phức tạp từ các nhà cung cấp khác nhau, AI Thực chiến - API Gateway cung cấp một **endpoint duy nhất** và một bộ quy tắc nhất quán.

* **Endpoint duy nhất:** Mọi yêu cầu đều được gửi đến `https://api.thucchien.ai`.
* **Tương thích với nhiều nhà cung cấp:** Cung cấp một giao diện thống nhất cho tất cả các nhà cung cấp này, cho phép bạn chuyển đổi giữa các model chỉ bằng cách thay đổi tham số `model`

Sự hợp nhất này giúp đơn giản hóa mã nguồn của bạn và giúp việc chuyển đổi giữa các mô hình AI trở nên dễ dàng.

---

## 2. Xác thực qua API Key[​](02-core-concepts.md#2-xác-thực-qua-api-key "Direct link to 2. Xác thực qua API Key")

Mọi yêu cầu gửi đến Gateway đều phải được xác thực bằng một API key. Key này phải được gửi trong header `Authorization` dưới dạng `Bearer` token.

**Ví dụ header:**

```
Authorization: Bearer <your_api_key>
```

Nếu API key bị thiếu hoặc không hợp lệ, hệ thống sẽ trả về lỗi `401 Unauthorized`.

---

## 3. Lựa chọn Model Linh hoạt[​](02-core-concepts.md#3-lựa-chọn-model-linh-hoạt "Direct link to 3. Lựa chọn Model Linh hoạt")

Bạn có thể truy cập hàng loạt mô hình AI từ các nhà cung cấp hàng đầu chỉ bằng cách thay đổi một tham số duy nhất: `model`.

**Ví dụ:** Để chuyển từ mô hình của OpenAI sang Google, bạn chỉ cần thay đổi giá trị của trường `model` trong body request.

* OpenAI Model
* Google Model

```
{
"model": "gemini-2.5-pro",
"messages": [
  { "role": "user", "content": "Hello from OpenAI!" }
]
}
```

```
{
"model": "gemini-2.5-pro",
"messages": [
  { "role": "user", "content": "Hello from Google!" }
]
}
```

Gateway sẽ tự động định tuyến yêu cầu của bạn đến nhà cung cấp tương ứng mà không yêu cầu bạn thay đổi bất kỳ logic nào khác.

---

## 4. Các Tham số Chung để Kiểm soát Kết quả[​](02-core-concepts.md#4-các-tham-số-chung-để-kiểm-soát-kết-quả "Direct link to 4. Các Tham số Chung để Kiểm soát Kết quả")

API của chúng tôi cung cấp các tham số chung giúp bạn kiểm soát đầu ra một cách nhất quán trên nhiều loại mô hình.

* **`prompt` hoặc `messages`**: Cung cấp đầu vào cho mô hình. `prompt` thường dùng cho các tác vụ đơn giản (như sinh ảnh), trong khi `messages` dùng cho các cuộc hội thoại có nhiều lượt.
* **`n`**: Chỉ định số lượng kết quả trả về. Ví dụ, `n: 2` trong API sinh ảnh sẽ tạo ra hai hình ảnh khác nhau từ cùng một `prompt`.
* **`response_format`**: Yêu cầu định dạng đầu ra cụ thể. Ví dụ, khi tạo ảnh, bạn có thể yêu cầu một URL (`"response_format": "url"`) hoặc dữ liệu ảnh mã hóa base64 (`"response_format": "b64_json"`).

---

## 5. Cấu trúc Phản hồi Nhất quán[​](02-core-concepts.md#5-cấu-trúc-phản-hồi-nhất-quán "Direct link to 5. Cấu trúc Phản hồi Nhất quán")

Dữ liệu trả về từ API luôn có cấu trúc JSON rõ ràng. Kết quả bạn cần thường nằm trong một trong hai trường sau:

* **`data`**: Một mảng các đối tượng kết quả. Thường được sử dụng cho các API trả về nhiều mục, như sinh ảnh hoặc âm thanh.
* **`choices`**: Một mảng các lựa chọn phản hồi. Thường được sử dụng trong các API sinh văn bản, nơi mỗi lựa chọn chứa một phiên bản hoàn thành văn bản.

Việc hiểu rõ các khái niệm này sẽ giúp bạn xây dựng ứng dụng một cách nhanh chóng và hiệu quả hơn trên nền tảng AI Thực chiến - API Gateway.