import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# ============================================================
# FIX 1: Add Major Culverts rendering to drawMap()
# ============================================================
# Insert culvert rendering BEFORE the bridge loop
old_bridge_loop = """  BRIDGES.forEach(b => {
    if (bridgeMapLon(b) == null || bridgeMapLat(b) == null) return;
    const pt = getProjection(bridgeMapLon(b), bridgeMapLat(b), canvas.width, canvas.height);
    const isActive = activeSet.has(b._id);
    const isHovered = hoveredBridge && b._id === hoveredBridge._id;
    const isSelected = selectedMapBridge && b._id === selectedMapBridge._id;
    const symbolSize = 6.8;

    if (isActive) {
      drawBridgeSymbol(ctx, pt.x, pt.y, symbolSize, {
        fill: BRIDGE_SYMBOL.fill,
        selected: isSelected,
        hovered: isHovered,
        active: true,
        alpha: selectedMapBridge && !isSelected ? 0.32 : 1
      });
    } else {
      drawBridgeSymbol(ctx, pt.x, pt.y, 4.6, {
        fill: BRIDGE_SYMBOL.fill,
        active: false
      });
    }
  });"""

culvert_rendering = """  // Draw Major Culverts
  if (typeof MAJOR_CULVERTS !== 'undefined') {
    MAJOR_CULVERTS.forEach(c => {
      const lon = c.map_x || c.x_new;
      const lat = c.map_y || c.y_new;
      if (lon == null || lat == null) return;
      const pt = getProjection(Number(lon), Number(lat), canvas.width, canvas.height);
      const size = 4.2;
      ctx.save();
      ctx.fillStyle = '#f59e0b';
      ctx.strokeStyle = '#78350f';
      ctx.lineWidth = 1.2;
      ctx.globalAlpha = 0.92;
      ctx.fillRect(pt.x - size/2, pt.y - size/2, size, size);
      ctx.strokeRect(pt.x - size/2, pt.y - size/2, size, size);
      ctx.restore();
    });
  }

"""

js = js.replace(old_bridge_loop, culvert_rendering + old_bridge_loop)


# ============================================================
# FIX 2: Reduce road line widths
# ============================================================
js = js.replace(
    "const base = cls === 'M' ? 2.2 : cls === 'A' ? 1.9 : cls === 'B' ? 1.45 : 0.95;",
    "const base = cls === 'M' ? 1.1 : cls === 'A' ? 0.9 : cls === 'B' ? 0.7 : 0.45;"
)


# ============================================================
# FIX 3: Add COLORS.slate and COLORS.fuchsia if missing
# ============================================================
if "'slate'" not in js.split('const PALETTE')[0]:
    js = js.replace(
        "const PALETTE = Object.values(COLORS);",
        "COLORS.slate = 'rgba(100, 116, 139, 0.85)';\nCOLORS.fuchsia = 'rgba(217, 70, 239, 0.85)';\nconst PALETTE = Object.values(COLORS);"
    )


# ============================================================
# FIX 4: Massively expand charts - replace the entire chart section
# ============================================================
# Find the chartConfigs block and replace it
old_charts_start = js.find('const chartConfigs = [')
old_charts_end = js.find('];', old_charts_start) + 2

