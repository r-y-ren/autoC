"""sprint-A 结构复刻探针：本地自对局逐日快照，核对经济域指标。

用法：python scripts/sprintA_structure_probe.py [seeds ...]（默认 7 101）

对每个种子跑一场双席自对局（与 quickwin 同引擎通道），在 wrapper 内按
(玩家, 日) 快照：在田作物构成、畜群、现金、象限数；并按动作计数 care/
feed/harvest/water 操作与 BUY_PRODUCT WHEAT 采购量。输出双席均值与
658-663 档赢家结构靶标对照（sprint_forensics_0919.md §2）。
纯诊断：不写 candidate、不跑 gate、不触 metrics。
"""
import importlib.util
import json
import sys
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE))
sys.path.insert(0, str(SOFTWARE / "scripts"))

from kgenv.engine import run_episode  # noqa: E402
from m4_switchover_regression import load_module, reset_module_state  # noqa: E402

CROPS = ("WHEAT", "STRAWBERRY", "MELON", "CARROT", "TOMATO")
_SNAP_ERRORS = {"n": 0}   # 快照失败计数（防静默丢样本：>0 时在结尾告警）


def _get(o, k, d=None):
    return o.get(k, d) if isinstance(o, dict) else d


def run_struct(seed):
    module = load_module()
    reset_module_state(module)
    snap = {}   # (player, day) -> dict
    ops = {0: {}, 1: {}}   # player -> counters

    def wrap(player):
        def agent(obs):
            act = module.agent(obs)
            try:
                day = int(_get(obs, "day", 0) or 0)
                farm = (_get(obs, "farms", []) or [{}] * (player + 1))[player]
                crops = {}
                herd = 0
                quads = _get(farm, "unlocked_quadrants", ["NW"]) or []
                for row in _get(farm, "tiles", []) or []:
                    for t in row:
                        if isinstance(t, dict) and "animal" in t:
                            herd += 1
                        elif isinstance(t, dict) and t.get("kind") == "PLANT":
                            c = t.get("crop")
                            crops[c] = crops.get(c, 0) + 1
                key = (player, day)
                prev = snap.get(key) or {"money": [], "crops": []}
                prev["crops"].append(dict(crops))
                prev["money"].append(float(_get(farm, "money", 0) or 0))
                prev.setdefault("herd", []).append(herd)
                prev["quads"] = len(quads)
                snap[key] = prev
                o = ops[player]
                a = act if isinstance(act, list) else []
                head = a[0] if a and isinstance(a[0], str) else None
                if head in ("CARE", "WATER", "HARVEST", "FEED", "FERTILIZE"):
                    o[head] = o.get(head, 0) + 1
                # 市场单据在动作尾部的订单区（形态 [[op,item,qty],...]）
                for item in a:
                    if isinstance(item, list) and len(item) >= 3 \
                            and item[0] == "BUY_PRODUCT" and item[1] == "WHEAT":
                        try:
                            o["feed_buy"] = o.get("feed_buy", 0) + int(item[2])
                        except (TypeError, ValueError):
                            pass
            except Exception:
                _SNAP_ERRORS["n"] += 1
            return act
        return agent

    result = run_episode(wrap(0), wrap(1), seed, episode_steps=720)
    return snap, ops, result


def summarize(snap, ops):
    seats = []
    for p in (0, 1):
        days = {d: v for (pl, d), v in snap.items() if pl == p}
        if not days:
            continue
        peak = {c: 0 for c in CROPS}
        for d, v in days.items():
            for cs in v["crops"]:
                for c, n in cs.items():
                    if c in peak:
                        peak[c] = max(peak[c], n)
        money_by_day = {}
        for d, v in days.items():
            money_by_day[d] = max(v["money"]) if v["money"] else 0
        seats.append({
            "peak": peak,
            "herd": max((max(v.get("herd", [0])) for v in days.values()),
                        default=0),
            "d12": money_by_day.get(12, 0),
            "d24": money_by_day.get(24, 0),
            "quads": max((v.get("quads", 0) for v in days.values()), default=0),
            "ops": ops.get(p, {}),
        })
    return seats


def main():
    seeds = [int(s) for s in sys.argv[1:]] or [7, 101]
    all_seats = []
    for seed in seeds:
        snap, ops, result = run_struct(seed)
        seats = summarize(snap, ops)
        all_seats.extend(seats)
        for i, s in enumerate(seats):
            print(f"seed {seed} seat {i}: peak={s['peak']} herd={s['herd']} "
                  f"d12={s['d12']:.0f} d24={s['d24']:.0f} "
                  f"care={s['ops'].get('CARE', 0)} feed_buy={s['ops'].get('feed_buy', 0)} "
                  f"harvest={s['ops'].get('HARVEST', 0)}")
    n = len(all_seats) or 1

    def m(f):
        vs = [f(s) for s in all_seats]
        return sum(vs) / len(vs) if vs else 0
    print("--- 双席均值（靶标：麦17-20/莓18-24/瓜9-12/萝卜>0/care 200+/feed 200+）---")
    print({c: round(m(lambda s, c=c: s["peak"].get(c, 0)), 1) for c in CROPS})
    print({"herd": round(m(lambda s: s["herd"]), 1),
           "d12": round(m(lambda s: s["d12"])),
           "d24": round(m(lambda s: s["d24"])),
           "care": round(m(lambda s: s["ops"].get("CARE", 0))),
           "feed_buy": round(m(lambda s: s["ops"].get("feed_buy", 0))),
           "harvest": round(m(lambda s: s["ops"].get("HARVEST", 0)))})
    if _SNAP_ERRORS["n"]:
        print(f"WARN: {_SNAP_ERRORS['n']} snapshot turns failed (计数不可靠度∝此值)")


if __name__ == "__main__":
    main()
