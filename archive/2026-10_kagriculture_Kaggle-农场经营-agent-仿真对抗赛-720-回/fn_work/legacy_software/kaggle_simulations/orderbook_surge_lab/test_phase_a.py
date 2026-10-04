# -*- coding: utf-8 -*-
"""test_phase_a —— decompose / mark / composition 三组（构造小夹具）。"""
import json

import pytest

from orderbook_surge_lab import phase_a as A

PX = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250}


def _obs(money, shed, prices):
    return {"farms": json.dumps([{"money": money[0]}, {"money": money[1]}]),
            "market": {"prices": dict(prices)},
            "private": json.dumps({"shed": dict(shed), "seeds": {},
                                   "inventories": [{}]})}


def _mk_replay(events, days=3, stock=20):
    """构造 N 日小回放：events={(t, seat): event}（JSON 串字段路径全覆盖）。

    event：('sell', item, qty, px) 库存减/资金加；('seed', item, qty) 资金减。
    steps[t] 携带 t 步转移后观测 + 驱动 t→t+1 的 action（twin 框架约定）。
    """
    n = days * 24
    steps = []
    money = {0: 3000.0, 1: 3000.0}
    shed = {0: {"WHEAT": stock}, 1: {"WHEAT": stock}}
    for t in range(n):
        row = []
        for seat in (0, 1):
            ev = events.get((t, seat))
            act = {"farmer": ["PASS"], "hands": [], "market": []}
            if ev:
                if ev[0] == "sell":
                    _, item, qty, px = ev
                    act["market"] = [["SELL", item, qty]]
                    shed[seat] = dict(shed[seat])
                    shed[seat][item] = shed[seat].get(item, 0) - qty
                    money[seat] = money[seat] + qty * px
                elif ev[0] == "seed":
                    _, item, qty = ev
                    act["market"] = [["BUY_SEED", item, qty]]
                    money[seat] = money[seat] - qty * A.SEED_VALUE[item]
            row.append({"action": act,
                        "observation": _obs([money[0], money[1]],
                                            shed[seat], PX),
                        "status": "ACTIVE"})
        steps.append(row)
    return {"info": {"EpisodeId": 42, "TeamNames": ["renyxin", "oppA"]},
            "rewards": [0.0, 0.0], "steps": steps}


# ---- decompose 组 -----------------------------------------------------------
class TestDailyNetflowDecompose:
    def test_basic_nets_volume_spend(self):
        # day1：我席 t=25 卖 WHEAT×10@25、t=26 买种 CARROT×3；对席 t=25 卖
        # WHEAT×20@25。day0/day2 静默（3 日夹具）。
        ev = {(25, 0): ("sell", "WHEAT", 10, 25),
              (26, 0): ("seed", "CARROT", 3),
              (25, 1): ("sell", "WHEAT", 20, 25)}
        rep = A.daily_netflow_decompose(_mk_replay(ev))
        assert rep["our_seat"] == 0 and len(rep["days"]) == 3
        d0, d1, d2 = rep["days"]
        assert d0["my"]["net"] == 0.0 and d0["opp"]["net"] == 0.0
        # 我席：Δmoney = 250-60 = 190，加回 seed 60 → 净收入 250
        assert d1["my"]["net"] == 250.0
        assert d1["my"]["vol_by_item"] == {"WHEAT": 10}
        assert d1["my"]["spend_seed"] == 60.0
        assert d1["my"]["avgpx"] == 25.0
        # sellable = 成交 10 + 日末持有 10
        assert d1["my"]["sellable"] == 20
        assert d1["opp"]["net"] == 500.0
        assert d1["opp"]["vol_total"] == 20
        assert d1["opp"]["sellable"] == 20  # 全清仓
        assert d2["my"]["net"] == 0.0

    def test_my_opp_views_match_seats(self):
        rep = A.daily_netflow_decompose(_mk_replay({}))
        d = rep["days"][1]
        assert d["my"] is d["seats"]["0"] and d["opp"] is d["seats"]["1"]

    def test_no_team_raises(self):
        bad = {"info": {"EpisodeId": 1, "TeamNames": ["a", "b"]}, "steps": []}
        with pytest.raises(ValueError):
            A.daily_netflow_decompose(bad)


