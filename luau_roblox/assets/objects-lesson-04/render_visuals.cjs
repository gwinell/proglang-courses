// Optional authoring utility. Students only need the committed SVG/GIF files.
const fs = require('node:fs/promises');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_CORE_PATH || 'playwright');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.CHROME_EXECUTABLE_PATH ? { executablePath: process.env.CHROME_EXECUTABLE_PATH } : {}),
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1200, height: 680 }, deviceScaleFactor: 1 });
    for (const group of ['08-reparent', '09-event-cooldown']) {
      const folder = path.join(__dirname, '_frames', group);
      const files = (await fs.readdir(folder)).filter(f => f.endsWith('.svg')).sort();
      for (const file of files) {
        const svg = await fs.readFile(path.join(folder, file), 'utf8');
        await page.setContent('<html><body style="margin:0">' + svg + '</body></html>');
        await page.screenshot({ path: path.join(folder, file.replace('.svg', '.png')) });
      }
      console.log(group + ': ' + files.length + ' frames');
    }
    for (const file of ['05-hierarchy.svg', '06-event-flow.svg', '07-lifecycle.svg']) {
      await page.setContent('<html><body style="margin:0">' + await fs.readFile(path.join(__dirname, file), 'utf8') + '</body></html>');
      await page.screenshot({ path: path.join(__dirname, '_frames', file.replace('.svg', '.png')) });
    }
  } finally {
    await browser.close();
  }
})().catch(e => { console.error(e.message); process.exitCode = 1; });
