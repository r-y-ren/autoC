# -*- coding: utf-8 -*-
"""build_s3buy5（s3buy5 lab）：BUY5 开局复刻 + 洗价层 + 中盘畜群自适应（SHEEP 弹性面）。

基底 = orderbook_composite_lab/build/c_final/main.py（sha a37c0d34…）。
干净室行为复刻（不拷贝无许可字节；D5/D6 指纹 + mooman 公开件概念重实现）：

  S3 = C_final 全部既有层（卖面/肥配比/M13）零改写
     + BUY5 开局替换（磁带手术 trunk 段，挂 _alt_install 外壳断言协同机器）：
       turn1 = [BUY_ANIMAL COW 1, BUY_PRODUCT WHEAT 5, BUY_PRODUCT WHEAT 13,
                BUY_PRODUCT WHEAT 30, SELL WHEAT 30, BUY_SEED WHEAT 1]
               族起手形 COW1+WHEAT5（D6 verbatim；±SHEEP 腿未取=非冻结指纹）
               + mooman 洗价形 WHEAT 13/30/30 原位 tape[0]（买 43 支撑 30 卖腿）
               + HybridOpening 功能种子腿。
       turn2 = [SELL WHEAT 1, HIRE×4, BUY_ANIMAL COW 1, BUY_ANIMAL SHEEP 2]
               D6 verbatim（t2 SELL WHEAT1+HIRE×4+BUY COW+SHEEP）；
               总量 2COW+2SHEEP 沿基底防放置链断链。
     + 中盘畜群自适应（尾块参数化；D6 弹性面修正）：
       摆动靶=SHEEP 数为主（GOOSE/COW/班组/单量/卖法=刚性面零触碰）；
       画像族→SHEEP 档位预设（h1_mirror→0 中档 / r37_2965_family→0 /
       wfr→+1 零畜群触碰 / unknown→+1 零足迹），市场态 ±1 档摆动
       （WOOL 稀缺→+1 保羊；WOOL 过剩→−1 减羊），档位=中盘晚波羊链
       抑制阶梯 {+1: 0 条, 0: ≤2 条, −1: ≤4 条}（减法手术：buy 扣量+
       pickup/place→PASS，build 留空栏；FIFO 池平衡校验 fail-closed），
       step≥144 画像锁存后生效，换局可逆。CARROT 地弹性=辅面（参数口留档，
       产线深埋本轮不作动器）。

产物 orderbook_s3buy5_lab/build/s3_buy5/（+ s3_open 自适应关断件）。
不改既有代码；不提交；不发射。
"""
from __future__ import annotations

import base64
import copy
import difflib
import hashlib
import json
import re
import time
import zlib
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
CFINAL = KSIM_DIR / "orderbook_composite_lab" / "build" / "c_final" / "main.py"
OUT_FULL = MODULE_DIR / "build" / "s3_buy5"
OUT_OPEN = MODULE_DIR / "build" / "s3_open"
OUT_WASH = MODULE_DIR / "build" / "s3_wash"
OUT_ADAPT0 = MODULE_DIR / "build" / "s3_adapt0"
EVID_DIR = MODULE_DIR / "evidence"
CFINAL_SHA = "a37c0d3487fe1d2152ec6c0b767b36afc21ad18207accb2d3cf1f1b077016a92"
SCHEMA = "orderbook_s3buy5_manifest/1.0"

