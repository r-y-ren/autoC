# -*- coding: utf-8 -*-
"""R19 测试面：cash_guard_block（入口/floor 组/defer 组）。

2026-09-26 跨批修订钉（用户裁决：现金守卫三处过度扣单根因修复）：
①逐单价丢单线（BUY_ANIMAL=该单实际成本 qty×单价，付得起不拦）；
②执行点现金计入同列表位序在前 SELL 单预期收入（卖价=observation 市场价，
  读不到回退不计）；③BUY_SEED 入顺延账重发范围（FIFO 回填）。

defer 组 = _r37_defer_low_priority 真测试（合成 obs/action 用例①-⑨）：
①缓 MELON 种子腾现金到下限（MELON 优先于价更高的 STRAWBERRY）；
②BUY_ANIMAL 逐单价丢单保护（修订①）：实际成本不足整单入账+槽置 []
  （卖单不动），付得起的单不拦（COW 450 反例）+ qty×单价 为线；
③HIRE/FEED/CARE/SELL/动物格 HARVEST/移动类一字节不动（逐类断言）+ HIRE 硬开销
  1+1+2=4 金核算（双面包夹恰=4）；
④槽位数不变（[] 空槽保位置语义，含既有空槽，防塌缩）；
⑤异常→原动作（状态缺 money / hit_floor 畸形[含 kind 枚举] / prices 畸形 /
  action 非 dict，且同型正常态确会顺延）；
⑥多单连续缓到达标（MELON 尾序→下一 MELON→其余种子，一次不够继续缓）；
⑦无单可缓→尽力返回不抛（只剩 HIRE/卖单、market 缺失）；
⑧卖单收入计入 end（修订②）：同列表卖单收入使下限达标→零顺延（反例=价读
  不到回退不计仍顺延），卖单本体一字节不动；
⑨kind=buy_animal 不施加 end 下限（平线连坐废止）：end 低于 floor 但无
  丢单→零顺延。
floor 组 = _r37_cash_guard 真测试（合成 obs/floors 用例①-⑧）：
①d0 日终窗（step 20..23）触线（动作后现金<12）→ hit_floor 非 None+动作被顺延，
  窗定义边界钉住（step 19/24 不适用、step 20/23 适用）；
②BUY_ANIMAL 逐单价丢单线（修订①）：执行点现金<该单实际成本才触（450 分界：
  COW 400 放行/羊 500 拦；qty×单价 为线）；提交前付得起不触（850 反例）；
③未触线零足迹（同对象返回+defer 不被调用，monkeypatch 计数）；
④floors 可配置生效（改 d0_end 判定随之变；buy_animal 经 prices 覆盖表标定）；
⑤hard_min 不可破（数值 <4 夹到 4；hard_min 更严生效）；
⑥畸形 obs/floors/action → 原动作不干预（含旧版平线数值 buy_animal、prices
  畸形；同型正常态确会触线）；
⑦双命中取 d0_end（修订①：其处置覆盖逐单丢单保护；等值/大值皆随 d0_end）；
⑧卖单收入计入（修订②）：位序在前 SELL 收入使 BUY_ANIMAL 执行点达标→放行；
  位序在后不计→仍拦；卖价读不到→回退不计=保守；卖单本体不动（反例钉住）。
入口组 = _r37_agent 真测试（合成 obs/action 用例①-⑩）：
①正常路径：guard 被调用（floors 三键常数钉住）且返回其 adjusted_action；
②guard 抛异常/返回畸形 adjusted_action → base_action 原样（fail-safe+账不动）；
③step==0 复位顺延账（预置账后 step0 调用→账清，且复位先于重试不回填）；
④重试回填：账中 BUY_ANIMAL+现金达标→回填空槽成功出账（真守卫不误伤）；
⑤无空槽→留账不回填且不挤占既有单（槽位对象逐一原样）；
⑥现金不达标→留账不回填（逐单价线：COW 350<400 留账；450 分界=COW 回填/
  SHEEP 留账）；
⑦动作集合不变量：HARVEST/卖单/HIRE/既有单一字节不动、槽位数不变
  （回填路径+守卫顺延路径两调用，顺延路径兼钉新顺延入账）；
⑧零干预路径同对象返回；
⑨BUY_SEED 入重发范围（修订③）：账中种子达标即回填（FIFO）；高价意图
  不饿死低价意图（SHEEP 留账 MELON 回填），种子回填账序=顺延序；
⑩种活时限（修订④）：截止线前回填✓（step 624=全局保守线，≤ 截止线才
  重发）；截止线后不出账重发✓；出账作废记 reason=plant_deadline✓（正常
  出清不算失败；作废记录原子提交/fail-safe/step0 复位同顺延账）；BUY_ANIMAL
  不受时限✓（棚仓无成活时限）；逐作物精细线可经 plant_deadline 参数传入
  （缺省 624）。
"""
import pytest  # noqa: F401

