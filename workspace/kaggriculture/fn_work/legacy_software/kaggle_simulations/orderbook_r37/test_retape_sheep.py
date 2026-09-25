# -*- coding: utf-8 -*-
"""R20 测试面：retape_sheep_timing（刀次核算组/资金序不变量）。

test_retape_sheep_timing 真测试拆七组（责任契约 fn_docs/hybrid/
responsibility.md【R19/R20 增补】retape_sheep_timing 行）：
①解码回路一致——decode→encode→decode 幂等、blob 区间外逐字节一致、compile、
  确定性双跑；真 r34a 无编辑往返逐字节恒等（编码参数同构）；
②刀次核算公式——构造用例 d11 买点=5 刀（达标）、d12 买点=4 刀（不达标即抛，
  ①刀次红定罪位）；边界 b=0→8 刀、b=12→4、b=23→1；
③手术只提前不推后——构造晚批（d12@288）→前移至窗内最早可行步（to_step<
  from_step、≤264、术后刀次 ≥5）；target_step 标定参数（B20）生效；
④达标批 no-op——原位不动（change_table 记 no-op，动作池零改写）；
⑤购买总量不变——羊/牛/鹅逐路由总量手术前后恒等（真 r34a+构造件）；
⑥资金序不变量——供资卖单之前不许挪入 BUY（V57）：有供资卖单时落点不得
  早于卖单位序（对照无卖单件落最早可行步），越窗界且被锁死记 skip 存活；
⑦实跑真 r34a 解剖快照——evidence/sheep_tape_dissection.json 一次性解剖
  产物，测试断言可复算（同源重算深等）+ 真磁带手术语义（route 115 批
  265→264 前移、route 12 批被供资卖单/槽位上限锁死记 skip、其余 no-op）。
"""
import base64
import copy
import json
import zlib
from pathlib import Path

import pytest  # noqa: F401

try:
    from orderbook_r37 import retape_sheep
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根跑测
    import retape_sheep


_HERE = Path(__file__).resolve().parent
_R34A_MAIN = _HERE.parent / "orderbook_2965_adopt" / "a" / "main.py"
_EVIDENCE = _HERE / "evidence" / "sheep_tape_dissection.json"


# ---------------------------------------------------------------------------
# 构造件：迷你磁带路由包（每步动作独立入池；剪毛链=同日 HARVEST→PLACE WOOL）
# ---------------------------------------------------------------------------
def _mk_pkg(steps, buys=(), sells=(), shear_days=(), others=()):
    """构造磁带路由包 {actions, routes:{'0':[...]}, shops:[]}。

    buys=[(step, qty)] 羊批；sells=[(step, item, qty)] 卖单（同步先于买入列）；
    shear_days=[day] 剪毛轮（day*24 farmer HARVEST、+1 PLACE WOOL 1）；
    others=[(step, order)] 其它订单（原样入列）。
    """
    markets = {s: [] for s in range(steps)}
    for s, item, q in sells:
        markets[s].append(["SELL", item, q])
    for s, order in others:
        markets[s].append(list(order))
    for s, q in buys:
        markets[s].append(["BUY_ANIMAL", "SHEEP", q])
    farmers = {s: ["PASS"] for s in range(steps)}
    for d in shear_days:
        farmers[d * 24] = ["HARVEST"]
        farmers[d * 24 + 1] = ["PLACE", "WOOL", 1]
    actions = [{"farmer": farmers[s], "hands": [], "market": markets[s]}
               for s in range(steps)]
    return {"actions": actions, "routes": {"0": list(range(steps))}, "shops": []}


def _mk_main(pkg):
    """路由包 → 合成 main 文本（与 r34a 同构 blob 行）。"""
    raw = json.dumps(pkg, separators=(",", ":"), ensure_ascii=False)
    body = base64.b85encode(zlib.compress(raw.encode("utf-8"), 9)).decode("ascii")
    return ("X = 1\n_R108_DATA=json.loads(zlib.decompress("
            "base64.b85decode('%s')))\nY = 2\n" % body)


