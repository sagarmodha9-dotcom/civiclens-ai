"""Databricks preflight: discover what this workspace supports and prove each capability separately.

    DATABRICKS_HOST=... DATABRICKS_TOKEN=... python lakehouse/databricks/preflight.py --out evidence/databricks

Steps (each PASS/FAIL on its own, nothing is inferred from another step):
  1 identity          SCIM Me -> user name
  2 catalogs          list catalogs with names; choose the working catalog: $DATABRICKS_CATALOG if set, else `workspace`
                      if present, else the first non-system catalog. Never tries to create a catalog (Free Edition has no
                      metastore storage root: CREATE CATALOG -> 400 INVALID_STATE, recorded 2026-10-23).
  3 schemas           CREATE SCHEMA IF NOT EXISTS <catalog>.bronze/silver/gold via UC API (ALREADY_EXISTS counts as pass)
  4 volume            CREATE managed VOLUME <catalog>.bronze.raw (ALREADY_EXISTS counts as pass)
  5 files             Files API PUT, GET (content must round-trip), DELETE under /Volumes/<catalog>/bronze/raw/_preflight/
  6 jobs_list         Jobs API list
  7 job_execution     import a one-cell notebook, submit a one-off serverless run, poll to TERMINATED, require SUCCESS and
                      the notebook's exit value to echo the run id. This is real compute, not an API ping.
Writes <out>/preflight.md and preflight.json stamped with GITHUB_RUN_ID, GITHUB_SHA, UTC time and an overall PASS/FAIL.
Exit 0 only if every step passes.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

import requests

SYSTEM_CATALOGS = {"system", "samples", "hive_metastore", "__databricks_internal"}


class DBX:
    def __init__(self, host: str, token: str):
        self.host, self.h = host.rstrip("/"), {"Authorization": f"Bearer {token}"}

    def req(self, method: str, path: str, **kw) -> requests.Response:
        kw.setdefault("timeout", 120)
        return requests.request(method, f"{self.host}{path}", headers={**self.h, **kw.pop("headers", {})}, **kw)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="evidence/databricks")
    ap.add_argument("--catalog", default=os.environ.get("DATABRICKS_CATALOG", ""))
    ap.add_argument("--skip-job", action="store_true")
    a = ap.parse_args()
    host, tok = os.environ.get("DATABRICKS_HOST", ""), os.environ.get("DATABRICKS_TOKEN", "")
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    stamp = {"run_id": os.environ.get("GITHUB_RUN_ID", "local"), "commit": os.environ.get("GITHUB_SHA", "local")[:12],
             "utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "host": host}
    steps: list[dict] = []

    def step(name: str, ok: bool, http: int | None, note: str):
        steps.append({"step": name, "pass": bool(ok), "http": http, "note": note[:300]}); print(f"{'PASS' if ok else 'FAIL'} {name}: {http} {note[:200]}", flush=True)

    if not host or not tok:
        step("secrets", False, None, "DATABRICKS_HOST / DATABRICKS_TOKEN not set"); return finish(out, stamp, steps, None)
    d = DBX(host, tok)

    # 1 identity
    r = d.req("GET", "/api/2.0/preview/scim/v2/Me")
    who = r.json().get("userName", "?") if r.ok else r.text[:100]
    step("identity", r.ok, r.status_code, who)

    # 2 catalogs
    r = d.req("GET", "/api/2.1/unity-catalog/catalogs")
    cats = [c.get("name") for c in r.json().get("catalogs", [])] if r.ok else []
    usable = [c for c in cats if c not in SYSTEM_CATALOGS]
    catalog = a.catalog or ("workspace" if "workspace" in cats else (usable[0] if usable else ""))
    step("catalogs", r.ok and bool(catalog), r.status_code, f"catalogs={cats}; chosen={catalog or 'NONE'}")
    if not catalog:
        return finish(out, stamp, steps, None)
    (out / "catalog.txt").write_text(catalog)

    # 3 schemas
    for s in ("bronze", "silver", "gold"):
        r = d.req("POST", "/api/2.1/unity-catalog/schemas", json={"name": s, "catalog_name": catalog})
        code = r.json().get("error_code", "") if not r.ok else ""
        step(f"schema {catalog}.{s}", r.ok or code in ("SCHEMA_ALREADY_EXISTS", "ALREADY_EXISTS"), r.status_code, code or "created")

    # 4 volume
    r = d.req("POST", "/api/2.1/unity-catalog/volumes", json={"name": "raw", "catalog_name": catalog, "schema_name": "bronze", "volume_type": "MANAGED"})
    code = r.json().get("error_code", "") if not r.ok else ""
    step(f"volume {catalog}.bronze.raw", r.ok or code in ("VOLUME_ALREADY_EXISTS", "ALREADY_EXISTS"), r.status_code, code or r.json().get("storage_location", "created"))

    # 5 files round trip
    payload = f"civiclens preflight {stamp['run_id']} {stamp['utc']}".encode()
    fpath = f"/api/2.0/fs/files/Volumes/{catalog}/bronze/raw/_preflight/{stamp['run_id']}.txt"
    r = d.req("PUT", fpath, data=payload, headers={"Content-Type": "application/octet-stream"}); step("files PUT", r.ok, r.status_code, r.text[:100])
    r = d.req("GET", fpath); step("files GET round-trip", r.ok and r.content == payload, r.status_code, "content matches" if r.content == payload else r.text[:100])
    r = d.req("DELETE", fpath); step("files DELETE", r.ok, r.status_code, r.text[:100])

    # 6 jobs list
    r = d.req("GET", "/api/2.1/jobs/list", params={"limit": 1}); step("jobs list", r.ok, r.status_code, f"{len(r.json().get('jobs', []))} job(s) visible")

    # 7 real job execution (serverless, one-off)
    if not a.skip_job:
        nb_path = f"/Users/{who}/civiclens-ai/_preflight"
        src = ("# Databricks notebook source\n"
               f"ok = spark.sql(\"SELECT current_catalog() AS c, current_user() AS u\").collect()[0]\n"
               f"spark.sql(\"CREATE SCHEMA IF NOT EXISTS {catalog}.bronze\")\n"
               f"spark.sql(\"CREATE OR REPLACE TABLE {catalog}.bronze._preflight AS SELECT '{stamp['run_id']}' AS run_id, current_timestamp() AS ts\")\n"
               f"n = spark.table(\"{catalog}.bronze._preflight\").count()\n"
               f"dbutils.notebook.exit(f\"run_id={stamp['run_id']} rows={{n}} user={{ok.u}}\")\n")
        d.req("POST", "/api/2.0/workspace/mkdirs", json={"path": f"/Users/{who}/civiclens-ai"})
        r = d.req("POST", "/api/2.0/workspace/import", json={"path": nb_path, "content": base64.b64encode(src.encode()).decode(), "overwrite": True, "format": "SOURCE", "language": "PYTHON"})
        step("notebook import", r.ok, r.status_code, nb_path if r.ok else r.text[:150])
        if r.ok:
            r = d.req("POST", "/api/2.1/jobs/runs/submit", json={"run_name": f"civiclens-preflight-{stamp['run_id']}", "tasks": [{"task_key": "preflight", "notebook_task": {"notebook_path": nb_path}}], "timeout_seconds": 1200})
            if not r.ok:
                step("job submit (serverless)", False, r.status_code, r.text[:200])
            else:
                run_id = r.json()["run_id"]; t0 = time.time(); st = {}
                while time.time() - t0 < 1200:
                    g = d.req("GET", "/api/2.1/jobs/runs/get", params={"run_id": run_id}).json(); st = g.get("state", {})
                    print("  job state:", st.get("life_cycle_state"), st.get("result_state", ""), flush=True)
                    if st.get("life_cycle_state") in ("TERMINATED", "SKIPPED", "INTERNAL_ERROR"): break
                    time.sleep(15)
                task_run = (g.get("tasks") or [{}])[0].get("run_id", run_id)
                o = d.req("GET", "/api/2.1/jobs/runs/get-output", params={"run_id": task_run}).json()
                result = (o.get("notebook_output") or {}).get("result", "")
                ok = st.get("result_state") == "SUCCESS" and f"run_id={stamp['run_id']}" in result
                step("job execution (serverless notebook, Delta table write+count)", ok, 200,
                     f"state={st.get('result_state')} output={result or o.get('error', '')[:150]} url={g.get('run_page_url', '')}")
                stamp["job_run_page_url"] = g.get("run_page_url")
    return finish(out, stamp, steps, catalog)


def finish(out: Path, stamp: dict, steps: list[dict], catalog: str | None) -> int:
    ok = all(s["pass"] for s in steps)
    rep = {"stamp": stamp, "catalog": catalog, "steps": steps, "pass": ok}
    (out / "preflight.json").write_text(json.dumps(rep, indent=1))
    md = [f"# Databricks preflight — **{'PASS' if ok else 'FAIL'}**", "",
          f"GitHub run `{stamp['run_id']}` · commit `{stamp['commit']}` · {stamp['utc']} · host `{stamp['host']}` · working catalog `{catalog}`", "",
          "Free Edition has no metastore storage root, so `CREATE CATALOG` is not supported (400 INVALID_STATE on 2026-10-23); the lakehouse uses the "
          "built-in `workspace` catalog. Each row below is tested on its own; nothing is inferred.", "",
          "| step | result | HTTP | note |", "|---|---|---|---|"]
    md += [f"| {s['step']} | {'PASS' if s['pass'] else 'FAIL'} | {s['http'] or ''} | {s['note'].replace('|', '/')} |" for s in steps]
    if stamp.get("job_run_page_url"):
        md += ["", f"Job run page: {stamp['job_run_page_url']}"]
    (out / "preflight.md").write_text("\n".join(md) + "\n")
    print(f"\npreflight {'PASS' if ok else 'FAIL'} -> {out}/preflight.md")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
