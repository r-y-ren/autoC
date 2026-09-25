# -*- coding: utf-8 -*-
"""R19 测试面：cash_guard_block（入口/floor 组/defer 组）。

defer 组 = _r37_defer_low_priority 真测试（合成 obs/action 用例①-⑦）：
①缓 MELON 种子腾现金到下限（MELON 优先于价更高的 STRAWBERRY）；
②现金不足 500 时 BUY_ANIMAL 整单入顺延账+槽置 []（卖单不动；下限已满足仍入账）；
③HIRE/FEED/CARE/SELL/动物格 HARVEST/移动类一字节不动（逐类断言）+ HIRE 硬开销
  1+1+2=4 金核算（双面包夹恰=4）；
④槽位数不变（[] 空槽保位置语义，含既有空槽，防塌缩）；
⑤异常→原动作（状态缺 money / hit_floor 畸形 / action 非 dict，且同型正常态确会顺延）；
⑥多单连续缓到达标（MELON 尾序→下一 MELON→其余种子，一次不够继续缓）；
⑦无单可缓→尽力返回不抛（只剩 HIRE/卖单、market 缺失）。
test_r37_agent/test_r37_cash_guard_floor 为 L3/L4 未实现桩（红=预期，不许动）。
"""
import pytest  # noqa: F401

try:
    from orderbook_r37 import cash_guard_block
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
    import cash_guard_block


def test_r37_agent():
    raise NotImplementedError("unimplemented:fn:_r37_agent")


def test_r37_cash_guard_floor():
    raise NotImplementedError("unimplemented:fn:_r37_cash_guard")


def _obs(money, hires_today=0):
    """合成 observation：cash_guard_block 只读 player / farms[seat] 的 money、
    hires_today（引擎 farm 字段名，kaggriculture.py _new_farm）。"""
    return {"player": 0, "step": 23, "day": 0, "hour": 23,
            "farms": [{"money": money, "hires_today": hires_today}]}


def _act(market, farmer=None, hands=None):
    """合成 action：market 位置性订单表（[] 空槽有意义）。"""
    return {"farmer": farmer if farmer is not None else ["PASS"],
            "hands": hands if hands is not None else [],
            "market": market}


def test_r37_defer_low_priority():
    # ①缓 MELON 种子腾现金到下限：120−80−100=−60 < 12 → 缓 MELON（优先于价更高
    # 的 STRAWBERRY）→ 20 ≥ 12 达标；STRAWBERRY 原对象保留。
    act = _act([["BUY_SEED", "MELON", 1], ["BUY_SEED", "STRAWBERRY", 1]])
    out = cash_guard_block._r37_defer_low_priority(
        _obs(120), act, {"floor": 12, "kind": "d0_end"})
    assert out["action"]["market"][0] == []
    assert out["action"]["market"][1] is act["market"][1]
    assert out["deferred"] == [{"op": "BUY_SEED", "item": "MELON", "qty": 1,
                                "cost": 80, "slot": 0}]
    assert len(out["action"]["market"]) == 2
    # 输入 action 不被原地改动（顺延只出新表）。
    assert act["market"] == [["BUY_SEED", "MELON", 1], ["BUY_SEED", "STRAWBERRY", 1]]


def test_r37_defer_low_priority_buy_animal_below_500():
    # ②a 现金不足 500：BUY_ANIMAL 整单入顺延账+槽置 []，卖单不动；320<500 无单
    # 可缓→尽力返回不抛。
    act = _act([["BUY_ANIMAL", "SHEEP", 2], ["SELL", "WOOL", 3]])
    out = cash_guard_block._r37_defer_low_priority(
        _obs(320), act, {"floor": 500, "kind": "buy_animal"})
    assert out["action"]["market"][0] == []
    assert out["action"]["market"][1] is act["market"][1]
    assert len(out["action"]["market"]) == 2
    assert out["deferred"] == [{"op": "BUY_ANIMAL", "item": "SHEEP", "qty": 2,
                                "cost": 1000, "slot": 0}]

    # ②b 触线处置期间现金不足 500 的 BUY_ANIMAL 一律整单入账：此处下限 12 已
    # 满足（450−400=50≥12），仍顺延——保意图防引擎静默丢（丢单线 400/400/500）。
    act_b = _act([["BUY_ANIMAL", "COW", 1]])
    out_b = cash_guard_block._r37_defer_low_priority(
        _obs(450), act_b, {"floor": 12, "kind": "d0_end"})
    assert out_b["action"]["market"] == [[]]
    assert out_b["deferred"] == [{"op": "BUY_ANIMAL", "item": "COW", "qty": 1,
                                  "cost": 400, "slot": 0}]


