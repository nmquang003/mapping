Nguồn: https://docs.thucchien.ai/docs/round-2/user-guide/references

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* [Hướng dẫn sử dụng API](00-overview.md)
* Tham khảo

# Tham khảo

Tài liệu của chúng tôi cung cấp mọi thứ bạn cần để tích hợp [AI Thực Chiến](https://thucchien.ai) gateway vào ứng dụng của mình.

Tuy nhiên, để hiểu sâu hơn về công nghệ nền tảng hoặc các khả năng của từng mô hình AI cụ thể, bạn có thể tham khảo tài liệu chính thức từ các nhà phát triển.

## LiteLLM[​](13-references.md#litellm "Direct link to LiteLLM")

* **[Tài liệu chính thức của LiteLLM](https://docs.litellm.ai/docs/)**: Nguồn thông tin toàn diện về công nghệ proxy đang được sử dụng, bao gồm các tính năng nâng cao như caching, fallbacks, và virtual keys.
* **[Hỗ trợ API của OpenAI trên LiteLLM](https://docs.litellm.ai/docs/providers/openai)**: Chi tiết về cách LiteLLM triển khai và hỗ trợ các endpoint theo chuẩn OpenAI.
* **[Reasoning content trên LiteLLM](https://docs.litellm.ai/docs/reasoning_content)**: Cách LiteLLM chuyển `reasoning_effort` tới từng nhà cung cấp và trả về phần suy nghĩ.

## Google[​](13-references.md#google "Direct link to Google")

* **[Tài liệu Google AI Gemini API](https://ai.google.dev/docs/gemini_api_overview)**: Tài liệu chính thức từ Google về cách sử dụng các mô hình Gemini.
* **[Tài liệu Gemini Enterprise Agent Platform (trước đây là Vertex AI)](https://cloud.google.com/vertex-ai/docs)**: Nền tảng host Gemini, Veo và embedding trên Google Cloud.
* **[Grounding with Google Search](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/grounding-with-google-search)**: Cách Gemini tìm kiếm web và quy định hiển thị kết quả.
* **[Bảng giá Agent Platform](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing)**: Giá gốc của Gemini, Veo, embedding và grounding.

## OpenAI[​](13-references.md#openai "Direct link to OpenAI")

* **[Tài liệu API OpenAI](https://platform.openai.com/docs)**: Tài liệu chính thức cho các model `gpt-*`, `o3`, `o4-mini`, `gpt-image-*`, TTS, STT và embedding.
* **[Reasoning models](https://platform.openai.com/docs/guides/reasoning)**: Cách dùng `reasoning_effort` và giới hạn token cho model reasoning.
* **[API reference: Chat Completions](https://platform.openai.com/docs/api-reference/chat/create)**: Đặc tả tham số `reasoning_effort`, `max_completion_tokens` (thay cho `max_tokens`, bắt buộc với `gpt-6*`).
* **[API reference: Responses](https://platform.openai.com/docs/api-reference/responses/create)**: Đặc tả `reasoning.effort` và `max_output_tokens`.
* **[Web search](https://platform.openai.com/docs/guides/tools-web-search)**: Tìm kiếm web qua Responses API.

## DeepSeek[​](13-references.md#deepseek "Direct link to DeepSeek")

* **[Tài liệu API DeepSeek](https://api-docs.deepseek.com/)**: Tài liệu chính thức cho các model DeepSeek.
* **[Thinking mode](https://api-docs.deepseek.com/guides/thinking_mode)**: Bật/tắt chế độ suy nghĩ và đọc `reasoning_content`.
* **[Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing/)**: Giá và tên model DeepSeek (`deepseek-flash` thay cho các tên cũ `deepseek-v4-flash`, `deepseek-v4-flash-vision-exp`).

Việc tham khảo các tài liệu này sẽ giúp bạn tận dụng tối đa sức mạnh của từng mô hình và giải quyết các vấn đề phức tạp hơn.