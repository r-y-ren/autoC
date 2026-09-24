# -*- coding: utf-8 -*-
"""test_phase_b —— arm / sells / replay / zerofootprint 四组。

不跑真回放、不装载 1MB main——唯一例外：L3 真文件装载断言（只装载不重演）。
"""
import json
import os

import pytest

from orderbook_surge_lab import phase_b as B

HERE = os.path.dirname(os.path.abspath(__file__))


def _obs(day=1, step=25, shed=None, prices=None, inv=None):
    shed = shed if shed is not None else {"WHEAT": 10, "CARROT": 5}
    prices = prices if prices is not None else {"WHEAT": 25, "CARROT": 35,
                                                "MELON": 250}
    return {"day": day, "hour": step % 24, "step": step, "player": 0,
            "market": {"prices": prices},
            "private": {"shed": dict(shed), "seeds": {},
                        "inventories": [dict(inv or {})]},
            "farms": [], "town": {}}


def _act(market=None, farmer=("PASS",)):
    return {"farmer": list(farmer), "hands": [],
            "market": market if market is not None else
            [["SELL", "WHEAT", 4]]}


def _sell_qty(action):
    out = {}
    for o in action["market"]:
        if B._is_sell(o):
            out[o[1]] = out.get(o[1], 0) + o[2]
    return out


# ---- sells 组 ---------------------------------------------------------------
class TestApplySurgeDaySells:
    def test_a1_align_rate_natural_order(self):
        # 库存 10+5=15，rate 0.8 → 目标 12：基座在架 4 计入 → 补 8
        # （WHEAT 4→10 用 6、CARROT 追加 2），当日总量恰 12
        out = B.apply_surge_day_sells(_act(), _obs(), {"rate": 0.8}, "A1")
        assert _sell_qty(out) == {"WHEAT": 10, "CARROT": 2}
        assert out["farmer"] == ["PASS"] and out["hands"] == []

    def test_a1_hard_cap_never_exceeds_shed(self):
        # 携带库存（inventories）计入目标但引擎只认 shed：逐品项 ≤ shed
        obs = _obs(inv={"WHEAT": 10, "CARROT": 5})
        out = B.apply_surge_day_sells(_act(), obs, {"rate": 1.0}, "A1")
        q = _sell_qty(out)
        assert q["WHEAT"] == 10 and q["CARROT"] == 5  # 上限即 shed

    def test_a1_only_raises_never_cuts(self):
        # rate 低（目标 1.5 < 基座在架 4）→ 原样不动
        out = B.apply_surge_day_sells(_act(), _obs(), {"rate": 0.1}, "A1")
        assert _sell_qty(out) == {"WHEAT": 4}

    def test_a1_empty_market_appends(self):
        out = B.apply_surge_day_sells(_act(market=[]), _obs(),
                                      {"rate": 1.0}, "A1")
        assert _sell_qty(out) == {"WHEAT": 10, "CARROT": 5}

    def test_a1_sold_tracker_counts_executed(self):
        # 已执行 10、rate 0.8 → 目标 0.8×25=20，在架 4 → 补 6：WHEAT 4→10
        tr = {"sold_by_item": {"WHEAT": 10}}
        out = B.apply_surge_day_sells(_act(), _obs(), {"rate": 0.8}, "A1",
                                      tracker=tr)
        assert _sell_qty(out) == {"WHEAT": 10}

    def test_a2_value_order_and_slot_fill(self):
        obs = _obs(shed={"WHEAT": 10, "CARROT": 5, "MELON": 2},
                   prices={"WHEAT": 10, "CARROT": 35, "MELON": 250})
        act = _act(market=[["SELL", "CARROT", 5], ["SELL", "WHEAT", 10]])
        out = B.apply_surge_day_sells(act, obs, {}, "A2")
        sells = [o for o in out["market"] if B._is_sell(o)]
        # 价值序：CARROT 35×5=175 > WHEAT 10×10=100 → CARROT 排前
        assert sells[0][1] == "CARROT"
        appended = {o[1]: o[2] for o in sells if o[1] == "MELON"}
        assert appended == {"MELON": 2}        # 高价值未卖品项补槽

    def test_a3_combines(self):
        out = B.apply_surge_day_sells(_act(), _obs(), {"rate": 1.0}, "A3")
        assert _sell_qty(out) == {"WHEAT": 10, "CARROT": 5}
        # 基座原 action 未被改动
        assert _act()["market"] == [["SELL", "WHEAT", 4]]

    def test_non_dict_market_passthrough(self):
        act = {"farmer": ["PASS"], "hands": [], "market": "weird"}
        out = B.apply_surge_day_sells(act, _obs(), {"rate": 1.0}, "A1")
        assert out["market"] == "weird"

    def test_unknown_arm_raises(self):
        with pytest.raises(ValueError):
            B.apply_surge_day_sells(_act(), _obs(), {}, "A0")


