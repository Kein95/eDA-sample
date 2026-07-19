import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Fix pillOpts
text = text.replace("bg: cur === label ? '#b68235' : '#fffdf9'", "bg: cur === label ? '#b68235' : 'var(--surface,#fffdf9)'")
text = text.replace("border: '#211d17'", "border: 'var(--ink,#211d17)'")

# Fix tab active background
text = text.replace("bg: t === i ? (this.isDark() ? '#f0ece3' : '#211d17') : 'transparent'", "bg: t === i ? (this.isDark() ? 'var(--ink,#f0ece3)' : 'var(--ink,#211d17)') : 'transparent'")
text = text.replace("color: t === i ? (this.isDark() ? '#14110c' : '#f5f2ec') : 'color-mix(in srgb, var(--ink,#211d17) 72%, transparent)'", "color: t === i ? 'var(--bg,#FAF9F7)' : 'color-mix(in srgb, var(--ink,#211d17) 72%, transparent)'")


with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Dark mode bugs fixed.")
