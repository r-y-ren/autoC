# 【中文】v15_h2h_v48.py —— v15 波次剧本候选 vs v48（解码真源码）本地 h2h
# ===========================================================================
# 背景（M-E1 验证门）：h2h_v48.json 基准 = 我方旧候选对 v48 16 局 0-16、
#   场均净负 -68.4k/-71.0k（2026-08-31，双席位）。v15「点火重构」的判据：
#   场均差距从 -68k 显著收窄（目标 ≤ -20k 或出现胜局），0-16 不允许复现。
# 对手 = 解码 v48 真源码（references/data/intel-notebooks/v48_main.py，
#   与 v48build/main.py 及 submission.tar.gz 字节一致，digest 已验）。
# 协议：官方 vendored 引擎（kgenv.arena.run_episode）16 局 = seeds
#   (101,102,103,104,201,202,203,204) × 双席位（我方 seat0/seat1 各 8），
#   与 h2h_v48.json 域一致；逐局记 rewards / daily money → m5k 点火日
#   （首次 money ≥ 5000 的 day，day = step//24）。
# 两种口径（诊断分层）：
#   shipped   = 提交形态 main.py（DTSP 黎明三选一，剧本候选由 rollout 仲裁）
#   wave-forced = PLANNER_OVERRIDES.wave_mode 预置（剧本强制为脑，诊断用）
# 胜负口径：终局钱数定胜负（赢 $1=赢，官方机制 #742083）。
# CLI：
#   python scripts/v15_h2h_v48.py                 # shipped 16 局
#   python scripts/v15_h2h_v48.py --mode forced   # wave-forced 16 局
#   python scripts/v15_h2h_v48.py --baseline      # 旗关 v13.8 基线 16 局
#   python scripts/v15_h2h_v48.py --seeds 101,102 --seats 0   # 快速冒烟
# 输出：exports/probes/v15_ignition/v15_h2h_v48_<mode>.json
# ===========================================================================

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
ROOT = os.path.dirname(SOFTWARE)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

from kgenv.arena import (SUBMISSION_MAIN, load_submission_agent,  # noqa: E402
                         run_episode)

# 对手 = 解码 v48 真源码（v48build/main.py，sha256 dadee25a…2664a——
# digest 已验证与 v48_main.py 内嵌断言及其 submission.tar.gz 逐字节一致；
# 不跑 v48_main.py 构建器：它向 CWD 落盘，违 D14 圈禁）。
V48_PATH = os.path.join(ROOT, "references", "data", "intel-notebooks",
                        "v48build", "main.py")
OUT_DIR = os.path.join(SOFTWARE, "exports", "probes", "v15_ignition")
SEASON_DAYS = 30
TURNS_PER_DAY = 24
M5K = 5000.0
BASELINE_SEEDS = (101, 102, 103, 104, 201, 202, 203, 204)


def ignition_day(daily_money):
    """m5k 点火日：首次日终 money ≥ 5000 的 day（0-based；未点火 = 99）。"""
    for day, m in enumerate(daily_money or []):
        if m is not None and m >= M5K:
            return day
    return 99


def load_v48_agent():
    loader = load_submission_agent          # get_last_callable 同语义
    return loader(V48_PATH)


