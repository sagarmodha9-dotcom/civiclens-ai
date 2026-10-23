"""SYNTHETIC raw tree in the exact layout the worker produces (manifest + prime CSV per agency x FY cell).
Columns follow the USAspending transaction download names in pipeline.REQUIRED_COLUMNS. Values are invented to
hit edge cases; nothing here is a real federal figure."""
from __future__ import annotations

import csv
import json
import random
from pathlib import Path

import pytest

from civiclens_lakehouse.pipeline import REQUIRED_COLUMNS

AG = ("036", "Department of Veterans Affairs")


def row(key, award, piid, date, obl, agency=AG, uei="UEI000001", name="ACME IT LLC", psc="D302", atype="C", mod="0",
        last_mod=None, parent="GS35F001"):
    r = {c: "" for c in REQUIRED_COLUMNS}
    r.update({"contract_transaction_unique_key": key, "contract_award_unique_key": award, "award_id_piid": piid,
              "parent_award_id_piid": parent, "modification_number": mod, "action_date": date,
              "federal_action_obligation": str(obl), "base_and_exercised_options_value": str(obl),
              "base_and_all_options_value": str(obl * 2), "awarding_agency_code": agency[0], "awarding_agency_name": agency[1],
              "awarding_sub_agency_code": "3600", "awarding_sub_agency_name": "VA Office", "funding_agency_code": agency[0],
              "funding_agency_name": agency[1], "recipient_uei": uei, "recipient_name": name, "recipient_parent_uei": uei,
              "recipient_parent_name": name, "product_or_service_code": psc, "product_or_service_code_description": "IT",
              "naics_code": "541512", "naics_description": "Computer Systems Design", "award_type_code": atype,
              "award_type": "DELIVERY ORDER", "action_type_code": "C", "action_type": "FUNDING ONLY ACTION",
              "period_of_performance_start_date": date, "period_of_performance_current_end_date": "2027-09-30",
              "last_modified_date": last_mod or date, "usaspending_permalink": f"https://www.usaspending.gov/award/{award}/"})
    return r


def write_cell(root: Path, agency: tuple, fy: int, rows: list[dict], run_id="20261023T000000Z"):
    d = root / f"agency={agency[0]}" / f"fy={fy}"
    d.mkdir(parents=True, exist_ok=True)
    name = "Contracts_PrimeTransactions_1.csv"
    with open(d / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS); w.writeheader(); w.writerows(rows)
    (d / "manifest.json").write_text(json.dumps({"run_id": run_id, "status": "complete", "agency_code": agency[0],
        "agency_name": agency[1], "fiscal_year": fy, "api_count": len(rows), "rows_total": len(rows),
        "files": [{"name": name, "kind": "prime_transactions", "rows": len(rows)}]}))


@pytest.fixture
def raw_tree(tmp_path: Path) -> Path:
    rnd = random.Random(7)
    root = tmp_path / "raw"
    fy25 = [
        # FY2025 boundary rows: Oct 1 2024 is FY2025, Sep 30 2025 is FY2025
        row("K-A1", "AWD-A", "PIID-A", "2024-10-01", 100000.00),
        row("K-A2", "AWD-A", "PIID-A", "2025-09-30", 50000.00, mod="P00001"),
        row("K-A3", "AWD-A", "PIID-A", "2025-03-01", -20000.00, mod="P00002"),      # de-obligation stays negative
        row("K-B1", "AWD-B", "PIID-B", "2025-01-15", 75000.00, uei="UEI000002", name="BETA SYSTEMS"),
        row("K-OUT", "AWD-OUT", "PIID-OUT", "2025-01-15", 999999.00, psc="R499"),  # out of scope PSC -> reject
        row("K-GRANT", "AWD-G", "PIID-G", "2025-01-15", 5000.00, atype="02"),      # not a contract type -> reject
        row("", "AWD-NOKEY", "PIID-N", "2025-01-15", 1.00),                        # missing key -> reject
        row("K-BADDATE", "AWD-BD", "PIID-BD", "not-a-date", 1.00),                 # unparseable date -> reject
    ]
    # a peer group of 40 ordinary awards (log-normal-ish, heavy right tail) + one planted outlier, PSC class D3
    peers = [row(f"K-P{i}", f"AWD-P{i}", f"PIID-P{i}", "2025-05-01", round(10 ** rnd.gauss(5.0, 0.3), 2),
                 uei=f"UEIP{i:05d}", name=f"VENDOR {i}", psc="D307") for i in range(40)]
    peers.append(row("K-OUTLIER", "AWD-OUTLIER", "PIID-OUTLIER", "2025-05-01", 250_000_000.00, uei="UEI999999", name="GIANT CORP", psc="D307"))
    fy25 += peers
    fy25.append(row("K-C0", "AWD-C", "PIID-C", "2025-02-01", 600000.00, uei="UEI000003", name="GAMMA INC", psc="D399"))
    write_cell(root, AG, 2025, fy25)
    fy24 = [row("K-B0", "AWD-B", "PIID-B", "2024-01-15", 10000.00, uei="UEI000002", name="BETA SYSTEMS"),          # BETA grew 7.5x -> growth flagged? delta 65k < 2M -> not flagged
            row("K-A0", "AWD-A", "PIID-A", "2023-10-01", 10.00)]
    write_cell(root, AG, 2024, fy24)
    # concentration cell: FY2026, PSC class 70, one vendor with 90% of $10M
    fy26 = [row("K-M1", "AWD-M1", "PIID-M1", "2025-11-01", 9_000_000.00, uei="UEI000003", name="GAMMA INC", psc="7030"),
            row("K-M2", "AWD-M2", "PIID-M2", "2025-11-01", 500_000.00, uei="UEI000004", name="DELTA", psc="7030"),
            row("K-M3", "AWD-M3", "PIID-M3", "2025-11-01", 500_000.00, uei="UEI000005", name="EPSILON", psc="7030"),
            row("K-C1", "AWD-C", "PIID-C", "2025-12-01", 2_500_000.00, uei="UEI000003", name="GAMMA INC")]   # GAMMA at VA: 600k -> 2.5M+9M
    write_cell(root, AG, 2026, fy26)
    return root
