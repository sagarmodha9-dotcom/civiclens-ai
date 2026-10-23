"""Every number the site shows comes from exactly one function here, each a parameterised SQL statement against the
read-only DuckDB snapshot. The AI investigator's tools call these same functions, so an AI "fact" is always a
value a dashboard endpoint could show. The SQL text is exposed on the Methodology page (`sql_for`).

Rules: parameters only through bind values (no string formatting of user input); every query has a row cap;
the connection is read-only; no function here writes.
"""
from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import duckdb

ROW_CAP = 2000
AGENCIES = {"036": "Department of Veterans Affairs", "070": "Department of Homeland Security",
            "075": "Department of Health and Human Services", "020": "Department of the Treasury",
            "013": "Department of Commerce", "028": "Social Security Administration"}
SETTLED_FYS = (2022, 2023, 2024, 2025)
PRELIMINARY_FYS = (2026,)


@dataclass(frozen=True)
class Scope:
    """The dashboard filter state. Also the hard boundary of what the AI investigator may query."""
    agency_code: str | None = None
    fiscal_year: int | None = None
    psc_class2: str | None = None
    recipient_uei: str | None = None

    def where(self, alias: str = "") -> tuple[str, list[Any]]:
        a = f"{alias}." if alias else ""
        clauses, params = [], []
        if self.agency_code:
            clauses.append(f"{a}awarding_agency_code = ?"); params.append(self.agency_code)
        if self.fiscal_year:
            clauses.append(f"{a}fiscal_year = ?"); params.append(int(self.fiscal_year))
        if self.psc_class2:
            clauses.append(f"{a}psc_class2 = ?"); params.append(self.psc_class2)
        if self.recipient_uei:
            clauses.append(f"{a}recipient_uei = ?"); params.append(self.recipient_uei)
        return (" WHERE " + " AND ".join(clauses)) if clauses else "", params


