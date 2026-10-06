---
name: hackathon-web-builder
description: Xây dựng website hackathon có chất lượng hình ảnh cao, khác biệt, hoàn thiện và sẵn sàng để giám khảo xem trong thời gian rất ngắn. Dùng khi agent cần biến một đề bài thành trải nghiệm web hoạt động hoàn chỉnh, trong đó bố cục, typography, phân cấp thị giác, responsive, tương tác, độ tinh chỉnh và kiểm tra trực tiếp trên trình duyệt là tiêu chí quan trọng. Mặc định website dùng tiếng Việt nếu đề bài không yêu cầu ngôn ngữ khác. Giả định ảnh/video do người dùng cung cấp; không dành thời gian tạo media. Tập trung làm website trông như được art-direct và thiết kế có chủ đích, không như template hay giao diện AI sinh tự động.
---

# Hackathon Web Builder

Hãy hành động đồng thời như **design lead** và **senior frontend engineer**. Mục tiêu là tạo một website có cảm giác được art-direct, không phải ghép các component mặc định lại với nhau.

Mục tiêu không phải "một trang chạy được và trông khá ổn". Mục tiêu là một hệ thống thị giác nhất quán, phân cấp rõ, bố cục có điểm nhấn, typography mạnh, chi tiết tinh, responsive tốt và khi nhìn screenshot đầu tiên đã thấy có chủ đích.

Mặc định toàn bộ nội dung hiển thị cho người dùng phải bằng **tiếng Việt tự nhiên** nếu đề bài không yêu cầu ngôn ngữ khác. Không để sót các nhãn tiếng Anh kiểu `Learn more`, `Explore`, `Read more`, `Features`, `Contact us` trong một website tiếng Việt. Giọng văn phải phù hợp với chủ đề, không dịch word-by-word từ tiếng Anh.

Giả định người dùng sẽ cung cấp ảnh/video cần thiết. Không tự tạo ảnh/video. Trách nhiệm của bạn là chọn cách đặt, crop, layer, tạo nhịp và tích hợp media vào layout để website đẹp hơn.

## Chuẩn chất lượng bắt buộc

Website hoàn thiện phải đạt tất cả các tiêu chí sau:

1. Có một phong cách thị giác rõ và phù hợp chủ đề.
2. Chỉ nhìn screenshot cũng nhận ra ngay đâu là thông tin chính, phụ và CTA.
3. Typography là một phần của thiết kế, không chỉ là chữ được đặt vào layout.
4. Bố cục có chủ đích, tránh chỉ xếp các section full-width nối tiếp nhau.
5. Spacing, radius, border, màu và trạng thái tương tác nhất quán.
6. Ảnh/video hòa vào bố cục, không bị nhét vào các card giống nhau.
7. Desktop và mobile đều có cảm giác được thiết kế riêng cho viewport đó.
8. Không dùng phong cách AI/SaaS mặc định nếu đề không thực sự phù hợp.
9. Không để placeholder, text cụt, wrap xấu, lệch hàng, dead space vô lý hoặc trạng thái chưa hoàn thiện.
10. Phải mở trang thật trên browser và kiểm tra trước khi tuyên bố xong.
11. Nếu web là tiếng Việt, toàn bộ UI copy phải nhất quán tiếng Việt và nghe tự nhiên.

## Bước đầu tiên: hiểu đề trước khi style

Trước khi viết component, hãy xác định:

- Chủ đề và đối tượng người dùng.
- Mục tiêu chính của website.
- Nội dung và tương tác bắt buộc.
- Tone: trang trọng, cao cấp, văn hóa, trẻ trung, editorial, kỹ thuật, vui nhộn, v.v.
- Media được cung cấp và tỉ lệ khung hình của chúng.
- Màu thương hiệu, font, logo hoặc constraint có sẵn.
- Một điều người dùng cần nhớ nhất sau khi rời trang.
- Website có phải hoàn toàn bằng tiếng Việt hay có nhu cầu song ngữ.

Sau đó tự viết một câu định hướng nội bộ:

`Website này phải có cảm giác như [mood/chất lượng tham chiếu cụ thể], không phải như [kiểu website generic cần tránh].`

Ví dụ:

- `Giống một bài editorial du lịch cao cấp, không phải danh bạ điểm đến.`
- `Giống microsite triển lãm bảo tàng, không phải bài tập sinh viên.`
- `Giống trang ra mắt sản phẩm premium, không phải landing page SaaS generic.`

Dùng câu này để loại bỏ các quyết định thiết kế lệch hướng về sau.

## Chọn một hướng thẩm mỹ và theo đến cùng

Không trộn nhiều ngôn ngữ thị giác tùy hứng. Chọn một hướng chính, ví dụ:

