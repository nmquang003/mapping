Nguồn: https://docs.thucchien.ai/docs/round-2/user-guide/rate-limits

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* [Hướng dẫn sử dụng API](00-overview.md)
* Giới hạn tốc độ (rate limit)

# Giới hạn tốc độ (rate limit)

Gateway giới hạn tốc độ gọi theo **đội**: mọi key của đội dùng chung một bộ đếm. Giới hạn tính trong cửa sổ trượt 60 giây. Vượt giới hạn, gateway trả lỗi `429`. Chờ vài giây rồi gọi lại (SDK `openai` tự thử lại 2 lần).

Giới hạn này khác với hết budget (`429 Budget has been exceeded`). Hết budget thì chờ không có tác dụng.

## Giới hạn chung của đội[​](12-rate-limits.md#giới-hạn-chung-của-đội "Direct link to Giới hạn chung của đội")

|  | Key chính thức | Key test |
| --- | --- | --- |
| Budget | $50 | $1 |
| Request mỗi phút (RPM), cộng mọi model | 300 | 20 |
| Token mỗi phút (TPM), cộng mọi model | 400.000 | 100.000 |
| Request song song mỗi key | 10 | 5 |

## Giới hạn riêng từng model[​](12-rate-limits.md#giới-hạn-riêng-từng-model "Direct link to Giới hạn riêng từng model")

Key chính thức có thêm giới hạn riêng cho các model dưới đây. Model không có trong bảng chỉ chịu giới hạn chung của đội.

| Model | Giới hạn mỗi đội |
| --- | --- |
| `gemini-2.5-pro`, `gemini-3.1-pro-preview` | 96.000 TPM |
| `gemini-3-pro-image`, `nano-banana-pro` | 48.000 TPM |
| `gemini-2.5-flash`, `gemini-3.1-flash-lite`, `gemini-3.5-flash`, `gemini-3.5-flash-lite`, `gemini-3.6-flash`, `gemini-3.7-flash`, `gemini-3.8-flash` | 384.000 TPM |
| `gpt-5.6-luna`, `gpt-6-luna`, `o4-mini` | 384.000 TPM |
| `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-6-sol`, `gpt-6.1-sol`, `gpt-6-astra` | 192.000 TPM |
| `o3` | 76.000 TPM |
| `gemini-2.5-flash-preview-tts`, `gemini-3.1-flash-tts-preview` | 158 RPM |
| `gemini-2.5-pro-preview-tts` | 132 RPM |
| `veo-3.1-generate-001`, `veo-3.1-fast-generate-001`, `veo-3.1-lite-generate-001` | 52 RPM |
| `gpt-image-2.5-flare`, `gpt-image-2.5-sunburst` | 4 RPM |
| `gemini-2.5-flash-image`, `gemini-3.1-flash-image`, `gemini-3.1-flash-lite-image`, `nano-banana`, `nano-banana-2`, `nano-banana-2-lite` | 60 RPM |

* Giới hạn chung vẫn áp dụng. Ví dụ đội dùng 300.000 token `gemini-3.8-flash` trong một phút thì chỉ còn 100.000 TPM cho mọi model khác.
* Xem giới hạn đang áp cho đội của bạn ở trang [Kiểm tra chi tiêu](https://docs.thucchien.ai/docs/round-2/api-reference/spend-checking): nhập key, khung kết quả liệt kê từng model và giới hạn của nó.

## Tránh bị 429[​](12-rate-limits.md#tránh-bị-429 "Direct link to Tránh bị 429")

* **Đặt `max_tokens` / `max_completion_tokens` vừa đủ.** Khi request bắt đầu, gateway giữ chỗ trước `token input + max_tokens`, rồi trả lại phần không dùng khi request xong. Với model Pro (96.000 TPM), một request đặt `max_tokens` 65.536 chiếm gần hết giới hạn của phút đó.
* **Dùng model Flash cho phần lớn công việc**, chỉ gọi model Pro khi thật cần.
* **Không bắn quá nhiều request song song.** Mỗi key chạy tối đa 10 request cùng lúc. Dùng hàng đợi và retry với exponential backoff.
* Ảnh OpenAI (`gpt-image-*`) chỉ 4 request/phút. Tạo nhiều ảnh thì dùng `nano-banana-2` hoặc `nano-banana-2-lite`.