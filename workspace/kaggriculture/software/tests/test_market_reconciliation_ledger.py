"""Focused tests for official-engine market reconciliation."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

SOFTWARE = Path(__file__).resolve().parents[1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RECON = _load("market_reconciliation", SOFTWARE / "scripts" /
              "sell_plan_reconciliation.py")
LEDGER = _load("market_ledger", SOFTWARE / "scripts" / "market_ledger.py")
OFFICIAL = pytest.importorskip(
    "kaggle_environments.envs.kaggriculture.kaggriculture")


def _seat(farms, private, action):
    return SimpleNamespace(
        observation=SimpleNamespace(
            farms=farms, private=private, market=None, day=4, hour=6),
        action=action,
    )


def test_official_process_market_logs_each_commit_and_failed_remainder():
    farm0 = OFFICIAL._new_farm(10, 3000)
    farm1 = OFFICIAL._new_farm(10, 3000)
    private0 = OFFICIAL._new_private()
    private1 = OFFICIAL._new_private()
    private0["shed"]["WHEAT"] = 2
    market = OFFICIAL._new_market()
    farms = [farm0, farm1]
    state = [
        _seat(farms, private0, {"market": [["SELL", "WHEAT", 3]]}),
        _seat(farms, private1, {}),
    ]
    state[0].observation.market = market
    state[1].observation.market = market

    ledger = LEDGER.OfficialMarketLedger(seed=17)
    with ledger.installed():
        OFFICIAL._process_market(state, SimpleNamespace(configuration={}))

    assert len(ledger.rows) == 3
    assert [row["success"] for row in ledger.rows] == [True, True, False]
    assert all(row["seed"] == 17 for row in ledger.rows)
    assert all(row["day"] == 4 and row["hour"] == 6 for row in ledger.rows)
    assert all(row["player"] == 0 and row["order_column"] == 0
               for row in ledger.rows)
    assert all(row["item"] == "WHEAT" and row["op"] == "SELL"
               for row in ledger.rows)
    assert ledger.rows[0]["unit_price"] > 0
    assert private0["shed"]["WHEAT"] == 0


def test_summarize_aggregates_real_fills_by_plan_and_item():
    records = {
        "ledger": [
            {"seed": 17, "day": 4, "hour": 6, "player": 0,
             "order_column": 0, "op": "SELL", "item": "MILK",
             "unit_price": 10, "success": True},
            {"seed": 17, "day": 4, "hour": 6, "player": 0,
             "order_column": 0, "op": "SELL", "item": "MILK",
             "unit_price": 20, "success": True},
            {"seed": 17, "day": 4, "hour": 12, "player": 0,
             "order_column": 0, "op": "SELL", "item": "MILK",
             "unit_price": 40, "success": False},
            # A real but tactical/unplanned fill must remain visible and be
            # excluded from the plan's fill quantity.
            {"seed": 17, "day": 4, "hour": 12, "player": 0,
             "order_column": 2, "op": "SELL", "item": "WOOL",
             "unit_price": 30, "success": True},
        ],
        "planned_clear": [{
            "seed": 17, "player": 0, "day": 4, "item": "MILK",
            "planned_qty": 3, "planned_price": 20,
        }],
        "holds": [],
    }

    summary = RECON.summarize(records, min_coverage=0.5,
                               max_abs_deviation_pct=50)

    assert summary["official_ledger_attempts"] == 4
    assert summary["official_successful_sell_fills"] == 3
    assert summary["planned_qty"] == 3
    assert summary["fill_qty"] == 2
    assert summary["unfilled_qty"] == 1
    assert summary["fill_coverage"] == round(2 / 3, 4)
    assert summary["coverage"] == round(2 / 3, 4)
    assert summary["unplanned_successful_sell_fills"] == 1
    plan = summary["by_plan"][0]
    assert plan["fill_qty"] == 2
    assert plan["weighted_avg_fill_price"] == 15.0
    assert plan["unfilled_qty"] == 1
    assert plan["coverage"] == round(2 / 3, 4)
    assert summary["by_item"][0]["weighted_avg_fill_price"] == 15.0
    assert summary["gate"]["status"] == "PASS"


def test_summary_gate_fails_when_coverage_or_deviation_misses_threshold():
    records = {
        "ledger": [{"seed": 1, "day": 2, "hour": 6, "player": 0,
                    "order_column": 1, "op": "SELL", "item": "EGG",
                    "unit_price": 10, "success": True}],
        "planned_clear": [{"seed": 1, "player": 0, "day": 2,
                            "item": "EGG", "planned_qty": 2,
                            "planned_price": 20}],
        "holds": [],
    }
    summary = RECON.summarize(records, min_coverage=0.75,
                               max_abs_deviation_pct=20)
    assert summary["gate"]["status"] == "FAIL"
    assert summary["gate"]["thresholds"] == {
        "min_coverage": 0.75,
        "max_p90_abs_deviation_pct": 20.0,
    }
    assert summary["gate"]["measured"]["coverage"] == 0.5
    assert summary["gate"]["measured"]["p90_abs_deviation_pct"] == 50.0


def test_legacy_summary_fixture_remains_compatible():
    records = {
        "sales": [{"item": "MILK", "deviation_pct": -2.0},
                   {"item": "MILK", "deviation_pct": 4.0}],
        "planned_clear": [{"item": "MILK", "sold": True}],
        "holds": [],
    }
    summary = RECON.summarize(records)
    assert summary["sales"] == 2
    assert summary["coverage"] == 1.0
    assert summary["price_deviation_pct"]["n"] == 2
