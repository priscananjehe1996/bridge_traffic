const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
    page.on('pageerror', error => console.log('BROWSER ERROR:', error.message));
    await page.goto('http://localhost:4206/index.html', { waitUntil: 'networkidle0' });
    await new Promise(r => setTimeout(r, 2000));
    await browser.close();
})();