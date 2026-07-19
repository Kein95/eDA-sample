import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Ticker tape
# <div style="border-top:3px solid var(--ink,#211d17);border-bottom:3px solid var(--ink,#211d17);overflow:hidden;display:flex;padding:15px 0;background:#111827;color:#fff" aria-hidden="true">
ticker_old = 'background:#111827;color:#fff" aria-hidden="true"'
ticker_new = 'background:#b68235;color:var(--ink,#211d17)" aria-hidden="true"'
text = text.replace(ticker_old, ticker_new)

# 2. 27 Buổi tặng
# <div style="background:#111827;border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);border-radius:0;padding:24px 26px;transition:transform 0.2s,box-shadow 0.2s" style-hover="transform:translate(-4px,-4px);box-shadow:8px 8px 0 var(--ink,#211d17)">
card_27_old = 'background:#111827;border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);border-radius:0;padding:24px 26px;transition:transform 0.2s,box-shadow 0.2s" style-hover="transform:translate(-4px,-4px);box-shadow:8px 8px 0 var(--ink,#211d17)"><p style="text-align:justify;font-family:\'Space Grotesk\',sans-serif;font-weight:700;font-size:clamp(40px,4vw,56px);line-height:1;color:#fff;margin:0;font-variant-numeric:tabular-nums">27</p>'
card_27_new = 'background:#2563EB;border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);border-radius:0;padding:24px 26px;transition:transform 0.2s,box-shadow 0.2s" style-hover="transform:translate(-4px,-4px);box-shadow:8px 8px 0 var(--ink,#211d17)"><p style="text-align:justify;font-family:\'Space Grotesk\',sans-serif;font-weight:700;font-size:clamp(40px,4vw,56px);line-height:1;color:#fff;margin:0;font-variant-numeric:tabular-nums">27</p>'
text = text.replace(card_27_old, card_27_new)

# 3. Nội dung & tài liệu tham khảo card
# <a href="https://drive.google.com/drive/folders/1JlXxhr-m3yKF8m8oZxoSg5hcq77CwNMh?usp=sharing" target="_blank" rel="noopener" style-hover="transform:translate(-6px,-6px);box-shadow:8px 8px 0 var(--ink,#211d17)" style="position:relative;display:flex;flex-direction:column;gap:8px;background:var(--ink,#211d17);border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);border-radius:0;padding:24px 26px;text-decoration:none;color:#f5f2ec;transition:all 0.2s;">
card_drive_old = 'background:var(--ink,#211d17);border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);border-radius:0;padding:24px 26px;text-decoration:none;color:#f5f2ec;transition:all 0.2s;">'
card_drive_new = 'background:#0891B2;border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);border-radius:0;padding:24px 26px;text-decoration:none;color:#f5f2ec;transition:all 0.2s;">'
text = text.replace(card_drive_old, card_drive_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated the remaining black boxes.")
