# -*- coding: utf-8 -*-
"""judge_r44 及择优面子件（R27）。

责任契约（fn_docs/hybrid/responsibility.md【R27 增补】）：判决 v27——
三形态（A/B/AB）×同局配对（vs r40 同 seed 双席）+单件消融（B 效应=AB vs A
边际）+安慰剂臂（B 单≡r40 逐字节等价面；A 非触发拍零足迹）；判据=A 臂实现价
≥0.80（局级中位）∧ 终局钱 +2k~4k/局 ∧ h2h ≥0.55；B 臂=等价面恒等 ∧ AB 边际
>0；聚合 evidence（source 记可复跑命令+seed 登记）。单局红计入不短路。

复用（不立桩）：realized_price_stats=orderbook_r43/judge_r26 import
（缺失时按其签名薄封装，报告登记）；判决机器=orderbook_r40/judge_r23
（_build_agents/_load_entry/_call_inner）+orderbook_r40/sim_bridge——
seated 双席位、同 seed 配对口径照抄 judge_r26._chunk；语料接口=局集
（seeds）配置化（corpus 传 seeds 局集，缺省走 config.seed_base）。

evidence JSON 契约：{_generated_at, source:{commands, seed_base},
arms:[{arm,n,wins,losses,ties,mean_margin}], criteria:{...}, verdict}。
verdict∈POSITIVE|NEGATIVE|KILLED（安慰剂破防=仪器失守→KILLED）。
"""
from __future__ import annotations

import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

MODULE_DIR = Path(__file__).resolve().parent
_KSIM = str(MODULE_DIR.parent)
if _KSIM not in sys.path:
    sys.path.insert(0, _KSIM)

RECORD_VERSION = "judge-r44/1.0"
UNKNOWN = "UNKNOWN"
FORMS = ("A", "B", "AB")
SEED_BASE = 660000                  # 与 judge_r26(640000)/gates_r43(650000) 错开
N_SEEDS_DEFAULT = 60                # 每臂 seed 数（×双席）
N_FACE_SEEDS_DEFAULT = 2            # 安慰剂面（等价面/零足迹）参考局数
REALIZED_BAR = 0.80                 # 判据：A 臂实现价（局级中位）
TERMINAL_BAND = (2000.0, 4000.0)    # 判据：终局钱 +2k~4k/局（带外=红）
H2H_BAR = 0.55                      # 判据：h2h
MIN_QUOTE = 2.0                     # quote<2 品永不触发（detect_dayhigh 同口径）
DAYHIGH_ITEMS = ("EGG", "MILK", "WOOL", "CARROT", "TOMATO", "STRAWBERRY",
                 "MELON")           # 七品（R27 增补原文）
SCORING_PAIR = ["r34a-new 56637411", "r44 本件"]
SCORING_PAIR_NOTE = ("本件=第 2 发，挤 r37 保 r40；计分对={r34a-new "
                     "56637411, 本件}")


# --------------------------------------------------------------- 复用件 --
def _realized_price_stats(states: Any) -> Dict[str, Any]:
    """实现价读数：judge_r26.realized_price_stats import 复用（不改写）；
    找不到→按其签名薄封装（口径一致，报告登记）。"""
    try:
        from orderbook_r43 import judge_r26 as j26  # noqa: WPS433
        return j26.realized_price_stats(states)
    except Exception:
        daily: Dict[Tuple[int, str], List[float]] = {}
        sells: List[Tuple[int, str, float, float]] = []
        for entry in (states or []):
            if not isinstance(entry, (list, tuple)) or len(entry) < 3:
                continue
            step, obs, act = entry[0], entry[1], entry[2]
            if not isinstance(obs, dict):
                continue
            prices = ((obs.get("market") or {}) if
                      isinstance(obs.get("market"), dict) else {}
                      ).get("prices") or {}
            day = int(step) // 24
            for item, px in (prices or {}).items():
                if isinstance(px, (int, float)) and not isinstance(px, bool):
                    daily.setdefault((day, str(item)), []).append(float(px))
            if isinstance(act, dict):
                for cmd in (act.get("market") or []):
                    if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                            and str(cmd[0]) == "SELL":
                        px = prices.get(str(cmd[1]))
                        if isinstance(px, (int, float)) \
                                and not isinstance(px, bool):
                            sells.append((day, str(cmd[1]), float(cmd[2]),
                                          float(px)))
        realized = UNKNOWN
        if sells:
            num = den = 0.0
            for day, item, qty, px in sells:
                pxs = daily.get((day, item)) or []
                avg = (sum(pxs) / len(pxs)) if pxs else px
                num += qty * px
                den += qty * avg
            realized = round(num / den, 4) if den > 0 else UNKNOWN
        return {"realized_px": realized, "terminal_money": UNKNOWN,
                "stranding": UNKNOWN}


