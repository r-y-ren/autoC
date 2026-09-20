# -*- coding: utf-8 -*-
"""Track-C (BC) M1-2: 评估 harness（spec User Story 7/8/9）.

协议（复用既有评估缝，不新造）：
  - 孪生 d0 全季注入：twin.build_state_from_replay(replay, 0) 起整季，
    我方席 = 待评 agent（官方语义 callable），对手席 = 回放真实动作
    （planner_offline_bench.rollout_with_replay_opponent 同口径）；
  - 对照组：v14.2 基线 = build_v13_namespace()（src/ 九模块 exec 装载），
    同局同席同对手流——单变量对比；
  - 评估局 = 训练 held-out 局（bc_track/data/split.json，game 级隔离，
    两席专家样本都不进训练）。

输出：
  - bc_track/exports/eval_v1.json   逐局 W/L、终局资金、行为诊断
  - bc_track/exports/eval_v1.md     人读摘要

用法：
  python bc_track/scripts/bc_eval.py --games 8
"""
from __future__ import annotations

import argparse
import glob
import json
import statistics
import sys
import time
import traceback
from collections import Counter
from pathlib import Path

BC_DIR = Path(__file__).resolve().parent
SOFTWARE = BC_DIR.parents[1]
sys.path.insert(0, str(BC_DIR))
sys.path.insert(0, str(SOFTWARE))

import bc_schema as S                                     # noqa: E402
from bc_policy import BCPolicy, to_plain_obs              # noqa: E402

TWIN_IMPORT_ERROR = None
try:
    from kaggle_simulations.agent.planner import twin     # noqa: E402
    sys.path.insert(0, str(SOFTWARE / "scripts"))
    from planner_offline_bench import build_v13_namespace  # noqa: E402
except Exception as _exc:                                 # noqa: BLE001
    TWIN_IMPORT_ERROR = f"{type(_exc).__name__}: {_exc}"

REPLAY_ROOTS = [SOFTWARE.parent / "references" / "data" / "online-replays"
                / "bc-top"]
ROUND_ROOT = SOFTWARE.parent / "references" / "data" / "online-replays"
EXPORTS = SOFTWARE / "bc_track" / "exports"
DATA = SOFTWARE / "bc_track" / "data"
DIRS = {"NORTH", "SOUTH", "EAST", "WEST"}


def build_replay_index() -> dict[str, Path]:
    """replay['id'] -> 路径（bc-top + round*）。"""
    index: dict[str, Path] = {}
    for root in REPLAY_ROOTS:
        for path in sorted(glob.glob(str(root / "episode-*.json"))):
            try:
                rid = json.load(open(path, encoding="utf-8")).get("id")
            except (OSError, ValueError):
                continue
            if rid:
                index[str(rid)] = Path(path)
    if ROUND_ROOT.is_dir():
        for rnd in sorted(p for p in ROUND_ROOT.iterdir()
                          if p.name.startswith("round") and p.is_dir()):
            for path in sorted(glob.glob(str(rnd / "episode-*.json"))):
                try:
                    rid = json.load(open(path, encoding="utf-8")).get("id")
                except (OSError, ValueError):
                    continue
                if rid:
                    index[str(rid)] = Path(path)
    return index


def pick_me_seat(replay: dict, top_teams: dict) -> int:
    """评估席选择：优先 top-30 队席（对手=非 top 席真实动作，贴梯局面）；
    否则 seat 0。确定性：两队都在/都不在取 0。"""
    teams = (replay.get("info") or {}).get("TeamNames") or []
    flags = [t in top_teams for t in teams]
    if sum(flags) == 1:
        return flags.index(True)
    return 0


def tally_action(action: dict) -> dict:
    """行为诊断计数（与 BCPolicy._tally_unit 同口径，供基线用）。"""
    out = Counter()
    for act in [action.get("farmer")] + list(action.get("hands") or []):
        if not act:
            continue
        op = act[0]
        out["unit_total"] += 1
        if op in DIRS:
            out["unit_move"] += 1
        elif op == "PASS":
            out["unit_pass"] += 1
        else:
            out[f"unit_{op}"] += 1
    for order in action.get("market") or []:
        if order:
            out[f"mkt_{order[0]}"] += 1
            out["mkt_orders"] += 1
    return dict(out)


