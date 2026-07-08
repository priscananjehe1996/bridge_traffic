const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('http://localhost:4202/index.html', { waitUntil: 'networkidle0' });
    await new Promise(r => setTimeout(r, 2000));
    const content = await page.evaluate(() => document.body.innerText);
    console.log(content.substring(0, 1000));
    await browser.close();
})();