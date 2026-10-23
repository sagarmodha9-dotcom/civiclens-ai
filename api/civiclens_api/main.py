"""CivicLens API: read-only analytics over the versioned DuckDB snapshot, plus the AI investigator endpoint.

    CIVICLENS_SNAPSHOT=build/civiclens.duckdb uvicorn civiclens_api.main:app

Public and credential-free by design: no endpoint accepts SQL, every query is one of `queries.SQL`, parameters are
validated by pydantic, and the investigator is rate-limited and budget-capped (see investigator.py).
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import queries as q
from .queries import AGENCIES, Scope, Snapshot

SNAPSHOT_PATH = Path(os.environ.get("CIVICLENS_SNAPSHOT", "build/civiclens.duckdb"))
app = FastAPI(title="CivicLens AI API", version="0.1.0",
              description="Read-only analytics over a versioned snapshot of USAspending federal IT procurement data.")
app.add_middleware(CORSMiddleware, allow_origins=os.environ.get("CIVICLENS_CORS", "*").split(","), allow_methods=["GET", "POST"],
                   allow_headers=["*"])
_snapshot: Snapshot | None = None


def snapshot() -> Snapshot:
    global _snapshot
    if _snapshot is None:
        if not SNAPSHOT_PATH.exists():
            raise HTTPException(503, f"snapshot not available at {SNAPSHOT_PATH}")
        _snapshot = Snapshot(SNAPSHOT_PATH)
    return _snapshot


class ScopeParams(BaseModel):
    agency: str | None = Field(None, pattern=r"^\d{3}$")
    fy: int | None = Field(None, ge=2022, le=2026)
    psc: str | None = Field(None, pattern=r"^[A-Z0-9]{1,2}$")
    recipient: str | None = Field(None, pattern=r"^[A-Z0-9]{12}$")

    def scope(self) -> Scope:
        if self.agency and self.agency not in AGENCIES:
            raise HTTPException(422, f"unknown agency code {self.agency}; known: {sorted(AGENCIES)}")
        return Scope(self.agency, self.fy, self.psc, self.recipient)


def scope_dep(agency: str | None = None, fy: int | None = None, psc: str | None = None, recipient: str | None = None) -> Scope:
    try:
        return ScopeParams(agency=agency, fy=fy, psc=psc, recipient=recipient).scope()
    except ValueError as e:                     # pydantic validation of query params -> 422, never a 500
        raise HTTPException(422, str(e).splitlines()[0]) from None


@app.middleware("http")
async def timing(request: Request, call_next):
    t0 = time.perf_counter()
    resp = await call_next(request)
    resp.headers["X-Response-Time-ms"] = str(int((time.perf_counter() - t0) * 1000))
    resp.headers["X-Snapshot-Version"] = _snapshot.version if _snapshot else "none"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Cache-Control"] = "public, max-age=300" if request.method == "GET" and request.url.path.startswith("/v1/") and "investigate" not in request.url.path else "no-store"
    return resp


@app.get("/healthz")
def healthz():
    s = snapshot()
    return {"ok": True, "snapshot_version": s.version, "built_utc": s.meta.get("built_utc"), "dq_all_pass": s.meta.get("dq", {}).get("_all_pass")}


@app.get("/v1/meta")
def meta():
    return q.meta(snapshot())


@app.get("/v1/overview")
def overview(scope: Scope = Depends(scope_dep)):
    s = snapshot()
    return {"scope": scope.__dict__, "by_fiscal_year": q.overview_by_fy(s, scope), "by_agency": q.overview_by_agency(s, scope),
            "top_recipients": q.top_recipients(s, scope, 10), "psc_mix": q.psc_mix(s, scope, 10),
            "anomaly_counts": {d: len(q.anomalies(s, scope, d, 500)) for d in ("large_award", "concentration", "recipient_growth")}}


@app.get("/v1/agency")
def agency(scope: Scope = Depends(scope_dep)):
    s = snapshot()
    return {"scope": scope.__dict__, "agency_fy": q.agency_fy(s, scope), "top_recipients": q.top_recipients(s, scope, 15),
            "psc_mix": q.psc_mix(s, scope, 15), "yoy_recipients": q.yoy_recipients(s, scope, 15)}


@app.get("/v1/anomalies")
def anomalies(detector: Literal["large_award", "concentration", "recipient_growth"] = "large_award",
              limit: int = Query(50, ge=1, le=500), scope: Scope = Depends(scope_dep)):
    return {"scope": scope.__dict__, "detector": detector, "items": q.anomalies(snapshot(), scope, detector, limit)}


@app.get("/v1/anomalies/{award_key}/{fy}")
def anomaly_detail(award_key: str, fy: int):
    d = q.anomaly_detail(snapshot(), award_key, fy)
    if not d:
        raise HTTPException(404, "no scored award-year with that key and fiscal year")
    return d


@app.get("/v1/awards/{award_key}")
def award(award_key: str):
    d = q.award(snapshot(), award_key)
    if not d:
        raise HTTPException(404, "award not in snapshot")
    return d


@app.get("/v1/search")
def search(query: str = Query(..., min_length=2, max_length=80), scope: Scope = Depends(scope_dep)):
    return {"items": q.search_awards(snapshot(), scope, query)}


@app.get("/v1/sql")
def sql_catalogue():
    """The exact SQL behind every endpoint, for the Methodology page."""
    return {"queries": q.SQL, "row_cap": q.ROW_CAP}


# investigator is mounted lazily so the API runs without an Anthropic key (cached/disabled mode)
try:
    from .investigator import router as investigator_router
    app.include_router(investigator_router, prefix="/v1")
except Exception as e:  # noqa: BLE001
    @app.get("/v1/investigate")
    def investigator_unavailable():
        return {"status": "unavailable", "reason": f"investigator module not loaded: {type(e).__name__}"}