# ---- mark 组 ----------------------------------------------------------------
def _dayrow(d, mynet, oppnet):
    base = {"vol_by_item": {}, "vol_total": 0, "avgpx": None, "sellable": 0,
            "inv_start": {}, "inv_end": {}, "spend_seed": 0,
            "spend_product": 0, "dropval": 0.0, "dropval_by_item": {}}
    my = dict(base, net=float(mynet))
    opp = dict(base, net=float(oppnet))
    return {"d": d, "px_mean": dict(PX), "seats": {"0": my, "1": opp},
            "my": my, "opp": opp}


def _decomp_from_nets(my, opp):
    days = [_dayrow(i, m, o) for i, (m, o) in enumerate(zip(my, opp))]
    return {"episode": 1, "names": ["renyxin", "o"], "our_seat": 0,
            "days": days}


class TestMarkSurgeDays:
    def test_surge_and_gap_boundary(self):
        my = [1000] * 30
        opp = [1000] * 30
        opp[5] = 4000            # gap 3000；4000 ≥ 1.5×中位 1000 → surge
        my[7] = 2500             # gap 恰 1500（>= 边界）→ surge
        opp[7] = 4000
        marked = A.mark_surge_days(_decomp_from_nets(my, opp))
        assert marked["surge_days"] == [5, 7]
        assert marked["opp_net_median"] == 1000.0

    def test_median_gate_blocks(self):
        my = [1000] * 30
        opp = [1000] * 30
        my[9] = -600             # gap 2000 但对席 1400 < 1.5×中位 → 不标
        opp[9] = 1400
        marked = A.mark_surge_days(_decomp_from_nets(my, opp))
        assert marked["surge_days"] == []

    def test_sensitivity_bands(self):
        my = [1000] * 30
        opp = [1000] * 30
        opp[3] = 2200            # gap 1200：th1000 标、th1500/2000 不标
        marked = A.mark_surge_days(_decomp_from_nets(my, opp))
        assert marked["surge_days"] == []
        assert marked["sensitivity"]["th1000"] == [3]
        assert marked["sensitivity"]["th1500"] == []
        assert marked["sensitivity"]["th2000"] == []

    def test_orientation_flip(self):
        my = [1000] * 30
        opp = [1000] * 30
        opp[4] = 5000
        dec = _decomp_from_nets(my, opp)
        assert A.mark_surge_days(dec, my_seat=0)["surge_days"] == [4]
        # 定向翻转：seat1 视角"对手"=seat0 无尖峰日 → 空
        assert A.mark_surge_days(dec, my_seat=1)["surge_days"] == []


# ---- composition 组 ---------------------------------------------------------
def _comp_row(vol_items, drop_items, inv_end=None):
    vol_items = vol_items or {}
    drop_items = drop_items or {}
    return {"net": sum(drop_items.values()), "vol_by_item": dict(vol_items),
            "vol_total": sum(vol_items.values()),
            "dropval": sum(drop_items.values()),
            "dropval_by_item": dict(drop_items),
            "avgpx": None, "sellable": sum(vol_items.values()),
            "inv_start": {}, "inv_end": dict(inv_end or {}),
            "spend_seed": 0, "spend_product": 0}


def _decomp_two_rows(my_row, opp_row, d=5, px=None):
    day = {"d": d, "px_mean": dict(px or PX),
           "seats": {"0": my_row, "1": opp_row}, "my": my_row, "opp": opp_row}
    return {"episode": 1, "names": ["renyxin", "o"], "our_seat": 0,
            "days": [day]}


