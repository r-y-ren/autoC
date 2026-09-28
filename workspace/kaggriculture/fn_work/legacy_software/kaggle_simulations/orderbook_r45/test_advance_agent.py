# -*- coding: utf-8 -*-
"""R28 测试面：债务账本式卖提前层（select 条件集/apply 记债/settle 抵扣+净量恒等/
lead 删失口径/agent 运行时包装）。合成夹具不跑真局；动作/观测字段形状以存量为真值。"""
from __future__ import annotations

from types import SimpleNamespace

from orderbook_r45 import advance_layer as al


# ---- 合成夹具（字段形状=存量真值：obs {step,player,market{prices,inventory},
#      town{unlocked_shops},private{shed}}；action {farmer,hands,market}） ----
def _obs(step=200, prices=None, shed=None, inv=None, shops=(), player=0):
    return {"step": step, "player": player,
            "market": {"prices": dict(prices or {}),
                       "inventory": dict(inv or {})},
            "town": {"unlocked_shops": list(shops)},
            "private": {"shed": dict(shed or {}), "seeds": {},
                        "inventories": [{}, {}]}}


def _act(market=()):
    return {"farmer": ["PASS"], "hands": [], "market": [list(o) for o in market]}


def _ledger(debts=None, settled=None):
    return {"debts": list(debts or []), "settled": list(settled or [])}


def _impl(tape, players=None):
    """假 _IMPL（layer S 先例 _FakeChassis 同口径）：chassis.routes/players。"""
    ch = SimpleNamespace(routes={1: tape},
                         players=players or {0: {"route": 1}})
    return SimpleNamespace(chassis=ch)


# 1 参真形态宿主 mock（r40 基座末 callable=_route40_agent(observation) 同元数）
def _route40_agent(observation):
    step = observation.get("step")
    if step == 200:
        return _act([["BUY_SEED", "WHEAT", 1]])
    if step == 203:
        return _act([["SELL", "EGG", 3]])
    return _act()


# 2 参宿主 mock（元数自适应对照组）
def _two_arg_host(observation, configuration=None):
    return _act([["SELL", "WHEAT", 1]])


# ---- select：条件集逐条 -------------------------------------------------
def test_select_advanceable(monkeypatch):
    """条件集：k 拍窗/已入仓/报价门（quote≥2∧quote≥base）/首单保护/已提前净额。"""
    monkeypatch.setattr(al, "_ADV_K", 4)
    obs = _obs(step=200, prices={"EGG": 60.0, "WHEAT": 30.0},
               shed={"EGG": 5, "WHEAT": 5})
    # 正例：首计划卖单保护（201 不动）+ 203 可提前（to_step=当前拍）
    view = {201: {"sells": {"EGG": 2}}, 203: {"sells": {"EGG": 3}}}
    assert al.select_advanceable(obs, view, _ledger()) == [
        {"item": "EGG", "qty": 3, "from_step": 203, "to_step": 200}]
    # 首单保护：该品只有 1 张计划卖单→零提前
    assert al.select_advanceable(obs, {202: {"sells": {"EGG": 5}}}, _ledger()) == []
    # k 拍窗：+5 超 k=4→不选；k 调 6（config 可调）后可选
    view2 = {201: {"sells": {"EGG": 1}}, 205: {"sells": {"EGG": 4}}}
    assert al.select_advanceable(obs, view2, _ledger()) == []
    monkeypatch.setattr(al, "_ADV_K", 6)
    assert al.select_advanceable(obs, view2, _ledger()) == [
        {"item": "EGG", "qty": 4, "from_step": 205, "to_step": 200}]
    monkeypatch.setattr(al, "_ADV_K", 4)
    # 已入仓：可提前量≤在仓（shed 2→只提前 2）；缺货→零提前
    obs2 = _obs(step=200, prices={"EGG": 60.0}, shed={"EGG": 2})
    assert al.select_advanceable(
        obs2, {201: {"sells": {"EGG": 1}}, 203: {"sells": {"EGG": 5}}},
        _ledger()) == [{"item": "EGG", "qty": 2, "from_step": 203,
                        "to_step": 200}]
    obs3 = _obs(step=200, prices={"EGG": 60.0}, shed={})
    assert al.select_advanceable(obs3, view, _ledger()) == []
    # 报价门：quote<2 永不提前；quote<base 谷底闸门拦；quote==base 放行
    obs4 = _obs(step=200, prices={"EGG": 1.5}, shed={"EGG": 5})
    assert al.select_advanceable(obs4, view, _ledger()) == []
    obs5 = _obs(step=200, prices={"EGG": 40.0}, shed={"EGG": 5})  # base 50
    assert al.select_advanceable(obs5, view, _ledger()) == []
    obs6 = _obs(step=200, prices={"EGG": 50.0}, shed={"EGG": 5})
    assert al.select_advanceable(obs6, view, _ledger()) == [
        {"item": "EGG", "qty": 3, "from_step": 203, "to_step": 200}]
    # 已提前净额：同 (item,due_step) 已记债量净扣（5−3→只再提前 2）
    led = _ledger([{"item": "EGG", "qty": 3, "due_step": 203,
                    "advance_step": 198}])
    assert al.select_advanceable(
        obs, {201: {"sells": {"EGG": 1}}, 203: {"sells": {"EGG": 5}}},
        led) == [{"item": "EGG", "qty": 2, "from_step": 203, "to_step": 200}]
    # 零量计划卖单不算"本就要卖"
    assert al.select_advanceable(
        obs, {201: {"sells": {"EGG": 1}}, 203: {"sells": {"EGG": 0}}},
        _ledger()) == []