def load_our_agent(mode):
    """shipped = main.py 原样；forced = 装载后预置剧本总闸。

    自行 spec 装载（与 kgenv.arena.load_submission_agent 同语义）以持有
    模块引用——main.py 装载期把 src 展开进其 globals，直接写剧本总闸。"""
    if mode != "forced":
        return load_submission_agent(SUBMISSION_MAIN)
    import importlib.util
    path = os.path.abspath(SUBMISSION_MAIN)
    spec = importlib.util.spec_from_file_location("v15_forced_candidate",
                                                  path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PLANNER_ENABLED = True
    module.PLANNER_OVERRIDES["wave_mode"] = True
    return module.agent


def load_flagoff_agent():
    """旗关基线：裸 src 命名空间（无 DTSP 配置名 → 钩子死路）。"""
    ns = {}
    exec("; ".join(("import copy", "import math", "import json",
                    "import hashlib")), ns)
    for mod in ("constants", "telemetry", "observer", "strategy", "mission",
                "solver", "executor", "market", "wave", "entry"):
        path = os.path.join(SOFTWARE, "kaggle_simulations", "agent", "src",
                            mod + ".py")
        with open(path, "r", encoding="utf-8") as handle:
            exec(compile(handle.read(), path, "exec"), ns)
    return ns["agent"]


def seat_daily(res, seat):
    """run_episode 的 daily_money -> 该席逐日 money 列表（day 序）。"""
    daily = res.get("daily_money") or []
    return [entry.get("money", [None, None])[seat] for entry in daily
            if isinstance(entry, dict)]


def run_one(our_fn, v48_fn, seed, our_seat):
    """单局：我方 our_seat 席，v48 对手席。返回结构化逐局记录。"""
    if our_seat == 0:
        res = run_episode(our_fn, v48_fn, seed, collect_daily=True)
    else:
        res = run_episode(v48_fn, our_fn, seed, collect_daily=True)
    rewards = res["rewards"]
    mine = float(rewards[our_seat])
    theirs = float(rewards[1 - our_seat])
    return {
        "seed": seed, "our_seat": our_seat,
        "our_money": mine, "v48_money": theirs,
        "margin": round(mine - theirs, 1),
        "win": mine > theirs, "tie": mine == theirs,
        "our_ignition_day": ignition_day(seat_daily(res, our_seat)),
        "v48_ignition_day": ignition_day(seat_daily(res, 1 - our_seat)),
        "turns": res.get("turns_played"),
        "statuses": res.get("statuses"),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="v15 vs v48 local h2h (M-E1 gate)")
    ap.add_argument("--mode", choices=("shipped", "forced"), default="shipped")
    ap.add_argument("--baseline", action="store_true",
                    help="旗关 v13.8 基线口径（ignore --mode）")
    ap.add_argument("--seeds", default=",".join(map(str, BASELINE_SEEDS)))
    ap.add_argument("--seats", default="0,1")
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    seeds = [int(s) for s in str(args.seeds).split(",") if s != ""]
    seats = [int(s) for s in str(args.seats).split(",") if s != ""]

    t0 = time.time()
    if args.baseline:
        label, our_fn = "flagoff_v138", load_flagoff_agent()
    else:
        label, our_fn = f"v15_{args.mode}", load_our_agent(args.mode)
    v48_fn = load_v48_agent()

    games = []
    for seed in seeds:
        for seat in seats:
            t1 = time.time()
            rec = run_one(our_fn, v48_fn, seed, seat)
            rec["wall_s"] = round(time.time() - t1, 1)
            games.append(rec)
            print(f"[{label}] seed={seed} seat={seat} "
                  f"ours={rec['our_money']:9.0f} v48={rec['v48_money']:9.0f} "
                  f"margin={rec['margin']:+10.0f} "
                  f"{'WIN' if rec['win'] else ('TIE' if rec['tie'] else 'LOSS')} "
                  f"ign(d) ours={rec['our_ignition_day']} "
                  f"v48={rec['v48_ignition_day']} [{rec['wall_s']}s]",
                  flush=True)

    n = len(games)
    wins = sum(1 for g in games if g["win"])
    ties = sum(1 for g in games if g["tie"])
    avg_margin = sum(g["margin"] for g in games) / max(1, n)
    our_ign = [g["our_ignition_day"] for g in games if g["our_ignition_day"] < 99]
    v48_ign = [g["v48_ignition_day"] for g in games if g["v48_ignition_day"] < 99]
    summary = {
        "label": label, "n_games": n,
        "wins": wins, "losses": sum(1 for g in games if not g["win"]
                                    and not g["tie"]), "ties": ties,
        "avg_margin": round(avg_margin, 1),
        "best_margin": round(max(g["margin"] for g in games), 1),
        "worst_margin": round(min(g["margin"] for g in games), 1),
        "our_ignition_days": our_ign,
        "v48_ignition_days": v48_ign,
        "our_ignition_median": sorted(our_ign)[len(our_ign) // 2] if our_ign else None,
        "gate": {
            "no_0_16_repeat": not (wins == 0 and ties == 0 and n >= 16),
            "avg_margin_le_minus20k_or_win": avg_margin > -20000.0 or wins > 0,
        },
        "games": games,
        "wall_total_s": round(time.time() - t0, 1),
    }
    out = args.out or os.path.join(OUT_DIR, f"v15_h2h_v48_{label}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as h:
        json.dump(summary, h, ensure_ascii=False, indent=1)
    print(json.dumps({k: summary[k] for k in
                      ("label", "n_games", "wins", "losses", "ties",
                       "avg_margin", "our_ignition_median", "gate")},
                     ensure_ascii=False))
    print(f"out -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