try:
    from orderbook_r37 import cash_guard_block
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
    import cash_guard_block


def test_r37_agent(monkeypatch):
    # ①正常路径：guard 被调用（floors 三键常数钉住）且返回其 adjusted_action。
    cash_guard_block._r37_agent._defer_ledger = []
    calls = []
    sentinel = _act([["SELL", "WOOL", 1]])

    def _stub(observation, action, floors):
        calls.append((observation, action, floors))
        return {"hit_floor": None, "adjusted_action": sentinel}

    monkeypatch.setattr(cash_guard_block, "_r37_cash_guard", _stub)
    base = _act([["BUY_SEED", "WHEAT", 1], []])
    obs = dict(_obs(500), step=10)
    out = cash_guard_block._r37_agent(obs, base)
    assert out is sentinel
    assert len(calls) == 1
    obs_g, act_g, floors = calls[0]
    assert obs_g is obs
    assert act_g is base  # 空账零回填→基座动作原对象交守卫
    assert floors == {"d0_end": 5, "buy_animal": "exact_cost", "hard_min": 4}  # 09-26 标定 12→5
    assert cash_guard_block._r37_agent._defer_ledger == []

    # ⑧零干预路径同对象返回（真守卫：step 10 窗外+动作无 BUY_ANIMAL→零足迹）。
    monkeypatch.undo()
    cash_guard_block._r37_agent._defer_ledger = []
    base8 = _act([["BUY_SEED", "WHEAT", 1], [], ["SELL", "WOOL", 2]])
    out8 = cash_guard_block._r37_agent(dict(_obs(500), step=10), base8)
    assert out8 is base8
    assert cash_guard_block._r37_agent._defer_ledger == []


def test_r37_agent_fail_safe(monkeypatch):
    # ②guard 抛异常→base_action 原样（fail-safe）+账不动（回填出账不提交，
    # 顺延不是删除）；guard 返回畸形 adjusted_action 同兜底。
    entry = {"op": "BUY_ANIMAL", "item": "GOOSE", "qty": 1, "cost": 300, "slot": 0}
    cash_guard_block._r37_agent._defer_ledger = [entry]
    base = _act([[], ["SELL", "WOOL", 1]])  # 空槽+520 现金→重试会先回填再交守卫

    def _boom(observation, action, floors):
        raise RuntimeError("guard down")

    monkeypatch.setattr(cash_guard_block, "_r37_cash_guard", _boom)
    out = cash_guard_block._r37_agent(dict(_obs(520), step=10), base)
    assert out is base
    assert base["market"][0] == []  # 输入不被原地改动
    assert cash_guard_block._r37_agent._defer_ledger == [entry]  # 账不动

    def _weird(observation, action, floors):
        return {"hit_floor": None, "adjusted_action": "oops"}

    monkeypatch.setattr(cash_guard_block, "_r37_cash_guard", _weird)
    out2 = cash_guard_block._r37_agent(dict(_obs(520), step=10), base)
    assert out2 is base
    assert cash_guard_block._r37_agent._defer_ledger == [entry]


def test_r37_agent_step0_reset():
    # ③step==0 复位顺延账：预置账后 step0 调用→账清；复位先于重试（预置
    # BUY_ANIMAL 意图即便现金达标也不回填）。
    cash_guard_block._r37_agent._defer_ledger = [
        {"op": "BUY_ANIMAL", "item": "GOOSE", "qty": 1, "cost": 300, "slot": 0},
        {"op": "BUY_SEED", "item": "MELON", "qty": 1, "cost": 80, "slot": 1}]
    base = _act([[], ["SELL", "WOOL", 1]])
    out = cash_guard_block._r37_agent(dict(_obs(520), step=0), base)
    assert out is base  # step 0 窗外且动作无购买单→零干预
    assert base["market"][0] == []  # 携带意图未被回填
    assert cash_guard_block._r37_agent._defer_ledger == []


