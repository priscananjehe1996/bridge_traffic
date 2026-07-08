with open('old_index_b678d36.html', 'r', encoding='utf-16') as f:
    lines = f.readlines()

traffic_start, traffic_end, od_start, od_end = -1, -1, -1, -1

for i, line in enumerate(lines):
    if 'panel-bridge-traffic' in line and 'class=' in line and 'id=' in line:
        traffic_start = i
    if '<!-- /panel-bridge-traffic -->' in line:
        traffic_end = i
    
    if 'panel-od-matrix' in line and 'class=' in line and 'id=' in line:
        od_start = i
    if '<!-- /panel-od-matrix -->' in line:
        od_end = i

print(traffic_start, traffic_end, od_start, od_end)

if traffic_start != -1 and traffic_end != -1:
    with open('bridge_traffic_panel.html', 'w', encoding='utf-8') as f:
        f.writelines(lines[traffic_start:traffic_end+1])

if od_start != -1 and od_end != -1:
    with open('od_matrix_panel.html', 'w', encoding='utf-8') as f:
        f.writelines(lines[od_start:od_end+1])
