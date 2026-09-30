# -*- coding: utf-8 -*-
"""judge_unified_v3：D4 统一求解完全体判决（判决先行·不发射不提交）。

新评判标准（任务 D4 预登记，必须按此判）：
  ①直接对战强面板 {oc_c3 冠军锚, mpx, tetsutani, V89} n=16 双席——对强面板
    h2h ≥ 0.5 且对 oc_c3 ≥ 0.5（才算更强）；
  ②弱锚 {r40, A} ≥ 0.8；
  ③flips_neg=0（胜位守卫：冠军锚 oc_c3 同 (seed,seat,对手) 平行臂的胜位被
    翻负数=0；主判强面板 scope，弱/全 scope 附列——②的 0.8 阈与弱锚全翻守卫
    自相矛盾，弱锚 flips 仅台账）；
  ④实现价非负（配对 Δratio_fill 全品∧MILK 均值≥0；同局双侧+平行臂双口径）。
  margin 只作参考（分析44 镜像错觉定理：配对边际≠直接对战）。
设计：unified_v3 单核两形态同手术面（D5 平台语义并入）——v3k=peak（原设计
对照）、v3p=platform（主形态）；基底 oc_c3（sha 3f8b57fd）；n=16=26 败局前
8 fold+新中性 673000+i*137×8，双席=32 局/臂。sim_bridge 对照认证 30/30 先行；
workers=2；预算 ≤450 局次。读数：margin=banks 差；h2h=(W+0.5T)/n 直接口径。
证据落 fn_docs/hybrid/results/2026-09-30-d4-unified-v3.json；账本落
orderbook_unifiedv3_lab/evidence/。不改既有代码；不提交；不发射。
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import multiprocessing
import os
import sys
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
REPO = KSIM_DIR.parents[2]
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
sys.path.insert(0, str(MODULE_DIR))

import build_unified_v3 as B3  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "judge_unified_u2", KSIM_DIR / "orderbook_unified_u2_lab" /
    "judge_unified_u2.py")
J = importlib.util.module_from_spec(_spec)
sys.modules["judge_unified_u2"] = J
_spec.loader.exec_module(J)
JM = J.JM                                   # WINDOW 已置 d14-27（336,648）
G = J.G
G.ENTRY_NAME = "_u3_agent"

RECORD_VERSION = "d4-unified-v3/1.0"
LOSS_FOLDS = JM.REPLAY_26[:8]
NEUTRAL_FOLDS = [673000 + i * 137 for i in range(8)]   # 新中性 673000+i*137×8
FOLDS_ALL = LOSS_FOLDS + NEUTRAL_FOLDS

_PANEL = {
    "oc_c3": ("orderbook_oppcond_lab/build/oc_c3/main.py",
              "3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d39ba9bd23d"),
    "mpx": ("orderbook_modelpx_lab/build/mpx_w24_p2_3_h14/main.py",
            "f0101de9b558d1f56334739f9a49a0a0d4bc860a898792a9b69fc72c3d84e44f"),
    "tetsutani": ("/tmp/a30-b1/tetsu_agent/main.py",
                  "55be5d5f124c8daaaa63c1a29ba4aab096004909666f04748007603c67b7d2a8"),
    "V89": ("orderbook_v89_lab/build/v89_pure/main.py",
            "01ee3976f97a9ac71be40eff667b24c5a69cd86fce88bbbdf25ea1e10aecd60d"),
    "r40": ("orderbook_r40/build/main.py",
            "4ce951f088740e0b3d4366dbf95f8bb225817b0417bbb2fcea6292a559ee9ea8"),
    "A": ("orderbook_r44_a/main.py",
          "b387307fc12e26107c58ee604146fc621099ce88124fa0876fdd7cef28300bd9"),
}
STRONG = ["oc_c3", "mpx", "tetsutani", "V89"]
WEAK = ["r40", "A"]
CONTROL_OPPS = ["mpx", "tetsutani", "V89", "r40", "A"]   # 冠军锚平行臂对手


def _panel_path(name):
    rel, _ = _PANEL[name]
    p = Path(rel)
    return str(p if p.is_absolute() else KSIM_DIR / rel)


WORKERS = 2
BUDGET_CAP = 450
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-d4-unified-v3.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "judge_u3_ledger.json"

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


# ------------------------------------------------------------ 装载/追踪 --
def _load_agent_v3(path):
    """单文件件装载（末 callable 语义）+ 台账报告（_U3_REPORT）。"""
    p = os.path.abspath(str(path))
    with open(p, "r", encoding="utf-8") as fh:
        src = fh.read()
    ns = {}
    exec_dir = os.path.dirname(p)
    sys.path.append(exec_dir)
    try:
        exec(compile(src, p, "exec"), ns)
    finally:
        sys.path.remove(exec_dir)
    entries = [v for v in ns.values() if callable(v)]
    if not entries:
        raise ValueError("%s 装载后无 callable" % p)
    reports = {k: ns[k] for k in ("_U3_REPORT",)
               if isinstance(ns.get(k), dict)}
    return entries[-1], reports


class _Tracer(JM._Tracer):
    pass


def _build_agents(spec):
    out = []
    sinks = {0: [], 1: []}
    for seat, a in enumerate(spec["agents"]):
        inner, reports = _load_agent_v3(a["path"])
        out.append(_Tracer(inner, seat, sinks[seat], reports))
    return out, sinks


def u3_reads(sink):
    last = None
    for entry in (sink or []):
        tel = entry[3] if len(entry) > 3 else None
        if isinstance(tel, dict) and isinstance(tel.get("_U3_REPORT"), dict):
            last = tel["_U3_REPORT"]
    return dict(last) if isinstance(last, dict) else {"present": False}


def _run_chunk(payload):
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = _build_agents(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, None, {"build_error": repr(exc)[:120]}))
            continue
        metas.append((spec, sinks, None))
    res = sb.run_games(games, cfg) if games else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks, berr) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"game_id": spec.get("game_id"), "seed": int(spec["seed"]),
               "seat": int(spec.get("our_seat", 0)), "arm": spec.get("arm"),
               "opponent": spec.get("opponent"), "stratum": spec.get("stratum"),
               "banks": rr.get("banks"), "error": rr.get("error"),
               "margin": None, "reads": {}, "items": None, "shadow": None,
               "u3": None, "stream_sha_our": None}
        if berr is not None:
            row["error"] = berr["build_error"]
        if row["banks"] is not None and row["error"] is None and sinks:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - float(
                banks[1 - row["seat"]])
            our = sinks[row["seat"]]
            row["reads"] = JM.end_reads(our)
            row["items"] = JM.item_reads(our)
            row["u3"] = u3_reads(our)
            row["stream_sha_our"] = JM._stream_digest(our)
            row["shadow"] = JM.shadow_window(sinks, int(spec["seed"]))
        out.append(row)
    return {"rows": out, "engine": res.get("engine"),
            "fallback_reason": res.get("fallback_reason")}


def _play(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n_chunks = max(1, min(workers * 2, max(1, len(specs))))
    chunks = [specs[i::n_chunks] for i in range(n_chunks)]
    chunks = [c for c in chunks if c]
    tasks = [{"specs": c, "cfg": dict(cfg or {})} for c in chunks]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_run_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_run_chunk, tasks)
    rows = []
    engines = []
    for part in parts:
        rows.extend(part["rows"])
        engines.append({"engine": part.get("engine"),
                        "fallback_reason": part.get("fallback_reason")})
    return rows, engines


def make_units(opp_path, opponent, stratum_prefix):
    units = []
    for seed in FOLDS_ALL:
        stratum = ("%s_loss" % stratum_prefix if seed in set(LOSS_FOLDS)
                   else "%s_neutral" % stratum_prefix)
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat,
                          "opp_path": opp_path, "opponent": opponent,
                          "stratum": stratum})
    return units


# ------------------------------------------------------------ 聚合 --
def direct_h2h(rows):
    """直接对战 h2h（margin 口径 W/L/T；n=16 双席=32 格）。"""
    n = w = l = t = 0
    margins = []
    for r in rows:
        if r.get("margin") is None:
            continue
        n += 1
        m = float(r["margin"])
        margins.append(m)
        if m > 0:
            w += 1
        elif m < 0:
            l += 1
        else:
            t += 1
    h2h = round((w + 0.5 * t) / n, 4) if n else None
    folds = {}
    for r in rows:
        if r.get("margin") is None:
            continue
        folds.setdefault(int(r["seed"]), []).append(
            1.0 if r["margin"] > 0 else (0.5 if r["margin"] == 0 else 0.0))
    fw = fl = ft = 0
    for s, sc in folds.items():
        avg = sum(sc) / len(sc)
        if avg >= 1.0:
            fw += 1
        elif avg <= 0.0:
            fl += 1
        else:
            ft += 1
    fold_h2h = round((fw + 0.5 * ft) / max(1, len(folds)), 4)
    return {"n": n, "W": w, "L": l, "T": t, "h2h": h2h,
            "margin_mean_ref": round(sum(margins) / n, 2) if n else None,
            "fold_dual_seat": {"W": fw, "L": fl, "T": ft, "h2h": fold_h2h}}


def _ratio_side(row, side, item=None):
    """单局实现价（fill 口径 ratio）：指定 seat 侧；全品或单品。"""
    sw = row.get("shadow") or {}
    by = (sw.get("per_item_by_seat") or {}).get(int(side)) or \
        (sw.get("per_item_by_seat") or {}).get(str(int(side))) or {}
    num = den = 0.0
    items = [item] if item else list(by.keys())
    for it in items:
        d = by.get(it) or by.get(str(it)) or {}
        base = float(JM.BASE_PX.get(it, 0) or 0)
        filled = float(d.get("filled") or 0)
        value = float(d.get("value") or 0)
        if base and filled:
            num += value
            den += filled * base
    return (num / den) if den else None


def realized_same_game(var_rows):
    """同局双侧实现价配对 Δ（v3p − oc_c3；32 直接局内完美配对市场）。"""
    out = {}
    for tag, item in (("all", None), ("milk", "MILK"), ("wool", "WOOL"),
                      ("strawberry", "STRAWBERRY")):
        deltas = []
        for r in var_rows:
            if r.get("margin") is None:
                continue
            side = int(r["seat"])
            vv = _ratio_side(r, side, item)
            vc = _ratio_side(r, 1 - side, item)
            if vv is None or vc is None:
                continue
            deltas.append(float(vv) - float(vc))
        out[tag] = {
            "n": len(deltas),
            "mean_delta": round(sum(deltas) / len(deltas), 4) if deltas
            else None,
            "nonneg": bool(deltas and (sum(deltas) / len(deltas)) >= 0)}
    out["nonneg_both"] = bool(out["all"]["nonneg"] and out["milk"]["nonneg"])
    out["nonneg_three"] = bool(out["milk"]["nonneg"] and out["wool"]["nonneg"]
                               and out["strawberry"]["nonneg"])
    return out


def realized_parallel(ctl_rows_by_opp, var_rows_by_opp):
    """平行臂实现价配对 Δ（v3p − 冠军锚；跨对手逐对合并，键含对手防碰撞）。"""
    out = {}
    for tag, item in (("all", None), ("milk", "MILK")):
        deltas = []
        for p, var_rows in var_rows_by_opp.items():
            ctl_map = {(r["seed"], r["seat"]): r
                       for r in ctl_rows_by_opp.get(p) or []}
            for r in var_rows:
                if r.get("margin") is None:
                    continue
                rc = ctl_map.get((r["seed"], r["seat"]))
                if not rc or rc.get("shadow") is None \
                        or r.get("shadow") is None:
                    continue
                vc = _ratio_side(rc, int(rc["seat"]), item)
                vv = _ratio_side(r, int(r["seat"]), item)
                if vc is None or vv is None:
                    continue
                deltas.append(float(vv) - float(vc))
        out[tag] = {
            "n": len(deltas),
            "mean_delta": round(sum(deltas) / len(deltas), 4) if deltas
            else None,
            "nonneg": bool(deltas and (sum(deltas) / len(deltas)) >= 0)}
    out["nonneg_both"] = bool(out["all"]["nonneg"] and out["milk"]["nonneg"])
    return out


def flips_agg(pair_stats_by_opp, opps):
    flips_neg = flips_pos = wc = wv = n = 0
    for o in opps:
        ps = pair_stats_by_opp.get(o) or {}
        flips_neg += int(ps.get("flips_neg") or 0)
        flips_pos += int(ps.get("flips_pos") or 0)
        wc += int(ps.get("win_control") or 0)
        wv += int(ps.get("win_variant") or 0)
        n += int(ps.get("n") or 0)
    return {"n": n, "flips_neg": flips_neg, "flips_pos": flips_pos,
            "win_control_oc_c3": wc, "win_variant_v3p": wv}


# ------------------------------------------------------------ 门 --
def gate_identity(pkg: Path, name: str):
    """identity 门：体积/成员/sha + 反提取回程逐字节=oc_c3 基座源。"""
    main_bytes = (pkg / "main.py").read_bytes()
    tar_bytes = (pkg / "submission.tar.gz").read_bytes()
    man = json.loads((pkg / "build_manifest.json").read_text(encoding="utf-8"))
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as tar:
        members = tar.getnames()
        inner = tar.extractfile("main.py").read()
    base = Path(man["base_main"]).read_bytes().decode("utf-8")
    tail = B3.build_block(B3.FORMS[name]["form"])
    stripped = main_bytes.decode("utf-8")
    extract_ok = stripped.endswith(tail + "\n")
    if extract_ok:
        stripped = stripped[:-(len(tail) + 1)]
        if stripped.endswith(B3.SEPARATOR):
            stripped = stripped[:-len(B3.SEPARATOR)]
    for old, new, cnt in reversed(B3.SUBS):
        if stripped.count(new) != cnt:
            extract_ok = False
            break
        stripped = stripped.replace(new, old)
    extract_ok = extract_ok and stripped == base
    sha_ok = (main_sha == man.get("main_sha256")
              and hashlib.sha256(tar_bytes).hexdigest()
              == man.get("tar_sha256"))
    ok = all([len(tar_bytes) < 100 * 1024 * 1024, members == ["main.py"],
              inner == main_bytes, sha_ok, extract_ok])
    return {"passed": ok, "main_sha256": main_sha,
            "tar_members": members, "inner_matches_disk": inner == main_bytes,
            "sha_matches_manifest": sha_ok,
            "reverse_extract_byte_identical_to_oc_c3_base": extract_ok,
            "base_main_sha256": hashlib.sha256(base.encode()).hexdigest()}


def run_gates(name, full=True):
    pkg = MODULE_DIR / "build" / name
    gates = {}
    fns = [("load", G._gate_load)]
    if full:
        fns += [("health", G._gate_health), ("determinism", G._gate_determinism)]
    for gname, fn in fns:
        try:
            gates[gname] = fn(pkg)
        except Exception as exc:
            gates[gname] = {"passed": False,
                            "error": "%s: %s" % (type(exc).__name__, exc)}
    try:
        gates["identity"] = gate_identity(pkg, name)
    except Exception as exc:
        gates["identity"] = {"passed": False,
                             "error": "%s: %s" % (type(exc).__name__, exc)}
    gates["overall"] = all(g.get("passed") for g in gates.values()
                           if isinstance(g, dict))
    return gates


def footprint_audit(var_rows):
    """足迹审计：判决级台账 + 零分歧局计数 + 648 后回基线计数。
    口径注记：同场基线臂（oc_c3×oc_c3 自对局）32 局次超出 450 预算，外部动作
    流恒等核验不做——零足迹以①反提取回程逐字节=oc_c3 基座（identity 门，仅
    8 站点+尾块可改）②decision_diff_steps 逐拍差分台账（kernel 决策与基线一致
    拍=动作逐字同，构造性成立）③错误回退基线计数 audit。"""
    keys = ("calls", "fires", "holds", "units", "base_fires", "mr_limited",
            "cap_limited", "half_fires", "peak_fulls", "platform_fires",
            "closing_fires", "errors", "post_win_base", "stranding_insured",
            "window_suppressed")
    agg = {k: 0 for k in keys}
    diff_steps = 0
    zero_diff_games = 0
    for r in var_rows:
        led = r.get("u3") or {}
        for k in keys:
            agg[k] += int(led.get(k) or 0)
        d = led.get("decision_diff_steps") or []
        diff_steps += len(d)
        if r.get("margin") is not None and not d:
            zero_diff_games += 1
    return {"passed": bool(agg["errors"] == 0),
            "ledger": agg, "decision_diff_steps_total": diff_steps,
            "zero_diff_games": zero_diff_games,
            "stream_identity_external": {
                "performed": False,
                "why": "同场基线臂 oc_c3×oc_c3 自对局 32 局次超 450 预算；"
                       "零足迹改以 identity 门反提取封印+决策差分台账审计"},
            "caliber": "非触发拍零足迹=kernel 决策与基线一致拍动作逐字同"
                       "（构造性：同 gate 结果+同 take→同 market_orders）；"
                       "decision_diff_steps 台账逐拍记录 fire/take 与基线差；"
                       "异常回退基线；648 后回基线 post_win_base 计数；"
                       "反提取回程逐字节=oc_c3 基座（identity 门）"}


# ------------------------------------------------------------ 主判 --
def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb
    t0 = time.perf_counter()
    for name, (rel, sha) in _PANEL.items():
        got = hashlib.sha256(Path(_panel_path(name)).read_bytes()).hexdigest()
        if got != sha:
            raise RuntimeError("面板成员 sha 漂移 %s: %s" % (name, got))

    budget = {"cap_局次": BUDGET_CAP, "auth_局次": 0, "gates_局次": 0,
              "judgment_局次": 0, "arms": {},
              "cap_scope": "全部局次（认证 60 + 四门 4 + 面板判决 384）≤450"}
    EV.update({
        "version": RECORD_VERSION,
        "experiment": ("D4 统一求解完全体 unified_v3：窗+模型核+半量门写成单一"
                       "连续空间求解器（卖时+卖量+窗联合优化），两形态同手术面对"
                       "照（v3k=peak 原设计 / v3p=platform D5 平台语义主形态）；"
                       "新判据=直接对战强面板 h2h≥0.5 且对 oc_c3≥0.5、弱锚≥0.8、"
                       "flips_neg=0、实现价非负；margin 只作参考"),
        "kernel": {
            "core": "单一连续空间求解器（每拍 MILK/WOOL/STRAWBERRY 单核决策；"
                    "CARROT 可选未启用，站点面 _S758_ITEMS 零改动）",
            "projection": "K=12 拍引擎公式价格轨迹（price(inv) 全表+城镇排水表"
                          "+R28 删失口径对手流），比较全用未取整连续价（u1v2 取整"
                          "修复件：取整丢分辨率→比较须连续空间）",
            "half_gate": "预测连续跌>$0.5→半量（drop_half 语义并入单核，≥1）",
            "v3k_peak": "柔窗 h14-22=1.0/h10-13,23=0.5/其余 0；现价≥连续投影峰"
                        "→全量（帽内）+MR≤0 截止（平局破向卖出）；窗将关闭末拍"
                        "清剩余；滞留保险",
            "v3p_platform": "D5 平台语义：小单持续放行不等峰（lot=max(1,帽 3/6/10"
                            "×窗权)）；跌幅>$0.5 半量保留；柔窗 d12-24 平台 "
                            "[288,576)=1.0/其余 0.5（产线节奏对齐）；连续空间比较"
                            "仅用于跌幅判定",
            "guards": "胜位守卫：648 后回基线+滞留保险（peak）；异常回退基线；"
                      "非触发拍零足迹；零跨拍挪量；磁带 blob 零触碰",
        },
        "design": {
            "base": "orderbook_oppcond_lab/build/oc_c3（sha 3f8b57fd…）",
            "surgery": "3 组字面量 8 站点替换（p_next 4+量帽 4；计数台账 4/1/3 + "
                       "反替换回程逐字节=基座源封印）；门字面量 4 处不动（哨兵"
                       "过门）；尾块注入（knee/expx/u1 先例）块首捕获 _hs_agent、"
                       "块尾末函数 _u3_agent",
            "components": "expx_lab 连续投影件/u1v2 取整修复件 + modelpx_lab "
                          "模型核 + unified_u2_lab drop_half 件（D5 平台语义"
                          "修订第三条款）",
            "corpus": {"loss_folds": LOSS_FOLDS, "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "673000+i*137（i=0..7）",
                       "n16": "败局 8 + 中性 8 =16 fold（n=16 双席=32 格/臂）"},
            "caliber": {
                "h2h": "直接同局（候选 vs 面板成员），margin=banks[our]−"
                       "banks[opp]，h2h=(W+0.5T)/n；另列双席折叠口径",
                "flips_neg": "冠军锚 oc_c3 平行臂同 (seed,seat,对手) 胜位翻负"
                             "（主判=强面板 scope；弱/全 scope 附列）",
                "realized": "Δratio_fill（v3p−oc_c3）同局双侧主口径+平行臂"
                            "对照；全品∧MILK 非负",
                "margin": "只作参考（分析44 镜像错觉：配对边际≠直接对战）"},
            "workers": WORKERS,
        },
        "source": {
            "commands": ["python3 orderbook_unifiedv3_lab/build_unified_v3.py",
                         "python3 orderbook_unifiedv3_lab/judge_unified_v3.py"],
            "forms": {"v3k": B3.FORMS["v3k"]["desc"],
                      "v3p": B3.FORMS["v3p"]["desc"]},
        },
        "gates": {}, "panel_pairs": {}, "criteria": {}, "verdict": {},
        "footprint_audit": {}, "budget": budget,
    })
    flush_evid()

    # ---- 1) sim_bridge 对照认证 30/30（不过即停） ----
    auth_corpus = list(LOSS_FOLDS) + list(NEUTRAL_FOLDS) + \
        [2026093001, 2026093002, 2026093003, 2026093004, 2026093005,
         2026093006, 2026093007, 2026093008, 2026093009, 2026093010,
         2026093011, 2026093012, 2026093013, 2026093014]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(MODULE_DIR / "evidence" / "sim_auth_record_v3.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "consistency_ok", "degraded",
                  "degraded_reason", "engine", "version")}
    EV["source"]["sim_auth"] = auth_lite
    budget["auth_局次"] = 60
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 2) 四门（v3p 全门；v3k 静态门） ----
    EV["gates"]["v3p"] = run_gates("v3p", full=True)
    budget["gates_局次"] += 4
    EV["gates"]["v3k"] = run_gates("v3k", full=False)
    for nm in ("v3p", "v3k"):
        if not EV["gates"][nm].get("overall"):
            ANOMALIES.append("%s 门未全过：%r" % (
                nm, {k: v.get("passed") for k, v in EV["gates"][nm].items()
                     if isinstance(v, dict)}))
    flush_evid()

    # ---- 3) 面板直接对战 + 冠军锚平行臂 ----
    def play_arm(arm, cand_path, units):
        rows, _ = _play(JM.make_specs(arm, cand_path, units), run_cfg)
        budget["judgment_局次"] += len(rows)
        budget["arms"][arm] = budget["arms"].get(arm, 0) + len(rows)
        bad = [r for r in rows if r.get("error")]
        if bad:
            ANOMALIES.append("%s: %d 局 error: %r"
                             % (arm, len(bad), bad[0].get("error")))
        return rows

    v3p_main = str(MODULE_DIR / "build" / "v3p" / "main.py")
    v3k_main = str(MODULE_DIR / "build" / "v3k" / "main.py")
    v3p_rows, v3k_rows, ctl_rows = {}, {}, {}
    for p in STRONG + WEAK:
        units = make_units(_panel_path(p), p, "d4")
        v3p_rows[p] = play_arm("v3p_vs_" + p, v3p_main, units)
        if p in CONTROL_OPPS:
            ctl_rows[p] = play_arm("oc_c3_vs_" + p,
                                   _panel_path("oc_c3"), units)
    units_c3 = make_units(_panel_path("oc_c3"), "oc_c3", "d4")
    v3k_rows["oc_c3"] = play_arm("v3k_vs_oc_c3", v3k_main, units_c3)
    flush_evid()

    # ---- 4) panel_pairs 聚合 ----
    pair_stats_by_opp = {}
    for p in CONTROL_OPPS:
        units = make_units(_panel_path(p), p, "d4")
        ctl_map = {(r["seed"], r["seat"]): r for r in ctl_rows[p]}
        var_map = {(r["seed"], r["seat"]): r for r in v3p_rows[p]}
        pair_stats_by_opp[p] = JM.pair_stats(ctl_map, var_map, units)

    for p in STRONG + WEAK:
        pp = {"v3p_direct": direct_h2h(v3p_rows[p])}
        if p in CONTROL_OPPS:
            pp["oc_c3_control_direct"] = direct_h2h(ctl_rows[p])
            ps = pair_stats_by_opp[p]
            pp["paired_vs_oc_c3"] = {
                "flips_neg": ps.get("flips_neg"),
                "flips_pos": ps.get("flips_pos"),
                "win_control_oc_c3": ps.get("win_control"),
                "win_variant_v3p": ps.get("win_variant"),
                "mean_delta_ref": ps.get("mean_delta")}
        EV["panel_pairs"][p] = pp
    EV["panel_pairs"]["v3k_vs_oc_c3_对照"] = {"v3k_direct":
                                              direct_h2h(v3k_rows["oc_c3"])}

    def pooled_h2h(rows_by_p, plist):
        w = l = t = n = 0
        for p in plist:
            d = direct_h2h(rows_by_p[p])
            w += d["W"]
            l += d["L"]
            t += d["T"]
            n += d["n"]
        return {"n": n, "W": w, "L": l, "T": t,
                "h2h": round((w + 0.5 * t) / n, 4) if n else None}

    strong_pooled = pooled_h2h(v3p_rows, STRONG)
    weak_pooled = pooled_h2h(v3p_rows, WEAK)
    EV["panel_pairs"]["strong_pooled"] = strong_pooled
    EV["panel_pairs"]["weak_pooled"] = weak_pooled
    EV["panel_pairs"]["flips_scopes"] = {
        "strong": flips_agg(pair_stats_by_opp,
                            [p for p in CONTROL_OPPS if p in STRONG]),
        "weak": flips_agg(pair_stats_by_opp, WEAK),
        "all": flips_agg(pair_stats_by_opp, CONTROL_OPPS)}

    # ---- 5) 实现价 + 足迹审计 ----
    EV["panel_pairs"]["realized_px"] = {
        "same_game_v3p_vs_oc_c3": realized_same_game(v3p_rows["oc_c3"]),
        "parallel_vs_oc_c3_control": realized_parallel(
            ctl_rows, {p: v3p_rows[p] for p in CONTROL_OPPS})}
    fp = footprint_audit(v3p_rows["oc_c3"])
    EV["footprint_audit"] = fp
    if not fp["passed"]:
        ANOMALIES.append("足迹审计未过：%r" % fp["violations"])

    # ---- 6) 判据 + verdict ----
    rp = EV["panel_pairs"]["realized_px"]["same_game_v3p_vs_oc_c3"]
    flips_strong = EV["panel_pairs"]["flips_scopes"]["strong"]["flips_neg"]
    h2h_oc3 = EV["panel_pairs"]["oc_c3"]["v3p_direct"]["h2h"]
    c = {
        "①强面板 h2h≥0.5 且对 oc_c3≥0.5": {
            "strong_pooled_h2h": strong_pooled["h2h"],
            "h2h_vs_oc_c3": h2h_oc3,
            "per_member": {p: EV["panel_pairs"][p]["v3p_direct"]["h2h"]
                           for p in STRONG},
            "passed": bool(strong_pooled["h2h"] is not None
                           and strong_pooled["h2h"] >= 0.5
                           and h2h_oc3 is not None and h2h_oc3 >= 0.5)},
        "②弱锚 {r40,A} h2h≥0.8": {
            "weak_pooled_h2h": weak_pooled["h2h"],
            "per_member": {p: EV["panel_pairs"][p]["v3p_direct"]["h2h"]
                           for p in WEAK},
            "passed": bool(weak_pooled["h2h"] is not None
                           and weak_pooled["h2h"] >= 0.8)},
        "③flips_neg==0": {
            "scope": "主判=强面板（mpx/tetsutani/V89）；弱/全 scope 附列"
                     "（②0.8 阈与弱锚全翻守卫自相矛盾，弱锚 flips 仅台账）",
            "flips_neg_strong": flips_strong,
            "flips_neg_weak": EV["panel_pairs"]["flips_scopes"]["weak"][
                "flips_neg"],
            "flips_neg_all": EV["panel_pairs"]["flips_scopes"]["all"][
                "flips_neg"],
            "passed": flips_strong == 0},
        "④实现价非负": {
            "same_game_all_mean_delta": rp["all"]["mean_delta"],
            "same_game_milk_mean_delta": rp["milk"]["mean_delta"],
            "nonneg_both": rp["nonneg_both"],
            "nonneg_three": rp.get("nonneg_three"),
            "parallel_mean_delta": EV["panel_pairs"]["realized_px"][
                "parallel_vs_oc_c3_control"].get("all"),
            "passed": bool(rp["nonneg_both"])},
        "margin 只作参考": {
            "per_member_margin_mean": {
                p: EV["panel_pairs"][p]["v3p_direct"]["margin_mean_ref"]
                for p in STRONG + WEAK},
            "note": "分析44 镜像错觉：配对边际≠直接对战；margin 不入判"},
    }
    EV["criteria"] = c
    passed = all(v.get("passed") for k, v in c.items() if k.startswith(("①", "②", "③", "④")))
    EV["verdict"] = {
        "criteria_passed": passed,
        "positive_arm": passed,
        "h2h_strong_pooled": strong_pooled["h2h"],
        "h2h_vs_oc_c3": h2h_oc3,
        "h2h_weak_pooled": weak_pooled["h2h"],
        "flips_neg_strong": flips_strong,
        "v3k_vs_v3p_对照": {
            "v3k_h2h_vs_oc_c3": EV["panel_pairs"]["v3k_vs_oc_c3_对照"][
                "v3k_direct"]["h2h"],
            "v3p_h2h_vs_oc_c3": h2h_oc3,
            "winner": ("v3p" if (EV["panel_pairs"]["v3k_vs_oc_c3_对照"]
                                 ["v3k_direct"]["h2h"] or 0) < (h2h_oc3 or 0)
                       else "v3k")},
        "verdict": ("CONFIRMED（四判据全过；才算更强）" if passed else
                    "NOT_CONFIRMED（见 criteria 逐条）"),
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    budget["total_局次"] = (budget["auth_局次"] + budget["gates_局次"]
                            + budget["judgment_局次"])
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP
    if not budget["within_cap"]:
        ANOMALIES.append("预算超限：%r" % budget)
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    LEDGER_PATH.write_text(json.dumps(
        {"budget": budget, "criteria": EV["criteria"],
         "panel_h2h": {p: EV["panel_pairs"][p]["v3p_direct"]["h2h"]
                       for p in STRONG + WEAK},
         "flips_scopes": EV["panel_pairs"]["flips_scopes"]},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("VERDICT:", json.dumps(EV["verdict"], ensure_ascii=False,
                                 default=str)[:600], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
