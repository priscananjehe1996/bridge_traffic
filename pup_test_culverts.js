const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', err => console.log('PAGE ERROR:', err.stack || err.message));
    await page.goto('http://localhost:4203/index.html', { waitUntil: 'networkidle0' });
    console.log('Page loaded.');
    await new Promise(r => setTimeout(r, 2000));
    await browser.close();
})();