class Snapshot:
    """One read-only connection per process, serialised; DuckDB is fast enough that this is fine at demo scale."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self._con = duckdb.connect(str(self.path), read_only=True)
        self._lock = threading.Lock()
        self.meta = json.loads(self._con.execute("SELECT meta_json FROM _meta").fetchone()[0])
        self.version = self.meta.get("snapshot_version", "local")
        self.last_sql: list[dict] = []

    def rows(self, sql: str, params: list | None = None, cap: int = ROW_CAP) -> list[dict]:
        with self._lock:
            cur = self._con.execute(sql, params or [])
            cols = [d[0] for d in cur.description]
            out = [dict(zip(cols, r)) for r in cur.fetchmany(cap)]
        self.last_sql.append({"sql": sql, "params": params or [], "rows": len(out)})
        self.last_sql = self.last_sql[-50:]
        return out

    def one(self, sql: str, params: list | None = None) -> dict | None:
        r = self.rows(sql, params, cap=1)
        return r[0] if r else None


# ------------------------------------------------------------------ catalogue of queries (also shown on the site)
SQL = {
    "meta": "SELECT meta_json FROM _meta",
    "agency_fy": """SELECT awarding_agency_code, awarding_agency_name, fiscal_year, it_category, obligations, transactions, awards, recipients
                    FROM gold_agency_fy{where} ORDER BY awarding_agency_code, fiscal_year, it_category""",
    "overview_by_fy": """SELECT fiscal_year, SUM(obligations) AS obligations, SUM(transactions) AS transactions, SUM(awards) AS awards
                         FROM gold_agency_fy{where} GROUP BY fiscal_year ORDER BY fiscal_year""",
    "overview_by_agency": """SELECT awarding_agency_code, MAX(awarding_agency_name) AS awarding_agency_name, SUM(obligations) AS obligations,
                             SUM(awards) AS awards, SUM(recipients) AS recipient_rows FROM gold_agency_fy{where}
                             GROUP BY awarding_agency_code ORDER BY obligations DESC""",
    "top_recipients": """SELECT recipient_uei, MAX(recipient_name) AS recipient_name, SUM(obligations) AS obligations, SUM(awards) AS awards
                         FROM gold_recipient_agency_fy{where} GROUP BY recipient_uei ORDER BY obligations DESC LIMIT ?""",
    "psc_mix": """SELECT psc_class2, MAX(psc_example_description) AS description, SUM(obligations) AS obligations, SUM(awards) AS awards
                  FROM gold_psc_fy{where} GROUP BY psc_class2 ORDER BY obligations DESC LIMIT ?""",
    "yoy_recipients": """SELECT c.recipient_uei, MAX(c.recipient_name) AS recipient_name, SUM(c.obligations) AS obligations,
                         SUM(p.obligations) AS prior_obligations
                         FROM gold_recipient_agency_fy c LEFT JOIN gold_recipient_agency_fy p
                           ON p.recipient_uei = c.recipient_uei AND p.awarding_agency_code = c.awarding_agency_code AND p.fiscal_year = c.fiscal_year - 1
                         {where} GROUP BY c.recipient_uei HAVING SUM(p.obligations) IS NOT NULL ORDER BY SUM(c.obligations) - SUM(p.obligations) DESC LIMIT ?""",
    "anomalies_large": """SELECT detector, award_key, piid, fiscal_year, awarding_agency_code, awarding_agency_name, recipient_uei, recipient_name,
                          psc, psc_class2, value, unit, peer_n, baseline_median, baseline_mad_log10, score, threshold, status, limits, usaspending_permalink
                          FROM anomaly_large_award{where} AND status = 'flagged' ORDER BY score DESC LIMIT ?""",
    "anomalies_concentration": """SELECT * FROM anomaly_concentration{where} AND status = 'flagged' ORDER BY score DESC LIMIT ?""",
    "anomalies_growth": """SELECT * FROM anomaly_recipient_growth{where} AND status = 'flagged' ORDER BY score DESC LIMIT ?""",
    "anomaly_detail": """SELECT * FROM anomaly_large_award WHERE award_key = ? AND fiscal_year = ?""",
    "award_fy": """SELECT * FROM gold_award_fy WHERE award_key = ? ORDER BY fiscal_year""",
    "award_transactions": """SELECT transaction_key, action_date, fiscal_year, modification_number, obligation, action_type, psc, recipient_name,
                             awarding_sub_agency_name, last_modified_date, usaspending_permalink
                             FROM silver_contract_transactions WHERE award_key = ? ORDER BY action_date, modification_number LIMIT ?""",
    "peer_group": """SELECT award_key, piid, recipient_name, value, score, status FROM anomaly_large_award
                     WHERE awarding_agency_code = ? AND psc_class2 = ? AND fiscal_year = ? ORDER BY value DESC LIMIT ?""",
    "search_awards": """SELECT award_key, piid, fiscal_year, awarding_agency_name, recipient_name, psc, obligations, usaspending_permalink
                        FROM gold_award_fy{where} AND (lower(recipient_name) LIKE ? OR lower(piid) LIKE ?) ORDER BY obligations DESC LIMIT ?""",
}


def _where(scope: Scope, alias: str = "", require: bool = False) -> tuple[str, list]:
    w, p = scope.where(alias)
    if require and not w:
        w = " WHERE 1=1"
    return w, p


def sql_for(name: str) -> str:
    return SQL[name]


# ------------------------------------------------------------------ query functions (used by API and AI tools)
def meta(s: Snapshot) -> dict:
    m = dict(s.meta)
    m["snapshot_version"] = s.version
    m["settled_fiscal_years"] = list(SETTLED_FYS)
    m["preliminary_fiscal_years"] = list(PRELIMINARY_FYS)
    m["agencies"] = AGENCIES
    return m


def agency_fy(s: Snapshot, scope: Scope) -> list[dict]:
    w, p = _where(scope)
    return s.rows(SQL["agency_fy"].format(where=w), p)


def overview_by_fy(s: Snapshot, scope: Scope) -> list[dict]:
    w, p = _where(scope)
    return s.rows(SQL["overview_by_fy"].format(where=w), p)


def overview_by_agency(s: Snapshot, scope: Scope) -> list[dict]:
    w, p = _where(scope)
    return s.rows(SQL["overview_by_agency"].format(where=w), p)


def top_recipients(s: Snapshot, scope: Scope, limit: int = 15) -> list[dict]:
    w, p = _where(scope)
    return s.rows(SQL["top_recipients"].format(where=w), p + [min(limit, 100)])


def psc_mix(s: Snapshot, scope: Scope, limit: int = 15) -> list[dict]:
    w, p = _where(scope)
    return s.rows(SQL["psc_mix"].format(where=w), p + [min(limit, 100)])


def yoy_recipients(s: Snapshot, scope: Scope, limit: int = 15) -> list[dict]:
    w, p = _where(scope, alias="c")
    return s.rows(SQL["yoy_recipients"].format(where=w), p + [min(limit, 100)])


def anomalies(s: Snapshot, scope: Scope, detector: str = "large_award", limit: int = 50) -> list[dict]:
    key = {"large_award": "anomalies_large", "concentration": "anomalies_concentration", "recipient_growth": "anomalies_growth"}[detector]
    sc = scope if detector == "large_award" else Scope(scope.agency_code, scope.fiscal_year, scope.psc_class2, None)
    w, p = _where(sc, require=True)
    return s.rows(SQL[key].format(where=w), p + [min(limit, 500)])


def anomaly_detail(s: Snapshot, award_key: str, fiscal_year: int) -> dict | None:
    d = s.one(SQL["anomaly_detail"], [award_key, int(fiscal_year)])
    if not d:
        return None
    d["award_years"] = s.rows(SQL["award_fy"], [award_key])
    d["transactions"] = s.rows(SQL["award_transactions"], [award_key, 200])
    d["peer_group_sample"] = s.rows(SQL["peer_group"], [d["awarding_agency_code"], d["psc_class2"], int(fiscal_year), 25])
    return d


def award(s: Snapshot, award_key: str) -> dict | None:
    years = s.rows(SQL["award_fy"], [award_key])
    if not years:
        return None
    return {"award_key": award_key, "years": years, "transactions": s.rows(SQL["award_transactions"], [award_key, 500])}


def search_awards(s: Snapshot, scope: Scope, q: str, limit: int = 25) -> list[dict]:
    w, p = _where(scope, require=True)
    like = f"%{q.lower().strip()}%"
    return s.rows(SQL["search_awards"].format(where=w), p + [like, like, min(limit, 100)])
