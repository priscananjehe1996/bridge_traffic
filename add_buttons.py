with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

btn_culvert = '<button class="tab" data-tab="major-culverts" role="tab">Major Culvert Inventory</button>'
btns_to_add = '\n<button class="tab" data-tab="bridge-traffic" role="tab">Bridge Traffic Analytics</button>\n<button class="tab" data-tab="od-matrix" role="tab">Origin-Destination Matrix</button>'

if btn_culvert in text and 'data-tab="bridge-traffic"' not in text:
    new_text = text.replace(btn_culvert, btn_culvert + btns_to_add)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Buttons added!')
elif 'data-tab="bridge-traffic"' in text:
    print('Buttons already present.')
else:
    print('Could not find anchor button.')