- Editorial / documentary
- Văn hóa / thủ công
- Luxury minimal
- Civic / institutional hiện đại
- Playful expressive
- Technical / data-rich
- Retro-modern
- Brutalist editorial
- Soft organic
- High-contrast monochrome

Sau khi chọn, quyết định rõ:

- Phong cách font display.
- Phong cách font body.
- Họ màu nền neutral.
- Một màu accent chính.
- Accent phụ nếu thật sự cần.
- Radius: vuông, nhỏ, vừa, pill hay phân theo chức năng.
- Border: không border, hairline, editorial rule, soft outline.
- Shadow: không dùng, rất nhẹ, hay depth mạnh.
- Media: full-bleed, framed, masked, collage hay editorial crop.
- Motion: restrained, soft, energetic, mechanical hay gần như không dùng.

Không quyết định từng section độc lập như các mini-site khác nhau.

## Tránh các dấu hiệu "AI design"

Không mặc định dùng:

- Gradient tím-xanh trên nền trắng/đen.
- Inter/Roboto/system font ở mọi nơi mà không có lý do.
- Hero căn giữa + gradient text + 2 nút + 3 card ngang bằng nhau.
- Mọi nội dung đều đặt trong card bo tròn.
- Glassmorphism tùy tiện.
- Quá nhiều pill/badge.
- Eyebrow label viết HOA nhỏ phía trên mọi heading.
- `01 / 02 / 03` khi nội dung không có thứ tự.
- Highlight một từ ngẫu nhiên trong mọi heading bằng màu khác/italic.
- Mọi section đều fade-up y hệt nhau.
- Blob, quả cầu, grid, glow chỉ để trang trí mà không liên quan chủ đề.
- Khoảng trống lớn do bố cục yếu nhưng được gọi là "minimal".
- Copy tiếng Việt sáo rỗng kiểu “Khám phá hành trình tuyệt vời của bạn” nếu không nói được giá trị cụ thể.

Nếu draft đầu trông giống template landing page phổ biến, hãy sửa **composition** trước khi polish chi tiết.

## Typography là hệ thống thiết kế chính

Đọc `references/visual-system.md` để áp dụng chi tiết.

Tối thiểu:

- Khi phù hợp, dùng một font display có cá tính + một font body dễ đọc.
- Tối đa 2 font family trừ khi brief có lý do mạnh.
- Dùng type scale có hệ thống, không đặt size ngẫu nhiên.
- Dùng weight để tạo hierarchy; không để mọi thứ đều semibold.
- Body text thường nên dài khoảng 55-75 ký tự mỗi dòng.
- Display text dùng line-height chặt hơn; body rộng rãi hơn.
- Chủ động kiểm soát line break của hero/heading lớn.
- Tránh một từ lẻ rơi xuống dòng cuối ở heading quan trọng.
- Không lạm dụng uppercase.
- Nav, button, metadata, body, caption và heading phải có role thị giác khác nhau.

Lưu ý riêng với tiếng Việt:

- Kiểm tra font có đầy đủ dấu tiếng Việt và render đẹp ở mọi weight.
- Tránh font display đẹp với tiếng Anh nhưng dấu tiếng Việt bị lệch, quá cao hoặc thô.
- Heading tiếng Việt thường dài hơn; đừng copy nguyên kích thước/wrapping từ layout tiếng Anh.
- Không ép letter-spacing quá chặt khiến dấu tiếng Việt khó đọc.
- Kiểm tra các cụm nhiều dấu như `trải nghiệm`, `nghệ thuật`, `địa phương`, `bền vững` ở heading lớn.

Một trang mạnh vẫn phải trông đẹp kể cả khi thay toàn bộ ảnh bằng các khối xám.

## Xây hệ thống không gian trước khi làm từng section

Dùng một geometry nhất quán:

- Một `max-width` chính cho nội dung.
- Một `text measure` cho đoạn đọc dài.
- Một spacing scale.
- Một nhịp section-gap.
- Horizontal padding cố định theo breakpoint.
- Một số grid pattern giới hạn.

Ưu tiên base 4px hoặc 8px. Chỉ dùng giá trị lẻ khi cần optical correction.

Điểm bắt đầu tham khảo:

- Mobile padding: 20-24px.
- Tablet padding: 32-48px.
- Desktop padding: 56-80px.
- Main max-width: 1200-1440px tùy mật độ.
- Reading column: 640-760px.
- Major section gap: 96-160px desktop, 64-96px mobile.

Đây chỉ là baseline, không phải luật cứng.

## Compose section thay vì xếp section

Tránh cấu trúc chỉ có:

`hero -> heading giữa -> 3 cards -> heading giữa -> 3 cards -> CTA`

Có thể dùng:

