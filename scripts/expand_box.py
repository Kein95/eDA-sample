import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Expand the box for Video Demo since it has hardcoded 58ch
text = text.replace("max-width:58ch\">Bốn trích đoạn từ", "max-width:85ch\">Bốn trích đoạn từ")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Expanded box width")
