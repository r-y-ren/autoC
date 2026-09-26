# -*- coding: utf-8 -*-
"""R21 测试面：predict_block（运行时五件：入口/infer/match/extrapolate/dodge）。

五组真测试（责任契约 fn_docs/hybrid/responsibility.md【R21 增补】）：
infer 组 = infer_rival_sells（库存差分/城镇消费扣减/下界标志/缺字段空账+
跨步账本）；match 组 = match_sellflow（键命中[step-2 身份指纹]/无键回退
global/置信=样本数×集中度/库缺失置信 0）；extrapolate 组 = extrapolate_sells
（写入 plan 步位/低置信跳过/坏容器不抛）；dodge 组 = apply_dodge（集中抛售
→错峰置 []/减量、未达标与置信不足零动作、买种养单/HARVEST/FEED/CARE/槽位数
不动、异常原动作）；入口组 = _predict_agent（全链串通/异常 fail-safe/
step0 复位/假父层注入）。
合成 obs 形状：{"step","day","hour","player","farms":[{money},…],
"market":{"inventory","prices"},"town":{"unlocked_shops"},"private"}（引擎
kaggriculture.py _new_farm/_new_market/_new_town 口径）。
"""
import pytest  # noqa: F401

try:
    from orderbook_predict import predict_block
except ImportError:  # 兜底：直接以 orderbook_predict/ 为 sys.path 根跑测
    import predict_block


@pytest.fixture(autouse=True)
def _clean_state():
    """清函数属性跨步账，保测试独立。"""
    for fn, attr in ((predict_block.infer_rival_sells, "_ledger"),
                     (predict_block.match_sellflow, "_identity"),
                     (predict_block._predict_agent, "_own_fills"),
                     (predict_block._predict_agent, "_dodge_log"),
                     (predict_block._predict_agent, "_opponent_plan")):
        try:
            delattr(fn, attr)
        except AttributeError:
            pass
    yield


def _obs(step, inv=None, prices=None, shops=None, money=(210.0, 229.0), player=0):
    """合成 observation（player=0 → 对手=farms[1]）。"""
    return {
        "step": step, "day": step // 24, "hour": step % 24, "player": player,
        "farms": [{"money": money[0]}, {"money": money[1]}],
        "market": {"inventory": dict(inv or {}), "prices": dict(prices or {})},
        "town": {"unlocked_shops": list(shops or [])},
        "private": {"shed": {}, "seeds": {}, "inventories": [{}]},
    }


def _act(market, farmer=None, hands=None):
    return {"farmer": farmer if farmer is not None else ["PASS"],
            "hands": hands if hands is not None else [],
            "market": market}


