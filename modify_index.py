import re

with open('index.html', 'r', encoding='utf-8') as f: html = f.read()

new_inner = """    <div class="card" style="height: 100%; overflow-y: auto;">
      <div class="card-title">Network Statistics &amp; Summary</div>
      <div class="card-subtitle">Categorical and numerical breakdowns of the bridge and major culvert inventory.</div>
      <div id="statisticsChartsContainer" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 16px; padding-bottom: 30px;"></div>
    </div>"""

html = re.sub(r'<div class="panel" id="panel-statistics">.*?</div>\s*</div>\s*<!-- PHOTOS PANEL -->', '<div class="panel" id="panel-statistics">\n' + new_inner + '\n  </div>\n\n  <!-- PHOTOS PANEL -->', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f: f.write(html)
print('Updated index.html')