def _r34a_text():
    return _R34A_MAIN.read_text(encoding="utf-8")


def _by_kind(rows, kind):
    return [r for r in rows if r["kind"] == kind]


def test_retape_sheep_timing():
    # 伞面冒烟（刀次核算组/资金序不变量）：构造件端到端——晚批前移+达标批
    # no-op+总量不变+资金序+术后核算通过；细节判据在七组专测钉住。
    pkg = _mk_pkg(480, buys=[(264, 1), (288, 2)], sells=[(200, "WOOL", 3)],
                  shear_days=[6, 9, 12, 15, 18])
    before = copy.deepcopy(pkg)
    out = retape_sheep.retape_sheep_timing(pkg)
    assert set(out) == {"routes", "change_table"}
    rows = out["change_table"]
    assert [(r["route"], r["kind"], r["from_step"], r["to_step"]) for r in rows] \
        == [("0", "no-op", 264, 264), ("0", "buy_move", 288, 200)]
    assert retape_sheep._animal_totals(
        [out["routes"]["actions"][i] for i in out["routes"]["routes"]["0"]]) \
        == {"SHEEP": 3}
    assert pkg == before


# ---------------------------------------------------------------------------
# ① 解码回路一致
# ---------------------------------------------------------------------------
def test_decode_encode_loop():
    # 真 r34a：无编辑往返逐字节恒等（编码参数与原 blob 同构）。
    text = _r34a_text()
    pkg = retape_sheep._decode_routes(text)
    assert set(pkg) == {"actions", "routes", "shops"}
    assert len(pkg["routes"]) == 41
    assert retape_sheep._encode_routes(text, pkg) == text

    # 改包回路：decode→encode→decode 幂等 + 区间外逐字节一致 + 可编译 +
    # 确定性双跑（防"跳自检假实现"，独立复跑四条）。
    edited = copy.deepcopy(pkg)
    edited["actions"][0]["market"].append(["HIRE"])
    new_text = retape_sheep._encode_routes(text, edited)
    assert retape_sheep._decode_routes(new_text) == edited
    m_old = retape_sheep._BLOB_RE.search(text)
    m_new = retape_sheep._BLOB_RE.search(new_text)
    lo_old, hi_old = m_old.span(1)
    lo_new, hi_new = m_new.span(1)
    raw_old = text.encode("utf-8")
    raw_new = new_text.encode("utf-8")
    assert raw_old[:lo_old] == raw_new[:lo_new]      # blob 前逐字节一致
    assert raw_old[hi_old:] == raw_new[hi_new:]      # blob 后逐字节一致
    compile(new_text, "<verify>", "exec")
    assert retape_sheep._encode_routes(text, edited) == new_text   # 双跑一致

    # 合成件同检（自足小 blob，不依赖真磁带）。
    pkg2 = _mk_pkg(8, buys=[(1, 1)], shear_days=[0])
    main2 = _mk_main(pkg2)
    pkg2b = retape_sheep._decode_routes(main2)
    assert pkg2b == pkg2
    assert retape_sheep._encode_routes(main2, pkg2b) == main2

    # 形态 fail-closed。
    with pytest.raises(ValueError):
        retape_sheep._decode_routes("no blob here")
    with pytest.raises(TypeError):
        retape_sheep._decode_routes(b"bytes")
    bad = copy.deepcopy(pkg2)
    bad["routes"]["0"] = [999]
    with pytest.raises(ValueError):
        retape_sheep._encode_routes(main2, bad)


