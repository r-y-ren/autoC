# -*- coding: utf-8 -*-
"""R22 测试面：retape_shear_phase（毛期错峰/刀次≥5 核算）。

test_retape_shear_phase 真测试拆五组（责任契约 fn_docs/hybrid/
responsibility.md【R22 增补】retape_shear_phase 行）：
①构造小磁带（2 羊格 5 产毛窗）→ 轮次整体偏移（每格剪毛日 +offset）且每格
  刀次 ≥5（术后 _shear_cells 口径）；
②偏移后越季/刀次 <5 → 该格 no-op 留档不抛（from_day==to_day 且 reason 起
  "no-op"）；全格不可行 → no-op 全局（routes 原样）；刀次 <5 即抛反例；
③不动买卖/FEED/CARE 反例——市场单（SELL/BUY）与 FEED/CARE 指令手术前后逐
  位恒等，只动剪毛 HARVEST 排程；
④空槽位次不变——市场单故意空槽 [] 不删不移不填（742943 空槽位次语义）；
⑤真 r37 实跑——orderbook_r37/build/main.py 解码手术（_decode_routes/
  _encode_routes 编解码自检链）：偏移格数/刀次核算摘要记 evidence/
  shear_phase_realrun.json，输入零改动（写时复制）+术后每格刀次 ≥5。
"""
import copy
import json
import sys
from pathlib import Path

import pytest  # noqa: F401

_HERE = Path(__file__).resolve().parent
_KSIM = _HERE.parent
if str(_KSIM) not in sys.path:
    sys.path.insert(0, str(_KSIM))

try:
    from orderbook_predict import retape_shear_phase as sp
except ImportError:  # 兜底：直接以 orderbook_predict/ 为 sys.path 根跑测
    import retape_shear_phase as sp

try:
    from orderbook_r37 import retape_sheep as rs
except ImportError:
    sys.path.insert(0, str(_KSIM / "orderbook_r37"))
    import retape_sheep as rs

_R37_MAIN = _KSIM / "orderbook_r37" / "build" / "main.py"
_EVIDENCE = _HERE / "evidence" / "shear_phase_realrun.json"


# ---------------------------------------------------------------------------
# 构造件：迷你磁带路由包（每步动作独立入池；hands 在棚边出生格不动=格位恒定，
# 故剪毛 HARVEST 时序平移后格位归属稳定）。
# ---------------------------------------------------------------------------
def _mk_pkg(steps, places=(), shear_days=(), market=None, feeds=(), n_hands=2):
    """构造磁带路由包 {actions, routes:{'0':[...]}, shops:[]}。

    places=[(step, unit_idx)] 该 unit 当拍 PLACE SHEEP（出生格上栏=买点）；
    shear_days=[(day, unit_idx)] 该 unit day*24 HARVEST（=产毛窗剪毛刀）；
    market={step: [orders]} 市场单（原样入列，含故意空槽 []）；
    feeds=[(step, unit_idx, op)] FEED/CARE 等单元指令（手术不动）。
    """
    farmers = {s: ["PASS"] for s in range(steps)}
    hands = {s: [["PASS"] for _ in range(n_hands)] for s in range(steps)}
    markets = {s: [] for s in range(steps)}
    for s, ui in places:
        hands[s][ui] = ["PLACE", "SHEEP", 1]
    for d, ui in shear_days:
        hands[d * 24][ui] = ["HARVEST"]
    for s, ui, op in feeds:
        hands[s][ui] = list(op)
    for s, orders in (market or {}).items():
        markets[s] = [list(o) for o in orders]
    actions = [{"farmer": farmers[s], "hands": hands[s], "market": markets[s]}
               for s in range(steps)]
    return {"actions": actions, "routes": {"0": list(range(steps))}, "shops": []}


def _cells_after(out, rid="0"):
    seq = [out["routes"]["actions"][i] for i in out["routes"]["routes"][rid]]
    grid = rs._derive_grid_info(out["routes"])[rid]
    return rs._shear_cells(seq, grid)


def _noop(row):
    return row["reason"].startswith("no-op")


