import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

ticker_old = 'background:#b68235;color:var(--ink,#211d17)" aria-hidden="true"'
ticker_new = 'background:var(--surface,#fffdf9);color:var(--ink,#211d17)" aria-hidden="true"'

if ticker_old in text:
    text = text.replace(ticker_old, ticker_new)
else:
    print("Could not find the ticker.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Ticker tape color updated successfully.")
