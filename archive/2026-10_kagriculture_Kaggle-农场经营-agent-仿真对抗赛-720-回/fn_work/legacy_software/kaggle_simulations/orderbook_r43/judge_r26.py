# -*- coding: utf-8 -*-
"""judge_r26 及判决面子件（R26）。

责任契约（fn_docs/hybrid/responsibility.md【R26 增补】）：仪器四件套——
安慰剂臂（纯重编码 vs r40 恒等）→单件消融（三组件各单件）→全件配对联赛；
分项=实现价 ≥0.88 ∧ 终局钱 ≥10.5 万/局 ∧ stranding≈0；总判=h2h ≥0.55。
"""
from __future__ import annotations

import json
import multiprocessing
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

MODULE_DIR = Path(__file__).resolve().parent
RECORD_VERSION = "judge-r26/1.0"
UNKNOWN = "UNKNOWN"
N_SEEDS_DEFAULT = 60            # 每臂 seed 数（×双席）
SEED_BASE = 640000
ARMS = ("placebo", "drain", "gran", "sheep", "full")
H2H_BAR = 0.55
REALIZED_BAR = 0.88
TERMINAL_MONEY_BAR = 105000.0


def realized_price_stats(states: Any) -> Dict[str, Any]:
    """实现价读数。签名意图：输入: traced 对局 [(step, obs, action)] /
    输出: {realized_px, terminal_money, stranding} / 错误: 缺字段→UNKNOWN。
    口径：实现价=Σ(qty×卖时市价)/Σ(qty×该局该品日均价)；
    终局钱=farms[obs.player].money（逐席干净口径，非 farms[0] 双侧污染读法）。"""
    try:
        daily: Dict[Tuple[int, str], List[float]] = {}
        sells: List[Tuple[int, str, float, float]] = []   # (day,item,qty,px)
        last_obs = None
        for entry in (states or []):
            if not isinstance(entry, (list, tuple)) or len(entry) < 3:
                continue
            step, obs, act = entry[0], entry[1], entry[2]
            if not isinstance(obs, dict):
                continue
            step = int(step)
            prices = ((obs.get("market") or {}) if
                      isinstance(obs.get("market"), dict) else {}
                      ).get("prices") or {}
            day = step // 24
            for item, px in (prices or {}).items():
                if isinstance(px, (int, float)):
                    daily.setdefault((day, str(item)), []).append(float(px))
            if isinstance(act, dict):
                for cmd in (act.get("market") or []):
                    if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                            and str(cmd[0]) == "SELL":
                        item = str(cmd[1])
                        px = prices.get(item)
                        if isinstance(px, (int, float)):
                            sells.append((day, item, float(cmd[2]),
                                          float(px)))
            last_obs = obs
        realized = UNKNOWN
        if sells:
            num = den = 0.0
            for day, item, qty, px in sells:
                pxs = daily.get((day, item)) or []
                avg = (sum(pxs) / len(pxs)) if pxs else px
                num += qty * px
                den += qty * avg
            realized = round(num / den, 4) if den > 0 else UNKNOWN
        terminal = UNKNOWN
        stranding = UNKNOWN
        if isinstance(last_obs, dict):
            # 逐席干净口径：farms[obs.player].money（缺席号回落席 0），
            # 修 P2 缺陷——旧 farms[0] 恒读使同局双侧读数同值污染。
            try:
                player = int(last_obs.get("player", 0))
            except (TypeError, ValueError):
                player = 0
            farms = last_obs.get("farms")
            if isinstance(farms, list) and 0 <= player < len(farms) \
                    and isinstance(farms[player], dict):
                try:
                    terminal = round(float(farms[player].get("money", 0.0)),
                                     2)
                except (TypeError, ValueError):
                    pass
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
            stranding = round(total, 2)
        return {"realized_px": realized, "terminal_money": terminal,
                "stranding": stranding}
    except Exception as exc:
        return {"realized_px": UNKNOWN, "terminal_money": UNKNOWN,
                "stranding": UNKNOWN, "error": repr(exc)[:120]}


def _chunk(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games, metas = [], []
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
    out = []
    for i, (spec, sinks) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"game_id": spec.get("game_id"), "seed": int(spec["seed"]),
               "seat": int(spec.get("our_seat", 0)), "arm": spec.get("arm"),
               "banks": rr.get("banks"), "error": rr.get("error")}
        if isinstance(sinks, dict) and "build_error" in sinks:
            row["error"] = sinks["build_error"]
        if row["banks"] is not None and row["error"] is None:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - \
                float(banks[1 - row["seat"]])
            sink = sinks.get(row["seat"]) if isinstance(sinks, dict) \
                else None
            row["reads"] = realized_price_stats(sink or []) \
                if sink is not None else {}
        else:
            row["margin"] = None
            row["reads"] = {}
        out.append(row)
    return out


