import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace the text to insert a <br> tag for line breaks
text = text.replace(
    'bài đánh giá năng lực. Đặc biệt, bạn sẽ được',
    'bài đánh giá năng lực.<br>Đặc biệt, bạn sẽ được'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Text split successfully.")
