Nguồn: https://docs.thucchien.ai/docs/round-2/user-guide/text-to-speech

* [Vòng Chung Khảo](https://docs.thucchien.ai/docs/round-2)
* [Hướng dẫn sử dụng API](00-overview.md)
* Chuyển văn bản thành giọng nói (Text-to-Speech)

# Chuyển văn bản thành giọng nói (Text-to-Speech)



Các mô hình Text-to-Speech (TTS) cho phép bạn chuyển đổi một đoạn văn bản thành file âm thanh có giọng nói tự nhiên.

**Các model được hỗ trợ** (Gemini Enterprise Agent Platform (trước đây là Vertex AI)):

* `gemini-3.1-flash-tts-preview`
* `gemini-2.5-flash-preview-tts`
* `gemini-2.5-pro-preview-tts`

**Model OpenAI:** `gpt-4o-mini-tts`. Model này dùng giọng của OpenAI (`alloy`, `nova`…) thay vì giọng Gemini, xem [Model OpenAI và DeepSeek](10-openai-deepseek.md#%C3%A2m-thanh).

**Endpoint:** `POST /audio/speech`

* curl
* Python (requests)
* Python (openai)

Cách này cho phép bạn nhanh chóng tạo và lưu file âm thanh.

```
curl https://api.thucchien.ai/audio/speech \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_api_key>" \
-d '{
  "model": "gemini-2.5-flash-preview-tts",
  "input": "Xin chào, đây là một thử nghiệm chuyển văn bản thành giọng nói qua [AI Thực Chiến](https://thucchien.ai) gateway.",
  "voice": "Zephyr"
}' \
--output speech_output.mp3
```

Kết quả bạn sẽ có file audio như sau:

Your browser does not support the audio element.

Cách này cho bạn quyền kiểm soát việc lưu file.

```
import requests

# --- Cấu hình ---
AI_API_BASE = "https://api.thucchien.ai"
AI_API_KEY = "sk-1234" # Thay bằng API key của bạn

# --- Thực thi ---
url = f"{AI_API_BASE}/audio/speech"
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {AI_API_KEY}"
}
data = {
  "model": "gemini-2.5-pro-preview-tts",
  "input": "Hello world! This is a test of the text-to-speech API.",
  "voice": "Puck"
}

response = requests.post(url, headers=headers, json=data, stream=True)

if response.status_code == 200:
  with open("speech_from_requests.mp3", "wb") as f:
      for chunk in response.iter_content(chunk_size=8192):
          f.write(chunk)
  print("File âm thanh đã được tạo thành công!")
else:
  print(f"Error: {response.status_code}")
  print(response.text)
```

Kết quả bạn sẽ có file audio như sau:

Your browser does not support the audio element.

Thư viện `openai` cung cấp một giao diện rất sạch sẽ cho tác vụ này.

```
from openai import OpenAI
from pathlib import Path

# --- Cấu hình ---
AI_API_BASE = "https://api.thucchien.ai"
AI_API_KEY = "sk-1234" # Thay bằng API key của bạn

# --- Thực thi ---
client = OpenAI(
  api_key=AI_API_KEY,
  base_url=AI_API_BASE
)

speech_file_path = Path(__file__).parent / "speech_from_openai.mp3"

response = client.audio.speech.create(
model="gemini-2.5-flash-preview-tts",
voice="Charon",
input="Hôm nay là một ngày đẹp trời để lập trình."
)

response.stream_to_file(speech_file_path)
print(f"File âm thanh đã được lưu tại: {speech_file_path}")
```

Kết quả bạn sẽ có file audio như sau:

Your browser does not support the audio element.

## Các tham số tùy chọn[​](06-text-to-speech.md#các-tham-số-tùy-chọn "Direct link to Các tham số tùy chọn")

Ngoài `model`, `input`, và `voice`, bạn có thể sử dụng thêm các tham số khác để tinh chỉnh giọng nói, tốc độ, và định dạng âm thanh đầu ra.

Để biết danh sách đầy đủ các tham số và cách sử dụng, vui lòng tham khảo tài liệu chính thức tại đây: [Google Cloud Text-to-Speech Documentation](https://cloud.google.com/text-to-speech/docs/gemini-tts#examples)