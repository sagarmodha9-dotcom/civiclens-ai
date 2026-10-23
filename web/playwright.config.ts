import { defineConfig, devices } from "@playwright/test";
export default defineConfig({
  testDir: "./tests", testIgnore: process.env.DEMO ? [] : ["**/demo.spec.ts"], timeout: 30_000, retries: 0, reporter: [["list"], ["json", { outputFile: "test-results/results.json" }]],
  use: { baseURL: process.env.E2E_BASE_URL ?? "http://localhost:3000", trace: "retain-on-failure" },
  projects: [{ name: "desktop", use: { ...devices["Desktop Chrome"] } }, { name: "mobile", use: { ...devices["Pixel 7"] } }],
});
