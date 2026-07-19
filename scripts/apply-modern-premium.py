# -*- coding: utf-8 -*-
import re
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "TuyenSinh-eDA2026.dc.html"
html = HTML.read_text(encoding="utf-8")

# 1. Soft shadows instead of hard solid blocks
# box-shadow: 4px 4px 0 #2E1065 -> dynamic soft shadow
def replace_shadow(m):
    val_str = m.group(1)
    if val_str.startswith('-'): val_str = val_str[1:] # absolute value
    offset = float(val_str) if '.' in val_str else int(val_str)
    
    blur = offset * 5
    y_off = offset * 2
    opacity = 12 if offset > 4 else 6
    
    return f"box-shadow:0 {y_off}px {blur}px color-mix(in srgb, var(--ink,#211d17) {opacity}%, transparent)"

html = re.sub(
    r'box-shadow:\s*(-?[\d.]+)px\s+-?[\d.]+px\s+0\s+(?:#[0-9a-fA-F]{3,6}|var\(--ink[^)]*\))',
    replace_shadow,
    html
)

# 2. Subtle 1px borders instead of thick neo-brutalist borders
html = re.sub(
    r'border:\s*[\d.]+(?:px)?\s+(?:solid|dashed)\s+(?:#[0-9a-fA-F]{3,6}|var\(--ink[^)]*\))',
    r'border:1px solid color-mix(in srgb, var(--ink,#211d17) 12%, transparent)',
    html
)

# 3. Increase border radius for smoother cards
html = html.replace('border-radius:0', 'border-radius:24px')
html = html.replace('border-radius:14px', 'border-radius:24px')
html = html.replace('border-radius:12px', 'border-radius:20px')

# 4. Glassmorphism on main surfaces
html = html.replace(
    'background:var(--surface,#fffdf9)',
    'background:color-mix(in srgb, var(--surface,#fffdf9) 65%, transparent);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px)'
)

# 5. Remove Neo-brutalist tilts (transform: rotate(...))
html = re.sub(r'transform:\s*rotate\(-?[\d.]+deg\)\s*;?', '', html)
html = html.replace('transform:rotate(0deg) ', 'transform:')
html = html.replace('translate(-2px,-2px)', 'translateY(-6px)')
html = html.replace('translate(-4px,-4px)', 'translateY(-8px)')

# 6. Animated Mesh-like Background Gradient
bg_animation = """
    @keyframes gradientMove {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
"""
if "gradientMove" not in html:
    html = html.replace('/* Animations */', '/* Animations */\n' + bg_animation)

old_applyBody = r"applyBody\(\)\s*\{\s*document\.body\.style\.background\s*=\s*this\.isDark\(\)\s*\?\s*'linear-gradient\([^']+\)'\s*:\s*'linear-gradient\([^']+\)';\s*document\.body\.style\.backgroundAttachment\s*=\s*'fixed';\s*\}"

new_applyBody = """applyBody() {
    document.body.style.background = this.isDark() 
      ? 'linear-gradient(-45deg, #1f112e, #11091b, #150d22, #0d0914)' 
      : 'linear-gradient(-45deg, #f8f5ff, #fff2f6, #eef0fc, #fdf5f5)';
    document.body.style.backgroundSize = '400% 400%';
    document.body.style.animation = 'gradientMove 15s ease infinite';
    document.body.style.backgroundAttachment = 'fixed';
  }"""
html = re.sub(old_applyBody, new_applyBody, html)

# The initial CSS rule for body
html = re.sub(
    r'body\s*\{\s*margin:\s*0;\s*background:\s*linear-gradient[^;]+;\s*background-attachment:\s*fixed;',
    r'body { margin: 0; background: linear-gradient(-45deg, #f8f5ff, #fff2f6, #eef0fc, #fdf5f5); background-size: 400% 400%; animation: gradientMove 15s ease infinite; background-attachment: fixed;',
    html
)

# 7. Upgrade buttons to look premium instead of flat boxes
# Existing buttons (like hover states)
html = html.replace('background:var(--gold)', 'background:linear-gradient(135deg, var(--gold), var(--deep));color:#fff;border:none')

HTML.write_text(html, encoding="utf-8")
print("Successfully applied modern premium glassmorphism style.")