# ---------------------------------------------------------------------------
# ② 刀次核算公式（构造用例：d11 买点=5 刀、d12=4 刀不达标抛）
# ---------------------------------------------------------------------------
def test_potential_shears_formula():
    f = retape_sheep._potential_shears
    assert f(24 * 11) == 5          # d11 买点=5 刀（d17/20/23/26/29 型）
    assert f(24 * 11 + 1) == 5
    assert f(24 * 12) == 4          # d12 买点=4 刀（不达标）
    assert f(24 * 0) == 8           # d0 买点=8 刀
    assert f(24 * 23) == 1
    assert f(24 * 24) == 0
    assert f(264) == 5 and f(288) == 4

    # d11 买点经公共入口达标（no-op 放行）；构造件需 ≥5 剪毛轮过②。
    pkg_ok = _mk_pkg(480, buys=[(264, 1)], shear_days=[6, 9, 12, 15, 18])
    out_ok = retape_sheep.retape_sheep_timing(pkg_ok)
    assert _by_kind(out_ok["change_table"], "no-op")

    # d12 买点被供资卖单/窗界锁死（step 270 卖单→无 ≥ 卖单位序的窗内落点）
    # → 记 skip 后仍①刀次红即抛（skip 不豁免刀次）。
    pkg_bad = _mk_pkg(480, buys=[(288, 1)], sells=[(270, "WOOL", 3)],
                      shear_days=[6, 9, 12, 15, 18])
    with pytest.raises(RuntimeError, match=r"①刀次红.*潜在刀次=4"):
        retape_sheep.retape_sheep_timing(pkg_bad)


# ---------------------------------------------------------------------------
# ③ 手术只提前不推后（构造晚批→前移）
# ---------------------------------------------------------------------------
def test_surgery_only_earlier_moves():
    pkg = _mk_pkg(480, buys=[(288, 2)], shear_days=[6, 9, 12, 15, 18])
    out = retape_sheep.retape_sheep_timing(pkg)
    moves = _by_kind(out["change_table"], "buy_move")
    assert len(moves) == 1
    row = moves[0]
    assert row["from_step"] == 288 and row["to_step"] < 288
    assert row["to_step"] <= 264 and row["item"] == "SHEEP" and row["qty"] == 2
    assert row["to_step"] == 0      # 缺省=窗内最早可行步
    # 术后刀次 ≥5 且输入零改动（写时复制）。
    routes = out["routes"]
    step_new = routes["routes"]["0"][row["to_step"]]
    assert routes["actions"][step_new]["market"][-1] == ["BUY_ANIMAL", "SHEEP", 2]
    src_idx = routes["routes"]["0"][288]
    assert routes["actions"][src_idx]["market"][0] == []
    assert retape_sheep._potential_shears(row["to_step"]) >= 5
    assert pkg == _mk_pkg(480, buys=[(288, 2)], shear_days=[6, 9, 12, 15, 18])

    # target_step 标定参数（B20 judge_sheep_league 输出）优先于缺省最早可行位。
    saved = retape_sheep.TARGET_WINDOW.get("target_step")
    try:
        retape_sheep.TARGET_WINDOW["target_step"] = 200
        out2 = retape_sheep.retape_sheep_timing(
            _mk_pkg(480, buys=[(288, 2)], shear_days=[6, 9, 12, 15, 18]))
        assert _by_kind(out2["change_table"], "buy_move")[0]["to_step"] == 200
    finally:
        retape_sheep.TARGET_WINDOW["target_step"] = saved

    # 推后禁令：已达窗内的批永不后移（no-op 原位）。
    pkg3 = _mk_pkg(480, buys=[(240, 1)], shear_days=[6, 9, 12, 15, 18])
    out3 = retape_sheep.retape_sheep_timing(pkg3)
    assert not _by_kind(out3["change_table"], "buy_move")
    assert _by_kind(out3["change_table"], "no-op")[0]["to_step"] == 240


