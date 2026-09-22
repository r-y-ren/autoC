#!/usr/bin/env python
"""twin_fidelity.py —— Track-B P1 数字孪生保真门（蓝图 m6 验收契约脚本）。

对官方线上回放证明孪生引擎（planner/twin.py）逐位保真：

  1) 全程走子比对：从回放 steps[0] 初态起、用官方动作流驱动孪生逐步推进，
     每步与回放观测做型别敏感的逐位比对（farms/market/town/双席 private/
     day/hour/step），记录首个分歧（若有）。
  2) 中间步注入重演：每局按 早/中/晚 三窗随机抽 >=3 个中间步，从孪生快照
     （等价 build_state_from_replay 的注入态）rollout 至终局，双席终局资金
     必须与回放真值逐位相等（float 位型 hex 入台账）。

CLI 契约（验收命令）：
  python scripts/twin_fidelity.py --mode official
      完整保真门：>=100 局 x >=3 中间步（默认全语料 184 局），产出
      exports/probes/twin_fidelity/fidelity_report.json 与
      exports/twin/p1_fidelity_summary.md；全过退出码 0，否则非 0。
  python scripts/twin_fidelity.py --mode smoke
      小样本快跑版（默认 4 局 x 2 步点），供 pytest 调用，<60s；同一套
      判据与退出码。

语料：references/data/online-replays/{round8,15,18,19,20,21,22,cmp-v92} 的
episode-*-replay.json + references/data/replay-corpus/raw/ 冻结核（60 局）。
回放缺 seed 时（语料中为 0 局）杂草/商店随机无法复现，按差异路径单列豁免。

P2 预留：scripts/planner_offline_bench.py --mode official 将复用本模块的
discover_games/check_game 与 twin.build_state_from_replay / run_to_end，
注入集 = round20/21/22 + cmp-v92，动作源换双席策略回调（run_to_end 已支持
callable(state) -> [a0, a1] 的用法）。
"""
import argparse
import json
import random
import sys
import time
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE))

from kaggle_simulations.agent.planner import twin  # noqa: E402

REPO = SOFTWARE.parents[1]
DATA_ROOT = SOFTWARE.parent / "references" / "data"
REPORT_PATH = SOFTWARE / "exports" / "probes" / "twin_fidelity" / "fidelity_report.json"
SUMMARY_PATH = SOFTWARE / "exports" / "twin" / "p1_fidelity_summary.md"
CORPUS_GROUPS = [
    ("round8", DATA_ROOT / "online-replays" / "round8"),
    ("round15", DATA_ROOT / "online-replays" / "round15"),
    ("round18", DATA_ROOT / "online-replays" / "round18"),
    ("round19", DATA_ROOT / "online-replays" / "round19"),
    ("round20", DATA_ROOT / "online-replays" / "round20"),
    ("round21", DATA_ROOT / "online-replays" / "round21"),
    ("round22", DATA_ROOT / "online-replays" / "round22"),
    ("cmp-v92", DATA_ROOT / "online-replays" / "cmp-v92"),
    ("corpus", DATA_ROOT / "replay-corpus" / "raw"),
]
SCHEMA = "twin-fidelity/1.0"
SAMPLE_SEED = 20260919
# 早/中/晚三窗（中间步抽样域；上限 690 保证 >=30 步的终局重演）。
WINDOWS = [(24, 240), (240, 480), (480, 690)]


def discover_games(data_root=None):
    """按固定组序枚举语料回放（确定性；过滤 forensic_manifest 等非对局文件）。"""
    root = Path(data_root) if data_root else DATA_ROOT
    games = []
    for group, base in CORPUS_GROUPS:
        base = Path(data_root) / base.relative_to(DATA_ROOT) if data_root else base
        if not base.is_dir():
            continue
        for path in sorted(base.glob("episode-*-replay.json")):
            games.append((group, path))
    return games


def sample_steps(game_id, n_points, rng_seed=SAMPLE_SEED):
    """按 早/中/晚 窗确定性抽样（random.Random(str) 走 sha512，跨平台稳定）。
    n_points<=3 时按 [早,晚] 均匀取窗；>3 时全域均匀补抽去重。"""
    rng = random.Random(f"{rng_seed}:{game_id}")
    if n_points <= 0:
        return []
    if n_points == 1:
        windows = [WINDOWS[1]]  # 单点取中窗
    elif n_points == 2:
        windows = [WINDOWS[0], WINDOWS[2]]  # 两点取 早+晚
    else:
        windows = WINDOWS
    picks = [rng.randrange(lo, hi) for lo, hi in windows]
    rng_all = random.Random(f"{rng_seed}:{game_id}:extra")
    while len(picks) < n_points:
        candidate = rng_all.randrange(WINDOWS[0][0], WINDOWS[-1][1])
        if candidate not in picks:
            picks.append(candidate)
    return sorted(picks)


