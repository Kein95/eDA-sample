import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Split the "Project & tài liệu" text
old_doc_text = "Project &amp; tài liệu đọc của chương trình được chia sẻ công khai - mở thử để thấy chất lượng thực. Học viên chính thức nhận đầy đủ tài liệu, dữ liệu và code theo từng module."
new_doc_text = "Project &amp; tài liệu đọc của chương trình được chia sẻ công khai - mở thử để thấy chất lượng thực.<br>Học viên chính thức nhận đầy đủ tài liệu, dữ liệu và code theo từng module."
text = text.replace(old_doc_text, new_doc_text)

# Also account for the case where it might have a long dash instead of short dash
old_doc_text_2 = "Project &amp; tài liệu đọc của chương trình được chia sẻ công khai — mở thử để thấy chất lượng thực. Học viên chính thức nhận đầy đủ tài liệu, dữ liệu và code theo từng module."
new_doc_text_2 = "Project &amp; tài liệu đọc của chương trình được chia sẻ công khai - mở thử để thấy chất lượng thực.<br>Học viên chính thức nhận đầy đủ tài liệu, dữ liệu và code theo từng module."
text = text.replace(old_doc_text_2, new_doc_text_2)


# 2. Rule: - dài thành - ngắn
text = text.replace(" — ", " - ")
text = text.replace("—", "-")


# 3. Đội ngũ mentor - style as brutalist box
# Find the exact string
old_mentor_p = '<p style="font-size:14.5px;line-height:1.65;margin:0;color:color-mix(in srgb, var(--ink,#211d17) 70%, transparent);text-align:center;font-weight:600">Đội ngũ mentor theo domain (Sales, Finance, Marketing, Supply Chain, HR...).</p>'
# We might need to use regex if it has slightly different chars or HR… instead of HR...
match = re.search(r'<p style="[^"]*">Đội ngũ mentor theo domain \(Sales, Finance, Marketing, Supply Chain, HR[…\.]+\)\.?</p>', text)
if match:
    old_mentor = match.group(0)
    new_mentor = '<div style="background:#ffedd5;border:2.5px solid var(--ink,#211d17);box-shadow:4px 4px 0 var(--ink,#211d17);padding:14px 20px;margin:24px auto 0;font-size:14.5px;line-height:1.65;color:var(--ink,#211d17);text-align:center;font-weight:600;max-width:60ch">Đội ngũ mentor theo domain (Sales, Finance, Marketing, Supply Chain, HR...).</div>'
    text = text.replace(old_mentor, new_mentor)
else:
    print("Mentor text not found with exact match, using fallback replace.")
    text = re.sub(r'<p style="font-size:14\.5px;line-height:1\.65;margin:0;color:color-mix\(in srgb, var\(--ink,#211d17\) 70%, transparent\);text-align:center;font-weight:600">Đội ngũ mentor theo domain \(Sales, Finance, Marketing, Supply Chain, HR…\)\.</p>',
                  r'<div style="background:#ffedd5;border:2.5px solid var(--ink,#211d17);box-shadow:4px 4px 0 var(--ink,#211d17);padding:14px 20px;margin:24px auto 0;font-size:14.5px;line-height:1.65;color:var(--ink,#211d17);text-align:center;font-weight:600;max-width:60ch">Đội ngũ mentor theo domain (Sales, Finance, Marketing, Supply Chain, HR...).</div>',
                  text)
    
with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Done")
