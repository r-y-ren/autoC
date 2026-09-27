# -*- coding: utf-8 -*-
"""R23 测试面：runtime_r40（续段选择/竞速/补洞三件）。

route 组（B29）：指纹累计 / step144 命中选路 / 无族回退 / step0 复位 /
异常回退。race 组（B30b）：SELL 前移生效 / V57 资金序反例 / 异常原动作。
hygiene 组（B30b）：零执行单清坑+补洞 / 拿不准不清 / 异常原动作+step0 复位。
"""
import json

import pytest  # noqa: F401

try:
    from orderbook_r40.runtime_r40 import (
        _route40_select, apply_race_slots, apply_slot_hygiene)
except ImportError:  # 兜底：直接以 orderbook_r40/ 为 sys.path 根跑测
    from runtime_r40 import _route40_select, apply_race_slots, \
        apply_slot_hygiene

KEY_A = "2|1|WHEAT:5|BAKERY+FARMERS_MARKET"     # 累计口径命中键
KEY_ZERO = "0|0|WHEAT:5|BAKERY+FARMERS_MARKET"  # 零累计对照键（亦在库中）
KEY_NOWIN = "1|0|MELON:3|BAKERY+FARMERS_MARKET"
LIB = {
    "version": "routelib/1.0",
    "families": {
        KEY_A: {"n_games": 3, "win_rate": 2 / 3, "best_route": 5,
                "margin_mean": 833.3,
                "segments": {"5": {"n": 3, "win_rate": 2 / 3,
                                   "margin_mean": 700.0}}},
        KEY_ZERO: {"n_games": 1, "win_rate": 1.0, "best_route": 7,
                   "margin_mean": 1.0, "segments": {}},
        KEY_NOWIN: {"n_games": 1, "win_rate": 0.0, "best_route": None,
                    "margin_mean": -1.0, "segments": {}},
    },
    "default": {"n_games": 5, "win_rate": 0.6, "best_route": 5,
                "margin_mean": 0.0, "segments": {}},
    "defeat_worlds": {"milk_flow": {"families": [], "covered": False},
                      "wool_flow": {"families": [], "covered": False},
                      "goose_flow": {"families": [], "covered": False}},
    "build_audit": {"n_games": 5, "n_families": 3, "coverage": 2 / 3,
                    "uncovered_families": [KEY_NOWIN], "library_sha": "0" * 64},
}
FALLBACK = {"route": None, "family": None, "confidence": 0.0}


def _obs(t, hands=0, uq=1, crops=None, shops=()):
    tiles = [[{"kind": "PLANT", "crop": c} for c, n in sorted((crops or {}).items())
              for _ in range(n)]]
    return {"day": t // 24, "hour": t % 24, "player": 1,
            "farms": [{"money": 0.0, "hands": [], "unlocked_quadrants": ["NW"],
                       "tiles": [[]]},
                      {"money": 0.0, "hands": [[0, 0]] * hands,
                       "unlocked_quadrants": ["NW"] * uq, "tiles": tiles}],
            "market": {"inventory": {"WHEAT": 9989}, "prices": {}},
            "town": {"unlocked_shops": list(shops)}}


def _reset():
    _route40_select._fp_state = None
    apply_slot_hygiene._ledger = None


def _hobs(step, money=500.0, inv=None):
    """hygiene/race 组观察桩：可控 money/inventory 的最小观察。"""
    return {"step": step, "player": 1,
            "farms": [{"money": 0.0}, {"money": money}],
            "market": {"inventory": dict(inv if inv is not None
                                         else {"WHEAT": 10}), "prices": {}}}


def _feed_key_a(lib=LIB):
    """喂出 KEY_A="2|1|WHEAT:5|BAKERY+FARMERS_MARKET" 的观察流（0..144）。"""
    _reset()
    for t in range(0, 144):
        _route40_select(_obs(t, hands=2 if t >= 1 else 0,
                             uq=2 if t >= 50 else 1), lib)
    return _route40_select(_obs(144, hands=2, uq=2, crops={"WHEAT": 5},
                                shops=["BAKERY", "FARMERS_MARKET"]), lib)