def _load_replay(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_game(path, points, bundle, compare_walk=True):
    """单局保真检查。返回结果 dict（pass / 首分歧 / 终局资金位型 / 耗时）。"""
    game_id = path.stem.replace("-replay", "")
    result = {
        "id": game_id, "group": None, "path": str(path),
        "seed": None, "steps": 0, "sample_steps": list(points),
        "walk": {"compared": 0, "first_divergence": None, "pass": False},
        "rollouts": [], "replay_rewards": None, "final_money": None,
        "bit_hex": None, "pass": False, "wall_ms": None,
        "timings_ms": {}, "attribution": None,
    }
    t_all = time.perf_counter()
    try:
        t0 = time.perf_counter()
        replay = _load_replay(path)
        result["timings_ms"]["parse"] = round((time.perf_counter() - t0) * 1000, 2)
    except (OSError, ValueError) as exc:
        result["attribution"] = {"category": "parse_error", "detail": str(exc)[:200]}
        result["wall_ms"] = round((time.perf_counter() - t_all) * 1000, 2)
        return result

    result["steps"] = len(replay.get("steps") or [])
    seed = (replay.get("info") or {}).get("seed")
    result["seed"] = seed
    rewards = twin.replay_final_rewards(replay)
    result["replay_rewards"] = rewards
    actions = twin.replay_transition_actions(replay)

    # ---- 1) 全程走子 + 逐步逐位比对 --------------------------------------
    state = twin.new_state_from_replay_head(replay, bundle)
    walk_ms = 0.0
    walk_ok = True
    compared = 0
    if compare_walk:
        t0 = time.perf_counter()
        for t in range(1, len(replay["steps"])):
            twin.step(state, actions[t - 1])
            ok, diffs = twin.states_bit_equal(state, replay, t)
            compared += 1
            if not ok:
                walk_ok = False
                result["walk"]["first_divergence"] = {
                    "step": t, "diffs": diffs}
                break
        walk_ms = (time.perf_counter() - t0) * 1000
    result["walk"]["compared"] = compared
    result["walk"]["pass"] = walk_ok
    result["timings_ms"]["walk"] = round(walk_ms, 2)

    # ---- 2) 中间步快照 -> 终局重演逐位比对 --------------------------------
    total_rollout_ms = 0.0
    total_rollout_steps = 0
    money = None
    bit_hex = None
    rollouts_ok = True
    if walk_ok:
        snaps = twin.rebuild_snapshots(replay, points, bundle)
        for point in points:
            snap = snaps[point]
            t0 = time.perf_counter()
            twin.run_to_end(snap, actions[point:])
            dt = (time.perf_counter() - t0) * 1000
            total_rollout_ms += dt
            total_rollout_steps += len(actions) - point
            money = twin.final_money(snap)
            truth = [None if r is None else float(r) for r in rewards]
            bit_ok = (money == truth and
                      [twin.money_bit_hex(m) for m in money] ==
                      [twin.money_bit_hex(r) for r in truth])
            rollouts_ok = rollouts_ok and bit_ok
            result["rollouts"].append({
                "step": point, "money": money, "bit_equal": bit_ok,
                "ms": round(dt, 2), "steps_run": len(actions) - point,
            })
        bit_hex = [twin.money_bit_hex(m) for m in (money or [])]
    result["final_money"] = money
    result["bit_hex"] = bit_hex
    result["rollouts_pass"] = rollouts_ok
    result["timings_ms"]["rollout_total"] = round(total_rollout_ms, 2)
    if total_rollout_steps:
        result["timings_ms"]["twin_step_ms"] = round(
            total_rollout_ms / total_rollout_steps, 4)

    # ---- 归因 -------------------------------------------------------------
    if not walk_ok:
        div = result["walk"]["first_divergence"] or {}
        diffs = div.get("diffs") or []
        paths = [d.get("path", "") for d in diffs]
        if seed is None and paths and all(
                p.startswith(".farms") or p.startswith(".town") for p in paths):
            category = "no_seed_random_divergence"
        else:
            category = "walk_divergence"
        result["attribution"] = {"category": category,
                                 "first_step": div.get("step"),
                                 "paths": paths[:6]}
    elif not rollouts_ok:
        result["attribution"] = {"category": "rollout_mismatch"}
    result["pass"] = bool(walk_ok and rollouts_ok)
    result["wall_ms"] = round((time.perf_counter() - t_all) * 1000, 2)
    return result


def run_gate(mode="official", games_limit=None, n_points=None,
             sample_seed=SAMPLE_SEED, data_root=None, out_path=None,
             summary_path=None, compare_walk=True, bench_games=12):
    """执行保真门，返回 (report, exit_code)。official 模式含基准测试。"""
    bundle = twin.load_engine()
    all_games = discover_games(data_root)
    if not all_games:
        return {"schema": SCHEMA, "error": "语料为空"}, 1
    if mode == "smoke":
        n_points = n_points or 2
        games = all_games[:4] if games_limit is None else all_games[:games_limit]
    else:
        n_points = n_points or 3
        games = all_games if games_limit is None else all_games[:games_limit]

    results = []
    bench = {"full_rollout_ms": [], "full_rollout_steps": [],
             "twin_step_ms": [], "compare_step_ms": []}
    bench_ids = set()
    if mode == "official":
        # 每组前若干局做整局纯 rollout 基准（无比对开销）。
        per_group = max(1, bench_games // len(CORPUS_GROUPS))
        seen = {}
        for group, path in all_games:
            seen.setdefault(group, 0)
            if seen[group] < per_group:
                bench_ids.add(path)
                seen[group] += 1

    t_gate = time.perf_counter()
    for group, path in games:
        points = sample_steps(f"{group}/{path.stem}", n_points, sample_seed)
        result = check_game(path, points, bundle, compare_walk=compare_walk)
        result["group"] = group
        results.append(result)

        if path in bench_ids:
            # 整局纯孪生 rollout（step 0 -> 终局，无比对）墙钟。
            replay = _load_replay(path)
            actions = twin.replay_transition_actions(replay)
            state = twin.new_state_from_replay_head(replay, bundle)
            t0 = time.perf_counter()
            twin.run_to_end(state, actions)
            dt = (time.perf_counter() - t0) * 1000
            bench["full_rollout_ms"].append(round(dt, 2))
            bench["full_rollout_steps"].append(len(actions))
            bench["twin_step_ms"].append(round(dt / max(1, len(actions)), 4))
            if result["timings_ms"].get("walk") and result["walk"]["compared"]:
                per_cmp = (result["timings_ms"]["walk"]
                           - (result["timings_ms"]["twin_step_ms"] or 0)
                           * result["walk"]["compared"]) / result["walk"]["compared"]
                bench["compare_step_ms"].append(round(max(0.0, per_cmp), 4))
    gate_ms = (time.perf_counter() - t_gate) * 1000

    games_n = len(results)
    sample_points_n = sum(len(r["sample_steps"]) for r in results
                          if r["rollouts"])
    walk_pass_n = sum(1 for r in results if r["walk"]["pass"])
    walk_compared_steps = sum(r["walk"]["compared"] for r in results)
    rollout_games_pass_n = sum(1 for r in results if r["rollouts_pass"])
    rollouts_n = sum(len(r["rollouts"]) for r in results)
    rollouts_bitexact_n = sum(1 for r in results
                              for ro in r["rollouts"] if ro["bit_equal"])
    passed_n = sum(1 for r in results if r["pass"])
    failures = [
        {"id": r["id"], "group": r["group"], "attribution": r["attribution"],
         "walk_first_divergence": r["walk"]["first_divergence"],
         "rollouts": r["rollouts"]}
        for r in results if not r["pass"]]

    def _stat(values):
        if not values:
            return None
        vals = sorted(values)
        n = len(vals)
        return {"n": n, "mean": round(sum(vals) / n, 4),
                "median": round(vals[n // 2], 4),
                "min": vals[0], "max": vals[-1]}

    full_ms = bench["full_rollout_ms"]
    full_steps = bench["full_rollout_steps"]
    median_ms = _stat(full_ms)["median"] if full_ms else None
    step_ms = _stat(bench["twin_step_ms"])
    cmp_ms = _stat(bench["compare_step_ms"])
    budget = {}
    if median_ms:
        budget = {
            "act_timeout_ms": 1000,
            "overage_pool_ms": 60000,
            "dawns_per_season": 30,
            "full_rollouts_per_turn_1s": int(1000 // median_ms),
            "full_rollouts_per_turn_with_pool_spread":
                int((1000 + 60000 / 30) // median_ms),
            "safety_margin_2x": int(1000 / 2 // median_ms),
            "safety_margin_5x": int(1000 / 5 // median_ms),
            "note": "评审机单核速度未知，按 2-5x 余量折算；透支池摊到 30 个黎明",
        }

    report = {
        "schema": SCHEMA,
        "mode": mode,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "engine_fingerprint": bundle.fingerprint,
        "corpus": {
            "groups": [g for g, _ in CORPUS_GROUPS],
            "games_discovered": len(all_games),
            "games_sampled": games_n,
            "sampling": {"seed": sample_seed, "windows": WINDOWS,
                         "points_per_game": n_points},
        },
        "verdict": {
            "games": games_n,
            "sample_points": sample_points_n,
            "walk_bitexact_games": walk_pass_n,
            "walk_bitexact_rate": round(walk_pass_n / games_n, 6) if games_n else 0,
            "walk_compared_steps": walk_compared_steps,
            "rollout_games_pass": rollout_games_pass_n,
            "rollouts_total": rollouts_n,
            "rollouts_bitexact": rollouts_bitexact_n,
            "rollout_bitexact_rate": round(rollouts_bitexact_n / rollouts_n, 6)
            if rollouts_n else 0,
            "games_pass": passed_n,
            "games_pass_rate": round(passed_n / games_n, 6) if games_n else 0,
            "overall_pass": passed_n == games_n and games_n > 0,
        },
        "benchmark": {
            "full_rollout_from_step0_ms": _stat(full_ms),
            "full_rollout_steps": _stat(full_steps),
            "twin_step_ms_pure": step_ms,
            "compare_step_ms": cmp_ms,
            "budget_per_dawn": budget,
        },
        "gate_wall_ms": round(gate_ms, 1),
        "failures": failures,
        "results": results,
    }

    out_path = Path(out_path) if out_path else REPORT_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    summary_path = Path(summary_path) if summary_path else SUMMARY_PATH
    if summary_path:
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(render_summary_md(report), encoding="utf-8")
    return report, 0 if report["verdict"]["overall_pass"] else 1


def render_summary_md(report):
    """精简台账（入库）：局数/步点数/通过率/逐位一致率/失败归因/指纹/基准。"""
    v = report["verdict"]
    b = report["benchmark"]
    fp = report["engine_fingerprint"]
    lines = [
        "# P1 孪生保真台账（twin_fidelity）",
        "",
        f"- 生成：{report['generated_at']}  模式：`{report['mode']}`  "
        f"门墙钟：{report['gate_wall_ms']:.0f} ms",
        f"- 指纹链：wheel `{fp['wheel']}`",
        f"  - wheel sha256 `{fp['wheel_sha256']}`",
        f"  - kaggriculture.py sha256 `{fp['scene_py_sha256']}`",
        f"  - kaggriculture.json sha256 `{fp['scene_json_sha256']}`",
        f"- 判据：全程走子逐步逐位比对 + 中间步注入重演终局资金逐位相等"
        f"（型别敏感，float 位型 hex 复核）。",
        "",
        "## 结论",
        "",
        f"- 语料：{report['corpus']['games_discovered']} 局可用，"
        f"抽样 {v['games']} 局 x {report['corpus']['sampling']['points_per_game']}"
        f" 步点（抽样种子 {report['corpus']['sampling']['seed']}，"
        f"早/中/晚窗 {report['corpus']['sampling']['windows']}）。",
        f"- 全程走子逐位一致：{v['walk_bitexact_games']}/{v['games']} 局"
        f"（{v['walk_bitexact_rate']*100:.2f}%），累计逐步比对 "
        f"{v.get('walk_compared_steps', 0)} 个步点。",
        f"- 终局重演逐位一致：{v['rollouts_bitexact']}/{v['rollouts_total']} 步点"
        f"（{v['rollout_bitexact_rate']*100:.2f}%）。",
        f"- **总体：{'PASS' if v['overall_pass'] else 'FAIL'}**"
        f"（通过 {v['games_pass']}/{v['games']} 局）。",
        "",
        "## 基准（本地实测，Python "
        f"{sys.version.split()[0]}）",
        "",
    ]
    if b.get("full_rollout_from_step0_ms"):
        s = b["full_rollout_from_step0_ms"]
        lines += [
            f"- 整局 rollout（step 0 -> 719，纯孪生、无比对）：中位 "
            f"{s['median']:.1f} ms（均值 {s['mean']:.1f}，min {s['min']:.1f}，"
            f"max {s['max']:.1f}，n={s['n']}）。",
            f"- 孪生单步：中位 {b['twin_step_ms_pure']['median']:.4f} ms/步"
            f"（含终局重演均值 {b['twin_step_ms_pure']['mean']:.4f}）。",
        ]
        if b.get("compare_step_ms"):
            lines.append(f"- 逐位比对开销：均值 {b['compare_step_ms']['mean']:.4f}"
                         f" ms/步（走子比对减去纯步进的摊余值）。")
        budget = b.get("budget_per_dawn") or {}
        if budget:
            lines += [
                "",
                "### 每黎明整局 rollout 预算（实测折算）",
                "",
                f"- 仅用 1s/回合 actTimeout：**{budget['full_rollouts_per_turn_1s']}"
                f" 条整局 rollout/黎明**。",
                f"- 加 60s 透支池摊 30 黎明（+2s/黎明）："
                f"**{budget['full_rollouts_per_turn_with_pool_spread']} 条/黎明**。",
                f"- 评审机安全余量 2x：{budget['safety_margin_2x']} 条；"
                f"5x：{budget['safety_margin_5x']} 条（余量依据：Kaggle 评审机"
                f"单核速度未知，engine-factsheet 风险①）。",
            ]
    lines += ["", "## 失败归因", ""]
    if not report["failures"]:
        lines.append("- 无失败例。")
    else:
        for f in report["failures"]:
            lines.append(f"- `{f['group']}/{f['id']}`："
                         f"{json.dumps(f['attribution'], ensure_ascii=False)}")
    lines += ["", "## 方法", "",
              "- 判据与口径细节见 "
              "`exports/probes/twin_fidelity/fidelity_report.json`（gitignored）",
              "  与 `scripts/twin_fidelity.py`（验收命令："
              "`python workspace/kaggriculture/software/scripts/twin_fidelity.py --mode official`）。",
              "- 孪生实现：`software/kaggle_simulations/agent/planner/twin.py`"
              "（stdlib-only；vendored 引擎指纹 fail-closed 校验；解释器零修改）。"]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mode", choices=["official", "smoke"], default="official")
    ap.add_argument("--games", type=int, default=None,
                    help="限制局数（默认 official=全语料，smoke=4）")
    ap.add_argument("--steps-per-game", type=int, default=None,
                    help="每局中间步点数（默认 official=3，smoke=2）")
    ap.add_argument("--sample-seed", type=int, default=SAMPLE_SEED)
    ap.add_argument("--data-root", default=None)
    ap.add_argument("--out", default=None, help="fidelity_report.json 路径")
    ap.add_argument("--summary", default=None,
                    help="p1_fidelity_summary.md 路径（传 '' 跳过台账写出）")
    ap.add_argument("--no-walk-compare", action="store_true",
                    help="跳过全程逐步比对（仅中间步重演判据）")
    args = ap.parse_args()

    if args.summary == "":
        summary_path = None
    elif args.summary:
        summary_path = Path(args.summary)
    else:
        summary_path = SUMMARY_PATH

    report, code = run_gate(
        mode=args.mode,
        games_limit=args.games,
        n_points=args.steps_per_game,
        sample_seed=args.sample_seed,
        data_root=args.data_root,
        out_path=args.out,
        summary_path=summary_path,
        compare_walk=not args.no_walk_compare)
    v = report["verdict"]
    print(json.dumps({
        "mode": report["mode"],
        "games": v["games"],
        "sample_points": v["sample_points"],
        "walk_bitexact_games": v["walk_bitexact_games"],
        "rollout_bitexact_rate": v["rollout_bitexact_rate"],
        "games_pass": v["games_pass"],
        "overall_pass": v["overall_pass"],
    }, ensure_ascii=False))
    out = args.out or str(REPORT_PATH)
    print(f"report -> {out}")
    print(f"summary -> {args.summary if args.summary else SUMMARY_PATH}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
