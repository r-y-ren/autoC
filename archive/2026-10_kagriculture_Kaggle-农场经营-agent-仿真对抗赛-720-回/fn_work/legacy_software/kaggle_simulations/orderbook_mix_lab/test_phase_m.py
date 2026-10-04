# -*- coding: utf-8 -*-
"""R15 单测：phase_m（percentile 三态/置换对有对无对/编排面 hermetic 夹具）。"""
import pytest

from orderbook_mix_lab import _base as B
from orderbook_mix_lab import phase_m as PM

BASE = dict(PM.BASE_PRICE_FALLBACK)


def _tables(price_rows, vol=None):
    """构造 daily_tables 夹具：price_rows=[{(item): [逐日价]}]；vol={(item): 量}。"""
    tables = []
    for gi, row in enumerate(price_rows):
        days = []
        n_days = max(len(v) for v in row.values())
        for d in range(n_days):
            seats = {}
            for seat in (0, 1):
                seats[str(seat)] = {"vol_by_item": dict(vol or {}),
                                    "inv_end": {}}
            days.append({"d": d,
                         "px_mean": {k: float(v[d]) for k, v in row.items()
                                     if d < len(v)},
                         "seats": seats})
        tables.append({"episode": 1000 + gi, "our_seat": 0, "days": days})
    return tables


# ---------------------------------------------------------------------------
# percentile 组
# ---------------------------------------------------------------------------
def test_percentile_three_states():
    # 崩价品 MELON 持续 0.4x；稀缺品 WHEAT 持续 1.8x；中性 CARROT 1.0x
    n = 12
    rows = [{"MELON": [BASE["MELON"] * 0.4] * n,
             "WHEAT": [BASE["WHEAT"] * 1.8] * n,
             "CARROT": [BASE["CARROT"] * 1.0] * n}]
    out = PM.item_price_percentile(_tables(rows), BASE)
    assert out["MELON"]["structural_low_price"] is True
    assert out["MELON"]["structural_high_price"] is False
    assert out["WHEAT"]["structural_high_price"] is True
    assert out["WHEAT"]["structural_low_price"] is False
    assert out["CARROT"]["structural_low_price"] is False
    assert out["CARROT"]["structural_high_price"] is False
    assert out["MELON"]["markup_median"] < 0.5
    assert out["WHEAT"]["markup_median"] > 1.5


def test_percentile_window_ignores_early_days():
    # 前 8 天高价、其后低价 → 窗口(≥8)面判低分位
    rows = [{"MELON": [BASE["MELON"] * 2.0] * 8 + [BASE["MELON"] * 0.4] * 10,
             "WHEAT": [BASE["WHEAT"] * 1.0] * 18,
             "CARROT": [BASE["CARROT"] * 1.0] * 18}]
    out = PM.item_price_percentile(_tables(rows), BASE)
    assert out["MELON"]["structural_low_price"] is True


def test_percentile_empty():
    assert PM.item_price_percentile([]) == {}


# ---------------------------------------------------------------------------
# swap 组
# ---------------------------------------------------------------------------
def _stats(pcts, supplies, caps):
    pct = {i: {"markup_pct_mean": v,
               "structural_low_price": v <= PM.LOW_PCT,
               "structural_high_price": v >= PM.HIGH_PCT}
           for i, v in pcts.items()}
    capacity = {i: {"mean_daily_sellable": c,
                    "median_by_day": {str(d): 1 for d in range(10)}}
                for i, c in caps.items()}
    return {"percentile": pct, "supply_share": supplies, "capacity": capacity}


def test_rank_swap_pairs_orders_by_score():
    stats = _stats({"MELON": 9.0, "STRAWBERRY": 20.0, "WHEAT": 90.0,
                    "CARROT": 70.0},
                   {"MELON": 0.41, "STRAWBERRY": 0.10, "WHEAT": 0.29,
                    "CARROT": 0.19},
                   {"MELON": 40.0, "STRAWBERRY": 5.0, "WHEAT": 1.0,
                    "CARROT": 1.0})
    ranked = PM.rank_swap_pairs(stats)
    assert ranked["crash_items"] == ["MELON"]
    assert set(ranked["scarce_items"]) == {"WHEAT", "CARROT"}
    pairs = ranked["pairs"]
    assert pairs and pairs[0]["from"] == "MELON" and pairs[0]["to"] == "WHEAT"
    assert pairs[0]["score"] >= pairs[1]["score"]
    # 产能窗：from 活跃日 ∩ to 停时窗（WHEAT fyd=2 → deadline day27）
    assert all(d <= 27 for d in pairs[0]["window_days"])


def test_rank_swap_pairs_empty():
    stats = _stats({"WHEAT": 50.0}, {"WHEAT": 0.3}, {"WHEAT": 10.0})
    ranked = PM.rank_swap_pairs(stats)
    assert ranked["pairs"] == [] and ranked["crash_items"] == []


# ---------------------------------------------------------------------------
# 编排面（hermetic：monkeypatch 回放发现与 decompose）
# ---------------------------------------------------------------------------
def test_phase_m_market_map_hermetic(monkeypatch):
    calls = {"n": 0}

    def fake_decompose(replay):
        calls["n"] += 1
        return _tables([{"MELON": [10.0] * 12, "WHEAT": [100.0] * 12,
                         "CARROT": [50.0] * 12}],
                       vol={"MELON": 10})[0]

    monkeypatch.setattr(PM._surge_corpus, "discover_replays",
                        lambda rd: [(1, "x.json"), (2, "y.json")])
    monkeypatch.setattr(PM._surge_corpus, "load_replay", lambda p: {})
    monkeypatch.setattr(PM._surge_a, "daily_netflow_decompose", fake_decompose)
    mm = PM.phase_m_market_map("whatever")
    assert mm["n_games"] == 2 and mm["n_ok"] == 2 and calls["n"] == 2
    assert set(mm["items"]) >= {"MELON", "WHEAT"}
    assert "swap_pairs_ranked" in mm and "capacity_windows" in mm
    assert mm["crash_items"] == ["MELON"] and mm["scarce_items"] == ["WHEAT"]
    assert mm["swap_pairs_ranked"][0]["from"] == "MELON"
    assert mm["params"]["low_pct"] == PM.LOW_PCT


def test_phase_m_single_game_failure_recorded(monkeypatch):
    def fake_decompose(replay):
        if replay == "bad":
            raise ValueError("boom")
        return _tables([{"MELON": [10.0] * 12}])[0]

    monkeypatch.setattr(PM._surge_corpus, "discover_replays",
                        lambda rd: [(1, "good"), (2, "bad")])
    monkeypatch.setattr(PM._surge_corpus, "load_replay", lambda p: p)
    monkeypatch.setattr(PM._surge_a, "daily_netflow_decompose", fake_decompose)
    mm = PM.phase_m_market_map("whatever")
    assert mm["n_ok"] == 1 and len(mm["errors"]) == 1
    assert mm["errors"][0]["episode"] == 2
