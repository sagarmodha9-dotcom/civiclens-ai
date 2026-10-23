"""Ingestion worker: pull contract transactions per agency x fiscal year into raw/ with a provenance manifest.

    python -m civiclens_ingest.worker --out data/raw --agency "Department of Veterans Affairs" --fy 2025

Idempotent: a cell (agency, FY) that already has a manifest with status "complete" and whose API count has not
changed is skipped; otherwise the previous files stay in place until the new download has fully landed and
verified, then the cell's `manifest.json` is swapped atomically. Nothing is appended across runs; Silver
deduplicates on the transaction unique key and prefers the newest run_id.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from .client import ApiError, UsaSpendingClient, contract_filters, fy_window, stable_hash

MANIFEST_VERSION = 1


def cell_dir(root: Path, agency_code: str, fy: int) -> Path:
    return root / f"agency={agency_code}" / f"fy={fy}"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def count_csv_rows(p: Path) -> int:
    with open(p, "rb") as f:
        return max(sum(1 for _ in f) - 1, 0)      # header excluded; the probe tells us if any file lacks one


def pull_cell(c: UsaSpendingClient, root: Path, agency_code: str, agency_name: str, fy: int,
              force: bool = False, poll_seconds: float = 15.0) -> dict:
    d = cell_dir(root, agency_code, fy)
    d.mkdir(parents=True, exist_ok=True)
    filters = contract_filters(agency_name, fy)
    filter_hash = stable_hash(filters)
    prev = json.loads((d / "manifest.json").read_text()) if (d / "manifest.json").exists() else None
    api_last_updated = c.last_updated()
    count = c.download_count(filters)
    expected = count.get("calculated_transaction_count")
    if count.get("transaction_rows_gt_limit"):
        raise ApiError(0, f"cell {agency_code}/{fy} exceeds the API's download row limit "
                          f"({count.get('maximum_transaction_limit')}); split the cell by quarter")
    if prev and not force and prev.get("status") == "complete" and prev.get("filter_hash") == filter_hash \
            and prev.get("api_count") == expected and prev.get("api_last_updated") == api_last_updated:
        return {**prev, "skipped": True}

    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    tmp = Path(tempfile.mkdtemp(prefix=f"civiclens-{agency_code}-{fy}-", dir=d))
    try:
        sub = c.request_transaction_download(filters)
        status = c.wait_for_download(sub["file_name"], poll_seconds=poll_seconds)
        zpath = tmp / sub["file_name"]
        meta = c.fetch_file(status.get("file_url") or sub.get("file_url"), zpath)
        files = []
        with zipfile.ZipFile(zpath) as z:
            for info in z.infolist():
                if info.filename.lower().endswith(".csv"):
                    z.extract(info, tmp)
                    p = tmp / info.filename
                    files.append({"name": info.filename, "bytes": p.stat().st_size, "sha256": sha256_file(p),
                                  "rows": count_csv_rows(p)})
        rows = sum(f["rows"] for f in files)
        manifest = {
            "manifest_version": MANIFEST_VERSION, "run_id": run_id, "status": "complete",
            "source": {"base": c.base, "endpoint": "/api/v2/download/transactions/", "file_name": sub["file_name"],
                       "file_url": status.get("file_url") or sub.get("file_url")},
            "request": {"filters": filters, "file_format": "csv"}, "filter_hash": filter_hash,
            "agency_code": agency_code, "agency_name": agency_name, "fiscal_year": fy, "window": fy_window(fy),
            "extracted_utc": run_id, "api_last_updated": api_last_updated,
            "api_count": expected, "api_count_response": count, "download_status": status,
            "zip": {"name": sub["file_name"], **meta}, "files": files, "rows_total": rows,
            "count_matches": (expected == rows) if expected is not None else None,
            "calls": c.records_json()[-6:],
        }
        if manifest["count_matches"] is False:
            manifest["status"] = "count_mismatch"       # kept, loadable, but flagged; publish gate decides
        # atomic swap: move files in, then write manifest last
        for f in files:
            shutil.move(str(tmp / f["name"]), str(d / f["name"]))
        shutil.move(str(zpath), str(d / zpath.name))
        tmp_manifest = d / "manifest.json.tmp"
        tmp_manifest.write_text(json.dumps(manifest, indent=1, default=str))
        os.replace(tmp_manifest, d / "manifest.json")
        return manifest
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/raw")
    ap.add_argument("--agency-code", required=True)
    ap.add_argument("--agency", required=True, help="awarding toptier agency name as USAspending spells it")
    ap.add_argument("--fy", type=int, required=True)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    c = UsaSpendingClient()
    try:
        m = pull_cell(c, Path(a.out), a.agency_code, a.agency, a.fy, force=a.force)
    except ApiError as e:
        print(f"FAILED {a.agency_code}/{a.fy}: {e}")
        return 1
    finally:
        c.close()
    print(json.dumps({k: m.get(k) for k in ("agency_code", "fiscal_year", "status", "skipped", "api_count",
                                             "rows_total", "count_matches", "run_id")}, indent=1))
    return 0 if m.get("status") == "complete" else 2


if __name__ == "__main__":
    sys.exit(main())
