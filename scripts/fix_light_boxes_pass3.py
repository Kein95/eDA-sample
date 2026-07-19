"""
Pass 3: Fix ALL remaining light-background elements that use var(--ink)
for text color, causing unreadable text in dark mode.
"""

file_path = r"D:\Projects\eDA\TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

ink_override = "--ink:#211d17;--deep:#7c5a24;"
count = 0

remaining_bgs = [
    "background:#fef08a;",   # yellow box (Early Bird)
    "background:#FEF08A;",   # yellow chip (uppercase variant)
    "background:#C7D2FE;",   # lavender chip (Record đầy đủ)
    "background:#f3f4f6;",   # grey info box (Lịch học bổ trợ)
]

for bg in remaining_bgs:
    marker = bg + ink_override
    if marker in text:
        print(f"  SKIP (already fixed): {bg}")
        continue
    n = text.count(bg)
    if n == 0:
        print(f"  NOT FOUND: {bg}")
        continue
    text = text.replace(bg, bg + ink_override)
    count += n
    print(f"  Fixed {n} occurrence(s) of {bg}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"\nDone – {count} element(s) patched.")