# ---- 开局常量（干净室：D6 verbatim 族起手 + mooman 洗价形 + 功能种子腿） ----
S3_T0 = [
    ["BUY_ANIMAL", "COW", 1],        # BUY5 族起手：COW1 抢建（D6 verbatim t1）
    ["BUY_PRODUCT", "WHEAT", 5],     # BUY5 族饲料腿 WHEAT5（D6 verbatim t1）
    ["BUY_PRODUCT", "WHEAT", 4],    # 洗价买腿（现金安全洗价骨架 9买/3卖）
    ["SELL", "WHEAT", 3],            # 洗价卖腿（v9 8/3 谱系形的族腿融合）
    ["BUY_SEED", "WHEAT", 1],        # HybridOpening 临时麦种子（功能腿）
]
# 洗价形全量版（任务括注口径：族起手 + mooman 13/30/30 原位 tape[0]）——
# 现金包络证伪件（v9 opensim 6,648 开局 + 本程 smoke：对 dump 型开局卖腿被
# 割 −20k..−65k 级联；作 s3_wash 消融臂留证，不入主件）。
S3_T0_WASH = [
    ["BUY_ANIMAL", "COW", 1],
    ["BUY_PRODUCT", "WHEAT", 5],
    ["BUY_PRODUCT", "WHEAT", 13],    # 洗价形买腿 13（mooman 公开概念）
    ["BUY_PRODUCT", "WHEAT", 30],    # 洗价形买腿 30（13+30=43 支撑 30 卖腿）
    ["SELL", "WHEAT", 30],           # 洗价形卖腿 30（原位 tape[0]，mooman 形）
    ["BUY_SEED", "WHEAT", 1],
]
S3_T1 = [
    ["SELL", "WHEAT", 1],            # D6 verbatim t2：SELL WHEAT1（洗价卖腿）
    ["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"],  # HIRE 批量（D5 4-5 域；
    # D6 verbatim ×4 系其自案劳动链；我方案链 step2 需 h0-h4 五手，取 5 防断链）
    ["BUY_ANIMAL", "COW", 1],        # D6 verbatim t2：BUY COW（总量 2 沿基底）
    ["BUY_ANIMAL", "SHEEP", 2],      # D6 verbatim t2：BUY SHEEP（总量 2 沿基底）
]

# ---- 自适应档位（D6 弹性面：SHEEP 数为主；抑制阶梯=晚波羊链） ----
TIER_DROPS = {1: 0, 0: 2, -1: 4}    # 档位→中盘晚波羊链抑制条数
TIER_PRESET = {"h1_mirror": 0, "r37_2965_family": 0, "wfr": 1,
               "unknown": 0}   # unknown=市场态驱动中档（herd 面非对手条件面）
SWING_PARAMS = {
    "signal": "market.inventory WOOL/EGG 比 @step144",
    "rule": "wool*2<egg → +1（保羊）；wool>egg*2 → −1（减羊）；deadzone 0",
    "blueprint": "SHEEP 数 CV 0.56-0.94（D6 全顶带）；GOOSE=刚性面",
    "carrot_secondary": "CARROT 地弹性为辅（CV 0.41，12-96 格）——参数口留档，"
                        "产线深埋本轮不作动器",
}


# ============================================================ 磁带解码 ==
def decode_blob(src: str):
    m = re.search(
        r"_R108_DATA=json.loads\(zlib.decompress\(base64.b85decode\('([^']+)'\)\)\)",
        src)
    if not m:
        raise RuntimeError("校验红：_R108_DATA blob 未找到")
    d = json.loads(zlib.decompress(base64.b85decode(m.group(1))))
    m2 = re.search(
        r"_OC_C3_DELTA = json.loads\(zlib.decompress\(base64.b85decode\('([^']+)'\)\)\)",
        src)
    c3 = json.loads(zlib.decompress(base64.b85decode(m2.group(1)))) if m2 else {}
    return d, c3, m.group(1)


def unit_ops(a):
    out = [("F", a.get("farmer"))]
    for k, h in enumerate(a.get("hands") or []):
        out.append(("h%d" % k, h))
    return [(u, c) for u, c in out if isinstance(c, list) and c]


# ============================================================ 羊链 ==
def find_sheep_pairs(acts, routes, rid):
    """中盘（step≥144）SHEEP 购置对：FIFO 池绑定 buy→pickup，pickup→place
    同单元。返回按时间序的对列（供晚波优先抑制）+ 池平衡校验所需事件。"""
    seq = routes[rid]
    n = len(seq)
    buys = []      # (step, slot, qty)
    picks = []     # (step, unit, place_step or None)
    for s, i in enumerate(seq):
        if s < 144:
            continue
        for k, o in enumerate(acts[i].get("market") or []):
            if (isinstance(o, list) and o and o[0] == "BUY_ANIMAL"
                    and o[1] == "SHEEP"):
                buys.append([s, k, int(o[2]) if len(o) > 2 else 1])
        for u, c in unit_ops(acts[i]):
            if c[:2] == ["PICKUP", "SHEEP"]:
                q = None
                for q2 in range(s + 1, min(s + 40, n)):
                    for u2, c2 in unit_ops(acts[seq[q2]]):
                        if u2 == u and c2[:2] == ["PLACE", "SHEEP"]:
                            q = q2
                            break
                    if q is not None:
                        break
                picks.append([s, u, q])
    # FIFO：每 buy 供 qty 个 pickup
    pairs, bi = [], 0
    remaining = 0
    for p in picks:
        while remaining == 0 and bi < len(buys):
            remaining = buys[bi][2]
            bi += 1
        if remaining == 0:
            continue
        remaining -= 1
        buy = buys[bi - 1]
        pairs.append({"buy_step": buy[0], "buy_slot": buy[1],
                      "pickup": p[0], "unit": p[1], "place": p[2]})
    return pairs, buys, picks


