"""
Fix: In dark mode, text inside boxes with hardcoded light backgrounds
becomes unreadable because var(--ink) flips to a light color.

Solution: Override --ink and --deep on those specific elements so
all child elements using var(--ink,...) get a forced-dark value,
regardless of the global theme.
"""

file_path = r"D:\Projects\eDA\TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Each pastel-background box needs --ink forced dark so child text stays readable.
# We inject --ink:#211d17;--deep:#7c5a24 into the style of each container.

light_bgs = [
    "background:#f1e5cf;",   # beige cards (Python, Data Viz)
    "background:#c7d2fe;",   # lavender info box (Video demo)
    "background:#fce7f3;",   # pink info box (Giảng viên)
    "background:#ffedd5;",   # peach info box (Mentor domain)
]

ink_override = "--ink:#211d17;--deep:#7c5a24;"

count = 0
for bg in light_bgs:
    # Only inject if not already overridden
    marker = bg + ink_override
    if marker in text:
        print(f"  SKIP (already fixed): {bg}")
        continue
    old = bg
    new = bg + ink_override
    n = text.count(old)
    text = text.replace(old, new)
    count += n
    print(f"  Fixed {n} occurrence(s) of {bg}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"\nDone – {count} element(s) patched with forced --ink override.")
