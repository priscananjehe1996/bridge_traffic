const http = require('http');
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const server = http.createServer((req, res) => {
  let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url.split('?')[0]);
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end(JSON.stringify(err));
      return;
    }
    const ext = path.extname(filePath);
    let contentType = 'text/html';
    if (ext === '.js') contentType = 'text/javascript';
    else if (ext === '.css') contentType = 'text/css';
    
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(data);
  });
});

server.listen(9124, async () => {
  let browser;
  try {
    browser = await puppeteer.launch({headless: 'new'});
    const page = await browser.newPage();
    page.on('console', msg => console.log('PAGE LOG:', msg.type(), msg.text()));
    page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));
    
    console.log('Navigating to http://localhost:9124');
    await page.goto('http://localhost:9124', {waitUntil: 'networkidle0', timeout: 30000});
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const tabs = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('.tab')).map(t => t.dataset.tab);
    });
    console.log('TABS FOUND:', tabs);
    
    await page.evaluate(() => {
       const tab = document.querySelector('.tab[data-tab="bridge-traffic"]');
       if (tab) tab.click();
    });
    console.log('Clicked Bridge Traffic tab');
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const activePanelId = await page.evaluate(() => {
       const panels = document.querySelectorAll('.panel');
       for (const p of panels) {
           const style = window.getComputedStyle(p);
           if (style.display !== 'none') return p.id;
       }
       return 'NONE';
    });
    console.log('ACTIVE PANEL:', activePanelId);
    
    await browser.close();
  } catch(e) {
    console.log('TEST SCRIPT ERROR:', e);
    if(browser) await browser.close();
  } finally {
    server.close();
  }
});
