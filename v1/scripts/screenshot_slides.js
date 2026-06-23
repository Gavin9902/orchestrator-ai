const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const HTML_PATH = path.join(__dirname, 'pitch.html');
const OUT_DIR = path.join(__dirname, 'pitch_frames');

(async () => {
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 675 } });
  await page.goto(`file://${HTML_PATH}`, { waitUntil: 'networkidle' });

  // Find all slide sections
  const sections = await page.$$('section, .hero, .section');
  console.log(`Found ${sections.length} sections`);

  for (let i = 0; i < sections.length; i++) {
    // Scroll section into view and wait for transitions
    await sections[i].scrollIntoViewIfNeeded();
    await page.waitForTimeout(800);

    // Screenshot just this section
    await sections[i].screenshot({
      path: path.join(OUT_DIR, `slide_${String(i).padStart(2, '0')}.png`),
    });
    console.log(`Screenshot slide ${i}`);
  }

  // Also take footer
  const footer = await page.$('.footer');
  if (footer) {
    await footer.screenshot({ path: path.join(OUT_DIR, `slide_${String(sections.length).padStart(2, '0')}.png`) });
    console.log('Screenshot footer');
  }

  await browser.close();
  console.log('Done. Frames saved to', OUT_DIR);
})();
