// Phone-width screenshots of the PUBLIC deployment (DEMO=1 only). Separate file: test.use() with device options at
// describe level is rejected by Playwright when the file also sets video options at the top level.
import { test, expect } from "@playwright/test";

test.skip(!process.env.DEMO, "demo recording only");
test.use({ viewport: { width: 412, height: 915 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });

const shot = (name: string) => `../docs/screenshots/${name}.png`;
const pause = (ms: number) => new Promise((r) => setTimeout(r, ms));

test("phone-width pages", async ({ page }) => {
  test.setTimeout(120_000);
  await page.goto("/?agency=036&fy=2025");
  await expect(page.locator(".kpi .value").first()).not.toHaveText("…", { timeout: 20_000 }); await pause(1500);
  await page.screenshot({ path: shot("m1-overview"), fullPage: true });
  await page.goto("/anomalies?agency=036&fy=2025");
  await expect(page.getByText(/Flagged in scope: \d+/)).toBeVisible({ timeout: 20_000 }); await pause(1500);
  await page.screenshot({ path: shot("m2-anomaly-lab"), fullPage: false });
  await page.goto("/investigator?agency=036&fy=2025"); await pause(2500);
  await page.screenshot({ path: shot("m3-investigator"), fullPage: false });
});
