# -*- coding: utf-8 -*-
"""Dung bang "nganh x mang phan tich" tu sheet Domain cua data/eDA_v9.xlsx.

Bang nay tra loi cau hoi hoc vien hay hoi nhat: "hoc xong lam o nganh nao".
Sinh tu file nguon nen sua Excel roi chay lai la trang cap nhat theo, khong go tay.

    python scripts/build-domain-matrix.py

Chay lai duoc nhieu lan: tu tim comment moc va thay dung khoi da chen.
"""
import html as html_mod
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "data" / "eDA_v9.xlsx"
HTML = ROOT / "TuyenSinh-eDA2026.dc.html"
MARK = "Bang nganh x mang phan tich - sinh boi build-domain-matrix.py"

# Thang do dam dan: cang do cang la mang nganh do song bang. Dung mot dai nhiet
# thay vi bon mau roi rac, de mat doc duoc cuong do ma khong can tra chu giai.
# Mo ta bam sat chu giai trong sheet Domain, khong suy dien them ve luong hay tuyen dung:
#   CORE = "Mission-critical (dedicated teams, heavy budget)"
#   RELEVANT = "Có làm nhưng không core" / MINIMAL = "Function tồn tại nhưng ít DA focus"
#   RARE = "Industry này ít cần"
# Ky hieu de canh mau: nguoi kho phan biet mau van doc duoc muc do.
LEVELS = {
    "🔴": ("CORE",      "#DC2626", "#fff",    "●", "Có đội chuyên trách và ngân sách riêng"),
    "🟡": ("RELEVANT",  "#FB923C", "#3b1a02", "◐", "Có làm, nhưng không phải trọng tâm"),
    "⚪": ("MINIMAL",   "#FEF3C7", "#5a4708", "○", "Có bộ phận, ít đầu tư cho phân tích"),
    "➖": ("RARE",      "",        "",        "·", "Ngành này hiếm khi cần tới"),
}


def esc(s):
    return html_mod.escape(str(s).replace("\n", " ").strip())


