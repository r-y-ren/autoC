# -*- coding: utf-8 -*-
"""R23 测试面：retape_lots（卖单批量化/卖出守恒）。

组内六件：①同品 3 单并 1 单（同拍并单缺省参数+跨拍批量化 max_orders_target=1）
+守恒核算过 / ②守恒破即抛 / ③窗外不动反例 / ④非卖单不动反例 / ⑤空槽位次不变 /
⑥真 r37 实跑（evidence/retape_lots_realrun.json）。另补越窗/参数越界即抛两件
（契约「越窗/守恒破→抛」成对覆盖）。
"""
import copy
import json
import statistics as st
from pathlib import Path

import pytest  # noqa: F401

try:
    from orderbook_r40 import retape_lots
except ImportError:  # 兜底：直接以 orderbook_r40/ 为 sys.path 根跑测
    import retape_lots
try:
    from orderbook_r37 import retape_sheep as _rs
except ImportError:
    import retape_sheep as _rs  # type: ignore

N_STEPS = 719
W0, W1 = 504, 672          # d21-28 窗（缺省 window）


def _mk_pkg(sells=(), others=(), units=(), n_steps=N_STEPS):
    """小磁带构造（_decode_routes 同形包）：sells=[(step,slot,item,qty)]，
    others=[(step,slot,order)]，units=[(step,'farmer'|'hands',op)]。"""
    markets = {}
    fields = {}

    def _put(step, slot, order):
        m = markets.setdefault(step, {})
        assert slot not in m, "测试构造槽位重复: (%d,%d)" % (step, slot)
        m[slot] = order

    for (s, slot, item, qty) in sells:
        _put(s, slot, ["SELL", item, qty])
    for (s, slot, order) in others:
        _put(s, slot, list(order))
    for (s, field, op) in units:
        fields.setdefault(s, {})[field] = copy.deepcopy(op)
    actions = []
    for s in range(n_steps):
        m = markets.get(s, {})
        width = (max(m) + 1) if m else 0
        act = {"farmer": ["PASS"], "hands": [], "market": [m.get(j, [])
                                                           for j in range(width)]}
        act.update(fields.get(s, {}))
        actions.append(act)
    return {"actions": actions, "routes": {"0": list(range(n_steps))},
            "shops": []}


def _view(pkg, rid="0"):
    return [pkg["actions"][i] for i in pkg["routes"][rid]]


def _sells(seq, lo, hi):
    return [(s, o) for s in range(lo, min(hi, len(seq)))
            for o in seq[s]["market"]
            if isinstance(o, list) and o and o[0] == "SELL"]


def test_sell_lots_merge_three_to_one():
    """①d21-28 同品 3 单→1 单（跨拍+同拍两式），守恒核算过。"""
    # 跨拍批量化：3 单散于窗内，max_orders_target=1 → 并成 1 单（落点=更早步）
    pkg = _mk_pkg(sells=[(505, 0, "WOOL", 2), (520, 1, "WOOL", 3),
                         (540, 0, "WOOL", 4)])
    out = retape_lots.retape_sell_lots(pkg, {"max_orders_target": 1})
    seq = _view(out["routes"])
    assert _sells(seq, W0, W1) == [(505, ["SELL", "WOOL", 9])]
    assert retape_lots._sell_totals(seq) == {"WOOL": 9}   # 卖出守恒核算过
    rows = out["change_table"]
    assert len(rows) == 1
    assert rows[0]["kind"] == "sell_lots" and rows[0]["item"] == "WOOL"
    assert rows[0]["from_steps"] == [505, 520, 540]
    assert rows[0]["to_step"] == 505 and rows[0]["qty"] == 9
    # 同拍并单（缺省参数）：同拍同品 3 单→1 单（落点=组内最早槽）
    pkg2 = _mk_pkg(sells=[(505, 2, "WOOL", 1), (505, 0, "WOOL", 2),
                          (505, 1, "WOOL", 4)])
    out2 = retape_lots.retape_sell_lots(pkg2)             # params=None→337 口径
    seq2 = _view(out2["routes"])
    assert _sells(seq2, W0, W1) == [(505, ["SELL", "WOOL", 7])]
    assert retape_lots._sell_totals(seq2) == {"WOOL": 7}
    assert out2["change_table"][0]["from_steps"] == [505, 505, 505]


def test_sell_conservation_break_raises(monkeypatch):
    """②守恒破即抛：写入量被故障注入少 1 → 术后核算 RuntimeError。"""
    pkg = _mk_pkg(sells=[(510, 0, "WOOL", 2), (520, 0, "WOOL", 3)])
    real = retape_lots._write_lot

    def leaky(mkt, slot, item, qty):
        real(mkt, slot, item, qty - 1)                    # 破守恒：少写 1

    monkeypatch.setattr(retape_lots, "_write_lot", leaky)
    with pytest.raises(RuntimeError, match="守恒"):
        retape_lots.retape_sell_lots(pkg, {"max_orders_target": 1})


