# -*- coding: utf-8 -*-
"""票 03 第 2 轮：最好 BC 候选的种子稳定性（合成季 × v48 路由陪练）.

动机：M1 的"2/8 动物经济路径"经席位 bug 修复后判定为 harness 伪影，
原定"对该路径做种子敏感性"失去对象；改为对**票 03 最好候选**
（A2 开局剧本注入 + schema 1.2 模型 + 市场解码约束）做同对手多种子
测试——固定陪练 = v48 'default' 719 步路由（解码件开环回放），只变
引擎种子（杂草生成/商店解锁/城镇消费随机源），隔离种子方差。

协议：twin 合成季头（planner_flagoff_golden.synthetic_season_head 同构：
NW 解锁、$3000、零棚零种、I0/base 全品市价表），BC 坐 seat0，v48 路由
坐 seat1，整季 720 步；逐日记录资金轨迹。

用法：
    python bc_track/scripts/bc_seed_stability.py --seeds 11 23 47 101
"""
from __future__ import annotations

import argparse
import ast
import base64
import json
import statistics
import sys
import zlib
from pathlib import Path

BC_DIR = Path(__file__).resolve().parent
SOFTWARE = BC_DIR.parents[1]
sys.path.insert(0, str(BC_DIR))
sys.path.insert(0, str(SOFTWARE))
sys.path.insert(0, str(SOFTWARE / "scripts"))

from kaggle_simulations.agent.planner import twin          # noqa: E402
from bc_policy import BCPolicy                              # noqa: E402
from bc_opening import OpeningScriptPolicy                 # noqa: E402
from bc_decode import MarketDecodePolicy                    # noqa: E402
from bc_eval import Recorder                                # noqa: E402

V48BUILD = (SOFTWARE.parent / "references" / "data" / "intel-notebooks"
            / "v48build" / "main.py")
EXPORTS = SOFTWARE / "bc_track" / "exports"
EPISODE_STEPS = 720
BOARD = 10
STARTING_MONEY = 3000.0


def load_v48_default_route() -> list:
    """解码 v48 'default' 路由（AST 提取 zlib+b85 payload，只读不改）。"""
    tree = ast.parse(V48BUILD.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if getattr(t, "id", "") == "_V48_ROUTES":
                    outer = node.value.args[0]
                    b85str = outer.func.value.args[0].args[0].value
                    payload = json.loads(zlib.decompress(
                        base64.b85decode(b85str)).decode("utf-8"))
                    return payload["default"]
    raise RuntimeError("_V48_ROUTES not found in v48build/main.py")


def synthetic_head(module, seed):
    """合成整季回放头（与 planner_flagoff_golden.synthetic_season_head
    同构：NW 解锁、$3000、零棚零种、无预解锁商店、I0/base 全品表）。"""
    tiles = []
    for y in range(BOARD):
        row = []
        for x in range(BOARD):
            quadrant = ("N" if y < BOARD // 2 else "S") + \
                       ("W" if x < BOARD // 2 else "E")
            row.append(None if quadrant == "NW" else "LOCKED")
        tiles.append(row)

    def farm():
        return {"money": float(STARTING_MONEY),
                "tiles": json.loads(json.dumps(tiles)),
                "farmer": [BOARD // 2 - 1, BOARD // 2 - 1], "hands": [],
                "unlocked_quadrants": ["NW"], "hires_today": 0}

    def private():
        return {"shed": dict.fromkeys(list(module.PRODUCTS)
                                      + list(module.ANIMALS), 0),
                "seeds": dict.fromkeys(module.CROPS, 0),
                "inventories": [{}]}

    market = {
        "inventory": {item: module.MARKET_PARAMS[item]["I0"]
                      for item in module.PRODUCTS},
        "prices": {item: module.MARKET_PARAMS[item]["base"]
                   for item in module.PRODUCTS},
    }
    head = []
    for player in (0, 1):
        obs = {"farms": [farm() for _ in range(2)],
               "market": json.loads(json.dumps(market)),
               "town": {"unlocked_shops": []},
               "day": 0, "hour": 0, "step": 0 if player == 0 else None,
               "player": player, "private": private(),
               "remainingOverageTime": 60}
        head.append({"action": None, "observation": obs if player == 0 else {},
                     "status": "ACTIVE"})
    return {"steps": [head],
            "configuration": {"episodeSteps": EPISODE_STEPS, "seed": seed},
            "info": {"seed": seed}, "rewards": [0, 0]}


def build_policy(model_path):
    base = BCPolicy(model_path, collect_stats=False)
    return MarketDecodePolicy(
        OpeningScriptPolicy(base, 96, collect_stats=False, units=True))


def run_seed(seed, route, model_path):
    bundle = twin.load_engine()
    replay = synthetic_head(bundle.module, seed)
    state = twin.new_state_from_replay_head(replay, bundle)
    policy = build_policy(model_path)
    rec = Recorder(policy, f"bc-seed{seed}")
    money_by_day = {}
    taken = 0
    while not state.env.done and taken < EPISODE_STEPS:
        obs = state.seats[0].observation
        mine = rec(obs)
        theirs = route[taken] if taken < len(route) else \
            {"farmer": ["PASS"], "hands": [], "market": []}
        twin.step(state, [mine, theirs])
        day = int(obs.day)
        money_by_day[day] = float(state.seats[0].observation.farms[0]
                                  ["money"])
        taken += 1
    finals = twin.final_money(state)
    return {"seed": seed, "final_me": finals[0], "final_opp": finals[1],
            "steps": taken, "money_by_day": money_by_day,
            "diag": rec.diagnostics()}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seeds", type=int, nargs="+", default=[11, 23, 47, 101])
    ap.add_argument("--model", default=str(SOFTWARE / "bc_track" / "models"
                                           / "bc_model_v2.py"))
    ap.add_argument("--out", default="seed_stability")
    args = ap.parse_args(argv)

    route = load_v48_default_route()
    rows = []
    for seed in args.seeds:
        row = run_seed(seed, route, args.model)
        rows.append(row)
        print(f"[seed {seed}] BC={row['final_me']:.0f} "
              f"v48route={row['final_opp']:.0f} steps={row['steps']} "
              f"move={row['diag']['unit_move_rate']:.1%} "
              f"CARE={row['diag']['care_total']}")

    finals = [r["final_me"] for r in rows]
    report = {
        "protocol": "synthetic-season x v48-default-route opponent / "
                    "best candidate = A2 opening(96, units) + schema1.2 "
                    "v2 model + market decode shim",
        "model": args.model,
        "seeds": args.seeds,
        "summary": {
            "n": len(finals),
            "median": statistics.median(finals),
            "mean": statistics.mean(finals),
            "min": min(finals), "max": max(finals),
            "collapse_lt_45k": sum(1 for m in finals if m < 45_000),
            "wins_vs_v48route": sum(1 for r in rows
                                    if r["final_me"] > r["final_opp"]),
        },
        "games": rows,
    }
    EXPORTS.mkdir(parents=True, exist_ok=True)
    out = EXPORTS / f"{args.out}.json"
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    print(json.dumps(report["summary"], indent=1))
    print(f"[seed-stability] -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
