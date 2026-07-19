import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Fix double text-align
text = text.replace("text-align:justify;background:#ffedd5;border:2.5px solid var(--ink,#211d17);box-shadow:4px 4px 0 var(--ink,#211d17);padding:14px 20px;margin:24px auto 0;font-size:14.5px;line-height:1.65;color:var(--ink,#211d17);text-align:center;",
                    "background:#ffedd5;border:2.5px solid var(--ink,#211d17);box-shadow:4px 4px 0 var(--ink,#211d17);padding:14px 20px;margin:24px auto 0;font-size:14.5px;line-height:1.65;color:var(--ink,#211d17);text-align:justify;")

# The form container has text-align:left;
text = text.replace("text-align:justify;background:var(--surface,#fffdf9);border:3px solid var(--ink,#211d17);padding:24px;margin:32px auto 0;max-width:440px;text-align:left;",
                    "background:var(--surface,#fffdf9);border:3px solid var(--ink,#211d17);padding:24px;margin:32px auto 0;max-width:440px;text-align:left;") # We probably want left for the form

# Let's ensure all paragraph tags are justified
# A more robust regex to find all <p> without justify and add it, unless they are specific headers.
def justify_all_ps():
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "<p " in line and "text-align" not in line and "eyebrow" not in line:
            lines[i] = re.sub(r'<p style="', r'<p style="text-align:justify;', line)
        if "text-align:justify;" in line and "text-align:center" in line:
            lines[i] = line.replace("text-align:center", "")
        if "text-align:justify;" in line and "text-align:left" in line:
             lines[i] = line.replace("text-align:left", "")
    return "\n".join(lines)

text = justify_all_ps()

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Cleaned up text alignment")