def test_route40_select_fingerprint_accumulates():
    """指纹累计：hires/land 跨步正增量入族键；冷启动对照落零累计键。"""
    res = _feed_key_a()
    assert res == {"route": 5, "family": KEY_A,
                   "confidence": pytest.approx(2 / 3)}
    _reset()
    cold = _route40_select(_obs(144, hands=2, uq=2, crops={"WHEAT": 5},
                                shops=["BAKERY", "FARMERS_MARKET"]), LIB)
    assert cold == {"route": 7, "family": KEY_ZERO,
                    "confidence": pytest.approx(1.0)}


def test_route40_select_step144_hit():
    """step144 命中选路：{route, family, confidence=族 win_rate} 且跨步锁定。"""
    res = _feed_key_a()
    assert res == {"route": 5, "family": KEY_A,
                   "confidence": pytest.approx(2 / 3)}
    assert _route40_select(_obs(145, hands=2, uq=2, crops={"WHEAT": 5},
                                shops=["BAKERY", "FARMERS_MARKET"]), LIB) == {
        "route": 5, "family": KEY_A, "confidence": pytest.approx(2 / 3)}
    assert _route40_select(_obs(300, hands=2, uq=2), LIB) == {
        "route": 5, "family": KEY_A, "confidence": pytest.approx(2 / 3)}
    assert _feed_key_a({"library": LIB})["route"] == 5     # 包装形态
    assert _feed_key_a(json.dumps(LIB))["route"] == 5      # 内嵌串形态


def test_route40_select_no_family_fallback():
    """无族回退：route=None 即回退 _router 店对逻辑；无胜局族同信号。"""
    _reset()
    for t in range(0, 144):
        _route40_select(_obs(t), LIB)      # hires=0/land=0
    res = _route40_select(_obs(144, crops={"CARROT": 9},
                               shops=["BAKERY", "FARMERS_MARKET"]), LIB)
    assert res == FALLBACK
    _reset()
    for t in range(0, 144):
        _route40_select(_obs(t, hands=1 if t >= 1 else 0), LIB)
    res = _route40_select(_obs(144, hands=1, crops={"MELON": 3},
                               shops=["BAKERY", "FARMERS_MARKET"]), LIB)
    assert res == {"route": None, "family": KEY_NOWIN, "confidence": 0.0}


def test_route40_select_step0_reset():
    """step0 复位：新局指纹重累计，旧局锁定不带入。"""
    assert _feed_key_a()["family"] == KEY_A
    _route40_select(_obs(0), LIB)          # 新局复位
    for t in range(1, 144):
        _route40_select(_obs(t, hands=3, uq=1), LIB)   # hires=3 → 非 KEY_A
    res = _route40_select(_obs(144, hands=3, uq=1, crops={"WHEAT": 5},
                               shops=["BAKERY", "FARMERS_MARKET"]), LIB)
    assert res == FALLBACK                 # 若未复位会返回 KEY_A 锁定
    assert _feed_key_a()["family"] == KEY_A  # 复位后重累计可再次命中


def test_route40_select_exception_fallback():
    """异常/库缺回退：不抛、route=None、且不污染锁定。"""
    _reset()
    assert _route40_select(None, LIB) == FALLBACK
    assert _route40_select({"player": 1}, LIB) == FALLBACK
    assert _route40_select({"farms": "bad"}, LIB) == FALLBACK
    assert _route40_select(_obs(144, crops={"WHEAT": 5},
                                shops=["BAKERY", "FARMERS_MARKET"]),
                           None) == FALLBACK
    assert _feed_key_a()["route"] == 5     # 异常后仍可正常命中


