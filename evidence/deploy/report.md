# Deployment — **PASS**

GitHub run `40115580863` · commit `7a2d939ddc26` · 2026-10-24T17:27:48+00:00 · snapshot `v20261023-1`

- API: https://civiclens-api.fly.dev — smoke success (healthz ok, snapshot version pinned, DQ pass, X-Snapshot-Version header)
- Site: https://civiclens-ai-smoky.vercel.app — deploy success
- Live e2e (Playwright desktop Chrome + Pixel 7 + axe WCAG 2.1 AA): success — {"expected": 21, "unexpected": 0, "skipped": 1, "duration_ms": 17674.694}
- Live API access-control smoke (CORS allowlist, 422 validation, 405 on writes, published SQL, headers, advertised rate limits): success — {"cors_rejects_unknown_origin": true, "cors_allows_site": true, "investigate_validates_input_422": true, "unknown_agency_rejected_422": true, "no_write_methods_405": true, "stream_validates_input_422": true, "stream_no_write_methods_405": true, "published_sql_readable": true, "security_headers": true, "rate_limits_advertised": true}
- Automated demo recording of the public site: success — docs/demo/civiclens-demo.mp4; screenshots: 10
- Cost: Fly.io shared-cpu-1x 512MB always-on + 1GB volume (approved <= $5/mo); Vercel Hobby free; Anthropic capped at $10/mo in console, app budget $5/mo.
