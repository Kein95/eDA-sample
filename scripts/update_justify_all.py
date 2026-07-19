import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

markers = [
    "Mỗi module một domain, một project",
    "Ô càng đậm, lĩnh vực đó càng nằm gần lõi",
    "Lớp học trực tiếp qua Zoom vào ba buổi",
    "Mỗi module tập trung vào một lĩnh vực thực tế",
    "Vòng ngoài gồm đúng 100 vạch",
    "Khai giảng:</strong>",
    "Đội ngũ mentor theo domain (Sales",
    "Điền thông tin, đội ngũ AI VIETNAM sẽ liên hệ",
    "Cảm ơn <strong>{{ rName }}</strong>"
]

for i, line in enumerate(lines):
    for marker in markers:
        if marker in line:
            # If text-align:justify is not already in this line, add it to the first style attribute
            if "text-align:justify" not in line:
                # Add it to <p style="..."> or <div style="...">
                line = re.sub(r'style="', r'style="text-align:justify;', line, count=1)
                lines[i] = line

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Added text-align:justify to marked elements.")
