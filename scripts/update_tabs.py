import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Expand Colophon box (line 853 equivalent)
text = text.replace(
    '<p style="text-align:justify;font-size:15px;line-height:1.7;color:rgba(245,242,236,0.6);margin:20px 0 0;max-width:65ch">',
    '<p style="text-align:justify;font-size:15px;line-height:1.7;color:rgba(245,242,236,0.6);margin:20px 0 0;max-width:100%">'
)

# 2. Timeline text & milestones - brutalist box
# The paragraph at line 874:
timeline_p = '<p style="text-align:justify;font-size:15px;line-height:1.75;margin:18px 0 0;color:color-mix(in srgb, var(--ink,#211d17) 70%, transparent)">Vòng ngoài gồm đúng 100 vạch'
# Replace the p tag with a wrapper box start
timeline_p_replacement = '<div style="background:var(--surface,#fffdf9);border:2.5px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);padding:24px 28px;margin:24px 0 0"><p style="text-align:justify;font-size:15px;line-height:1.75;margin:0;color:color-mix(in srgb, var(--ink,#211d17) 70%, transparent)">Vòng ngoài gồm đúng 100 vạch'
text = text.replace(timeline_p, timeline_p_replacement)

# Close the wrapper after the button at line 881. Wait, there's a button. Does the user want the button inside the box or outside?
# "Vòng ngoài gồm đúng... 05.2027 Final Exam... thiếu box". It implies the text and milestones. I will put the button inside the box as well, so close after the button.
# Let's search for the button:
btn_str = '<button type="button" onClick="{{ goRoadmap }}" style-hover="background:#b68235;color:#1c1710" style="cursor:pointer;white-space:nowrap;font-family:\'Space Grotesk\',sans-serif;font-weight:600;font-size:14px;padding:12px 22px;border-radius:999px;background:var(--tint,#f1e5cf);border:3px solid var(--ink,#211d17);color:var(--tintdeep,#7c5a24);transition:background .15s,color .15s;margin-top:26px">Mở lộ trình chi tiết →</button>'
text = text.replace(btn_str, btn_str + '</div>')

# 3. Khai giảng box color
# <div style="background:var(--tint,#f1e5cf);border:2.5px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);padding:18px 22px;margin:24px 0 0;max-width:100%">
box_tint = '<div style="background:var(--tint,#f1e5cf);border:2.5px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);padding:18px 22px;margin:24px 0 0;max-width:100%">'
box_surface = '<div style="background:var(--surface,#fffdf9);border:2.5px solid var(--ink,#211d17);box-shadow:5px 5px 0 var(--ink,#211d17);padding:18px 22px;margin:24px 0 0;max-width:100%">'
text = text.replace(box_tint, box_surface)


# 4. Trống đồng background for other tabs
# We'll inject the SVG drum into the top of the container for Tab 1, 2, 3, 4, 5
drum_bg = """
    <sc-if value="{{ dongSonOn }}" hint-placeholder-val="{{ true }}">
      <div style="position:absolute;top:100px;right:-150px;width:500px;height:500px;opacity:0.04;pointer-events:none;background:var(--ink,#211d17);-webkit-mask:url('assets/dongson-drum.svg') center/contain no-repeat;mask:url('assets/dongson-drum.svg') center/contain no-repeat;animation:drumspin 280s linear infinite"></div>
    </sc-if>
"""

tab_headers = [
    # Tab 1
    '<div style="animation:tabfade .35s ease both;max-width:1200px;margin:0 auto;padding:68px clamp(16px,4vw,56px) 90px;position:relative;overflow:hidden">',
    # Tab 2
    '<div style="animation:tabfade .35s ease both;max-width:1200px;margin:0 auto;padding:68px clamp(16px,4vw,56px) 90px;position:relative;overflow:hidden">',
    # Tab 3
    '<div style="animation:tabfade .35s ease both;max-width:1200px;margin:0 auto;padding:68px clamp(16px,4vw,56px) 90px">',
    # Tab 4
    '<div style="animation:tabfade .35s ease both;max-width:1200px;margin:0 auto;padding:68px clamp(16px,4vw,56px) 90px">',
    # Tab 5
    '<div style="animation:tabfade .35s ease both;max-width:1200px;margin:0 auto;padding:68px clamp(16px,4vw,56px) 90px">'
]

# Note: Some containers don't have position:relative and overflow:hidden. Let's add them to ensure the absolute positioned drum behaves correctly.
tab_container_regex = r'(<div style="animation:tabfade \.35s ease both;max-width:1200px;margin:0 auto;padding:68px clamp\(16px,4vw,56px\) 90px[^"]*")>'
def replacer(m):
    original_style = m.group(1)
    if 'position:relative' not in original_style:
        original_style = original_style + ';position:relative;overflow:hidden'
    return original_style + '>' + drum_bg

# But wait, Tab 1 and 2 already have position:relative;overflow:hidden in the source, so they will be matched.
# Tab 3, 4, 5 do not.
# We want to replace exactly after those container opening tags. Let's use re.sub but limit it so we don't mess up Tab 0.
# Wait, Tab 0 doesn't have `padding:68px clamp(16px,4vw,56px) 90px`. Only tabs 1-5 have it!
text = re.sub(tab_container_regex, replacer, text)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updates applied successfully.")