# ---- arm 组 -----------------------------------------------------------------
class TestBuildTreatmentArm:
    def test_off_surge_passthrough_same_object(self):
        base = _act()
        l3 = lambda obs: base
        arm = B.build_treatment_arm(l3, {1: {"rate": 1.0}}, "A1")
        got = arm(_obs(day=0, step=3))
        assert got is base                     # 同对象透传

    def test_on_surge_modifies_and_records_pairs(self):
        base = _act()
        l3 = lambda obs: base
        arm = B.build_treatment_arm(l3, {1: {"rate": 0.8}}, "A1")
        got = arm(_obs(day=1, step=25))
        assert _sell_qty(got) == {"WHEAT": 10, "CARROT": 2}  # 目标 12−在架4
        assert len(arm.pairs) == 1
        day, step, b, o = arm.pairs[0]
        assert (day, step) == (1, 25) and b is base and o is got

    def test_fail_safe_returns_base_on_error(self):
        l3 = lambda obs: _act()
        arm = B.build_treatment_arm(l3, {1: {"rate": [1, 2]}}, "A1")
        got = arm(_obs(day=1, step=25))        # float(list) 抛 → 回退原 action
        assert _sell_qty(got) == {"WHEAT": 4}

    def test_step0_reset_and_day_roll(self):
        base = _act()
        l3 = lambda obs: base
        arm = B.build_treatment_arm(l3, {1: {"rate": 1.0}}, "A1")
        arm(_obs(day=1, step=25))
        arm(_obs(day=1, step=26))
        arm(_obs(day=2, step=50))              # 跨日重置（不在此日处置）
        assert arm.pairs[-1][3] is base

    def test_unknown_arm_rejected(self):
        with pytest.raises(ValueError):
            B.build_treatment_arm(lambda o: _act(), {}, "A0")