def test_r37_agent_retry_refill():
    # ④账中 BUY_ANIMAL+现金达标→回填空槽成功出账（真守卫同口径同线不误伤：
    # at 520≥300[GOOSE 实际成本]→零足迹放行，回填单留存）。
    cash_guard_block._r37_agent._defer_ledger = [
        {"op": "BUY_ANIMAL", "item": "GOOSE", "qty": 1, "cost": 300, "slot": 3}]
    base = _act([[], ["SELL", "WOOL", 1]])
    out = cash_guard_block._r37_agent(dict(_obs(520), step=10), base)
    assert out is not base
    assert out["market"][0] == ["BUY_ANIMAL", "GOOSE", 1]
    assert out["market"][1] is base["market"][1]
    assert base["market"][0] == []  # 输入不被原地改动
    assert cash_guard_block._r37_agent._defer_ledger == []  # 回填成功→出账

    # ⑤满 10 槽（cap）→留账不回填且不挤占既有单（槽位对象逐一原样）。
    entry5 = {"op": "BUY_ANIMAL", "item": "SHEEP", "qty": 1, "cost": 500, "slot": 0}
    cash_guard_block._r37_agent._defer_ledger = [entry5]
    base5 = _act([["SELL", "WOOL", 1]] + [["BUY_SEED", "WHEAT", 1]] * 9)
    out5 = cash_guard_block._r37_agent(dict(_obs(900), step=10), base5)
    assert out5 is base5
    assert all(out5["market"][i] is base5["market"][i] for i in range(10))
    assert cash_guard_block._r37_agent._defer_ledger == [entry5]  # 满 10 留账

    # ⑤b 无空槽但有余量（<10 槽）→尾部追加当步落位（09-26 修订⑤：消
    # "等空槽 101 步"的计划漂移蝴蝶——门禁死种超标确诊根因）；既有槽不动。
    entry5b = {"op": "BUY_ANIMAL", "item": "SHEEP", "qty": 1, "cost": 500, "slot": 0}
    cash_guard_block._r37_agent._defer_ledger = [entry5b]
    base5b = _act([["SELL", "WOOL", 1], ["BUY_SEED", "WHEAT", 1], ["HIRE"]])
    out5b = cash_guard_block._r37_agent(dict(_obs(900), step=10), base5b)
    assert out5b is not base5b
    assert out5b["market"][:3] == [["SELL", "WOOL", 1],
                                   ["BUY_SEED", "WHEAT", 1], ["HIRE"]]
    assert out5b["market"][3] == ["BUY_ANIMAL", "SHEEP", 1]
    assert all(out5b["market"][i] is base5b["market"][i] for i in range(3))
    assert cash_guard_block._r37_agent._defer_ledger == []  # 尾部落位→出账

    # ⑥逐单价线（修订①）：350<400（COW 成本）→留账不回填；450 分界=
    # COW（400）回填/SHEEP（500）留账（付得起的不再被平线 500 连坐）。
    entry6 = {"op": "BUY_ANIMAL", "item": "COW", "qty": 1, "cost": 400, "slot": 1}
    cash_guard_block._r37_agent._defer_ledger = [entry6]
    base6 = _act([[], ["SELL", "WOOL", 1]])
    out6 = cash_guard_block._r37_agent(dict(_obs(350), step=10), base6)
    assert out6 is base6
    assert base6["market"][0] == []  # 空槽未被回填
    assert cash_guard_block._r37_agent._defer_ledger == [entry6]

    cash_guard_block._r37_agent._defer_ledger = [dict(entry6)]
    out6b = cash_guard_block._r37_agent(dict(_obs(450), step=10),
                                        _act([[], ["SELL", "WOOL", 1]]))
    assert out6b["market"][0] == ["BUY_ANIMAL", "COW", 1]   # 450≥400 回填
    assert cash_guard_block._r37_agent._defer_ledger == []

    entry6c = {"op": "BUY_ANIMAL", "item": "SHEEP", "qty": 1, "cost": 500, "slot": 1}
    cash_guard_block._r37_agent._defer_ledger = [dict(entry6c)]
    out6c = cash_guard_block._r37_agent(dict(_obs(450), step=10),
                                        _act([[], ["SELL", "WOOL", 1]]))
    assert out6c["market"][0] == []                          # 450<500 留账
    assert cash_guard_block._r37_agent._defer_ledger == [entry6c]


