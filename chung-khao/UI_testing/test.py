from openai import OpenAI
import base64

# --- Cấu hình ---
AI_API_BASE = "https://api.thucchien.ai/v1"
AI_API_KEY = "<your_api_key>"

# --- Khởi tạo client ---
client = OpenAI(
  api_key=AI_API_KEY,
  base_url=AI_API_BASE
)

# --- Gọi API để tạo hình ảnh ---
response = client.images.generate(
  model="nano-banana-2",
  prompt="An astronaut riding a horse on Mars, photorealistic",
  extra_body={"aspect_ratio": "16:9"},
)

# --- Xử lý và lưu từng ảnh ---
for i, image_obj in enumerate(response.data):
  b64_data = image_obj.b64_json
  image_data = base64.b64decode(b64_data)
  
  save_path = f"generated_image_{i+1}.png"
  with open(save_path, 'wb') as f:
      f.write(image_data)
  print(f"Image saved to {save_path}")