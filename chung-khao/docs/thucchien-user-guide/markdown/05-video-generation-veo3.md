Nguồn: https://docs.thucchien.ai/docs/round-2/user-guide/video-generation-veo3

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* [Hướng dẫn sử dụng API](00-overview.md)
* Sinh video với Veo 3.1 (Quy trình bất đồng bộ)

# Sinh video với Veo 3.1 (Quy trình bất đồng bộ)



Việc tạo video là một tác vụ tốn nhiều tài nguyên và thời gian. Do đó, tương tác với mô hình Veo không diễn ra ngay lập tức mà theo một quy trình bất đồng bộ (asynchronous) gồm 3 bước. API tuân theo chuẩn [OpenAI Videos API](https://platform.openai.com/docs/api-reference/videos), nên bạn dùng được thư viện `openai` và header `Authorization: Bearer` như các API khác.

**Model được hỗ trợ** (Gemini Enterprise Agent Platform (trước đây là Vertex AI)):

* `veo-3.1-generate-001`: chất lượng cao nhất, $0.40 / giây video
* `veo-3.1-fast-generate-001`: nhanh hơn, $0.10 / giây video (720p), $0.12 / giây (1080p)
* `veo-3.1-lite-generate-001`: rẻ nhất, $0.05 / giây video (720p)

Chi phí

Video được tính tiền theo số giây ngay khi tác vụ được tạo, kể cả khi bạn không tải video về. Không gửi `seconds` thì video dài 8 giây. Hãy thử prompt với `veo-3.1-lite-generate-001` và `"seconds": "4"` trước khi dùng model đắt hơn.

## Tổng quan quy trình[​](05-video-generation-veo3.md#tổng-quan-quy-trình "Direct link to Tổng quan quy trình")

1. **Bắt đầu tác vụ:** Gửi `POST /v1/videos` chứa mô tả (prompt). API trả về `id` của video để bạn theo dõi.
2. **Kiểm tra trạng thái:** Gửi `GET /v1/videos/{id}` lặp lại cho đến khi `status` là `completed` (hoặc `failed`).
3. **Tải video:** Gửi `GET /v1/videos/{id}/content` để tải file mp4.

## Hướng dẫn chi tiết[​](05-video-generation-veo3.md#hướng-dẫn-chi-tiết "Direct link to Hướng dẫn chi tiết")

* curl (Từng bước)
* Python (OpenAI SDK)

#### Bước 1: Bắt đầu tạo video

```
curl -X POST https://api.thucchien.ai/v1/videos \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_api_key>" \
-d '{
  "model": "veo-3.1-lite-generate-001",
  "prompt": "A cinematic shot of a hummingbird flying in slow motion",
  "seconds": "4",
  "size": "1280x720"
}'
```

Nếu thành công, API sẽ trả về một JSON chứa `id` của video. Hãy lưu lại giá trị này.

```
{
"id": "video_bGl0ZWxsbTpjdXN0b21fbGxtX3Byb3ZpZGVy...",
"object": "video",
"status": "processing",
"created_at": 1790159271,
"model": "veo-3.1-lite-generate-001"
}
```

#### Bước 2: Kiểm tra trạng thái

```
curl https://api.thucchien.ai/v1/videos/<video_id> \
-H "Authorization: Bearer <your_api_key>"
```

Lặp lại yêu cầu này (ví dụ 10 giây một lần) cho đến khi response có `"status": "completed"`. Video 4–8 giây thường mất từ 30 giây đến vài phút.

```
{
"id": "video_bGl0ZWxsbTpjdXN0b21fbGxtX3Byb3ZpZGVy...",
"object": "video",
"status": "completed",
"created_at": 1790159271,
"model": "veo-3.1-lite-generate-001"
}
```

#### Bước 3: Tải video

```
curl https://api.thucchien.ai/v1/videos/<video_id>/content \
-H "Authorization: Bearer <your_api_key>" \
--output my_generated_video.mp4
```

Kết quả bạn sẽ có file video như sau:

[

Your browser does not support the video tag.

](../assets/87c79439b948.mp4)

Kịch bản dưới đây tự động hóa cả 3 bước bằng thư viện `openai` (`pip install openai`).

```
import time
from openai import OpenAI

client = OpenAI(
  api_key="<your_api_key>",
  base_url="https://api.thucchien.ai",
)

# Bước 1: bắt đầu tạo video
video = client.videos.create(
  model="veo-3.1-lite-generate-001",
  prompt="A cat playing with a ball of yarn in a sunny garden",
  seconds="4",
  size="1280x720",
)
print("Đã tạo:", video.id)

# Bước 2: kiểm tra trạng thái tới khi xong
while video.status not in ("completed", "failed"):
  time.sleep(10)
  video = client.videos.retrieve(video.id)
  print("Trạng thái:", video.status)

if video.status == "failed":
  raise SystemExit(f"Tạo video thất bại: {video.error}")

# Bước 3: tải video
content = client.videos.download_content(video.id)
content.write_to_file("my_generated_video.mp4")
print("Đã lưu my_generated_video.mp4")
```

## Tạo video từ ảnh (image-to-video)[​](05-video-generation-veo3.md#tạo-video-từ-ảnh-image-to-video "Direct link to Tạo video từ ảnh (image-to-video)")

Gửi thêm ảnh khởi đầu qua trường `input_reference`. Khi có file, request phải ở dạng `multipart/form-data` thay vì JSON.

* curl
* Python (OpenAI SDK)

```
curl -X POST https://api.thucchien.ai/v1/videos \
-H "Authorization: Bearer <your_api_key>" \
-F model=veo-3.1-lite-generate-001 \
-F prompt="The camera slowly zooms in while leaves drift in the wind" \
-F seconds=4 \
-F size=1280x720 \
-F input_reference=@start.png
```

```
video = client.videos.create(
  model="veo-3.1-lite-generate-001",
  prompt="The camera slowly zooms in while leaves drift in the wind",
  seconds="4",
  size="1280x720",
  input_reference=open("start.png", "rb"),
)
```

Bước 2 và 3 giống như trên.

## Các tham số[​](05-video-generation-veo3.md#các-tham-số "Direct link to Các tham số")

| Tham số | Giá trị | Mặc định |
| --- | --- | --- |
| `model` | `veo-3.1-generate-001`, `veo-3.1-fast-generate-001`, `veo-3.1-lite-generate-001` | bắt buộc |
| `prompt` | Mô tả video | bắt buộc |
| `seconds` | `"4"`, `"6"`, `"8"` | `"8"` |
| `size` | `"1280x720"`, `"1920x1080"` (16:9), `"720x1280"`, `"1080x1920"` (9:16) | `"1280x720"` |
| `input_reference` | File ảnh khởi đầu (multipart) | không có |

Mẹo viết prompt cho Veo, xem [hướng dẫn của Google](https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide).