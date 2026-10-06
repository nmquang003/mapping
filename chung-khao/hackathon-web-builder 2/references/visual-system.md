# Hệ thống thị giác

Dùng tài liệu này khi thiết lập hoặc tinh chỉnh typography, spacing, màu, border, radius, shadow và hierarchy của website.

## 1. Type scale

Dùng scale có chủ đích. Một baseline thực tế:

- Display / hero: `clamp(3rem, 7vw, 6.5rem)`
- H1 page title: `clamp(2.5rem, 5vw, 5rem)`
- H2 section: `clamp(2rem, 3.5vw, 3.5rem)`
- H3 subsection: `1.35-1.75rem`
- Lead/body lớn: `1.1-1.3rem`
- Body: `0.98-1.08rem`
- Small/meta: `0.78-0.9rem`

Không dùng toàn bộ scale một cách máy móc. Chỉ chọn các level thật sự cần.

### Line-height

- Display lớn: `0.9-1.05`
- Section heading: `1.0-1.15`
- Body sans: `1.5-1.7`
- Body serif: `1.6-1.85`
- Metadata nhỏ: `1.3-1.5`

### Tracking

- Display lớn có thể dùng tracking âm nhẹ.
- Uppercase label nếu thực sự cần thì tăng tracking.
- Body text thường giữ gần mặc định.
- Với tiếng Việt, không siết tracking quá mạnh vì dấu dễ bị bí và khó đọc.

### Weight

Các role thường dùng:

- Body: 400-450
- Emphasis: 500
- Section heading: 500-650
- Hero: tùy cá tính font

Không biến toàn bộ UI thành 600-700.

### Lưu ý font tiếng Việt

- Kiểm tra đủ glyph tiếng Việt ở mọi weight đang dùng.
- Test các từ nhiều dấu ở size lớn.
- Tránh font có dấu đặt quá cao/thấp hoặc bị vỡ ở italic/bold.
- Heading tiếng Việt thường dài hơn tiếng Anh; kiểm soát wrap bằng width/size/copy thay vì ép xuống quá nhỏ.

## 2. Spacing system

Dùng token set nhỏ. Ví dụ base 8px:

- 4px optical micro-gap
- 8px
- 12px
- 16px
- 24px
- 32px
- 48px
- 64px
- 96px
- 128px
- 160px

Dùng spacing để thể hiện quan hệ ngữ nghĩa:

- Label -> heading: nhỏ.
- Heading -> paragraph: vừa.
- Paragraph -> CTA: vừa-lớn.
- Nhóm nội dung khác nhau: lớn.
- Ranh giới section chính: rất lớn.

Không dùng cùng một vertical gap cho mọi element.

## 3. Alignment

Chọn alignment anchors rõ:

- Main page grid.
- Cạnh text column.
- Cạnh media.
- Cạnh section title.

Một trang tinh thường đẹp vì nhiều element ở xa nhau vẫn cùng nằm trên các guide vô hình.

Chỉ dùng center alignment có chủ đích. Nội dung dài hoặc giàu thông tin thường hợp left-align hơn.

## 4. Grid

Grid desktop thường dùng:

- 12-column editorial grid cho asymmetry linh hoạt.
- 8-column grid cho trang vừa phức tạp.
- 2-column split cho storytelling tập trung.

Giữ gutter nhất quán. Không đổi logic grid ngẫu nhiên giữa các section.

Cho phép một số element phá grid có chủ đích, ví dụ hero media hoặc pull quote.

## 5. Color

Xây màu theo role thay vì theo từng hex rời rạc.

Cấu trúc palette gợi ý:

- Background neutral.
- Secondary surface neutral.
- Primary text.
- Muted text.
- Hairline border.
- Primary accent.
- Accent hover/pressed.

Nếu phù hợp, dùng neutral có hue nhẹ: ivory ấm thay vì trắng tinh, navy-black thay vì đen tuyệt đối, stone gray thay vì gray trung tính.

Không dùng muted text quá nhạt chỉ vì trông “soft”.

## 6. Border radius

Chọn một personality:

### Sharp editorial
- 0-4px

### Refined modern
- 8-16px

### Friendly / playful
- 16-28px

### Pill
- Chỉ dành cho chip, filter, compact control hoặc khi brand language thực sự cần.

Không trộn 4px, 12px, 20px, 32px và 999px khắp trang mà không có lý do chức năng.

## 7. Border

Dùng border để phân tách/tổ chức, không để trang trí mọi object.

Lựa chọn tốt:

- Hairline neutral border.
- Editorial rule.
- Accent underline.
- Section divider.

Nếu trang có nhiều card, thường sẽ đẹp hơn khi bỏ border/shadow ở một phần card.

## 8. Shadow

Dùng tiết chế.

Hợp lý cho:

- Floating nav trên media.
- Modal/popover.
- Một card thật sự cần elevation.

Không đặt cùng một box-shadow cho mọi card.

Với aesthetic editorial/cultural/brutalist, không shadow có thể tốt hơn.

## 9. Surface hierarchy

Không tạo 5 sắc xám gần giống nhau.

Thường chỉ cần:

- Page background.
- Secondary section surface.
- Elevated interactive surface.

Ba tầng thường đã đủ.

## 10. Contrast hierarchy

Không để mọi thứ đều đậm như nhau.

Dùng tier:

- Primary content: mạnh nhất.
- Supporting content: vừa.
- Metadata/caption: nhẹ hơn nhưng vẫn đọc được.
- Disabled/deemphasized: rõ ràng là phụ.

## 11. Optical refinement

Sau khi căn bằng số, nhìn bằng mắt lần nữa.

Các correction thường gặp:

- Icon có thể cần chỉnh 1-2px theo chiều dọc so với text.
- Icon tròn thường trông nhỏ hơn icon vuông cùng box-size.
- Display type lớn có thể cần gap trên/dưới chặt hơn bounding box.
- Button text đôi khi cần compensation nhẹ tùy font metrics.
- Logo hiếm khi trông cân chỉ bằng geometric center.

Ưu tiên thứ nhìn cân hơn thứ mathematically equal.
