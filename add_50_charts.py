import re
import json

with open('d:/OneDrive/Bridge stuff/bridge_traffic_deploy/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# I will define 50 new charts using existing datasets

new_charts = """
{ id: 'stat_extra_1', title: 'Bridges by Traffic Priority', type: 'pie', labels: Object.keys(bTrafficPriority), data: Object.values(bTrafficPriority), colors: [COLORS.emerald, COLORS.blue, COLORS.orange, COLORS.red, COLORS.purple] },
{ id: 'stat_extra_2', title: 'Culverts by Road Condition', type: 'bar', labels: Object.keys(cRoadCond), data: Object.values(cRoadCond), color: COLORS.emerald },
{ id: 'stat_extra_3', title: 'Culverts by Number of Cells', type: 'bar', labels: Object.keys(cCells), data: Object.values(cCells), color: COLORS.blue },
{ id: 'stat_extra_4', title: 'Culverts by Diameter Band', type: 'pie', labels: Object.keys(cDiam), data: Object.values(cDiam), colors: [COLORS.blue, COLORS.cyan, COLORS.emerald, COLORS.orange, COLORS.gray] },
{ id: 'stat_extra_5', title: 'Culverts Recommended Action', type: 'bar', labels: Object.keys(cAct), data: Object.values(cAct), color: COLORS.orange },
{ id: 'stat_extra_6', title: 'Bridges by Substructure Condition', type: 'pie', labels: Object.keys(bSub), data: Object.values(bSub), colors: [COLORS.emerald, COLORS.cyan, COLORS.orange, COLORS.red] },
{ id: 'stat_extra_7', title: 'Bridges by Waterway Condition', type: 'pie', labels: Object.keys(bWaterwayCond), data: Object.values(bWaterwayCond), colors: [COLORS.emerald, COLORS.blue, COLORS.orange, COLORS.red] },
{ id: 'stat_extra_8', title: 'Bridges by Expansion Joint Condition', type: 'bar', labels: Object.keys(bExpCond), data: Object.values(bExpCond), color: COLORS.purple },
{ id: 'stat_extra_9', title: 'Bridges by Pier Condition', type: 'bar', labels: Object.keys(bPierCond), data: Object.values(bPierCond), color: COLORS.red },
{ id: 'stat_extra_10', title: 'Bridges by Abutment Condition', type: 'pie', labels: Object.keys(bAbutCond), data: Object.values(bAbutCond), colors: [COLORS.emerald, COLORS.orange, COLORS.red, COLORS.blue] },
{ id: 'stat_extra_11', title: 'Top 10 Rivers Crossed', type: 'bar', indexAxis: 'y', labels: topRivers.slice(0, 10).map(x => x[0]), data: topRivers.slice(0, 10).map(x => x[1]), color: COLORS.cyan },
{ id: 'stat_extra_12', title: 'Bridges by Number of Spans', type: 'bar', labels: Object.keys(bSpanCount), data: Object.values(bSpanCount), color: COLORS.blue },
{ id: 'stat_extra_13', title: 'Bridges by Number of Piers', type: 'pie', labels: Object.keys(bPierCount), data: Object.values(bPierCount), colors: [COLORS.cyan, COLORS.blue, COLORS.emerald, COLORS.orange, COLORS.purple, COLORS.red] },
{ id: 'stat_extra_14', title: 'Bridges by Width Band', type: 'bar', labels: Object.keys(bWidth), data: Object.values(bWidth), color: COLORS.emerald },
{ id: 'stat_extra_15', title: 'Bridges by Approach Slab Presence', type: 'pie', labels: Object.keys(bApproachSlab), data: Object.values(bApproachSlab), colors: [COLORS.emerald, COLORS.orange, COLORS.red] },
{ id: 'stat_extra_16', title: 'Bridges by Weight Restriction', type: 'pie', labels: Object.keys(bWeightRestr), data: Object.values(bWeightRestr), colors: [COLORS.orange, COLORS.emerald, COLORS.gray] },
{ id: 'stat_extra_17', title: 'Bridges on Superload Routes', type: 'bar', labels: Object.keys(bSuperLoad), data: Object.values(bSuperLoad), color: COLORS.purple },
{ id: 'stat_extra_18', title: 'Bridges by Scour Protection Type', type: 'bar', indexAxis: 'y', labels: Object.keys(bScourProt), data: Object.values(bScourProt), color: COLORS.cyan },
{ id: 'stat_extra_19', title: 'Bridges by Scour Risk', type: 'pie', labels: Object.keys(bScour), data: Object.values(bScour), colors: [COLORS.emerald, COLORS.orange, COLORS.red, COLORS.gray] },
{ id: 'stat_extra_20', title: 'Bridges by Parapet/Rail Type', type: 'bar', indexAxis: 'y', labels: Object.keys(bParapet), data: Object.values(bParapet), color: COLORS.blue },
{ id: 'stat_extra_21', title: 'Bridges by Wearing Surface', type: 'pie', labels: Object.keys(bWearing), data: Object.values(bWearing), colors: [COLORS.emerald, COLORS.cyan, COLORS.blue, COLORS.purple, COLORS.orange] },
{ id: 'stat_extra_22', title: 'Bridges by Bearing Type', type: 'bar', indexAxis: 'y', labels: Object.keys(bBearings), data: Object.values(bBearings), color: COLORS.emerald },
{ id: 'stat_extra_23', title: 'Bridges by Detailed Bridge Type', type: 'bar', indexAxis: 'y', labels: Object.keys(bBridgeType), data: Object.values(bBridgeType), color: COLORS.orange },
{ id: 'stat_extra_24', title: 'Culverts by Waterway Condition', type: 'pie', labels: Object.keys(cWater), data: Object.values(cWater), colors: [COLORS.emerald, COLORS.orange, COLORS.red, COLORS.gray] },
{ id: 'stat_extra_25', title: 'Culverts by Inlet/Outlet Condition', type: 'bar', labels: Object.keys(cInlet), data: Object.values(cInlet), color: COLORS.blue },
{ id: 'stat_extra_26', title: 'Bridges by Abutment Type', type: 'bar', indexAxis: 'y', labels: Object.keys(bAbutment), data: Object.values(bAbutment), color: COLORS.purple },
{ id: 'stat_extra_27', title: 'Bridges by Pier Type Detailed', type: 'pie', labels: Object.keys(bPier), data: Object.values(bPier), colors: [COLORS.cyan, COLORS.emerald, COLORS.blue, COLORS.orange, COLORS.purple] },
{ id: 'stat_extra_28', title: 'Bridges by Detailed Deck Type', type: 'bar', indexAxis: 'y', labels: Object.keys(bDeckType), data: Object.values(bDeckType), color: COLORS.cyan },
{ id: 'stat_extra_29', title: 'Bridges by Expansion Joint Type', type: 'bar', indexAxis: 'y', labels: Object.keys(bExpansion), data: Object.values(bExpansion), color: COLORS.emerald },
{ id: 'stat_extra_30', title: 'Bridges Span Grouping', type: 'pie', labels: Object.keys(bSpans), data: Object.values(bSpans), colors: [COLORS.blue, COLORS.cyan, COLORS.gray] },
{ id: 'stat_extra_31', title: 'Bridges Recommended Action', type: 'bar', labels: Object.keys(bAct), data: Object.values(bAct), color: COLORS.orange },
{ id: 'stat_extra_32', title: 'Bridges Construction Decade', type: 'bar', labels: Object.keys(bDecade2), data: Object.values(bDecade2), color: COLORS.purple },
{ id: 'stat_extra_33', title: 'Bridges by Deck Material', type: 'bar', indexAxis: 'y', labels: Object.keys(bDeck), data: Object.values(bDeck), color: COLORS.blue },
{ id: 'stat_extra_34', title: 'Culverts by Detailed Type', type: 'bar', indexAxis: 'y', labels: Object.keys(cType), data: Object.values(cType), color: COLORS.orange },
{ id: 'stat_extra_35', title: 'Bridges by Crossing Description', type: 'pie', labels: Object.keys(bCrossing), data: Object.values(bCrossing), colors: [COLORS.emerald, COLORS.cyan, COLORS.blue, COLORS.purple, COLORS.orange] },
{ id: 'stat_extra_36', title: 'Bridges Superstructure Rating', type: 'bar', labels: Object.keys(bSuper), data: Object.values(bSuper), color: COLORS.cyan },
{ id: 'stat_extra_37', title: 'Bridges Roadway Rating', type: 'pie', labels: Object.keys(bRoadwayCond), data: Object.values(bRoadwayCond), colors: [COLORS.emerald, COLORS.orange, COLORS.red, COLORS.gray] },
{ id: 'stat_extra_38', title: 'Bridges Approaches Rating', type: 'bar', labels: Object.keys(bApproachesCond), data: Object.values(bApproachesCond), color: COLORS.blue },
{ id: 'stat_extra_39', title: 'Bridges by Flow Directions', type: 'pie', labels: Object.keys(bTrafficFlow), data: Object.values(bTrafficFlow), colors: [COLORS.cyan, COLORS.emerald, COLORS.gray] },
{ id: 'stat_extra_40', title: 'Bridges by Number of Lanes', type: 'bar', labels: Object.keys(bLanes), data: Object.values(bLanes), color: COLORS.purple },
{ id: 'stat_extra_41', title: 'Bridges by Surface Type', type: 'bar', labels: Object.keys(bSurface), data: Object.values(bSurface), color: COLORS.orange },
{ id: 'stat_extra_42', title: 'Culverts by Region', type: 'pie', labels: Object.keys(cRegion), data: Object.values(cRegion), colors: [COLORS.emerald, COLORS.cyan, COLORS.blue, COLORS.purple, COLORS.orange, COLORS.red] },
{ id: 'stat_extra_43', title: 'Bridges by Region', type: 'pie', labels: Object.keys(bRegion), data: Object.values(bRegion), colors: [COLORS.emerald, COLORS.cyan, COLORS.blue, COLORS.purple, COLORS.orange, COLORS.red] },
{ id: 'stat_extra_44', title: 'Bridges vs Culverts Total Count', type: 'bar', labels: ['Bridges', 'Culverts'], data: [bridges.length, culverts.length], color: COLORS.blue },
{ id: 'stat_extra_45', title: 'Bridge Overall Conditions', type: 'bar', labels: Object.keys(bCond), data: Object.values(bCond), color: COLORS.emerald },
{ id: 'stat_extra_46', title: 'Culvert Overall Conditions', type: 'bar', labels: Object.keys(cCond), data: Object.values(cCond), color: COLORS.orange },
{ id: 'stat_extra_47', title: 'Bridges by Road Class', type: 'pie', labels: Object.keys(bClass), data: Object.values(bClass), colors: [COLORS.emerald, COLORS.cyan, COLORS.blue, COLORS.purple, COLORS.orange, COLORS.red] },
{ id: 'stat_extra_48', title: 'Culverts by Road Class', type: 'pie', labels: Object.keys(cClass), data: Object.values(cClass), colors: [COLORS.emerald, COLORS.cyan, COLORS.blue, COLORS.purple, COLORS.orange, COLORS.red] },
{ id: 'stat_extra_49', title: 'Bridges by Maintenance Station', type: 'bar', indexAxis: 'y', labels: Object.keys(bStation), data: Object.values(bStation), color: COLORS.cyan },
{ id: 'stat_extra_50', title: 'Culverts by Maintenance Station', type: 'bar', indexAxis: 'y', labels: Object.keys(cStation), data: Object.values(cStation), color: COLORS.orange },
"""

idx = text.find("id: 'stat60', title: 'Network Condition Funnel', type: 'bar', labels: funnelLabels, data: funnelData, colors: funnelColors }")
if idx == -1:
    print("Could not find stat60!")
else:
    end_idx = text.find('];', idx)
    text = text[:end_idx] + "},\n" + new_charts + text[end_idx:]
    with open('d:/OneDrive/Bridge stuff/bridge_traffic_deploy/app.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added 50 charts!")
