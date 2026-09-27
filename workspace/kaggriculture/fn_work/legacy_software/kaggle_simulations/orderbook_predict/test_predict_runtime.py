# -*- coding: utf-8 -*-
"""R21/R22 测试面：predict_block（运行时六件：入口/infer/match/extrapolate/
dodge/detect_clone）。

分组真测试（责任契约 fn_docs/hybrid/responsibility.md【R21/R22 增补】）：
infer 组 = infer_rival_sells（库存差分/城镇消费扣减/下界标志/缺字段空账+
跨步账本）；match 组 = match_sellflow（键命中[step-2 身份指纹]/无键回退
global/置信=样本数×集中度/库缺失置信 0）；extrapolate v2 组 = extrapolate_sells
（限频六道门逐项[窗外/低于 K/每步每品 1 单/带通两端/价门/噪声门]+量级档
少中多+credit 减记与禁净加卖）；dodge v2 组 = apply_dodge（门判定 allow/deny
两分支、action 原样零改动反例、异常全 allow）；入口 v2 组 = _predict_agent
（非克隆零动作零写入/克隆走链/credit step0 复位/deny 回滚/异常 fail-safe）；
clone 组 = detect_clone。
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
                     (predict_block.detect_clone, "_stream"),
                     (predict_block.extrapolate_sells, "_credit"),
                     (predict_block._predict_agent, "_own_fills"),
                     (predict_block._predict_agent, "_dodge_log"),
                     (predict_block._predict_agent, "_opponent_plan"),
                     (predict_block._predict_agent, "_credit"),
                     (predict_block._predict_agent, "_written")):
        try:
            delattr(fn, attr)
        except AttributeError:
            pass
    yield


def _obs(step, inv=None, prices=None, shops=None, money=(210.0, 229.0), player=0,
         shed=None):
    """合成 observation（player=0 → 对手=farms[1]）；shed=自家棚存（v2 棚存口径）。"""
    return {
        "step": step, "day": step // 24, "hour": step % 24, "player": player,
        "farms": [{"money": money[0]}, {"money": money[1]}],
        "market": {"inventory": dict(inv or {}), "prices": dict(prices or {})},
        "town": {"unlocked_shops": list(shops or [])},
        "private": {"shed": dict(shed or {}), "seeds": {}, "inventories": [{}]},
    }


def _act(market, farmer=None, hands=None):
    return {"farmer": farmer if farmer is not None else ["PASS"],
            "hands": hands if hands is not None else [],
            "market": market}


def test_infer_rival_sells():
    # ①精确账（非删失）：价>$3 且 sold≥2 → 精确 net_qty=D−U。
    #   WHEAT 差分 +8、自家净卖 sell3−buy0=3 → 对手净卖 5（sold 5≥2、价 25>3）。
    assert predict_block.infer_rival_sells(
        _obs(1, inv={"WHEAT": 1000}, prices={"WHEAT": 25}), None) == {}
    out = predict_block.infer_rival_sells(
        _obs(2, inv={"WHEAT": 1008}, prices={"WHEAT": 25}),
        {"sell": {"WHEAT": 3}})
    assert out["WHEAT"] == {"net_qty": 5, "lower_bound": False}

    # ②城镇消费扣减（prev=24：24%4==0 店消费 YARN_STORE 倍率 2 + 24%24==0
    #   中心单 +1 → WOOL 消费 3）：差分 −1 + 消费 3 → 对手净卖 2（精确）。
    predict_block.infer_rival_sells(
        _obs(24, inv={"WOOL": 500}, prices={"WOOL": 200},
             shops=["YARN_STORE"]), None)
    out = predict_block.infer_rival_sells(
        _obs(25, inv={"WOOL": 499}, prices={"WOOL": 200},
             shops=["YARN_STORE"]), None)
    assert out["WOOL"] == {"net_qty": 2, "lower_bound": False}

    # ③删失下界标记：价 ≤$3（含界）或自家账带 floor_sells（$1 地板不入公开
    #   库存）→ 只记下界 {max(0,D−U), lower_bound: True}，禁止当精确值。
    #   MILK 价 3：D=5,U=0 → 下界 5；EGG 价 50 但 floor_sells 证据：
    #   D=4,U=1 → 下界 3（下界值计算=max(0, D−U)）。
    predict_block.infer_rival_sells(
        _obs(40, inv={"MILK": 10, "EGG": 20},
             prices={"MILK": 3, "EGG": 50}), None)
    out = predict_block.infer_rival_sells(
        _obs(41, inv={"MILK": 15, "EGG": 24}, prices={"MILK": 3, "EGG": 50}),
        {"sell": {"EGG": 1}, "floor_sells": {"EGG": 2}})
    assert out["MILK"] == {"net_qty": 5, "lower_bound": True}
    assert out["EGG"] == {"net_qty": 3, "lower_bound": True}

    # ④噪声门（sold<2 不入精确账）：价>3 但推算 sold=1 → 只记下界 1。
    predict_block.infer_rival_sells(
        _obs(50, inv={"CARROT": 300}, prices={"CARROT": 35}), None)
    out = predict_block.infer_rival_sells(
        _obs(51, inv={"CARROT": 301}, prices={"CARROT": 35}), None)
    assert out["CARROT"] == {"net_qty": 1, "lower_bound": True}

    # ⑤禁填 0 反例：删失/噪声品下界为 0（D−U≤0）→ 整条不入账，
    #   不得写 {"net_qty": 0, …}。MELON 零差分（价 1 删失）与 WHEAT 负净卖同禁。
    predict_block.infer_rival_sells(
        _obs(60, inv={"MELON": 10, "WHEAT": 100},
             prices={"MELON": 1, "WHEAT": 25}), None)
    out = predict_block.infer_rival_sells(
        _obs(61, inv={"MELON": 10, "WHEAT": 97},
             prices={"MELON": 1, "WHEAT": 25}), None)
    assert out == {}
    assert "MELON" not in out and "WHEAT" not in out

    # ⑥缺字段→空账不抛、账本不动；跨步账本（函数属性自包含）累积供外推。
    assert predict_block.infer_rival_sells({"step": 70}, None) == {}
    assert predict_block.infer_rival_sells({"step": 70, "market": {}}, None) == {}
    assert predict_block.infer_rival_sells(
        {"step": 71, "market": {"inventory": "bad"}}, None) == {}
    ledger = predict_block.infer_rival_sells._ledger
    assert ledger["prev"]["step"] == 61
    assert ledger["items"] == {}
    assert ledger["history"] == {"WHEAT": [5], "WOOL": [2], "MILK": [5],
                                 "EGG": [3], "CARROT": [1]}


def test_match_sellflow():
    lib = {"version": "t", "global": {
        "1": {"CARROT": {"qty_sum": 4, "count": 2, "qty_max": 2}}}}
    lib["keys"] = {"BAKERY,YARN_STORE||229.0:9989": {"n_episodes": 5, "hist": {
        "1": {"MILK": {"qty_sum": 9, "count": 3, "qty_max": 4},
              "WOOL": {"qty_sum": 2, "count": 1, "qty_max": 2}}}}}
    # ①键命中（旧库条目无新字段→沿 v1 采纳）：step 2 抓对手身份
    #   （farms[1].money=229.0、WHEAT 库存 9989），step 50 身份值已变仍用
    #   step-2 指纹命中键；win=50//48=1→窗 [0,1,2]；置信=样本×集中度。
    o2 = _obs(2, inv={"WHEAT": 9989}, prices={"WHEAT": 25},
              shops=["BAKERY", "YARN_STORE"], money=(210.0, 229.0))
    predict_block.match_sellflow(o2, lib)  # 播种 step-2 身份（229.0:9989）
    o50 = _obs(50, inv={"WHEAT": 9000}, prices={"WHEAT": 25},
               shops=["BAKERY", "YARN_STORE"], money=(250.0, 229.0))
    out = predict_block.match_sellflow(o50, lib)
    m = out["matches"]
    assert m["source"] == "key" and m["key"] == "BAKERY,YARN_STORE||229.0:9989"
    assert m["wins"] == [0, 1, 2] and m["step"] == 50 and m["skipped"] is False
    assert m["items"]["MILK"] == {"qty_sum": 9, "count": 3, "qty_max": 4}
    assert m["items"]["WOOL"] == {"qty_sum": 2, "count": 1, "qty_max": 2}
    # 置信=样本因子×集中度=(4/10)×(9/11)
    assert abs(out["confidence"] - (4 / 10) * (9 / 11)) < 1e-9
    assert out["top1"] == {"key": "BAKERY,YARN_STORE||229.0:9989",
                           "source": "key", "adopted": True}

    # ②TOP-1：候选序两键同窗命中→只取 n_episodes 最优一键，不做多键展开
    #   （n=9 > n=2 → 取 legacy 键，WOOL 分布不并入）。
    lib2 = {"version": "t", "keys": {
        "BAKERY|YARN_STORE||m229_w9989": {"n_episodes": 2, "hist": {
            "1": {"WOOL": {"qty_sum": 12, "count": 3, "qty_max": 6}}}},
        "BAKERY,YARN_STORE||229.0:9989": {"n_episodes": 9, "hist": {
            "1": {"MILK": {"qty_sum": 9, "count": 3, "qty_max": 4}}}}},
        "global": {}}
    out = predict_block.match_sellflow(o50, lib2)
    m = out["matches"]
    assert m["key"] == "BAKERY,YARN_STORE||229.0:9989" and m["source"] == "key"
    assert set(m["items"]) == {"MILK"}
    assert out["top1"]["key"] == "BAKERY,YARN_STORE||229.0:9989"
    assert out["top1"]["adopted"] is True

    # ③历史置信门（远端 1-4 回合信号）两分支：条目带 history_hits/hit_rate，
    #   ≥3 且 ≥0.70（含界）才采纳；否则 skipped、置信 0、不 fire。
    def _gated(hits, rate):
        return {"version": "t", "global": {}, "keys": {
            "BAKERY,YARN_STORE||229.0:9989": {
                "n_episodes": 5, "history_hits": hits, "hit_rate": rate,
                "hist": {"1": {"MILK": {"qty_sum": 9, "count": 3,
                                        "qty_max": 4}}}}}}

    out = predict_block.match_sellflow(o50, _gated(3, 0.70))
    assert out["matches"]["source"] == "key"
    assert out["matches"]["skipped"] is False
    assert out["top1"]["adopted"] is True and out["confidence"] > 0
    for hits, rate in ((2, 0.90), (3, 0.69)):
        out = predict_block.match_sellflow(o50, _gated(hits, rate))
        assert out["matches"]["source"] == "skipped"
        assert out["matches"]["items"] == {} and out["matches"]["skipped"] is True
        assert out["confidence"] == 0.0 and out["top1"]["adopted"] is False

    # ④无键→回退 library["global"]（同 hist 形聚合）且置信降一档（×0.5）。
    out = predict_block.match_sellflow(o50, {"version": "t", "keys": {},
                                             "global": lib["global"]})
    assert out["matches"]["source"] == "global" and out["top1"]["key"] is None
    assert out["matches"]["items"]["CARROT"] == {"qty_sum": 4, "count": 2, "qty_max": 2}
    assert abs(out["confidence"] - (2 / 10) * 1.0 * 0.5) < 1e-9

    # ⑤库缺失/畸形→confidence=0 不抛。
    for bad_lib in (None, {}, "bad"):
        out = predict_block.match_sellflow(o50, bad_lib)
        assert out["confidence"] == 0.0 and out["top1"]["adopted"] is False


def test_extrapolate_sells():
    """extrapolate v2 限频六道门逐项（全过才写）：①窗外 ②低于 K ③每步每品
    恰 1 单 ④带通两端 ⑤价门 ⑥噪声门 skipped；坏容器/缺账 fail-safe 不抛。"""

    def _mk(step=500, net=6, items=None, skipped=False):
        inf = {"step": step, "items": {"MILK": {"net_qty": net, "lower_bound": False}}}
        dist = {"MILK": {"qty_sum": 10, "count": 5, "qty_max": 3}} if items is None else items
        matches = {"matches": {"items": dist, "wins": [10], "source": "key",
                               "key": "k", "step": step, "skipped": skipped},
                   "confidence": 0.8,
                   "top1": {"key": "k", "source": "key", "adopted": True}}
        return inf, matches

    def _acct(stock=50, plan=30, prices=None, dump=None):
        acct = {"stock": {"MILK": stock}, "plan": {"MILK": plan},
                "prices": {"MILK": 160 if prices is None else prices}}
        if dump is not None:
            acct["dump_prices"] = {"MILK": dump}
        return acct

    def _plan(n=700):
        return [{"market": []} for _ in range(n)]

    # ①触发窗 step∈[336,646]（含界）：窗外不写。
    for off_step in (300, 335, 647, 700):
        inf, matches = _mk(step=off_step)
        plan = _plan()
        out = predict_block.extrapolate_sells(inf, matches, plan, _acct())
        assert out["written"] == []
        assert {"item": "MILK", "reason": "window"} in out["skipped"]
        assert all(s["market"] == [] for s in plan)
    for edge in (336, 646):                       # 含界两头开火
        inf, matches = _mk(step=edge)
        out = predict_block.extrapolate_sells(inf, matches, _plan(), _acct())
        assert out["written"] == [{"item": "MILK", "qty": 30, "tier": "中"}]

    # ②开火门槛：近 2 回合 TOP-1 预测净卖=2×pred<K=4 不写。
    inf, matches = _mk(net=1)                     # 2×1=2<4
    out = predict_block.extrapolate_sells(inf, matches, _plan(), _acct())
    assert out["written"] == []
    assert {"item": "MILK", "reason": "below_k"} in out["skipped"]
    inf2 = {"step": 500, "items": {"MILK": {"net_qty": 0, "lower_bound": False}}}
    _, matches2 = _mk(items={"MILK": {"qty_sum": 2, "count": 2, "qty_max": 1}})
    out = predict_block.extrapolate_sells(inf2, matches2, _plan(), _acct())
    assert {"item": "MILK", "reason": "below_k"} in out["skipped"]

    # ③每步每品恰 1 单：槽位已有该品 SELL 单→该步位跳过不堆单。
    plan = _plan()
    plan[501]["market"] = [["SELL", "MILK", 7]]
    inf, matches = _mk()
    out = predict_block.extrapolate_sells(inf, matches, plan, _acct(stock=20, plan=30))
    assert plan[501]["market"] == [["SELL", "MILK", 7]]      # 恰 1 单零堆单
    assert plan[502]["market"] == [["SELL", "MILK", 20]]
    assert {"item": "MILK", "reason": "dup"} in out["skipped"]

    # ④量级带通 4≤qty≤99（qty=min(棚存, 48h 计划)）：两端拒绝、含界放行。
    for stock, plan_q, ok_qty in ((3, 3, None), (2, 50, None), (120, 120, None),
                                  (4, 4, 4), (99, 99, 99)):
        inf, matches = _mk()
        out = predict_block.extrapolate_sells(
            inf, matches, _plan(), _acct(stock=stock, plan=plan_q))
        if ok_qty is None:
            assert out["written"] == []
            assert {"item": "MILK", "reason": "band"} in out["skipped"]
        else:
            assert out["written"] == [{"item": "MILK", "qty": ok_qty,
                                       "tier": "少" if ok_qty < 20 else "多"}]

    # ⑤价门（min_sell_price=2 + base 价门）：预测倾销价<base→price、<2→floor。
    inf, matches = _mk()
    out = predict_block.extrapolate_sells(inf, matches, _plan(), _acct(dump=150))
    assert out["written"] == []
    assert {"item": "MILK", "reason": "price"} in out["skipped"]
    out = predict_block.extrapolate_sells(inf, matches, _plan(), _acct(dump=1.5))
    assert {"item": "MILK", "reason": "price"} in out["skipped"]   # <base 先拦
    out = predict_block.extrapolate_sells(
        inf, matches, _plan(), _acct(prices=1, dump=1.5))          # base≤价<2
    assert {"item": "MILK", "reason": "floor"} in out["skipped"]
    out = predict_block.extrapolate_sells(inf, matches, _plan(), _acct(dump=160))
    assert out["written"] == [{"item": "MILK", "qty": 30, "tier": "中"}]

    # ⑥噪声门：matches.skipped（远端未过历史门）→不写。
    inf, matches = _mk(skipped=True)
    out = predict_block.extrapolate_sells(inf, matches, _plan(), _acct())
    assert out["written"] == []
    assert {"item": "MILK", "reason": "noise"} in out["skipped"]

    # fail-safe：缺账（棚存/计划量/基价取不到）与坏容器不写不抛。
    inf, matches = _mk()
    for acct in ({}, {"stock": {"MILK": 50}}, {"plan": {"MILK": 30}},
                 {"stock": {"MILK": 50}, "plan": {"MILK": 30}}):
        out = predict_block.extrapolate_sells(inf, matches, _plan(), acct)
        assert out["written"] == []
        assert {"item": "MILK", "reason": "no_account"} in out["skipped"]
    out = predict_block.extrapolate_sells(inf, matches, _plan())
    assert out["written"] == []
    assert predict_block.extrapolate_sells(inf, matches, {"bad": 1},
                                           _acct())["written"] == []
    out = predict_block.extrapolate_sells(inf, matches, [{"market": []}], _acct())
    assert out["written"] == [] and out["skipped"]


def test_extrapolate_sells_tier_and_credit():
    """extrapolate v2 量级档（少<20/中 20-60/多>60）+credit 减记与禁净加卖。"""

    def _mk(step=500, net=6):
        inf = {"step": step, "items": {"MILK": {"net_qty": net, "lower_bound": False}}}
        matches = {"matches": {"items": {"MILK": {"qty_sum": 10, "count": 5,
                                                  "qty_max": 3}},
                               "wins": [10], "source": "key", "key": "k",
                               "step": step, "skipped": False},
                   "confidence": 0.8,
                   "top1": {"key": "k", "source": "key", "adopted": True}}
        return inf, matches

    # 量级档三档按 qty 分档：15→少、45→中、80→多。
    for qty, tier in ((15, "少"), (45, "中"), (80, "多")):
        acct = {"stock": {"MILK": qty}, "plan": {"MILK": qty},
                "prices": {"MILK": 160}}
        plan = [{"market": []} for _ in range(700)]
        inf, matches = _mk()
        out = predict_block.extrapolate_sells(inf, matches, plan, acct)
        assert out["written"] == [{"item": "MILK", "qty": qty, "tier": tier}]

    # credit 减记：每写一单按 qty 扣减该品自家后续计划卖量（30→0，只写一单）。
    acct = {"stock": {"MILK": 50}, "plan": {"MILK": 30}, "prices": {"MILK": 160}}
    plan = [{"market": []} for _ in range(700)]
    inf, matches = _mk()
    out = predict_block.extrapolate_sells(inf, matches, plan, acct)
    assert out["written"] == [{"item": "MILK", "qty": 30, "tier": "中"}]
    assert out["credit_debited"] == [{"item": "MILK", "step": 501, "qty": 30}]
    assert acct["plan"] == {"MILK": 0}                # 减记落账
    assert plan[502]["market"] == []                  # credit 耗尽不再写

    # 禁净加卖：累计写量 ≤ 计划量（100 计划/50 棚存→50+50 两单封顶）。
    acct = {"stock": {"MILK": 50}, "plan": {"MILK": 100}, "prices": {"MILK": 160}}
    plan = [{"market": []} for _ in range(700)]
    out = predict_block.extrapolate_sells(inf, matches, plan, acct)
    assert [w["qty"] for w in out["written"]] == [50, 50]
    assert sum(w["qty"] for w in out["written"]) == 100 <= 100
    assert acct["plan"] == {"MILK": 0}
    assert len(out["credit_debited"]) == 2

    # credit 为负不再写（禁净加卖反例）。
    acct = {"stock": {"MILK": 50}, "plan": {"MILK": -5}, "prices": {"MILK": 160}}
    plan = [{"market": []} for _ in range(700)]
    out = predict_block.extrapolate_sells(inf, matches, plan, acct)
    assert out["written"] == []
    assert {"item": "MILK", "reason": "no_credit"} in out["skipped"]
    assert all(s["market"] == [] for s in plan)


def test_apply_dodge():
    """dodge v2=门：预测倾销价<base→deny/否则 allow 两分支；**action 原样零
    改动**（反例钉住 v1 顺延置 []/减量语义已删）；异常→全 allow+原动作。"""
    obs = _obs(50, inv={"MILK": 500}, prices={"MILK": 160, "WOOL": 200, "WHEAT": 25})
    act = _act([["BUY_SEED", "WHEAT", 1], ["SELL", "MILK", 3], ["SELL", "WOOL", 5], []],
               farmer=["HARVEST"], hands=[["FEED"], ["CARE"]])

    # ①门判定两分支：倾销价 120<base 160→deny；200/160（含界）→allow。
    out = predict_block.apply_dodge(obs, act, {"prices": {"MILK": 120, "WOOL": 200}})
    assert out["gates"] == {"MILK": "deny", "WOOL": "allow"}
    out = predict_block.apply_dodge(obs, act, {"prices": {"MILK": 160}})
    assert out["gates"] == {"MILK": "allow"}
    out = predict_block.apply_dodge(obs, act, {
        "sells": [{"item": "MILK", "qty": 9, "price": 159.9}]})
    assert out["gates"] == {"MILK": "deny"}

    # ②action 原样零改动反例：预测集中抛售（v1 会顺延/减量）也一字不动。
    out = predict_block.apply_dodge(obs, act, {"confidence": 0.9, "sells": [
        {"item": "MILK", "qty": 5, "steps": [51, 52], "price": 100},
        {"item": "WOOL", "qty": 3, "steps": [51], "price": 300}]})
    assert out["action"] is act                       # 同对象零改动
    assert act["market"] == [["BUY_SEED", "WHEAT", 1], ["SELL", "MILK", 3],
                             ["SELL", "WOOL", 5], []]
    assert out["gates"] == {"MILK": "deny", "WOOL": "allow"}

    # ③异常→全 allow+原动作（predictions 畸形/observation 非 dict 不抛）。
    out = predict_block.apply_dodge(obs, act, {"confidence": "bad", "prices": "bad",
                                               "sells": [{"item": "MILK"}]})
    assert out["action"] is act
    assert out["gates"] == {"MILK": "allow"}
    for bad_obs in (None, "bad", ["not-a-dict"]):
        out = predict_block.apply_dodge(bad_obs, act, {"prices": {"MILK": 1}})
        assert out["action"] is act
        assert out["gates"] == {"MILK": "allow"}
    out = predict_block.apply_dodge(obs, ["not-a-dict"], {"prices": {"MILK": 100}})
    assert out["action"] == ["not-a-dict"]             # 非 dict 动作也原样零改动
    assert out["gates"] == {"MILK": "deny"}
    out = predict_block.apply_dodge(obs, act, None)
    assert out["action"] is act and out["gates"] == {}


def test_predict_agent(monkeypatch):
    """入口 v2：非克隆→父层动作原样（全链零动作零写入）；克隆→走链
    （detect_clone→infer→match→extrapolate credit 减记）；step0 复位全账。"""
    calls = []
    sentinel = _act([["SELL", "WOOL", 1]])
    actions = {500: sentinel}

    def _fake_parent(observation):
        calls.append(observation)
        return actions.get(observation["step"], _act([]))

    monkeypatch.setattr(predict_block, "_PREDICT_PARENT", _fake_parent,
                        raising=False)
    lib = {"version": "t", "keys": {
        "BAKERY|YARN_STORE||m229_w9989": {"n_episodes": 8, "hist": {
            "10": {"MILK": {"qty_sum": 20, "count": 10, "qty_max": 6}}}}},
        "global": {}}
    monkeypatch.setattr(predict_block, "_PREDICT_LIBRARY", lib, raising=False)
    shops = ["BAKERY", "YARN_STORE"]

    # ①假父层注入 + 非克隆→父层动作原样，全链零动作零写入（plan/credit 不动）。
    predict_block._predict_agent._opponent_plan = []
    predict_block._predict_agent._credit = {"plan": {"MILK": 7}}
    o500 = _obs(500, inv={"WHEAT": 9989}, prices={"WHEAT": 25}, shops=shops,
                money=(210.0, 250.0))
    out = predict_block._predict_agent(o500)
    assert calls[-1] is o500                      # 假父层被调、观测原样传入
    assert out is sentinel                        # 非克隆零动作
    assert predict_block._predict_agent._opponent_plan == []
    assert predict_block._predict_agent._credit == {"plan": {"MILK": 7}}

    # ②克隆走链：step 499 播种推断账 → step 500 差分对手净卖 MILK 6（精确）
    #   → match TOP-1 命中置信 1.0 → extrapolate 六门全过写 plan[501]（量级档
    #   中）+credit 减记 30→0 → dodge 门 allow → 父层动作原样返回。
    predict_block.detect_clone._stream = {"agree": 20, "total": 20}  # 相似度 1.0
    predict_block._predict_agent._credit = {"plan": {"MILK": 30}}
    predict_block.infer_rival_sells(
        _obs(499, inv={"WHEAT": 9989, "MILK": 500},
             prices={"MILK": 160, "WHEAT": 25}, shops=shops, shed={"MILK": 50}),
        None)                                     # 播种 step-499 快照
    o500b = _obs(500, inv={"WHEAT": 9989, "MILK": 506},
                 prices={"MILK": 160, "WHEAT": 25}, shops=shops, shed={"MILK": 50})
    out = predict_block._predict_agent(o500b)
    assert out is sentinel                        # 门不改动作：父层动作原样
    plan = predict_block._predict_agent._opponent_plan
    assert plan[501]["market"] == [["SELL", "MILK", 30]]
    assert predict_block._predict_agent._credit["plan"] == {"MILK": 0}
    assert predict_block._predict_agent._written == [
        {"item": "MILK", "qty": 30, "tier": "中"}]
    assert predict_block._predict_agent._dodge_log == [
        {"item": "MILK", "gate": "allow"}]

    # ③step0 复位全账（推断账/身份/相似度快照/plan/credit/自家账/门账）。
    predict_block.infer_rival_sells._ledger = {"junk": True}
    predict_block.match_sellflow._identity = {"step": 500, "money": 0, "wheat": 0}
    predict_block.detect_clone._stream = {"agree": 9, "total": 9}
    predict_block._predict_agent._own_fills = {"sell": {"WHEAT": 9}}
    predict_block._predict_agent._dodge_log = [{"junk": 1}]
    old_plan = [{"market": [["SELL", "MILK", 1]]}] * 5
    predict_block._predict_agent._opponent_plan = old_plan
    predict_block._predict_agent._credit = {"plan": {"MILK": 5}, "junk": True}
    predict_block._predict_agent._written = [{"junk": 1}]
    out = predict_block._predict_agent(
        _obs(0, inv={"WHEAT": 9989}, prices={"WHEAT": 25}, shops=shops))
    assert out == _act([])
    assert getattr(predict_block.infer_rival_sells, "_ledger", None) is None
    assert getattr(predict_block.match_sellflow, "_identity", None) is None
    assert getattr(predict_block.detect_clone, "_stream", None) is None
    assert predict_block._predict_agent._own_fills == {"sell": {}, "buy": {},
                                                       "floor_sells": {}}
    assert predict_block._predict_agent._dodge_log == []
    assert predict_block._predict_agent._opponent_plan == []
    assert predict_block._predict_agent._credit == {}
    assert predict_block._predict_agent._written == []


def test_predict_agent_deny_rollback_and_failsafe(monkeypatch):
    """入口 v2：deny 品 written 条目作废+plan 钩子单回滚+credit 回滚；链中异常
    →父层动作原样；父层抛→PASS 兜底。"""
    sentinel = _act([["SELL", "WOOL", 1]])
    actions = {500: sentinel}

    def _fake_parent(observation):
        return actions.get(observation["step"], sentinel)

    monkeypatch.setattr(predict_block, "_PREDICT_PARENT", _fake_parent,
                        raising=False)
    lib = {"version": "t", "keys": {
        "BAKERY|YARN_STORE||m229_w9989": {"n_episodes": 8, "hist": {
            "10": {"MILK": {"qty_sum": 20, "count": 10, "qty_max": 6}}}}},
        "global": {}}
    monkeypatch.setattr(predict_block, "_PREDICT_LIBRARY", lib, raising=False)
    shops = ["BAKERY", "YARN_STORE"]

    # deny 回滚：传入账 base 覆盖 100+倾销价 150 → extrapolate 过价门写入；
    # dodge 以 obs 市场价 base 160 判 150<160 → deny → 全链回滚。
    predict_block.detect_clone._stream = {"agree": 20, "total": 20}
    predict_block.infer_rival_sells(
        _obs(499, inv={"WHEAT": 9989, "MILK": 500},
             prices={"MILK": 160, "WHEAT": 25}, shops=shops, shed={"MILK": 50}),
        None)
    predict_block._predict_agent._credit = {"plan": {"MILK": 30},
                                            "prices": {"MILK": 100},
                                            "dump_prices": {"MILK": 150}}
    out = predict_block._predict_agent(
        _obs(500, inv={"WHEAT": 9989, "MILK": 506},
             prices={"MILK": 160, "WHEAT": 25}, shops=shops, shed={"MILK": 50}))
    assert out is sentinel                        # 动作零改动
    plan = predict_block._predict_agent._opponent_plan
    assert plan[501]["market"] == []              # 钩子单已回滚
    assert plan[502]["market"] == []
    assert predict_block._predict_agent._credit["plan"] == {"MILK": 30}
    assert predict_block._predict_agent._written == []      # written 条目作废
    assert predict_block._predict_agent._dodge_log == [
        {"item": "MILK", "gate": "deny"}]

    # 异常 fail-safe：链中 infer 抛→父层动作原样；父层抛→PASS 兜底。
    real_infer = predict_block.infer_rival_sells

    def _boom(observation):
        raise RuntimeError("chain broke")

    monkeypatch.setattr(predict_block, "infer_rival_sells", _boom)
    out = predict_block._predict_agent(
        _obs(510, inv={"WHEAT": 9989}, prices={"WHEAT": 25}, shops=shops))
    assert out is sentinel
    monkeypatch.setattr(predict_block, "infer_rival_sells", real_infer)

    def _bad_parent(observation):
        raise RuntimeError("parent broke")

    monkeypatch.setattr(predict_block, "_PREDICT_PARENT", _bad_parent,
                        raising=False)
    out = predict_block._predict_agent(_obs(511))
    assert out == {"farmer": ["PASS"], "hands": [], "market": []}


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


def test_detect_clone():
    """clone 组（R22 改3/改4 门）：step1 现金差 <$0.5（严格）/相似度 ≥0.95
    （含界）/缺字段与异常保守非克隆；跨步快照=函数属性 detect_clone._stream
    可注入自包含。"""

    def _reset():
        try:
            delattr(predict_block.detect_clone, "_stream")
        except AttributeError:
            pass

    # ①step1 现金镜像：与自家差 <$0.5 判克隆；0.5 边界（含）与超差→不 fire；
    #   非 step1 拍不走现金规则。
    _reset()
    out = predict_block.detect_clone(_obs(1, money=(210.0, 210.3)))
    assert out["is_clone"] is True and out["evidence"]["trigger"] == "cash"
    assert out["evidence"]["cash_diff"] == pytest.approx(0.3)
    _reset()
    out = predict_block.detect_clone(_obs(1, money=(210.0, 210.5)))
    assert out["is_clone"] is False and out["evidence"]["trigger"] is None
    _reset()
    assert predict_block.detect_clone(
        _obs(1, money=(210.0, 211.0)))["is_clone"] is False
    _reset()
    assert predict_block.detect_clone(
        _obs(2, money=(210.0, 210.3)))["is_clone"] is False

    # ②行为相似度：近 N=10 步动作流一致率 ≥0.95（含界）判克隆，两侧钉住。
    _reset()
    predict_block.detect_clone._stream = {"agree": 19, "total": 20}
    out = predict_block.detect_clone(_obs(5, money=(210.0, 250.0)))
    assert out["similarity"] == pytest.approx(0.95) and out["is_clone"] is True
    assert out["evidence"]["trigger"] == "similarity"
    _reset()
    predict_block.detect_clone._stream = {"agree": 18, "total": 20}
    out = predict_block.detect_clone(_obs(5, money=(210.0, 250.0)))
    assert out["similarity"] == pytest.approx(0.9) and out["is_clone"] is False
    # 真喂动作流：10 步全同 → 1.0 判克隆；错 1 步（window 截近 10 步）→ 0.9 不判。
    _reset()
    for s in range(10, 20):
        o = _obs(s, money=(210.0, 250.0))
        o["farms"][0]["action"] = ["SELL", "MILK", 3]
        o["farms"][1]["action"] = ["SELL", "MILK", 3]
        out = predict_block.detect_clone(o)
    assert out["similarity"] == pytest.approx(1.0) and out["is_clone"] is True
    _reset()
    for s in range(10, 21):
        o = _obs(s, money=(210.0, 250.0))
        o["farms"][0]["action"] = ["SELL", "MILK", 3]
        o["farms"][1]["action"] = ["SELL", "MILK", 3 if s < 20 else 4]
        out = predict_block.detect_clone(o)
    assert out["similarity"] == pytest.approx(0.9) and out["is_clone"] is False

    # ③缺字段保守：任一必需字段缺失/畸形→非克隆（不 fire）。
    _reset()
    assert predict_block.detect_clone(
        {"step": 1, "player": 0})["is_clone"] is False
    assert predict_block.detect_clone(
        {"step": 1, "player": 0, "farms": [{"money": 210.0}]})["is_clone"] is False
    o = _obs(1, money=(210.0, 210.0))
    o["farms"][1].pop("money")  # 缺对手 money：即使现金差本可命中也保守不 fire
    assert predict_block.detect_clone(o)["is_clone"] is False
    o = _obs(1, money=(210.0, 210.0))
    o.pop("player")
    assert predict_block.detect_clone(o)["is_clone"] is False
    _reset()  # 无动作字段且无缓存 → similarity 0 不 fire
    out = predict_block.detect_clone(_obs(5, money=(210.0, 250.0)))
    assert out["is_clone"] is False and out["similarity"] == 0.0

    # ④异常→非克隆不抛。
    for bad in (None, "bad", 42, {"step": 1, "player": 0, "farms": "bad"}):
        assert predict_block.detect_clone(bad) == {
            "is_clone": False, "similarity": 0.0, "evidence": {}}
    _reset()
