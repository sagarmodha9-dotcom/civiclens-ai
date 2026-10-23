"""Builds a small SYNTHETIC snapshot with the lakehouse pipeline (same code path as production) and serves the API
over it. Nothing here is a real federal figure."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "lakehouse")); sys.path.insert(0, str(ROOT / "lakehouse" / "tests")); sys.path.insert(0, str(ROOT / "api"))

import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("lakehouse_fixtures", ROOT / "lakehouse" / "tests" / "conftest.py")
_lf = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_lf)
_raw_tree = _lf.raw_tree


@pytest.fixture(scope="session")
def snapshot_path(tmp_path_factory) -> Path:
    from civiclens_lakehouse.pipeline import build_duckdb
    tmp = tmp_path_factory.mktemp("snap")
    root = _raw_tree.__wrapped__(tmp)
    db = tmp / "civiclens.duckdb"
    meta = build_duckdb(root, db)
    assert meta["dq"]["_all_pass"]
    return db


@pytest.fixture(scope="session")
def client(snapshot_path):
    os.environ["CIVICLENS_SNAPSHOT"] = str(snapshot_path)
    os.environ.pop("ANTHROPIC_API_KEY", None)
    from fastapi.testclient import TestClient
    import civiclens_api.main as m
    m.SNAPSHOT_PATH = snapshot_path; m._snapshot = None
    return TestClient(m.app)
