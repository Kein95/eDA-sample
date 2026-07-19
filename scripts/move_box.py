import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# The box HTML
box_html = '<div style="background:#f3f4f6;border:2.5px solid var(--ink,#211d17);box-shadow:3px 3px 0 var(--ink,#211d17);padding:12px 16px;margin:22px 0 0;font-size:13.5px;font-weight:600;color:var(--ink,#211d17);text-align:justify;max-width:100%">Lịch học bổ trợ và warm-up sẽ được gửi qua email sau khi đăng ký.<br>Tất cả buổi học đều có bản ghi dành cho học viên bận lịch.</div>'

if box_html in text:
    # Remove it from its current position
    text = text.replace(box_html, '')
    
    # We need to find the closing tag of the main grid.
    # The grid structure is:
    # <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:56px;align-items:start">
    #   <div> ... left ... </div>
    #   <div style="display:grid;gap:24px"> ... right ... </div>
    # </div>
    
    # We will search for the right column closing tags.
    # Wait, the easiest way is to find the Pre-Course right column content and its closing tags.
    
    search_str = 'Dashboard tự động với Python, Cloud và SQL</span><span style="font-size:12px;font-weight:600;color:var(--deep,#8a6228)">Dr. Đình Vinh</span></div></div></div>\n        </div>\n      </div>\n    </div>'
    
    new_box_html = '\n    <div style="background:#f3f4f6;border:2.5px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);padding:18px 24px;margin:32px 0 0;font-size:14.5px;font-weight:600;color:var(--ink,#211d17);text-align:center;width:100%;box-sizing:border-box">Lịch học bổ trợ và warm-up sẽ được gửi qua email sau khi đăng ký.<br>Tất cả buổi học đều có bản ghi dành cho học viên bận lịch.</div>'
    
    # Replace the closing of the grid with the closing + the new box
    text = text.replace(search_str, search_str + new_box_html)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Box moved to span full width.")
