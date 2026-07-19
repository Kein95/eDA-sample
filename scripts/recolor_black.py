import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace the 08 icon background
icon_08 = '<span style="display:inline-flex;width:52px;height:52px;border-radius:14px;background:#111827;border:2.5px dashed var(--ink,#211d17);box-shadow:3px 3px 0 var(--ink,#211d17);align-items:center;justify-content:center;font-family:\'Space Grotesk\',sans-serif;font-weight:800;font-size:19px;color:#fff;font-variant-numeric:tabular-nums">08</span>'
icon_08_new = '<span style="display:inline-flex;width:52px;height:52px;border-radius:14px;background:#0891B2;border:2.5px dashed var(--ink,#211d17);box-shadow:3px 3px 0 var(--ink,#211d17);align-items:center;justify-content:center;font-family:\'Space Grotesk\',sans-serif;font-weight:800;font-size:19px;color:#fff;font-variant-numeric:tabular-nums">08</span>'
text = text.replace(icon_08, icon_08_new)

# Replace the Co-founder tag
cofounder = '<div style="position:absolute;top:-14px;right:-10px;background:#111827;color:#fff;border:3px solid var(--ink,#211d17);padding:4px 10px;font-size:11px;font-weight:700;text-transform:uppercase;box-shadow:3px 3px 0 var(--ink,#211d17)">Co-founder</div>'
cofounder_new = '<div style="position:absolute;top:-14px;right:-10px;background:#E11D48;color:#fff;border:3px solid var(--ink,#211d17);padding:4px 10px;font-size:11px;font-weight:700;text-transform:uppercase;box-shadow:3px 3px 0 var(--ink,#211d17)">Co-founder</div>'
text = text.replace(cofounder, cofounder_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Colors updated successfully.")
