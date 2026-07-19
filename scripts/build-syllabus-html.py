# -*- coding: utf-8 -*-
"""docs/eDA-2026-Syllabus.md  ->  docs/eDA-2026-Syllabus.html

Vi sao can: may chu tinh serve .md voi Content-Type application/octet-stream,
nen bam "Mo tai lieu" thi trinh duyet TAI VE thay vi mo ra doc. Ban .html mo
duoc o moi noi ma khong phai chinh cau hinh may chu.

File .md van la ban goc. Sua .md xong thi chay lai script nay.
    python scripts/build-syllabus-html.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "eDA-2026-Syllabus.md"
DST = ROOT / "docs" / "eDA-2026-Syllabus.html"

# Theme Dong Son, dung lai bien mau cua trang tuyen sinh.
CSS = """
:root{--bg:#f5f2ec;--ink:#211d17;--surface:#fffdf9;--gold:#b68235;--deep:#8a6228;--line:#e0d8c8;--dot:rgba(33,29,23,0.15)}
@media (prefers-color-scheme:dark){
:root{--bg:#14110c;--ink:#f0ebe1;--surface:#1e1913;--line:#3a3227;--dot:rgba(255,255,255,0.08)}
}
*{box-sizing:border-box}
body{margin:0;background-color:var(--bg);background-image:radial-gradient(var(--dot) 2px, transparent 2px);background-size:24px 24px;color:var(--ink);
  font:16px/1.75 'Be Vietnam Pro',system-ui,-apple-system,Segoe UI,sans-serif;
  padding:clamp(24px,5vw,64px) clamp(16px,5vw,32px)}
main{max-width:920px;margin:0 auto;background:var(--surface);border:3px solid var(--ink);box-shadow:8px 8px 0 var(--ink);padding:clamp(20px,4vw,48px)}
h1{font-family:'Space Grotesk',system-ui,sans-serif;font-size:clamp(28px,4vw,42px);
  line-height:1.15;letter-spacing:-.02em;margin:0 0 16px;text-transform:uppercase}
h2{font-family:'Space Grotesk',system-ui,sans-serif;font-size:clamp(20px,2.6vw,26px);
  letter-spacing:-.01em;margin:56px 0 20px;padding:12px 20px;border:3px solid var(--ink);background:var(--gold);color:#1c1710;box-shadow:4px 4px 0 var(--ink)}
h3{font-family:'Space Grotesk',system-ui,sans-serif;font-size:19px;margin:32px 0 12px;display:inline-block;border-bottom:3px solid var(--ink)}
p{margin:12px 0}
em{color:var(--deep);font-style:normal;font-weight:600;font-size:14.5px;background:var(--line);padding:2px 6px;border:2px solid var(--ink)}
ul{list-style:none;padding:0;margin:16px 0}
li{margin:10px 0;padding-left:32px;position:relative}
li::before{content:"";position:absolute;left:8px;top:10px;width:10px;height:10px;background:var(--gold);border:2px solid var(--ink)}
a{color:var(--deep);text-decoration:none;border-bottom:2px solid var(--ink);font-weight:700;transition:all 0.15s}
a:hover{background:var(--ink);color:var(--surface)}
code{background:color-mix(in srgb,var(--ink) 8%,transparent);padding:2px 6px;border:2px solid var(--ink);font-size:14px;font-weight:700}
.tablewrap{overflow-x:auto;margin:24px 0;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;min-width:520px;background:var(--surface);
  border:3px solid var(--ink);font-size:14.5px}
th,td{border-bottom:2px solid var(--ink);border-right:2px solid var(--ink);padding:12px 16px;text-align:left;vertical-align:top}
th{background:color-mix(in srgb,var(--gold) 20%,transparent);font-weight:700;
  font-family:'Space Grotesk',system-ui,sans-serif;white-space:nowrap}
tr:last-child td{border-bottom:0}
td:last-child,th:last-child{border-right:0}
td:first-child,th:first-child{width:1%;white-space:nowrap;color:var(--deep);font-weight:700}
.back{display:inline-block;margin-bottom:32px;font-weight:700;font-size:15px;text-decoration:none;
  border:3px solid var(--ink);padding:10px 20px;background:var(--gold);color:#1c1710;box-shadow:4px 4px 0 var(--ink);transition:transform 0.15s, box-shadow 0.15s}
.back:hover{transform:translate(-4px,-4px);box-shadow:8px 8px 0 var(--ink);background:var(--ink);color:var(--surface)}
"""


def inline(text: str) -> str:
    """Chuyen phan dinh dang trong mot dong. Escape truoc, chen the sau."""
    out = html.escape(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<em>\1</em>", out)
    out = re.sub(r"`(.+?)`", r"<code>\1</code>", out)
    out = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', out)
    return out


def split_row(line: str):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def convert(md: str) -> str:
    lines = md.split("\n")
    out, i, title = [], 0, "Syllabus"

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Bang: dong "|...|" theo sau boi dong ngan cach "|---|"
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s\-:|]+\|$", lines[i + 1].strip()):
            head = split_row(stripped)
            i += 2
            body = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                body.append(split_row(lines[i].strip()))
                i += 1
            out.append('<div class="tablewrap"><table><thead><tr>'
                       + "".join(f"<th>{inline(c)}</th>" for c in head)
                       + "</tr></thead><tbody>")
            for row in body:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
            out.append("</tbody></table></div>")
            continue

        # Danh sach gach dau dong
        if stripped.startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].strip().startswith("- "):
                out.append(f"<li>{inline(lines[i].strip()[2:])}</li>")
                i += 1
            out.append("</ul>")
            continue

        m = re.match(r"^(#{1,3})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            text = inline(m.group(2))
            if level == 1 and title == "Syllabus":
                title = re.sub(r"<[^>]+>", "", text)
            out.append(f"<h{level}>{text}</h{level}>")
        elif stripped:
            out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    return (
        "<!doctype html>\n<html lang=\"vi\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
        f"<title>{html.escape(title)}</title>\n"
        "<link rel=\"icon\" href=\"../assets/logo-mark.png\">\n"
        "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
        "<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n"
        "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?"
        "family=Space+Grotesk:wght@400;600;700&family=Be+Vietnam+Pro:wght@400;600;700&display=swap\">\n"
        f"<style>{CSS}</style>\n</head>\n<body>\n<main>\n"
        "<a class=\"back\" href=\"../TuyenSinh-eDA2026.dc.html\">← Về trang tuyển sinh</a>\n"
        + "\n".join(out)
        + "\n</main>\n</body>\n</html>\n"
    )


if __name__ == "__main__":
    DST.write_text(convert(SRC.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"{SRC.name} -> {DST.name} ({DST.stat().st_size:,} bytes)")
