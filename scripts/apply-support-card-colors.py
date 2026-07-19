# -*- coding: utf-8 -*-
"""To mau nhan "N BUỔI" cua 5 the Bo tro (tab Uu dai som).

Nam the deu dung mot mau vang #b68235 nen nhin nhu mot khoi. Gan moi mon mot mau,
bam theo mon do xuat hien o module nao trong lo trinh, de he mau toan trang thong nhat.

Nhan dien the theo TEN MON trong the <span>, khong theo thu tu chuoi — bai hoc tu
apply-module-colors.py, script do tung bat nham so trang tri o dau tab.

    python scripts/apply-support-card-colors.py
"""
import re
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "TuyenSinh-eDA2026.dc.html"

# Mon -> mau, khop voi module day mon do trong lo trinh
SUBJECTS = {
    "Excel":        "#2563EB",   # nhu Module 1
    "Python":       "#16A34A",
    "Pandas & SQL": "#EA580C",   # nhu Module 3 (SQL)
    "Data Viz":     "#0D9488",
    "Power BI":     "#4F46E5",   # nhu Module 6
}

html = HTML.read_text(encoding="utf-8")

# Chi tim trong dung khoi "Bo tro". Cac tu nhu "Excel" hay "Power BI" con xuat hien
# o hero va o lo trinh; tim tren ca file se bat nham cho khac.
block_start = html.index("Bổ trợ · 18 buổi nền tảng")
# Ket thuc = the dong can bang cua luoi chua 5 the (khoi nay khong nam trong <section>)
grid = html.index('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))', block_start)
depth, k = 0, grid
while k < len(html):
    if html.startswith("<div", k):
        depth += 1
    elif html.startswith("</div>", k):
        depth -= 1
        if depth == 0:
            break
    k += 1
block_end = k
done = []

for subject, color in SUBJECTS.items():
    esc_subject = re.escape(subject.replace("&", "&amp;"))
    m = re.compile(r'>' + esc_subject + r'</span>').search(html, block_start, block_end)
    if not m:
        print(f"khong tim thay mon {subject} trong khoi Bo tro")
        continue

    seg_start = html.rfind('<div style="position:absolute;top:-12px', 0, m.start())
    if seg_start < 0:
        print(f"{subject}: khong tim thay nhan so buoi")
        continue
    seg_end = html.find("</div>", seg_start) + len("</div>")
    label = html[seg_start:seg_end]

    new = label.replace("background:#b68235", f"background:{color}")
    new = new.replace("color:var(--surface,#fffdf9)", "color:#fff")
    if new == label:
        continue
    html = html[:seg_start] + new + html[seg_end:]
    done.append(subject)

HTML.write_text(html, encoding="utf-8")
print("da to nhan so buoi cho:", ", ".join(done) or "(khong co)")
