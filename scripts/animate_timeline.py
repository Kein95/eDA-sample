import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# For the 100 Buổi Live SVG, add a <style> right after <svg ...>
# We will target all paths with stroke-width="30" to make them dashed and animated.
style_block = """<style>
@keyframes march {
  to { stroke-dashoffset: -24; }
}
path[stroke-width="30"] {
  stroke-dasharray: 8 8 !important;
  animation: march 1.5s linear infinite;
}
</style>"""

svg_start = '<svg viewBox="0 0 680 680" style="width:100%;height:auto;display:block" role="img" aria-label="Vòng năm eDA 2026 - toàn bộ buổi học khắc quanh mặt trống">'
new_svg_start = svg_start + style_block

if svg_start in text and style_block not in text:
    text = text.replace(svg_start, new_svg_start)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Timeline SVG animated successfully!")
else:
    print("SVG start not found or already animated.")
