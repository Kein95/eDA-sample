import sys

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update eyebrow
text = text.replace(
    '<span class="eyebrow">Ưu đãi tham gia sớm · trước 05.08.2026</span>',
    '<span class="eyebrow">Ưu đãi tham gia sớm · Trước 05.08.2026</span>'
)

# 2. Update h1 title
text = text.replace(
    '<span style="display:block">Early-bird: Học trước phần nền.</span><span style="display:block;color:#b68235">Miễn phí.</span>',
    '<span style="display:block">Early Bird: Học trước phần nền - </span><span style="display:block;color:#b68235">hoàn toàn miễn phí.</span>'
)

# 3. Update main box
old_box = "Khoảng cách lớn nhất giữa học viên không nằm ở khoá chính - nó nằm ở phần nền.<br>Giữ vé Early-bird, bạn nhận trọn 18 buổi bổ trợ và 9 buổi warm-up Python &amp; SQL live Zoom cùng giảng viên chính, trước khai giảng 06.09.<br>Vào Module 1, bạn đã quen tay."
new_box = "Khoảng cách lớn nhất giữa các học viên không nằm ở khóa chính, mà nằm ở mức độ vững vàng của phần nền.<br><br>Khi giữ vé Early Bird, bạn nhận trọn <strong>18 buổi bổ trợ</strong> và <strong>9 buổi warm-up Python &amp; SQL trực tiếp qua Zoom</strong> cùng giảng viên chính, trước ngày khai giảng <strong>06.09.2026</strong>.<br><br>Đến Module 1, bạn đã quen công cụ, vững kiến thức nền và sẵn sàng bắt nhịp với lộ trình chính."
text = text.replace(old_box, new_box)

# 4. Update small box
old_small = "Lịch bổ trợ &amp; warm-up gửi qua email sau khi đăng ký.<br>Có record cho người bận lịch."
new_small = "Lịch học bổ trợ và warm-up sẽ được gửi qua email sau khi đăng ký.<br>Tất cả buổi học đều có bản ghi dành cho học viên bận lịch."
text = text.replace(old_small, new_small)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Early bird texts updated successfully")