def test_infer_rival_sells():
    # ①库存差分−自家成交（prev=1→cur=2，两端均无城镇消费触发）：
    #   WHEAT 差分 +6、自家净卖 sell2−buy1=1 → 对手净卖 5；
    #   MILK 差分 −2、自家零 → 对手净卖 −2。
    assert predict_block.infer_rival_sells(
        _obs(1, inv={"WHEAT": 1000, "MILK": 500},
             prices={"WHEAT": 25, "MILK": 160}), None) == {}
    out = predict_block.infer_rival_sells(
        _obs(2, inv={"WHEAT": 1006, "MILK": 498},
             prices={"WHEAT": 25, "MILK": 160}),
        {"sell": {"WHEAT": 2}, "buy": {"WHEAT": 1}})
    assert out["WHEAT"] == {"net_qty": 5, "lower_bound": False}
    assert out["MILK"] == {"net_qty": -2, "lower_bound": False}

    # ②城镇消费扣减——店消费（prev=8：8%4==0 触发；YARN_STORE 单品类店倍率 2）：
    #   WOOL 差分 −1 + 消费 2 → 对手净卖 +1。
    predict_block.infer_rival_sells(
        _obs(8, inv={"WOOL": 500}, prices={"WOOL": 200},
             shops=["YARN_STORE"]), None)
    out = predict_block.infer_rival_sells(
        _obs(9, inv={"WOOL": 499}, prices={"WOOL": 200},
             shops=["YARN_STORE"]), None)
    assert out["WOOL"] == {"net_qty": 1, "lower_bound": False}

    # ②b 中心消费（prev=24：24%24==0 触发，全品各 −1、FERTILIZER 不在中心单）：
    #   CARROT 差分 −2 + 消费 1 → 对手净卖 −1；FERTILIZER 零差分零消费→不入账。
    predict_block.infer_rival_sells(
        _obs(24, inv={"CARROT": 300, "FERTILIZER": 40},
             prices={"CARROT": 35, "FERTILIZER": 100}), None)
    out = predict_block.infer_rival_sells(
        _obs(25, inv={"CARROT": 298, "FERTILIZER": 40},
             prices={"CARROT": 35, "FERTILIZER": 100}), None)
    assert out["CARROT"] == {"net_qty": -1, "lower_bound": False}
    assert "FERTILIZER" not in out

    # ③下界标志：MILK 市场价 1（$1 地板成交不入库存）→ lower_bound；
    #   自家账带 floor_sells（WOOL）也置下界；EGG 正常价→False。
    predict_block.infer_rival_sells(
        _obs(1, inv={"MILK": 10, "WOOL": 100, "EGG": 20},
             prices={"MILK": 1, "WOOL": 200, "EGG": 50}), None)
    out = predict_block.infer_rival_sells(
        _obs(2, inv={"MILK": 12, "WOOL": 97, "EGG": 21},
             prices={"MILK": 1, "WOOL": 200, "EGG": 50}),
        {"floor_sells": {"WOOL": 1}})
    assert out["MILK"] == {"net_qty": 2, "lower_bound": True}
    assert out["WOOL"] == {"net_qty": -3, "lower_bound": True}
    assert out["EGG"] == {"net_qty": 1, "lower_bound": False}

    # ④缺字段→空账不抛；跨步账本（函数属性自包含）累积供外推。
    assert predict_block.infer_rival_sells({"step": 5}, None) == {}
    assert predict_block.infer_rival_sells({"step": 5, "market": {}}, None) == {}
    assert predict_block.infer_rival_sells(
        {"step": 6, "market": {"inventory": "bad"}}, None) == {}
    ledger = predict_block.infer_rival_sells._ledger
    assert ledger["prev"]["step"] == 2
    assert ledger["items"]["MILK"] == {"net_qty": 2, "lower_bound": True}
    assert ledger["history"]["WOOL"] == [1, -3]


def test_match_sellflow():
    lib = {"version": "t", "global": {
        "1": {"CARROT": {"qty_sum": 4, "count": 2, "qty_max": 2}}}}
    lib["keys"] = {"BAKERY,YARN_STORE||229.0:9989": {"n_episodes": 5, "hist": {
        "1": {"MILK": {"qty_sum": 9, "count": 3, "qty_max": 4},
              "WOOL": {"qty_sum": 2, "count": 1, "qty_max": 2}}}}}
    # ①键命中：step 2 抓对手身份（farms[1].money=229.0、WHEAT 库存 9989），
    #   step 50 身份值已变仍用 step-2 指纹命中键；win=50//48=1→窗 [0,1,2]。
    o2 = _obs(2, inv={"WHEAT": 9989}, prices={"WHEAT": 25},
              shops=["BAKERY", "YARN_STORE"], money=(210.0, 229.0))
    predict_block.match_sellflow(o2, lib)  # 播种 step-2 身份（229.0:9989）
    o50 = _obs(50, inv={"WHEAT": 9000}, prices={"WHEAT": 25},
               shops=["BAKERY", "YARN_STORE"], money=(250.0, 229.0))
    out = predict_block.match_sellflow(o50, lib)
    m = out["matches"]
    assert m["source"] == "key" and m["key"] == "BAKERY,YARN_STORE||229.0:9989"
    assert m["wins"] == [0, 1, 2] and m["step"] == 50
    assert m["items"]["MILK"] == {"qty_sum": 9, "count": 3, "qty_max": 4}
    assert m["items"]["WOOL"] == {"qty_sum": 2, "count": 1, "qty_max": 2}
    # 置信=样本因子×集中度=(4/10)×(9/11)
    assert abs(out["confidence"] - (4 / 10) * (9 / 11)) < 1e-9

    # ②无键→回退 library["global"]（同 hist 形聚合）。
    out = predict_block.match_sellflow(o50, {"version": "t", "keys": {},
                                             "global": lib["global"]})
    assert out["matches"]["source"] == "global"
    assert out["matches"]["items"]["CARROT"] == {"qty_sum": 4, "count": 2, "qty_max": 2}
    assert abs(out["confidence"] - (2 / 10) * 1.0) < 1e-9

    # ③置信口径：样本因子封顶 1（n=20→1.0）、集中度=最大单品量占比。
    flat = {"global": {"1": {"A": {"qty_sum": 5, "count": 10, "qty_max": 1},
                             "B": {"qty_sum": 5, "count": 10, "qty_max": 1}}}}
    out = predict_block.match_sellflow(o50, flat)
    assert abs(out["confidence"] - 1.0 * 0.5) < 1e-9

    # ④库缺失/畸形→confidence=0 不抛。
    assert predict_block.match_sellflow(o50, None)["confidence"] == 0.0
    assert predict_block.match_sellflow(o50, {})["confidence"] == 0.0
    assert predict_block.match_sellflow(o50, "bad")["confidence"] == 0.0


