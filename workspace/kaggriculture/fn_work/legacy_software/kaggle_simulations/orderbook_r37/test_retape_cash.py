# -*- coding: utf-8 -*-
"""R19/R20 测试面：retape_cash_reserve（d0 现金留存磁带手术）。

用例面（用户裁决 2026-09-26 源头补丁·测试①②③④⑥；⑤audit 新类归因在
test_build_r37.py audit 组）：
①构造小磁带（d0 种子单+远期 PLANT）→买点后移且供种链完好（种子到达不晚于
  PLANT 需要、PICKUP/PLANT/收成链零改动、源槽换 [] 尾部追加、输入零改动）；
②依赖消费过近→no-op 留档（零改动、reason 记候选判定）；
③断供种链/越 624 即抛（monkeypatch 落点制造违例→RuntimeError）；
④d0 日终 ≥5 核算（守卫投影口径静态近似：HIRE fib/种子畜精确扣减、卖单
  收入计入；手术逐笔挪动直至推算 ≥5）；
⑥真 r34a 实跑（多少路由动了/每路由 change_table 摘要）记
  evidence/retape_cash_realrun.json（确定性双跑、逐路由留档）。
"""
import copy
import hashlib
import json
from pathlib import Path

import pytest

try:
    from orderbook_r37 import retape_cash as RC
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
    import retape_cash as RC

try:
    from orderbook_r37 import retape_sheep as _rs
except ImportError:
    import retape_sheep as _rs


# ---------------------------------------------------------------------------
# 夹具：迷你磁带构造（actions 池+单路由逐步指针，写时复制口径）
# ---------------------------------------------------------------------------
def _mk_pkg(steps, market_at=None, farmer_at=None, hands_at=None):
    """步骤数 steps 的单路由磁带包（其余步空转）。

    market_at/farmer_at/hands_at: {step: 值}；hands_at[step]=[指令列表...]。
    """
    market_at = market_at or {}
    farmer_at = farmer_at or {}
    hands_at = hands_at or {}
    actions = []
    for s in range(steps):
        actions.append({
            "farmer": list(farmer_at.get(s, ["PASS"])),
            "hands": [list(h) for h in hands_at.get(s, [])],
            "market": [list(o) for o in market_at.get(s, [])],
        })
    return {"actions": actions, "routes": {"0": list(range(steps))},
            "shops": []}


def _by_kind(rows, kind):
    return [r for r in rows if r["kind"] == kind]


# ---------------------------------------------------------------------------
# ① d0 种子单+远期 PLANT → 买点后移且供种链完好
# ---------------------------------------------------------------------------
def test_retape_cash_moves_buy_before_far_plant():
    # d0 开销 3030（MELON 1@2=80 + SHEEP 5@5=2500 + COW 1@5=400 + WHEAT 5@6=50）
    # → 推算 d0 日终 -30 <5；候选= MELON@2（依赖消费=step 100 远期 PLANT，可挪）
    # 与 WHEAT@6（消费@7 过近，紧迫）。手术只挪 MELON@2→99（依赖消费前最近
    # 可行拍=同日/前一日窗内 72..99 的最大可行拍），推算 -30+80=50 ≥5 达线停。
    pkg = _mk_pkg(
        130,
        market_at={
            2: [["BUY_SEED", "MELON", 1]],
            5: [["BUY_ANIMAL", "SHEEP", 5], ["BUY_ANIMAL", "COW", 1]],
            6: [["BUY_SEED", "WHEAT", 5]],
        },
        farmer_at={7: ["PLANT", "WHEAT"], 100: ["PLANT", "MELON"]},
    )
    before = copy.deepcopy(pkg)
    out = RC.retape_cash_reserve(pkg)

    # 输入零改动（写时复制）
    assert pkg == before
    rows = out["change_table"]
    moves = _by_kind(rows, "cash_reserve_buy_move")
    assert [(r["from_step"], r["to_step"], r["item"], r["qty"]) for r in moves] \
        == [(2, 99, "MELON", 1)]
    assert not _by_kind(rows, "no-op")            # 达线即停不再留 no-op

    new = out["routes"]
    seq = [new["actions"][i] for i in new["routes"]["0"]]
    # 供种链完好：源槽换 [] 占位、目标步尾部追加、PICKUP/PLANT/收成链零改动
    assert seq[2]["market"] == [[]]
    assert seq[99]["market"][-1] == ["BUY_SEED", "MELON", 1]
    assert seq[100]["farmer"] == ["PLANT", "MELON"]
    assert seq[7]["farmer"] == ["PLANT", "WHEAT"]
    assert seq[6]["market"] == [["BUY_SEED", "WHEAT", 5]]      # 别类单零改动
    assert seq[5]["market"] == [["BUY_ANIMAL", "SHEEP", 5],
                                ["BUY_ANIMAL", "COW", 1]]
    # 种子到达不晚于需要：移后买点 99 < 依赖消费 100（市场结算后一拍可用）
    assert moves[0]["to_step"] < 100
    # 订单槽位守恒语义：既有槽位（含空槽）不删不移不填，仅尾部追加
    assert len(seq[2]["market"]) == len(before["actions"][2]["market"])
    assert len(seq[99]["market"]) == len(before["actions"][99]["market"]) + 1
    # 达线核算：推算 d0 日终 ≥5（reason 自带推算值）
    assert RC._project_d0_end(seq) >= RC.D0_CASH_FLOOR
    assert "-30.0→50.0" in moves[0]["reason"]


