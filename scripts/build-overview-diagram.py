# -*- coding: utf-8 -*-
"""Sinh so do tong quan eDA 2026, bam sat assets/Overview_eDA2026.jpg:
vong tron nang luc ben trai + pipeline 8 module ngang ben phai, callout co mui ten
dut net chi dung module, 5 nhom mau, nen hatch.

Moi cot (module + cac callout + mui ten cua no) nam trong mot <g class="dcol">
=> hien dan tung cot khi vao trang, va ro ca cot khi di chuot vao bat ky o nao.

Chay lai duoc nhieu lan: tu tim khoi da chen qua comment moc va thay dung 4 dong do.
"""
import io

from pathlib import Path
HTML = Path(__file__).resolve().parent.parent / "TuyenSinh-eDA2026.dc.html"

# ── Bang mau: (vien, nen hatch, mau vach hatch) ─────────────────────────────
PALETTE = {
    "blue":   ("#4472C4", "#EEF3FB", "#4472C4"),
    "green":  ("#548235", "#EFF6E8", "#70AD47"),
    "orange": ("#C55A11", "#FDF1E6", "#ED7D31"),
    "red":    ("#B01513", "#FCEDEC", "#C00000"),
    "gold":   ("#BF9000", "#FBF4DC", "#BF9000"),
}
MOD_GREEN = ("#548235", "#A9D18E")
MOD_BLUE  = ("#3B5FA8", "#9CB4E0")
MOD_PINK  = ("#B87C9C", "#E3A9C4")

SANS = "'Be Vietnam Pro',sans-serif"
HEAD = "'Space Grotesk',sans-serif"
INK  = "#211d17"

# ── Hinh hoc (canvas gon hon ban truoc: 1830 thay vi 2000) ──────────────────
W, H       = 1830, 780
PIPE_X0    = 455
MOD_W, SEP_W, NOTCH = 150, 18, 24
STEP       = MOD_W + SEP_W          # 168
BAND_TOP, BAND_BOT = 300, 400
BAND_MID   = (BAND_TOP + BAND_BOT) // 2

# Cac hang deu duoc tinh theo the CAO NHAT trong hang (xem phan "Bo cuc doc" ben duoi),
# vi chieu cao the phu thuoc so dong sau khi tu xuong dong. Gan so cung o day tung lam
# hang A bi cat mat goc tren va hang C dam vao hang D.
TOP_MARGIN = 10           # chua cho vien + bong cua the cao nhat hang A
ROW_AB_GAP = 30
ROW_C_TOP  = 436
ROW_CD_GAP = 26
BOX_W      = 152
BOX_PAD    = 16
BOLD_F     = 1.05         # chu dam rong hon chu thuong ~5%
FS_BOX     = 19
OFF_L, OFF_R = -56, 26    # hang 1 lech trai, hang 2 lech phai (de mui ten khong dam vao o)

# Uoc luong be rong ky tu theo em — du de tu xuong dong ma khong tran khung.
_NARROW = set("iljtfr.,;:'!|()[]/ ")
_WIDE   = set("MWmw@")

def text_w(s, fs):
    em = sum(0.30 if c in _NARROW else (0.88 if c in _WIDE else 0.56) for c in s)
    return em * fs

FS_MIN    = 15
MAX_LINES = 3             # the cao qua 3 dong se dam vao hang ke ben

def fit(lines, bold=False):
    """Chon co chu lon nhat ma noi dung van goi trong MAX_LINES dong.
    Co dinh co chu roi cho xuong dong tuy y tung lam the 5 dong dam vao pipeline."""
    for fs in range(FS_BOX, FS_MIN - 1, -1):
        wrapped = wrap(lines, bold, fs)
        if len(wrapped) <= MAX_LINES:
            return wrapped, fs
    return wrap(lines, bold, FS_MIN), FS_MIN

def line_gap(fs): return fs + 7
def box_h(n, fs):  return max(56, 16 + n * line_gap(fs))

def wrap(lines, bold=False, fs=FS_BOX):
    """Giu ngat dong chon tay, cat tiep bat ky dong nao con qua rong."""
    max_w = (BOX_W - BOX_PAD) / (BOLD_F if bold else 1.0)
    out_lines = []
    for raw in lines:
        cur = ""
        for word in raw.split(" "):
            cand = word if not cur else cur + " " + word
            if text_w(cand, fs) <= max_w or not cur:
                cur = cand
            else:
                out_lines.append(cur)
                cur = word
        if cur:
            out_lines.append(cur)
    return out_lines