def build_tier_deltas(acts, routes, c3_cells):
    """档位→抑制阶梯（晚波羊链优先；减法：buy 扣量 + pickup/place→PASS）。
    池平衡 fail-closed：抑制后 SHEEP 池时间线仍全程 ≥0 才落链。"""
    deltas = {"1": {}, "0": {}, "-1": {}}
    per_route = {}
    for rid in routes:
        pairs, buys, picks = find_sheep_pairs(acts, routes, rid)
        # 抑制候选：晚波优先（pickup 步倒序）；buy 逐头扣量
        cand = sorted(pairs, key=lambda x: -x["pickup"])
        chosen = {"1": [], "0": [], "-1": []}
        info = {}
        for tier in (1, 0, -1):
            want = TIER_DROPS[tier]
            sel = []
            for c in cand:
                if len(sel) >= want:
                    break
                sel.append(c)
            # 池平衡校验：模拟 SHEEP 池（buy+ / pickup-），抑制集从事件中移除
            # fail-closed：逐条回退（先退最新）直到平衡
            while sel and not _pool_ok(acts, routes, rid, sel):
                sel = sel[1:]
            chosen[tier] = sel
            if not sel:
                continue
            per = deltas[str(tier)].setdefault(rid, {})
            # 同步累加 mut（同一动作格可含多单元/多单；先收集后物化）
            muts = {}

            def add_mut(step, fn):
                muts.setdefault(step, []).append(fn)

            # buy 扣量（按 buy_step 聚合多槽；一次物化防槽位漂移）
            dec = {}
            for c in sel:
                key = (c["buy_step"], c["buy_slot"])
                dec[key] = dec.get(key, 0) + 1
            dec_by_step = {}
            for (bs, slot), k in dec.items():
                dec_by_step.setdefault(bs, {})[slot] = k
            for bs, slots in dec_by_step.items():
                def mut_buy(a, _slots=slots):
                    for _slot, _k in _slots.items():
                        o = list(a["market"][_slot])
                        q = int(o[2]) if len(o) > 2 else 1
                        if q - _k <= 0:
                            a["market"][_slot] = None
                        else:
                            a["market"][_slot] = [
                                "BUY_ANIMAL", "SHEEP", q - _k]
                    a["market"] = [x for x in a["market"] if x is not None]

                add_mut(bs, mut_buy)
            for c in sel:
                def mut_pick(a, _u=c["unit"]):
                    _set_unit(a, _u, "PICKUP", ["PASS"])

                add_mut(c["pickup"], mut_pick)
                if c["place"] is not None:
                    def mut_place(a, _u=c["unit"]):
                        _set_unit(a, _u, "PLACE", ["PASS"])

                    add_mut(c["place"], mut_place)
            for step, fns in muts.items():
                def mut_all(a, _fns=fns):
                    for fn in _fns:
                        fn(a)

                per[str(step)] = edit_action(acts, routes, rid, step, mut_all)
            info[str(tier)] = [{"buy_step": c["buy_step"], "pickup": c["pickup"],
                                "unit": c["unit"], "place": c["place"]}
                               for c in sel]
        # C3 触点排他（同面干扰定理前提）
        for tier, per in deltas.items():
            for rid2 in list(per):
                if rid2 != rid:
                    continue
                bad = [int(k) for k in per[rid2] if (rid, int(k)) in c3_cells]
                if bad:
                    raise RuntimeError("S3 抑制触点撞 C3 触点: %s %r" % (rid, bad))
        per_route[rid] = info
    return deltas, per_route