# ---------------------------------------------------------------------------
# ② 依赖消费过近 → no-op 留档（零改动）
# ---------------------------------------------------------------------------
def test_retape_cash_noop_when_consumption_near():
    # 推算 d0 日终 -10 <5，但窗内两张种子单的依赖消费都在 d0 窗内（7/10）
    # → 保守判定全紧迫 → 零改动 no-op 留档。
    pkg = _mk_pkg(
        40,
        market_at={
            5: [["BUY_ANIMAL", "COW", 7]],
            6: [["BUY_SEED", "MELON", 2]],
            9: [["BUY_SEED", "WHEAT", 5]],
        },
        farmer_at={7: ["PLANT", "MELON"], 10: ["PLANT", "WHEAT"]},
    )
    before = copy.deepcopy(pkg)
    out = RC.retape_cash_reserve(pkg)
    assert pkg == before
    assert out["routes"] == before                 # 零改动
    rows = out["change_table"]
    assert len(rows) == 1
    row = rows[0]
    assert row["kind"] == "no-op" and row["item"] is None and row["qty"] == 0
    assert "no feasible candidate" in row["reason"]
    assert "紧迫" in row["reason"] and "运行时守卫兜底" in row["reason"]
    # 窗内无种子单的形态同样 no-op 留档
    empty = _mk_pkg(30, market_at={5: [["BUY_ANIMAL", "COW", 1]]})
    out2 = RC.retape_cash_reserve(empty)
    assert len(out2["change_table"]) == 1
    assert out2["change_table"][0]["kind"] == "no-op"
    assert "窗内种子单 0 张" in out2["change_table"][0]["reason"]


# ---------------------------------------------------------------------------
# ③ 断供种链/越 624 即抛
# ---------------------------------------------------------------------------
def test_retape_cash_raises_on_chain_break_or_deadline(monkeypatch):
    # 700 步磁带（落点可越 624 才能进术后核算；勾选落点由 monkeypatch 造违例）
    pkg = _mk_pkg(
        700,
        market_at={2: [["BUY_SEED", "MELON", 1]],
                   5: [["BUY_ANIMAL", "SHEEP", 5], ["BUY_ANIMAL", "COW", 1]],
                   6: [["BUY_SEED", "WHEAT", 5]]},
        farmer_at={7: ["PLANT", "WHEAT"], 100: ["PLANT", "MELON"]},
    )
    # 断供种链：落点被造到依赖消费拍（种子到达晚于 PLANT 需要）→ 抛
    monkeypatch.setattr(RC, "_pick_landing",
                        lambda seq, from_step, consumption: consumption)
    with pytest.raises(RuntimeError, match="断供种链"):
        RC.retape_cash_reserve(copy.deepcopy(pkg))
    # 越种植截止线：落点被造到 625 → 抛
    monkeypatch.setattr(RC, "_pick_landing",
                        lambda seq, from_step, consumption: 625)
    with pytest.raises(RuntimeError, match="越种植截止线"):
        RC.retape_cash_reserve(copy.deepcopy(pkg))
    # 常量口径钉：种植截止线=624（EXP402/layer S 同源）
    assert RC.PLANTING_DEADLINE == 624


