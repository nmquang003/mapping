# Atlas Việt — RAG có dẫn nguồn

RAG sử dụng bốn database trong `../data-catalog.json` (tính từ `atlas-viet/` là `../data-catalog.json`), đọc SQLite ở chế độ chỉ đọc. Không sửa database nguồn.

## Gói chạy độc lập

Gói `release/atlas-viet-rag.zip` gồm website, backend, bốn database, tư liệu JSON và chỉ mục 142 embedding thật. Không có API key. Giải nén toàn bộ, giữ cấu trúc, vào `atlas-viet/`, sao chép `.env.example` thành `.env`, điền key BTC rồi chạy `python3 run.py` (Windows: `python run.py`). Cần Python 3.10 trở lên; không cần cài thêm thư viện cho runtime. Có `launch.command` và `launch.bat` để khởi động.

Tạo lại gói sau khi sửa code/data: `python3 scripts/package_rag.py`. Script chỉ lấy danh sách file cho phép và kiểm tra không có key môi trường trong nội dung gói. Chỉ mục trong gói là dữ liệu sinh ra; ở repo nó vẫn được bỏ qua bởi Git.

## Chạy

Từ thư mục `chung-khao/atlas-viet/`, đặt `THUCCHIEN_API_KEY` hoặc `AITC_API_KEY` trong môi trường của backend. Không đưa key vào trình duyệt, mã nguồn hoặc chat.

```sh
python3 rag/server.py build-index
python3 rag/server.py serve --port 4322
```

Mở http://127.0.0.1:4322/. Máy chủ phục vụ cả website và API. Khi mở bản web tĩnh cũ tại cổng 4321 trên localhost, khung chat cũng kết nối tới backend 4322. Máy chủ 7860 và máy chủ web tĩnh 4321 không bị dừng.

`serve` kiểm tra và cập nhật chỉ mục trước khi phục vụ. Cache nằm ở `.rag/index.json`, được bỏ qua trong Git. Model, base URL và nội dung từng tư liệu được kiểm tra trước khi tái sử dụng vector; đổi model hoặc sửa nội dung cần embedding lại phần tương ứng. Muốn dùng bản database mới, tạo lại SQLite từ seed theo hướng dẫn của bộ dữ liệu rồi khởi động lại backend.

Backend dùng thư viện chuẩn Python; không yêu cầu cài SDK hoặc dịch vụ vector riêng. TLS luôn được xác minh; trên macOS dùng `/etc/ssl/cert.pem` nếu có.

## Model và API

Mặc định:

- Embedding: `text-multilingual-embedding-002`, 768 chiều, hỗ trợ tiếng Việt.
- Sinh văn bản: `deepseek-flash` (JSON mode, tắt thinking theo tài liệu BTC).
- Gateway: `https://api.thucchien.ai`. Lỗi 429 hoặc 5xx được thử lại tối đa hai lần với thời gian chờ tăng dần.
- Embedding gọi `/embeddings`; chat gọi `/v1/chat/completions` theo quy ước gateway trong `../AGENTS.md`.

Có thể cấu hình qua `ATLAS_EMBEDDING_MODEL`, `ATLAS_CHAT_MODEL`, `AITC_BASE_URL`. Danh sách chiều embedding lấy từ [tài liệu BTC](../../docs/thucchien-user-guide/markdown/09-embeddings.md). Chỉ gửi `model` và `input` cho embedding, `model` và `messages` cho chat; với DeepSeek thêm `response_format` JSON và `thinking` disabled được BTC tài liệu hóa. Với `gemini-embedding-2`, gửi từng đoạn riêng đúng lưu ý BTC.

## Kho tri thức và luồng xử lý

Bộ dữ liệu hiện tại tạo 142 tư liệu: 113 dữ kiện/tổng quan từ `chatbot_knowledge` và 29 hồ sơ `places`, có mô tả, điểm nổi bật, ghi chú giới hạn. Mọi tư liệu phải có nguồn trạng thái `source_checked`. Giá/lịch trong `dated_practical_info` không được đưa vào chỉ mục. Khóa tư liệu và nguồn gồm tiền tố địa phương, tránh trùng `F01`, `S01` giữa các bộ.

