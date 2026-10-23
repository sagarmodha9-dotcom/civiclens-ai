from __future__ import annotations

import json
from pathlib import Path

import duckdb
import pytest

from civiclens_lakehouse.pipeline import PARAMS, SchemaDriftError, build_duckdb, check_schema, render


@pytest.fixture
def built(raw_tree, tmp_path):
    db = tmp_path / "civiclens.duckdb"
    meta = build_duckdb(raw_tree, db)
    con = duckdb.connect(str(db), read_only=True)
    yield con, meta
    con.close()


def one(con, sql):
    return con.execute(sql).fetchone()[0]


# ---------------------------------------------------------------- schema + silver rules
def test_schema_drift_fails_loudly_with_the_missing_columns():
    with pytest.raises(SchemaDriftError) as ei:
        check_schema(["action_date", "_ingest_run_id"])
    assert "contract_transaction_unique_key" in str(ei.value) and "federal_action_obligation" in str(ei.value)


def test_fiscal_year_boundaries_and_cell_consistency(built):
    con, meta = built
    assert one(con, "SELECT fiscal_year FROM silver_contract_transactions WHERE transaction_key='K-A1'") == 2025   # 2024-10-01
    assert one(con, "SELECT fiscal_year FROM silver_contract_transactions WHERE transaction_key='K-A2'") == 2025   # 2025-09-30
    assert one(con, "SELECT fiscal_year FROM silver_contract_transactions WHERE transaction_key='K-A0'") == 2024   # 2023-10-01
    assert meta["dq"]["fiscal_year_matches_cell"]["pass"]


def test_rejects_carry_reasons_and_bronze_is_fully_accounted_for(built):
    con, meta = built
    reasons = dict(con.execute("SELECT transaction_key, reason FROM silver_rejects").fetchall())
    assert reasons["K-OUT"] == "psc out of scope" and reasons["K-GRANT"] == "not a contract award type"
    assert reasons.get("") == "missing transaction key" or reasons.get(None) == "missing transaction key"
    assert reasons["K-BADDATE"] == "unparseable action_date"
    assert meta["dq"]["bronze_accounted_for"]["pass"], meta["dq"]["bronze_accounted_for"]
    assert one(con, "SELECT COUNT(*) FROM silver_contract_transactions WHERE transaction_key IN ('K-OUT','K-GRANT','K-BADDATE')") == 0


def test_deobligations_stay_negative_and_award_fy_nets_correctly(built):
    con, _ = built
    assert float(one(con, "SELECT obligation FROM silver_contract_transactions WHERE transaction_key='K-A3'")) == -20000.0
    r = con.execute("SELECT obligations, deobligations, transactions FROM gold_award_fy WHERE award_key='AWD-A' AND fiscal_year=2025").fetchone()
    assert (float(r[0]), float(r[1]), r[2]) == (130000.0, -20000.0, 3)


def test_newest_run_wins_on_duplicate_key(raw_tree, tmp_path):
    # re-deliver K-B1 in a newer run with a corrected amount in the SAME cell file
    from conftest import AG, row, write_cell
    d = raw_tree / "agency=036" / "fy=2025"
    rows = list(__import__("csv").DictReader(open(d / "Contracts_PrimeTransactions_1.csv")))
    rows.append(row("K-B1", "AWD-B", "PIID-B", "2025-01-15", 80000.00, uei="UEI000002", name="BETA SYSTEMS", last_mod="2025-06-01"))
    write_cell(raw_tree, AG, 2025, rows, run_id="20261024T000000Z")
    meta = build_duckdb(raw_tree, tmp_path / "x.duckdb")
    con = duckdb.connect(str(tmp_path / "x.duckdb"), read_only=True)
    assert one(con, "SELECT COUNT(*) FROM silver_contract_transactions WHERE transaction_key='K-B1'") == 1
    assert float(one(con, "SELECT obligation FROM silver_contract_transactions WHERE transaction_key='K-B1'")) == 80000.0
    assert meta["dq"]["silver_unique_keys"]["pass"] and meta["dq"]["bronze_accounted_for"]["pass"]


# ---------------------------------------------------------------- gold reconciliation
def test_gold_tables_reconcile_to_silver_to_the_cent(built):
    con, meta = built
    assert meta["dq"]["gold_award_equals_silver"]["pass"] and meta["dq"]["gold_agency_equals_silver"]["pass"]
    s = float(one(con, "SELECT SUM(obligation) FROM silver_contract_transactions"))
    for t in ("gold_award_fy", "gold_agency_fy", "gold_recipient_agency_fy", "gold_psc_fy"):
        assert abs(float(one(con, f"SELECT SUM(obligations) FROM {t}")) - s) < 0.005, t


def test_every_dashboard_number_is_reproducible_from_silver(built):
    con, _ = built
    g = float(one(con, "SELECT obligations FROM gold_agency_fy WHERE fiscal_year=2025 AND it_category='IT services'"))
    s = float(one(con, "SELECT SUM(obligation) FROM silver_contract_transactions WHERE fiscal_year=2025 AND psc LIKE 'D%'"))
    assert abs(g - s) < 0.005


