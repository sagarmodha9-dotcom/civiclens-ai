# Deployment — **FAIL**

GitHub run `40013076317` · commit `c4be8941ae9f` · 2026-10-23T19:39:15+00:00 · snapshot `v20261023-1`

- API:  — smoke skipped (healthz ok, snapshot version pinned, DQ pass, X-Snapshot-Version header)
- Site:  — deploy skipped
- Live e2e (Playwright desktop Chrome + Pixel 7 + axe WCAG 2.1 AA): skipped — {"error": "[Errno 2] No such file or directory: 'e2e-results.json'"}
- Live API access-control smoke (CORS allowlist, 422 validation, 405 on writes, published SQL, headers, advertised rate limits): skipped — {}
- Automated demo recording of the public site: skipped — none; screenshots: 0
- Cost: Fly.io shared-cpu-1x 512MB always-on + 1GB volume (approved <= $5/mo); Vercel Hobby free; Anthropic capped at $10/mo in console, app budget $5/mo.
