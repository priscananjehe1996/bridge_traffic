import re

code = """
let statisticsChartsInitialized = false;
function initStatisticsTab() {
  if (statisticsChartsInitialized) return;
  const container = document.getElementById('statisticsChartsContainer');
  if (!container) return;

  const bridges = typeof BRIDGES !== 'undefined' ? BRIDGES : [];
  const culverts = typeof MAJOR_CULVERTS !== 'undefined' ? MAJOR_CULVERTS : [];

  const bRegion = {}; bridges.forEach(b => { const r = b.region || 'Unknown'; bRegion[r] = (bRegion[r] || 0) + 1; });
  const cRegion = {}; culverts.forEach(c => { const r = c.region || 'Unknown'; cRegion[r] = (cRegion[r] || 0) + 1; });
  const bClass = {}; bridges.forEach(b => { const c = canonicalRoadClass(b.road_class); bClass[c] = (bClass[c] || 0) + 1; });
  const cClass = {}; culverts.forEach(c => { const c_cls = canonicalRoadClass(c.road_class); cClass[c_cls] = (cClass[c_cls] || 0) + 1; });
  const bStation = {}; bridges.forEach(b => { const s = b.station || 'Unknown'; bStation[s] = (bStation[s] || 0) + 1; });
  const cStation = {}; culverts.forEach(c => { const s = c.station || 'Unknown'; cStation[s] = (cStation[s] || 0) + 1; });
  
  const bCond = {}; bridges.forEach(b => { const c = b.condition_category || 'Unknown'; bCond[c] = (bCond[c] || 0) + 1; });
  const cCond = {}; culverts.forEach(c => { const cond = c.overall_cond || c.condition_category || 'Unknown'; cCond[cond] = (cCond[cond] || 0) + 1; });
  
  const bSuper = {}; bridges.forEach(b => { const c = b.superstructure_cond || 'Unknown'; bSuper[c] = (bSuper[c] || 0) + 1; });
  const cWater = {}; culverts.forEach(c => { const cond = c.waterway_cond || 'Unknown'; cWater[cond] = (cWater[cond] || 0) + 1; });
  
  const bSub = {}; bridges.forEach(b => { const c = b.substructure_cond || 'Unknown'; bSub[c] = (bSub[c] || 0) + 1; });
  const cInlet = {}; culverts.forEach(c => { const cond = c.inlet_outlet_cond || 'Unknown'; cInlet[cond] = (cInlet[cond] || 0) + 1; });
  
  const bDeck = {}; bridges.forEach(b => { const d = bmsCodeDescription('type_deck_material', b.type_deck_material); bDeck[d] = (bDeck[d] || 0) + 1; });
  const cType = {}; culverts.forEach(c => { const t = BMS_CODE_LOOKUPS.type_bridge?.[c.type_culvert] || c.type_culvert || 'Unknown'; cType[t] = (cType[t] || 0) + 1; });
  
  const bCrossing = {}; bridges.forEach(b => { const d = bmsCodeDescription('type_crossing', b.type_crossing); bCrossing[d] = (bCrossing[d] || 0) + 1; });
  const cRoadway = {}; culverts.forEach(c => { const d = c.roadway_cond || 'Unknown'; cRoadway[d] = (cRoadway[d] || 0) + 1; });
  
  const bDecade = {}; bridges.forEach(b => { 
    if(b.year_compl) { 
      const dec = Math.floor(b.year_compl / 10) * 10; 
      bDecade[dec + 's'] = (bDecade[dec + 's'] || 0) + 1; 
    } else {
      bDecade['Unknown'] = (bDecade['Unknown'] || 0) + 1;
    }
  });
  
  const bScour = {}; bridges.forEach(b => { const s = bmsCodeDescription('scour_risk', b.scour_risk); bScour[s] = (bScour[s] || 0) + 1; });
  
  const bLength = { '< 10m':0, '10-20m':0, '20-50m':0, '50-100m':0, '> 100m':0, 'Unknown': 0 };
  bridges.forEach(b => {
    if (!b.bridge_len) bLength['Unknown']++;
    else if (b.bridge_len < 10) bLength['< 10m']++;
    else if (b.bridge_len < 20) bLength['10-20m']++;
    else if (b.bridge_len < 50) bLength['20-50m']++;
    else if (b.bridge_len < 100) bLength['50-100m']++;
    else bLength['> 100m']++;
  });

  const chartConfigs = [
    { id: 'stat1', title: '1. Bridges by Region', type: 'bar', labels: Object.keys(bRegion), data: Object.values(bRegion), color: COLORS.cyan },
    { id: 'stat2', title: '2. Culverts by Region', type: 'bar', labels: Object.keys(cRegion), data: Object.values(cRegion), color: COLORS.emerald },
    { id: 'stat3', title: '3. Bridges by Road Class', type: 'pie', labels: Object.keys(bClass), data: Object.values(bClass), colors: [COLORS.cyan, COLORS.blue, COLORS.indigo, COLORS.violet] },
    { id: 'stat4', title: '4. Culverts by Road Class', type: 'pie', labels: Object.keys(cClass), data: Object.values(cClass), colors: [COLORS.emerald, COLORS.teal, COLORS.green, COLORS.lime] },
    { id: 'stat5', title: '5. Bridges by Maintenance Station', type: 'bar', indexAxis: 'y', labels: Object.keys(bStation), data: Object.values(bStation), color: COLORS.cyan },
    { id: 'stat6', title: '6. Culverts by Maintenance Station', type: 'bar', indexAxis: 'y', labels: Object.keys(cStation), data: Object.values(cStation), color: COLORS.emerald },
    { id: 'stat7', title: '7. Bridges by Overall Condition', type: 'bar', labels: Object.keys(bCond), data: Object.values(bCond), color: COLORS.blue },
    { id: 'stat8', title: '8. Culverts by Overall Condition', type: 'bar', labels: Object.keys(cCond), data: Object.values(cCond), color: COLORS.teal },
    { id: 'stat9', title: '9. Bridges Superstructure Condition', type: 'bar', labels: Object.keys(bSuper), data: Object.values(bSuper), color: COLORS.indigo },
    { id: 'stat10', title: '10. Culverts Waterway Condition', type: 'bar', labels: Object.keys(cWater), data: Object.values(cWater), color: COLORS.green },
    { id: 'stat11', title: '11. Bridges Substructure Condition', type: 'bar', labels: Object.keys(bSub), data: Object.values(bSub), color: COLORS.violet },
    { id: 'stat12', title: '12. Culverts Inlet/Outlet Condition', type: 'bar', labels: Object.keys(cInlet), data: Object.values(cInlet), color: COLORS.lime },
    { id: 'stat13', title: '13. Bridges by Deck Material', type: 'pie', labels: Object.keys(bDeck), data: Object.values(bDeck), colors: [COLORS.rose, COLORS.amber, COLORS.cyan, COLORS.emerald, COLORS.blue] },
    { id: 'stat14', title: '14. Culverts by Structure Type', type: 'pie', labels: Object.keys(cType), data: Object.values(cType), colors: [COLORS.teal, COLORS.green, COLORS.lime, COLORS.amber, COLORS.orange] },
    { id: 'stat15', title: '15. Bridge Crossings by Type', type: 'bar', labels: Object.keys(bCrossing), data: Object.values(bCrossing), color: COLORS.cyan },
    { id: 'stat16', title: '16. Culverts by Roadway Condition', type: 'bar', labels: Object.keys(cRoadway), data: Object.values(cRoadway), color: COLORS.emerald },
    { id: 'stat17', title: '17. Bridges Built per Decade', type: 'bar', labels: Object.keys(bDecade).sort(), data: Object.keys(bDecade).sort().map(k => bDecade[k]), color: COLORS.indigo },
    { id: 'stat18', title: '18. Total Structures by Asset Type', type: 'doughnut', labels: ['Bridges', 'Major Culverts'], data: [bridges.length, culverts.length], colors: [COLORS.cyan, COLORS.emerald] },
    { id: 'stat19', title: '19. Bridge Scour Risk Profile', type: 'pie', labels: Object.keys(bScour), data: Object.values(bScour), colors: [COLORS.red, COLORS.orange, COLORS.amber, COLORS.green, COLORS.blue] },
    { id: 'stat20', title: '20. Bridge Length Distribution', type: 'bar', labels: Object.keys(bLength), data: Object.values(bLength), color: COLORS.cyan }
  ];

  let html = '';
  chartConfigs.forEach(c => {
    html += `
      <div class="card" style="box-shadow:none; border:1px solid rgba(255,255,255,0.05); min-height: 250px;">
        <div class="card-title">${htmlEscape(c.title)}</div>
        <div class="chart-container" style="position: relative; height: 220px;"><canvas id="${c.id}"></canvas></div>
      </div>
    `;
  });
  container.innerHTML = html;

  chartConfigs.forEach(c => {
    const ctx = document.getElementById(c.id).getContext('2d');
    const isPie = c.type === 'pie' || c.type === 'doughnut';
    const config = {
      type: c.type,
      data: {
        labels: c.labels,
        datasets: [{
          label: 'Count',
          data: c.data,
          backgroundColor: c.colors || c.color,
          borderWidth: 0,
          borderRadius: isPie ? 0 : 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: c.indexAxis || 'x',
        plugins: {
          legend: { display: isPie, position: 'right', labels: { color: 'rgba(255,255,255,0.7)', font: { size: 10 } } },
          tooltip: {
            backgroundColor: 'rgba(15,23,42,0.9)',
            titleColor: '#fff',
            bodyColor: '#cbd5e1',
            borderColor: 'rgba(255,255,255,0.1)',
            borderWidth: 1,
            padding: 10
          }
        },
        scales: isPie ? {} : {
          x: { ticks: { color: 'rgba(255,255,255,0.5)', autoSkip: false, maxRotation: 45, minRotation: 45 }, grid: { display: false } },
          y: { ticks: { color: 'rgba(255,255,255,0.5)' }, grid: { color: 'rgba(255,255,255,0.05)' }, beginAtZero: true }
        }
      }
    };
    new Chart(ctx, config);
  });

  statisticsChartsInitialized = true;
}
"""

with open('app.js', 'a', encoding='utf-8') as f:
    f.write('\\n' + code + '\\n')
print('Added initStatisticsTab to app.js')
