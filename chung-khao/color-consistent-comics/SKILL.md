---
name: color-consistent-comics
description: Tạo và chỉnh sửa truyện tranh tiếng Việt với nét vẽ, nhân vật nhất quán và bảng màu phẳng tươi. Dùng khi yêu cầu giữ nét đổi màu, tạo storyboard, character sheet, trang truyện tiếp theo hoặc chuẩn bị chữ chỉnh sửa được trong PPT/Canva; đặc biệt cho truyện Đồng đội bên kia màn hình.
---

# Truyện tranh: giữ nét, đổi màu

## Ý đồ đã chốt

- Giữ nét vẽ, khuôn mặt, tỷ lệ và tạo hình từ ảnh gốc của người dùng. Không tự chuyển sang nét Scott Pilgrim, chibi hoặc nét của họa sĩ khác.
- Áp dụng hướng màu người dùng thích ở Scott Pilgrim bản màu: mảng màu phẳng, tươi, tương phản rõ, bóng gọn và điểm nhấn có chọn lọc. Mô tả bằng thuộc tính thị giác cụ thể, không chỉ ghi tên họa sĩ trong prompt.
- Phân biệt credit: Bryan Lee O’Malley là tác giả/họa sĩ Scott Pilgrim; Nathan Fairbairn phụ trách phần màu của bản màu được tham khảo. Không gán toàn bộ phần màu cho O’Malley.
- Giữ bối cảnh Việt Nam và nhân vật sinh viên. Làm cảnh vui sáng sủa, cảnh căng thẳng vẫn rõ và dễ đọc.
- Ưu tiên yêu cầu mới nhất của người dùng nếu khác mặc định ở đây.

## Tài liệu cần đọc

- Đọc `references/color-direction.md` khi tô màu hoặc viết prompt màu.
- Đọc `references/project.md` khi làm truyện **Đồng đội bên kia màn hình**.
- Đọc `references/prompt-templates.md` khi gọi công cụ ảnh, viết prompt/API payload hoặc sửa một khung.

## Xác định đầu vào

1. Xác định phạm vi: đổi màu, tạo trang mới, thiết kế nhân vật, sửa chữ hay xuất bản chỉnh sửa được. Chỉ thực hiện phạm vi được yêu cầu.
2. Tìm ảnh/trang gốc đã được chọn trong ngữ cảnh hoặc tệp người dùng cung cấp. Mở xem trước khi chỉnh sửa. Không coi mọi ảnh từng sinh là mẫu đã duyệt.
3. Gán vai trò cho từng reference:
   - `linework_source`: nét, khuôn mặt, tư thế và bố cục trang cần sửa.
   - `character_reference`: nhận dạng và trang phục từng nhân vật.
   - `color_reference`: quan hệ màu và cách tô; không lấy khuôn mặt hoặc bố cục từ đây.
   - `layout_reference`: bố cục nếu làm trang mới.
4. Với đổi màu, lấy ảnh đích làm nguồn nét ưu tiên cao nhất. Với trang mới, lấy mẫu nhân vật đã duyệt để giữ nhận dạng.
5. Skill không đóng gói ảnh gốc hoặc trang Scott Pilgrim. Không giả vờ có ảnh reference. Nếu ảnh gốc không truy cập được, hoàn thành prompt/kế hoạch có thể làm và xin đúng ảnh còn thiếu trước khi hứa giữ nguyên nét. Nếu chỉ thiếu ảnh màu, dùng bảng màu đề xuất và ghi rõ đó là phương án khởi đầu.
6. Không hỏi lại màu hoặc cốt truyện đã có. Chỉ hỏi nếu nhiều ảnh gốc khác nhau khiến không xác định được ảnh cần giữ nét.

## Tô lại trang có sẵn

1. Ghi các thành phần phải khóa: tỷ lệ trang, viền khung, thứ tự đọc, nhân vật, nét mặt, tay, đồ vật, góc máy và vị trí chữ.
2. Gửi ảnh gốc qua cơ chế edit/reference của công cụ ảnh đang có. Ghi rõ **color-only edit**; không tạo lại trang từ văn bản nếu có thể chỉnh trực tiếp.
3. Đổi fill, bảng màu, bóng phẳng và độ tương phản. Giữ hình học và nét mực; không thêm trang trí hoặc chi tiết khuôn mặt không cần thiết.
4. Khi chỉ yêu cầu đổi màu, giữ nguyên lời thoại và vị trí chữ. Không tự xóa chữ để chuẩn bị PPT.
5. So kết quả với ảnh gốc: mặt, tóc, tỷ lệ, tay, số khung, đồ vật, nét và chữ. Nếu bị đổi nét, sửa riêng phần sai với ảnh gốc; không dùng ảnh lỗi làm chuẩn cho lần tiếp theo.
6. Gọi kết quả là bản xem thử nếu người dùng chưa duyệt màu. Không khẳng định giữ nguyên từng pixel khi công cụ sinh ảnh đã vẽ lại.

## Làm trang mới

