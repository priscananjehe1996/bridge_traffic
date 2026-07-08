import os
import json
import collections

source_dir = 'G:/My Drive/MOWT/Uganda National Road Network Repository/Bridge stuff/PHOTOS'

photos_by_id = collections.defaultdict(list)

print(f"Scanning {source_dir}...")

for root, _, files in os.walk(source_dir):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            # The bridge ID is usually the folder name or prefix
            folder_name = os.path.basename(root)
            
            # Parse from filename
            parts = f.split('_')
            bridge_id = parts[0].strip().upper()
            
            # Use folder name if it matches Bxxx pattern and filename doesn't
            if not bridge_id.startswith('B') and folder_name.startswith('B'):
                bridge_id = folder_name
                
            # Still valid if it starts with B or C (Bridges, Culverts)
            if bridge_id.startswith('B') or bridge_id.startswith('C'):
                # Handle spaces or strange characters
                bridge_id = bridge_id.split(' ')[0]
                
                # Construct absolute file URI
                abs_path = os.path.join(root, f).replace('\\', '/')
                # Modern browsers use file:/// for absolute paths
                file_uri = f"file:///{abs_path}"
                
                photos_by_id[bridge_id].append(file_uri)

print(f"Found {sum(len(v) for v in photos_by_id.values())} photos.")

js_content = f"const PHOTOS_DATA = {json.dumps(photos_by_id, indent=2)};\n"
with open('d:/OneDrive/Bridge stuff/bridge_traffic_deploy/photos_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Done generating photos_data.js!")
