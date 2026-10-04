# -*- coding: utf-8 -*-
"""run_judgment —— R14 两阶段判决实验 CLI 编排。

流程：corpus_select → phase_a_attribution（全量；零可处置 surge 日 →
KILLED_A 短路出 evidence）→ corpus_select(phase_b) → phase_b_four_arm_replay
（四臂×双席位）→ judge_verdicts → evidence 落盘 + 控制台摘要。

用法：
  python3 orderbook_surge_lab/run_judgment.py [--replay-dir /tmp/r33audit]
      [--l3-main ../orderbook_l3_derivative/main.py] [--threshold 1500]
      [--median-mult 1.5] [--phase-b-budget 7200] [--limit N] [--skip-phase-b]
任一环节 fail-closed 即整体 fail（evidence 仍落盘记 error 面）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_KSIM = os.path.dirname(_HERE)
if __name__ == "__main__" and _KSIM not in sys.path:
    sys.path.insert(0, _KSIM)

from orderbook_surge_lab import corpus as C  # noqa: E402
from orderbook_surge_lab import judge as J  # noqa: E402
from orderbook_surge_lab import phase_a as A  # noqa: E402
from orderbook_surge_lab import phase_b as B  # noqa: E402

DEFAULT_L3_MAIN = os.path.normpath(os.path.join(
    _KSIM, "orderbook_l3_derivative", "main.py"))
EVIDENCE_DIR = os.path.join(_HERE, "evidence")

# 重演预算（需求：≤200 局次）。四臂×双席位=8 局次/局；对照臂每席 1 次。
MAX_REPLAYS = 200
REPLAYS_PER_GAME = 8


def _write_json(path, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return path


def run_judgment(replay_dir=C.DEFAULT_REPLAY_DIR, l3_main=DEFAULT_L3_MAIN,
                 threshold=A.DEFAULT_THRESHOLD,
                 median_mult=A.DEFAULT_MEDIAN_MULT, limit=None,
                 skip_phase_b=False, phase_b_budget_s=7200.0,
                 evidence_dir=EVIDENCE_DIR, log=None):
    """编排裁决（责任面入口；CLI 为薄壳）。返回 evidence dict。

    evidence：source（可复跑命令/语料清单/胜局抽样记录/方法注记与偏差）+
    phase_a（全景+深描+敏感度，逐日全表另存 phase_a_full.json）+ phase_b
    （逐局逐臂双席 margin/Δ/零足迹）+ judge（逐臂 verdict/胜出臂/敏感度）
    + overall verdict ∈ {POSITIVE, NEGATIVE, KILLED_A}。
    """
    log = log or (lambda msg: print(msg, flush=True))
    t0 = time.perf_counter()
    evidence = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "protocol": "orderbook-surge-lab-judgment/1.0"}
    overall, killed_a = None, False
    # ---- Phase A ----------------------------------------------------------
    try:
        entries = C.corpus_select(replay_dir)["phase_a"]
        if limit is not None:
            entries = entries[:int(limit)]
        if not entries:
            raise ValueError(f"语料目录无回放: {replay_dir}")
        report_a = A.phase_a_attribution(entries, threshold, median_mult)
    except Exception as exc:
        evidence["error"] = f"Phase A fail-closed: {type(exc).__name__}: {exc}"
        evidence["overall"] = "FAIL"
        _write_json(os.path.join(evidence_dir, "judgment.json"), evidence)
        return evidence
    log(f"[phase_a] n={report_a['panorama']['n_games']} "
        f"ok={report_a['panorama']['n_ok']} "
        f"surge_games={report_a['panorama']['n_games_with_surge']} "
        f"treatable={report_a['panorama']['n_games_treatable']} "
        f"treatable_losses={report_a['panorama']['n_treatable_losses']} "
        f"({time.perf_counter() - t0:.0f}s)")

    full_path = _write_json(
        os.path.join(evidence_dir, "phase_a_full.json"),
        {"per_game": report_a["per_game"], "threshold": threshold,
         "median_mult": median_mult})

    pan = report_a["panorama"]
    if pan["n_treatable_surge_days"] == 0:
        killed_a = True
        overall = "KILLED_A"

    # ---- Phase B ----------------------------------------------------------
    phase_b_out = None
    corpus_b = None
    if killed_a:
        log("[phase_b] 短路：全语料零可处置 surge 日 → KILLED_A")
    elif skip_phase_b:
        log("[phase_b] --skip-phase-b：跳过（测试模式）")
    else:
        try:
            sel = C.corpus_select(replay_dir, report_a)
            corpus_b = sel["phase_b"]
            n_games = len(corpus_b["losses"]) + len(corpus_b["wins"])
            budget_note = None
            if n_games * REPLAYS_PER_GAME > MAX_REPLAYS:
                # 预算圈禁：可处置败局按 |margin| 升序（最近翻盘优先）截尾
                room = max(0, MAX_REPLAYS
                           - REPLAYS_PER_GAME * len(corpus_b["wins"])) // REPLAYS_PER_GAME
                keep = sorted(corpus_b["losses"],
                              key=lambda g: abs(g.get("margin") or 0))[:room]
                dropped = [g["episode"] for g in corpus_b["losses"][len(keep):]]
                corpus_b = {"losses": keep, "wins": corpus_b["wins"]}
                budget_note = {"kept": room, "dropped_episodes": dropped}
                log(f"[phase_b] 预算截尾：败局保留 {room}，剔除 {len(dropped)}")
            if not corpus_b["losses"] and not corpus_b["wins"]:
                raise ValueError("Phase B 语料为空")
            evidence["_sampling"] = sel.get("sampling")
            phase_b_out = B.phase_b_four_arm_replay(
                corpus_b, report_a, l3_main, wall_budget_s=phase_b_budget_s,
                log=log)
            if budget_note:
                phase_b_out["budget_trim"] = budget_note
            log(f"[phase_b] games={phase_b_out['summary']['n_games']} "
                f"replays={phase_b_out['summary']['n_replays']} "
                f"red={phase_b_out['summary']['n_red']} "
                f"({time.perf_counter() - t0:.0f}s)")
        except Exception as exc:
            evidence["error"] = (evidence.get("error") or "") + \
                f"Phase B fail-closed: {type(exc).__name__}: {exc}"
            phase_b_out = phase_b_out or {"per_game": [], "summary": {
                "n_games": 0, "n_replays": 0, "n_red": 0}}

    # ---- judge -------------------------------------------------------------
    judge_out = None
    if phase_b_out is not None:
        phase_b_out = dict(phase_b_out)
        phase_b_out["_corpus"] = corpus_b
        judge_out = J.judge_verdicts(phase_b_out, report_a, killed_a=killed_a)
        overall = judge_out["overall"]
    elif killed_a:
        judge_out = {"overall": "KILLED_A",
                     "criteria": "全语料零可处置 surge 日（run_judgment 短路）"}

    # ---- evidence 汇总 ------------------------------------------------------
    # 对照保真度：对照臂在原我方席的 margin vs 原局记录 margin（孪生+L3
    # 重演与原局的对齐度；Δ 为对照相对值，不受小漂移影响）
    control_fidelity = []
    if phase_b_out is not None:
        for g in phase_b_out.get("per_game", []):
            seat = g.get("seat")
            if seat is None or seat not in (0, 1):
                continue
            ctrl = ((g.get("arms") or {}).get(f"seat{seat}") or {}) \
                .get("control", {}).get("margin")
            if ctrl is not None:
                control_fidelity.append(
                    {"episode": g.get("episode"),
                     "recorded": g.get("margin"), "control": ctrl,
                     "drift": round(ctrl - g.get("margin"), 1)})
    deep = []
    for g in report_a.get("deep_dive", []):
        if g.get("error"):
            deep.append({"episode": g.get("episode"), "error": g["error"]})
            continue
        ours = (g.get("orientations") or {}).get("our") or {}
        deep.append({
            "episode": g.get("episode"), "tag": g.get("tag"),
            "res": g.get("res"), "margin": g.get("margin"),
            "surge_days": ours.get("surge_days"),
            "composition": ours.get("composition"),
            "treatable_surge_days": g.get("treatable_surge_days"),
        })
    evidence.update({
        "source": {
            "rerun_command": (
                f"cd {_KSIM} && python3 orderbook_surge_lab/run_judgment.py"
                f" --replay-dir {os.path.abspath(replay_dir)}"
                f" --l3-main {os.path.abspath(l3_main)}"
                f" --threshold {threshold} --median-mult {median_mult}"),
            "replay_dir": os.path.abspath(replay_dir),
            "corpus_phase_a": [e["episode"] for e in entries],
            "corpus_phase_b": (
                {"losses": [g["episode"] for g in corpus_b["losses"]],
                 "wins": [g["episode"] for g in corpus_b["wins"]]}
                if corpus_b else None),
            "win_sampling": evidence.pop("_sampling", None),
            "phase_a_full_path": full_path,
            "method_notes": list(report_a["method_notes"]) + [
                "Phase B 对手席=录像开环重放（R8 先例）：对手不反应，反应性损失记注记",
                "零足迹双层口径：包装层（同观测非 surge 日 wrapped==base，判据绑定面）+流层（首 surge 日前逐字节一致；其后市场态因果发散（含 surge 日内基座后续反应）记 first_alien_diff/aftermath 报告面不判红）",
                "A1 目标=rate×当日累计可卖（期初+日内到货自适应，剩余量逐步 re-quote）",
                "A2=卖单按 当日价×shed库存 价值降序重排+空槽补单（引擎品项市场独立→重排为二阶效应，补单为主效应）",
                "L3 对照臂=官方 last-callable 全新装载（每局次），零改动在飞件",
            ],
        },
        "phase_a": {
            "panorama": pan,
            "deep_dive": deep,
            "threshold": threshold, "median_mult": median_mult,
            "errors": report_a["errors"],
        },
        "phase_b": (({k: v for k, v in phase_b_out.items() if k != "_corpus"})
                    if phase_b_out is not None else None),
        "control_fidelity": control_fidelity,
        "judge": judge_out,
        "overall": overall or "FAIL",
        "wall_s": round(time.perf_counter() - t0, 1),
    })
    target = _write_json(os.path.join(evidence_dir, "judgment.json"), evidence)
    log(f"[judgment] overall={evidence['overall']} → {target}")
    _console_summary(evidence)
    return evidence


def _console_summary(ev):
    pan = (ev.get("phase_a") or {}).get("panorama") or {}
    if pan:
        print(f"Phase A: games={pan.get('n_games')} surge_games="
              f"{pan.get('n_games_with_surge')} treatable="
              f"{pan.get('n_games_treatable')} treatable_losses="
              f"{pan.get('n_treatable_losses')} surge_days="
              f"{pan.get('n_surge_days_total')} treatable_surge_days="
              f"{pan.get('n_treatable_surge_days')}")
        comp = pan.get("composition_means") or {}
        if comp:
            print(f"  composition means: quant={comp.get('quant_gap')} "
                  f"mix={comp.get('mix_gap')} px={comp.get('px_gap')} "
                  f"structural={comp.get('structural_gap')} "
                  f"coverage={comp.get('coverage_mean')}")
        pi = pan.get("price_identifiability") or {}
        if pi.get("n_items_scored"):
            print(f"  price identifiability: mean_pct="
                  f"{pi.get('mean_percentile')} frac>=70pct="
                  f"{pi.get('frac_ge_70pct')} n={pi.get('n_items_scored')}")
    pb = ev.get("phase_b")
    if pb:
        s = pb.get("summary") or {}
        print(f"Phase B: games={s.get('n_games')} replays={s.get('n_replays')}"
              f" red={s.get('n_red')} wall={s.get('wall_s')}s")
        cf = ev.get("control_fidelity") or []
        exact = sum(1 for r in cf if abs(r["drift"]) < 0.5)
        if cf:
            print(f"  control fidelity: {exact}/{len(cf)} exact "
                  f"(drift max {max(abs(r['drift']) for r in cf)})")
    jd = ev.get("judge")
    if jd and jd.get("per_arm"):
        print("Judge per-arm:")
        for arm, st in jd["per_arm"].items():
            print(f"  {arm}: positive={st['positive']} "
                  f"n_sig={st['n_sig']} n_pos={st['n_pos']} "
                  f"harm={st['n_harm_violations']} "
                  f"sig_med={st['sig_delta_median']} "
                  f"range=[{st['all_delta_min']},{st['all_delta_max']}]")
        print(f"OVERALL: {jd['overall']} winning_arm={jd.get('winning_arm')}"
              f" fail_closed={jd.get('fail_closed')}")
    print(f"OVERALL VERDICT: {ev.get('overall')}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="R14 surge 日卖时判决实验")
    ap.add_argument("--replay-dir", default=C.DEFAULT_REPLAY_DIR)
    ap.add_argument("--l3-main", default=DEFAULT_L3_MAIN)
    ap.add_argument("--threshold", type=float, default=A.DEFAULT_THRESHOLD)
    ap.add_argument("--median-mult", type=float,
                    default=A.DEFAULT_MEDIAN_MULT)
    ap.add_argument("--limit", type=int, default=None,
                    help="Phase A 只跑前 N 局（冒烟用）")
    ap.add_argument("--skip-phase-b", action="store_true")
    ap.add_argument("--phase-b-budget", type=float, default=7200.0)
    args = ap.parse_args(argv)
    ev = run_judgment(replay_dir=args.replay_dir, l3_main=args.l3_main,
                      threshold=args.threshold, median_mult=args.median_mult,
                      limit=args.limit, skip_phase_b=args.skip_phase_b,
                      phase_b_budget_s=args.phase_b_budget)
    return 0 if ev.get("overall") in ("POSITIVE", "NEGATIVE", "KILLED_A") else 1


if __name__ == "__main__":
    sys.exit(main())