def test_extrapolate_sells():
    def _mk(conf, items, step=50):
        return {"matches": {"items": items, "wins": [1], "source": "key",
                            "key": "k", "step": step}, "confidence": conf}

    inf = {"step": 50, "items": {"MILK": {"net_qty": 2, "lower_bound": False}}}
    matches = _mk(0.8, {"MILK": {"qty_sum": 10, "count": 5, "qty_max": 3}})

    # ①写入 plan 步位：净卖 2>0→qty=2，落 plan[51]/plan[52]（["SELL",item,qty]）。
    plan = [{"market": []} for _ in range(60)]
    out = predict_block.extrapolate_sells(inf, matches, plan)
    assert out["written"] == [{"step": 51, "item": "MILK", "qty": 2},
                              {"step": 52, "item": "MILK", "qty": 2}]
    assert out["skipped"] == []
    assert plan[51]["market"] == [["SELL", "MILK", 2]]
    assert plan[52]["market"] == [["SELL", "MILK", 2]]

    # ①b 无净卖但库有量→qty=round(qty_sum/count)=2；空槽补 {"market": []}。
    inf2 = {"step": 50, "items": {"WOOL": {"net_qty": 0, "lower_bound": False}}}
    plan2 = [{} for _ in range(60)]
    out = predict_block.extrapolate_sells(
        inf2, _mk(0.8, {"WOOL": {"qty_sum": 10, "count": 5, "qty_max": 3}}), plan2)
    assert plan2[51]["market"] == [["SELL", "WOOL", 2]] and out["written"]

    # ②低置信跳过（0.3<0.5）→不写不抛。
    plan3 = [{"market": []} for _ in range(60)]
    out = predict_block.extrapolate_sells(
        inf, _mk(0.3, {"MILK": {"qty_sum": 10, "count": 5, "qty_max": 3}}), plan3)
    assert out["written"] == [] and out["skipped"]
    assert plan3[51]["market"] == [] and plan3[52]["market"] == []

    # ③坏容器不抛：plan 非列表→不写；槽位/market 畸形→该处不写。
    assert predict_block.extrapolate_sells(inf, matches, {"bad": 1})["written"] == []
    plan4 = [{"market": []}, "bad", {"market": 7}]
    out = predict_block.extrapolate_sells(
        {"step": 0, "items": {"MILK": {"net_qty": 2, "lower_bound": False}}},
        _mk(0.8, {"MILK": {"qty_sum": 10, "count": 5, "qty_max": 3}}, step=0), plan4)
    assert out["written"] == [] and out["skipped"]
    # 步位越界（plan 太短）→不写。
    out = predict_block.extrapolate_sells(inf, matches, [{"market": []}])
    assert out["written"] == [] and out["skipped"]