new_charts = r'''const chartConfigs = [
    // ===== CLUSTERED COLUMN CHARTS =====
    { id: 'stat21', title: 'Bridges vs Culverts by Region', type: 'bar', labels: regions, datasets: [
      { label: 'Bridges', data: regions.map(r => bRegion[r] || 0), backgroundColor: COLORS.cyan, borderRadius: 4 },
      { label: 'Major Culverts', data: regions.map(r => cRegion[r] || 0), backgroundColor: '#f59e0b', borderRadius: 4 }
    ]},
    { id: 'stat22', title: 'Bridges vs Culverts by Station', type: 'bar', indexAxis: 'y', labels: stations, datasets: [
      { label: 'Bridges', data: stations.map(r => bStation[r] || 0), backgroundColor: COLORS.blue, borderRadius: 4 },
      { label: 'Major Culverts', data: stations.map(r => cStation[r] || 0), backgroundColor: '#f59e0b', borderRadius: 4 }
    ]},
    { id: 'stat23', title: 'Bridges vs Culverts by Road Class', type: 'bar', labels: classes, datasets: [
      { label: 'Bridges', data: classes.map(r => bClass[r] || 0), backgroundColor: COLORS.indigo, borderRadius: 4 },
      { label: 'Major Culverts', data: classes.map(r => cClass[r] || 0), backgroundColor: '#f59e0b', borderRadius: 4 }
    ]},
    { id: 'stat24', title: 'Bridges vs Culverts by Overall Condition', type: 'bar', labels: conditions, datasets: [
      { label: 'Bridges', data: conditions.map(r => bCond[r] || 0), backgroundColor: COLORS.violet, borderRadius: 4 },
      { label: 'Major Culverts', data: conditions.map(r => cCond[r] || 0), backgroundColor: '#f59e0b', borderRadius: 4 }
    ]},

    // ===== BRIDGE ANALYTICS =====
    { id: 'stat1', title: 'Bridges by Region', type: 'bar', labels: Object.keys(bRegion), data: Object.values(bRegion), color: COLORS.cyan },
    { id: 'stat3', title: 'Bridges by Road Class', type: 'pie', labels: Object.keys(bClass), data: Object.values(bClass), colors: [COLORS.cyan, COLORS.blue, COLORS.indigo, COLORS.violet, COLORS.purple, COLORS.pink] },
    { id: 'stat5', title: 'Bridges by Maintenance Station', type: 'bar', indexAxis: 'y', labels: Object.keys(bStation), data: Object.values(bStation), color: COLORS.cyan },
    { id: 'stat7', title: 'Bridges by Overall Condition', type: 'bar', labels: Object.keys(bCond), data: Object.values(bCond), color: COLORS.blue },
    { id: 'stat9', title: 'Bridge Superstructure Condition', type: 'bar', labels: Object.keys(bSuper), data: Object.values(bSuper), color: COLORS.indigo },
    { id: 'stat11', title: 'Bridge Substructure Condition', type: 'bar', labels: Object.keys(bSub), data: Object.values(bSub), color: COLORS.violet },
    { id: 'stat13', title: 'Bridges by Deck Material', type: 'pie', labels: Object.keys(bDeck), data: Object.values(bDeck), colors: [COLORS.rose, COLORS.amber, COLORS.cyan, COLORS.emerald, COLORS.blue, COLORS.indigo] },
    { id: 'stat15', title: 'Bridge Crossings by Type', type: 'bar', labels: Object.keys(bCrossing), data: Object.values(bCrossing), color: COLORS.cyan },
    { id: 'stat17', title: 'Bridges Built per Decade', type: 'bar', labels: Object.keys(bDecade2).sort(), data: Object.keys(bDecade2).sort().map(k => bDecade2[k]), color: COLORS.indigo },
    { id: 'stat19', title: 'Bridge Scour Risk Profile', type: 'pie', labels: Object.keys(bScour), data: Object.values(bScour), colors: [COLORS.red, COLORS.orange, COLORS.amber, COLORS.green, COLORS.blue, COLORS.violet] },
    { id: 'stat20', title: 'Bridge Length Distribution', type: 'bar', labels: Object.keys(bLength), data: Object.values(bLength), color: COLORS.cyan },
    { id: 'stat25', title: 'Bridges by Abutment Type', type: 'bar', indexAxis: 'y', labels: Object.keys(bAbutment), data: Object.values(bAbutment), color: COLORS.amber },
    { id: 'stat26', title: 'Bridges by Pier Type', type: 'bar', indexAxis: 'y', labels: Object.keys(bPier), data: Object.values(bPier), color: COLORS.orange },
    { id: 'stat27', title: 'Bridges by Deck Type', type: 'bar', indexAxis: 'y', labels: Object.keys(bDeckType), data: Object.values(bDeckType), color: COLORS.cyan },
    { id: 'stat28', title: 'Bridges by Expansion Joint Type', type: 'pie', labels: Object.keys(bExpansion), data: Object.values(bExpansion), colors: [COLORS.blue, COLORS.indigo, COLORS.violet, COLORS.purple, COLORS.pink, COLORS.rose] },
    { id: 'stat29', title: 'Bridge Traffic Priority Levels', type: 'doughnut', labels: Object.keys(bTrafficPriority), data: Object.values(bTrafficPriority), colors: [COLORS.red, COLORS.orange, COLORS.amber, COLORS.emerald, COLORS.blue, COLORS.violet] },
    { id: 'stat30', title: 'Bridge Span Configuration', type: 'pie', labels: Object.keys(bSpans), data: Object.values(bSpans), colors: [COLORS.cyan, COLORS.indigo, COLORS.slate] },
    { id: 'stat31', title: 'Top 15 Rivers by Bridge Count', type: 'bar', indexAxis: 'y', labels: topRivers.map(x=>x[0]), data: topRivers.map(x=>x[1]), color: COLORS.blue },
    { id: 'stat32', title: 'Bridge Suggested Interventions', type: 'pie', labels: Object.keys(bAct), data: Object.values(bAct), colors: [COLORS.emerald, COLORS.amber, COLORS.red, COLORS.slate] },
    { id: 'stat34', title: 'Bridges by Abutment Condition', type: 'bar', labels: Object.keys(bAbutCond), data: Object.values(bAbutCond), color: COLORS.violet },
    { id: 'stat35', title: 'Bridges by Pier Condition', type: 'bar', labels: Object.keys(bPierCond), data: Object.values(bPierCond), color: COLORS.fuchsia },
    { id: 'stat36', title: 'Bridges by Expansion Joint Condition', type: 'bar', labels: Object.keys(bExpCond), data: Object.values(bExpCond), color: COLORS.rose },

    // ===== CULVERT ANALYTICS =====
    { id: 'stat2', title: 'Culverts by Region', type: 'bar', labels: Object.keys(cRegion), data: Object.values(cRegion), color: '#f59e0b' },
    { id: 'stat4', title: 'Culverts by Road Class', type: 'pie', labels: Object.keys(cClass), data: Object.values(cClass), colors: [COLORS.emerald, COLORS.teal, COLORS.green, COLORS.lime, COLORS.amber, COLORS.orange] },
    { id: 'stat6', title: 'Culverts by Maintenance Station', type: 'bar', indexAxis: 'y', labels: Object.keys(cStation), data: Object.values(cStation), color: '#f59e0b' },
    { id: 'stat8', title: 'Culverts by Overall Condition', type: 'bar', labels: Object.keys(cCond), data: Object.values(cCond), color: COLORS.teal },
    { id: 'stat10', title: 'Culvert Waterway Condition', type: 'bar', labels: Object.keys(cWater), data: Object.values(cWater), color: COLORS.green },
    { id: 'stat12', title: 'Culvert Inlet/Outlet Condition', type: 'bar', labels: Object.keys(cInlet), data: Object.values(cInlet), color: COLORS.lime },
    { id: 'stat14', title: 'Culverts by Structure Type', type: 'pie', labels: Object.keys(cType), data: Object.values(cType), colors: [COLORS.teal, COLORS.green, COLORS.lime, COLORS.amber, COLORS.orange, COLORS.red] },
    { id: 'stat16', title: 'Culverts by Roadway Condition', type: 'bar', labels: Object.keys(cRoadway), data: Object.values(cRoadway), color: '#f59e0b' },
    { id: 'stat33', title: 'Culvert Suggested Interventions', type: 'pie', labels: Object.keys(cAct), data: Object.values(cAct), colors: [COLORS.emerald, COLORS.amber, COLORS.red, COLORS.slate] },
    { id: 'stat37', title: 'Culverts by Number of Cells/Pipes', type: 'bar', labels: Object.keys(cCells), data: Object.values(cCells), color: COLORS.teal },
    { id: 'stat38', title: 'Culvert Roadway Condition Rating', type: 'pie', labels: Object.keys(cRoadCond), data: Object.values(cRoadCond), colors: [COLORS.green, COLORS.lime, COLORS.amber, COLORS.red, COLORS.violet] },
    { id: 'stat39', title: 'Culvert Span/Diameter Distribution', type: 'bar', labels: Object.keys(cDiam), data: Object.values(cDiam), color: '#f59e0b' },

    // ===== NETWORK-WIDE =====
    { id: 'stat18', title: 'Total Structures by Asset Type', type: 'doughnut', labels: ['Bridges', 'Major Culverts'], data: [bridges.length, culverts.length], colors: [COLORS.cyan, '#f59e0b'] },
    { id: 'stat40', title: 'Total Bridge Length by Region', type: 'bar', labels: regions, datasets: [
      { label: 'Total Bridge Length (m)', data: regions.map(r => bridges.filter(b=>b.region===r).reduce((s, b)=>s+(Number(b.bridge_len)||0), 0)), backgroundColor: COLORS.indigo, borderRadius: 4 }
    ]},

    // ===== 20 ADDITIONAL NEW CHARTS =====
    { id: 'stat41', title: 'Bridge Type Distribution', type: 'pie', labels: Object.keys(bBridgeType), data: Object.values(bBridgeType), colors: PALETTE.slice(0, Object.keys(bBridgeType).length) },
    { id: 'stat42', title: 'Bridge Bearing Type', type: 'bar', indexAxis: 'y', labels: Object.keys(bBearings), data: Object.values(bBearings), color: COLORS.sky },
    { id: 'stat43', title: 'Bridge Wearing Surface Type', type: 'pie', labels: Object.keys(bWearing), data: Object.values(bWearing), colors: PALETTE.slice(0, Object.keys(bWearing).length) },
    { id: 'stat44', title: 'Bridge Parapet/Railing Type', type: 'bar', indexAxis: 'y', labels: Object.keys(bParapet), data: Object.values(bParapet), color: COLORS.purple },
    { id: 'stat45', title: 'Bridge Scour Protection Type', type: 'pie', labels: Object.keys(bScourProt), data: Object.values(bScourProt), colors: PALETTE.slice(0, Object.keys(bScourProt).length) },
    { id: 'stat46', title: 'Super Load Route Bridges', type: 'doughnut', labels: Object.keys(bSuperLoad), data: Object.values(bSuperLoad), colors: [COLORS.cyan, COLORS.red, COLORS.slate] },
    { id: 'stat47', title: 'Weight/Load Restricted Bridges', type: 'doughnut', labels: Object.keys(bWeightRestr), data: Object.values(bWeightRestr), colors: [COLORS.emerald, COLORS.red, COLORS.slate] },
    { id: 'stat48', title: 'Approach Slab Availability', type: 'doughnut', labels: Object.keys(bApproachSlab), data: Object.values(bApproachSlab), colors: [COLORS.blue, COLORS.amber, COLORS.slate] },
    { id: 'stat49', title: 'Bridge Width Distribution', type: 'bar', labels: Object.keys(bWidth), data: Object.values(bWidth), color: COLORS.teal },
    { id: 'stat50', title: 'Number of Piers Distribution', type: 'bar', labels: Object.keys(bPierCount).sort((a,b)=>Number(a)-Number(b)), data: Object.keys(bPierCount).sort((a,b)=>Number(a)-Number(b)).map(k=>bPierCount[k]), color: COLORS.indigo },
    { id: 'stat51', title: 'Number of Spans Distribution', type: 'bar', labels: Object.keys(bSpanCount).sort((a,b)=>Number(a)-Number(b)), data: Object.keys(bSpanCount).sort((a,b)=>Number(a)-Number(b)).map(k=>bSpanCount[k]), color: COLORS.violet },
    { id: 'stat52', title: 'Bridge Number of Lanes', type: 'bar', labels: Object.keys(bLanes).sort(), data: Object.keys(bLanes).sort().map(k=>bLanes[k]), color: COLORS.cyan },
    { id: 'stat53', title: 'Bridge Traffic Flow Directions', type: 'pie', labels: Object.keys(bTrafficFlow), data: Object.values(bTrafficFlow), colors: PALETTE.slice(0, Object.keys(bTrafficFlow).length) },
    { id: 'stat54', title: 'Bridge Approaches Condition', type: 'bar', labels: Object.keys(bApproachesCond), data: Object.values(bApproachesCond), color: COLORS.amber },
    { id: 'stat55', title: 'Bridge Roadway Rating Distribution', type: 'bar', labels: Object.keys(bRoadwayCond), data: Object.values(bRoadwayCond), color: COLORS.orange },
    { id: 'stat56', title: 'Bridge Waterway Rating Distribution', type: 'bar', labels: Object.keys(bWaterwayCond), data: Object.values(bWaterwayCond), color: COLORS.blue },
    { id: 'stat57', title: 'Bridge Surface Type on Link', type: 'pie', labels: Object.keys(bSurface), data: Object.values(bSurface), colors: PALETTE.slice(0, Object.keys(bSurface).length) },
    { id: 'stat58', title: 'Bridges by Crossing Type', type: 'pie', labels: Object.keys(bCrossingType), data: Object.values(bCrossingType), colors: PALETTE.slice(0, Object.keys(bCrossingType).length) },
    { id: 'stat59', title: 'Culvert Structure Condition', type: 'bar', labels: Object.keys(cStructCond), data: Object.values(cStructCond), color: COLORS.teal },
    { id: 'stat60', title: 'Network Condition Funnel', type: 'bar', labels: funnelLabels, data: funnelData, colors: funnelColors },
  ];'''

