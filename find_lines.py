with open('app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = -1
end = -1
for i, line in enumerate(lines):
    if 'function openBridgeModal' in line:
        start = i + 1
    if 'document.getElementById("bridgeModal").classList.add("active")' in line or 'document.getElementById(\'bridgeModal\').classList.add(\'active\')' in line:
        end = i + 1
        
print(f"Start: {start}, End: {end}")