# ---------------------------------------------------------------------------
# ④ 达标批 no-op
# ---------------------------------------------------------------------------
def test_noop_for_compliant_batch():
    pkg = _mk_pkg(480, buys=[(1, 2), (150, 2), (264, 1)],
                  sells=[(150, "WOOL", 12)], shear_days=[6, 9, 12, 15, 18])
    before = copy.deepcopy(pkg)
    out = retape_sheep.retape_sheep_timing(pkg)
    assert len(out["change_table"]) == 3
    assert {r["kind"] for r in out["change_table"]} == {"no-op"}
    assert [r["from_step"] for r in out["change_table"]] == [1, 150, 264]
    for r in out["change_table"]:
        assert r["from_step"] == r["to_step"]
    assert out["routes"] == before                 # 零改写（原样深等）
    assert pkg == before                           # 输入零改动


# ---------------------------------------------------------------------------
# ⑤ 购买总量不变
# ---------------------------------------------------------------------------
def test_purchase_totals_preserved():
    pkg = _mk_pkg(480, buys=[(288, 2), (300, 1)],
                  shear_days=[6, 9, 12, 15, 18])
    before = retape_sheep._animal_totals(
        [pkg["actions"][i] for i in pkg["routes"]["0"]])
    out = retape_sheep.retape_sheep_timing(pkg)
    after = retape_sheep._animal_totals(
        [out["routes"]["actions"][i] for i in out["routes"]["routes"]["0"]])
    assert before == after == {"SHEEP": 3}

    # 真 r34a：41 路由羊/牛/鹅总量逐路由恒等（route 9=6牛+11羊 目标结构不动）。
    text = _r34a_text()
    pkg_r = retape_sheep._decode_routes(text)
    base = {rid: retape_sheep._animal_totals([pkg_r["actions"][i] for i in ids])
            for rid, ids in pkg_r["routes"].items()}
    out_r = retape_sheep.retape_sheep_timing(pkg_r)
    for rid, ids in out_r["routes"]["routes"].items():
        got = retape_sheep._animal_totals([out_r["routes"]["actions"][i] for i in ids])
        assert got == base[rid], (rid, got, base[rid])
    assert base["9"] == {"COW": 6, "SHEEP": 11}


# ---------------------------------------------------------------------------
# ⑥ 资金序不变量（供资卖单之前不许挪入 BUY）
# ---------------------------------------------------------------------------
def test_funding_order_invariant():
    # 有供资卖单（step 200）：默认最早可行位被卖单锁住→落点=卖单同步步尾
    # （(200,1) ≥ (200,0)，不挪到供资卖单成交前）。
    pkg = _mk_pkg(480, buys=[(288, 1)], sells=[(200, "WOOL", 3)],
                  shear_days=[6, 9, 12, 15, 18])
    out = retape_sheep.retape_sheep_timing(pkg)
    row = _by_kind(out["change_table"], "buy_move")[0]
    assert row["to_step"] == 200                  # 而非最早的 step 0
    assert row["to_step"] > 0
    tgt = out["routes"]["actions"][out["routes"]["routes"]["0"][200]]["market"]
    assert tgt[-1] == ["BUY_ANIMAL", "SHEEP", 1]  # 追加在卖单（下标0）之后

    # 对照：无供资卖单→落最早可行步（证明上例如非资金序必落 0）。
    out2 = retape_sheep.retape_sheep_timing(
        _mk_pkg(480, buys=[(288, 1)], shear_days=[6, 9, 12, 15, 18]))
    assert _by_kind(out2["change_table"], "buy_move")[0]["to_step"] == 0

    # 供资卖单锁死窗内全部落点（step 264 卖单 + 该步 10 槽满）→ 换步无果记
    # skip 存活；该批刀次达标（265=d11，5 刀）仅③残差→skip 豁免不抛。
    out3 = retape_sheep.retape_sheep_timing(
        _mk_pkg(480, buys=[(265, 1)], sells=[(264, "WOOL", 3)],
                shear_days=[6, 9, 12, 15, 18],
                others=[(264, ["HIRE"])] * 9))
    skips = _by_kind(out3["change_table"], "skip")
    assert len(skips) == 1 and skips[0]["from_step"] == 265
    assert not _by_kind(out3["change_table"], "buy_move")
    assert "funding_sell=264,0" in skips[0]["reason"]

    # 同步槽序（V57 同回合形态）：供资卖单在同列表前位，落点不得反超其位序。
    pkg4 = _mk_pkg(480, buys=[(288, 1)], sells=[(200, "WOOL", 3)],
                   shear_days=[6, 9, 12, 15, 18])
    pkg4["actions"][200]["market"] = [["SELL", "WOOL", 3], [], ["HIRE"]]
    out4 = retape_sheep.retape_sheep_timing(pkg4)
    row4 = _by_kind(out4["change_table"], "buy_move")[0]
    assert row4["to_step"] == 200
    tgt4 = out4["routes"]["actions"][out4["routes"]["routes"]["0"][200]]["market"]
    assert tgt4[:3] == [["SELL", "WOOL", 3], [], ["HIRE"]]
    assert tgt4[3:] == [["BUY_ANIMAL", "SHEEP", 1]]   # 追加尾部，空槽位次不动


