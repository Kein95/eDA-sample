import sys

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Block 1
text = text.replace("End2End thật sự", "End-to-End thực chiến")
text = text.replace(
    "Không dừng ở dashboard - đi trọn con đường của một Data Analyst hiện đại: Excel, Power BI, SQL, pipeline, forecasting, đến khi tự tin nhận việc thật.",
    "Không dừng lại ở dashboard. Bạn sẽ đi trọn quy trình của một Data Analyst hiện đại: từ Excel, Power BI và SQL đến data pipeline, forecasting và triển khai bài toán thực tế - đủ tự tin để nhận việc và tạo ra kết quả."
)

# Block 2
text = text.replace("Agentic AI trong DA", "Agentic AI trong Data Analytics")
text = text.replace(
    "Một module riêng cho Agentic AI: dùng AI trong Excel, Power BI, SQL và toàn bộ quy trình phân tích - kỹ năng thị trường 2026 đòi hỏi.",
    "Một module chuyên biệt về Agentic AI, giúp bạn ứng dụng AI trong Excel, Power BI, SQL và toàn bộ quy trình phân tích dữ liệu - năng lực ngày càng quan trọng trên thị trường lao động năm 2026."
)

# Block 3
text = text.replace("Mentor theo domain", "Mentorship theo domain")
text = text.replace(
    "Nhóm mentorship theo ngành - phân tích dữ liệu của chính lĩnh vực bạn theo đuổi: Sales, Finance, Supply Chain, HR, Credit Risk…",
    "Tham gia nhóm mentorship chuyên sâu theo đúng lĩnh vực bạn muốn theo đuổi. Bạn sẽ phân tích dữ liệu và giải quyết các bài toán thực tế trong Sales, Finance, Supply Chain, HR, Credit Risk và nhiều ngành khác."
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Done updates for Why section")