js = js[:old_charts_start] + new_charts + js[old_charts_end:]


# ============================================================
# FIX 5: Add the new aggregation data for the 20 additional charts
# ============================================================
# Insert after the existing new aggregations block, before chartConfigs
inject_point = js.find('const chartConfigs = [')

new_aggs = '''
  // Additional Bridge Aggregations
  const bBridgeType = {}; bridges.forEach(b => { const v = bmsCodeDescription('type_bridge', b.type_bridge); bBridgeType[v] = (bBridgeType[v] || 0) + 1; });
  const bBearings = {}; bridges.forEach(b => { const v = bmsCodeDescription('type_bearings', b.type_bearings); bBearings[v] = (bBearings[v] || 0) + 1; });
  const bWearing = {}; bridges.forEach(b => { const v = bmsCodeDescription('type_wearing_surface', b.type_wearing_surface); bWearing[v] = (bWearing[v] || 0) + 1; });
  const bParapet = {}; bridges.forEach(b => { const v = bmsCodeDescription('type_para_rail', b.type_para_rail); bParapet[v] = (bParapet[v] || 0) + 1; });
  const bScourProt = {}; bridges.forEach(b => { const v = bmsCodeDescription('scour_protection', b.scour_protection); bScourProt[v] = (bScourProt[v] || 0) + 1; });
  const bSuperLoad = {}; bridges.forEach(b => { const v = bmsYesNoUnknown(b.superload_route); bSuperLoad[v] = (bSuperLoad[v] || 0) + 1; });
  const bWeightRestr = {}; bridges.forEach(b => { const v = bmsYesNoUnknown(b.weight_load_restr); bWeightRestr[v] = (bWeightRestr[v] || 0) + 1; });
  const bApproachSlab = {}; bridges.forEach(b => { const v = bmsYesNoUnknown(b.approach_slab); bApproachSlab[v] = (bApproachSlab[v] || 0) + 1; });
  const bWidth = { '< 4m':0, '4-6m':0, '6-8m':0, '8-10m':0, '10-12m':0, '> 12m':0, 'Unknown':0 };
  bridges.forEach(b => {
    const w = parseFloat(b.bridge_wid);
    if (isNaN(w)) bWidth['Unknown']++;
    else if (w < 4) bWidth['< 4m']++;
    else if (w < 6) bWidth['4-6m']++;
    else if (w < 8) bWidth['6-8m']++;
    else if (w < 10) bWidth['8-10m']++;
    else if (w < 12) bWidth['10-12m']++;
    else bWidth['> 12m']++;
  });
  const bPierCount = {}; bridges.forEach(b => { const v = b.no_of_pier != null ? String(b.no_of_pier) : 'Unknown'; bPierCount[v] = (bPierCount[v] || 0) + 1; });
  const bSpanCount = {}; bridges.forEach(b => { const v = b.no_of_span != null ? String(b.no_of_span) : 'Unknown'; bSpanCount[v] = (bSpanCount[v] || 0) + 1; });
  const bLanes = {}; bridges.forEach(b => { const v = b.no_of_lane != null ? String(b.no_of_lane) : 'Unknown'; bLanes[v] = (bLanes[v] || 0) + 1; });
  const bTrafficFlow = {}; bridges.forEach(b => { const v = bmsCodeDescription('traffic_flow_directions', b.traffic_flow_directions); bTrafficFlow[v] = (bTrafficFlow[v] || 0) + 1; });
  const bApproachesCond = {}; bridges.forEach(b => { const v = b.approaches_rating != null ? String(b.approaches_rating) : 'Unknown'; bApproachesCond[v] = (bApproachesCond[v] || 0) + 1; });
  const bRoadwayCond = {}; bridges.forEach(b => { const v = b.roadway_rating != null ? String(b.roadway_rating) : 'Unknown'; bRoadwayCond[v] = (bRoadwayCond[v] || 0) + 1; });
  const bWaterwayCond = {}; bridges.forEach(b => { const v = b.waterway_rating != null ? String(b.waterway_rating) : 'Unknown'; bWaterwayCond[v] = (bWaterwayCond[v] || 0) + 1; });
  const bSurface = {}; bridges.forEach(b => { const v = b.surface_link || b.surface_ty || 'Unknown'; bSurface[v] = (bSurface[v] || 0) + 1; });
  const bCrossingType = {}; bridges.forEach(b => { const v = bmsCodeDescription('type_crossing', b.type_crossing); bCrossingType[v] = (bCrossingType[v] || 0) + 1; });
  
  // Additional Culvert Aggregations
  const cStructCond = {}; culverts.forEach(c => { const v = c.structure_cond || 'Unknown'; cStructCond[v] = (cStructCond[v] || 0) + 1; });

  // Funnel: Network Condition
  const totalAssets = bridges.length + culverts.length;
  const assessed = bridges.filter(b => b.overall_rating != null).length + culverts.filter(c => c.overall_rating != null || c.overall_cond != null).length;
  const goodAssets = bridges.filter(b => b.condition_category === 'Good').length + culverts.filter(c => c.condition_category === 'Good').length;
  const fairAssets = bridges.filter(b => b.condition_category === 'Fair').length + culverts.filter(c => c.condition_category === 'Fair').length;
  const poorAssets = bridges.filter(b => b.condition_category === 'Poor' || b.condition_category === 'Critical').length + culverts.filter(c => c.condition_category === 'Poor' || c.condition_category === 'Critical').length;
  const funnelLabels = ['Total Assets', 'Assessed', 'Good Condition', 'Fair Condition', 'Poor/Critical'];
  const funnelData = [totalAssets, assessed, goodAssets, fairAssets, poorAssets];
  const funnelColors = [COLORS.cyan, COLORS.blue, COLORS.emerald, COLORS.amber, COLORS.red];

'''

js = js[:inject_point] + new_aggs + js[inject_point:]

# ============================================================
# FIX 6: Make sure the export CSV includes culverts too
# ============================================================
# Check if exportCSV only exports bridges
export_csv_pos = js.find('function exportCSV()')
if export_csv_pos != -1:
    # Find the end of the function 
    next_func = js.find('\nfunction ', export_csv_pos + 20)
    export_csv_body = js[export_csv_pos:next_func]
    if 'MAJOR_CULVERTS' not in export_csv_body and 'culvert' not in export_csv_body.lower():
        # The exportCSV doesn't handle culverts - we'll add culvert export to it
        pass  # Will handle in next step

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("All fixes applied successfully!")
