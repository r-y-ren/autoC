# 【中文】planner_flagoff_golden.py —— DTSP 惰性旋钮旗关等价·黄金动作哈希
# ===========================================================================
# 用途（蓝图 m7 修订授权，2026-09-19）：钉住"PLANNER_ENABLED=False 时行为
#   与现役 v13.8 逐字节等价"（沿 ROUTE_EXECUTOR 开旗先例）。
# 机理：孪生直驱全季自博弈（v13.8 双席同一命名空间），逐步捕获双方动作流，
#   canonical JSON（sort_keys+紧凑分隔符）后 sha256。黄金基线在 src 扩展
#   落地【前】从 v13.8 工作树捕获并冻结到
#   exports/probes/planner_flagoff/golden_v138.json（含引擎指纹链与种子表）；
#   之后的任何 src/ 改动都必须在旗关下复现同一哈希，否则视为破坏现役行为。
# 种子表：>=6 个全季种子（ weeds/商店解锁随机由 info.seed 确定性驱动，
#   与 twin 保真门同源；种子值本身无线上含义，不占用 holdout 种子域）。
# CLI：
#   --emit            打印当前工作树 src/ 的全季哈希（捕获基线用）
#   --check（默认）   当前工作树 vs 冻结 JSON 逐种子比对，不一致 exit 1
#   --probe-on        旗开+激进覆盖跑 1 种子，断言哈希必异（通道活性自检）
# 纪律：stdlib-only、确定性；不修改 twin/planner 任何文件（只读消费）。
# ===========================================================================

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(SCRIPT_DIR)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

from kaggle_simulations.agent.planner import twin  # noqa: E402

GOLDEN_DIR = os.path.join(SOFTWARE, "exports", "probes", "planner_flagoff")
GOLDEN_PATH = os.path.join(GOLDEN_DIR, "golden_v138.json")
SEEDS = (11, 22, 33, 47, 58, 69)      # >=6 全季种子（任务包下限）
EPISODE_STEPS = 720                    # 30 天 × 24 步（官方整季）
BOARD = 10
STARTING_MONEY = 3000


def synthetic_season_head(seed, episode_steps=EPISODE_STEPS):
    """合成整季回放头（与 tests/test_twin_fidelity._synthetic_replay 同构：
    NW 象限解锁、其余 LOCKED、3000 起始资金、零棚零种、无预解锁商店；
    market 初值=引擎 MARKET_PARAMS 的 I0/base 全品表——与框架 _initialize
    产物一致，防止空价格表让曲线引擎除零退化）。"""
    module = twin.load_engine().module
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
        head.append({"action": None, "status": "ACTIVE", "reward": 0,
                     "info": {}, "observation": obs})
    cfg = {"episodeSteps": episode_steps, "actTimeout": 1, "boardSize": BOARD,
           "startingMoney": STARTING_MONEY, "maxMarketOrdersPerTurn": 10,
           "turnsPerDay": 24, "shedCapacity": 100, "weedSpawnChance": 0.005,
           "townShopUnlockInterval": 3, "townShopSellInterval": 4,
           "townCenterSellInterval": 24, "seed": None, "farmHandCostMult": 1,
           "marketParams": {}}
    return {"steps": [head], "configuration": cfg, "info": {"seed": seed}}


def season_action_hash(agent_fn, seed):
    """整季双席 v13.8 自博弈的动作流哈希与终局资金（确定性）。"""
    bundle = twin.load_engine()
    state = twin.new_state_from_replay_head(synthetic_season_head(seed),
                                            bundle)
    stream = []

    def source(st):
        obs0 = st.seats[0].observation
        obs1 = st.seats[1].observation
        pair = [agent_fn(obs0), agent_fn(obs1)]
        stream.append(pair)
        return pair

    twin.run_to_end(state, source)
    payload = json.dumps(stream, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return {"seed": seed, "steps": len(stream), "sha256": digest,
            "final_money": [round(m, 3) for m in twin.final_money(state)]}


def build_v138_namespace():
    """按 main.py 同语义把现工作树 src/ 九模块 exec 进扁平命名空间。"""
    agent_dir = os.path.join(SOFTWARE, "kaggle_simulations", "agent")
    order = ("constants", "telemetry", "observer", "strategy", "mission",
             "solver", "executor", "market", "entry")
    ns = {}
    exec("; ".join(("import copy", "import math", "import json",
                    "import hashlib")), ns)
    for mod in order:
        path = os.path.join(agent_dir, "src", mod + ".py")
        with open(path, "r", encoding="utf-8") as handle:
            source = handle.read()
        exec(compile(source, path, "exec"), ns)
    return ns


def hashes_for_seeds(seeds=SEEDS):
    ns = build_v138_namespace()
    agent_fn = ns["agent"]
    return [season_action_hash(agent_fn, seed) for seed in seeds]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="DTSP 旗关等价黄金动作哈希（--emit 捕获 / 默认校验）")
    parser.add_argument("--emit", action="store_true",
                        help="打印当前工作树哈希（基线捕获模式）")
    parser.add_argument("--probe-on", action="store_true",
                        help="旗开+覆盖跑 1 种子，断言哈希必异（通道活性）")
    parser.add_argument("--golden", default=GOLDEN_PATH)
    args = parser.parse_args(argv)

    if args.emit:
        import io
        from contextlib import redirect_stdout
        # 引擎 wheel 首载时 kaggle_environments 注册表会向 stdout 打印
        # 无害告警（cabt/open_spiel 缺可选依赖）——emit 模式必须输出纯
        # JSON，故捕获之（与 --check 的逐行报告路径无关）。
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            rows = hashes_for_seeds()
        print(json.dumps({"seeds": rows}, ensure_ascii=False, indent=1))
        return 0

    if args.probe_on:
        ns = build_v138_namespace()
        ns["PLANNER_ENABLED"] = True
        ns["PLANNER_OVERRIDES"] = {
            "mode_volume_day_start": -99,   # VOLUME 无条件可入场
            "mode_volume_day_end": 99,
            "herd_day_shift": 2,            # 畜群节奏后移 2 天
            "sell_price_discount": 0.75,    # 悲观卖出
        }
        agent_fn = ns["agent"]
        row = season_action_hash(agent_fn, SEEDS[0])
        baseline = {r["seed"]: r["sha256"] for r in hashes_for_seeds(SEEDS[:1])}
        changed = row["sha256"] != baseline[SEEDS[0]]
        print(json.dumps({"seed": row["seed"], "flag_on_sha256": row["sha256"],
                          "flag_off_sha256": baseline[SEEDS[0]],
                          "channel_bites": changed}, ensure_ascii=False))
        return 0 if changed else 1

    with open(args.golden, "r", encoding="utf-8") as handle:
        golden = json.load(handle)
    expected = {row["seed"]: row["sha256"] for row in golden["seeds"]}
    rows = hashes_for_seeds(tuple(sorted(expected)))
    failures = [r for r in rows if expected.get(r["seed"]) != r["sha256"]]
    for r in rows:
        mark = "OK" if expected.get(r["seed"]) == r["sha256"] else "MISMATCH"
        print(f"[flagoff] seed={r['seed']} steps={r['steps']} "
              f"money={r['final_money']} {mark}")
    if failures:
        sys.stderr.write(
            f"[exit 1] 旗关等价破坏：{len(failures)}/{len(rows)} 种子哈希"
            f"与 v13.8 黄金基线不一致（PLANNER_ENABLED 必须恒 False 等价）\n")
        return 1
    print(f"[flagoff] {len(rows)}/{len(rows)} 种子与 v13.8 黄金基线逐字节一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
