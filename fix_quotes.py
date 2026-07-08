with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("\\'rgba", "'rgba").replace("\\',", "',")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Quotes fixed")