def build():
    ws = openpyxl.load_workbook(XLSX, data_only=True)["Domain"]
    rows = list(ws.iter_rows(values_only=True))

    # Sheet co vai dong trong o dau, nen phai tim dong tieu de thay vi lay rows[0].
    head_i = next(i for i, r in enumerate(rows)
                  if r and r[0] and "Industry" in str(r[0]))
    header = [c for c in rows[head_i][1:] if c]
    rows = rows[head_i:]
    data = []
    for r in rows[1:]:
        label = str(r[0]).strip() if r[0] else ""
        # Bo dong chu giai ("🔴 CORE"...) va dong ghi chu cuoi bang
        if not label or label.startswith(tuple(LEVELS)) or "project" in label.lower():
            continue
        cells = list(r[1:1 + len(header)])
        # Duoi bang con cac dong dat ten project (M1, M2...) chi co mot o.
        # Dong nganh that phai gan du 10 o, va o phai la ky hieu muc do.
        marks = sum(1 for c in cells if c and str(c).strip() in LEVELS)
        if marks < len(header) - 1:
            continue
        data.append((label, cells))

    out = []
    out.append('    <!-- ' + MARK + ' -->')
    out.append('    <section style="max-width:1400px;margin:0 auto;padding:20px clamp(16px,4vw,56px) 70px">')
    out.append('      <div style="text-align:center;max-width:62ch;margin:0 auto">')
    out.append('        <span class="eyebrow"><span class="eyebrow__drum"></span>Học xong thì làm ở đâu</span>')
    out.append('        <h2 style="font-family:\'Space Grotesk\',sans-serif;font-weight:700;'
               'font-size:clamp(26px,3vw,40px);line-height:1.14;letter-spacing:-0.02em;margin:22px 0 0">'
               'Mười ngành, <span style="color:#DC2626">mỗi ngành ưu tiên một nhóm lĩnh vực khác nhau</span>.</h2>')
    out.append('        <p style="font-size:15.5px;line-height:1.75;margin:24px auto 0;'
               'color:color-mix(in srgb, var(--ink,#211d17) 72%, transparent)">'
               'Ô càng đậm, lĩnh vực đó càng nằm gần lõi hoạt động của ngành - thường có đội ngũ chuyên trách và ngân sách riêng.<br><br>'
               'Đọc theo hàng để biết một ngành cần những năng lực gì; đọc theo cột để xác định lĩnh vực bạn muốn theo đuổi '
               'đang được ưu tiên ở đâu.</p>')
    out.append('      </div>')

    # Chu giai
    out.append('      <div style="display:flex;flex-wrap:wrap;gap:10px 18px;justify-content:center;margin-top:26px">')
    for _, (name, bg, fg, sym, desc) in LEVELS.items():
        swatch = (f'background:{bg};color:{fg};' if bg
                  else 'background:transparent;border-style:dashed;')
        # O chu giai mang dung ky hieu nhu o trong bang, de doi chieu bang mat
        out.append(f'        <span style="display:inline-flex;align-items:center;gap:8px;font-size:12.5px;font-weight:600">'
                   f'<span style="width:16px;height:16px;{swatch}border:2px solid #2E1065;display:inline-flex;'
                   f'align-items:center;justify-content:center;font-size:9px;line-height:1">{sym}</span>'
                   f'{esc(name)} · <span style="font-weight:500;opacity:.75">{esc(desc)}</span></span>')
    out.append('      </div>')

    out.append('      <div style="margin-top:26px;overflow-x:auto;overflow-y:hidden">')
    out.append('        <table style="border-collapse:collapse;min-width:920px;width:100%;'
               'background:var(--surface,#fffdf9);border:3px solid #2E1065;'
               'box-shadow:5px 5px 0 #2E1065;font-size:12.5px">')

    # Dau bang: ten cot xoay doc cho vua be ngang
    out.append('          <thead><tr>')
    out.append('            <th style="border-bottom:2px solid #2E1065;border-right:2px solid #2E1065;'
               'padding:10px 12px;text-align:left;white-space:nowrap;position:sticky;left:0;'
               'background:var(--surface,#fffdf9);font-family:\'Space Grotesk\',sans-serif">Ngành</th>')
    for h in header:
        label = esc(h).replace(" Analytics", "")
        out.append('            <th style="border-bottom:2px solid #2E1065;padding:10px 6px;'
                   'font-family:\'Space Grotesk\',sans-serif;font-size:11.5px;line-height:1.25;'
                   f'min-width:72px">{label}</th>')
    out.append('          </tr></thead><tbody>')

    for industry, cells in data:
        out.append('          <tr>')
        out.append('            <td style="border-right:2px solid #2E1065;padding:9px 12px;font-weight:700;'
                   'white-space:nowrap;position:sticky;left:0;background:var(--surface,#fffdf9);'
                   f'font-family:\'Space Grotesk\',sans-serif">{esc(industry)}</td>')
        for c in cells:
            key = str(c).strip() if c else ""
            name, bg, fg, sym, _ = LEVELS.get(key, ("", "", "", "·", ""))
            if bg:
                # Truoc day o bang in name[:4] nen ra "RELE", "MINI" cut dau duoi.
                # Dung ky hieu tron ven, ten day du de o phan chu giai.
                style = f'background:{bg};color:{fg};font-weight:700;font-size:12px'
                text = sym
            else:
                style = 'color:color-mix(in srgb, var(--ink,#211d17) 28%, transparent)'
                text = '·'
            out.append(f'            <td style="text-align:center;padding:9px 4px;'
                       f'border-top:1px solid color-mix(in srgb, #2E1065 18%, transparent);{style}">{text}</td>')
        out.append('          </tr>')

    out.append('          </tbody></table>')
    out.append('      </div>')
    out.append('    </section>')
    return "\n".join(out) + "\n", len(data), len(header)


def splice(block):
    lines = HTML.read_text(encoding="utf-8").split("\n")
    hit = [i for i, l in enumerate(lines) if MARK in l]
    if hit:                                  # chay lai: thay dung khoi cu
        i = hit[0]
        end = next(j for j in range(i, len(lines)) if lines[j].strip() == "</section>")
        lines[i:end + 1] = block.rstrip("\n").split("\n")
    else:                                    # lan dau: chen ngay sau khoi so do tong quan
        anchor = next(i for i, l in enumerate(lines) if "So do tong quan — sinh boi" in l)
        end = next(j for j in range(anchor, len(lines)) if lines[j].strip() == "</section>")
        lines[end + 1:end + 1] = ["", *block.rstrip("\n").split("\n")]
    HTML.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    block, n_ind, n_dom = build()
    splice(block)
    print(f"da dung bang {n_ind} nganh x {n_dom} mang phan tich")
