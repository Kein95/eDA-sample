import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Timeline text span color
text = text.replace(
    '<span style="color:#7C3AED">',
    '<span style="color:#DC2626">'
)

# 2. Big 08 icon background
text = text.replace(
    'background:#7C3AED;',
    'background:#111827;'
)

# 3. Co-founder tag background
text = text.replace(
    'background:#8b5cf6;',
    'background:#111827;'
)

# 4. Domain Matrix dark purple borders/colors
text = text.replace('#2E1065', 'var(--ink,#211d17)')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Purple colors replaced successfully.")