def test_out_of_window_sell_orders_untouched():
    """③窗外不动反例：窗外同拍同品单也不并（手术限 d21-28 窗），输入零改动。"""
    pkg = _mk_pkg(sells=[(480, 0, "WOOL", 2), (480, 1, "WOOL", 5),   # 窗外（d20）
                         (510, 0, "WOOL", 3), (520, 0, "WOOL", 4)])  # 窗内
    snap = copy.deepcopy(pkg)
    out = retape_lots.retape_sell_lots(pkg, {"max_orders_target": 1})
    assert pkg == snap                                    # 写时复制：输入零改动
    seq = _view(out["routes"])
    assert _sells(seq, 0, W0) == [(480, ["SELL", "WOOL", 2]),
                                 (480, ["SELL", "WOOL", 5])]
    assert _sells(seq, W0, W1) == [(510, ["SELL", "WOOL", 7])]
    assert retape_lots._sell_totals(seq) == {"WOOL": 14}  # 全带守恒


def test_non_sell_orders_and_units_untouched():
    """④非卖单不动反例：BUY_*/HIRE 与 FEED/CARE/HARVEST/移动逐槽逐拍原样。"""
    pkg = _mk_pkg(
        sells=[(510, 0, "WOOL", 2), (520, 0, "WOOL", 3)],
        others=[(510, 1, ["BUY_SEED", "WHEAT", 5]), (515, 0, ["HIRE"]),
                (520, 1, ["BUY_ANIMAL", "SHEEP", 2]),
                (521, 0, ["BUY_PRODUCT", "MILK", 1]), (530, 0, ["BUY_LAND", 1])],
        units=[(511, "farmer", ["FEED"]), (512, "hands", [["CARE"]]),
               (513, "hands", [["HARVEST"]]), (514, "farmer", ["MOVE", "NORTH"])])
    snap = copy.deepcopy(pkg)
    out = retape_lots.retape_sell_lots(pkg, {"max_orders_target": 1})
    seq, orig = _view(out["routes"]), _view(snap)
    for s in (510, 511, 512, 513, 514, 515, 520, 521, 530):
        assert seq[s].get("farmer") == orig[s].get("farmer")
        assert seq[s].get("hands") == orig[s].get("hands")
    assert seq[510]["market"][1] == ["BUY_SEED", "WHEAT", 5]
    assert seq[515]["market"][0] == ["HIRE"]
    assert seq[520]["market"][1] == ["BUY_ANIMAL", "SHEEP", 2]
    assert seq[521]["market"][0] == ["BUY_PRODUCT", "MILK", 1]
    assert seq[530]["market"][0] == ["BUY_LAND", 1]
    assert _sells(seq, W0, W1) == [(510, ["SELL", "WOOL", 5])]   # 对照：卖单已并


def test_empty_slot_ordering_preserved():
    """⑤空槽位次不变：合并后空出的槽置 [] 不删，槽位数与位次逐槽保持。"""
    pkg = _mk_pkg(sells=[(510, 1, "WOOL", 2), (512, 3, "WOOL", 3)],
                  others=[(510, 2, ["BUY_SEED", "WHEAT", 1]), (512, 0, ["HIRE"])])
    snap = copy.deepcopy(pkg)
    out = retape_lots.retape_sell_lots(pkg, {"max_orders_target": 1})
    seq, orig = _view(out["routes"]), _view(snap)
    for s in (510, 512):
        assert len(seq[s]["market"]) == len(orig[s]["market"])
    assert seq[510]["market"] == [[], ["SELL", "WOOL", 5],
                                  ["BUY_SEED", "WHEAT", 1]]
    assert seq[512]["market"] == [["HIRE"], [], [], []]   # 源槽置 [] 位次不动


def test_window_bounds_fail_closed():
    """越界参数即抛：window 越出磁带步界 → ValueError。"""
    pkg = _mk_pkg(sells=[(510, 0, "WOOL", 1)])
    with pytest.raises(ValueError, match="越出磁带步界"):
        retape_lots.retape_sell_lots(pkg, {"window": (504, 800)})
    with pytest.raises(ValueError):
        retape_lots.retape_sell_lots(pkg, {"window": (505, 505)})
    with pytest.raises(ValueError):
        retape_lots.retape_sell_lots(pkg, {"max_orders_target": 0})