def test_select_advanceable_turn_gates():
    """清晨拍 step%24==23 零动作；同拍 BUY_PRODUCT 整拍门；当天 PICKUP 整品排除。"""
    obs = _obs(step=200, prices={"EGG": 60.0, "WHEAT": 30.0},
               shed={"EGG": 5, "WHEAT": 5})
    view = {201: {"sells": {"EGG": 1, "WHEAT": 1}},
            203: {"sells": {"EGG": 3, "WHEAT": 3}}}
    assert al.select_advanceable(obs, view, _ledger())  # 基线有动作
    # 清晨结算拍（215=day8h23）
    assert al.select_advanceable(_obs(step=215, prices={"EGG": 60.0},
                                      shed={"EGG": 5}), view, _ledger()) == []
    # 同拍 BUY_PRODUCT→整拍零动作（即便买的是别的品）
    view_buy = dict(view)
    view_buy[200] = {"buy_product": {"WHEAT": 1}}
    assert al.select_advanceable(obs, view_buy, _ledger()) == []
    # 当天 PICKUP 品排除（EGG 排除、WHEAT 照常）
    view_pick = dict(view)
    view_pick[205] = {"pickup": {"EGG": 1}}  # 205 在 day8（192-215）内
    out = al.select_advanceable(obs, view_pick, _ledger())
    assert [o["item"] for o in out] == ["WHEAT"]
    # 非当天 PICKUP（220 属 day9）不排除
    view_pick2 = dict(view)
    view_pick2[220] = {"pickup": {"EGG": 1}}
    assert [o["item"] for o in al.select_advanceable(
        obs, view_pick2, _ledger())] == ["EGG", "WHEAT"]