def test_r37_agent_seed_refill():
    # ⑨BUY_SEED 入重发范围（修订③）：账中种子现金达标即回填空 [] 槽（FIFO）。
    cash_guard_block._r37_agent._defer_ledger = [
        {"op": "BUY_SEED", "item": "MELON", "qty": 1, "cost": 80, "slot": 1}]
    base = _act([[], ["SELL", "WOOL", 1]])
    out = cash_guard_block._r37_agent(dict(_obs(100), step=10), base)
    assert out is not base
    assert out["market"][0] == ["BUY_SEED", "MELON", 1]
    assert out["market"][1] is base["market"][1]  # 卖单原对象不动
    assert base["market"][0] == []
    assert cash_guard_block._r37_agent._defer_ledger == []  # 回填成功→出账

    # FIFO+高价意图不饿死低价意图：SHEEP（500>450）无可负担空槽→留账，
    # 后续 MELON 照常回填（旧版 break 连坐=种子永久丢弃根因③）。
    sheep = {"op": "BUY_ANIMAL", "item": "SHEEP", "qty": 1, "cost": 500, "slot": 0}
    melon = {"op": "BUY_SEED", "item": "MELON", "qty": 1, "cost": 80, "slot": 1}
    cash_guard_block._r37_agent._defer_ledger = [sheep, melon]
    out2 = cash_guard_block._r37_agent(dict(_obs(450), step=10),
                                       _act([[], [], ["HIRE"]]))
    assert out2["market"][0] == ["BUY_SEED", "MELON", 1]   # 低价意图先补上
    assert out2["market"][1] == []
    assert out2["market"][2] is not None
    assert cash_guard_block._r37_agent._defer_ledger == [sheep]  # 高价意图留账

    # 账序=顺延序（FIFO）：两条均可负担→按账序落先后空槽。
    cash_guard_block._r37_agent._defer_ledger = [
        {"op": "BUY_SEED", "item": "MELON", "qty": 1, "cost": 80, "slot": 5},
        {"op": "BUY_ANIMAL", "item": "GOOSE", "qty": 1, "cost": 300, "slot": 6}]
    base3 = _act([[], [], ["SELL", "WOOL", 1]])
    out3 = cash_guard_block._r37_agent(dict(_obs(600), step=10), base3)
    assert out3["market"][0] == ["BUY_SEED", "MELON", 1]     # 先顺延先回填
    assert out3["market"][1] == ["BUY_ANIMAL", "GOOSE", 1]
    assert out3["market"][2] is base3["market"][2]           # 卖单原对象不动
    assert cash_guard_block._r37_agent._defer_ledger == []


def test_r37_agent_action_invariants():
    # ⑦动作集合不变量（回填路径）：HARVEST/卖单/HIRE/既有单一字节不动、
    # 槽位数不变、回填只落空 [] 槽。
    cash_guard_block._r37_agent._defer_ledger = [
        {"op": "BUY_ANIMAL", "item": "GOOSE", "qty": 1, "cost": 300, "slot": 9}]
    base = _act([["SELL", "WOOL", 3], ["BUY_SEED", "MELON", 1], [], ["HIRE"]],
                farmer=["HARVEST"], hands=[["FEED"], ["CARE"], ["NORTH"]])
    out = cash_guard_block._r37_agent(dict(_obs(600), step=10), base)
    assert out["market"][2] == ["BUY_ANIMAL", "GOOSE", 1]  # 回填空槽（at 520≥300）
    assert out["farmer"] is base["farmer"] and out["farmer"] == ["HARVEST"]
    assert out["hands"] is base["hands"]
    assert out["hands"] == [["FEED"], ["CARE"], ["NORTH"]]
    assert out["market"][0] is base["market"][0]
    assert out["market"][1] is base["market"][1]
    assert out["market"][3] is base["market"][3]
    assert len(out["market"]) == len(base["market"]) == 4
    assert base["market"][2] == []
    assert cash_guard_block._r37_agent._defer_ledger == []  # 回填出账

    # ⑦（守卫顺延路径）：MELON 被顺延时卖单/HIRE/槽位数不动，新顺延入账。
    cash_guard_block._r37_agent._defer_ledger = []
    base2 = _act([["SELL", "WOOL", 1], ["BUY_SEED", "MELON", 1], ["HIRE"]],
                 farmer=["HARVEST"], hands=[["FEED"], ["CARE"]])
    out2 = cash_guard_block._r37_agent(dict(_obs(50), step=23), base2)
    assert out2["market"] == [["SELL", "WOOL", 1], [], ["HIRE"]]
    assert out2["farmer"] is base2["farmer"]
    assert out2["hands"] is base2["hands"]
    assert out2["market"][0] is base2["market"][0]
    assert out2["market"][2] is base2["market"][2]
    assert len(out2["market"]) == 3
    assert base2["market"][1] == ["BUY_SEED", "MELON", 1]  # 输入不被原地改动
    assert cash_guard_block._r37_agent._defer_ledger == [
        {"op": "BUY_SEED", "item": "MELON", "qty": 1, "cost": 80, "slot": 1}]


