# -*- coding: utf-8 -*-
"""Doi mau vien va bong cung tu den tuyen sang muc tim rat sam.

Vi sao: phong cach the cua trang (vien day, bong cung, khong bo goc mo) can do nang,
nhung den tuyen #211d17 lam ca trang bi "chet". Muc tim #2E1065 giu nguyen do nang
do, ma an vao he mau tim/xanh/cam cua tung module, khong con cam giac den.

Chi doi mau VIEN va BONG. Mau CHU van la --ink, vi chu can tuong phan toi da.

Chay lai duoc nhieu lan (lan hai khong tim thay gi de doi thi bao 0).
    python scripts/swap-ink-to-violet.py
"""
import re
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "TuyenSinh-eDA2026.dc.html"
EDGE = "#2E1065"          # violet-950, du sam de dong vai tro vien den

html = HTML.read_text(encoding="utf-8")
before = html

# 1) Vien: "border:Npx solid var(--ink,#211d17)" (ke ca dashed) -> muc tim
html = re.sub(
    r'(border(?:-top|-bottom|-left|-right)?:\s*[\d.]+px\s+(?:solid|dashed)\s+)var\(--ink,#211d17\)',
    r'\1' + EDGE, html)

# 2) Bong cung: "box-shadow:Npx Npx 0 var(--ink,#211d17)" -> muc tim
html = re.sub(
    r'(box-shadow:\s*-?[\d.]+px\s+-?[\d.]+px\s+0\s+)var\(--ink,#211d17\)',
    r'\1' + EDGE, html)

# 3) Vien/bong viet thang mau den trong style-hover cung phai doi cho khop
html = re.sub(r'(box-shadow:\s*-?[\d.]+px\s+-?[\d.]+px\s+0\s+)#211d17', r'\1' + EDGE, html)
html = re.sub(r'(border:\s*[\d.]+px\s+(?:solid|dashed)\s+)#211d17', r'\1' + EDGE, html)

if html == before:
    print("khong co gi de doi (co the da chay roi)")
else:
    HTML.write_text(html, encoding="utf-8")
    print(f"da doi {before.count('var(--ink,#211d17)') - html.count('var(--ink,#211d17)')} "
          f"khai bao vien/bong sang {EDGE}")