# ---- replay 组 ---------------------------------------------------------------
def _mini_replay(n_steps=4):
    """twin 真引擎微局：双席 PASS 动作流 n 步（episodeSteps 截短）。"""
    twin = B._twin()
    module = twin.load_engine().module
    board = 10
    # NW 象限解锁（gate_common.synthetic_season_head 同构）
    tiles = [[None if (y < board // 2) and (x < board // 2) else "LOCKED"
              for x in range(board)] for y in range(board)]

    def farm():
        return {"money": 3000.0, "tiles": json.loads(json.dumps(tiles)),
                "farmer": [board // 2 - 1, board // 2 - 1], "hands": [],
                "unlocked_quadrants": ["NW"], "hires_today": 0}

    def private():
        return {"shed": dict.fromkeys(list(module.PRODUCTS)
                                      + list(module.ANIMALS), 0),
                "seeds": dict.fromkeys(module.CROPS, 0),
                "inventories": [{}]}

    market = {"inventory": {i: module.MARKET_PARAMS[i]["I0"]
                            for i in module.PRODUCTS},
              "prices": {i: module.MARKET_PARAMS[i]["base"]
                         for i in module.PRODUCTS}}
    head = []
    for player in (0, 1):
        obs = {"farms": [farm() for _ in range(2)],
               "market": json.loads(json.dumps(market)),
               "town": {"unlocked_shops": []},
               "day": 0, "hour": 0, "step": 0 if player == 0 else None,
               "player": player, "private": private(),
               "remainingOverageTime": 60}
        head.append({"action": {"farmer": ["PASS"], "hands": [],
                                "market": []},
                     "status": "ACTIVE", "reward": 0, "observation": obs})
    steps = [head]
    for _ in range(n_steps):
        steps.append([{"action": {"farmer": ["PASS"], "hands": [],
                                  "market": []}}
                      for _ in (0, 1)])
    cfg = {"episodeSteps": n_steps + 1, "actTimeout": 1, "boardSize": board,
           "startingMoney": 3000, "maxMarketOrdersPerTurn": 10,
           "turnsPerDay": 24, "shedCapacity": 100, "weedSpawnChance": 0.005,
           "townShopUnlockInterval": 3, "townShopSellInterval": 4,
           "townCenterSellInterval": 24, "seed": None,
           "farmHandCostMult": 1, "marketParams": {}}
    return {"steps": steps, "configuration": cfg, "info": {"seed": 7},
            "rewards": [3000.0, 3000.0]}


class TestReplayDualSeat:
    def test_pass_game_margin_zero_both_seats(self):
        replay = _mini_replay()
        agent = lambda obs: {"farmer": ["PASS"], "hands": [], "market": []}
        for seat in (0, 1):
            res = B.replay_dual_seat(replay, agent, seat)
            assert res["status"] == "DONE"
            assert res["margin"] == 0.0
            assert res["steps_n"] == len(replay["steps"]) - 1
            assert len(res["stream"]) == res["steps_n"]

    def test_engine_state_reflects_our_sells(self):
        # 我席带 WHEAT 库存直接卖：engine 真结算（money 上升 → margin>0）
        replay = _mini_replay()

        def agent(obs):
            shed_w = obs["private"]["shed"].get("WHEAT", 0)
            if shed_w <= 0:
                return {"farmer": ["PASS"], "hands": [], "market": []}
            return {"farmer": ["PASS"], "hands": [],
                    "market": [["SELL", "WHEAT", shed_w]]}

        # 注入库存：改 head 私有态
        for seat in (0, 1):
            priv = replay["steps"][0][seat]["observation"]["private"]
            priv["shed"]["WHEAT"] = 30
        res = B.replay_dual_seat(replay, agent, 0)
        assert res["margin"] > 0               # 我席卖 WHEAT 得钱

    def test_l3_real_file_load_only(self):
        main = os.path.normpath(os.path.join(
            HERE, "..", "orderbook_l3_derivative", "main.py"))
        if not os.path.isfile(main):
            pytest.skip("L3 main 不在本机")
        fn = B.load_l3_callable(main)
        assert callable(fn)
        assert getattr(fn, "__name__", "") == "_cxs_agent"  # 官方末 callable


# ---- zerofootprint 组 --------------------------------------------------------
class TestCompareActionStream:
    def test_identical_streams(self):
        s = [{"farmer": ["PASS"], "hands": [], "market": []}] * 5
        r = B.compare_action_stream(s, list(s), [0])
        assert r["identical_off_surge"] and r["binding_ok"]
        assert r["first_divergence"] is None

    def test_no_surge_days_requires_full_identity(self):
        s = [{"farmer": ["PASS"]}] * 5
        t = list(s)
        t[3] = {"farmer": ["MOVE", 0, 0]}
        r = B.compare_action_stream(s, t, [])
        assert not r["binding_ok"] and not r["identical_off_surge"]
        assert r["first_divergence"] == 3

    def test_diff_before_first_surge_day_binds(self):
        s = [{"farmer": ["PASS"]}] * 50
        t = list(s)
        t[10] = {"farmer": ["MOVE", 1, 1]}     # day0，首 surge 日=1 之前
        r = B.compare_action_stream(s, t, [1])
        assert not r["binding_ok"]

    def test_surge_day_sell_only_diff_ok_aftermath_annotated(self):
        base = {"farmer": ["PASS"], "hands": [], "market": []}
        s = [dict(base) for _ in range(72)]
        t = [dict(base) for _ in range(72)]
        t[25] = {"farmer": ["PASS"], "hands": [],
                 "market": [["SELL", "WHEAT", 9]]}     # day1=surge
        t[30] = {"farmer": ["PASS"], "hands": [],
                 "market": [["SELL", "CARROT", 1]]}    # day1 内 aftermath 同属 surge
        r = B.compare_action_stream(s, t, [1])
        assert r["binding_ok"] and r["first_divergence"] == 25
        assert r["n_surge_diffs"] == 2
        t[50] = {"farmer": ["MOVE", 0, 0]}             # day2 非 surge 因果余波
        r = B.compare_action_stream(s, t, [1])
        assert r["binding_ok"]
        assert r["n_causal_aftermath"] == 1
        assert not r["identical_off_surge"]

    def test_surge_day_alien_diff_flagged(self):
        s = [{"farmer": ["PASS"], "hands": [], "market": []}] * 30
        t = [dict(x) for x in s]
        t[25] = {"farmer": ["MOVE", 0, 0], "hands": [], "market": []}
        r = B.compare_action_stream(s, t, [1])
        assert r["first_alien_diff"] is not None
        assert r["first_alien_diff"]["step"] == 25


class TestWrapperZeroFootprint:
    def test_ok_and_violations(self):
        base = {"farmer": ["PASS"], "hands": [], "market": []}
        mod_sell = {"farmer": ["PASS"], "hands": [],
                    "market": [["SELL", "WHEAT", 9]]}
        mod_farmer = {"farmer": ["MOVE", 0, 0], "hands": [], "market": []}
        pairs = [(0, 3, base, base),           # 非 surge 透传
                 (1, 25, base, mod_sell),      # surge 卖单改造 ✓
                 (1, 26, base, mod_farmer),    # surge 非 卖单差异 ✗
                 (2, 50, base, mod_sell)]      # 非 surge 改造 ✗
        r = B.wrapper_zero_footprint(pairs, [1])
        assert not r["ok"]
        kinds = {v["kind"] for v in r["violations"]}
        assert kinds == {"surge_alien_diff", "off_surge_modification"}
        assert r["n_modified_steps"] == 3

    def test_empty_pairs_ok(self):
        assert B.wrapper_zero_footprint(None, [1])["ok"]
