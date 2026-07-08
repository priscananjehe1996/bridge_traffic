const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

    const filePath = 'file:///' + path.resolve('index.html').replace(/\\/g, '/');
    console.log('Loading:', filePath);
    
    await page.goto(filePath, { waitUntil: 'networkidle0' });
    
    console.log('Page loaded. Checking for elements...');
    
    await new Promise(r => setTimeout(r, 2000));
    
    await browser.close();
})();