def _run_rows(specs: Sequence[Dict[str, Any]],
              cfg: Any = None) -> List[Dict[str, Any]]:
    """局规格→行（口径照抄 judge_r26._chunk：seated 双席位、同 seed 配对；
    kind=face 局保留 states 供安慰剂面）。错误: 单局红计入不短路。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    cfg = dict(cfg or {})
    games: List[Dict[str, Any]] = []
    metas: List[Tuple[Dict[str, Any], Any]] = []
    for spec in specs:
        try:
            agents, sinks = j23._build_agents(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, {"build_error": repr(exc)[:120]}))
            continue
        metas.append((spec, sinks))
    res = sb.run_games(games, cfg) if games else {"games": []}
    rows_run = list(res.get("games") or [])
    out: List[Dict[str, Any]] = []
    for i, (spec, sinks) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row: Dict[str, Any] = {
            "game_id": spec.get("game_id"), "seed": int(spec["seed"]),
            "seat": int(spec.get("our_seat", 0)), "arm": spec.get("arm"),
            "kind": spec.get("kind"), "banks": rr.get("banks"),
            "error": rr.get("error"), "margin": None, "reads": {},
            "states": None}
        if isinstance(sinks, dict) and "build_error" in sinks:
            row["error"] = sinks["build_error"]
            sinks = None
        if row["banks"] is not None and row["error"] is None:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - \
                float(banks[1 - row["seat"]])
            sink = sinks.get(row["seat"]) if isinstance(sinks, dict) \
                else None
            if sink is not None:
                if spec.get("kind") == "face":
                    row["states"] = list(sink)
                else:
                    row["reads"] = _realized_price_stats(sink)
        out.append(row)
    return out


# --------------------------------------------------------------- 小工具 --
def _is_num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _num(v: Any) -> Any:
    return v if _is_num(v) else UNKNOWN


def _resolve_main(path: Any) -> str:
    p = Path(str(path))
    if p.is_dir():
        p = p / "main.py"
    return str(p)


def _seeds_from(corpus: Any, seed_base: int, n_seeds: int) -> List[int]:
    """语料接口=局集配置化：seeds 列表或 {"seeds": [...]} 直用；否则
    seed_base 缺省局集（seed 登记进 evidence.source）。"""
    if isinstance(corpus, (list, tuple)) and corpus and \
            all(isinstance(s, int) and not isinstance(s, bool)
                for s in corpus):
        return [int(s) for s in corpus]
    if isinstance(corpus, dict) and isinstance(corpus.get("seeds"),
                                               (list, tuple)):
        seq = [int(s) for s in corpus["seeds"]
               if isinstance(s, int) and not isinstance(s, bool)]
        if seq:
            return seq
    return [seed_base + i for i in range(n_seeds)]


def _action_bytes(act: Any) -> bytes:
    """逐字节等价面的比对面：动作规范化 JSON 字节。"""
    return json.dumps(act, ensure_ascii=False, sort_keys=True,
                      default=str).encode("utf-8")


def _obs_struct():
    """obs 包装复用 gate_launch_fourgate_l1._to_struct（dict+属性双通道）。"""
    l1_dir = str(MODULE_DIR.parent / "orderbook_l1_derivative")
    if l1_dir not in sys.path:
        sys.path.insert(0, l1_dir)
    import gate_launch_fourgate_l1 as l1g  # noqa: WPS433
    return l1g._to_struct


def _trigger_steps(states: Sequence[Any]) -> Set[int]:
    """非触发拍判定面（超集口径）：quote≥2 且（换日首拍∨严格新高）计触发。
    取超集防 detect_dayhigh 边界口径差异误红——非触发拍零足迹只在确定
    非新高拍拉红。"""
    highs: Dict[Tuple[int, str], float] = {}
    triggers: Set[int] = set()
    for entry in states or []:
        if not isinstance(entry, (list, tuple)) or len(entry) < 3:
            continue
        step, obs = entry[0], entry[1]
        if not isinstance(obs, dict):
            continue
        step = int(step)
        prices = ((obs.get("market") or {}) if
                  isinstance(obs.get("market"), dict) else {}
                  ).get("prices") or {}
        day = step // 24
        for item in DAYHIGH_ITEMS:
            q = prices.get(item)
            if not _is_num(q) or float(q) < MIN_QUOTE:
                continue
            key = (day, item)
            prior = highs.get(key)
            if prior is None or float(q) > prior:
                triggers.add(step)
            highs[key] = float(q) if prior is None else max(prior, float(q))
    return triggers


def _face_divergences(arm_main: str,
                      states: Sequence[Any]) -> Dict[str, Any]:
    """安慰剂面：形态末 callable 逐拍驱动在 r40 自打参考轨迹上逐步对字节。
    B 单=全轨迹逐字节恒等；A=差异拍⊆触发面（非触发拍零足迹）。
    错误: 装载/驱动异常→记 error 并按破防计（fail-closed）。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    out: Dict[str, Any] = {"diff_steps": [], "violations": [],
                           "trigger_steps": [], "byte_identical": False,
                           "zero_footprint": False, "error": None}
    try:
        fn = j23._load_entry(str(arm_main))
    except Exception as exc:
        out["error"] = "load: %s" % repr(exc)[:120]
        return out
    try:
        wrap = _obs_struct()
    except Exception:
        wrap = None
    triggers = _trigger_steps(states)
    out["trigger_steps"] = sorted(triggers)
    for entry in states or []:
        if not isinstance(entry, (list, tuple)) or len(entry) < 3:
            continue
        step, obs, act_ref = int(entry[0]), entry[1], entry[2]
        try:
            drive = wrap(obs) if wrap is not None else obs
            act = j23._call_inner(fn, drive, None)
        except Exception as exc:
            out["violations"].append(step)
            out["error"] = "drive@%d: %s" % (step, repr(exc)[:80])
            continue
        if _action_bytes(act) != _action_bytes(act_ref):
            out["diff_steps"].append(step)
            if step not in triggers:
                out["violations"].append(step)
    out["byte_identical"] = not out["diff_steps"] and out["error"] is None
    out["zero_footprint"] = not out["violations"] and out["error"] is None
    return out