def mod_x0(i): return PIPE_X0 + i * STEP
def col_c(i):  return mod_x0(i) + 84        # tam thi giac cua module

# ── Noi dung: {module: (cac dong chu, mau, in dam)} ─────────────────────────
ROW_A = {  # hang tren cung — domain
    0: (["Sales Domain"],                                  "blue",   False),
    1: (["Finance Domain"],                                "green",  False),
    2: (["Marketing Domain"],                              "orange", False),
    4: (["Supply Chain", "Domain"],                        "blue",   False),
    5: (["Automatic EDA"],                                 "blue",   True),
    6: (["Forecasting &", "Clustering &", "Anomaly Detection"], "gold", False),
    7: (["Lớp luyện", "PL 300"],                           "orange", True),
}
ROW_B = {  # hang 2 — cong cu / ky thuat
    0: (["DA Using Excel"],                                "blue",   False),
    1: (["DA Using", "Power BI"],                          "green",  False),
    2: (["SQL &", "BigQuery"],                             "orange", False),
    3: (["AI for Excel,", "Power BI, SQL,", "and DA Process"], "red", True),
    4: (["Advanced", "Knowledge", "for DA"],               "blue",   False),
    5: (["Data Pipeline"],                                 "blue",   True),
    6: (["Credit Risk", "Domain"],                         "gold",   False),
}
ROW_C = {  # duoi pipeline — soft skill / domain project
    0: (["Problem", "Framing Skill"],                      "blue",   False),
    1: (["Visualization", "& Storytelling"],               "green",  False),
    2: (["Stakeholder", "Management Skill"],               "orange", False),
    3: (["Game, EdTech,", "Marketing, and", "HR Domains"], "red",    False),
    4: (["Analysis &", "Business Mindset"],                "green",  False),
    5: (["Logical Thinking", "& Problem", "Solving for DA"], "blue",  False),
    6: (["Presentation", "& Teamwork Skills"],             "gold",   False),
    7: (["Lớp luyện AWS", "Cloud Practitioner"],           "orange", False),
}
ROW_D = {  # hang duoi cung — seminar
    0: (["Seminar:", "DA in Sales"],                       "blue",   False),
    1: (["Seminar:", "DA in Finance"],                     "green",  False),
    2: (["Seminar:", "DA in Marketing"],                   "orange", False),
    4: (["Seminar: DA in", "Supply Chain"],                "green",  False),
    5: (["Seminar: DA", "in Operations"],                  "blue",   False),
    6: (["Final Exam"],                                    "gold",   True),
}
MODULES = [
    ("Module 1", "Basic DA"),    ("Module 2", "Power BI"),
    ("Module 3", "SQL"),         ("Module 4", "AI; Domain"),
    ("Module 5", "Advanced DA"), ("Module 6", "DA+DE"),
    ("Module 7", "DA+DS"),       ("Module 8", "(Optional)"),
]

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ── Bo cuc doc: neo theo the cao nhat cua tung hang ─────────────────────────
def item_h(lines, bold):
    wrapped, fs = fit(lines, bold)
    return box_h(len(wrapped), fs)

def tallest(row):
    return max(item_h(lines, bold) for lines, _, bold in row.values())

ROW_A_BASE = TOP_MARGIN + tallest(ROW_A)          # day hang A; the moc nguoc len tu day
ROW_B_TOP  = ROW_A_BASE + ROW_AB_GAP
ROW_D_TOP  = ROW_C_TOP + tallest(ROW_C) + ROW_CD_GAP

# Cac the khong duoc dam vao bang chevron o giua, cung khong duoc tran khoi canvas.
assert ROW_B_TOP + tallest(ROW_B) < BAND_TOP, "hang B dam vao pipeline"
assert ROW_D_TOP + tallest(ROW_D) < 686, "hang D dam vao bang mentorship"

