import json
import re
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from shapely.ops import nearest_points

print("Loading shapefile...")
# Load the road network
roads = gpd.read_file('d:/OneDrive/Bridge stuff/network2026/network2026.shp')

# Ensure spatial index is built
roads.sindex

print("Reading bridge_data.js...")
with open('bridge_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

bridges_match = re.search(r'const BRIDGES = (\[.*?\]);', text, re.DOTALL)
culverts_match = re.search(r'const MAJOR_CULVERTS = (\[.*?\]);', text, re.DOTALL)

bridges = json.loads(bridges_match.group(1))
culverts = json.loads(culverts_match.group(1))

def process_structures(structs):
    print(f"Processing {len(structs)} structures...")
    # Create GeoDataFrame for structures in WGS84
    geometry = [Point(s.get('x_new', s.get('map_x', 0)), s.get('y_new', s.get('map_y', 0))) for s in structs]
    gdf_structs = gpd.GeoDataFrame(structs, geometry=geometry, crs="EPSG:4326")
    
    # Project to EPSG:32636
    gdf_structs_utm = gdf_structs.to_crs(roads.crs)
    
    for idx, row in gdf_structs_utm.iterrows():
        point = row.geometry
        if point.is_empty:
            continue
            
        # Find nearest road
        nearest_idx = roads.sindex.nearest(point)[1][0]
        nearest_road = roads.iloc[nearest_idx]
        
        # Snap point to nearest road
        snapped_point = nearest_road.geometry.interpolate(nearest_road.geometry.project(point))
        
        # Convert snapped point back to WGS84
        snapped_point_wgs84 = gpd.GeoSeries([snapped_point], crs=roads.crs).to_crs("EPSG:4326").iloc[0]
        
        # Update struct dictionary
        s = structs[idx]
        s['x_new'] = snapped_point_wgs84.x
        s['y_new'] = snapped_point_wgs84.y
        s['map_x'] = snapped_point_wgs84.x
        s['map_y'] = snapped_point_wgs84.y
        s['link_no'] = nearest_road.get('Link_ID_1', s.get('link_no'))
        s['road_no'] = nearest_road.get('Road_No_1', s.get('road_no'))
        s['link_name'] = nearest_road.get('Link_Name', s.get('link_name'))
        s['station'] = nearest_road.get('Maintena_2', s.get('station'))
        s['region'] = nearest_road.get('Maintena_3', s.get('region'))
        s['road_class'] = nearest_road.get('Road_Cla_1', s.get('road_class'))
        
        # Interpolate chainage
        fraction = nearest_road.geometry.project(point, normalized=True)
        start_chain = nearest_road.get('Chainage_1', 0)
        end_chain = nearest_road.get('Chainage_2', nearest_road.get('Length_km_', 0))
        try:
            ch_val = start_chain + fraction * (end_chain - start_chain)
            s['km'] = round(ch_val, 3)
            s['chainage_validated_km'] = round(ch_val, 3)
        except:
            pass

process_structures(bridges)
process_structures(culverts)

print("Writing back to bridge_data.js...")
new_bridges_json = json.dumps(bridges, indent=2)
new_culverts_json = json.dumps(culverts, indent=2)

text = text[:bridges_match.start(1)] + new_bridges_json + text[bridges_match.end(1):]
culverts_match = re.search(r'const MAJOR_CULVERTS = (\[.*?\]);', text, re.DOTALL)
text = text[:culverts_match.start(1)] + new_culverts_json + text[culverts_match.end(1):]

with open('bridge_data.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done!")
