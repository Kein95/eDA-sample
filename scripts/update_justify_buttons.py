import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Justify the 3 paragraphs in "Vì sao chọn"
p1_old = '<p style="font-size:14.5px;line-height:1.7;margin:10px 0 0;color:rgba(255,255,255,0.9)">Không dừng ở dashboard - đi trọn con đường của một Data Analyst hiện đại: Excel, Power BI, SQL, pipeline, forecasting, đến khi tự tin nhận việc thật.</p>'
p1_new = '<p style="font-size:14.5px;line-height:1.7;margin:10px 0 0;color:rgba(255,255,255,0.9);text-align:justify">Không dừng ở dashboard - đi trọn con đường của một Data Analyst hiện đại: Excel, Power BI, SQL, pipeline, forecasting, đến khi tự tin nhận việc thật.</p>'
text = text.replace(p1_old, p1_new)

p2_old = '<p style="font-size:14.5px;line-height:1.7;margin:10px 0 0;color:rgba(255,255,255,0.9)">Một module riêng cho Agentic AI: dùng AI trong Excel, Power BI, SQL và toàn bộ quy trình phân tích - kỹ năng thị trường 2026 đòi hỏi.</p>'
p2_new = '<p style="font-size:14.5px;line-height:1.7;margin:10px 0 0;color:rgba(255,255,255,0.9);text-align:justify">Một module riêng cho Agentic AI: dùng AI trong Excel, Power BI, SQL và toàn bộ quy trình phân tích - kỹ năng thị trường 2026 đòi hỏi.</p>'
text = text.replace(p2_old, p2_new)

p3_old = '<p style="font-size:14.5px;line-height:1.7;margin:10px 0 0;color:rgba(255,255,255,0.9)">Nhóm mentorship theo ngành - phân tích dữ liệu của chính lĩnh vực bạn theo đuổi: Sales, Finance, Supply Chain, HR, Credit Risk.</p>'
p3_new = '<p style="font-size:14.5px;line-height:1.7;margin:10px 0 0;color:rgba(255,255,255,0.9);text-align:justify">Nhóm mentorship theo ngành - phân tích dữ liệu của chính lĩnh vực bạn theo đuổi: Sales, Finance, Supply Chain, HR, Credit Risk.</p>'
text = text.replace(p3_old, p3_new)

# fallback for generic replacement if exact match fails due to special chars:
text = re.sub(r'(<p style="font-size:14\.5px;line-height:1\.7;margin:10px 0 0;color:rgba\(255,255,255,0\.9\))(">)', r'\1;text-align:justify\2', text)


# 2. Update button background at line 1047
old_btn = 'background:var(--surface,#fffdf9);border:3px solid var(--ink,#211d17);box-shadow:4px 4px 0 var(--ink,#211d17);color:var(--ink,#211d17);transition:all .15s">Ưu đãi Early-bird</button>'
new_btn = 'background:#FDE047;border:3px solid var(--ink,#211d17);box-shadow:4px 4px 0 var(--ink,#211d17);color:var(--ink,#211d17);transition:all .15s">Ưu đãi Early-bird</button>'
text = text.replace(old_btn, new_btn)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Done")