# Be rong an toan cho chu trong chevron: hai ben deu bi vat cheo NOTCH, va chevron
# hong ke tiep phu len phan mui ben phai. Chu rong hon muc nay se de len rìa hong.
# 106 la muc giu duoc "AI; Domain" tren mot dong nhu ban goc, ma "Advanced DA" (118)
# van phai xuong dong. O do cao dong phu de, ria hong bat dau tan x0+141 nen con du khe.
MOD_TEXT_W = 106
MOD_TEXT_DX = 76          # tam chu, lech trai hon tam hinh hoc de tranh mui nhon

out = io.StringIO()
w = out.write

w(f'<svg viewBox="0 0 {W} {H}" role="img" '
  f'aria-label="So do tong quan eDA 2026: bon tru cot nang luc va tam module gan domain, cong cu, soft skill, seminar" '
  f'style="display:block;width:100%;min-width:980px;max-width:1240px;margin:0 auto;height:auto">')

# ── CSS: hien dan tung cot + lam noi ca cot khi di chuot vao ────────────────
# Luu y: khong de hai dau } dinh nhau, tranh dung cu phap {{ }} cua dc-runtime.
w("<style>"
  ".dcol{animation:dcolIn .5s cubic-bezier(.2,.7,.3,1) both}"
  "@keyframes dcolIn{from{opacity:0;transform:translateY(14px)}"
  "to{opacity:1;transform:none}"
  "}"
  ".dband{animation:dcolIn .5s cubic-bezier(.2,.7,.3,1) .62s both}"
  ".dring{animation:dcolIn .55s cubic-bezier(.2,.7,.3,1) both}"
  ".cbox,.chev{transition:opacity .18s ease,stroke-width .18s ease}"
  ".arw{transition:opacity .18s ease,stroke-width .18s ease;animation:ants 1.2s linear infinite}"
  # Mo nhat cac cot khac khi dang tro vao mot cot => cot dang xem noi han.
  # Phai dung !important: animation dcolIn khoa opacity:1 o keyframe cuoi (fill both),
  # ma khai bao trong animation thang khai bao thuong trong tang bac cascade.
  # Va rule giu sang phai co do dac hieu cao hon rule lam mo (0-3-1 > 0-2-1).
  "svg:hover .dcol{opacity:.4!important}"
  "svg:hover .dcol:hover{opacity:1!important}"
  ".dcol:hover .cbox{stroke-width:3.2}"
  ".dcol:hover .arw{stroke-width:3}"
  "@keyframes ants{to{stroke-dashoffset:-26}"
  "}"
  "@media (prefers-reduced-motion:reduce){"
  ".dcol,.dband,.dring{animation:none}"
  ".dcol:hover .arw{animation:none}"
  "svg:hover .dcol{opacity:1!important}"
  "}"
  "</style>")

# ── defs: hatch cho tung mau ────────────────────────────────────────────────
w("<defs>")
for name, (_, bg, hatch) in PALETTE.items():
    w(f'<pattern id="hx-{name}" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
      f'<rect width="9" height="9" fill="{bg}"></rect>'
      f'<line x1="0" y1="0" x2="0" y2="9" stroke="{hatch}" stroke-width="1.2" stroke-opacity="0.32"></line>'
      f'</pattern>')
w('<pattern id="hx-circle" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
  '<rect width="9" height="9" fill="#F7F5EF"></rect>'
  '<line x1="0" y1="0" x2="0" y2="9" stroke="#70AD47" stroke-width="1" stroke-opacity="0.22"></line>'
  '</pattern>')
w("</defs>")