# ---------------------------------------------------------------------------
# ⑦ 真 r34a 解剖快照可复算 + 真磁带手术语义
# ---------------------------------------------------------------------------
def test_dissection_snapshot_recomputable():
    assert _EVIDENCE.exists(), "缺一次性解剖产物 evidence/sheep_tape_dissection.json"
    snap_saved = json.loads(_EVIDENCE.read_text(encoding="utf-8"))
    snap = retape_sheep._dissection_snapshot(
        _r34a_text(), "orderbook_2965_adopt/a/main.py")
    assert snap == snap_saved                 # 一次性产物=可复算（同源重算深等）
    assert len(snap["routes"]) == 41
    r9 = snap["routes"]["9"]
    assert r9["animal_totals"] == {"COW": 6, "SHEEP": 11}
    assert sum(b["qty"] for b in r9["sheep_batches"]) == 11
    for b in r9["sheep_batches"]:
        assert b["potential_cuts"] >= 5
    assert len(r9["shear_rounds"]) >= 5
    # 越窗批清单（route 12/115 的 step 265 批）与刀次口径钉住。
    late = [(rid, b["from_step"]) for rid, v in snap["routes"].items()
            for b in v["sheep_batches"] if b["from_step"] > 264]
    assert late == [("12", 265), ("115", 265)]


def test_real_r34a_surgery_semantics():
    text = _r34a_text()
    pkg = retape_sheep._decode_routes(text)
    before = copy.deepcopy(pkg)
    out = retape_sheep.retape_sheep_timing(pkg)
    rows = out["change_table"]
    # 真磁带语义：route 115 批 265→264 前移（唯一位移）；route 12 批被
    # 供资卖单 (264,1)+目标步槽位上限锁死记 skip；其余 229 批 no-op。
    moves = _by_kind(rows, "buy_move")
    assert [(r["route"], r["from_step"], r["to_step"]) for r in moves] \
        == [("115", 265, 264)]
    skips = _by_kind(rows, "skip")
    assert [(r["route"], r["from_step"]) for r in skips] == [("12", 265)]
    assert len(_by_kind(rows, "no-op")) == 229
    assert len(rows) == 231                    # 逐批一行（含 no-op 行）
    # 只提前不推后 + 输入零改动 + 术后核算过（不抛）。
    assert all(r["to_step"] <= r["from_step"] for r in rows)
    assert pkg == before
    # 移动步槽位形态：源槽留 []、目标步尾部追加、其余槽位逐位不动。
    moved_src = out["routes"]["actions"][out["routes"]["routes"]["115"][265]]
    assert moved_src["market"][7] == []
    assert moved_src["market"][:7] == before["actions"][
        before["routes"]["115"][265]]["market"][:7]
    tgt = out["routes"]["actions"][out["routes"]["routes"]["115"][264]]["market"]
    assert tgt[-1] == ["BUY_ANIMAL", "SHEEP", 1] and len(tgt) == 7
