import re

with open('d:/OneDrive/Bridge stuff/bridge_traffic_deploy/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# I will append the table generation code right after `statisticsChartsInitialized = true;`

table_code = """

// GENERATE SUMMARY TABLES
const tableContainer = document.getElementById('statisticsTablesContainer');
if (tableContainer) {
    let tHtml = `<div class="card" style="margin-bottom: 30px;">
        <div class="card-title">Detailed Network Summary Tables</div>
        <div class="card-subtitle">Tabular data for all major aggregations</div>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 20px;">
    `;
    
    const makeTable = (title, dataObj) => {
        let rows = '';
        let total = 0;
        const sortedKeys = Object.keys(dataObj).sort((a,b) => dataObj[b] - dataObj[a]);
        sortedKeys.forEach(k => {
            rows += `<tr><td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.1);">${k}</td><td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); text-align: right;">${dataObj[k]}</td></tr>`;
            total += dataObj[k];
        });
        rows += `<tr><td style="padding: 8px; font-weight: bold; color: #fff;">Total</td><td style="padding: 8px; font-weight: bold; color: #fff; text-align: right;">${total}</td></tr>`;
        
        return `
        <div style="background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 16px;">
            <h4 style="margin: 0 0 12px 0; color: #38bdf8; font-size: 14px;">${title}</h4>
            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">
                <thead>
                    <tr>
                        <th style="text-align: left; padding: 8px; border-bottom: 2px solid rgba(255,255,255,0.1); color: #94a3b8;">Category</th>
                        <th style="text-align: right; padding: 8px; border-bottom: 2px solid rgba(255,255,255,0.1); color: #94a3b8;">Count</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows}
                </tbody>
            </table>
        </div>
        `;
    };

    tHtml += makeTable('Bridges by Region', bRegion);
    tHtml += makeTable('Culverts by Region', cRegion);
    tHtml += makeTable('Bridges by Station', bStation);
    tHtml += makeTable('Bridges by Road Class', bClass);
    tHtml += makeTable('Bridges Overall Condition', bCond);
    tHtml += makeTable('Culverts Overall Condition', cCond);
    tHtml += makeTable('Bridges by Deck Material', bDeck);
    tHtml += makeTable('Bridges Recommended Action', bAct);
    tHtml += makeTable('Bridges by Construction Decade', bDecade2);
    tHtml += makeTable('Culverts by Recommended Action', cAct);

    tHtml += `</div></div>`;
    tableContainer.innerHTML = tHtml;
}
"""

idx = text.find("statisticsChartsInitialized = true;")
if idx != -1:
    text = text[:idx] + table_code + "\n" + text[idx:]
    with open('d:/OneDrive/Bridge stuff/bridge_traffic_deploy/app.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Tables added!")
else:
    print("Could not find insertion point!")