def test_apply_dodge():
    obs = _obs(50, inv={"MILK": 500}, prices={"MILK": 160, "WOOL": 200, "WHEAT": 25})
    act = _act([["BUY_SEED", "WHEAT", 1], ["SELL", "MILK", 3], ["SELL", "WOOL", 5], []],
               farmer=["HARVEST"], hands=[["FEED"], ["CARE"]])
    pred = {"confidence": 0.9, "sells": [
        {"item": "MILK", "qty": 5, "steps": [51, 52]},  # Q=5≥单量 3→整单顺延
        {"item": "WOOL", "qty": 3, "steps": [51]}]}     # Q=3<单量 5→减量改单

    # ①集中抛售→错峰置 [] 保位次 / 减量改单；买种养单与单元动作一字节不动。
    out = predict_block.apply_dodge(obs, act, pred)
    m = out["action"]["market"]
    assert m[0] == ["BUY_SEED", "WHEAT", 1]        # 买种养单不动
    assert m[1] == []                              # 错峰：槽置 [] 保位次
    assert m[2] == ["SELL", "WOOL", 2]             # 减量改单
    assert m[3] == [] and len(m) == 4              # 槽位数不变（不改出口截断）
    assert out["action"]["farmer"] is act["farmer"]    # HARVEST 不动
    assert out["action"]["hands"] is act["hands"]      # FEED/CARE 不动
    assert out["dodges"] == [
        {"op": "defer", "item": "MILK", "qty": 3, "slot": 1, "due_step": 52},
        {"op": "reduce", "item": "WOOL", "qty": 3, "new_qty": 2, "slot": 2,
         "due_step": 51}]
    # 原动作不被原地改动（避让出新表）。
    assert act["market"][1] == ["SELL", "MILK", 3]

    # ②未达标零动作（Q=2<3）与置信不足零动作（0.4<0.5）：返回原对象。
    out = predict_block.apply_dodge(
        obs, act, {"confidence": 0.9, "sells": [{"item": "MILK", "qty": 2,
                                                 "steps": [51]}]})
    assert out["action"] is act and out["dodges"] == []
    out = predict_block.apply_dodge(
        obs, act, {"confidence": 0.4, "sells": [{"item": "MILK", "qty": 9,
                                                 "steps": [51]}]})
    assert out["action"] is act and out["dodges"] == []
    out = predict_block.apply_dodge(obs, act, None)
    assert out["action"] is act and out["dodges"] == []

    # ③异常→原动作（action 非 dict / predictions 畸形不抛）。
    out = predict_block.apply_dodge(obs, ["not-a-dict"], pred)
    assert out["action"] == ["not-a-dict"] and out["dodges"] == []
    out = predict_block.apply_dodge(obs, act, {"confidence": "bad",
                                               "sells": "bad"})
    assert out["action"] is act and out["dodges"] == []


