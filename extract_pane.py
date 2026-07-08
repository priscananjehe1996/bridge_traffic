import sys

with open('pane.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'bridgeAnalyticsPane' in line:
        start = i
        while start > 0 and 'class="map-side-pane"' not in lines[start]:
            start -= 1
        end = i
        while end < len(lines) and 'map-workspace' not in lines[end]:
            end += 1
        with open('pane_extracted.txt', 'w', encoding='utf-8') as outf:
            outf.write(''.join(lines[start:end-1]))
        break
