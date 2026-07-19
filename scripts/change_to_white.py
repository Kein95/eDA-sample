import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. First 4 cards: change from var(--tint,#f1e5cf) to var(--surface,#fffdf9)
text = text.replace('background:var(--tint,#f1e5cf)', 'background:var(--surface,#fffdf9)')

# 2. Drive share card (Mở thư mục →)
# It has: background:#0891B2
# text color: color:#fff
# desc color: color:rgba(245,242,236,0.7)
# link color: color:#d9a860

drive_card_old = '''<a href="https://drive.google.com/drive/folders/1JlXxhr-m3yKF8m8oZxoSg5hcq77CwNMh?usp=sharing" target="_blank" rel="noopener" style-hover="transform:translate(-6px,-6px);box-shadow:8px 8px 0 var(--ink,#211d17)" style="position:relative;display:flex;flex-direction:column;gap:8px;background:#0891B2;border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);border-radius:0;padding:24px 26px;text-decoration:none;color:#f5f2ec;transition:all 0.2s;">
        <div style="position:absolute;top:-14px;right:-10px;background:#22c55e;color:#000;border:3px solid var(--ink,#211d17);padding:4px 10px;font-size:11px;font-weight:700;text-transform:uppercase;box-shadow:3px 3px 0 var(--ink,#211d17)">Drive Share</div>
        <span style="font-family:'Space Grotesk',sans-serif;font-weight:800;font-size:20px;letter-spacing:-0.02em;margin-top:8px;color:#fff">Nội dung &amp; tài liệu tham khảo</span>
        <span style="font-size:14px;line-height:1.65;font-weight:500;color:rgba(245,242,236,0.7);text-align:justify;display:block">Thư mục chia sẻ chính thức của chương trình, gồm nội dung học, tài liệu tham khảo và các bản demo.</span>
        <span style="font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:700;color:#d9a860;margin-top:auto;text-transform:uppercase;letter-spacing:0.05em">Mở thư mục →</span>
      </a>'''

drive_card_new = '''<a href="https://drive.google.com/drive/folders/1JlXxhr-m3yKF8m8oZxoSg5hcq77CwNMh?usp=sharing" target="_blank" rel="noopener" style-hover="transform:translate(-6px,-6px);box-shadow:8px 8px 0 var(--ink,#211d17)" style="position:relative;display:flex;flex-direction:column;gap:8px;background:var(--surface,#fffdf9);border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);border-radius:0;padding:24px 26px;text-decoration:none;color:var(--ink,#211d17);transition:all 0.2s;">
        <div style="position:absolute;top:-14px;right:-10px;background:#22c55e;color:#000;border:3px solid var(--ink,#211d17);padding:4px 10px;font-size:11px;font-weight:700;text-transform:uppercase;box-shadow:3px 3px 0 var(--ink,#211d17)">Drive Share</div>
        <span style="font-family:'Space Grotesk',sans-serif;font-weight:800;font-size:20px;letter-spacing:-0.02em;margin-top:8px;color:var(--ink,#211d17)">Nội dung &amp; tài liệu tham khảo</span>
        <span style="font-size:14px;line-height:1.65;font-weight:500;color:color-mix(in srgb, var(--ink,#211d17) 70%, transparent);text-align:justify;display:block">Thư mục chia sẻ chính thức của chương trình, gồm nội dung học, tài liệu tham khảo và các bản demo.</span>
        <span style="font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:700;color:var(--deep,#8a6228);margin-top:auto;text-transform:uppercase;letter-spacing:0.05em">Mở thư mục →</span>
      </a>'''

if drive_card_old in text:
    text = text.replace(drive_card_old, drive_card_new)
else:
    print("Could not find drive card.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Cards changed to white successfully.")
