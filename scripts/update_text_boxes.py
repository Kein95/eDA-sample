import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Team text
old_team = '<p style="font-size:15.5px;line-height:1.75;max-width:58ch;margin:22px 0 0;color:color-mix(in srgb, var(--ink,#211d17) 70%, transparent)">Các buổi học live do giảng viên chính của AI VIETNAM trực tiếp đứng lớp, cùng đội ngũ mentor đi theo từng nhóm domain suốt khoá.</p>'
new_team = '<div style="background:#fce7f3;border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);padding:16px 20px;margin:22px 0 0;font-size:15px;line-height:1.7;font-weight:500;color:var(--ink,#211d17);text-align:justify;max-width:58ch">Các buổi học live do giảng viên chính của AI VIETNAM trực tiếp đứng lớp, cùng đội ngũ mentor đi theo từng nhóm domain suốt khoá.</div>'
text = text.replace(old_team, new_team)

# 2. Project & tài liệu text
old_doc = '<p style="font-size:15.5px;line-height:1.75;max-width:58ch;margin:22px 0 0;color:color-mix(in srgb, var(--ink,#211d17) 70%, transparent)">Project &amp; tài liệu đọc của chương trình được chia sẻ công khai — mở thử để thấy chất lượng thực. Học viên chính thức nhận đầy đủ tài liệu, dữ liệu và code theo từng module.</p>'
new_doc = '<div style="background:#e0f2fe;border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);padding:16px 20px;margin:22px 0 0;font-size:15px;line-height:1.7;font-weight:500;color:var(--ink,#211d17);text-align:justify;max-width:58ch">Project &amp; tài liệu đọc của chương trình được chia sẻ công khai — mở thử để thấy chất lượng thực. Học viên chính thức nhận đầy đủ tài liệu, dữ liệu và code theo từng module.</div>'
text = text.replace(old_doc, new_doc)

# 3. Video text
old_vid = '<p style="font-size:14.5px;line-height:1.7;max-width:58ch;font-weight:500;margin:12px 0 0;color:color-mix(in srgb, var(--ink,#211d17) 75%, transparent)">Bốn trích đoạn từ lớp học thật. Xem để biết giảng viên dạy ra sao, nhịp học nhanh chậm thế nào, có hợp với mình không. Bấm vào thẻ là xem ngay tại trang, không cần rời đi.</p>'
new_vid = '<div style="background:#c7d2fe;border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);padding:16px 20px;margin:16px 0 0;font-size:14.5px;line-height:1.7;font-weight:500;color:var(--ink,#211d17);text-align:justify;max-width:58ch">Bốn trích đoạn từ lớp học thật. Xem để biết giảng viên dạy ra sao, nhịp học nhanh chậm thế nào, có hợp với mình không. Bấm vào thẻ là xem ngay tại trang, không cần rời đi.</div>'
text = text.replace(old_vid, new_vid)

# 4. Lịch bổ trợ text
old_lich = '<p style="font-size:12.5px;line-height:1.6;margin:18px 0 0;color:color-mix(in srgb, var(--ink,#211d17) 50%, transparent)">Lịch bổ trợ &amp; warm-up gửi qua email sau khi đăng ký. Có record cho người bận lịch.</p>'
new_lich = '<div style="background:#f3f4f6;border:2.5px solid var(--ink,#211d17);box-shadow:3px 3px 0 var(--ink,#211d17);padding:12px 16px;margin:22px 0 0;font-size:13.5px;font-weight:600;color:var(--ink,#211d17);text-align:justify;max-width:90%">Lịch bổ trợ &amp; warm-up gửi qua email sau khi đăng ký. Có record cho người bận lịch.</div>'
text = text.replace(old_lich, new_lich)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated text boxes")