def _pool_ok(acts, routes, rid, sel):
    """抑制 sel 后 SHEEP 池时间线全程 ≥0（buy+/pickup-，FIFO 无关仅计数）。"""
    seq = routes[rid]
    drop_buy, drop_pick = {}, set()
    for c in sel:
        drop_buy[(c["buy_step"], c["buy_slot"])] = \
            drop_buy.get((c["buy_step"], c["buy_slot"]), 0) + 1
        drop_pick.add(c["pickup"])
    bal = 0
    events = []
    for s in range(144, len(seq)):
        a = acts[seq[s]]
        for k, o in enumerate(a.get("market") or []):
            if (isinstance(o, list) and o and o[0] == "BUY_ANIMAL"
                    and o[1] == "SHEEP"):
                q = int(o[2]) if len(o) > 2 else 1
                q -= drop_buy.get((s, k), 0)
                events.append((s, 0, max(0, q)))
        if s not in drop_pick:
            for u, c in unit_ops(a):
                if c[:2] == ["PICKUP", "SHEEP"]:
                    events.append((s, 1, 1))
    events.sort(key=lambda x: (x[0], x[1]))
    for _, kind, q in events:
        bal += q if kind == 0 else -q
        if bal < 0:
            return False
    return True


def edit_action(acts, routes, rid, step, mut):
    """返回替换动作（深拷贝 + mut 作用于动作 dict）；不触碰原对象。"""
    a = copy.deepcopy(acts[routes[rid][step]])
    mut(a)
    return a


def _set_unit(a, unit, kind, to):
    def flip(cmd):
        if cmd and cmd[0] == kind:
            cmd[:] = list(to)
    if unit == "F":
        flip(a.get("farmer") or [])
        return
    idx = int(unit[1:])
    hands = a.get("hands") or []
    if 0 <= idx < len(hands):
        flip(hands[idx])


