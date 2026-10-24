"""Build the synthetic DuckDB snapshot the browser tests run against in CI (the same raw tree the API/lakehouse tests use).

    python scripts/make_e2e_snapshot.py build/e2e.duckdb

Synthetic data only — no network, no real agencies' figures. The DQ gate must pass or this exits non-zero, so a broken pipeline
cannot hide behind a green browser test."""
import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lakehouse_fixtures", ROOT / "lakehouse" / "tests" / "conftest.py")
lf = importlib.util.module_from_spec(spec); spec.loader.exec_module(lf)
from civiclens_lakehouse.pipeline import build_duckdb  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1 else "build/e2e.duckdb")
out.parent.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    raw = lf.raw_tree.__wrapped__(Path(tmp))
    meta = build_duckdb(raw, out)
ok = bool(meta["dq"]["_all_pass"])
print(f"snapshot {out} built: dq_all_pass={ok} tables={ {k: v for k, v in meta.get('tables', {}).items()} }")
sys.exit(0 if ok else 1)
