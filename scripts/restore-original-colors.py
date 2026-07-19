# -*- coding: utf-8 -*-
import re
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "TuyenSinh-eDA2026.dc.html"
html = HTML.read_text(encoding="utf-8")

# 1. Restore Matrix Colors to vibrant (but retro/soft) colors
html = html.replace('color-mix(in srgb, var(--gold,#b68235) 90%, transparent)', '#ef4444')
html = html.replace('color-mix(in srgb, var(--gold,#b68235) 45%, transparent)', '#f97316')
html = html.replace('color-mix(in srgb, var(--gold,#b68235) 15%, transparent)', '#fef08a')

# 2. Restore Gold buttons (remove flat gradients, restore borders)
html = html.replace('background:linear-gradient(135deg, var(--gold), var(--deep));color:#fff;border:none', 'background:var(--gold)')

# 3. Restore Slate sections back to Ink (Original Neo-Brutalism uses Black blocks)
# Wait, if they liked Slate, maybe keep it? But they said "màu sắc vẫn giữ nguyên" (keep original colors).
# The original color of the blocks was var(--ink,#211d17).
html = html.replace('background:#0f172a', 'background:var(--ink,#211d17)')

# 4. Just in case, ensure the legend matches
html = html.replace('background:#DC2626', 'background:#ef4444')
html = html.replace('background:#FB923C', 'background:#f97316')
html = html.replace('background:#FEF3C7', 'background:#fef08a')

HTML.write_text(html, encoding="utf-8")
print("Restored original colors (Red/Orange/Yellow matrix, Gold buttons, Ink blocks).")