def test_r37_defer_low_priority_keeps_protected_ops():
    # ③a 逐类不动（对象级）：动物格 HARVEST（farmer）/FEED/CARE/移动类（hands）
    # /HIRE/卖单（market 槽）一个字节不动，仅 MELON 种子槽置 []。
    act = _act([["HIRE"], ["SELL", "WOOL", 3], ["BUY_SEED", "MELON", 1]],
               farmer=["HARVEST"], hands=[["FEED"], ["CARE"], ["NORTH"]])
    out = cash_guard_block._r37_defer_low_priority(
        _obs(30), act, {"floor": 12, "kind": "d0_end"})
    got = out["action"]
    assert got["farmer"] is act["farmer"] and got["farmer"] == ["HARVEST"]
    assert got["hands"] is act["hands"]
    assert got["hands"][0] == ["FEED"] and got["hands"][1] == ["CARE"]
    assert got["hands"][2] == ["NORTH"]
    assert got["market"][0] is act["market"][0] == ["HIRE"]
    assert got["market"][1] is act["market"][1] == ["SELL", "WOOL", 3]
    assert got["market"][2] == []
    assert out["deferred"] == [{"op": "BUY_SEED", "item": "MELON", "qty": 1,
                                "cost": 80, "slot": 2}]

    # ③b HIRE 硬开销照常计价（三张=1+1+2=4 金，fib 递增）——双面包夹恰=4：
    # 26−4−10=12 恰达标 → 零顺延原动作返回（若 HIRE 计价>4 会顺延→红）；
    # 25−4−10=11 < 12 → 缓 WHEAT（若 HIRE 计价<4 会不缓→红）。
    hires = _act([["HIRE"], ["HIRE"], ["HIRE"], ["BUY_SEED", "WHEAT", 1]])
    out_a = cash_guard_block._r37_defer_low_priority(
        _obs(26), hires, {"floor": 12, "kind": "d0_end"})
    assert out_a["action"] is hires and out_a["deferred"] == []
    out_b = cash_guard_block._r37_defer_low_priority(
        _obs(25), hires, {"floor": 12, "kind": "d0_end"})
    assert out_b["action"]["market"][:3] == [["HIRE"], ["HIRE"], ["HIRE"]]
    assert out_b["action"]["market"][3] == []
    assert out_b["deferred"] == [{"op": "BUY_SEED", "item": "WHEAT", "qty": 1,
                                  "cost": 10, "slot": 3}]


def test_r37_defer_low_priority_slots_stable():
    # ④槽位数不变（防 [] 塌缩）：含既有空槽；被缓槽置 []，卖单/种子单仍原位。
    act = _act([["SELL", "WOOL", 1], ["BUY_SEED", "MELON", 2], [],
                ["BUY_SEED", "WHEAT", 1]])
    out = cash_guard_block._r37_defer_low_priority(
        _obs(200), act, {"floor": 100, "kind": "d0_end"})
    market = out["action"]["market"]
    assert len(market) == len(act["market"]) == 4
    assert market[0] is act["market"][0]
    assert market[1] == []
    assert market[2] is act["market"][2] and market[2] == []
    assert market[3] is act["market"][3]
    assert out["deferred"] == [{"op": "BUY_SEED", "item": "MELON", "qty": 2,
                                "cost": 160, "slot": 1}]


def test_r37_defer_low_priority_fail_safe():
    # ⑤异常→不干预（原动作+空顺延账）。同型正常态确会顺延（50−80<12），证
    # fail-safe 不是本来就没动作可做。
    act = _act([["BUY_SEED", "MELON", 1]])
    ok = cash_guard_block._r37_defer_low_priority(
        _obs(50), act, {"floor": 12, "kind": "d0_end"})
    assert ok["deferred"] != [] and ok["action"] is not act

    broken_obs = {"player": 0, "farms": [{}]}  # 缺 money
    out = cash_guard_block._r37_defer_low_priority(
        broken_obs, act, {"floor": 12, "kind": "d0_end"})
    assert out["action"] is act and out["deferred"] == []

    for bad_floor in ({"kind": "d0_end"},              # 缺 floor
                      {"floor": -1, "kind": "d0_end"},  # 负下限
                      {"floor": 12},                    # 缺 kind
                      {"floor": "12", "kind": "d0_end"},  # 非数
                      None):                            # 非 dict
        out = cash_guard_block._r37_defer_low_priority(_obs(50), act, bad_floor)
        assert out["action"] is act and out["deferred"] == [], bad_floor

    weird = ["BUY_SEED", "MELON", 1]  # action 非 dict
    out = cash_guard_block._r37_defer_low_priority(
        _obs(50), weird, {"floor": 12, "kind": "d0_end"})
    assert out["action"] is weird and out["deferred"] == []


def test_r37_defer_low_priority_multi_defer():
    # ⑥一次不够继续缓（含 MELON 尾序+MELON 优先于其余种子）：100−80−20−80=−80 < 90
    # → 缓 MELON@slot2（尾序）→ 0 < 90 → 缓 MELON@slot0 → 80 < 90 → 缓 CARROT@slot1
    # → 100 ≥ 90 达标。
    act = _act([["BUY_SEED", "MELON", 1], ["BUY_SEED", "CARROT", 1],
                ["BUY_SEED", "MELON", 1]])
    out = cash_guard_block._r37_defer_low_priority(
        _obs(100), act, {"floor": 90, "kind": "d0_end"})
    assert out["action"]["market"] == [[], [], []]
    assert out["deferred"] == [
        {"op": "BUY_SEED", "item": "MELON", "qty": 1, "cost": 80, "slot": 2},
        {"op": "BUY_SEED", "item": "MELON", "qty": 1, "cost": 80, "slot": 0},
        {"op": "BUY_SEED", "item": "CARROT", "qty": 1, "cost": 20, "slot": 1},
    ]


def test_r37_defer_low_priority_best_effort():
    # ⑦无单可缓→尽力返回不抛：只剩 HIRE/卖单（0−1<12 但无可缓购买单）→ 原动作。
    act = _act([["HIRE"], ["SELL", "WOOL", 1]])
    out = cash_guard_block._r37_defer_low_priority(
        _obs(0), act, {"floor": 12, "kind": "d0_end"})
    assert out["action"] is act and out["deferred"] == []

    # market 缺失同样不抛（无单可缓）。
    bare = {"farmer": ["PASS"], "hands": []}
    out = cash_guard_block._r37_defer_low_priority(
        _obs(0), bare, {"floor": 500, "kind": "buy_animal"})
    assert out["action"] is bare and out["deferred"] == []
