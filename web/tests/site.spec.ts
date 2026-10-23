import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("overview loads real numbers, snapshot version and no console errors", async ({ page }) => {
  const errors: string[] = [];
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.locator(".kpi .value").first()).not.toHaveText("…", { timeout: 15_000 });
  await expect(page.getByText(/snapshot /).first()).toBeVisible();
  await expect(page.locator(".tbl tbody tr").first()).toBeVisible();
  expect(errors.filter((e) => !e.includes("favicon"))).toEqual([]);
});

test("scope filters propagate through URL, charts and the investigator scope", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Agency").selectOption("036");
  await page.getByLabel("Fiscal year").selectOption("2025");
  await expect(page).toHaveURL(/agency=036/); await expect(page).toHaveURL(/fy=2025/);
  await page.getByRole("link", { name: "Anomaly Lab" }).first().click();
  await expect(page).toHaveURL(/anomalies\?.*agency=036/);
  await expect(page.getByText(/Flagged in scope: \d+/)).toBeVisible();
  await page.getByRole("link", { name: "AI Investigator" }).first().click();
  await expect(page.getByText(/scope: Veterans Affairs · FY2025/)).toBeVisible();
});

test("anomaly detail explains the flag with peer group, baseline, score and limits", async ({ page }) => {
  await page.goto("/anomalies?agency=036&fy=2025");
  const why = page.getByRole("button", { name: "Why?" }).first();
  await expect(why).toBeVisible({ timeout: 15_000 });
  await why.click();
  await expect(page.getByText("Why this award-year was scored")).toBeVisible();
  for (const label of ["Peer group", "Peer size", "Baseline median", "Robust z (log10)", "Status"]) await expect(page.getByText(label, { exact: true })).toBeVisible();
  await expect(page.getByText(/not a finding of wrongdoing/).first()).toBeVisible();
  await expect(page.getByText(/Transactions in the snapshot/)).toBeVisible();
});

test("empty state when the scope has nothing, and reset clears it", async ({ page }) => {
  await page.goto("/anomalies?agency=028&fy=2022");
  await expect(page.getByText(/No flagged items in this scope/)).toBeVisible({ timeout: 15_000 });
  await page.getByRole("button", { name: "Reset" }).click();
  await expect(page).not.toHaveURL(/agency=028/);
});

test("API failure shows an error state, not a blank page", async ({ page }) => {
  await page.route("**/v1/overview**", (r) => r.fulfill({ status: 503, contentType: "application/json", body: JSON.stringify({ detail: "snapshot not available" }) }));
  await page.goto("/");
  await expect(page.getByRole("alert").first()).toContainText("snapshot not available");
  await expect(page.getByRole("button", { name: "Try again" })).toBeVisible();
});

test("investigator shows the disabled/cached mode honestly when live AI is off", async ({ page }) => {
  await page.goto("/investigator?agency=036&fy=2025");
  await page.getByLabel("Your question").fill("Which recipients received the most?");
  await page.getByRole("button", { name: "Ask" }).click();
  await expect(page.getByText(/live AI investigation is disabled|Facts \(computed by SQL/).first()).toBeVisible({ timeout: 20_000 });
});

test("methodology publishes the SQL and the anomaly status breakdown", async ({ page }) => {
  await page.goto("/methodology");
  await expect(page.getByText("The SQL behind each endpoint")).toBeVisible();
  const d = page.locator("details", { hasText: "anomalies_large" }).first();
  await d.locator("summary").click();
  await expect(d.locator("pre")).toContainText("FROM anomaly_large_award");
  await expect(page.getByRole("cell", { name: "large_award" })).toBeVisible();
});

test("no serious accessibility violations on the main pages", async ({ page }) => {
  for (const path of ["/", "/anomalies?agency=036&fy=2025", "/investigator", "/methodology"]) {
    await page.goto(path); await page.waitForTimeout(1500);
    const res = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
    const serious = res.violations.filter((v) => ["serious", "critical"].includes(v.impact ?? ""));
    expect(serious.map((v) => `${path}: ${v.id} ${v.nodes.length}`)).toEqual([]);
  }
});

test("mobile layout has no horizontal scroll and nav is reachable", async ({ page, isMobile }) => {
  test.skip(!isMobile, "mobile project only");
  await page.goto("/");
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  expect(overflow).toBe(false);
  await page.getByRole("link", { name: "Anomaly Lab" }).first().click();
  await expect(page.getByRole("heading", { name: "Anomaly Lab" })).toBeVisible();
});
