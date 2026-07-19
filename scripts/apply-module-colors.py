# -*- coding: utf-8 -*-
"""Gan mot mau rieng cho tung module trong tab Lo trinh.

Vi sao lam: ca trang truoc day chi dung mot mau vang #b68235, nhin don dieu, trong
khi phong cach the (vien den day, bong cung, khong bo goc mo) von song bang khoi
mau phang manh.

Mau khong boi cho vui: no NOI TIEP he mau da co trong so do tong quan, nen module 3
mau cam o so do thi cung cam o lo trinh. Nguoi hoc nhin mot cai la noi duoc hai cho.

Chay lai duoc nhieu lan: script tim dung the so module theo so thu tu roi thay.
    python scripts/apply-module-colors.py
"""
import re
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "TuyenSinh-eDA2026.dc.html"

# Tam mau bam theo nhom domain cua tung module trong so do tong quan.
# Do bao hoa du cao de chu trang doc duoc, va deu hop tren nen kem.
MODULE_COLORS = {
    "01": "#2563EB",   # Excel · Sales          (xanh duong)
    "02": "#16A34A",   # Power BI · Finance     (xanh la)
    "03": "#EA580C",   # SQL · Marketing        (cam)
    "04": "#DC2626",   # Agentic AI · da domain (do)
    "05": "#0D9488",   # Advanced DA · Supply   (xanh muc)
    "06": "#4F46E5",   # DA+DE · Operations     (cham)
    "07": "#CA8A04",   # DA+DS · Credit Risk    (vang dam)
    "08": "#7C3AED",   # Luyen chung chi        (tim)
}

BADGE = (
    'display:inline-flex;width:52px;height:52px;border-radius:14px;'
    'background:{color};border:2.5px solid var(--ink,#211d17);'
    'box-shadow:3px 3px 0 var(--ink,#211d17);'
    'align-items:center;justify-content:center;'
    "font-family:'Space Grotesk',sans-serif;font-weight:800;font-size:19px;"
    'color:#fff;font-variant-numeric:tabular-nums'
)

# Module 08 la khoi "Luyen chung chi", the so cua no la o nét đứt chu khong phai the day.
BADGE_08 = (
    'display:inline-flex;width:52px;height:52px;border-radius:14px;'
    'background:{color};border:2.5px dashed var(--ink,#211d17);'
    'box-shadow:3px 3px 0 var(--ink,#211d17);'
    'align-items:center;justify-content:center;'
    "font-family:'Space Grotesk',sans-serif;font-weight:800;font-size:19px;"
    'color:#fff;font-variant-numeric:tabular-nums'
)

html = HTML.read_text(encoding="utf-8")
changed = 0

for num, color in MODULE_COLORS.items():
    style = (BADGE_08 if num == "08" else BADGE).format(color=color)
    # Bat dung the <span style="..."> ... >NN</span> cua rieng module do.
    pattern = re.compile(r'<span style="[^"]*?">(' + num + r')</span>')

    def swap(m, s=style, n=num):
        global changed
        changed += 1
        return f'<span style="{s}">{n}</span>'

    html, n_sub = pattern.subn(swap, html, count=1)
    if n_sub == 0:
        raise SystemExit(f"khong tim thay the so module {num} — dung lai de kiem tra")

HTML.write_text(html, encoding="utf-8")
print(f"da to mau {changed}/{len(MODULE_COLORS)} the so module")