def test_select_advanceable_horizon_and_window(monkeypatch):
    """视界 clamp(measure_rival_lead()+12,40,48)：lead+12 边、40 下界、48 封顶；
    窗口 step 192-695 边界（之外零动作）。"""
    monkeypatch.setattr(al, "_ADV_K", 50)  # 放开 k 使视界成为实际约束
    obs = _obs(step=200, prices={"WHEAT": 30.0}, shed={"WHEAT": 100})
    view = {236: {"sells": {"WHEAT": 1}}, 238: {"sells": {"WHEAT": 1}},
            242: {"sells": {"WHEAT": 1}}, 250: {"sells": {"WHEAT": 1}}}

    def _lead(monkeypatch, value):
        monkeypatch.setattr(al, "measure_rival_lead", lambda hist: value)

    # lead=0→0+12=12→下界 40：238 进（≤240）、242/250 出
    _lead(monkeypatch, 0)
    assert [o["from_step"] for o in al.select_advanceable(
        obs, view, _ledger())] == [238]
    # lead=29→41：242（=242>241）出
    _lead(monkeypatch, 29)
    assert [o["from_step"] for o in al.select_advanceable(
        obs, view, _ledger())] == [238]
    # lead=30→42：242 进、250 出（lead+12 边界）
    _lead(monkeypatch, 30)
    assert [o["from_step"] for o in al.select_advanceable(
        obs, view, _ledger())] == [238, 242]
    # lead=100→112→封顶 48：242 进、250（=250>248）出
    _lead(monkeypatch, 100)
    assert [o["from_step"] for o in al.select_advanceable(
        obs, view, _ledger())] == [238, 242]
    # 窗口 192-695 边界（191/696 外零动作；192/694 内有动作；695=dawn 拍另测）
    monkeypatch.setattr(al, "_ADV_K", 4)
    monkeypatch.setattr(al, "measure_rival_lead", lambda hist: 40)
    ok_view = {194: {"sells": {"WHEAT": 1}}, 196: {"sells": {"WHEAT": 1}}}
    assert al.select_advanceable(_obs(step=191, prices={"WHEAT": 30.0},
                                      shed={"WHEAT": 5}), ok_view,
                                 _ledger()) == []
    assert al.select_advanceable(_obs(step=192, prices={"WHEAT": 30.0},
                                      shed={"WHEAT": 5}), ok_view, _ledger())
    tail_view = {697: {"sells": {"WHEAT": 1}}, 698: {"sells": {"WHEAT": 1}}}
    assert al.select_advanceable(_obs(step=696, prices={"WHEAT": 30.0},
                                      shed={"WHEAT": 5}), tail_view,
                                 _ledger()) == []
    assert al.select_advanceable(_obs(step=694, prices={"WHEAT": 30.0},
                                      shed={"WHEAT": 5}),
                                 {696: {"sells": {"WHEAT": 1}},
                                  698: {"sells": {"WHEAT": 1}}},
                                 _ledger())
    # 695=day28h23=dawn 拍（窗口内但清晨拍零动作）
    assert al.select_advanceable(_obs(step=695, prices={"WHEAT": 30.0},
                                      shed={"WHEAT": 5}), tail_view,
                                 _ledger()) == []


def test_select_advanceable_plan_view_failures():
    """计划视图解析失败→空集（零动作）：None/调用异常/条目畸形全数拦下。"""
    obs = _obs(step=200, prices={"EGG": 60.0}, shed={"EGG": 5})
    assert al.select_advanceable(obs, None, _ledger()) == []
    assert al.select_advanceable(obs, "bad-view", _ledger()) == []

    def _boom(o):
        raise RuntimeError("plan view boom")

    assert al.select_advanceable(obs, _boom, _ledger()) == []
    assert al.select_advanceable(obs, lambda o: None, _ledger()) == []
    assert al.select_advanceable(obs, {203: {"sells": {"EGG": 3}}}, None) == []
    for bad in ({"203": {"sells": {"EGG": 3}}},          # 步键非数值
                {203: "bad"},                            # 条目非 dict
                {203: {"sells": {"EGG": "x"}}},          # 量非数值
                {203: {"sells": {"EGG": -1}}},           # 量负
                {203: {"sells": [1, 2]}},                # sells 非 dict
                {203: {"pickup": {"EGG": True}}}):       # 量非数值（bool）
        assert al.select_advanceable(obs, bad, _ledger()) == []


