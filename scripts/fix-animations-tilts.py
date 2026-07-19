# -*- coding: utf-8 -*-
import re
import random
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "TuyenSinh-eDA2026.dc.html"
html = HTML.read_text(encoding="utf-8")

# 1. Restore the drumspin keyframes
html = html.replace('@keyframes drumspin { from {  } to {  } }', '@keyframes drumspin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }')

# Just in case it was partially matched:
if '@keyframes drumspin { from { transform: rotate(0deg); }' not in html:
    html = re.sub(r'@keyframes drumspin \{[\s\S]*?\}', '@keyframes drumspin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }', html)

# 2. Add retro tilt back to the major cards to make it not "xấu" (ugly/rigid)
# Let's find large cards which have "padding:32px 36px" or "padding:26px 28px" (from Mentor module)
# and add a slight transform to them if they don't have one.
def add_tilt(match):
    style_str = match.group(1)
    if 'transform:rotate' not in style_str:
        tilt = round(random.uniform(-1.5, 1.5), 1)
        if abs(tilt) < 0.5: tilt = 1.2
        return f'style="{style_str};transform:rotate({tilt}deg)"'
    return match.group(0)

# The cards usually have `border:3px solid var(--ink` and are block-level (not span)
html = re.sub(r'style="([^"]*border:3px solid var\(--ink,#211d17\)[^"]*box-shadow:[^"]*)"', add_tilt, html)

HTML.write_text(html, encoding="utf-8")
print("Restored drumspin and added retro tilts to cards.")
