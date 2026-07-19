import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Expand the "Project & tài liệu" box
old_box = "Project &amp; tài liệu đọc của chương trình được chia sẻ công khai - mở thử để thấy chất lượng thực.<br>Học viên chính thức nhận đầy đủ tài liệu, dữ liệu và code theo từng module.</div>"
new_box = old_box # to check if it's there
# wait, the exact tag is:
# <div style="background:#e0f2fe;border:3px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);padding:16px 20px;margin:22px 0 0;font-size:15px;line-height:1.7;font-weight:500;color:var(--ink,#211d17);text-align:justify;max-width:58ch">Project &amp; tài liệu đọc...

text = text.replace("text-align:justify;max-width:58ch\">Project &amp; tài liệu đọc của chương trình", "text-align:justify;max-width:100%\">Project &amp; tài liệu đọc của chương trình")


# 2. Box for the hero text
old_hero_p = """        <p style="font-size:16.5px;line-height:1.75;max-width:56ch;margin:26px 0 0;color:rgba(245,242,236,0.72);animation:rise .6s ease .38s both">
          8 module End2End - Excel, Power BI, SQL, Agentic AI, data pipeline, forecasting.<br>
          Mỗi module một domain thật, một project thật.<br>
          Học online buổi tối, hợp cả học sinh, sinh viên và người đi làm.
        </p>"""

new_hero_div = """        <div style="font-size:16px;line-height:1.75;max-width:56ch;margin:26px 0 0;color:rgba(245,242,236,0.9);animation:rise .6s ease .38s both;background:rgba(255,255,255,0.04);border:2px solid rgba(255,255,255,0.2);box-shadow:5px 5px 0 rgba(255,255,255,0.15);padding:20px 24px;backdrop-filter:blur(4px)">
          8 module End2End - Excel, Power BI, SQL, Agentic AI, data pipeline, forecasting.<br>
          Mỗi module một domain thật, một project thật.<br>
          Học online buổi tối, hợp cả học sinh, sinh viên và người đi làm.
        </div>"""

text = text.replace(old_hero_p, new_hero_div)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updates applied")