# ---- apply：记债+插队首 -------------------------------------------------
def test_apply_advance_with_debt():
    """插队首保序+等额记债四字段台账；畸形/槽满/账本异常→该笔不提前；原单不动。"""
    orders = [{"item": "EGG", "qty": 3, "from_step": 203, "to_step": 200},
              {"item": "WHEAT", "qty": 2, "from_step": 204, "to_step": 200}]
    action = _act([["BUY_SEED", "WHEAT", 1]])
    led = _ledger()
    res = al.apply_advance_with_debt(orders, action, led)
    assert res["action"]["market"] == [["SELL", "EGG", 3], ["SELL", "WHEAT", 2],
                                       ["BUY_SEED", "WHEAT", 1]]
    assert led["debts"] == [{"item": "EGG", "qty": 3, "due_step": 203,
                             "advance_step": 200},
                            {"item": "WHEAT", "qty": 2, "due_step": 204,
                             "advance_step": 200}]
    assert res["applied"] == orders and res["skipped"] == []
    assert action["market"] == [["BUY_SEED", "WHEAT", 1]]  # 原 action 不动
    # 畸形单→该笔不提前不记账
    led2 = _ledger()
    res2 = al.apply_advance_with_debt(
        [{"item": "EGG", "qty": 0, "from_step": 203, "to_step": 200},
         {"item": None, "qty": 3, "from_step": 203, "to_step": 200},
         {"item": "WHEAT", "qty": 1.5, "from_step": 203, "to_step": 200}],
        _act(), led2)
    assert res2["applied"] == [] and led2["debts"] == []
    assert [s["reason"] for s in res2["skipped"]] == ["malformed"] * 3
    # 10 槽满→不提前（宁缺勿挤，不挤原单）
    led3 = _ledger()
    full = _act([["SELL", "I%d" % i, 1] for i in range(10)])
    res3 = al.apply_advance_with_debt(
        [{"item": "EGG", "qty": 3, "from_step": 203, "to_step": 200}],
        full, led3)
    assert res3["applied"] == [] and led3["debts"] == []
    assert res3["skipped"][0]["reason"] == "no_slot"
    assert len(res3["action"]["market"]) == 10  # 原单不挤
    # 账本异常→全部不提前
    res4 = al.apply_advance_with_debt(orders, _act(), {"debts": "bad"})
    assert res4["applied"] == [] and len(res4["skipped"]) == 2
    # 零提前→原对象原样返回
    a = _act()
    res5 = al.apply_advance_with_debt([], a, _ledger())
    assert res5["action"] is a


# ---- settle：到期抵扣+净量恒等 -----------------------------------------
def test_settle_debts():
    """due_step≤当前拍抵扣（只减不加）；跨步台账防重复抵扣；步不明/账本异常→不抵扣。"""
    led = _ledger([{"item": "EGG", "qty": 3, "due_step": 100,
                    "advance_step": 97}])
    action = {"step": 100, "market": [["SELL", "EGG", 5], ["SELL", "WHEAT", 2]]}
    res = al.settle_debts(action, led)
    assert res["action"]["market"] == [["SELL", "EGG", 2], ["SELL", "WHEAT", 2]]
    assert res["settled"] == [{"item": "EGG", "qty": 3, "due_step": 100,
                               "advance_step": 97, "debt_idx": 0}]
    assert res["warnings"] == []
    assert action["market"][0] == ["SELL", "EGG", 5]  # 原单不改对象
    # 跨步防重复抵扣：闭合债不再抵扣（同拍复调+跨拍均防护）
    again = al.settle_debts({"step": 100, "market": [["SELL", "EGG", 5]]}, led)
    assert again["settled"] == [] and again["action"]["market"] == \
        [["SELL", "EGG", 5]]
    later = al.settle_debts({"step": 101, "market": [["SELL", "EGG", 5]]}, led)
    assert later["settled"] == []
    assert len(led["settled"]) == 1  # 台账恰 1 行（净量恒等不双记）
    # 未到期不抵扣
    led2 = _ledger([{"item": "EGG", "qty": 3, "due_step": 101,
                     "advance_step": 97}])
    r2 = al.settle_debts({"step": 100, "market": [["SELL", "EGG", 5]]}, led2)
    assert r2["settled"] == [] and r2["action"]["market"] == [["SELL", "EGG", 5]]
    # 步标缺失→不抵扣
    r3 = al.settle_debts({"market": [["SELL", "EGG", 5]]}, led2)
    assert r3["settled"] == []
    # 账本异常→不抵扣（宁可不提前也不双卖）
    r4 = al.settle_debts({"step": 100, "market": [["SELL", "EGG", 5]]},
                         {"debts": "bad", "settled": []})
    assert r4["settled"] == []
    assert r4["warnings"] == [{"kind": "ledger_malformed"}]
    assert r4["action"]["market"] == [["SELL", "EGG", 5]]
    # 同品多债累计抵扣（2+3 吃满 5 单量）
    led5 = _ledger([{"item": "EGG", "qty": 2, "due_step": 100,
                     "advance_step": 96},
                    {"item": "EGG", "qty": 3, "due_step": 100,
                     "advance_step": 97}])
    r5 = al.settle_debts({"step": 100, "market": [["SELL", "EGG", 5]]}, led5)
    assert r5["action"]["market"] == [["SELL", "EGG", 0]]
    assert [row["qty"] for row in r5["settled"]] == [2, 3]


