import os
import shutil
import json
import collections
from pathlib import Path

source_dir = 'G:/My Drive/MOWT/Uganda National Road Network Repository/Bridge stuff/PHOTOS'
target_dir = 'd:/OneDrive/Bridge stuff/bridge_traffic_deploy/photos'

os.makedirs(target_dir, exist_ok=True)

photos_by_id = collections.defaultdict(list)

print(f"Scanning {source_dir}...")
copied = 0

for root, _, files in os.walk(source_dir):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            # The bridge ID is usually the folder name or prefix
            folder_name = os.path.basename(root)
            # Or parse from filename
            parts = f.split('_')
            bridge_id = parts[0].strip().upper()
            
            # Use folder name if it matches Bxxx pattern and filename doesn't
            if not bridge_id.startswith('B') and folder_name.startswith('B'):
                bridge_id = folder_name
                
            # Still valid if it starts with B or C (Bridges, Culverts)
            if bridge_id.startswith('B') or bridge_id.startswith('C'):
                # Handle spaces or strange characters
                bridge_id = bridge_id.split(' ')[0]
                
                # To prevent naming collisions, append folder name if needed, or just use filename
                new_filename = f
                # if the filename is generic like "photo1.jpg", it might collide. But let's assume they are unique enough
                # Wait, to be safe, let's prefix with bridge ID if it's not there
                if not new_filename.upper().startswith(bridge_id):
                    new_filename = f"{bridge_id}_{f}"
                    
                photos_by_id[bridge_id].append(f'photos/{new_filename}')
                
                src_path = os.path.join(root, f)
                dst_path = os.path.join(target_dir, new_filename)
                
                if not os.path.exists(dst_path):
                    shutil.copy2(src_path, dst_path)
                    copied += 1

print(f"Copied {copied} new images. Total photos mapped: {sum(len(v) for v in photos_by_id.values())}")

js_content = f"const PHOTOS_DATA = {json.dumps(photos_by_id, indent=2)};\n"
with open('d:/OneDrive/Bridge stuff/bridge_traffic_deploy/photos_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Done!")
