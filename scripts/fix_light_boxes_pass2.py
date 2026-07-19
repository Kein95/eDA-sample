"""
Fix remaining light-background boxes that were missed in the first pass.
"""

file_path = r"D:\Projects\eDA\TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

ink_override = "--ink:#211d17;--deep:#7c5a24;"
count = 0

# Additional light backgrounds missed in first pass
extra_bgs = [
    "background:#e0f2fe;",   # light blue info boxes (Tài liệu section + Syllabus badge)
]

for bg in extra_bgs:
    marker = bg + ink_override
    if marker in text:
        print(f"  SKIP (already fixed): {bg}")
        continue
    n = text.count(bg)
    text = text.replace(bg, bg + ink_override)
    count += n
    print(f"  Fixed {n} occurrence(s) of {bg}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"\nDone – {count} additional element(s) patched.")
