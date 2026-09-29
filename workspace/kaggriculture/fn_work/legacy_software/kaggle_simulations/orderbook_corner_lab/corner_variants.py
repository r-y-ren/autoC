# -*- coding: utf-8 -*-
"""corner_variants（corner-cases）：H1 三改进角实测变体（care2/fertilize-on/dephase）。

责任口径（任务 corner-cases；分析40 表#3 + 建模轮未验结论首验）：
基底=orderbook_strongest_lab/build/h1/main.py（sha 76b5f842…）。三个变体：
- care2（建模轮"CARE 翻倍最优"首验）：磁带内动物格 CARE 动作翻倍——只在
  空闲手/可插拍位（op==['PASS'] 或空指令）插 ['CARE']，**不动 BUILD/PLANT/
  HARVEST/WATER/FEED 面**（一切非空指令零覆盖）；优先未照护 (格,日)（生效位）
  后补已照护位（引擎同日幂等=安全空转）；量守恒口径=既有 (unit,op) 多重集
  逐路由精确不变 + 插入计数==审计行数；**外壳硬断言格一律跳过**（route 0
  tape[2-6].hands[1]、tape[29].hands[2]、tape[49-57].hands[0]、tape[84-91].
  hands[0]、tape[2-4].hands[4]——触碰 tape[29] 类断言格即弃）。
- fertilize-on（"按吸收率定速"操作化）：引擎 FERTILIZE 吸收窗=fertilized_
  until_day=day+2（3 日）→ 定速=每 3 日对活跃植格补肥（d0,d0+3,…），同法在
  空闲手/可插拍位插 ['FERTILIZE']；无肥在仓=引擎静默空转（安全）。
- dephase（分析40 表#3 卖相位去集中）：禁区口径（同拍单集不动、跨拍不挪量、
  跨相位等价交换=红线）下唯一合法面=**日新高追加单挂拍轮转**——S928 日新高
  追加单不再落在触发拍，缓冲后挂到轮转目标相位（k%4 全相位轮转）首个同日
  拍；同品同量、只追加不改写既有单；日末/终局强制落挂。磁带零触碰（blob
  逐字节同构），手术=S928 追加行改缓冲 + 追加尾层挂拍（新文件变体壳）。
手术=写时复制（retape_sheep._cow_action/_commit_action 池语义）+_encode_routes
四重自检。审计=逐事件 change_table + 多重集守恒 + 画像前后。孪生三闸先行
（tape_variants.feasibility_twin 原件复用；现金/劳动/棚容，违规即弃）。
只写 orderbook_corner_lab/。
"""
from __future__ import annotations

import copy
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))

try:
    from orderbook_track1_lab import tape_variants as tv  # noqa: E402
except ImportError:  # 目录非包（无 __init__）：直插路径导入
    sys.path.insert(0, str(KSIM_DIR / "orderbook_track1_lab"))
    import tape_variants as tv  # noqa: E402
from orderbook_r37 import retape_sheep as rs  # noqa: E402

RECORD_VERSION = "corner-variants/1.0"
H1_MAIN = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
BUILD_DIR = MODULE_DIR / "build"
DAY = 24
ANIMALS = {"COW", "SHEEP", "GOOSE"}

# 外壳硬断言格（H1 main _alt_install/_CL_INSTALL 实据；route 0）：触碰即
# tape[29] 类断言格硬断言炸毁——一律跳过。
GUARD_CELLS = (
    {(s, "h1") for s in range(2, 7)}
    | {(29, "h2")}
    | {(s, "h0") for s in range(49, 58)}
    | {(s, "h0") for s in range(84, 92)}
    | {(s, "h4") for s in range(2, 5)}
)

IDLE_OPS = {None, tuple(), ("PASS",)}


def _op_key(op: Any) -> Tuple:
    if isinstance(op, list):
        return tuple(op)
    return tuple() if op is None else (str(op),)


def _slot_map(seq: List[Dict[str, Any]]) -> Dict[Tuple[int, str], List]:
    """(step, unit) → 指令（含空指令；farmer='F'，hands[i]='h{i}'）。"""
    out: Dict[Tuple[int, str], List] = {}
    for s, a in enumerate(seq):
        fu = a.get("farmer")
        if isinstance(fu, list):
            out[(s, "F")] = fu
        for i, h in enumerate(a.get("hands") or []):
            if isinstance(h, list):
                out[(s, "h%d" % i)] = h
    return out