def test_settle_debts_overflow_and_identity():
    """债量>单量→该单清零+溢出告警；净量恒等正例=Σadvance=Σsettled；
    违例反例=溢出短口如实入账（Σsettled<Σadvance 可见）。"""
    led = _ledger([{"item": "EGG", "qty": 10, "due_step": 100,
                    "advance_step": 96}])
    res = al.settle_debts({"step": 100, "market": [["SELL", "EGG", 4]]}, led)
    assert res["action"]["market"] == [["SELL", "EGG", 0]]  # 该单清零
    assert res["warnings"] == [{"kind": "settle_overflow", "item": "EGG",
                                "due_step": 100, "debt_qty": 10,
                                "deducted": 4, "short": 6}]
    assert res["settled"][0]["qty"] == 4  # 实际抵扣量如实入账
    adv = sum(r["qty"] for r in led["debts"])
    setl = sum(r["qty"] for r in led["settled"])
    assert (adv, setl) == (10, 4)  # 违例反例：恒等缺口可见（judge 计违例）
    # 全无单可抵：清零不出、短口=全债
    led2 = _ledger([{"item": "WOOL", "qty": 5, "due_step": 100,
                     "advance_step": 96}])
    res2 = al.settle_debts({"step": 100, "market": [["SELL", "EGG", 4]]}, led2)
    assert res2["warnings"][0]["kind"] == "settle_overflow"
    assert res2["warnings"][0]["short"] == 5
    assert res2["settled"][0]["qty"] == 0
    # 净量恒等正例：满额抵扣→逐品 Σadvance=Σsettled
    led3 = _ledger([{"item": "EGG", "qty": 3, "due_step": 100,
                     "advance_step": 97},
                    {"item": "WHEAT", "qty": 2, "due_step": 101,
                     "advance_step": 99}])
    al.settle_debts({"step": 100, "market": [["SELL", "EGG", 3]]}, led3)
    al.settle_debts({"step": 101, "market": [["SELL", "WHEAT", 2]]}, led3)
    sums_adv, sums_set = {}, {}
    for row in led3["debts"]:
        sums_adv[row["item"]] = sums_adv.get(row["item"], 0) + row["qty"]
    for row in led3["settled"]:
        sums_set[row["item"]] = sums_set.get(row["item"], 0) + row["qty"]
    assert sums_adv == sums_set == {"EGG": 3, "WHEAT": 2}


def test_net_identity_roundtrip():
    """端到端纯函数链 select→apply→settle：净量恒等=提前量=到期抵扣量。"""
    obs = _obs(step=200, prices={"EGG": 60.0}, shed={"EGG": 5})
    view = {201: {"sells": {"EGG": 2}}, 203: {"sells": {"EGG": 3}}}
    led = _ledger()
    orders = al.select_advanceable(obs, view, led)
    res = al.apply_advance_with_debt(orders, _act(), led)
    assert res["action"]["market"][0] == ["SELL", "EGG", 3]
    due = orders[0]["from_step"]
    sres = al.settle_debts({"step": due,
                            "market": [["SELL", "EGG", 3]]}, led)
    assert sres["action"]["market"] == [["SELL", "EGG", 0]]
    assert sum(r["qty"] for r in led["debts"]) == \
        sum(r["qty"] for r in led["settled"]) == 3