class Recorder:
    """agent 包装器：记录行为诊断 + 异常计数（异常回合降级 PASS）。"""

    def __init__(self, agent_fn, name):
        self.agent_fn = agent_fn
        self.name = name
        self.tally: Counter = Counter()
        self.errors = 0
        self.last_error = ""
        self.hires_per_day: dict[int, int] = {}
        self._day = -1
        self.market_trace_d0d3: list = []   # (step, orders)，取证用

    def __call__(self, obs):
        plain = to_plain_obs(obs)
        day = int(plain.get("day") or 0)
        step = plain.get("step")
        if step is None:
            step = day * 24 + int(plain.get("hour") or 0)
        try:
            action = self.agent_fn(obs)
        except Exception as exc:                           # noqa: BLE001
            self.errors += 1
            self.last_error = f"{type(exc).__name__}: {exc}"
            action = {"farmer": ["PASS"], "hands": [], "market": []}
        if day != self._day:
            self._day = day
        if int(step) < 96:
            self.market_trace_d0d3.append(
                (int(step), [list(o) for o in action.get("market") or []]))
        for k, v in tally_action(action).items():
            self.tally[k] += v
        self.hires_per_day[day] = self.hires_per_day.get(day, 0) + sum(
            1 for o in action.get("market") or [] if o and o[0] == "HIRE")
        return action

    def diagnostics(self) -> dict:
        t = self.tally
        n = max(t.get("unit_total", 0), 1)
        hires = self.hires_per_day
        return {
            "unit_move_rate": round(t.get("unit_move", 0) / n, 4),
            "unit_pass_rate": round(t.get("unit_pass", 0) / n, 4),
            "care_total": t.get("unit_CARE", 0),
            "water_total": t.get("unit_WATER", 0),
            "harvest_total": t.get("unit_HARVEST", 0),
            "unit_total": t.get("unit_total", 0),
            "mkt_orders": t.get("mkt_orders", 0),
            "mkt_sell": t.get("mkt_SELL", 0),
            "mkt_hire": t.get("mkt_HIRE", 0),
            "mkt_buy_seed": t.get("mkt_BUY_SEED", 0),
            "mkt_buy_animal": t.get("mkt_BUY_ANIMAL", 0),
            "mkt_buy_product": t.get("mkt_BUY_PRODUCT", 0),
            "mkt_buy_land": t.get("mkt_BUY_LAND", 0),
            "hires_total": sum(hires.values()),
            "hire_days_active": sum(1 for v in hires.values() if v > 0),
            "errors": self.errors,
            "last_error": self.last_error,
        }


def rollout(state, me_seat, agent_fn, opp_actions):
    """整季 rollout（planner_offline_bench.rollout_with_replay_opponent
    同构，本地展开以便异常兜底在 Recorder 内做）。

    席位修正（票 03，2026-09-20）：动作必须按席位索引提交——me_seat=1 时
    BC 动作给 seats[1]、回放对手动作给 seats[0]。M1 版本恒以
    [mine, theirs] 提交，me_seat=1 的 2 局（951e3540/f010fe7c）实为
    "BC 动作进了 seat0、顶级回放动作进了 seat1"，其 132-157k 是回放动作
    流的产物（harness 伪影），已判定为无效对照。
    """
    taken = 0
    max_steps = 720
    me_seat = int(me_seat)
    while not state.env.done and taken < len(opp_actions) \
            and taken < max_steps:
        obs = state.seats[me_seat].observation
        mine = agent_fn(obs)
        theirs = opp_actions[taken][1 - me_seat]
        actions = [None, None]
        actions[me_seat] = mine
        actions[1 - me_seat] = theirs
        twin.step(state, actions)
        taken += 1
    return twin.final_money(state), taken