def test_r37_agent_seed_plant_deadline(monkeypatch):
    # ⑩种活时限（修订④）：截止线前回填✓ / 截止线后不出账重发✓ /
    # 出账作废记 reason=plant_deadline✓ / BUY_ANIMAL 不受时限✓。
    # (1) 截止线前（step 624 恰=全局保守线，≤ 截止线才重发）回填照旧出账，
    # 无作废记录。
    cash_guard_block._r37_agent._defer_ledger = [
        {"op": "BUY_SEED", "item": "MELON", "qty": 1, "cost": 80, "slot": 1}]
    cash_guard_block._r37_agent._void_ledger = []
    out = cash_guard_block._r37_agent(dict(_obs(100), step=624),
                                      _act([[], ["SELL", "WOOL", 1]]))
    assert out["market"][0] == ["BUY_SEED", "MELON", 1]
    assert out["market"][1] == ["SELL", "WOOL", 1]     # 卖单不动
    assert cash_guard_block._r37_agent._defer_ledger == []   # 回填成功→出账
    assert cash_guard_block._r37_agent._void_ledger == []

    # (2)(3) 过截止线（step 625）：空槽不回填（不出账重发）、意图出账作废
    # 记 reason=plant_deadline（成活时限正常出清、不算重发失败）；输入动作
    # 不被原地改动。
    entry = {"op": "BUY_SEED", "item": "MELON", "qty": 1, "cost": 80, "slot": 1}
    cash_guard_block._r37_agent._defer_ledger = [entry]
    cash_guard_block._r37_agent._void_ledger = []
    base2 = _act([[], ["SELL", "WOOL", 1]])
    out2 = cash_guard_block._r37_agent(dict(_obs(100), step=625), base2)
    assert out2["market"][0] == []                     # 空槽未被回填
    assert base2["market"][0] == []                    # 输入不被原地改动
    assert cash_guard_block._r37_agent._defer_ledger == []   # 意图出账
    assert cash_guard_block._r37_agent._void_ledger == [
        {"op": "BUY_SEED", "item": "MELON", "qty": 1, "cost": 80,
         "slot": 1, "reason": "plant_deadline", "step": 625}]

    # 作废出账同顺延账 fail-safe 原子提交：guard 抛异常→账与作废记录皆不动。
    entry_f = {"op": "BUY_SEED", "item": "MELON", "qty": 1, "cost": 80,
               "slot": 1}
    cash_guard_block._r37_agent._defer_ledger = [entry_f]
    cash_guard_block._r37_agent._void_ledger = []

    def _boom(observation, action, floors):
        raise RuntimeError("guard down")

    monkeypatch.setattr(cash_guard_block, "_r37_cash_guard", _boom)
    out_f = cash_guard_block._r37_agent(dict(_obs(100), step=700),
                                        _act([[], ["SELL", "WOOL", 1]]))
    assert out_f["market"][0] == []
    assert cash_guard_block._r37_agent._defer_ledger == [entry_f]  # 账不动
    assert cash_guard_block._r37_agent._void_ledger == []          # 记录不动
    monkeypatch.undo()

    # step==0 复位同清作废记录（复位先于重试）。
    cash_guard_block._r37_agent._defer_ledger = []
    cash_guard_block._r37_agent._void_ledger = [
        {"op": "BUY_SEED", "item": "MELON", "qty": 1, "cost": 80,
         "slot": 1, "reason": "plant_deadline", "step": 700}]
    out_r = cash_guard_block._r37_agent(dict(_obs(100), step=0),
                                        _act([[], ["SELL", "WOOL", 1]]))
    assert out_r["market"][0] == []                    # 携带作废意图不回填
    assert cash_guard_block._r37_agent._void_ledger == []

    # (4) BUY_ANIMAL 不受时限（棚仓无成活时限）：过线步（step 700）现金
    # 达标照常回填出账，不产生作废记录。
    goose = {"op": "BUY_ANIMAL", "item": "GOOSE", "qty": 1, "cost": 300,
             "slot": 3}
    cash_guard_block._r37_agent._defer_ledger = [goose]
    cash_guard_block._r37_agent._void_ledger = []
    out3 = cash_guard_block._r37_agent(dict(_obs(520), step=700),
                                       _act([[], ["SELL", "WOOL", 1]]))
    assert out3["market"][0] == ["BUY_ANIMAL", "GOOSE", 1]
    assert cash_guard_block._r37_agent._defer_ledger == []
    assert cash_guard_block._r37_agent._void_ledger == []

    # 逐作物精细线（plant_deadline 参数，缺省 624）：{"CARROT": 600}→step
    # 601 时 CARROT 出账作废、WHEAT（缺项回退 624）照常回填。
    carrot = {"op": "BUY_SEED", "item": "CARROT", "qty": 1, "cost": 20,
              "slot": 4}
    wheat = {"op": "BUY_SEED", "item": "WHEAT", "qty": 1, "cost": 10,
             "slot": 5}
    cash_guard_block._r37_agent._defer_ledger = [carrot, wheat]
    cash_guard_block._r37_agent._void_ledger = []
    out4 = cash_guard_block._r37_agent(dict(_obs(100), step=601),
                                       _act([[], [], ["SELL", "WOOL", 1]]),
                                       plant_deadline={"CARROT": 600})
    assert out4["market"][0] == ["BUY_SEED", "WHEAT", 1]   # 低价意图先补上
    assert out4["market"][1] == []
    assert cash_guard_block._r37_agent._defer_ledger == []
    assert cash_guard_block._r37_agent._void_ledger == [
        {"op": "BUY_SEED", "item": "CARROT", "qty": 1, "cost": 20,
         "slot": 4, "reason": "plant_deadline", "step": 601}]


