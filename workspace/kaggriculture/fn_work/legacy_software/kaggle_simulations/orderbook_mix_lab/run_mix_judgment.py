# -*- coding: utf-8 -*-
"""run_mix_judgment —— R15 反周期产线 mix 判决实验 CLI 编排。

流程：select_corpus_r15 → phase_m_market_map（零合格置换对 → KILLED 短路）
→ generate_mix_variants（全不可行 → KILLED 短路）→ openloop_replay_variants
（26 败局×2 席+10 胜局×1 席，对照=原版 L3[R14 重合局复用+抽验]）→
closedloop_probe（开环 POSITIVE 变体 vs 原版 L3 镜像近亲局双席位直接对打）
→ judge_mix_verdicts → evidence/mix_judgment.json + 控制台摘要。

用法：
  python3 orderbook_mix_lab/run_mix_judgment.py [--replay-dir /tmp/r33audit]
      [--l3-main ../orderbook_l3_derivative/main.py]
      [--scales 0.1,0.2,0.3] [--max-variants 16] [--budget 1100]
任一组件 fail-closed 即整体 fail（evidence 仍落盘记 error 面）。
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

from orderbook_mix_lab import _base as B  # noqa: E402
from orderbook_mix_lab import closedloop as CL  # noqa: E402
from orderbook_mix_lab import corpus_r15 as C  # noqa: E402
from orderbook_mix_lab import judge_mix as J  # noqa: E402
from orderbook_mix_lab import openloop as OL  # noqa: E402
from orderbook_mix_lab import phase_m as M  # noqa: E402
from orderbook_mix_lab import variant_gen as VG  # noqa: E402

EVIDENCE_DIR = os.path.join(_HERE, "evidence")
VARIANTS_DIR = os.path.join(_HERE, "variants")

METHOD_NOTES = [
    "Phase M 结构判据面=Markup(价/引擎基准价)截面包位（基准价 twin 引擎 "
    "MARKET_PARAMS.base 运行时校验）；字面 own-pool 分位面在平稳序列均值"
    "数学回归 ~50、35/65 阈不可达（86 局实测零品项过阈，会造成假性 KILLED），"
    "故 own-pool 面保留为趋势证据、判据面按 Markup 截面分位落地——口径偏差登记",
    "Phase M 供给密度=家族（双席）逐日成交量份额（供给流入市场口径）",
    "变体手术：L3 基座 _R108_DATA 动作表共享条目改写 BUY_SEED/PLANT 事件"
    "（品名载荷改写、不增删订单/指令，market 单数上限天然保持）；路由/反应层/"
    "清仓结构逐字节保留；blob 区间外逐字节一致+编译+解码回路+确定性双跑自检",
    "种子覆盖保守口径：引擎步内先单元后市场 → 变体植物的 to 种子由严格更早步"
    "的已转换 BUY_SEED 覆盖；转换买入沿 chosen 逐日累计分布配额且总量守恒"
    "（未转换种子足额供养未入选 from 植物）",
    "开环对照臂复用 R14 evidence（重合局双席 control margin）+抽验 2 局"
    "（漂移>1 弃用复用全量实测）",
    "开环对手席=录像开环重放（R8 先例口径，对手不反应）；闭环副证补该面"
    "（twin 双席活体，对手可反应），镜像近亲池不足 5 局时取全池（记 note）",
    "胜局语料 rng=random.Random(20260925r15)（材料串 sha256 前 16 hex 转 int，"
    "R14 同款推导）；mirror 抽样同种子材料独立实例",
    "feasibility 孪生空跑（R9 gen_schedule 四约束族口径落地）：劳动=指令数"
    "不变性核验、现金=种子差价累计 vs 26 败局我席日末资金逐日最小值地板、"
    "棚容=to 品净累积粗模型峰值≤100、停时=day+FIRST_YIELD_DAY[to]≤29",
]


def _write_json(path, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return path


def _money_floor_curve(replay_entries):
    """26 败局我席日末资金逐日最小值（feasibility 现金地板，最差收入面）。"""
    floors = None
    for g in replay_entries:
        try:
            with open(g["path"], "r", encoding="utf-8") as fh:
                replay = json.load(fh)
            names = replay.get("info", {}).get("TeamNames") or []
            seat = names.index(B.TEAM_NAME)
            steps = replay.get("steps") or []
            day_money = []
            for d in range(30):
                si = min(d * 24 + 23, len(steps) - 1)
                obs = (steps[si][seat] or {}).get("observation") or {}
                farms = obs.get("farms")
                if isinstance(farms, str):
                    farms = json.loads(farms)
                day_money.append(float(farms[seat]["money"]))
            floors = ([min(a, b) for a, b in zip(floors, day_money)]
                      if floors else day_money)
        except Exception:
            continue
    return [round(v, 1) for v in floors] if floors else None


def run_mix_judgment(replay_dir=B.DEFAULT_REPLAY_DIR, out_dir=EVIDENCE_DIR,
                     l3_main=B.DEFAULT_L3_MAIN, scales=(0.10, 0.20, 0.30),
                     max_variants=16, budget=B.MAX_REPLAYS,
                     variants_dir=VARIANTS_DIR, audit_rows=None, log=None):
    """编排裁决（责任面入口；CLI 为薄壳）。返回 evidence dict。"""
    log = log or (lambda msg: print(msg, flush=True))
    t0 = time.perf_counter()
    replay_dir = os.path.abspath(replay_dir)
    evidence = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "protocol": "orderbook-mix-lab-judgment/1.0"}
    overall, killed_reason = None, None

    def _ev_base():
        return {
            "rerun_command": (
                f"cd {_KSIM} && python3 orderbook_mix_lab/run_mix_judgment.py"
                f" --replay-dir {replay_dir} --l3-main {os.path.abspath(l3_main)}"),
            "replay_dir": replay_dir,
            "method_notes": list(METHOD_NOTES),
        }

    # ---- S1 语料 + Phase M -------------------------------------------------
    try:
        sel = C.select_corpus_r15(replay_dir, audit_rows)
        if sel["errors"]:
            raise ValueError(f"语料缺回放 fail-closed: {sel['errors']}")
        if not sel["losses26"]:
            raise ValueError("losses26 为空")
        mm = M.phase_m_market_map(replay_dir)
    except Exception as exc:
        evidence["source"] = _ev_base()
        evidence["error"] = f"S1 fail-closed: {type(exc).__name__}: {exc}"
        evidence["overall"] = "FAIL"
        _write_json(os.path.join(out_dir, "mix_judgment.json"), evidence)
        return evidence
    log(f"[phase_m] games={mm['n_games']} ok={mm['n_ok']} "
        f"crash={mm['crash_items']} scarce={mm['scarce_items']} "
        f"pairs={len(mm['swap_pairs_ranked'])} ({time.perf_counter()-t0:.0f}s)")
    if not mm["swap_pairs_ranked"]:
        killed_reason = "Phase M 零合格置换对（无品项同时满足结构性高价+可置换）"
        overall = "KILLED"

    # ---- S2 变体生成 --------------------------------------------------------
    variants_out = None
    corpus = None
    if killed_reason is None:
        try:
            floor = _money_floor_curve(sel["losses26"])
            variants_out = VG.generate_mix_variants(
                mm["swap_pairs_ranked"], scales=scales,
                max_variants=max_variants, l3_main_path=l3_main,
                out_dir=variants_dir,
                base_context={"money_floor_curve": floor})
            corpus = {"losses26": sel["losses26"], "wins10": sel["wins10"]}
        except Exception as exc:
            evidence["source"] = _ev_base()
            evidence["error"] = f"S2 fail-closed: {type(exc).__name__}: {exc}"
            evidence["overall"] = "FAIL"
            _write_json(os.path.join(out_dir, "mix_judgment.json"), evidence)
            return evidence
        log(f"[variants] points={variants_out['audit']['n_points']} "
            f"built={variants_out['audit']['n_variants']} "
            f"dropped={variants_out['audit']['n_dropped']}")
        if variants_out["audit"]["feasible_zero"]:
            killed_reason = "全部参数点不可行（零可用变体）"
            overall = "KILLED"

    # ---- S3 开环 + 闭环 + 判据 ----------------------------------------------
    open_out = closed_out = judge_out = None
    if killed_reason is None:
        try:
            open_out = OL.openloop_replay_variants(
                variants_out["variants"], corpus, l3_main, budget=budget,
                log=log)
            s = open_out["summary"]
            log(f"[openloop] variants={s['n_run_variants']} replays={s['n_replays']} "
                f"control(fresh={s['control_fresh']},reused={s['control_reused']},"
                f"reuse_ok={s['reuse_ok']}) red/截断={s['budget_stopped']} "
                f"({s['wall_s']}s)")
        except Exception as exc:
            evidence["source"] = _ev_base()
            evidence["error"] = f"S3 openloop fail-closed: {type(exc).__name__}: {exc}"
            evidence["overall"] = "FAIL"
            _write_json(os.path.join(out_dir, "mix_judgment.json"), evidence)
            return evidence
        pos_ids = [vid for vid, rec in open_out["per_variant"].items()
                   if J.variant_openloop_positive(rec.get("games"))[0]]
        if pos_ids:
            pos_variants = [v for v in variants_out["variants"]
                            if v["id"] in pos_ids]
            try:
                closed_out = CL.closedloop_probe(
                    pos_variants, sel["mirror"], l3_main, log=log)
            except Exception as exc:
                evidence["source"] = _ev_base()
                evidence["error"] = (f"S3 closedloop fail-closed: "
                                     f"{type(exc).__name__}: {exc}")
                evidence["overall"] = "FAIL"
                _write_json(os.path.join(out_dir, "mix_judgment.json"), evidence)
                return evidence
        judge_out = J.judge_mix_verdicts(open_out, closed_out, killed=False)
        overall = judge_out["overall"]
    else:
        judge_out = {"overall": "KILLED", "killed_reason": killed_reason,
                     "per_variant": {}, "winning_variant": None,
                     "sensitivity": {}, "fail_closed": False}
        log(f"[judge] KILLED 短路：{killed_reason}")

    # ---- S4 evidence ---------------------------------------------------------
    evidence.update({
        "source": _ev_base(),
        "corpus": {
            "losses26": [g["episode"] for g in sel["losses26"]],
            "wins10": [g["episode"] for g in sel["wins10"]],
            "mirror": [g["episode"] for g in sel["mirror"]],
            "mirror_note": sel["sampling"].get("note"),
            "sampling": {k: sel["sampling"][k] for k in
                         ("seed_material", "seed_derivation", "picked_wins",
                          "mirror_pool", "picked_mirror")},
            "early_crash_excluded": list(B.EARLY_CRASH),
        },
        "phase_m": {
            "params": mm["params"],
            "base_prices": mm["base_prices"],
            "base_prices_from_engine": mm["base_prices_from_engine"],
            "crash_items": mm["crash_items"],
            "scarce_items": mm["scarce_items"],
            "items": mm["items"],
            "swap_pairs_ranked": mm["swap_pairs_ranked"],
            "capacity_windows": mm["capacity_windows"],
            "n_games": mm["n_games"], "n_ok": mm["n_ok"],
            "errors": mm["errors"],
        },
        "variants": variants_out,
        "openloop": open_out,
        "closedloop": closed_out,
        "judge": judge_out,
        "overall": overall or "FAIL",
        "wall_s": round(time.perf_counter() - t0, 1),
    })
    target = _write_json(os.path.join(out_dir, "mix_judgment.json"), evidence)
    log(f"[judgment] overall={evidence['overall']} → {target}")
    _console_summary(evidence)
    return evidence


def _console_summary(ev):
    pm = ev.get("phase_m") or {}
    if pm:
        print(f"Phase M: games={pm.get('n_games')} crash={pm.get('crash_items')} "
              f"scarce={pm.get('scarce_items')} "
              f"pairs={len(pm.get('swap_pairs_ranked') or [])}")
        for p in (pm.get("swap_pairs_ranked") or [])[:4]:
            print(f"  pair {p['from']}->{p['to']} score={p['score']} "
                  f"gap={p['pct_gap']} cap={p['from_capacity']}")
    var = ev.get("variants")
    if var:
        a = var["audit"]
        print(f"Variants: points={a['n_points']} built={a['n_variants']} "
              f"dropped={a['n_dropped']}")
        for v in var["variants"]:
            print(f"  {v['id']}: moved={v.get('moved_n')} "
                  f"target={v.get('target_n')} feasible={v['feasible']}")
    ol = ev.get("openloop")
    if ol:
        s = ol["summary"]
        print(f"Openloop: replays={s['n_replays']} wall={s['wall_s']}s "
              f"control reused={s['control_reused']} fresh={s['control_fresh']} "
              f"reuse_ok={s['reuse_ok']}")
        jd = (ev.get("judge") or {}).get("per_variant") or {}
        for vid, rec in jd.items():
            print(f"  {vid}: flips={rec.get('n_flip')}/{rec.get('n_loss')} "
                  f"med_Δ={rec.get('loss_delta_median')} "
                  f"harm={rec.get('n_harm_violations')} "
                  f"openloop_pos={rec.get('openloop_positive')} "
                  f"variant_pos={rec.get('variant_positive')}")
    cl = ev.get("closedloop")
    if cl:
        for vid, rec in cl["per_variant"].items():
            print(f"Closedloop {vid}: wins={rec['wins']}/{rec['runs']} "
                  f"rate={rec['rate']} median={rec['median_margin']}")
    print(f"OVERALL VERDICT: {ev.get('overall')}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="R15 反周期产线 mix 判决实验")
    ap.add_argument("--replay-dir", default=B.DEFAULT_REPLAY_DIR)
    ap.add_argument("--l3-main", default=B.DEFAULT_L3_MAIN)
    ap.add_argument("--scales", default="0.1,0.2,0.3",
                    help="幅度档（逗号分隔小数）")
    ap.add_argument("--max-variants", type=int, default=16)
    ap.add_argument("--budget", type=int, default=B.MAX_REPLAYS)
    args = ap.parse_args(argv)
    scales = tuple(float(x) for x in str(args.scales).split(","))
    ev = run_mix_judgment(replay_dir=args.replay_dir, l3_main=args.l3_main,
                          scales=scales, max_variants=args.max_variants,
                          budget=args.budget)
    return 0 if ev.get("overall") in ("POSITIVE", "NEGATIVE", "KILLED") else 1


if __name__ == "__main__":
    sys.exit(main())