class TestClassifySurgeComposition:
    def test_pure_volume_uncovered_is_structural(self):
        # 纯量差形态：同品同价，我 10 对 30 且我无余量 → 结构性 100%
        my = _comp_row({"WHEAT": 10}, {"WHEAT": 250.0})
        opp = _comp_row({"WHEAT": 30}, {"WHEAT": 750.0})
        c = A.classify_surge_composition(_decomp_two_rows(my, opp), 5)
        assert c["quant_gap"] == 500.0
        assert c["mix_gap"] == 0.0 and c["px_gap"] == 0.0
        assert c["structural_gap"] == 500.0
        assert c["structural_share"] >= 0.7 and c["treatable"] is False

    def test_mix_shape_with_stock_treatable(self):
        # mix 形态：对手卖高价 CARROT 我卖 WHEAT；我持有 CARROT 9 → 覆盖 90%
        my = _comp_row({"WHEAT": 10}, {"WHEAT": 250.0}, inv_end={"CARROT": 9})
        opp = _comp_row({"CARROT": 10}, {"CARROT": 350.0})
        c = A.classify_surge_composition(_decomp_two_rows(my, opp), 5)
        assert c["dropval_gap"] == 100.0
        assert abs(c["quant_gap"] + c["mix_gap"] + c["px_gap"]
                   - c["dropval_gap"]) < 1e-6
        assert c["mix_gap"] == 100.0
        assert c["structural_gap"] == 35.0     # (10-9)×35
        assert c["coverage"] == 0.9 and c["treatable"] is True

    def test_price_timing_shape(self):
        # 价差形态：同品同量，对手日内时点更优（实现价 38 vs 我 30）
        my = _comp_row({"CARROT": 10}, {"CARROT": 300.0})
        opp = _comp_row({"CARROT": 10}, {"CARROT": 380.0})
        c = A.classify_surge_composition(_decomp_two_rows(my, opp), 5)
        assert c["quant_gap"] == 0.0 and c["mix_gap"] == 0.0
        assert c["px_gap"] == 80.0
        assert c["structural_gap"] == 0.0 and c["treatable"] is True

    def test_pure_structural_no_stock(self):
        my = _comp_row({}, {})
        opp = _comp_row({"MELON": 20}, {"MELON": 5000.0})
        c = A.classify_surge_composition(_decomp_two_rows(my, opp), 5)
        assert c["structural_share"] >= 0.7
        assert c["coverage"] == 0.0 and c["treatable"] is False
        assert c["opp_short_rate"] == 1.0

    def test_price_percentile(self):
        my = _comp_row({}, {})
        opp = _comp_row({"WHEAT": 10}, {"WHEAT": 250.0})
        series = {"WHEAT": [20.0] * 9 + [25.0] * 18 + [30.0] * 3}
        c = A.classify_surge_composition(
            _decomp_two_rows(my, opp), 5, price_series=series)
        # 当日价 25：全程 30 天中 ≤25 占 27/30 = 90 分位
        assert c["price_percentile"]["WHEAT"] == 90.0

    def test_missing_day_returns_none(self):
        assert A.classify_surge_composition(
            _decomp_two_rows(_comp_row({}, {}), _comp_row({}, {})), 99) is None


# ---- attribution 编排 --------------------------------------------------------
class TestPhaseAAttribution:
    def test_small_corpus_report_and_error_tolerance(self, tmp_path):
        # 局 101：day1 对手 surge（net 2500 vs 我 125，中位 0）且我库存可覆盖
        ev = {(25, 1): ("sell", "WHEAT", 100, 25),
              (25, 0): ("sell", "WHEAT", 5, 25)}
        (tmp_path / "episode-101-replay.json").write_text(
            json.dumps(_mk_replay(ev, stock=200)), encoding="utf-8")
        (tmp_path / "episode-102-replay.json").write_text(
            "{ broken", encoding="utf-8")
        entries = [
            {"episode": 101,
             "path": str(tmp_path / "episode-101-replay.json")},
            {"episode": 102,
             "path": str(tmp_path / "episode-102-replay.json")}]
        rep = A.phase_a_attribution(entries)
        pan = rep["panorama"]
        assert pan["n_games"] == 2 and pan["n_errors"] == 1
        assert rep["errors"][0]["episode"] == 102
        g = next(g for g in rep["per_game"] if g["episode"] == 101)
        assert g["surge_days"] == [1]           # gap 2375 ≥1500，2500 ≥1.5×0
        comp = g["orientations"]["our"]["composition"]["1"]
        assert comp["treatable"] is True        # 我余量 95+成交5 ≥ 对手 100
        assert comp["opp_short_rate"] == 0.5    # 100/(100+日末 100)
        assert pan["n_games_with_surge"] == 1
        assert pan["n_games_treatable"] == 1
        assert "sellable=当日成交+日末持有" in "".join(rep["method_notes"])