# ---- measure_rival_lead：库存差分+删失口径 ------------------------------
def test_measure_rival_lead():
    """rival_sold=inv'−inv+town_draw−own_sold；近窗最大 lead；数据不足→默认 40。"""
    assert al.measure_rival_lead([]) == 40
    assert al.measure_rival_lead(None) == 40
    assert al.measure_rival_lead("bad") == 40
    one = [{"step": 200, "market": {"prices": {"EGG": 60.0},
                                    "inventory": {"EGG": 10}},
            "town": {"unlocked_shops": []}, "own_sold": {}}]
    assert al.measure_rival_lead(one) == 40  # 样本不足
    # 正例：200→201 库存 +2=对手卖 2（下界≥2 记事件）；我方 203 实卖→lead=3
    hist = [
        {"step": 200, "market": {"prices": {"EGG": 60.0},
                                 "inventory": {"EGG": 10}},
         "town": {"unlocked_shops": []}, "own_sold": {}},
        {"step": 201, "market": {"prices": {"EGG": 60.0},
                                 "inventory": {"EGG": 12}},
         "town": {"unlocked_shops": []}, "own_sold": {}},
        {"step": 202, "market": {"prices": {"EGG": 60.0},
                                 "inventory": {"EGG": 14}},
         "town": {"unlocked_shops": []}, "own_sold": {}},
        {"step": 203, "market": {"prices": {"EGG": 60.0},
                                 "inventory": {"EGG": 16}},
         "town": {"unlocked_shops": []}, "own_sold": {"EGG": 1}},
    ]
    # 事件 (200,EGG)→lead 203−200=3；(201,EGG)→2；(202,EGG)→1；取最大 3
    assert al.measure_rival_lead(hist) == 3
    # own_sold 扣减：Δ5−own 3=2 仍记事件；town_draw 计入（192 拍日界抽货）
    hist2 = [
        {"step": 192, "market": {"prices": {"EGG": 60.0},
                                 "inventory": {"EGG": 10}},
         "town": {"unlocked_shops": ["PET_CAFE"]},
         "own_sold": {"EGG": 3}},
        {"step": 193, "market": {"prices": {"EGG": 60.0},
                                 "inventory": {"EGG": 15}},
         "town": {"unlocked_shops": ["PET_CAFE"]}, "own_sold": {}},
        {"step": 194, "market": {"prices": {"EGG": 60.0},
                                 "inventory": {"EGG": 15}},
         "town": {"unlocked_shops": ["PET_CAFE"]}, "own_sold": {"EGG": 5}},
    ]
    # draw(192)=镇心 +1（PET_CAFE 抽 CARROT 不涉 EGG）→ rival=15−10+1−3=3≥2
    # 事件 @192；我方 194 实卖 → lead=2
    assert al.measure_rival_lead(hist2) == 2
    # 断档（200→202）→不配对、不填 0（不虚构事件）→ 无事件 → 默认 40
    gap = [hist[0], hist[2]]
    assert al.measure_rival_lead(gap) == 40
    # 下界<2 不记事件（只记下界）
    hist3 = [
        {"step": 200, "market": {"prices": {"EGG": 60.0},
                                 "inventory": {"EGG": 10}},
         "town": {"unlocked_shops": []}, "own_sold": {}},
        {"step": 201, "market": {"prices": {"EGG": 60.0},
                                 "inventory": {"EGG": 11}},
         "town": {"unlocked_shops": []}, "own_sold": {}},
        {"step": 202, "market": {"prices": {"EGG": 60.0},
                                 "inventory": {"EGG": 11}},
         "town": {"unlocked_shops": []}, "own_sold": {"EGG": 1}},
    ]
    assert al.measure_rival_lead(hist3) == 40


