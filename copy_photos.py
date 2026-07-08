import os
import shutil
import json

source_dir = 'G:/My Drive/MOWT/Uganda National Road Network Repository/Bridge stuff/PHOTOS'
dest_dir = 'd:/OneDrive/Bridge stuff/bridge_traffic_deploy/PHOTOS'

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

print(f"Copying photos from {source_dir} to {dest_dir}...")
copied = 0
photos_map = {}

for root, dirs, files in os.walk(source_dir):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # get bridge ID from folder name or file name
            folder_name = os.path.basename(root)
            b_id = folder_name.split('_')[0].split(' ')[0]
            
            src_path = os.path.join(root, f)
            dest_path = os.path.join(dest_dir, f)
            
            # handle duplicates
            counter = 1
            final_dest = dest_path
            final_name = f
            while os.path.exists(final_dest):
                name, ext = os.path.splitext(f)
                final_name = f"{name}_{counter}{ext}"
                final_dest = os.path.join(dest_dir, final_name)
                counter += 1
                
            shutil.copy2(src_path, final_dest)
            copied += 1
            
            if b_id not in photos_map:
                photos_map[b_id] = []
            photos_map[b_id].append(f'PHOTOS/{final_name}')

print(f"Copied {copied} photos.")

js_content = "const PHOTOS_DATA = " + json.dumps(photos_map, indent=2) + ";\n"
with open('d:/OneDrive/Bridge stuff/bridge_traffic_deploy/photos_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Updated photos_data.js")