def test_r37_cash_guard_floor(monkeypatch):
    def F(d0=12, ba="exact_cost", hard=4, prices=None):
        f = {"d0_end": d0, "buy_animal": ba, "hard_min": hard}
        if prices is not None:
            f["prices"] = prices
        return f

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

    # ②逐单价丢单线（修订①）：450 分界——COW（400）放行/羊（500）拦。
    act_cow = _act([["BUY_ANIMAL", "COW", 1]])
    out_cow = cash_guard_block._r37_cash_guard(dict(_obs(450), step=10), act_cow, F())
    assert out_cow["hit_floor"] is None and out_cow["adjusted_action"] is act_cow
    act_sheep = _act([["BUY_ANIMAL", "SHEEP", 1]])
    out_sheep = cash_guard_block._r37_cash_guard(dict(_obs(450), step=10), act_sheep, F())
    assert out_sheep["hit_floor"] == {"floor": 500, "kind": "buy_animal"}
    assert out_sheep["adjusted_action"]["market"] == [[]]
    # 线=qty×单价：COW×2 成本 800，450 执行点不足→整单顺延。
    out_qty = cash_guard_block._r37_cash_guard(dict(_obs(450), step=10),
                                               _act([["BUY_ANIMAL", "COW", 2]]), F())
    assert out_qty["hit_floor"] == {"floor": 800, "kind": "buy_animal"}
    assert out_qty["adjusted_action"]["market"] == [[]]
    # 执行点口径钉住：提交前 850 ≥ 400 不触（动作后 450<500 不作触发）。
    out_b2 = cash_guard_block._r37_cash_guard(dict(_obs(850), step=10), act_cow, F())
    assert out_b2["hit_floor"] is None and out_b2["adjusted_action"] is act_cow

    # ③未触线零足迹（monkeypatch 计数 defer 未被调用）；换桩后 undo 保后续用例真 defer。
    calls = []

    def _counting(observation, action, hit_floor, prices=None):
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
    # buy_animal 经 prices 覆盖表标定：GOOSE 提交前 550 缺省（300）放行、
    # 覆盖价 600 下触线（逐单价线随之移动）。
    act_g = _act([["BUY_ANIMAL", "GOOSE", 1]])
    out_g = cash_guard_block._r37_cash_guard(dict(_obs(550), step=10), act_g, F())
    assert out_g["hit_floor"] is None and out_g["adjusted_action"] is act_g
    out_g2 = cash_guard_block._r37_cash_guard(dict(_obs(550), step=10), act_g,
                                              F(prices={"GOOSE": 600}))
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
                      {"d0_end": 12, "buy_animal": "exact_cost"},   # 缺 hard_min
                      {"d0_end": "12", "buy_animal": "exact_cost",
                       "hard_min": 4},                              # 非数
                      {"d0_end": 12, "buy_animal": "exact_cost",
                       "hard_min": None},                           # 非数
                      {"d0_end": True, "buy_animal": "exact_cost",
                       "hard_min": 4},                              # bool 不作数
                      {"d0_end": float("nan"), "buy_animal": "exact_cost",
                       "hard_min": 4},
                      {"d0_end": 12, "buy_animal": "exact_cost",
                       "hard_min": float("inf")},
                      {"d0_end": 12, "buy_animal": 500,              # 旧版平线数值废止
                       "hard_min": 4},
                      {"d0_end": 12, "buy_animal": "exact_cost", "hard_min": 4,
                       "prices": "x"},                              # prices 非 dict
                      {"d0_end": 12, "buy_animal": "exact_cost", "hard_min": 4,
                       "prices": {"COW": -1}},                      # 非正价
                      {"d0_end": 12, "buy_animal": "exact_cost", "hard_min": 4,
                       "prices": {"COW": "400"}}):                  # 非数价
        out_m = cash_guard_block._r37_cash_guard(_obs(50), act_m, bad_floor)
        assert out_m["hit_floor"] is None and out_m["adjusted_action"] is act_m, bad_floor

    weird = ["BUY_SEED", "MELON", 1]  # action 非 dict
    out_m = cash_guard_block._r37_cash_guard(_obs(50), weird, F())
    assert out_m["hit_floor"] is None and out_m["adjusted_action"] is weird

    # ⑦双命中取 d0_end（修订①：其处置覆盖逐单丢单保护）：d0 窗内 + BUY_ANIMAL
    # 执行点 300<400 + 动作后 −100<12 两线同触 → 随 d0_end（floor 12）。
    act_h = _act([["BUY_ANIMAL", "COW", 1]])
    out_h = cash_guard_block._r37_cash_guard(dict(_obs(300), step=23), act_h, F())
    assert out_h["hit_floor"] == {"floor": 12, "kind": "d0_end"}
    assert out_h["adjusted_action"]["market"] == [[]]
    # d0_end 配高更严同随 d0_end（end=170、GOOSE 执行点 470 付得起 300 不触
    # 丢单线），顺延直至 600（MELON→GOOSE 全缓仍 550<600 尽力返回）。
    act_h2 = _act([["BUY_SEED", "MELON", 1], ["BUY_ANIMAL", "GOOSE", 1]])
    out_h2 = cash_guard_block._r37_cash_guard(dict(_obs(550), step=23), act_h2, F(d0=600))
    assert out_h2["hit_floor"] == {"floor": 600, "kind": "d0_end"}
    assert out_h2["adjusted_action"]["market"] == [[], []]
    # 等值取 d0_end。
    out_h3 = cash_guard_block._r37_cash_guard(dict(_obs(300), step=23), act_h, F(d0=500))
    assert out_h3["hit_floor"] == {"floor": 500, "kind": "d0_end"}
    # 窗外纯丢单→kind=buy_animal（触发线=被拦单成本）。
    out_h4 = cash_guard_block._r37_cash_guard(dict(_obs(300), step=10), act_h, F())
    assert out_h4["hit_floor"] == {"floor": 400, "kind": "buy_animal"}
    assert out_h4["adjusted_action"]["market"] == [[]]