def test_measure_rival_lead_censoring():
    """$1 地板删失口径：≤3 报价拍成交不入公开库存→跳过不记 0（只记下界）。"""
    # 地板拍：库存大动也不记事件（不填 0），无事件→默认 40
    floor_hist = [
        {"step": 200, "market": {"prices": {"EGG": 1.0},
                                 "inventory": {"EGG": 10}},
         "town": {"unlocked_shops": []}, "own_sold": {}},
        {"step": 201, "market": {"prices": {"EGG": 1.0},
                                 "inventory": {"EGG": 40}},
         "town": {"unlocked_shops": []}, "own_sold": {}},
        {"step": 202, "market": {"prices": {"EGG": 1.0},
                                 "inventory": {"EGG": 40}},
         "town": {"unlocked_shops": []}, "own_sold": {"EGG": 1}},
    ]
    assert al.measure_rival_lead(floor_hist) == 40
    # 逐品删失：EGG 地板跳过、WOOL 健康照记事件
    mixed = [
        {"step": 200, "market": {"prices": {"EGG": 1.0, "WOOL": 200.0},
                                 "inventory": {"EGG": 10, "WOOL": 10}},
         "town": {"unlocked_shops": []}, "own_sold": {}},
        {"step": 201, "market": {"prices": {"EGG": 1.0, "WOOL": 200.0},
                                 "inventory": {"EGG": 90, "WOOL": 14}},
         "town": {"unlocked_shops": []}, "own_sold": {}},
        {"step": 202, "market": {"prices": {"EGG": 1.0, "WOOL": 200.0},
                                 "inventory": {"EGG": 90, "WOOL": 14}},
         "town": {"unlocked_shops": []}, "own_sold": {"WOOL": 1}},
    ]
    assert al.measure_rival_lead(mixed) == 2  # WOOL 事件 @200，我方 202 实卖
    # 报价缺字段→不确定不记（不填 0）
    nolprice = [
        {"step": 200, "market": {"prices": {}, "inventory": {"EGG": 10}},
         "town": {"unlocked_shops": []}, "own_sold": {}},
        {"step": 201, "market": {"prices": {}, "inventory": {"EGG": 30}},
         "town": {"unlocked_shops": []}, "own_sold": {}},
    ]
    assert al.measure_rival_lead(nolprice) == 40


# ---- _advance_agent：运行时包装（1 参真形态驱动全链） --------------------
def test_advance_agent(monkeypatch):
    """全链（1 参宿主 mock）：settle 先结账→select→apply 记债→到期抵扣；
    净量恒等；零足迹快道回原对象；k 经 configuration 可调。"""
    monkeypatch.setattr(al, "_ADV_HOST_AGENT", _route40_agent)
    monkeypatch.setattr(al, "_ADV_LEDGER", _ledger())
    monkeypatch.setattr(al, "_ADV_HISTORY", [])
    monkeypatch.setattr(al, "_IMPL", _impl(
        {202: {"market": [["SELL", "EGG", 5]]},
         203: {"market": [["SELL", "EGG", 3]]}}), raising=False)
    monkeypatch.setattr(al, "_ADV_K", 4)
    obs200 = _obs(step=200, prices={"EGG": 60.0}, shed={"EGG": 5})
    out = al._advance_agent(obs200, {"k": 4})
    # 提前单插队首（磁带 203 的 3 单位提前到 200 拍；202 首单保护不动）
    assert out == {"farmer": ["PASS"], "hands": [],
                   "market": [["SELL", "EGG", 3], ["BUY_SEED", "WHEAT", 1]]}
    assert al._ADV_LEDGER["debts"] == [
        {"item": "EGG", "qty": 3, "due_step": 203, "advance_step": 200}]
    assert al._ADV_LEDGER["settled"] == []
    # 零足迹快道：安静拍回宿主原动作（同一对象）
    quiet_act = _act()
    monkeypatch.setattr(al, "_ADV_HOST_AGENT",
                        lambda observation, configuration=None: quiet_act)
    assert al._advance_agent(_obs(step=201, prices={"EGG": 60.0},
                                  shed={"EGG": 5}), None) is quiet_act
    monkeypatch.setattr(al, "_ADV_HOST_AGENT", _route40_agent)
    # 到期拍（203）：先结账抵扣磁带卖单→净量恒等 Σadvance=Σsettled
    out3 = al._advance_agent(_obs(step=203, prices={"EGG": 60.0},
                                  shed={"EGG": 5}), None)
    assert out3["market"] == [["SELL", "EGG", 0]]
    assert al._ADV_LEDGER["settled"] == [
        {"item": "EGG", "qty": 3, "due_step": 203, "advance_step": 200,
         "debt_idx": 0}]
    adv = sum(r["qty"] for r in al._ADV_LEDGER["debts"])
    setl = sum(r["qty"] for r in al._ADV_LEDGER["settled"])
    assert adv == setl == 3
    # 重复抵扣防护：203 拍复调不再抵扣（闭合债跳过）
    al._advance_agent(_obs(step=203, prices={"EGG": 60.0}, shed={"EGG": 5}),
                      None)
    assert len(al._ADV_LEDGER["settled"]) == 1
    # k 经 configuration 覆写模块缺省
    al._advance_agent(_obs(step=204, prices={"EGG": 60.0}, shed={"EGG": 5}),
                      {"k": 6})
    assert al._ADV_K == 6


