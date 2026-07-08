const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport({width: 1280, height: 800});
    await page.goto('http://localhost:4201/index.html', { waitUntil: 'networkidle0' });
    await new Promise(r => setTimeout(r, 2000));
    await page.screenshot({path: 'd:/OneDrive/Bridge stuff/bridge_traffic_deploy/screenshot.png'});
    await browser.close();
})();