def _route_ctx(pkg: Dict[str, Any], rid: str) -> Dict[str, Any]:
    """路由上下文：走位链 + 动物格/植格 + CARE 照护面 + FERTILIZE 面。"""
    idxs = pkg["routes"][rid]
    seq = [pkg["actions"][i] for i in idxs]
    blk = rs._derive_route_block(seq)
    if blk is None:
        return {"derive_ok": False}
    pos = blk["unit_pos"]
    anim_tiles: Dict[Any, Tuple[str, int]] = {}
    plant_tiles: Dict[Any, Dict[str, Any]] = {}
    cared: set = set()
    fert_days: Dict[Any, set] = {}
    care_n = 0
    fert_n = 0
    for s, a in enumerate(seq):
        day = s // DAY
        for u, op in rs._units(a):
            if not (isinstance(op, list) and len(op) > 1 and op[0] == "PLACE"):
                continue
            p = pos.get((s, u))
            if op[1] in ANIMALS and p is not None and p not in anim_tiles:
                anim_tiles[p] = (op[1], day)
        for u, op in rs._units(a):
            if not isinstance(op, list) or len(op) < 2:
                continue
            if op[0] == "PLANT":
                p = pos.get((s, u))
                if p is not None and p not in plant_tiles:
                    plant_tiles[p] = {"crop": op[1], "plant_day": day,
                                      "last_harvest_day": None}
            elif op[0] == "HARVEST":
                p = pos.get((s, u))
                if p in plant_tiles:
                    plant_tiles[p]["last_harvest_day"] = day
        for u, op in rs._units(a):
            if isinstance(op, list) and op and op[0] == "CARE":
                care_n += 1
                p = pos.get((s, u))
                if p in anim_tiles:
                    cared.add((p, day))
            elif isinstance(op, list) and op and op[0] == "FERTILIZE":
                fert_n += 1
                p = pos.get((s, u))
                if p in plant_tiles:
                    fert_days.setdefault(p, set()).add(day)
    return {"derive_ok": True, "seq": seq, "pos": pos, "slots": _slot_map(seq),
            "anim_tiles": anim_tiles, "plant_tiles": plant_tiles,
            "cared": cared, "fert_days": fert_days,
            "care_n": care_n, "fert_n": fert_n}


# ------------------------------------------------------------ CARE2 手术 --

