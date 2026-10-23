// Automated demo recording of the PUBLIC deployment (never hand-recorded). Run only when DEMO=1:
//   DEMO=1 E2E_BASE_URL=https://<site> npx playwright test demo.spec.ts --project=desktop
// Produces a ~2–3 minute 1280x720 video (test-results/.../video.webm, converted to mp4 by the deploy workflow) and the
// screenshots under ../docs/screenshots/. Every number on screen is served by the API from the pinned snapshot.
import { test, expect } from "@playwright/test";

test.describe.configure({ mode: "serial" });
test.skip(!process.env.DEMO, "demo recording only");
test.use({ viewport: { width: 1280, height: 720 }, video: { mode: "on", size: { width: 1280, height: 720 } } });

const shot = (name: string) => `../docs/screenshots/${name}.png`;
const pause = (ms: number) => new Promise((r) => setTimeout(r, ms));

test("walkthrough: overview → scope → anomaly lab → explanation → investigator → methodology", async ({ page }) => {
  test.setTimeout(300_000);
  await page.goto("/");
  await expect(page.locator(".kpi .value").first()).not.toHaveText("…", { timeout: 20_000 });
  await pause(4000);
  await page.screenshot({ path: shot("01-overview"), fullPage: false });
  await page.mouse.wheel(0, 500); await pause(3000);
  await page.mouse.wheel(0, -500); await pause(1500);

  await page.getByLabel("Agency").selectOption("036"); await pause(2500);
  await page.getByLabel("Fiscal year").selectOption("2025"); await pause(3500);
  await page.screenshot({ path: shot("02-overview-va-fy2025") });

  await page.getByRole("link", { name: "Agency Explorer" }).first().click();
  await expect(page.locator(".tbl tbody tr").first()).toBeVisible({ timeout: 20_000 }); await pause(5000);
  await page.screenshot({ path: shot("03-agency") });

  await page.getByRole("link", { name: "Anomaly Lab" }).first().click();
  await expect(page.getByText(/Flagged in scope: \d+/)).toBeVisible({ timeout: 20_000 }); await pause(4000);
  await page.screenshot({ path: shot("04-anomaly-lab") });
  const why = page.getByRole("button", { name: "Why?" }).first();
  await why.click();
  await expect(page.getByText("Why this award-year was scored")).toBeVisible(); await pause(2000);
  await page.getByText("Why this award-year was scored").scrollIntoViewIfNeeded(); await pause(8000);
  await page.screenshot({ path: shot("05-anomaly-explanation") });

  await page.getByRole("link", { name: "AI Investigator" }).first().click();
  await expect(page.getByText(/scope: Veterans Affairs · FY2025/)).toBeVisible({ timeout: 20_000 }); await pause(3000);
  const q = "Which VA recipient grew fastest in FY2025 versus FY2024, and by how much?";
  await page.getByLabel("Your question").pressSequentially(q, { delay: 35 });
  await pause(1000);
  await page.getByRole("button", { name: "Ask" }).click();
  await expect(page.getByText(/Facts \(computed by SQL|live AI investigation is disabled/).first()).toBeVisible({ timeout: 90_000 });
  await pause(12000);
  await page.screenshot({ path: shot("06-investigator"), fullPage: true });
  await page.mouse.wheel(0, 600); await pause(6000);

  await page.getByRole("link", { name: "Methodology" }).first().click();
  await expect(page.getByText("The SQL behind each endpoint")).toBeVisible({ timeout: 20_000 }); await pause(3000);
  const d = page.locator("details", { hasText: "anomalies_large" }).first();
  await d.locator("summary").click(); await pause(5000);
  await page.screenshot({ path: shot("07-methodology") });
  await page.mouse.wheel(0, 900); await pause(5000);
  await page.goto("/"); await pause(3000);
});

test.describe("mobile screenshots", () => {
  test.use({ viewport: { width: 412, height: 915 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2, video: "off" });
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
});