# ============================================================ 尾块 ==
def make_tail(delta_json: str, adaptive_on: bool, t0, preset_mode: str) -> str:
    tail = '''

# ==== S3 BUY5 开局复刻 + 中盘畜群自适应（s3buy5 尾块；干净室行为复刻） ====
# 来源口径：D6 verbatim 族起手（t1 COW1+WHEAT5±SHEEP；t2 SELL WHEAT1+
# HIRE×4+BUY COW+SHEEP）+ mooman 公开概念洗价形 WHEAT 13/30/30（买 43 支撑
# 30 卖腿，原位 tape[0]）+ HybridOpening 功能种子腿。不拷贝无许可字节。
# 自适应（D6 弹性面）：摆动靶=SHEEP 数（GOOSE/COW/班组/单量/卖法=刚性面）。
_S3_T0 = __T0_JSON__
_S3_T1 = [["SELL", "WHEAT", 1], ["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"],
          ["HIRE"], ["BUY_ANIMAL", "COW", 1], ["BUY_ANIMAL", "SHEEP", 2]]
_S3_ALT_INSTALL = _alt_install
_S3_TIER_DELTA = json.loads(zlib.decompress(base64.b85decode(
    '%(delta)s')))
_S3_TIER_PRESET = __PRESET_JSON__
_S3_SAFE_DEFAULT = __SAFE_JSON__
_S3_ADAPTIVE_ON = %(adaptive)s
_S3_LATCHED = [False]
_S3_BACKUP = [None]
_S3_REPORT = {"install_calls": 0, "install_errors": 0, "cls": None,
              "swing": None, "tier": None, "cells": 0, "latches": 0,
              "restores": 0, "adaptive_on": %(adaptive)s}


def _s3_install_opening():
    """磁带手术 trunk 段：turn1-2 市场单重排（外壳 _alt_install 恢复后落座）。"""
    routes = _IMPL.chassis.routes
    for tape in routes.values():
        tape[0] = dict(tape[0], market=[list(o) for o in _S3_T0])
        tape[1] = dict(tape[1], market=[list(o) for o in _S3_T1])


def _alt_install(mode):
    _S3_ALT_INSTALL(mode)
    try:
        _s3_install_opening()
        _S3_REPORT["install_calls"] += 1
    except Exception:
        _S3_REPORT["install_errors"] += 1


def _s3_swing(obs):
    """市场态 ±1 档摆动（WOOL 稀缺保羊/过剩减羊；D6 响应市场自适应）。"""
    try:
        inv = ((obs.get("market") or {})
               if isinstance(obs.get("market"), dict) else {}).get("inventory") or {}
        wool = int(inv.get("WOOL", 0)) + 1
        egg = int(inv.get("EGG", 0)) + 1
        if wool * 2 < egg:
            return 1
        if wool > egg * 2:
            return -1
    except Exception:
        pass
    return 0


def _s3_restore():
    try:
        bk = _S3_BACKUP[0] or {}
        for (rid, idx), act in bk.items():
            seq = _IMPL.chassis.routes.get(rid)
            if seq is not None and 0 <= idx < len(seq):
                seq[idx] = act
    except Exception:
        pass
    _S3_BACKUP[0] = None
    _S3_LATCHED[0] = False


def _s3_apply(observation, step):
    if _S3_LATCHED[0] or int(step) < 144:
        return
    _S3_LATCHED[0] = True
    _S3_REPORT["latches"] += 1
    try:
        cls = _oc_cls(observation, int(step))
        sw = _s3_swing(observation)
        if cls == "wfr":
            tier = 1   # C3 域独占：wfr 零畜群触碰
        elif not _S3_ADAPTIVE_ON or _S3_SAFE_DEFAULT:
            tier = 1   # safe 档=机制armed但钉 +1（作动代价见 s3_adapt0 消融）
        else:
            preset = _S3_TIER_PRESET.get(cls, 0)
            tier = max(-1, min(1, preset + sw))
        _S3_REPORT.update(cls=cls, swing=sw, tier=tier, cells=0)
        if tier == 1:
            return
        delta = _S3_TIER_DELTA.get(str(tier)) or {}
        bk = {}
        for rid, per in delta.items():
            rid_k = int(rid) if str(rid).lstrip("-").isdigit() else rid
            seq = _IMPL.chassis.routes.get(rid_k)
            if seq is None:
                continue
            for k, act in per.items():
                i = int(k)
                if 0 <= i < len(seq):
                    bk[(rid_k, i)] = seq[i]
                    seq[i] = act
        _S3_BACKUP[0] = bk
        _S3_REPORT["cells"] = len(bk)
    except Exception:
        _S3_REPORT["cells"] = -1


_S3_OC_AFTER = _oc_after


def _oc_after(observation, action):
    """S3 换局还原：step==0/step 回退 → 自适应换表还原+闩复位（M13 同模板）。"""
    try:
        step = int((observation or {}).get("step", 0))
        player = int((observation or {}).get("player", 0))
        st = _OC_STATE.get(player)
        if st is None or step == 0 or step <= st.get("last_step", -1):
            _s3_restore()
            _S3_REPORT["restores"] += 1
    except Exception:
        pass
    return _S3_OC_AFTER(observation, action)


_S3_PARENT = _hs_agent
del _hs_agent


def _hs_agent(observation, configuration=None):
    try:
        _s3_apply(observation, int((observation or {}).get("step", 0)))
    except Exception:
        pass
    return _S3_PARENT(observation, configuration)


_hs_agent.telemetry = _S3_REPORT

# ---- 入口归一（末函数=_hs_agent；s3 尾块不改入口语义） ----
_S3_ENTRY_TMP = _hs_agent
del _hs_agent
_hs_agent = _S3_ENTRY_TMP
del _S3_ENTRY_TMP
''' % {"delta": delta_json,
       "adaptive": "True" if adaptive_on else "False"}
    preset = ({"h1_mirror": 1, "r37_2965_family": 1, "wfr": 1, "unknown": 1}
              if preset_mode == "safe" else
              {"h1_mirror": 0, "r37_2965_family": 0, "wfr": 1, "unknown": 0})
    tail = tail.replace("__T0_JSON__", json.dumps(t0))
    tail = tail.replace("__PRESET_JSON__", json.dumps(preset))
    return tail.replace("__SAFE_JSON__",
                        "True" if preset_mode == "safe" else "False")


