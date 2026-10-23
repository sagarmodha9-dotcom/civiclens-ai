"""USAspending API v2 client: the only module that talks to api.usaspending.gov.

Design rules
- One request in flight; exponential backoff on 429/5xx/transport errors; every request has a wall-clock timeout.
- Nothing here interprets data. It returns parsed JSON or saves a file, and records what it did (URL, request body,
  status, timing, response keys) so `probe.py` and the worker can write provenance without re-deriving it.
- Endpoint paths and request shapes live in one place (`Endpoints`) so a live probe can falsify them.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import httpx

BASE = "https://api.usaspending.gov"
CONTRACT_TYPES = ["A", "B", "C", "D"]          # BPA call, purchase order, delivery order, definitive contract
USER_AGENT = "civiclens-ai/0.1 (+https://github.com/sagarmodha9-dotcom/civiclens-ai)"


class Endpoints:
    last_updated = "/api/v2/awards/last_updated/"
    toptier_agencies = "/api/v2/references/toptier_agencies/"
    download_count = "/api/v2/download/count/"
    download_transactions = "/api/v2/download/transactions/"
    download_status = "/api/v2/download/status/"
    spending_by_award = "/api/v2/search/spending_by_award/"
    spending_by_award_count = "/api/v2/search/spending_by_award_count/"
    award = "/api/v2/awards/{id}/"
    transactions = "/api/v2/transactions/"


class ApiError(Exception):
    def __init__(self, status: int, message: str, url: str = ""):
        super().__init__(f"{status}: {message}")
        self.status, self.url = status, url


@dataclass
class CallRecord:
    """What happened on one logical call (retries included), kept for provenance."""
    method: str
    url: str
    request: Any
    status: int | None
    attempts: int
    elapsed_ms: int
    response_keys: list[str] = field(default_factory=list)
    error: str | None = None
    started_utc: str = ""


def fy_window(fy: int) -> tuple[str, str]:
    """Federal fiscal year n runs Oct 1 of n-1 through Sep 30 of n."""
    return f"{fy - 1}-10-01", f"{fy}-09-30"


def contract_filters(agency_name: str, fy: int, psc_prefixes: tuple[str, ...] = ("D", "70")) -> dict:
    """The ONE filter body used for counts, downloads and reconciliation, so every comparison is same-scope.

    PSC codes are passed as the search API's tree form: ["Service", "D"] selects every D-series service PSC,
    ["Product", "70"] every 70-series product PSC. The live probe records whether the count endpoint accepts
    this form; if it does not, the probe fails loudly rather than silently widening the scope.
    """
    start, end = fy_window(fy)
    psc = []
    for p in psc_prefixes:
        psc.append(["Service", p] if p.isalpha() else ["Product", p])
    return {
        "time_period": [{"start_date": start, "end_date": end, "date_type": "action_date"}],
        "award_type_codes": list(CONTRACT_TYPES),
        "agencies": [{"type": "awarding", "tier": "toptier", "name": agency_name}],
        "psc_codes": {"require": psc},
    }


class UsaSpendingClient:
    def __init__(self, base: str = BASE, timeout: float = 60.0, max_retries: int = 5,
                 sleep: Callable[[float], None] = time.sleep, transport: httpx.BaseTransport | None = None):
        self.base, self.timeout, self.max_retries, self._sleep = base.rstrip("/"), timeout, max_retries, sleep
        self._http = httpx.Client(timeout=timeout, headers={"User-Agent": USER_AGENT}, transport=transport)
        self.records: list[CallRecord] = []

    # ------------------------------------------------------------------ core
    def _call(self, method: str, path: str, body: dict | None = None, params: dict | None = None) -> Any:
        url = self.base + path
        delay, attempts, t0 = 1.0, 0, time.perf_counter()
        started = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
        last_err: str | None = None
        status: int | None = None
        while attempts <= self.max_retries:
            attempts += 1
            try:
                r = self._http.request(method, url, json=body, params=params)
                status = r.status_code
            except httpx.HTTPError as e:                      # timeout, connection reset, DNS
                last_err = type(e).__name__
                if attempts > self.max_retries:
                    break
                self._sleep(min(delay, 60.0)); delay *= 2
                continue
            if status in (429, 500, 502, 503, 504) and attempts <= self.max_retries:
                ra = r.headers.get("retry-after")
                self._sleep(min(float(ra) if ra and ra.isdigit() else delay, 60.0)); delay *= 2
                last_err = f"HTTP {status}"
                continue
            if status >= 400:
                detail = r.text[:300]
                self.records.append(CallRecord(method, url, body or params, status, attempts,
                                               int((time.perf_counter() - t0) * 1000), [], detail, started))
                raise ApiError(status, detail, url)
            data = r.json() if r.content else {}
            keys = sorted(data.keys()) if isinstance(data, dict) else ["<list>"]
            self.records.append(CallRecord(method, url, body or params, status, attempts,
                                           int((time.perf_counter() - t0) * 1000), keys, None, started))
            return data
        self.records.append(CallRecord(method, url, body or params, status, attempts,
                                       int((time.perf_counter() - t0) * 1000), [], last_err, started))
        raise ApiError(status or 0, f"no response after {attempts} attempts ({last_err})", url)

    # ------------------------------------------------------------------ endpoints
    def last_updated(self) -> str:
        return self._call("GET", Endpoints.last_updated)["last_updated"]

    def toptier_agencies(self) -> list[dict]:
        return self._call("GET", Endpoints.toptier_agencies).get("results", [])

    def download_count(self, filters: dict) -> dict:
        """Probed 2026-10-23: returns calculated_count, maximum_limit, rows_gt_limit, spending_level, messages, plus
        the deprecated transaction_* twins. We send spending_level explicitly and read the new names."""
        return self._call("POST", Endpoints.download_count, {"filters": filters, "spending_level": "transactions"})

    def request_transaction_download(self, filters: dict, columns: list[str] | None = None) -> dict:
        """Probed 2026-10-23: the job's zip is named PrimeTransactionsAndSubawards_*.zip and its status total_rows
        counts prime AND sub-award rows (272 vs a prime count of 235 for SSA FY2026). The worker must count only
        the prime-transaction CSV."""
        body: dict = {"filters": filters, "file_format": "csv", "spending_level": "transactions"}
        if columns:
            body["columns"] = columns
        return self._call("POST", Endpoints.download_transactions, body)

    def download_status(self, file_name: str) -> dict:
        return self._call("GET", Endpoints.download_status, params={"file_name": file_name})

    def wait_for_download(self, file_name: str, poll_seconds: float = 10.0, max_wait_seconds: float = 1800.0) -> dict:
        waited = 0.0
        while True:
            s = self.download_status(file_name)
            if s.get("status") == "finished":
                return s
            if s.get("status") == "failed":
                raise ApiError(0, f"download job failed: {s.get('message')}", Endpoints.download_status)
            if waited >= max_wait_seconds:
                raise ApiError(0, f"download not finished after {int(waited)} s (status={s.get('status')})",
                               Endpoints.download_status)
            self._sleep(poll_seconds); waited += poll_seconds

    def fetch_file(self, url: str, dest: Path, timeout: float = 300.0) -> dict:
        """Stream a (zip) file to disk with retries; returns size and sha256.

        Regression (run 39961334170, 2026-10-23): the first full pull died here on DHS FY2022 when the file server
        dropped the connection before sending response headers. The job had already finished; only the fetch was
        unlucky. Now: up to max_retries attempts with backoff, a file-server timeout of its own, partial files
        removed on failure, and any transport error surfaced as ApiError so the caller can record it per cell."""
        dest.parent.mkdir(parents=True, exist_ok=True)
        delay, last = 2.0, "unknown"
        for attempt in range(1, self.max_retries + 2):
            h, size, t0 = hashlib.sha256(), 0, time.perf_counter()
            try:
                with self._http.stream("GET", url, timeout=timeout) as r:
                    if r.status_code in (429, 500, 502, 503, 504):
                        raise httpx.HTTPStatusError(f"HTTP {r.status_code}", request=r.request, response=r)
                    r.raise_for_status()
                    with open(dest, "wb") as f:
                        for chunk in r.iter_bytes(1 << 20):
                            f.write(chunk); h.update(chunk); size += len(chunk)
                self.records.append(CallRecord("GET", url, None, 200, attempt, int((time.perf_counter() - t0) * 1000), ["<file>"], None,
                                               dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")))
                return {"bytes": size, "sha256": h.hexdigest(), "attempts": attempt}
            except (httpx.HTTPError, OSError) as e:
                last = f"{type(e).__name__}: {str(e)[:120]}"
                if dest.exists():
                    dest.unlink()
                if attempt > self.max_retries:
                    break
                self._sleep(min(delay, 60.0)); delay *= 2
        self.records.append(CallRecord("GET", url, None, None, self.max_retries + 1, 0, [], last,
                                       dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")))
        raise ApiError(0, f"file download failed after {self.max_retries + 1} attempts ({last})", url)

    def spending_by_award_page(self, filters: dict, fields: list[str], page: int = 1, limit: int = 100,
                               sort: str = "Award Amount", order: str = "desc", last_record_unique_id=None,
                               last_record_sort_value=None) -> dict:
        body: dict = {"filters": filters, "fields": fields, "page": page, "limit": limit, "sort": sort,
                      "order": order, "spending_level": "awards"}
        if last_record_unique_id is not None:
            body["last_record_unique_id"] = last_record_unique_id
            body["last_record_sort_value"] = last_record_sort_value
        return self._call("POST", Endpoints.spending_by_award, body)

    def iter_awards(self, filters: dict, fields: list[str], limit: int = 100, max_pages: int = 10_000):
        """Yield awards across pages using page_metadata.hasNext (and keyset fields when the API returns them)."""
        page, lr_id, lr_sort = 1, None, None
        while page <= max_pages:
            data = self.spending_by_award_page(filters, fields, page, limit,
                                               last_record_unique_id=lr_id, last_record_sort_value=lr_sort)
            for row in data.get("results", []):
                yield row
            meta = data.get("page_metadata", {})
            if not meta.get("hasNext"):
                return
            lr_id, lr_sort = meta.get("last_record_unique_id"), meta.get("last_record_sort_value")
            page += 1

    def spending_by_award_count(self, filters: dict) -> dict:
        return self._call("POST", Endpoints.spending_by_award_count, {"filters": filters})

    def award(self, generated_unique_award_id: str) -> dict:
        return self._call("GET", Endpoints.award.format(id=generated_unique_award_id))

    def award_transactions(self, award_id: str, limit: int = 100) -> list[dict]:
        out, page = [], 1
        while True:
            data = self._call("POST", Endpoints.transactions, {"award_id": award_id, "page": page, "limit": limit,
                                                                "sort": "action_date", "order": "asc"})
            out.extend(data.get("results", []))
            if not data.get("page_metadata", {}).get("hasNext"):
                return out
            page += 1

    # ------------------------------------------------------------------ provenance
    def records_json(self) -> list[dict]:
        return [r.__dict__ for r in self.records]

    def close(self) -> None:
        self._http.close()


def stable_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]
