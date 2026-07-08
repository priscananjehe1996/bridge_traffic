const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('http://localhost:4205/index.html', { waitUntil: 'networkidle0' });
    await new Promise(r => setTimeout(r, 2000));
    const emptyCells = await page.evaluate(() => {
        const tds = Array.from(document.querySelectorAll('td'));
        return tds.filter(td => !td.textContent || td.textContent.trim() === '' || td.textContent.includes('undefined') || td.textContent.includes('NaN')).map(td => td.outerHTML);
    });
    console.log('Empty or invalid cells found:', emptyCells.length);
    if (emptyCells.length > 0) {
        console.log(emptyCells.slice(0, 10).join('\n'));
    }
    await browser.close();
})();