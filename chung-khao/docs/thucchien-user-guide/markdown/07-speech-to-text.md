Nguồn: https://docs.thucchien.ai/docs/round-2/user-guide/speech-to-text

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* [Hướng dẫn sử dụng API](00-overview.md)
* Chuyển giọng nói thành văn bản (Speech-to-Text)

# Chuyển giọng nói thành văn bản (Speech-to-Text)



Mô hình Speech-to-Text (STT) nhận một file âm thanh và trả về nội dung lời nói dưới dạng văn bản, hỗ trợ tiếng Việt.

**Model được hỗ trợ** (Gemini Enterprise Agent Platform (trước đây là Vertex AI)):

* `gemini-3.5-transcribe-preview`

**Model OpenAI:** `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `gpt-transcribe`, `whisper-1`. Riêng `gpt-transcribe` phải gửi `response_format=json`, xem [Model OpenAI và DeepSeek](10-openai-deepseek.md#%C3%A2m-thanh).

**Endpoint:** `POST /audio/transcriptions`

Request gửi dạng `multipart/form-data` (upload file), không phải JSON.

* curl
* Python (requests)
* Python (openai)

```
curl https://api.thucchien.ai/audio/transcriptions \
-H "Authorization: Bearer <your_api_key>" \
-F model=gemini-3.5-transcribe-preview \
-F file=@speech.mp3
```

```
import requests

# --- Cấu hình ---
AI_API_BASE = "https://api.thucchien.ai"
AI_API_KEY = "sk-1234" # Thay bằng API key của bạn

# --- Thực thi ---
with open("speech.mp3", "rb") as f:
  response = requests.post(
      f"{AI_API_BASE}/audio/transcriptions",
      headers={"Authorization": f"Bearer {AI_API_KEY}"},
      data={"model": "gemini-3.5-transcribe-preview"},
      files={"file": ("speech.mp3", f, "audio/mpeg")},
  )

if response.status_code == 200:
  print(response.json()["text"])
else:
  print(f"Error: {response.status_code}")
  print(response.text)
```

```
from openai import OpenAI

# --- Cấu hình ---
AI_API_BASE = "https://api.thucchien.ai"
AI_API_KEY = "sk-1234" # Thay bằng API key của bạn

# --- Thực thi ---
client = OpenAI(
  api_key=AI_API_KEY,
  base_url=AI_API_BASE
)

with open("speech.mp3", "rb") as audio_file:
  transcript = client.audio.transcriptions.create(
      model="gemini-3.5-transcribe-preview",
      file=audio_file,
  )

print(transcript.text)
```

Kết quả trả về là JSON, nội dung lời nói nằm trong trường `text`:

```
{
  "text": "Xin chào các đội thi.",
  "usage": {
    "type": "tokens",
    "input_tokens": 51,
    "output_tokens": 6,
    "total_tokens": 57
  },
  "task": "transcribe"
}
```

Kết hợp với Text-to-Speech

Bạn có thể dùng file âm thanh sinh ra từ [Text-to-Speech](06-text-to-speech.md) để thử nhanh endpoint này.