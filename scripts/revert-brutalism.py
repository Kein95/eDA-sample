# -*- coding: utf-8 -*-
import re
import random
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "TuyenSinh-eDA2026.dc.html"
html = HTML.read_text(encoding="utf-8")

# 1. Revert glass shadows back to hard neo-brutalist drop shadows
def revert_shadow(m):
    # m.group(1) is y_off, e.g., "16"
    y_off = int(m.group(1))
    orig = y_off // 2
    return f"box-shadow:{orig}px {orig}px 0 var(--ink,#211d17)"

html = re.sub(
    r'box-shadow:0 (\d+)px \d+px color-mix\(in srgb, var\(--ink,#211d17\) \d+%, transparent\)',
    revert_shadow,
    html
)

# 2. Revert borders back to thick solid lines
html = re.sub(
    r'border:1px solid color-mix\(in srgb, var\(--ink,#211d17\) 12%, transparent\)',
    r'border:3px solid var(--ink,#211d17)',
    html
)

# Replace any `#0f172a` back to `var(--ink,#211d17)` (which was the purple/slate we added)
html = html.replace('#0f172a', 'var(--ink,#211d17)')

# 3. Revert border radii to sharp/retro (0 or 8px)
html = html.replace('border-radius:24px', 'border-radius:0')
html = html.replace('border-radius:20px', 'border-radius:0')

# 4. Remove glassmorphism background
html = html.replace(
    'background:color-mix(in srgb, var(--surface,#fffdf9) 65%, transparent);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px)',
    'background:var(--surface,#fffdf9)'
)

# 5. Revert hover transitions (translateY back to diagonal translate)
html = html.replace('translateY(-6px)', 'translate(-4px,-4px)')
html = html.replace('translateY(-8px)', 'translate(-6px,-6px)')

# 6. Revert background to a TRENDY NEO-BRUTALIST dotted pattern!
old_applyBody = r"applyBody\(\)\s*\{[\s\S]*?backgroundAttachment = 'fixed';\s*\}"

new_applyBody = """applyBody() {
    const isDark = this.isDark();
    const bg = isDark ? '#14110c' : '#f5f2ec';
    const dot = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(33,29,23,0.15)';
    document.body.style.backgroundColor = bg;
    document.body.style.backgroundImage = `radial-gradient(${dot} 2px, transparent 2px)`;
    document.body.style.backgroundSize = '24px 24px';
    document.body.style.backgroundPosition = '0 0';
  }"""
html = re.sub(old_applyBody, new_applyBody, html)

# The initial CSS rule for body
html = re.sub(
    r'body\s*\{\s*margin:\s*0;\s*background:\s*linear-gradient[^;]+;\s*background-size:[^;]+;\s*animation:[^;]+;\s*background-attachment:\s*fixed;',
    r'body { margin: 0; background-color: #f5f2ec; background-image: radial-gradient(rgba(33,29,23,0.15) 2px, transparent 2px); background-size: 24px 24px; text-wrap: pretty; -webkit-font-smoothing: antialiased;',
    html
)

# Remove the gradientMove animation from CSS
html = re.sub(r'@keyframes gradientMove \{[\s\S]*?\}', '', html)

# Let's add slight random rotations back to the big cards to make it truly RetroUI/Neo-brutalist
# Look for cards with border:3px solid var(--ink,#211d17);box-shadow...
def add_tilt(m):
    tilt = round(random.uniform(-1.5, 1.5), 1)
    if abs(tilt) < 0.5: tilt = 1.2
    return m.group(0) + f';transform:rotate({tilt}deg)'

# Instead of random regex, I'll just let CSS do the work if needed.
# Let's just write back the HTML.

HTML.write_text(html, encoding="utf-8")
print("Successfully restored Neo-brutalism / RetroUI style with dotted background!")