def test_retape_shear_phase():
    # 伞面冒烟（错峰手术组）：构造件端到端——2 羊格错峰+术后每格刀次 ≥5+输入
    # 零改动；细节判据在五组专测钉住。
    pkg = _mk_pkg(720, places=[(9 * 24 + 1, 0), (9 * 24 + 1, 1)],
                  shear_days=[(d, 0) for d in (15, 18, 21, 24, 27)]
                              + [(d, 1) for d in (15, 18, 21, 24, 27)])
    before = copy.deepcopy(pkg)
    out = sp.retape_shear_phase(pkg)
    assert set(out) == {"routes", "change_table"}
    assert pkg == before                       # 输入零改动（写时复制）
    assert len(out["change_table"]) == 2
    for c, v in _cells_after(out).items():
        assert v["n_cuts"] >= 5
        assert sorted(s // 24 for s in v["cuts"]) == [17, 20, 23, 26, 29]


# ---------------------------------------------------------------------------
# ① 轮次整体偏移 + 每格刀次 ≥5
# ---------------------------------------------------------------------------
def test_phase_shift_moves_rounds():
    pkg = _mk_pkg(720, places=[(9 * 24 + 1, 0), (9 * 24 + 1, 1)],
                  shear_days=[(d, 0) for d in (15, 18, 21, 24, 27)]
                              + [(d, 1) for d in (15, 18, 21, 24, 27)])
    out = sp.retape_shear_phase(pkg)
    rows = out["change_table"]
    # 2 羊格 5 产毛窗 → 轮次整体偏移（剪毛日 15/18/21/24/27 → 17/20/23/26/29）。
    assert len(rows) == 2
    for r in rows:
        assert r["kind"] == "shear_phase" and r["item"] == "WOOL"
        assert not _noop(r)
        assert r["from_day"] == 15 and r["to_day"] == 17   # 相位锚 +2
        assert r["cells"] == [(5, 4)] or r["cells"] == [(4, 5)]
    # 每格刀次 ≥5 且剪毛日整体 +2（产毛窗 [15,29] 内不越季）。
    cells = _cells_after(out)
    assert set(cells) == {(5, 4), (4, 5)}
    for c, v in cells.items():
        days = sorted(s // 24 for s in v["cuts"])
        assert v["n_cuts"] >= 5
        assert days == [17, 20, 23, 26, 29]     # = 原 [15,18,21,24,27] +2
        assert all(d <= 29 for d in days)       # 不越季
    # offset 可配：+3 → 15/18/21/24/27 → 18/21/24/27/30（30 越季丢弃→4 刀 no-op）。
    pkg3 = _mk_pkg(720, places=[(9 * 24 + 1, 0), (9 * 24 + 1, 1)],
                   shear_days=[(d, 0) for d in (15, 18, 21, 24, 27)]
                               + [(d, 1) for d in (15, 18, 21, 24, 27)])
    out3 = sp.retape_shear_phase(pkg3, offset=3)
    for r in out3["change_table"]:
        assert _noop(r) and r["from_day"] == r["to_day"] == 15


# ---------------------------------------------------------------------------
# ② 偏移后越季/刀次 <5 → 该格 no-op 留档不抛；全格不可行 → no-op 全局
# ---------------------------------------------------------------------------
def test_noop_when_infeasible():
    # 买点 d11 → 产毛窗 [17,29]，+2 → 19/22/25/28/31（31 出季丢弃）→ 4 刀 <5
    # → 两格 no-op（不抛），routes 原样（no-op 全局）。
    pkg = _mk_pkg(720, places=[(11 * 24 + 1, 0), (11 * 24 + 1, 1)],
                  shear_days=[(d, 0) for d in (17, 20, 23, 26, 29)]
                              + [(d, 1) for d in (17, 20, 23, 26, 29)])
    before = copy.deepcopy(pkg)
    out = sp.retape_shear_phase(pkg)             # 不抛
    assert pkg == before
    assert out["routes"] == before               # 全格不可行 → no-op 全局
    assert len(out["change_table"]) == 2
    for r in out["change_table"]:
        assert _noop(r) and r["from_day"] == r["to_day"] == 17
    # 逐格 no-op 留档不抛：混合格（1 可挪 1 不可挪）→ 1 shift + 1 no-op，不抛。
    mixed = _mk_pkg(720, places=[(9 * 24 + 1, 0), (11 * 24 + 1, 1)],
                    shear_days=[(d, 0) for d in (15, 18, 21, 24, 27)]
                                + [(d, 1) for d in (17, 20, 23, 26, 29)])
    outm = sp.retape_shear_phase(mixed)          # 不抛
    kinds = sorted((_noop(r), tuple(r["cells"])) for r in outm["change_table"])
    assert kinds == [(False, ((5, 4),)), (True, ((4, 5),))]
    for c, v in _cells_after(outm).items():
        assert v["n_cuts"] >= 5
    # 刀次 <5 即抛反例：3 刀格（无可行错峰保 3 刀）→ 术后核算红即抛。
    short = _mk_pkg(720, places=[(9 * 24 + 1, 0)],
                    shear_days=[(d, 0) for d in (15, 18, 21)])
    with pytest.raises(RuntimeError, match=r"刀次<5"):
        sp.retape_shear_phase(short)


# ---------------------------------------------------------------------------
# ③ 不动买卖/FEED/CARE（反例）+ ④ 空槽位次不变
# ---------------------------------------------------------------------------
def test_market_feed_care_untouched_and_slots():
    market = {
        100: [["SELL", "WOOL", 3], [], ["HIRE"]],   # 含故意空槽 []
        200: [["BUY_ANIMAL", "SHEEP", 1], [], [], ["SELL", "MILK", 2]],
    }
    feeds = [(300, 0, ["FEED"]), (301, 1, ["CARE"]), (302, 0, ["FEED"])]
    pkg = _mk_pkg(720, places=[(9 * 24 + 1, 0), (9 * 24 + 1, 1)],
                  shear_days=[(d, 0) for d in (15, 18, 21, 24, 27)]
                              + [(d, 1) for d in (15, 18, 21, 24, 27)],
                  market=market, feeds=feeds)
    before = copy.deepcopy(pkg)
    out = sp.retape_shear_phase(pkg)

    def snap(routes):
        return {"market": [list(routes["actions"][i].get("market") or [])
                           for i in routes["routes"]["0"]],
                "feed": [(s, routes["actions"][routes["routes"]["0"][s]]
                          ["hands"][ui])
                         for s, ui, _ in feeds]}

    sb, sa = snap(before), snap(out["routes"])
    # ③ 买卖/FEED/CARE 逐位恒等（只动剪毛 HARVEST 排程）。
    assert sa["market"] == sb["market"]
    assert sa["feed"] == sb["feed"]
    # ④ 空槽位次不变：市场单每拍列表（含 []）逐槽不删不移不填。
    for s in (100, 200):
        i_new = out["routes"]["routes"]["0"][s]
        i_old = before["routes"]["0"][s]
        assert out["routes"]["actions"][i_new]["market"] \
            == before["actions"][i_old]["market"]
        assert [o for o in out["routes"]["actions"][i_new]["market"]] \
            == [o for o in before["actions"][i_old]["market"]]
    # 剪毛 HARVEST 确被挪动（手术生效），且术后刀次 ≥5。
    for c, v in _cells_after(out).items():
        assert v["n_cuts"] >= 5
        assert sorted(s // 24 for s in v["cuts"]) == [17, 20, 23, 26, 29]


# ---------------------------------------------------------------------------
# ⑤ 真 r37 实跑：解码手术 + 编解码自检链 + 摘要记 evidence
# ---------------------------------------------------------------------------
def test_real_r37_run():
    assert _R37_MAIN.exists(), "缺真 r37 底版 orderbook_r37/build/main.py"
    text = _R37_MAIN.read_text(encoding="utf-8")

    # 编解码自检链：真 r37 无编辑往返逐字节恒等（_decode/_encode 同构）。
    pkg = rs._decode_routes(text)
    assert rs._encode_routes(text, pkg) == text

    before = copy.deepcopy(pkg)
    out = sp.retape_shear_phase(pkg)             # 真跑手术
    assert pkg == before                         # 输入零改动（写时复制）

    rows = out["change_table"]
    shifted = [r for r in rows if not _noop(r)]
    noop = [r for r in rows if _noop(r)]

    # 术后每格刀次核算摘要（≥5 红绿；历史仅报）。
    grid2 = rs._derive_grid_info(out["routes"])
    cuts = []
    for rid, g in grid2.items():
        seq = [out["routes"]["actions"][i] for i in out["routes"]["routes"][rid]]
        for c, v in rs._shear_cells(seq, g).items():
            cuts.append(v["n_cuts"])
    assert cuts and min(cuts) >= 5               # 刀次 <5 即抛 → 不触红
    hist = {}
    for n in cuts:
        hist[str(n)] = hist.get(str(n), 0) + 1

    # 编解码自检链：手术后包可 encode（四件套）且解码回路一致。
    text2 = rs._encode_routes(text, out["routes"])
    assert rs._decode_routes(text2) == out["routes"]

    summary = {
        "source": "orderbook_r37/build/main.py",
        "offset": 2,
        "min_cuts_required": 5,
        "total_cells": len(cuts),
        "shifted_cells": len(shifted),
        "noop_cells": len(noop),
        "min_cuts_after": min(cuts),
        "cut_hist_after": dict(sorted(hist.items(), key=lambda kv: int(kv[0]))),
        "shifted_routes": sorted({r["route"] for r in shifted},
                                 key=lambda k: int(k)),
        "encode_roundtrip_identical": True,
    }
    _EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    _EVIDENCE.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                         encoding="utf-8")

    assert _EVIDENCE.exists()
    saved = json.loads(_EVIDENCE.read_text(encoding="utf-8"))
    assert saved == summary
    assert saved["total_cells"] > 0 and saved["min_cuts_after"] >= 5
    assert saved["shifted_cells"] + saved["noop_cells"] == saved["total_cells"]
