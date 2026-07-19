import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Expand the Early Bird box
text = text.replace(
    "text-align:justify;max-width:90%",
    "text-align:justify;max-width:100%"
)

# 2. Hero sections: "8 module End2End..."
hero_style_1 = 'p style="text-align:justify;font-size:16.5px;line-height:1.75;max-width:65ch;margin:26px 0 0;color:color-mix(in srgb, var(--ink,#211d17) 72%, transparent);animation:rise .6s ease .38s both"'
hero_box_1 = 'div style="background:var(--surface,#fffdf9);border:2.5px solid var(--ink,#211d17);box-shadow:4px 4px 0 var(--ink,#211d17);padding:16px 20px;margin:26px 0 0;font-size:15px;line-height:1.7;color:var(--ink,#211d17);font-weight:500;text-align:justify;max-width:65ch;animation:rise .6s ease .38s both"'
text = text.replace(f'<{hero_style_1}>', f'<{hero_box_1}>')

hero_style_2 = 'p style="text-align:justify;font-size:16px;line-height:1.75;max-width:55ch;margin:24px 0 0;color:color-mix(in srgb, var(--ink,#211d17) 72%, transparent)"'
hero_box_2 = 'div style="background:var(--surface,#fffdf9);border:2.5px solid var(--ink,#211d17);box-shadow:4px 4px 0 var(--ink,#211d17);padding:16px 20px;margin:24px 0 0;font-size:15px;line-height:1.7;color:var(--ink,#211d17);font-weight:500;text-align:justify;max-width:55ch"'
text = text.replace(f'<{hero_style_2}>', f'<{hero_box_2}>')

# Fix closing tags for Hero sections. Since the paragraphs are immediately followed by <div style="display:flex..., we can regex replace the </p> right before it.
text = re.sub(r'</p>\s*(?=<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:3[04]px)', r'</div>\n        ', text)

# 3. Domain description box
domain_style = 'p style="text-align:justify;font-size:15.5px;line-height:1.75;margin:24px auto 0;color:color-mix(in srgb, var(--ink,#211d17) 72%, transparent)"'
domain_box = 'div style="background:var(--tint,#f1e5cf);border:2.5px solid var(--ink,#211d17);box-shadow:4px 4px 0 var(--ink,#211d17);padding:16px 20px;margin:24px auto 0;font-size:14.5px;line-height:1.7;color:var(--ink,#211d17);font-weight:500;text-align:justify;max-width:62ch"'
text = text.replace(f'<{domain_style}>Ô càng đậm', f'<{domain_box}>Ô càng đậm')
# Replace </p> for Domain box
text = text.replace('đang được ưu tiên ở đâu.</p>', 'đang được ưu tiên ở đâu.</div>')

# 4. Zoom text box
zoom_style = 'p style="text-align:justify;font-size:15.5px;line-height:1.75;margin:20px 0 0;color:color-mix(in srgb, var(--ink,#211d17) 72%, transparent);max-width:50ch"'
zoom_box = 'div style="background:var(--surface,#fffdf9);border:2.5px solid var(--ink,#211d17);box-shadow:4px 4px 0 var(--ink,#211d17);padding:16px 20px;margin:20px 0 0;font-size:14.5px;line-height:1.7;color:var(--ink,#211d17);font-weight:500;text-align:justify;max-width:55ch"'
text = text.replace(f'<{zoom_style}>Lớp học trực tiếp qua Zoom', f'<{zoom_box}>Lớp học trực tiếp qua Zoom')
# Replace </p> for Zoom box
text = text.replace('trợ sát sao qua nhóm học tập.</p>', 'trợ sát sao qua nhóm học tập.</div>')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Boxes added successfully.")
