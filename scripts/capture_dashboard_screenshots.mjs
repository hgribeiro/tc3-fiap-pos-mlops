import { chromium } from 'playwright';

const baseUrl = 'http://localhost:3847/dashboard/';
const outputDir = 'docs/dashboard_screenshots';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 1100 } });

try {
  await page.goto(baseUrl, { waitUntil: 'networkidle' });
  await page.waitForSelector('#histogram-chart', { timeout: 30000 });
  await page.waitForTimeout(2500);

  const edaSection = page.locator('#distribution-section .chart-grid-2');
  await edaSection.screenshot({
    path: `${outputDir}/dashboard_eda_graficos.png`
  });

  await page.click('.tab-btn[data-target="ml-content"]');
  await page.waitForTimeout(1500);
  await page.waitForSelector('#model-comparison-chart', { timeout: 30000 });
  await page.waitForTimeout(2000);

  const mlSection = page.locator('#supervised-section .chart-grid-2').first();
  await mlSection.screenshot({
    path: `${outputDir}/dashboard_ml_graficos.png`
  });
} finally {
  await browser.close();
}