def _play(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", 16))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})}
             for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_chunk, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def judge_r26(package: Any, corpus: Any = None,
              config: Any = None) -> Dict[str, Any]:
    """判决 v26（安慰剂+单件消融+配对）。签名意图：输入: 各臂件路径+配置 /
    输出: evidence JSON / 错误: 单局红计入不短路。"""
    cfg = dict(config) if isinstance(config, dict) else {}
    arms = cfg.get("arms") or {a: cfg.get("main") for a in ARMS}
    r40 = str(cfg.get("r40_main") or MODULE_DIR.parent / "orderbook_r40" /
              "build" / "main.py")
    n_seeds = int(cfg.get("n_seeds", N_SEEDS_DEFAULT))
    workers = int(cfg.get("workers", 16))
    run_cfg = {"engine": cfg.get("engine", "auto"), "workers": workers}
    if cfg.get("bridge") is not None:
        run_cfg["bridge"] = cfg["bridge"]
    t0 = time.perf_counter()
    seeds = [SEED_BASE + i for i in range(n_seeds)]
    stats: Dict[str, Dict[str, Any]] = {}
    for arm, main_path in arms.items():
        specs = []
        for seed in seeds:
            for seat in (0, 1):
                a = {"type": "python", "path": str(main_path)}
                b = {"type": "python", "path": r40}
                agents = [a, b] if seat == 0 else [b, a]
                specs.append({"game_id": "j26-%s-%d-s%d" % (arm, seed, seat),
                              "seed": seed, "kind": "judge", "arm": arm,
                              "our_seat": seat, "trace": True,
                              "agents": agents})
        rows = _play(specs, run_cfg)
        ms = [r["margin"] for r in rows if isinstance(r.get("margin"),
                                                      (int, float))]
        px = [r["reads"]["realized_px"] for r in rows
              if isinstance(r.get("reads"), dict) and
              isinstance(r["reads"].get("realized_px"), float)]
        tm = [r["reads"]["terminal_money"] for r in rows
              if isinstance(r.get("reads"), dict) and
              isinstance(r["reads"].get("terminal_money"),
                         (int, float)) and
              not isinstance(r["reads"].get("terminal_money"), bool)]
        st = [r["reads"]["stranding"] for r in rows
              if isinstance(r.get("reads"), dict) and
              isinstance(r["reads"].get("stranding"),
                         (int, float)) and
              not isinstance(r["reads"].get("stranding"), bool)]
        stats[arm] = {
            "n": len(rows),
            "h2h": round(sum(1 for m in ms if m > 0) / len(ms), 4) if ms
            else UNKNOWN,
            "mean_margin": round(sum(ms) / len(ms), 1) if ms else UNKNOWN,
            "realized_px_mean": round(sum(px) / len(px), 4) if px
            else UNKNOWN,
            "terminal_money_mean": round(sum(tm) / len(tm), 1) if tm
            else UNKNOWN,
            "stranding_mean": round(sum(st) / len(st), 2) if st
            else UNKNOWN,
        }
    full = stats.get("full") or {}
    placebo = stats.get("placebo") or {}
    placebo_ok = isinstance(placebo.get("h2h"), float) and \
        0.35 <= placebo["h2h"] <= 0.65
    crit = {
        "placebo_identity": {"value": placebo.get("h2h"),
                             "verdict": "PASS" if placebo_ok else "FAIL"},
        "realized_px": {"value": full.get("realized_px_mean"),
                        "bar": REALIZED_BAR,
                        "verdict": "PASS" if
                        isinstance(full.get("realized_px_mean"), float) and
                        full["realized_px_mean"] >= REALIZED_BAR
                        else "FAIL"},
        "terminal_money": {"value": full.get("terminal_money_mean"),
                           "bar": TERMINAL_MONEY_BAR,
                           "verdict": "PASS" if
                           isinstance(full.get("terminal_money_mean"),
                                      (int, float)) and
                           full["terminal_money_mean"] >=
                           TERMINAL_MONEY_BAR else "FAIL"},
        "h2h": {"value": full.get("h2h"), "bar": H2H_BAR,
                "verdict": "PASS" if isinstance(full.get("h2h"), float)
                and full["h2h"] >= H2H_BAR else "FAIL"},
    }
    evidence = {
        "version": RECORD_VERSION,
        "written_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "config": {"n_seeds": n_seeds, "arms": {k: str(v) for k, v in
                                                arms.items()}},
        "arms": stats,
        "criteria": crit,
        "pass": all(c["verdict"] == "PASS" for c in crit.values()),
        "elapsed_s": round(time.perf_counter() - t0, 2),
    }
    out_path = Path(cfg.get("evidence_path") or MODULE_DIR / "evidence" /
                    "judge_r26_realrun.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=1,
                                   default=str) + "\n", encoding="utf-8")
    evidence["evidence_path"] = str(out_path)
    return evidence
