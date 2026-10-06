# Prompt mẫu

Điền trường trong ngoặc nhọn bằng dữ liệu thật; không gửi placeholder. Có thể dùng tiếng Anh cho hình ảnh; giữ lời thoại Việt đúng nguyên văn khi có chữ.

## Đổi màu trang có sẵn

```text
TASK: Color-only edit of input image 1.
REFERENCE ROLES:
Image 1 = authoritative linework, character identity, geometry, panel layout and lettering.
{List other attached images in actual input order and state each role. Omit absent references.}

PRESERVE:
Keep original ink contours, line weight, facial features, apparent ages, body proportions, expressions, poses, hands, objects, camera angles, panel borders, speech balloons and composition. Preserve all existing Vietnamese lettering verbatim. Do not adopt another artist's drawing style or redesign the characters.

CHANGE ONLY COLOR:
Use fresh flat graphic-comic colors, selective medium-to-high saturation, clear value separation, restrained one- or two-step cel shadows and small highlights. Use light quiet backgrounds. Keep Minh's shirt yellow and Huy's shirt blue. Keep natural skin tones. Use {scene palette and emotional intent}. Avoid all-over neon, cinematic teal-orange grading, heavy gradients, glossy airbrushed skin, bloom and 3D rendering.

OUTPUT:
One complete page with original aspect ratio and crop. No new captions, decoration or extra panels. If a color reference is attached, use its color relationships only, never its faces, poses or layout.
```

## Trang mới, chữ tách riêng

```text
Create page {number} of an original Vietnamese comic.
Use attached approved character sheets for identity and line quality.
Use approved color sample only for palette, flat fills and shading.
Keep drawing style and adult/student proportions of the character references.
PAGE: {aspect ratio, panel layout, margins, gutters, reading order}.
CONTINUITY: {room anchors, clothing, props, time}.
COLOR: {palette, character colors, background values, focal accent}.
PANEL 1: {camera, action, emotion, subjects, reserved balloon area}.
PANEL 2: {...}.
{Continue for actual panel count.}
Do not render text, letters, numbers, logos, interface text or sound effects.
Leave specified negative space for editable lettering; do not fill it with detail.
Keep every panel's action clear and character identities consistent.
```

## Sửa cục bộ

```text
Edit only {precise region or panel} in supplied page.
Fix {one concrete defect} using {specified reference} as authority.
Preserve the rest, character identities, approved palette, framing and lettering. Do not regenerate or redesign unrelated panels.
```

## Dữ liệu chữ tách riêng

Lưu cùng dự án:

```json
{
  "page": 2,
  "canvas_ratio": "2:3",
  "items": [
    {
      "id": "p2-panel1-huy-01",
      "panel": 1,
      "type": "dialogue",
      "speaker": "Huy",
      "text": "Mai học tiết đầu đấy. Ngủ chưa?",
      "box": {"x": 0.06, "y": 0.09, "w": 0.29, "h": 0.08},
      "tail_target": {"x": 0.22, "y": 0.28}
    }
  ]
}
```

Tọa độ chỉ minh họa schema, chưa được đo. Dùng gốc trên trái, chuẩn hóa theo toàn trang. Đo lại khi có tranh; điều chỉnh balloon theo text thật, không ép chữ vào vị trí mẫu.
