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
floor 组 = _r37_cash_guard 真测试（合成 obs/floors 用例①-⑦）：
①d0 日终窗（step 20..23）触线（动作后现金<12）→ hit_floor 非 None+动作被顺延，
  窗定义边界钉住（step 19/24 不适用、step 20/23 适用）；
②含 BUY_ANIMAL 且执行点现金<500 → 保护性顺延（执行点口径钉住：提交前 ≥500 不触）；
③未触线零足迹（同对象返回+defer 不被调用，monkeypatch 计数）；
④floors 可配置生效（改 d0_end/buy_animal 值判定随之变）；
⑤hard_min 不可破（数值 <4 夹到 4；hard_min 更严生效）；
⑥畸形 obs/floors/action → 原动作不干预（同型正常态确会触线）；
⑦双命中取更严（默认取 buy_animal 500；d0_end 更严随 d0_end；等值取 d0_end）。
test_r37_agent 为 L3 未实现桩（红=预期，不许动）。
"""
import pytest  # noqa: F401

try:
    from orderbook_r37 import cash_guard_block
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
    import cash_guard_block


def test_r37_agent():
    raise NotImplementedError("unimplemented:fn:_r37_agent")


def test_r37_cash_guard_floor(monkeypatch):
    def F(d0=12, ba=500, hard=4):
        return {"d0_end": d0, "buy_animal": ba, "hard_min": hard}

    # ①d0 日终窗触线：50−80−10=−40 < 12 → hit_floor 非 None+MELON 被顺延。
    act = _act([["BUY_SEED", "MELON", 1], ["BUY_SEED", "WHEAT", 1]])
    out = cash_guard_block._r37_cash_guard(_obs(50), act, F())
    assert out["hit_floor"] == {"floor": 12, "kind": "d0_end"}
    assert out["adjusted_action"] is not act
    assert out["adjusted_action"]["market"] == [[], ["BUY_SEED", "WHEAT", 1]]
    # 窗定义钉住（step 20..23 含）：窗外 step 19/24 同状态不适用 d0_end。
    for step_out in (19, 24):
        out2 = cash_guard_block._r37_cash_guard(dict(_obs(50), step=step_out), act, F())
        assert out2["hit_floor"] is None and out2["adjusted_action"] is act
    for step_in in (20, 23):
        out3 = cash_guard_block._r37_cash_guard(dict(_obs(50), step=step_in), act, F())
        assert out3["hit_floor"] == {"floor": 12, "kind": "d0_end"}

    # ②BUY_ANIMAL 执行点现金<500 → 保护性顺延（整单入账）。
    act_b = _act([["BUY_ANIMAL", "COW", 1]])
    out_b = cash_guard_block._r37_cash_guard(dict(_obs(450), step=10), act_b, F())
    assert out_b["hit_floor"] == {"floor": 500, "kind": "buy_animal"}
    assert out_b["adjusted_action"]["market"] == [[]]
    # 执行点口径钉住：提交前 850 ≥ 500 不触（动作后 450<500 不作触发）。
    out_b2 = cash_guard_block._r37_cash_guard(dict(_obs(850), step=10), act_b, F())
    assert out_b2["hit_floor"] is None and out_b2["adjusted_action"] is act_b

    # ③未触线零足迹（monkeypatch 计数 defer 未被调用）；换桩后 undo 保后续用例真 defer。
    calls = []

    def _counting(observation, action, hit_floor):
        calls.append(hit_floor)
        return {"action": action, "deferred": []}

    monkeypatch.setattr(cash_guard_block, "_r37_defer_low_priority", _counting)
    act_c = _act([["BUY_SEED", "WHEAT", 1]])
    out_c = cash_guard_block._r37_cash_guard(_obs(22), act_c, F())  # 22−10=12 恰达标
    assert out_c["hit_floor"] is None
    assert out_c["adjusted_action"] is act_c
    assert calls == []
    monkeypatch.undo()

    # ④floors 可配置生效：end=20（30−10）在 d0_end=12 下放行、d0_end=30 下触线。
    out_d = cash_guard_block._r37_cash_guard(_obs(30), act_c, F(d0=12))
    assert out_d["hit_floor"] is None and out_d["adjusted_action"] is act_c
    out_d2 = cash_guard_block._r37_cash_guard(_obs(30), act_c, F(d0=30))
    assert out_d2["hit_floor"] == {"floor": 30, "kind": "d0_end"}
    assert out_d2["adjusted_action"]["market"] == [[]]
    # buy_animal 同理可配置：GOOSE 提交前 550 在 500 线下放行、600 线上触线。
    act_g = _act([["BUY_ANIMAL", "GOOSE", 1]])
    out_g = cash_guard_block._r37_cash_guard(dict(_obs(550), step=10), act_g, F())
    assert out_g["hit_floor"] is None and out_g["adjusted_action"] is act_g
    out_g2 = cash_guard_block._r37_cash_guard(dict(_obs(550), step=10), act_g, F(ba=600))
    assert out_g2["hit_floor"] == {"floor": 600, "kind": "buy_animal"}
    assert out_g2["adjusted_action"]["market"] == [[]]

    # ⑤hard_min 不可破（夹持制钉住）：d0_end=2/hard=1 夹到 4——end=3（13−10）本应
    # 在配置 2 之下放行，硬底线 4 必触（若未夹持→红）；负值同夹到 4。
    out_e = cash_guard_block._r37_cash_guard(_obs(13), act_c, F(d0=2, hard=1))
    assert out_e["hit_floor"] == {"floor": 4, "kind": "d0_end"}
    assert out_e["adjusted_action"]["market"] == [[]]
    out_e2 = cash_guard_block._r37_cash_guard(_obs(13), act_c, F(d0=-100))
    assert out_e2["hit_floor"] == {"floor": 4, "kind": "d0_end"}
    # hard_min 配高更严：d0_end=12 夹到 20——end=19（29−10）触线于 20。
    out_e3 = cash_guard_block._r37_cash_guard(_obs(29), act_c, F(d0=12, hard=20))
    assert out_e3["hit_floor"] == {"floor": 20, "kind": "d0_end"}
    assert out_e3["adjusted_action"]["market"] == [[]]

    # ⑥畸形 obs/floors/action → 原动作不干预。同型正常态确会触线（50−80<12），
    # 证 fail-safe 不是本来就没得判定。
    act_m = _act([["BUY_SEED", "MELON", 1]])
    ok = cash_guard_block._r37_cash_guard(_obs(50), act_m, F())
    assert ok["hit_floor"] == {"floor": 12, "kind": "d0_end"}
    assert ok["adjusted_action"] is not act_m

    for bad_obs in ({"player": 0, "step": 23, "farms": [{}]},           # 缺 money
                    {"player": 0, "farms": [{"money": 50}]},            # 缺 step
                    {"player": 0, "step": "23", "farms": [{"money": 50}]},   # step 非数
                    {"player": 0, "step": 23, "farms": [{"money": "50"}]},   # money 非数
                    {"player": 0, "step": 23, "farms": [{"money": 50,
                                                         "hires_today": -1}]}):  # hires 畸形
        out_m = cash_guard_block._r37_cash_guard(bad_obs, act_m, F())
        assert out_m["hit_floor"] is None and out_m["adjusted_action"] is act_m, bad_obs

    for bad_floor in (None, [], "floors", {},                       # 非 dict/缺三键
                      {"d0_end": 12, "buy_animal": 500},            # 缺 hard_min
                      {"d0_end": "12", "buy_animal": 500, "hard_min": 4},    # 非数
                      {"d0_end": 12, "buy_animal": 500, "hard_min": None},  # 非数
                      {"d0_end": True, "buy_animal": 500, "hard_min": 4},   # bool 不作数
                      {"d0_end": float("nan"), "buy_animal": 500, "hard_min": 4},
                      {"d0_end": 12, "buy_animal": float("inf"), "hard_min": 4}):
        out_m = cash_guard_block._r37_cash_guard(_obs(50), act_m, bad_floor)
        assert out_m["hit_floor"] is None and out_m["adjusted_action"] is act_m, bad_floor

    weird = ["BUY_SEED", "MELON", 1]  # action 非 dict
    out_m = cash_guard_block._r37_cash_guard(_obs(50), weird, F())
    assert out_m["hit_floor"] is None and out_m["adjusted_action"] is weird

    # ⑦双命中取更严：d0 窗内 + BUY_ANIMAL 执行点 300<500 + 动作后 −100<12 两线同触
    # → 默认取 buy_animal 500。
    act_h = _act([["BUY_ANIMAL", "COW", 1]])
    out_h = cash_guard_block._r37_cash_guard(dict(_obs(300), step=23), act_h, F())
    assert out_h["hit_floor"] == {"floor": 500, "kind": "buy_animal"}
    assert out_h["adjusted_action"]["market"] == [[]]
    # 反向更严：d0_end=600 > buy_animal 500 → kind 随更严线（end=170、GOOSE 执行点
    # 470 两线同触），顺延直至 600（MELON→GOOSE 全缓仍 550<600 尽力返回）。
    act_h2 = _act([["BUY_SEED", "MELON", 1], ["BUY_ANIMAL", "GOOSE", 1]])
    out_h2 = cash_guard_block._r37_cash_guard(dict(_obs(550), step=23), act_h2, F(d0=600))
    assert out_h2["hit_floor"] == {"floor": 600, "kind": "d0_end"}
    assert out_h2["adjusted_action"]["market"] == [[], []]
    # 等值取 d0_end。
    out_h3 = cash_guard_block._r37_cash_guard(dict(_obs(300), step=23), act_h, F(d0=500))
    assert out_h3["hit_floor"] == {"floor": 500, "kind": "d0_end"}


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
