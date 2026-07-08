import json
import re
import pandas as pd
import math

js_file = 'd:/OneDrive/Bridge stuff/bridge_traffic_deploy/bridge_data.js'
with open(js_file, 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const BRIDGES = (\[.*?\]);', text, re.DOTALL)
if not m:
    print("Could not parse BRIDGES from JS.")
    exit(1)

bridges = json.loads(m.group(1))

# Find highest existing B*** number
max_b = 0
for b in bridges:
    b_no = str(b.get('bridge_no', ''))
    if re.match(r'^B\d{3}$', b_no):
        num = int(b_no[1:])
        if num > max_b:
            max_b = num

# Fix bridge numbers
renamed = {}
for b in bridges:
    b_no = str(b.get('bridge_no', ''))
    if not re.match(r'^B\d{3}$', b_no):
        # We need to assign a new number
        max_b += 1
        new_no = f'B{max_b:03d}'
        renamed[b_no] = new_no
        b['original_bad_bridge_no'] = b_no
        b['bridge_no'] = new_no
        b['_id'] = f'bridge-{new_no}'

print(f"Renamed {len(renamed)} bad bridge numbers. Max B is now B{max_b:03d}.")

# Correct missing attributes from National Road Network
try:
    df_net = pd.read_excel('d:/OneDrive/Bridge stuff/National Road Network_ July 2026.xlsx')
    # Build dictionary
    net_dict = {}
    for i, row in df_net.iterrows():
        link_id = str(row.get('Link_ID', ''))
        if link_id and link_id != 'nan':
            net_dict[link_id] = {
                'road_no': row.get('Road_No'),
                'road_class': row.get('Road_Class'),
                'link_name': row.get('Link_Name'),
                'surface_link': row.get('Surface_Type'),
                'station': row.get('Maintenance_Station'),
                'region': row.get('Maintenance_Region'),
                'pave_age': row.get('Pavement Age')
            }
    
    updated_attrs = 0
    for b in bridges:
        link_no = b.get('link_no')
        if link_no in net_dict:
            nd = net_dict[link_no]
            if pd.notna(nd['road_no']): b['road_no'] = str(nd['road_no'])
            if pd.notna(nd['road_class']): b['road_class'] = str(nd['road_class'])
            if pd.notna(nd['link_name']): b['link_name'] = str(nd['link_name'])
            if pd.notna(nd['surface_link']): b['surface_link'] = str(nd['surface_link'])
            if pd.notna(nd['station']): b['station'] = str(nd['station'])
            if pd.notna(nd['region']): b['region'] = str(nd['region'])
            if pd.notna(nd['pave_age']): b['pave_age'] = float(nd['pave_age'])
            updated_attrs += 1
            
    print(f"Updated attributes for {updated_attrs} bridges using National Road Network data.")
except Exception as e:
    print("Error reading network excel:", e)

# Write back
new_json = json.dumps(bridges, indent=2)
new_text = text[:m.start(1)] + new_json + text[m.end(1):]

with open(js_file, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Saved bridge_data.js")
