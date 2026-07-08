const fs = require('fs');

const roads = JSON.parse(fs.readFileSync('roads.json', 'utf8'));
const linkMap = {};
roads.forEach(r => {
  if (r.Link_ID) {
    linkMap[String(r.Link_ID).trim()] = {
      link_name: r.Link_Name,
      road_class: r.Road_Class,
      region: r.Maintenance_Region,
      station: r.Maintenance_Station
    };
  }
});

let data = fs.readFileSync('bridge_data.js', 'utf8');

function enrichArray(arrayStr) {
  // It's a JS array of objects. We can eval it safely in this context.
  let arr;
  try {
    arr = eval(arrayStr);
  } catch (e) {
    console.error('Eval error', e);
    return arrayStr;
  }
  
  arr.forEach(item => {
    let link_no = String(item.link_no || '').trim();
    if (linkMap[link_no]) {
      const info = linkMap[link_no];
      if (!item.link_name || item.link_name === 'N/A') item.link_name = info.link_name;
      if (!item.road_class || item.road_class === 'N/A' || item.road_class === 'Unknown') item.road_class = info.road_class;
      if (!item.region || item.region === 'N/A') item.region = info.region;
      if (!item.station || item.station === 'N/A') item.station = info.station;
      if (!item.road_name || item.road_name === 'N/A') item.road_name = info.link_name;
    }
  });
  
  return JSON.stringify(arr, null, 2);
}

const bridgesRegex = /const BRIDGES = (\[[\s\S]*?\]);/;
const culvertsRegex = /const MAJOR_CULVERTS = (\[[\s\S]*?\]);/;

data = data.replace(bridgesRegex, (match, p1) => `const BRIDGES = ${enrichArray(p1)};`);
data = data.replace(culvertsRegex, (match, p1) => `const MAJOR_CULVERTS = ${enrichArray(p1)};`);

fs.writeFileSync('bridge_data.js', data, 'utf8');
console.log('Enriched bridge_data.js successfully.');
