"""M1+M3 共用：孪生装载、回放语料、经济常数（只读仓库，只写 /tmp/mathmodel）。"""
import os, sys, json, math

CAMP = "/mnt/data/Code/autoC/workspace/kaggriculture"
SOFTWARE = os.path.join(CAMP, "software")
FN_WORK_ROB = os.path.join(CAMP, "fn_work", "src", "run_official_bench")
for _p in (SOFTWARE, FN_WORK_ROB):
    if _p not in sys.path:
        sys.path.insert(0, _p)

REPLAY_DIR = os.path.join(
    CAMP, "software/kaggle_simulations/v48_hybrid/fn_docs/results/replays-lead-collapse")
OUT = "/tmp/mathmodel"

# CORPUS.md 表（ep -> 我席/原margin/对手终局/峰值日/峰值额）
CORPUS = [
    # ep, me_seat, orig_margin, opp_final, peak_day, peak_amt
    (111336733, 1, -1739.0, 101875.0, 21, 13781.0),
    (111297358, 0, -3286.0, 72240.0, 26, 8749.0),
    (111289536, 0, -1276.0, 84488.0, 17, 8696.0),
    (111286146, 1, -4883.0, 52075.0, 17, 7991.0),
    (111287283, 0, -304.0, 55336.0, 10, 5535.0),
    (111306349, 0, -21296.0, 91150.0, 10, 4904.0),
    (111405339, 0, -987.0, 93370.0, 22, 4199.0),
    (111421048, 0, -11291.0, 104888.0, 6, 1790.0),
    (111370910, 1, -3155.0, 94598.0, 6, 1590.0),
    (111653327, 1, -36154.0, 149814.0, 6, 1505.0),
    (111393589, 1, -11121.0, 63569.0, 9, 1430.0),
    (111318595, 0, -5238.0, 86070.0, 6, 1385.0),
    (111323075, 0, -20649.0, 108845.0, 9, 1363.0),
    (111320833, 0, -6368.0, 83905.0, 6, 1159.0),
]

STEPS_PER_DAY = 24
PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]


def load_twin():
    from kaggle_simulations.agent.planner import twin
    return twin


def load_replay(ep):
    return json.load(open(os.path.join(REPLAY_DIR, f"episode-{ep}-replay.json")))


def replay_actions(replay):
    out = []
    for t in range(1, len(replay["steps"])):
        out.append([(replay["steps"][t][0] or {}).get("action"),
                    (replay["steps"][t][1] or {}).get("action")])
    return out


def market_orders(action):
    if not isinstance(action, dict):
        return []
    m = action.get("market")
    return m if isinstance(m, list) else []
