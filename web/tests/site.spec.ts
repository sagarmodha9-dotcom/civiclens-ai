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
  await page.getByLabel("Agency", { exact: true }).selectOption("036");
  await page.getByLabel("Fiscal year", { exact: true }).selectOption("2025");
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
  // Data-independent: find a scope with no flagged large awards from the API the site uses (the synthetic test snapshot and the
  // real snapshot differ; on real data SSA FY2022 has 4 flagged, which is why this test cannot hard-code a scope).
  const api = process.env.E2E_API_URL ?? "http://localhost:8000";
  let empty: string | null = null;
  outer: for (const agency of ["028", "013", "020", "075", "070", "036"]) for (const fy of [2022, 2023, 2024, 2025, 2026]) for (const psc of ["", "DK", "DC", "DJ", "DB", "DE"]) {
    const qs = `agency=${agency}&fy=${fy}${psc ? `&psc=${psc}` : ""}`;
    const r = await page.request.get(`${api}/v1/anomalies?detector=large_award&limit=1&${qs}`);
    if (r.ok() && ((await r.json()).items ?? []).length === 0) { empty = qs; break outer; }
  }
  expect(empty, "no empty large_award scope found in the snapshot").not.toBeNull();
  await page.goto(`/anomalies?${empty}`);
  await expect(page.getByText(/No flagged items in this scope/)).toBeVisible({ timeout: 15_000 });
  await page.getByRole("button", { name: "Reset" }).click();
  await expect(page).not.toHaveURL(/agency=/);
});

test("API failure shows an error state, not a blank page", async ({ page }) => {
  await page.route("**/v1/overview**", (r) => r.fulfill({ status: 503, contentType: "application/json", body: JSON.stringify({ detail: "snapshot not available" }) }));
  await page.goto("/");
  await expect(page.getByRole("alert").first()).toContainText("snapshot not available");
  await expect(page.getByRole("button", { name: "Try again" })).toBeVisible();
});

test("investigator answers with verified facts, or says honestly why it cannot (disabled / rate-limited)", async ({ page }) => {
  test.setTimeout(120_000);
  await page.goto("/investigator?agency=036&fy=2025");
  await page.getByLabel("Your question").fill("Which recipients received the most?");
  await page.getByRole("button", { name: "Ask" }).click();
  // a live Haiku answer with tool calls and server verification takes 20–60 s on the public API; cached answers return at once
  await expect(page.getByText(/live AI investigation is disabled|Facts \(computed by SQL|rate limit|limited|budget/i).first()).toBeVisible({ timeout: 90_000 });
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
