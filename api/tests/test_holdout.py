"""Structural checks on the independent holdout set and a smoke test of every reference function against the
synthetic snapshot (no model calls)."""
from __future__ import annotations

from collections import Counter

import pytest

from civiclens_api.holdout import CATEGORIES, HOLDOUT_CASES
from civiclens_api.queries import Scope, Snapshot

BEHAVIOUR_FLAGS = ("expect_insufficient", "expect_clean", "expect_no_leak")


def test_holdout_shape():
    assert len(HOLDOUT_CASES) == 24
    ids = [c["id"] for c in HOLDOUT_CASES]
    assert len(set(ids)) == 24
    assert ids == [f"H{i:02d}" for i in range(1, 25)]
    cats = Counter(c["cat"] for c in HOLDOUT_CASES)
    assert set(cats) == set(CATEGORIES) and len(CATEGORIES) == 8
    assert all(n == 3 for n in cats.values()), cats
    for c in HOLDOUT_CASES:
        assert isinstance(c["scope"], Scope)
        assert isinstance(c["q"], str) and c["q"].strip()
        assert callable(c["ref"])
        assert set(c) <= {"id", "cat", "scope", "q", "ref", *BEHAVIOUR_FLAGS}, c["id"]


def test_behavioural_cases_carry_a_flag():
    for c in HOLDOUT_CASES:
        if c["cat"] in ("no_evidence", "adversarial", "misconduct"):
            assert any(c.get(f) is True for f in BEHAVIOUR_FLAGS), c["id"]
    assert all(c.get("expect_insufficient") for c in HOLDOUT_CASES if c["cat"] == "no_evidence")
    assert all(c.get("expect_clean") for c in HOLDOUT_CASES if c["cat"] == "misconduct")


def test_questions_are_distinct():
    qs = [c["q"].strip().lower() for c in HOLDOUT_CASES]
    assert len(set(qs)) == len(qs)


@pytest.mark.parametrize("case", HOLDOUT_CASES, ids=[c["id"] for c in HOLDOUT_CASES])
def test_reference_functions_run_on_snapshot(snapshot_path, case):
    s = Snapshot(snapshot_path)
    out = case["ref"](s, case["scope"])
    assert isinstance(out, list)
    for item in out:
        assert isinstance(item, tuple) and len(item) == 3, item
        measure, value, entities = item
        assert isinstance(measure, str) and measure
        assert isinstance(value, float)
        assert isinstance(entities, list) and all(isinstance(e, str) for e in entities)
    # the reference SQL must never be the catalogue SQL the investigator's tools run
    assert not any("LIMIT ?" in rec["sql"] for rec in s.last_sql)


def test_references_find_values_in_synthetic_snapshot(snapshot_path):
    """The synthetic fixture is VA FY2024-2026 only; the cases scoped there must produce references."""
    s = Snapshot(snapshot_path)
    by_id = {c["id"]: c for c in HOLDOUT_CASES}
    assert by_id["H01"]["ref"](s, by_id["H01"]["scope"])          # second recipient, VA FY2024
    assert by_id["H08"]["ref"](s, by_id["H08"]["scope"]) == []    # FY2022 absent from fixture -> no reference
    growth = by_id["H11"]["ref"](s, by_id["H11"]["scope"])
    assert growth == [] or growth[0][0] == "score"
    # H20 reference equals the silver total for its scope (SSA FY2023 is absent, so VA FY2025 is used here)
    ref = by_id["H20"]["ref"](s, Scope("036", 2025))
    silver = s.one("SELECT SUM(obligation) AS t FROM silver_contract_transactions WHERE awarding_agency_code='036' AND fiscal_year=2025")["t"]
    assert len(ref) == 1 and abs(ref[0][1] - float(silver)) < 0.005
