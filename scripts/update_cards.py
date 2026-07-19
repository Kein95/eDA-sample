import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Tab renaming: Ưu đãi sớm -> Early Bird
text = text.replace('Ưu đãi sớm', 'Early Bird')

# 2. Button renaming: Mở lộ trình chi tiết -> Lộ trình chi tiết
text = text.replace('Mở lộ trình chi tiết', 'Lộ trình chi tiết')

# 3. Change white background of the 4 Document cards
# The cards all start with something like this:
# style="position:relative;display:flex;flex-direction:column;gap:8px;background:var(--surface,#fffdf9);border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);border-radius:0;padding:24px 26px;text-decoration:none;color:var(--ink,#211d17);transition:all 0.2s;"

# Card 1: Marketing Analytics - starts with href="https://drive.google.com/file/d/1HDr8nKMf5yqfUZoIR_YcIG5Rfkv2Pw3P/view"
card1_href = 'href="https://drive.google.com/file/d/1HDr8nKMf5yqfUZoIR_YcIG5Rfkv2Pw3P/view"'
# We want to replace `background:var(--surface,#fffdf9)` with `background:#FCA5A5` on the line containing `card1_href`.
def replacer1(m):
    return m.group(0).replace('background:var(--surface,#fffdf9)', 'background:#FCA5A5')
text = re.sub(r'<a href="https://drive\.google\.com/file/d/1HDr8nKMf5yqfUZoIR_YcIG5Rfkv2Pw3P/view"[^>]+>', replacer1, text)

# Card 2: Retail Analytics - starts with href="https://drive.google.com/file/d/1ObBAKfuKm8J1OUCnV50oVyCnQLMSnb3e/view"
def replacer2(m):
    return m.group(0).replace('background:var(--surface,#fffdf9)', 'background:#93C5FD')
text = re.sub(r'<a href="https://drive\.google\.com/file/d/1ObBAKfuKm8J1OUCnV50oVyCnQLMSnb3e/view"[^>]+>', replacer2, text)

# Card 3: Digital Marketing - starts with href="https://drive.google.com/file/d/1ov8eWsaOJPsDff5nXxBdEuwIjohk1Bk9/view"
def replacer3(m):
    return m.group(0).replace('background:var(--surface,#fffdf9)', 'background:#86EFAC')
text = re.sub(r'<a href="https://drive\.google\.com/file/d/1ov8eWsaOJPsDff5nXxBdEuwIjohk1Bk9/view"[^>]+>', replacer3, text)

# Card 4: Syllabus - starts with href="docs/eDA-2026-Syllabus.html"
def replacer4(m):
    return m.group(0).replace('background:var(--surface,#fffdf9)', 'background:#FDE047')
text = re.sub(r'<a href="docs/eDA-2026-Syllabus\.html"[^>]+>', replacer4, text)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Card colors and text updated successfully.")
