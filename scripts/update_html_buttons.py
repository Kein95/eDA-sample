import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update buttons
text = text.replace('color:#17140f;transition:all .15s">Đăng ký giữ chỗ →</button>', 'color:#fff;transition:all .15s">Đăng ký ngay →</button>')
text = text.replace('color:#fff;transition:all .15s">Đăng ký giữ chỗ →</button>', 'color:#fff;transition:all .15s">Đăng ký ngay →</button>')
text = text.replace('color:#fff;transition:all .15s;margin-top:26px">Giữ chỗ ngay →</button>', 'color:#fff;transition:all .15s;margin-top:26px">Đăng ký ngay →</button>')
text = text.replace('color:#17140f;transition:all .15s">Đăng ký giữ chỗ</button>', 'color:#fff;transition:all .15s">Đăng ký ngay</button>')
text = text.replace('color:#fff;transition:all .15s">Đăng ký giữ chỗ</button>', 'color:#fff;transition:all .15s">Đăng ký ngay</button>')
text = text.replace('color:#fff;transition:all .15s;margin-top:26px">Giữ chỗ ngay</button>', 'color:#fff;transition:all .15s;margin-top:26px">Đăng ký ngay</button>')


with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated HTML buttons")
