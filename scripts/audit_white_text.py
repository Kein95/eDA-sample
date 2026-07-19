import re

with open(r"D:\Projects\eDA\TuyenSinh-eDA2026.dc.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find color:#fff on elements that do NOT have a dark background
# These are elements with white text that might be unreadable on light backgrounds
color_white_re = re.compile(r'color:#fff\b')
bg_dark_re = re.compile(r'background:#(?:[0-4][0-9a-f]{5}|[0-9a-f]{2}[0-4][0-9a-f]{3})', re.I)

for m in color_white_re.finditer(text):
    line_no = text[:m.start()].count('\n') + 1
    # Get the enclosing tag
    tag_start = text.rfind('<', 0, m.start())
    tag_end = text.find('>', m.end())
    if tag_start < 0 or tag_end < 0:
        continue
    tag = text[tag_start:tag_end+1]
    # Check if this same tag has a dark background
    has_bg = re.search(r'background:#([0-9a-fA-F]{3,6})', tag)
    if has_bg:
        bg = has_bg.group(1).lower()
        if len(bg) == 3:
            bg = bg[0]*2 + bg[1]*2 + bg[2]*2
        r, g, b = int(bg[0:2],16), int(bg[2:4],16), int(bg[4:6],16)
        lum = 0.299*r + 0.587*g + 0.114*b
        if lum < 128:
            continue  # dark bg with white text = fine
        # Light bg with white text = PROBLEM
        print(f"L{line_no}: WHITE TEXT ON LIGHT BG #{has_bg.group(1)} lum={lum:.0f}")
        print(f"  {tag[:200]}")
        print()
    else:
        # No background in same tag - check if text could be on a light parent
        # Just flag it for review
        snippet = tag[:150] if len(tag) < 200 else tag[:150] + "..."
        # Skip if it's clearly on a dark-bg parent (like the colored stat cards)
        # Look back 300 chars for parent background
        ctx = text[max(0, tag_start-300):tag_start]
        parent_bg = re.findall(r'background:#([0-9a-fA-F]{3,6})', ctx)
        if parent_bg:
            last_bg = parent_bg[-1].lower()
            if len(last_bg) == 3:
                last_bg = last_bg[0]*2 + last_bg[1]*2 + last_bg[2]*2
            r, g, b = int(last_bg[0:2],16), int(last_bg[2:4],16), int(last_bg[4:6],16)
            lum = 0.299*r + 0.587*g + 0.114*b
            if lum < 128:
                continue  # parent is dark, white text OK

        print(f"L{line_no}: WHITE TEXT, NO BG IN SAME TAG (check parent)")
        print(f"  {snippet}")
        print()

print("=== done ===")
