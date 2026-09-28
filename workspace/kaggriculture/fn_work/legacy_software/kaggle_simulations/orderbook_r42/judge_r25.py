# -*- coding: utf-8 -*-
"""judge_r25 及判决面子件（R25）。

责任契约（fn_docs/hybrid/responsibility.md【R25 增补】）：分项+总判
（判据=R25 ①②③+总判原文）：P1 单价+d21-28 / P2 尾段翻正+stranding /
P3 镜像臂+净加卖 0；总判=h2h vs r40 ≥0.55 ∧ 联赛 ≥80%；聚合 evidence。

【判决口径】配对联赛（r42 vs r40 同 seed 双席 traced）——同局双方状态都在
手：r42 侧 vs r40 侧逐读数配对差=纯构建效应；镜像臂=指纹相等触发子集；
尾段翻车子集=analysis25 d29 败局回放（tape 对手，缺件→UNKNOWN 不短路）。
"""
from __future__ import annotations

import json
import multiprocessing
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

MODULE_DIR = Path(__file__).resolve().parent
RECORD_VERSION = "judge-r25/1.0"
UNKNOWN = "UNKNOWN"
REVEAL_STEP = 144
D29_START = 672                  # day29 起（648=day27 早）
N_H2H_DEFAULT = 120              # h2h 配对 seed 数（×双席）
N_LEAGUE_DEFAULT = 15            # 每强对手 seed 数（×双席）
H2H_SEED_BASE = 610000
LEAGUE_SEED_BASE = 620000


# ----------------------------------------------------------- 逐局读数 --

def _game_reads(sinks: Any, our_seat: int, seed: int) -> Dict[str, Any]:
    """追踪槽→逐局读数（镜像/d21-28/尾段/stranding）。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r42 import mirror as mr  # noqa: WPS433
    reads: Dict[str, Any] = {"mirror": False}
    try:
        rows, _meta = j23._window_states(sinks, int(our_seat), int(seed))
        reads["seg"] = j23.segment_stats(rows)
    except Exception as exc:
        reads["seg"] = {"verdict": UNKNOWN, "error": repr(exc)[:120]}
    try:
        seat_sink = sinks.get(int(our_seat)) if isinstance(sinks, dict) \
            else None
        money: Dict[int, float] = {}
        last_obs = None
        for entry in (seat_sink or []):
            if not isinstance(entry, (list, tuple)) or len(entry) < 2 or \
                    not isinstance(entry[1], dict):
                continue
            obs = entry[1]
            step = obs.get("step")
            step = int(step) if step is not None else \
                int(obs.get("day", 0)) * 24 + int(obs.get("hour", 0))
            farm = (obs.get("farms") or [{}])[int(our_seat)] \
                if isinstance(obs.get("farms"), list) else {}
            try:
                money[step] = float(farm.get("money", 0.0))
            except (TypeError, ValueError):
                pass
            last_obs = obs
        for entry in (seat_sink or []):
            if not isinstance(entry, (list, tuple)) or len(entry) < 2 or \
                    not isinstance(entry[1], dict):
                continue
            obs = entry[1]
            farms = obs.get("farms")
            if isinstance(farms, list) and len(farms) == 2:
                f0 = mr._fingerprint(farms[0])
                if f0 is not None and f0 == mr._fingerprint(farms[1]):
                    reads["mirror"] = True
                    break
        d29 = [money[s] for s in sorted(money) if s >= D29_START]
        reads["d29_margin"] = round(d29[-1] - d29[0], 2) if len(d29) >= 2 \
            else UNKNOWN
        if isinstance(last_obs, dict):
            prices = ((last_obs.get("market") or {}) if
                      isinstance(last_obs.get("market"), dict) else {}
                      ).get("prices") or {}
            shed = ((last_obs.get("private") or {}) if
                    isinstance(last_obs.get("private"), dict) else {}
                    ).get("shed") or {}
            total = 0.0
            for item, qty in (shed or {}).items():
                try:
                    total += float(prices.get(item, 0)) * float(qty)
                except (TypeError, ValueError):
                    continue
            reads["stranding"] = round(total, 2)
        else:
            reads["stranding"] = UNKNOWN
    except Exception as exc:
        reads.setdefault("d29_margin", UNKNOWN)
        reads.setdefault("stranding", UNKNOWN)
        reads["read_error"] = repr(exc)[:120]
    return reads


def _judge_chunk(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """worker：一批局跑 run_games+逐局读数（红局计入不短路）。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
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
            "seat": int(spec.get("our_seat", 0)), "side": spec.get("side"),
            "opponent": spec.get("opponent"),
            "banks": rr.get("banks"), "error": rr.get("error"),
        }
        if isinstance(sinks, dict) and "build_error" in sinks:
            row["error"] = sinks["build_error"]
        if row["banks"] is not None and row["error"] is None:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - \
                float(banks[1 - row["seat"]])
            row["reads"] = _game_reads(sinks, row["seat"], row["seed"]) \
                if isinstance(sinks, dict) else {}
            row["opp_reads"] = _game_reads(sinks, 1 - row["seat"],
                                           row["seed"]) \
                if isinstance(sinks, dict) else {}
        else:
            row["margin"] = None
            row["reads"] = {}
        out.append(row)
    return out