# ── Vong tron nang luc (trai) ───────────────────────────────────────────────
CX, CY, R, RI = 215, 330, 190, 66
w('<g class="dring">')
w(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#hx-circle)" stroke="#70AD47" stroke-width="2.2"></circle>')
k = 0.70711
for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
    w(f'<line x1="{CX + sx*RI*k:.1f}" y1="{CY + sy*RI*k:.1f}" '
      f'x2="{CX + sx*R*k:.1f}" y2="{CY + sy*R*k:.1f}" stroke="#70AD47" stroke-width="1.6"></line>')
for label, tx, ty in (
        (["Knowledge", "Domain"], CX, 196),
        (["Technical", "Skills"], CX + 128, 322),
        (["Soft", "Skills"],      CX, 448),
        (["AI"],                  CX - 128, 340)):
    # 24 la co chu lon nhat ma "Technical" con lot vua khe giua vong trong va vong ngoai (124 don vi)
    w(f'<text x="{tx}" y="{ty}" font-family="{HEAD}" font-size="24" font-weight="600" fill="{INK}" text-anchor="middle">')
    for j, ln in enumerate(label):
        w(f'<tspan x="{tx}" dy="{0 if j == 0 else 27}">{esc(ln)}</tspan>')
    w("</text>")
w(f'<circle cx="{CX}" cy="{CY}" r="{RI}" fill="#FFFDF9" stroke="#BF9000" stroke-width="2.2"></circle>')
for txt, dy, fs in (("End2End", -13, 19), ("Data", 9, 19), ("Analytics", 31, 19)):
    w(f'<text x="{CX}" y="{CY+dy}" font-family="{HEAD}" font-size="{fs}" font-weight="700" '
      f'fill="{INK}" text-anchor="middle">{esc(txt)}</text>')
w("</g>")

def arrow(x, y_from, y_to, color, up):
    head = 13
    tail_end = y_to + head if up else y_to - head
    w(f'<line class="arw" x1="{x}" y1="{y_from}" x2="{x}" y2="{tail_end}" stroke="{color}" '
      f'stroke-width="2" stroke-dasharray="7 6" stroke-opacity="0.9"></line>')
    tip_y = y_to
    off = head if up else -head
    w(f'<path d="M{x},{tip_y} L{x-7},{tip_y+off} L{x+7},{tip_y+off} Z" fill="{color}"></path>')

def callout(x_center, y_top, lines, color, bold):
    stroke = PALETTE[color][0]
    lines, fs = fit(lines, bold)
    gap = line_gap(fs)
    h = box_h(len(lines), fs)
    x = x_center - BOX_W // 2
    w(f'<rect class="cbox" x="{x}" y="{y_top}" width="{BOX_W}" height="{h}" rx="7" '
      f'fill="url(#hx-{color})" stroke="{stroke}" stroke-width="2"></rect>')
    fy = y_top + h / 2 - (len(lines) - 1) * gap / 2 + fs / 2 - 2
    w(f'<text x="{x_center}" y="{fy:.0f}" font-family="{SANS}" font-size="{fs}" '
      f'font-weight="{"700" if bold else "500"}" fill="{INK}" text-anchor="middle">')
    for j, ln in enumerate(lines):
        w(f'<tspan x="{x_center}" dy="{0 if j == 0 else gap}">{esc(ln)}</tspan>')
    w("</text>")
    return h

# ── 8 cot: module + chevron hong + 4 the callout + mui ten, moi cot mot <g> ──
for i, (title, sub) in enumerate(MODULES):
    w(f'<g class="dcol" style="animation-delay:{0.06 * i + 0.08:.2f}s">')

    x0, x1 = mod_x0(i), mod_x0(i) + MOD_W
    stroke, fill = MOD_GREEN if i % 2 == 0 else MOD_BLUE
    if i == 0:      # module dau canh trai phang, giong ban goc
        d = f"M{x0},{BAND_TOP} L{x1-NOTCH},{BAND_TOP} L{x1},{BAND_MID} L{x1-NOTCH},{BAND_BOT} L{x0},{BAND_BOT} Z"
    else:
        d = (f"M{x0},{BAND_TOP} L{x1-NOTCH},{BAND_TOP} L{x1},{BAND_MID} L{x1-NOTCH},{BAND_BOT} "
             f"L{x0},{BAND_BOT} L{x0+NOTCH},{BAND_MID} Z")
    w(f'<path class="chev" d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="1.8"></path>')

    ps, pf = MOD_PINK
    dp = (f"M{x1-NOTCH},{BAND_TOP} L{x1-NOTCH+SEP_W},{BAND_TOP} L{x1+SEP_W},{BAND_MID} "
          f"L{x1-NOTCH+SEP_W},{BAND_BOT} L{x1-NOTCH},{BAND_BOT} L{x1},{BAND_MID} Z")
    w(f'<path class="chev" d="{dp}" fill="{pf}" stroke="{ps}" stroke-width="1.5"></path>')

    # Ten module + phu de, phu de tu xuong dong neu rong hon vung an toan
    # ("Advanced DA" rong 124 > 100 nen tach thanh "Advanced" / "DA").
    tx = x0 + MOD_TEXT_DX
    sub_lines, cur = [], ""
    for word in sub.split(" "):
        cand = word if not cur else cur + " " + word
        if text_w(cand, 21) / BOLD_F <= MOD_TEXT_W or not cur:
            cur = cand
        else:
            sub_lines.append(cur)
            cur = word
    sub_lines.append(cur)

    rows = 1 + len(sub_lines)
    y0 = BAND_MID - (rows - 1) * 13 + 7
    w(f'<text x="{tx}" y="{y0}" font-family="{HEAD}" font-size="21" font-weight="700" '
      f'fill="#14110c" text-anchor="middle">{esc(title)}</text>')
    for j, ln in enumerate(sub_lines):
        w(f'<text x="{tx}" y="{y0 + 26 * (j + 1)}" font-family="{HEAD}" font-size="21" '
          f'font-weight="700" fill="#10239E" text-anchor="middle">{esc(ln)}</text>')

    cc = col_c(i)
    if i in ROW_A:
        lines, color, bold = ROW_A[i]
        ax, h = cc + OFF_L, item_h(lines, bold)   # hang A neo theo day nen can biet cao truoc
        callout(ax, ROW_A_BASE - h, lines, color, bold)      # hang A neo theo day
        arrow(ax, ROW_A_BASE, BAND_TOP - 4, PALETTE[color][0], up=False)
    if i in ROW_B:
        lines, color, bold = ROW_B[i]
        bx = cc + OFF_R
        h = callout(bx, ROW_B_TOP, lines, color, bold)
        arrow(bx, ROW_B_TOP + h, BAND_TOP - 4, PALETTE[color][0], up=False)
    if i in ROW_C:
        lines, color, bold = ROW_C[i]
        cx_ = cc + OFF_L
        callout(cx_, ROW_C_TOP, lines, color, bold)
        arrow(cx_, ROW_C_TOP, BAND_BOT + 4, PALETTE[color][0], up=True)
    if i in ROW_D:
        lines, color, bold = ROW_D[i]
        dx = cc + OFF_R
        callout(dx, ROW_D_TOP, lines, color, bold)
        arrow(dx, ROW_D_TOP, BAND_BOT + 4, PALETTE[color][0], up=True)

    w("</g>")

# ── Bang mentorship duoi cung ───────────────────────────────────────────────
by0, by1 = 686, 756
bx0, bx1 = PIPE_X0, mod_x0(7) + MOD_W + SEP_W
w(f'<g class="dband"><path d="M{bx0},{by0} L{bx1-52},{by0} L{bx1},{(by0+by1)//2} '
  f'L{bx1-52},{by1} L{bx0},{by1} Z" fill="url(#hx-gold)" stroke="#BF9000" stroke-width="2"></path>')
w(f'<text x="{(bx0+bx1)//2}" y="{(by0+by1)//2 + 9}" font-family="{HEAD}" font-size="26" '
  f'font-weight="700" fill="{INK}" text-anchor="middle">Domain-Focused Mentorship Groups</text></g>')
w("</svg>")

svg = out.getvalue()
assert "{{" not in svg, "SVG chua '{{' — se bi dc-runtime hieu nham la binding"

# ── Chen vao HTML ───────────────────────────────────────────────────────────
with open(HTML, "r", encoding="utf-8") as f:
    lines = f.readlines()

MARK = "So do tong quan - sinh boi gen-overview-svg.py"
new_block = (
    f'      <!-- {MARK} - cuon ngang tren man hinh hep -->\n'
    '      <div style="margin-top:34px;overflow-x:auto;overflow-y:hidden">\n'
    f'{svg}\n'
    '      </div>\n'
)

hit = [i for i, ln in enumerate(lines) if MARK in ln or "Full-bleed de so do ngang" in ln]
if hit:                                   # chay lai: thay dung khoi da chen (4 dong)
    i = hit[0]
    assert "</div>" in lines[i + 3], "khoi da chen khong con nguyen ven — dung lai de kiem tra"
    lines[i:i + 4] = [new_block]
else:                                     # lan dau
    old = "".join(lines[542:559])
    assert 'viewBox="0 0 360 360"' in old, "khong tim thay vong tron cu — dung lai de kiem tra"
    lines[542:559] = [new_block]

with open(HTML, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("SVG bytes:", len(svg), "| canvas:", f"{W}x{H}",
      "| callouts:", len(ROW_A) + len(ROW_B) + len(ROW_C) + len(ROW_D))