1. Giữ số trang theo kịch bản, tính cả bìa. Lập danh sách khung gồm góc máy, hành động, người nói, lời thoại, vùng chữ và mục tiêu cảm xúc.
2. Dùng mẫu nhân vật và trang màu đã duyệt; không thiết kế lại nhân vật trong mỗi lần gọi.
3. Với theme chưa có mẫu duyệt, ưu tiên thử một cảnh trước khi làm cả truyện. Nếu người dùng đã yêu cầu làm toàn bộ, tiếp tục trong phạm vi đó, không tự thêm điểm dừng xin phép.
4. Giữ hướng đọc trái sang phải, trên xuống dưới. Thường dùng 3–5 khung/trang, một hành động chính mỗi khung. Cho cảnh quan trọng nhiều diện tích hơn.
5. Với trang 2 dự án, dùng một khung ngang trên, hai khung giữa, một khung ngang dưới. Trang nội dung đầu tiên là trang 2; trang 1 là bìa.
6. Giữ vị trí phòng, cửa, giường, bàn và hướng nhìn nhất quán. Cho cảnh trong game màu riêng nhưng không át nhân vật ngoài đời.
7. Nếu đầu ra cần sửa chữ, tạo ảnh không chữ và dành khoảng trống cho balloon. Lưu lời thoại riêng rồi chèn bằng công cụ dàn trang.

## Chữ tiếng Việt và bản chỉnh sửa được

- Giữ nguyên lời thoại đã chốt, dấu tiếng Việt và tên Minh/Huy/Khang/KạĐêm. Chỉ rút gọn khi được yêu cầu hoặc nêu rõ đề xuất thay đổi.
- Với bản sản xuất, ưu tiên tranh raster + balloon/ô dẫn/text box riêng. Nếu người dùng muốn mọi hình cũng sửa được, giải thích tranh raster không tự thành vector; cần tách asset hoặc vẽ lại.
- Lưu chữ theo page/panel/speaker/text và vị trí chuẩn hóa 0–1. Tách tiêu đề, lời thoại, tin nhắn, chữ giao diện, lời dẫn và thông điệp cuối.
- Chọn font đầy đủ dấu Việt; kiểm tra font thực tế được cài. Kiểm tra cỡ chữ ở toàn trang; mở rộng balloon thay vì thu chữ quá nhỏ. Chừa đệm khoảng 8–12% bề rộng balloon; tránh đuôi chỉ nhầm người.
- Với PPT, dùng một trang truyện trên một slide đúng tỷ lệ, tranh nền rồi text box/shape chỉnh sửa được. Với Canva, dùng chữ/shape native nếu công cụ hỗ trợ; nếu nhập PPTX, kiểm tra lại font và ngắt dòng.
- Nếu ảnh đã có chữ lỗi, ưu tiên xóa/inpaint chữ trong balloon rồi thêm text box. Phủ hộp trắng là giải pháp tạm: chữ cũ vẫn trong nền và có thể lộ khi dịch chuyển.
- Kiểm tra từng câu theo kịch bản và xem bản render. Không nhận là Canva/PPT có lớp chữ nếu chỉ xuất PNG.
- Dùng công cụ/kỹ năng trình chiếu khi có; không bịa khả năng kết nối hoặc đã xuất tệp.

## Công cụ, API và ghi nhận

- Dùng công cụ ảnh được hỗ trợ để tạo/chỉnh ảnh. Không cố định tên model, giá hoặc tham số không được API hiện tại hỗ trợ.
- Với API trực tiếp, file SKILL.md không tự được API đọc: agent phải nạp phần hướng dẫn liên quan, tạo prompt và gửi ảnh reference thực sự vào request. Đường dẫn nằm trong prompt không thay thế image input.
- Khi viết mã, tách model/size/quality/output thành cấu hình. Chỉ dùng giá trị đã kiểm tra với provider; không ghi khóa API trong tệp.
- Lưu prompt thực tế, vai trò và thứ tự reference, model/tham số nếu biết, kết quả, các lần sửa và quyết định duyệt. Usage không được trả về thì ghi không có dữ liệu; không tự biến ước tính thành chi phí thực.
- Nếu cuộc thi có quy định Gateway/AI log, đọc quy định người dùng cung cấp và cấu hình đúng; không suy đoán nhà cung cấp được phép.

## Kiểm tra trước khi giao

- [ ] Đúng phạm vi; đổi màu không làm thay nét hoặc bố cục.
- [ ] Nhân vật đúng nhận dạng, trang phục, độ tuổi; không biến sinh viên thành trẻ nhỏ.
- [ ] Màu tươi, nền dịu, điểm nhìn rõ; không phủ neon hoặc grading tối toàn trang.
- [ ] Màu nhân vật ổn định, da tự nhiên, chữ nổi rõ trên balloon.
- [ ] Đúng số khung, trình tự hành động, người nói và chữ tiếng Việt.
- [ ] Cơ chế lừa đảo có chuỗi hành vi, không ám chỉ chỉ bấm link là mất tiền.
- [ ] Nếu giao bản chỉnh sửa được, đã kiểm tra text/shape và render.
- [ ] Nói ngắn gọn thay đổi và giới hạn; không nhận là đã được người dùng duyệt.
