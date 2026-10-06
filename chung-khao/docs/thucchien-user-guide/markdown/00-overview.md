Nguồn: https://docs.thucchien.ai/docs/user-guide

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* Hướng dẫn sử dụng API

# Hướng dẫn sử dụng API

Hướng dẫn chi tiết cách tương tác với các mô hình AI thông qua LiteLLM Proxy.

[## 📄️ Giới thiệu

Chào mừng bạn đến với tài liệu hướng dẫn sử dụng AI Thực Chiến gateway. Tài liệu này sẽ cung cấp cho bạn mọi thông tin cần thiết để tích hợp các mô hình Trí tuệ nhân tạo (AI) mạnh mẽ vào ứng dụng của bạn chỉ với một API key duy nhất.](01-introduction.md)

[## 📄️ Các khái niệm cốt lõi

---](02-core-concepts.md)

[## 📄️ Sinh văn bản (Text Generation)

Các mô hình sinh văn bản cho phép bạn thực hiện nhiều tác vụ như trả lời câu hỏi, viết nội dung, tóm tắt văn bản, và nhiều hơn nữa. API này tuân theo chuẩn của OpenAI, vì vậy bạn có thể sử dụng các thư viện client của OpenAI một cách trực tiếp.](03-text-generation.md)

[## 📄️ Sinh hình ảnh (Image Generation)

AI cung cấp hai phương pháp để tạo hình ảnh từ mô tả văn bản (prompt), tùy thuộc vào mô hình bạn sử dụng.](04-image-generation.md)

[## 📄️ Sinh video với Veo 3.1 (Quy trình bất đồng bộ)

Việc tạo video là một tác vụ tốn nhiều tài nguyên và thời gian. Do đó, tương tác với mô hình Veo không diễn ra ngay lập tức mà theo một quy trình bất đồng bộ (asynchronous) gồm 3 bước. API tuân theo chuẩn OpenAI Videos API, nên bạn dùng được thư viện openai và header Authorization: Bearer như các API khác.](05-video-generation-veo3.md)

[## 📄️ Chuyển văn bản thành giọng nói (Text-to-Speech)

Các mô hình Text-to-Speech (TTS) cho phép bạn chuyển đổi một đoạn văn bản thành file âm thanh có giọng nói tự nhiên.](06-text-to-speech.md)

[## 📄️ Chuyển giọng nói thành văn bản (Speech-to-Text)

Mô hình Speech-to-Text (STT) nhận một file âm thanh và trả về nội dung lời nói dưới dạng văn bản, hỗ trợ tiếng Việt.](07-speech-to-text.md)

[## 📄️ Tìm kiếm web (Google Search grounding)

Mặc định, model chỉ biết thông tin đến thời điểm được huấn luyện. Bật tìm kiếm web thì model tự tạo truy vấn, tìm trên Internet rồi trả lời dựa trên kết quả mới nhất, kèm danh sách nguồn. Tính năng này hợp với câu hỏi về tin tức, giá cả, lịch thi đấu hay số liệu mới.](08-google-search-grounding.md)

[## 📄️ Embedding

Embedding biến một đoạn văn bản thành một vector số, dùng cho tìm kiếm ngữ nghĩa, RAG, phân cụm hay so sánh độ giống nhau giữa các câu. Gọi qua endpoint /embeddings, cùng base\_url và API key như các trang trước.](09-embeddings.md)

[## 📄️ Model OpenAI và DeepSeek

Ngoài Gemini, gateway còn cung cấp model của OpenAI và DeepSeek. Cách gọi y hệt các trang trước//api.thucchien.ai", cùng API key, chỉ cần đổi model.](10-openai-deepseek.md)

[## 📄️ Bảng giá model

Giá tính bằng USD, là mức gateway dùng để trừ budget của key. /1M nghĩa là trên 1 triệu token. Bạn xem chi phí từng request trong header x-litellm-response-cost hoặc trên trang quản lý key.](11-pricing.md)

[## 📄️ Giới hạn tốc độ (rate limit)

Gateway giới hạn tốc độ gọi theo đội: mọi key của đội dùng chung một bộ đếm. Giới hạn tính trong cửa sổ trượt 60 giây. Vượt giới hạn, gateway trả lỗi 429. Chờ vài giây rồi gọi lại (SDK openai tự thử lại 2 lần).](12-rate-limits.md)

[## 📄️ Tham khảo

Tài liệu của chúng tôi cung cấp mọi thứ bạn cần để tích hợp AI Thực Chiến gateway vào ứng dụng của mình.](13-references.md)

[Previous

Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)[Next

Giới thiệu](01-introduction.md)