def test_r37_cash_guard_sell_income():
    # ⑧卖单收入计入（修订②）：位序在前 SELL 收入（2×60=120）使 COW 执行点
    # 320+120=440 ≥ 400 放行（旧口径 320<500 连坐=过度扣单根因②）；卖价
    # 估计=observation 市场价（_obs prices → market.prices）。
    F = {"d0_end": 12, "buy_animal": "exact_cost", "hard_min": 4}
    act = _act([["SELL", "WOOL", 2], ["BUY_ANIMAL", "COW", 1]])
    out = cash_guard_block._r37_cash_guard(
        dict(_obs(320, prices={"WOOL": 60}), step=10), act, F)
    assert out["hit_floor"] is None and out["adjusted_action"] is act
    assert out["adjusted_action"]["market"][0] is act["market"][0]  # 卖单不动

    # 位序在后的卖单不计（引擎先序单位先成交：BUY 先结算，收入救不了它）。
    act2 = _act([["BUY_ANIMAL", "COW", 1], ["SELL", "WOOL", 2]])
    out2 = cash_guard_block._r37_cash_guard(
        dict(_obs(320, prices={"WOOL": 60}), step=10), act2, F)
    assert out2["hit_floor"] == {"floor": 400, "kind": "buy_animal"}
    assert out2["adjusted_action"]["market"] == [[], ["SELL", "WOOL", 2]]
    assert out2["adjusted_action"]["market"][1] is act2["market"][1]  # 卖单不动

    # 卖价读不到→回退不计=保守：同型同现金仍拦（上例放行不是本来就不拦）。
    out3 = cash_guard_block._r37_cash_guard(dict(_obs(320), step=10), act, F)
    assert out3["hit_floor"] == {"floor": 400, "kind": "buy_animal"}
    assert out3["adjusted_action"]["market"] == [["SELL", "WOOL", 2], []]

    # d0 end 同计卖单收入：30+120−10=140 ≥ 12 不触 d0_end（卖单不动）。
    act4 = _act([["SELL", "WOOL", 2], ["BUY_SEED", "WHEAT", 1]])
    out4 = cash_guard_block._r37_cash_guard(
        _obs(30, prices={"WOOL": 60}), act4, F)
    assert out4["hit_floor"] is None and out4["adjusted_action"] is act4


def _obs(money, hires_today=0, prices=None):
    """合成 observation：cash_guard_block 只读 player / farms[seat] 的 money、
    hires_today（引擎 farm 字段名，kaggriculture.py _new_farm）；prices 非
    None 时补 observation["market"]["prices"]（卖价估计口径，修订②）。"""
    obs = {"player": 0, "step": 23, "day": 0, "hour": 23,
           "farms": [{"money": money, "hires_today": hires_today}]}
    if prices is not None:
        obs["market"] = {"prices": prices}
    return obs


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