def test_out_of_window_move_raises(monkeypatch):
    """越窗即抛：故障注入把合并单落到窗外步 → 术后对账 RuntimeError。"""
    pkg = _mk_pkg(sells=[(510, 0, "WOOL", 2), (520, 0, "WOOL", 3)])

    def relocate(p, rid, item, members, change_table, reason):
        total = sum(q for _, _, q in members)
        for s in sorted({m[0] for m in members}):        # 源槽清空（守恒仍平）
            idxs, _, act = _rs._cow_action(p, rid, s)
            for ms, slot, _q in members:
                if ms == s:
                    act["market"][slot] = []
            _rs._commit_action(p, idxs, s, act)
        idxs, _, act = _rs._cow_action(p, rid, 700)      # 越窗落点（窗 [504,672)）
        act["market"].append(["SELL", item, total])
        _rs._commit_action(p, idxs, 700, act)
        change_table.append({"route": rid, "kind": "sell_lots", "item": item,
                             "from_steps": [m[0] for m in members],
                             "to_step": 700, "qty": total, "reason": "inject"})

    monkeypatch.setattr(retape_lots, "_apply_group", relocate)
    with pytest.raises(RuntimeError, match="越窗"):
        retape_lots.retape_sell_lots(pkg, {"max_orders_target": 1})


def test_realrun_r37_tape_evidence():
    """⑥真 r37 实跑：build/main.py 解码手术，窗内单数/单均量/守恒摘要落盘。"""
    main_path = Path("/tmp/kagr_root/fn_work/legacy_software/kaggle_simulations"
                     "/orderbook_r37/build/main.py")
    if not main_path.is_file():
        pytest.skip("真跑基座缺失: %s" % main_path)
    text = main_path.read_text(encoding="utf-8")
    pkg = _rs._decode_routes(text)
    snap = copy.deepcopy(pkg)
    target, (w0, w1) = retape_lots._resolve_params(None)

    def _stats(p):
        per = {}
        for rid in retape_lots._route_order(p["routes"]):
            seq = retape_lots._seq(p, rid)
            lots = retape_lots._sell_scan(seq, w0, w1)
            wq = sum(q for _, _, _, q in lots)
            per[str(rid)] = {
                "window_orders": len(lots),
                "window_qty": wq,
                "avg_qty": round(wq / len(lots), 3) if lots else 0.0,
                "total_orders": retape_lots._sell_count(seq),
                "totals": retape_lots._sell_totals(seq),
            }
        return per

    before = _stats(pkg)
    out = retape_lots.retape_sell_lots(pkg, None)         # 缺省 337 口径
    assert pkg == snap                                    # 输入零改动
    after = _stats(out["routes"])
    assert all(before[r]["totals"] == after[r]["totals"] for r in before)
    # 编解码回路自检（复用 retape_sheep R15 自检链）
    new_text = _rs._encode_routes(text, out["routes"])
    assert _rs._decode_routes(new_text) == out["routes"]

    wo_b = [before[r]["window_orders"] for r in before]
    wo_a = [after[r]["window_orders"] for r in after]
    avg_b = [before[r]["avg_qty"] for r in before]
    avg_a = [after[r]["avg_qty"] for r in after]
    tot_b = [before[r]["total_orders"] for r in before]
    tot_a = [after[r]["total_orders"] for r in after]
    n_pairs = sum(len(before[r]["totals"]) for r in before)
    ev = {
        "source": str(main_path),
        "params": {"max_orders_target": target, "window": [w0, w1]},
        "n_routes": len(before),
        "window_orders": {"before_median": st.median(wo_b),
                          "after_median": st.median(wo_a),
                          "before_total": sum(wo_b), "after_total": sum(wo_a)},
        "avg_qty_per_order": {"before_median": st.median(avg_b),
                              "after_median": st.median(avg_a)},
        "route_sell_counts": {"before_median": st.median(tot_b),
                              "after_median": st.median(tot_a),
                              "target": target,
                              "n_at_or_below_target": sum(1 for t in tot_a
                                                          if t <= target)},
        "conservation": {"ok": True, "n_route_item_pairs": n_pairs},
        "encode_roundtrip": True,
        "change_table_rows": len(out["change_table"]),
        "per_route": {r: {"before": before[r], "after": after[r]}
                      for r in sorted(before, key=int)},
    }
    ev_path = Path(__file__).resolve().parent / "evidence" / \
        "retape_lots_realrun.json"
    ev_path.parent.mkdir(parents=True, exist_ok=True)
    ev_path.write_text(json.dumps(ev, ensure_ascii=False, indent=1),
                       encoding="utf-8")
    assert ev_path.exists()
    # 判据：窗内单数中位下探/单均量升/整路由单数对标 337 量级
    assert st.median(wo_a) < st.median(wo_b)
    assert st.median(avg_a) > st.median(avg_b)
    assert abs(st.median(tot_a) - target) <= 5
    assert sum(1 for t in tot_a if t <= target) >= 35
    assert all(r["kind"] == "sell_lots" for r in out["change_table"])