def surgery_care2(pkg: Dict[str, Any], table: List[Dict[str, Any]]
                  ) -> Dict[str, Any]:
    """动物格 CARE 翻倍：空闲手/可插拍位插 ['CARE']（优先未照护 (格,日)）。

    只覆盖空指令（['PASS']/空列表）；硬断言格跳过；目标=既有 CARE 数翻倍
    （受可插位上限约束→shortfall 留档）。
    """
    stats = {"routes": 0, "derive_failed": 0, "events_base": 0,
             "inserted": 0, "inserted_eff": 0, "inserted_noop": 0,
             "shortfall": 0, "guarded_skipped": 0}
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        ctx = _route_ctx(pkg, rid)
        if not ctx.get("derive_ok"):
            stats["derive_failed"] += 1
            continue
        stats["routes"] += 1
        stats["events_base"] += ctx["care_n"]
        target = ctx["care_n"]          # 翻倍=再插 care_n 个
        if target <= 0:
            continue
        covered = set(ctx["cared"])
        cands_eff: List[Tuple[int, str, Any]] = []
        cands_noop: List[Tuple[int, str, Any]] = []
        for (s, u), op in sorted(ctx["slots"].items()):
            if _op_key(op) not in IDLE_OPS:
                continue
            p = ctx["pos"].get((s, u))
            if p not in ctx["anim_tiles"]:
                continue
            if rid == "0" and (s, u) in GUARD_CELLS:
                stats["guarded_skipped"] += 1
                continue
            if (p, s // DAY) not in covered:
                cands_eff.append((s, u, p))
                covered.add((p, s // DAY))   # 同 (格,日) 仅首个生效
            else:
                cands_noop.append((s, u, p))
        picks = (cands_eff + cands_noop)[:target]
        n_eff = min(len(cands_eff), len(picks))
        for s, u, p in picks:
            idxs, _idx, act = rs._cow_action(pkg, rid, s)
            old = list(dict(rs._units(act)).get(u) or [])
            rs._set_unit(act, u, ["CARE"])
            rs._commit_action(pkg, idxs, s, act)
            table.append({"route": rid, "kind": "care_insert", "step": s,
                          "unit": u, "tile": str(p), "from": old,
                          "to": ["CARE"], "status": "inserted"})
            stats["inserted"] += 1
        stats["inserted_eff"] += n_eff
        stats["shortfall"] += max(0, target - len(picks))
    stats["inserted_noop"] = stats["inserted"] - stats["inserted_eff"]
    return stats


# ------------------------------------------------------- fertilize-on 手术 --

def surgery_fert_on(pkg: Dict[str, Any], table: List[Dict[str, Any]]
                    ) -> Dict[str, Any]:
    """按吸收率定速施肥：3 日吸收窗（day..day+2）→ 每 3 日活跃植格补肥。

    空闲手/可插拍位插 ['FERTILIZE']；无肥在仓=引擎静默空转（安全）；硬断言格
    跳过；只覆盖空指令。
    """
    stats = {"routes": 0, "derive_failed": 0, "events_base": 0,
             "inserted": 0, "inserted_eff": 0, "shortfall": 0,
             "guarded_skipped": 0, "pace": "每 3 日/植格（引擎吸收窗 day..day+2）"}
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        ctx = _route_ctx(pkg, rid)
        if not ctx.get("derive_ok"):
            stats["derive_failed"] += 1
            continue
        stats["routes"] += 1
        stats["events_base"] += ctx["fert_n"]
        # 吸收率定速日程：d0, d0+3, … ≤ min(末次收获日, 29)
        sched: Dict[Tuple[Any, int], bool] = {}
        for p, meta in ctx["plant_tiles"].items():
            end = meta["last_harvest_day"]
            end = min(end if end is not None else 29, 29)
            d = meta["plant_day"]
            while d <= end:
                sched[(p, d)] = bool((p, d) not in ctx["fert_days"])
                d += 3
        target = sum(1 for v in sched.values() if v)   # 只补未施肥 (格,日)
        cands: Dict[Tuple[Any, int], Tuple[int, str]] = {}
        for (s, u), op in sorted(ctx["slots"].items()):
            if _op_key(op) not in IDLE_OPS:
                continue
            p = ctx["pos"].get((s, u))
            key = (p, s // DAY)
            if p not in ctx["plant_tiles"] or key not in sched:
                continue
            if rid == "0" and (s, u) in GUARD_CELLS:
                stats["guarded_skipped"] += 1
                continue
            if key not in cands:
                cands[key] = (s, u)
        picks = sorted(cands.items())
        n_eff = 0
        for key, (s, u) in picks:
            if not sched[key]:
                continue
            idxs, _idx, act = rs._cow_action(pkg, rid, s)
            old = list(dict(rs._units(act)).get(u) or [])
            rs._set_unit(act, u, ["FERTILIZE"])
            rs._commit_action(pkg, idxs, s, act)
            table.append({"route": rid, "kind": "fert_insert", "step": s,
                          "unit": u, "tile": str(key[0]), "day": key[1],
                          "from": old, "to": ["FERTILIZE"],
                          "status": "inserted"})
            stats["inserted"] += 1
            n_eff += 1
        stats["inserted_eff"] += n_eff
        stats["shortfall"] += max(0, target - len(cands))
    return stats


# ------------------------------------------------------------ 审计 --

def audit_insert(built: Dict[str, Any], pkg_base: Dict[str, Any]) -> Dict[str, Any]:
    """量守恒：非空闲件零丢失零改写；空闲（PASS/空）件只被插入 op 改写。"""
    vid = built["variant_id"]
    add_op = "CARE" if vid == "care2" else "FERTILIZE"
    rows = {}
    ok = True
    rids = sorted(set(r["route"] for r in built["table"])
                  or pkg_base["routes"].keys(), key=lambda k: int(k))
    n_inserted = sum(1 for r in built["table"] if r.get("status") == "inserted")
    for rid in rids:
        b = _route_ops(pkg_base, rid)
        v = _route_ops(built["pkg"], rid)
        lost = b - v
        gained = v - b
        lost_nonidle = {str(k): n for k, n in lost.items()
                        if k[1] not in ("PASS", "")}
        gained_other = {str(k): n for k, n in gained.items()
                        if k[1] != add_op}
        n_rows_rid = sum(1 for r in built["table"]
                         if r.get("status") == "inserted"
                         and str(r.get("route")) == str(rid))
        same = (not lost_nonidle and not gained_other
                and sum(gained.values()) == n_rows_rid)
        ok = ok and same
        rows[rid] = {"base_n": sum(b.values()), "var_n": sum(v.values()),
                     "lost_idle_pass": sum(lost.values()),
                     "lost_nonidle": lost_nonidle,
                     "gained": dict(gained),
                     "gained_other": gained_other,
                     "table_rows": n_rows_rid, "ok": bool(same)}
    return {"variant_id": vid, "conservation_ok": bool(ok),
            "conservation_note": "非空闲件零丢失零改写；空闲 PASS 仅被 %s"
            "插入改写；市场单零触碰（写时复制池语义）" % add_op,
            "n_table_rows": len(built["table"]), "n_inserted": n_inserted,
            "routes": rows}


def _route_ops(pkg: Dict[str, Any], rid: str) -> Counter:
    c: Counter = Counter()
    idxs = pkg["routes"][rid]
    for i in idxs:
        for u, op in rs._units(pkg["actions"][i]):
            c[(u, str(op[0]), str(op[1]) if len(op) > 1 else "")] += 1
    return c


# ------------------------------------------------------------ dephase 壳 --

# 日新高追加单簇（H1 step928/948 变现簇实据）四个纯追加点：S928（EGG/MILK/
# WOOL）、S948（CARROT/TOMATO/STRAWBERRY/MELON）、S932（step709 MILK 无
# 同品槽支）、S939（step693 MILK 无同品槽支）。同拍并单支（sell_idx 非空
# → 改写既有槽）属同拍并单不动面，不改。
_DP_PATCHES = [
    ("S928",
     "market.append(['SELL',item,qty])\n"
     "            added += 1; _S928_REPORT['units'] += qty",
     "_DH_DEPHASE_BUF.append([p, step, item, qty])\n"
     "            added += 1; _S928_REPORT['units'] += qty"),
    ("S948",
     "market.append(['SELL',item,qty])\n"
     "        result=dict(action,market=market)\n"
     "        _S948_REPORT['changed']+=1",
     "_DH_DEPHASE_BUF.append([p, step, item, qty])\n"
     "        result=dict(action,market=market)\n"
     "        _S948_REPORT['changed']+=1"),
    ("S932",
     "if sell_idx is None:\n"
     "            market.append(['SELL','MILK',qty])\n"
     "        else:",
     "if sell_idx is None:\n"
     "            _DH_DEPHASE_BUF.append([p, step, 'MILK', qty])\n"
     "        else:"),
    ("S939",
     "if sell_idx is None:market.append(['SELL','MILK',qty])\n"
     "        else:market[sell_idx][2]=int(market[sell_idx][2])+qty",
     "if sell_idx is None:_DH_DEPHASE_BUF.append([p, step, 'MILK', qty])\n"
     "        else:market[sell_idx][2]=int(market[sell_idx][2])+qty"),
]

_DP_TAIL = '''

# ==== corner-lab dephase 尾层（追加单相位去集中：日新高追加单挂拍轮转） ====
# 责任口径：日新高追加单簇（S928/S948/S932/S939 纯追加支）挂拍改轮转目标相位
# （k%4）首个同日拍；同品同量、只追加不改写既有单（同拍单集不动/跨拍不挪量
# 红线内）；日末(step%24==23)与终局强制落挂。磁带 blob 零触碰。
_DP_PARENT = agent
_DP_STATE = {}
_DP_REPORT = dict(created=0, created_units=0, hung=0, hung_units=0,
                  flush_eod=0, flush_end=0, slot_full=0, errors=0)


def _dp_agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    p = int(observation.get('player', 0))
    st = _DP_STATE.get(p)
    if st is None or step <= int(st.get('last', -1)):
        st = _DP_STATE[p] = {'last': -1, 'n': 0, 'buf': []}
        del _DH_DEPHASE_BUF[:]
    action = _DP_PARENT(observation, configuration)
    st['last'] = step
    try:
        mine = [e for e in _DH_DEPHASE_BUF if e[0] == p]
        if mine:
            del _DH_DEPHASE_BUF[:]
            for _pl, _s, item, qty in mine:
                st['buf'].append([item, qty, st['n'] % 4])
                st['n'] += 1
                _DP_REPORT['created'] += 1
                _DP_REPORT['created_units'] += int(qty)
        if not st['buf']:
            return action
        market = [list(o) for o in (action.get('market') or [])]
        keep = []
        force = (step % 24 == 23) or (step >= 719)
        for item, qty, tgt in st['buf']:
            if not force and (step % 4) != tgt:
                keep.append([item, qty, tgt])
                continue
            if len(market) >= 10:
                _DP_REPORT['slot_full'] += 1
                keep.append([item, qty, tgt])
                continue
            market.append(['SELL', item, qty])
            _DP_REPORT['hung'] += 1
            _DP_REPORT['hung_units'] += int(qty)
            if force:
                if step >= 719:
                    _DP_REPORT['flush_end'] += 1
                else:
                    _DP_REPORT['flush_eod'] += 1
        st['buf'] = keep
        return dict(action, market=market)
    except Exception:
        _DP_REPORT['errors'] += 1
        return action


_dp_agent.telemetry = _DP_REPORT
agent = _dp_agent
kaggle_submission_agent = _dp_agent
'''


def build_dephase(main_text: str) -> Dict[str, Any]:
    """dephase 壳手术：日新高追加单簇四纯追加点改缓冲 + 尾层挂拍轮转。

    新文件变体（不动既有代码）；锚点任一计数≠1 即弃（fail-closed）。
    """
    t0 = time.perf_counter()
    counts = {name: main_text.count(old) for name, old, _new in _DP_PATCHES}
    if any(c != 1 for c in counts.values()):
        return {"variant_id": "dephase", "ok": False,
                "error": "追加锚点计数须全=1: %s" % counts}
    new_text = main_text
    for name, old, new in _DP_PATCHES:
        new_text = new_text.replace(old, new, 1)
    new_text = new_text.replace(
        "def step928_multi_dayhigh_animal_product_sale_agent(observation, "
        "configuration=None):",
        "_DH_DEPHASE_BUF = []\n\n"
        "def step928_multi_dayhigh_animal_product_sale_agent(observation, "
        "configuration=None):", 1)
    new_text = new_text + _DP_TAIL
    try:
        compile(new_text, "<dephase_variant>", "exec")
    except Exception as exc:
        return {"variant_id": "dephase", "ok": False,
                "error": "compile 失败: %r" % exc}
    return {"variant_id": "dephase", "ok": True, "main_text": new_text,
            "patch": {
                "form": ("追加单相位去集中：日新高追加单簇（S928/S948/S932/S939 "
                         "纯追加支）挂拍 k%4 轮转全相位"),
                "tape_touched": False,
                "red_lines": ("同拍单集不动（既有单零改写，只追加；同拍并单支"
                              "不动）；跨拍不挪量（磁带卖单零触碰；追加单=同拍"
                              "追加族的挂拍选择，非既有单挪量）；跨相位同品同量"
                              "等价交换=红线未做"),
                "lines_patched": [
                    "%s 追加行→_DH_DEPHASE_BUF 缓冲" % n
                    for n, _o, _n2 in _DP_PATCHES]
                + ["尾层 _dp_agent 挂拍 k%4 轮转+日末/终局强制落挂"],
                "anchor_counts": counts},
            "elapsed_s": round(time.perf_counter() - t0, 2)}


# ------------------------------------------------------------ 构建 --

def build_variant(vid: str, pkg_base: Dict[str, Any], main_text: str
                  ) -> Dict[str, Any]:
    """磁带手术变体构建：手术→审计→编码（四重自检）→main 文本。"""
    if vid not in ("care2", "fert_on"):
        raise ValueError("未知磁带变体: %r" % vid)
    work = copy.deepcopy(pkg_base)
    table: List[Dict[str, Any]] = []
    t0 = time.perf_counter()
    if vid == "care2":
        stats = surgery_care2(work, table)
    else:
        stats = surgery_fert_on(work, table)
    rs._pool_residue_sweep(work)
    new_text = rs._encode_routes(main_text, work)
    aud = audit_insert({"variant_id": vid, "table": table, "pkg": work},
                       pkg_base)
    return {"variant_id": vid, "pkg": work, "table": table, "stats": stats,
            "audit": aud, "main_text": new_text,
            "elapsed_s": round(time.perf_counter() - t0, 2)}


def twin_check(built: Dict[str, Any], pkg_base: Dict[str, Any],
               rids: List[str]) -> Dict[str, Any]:
    """孪生三闸（tape_variants.feasibility_twin 原件复用；违规即弃）。"""
    return tv.feasibility_twin(built["pkg"], pkg_base, rids)