# ============================================================ diff 审计 ==
def diff_audit(base_src: str, new_src: str, c3_cells, deltas, per_route):
    lb, ln = base_src.splitlines(), new_src.splitlines()
    sm = difflib.SequenceMatcher(None, lb, ln, autojunk=False)
    hunks = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        sample = " ".join(x[:120] for x in ln[j1:min(j2, j1 + 4)])
        hunks.append({"tag": tag, "a_lines": [i1 + 1, i2],
                      "b_lines": [j1 + 1, j2], "sample": sample[:300]})
    classes = {}
    for h in hunks:
        c = "s3:tail" if "S3 BUY5" in h["sample"] or h["tag"] == "insert" \
            else "unclassified"
        h["face"] = c
        classes[c] = classes.get(c, 0) + 1
    prefix_ok = new_src.startswith(base_src)
    tail = new_src[len(base_src):] if prefix_ok else ""
    s3_cells = set()
    for tier, per in deltas.items():
        for rid, cells in per.items():
            for k in cells:
                s3_cells.add((rid, int(k)))
    overlap = sorted(s3_cells & c3_cells)
    d_b, _, blob_b = decode_blob(base_src)
    d_n, _, blob_n = decode_blob(new_src)
    blob_same = blob_b == blob_n
    sell_markers = ["_s758", "_S758", "_s804", "_S804", "_r37_reorder",
                    "_v224_sales", "_m13_c3_restore", "FERTILIZE"]
    tail_hits = [m for m in sell_markers if m in tail]
    n_cells = sum(len(cells) for per in deltas.values()
                  for cells in per.values())
    return {
        "faces": {
            "s3_opening_trunk": {
                "src": "_alt_install 外壳协同（tape[0..1] market 重排）",
                "surface": "turn1-2 市场单（D6 族起手 + mooman 洗价形 13/30/30）",
            },
            "s3_adaptive_sheep": {
                "src": "尾块 _s3_apply（step≥144 换表；晚波羊链抑制阶梯）",
                "tier_cells_all": n_cells,
                "elastic_face": "SHEEP 数（GOOSE/COW/班组/单量/卖法=刚性面零触碰）",
                "per_route": per_route,
            },
            "c_final_unchanged": {
                "sell_face_touch": 0, "fert_touch": 0, "m13_touch": 0,
                "caliber": "卖面/肥配比/M13 决策码零引用（尾块 marker 扫描）；"
                           "磁带 blob 逐字节同源",
            },
        },
        "n_hunks": len(hunks),
        "hunk_classes": classes,
        "unclassified_hunks": classes.get("unclassified", 0),
        "tail_is_append_only": bool(prefix_ok),
        "tape_blob_identical": bool(blob_same),
        "sell_face_markers_in_tail": tail_hits,
        "c3_cells_overlap": overlap[:5],
        "zero_conflict": bool(prefix_ok and blob_same and not overlap
                             and not tail_hits
                             and classes.get("unclassified", 0) == 0),
    }


# ============================================================ 构建 ==
def build_one(src, deltas, adaptive_on, t0, preset_mode):
    delta_json = base64.b85encode(zlib.compress(
        json.dumps(deltas, separators=(",", ":")).encode("utf-8"), 9)
    ).decode("ascii")
    tail = make_tail(delta_json, adaptive_on, t0, preset_mode)
    injected = src + tail
    if injected[:-len(tail)] != src:
        raise RuntimeError("校验①红 反替换回程 != c_final 基底源")
    try:
        compile(injected, "<s3_buy5>", "exec")
    except Exception as exc:
        raise RuntimeError("校验②红 语法不通过: %r" % (exc,))
    ns = {}
    try:
        exec(compile(injected, "<s3_buy5>", "exec"), ns)
    except Exception as exc:
        raise RuntimeError("校验③红 exec 失败: %r" % (exc,))
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != "_hs_agent":
        raise RuntimeError("校验④红 末 callable=%r"
                           % (loaded[-1].__name__ if loaded else None,))
    for k in ("_S3_ALT_INSTALL", "_S3_OC_AFTER", "_S3_PARENT"):
        if ns.get(k) is None:
            raise RuntimeError("校验④红 捕获缺失 %s" % k)
    if ns.get("_S3_LATCHED") != [False]:
        raise RuntimeError("校验④红 闩初值漂移")
    return injected, tail