def test_r37_defer_low_priority_buy_animal_exact_cost():
    # ②a 逐单价丢单保护（修订①）：SHEEP×2 成本 1000>320 整单入顺延账+槽置 []，
    # 卖单不动；320<1000 无单可缓→尽力返回不抛。
    act = _act([["BUY_ANIMAL", "SHEEP", 2], ["SELL", "WOOL", 3]])
    out = cash_guard_block._r37_defer_low_priority(
        _obs(320), act, {"floor": 500, "kind": "buy_animal"})
    assert out["action"]["market"][0] == []
    assert out["action"]["market"][1] is act["market"][1]
    assert len(out["action"]["market"]) == 2
    assert out["deferred"] == [{"op": "BUY_ANIMAL", "item": "SHEEP", "qty": 2,
                                "cost": 1000, "slot": 0}]

    # ②b 付得起的单不拦（旧版平线 500 连坐废止）：COW 成本 400≤450 执行点
    # 付得起→零顺延零足迹（哪怕下限 12 已满足旧版仍顺延→红即回退）。
    act_b = _act([["BUY_ANIMAL", "COW", 1]])
    out_b = cash_guard_block._r37_defer_low_priority(
        _obs(450), act_b, {"floor": 12, "kind": "d0_end"})
    assert out_b["action"] is act_b and out_b["deferred"] == []
    # 450 分界另一半：SHEEP 成本 500>450 → 整单入账。
    act_c = _act([["BUY_ANIMAL", "SHEEP", 1]])
    out_c = cash_guard_block._r37_defer_low_priority(
        _obs(450), act_c, {"floor": 12, "kind": "d0_end"})
    assert out_c["action"]["market"] == [[]]
    assert out_c["deferred"] == [{"op": "BUY_ANIMAL", "item": "SHEEP", "qty": 1,
                                  "cost": 500, "slot": 0}]
    # 线=qty×单价：COW×2 成本 800>450 → 整单入账（cost 记 800）。
    act_d = _act([["BUY_ANIMAL", "COW", 2]])
    out_d = cash_guard_block._r37_defer_low_priority(
        _obs(450), act_d, {"floor": 12, "kind": "d0_end"})
    assert out_d["action"]["market"] == [[]]
    assert out_d["deferred"] == [{"op": "BUY_ANIMAL", "item": "COW", "qty": 2,
                                  "cost": 800, "slot": 0}]


def test_r37_defer_low_priority_no_end_floor_for_buy_animal():
    # ⑨kind=buy_animal 不施加 end 下限（平线连坐废止）：现金 450、动作后 0，
    # COW 执行点付得起→零顺延（旧版按 end<500 连坐全缓→红即回退）。
    act = _act([["BUY_ANIMAL", "COW", 1]])
    out = cash_guard_block._r37_defer_low_priority(
        _obs(450), act, {"floor": 500, "kind": "buy_animal"})
    assert out["action"] is act and out["deferred"] == []


def test_r37_defer_low_priority_sell_income():
    # ⑧卖单收入计入 end（修订②）：30+2×60−80=70 ≥ 12 → 零顺延，卖单不动；
    # 卖价估计=observation 市场价（_obs prices → market.prices）。
    act = _act([["SELL", "WOOL", 2], ["BUY_SEED", "MELON", 1]])
    out = cash_guard_block._r37_defer_low_priority(
        _obs(30, prices={"WOOL": 60}), act, {"floor": 12, "kind": "d0_end"})
    assert out["action"] is act and out["deferred"] == []
    assert act["market"][0] == ["SELL", "WOOL", 2]  # 卖单不动（反例）
    # 卖价读不到→回退不计=保守：30−80=−50 < 12 仍缓 MELON（卖单依旧不动）。
    out2 = cash_guard_block._r37_defer_low_priority(
        _obs(30), act, {"floor": 12, "kind": "d0_end"})
    assert out2["action"]["market"] == [["SELL", "WOOL", 2], []]
    assert out2["action"]["market"][0] is act["market"][0]
    assert out2["deferred"] == [{"op": "BUY_SEED", "item": "MELON", "qty": 1,
                                 "cost": 80, "slot": 1}]


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
                      {"floor": 12, "kind": "weird"},   # kind 枚举外
                      {"floor": 12, "kind": 500},       # kind 非 str
                      None):                            # 非 dict
        out = cash_guard_block._r37_defer_low_priority(_obs(50), act, bad_floor)
        assert out["action"] is act and out["deferred"] == [], bad_floor

    for bad_prices in ("x", {"COW": 0}, {"COW": -1}, {"COW": "400"}, [1]):
        out = cash_guard_block._r37_defer_low_priority(
            _obs(50), act, {"floor": 12, "kind": "d0_end"}, bad_prices)
        assert out["action"] is act and out["deferred"] == [], bad_prices

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