- Full-bleed media + text block lệch trục.
- Split 5/7 hoặc 4/8.
- Quote/statistic lớn băng qua nhiều cột.
- Sticky text + nội dung scroll.
- Ảnh editorial + caption rail.
- Horizontal story strip.
- Bento chỉ khi hierarchy nội dung thực sự khác nhau.
- Xen kẽ section dày và section thoáng.
- Overlap nhẹ giữa media/content để tạo chiều sâu.
- Một vài section edge-to-edge để reset nhịp thị giác.

Một trang nên dùng tối đa khoảng 3 pattern bố cục chính. Repetition tạo coherence; variation tạo interest.

Đọc `references/layout-patterns.md` khi quyết định cấu trúc trang.

## Chuẩn cho hero

Hero phải trả lời trong vài giây:

- Đây là gì?
- Tại sao đáng quan tâm?
- Tôi nên làm gì tiếp theo?

Ưu tiên một trong các cấu trúc:

- Split editorial hero.
- Full-bleed media + anchored copy.
- Typographic hero lớn + media crop hỗ trợ.
- Asymmetric collage hero.
- Minimal statement hero + một visual mạnh phía dưới.

Quy tắc:

- Chỉ có một focal point chính.
- Thường chỉ cần một primary CTA; secondary CTA chỉ khi phục vụ một hành động khác rõ ràng.
- Không nhồi đồng thời card, feature list, logo, statistic vào hero.
- Đặt copy ở vùng media có breathing room.
- Overlay chỉ đủ để đảm bảo contrast.
- Không mặc định `100vh`.
- Mobile ưu tiên readability hơn việc giữ y nguyên desktop composition.
- Headline tiếng Việt cần ngắn, cụ thể, có nhịp; tránh câu dài như đoạn mô tả.
- Subheading nên làm rõ giá trị, không lặp lại headline bằng từ khác.

## Dùng ảnh/video người dùng cung cấp như vật liệu bố cục

Không tạo media. Hãy quan sát asset và thiết kế xung quanh chúng.

Với mỗi asset, xác định:

- Chủ thể nằm ở đâu.
- Vùng crop an toàn.
- Orientation/aspect ratio.
- Có thể overlay chữ không.
- Nên full-bleed, framed, masked hay dùng như detail.

Ưu tiên crop có chủ đích thay vì `object-cover` cho mọi thứ.

Thiết lập hierarchy media:

- Một visual chính.
- Một số visual hỗ trợ.
- Visual nhỏ chỉ dùng khi bổ sung thông tin hoặc nhịp.

Không đặt mọi ảnh vào cùng một rounded rectangle.

Với video:

- Dùng ở nơi motion thật sự tăng ý nghĩa/không khí.
- Controls phải phù hợp vai trò video.
- Nếu làm background, bảo đảm text vẫn đọc được trên mọi frame.
- Có poster/fallback nếu có thể.
- Tôn trọng `prefers-reduced-motion` với chuyển động không thiết yếu.

## Hệ màu

Dùng CSS variables/tokens. Không rải các màu literal không liên quan khắp component.

Xây palette theo role:

- `--bg`
- `--surface`
- `--surface-strong`
- `--text`
- `--text-muted`
- `--border`
- `--accent`
- `--accent-contrast`

Khi hợp chủ đề, ưu tiên near-neutral có chút hue thay vì trắng/đen tuyệt đối.

Accent phải dùng có chọn lọc. Nếu cái gì cũng accent thì không còn emphasis.

Tham khảo nhịp màu:

- 70-85% neutral/background.
- 10-20% surface/supporting details.
- 5-10% accent/emphasis.

Không cần áp dụng như công thức toán; chỉ dùng để giữ kỷ luật thị giác.

## Card: chỉ dùng khi nội dung thật sự có tính card

Card hợp lý khi nội dung:

- độc lập,
- có thể scan,
- lặp lại,
- clickable,
- hoặc cần so sánh.

Không bọc đoạn văn vào card chỉ để “có design”.

Khi dùng card:

- Phân biệt rõ clickable và static.
- Giữ padding/radius nhất quán.
- Không lồng card trong card nếu không có lý do.
- Không để mọi card cao bằng nhau nếu nội dung/hierarchy không cần.
- Cho phép một item nổi bật hơn nếu nội dung quan trọng hơn.

## Motion và interaction

Motion phải giúp:

- hiểu quan hệ,
- xác nhận tương tác,
- dẫn mắt,
- hoặc tạo atmosphere hợp chủ đề.

Không dùng animation chỉ để chứng minh trang “có animation”.

Guideline:

- Hover micro-interaction: khoảng 120-220ms.
- Small state transition: 160-280ms.
- Entrance lớn: 300-600ms, dùng tiết chế.
- Ưu tiên opacity/transform hơn properties gây layout reflow.
- Không stagger hàng chục item nếu không có giá trị.
- Không để content quan trọng phải chờ animation mới nhìn thấy.
- Tôn trọng reduced motion.