def main():
    t0 = time.perf_counter()
    base_bytes = CFINAL.read_bytes()
    sha = hashlib.sha256(base_bytes).hexdigest()
    if sha != CFINAL_SHA:
        raise RuntimeError("c_final 基底 sha 漂移: %s" % sha)
    src = base_bytes.decode("utf-8")
    d, c3, _ = decode_blob(src)
    acts, routes = d["actions"], d["routes"]
    c3_cells = {(rid, int(s)) for rid, per in c3.items() for s in per}
    deltas, per_route = build_tier_deltas(acts, routes, c3_cells)

    EVID_DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    audit = None
    forms = (("s3_buy5", True, OUT_FULL, S3_T0, "safe"),
             ("s3_open", False, OUT_OPEN, S3_T0, "safe"),
             ("s3_adapt0", True, OUT_ADAPT0, S3_T0, "act"),
             ("s3_wash", False, OUT_WASH, S3_T0_WASH, "safe"))
    for tag, on, outdir, form_t0, pmode in forms:
        injected, tail = build_one(src, deltas, on, form_t0, pmode)
        data = injected.encode("utf-8")
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "main.py").write_bytes(data)
        out[tag] = {"sha256": hashlib.sha256(data).hexdigest(),
                    "bytes": len(data), "adaptive_on": on}
        if tag == "s3_buy5":
            audit = diff_audit(src, injected, c3_cells, deltas, per_route)
            if not audit["zero_conflict"]:
                raise RuntimeError("校验⑤红 diff 审计未过: %r"
                                   % (audit.get("c3_cells_overlap"),))
            man = {
                "schema": SCHEMA, "form": "s3_buy5",
                "desc": "BUY5 开局复刻+洗价层+中盘畜群自适应（SHEEP 弹性面；"
                        "C_final 全层保留）",
                "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "base_main": str(CFINAL), "base_main_sha256": sha,
                "main_sha256": out[tag]["sha256"],
                "main_bytes": out[tag]["bytes"], "entry": "_hs_agent",
                "opening": {
                    "turn1": S3_T0, "turn2": S3_T1,
                    "sources": {
                        "d6_verbatim": "t1 COW1+WHEAT5±SHEEP、t2 SELL WHEAT1"
                                      "+HIRE×4+BUY COW+SHEEP（D6 实测）",
                        "wash_form": "mooman 公开概念洗价形 WHEAT 13/30/30"
                                    "（买 43 支撑 30 卖腿；原位 tape[0]）",
                        "d5_fingerprint": "D5 turn1 BUY COW+WHEAT(饲料)；"
                                          "turn2 SELL WHEAT+HIRE×4-5+COW+SHEEP",
                        "sheep_leg": "±SHEEP 腿未取（非冻结指纹；总量 2SHEEP "
                                     "落 turn2 防放置链断链）",
                    },
                },
                "adaptive": {
                    "preset": TIER_PRESET, "swing": SWING_PARAMS,
                    "tier_drops": TIER_DROPS,
                    "elastic_face": "SHEEP 数（GOOSE/COW/班组/单量/卖法=刚性面）",
                    "tier_cells_all": audit["faces"]["s3_adaptive_sheep"]
                    ["tier_cells_all"],
                    "chain_counts": {rid: v for rid, v in per_route.items()
                                     if v.get("0") or v.get("-1")},
                    "reversible": "step==0/step 回退还原+闩复位（M13 同模板）",
                },
                "diff_audit": audit,
                "roundtrip_identity_ok": True,
                "compile_ok": True, "exec_ok": True,
                "elapsed_s": round(time.perf_counter() - t0, 1),
            }
            (OUT_FULL / "build_manifest.json").write_text(
                json.dumps(man, ensure_ascii=False, indent=1, default=str)
                + "\n", encoding="utf-8")
    (EVID_DIR / "build_s3buy5.json").write_text(
        json.dumps({"version": "s3buy5-build/1.0", "base_sha256": sha,
                    "forms": out, "diff_audit": audit},
                   ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("built s3_buy5", out["s3_buy5"]["sha256"][:16],
          "s3_open", out["s3_open"]["sha256"][:16], flush=True)
    return out


if __name__ == "__main__":
    main()