def test_predict_agent(monkeypatch):
    real_infer = predict_block.infer_rival_sells
    calls = []
    actions = {
        0: _act([]),
        49: _act([]),
        50: _act([["SELL", "MILK", 3]], farmer=["HARVEST"], hands=[["CARE"]]),
    }
    sentinel = _act([["SELL", "WOOL", 1]])
    actions[60] = sentinel

    def _fake_parent(observation):
        calls.append(observation)
        return actions.get(observation["step"], _act([]))

    monkeypatch.setattr(predict_block, "_PREDICT_PARENT", _fake_parent,
                        raising=False)
    lib = {"version": "t", "keys": {
        "BAKERY,YARN_STORE||229.0:9989": {"n_episodes": 8, "hist": {
            "1": {"MILK": {"qty_sum": 20, "count": 10, "qty_max": 6}}}}},
        "global": {}}
    monkeypatch.setattr(predict_block, "_PREDICT_LIBRARY", lib, raising=False)
    shops = ["BAKERY", "YARN_STORE"]

    # ①假父层注入 + ②全链串通：step 49 播种账 → step 50 差分对手净卖 MILK 6
    #   → match 置信 1.0（n=10、集中度 1）→ extrapolate 写 plan[51]/[52]
    #   → apply_dodge 顺延本步 MILK 卖单（槽置 []）。
    o49 = _obs(49, inv={"WHEAT": 9989, "MILK": 500},
               prices={"MILK": 160, "WHEAT": 25}, shops=shops)
    predict_block._predict_agent(o49)
    o50 = _obs(50, inv={"WHEAT": 9989, "MILK": 506},
               prices={"MILK": 160, "WHEAT": 25}, shops=shops)
    out = predict_block._predict_agent(o50)
    assert calls[-1] is o50                       # 假父层被调、观测原样传入
    assert out["market"] == [[]]                  # MILK 卖单被顺延（保位次）
    assert out["farmer"] == ["HARVEST"] and out["hands"] == [["CARE"]]
    plan = predict_block._predict_agent._opponent_plan
    assert plan[51]["market"] == [["SELL", "MILK", 6]]
    assert plan[52]["market"] == [["SELL", "MILK", 6]]
    assert predict_block._predict_agent._dodge_log == [
        {"op": "defer", "item": "MILK", "qty": 3, "slot": 0, "due_step": 52}]
    assert predict_block._predict_agent._own_fills["sell"] == {}  # 被避让→无成交账

    # ③异常 fail-safe：链中 infer 抛→父层动作原样；父层抛→PASS 兜底。
    def _boom(observation):
        raise RuntimeError("chain broke")

    monkeypatch.setattr(predict_block, "infer_rival_sells", _boom)
    out = predict_block._predict_agent(_obs(60, inv={"WHEAT": 9989}))
    assert out is sentinel
    monkeypatch.setattr(predict_block, "infer_rival_sells", real_infer)

    def _bad_parent(observation):
        raise RuntimeError("parent broke")

    monkeypatch.setattr(predict_block, "_PREDICT_PARENT", _bad_parent,
                        raising=False)
    out = predict_block._predict_agent(_obs(61))
    assert out == {"farmer": ["PASS"], "hands": [], "market": []}
    monkeypatch.setattr(predict_block, "_PREDICT_PARENT", _fake_parent,
                        raising=False)

    # ④step0 复位账与 plan 容器（预置脏账→调用后清空重建）。
    predict_block.infer_rival_sells._ledger = {"junk": True}
    predict_block.match_sellflow._identity = {"step": 500, "money": 0, "wheat": 0}
    predict_block._predict_agent._own_fills = {"sell": {"WHEAT": 9}}
    predict_block._predict_agent._dodge_log = [{"junk": 1}]
    old_plan = [{"market": [["SELL", "MILK", 1]]}] * 5
    predict_block._predict_agent._opponent_plan = old_plan
    out = predict_block._predict_agent(
        _obs(0, inv={"WHEAT": 9989}, prices={"WHEAT": 25}, shops=shops))
    assert out == _act([])
    assert "junk" not in predict_block.infer_rival_sells._ledger
    assert predict_block._predict_agent._dodge_log == []
    assert predict_block._predict_agent._opponent_plan is not old_plan
    assert predict_block._predict_agent._own_fills == {"sell": {}, "buy": {},
                                                       "floor_sells": {}}
    assert predict_block.match_sellflow._identity["step"] == 0


def test_match_sellflow_canonical_key():
    """规范键路径钉住（评审 P2）：店对|m钱_w麦 形式直接命中 keys[source="key"]，
    与 sellflow.py 建库口径同构；非整 money 按 int(round()) 量化（P3a 对齐）。"""
    lib = {"version": "sellflow/1.0",
           "keys": {"BAKERY|YARN_STORE||m230_w9989": {
               "n_episodes": 3,
               "hist": {"1": {"WOOL": {"qty_sum": 12, "count": 3, "qty_max": 6}}}}},
           "global": {"n_episodes": 0, "hist": {}}}
    obs = {"step": 50, "player": 0,
           "farms": [{"money": 1.0}, {"money": 229.7, "tiles": []}],
           "market": {"inventory": {"WHEAT": 9989.0}, "prices": {"WOOL": 5}},
           "town": {"unlocked_shops": ["BAKERY", "YARN_STORE"]}}
    obs["step"] = 2   # 身份指纹抓拍点
    from orderbook_predict import predict_block as _pb
    out = _pb.match_sellflow(obs, lib)
    assert out["matches"].get("source") == "key"
    assert (out["matches"].get("key") or "").startswith("BAKERY|YARN_STORE||m230_w")