# ---------------------------------------------------------------------------
# ④ d0 日终 ≥5 核算（守卫投影口径静态近似）
# ---------------------------------------------------------------------------
def test_retape_cash_d0_end_accounting():
    # 投影口径逐项核：HIRE fib（1,1,2…）、种子/畜精确扣减、BUY_PRODUCT base
    # 扣减、卖单收入 base 计入、钱起点 3000。
    seq = _mk_pkg(
        30,
        market_at={1: [["HIRE"], ["HIRE"], ["BUY_SEED", "MELON", 1],
                       ["BUY_ANIMAL", "SHEEP", 1]],
                   2: [["BUY_PRODUCT", "WHEAT", 4], ["SELL", "WOOL", 2]]},
    )["actions"]
    # 3000 - (1+1) - 80 - 500 - 4*25 + 2*200 = 2718.0
    assert RC._project_d0_end(seq) == 2718.0

    # 手术核算面：d0 开销 3090（MELON 2@2=160 + MELON 1@3=80 + COW 7@5=2800
    # + WHEAT 5@6=50）→ 推算 -90；两笔 MELON 可挪（消费@100），逐笔挪动
    # （MELON 优先、依赖消费同拍取买点更靠后者先挪）直至推算 ≥5：-90+80+160=150。
    pkg = _mk_pkg(
        130,
        market_at={2: [["BUY_SEED", "MELON", 2]],
                   3: [["BUY_SEED", "MELON", 1]],
                   5: [["BUY_ANIMAL", "COW", 7]],
                   6: [["BUY_SEED", "WHEAT", 5]]},
        farmer_at={7: ["PLANT", "WHEAT"], 100: ["PLANT", "MELON"]},
    )
    out = RC.retape_cash_reserve(pkg)
    moves = _by_kind(out["change_table"], "cash_reserve_buy_move")
    assert [(r["from_step"], r["to_step"], r["item"], r["qty"]) for r in moves] \
        == [(3, 99, "MELON", 1), (2, 99, "MELON", 2)]
    seq2 = [out["routes"]["actions"][i] for i in out["routes"]["routes"]["0"]]
    projected = RC._project_d0_end(seq2)
    assert projected == 150.0 and projected >= RC.D0_CASH_FLOOR
    assert not _by_kind(out["change_table"], "no-op")


# ---------------------------------------------------------------------------
# ⑥ 真 r34a 实跑（多少路由动了/每路由 change_table 摘要）→ evidence 留档
# ---------------------------------------------------------------------------
def test_retape_cash_realrun_evidence():
    r34a = (Path(__file__).resolve().parent.parent
            / "orderbook_2965_adopt" / "a" / "main.py")
    text = r34a.read_text(encoding="utf-8")
    pkg = _rs._decode_routes(text)
    before = copy.deepcopy(pkg)
    out = RC.retape_cash_reserve(pkg)
    out2 = RC.retape_cash_reserve(pkg)
    assert pkg == before                          # 输入零改动
    # 确定性双跑：变更表逐字节一致
    assert json.dumps(out["change_table"], sort_keys=True) \
        == json.dumps(out2["change_table"], sort_keys=True)

    routes = sorted(out["routes"]["routes"], key=lambda k: int(k))
    assert len(routes) == 41
    per_route = []
    n_moved = 0
    for rid in routes:
        rows = [r for r in out["change_table"] if r["route"] == rid]
        moves = _by_kind(rows, "cash_reserve_buy_move")
        n_moved += 1 if moves else 0
        for r in rows:
            assert set(r) == {"route", "kind", "from_step", "to_step",
                              "item", "qty", "reason"}
            assert r["kind"] in ("cash_reserve_buy_move", "no-op")
        per_route.append({
            "route": rid,
            "n_moves": len(moves),
            "rows": [{"kind": r["kind"], "from_step": r["from_step"],
                      "to_step": r["to_step"], "item": r["item"],
                      "qty": r["qty"], "reason": r["reason"]} for r in rows],
        })
    # 逐路由恰一行留档（move 或 no-op）；真 r34a 磁带 d0 窗为零余量买即种
    # 流水线（每张种子单依赖消费=后 1-2 拍且在 d0 窗内），保守规则下应为
    # 全程 no-op（多少路由动了以台账为准，此处钉形态不钉数量）。
    assert all(len(p["rows"]) >= 1 for p in per_route)

    evidence = {
        "generated_by": "orderbook_r37/test_retape_cash.py::"
                        "test_retape_cash_realrun_evidence",
        "source": str(r34a),
        "source_sha256": hashlib.sha256(
            r34a.read_bytes()).hexdigest(),
        "accounting": {
            "start_money": RC.START_MONEY,
            "floor": RC.D0_CASH_FLOOR,
            "planting_deadline": RC.PLANTING_DEADLINE,
            "projected_d0_end_route0": RC._project_d0_end(
                [pkg["actions"][i] for i in pkg["routes"]["0"]]),
        },
        "n_routes": len(routes),
        "n_routes_moved": n_moved,
        "per_route": per_route,
    }
    out_path = Path(__file__).resolve().parent / "evidence" \
        / "retape_cash_realrun.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=1)
                        + "\n", encoding="utf-8")
    saved = json.loads(out_path.read_text(encoding="utf-8"))
    assert saved["n_routes_moved"] == n_moved
    assert saved["per_route"] == per_route
