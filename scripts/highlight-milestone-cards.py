# -*- coding: utf-8 -*-
"""Lam noi bat cac the "moc" trong tab Lo trinh (Module 4, Final Exam, Luyen chung chi).

Nhan dien the theo SO TREN BADGE ('04', 'FE', '08') chu khong theo vi tri chuoi.
Lan truoc do dinh vi bang rfind nen bat nham Module 07, tô tím no roi lam chu chim mat.

Khi to nen sam, phai doi luon MOI mau chu ben trong; neu khong se con chu #b68235
va color-mix(--ink) nam tren nen tim, doc khong ra.

    python scripts/highlight-milestone-cards.py
"""
import re
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "TuyenSinh-eDA2026.dc.html"

DEEP = "#2E1065"          # nen sam cua the moc
HILITE = {"04", "FE", "08"}   # badge cua cac the can lam noi

# Mau chu tren nen sam
TEXT_MAP = [
    (r'color:var\(--ink,#211d17\)', 'color:#f6f2ea'),
    (r'color:color-mix\(in srgb, var\(--ink,#211d17\) \d+%, transparent\)', 'color:rgba(246,242,234,0.78)'),
    (r'color:var\(--deep,#8a6228\)', 'color:#e8bf72'),
    (r'color:#b68235', 'color:#e8bf72'),
    (r'color:#8a6228', 'color:#e8bf72'),
]


def badge_of(card: str):
    """So hien tren badge cua the, vi du '04' hoac 'FE'."""
    m = re.search(r'font-variant-numeric:tabular-nums[^>]*>([^<]{1,3})</span>', card)
    return m.group(1).strip() if m else None


def highlight(card: str) -> str:
    card = card.replace('background:var(--surface,#fffdf9)', f'background:{DEEP}', 1)
    card = re.sub(r'border:1px solid [^;"]+', f'border:3px solid {DEEP}', card, count=1)
    for pat, rep in TEXT_MAP:
        card = re.sub(pat, rep, card)
    return card


def plain(card: str) -> str:
    """Tra the ve trang thai binh thuong (dung de sua the bi to nham)."""
    card = card.replace(f'background:{DEEP}', 'background:var(--surface,#fffdf9)', 1)
    card = card.replace('color:#f6f2ea', 'color:var(--ink,#211d17)')
    card = card.replace('color:rgba(246,242,234,0.78)',
                        'color:color-mix(in srgb, var(--ink,#211d17) 60%, transparent)')
    card = card.replace('color:#e8bf72', 'color:var(--deep,#8a6228)')
    card = card.replace('color:#f5f2ec', 'color:var(--ink,#211d17)')
    card = card.replace('color:#d9a860', 'color:var(--deep,#8a6228)')
    card = re.sub(r'color:rgba\(245,242,236,[\d.]+\)',
                  'color:color-mix(in srgb, var(--ink,#211d17) 60%, transparent)', card)
    return card


html = HTML.read_text(encoding="utf-8")
parts, pos, done = [], 0, []

for m in re.finditer(r'<details\b.*?</details>', html, re.S):
    parts.append(html[pos:m.start()])
    card = m.group(0)
    num = badge_of(card)
    card = plain(card)                    # ve trung tinh truoc, roi moi to lai neu can
    if num in HILITE:
        card = highlight(card)
        done.append(num)
    parts.append(card)
    pos = m.end()

parts.append(html[pos:])
HTML.write_text("".join(parts), encoding="utf-8")
print("da lam noi cac the:", ", ".join(done) or "(khong co)")
