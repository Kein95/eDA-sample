import sys

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace line breaks in Lo trinh module details
text = text.replace(
    "Mỗi module gắn với một domain thực tế và kết thúc bằng project cùng bài exam đánh giá năng lực. Bấm vào từng module để xem lịch học chi tiết của từng buổi.",
    "Mỗi module gắn với một domain thực tế và kết thúc bằng project cùng bài exam đánh giá năng lực.<br>Bấm vào từng module để xem lịch học chi tiết của từng buổi."
)

# Replace line breaks in Video demo details
text = text.replace(
    "Bốn trích đoạn từ lớp học thật. Xem để biết giảng viên dạy ra sao, nhịp học nhanh chậm thế nào, có hợp với mình không. Bấm vào thẻ là xem ngay tại trang, không cần rời đi.",
    "Bốn trích đoạn từ lớp học thật.<br>Xem để biết giảng viên dạy ra sao, nhịp học nhanh chậm thế nào, có hợp với mình không.<br>Bấm vào thẻ là xem ngay tại trang, không cần rời đi."
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Line breaks added successfully!")