def _fold_arm(rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """同 seed 双席折叠为独立局（席位翻转不双计；分析20 playbook 口径）：
    score=两席均分（胜 1.0/平 0.5/负 0.0），≥1.0 胜、≤0.0 负、余平；
    缺席/红局→该 seed 记负（fail-closed）。h2h=(胜+0.5平)/独立 n。"""
    pairs: Dict[Any, List[Dict[str, Any]]] = {}
    for r in rows or []:
        pairs.setdefault(r.get("seed"), []).append(r)
    wins = losses = ties = 0
    margins: List[float] = []
    for seed in sorted(pairs):
        rs = pairs[seed]
        ms = [float(r["margin"]) for r in rs if _is_num(r.get("margin"))]
        if len(rs) != 2 or len(ms) != 2:
            losses += 1
            margins.extend(ms)
            continue
        score = sum(1.0 if m > 0 else 0.5 if m == 0 else 0.0
                    for m in ms) / 2.0
        margins.append(sum(ms) / 2.0)
        if score >= 1.0:
            wins += 1
        elif score <= 0.0:
            losses += 1
        else:
            ties += 1
    n = len(pairs)
    return {"n": n, "wins": wins, "losses": losses, "ties": ties,
            "h2h": round((wins + 0.5 * ties) / n, 4) if n else UNKNOWN,
            "mean_margin": round(sum(margins) / len(margins), 1) if margins
            else UNKNOWN}


# --------------------------------------------------------------- 判决面 --
def judge_r44(packages: Any, corpus: Any = None,
              config: Any = None) -> Dict[str, Any]:
    """判决 v27。签名意图：输入: 三形态包+语料+配置 / 输出: evidence JSON
    （逐形态逐局 Δ+判据表） / 错误: 单局红计入不短路。"""
    if not isinstance(packages, dict) or \
            any(f not in packages for f in FORMS):
        raise ValueError("packages 须含 A/B/AB 三形态路径")   # fail-closed
    cfg = dict(config) if isinstance(config, dict) else {}
    mains = {f: _resolve_main(packages[f]) for f in FORMS}
    r40 = str(cfg.get("r40_main") or MODULE_DIR.parent / "orderbook_r40" /
              "build" / "main.py")
    n_seeds = int(cfg.get("n_seeds", N_SEEDS_DEFAULT))
    seed_base = int(cfg.get("seed_base", SEED_BASE))
    n_face = max(1, min(int(cfg.get("n_face_seeds", N_FACE_SEEDS_DEFAULT)),
                        max(1, n_seeds)))
    seeds = _seeds_from(corpus, seed_base, n_seeds)
    run_cfg: Dict[str, Any] = {"engine": cfg.get("engine", "auto"),
                               "workers": int(cfg.get("workers", 16))}
    if cfg.get("bridge") is not None:
        run_cfg["bridge"] = cfg["bridge"]
    t0 = time.perf_counter()

    # 配对局：三形态 × 同 seed 双席 vs r40（同局配对）
    arm_rows: Dict[str, List[Dict[str, Any]]] = {}
    for form in FORMS:
        specs = []
        for seed in seeds:
            for seat in (0, 1):
                a = {"type": "python", "path": mains[form]}
                b = {"type": "python", "path": r40}
                agents = [a, b] if seat == 0 else [b, a]
                specs.append({"game_id": "j44-%s-%d-s%d" % (form, seed, seat),
                              "seed": seed, "kind": "pair", "arm": form,
                              "our_seat": seat, "trace": True,
                              "agents": agents})
        arm_rows[form] = _run_rows(specs, run_cfg)

    # 安慰剂参考面：[r40, r40] 自打同 seed 取 seat0 轨迹
    face_specs = [{"game_id": "j44-face-%d" % seed, "seed": seed,
                   "kind": "face", "arm": "face", "our_seat": 0,
                   "trace": True,
                   "agents": [{"type": "python", "path": r40},
                              {"type": "python", "path": r40}]}
                  for seed in seeds[:n_face]]
    face_rows = _run_rows(face_specs, run_cfg)

    # 读数聚合（局级中位/独立 n 折叠）
    stats: Dict[str, Dict[str, Any]] = {}
    for form in FORMS:
        rows = arm_rows[form]
        fold = _fold_arm(rows)
        pxs = [float(r["reads"]["realized_px"]) for r in rows
               if isinstance(r.get("reads"), dict)
               and _is_num(r["reads"].get("realized_px"))]
        fold["realized_px_median"] = round(statistics.median(pxs), 4) \
            if pxs else UNKNOWN
        stats[form] = fold

    marginal = UNKNOWN
    if _is_num(stats["AB"]["mean_margin"]) and _is_num(stats["A"]["mean_margin"]):
        marginal = round(float(stats["AB"]["mean_margin"])
                         - float(stats["A"]["mean_margin"]), 1)

    # 安慰剂面：B 单≡r40 逐字节等价；A 非触发拍零足迹
    face: Dict[str, Any] = {}
    for form in ("A", "B"):
        per_seed = []
        for row in face_rows:
            states = row.get("states") or []
            if row.get("error") or not states:
                per_seed.append({"seed": row.get("seed"),
                                 "error": row.get("error") or "无参考轨迹",
                                 "diff_steps": [], "violations": [],
                                 "byte_identical": False,
                                 "zero_footprint": False})
                continue
            per_seed.append(dict({"seed": row.get("seed")},
                                 **_face_divergences(mains[form], states)))
        ok = bool(per_seed) and all(not s.get("error") for s in per_seed)
        face[form] = {
            "per_seed": per_seed,
            "byte_identical": bool(ok and all(s.get("byte_identical")
                                              for s in per_seed)),
            "zero_footprint": bool(ok and all(s.get("zero_footprint")
                                              for s in per_seed))}
    placebo = {
        "a_zero_footprint": {
            "value": face["A"]["zero_footprint"], "per_seed":
            face["A"]["per_seed"],
            "verdict": "PASS" if face["A"]["zero_footprint"] else "FAIL"},
        "b_equiv_face": {
            "value": face["B"]["byte_identical"], "per_seed":
            face["B"]["per_seed"],
            "verdict": "PASS" if face["B"]["byte_identical"] else "FAIL"}}

    # 判据表：A 臂 3 项；B 臂=等价面恒等∧AB 边际>0；AB=A 3 项+边际
    def _chk(value: Any, ok: bool, bar: Any = None) -> Dict[str, Any]:
        d: Dict[str, Any] = {"value": value,
                             "verdict": "PASS" if ok else "FAIL"}
        if bar is not None:
            d["bar"] = bar
        return d

    crit: Dict[str, Any] = {}
    for form in FORMS:
        s = stats[form]
        px, tm, h2h = s["realized_px_median"], s["mean_margin"], s["h2h"]
        checks: Dict[str, Any] = {}
        if form == "B":
            # B 臂判据=等价面恒等∧AB 边际>0（R27 原文两项）
            checks["equiv_face_identity"] = _chk(
                face["B"]["byte_identical"], face["B"]["byte_identical"])
        else:
            checks["realized_px_median"] = _chk(
                px, _is_num(px) and float(px) >= REALIZED_BAR, REALIZED_BAR)
            checks["terminal_money_delta"] = _chk(
                tm, _is_num(tm)
                and TERMINAL_BAND[0] <= float(tm) <= TERMINAL_BAND[1],
                list(TERMINAL_BAND))
            checks["h2h"] = _chk(h2h, _is_num(h2h)
                                 and float(h2h) >= H2H_BAR, H2H_BAR)
        if form in ("B", "AB"):
            checks["ab_marginal"] = _chk(marginal, _is_num(marginal)
                                         and float(marginal) > 0, 0.0)
        achieved = sum(1 for c in checks.values()
                       if c["verdict"] == "PASS")
        crit[form] = {"checks": checks, "achieved": achieved,
                      "total": len(checks), "h2h": _num(h2h),
                      "realized_px": _num(px),
                      "verdict": "PASS" if achieved == len(checks)
                      else "FAIL"}
    crit["placebo"] = placebo

    instrument_ok = bool(placebo["a_zero_footprint"]["value"]
                         and placebo["b_equiv_face"]["value"])
    if not instrument_ok:
        verdict = "KILLED"          # 安慰剂破防→证据污染，族判死
    elif any(crit[f]["verdict"] == "PASS" for f in FORMS):
        verdict = "POSITIVE"
    else:
        verdict = "NEGATIVE"

    params = json.dumps(
        {"packages": mains,
         "corpus": corpus if isinstance(corpus, (list, dict, str)) else None,
         "config": {k: v for k, v in cfg.items()
                    if isinstance(v, (int, float, bool, str, type(None)))}},
        ensure_ascii=False, sort_keys=True)
    command = ("python3 -c \"import json,sys;sys.path.insert(0,%r);"
               "from orderbook_r44.judge_r44 import judge_r44;"
               "p=json.loads(%r);print(json.dumps(judge_r44(p['packages'],"
               " p['corpus'], p['config']), ensure_ascii=False,"
               " default=str))\"" % (_KSIM, params))

    evidence: Dict[str, Any] = {
        "_generated_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "version": RECORD_VERSION,
        "source": {"commands": [command], "seed_base": seed_base,
                   "n_seeds": len(seeds), "seeds": list(seeds),
                   "r40_main": str(r40)},
        "arms": [{"arm": f, "n": stats[f]["n"], "wins": stats[f]["wins"],
                  "losses": stats[f]["losses"], "ties": stats[f]["ties"],
                  "mean_margin": stats[f]["mean_margin"]} for f in FORMS],
        "arm_reads": stats,
        "ablation": {"b_effect": {"value": marginal, "bar": 0.0,
                                  "note": "B 效应=AB vs A 边际",
                                  "verdict": "PASS" if _is_num(marginal)
                                  and float(marginal) > 0 else "FAIL"}},
        "placebo": placebo,
        "criteria": crit,
        "verdict": verdict,
        "elapsed_s": round(time.perf_counter() - t0, 2)}
    out_path = Path(cfg.get("evidence_path") or MODULE_DIR / "evidence" /
                    "judge_r44_realrun.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=1,
                                   default=str) + "\n", encoding="utf-8")
    evidence["evidence_path"] = str(out_path)
    return evidence