def test_advance_agent_two_arg_host(monkeypatch):
    """2 参宿主用例：元数自适应绑定二参形态（configuration 透传）。"""
    seen = {}

    def _host2(observation, configuration=None):
        seen["cfg"] = configuration
        return _act([["SELL", "WHEAT", 1]])

    monkeypatch.setattr(al, "_ADV_HOST_AGENT", _host2)
    monkeypatch.setattr(al, "_ADV_LEDGER", _ledger())
    monkeypatch.setattr(al, "_ADV_HISTORY", [])
    monkeypatch.setattr(al, "_IMPL", None, raising=False)
    out = al._advance_agent(_obs(step=300, prices={"WHEAT": 30.0},
                                 shed={"WHEAT": 1}), {"k": 4})
    assert out == {"farmer": ["PASS"], "hands": [],
                   "market": [["SELL", "WHEAT", 1]]}
    assert seen["cfg"] == {"k": 4}


def test_advance_agent_fallback_and_reset(monkeypatch):
    """异常回退=宿主原动作同对象；step==0 复位账本+历史。"""
    act = _act([["SELL", "EGG", 1]])
    monkeypatch.setattr(al, "_ADV_HOST_AGENT",
                        lambda observation, configuration=None: act)
    monkeypatch.setattr(al, "_ADV_LEDGER", _ledger(
        [{"item": "EGG", "qty": 3, "due_step": 203, "advance_step": 200}]))
    monkeypatch.setattr(al, "_ADV_HISTORY", [{"step": 7}])
    monkeypatch.setattr(al, "_IMPL", _impl(
        {202: {"market": [["SELL", "EGG", 5]]},
         203: {"market": [["SELL", "EGG", 3]]}}), raising=False)
    # 层内异常→回退宿主原动作（同一对象）
    def _boom(orders, action, ledger):
        raise RuntimeError("apply boom")

    monkeypatch.setattr(al, "apply_advance_with_debt", _boom)
    out = al._advance_agent(_obs(step=200, prices={"EGG": 60.0},
                                 shed={"EGG": 5}), None)
    assert out is act
    # step 解析异常→同一对象
    assert al._advance_agent({"step": "x"}, None) is act
    # step==0 复位账本+观测历史（复位先于链路，抛错亦已复位）
    al._advance_agent(_obs(step=0, prices={"EGG": 60.0}, shed={"EGG": 5}),
                      None)
    assert al._ADV_LEDGER == {"debts": [], "settled": []}
    assert [r["step"] for r in al._ADV_HISTORY] == [0]
