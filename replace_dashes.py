import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace general functions returning '-'
js = re.sub(r"return '-';", "return 'N/A';", js)
js = re.sub(r"return '- ' \+", "return 'N/A ' +", js)

# Replace logical OR fallbacks: || '-'
js = re.sub(r"\|\|\s*'-'", "|| 'N/A'", js)

# Replace ternary fallbacks: : '-'
js = re.sub(r":\s*'-'", ": 'N/A'", js)

# Replace BMS 'Unknown' with 'N/A'
js = re.sub(r"return 'Unknown';", "return 'N/A';", js)
js = re.sub(r"cleanBmsDescription\(direct \|\| 'Unknown'\);", "cleanBmsDescription(direct || 'N/A');", js)
js = re.sub(r"cleanBmsDescription\(direct \|\| 'N/A'\);", "cleanBmsDescription(direct || 'N/A');", js)

# Replace array join or other literal '-' usage in UI strings if they exist
js = re.sub(r"\? '-' :", "? 'N/A' :", js)
js = re.sub(r"=== '-'", "=== 'N/A'", js)
js = re.sub(r"td\.textContent = '-';", "td.textContent = 'N/A';", js)
js = re.sub(r"compensation: '-',", "compensation: 'N/A',", js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Done")
