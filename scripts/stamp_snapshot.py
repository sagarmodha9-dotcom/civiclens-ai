"""Stamp a built DuckDB file as an immutable, versioned snapshot, refusing if the DQ gate failed.

    python scripts/stamp_snapshot.py --db build/civiclens.duckdb --version v12 --source-run 39961334170 --out dist/

Writes dist/civiclens_v12.duckdb (with _meta.snapshot_version set), dist/civiclens_v12.sha256, dist/snapshot.json
(version, as-of = API last_updated seen at ingest, built_utc, row counts, DQ summary, anomaly summary, source run id).
Promotion to 'latest' is a separate step (publish workflow) so a bad build can never overwrite a good one.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

import duckdb


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True); ap.add_argument("--version", required=True); ap.add_argument("--source-run", default="")
    ap.add_argument("--raw", default="data/raw"); ap.add_argument("--out", default="dist")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(a.db, read_only=True)
    meta = json.loads(con.execute("SELECT meta_json FROM _meta").fetchone()[0]); con.close()
    if not meta["dq"]["_all_pass"]:
        failing = [k for k, v in meta["dq"].items() if not k.startswith("_") and not v.get("pass")]
        print(f"REFUSED: DQ gate failed: {failing}"); return 1
    # as-of = the API last_updated recorded by the manifests (all cells should agree; report the set)
    asof = sorted({json.loads(m.read_text()).get("api_last_updated") for m in Path(a.raw).rglob("manifest.json")
                   if m.parent.name.startswith("fy=")} - {None})
    dest = out / f"civiclens_{a.version}.duckdb"
    shutil.copyfile(a.db, dest)
    con = duckdb.connect(str(dest))
    meta.update({"snapshot_version": a.version, "source_ingest_run": a.source_run, "api_last_updated": asof, "schema_version": 1})
    con.execute("CREATE OR REPLACE TABLE _meta AS SELECT ? AS meta_json", [json.dumps(meta, default=str)]); con.close()
    sha = hashlib.sha256(dest.read_bytes()).hexdigest()
    (out / f"civiclens_{a.version}.sha256").write_text(f"{sha}  {dest.name}\n")
    manifest = {"version": a.version, "file": dest.name, "sha256": sha, "bytes": dest.stat().st_size, "built_utc": meta["built_utc"],
                "api_last_updated": asof, "source_ingest_run": a.source_run, "tables": meta["tables"], "dq_all_pass": True,
                "anomaly_summary": meta.get("anomaly_summary"), "schema_version": 1}
    (out / "snapshot.json").write_text(json.dumps(manifest, indent=1))
    print(json.dumps({k: manifest[k] for k in ("version", "file", "sha256", "bytes", "api_last_updated")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
