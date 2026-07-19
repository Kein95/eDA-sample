import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Change the 4 document cards back from pastel to var(--tint,#f1e5cf)
text = text.replace('background:#FCA5A5', 'background:var(--tint,#f1e5cf)')
text = text.replace('background:#93C5FD', 'background:var(--tint,#f1e5cf)')
text = text.replace('background:#86EFAC', 'background:var(--tint,#f1e5cf)')
text = text.replace('background:#FDE047', 'background:var(--tint,#f1e5cf)')

# 2. Change 27 Buổi tặng from #2563EB (same as 8 Module) to #DC2626 (Red)
# First let's locate the 27 Buổi tặng box.
search_27 = 'background:#2563EB;border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);border-radius:0;padding:24px 26px;transition:transform 0.2s,box-shadow 0.2s" style-hover="transform:translate(-4px,-4px);box-shadow:8px 8px 0 var(--ink,#211d17)"><p style="text-align:justify;font-family:\'Space Grotesk\',sans-serif;font-weight:700;font-size:clamp(40px,4vw,56px);line-height:1;color:#fff;margin:0;font-variant-numeric:tabular-nums">27</p>'
replace_27 = 'background:#DC2626;border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);border-radius:0;padding:24px 26px;transition:transform 0.2s,box-shadow 0.2s" style-hover="transform:translate(-4px,-4px);box-shadow:8px 8px 0 var(--ink,#211d17)"><p style="text-align:justify;font-family:\'Space Grotesk\',sans-serif;font-weight:700;font-size:clamp(40px,4vw,56px);line-height:1;color:#fff;margin:0;font-variant-numeric:tabular-nums">27</p>'

if search_27 in text:
    text = text.replace(search_27, replace_27)
else:
    print("Could not find the exact 27 Buoi tang block.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Colors updated successfully.")