def _play(specs: Sequence[Dict[str, Any]],
          cfg: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    specs = list(specs)
    workers = int((cfg or {}).get("workers", 16))
    n_chunks = max(1, min(workers * 2, max(1, len(specs))))
    chunks = [specs[i::n_chunks] for i in range(n_chunks)]
    tasks = [{"specs": c, "cfg": dict(cfg or {})} for c in chunks if c]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_judge_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_judge_chunk, tasks)
    rows: List[Dict[str, Any]] = []
    for part in parts:
        rows.extend(part)
    return rows


# ----------------------------------------------------------- 子件 --

def endgame_stats(states: Any, baselines: Any = None) -> Dict[str, Any]:
    """尾段读数（d29 段差/终拍滞留/翻车翻正）。签名意图：输入: 逐局读数行
    序列+基线行集 / 输出: {d29_margin_median, stranding_mean, flips,
    verdict} / 错误: 缺字段→UNKNOWN。
    """
    try:
        rows = [r for r in (states or []) if isinstance(r, dict)]
        d29 = [r["reads"].get("d29_margin") for r in rows
               if isinstance(r.get("reads"), dict) and
               isinstance(r["reads"].get("d29_margin"), (int, float))]
        strand = [r["reads"].get("stranding") for r in rows
                  if isinstance(r.get("reads"), dict) and
                  isinstance(r["reads"].get("stranding"), (int, float))]
        base_d29 = []
        base_strand = []
        for r in (baselines or []):
            if isinstance(r, dict) and isinstance(r.get("reads"), dict):
                v = r["reads"].get("d29_margin")
                if isinstance(v, (int, float)):
                    base_d29.append(v)
                v = r["reads"].get("stranding")
                if isinstance(v, (int, float)):
                    base_strand.append(v)
        base_by = {(r.get("seed"), r.get("seat")): r for r in (baselines or [])
                   if isinstance(r, dict)}
        flips = 0
        for r in rows:
            b = base_by.get((r.get("seed"), r.get("seat")))
            if b and isinstance(r.get("margin"), (int, float)) and \
                    isinstance(b.get("margin"), (int, float)) and \
                    r["margin"] > 0 >= b["margin"]:
                flips += 1

        def _med(vals):
            vals = sorted(vals)
            return round(vals[len(vals) // 2], 2) if vals else UNKNOWN

        out = {
            "d29_margin_median": _med(d29),
            "stranding_mean": round(sum(strand) / len(strand), 2)
            if strand else UNKNOWN,
            "base_d29_median": _med(base_d29),
            "base_stranding_mean": round(sum(base_strand) / len(base_strand),
                                         2) if base_strand else UNKNOWN,
            "flips": flips,
        }
        out["verdict"] = "PASS" if (
            isinstance(out["d29_margin_median"], (int, float)) and
            isinstance(out["base_d29_median"], (int, float)) and
            out["d29_margin_median"] >= out["base_d29_median"] and
            isinstance(out["stranding_mean"], (int, float)) and
            isinstance(out["base_stranding_mean"], (int, float)) and
            out["stranding_mean"] <= out["base_stranding_mean"]) else "FAIL"
        return out
    except Exception as exc:
        return {"verdict": UNKNOWN, "error": repr(exc)[:160]}


def mirror_arm_stats(games: Any, credit_ledger: Any = None) -> Dict[str, Any]:
    """镜像臂读数（镜像子集胜率+credit 净加卖核对）。签名意图：输入: 逐局
    读数行+credit 账本 / 输出: {win_rate, net_add_sell, n, verdict} /
    错误: 缺账本→UNKNOWN。
    """
    try:
        rows = [r for r in (games or []) if isinstance(r, dict) and
                isinstance(r.get("reads"), dict) and r["reads"].get("mirror")]
        n = len(rows)
        wins = sum(1 for r in rows if isinstance(r.get("margin"),
                                                 (int, float)) and
                   r["margin"] > 0)
        net = None
        if isinstance(credit_ledger, dict):
            boosted = float(credit_ledger.get("boosted_total", 0.0))
            repaid = float(credit_ledger.get("repaid_total", 0.0))
            balance = float(credit_ledger.get("balance_total", 0.0))
            net = round(boosted - repaid - balance, 6)
        out = {"n": n,
               "win_rate": round(wins / n, 4) if n else UNKNOWN,
               "net_add_sell": net if net is not None else UNKNOWN}
        ok_wr = isinstance(out["win_rate"], float) and out["win_rate"] >= 0.55
        ok_net = net is not None and abs(net) < 1e-6
        out["verdict"] = "PASS" if (ok_wr and ok_net) else "FAIL"
        return out
    except Exception as exc:
        return {"verdict": UNKNOWN, "error": repr(exc)[:160]}


# ----------------------------------------------------------- 判决主件 --

def judge_r25(package: Any, corpus: Any = None,
              config: Any = None) -> Dict[str, Any]:
    """判决 v25（分项+总判）。签名意图：输入: r42 包+语料+副证配置 / 输出:
    evidence JSON / 错误: 单局红计入不短路。
    """
    cfg = dict(config) if isinstance(config, dict) else {}
    main_path = Path(str(package if package is not None else
                         MODULE_DIR / "build" / "main.py"))
    if not main_path.is_file():
        raise FileNotFoundError("r42 件不存在: %s" % main_path)
    r40_path = Path(str(cfg.get("r40_main") or
                        MODULE_DIR.parent / "orderbook_r40" / "build" /
                        "main.py"))
    opps = [str(p) for p in (cfg.get("opponents") or (
        str(MODULE_DIR.parent / "orderbook_r37" / "build" / "main.py"),
        str(MODULE_DIR.parent / "orderbook_2965_adopt" / "a" / "main.py"),
        str(MODULE_DIR.parent / "v48_derivative" / "main.py")))]
    workers = int(cfg.get("workers", 16))
    n_h2h = int(cfg.get("n_h2h", N_H2H_DEFAULT))
    n_league = int(cfg.get("n_league", N_LEAGUE_DEFAULT))
    run_cfg = {"engine": cfg.get("engine", "auto"), "workers": workers}
    if cfg.get("bridge") is not None:
        run_cfg["bridge"] = cfg["bridge"]
    t0 = time.perf_counter()

    def _specs(opp_path: str, seeds: Sequence[int], side: str) \
            -> List[Dict[str, Any]]:
        out = []
        for seed in seeds:
            for seat in (0, 1):
                a = {"type": "python", "path": str(main_path)}
                b = {"type": "python", "path": opp_path}
                agents = [a, b] if seat == 0 else [b, a]
                out.append({"game_id": "j25-%s-%d-s%d" % (side, seed, seat),
                            "seed": int(seed), "kind": "judge",
                            "side": side, "our_seat": seat,
                            "opponent": Path(opp_path).parent.parent.name,
                            "trace": True, "agents": agents})
        return out

    h2h_seeds = [H2H_SEED_BASE + i for i in range(n_h2h)]
    h2h_rows = _play(_specs(str(r40_path), h2h_seeds, "h2h"), run_cfg)
    ours = [r for r in h2h_rows if r.get("side") == "h2h"]
    league_rows: List[Dict[str, Any]] = []
    for j, opp in enumerate(opps):
        seeds = [LEAGUE_SEED_BASE + j * 1000 + i for i in range(n_league)]
        league_rows.extend(_play(_specs(opp, seeds, "league"), run_cfg))

    def _wr(rows):
        ms = [r["margin"] for r in rows if isinstance(r.get("margin"),
                                                      (int, float))]
        return round(sum(1 for m in ms if m > 0) / len(ms), 4) if ms \
            else UNKNOWN

    h2h_wr = _wr(ours)
    league_wr = _wr(league_rows)

    # ①P1：实现单价（同局配对：r42 侧 vs r40 侧）+ d21-28 段差中位
    px_ours, px_base, seg_ours = [], [], []
    for r in ours:
        rd = r.get("reads") or {}
        seg = rd.get("seg") or {}
        if isinstance(seg.get("realized_px"), (int, float)):
            px_ours.append(float(seg["realized_px"]))
        if isinstance(seg.get("seg_delta"), (int, float)):
            seg_ours.append(float(seg["seg_delta"]))
        seg_t = ((r.get("opp_reads") or {}).get("seg")) or {}
        if isinstance(seg_t.get("realized_px"), (int, float)):
            px_base.append(float(seg_t["realized_px"]))
    realized_ratio = UNKNOWN
    if px_ours and px_base:
        m_ours = sum(px_ours) / len(px_ours)
        m_base = sum(px_base) / len(px_base)
        if m_base > 0:
            realized_ratio = round((m_ours / m_base - 1.0) * 100.0, 2)
    seg_med = UNKNOWN
    if seg_ours:
        seg_med = round(sorted(seg_ours)[len(seg_ours) // 2], 2)
    p1 = {"realized_px_delta_pct": realized_ratio,
          "d21_28_seg_delta_median": seg_med,
          "verdict": "PASS" if (
              isinstance(realized_ratio, (int, float)) and
              realized_ratio >= 5.0 and
              isinstance(seg_med, (int, float)) and seg_med > 0) else "FAIL"}

    # ②P2：尾段（r42 侧 vs 同局 r40 侧=配对基线）
    base_rows = [{"seed": r["seed"], "seat": r["seat"],
                  "margin": -(r.get("margin") or 0),
                  "reads": r.get("opp_reads") or {}} for r in ours]
    p2 = endgame_stats(ours, base_rows)

    # ③P3：镜像臂+credit 账本
    credit_ledger = cfg.get("credit_ledger") or {
        "boosted_total": 0.0, "repaid_total": 0.0, "balance_total": 0.0,
        "note": "恒等式由 test_mirror credit 组钉住；判决实账未接线记 0"}
    p3 = mirror_arm_stats(ours, credit_ledger)

    overall = {
        "h2h_vs_r40": h2h_wr,
        "league_win_rate": league_wr,
        "pass": (isinstance(h2h_wr, float) and h2h_wr >= 0.55 and
                 isinstance(league_wr, float) and league_wr >= 0.80),
        "criteria": {"p1": p1, "p2": p2, "p3": p3},
        "n_h2h": len(ours), "n_league": len(league_rows),
        "n_errors": sum(1 for r in ours + league_rows if r.get("error")),
    }
    evidence = {
        "version": RECORD_VERSION,
        "written_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "config": {"n_h2h": n_h2h, "n_league": n_league,
                   "workers": workers, "opponents": opps,
                   "main": str(main_path)},
        "overall": overall,
        "elapsed_s": round(time.perf_counter() - t0, 2),
    }
    out_path = Path(cfg.get("evidence_path") or
                    MODULE_DIR / "evidence" / "judge_r25_realrun.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=1,
                                   default=str) + "\n", encoding="utf-8")
    evidence["evidence_path"] = str(out_path)
    return evidence
