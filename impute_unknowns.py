import os
import json
import re
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

source_dir = 'd:/OneDrive/Bridge stuff'

master_dict = {}

def update_bridge(b_id, row):
    if b_id not in master_dict:
        master_dict[b_id] = {}
    
    # Check common columns
    mapping = {
        'TypeDeck': 'type_deck',
        'TypeDeckMaterial': 'type_deck_material',
        'TypeAbutmentL': 'type_abutment_l',
        'TypeAbutmentR': 'type_abutment_r',
        'TypePiers': 'type_piers',
        'OVERALL RATING': 'overall_rating',
        'Overall Rating': 'overall_rating',
        'Road_Class': 'road_class',
        'TypeCrossing': 'type_crossing'
    }
    
    for col, attr in mapping.items():
        if col in row and pd.notna(row[col]) and str(row[col]).strip() != '':
            # Don't overwrite with 0 or Unknown if we already have a valid one
            val = row[col]
            if str(val) in ['0', '00', '?', 'Unknown', 'N/A']:
                continue
            master_dict[b_id][attr] = val

print("Scanning all excel and csv files...")
for root, dirs, files in os.walk(source_dir):
    # skip node_modules or output dirs
    if 'node_modules' in root or '.git' in root:
        continue
    for f in files:
        if f.endswith('.xlsx') or f.endswith('.xls'):
            path = os.path.join(root, f)
            if '~$' in f: continue
            try:
                xl = pd.read_excel(path, sheet_name=None, nrows=5000)
                for sheet, df in xl.items():
                    # Find a column that looks like bridge ID
                    id_col = None
                    for c in df.columns:
                        if str(c).lower() in ['bridge_no', 'bridgenumber', 'bridge no', 'new bridge number']:
                            id_col = c
                            break
                    if id_col:
                        for _, row in df.iterrows():
                            b_id = str(row[id_col]).strip()
                            if b_id:
                                update_bridge(b_id, row)
            except Exception as e:
                pass
        elif f.endswith('.csv'):
            path = os.path.join(root, f)
            try:
                df = pd.read_csv(path, nrows=5000)
                id_col = None
                for c in df.columns:
                    if str(c).lower() in ['bridge_no', 'bridgenumber', 'bridge no', 'new bridge number']:
                        id_col = c
                        break
                if id_col:
                    for _, row in df.iterrows():
                        b_id = str(row[id_col]).strip()
                        if b_id:
                            update_bridge(b_id, row)
            except Exception as e:
                pass

print(f"Built master dict for {len(master_dict)} bridges.")

print("Patching bridge_data.js...")
with open('d:/OneDrive/Bridge stuff/bridge_traffic_deploy/bridge_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

bridges_match = re.search(r'const BRIDGES = (\[.*?\]);', text, re.DOTALL)
bridges = json.loads(bridges_match.group(1))

patched = 0
for b in bridges:
    b_id = str(b.get('bridge_no')).strip()
    alt_id = str(b.get('new_bridge_no')).strip()
    
    updates = {}
    if b_id in master_dict:
        updates.update(master_dict[b_id])
    if alt_id in master_dict:
        updates.update(master_dict[alt_id])
        
    for k, v in updates.items():
        if not b.get(k) or str(b.get(k)) in ['0', '00', '?', 'Unknown', 'N/A']:
            b[k] = v
            patched += 1

print(f"Made {patched} patches to bridge attributes.")

new_bridges_json = json.dumps(bridges, indent=2)
text = text[:bridges_match.start(1)] + new_bridges_json + text[bridges_match.end(1):]

with open('d:/OneDrive/Bridge stuff/bridge_traffic_deploy/bridge_data.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done!")
