import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<div class="modal-overlay" id="bridgeModal">')
end = text.find('</div></div></div>', start)
print(text[start:end+500])