def test_apply_race_slots_sell_forward():
    """竞速前移生效：SELL 按原序挤进区段前部空槽，空槽后移保槽数；
    非 SELL 锚单原位不动；不删不增单；输入动作不被改。"""
    sell_w = ["SELL", "WHEAT", 5]
    sell_wo = ["SELL", "WOOL", 3]
    buy = ["BUY_PRODUCT", "SEED", 2]
    action = {"farmer": ["PASS"], "hands": [["PLANT", 0, 0, "WHEAT"]],
              "market": [[], sell_w, [], sell_wo, buy, []]}
    res = apply_race_slots(_hobs(120), action)
    assert res["market"] == [["SELL", "WHEAT", 5], ["SELL", "WOOL", 3],
                             [], [], ["BUY_PRODUCT", "SEED", 2], []]
    assert res["farmer"] == ["PASS"] and res["hands"] == [["PLANT", 0, 0, "WHEAT"]]
    # 不删不增单：槽位多重集守恒
    assert sorted(map(tuple, res["market"])) == \
        sorted(map(tuple, action["market"]))
    assert action["market"] == [[], sell_w, [], sell_wo, buy, []]


def test_apply_race_slots_v57_funding_invariant():
    """V57 资金序反例：供资卖单可前移，但绝不跨越 BUY/HIRE——SELL 间换序
    的天真法会把 BUY 挤到供资卖单前（违例形态），钉住不发生。"""
    sell_fund = ["SELL", "WHEAT", 5]        # 供资卖单（flush 日卖→买）
    buy = ["BUY_PRODUCT", "WHEAT", 3]
    sell_wo = ["SELL", "WOOL", 3]
    action = {"farmer": ["PASS"], "hands": [],
              "market": [[], sell_fund, buy, sell_wo, []]}
    res = apply_race_slots(_hobs(121), action)
    m = res["market"]
    assert m == [["SELL", "WHEAT", 5], [], ["BUY_PRODUCT", "WHEAT", 3],
                 ["SELL", "WOOL", 3], []]
    assert m.index(sell_fund) < m.index(buy)   # 供资卖单仍在 BUY 前（V57）
    assert m.index(sell_wo) > m.index(buy)     # WOOL 未跨越 BUY/HIRE
    # 反例形态留档：SELL 间换序天真法把 BUY 挪到供资卖单前 = V57 违例
    naive = [["SELL", "WOOL", 3], buy, sell_fund, [], []]
    assert naive.index(buy) < naive.index(sell_fund)


def test_apply_race_slots_exception_original():
    """异常/形态非法→原动作对象逐字返回；正常动作照常前移。"""
    action = {"farmer": ["PASS"], "hands": [], "market": [["SELL", "WHEAT", 5]]}
    assert apply_race_slots(_hobs(122), None) is None
    bad = {"market": "bad"}
    assert apply_race_slots(_hobs(122), bad) is bad
    bad2 = {"market": [["SELL", "WHEAT", 5], "junk"]}
    assert apply_race_slots(_hobs(122), bad2) is bad2
    ok = {"farmer": ["PASS"], "hands": [], "market": [[], ["SELL", "WHEAT", 5]]}
    assert apply_race_slots(_hobs(122), ok)["market"] == \
        [["SELL", "WHEAT", 5], []]


def test_apply_slot_hygiene_clear_and_fill():
    """qty==0 真占坑单清坑+补洞（B32 机制修正后口径）：同槽同单+成交对账
    零变化+qty==0→置 [] 清坑，后位有效单链式前移填坑（空槽原地不动、保槽
    不删）；只动市场单。"""
    _reset()
    squatter = ["SELL", "WHEAT", 0]
    buy = ["BUY_PRODUCT", "SEED", 2]
    wool = ["SELL", "WOOL", 3]
    a1 = {"farmer": ["PASS"], "hands": [], "market": [squatter, [], [], []]}
    r1 = apply_slot_hygiene(_hobs(100, money=500.0, inv={"WHEAT": 10}), a1)
    assert r1["cleared"] == [] and r1["action"] is a1      # 首拍只记账
    a2 = {"farmer": ["PASS"], "hands": [],
          "market": [squatter, buy, [], wool]}
    r2 = apply_slot_hygiene(_hobs(101, money=500.0, inv={"WHEAT": 10}), a2)
    assert r2["cleared"] == [{"slot": 0, "order": ["SELL", "WHEAT", 0]}]
    assert r2["filled"] == [
        {"to": 0, "from": 1, "order": ["BUY_PRODUCT", "SEED", 2]},
        {"to": 1, "from": 3, "order": ["SELL", "WOOL", 3]}]
    assert r2["action"]["market"] == [["BUY_PRODUCT", "SEED", 2],
                                      ["SELL", "WOOL", 3], [], []]
    assert r2["action"]["farmer"] == ["PASS"]   # 只动自家市场单
    assert a2["market"] == [squatter, buy, [], wool]   # 输入不被改


