import json, re

with open('bridge_data.js', 'r', encoding='utf-8') as f:
    data = f.read()

m = re.search(r'const MAJOR_CULVERTS = (\[.*?\]);', data, flags=re.DOTALL)
if m:
    json_str = m.group(1).replace('null', 'None').replace('NaN', 'None')
    try:
        # evaluate the string
        culverts = eval(json_str)
        for i in range(3):
            print(culverts[i])
    except Exception as e:
        print("eval failed:", e)
        # fallback to finding specific keys
        for match in re.finditer(r'\{[^\}]+\}', data):
            text = match.group(0)
            if '"C002"' in text or '"C003"' in text:
                print(text)