# --------------------------------------------------------------- 择优面 --
def pick_launch_form(evidence: Any) -> Dict[str, Any]:
    """择优单发（用户裁决）。签名意图：输入: evidence JSON / 输出:
    {launch_form, rationale, archived_forms}（+scores/scoring_pair） /
    错误: 无形态达标→不选（全收档）。评分序=判据达成数>h2h>实现价。"""
    ev = evidence if isinstance(evidence, dict) else {}
    crit = ev.get("criteria") or {}
    scoring_pair = {"pair": list(SCORING_PAIR), "note": SCORING_PAIR_NOTE}
    scores: Dict[str, Dict[str, Any]] = {}
    for form in FORMS:
        e = crit.get(form) or {}
        scores[form] = {"achieved": int(e.get("achieved") or 0),
                        "total": int(e.get("total") or 0),
                        "h2h": _num(e.get("h2h")),
                        "realized_px": _num(e.get("realized_px")),
                        "verdict": e.get("verdict")}

    def _rank_key(form: str):
        s = scores[form]
        h2h = float(s["h2h"]) if _is_num(s["h2h"]) else -1.0
        px = float(s["realized_px"]) if _is_num(s["realized_px"]) else -1.0
        return (-s["achieved"], -h2h, -px, FORMS.index(form))

    if ev.get("verdict") == "KILLED":
        return {"launch_form": None,
                "rationale": "判决 KILLED（安慰剂破防/仪器失守）→不选"
                             "（全收档）",
                "archived_forms": list(FORMS), "scores": scores,
                "scoring_pair": scoring_pair}
    eligible = [f for f in FORMS if scores[f]["verdict"] == "PASS"]
    if not eligible:
        return {"launch_form": None,
                "rationale": "无形态达标→不选（全收档）",
                "archived_forms": list(FORMS), "scores": scores,
                "scoring_pair": scoring_pair}
    ranked = sorted(eligible, key=_rank_key)
    winner = ranked[0]
    order_txt = ">".join("%s(达成%d/%d,h2h=%s,实现价=%s)" % (
        f, scores[f]["achieved"], scores[f]["total"], scores[f]["h2h"],
        scores[f]["realized_px"]) for f in ranked)
    return {"launch_form": winner,
            "rationale": "评分序（判据达成数>h2h>实现价）：%s；选定 %s"
                         "（唯一发射形态，落选收档）" % (order_txt, winner),
            "archived_forms": [f for f in FORMS if f != winner],
            "scores": scores, "scoring_pair": scoring_pair}