1. AI phân loại phạm vi, địa phương, địa danh và viết lại câu hỏi có ngữ cảnh.
2. Backend xác nhận các ID có trong danh mục; câu hỏi ngoài phạm vi/thiếu địa danh được từ chối hoặc yêu cầu làm rõ.
3. Embedding câu hỏi bằng cùng model lập chỉ mục; tính cosine, kết hợp mức trùng từ và ngữ cảnh địa danh. Lấy tối đa 8 tư liệu trong phạm vi đã xác nhận.
4. AI viết các câu trả lời gắn ID tư liệu hỗ trợ. Backend loại câu trả lời thiếu trích dẫn hoặc chứa ID không có trong kết quả truy xuất.
5. Một lượt AI thứ hai kiểm tra từng câu có được tư liệu được dẫn hỗ trợ và có giữ mốc thời gian hay không, đồng thời chọn tập tư liệu trích dẫn đủ và gọn nhất. Nếu không đạt, báo thiếu căn cứ.
6. Backend ánh xạ ID sang URL thật trong SQLite; AI không được tự tạo URL.

`ATLAS_MIN_SIMILARITY` mặc định `0.45`. Đây là ngưỡng khởi đầu, cần tiếp tục hiệu chỉnh theo bộ câu hỏi đánh giá. Lịch sử hội thoại tối đa 6 lượt dùng để giải tham chiếu, không được coi là nguồn tri thức.

Các kiểm tra trên không bảo đảm loại bỏ tuyệt đối mọi sai sót của mô hình. Chất lượng phụ thuộc dữ liệu nguồn, truy xuất và việc kiểm tra câu trả lời. `source_checked` không đồng nghĩa mọi dữ kiện đã được xác minh độc lập. Khi câu hỏi về thông tin thực dụng có thể thay đổi, bản này từ chối cung cấp như thông tin hiện hành; chưa có cơ chế tra cứu web trực tiếp.

## API

- `GET /api/status`: trạng thái chỉ mục, model, số tư liệu và phạm vi; không chứa API key.
- `POST /api/chat`: JSON gồm `question`, `dataset_id` (tùy chọn), `history` (tùy chọn).
- Kết quả: `status`, `answer`, `claims`, `sources`, `retrieved_record_ids`.
- Trạng thái nội dung: `answered`, `out_of_scope`, `insufficient_data`, `clarification`.
- Lỗi đầu vào: HTTP 400; origin không được phép: 403; quá 2 câu hỏi đồng thời: 429; API chưa sẵn sàng/lỗi: 503.

UI hiển thị nguồn cạnh từng câu, có thể mở danh sách nguồn, lưu ngữ cảnh hội thoại trong bộ nhớ trang. Phần trả lời được render bằng text node để không thực thi HTML do AI tạo. Nút hỏi Atlas trên thẻ địa danh điền câu hỏi và chọn địa phương; người dùng bấm Gửi.

Máy chủ chỉ bind `127.0.0.1`, phục vụ bản local. Khi triển khai công khai cần cấu hình reverse proxy/HTTPS, origin, xác thực và hạn mức phù hợp; không đưa trực tiếp máy chủ phát triển này lên Internet.

## Kiểm tra

```sh
python3 -m unittest discover -s rag -p 'test_*.py' -v
uv run --no-project --with playwright python scripts/check_rag.py
uv run --no-project --with playwright python scripts/check_rag.py --live
```

Unit test không gọi API thật. Browser test mặc định giả lập câu trả lời API, kiểm tra nguồn, render an toàn, lỗi API, ngữ cảnh địa danh và bố cục mobile. `--live` dùng backend 4322/API BTC thật và tiêu thụ hạn mức.