# ---------------------------------------------------------------- anomalies
def test_planted_outlier_is_flagged_and_ordinary_peers_are_not(built):
    con, _ = built
    st = dict(con.execute("SELECT award_key, status FROM anomaly_large_award WHERE psc_class2='D3' AND fiscal_year=2025").fetchall())
    assert st["AWD-OUTLIER"] == "flagged"
    flagged = [k for k, v in st.items() if v == "flagged"]
    assert flagged == ["AWD-OUTLIER"], flagged
    r = con.execute("SELECT peer_n, score, threshold, baseline_median FROM anomaly_large_award WHERE award_key='AWD-OUTLIER'").fetchone()
    assert r[0] == 44 and r[1] >= 3.5 and r[2] == 3.5 and 50_000 < r[3] < 200_000   # 40 peers + outlier + AWD-A, AWD-B, AWD-C (all D3)


def test_small_peer_groups_abstain_instead_of_scoring(built):
    con, _ = built
    st = con.execute("SELECT DISTINCT status FROM anomaly_large_award WHERE psc_class2='70'").fetchall()
    assert all(s[0].startswith("not scored") for s in st), st


@pytest.mark.parametrize("shape,limit", [("lognormal", 0.02), ("pareto", 0.06)])
def test_heavy_tail_flag_rate_is_bounded(tmp_path, shape, limit):
    """SYNTHETIC peer groups of 400 awards with NO planted outlier. Log-normal (sigma 1.2, the shape procurement
    obligations usually have) must flag <= 2%. A pure Pareto(1.5) is skewed even on the log scale and flags more;
    the bound here (6%) is the documented limit of a symmetric MAD rule, stated on the Methodology page."""
    import random
    from conftest import AG, row, write_cell
    rnd = random.Random(11)
    draw = (lambda: 10 ** rnd.gauss(5.0, 1.2)) if shape == "lognormal" else (lambda: 50_000 * rnd.paretovariate(1.5))
    rows = [row(f"K-H{i}", f"AWD-H{i}", f"PIID-H{i}", "2025-04-01", round(draw(), 2), uei=f"UEI{i:06d}", name=f"V{i}", psc="D399")
            for i in range(400)]
    write_cell(tmp_path / "raw", AG, 2025, rows)
    meta = build_duckdb(tmp_path / "raw", tmp_path / "h.duckdb")
    assert meta["dq"]["flag_rate_large_award"]["rate"] <= limit, meta["dq"]["flag_rate_large_award"]


def test_concentration_cell_is_flagged_with_top_recipient(built):
    con, _ = built
    r = con.execute("SELECT status, score, top_share, top_recipient_name, peer_n FROM anomaly_concentration "
                    "WHERE psc_class2='70' AND fiscal_year=2026").fetchone()
    assert r[0] == "flagged" and r[1] > 8000 and r[2] == 90.0 and r[3] == "GAMMA INC" and r[4] == 3


def test_recipient_growth_rules(built):
    con, _ = built
    g = dict(con.execute("SELECT recipient_name, status FROM anomaly_recipient_growth WHERE fiscal_year=2026").fetchall())
    assert g["GAMMA INC"] == "flagged"                      # 600k -> 11.5M, ratio > 3, delta > 2M
    g25 = dict(con.execute("SELECT recipient_name, status FROM anomaly_recipient_growth WHERE fiscal_year=2025").fetchall())
    assert g25["BETA SYSTEMS"].startswith("not scored")      # prior 10k < 500k base floor
    assert g25["ACME IT LLC"].startswith("not scored")       # prior year 10.00 < floor


def test_no_misconduct_vocabulary_in_limits_text(built):
    con, _ = built
    for t in ("anomaly_large_award", "anomaly_concentration", "anomaly_recipient_growth"):
        txt = one(con, f"SELECT MAX(limits) FROM {t}").lower()
        for banned in ("fraud", "waste", "abuse", "corrupt", "misconduct", "illegal"):
            assert banned not in txt, (t, banned)
        assert "not a finding of wrongdoing" in txt


def test_anomalies_are_deterministic_across_builds(raw_tree, tmp_path):
    a = build_duckdb(raw_tree, tmp_path / "a.duckdb"); b = build_duckdb(raw_tree, tmp_path / "b.duckdb")
    ca, cb = duckdb.connect(str(tmp_path / "a.duckdb"), read_only=True), duckdb.connect(str(tmp_path / "b.duckdb"), read_only=True)
    q = "SELECT award_key, status, ROUND(score, 6) FROM anomaly_large_award ORDER BY award_key, fiscal_year"
    assert ca.execute(q).fetchall() == cb.execute(q).fetchall()
    assert a["tables"] == b["tables"]


def test_sql_files_contain_no_unsubstituted_parameters():
    import re
    for name in ("anomalies.sql", "gold.sql", "silver_contract_transactions.sql", "silver_rejects.sql"):
        assert not re.search(r"\{[a-z_]+\}", render(name)), name