def test_apply_slot_hygiene_qty_gt0_standing_never_cleared():
    """B32 机制修正钉：qty>0 站立单=排队限价单（上一拍未成交≠占坑）——
    即使其余对账全真也一概不清（清=丢队列位次，单件 h2h 实测崩 0.075）。"""
    _reset()
    standing = ["SELL", "WHEAT", 5]
    a1 = {"farmer": ["PASS"], "hands": [], "market": [standing, [], [], []]}
    apply_slot_hygiene(_hobs(400, money=500.0, inv={"WHEAT": 10}), a1)
    a2 = {"farmer": ["PASS"], "hands": [],
          "market": [standing, ["SELL", "WOOL", 3], [], []]}
    r = apply_slot_hygiene(_hobs(401, money=500.0, inv={"WHEAT": 10}), a2)
    assert r["cleared"] == [] and r["filled"] == []
    assert r["action"] is a2                        # 原样返回不补洞


def test_apply_slot_hygiene_unsure_keeps():
    """拿不准不清（保守）：对账有变化/账本缺拍/单形变动→一概不清坑。"""
    _reset()
    squatter = ["SELL", "WHEAT", 0]
    a1 = {"farmer": ["PASS"], "hands": [], "market": [squatter, []]}
    # ①无账本（首拍）不与历史对账→不清
    r = apply_slot_hygiene(_hobs(200, money=500.0), a1)
    assert r["cleared"] == [] and r["filled"] == []
    # ②money 变化（可能已成交）→不清
    _reset()
    apply_slot_hygiene(_hobs(200, money=500.0), a1)
    a2 = {"farmer": ["PASS"], "hands": [], "market": [["SELL", "WHEAT", 0], []]}
    r = apply_slot_hygiene(_hobs(201, money=520.0), a2)
    assert r["cleared"] == [] and r["filled"] == [] and r["action"] is a2
    # ③同槽单形变动（qty 0→3）→不清
    _reset()
    apply_slot_hygiene(_hobs(300, money=500.0), a1)
    a3 = {"farmer": ["PASS"], "hands": [], "market": [["SELL", "WHEAT", 3], []]}
    r = apply_slot_hygiene(_hobs(301, money=500.0), a3)
    assert r["cleared"] == [] and r["filled"] == []


def test_apply_slot_hygiene_exception_and_step0_reset():
    """异常→原动作+空账；step0/步标回退→账本复位（本拍不清、次拍起
    重新对账可清）。"""
    action = {"farmer": ["PASS"], "hands": [], "market": [["SELL", "WHEAT", 5]]}
    r = apply_slot_hygiene(None, action)
    assert r["action"] is action and r["cleared"] == [] and r["filled"] == []
    bad = {"market": "bad"}
    r = apply_slot_hygiene(_hobs(1), bad)
    assert r["action"] is bad and r["cleared"] == []
    _reset()
    squatter = ["SELL", "WHEAT", 0]
    a1 = {"farmer": ["PASS"], "hands": [], "market": [squatter, []]}
    apply_slot_hygiene(_hobs(50, money=500.0), a1)          # 建账
    a2 = {"farmer": ["PASS"], "hands": [], "market": [squatter, []]}
    r = apply_slot_hygiene(_hobs(0, money=500.0), a2)       # step0 复位
    assert r["cleared"] == [] and r["action"] is a2         # 不带旧账清坑
    a3 = {"farmer": ["PASS"], "hands": [], "market": [squatter, []]}
    r = apply_slot_hygiene(_hobs(1, money=500.0), a3)       # 复位后重新对账
    assert r["cleared"] == [{"slot": 0, "order": ["SELL", "WHEAT", 0]}]
    assert r["filled"] == [] and r["action"]["market"] == [[], []]
