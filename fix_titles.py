import re
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = re.sub(r"title: '\d+\.\s*", "title: '", js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('Removed numbers from chart titles.')