def main(argv=None) -> int:
    if TWIN_IMPORT_ERROR is not None:
        sys.stderr.write(f"[exit 2] 依赖不可用: {TWIN_IMPORT_ERROR}\n")
        return 2
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--games", type=int, default=8)
    ap.add_argument("--model", default=None)
    ap.add_argument("--skip-baseline", action="store_true")
    ap.add_argument("--out", default="eval_v1")
    ap.add_argument("--opening", type=int, default=0,
                    help=">0 = 前 N 步市场订单走 v48 剧本先验"
                         "（bc_opening.OpeningScriptPolicy；0=关）")
    ap.add_argument("--opening-units", action="store_true",
                    help="开局剧本连单位动作一起注入（A2 全剧本模式；"
                         "需 --opening >0）")
    ap.add_argument("--decode", action="store_true",
                    help="市场头 state-grounded 解码约束（bc_decode："
                         "SELL 锚定棚存/HIRE 去重/BUY 预算掩码）")
    args = ap.parse_args(argv)

    t0 = time.time()
    split = json.loads((DATA / "split.json").read_text(encoding="utf-8"))
    held = split["heldout_games"]
    index = build_replay_index()
    top_teams = {}
    import csv
    lb = (SOFTWARE.parent / "references" / "data" / "lb-snapshot-20260920"
          / "kaggriculture-publicleaderboard-2026-09-20T02_21_40.csv")
    with open(lb, "r", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            try:
                if 1 <= int(row["Rank"]) <= 30:
                    top_teams[row["TeamName"]] = int(row["Rank"])
            except (KeyError, ValueError):
                continue

    # 确定性选局：bc-top 优先（对手流覆盖当前 meta），不足补 local
    games = [g for g in held if g.startswith("bc-top:")]
    games += [g for g in held if g.startswith("local:")]
    games = games[:args.games]
    print(f"[eval] held-out games={len(held)} -> evaluating {len(games)}")

    twin.load_engine()
    policy = BCPolicy(args.model, collect_stats=False)
    if args.opening > 0:
        from bc_opening import OpeningScriptPolicy
        policy = OpeningScriptPolicy(policy, until_step=args.opening,
                                     collect_stats=False,
                                     units=args.opening_units)
    if args.decode:
        from bc_decode import MarketDecodePolicy
        policy = MarketDecodePolicy(policy, collect_stats=False)

    rows = []
    for gkey in games:
        rid = gkey.split(":", 1)[1]
        path = index.get(rid)
        if not path:
            print(f"[eval] {gkey}: replay not found, skip")
            continue
        replay = json.loads(path.read_text(encoding="utf-8"))
        teams = (replay.get("info") or {}).get("TeamNames") or ["?", "?"]
        me_seat = pick_me_seat(replay, top_teams)
        acts = twin.replay_transition_actions(replay)
        truth = [float(x) for x in replay.get("rewards") or [0, 0]]

        row = {"game": gkey, "teams": teams, "me_seat": me_seat,
               "truth": truth, "episode": replay.get("info", {}).get(
                   "EpisodeId")}
        # --- BC ---
        bc_rec = Recorder(policy, "bc")
        state = twin.build_state_from_replay(replay, 0)
        t_g = time.time()
        finals, taken = rollout(state, me_seat, bc_rec, acts)
        row["bc"] = {
            "final_me": finals[me_seat], "final_opp": finals[1 - me_seat],
            "win": finals[me_seat] > finals[1 - me_seat],
            "wall_s": round(time.time() - t_g, 1), "steps": taken,
            "diag": bc_rec.diagnostics(),
            "market_trace_d0d3": [
                (s, o) for s, o in bc_rec.market_trace_d0d3 if o],
        }
        # --- v14.2 基线（同局同席同对手流） ---
        if not args.skip_baseline:
            try:
                ns, _applied, _skipped = build_v13_namespace(None)
                base_fn = ns["agent"]
            except Exception as exc:                       # noqa: BLE001
                row["baseline"] = {"error": f"{type(exc).__name__}: {exc}"}
                base_fn = None
            if base_fn is not None:
                base_rec = Recorder(base_fn, "v14.2")
                state = twin.build_state_from_replay(replay, 0)
                t_g = time.time()
                finals_b, _tb = rollout(state, me_seat, base_rec, acts)
                row["baseline"] = {
                    "final_me": finals_b[me_seat],
                    "final_opp": finals_b[1 - me_seat],
                    "win": finals_b[me_seat] > finals_b[1 - me_seat],
                    "wall_s": round(time.time() - t_g, 1),
                    "diag": base_rec.diagnostics(),
                }
        rows.append(row)
        del replay
        print(f"[eval] {gkey} me_seat={me_seat} teams={teams} "
              f"BC={row['bc']['final_me']:.0f} "
              f"base={row.get('baseline', {}).get('final_me', float('nan')):.0f}"
              f" truth_me={truth[me_seat]:.0f}")

    # ---- 汇总 ----
    bc_money = [r["bc"]["final_me"] for r in rows]
    bc_wins = sum(1 for r in rows if r["bc"]["win"])
    base_rows = [r for r in rows if "final_me" in r.get("baseline", {})]
    base_money = [r["baseline"]["final_me"] for r in base_rows]
    base_wins = sum(1 for r in base_rows if r["baseline"]["win"])
    h2h = [1 if r["bc"]["final_me"] > r["baseline"]["final_me"]
           else 0 if r["bc"]["final_me"] < r["baseline"]["final_me"] else -1
           for r in base_rows]
    diffs = [r["bc"]["final_me"] - r["baseline"]["final_me"] for r in base_rows]
    bc_med = statistics.median(bc_money) if bc_money else None
    base_med = statistics.median(base_money) if base_money else None
    summary = {
        "n_games": len(rows),
        "bc_wins_vs_replay_opp": bc_wins,
        "baseline_wins_vs_replay_opp": base_wins,
        "bc_median_money": bc_med,
        "baseline_median_money": base_med,
        "bc_mean_money": statistics.mean(bc_money) if bc_money else None,
        "baseline_mean_money": (statistics.mean(base_money)
                                if base_money else None),
        "h2h_bc_wins": sum(1 for x in h2h if x == 1),
        "h2h_baseline_wins": sum(1 for x in h2h if x == 0),
        "h2h_ties": sum(1 for x in h2h if x == -1),
        "h2h_median_diff": statistics.median(diffs) if diffs else None,
        "h2h_mean_diff": statistics.mean(diffs) if diffs else None,
        "collapse_lt_45k_bc": sum(1 for m in bc_money if m < 45_000),
        "collapse_lt_45k_baseline": sum(1 for m in base_money if m < 45_000),
        "bc_move_rate_mean": statistics.mean(
            r["bc"]["diag"]["unit_move_rate"] for r in rows) if rows else None,
        "bc_pass_rate_mean": statistics.mean(
            r["bc"]["diag"]["unit_pass_rate"] for r in rows) if rows else None,
        "bc_care_mean": statistics.mean(
            r["bc"]["diag"]["care_total"] for r in rows) if rows else None,
        "base_move_rate_mean": statistics.mean(
            r["baseline"]["diag"]["unit_move_rate"]
            for r in base_rows) if base_rows else None,
        "base_pass_rate_mean": statistics.mean(
            r["baseline"]["diag"]["unit_pass_rate"]
            for r in base_rows) if base_rows else None,
        "base_care_mean": statistics.mean(
            r["baseline"]["diag"]["care_total"]
            for r in base_rows) if base_rows else None,
        "bc_errors_total": sum(r["bc"]["diag"]["errors"] for r in rows),
    }
    report = {
        "protocol": "twin-d0-fullseason / opponent=replay-actions / "
                    "baseline=build_v13_namespace (v14.2 src/)",
        "model": args.model or str(SOFTWARE / "bc_track" / "models"
                                   / "bc_model_v1.py"),
        "schema": S.SCHEMA_VERSION,
        "opening_script_steps": args.opening,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": summary,
        "games": rows,
        "wall_seconds": round(time.time() - t0, 1),
    }
    EXPORTS.mkdir(parents=True, exist_ok=True)
    out_json = EXPORTS / f"{args.out}.json"
    out_json.write_text(json.dumps(report, indent=1, ensure_ascii=False),
                        encoding="utf-8")

    def _fmt_pct(v):
        return f"{v:.1%}" if v is not None else "n/a"

    def _fmt_or(v):
        return f"{v:.0f}" if v is not None else "n/a"

    md = ["# Track-C BC 首跑评估（bc_eval）", "",
          f"- 协议：{report['protocol']}",
          f"- 局数：{summary['n_games']}（held-out，训练零泄漏）",
          f"- BC median={_fmt_or(summary['bc_median_money'])}"
          f" vs v14.2 median={_fmt_or(summary['baseline_median_money'])}",
          f"- H2H（同局同对手流）：BC {summary['h2h_bc_wins']} — "
          f"{summary['h2h_baseline_wins']} v14.2（tie {summary['h2h_ties']}）；"
          f"median Δ={_fmt_or(summary['h2h_median_diff'])}",
          f"- 塌方带（<45k）：BC {summary['collapse_lt_45k_bc']} / "
          f"v14.2 {summary['collapse_lt_45k_baseline']}",
          f"- 行为：BC move={summary['bc_move_rate_mean']:.1%} "
          f"pass={summary['bc_pass_rate_mean']:.1%} "
          f"CARE={summary['bc_care_mean']:.0f} | "
          f"v14.2 move={_fmt_pct(summary['base_move_rate_mean'])} "
          f"pass={_fmt_pct(summary['base_pass_rate_mean'])} "
          f"CARE={_fmt_or(summary['base_care_mean'])}",
          f"- X-ray 榜首参照：move 53.8% / pass 3.8% / CARE 348",
          f"- BC agent 异常：{summary['bc_errors_total']}", "",
          "| 局 | BC | v14.2 | 真值 | BC W | v14.2 W |",
          "|---|---:|---:|---:|---|---|"]
    for r in rows:
        b = r.get("baseline", {}).get("final_me")
        b_txt = f"{b:.0f}" if b is not None else "n/a"
        w_txt = ("W" if r.get("baseline", {}).get("win")
                 else "L" if "win" in r.get("baseline", {}) else "?")
        md.append(f"| {r['game'][:40]} | {r['bc']['final_me']:.0f} "
                  f"| {b_txt} | {r['truth'][r['me_seat']]:.0f} "
                  f"| {'W' if r['bc']['win'] else 'L'} "
                  f"| {w_txt} |")
    (EXPORTS / f"{args.out}.md").write_text("\n".join(md) + "\n",
                                            encoding="utf-8")
    print(f"[eval] done wall={report['wall_seconds']}s -> {out_json}")
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
