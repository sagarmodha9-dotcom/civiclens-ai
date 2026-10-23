"""The independent re-implementation must agree with the SQL detectors on the synthetic tree (planted outlier,
concentration cell, growth case), and the source trace must tie every sampled flagged value back to Bronze."""
import json
import subprocess
import sys
from pathlib import Path

from civiclens_lakehouse.pipeline import build_duckdb


def test_validation_agrees_with_pipeline(raw_tree: Path, tmp_path: Path):
    db = tmp_path / "snap.duckdb"
    build_duckdb(raw_tree, db)
    out = tmp_path / "ev"
    r = subprocess.run([sys.executable, "-m", "civiclens_lakehouse.validate_anomalies", "--snapshot", str(db), "--out", str(out)],
                       capture_output=True, text=True, cwd=Path(__file__).resolve().parents[1])
    assert r.returncode == 0, r.stdout + r.stderr
    rep = json.loads((out / "validation.json").read_text())
    assert rep["pass"] is True
    by = {x["detector"]: x for x in rep["recomputation"]}
    assert by["large_award"]["flagged_pipeline"] >= 1 and by["large_award"]["flagged_sets_identical"]
    assert by["concentration"]["flagged_pipeline"] >= 1 and by["concentration"]["flagged_sets_identical"]
    assert by["recipient_growth"]["flagged_sets_identical"]
    assert all(x["max_relative_score_diff"] <= 1e-6 for x in rep["recomputation"])
    traced = rep["source_trace"]
    assert any(t["detector"] == "large_award" and t["recipient"] == "GIANT CORP" and t["bronze_matches"] and t["silver_matches"] for t in traced)
    assert any(t["detector"] == "concentration" and t["top_recipient"] == "GAMMA INC" for t in traced)
    assert (out / "validation.md").read_text().startswith("# Anomaly engine validation — **PASS**")


def test_validation_detects_a_tampered_table(raw_tree: Path, tmp_path: Path):
    """If someone edits a score or un-flags a row after the fact, the recomputation must FAIL (the check has teeth)."""
    import duckdb
    db = tmp_path / "snap.duckdb"
    build_duckdb(raw_tree, db)
    con = duckdb.connect(str(db)); con.execute("UPDATE anomaly_large_award SET status = 'normal' WHERE status = 'flagged'"); con.close()
    out = tmp_path / "ev"
    r = subprocess.run([sys.executable, "-m", "civiclens_lakehouse.validate_anomalies", "--snapshot", str(db), "--out", str(out)],
                       capture_output=True, text=True, cwd=Path(__file__).resolve().parents[1])
    assert r.returncode == 1
    rep = json.loads((out / "validation.json").read_text())
    assert rep["pass"] is False and not [x for x in rep["recomputation"] if x["detector"] == "large_award"][0]["flagged_sets_identical"]