## Responsive = thiết kế lại, không phải thu nhỏ

Ở mỗi breakpoint hãy tự hỏi:

- Hierarchy nào phải giữ?
- Có cần đổi thứ tự content/media không?
- Crop có còn đúng không?
- Heading có cần giảm size hoặc đổi line break không?
- Có section nào nên đổi từ grid sang flow không?
- Sticky/hover behavior có còn hợp trên touch không?
- CTA có dễ bấm không?

Không chỉ `flex-col` mọi thứ rồi coi như responsive xong.

Với mobile:

- Heading cần ngắn hơn về chiều ngang.
- Tránh line break xấu do cụm từ tiếng Việt dài.
- Tối thiểu tap target khoảng 44px khi phù hợp.
- Loại bớt decoration nếu làm màn hình chật.
- Navigation phải rõ và dễ dùng bằng một tay.

## Copy tiếng Việt

Nếu user không cung cấp toàn bộ copy, hãy viết nội dung tiếng Việt ngắn gọn, tự nhiên và đúng tone.

Nguyên tắc:

- Ưu tiên câu ngắn, chủ động, cụ thể.
- Tránh sáo ngữ marketing nếu không thêm thông tin.
- Không dịch literal cấu trúc tiếng Anh.
- CTA phải là động từ rõ: `Xem hành trình`, `Khám phá địa điểm`, `Đăng ký tham gia`, `Xem bản đồ`, `Tìm hiểu thêm`.
- Metadata/ngày/đơn vị tiền tệ phải theo ngữ cảnh Việt Nam nếu phù hợp.
- Dùng dấu câu tiếng Việt tự nhiên; không lạm dụng dấu `—` kiểu copy tiếng Anh.
- Kiểm tra chính tả và dấu trước khi hoàn thành.

## Ưu tiên trong hackathon

Khi thời gian ngắn, ưu tiên theo thứ tự:

1. Đủ requirement bắt buộc.
2. Hero + first viewport thật mạnh.
3. Typography + spacing + page rhythm.
4. 1-2 interaction có ý nghĩa.
5. Responsive cho các màn hình chính.
6. Polish chi tiết.

Không hy sinh requirement để chạy theo decoration.

Không over-engineer backend/abstraction mà giám khảo không nhìn thấy nếu không cần cho chức năng.

## Browser QA bắt buộc

Không được tuyên bố xong chỉ vì build pass.

Phải kiểm tra trang render thật và sửa những thứ nhìn thấy được.

Kiểm tra ít nhất:

- Desktop rộng khoảng 1440px.
- Laptop khoảng 1280px.
- Mobile khoảng 390px.

Quan sát:

- Heading wrap.
- Alignment.
- Section rhythm.
- Crop ảnh/video.
- Contrast.
- Overflow.
- Sticky/fixed element.
- Navigation.
- Hover/focus.
- Console errors.
- Asset bị fail.
- Layout shift.
- Nội dung tiếng Anh còn sót trong website tiếng Việt.

Sau đó đọc `references/polish-checklist.md` và làm final pass.

## Final screenshot test

Trước khi giao, nhìn trang như giám khảo chỉ có 10 giây.

Tự hỏi:

- Có thể nhận ra ngay chủ đề không?
- Hero có cảm giác bespoke hay template?
- Có một khoảnh khắc thị giác đáng nhớ không?
- Có section nào trông như filler không?
- Trang có quá nhiều card không?
- Có chỗ nào căn giữa chỉ vì dễ code không?
- Typography có đủ mạnh để nâng trang lên không?
- Media có đang hỗ trợ bố cục không?
- Mobile có giống sản phẩm hoàn thiện không?
- Copy tiếng Việt có tự nhiên và nhất quán không?

Nếu câu trả lời chưa tốt, sửa composition/hierarchy trước, rồi mới chỉnh shadow, border hay animation.

## Thứ tự làm việc khuyến nghị

1. Đọc đề và tạo requirement checklist.
2. Xác định audience + mục tiêu + tone.
3. Chọn một visual direction duy nhất.
4. Chốt typography, color, grid, spacing, radius.
5. Sketch cấu trúc page/section trước khi code sâu.
6. Build skeleton và requirement bắt buộc.
7. Tích hợp media được cung cấp vào layout.
8. Tinh chỉnh hero và 2-3 section quan trọng nhất.
9. Làm responsive có chủ đích.
10. Mở browser, kiểm tra trực tiếp và sửa.
11. Chạy polish checklist.
12. So lại toàn bộ requirement trước khi giao.

Ưu tiên website **đẹp có hệ thống**, không phải đẹp nhờ vài hiệu ứng rời rạc.
