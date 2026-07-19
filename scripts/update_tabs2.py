import re

file_path = "D:/Projects/eDA/TuyenSinh-eDA2026.dc.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# First fix the syntax error in Tabs 3, 4, 5
text = text.replace(
    '90px";position:relative;overflow:hidden>',
    '90px;position:relative;overflow:hidden">'
)
# Make sure we don't duplicate the drum if it was already added somewhere.
# I will just manually inject the drum bg after these exact strings.

drum_bg = """
    <sc-if value="{{ dongSonOn }}" hint-placeholder-val="{{ true }}">
      <div style="position:absolute;top:100px;right:-150px;width:500px;height:500px;opacity:0.04;pointer-events:none;background:var(--ink,#211d17);-webkit-mask:url('assets/dongson-drum.svg') center/contain no-repeat;mask:url('assets/dongson-drum.svg') center/contain no-repeat;animation:drumspin 280s linear infinite"></div>
    </sc-if>
"""

tab_str = '<div style="animation:tabfade .35s ease both;max-width:1200px;margin:0 auto;padding:68px clamp(16px,4vw,56px) 90px;position:relative;overflow:hidden">'

# But wait, Tab 1 and Tab 2 might ALREADY have the drum bg if I ran a previous script?
# Let's clean up any existing drum_bg first to avoid duplication.
text = re.sub(
    r'\s*<sc-if value="\{\{ dongSonOn \}\}" hint-placeholder-val="\{\{ true \}\}">\s*<div style="position:absolute;top:100px;right:-150px[^>]+></div>\s*</sc-if>',
    '', text
)

# Now inject it back to all 5 tabs.
# The tab_str appears 5 times (now that we fixed the typo)
text = text.replace(tab_str, tab_str + drum_bg)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Tabs fixed and updated successfully.")
