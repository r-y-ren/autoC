# -*- coding: utf-8
# 位置模拟器：开环磁带的确定性行走轨迹（不跑引擎，只算格子坐标）。
# 供 R9-G2 磁带手术设计用：定位 BUILD/PLACE/FEED 覆盖面。
from __future__ import annotations
import json

MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "WEST": (-1, 0), "EAST": (1, 0)}
BS = 10
SHED_TILES = [(4, 4), (5, 4), (4, 5), (5, 5)]


def spawn_hand(pos_list):
    occ = {t: 0 for t in SHED_TILES}
    for p in pos_list:
        p = tuple(p)
        if p in occ:
            occ[p] += 1
    best = sorted(occ.items(), key=lambda kv: (kv[1], SHED_TILES.index(kv[0])))
    return list(best[0][0])


def simulate(route, hires_per_day):
    """返回 steps: [{pos0..posN, ops:[(who,op,tile)]}]；who=0 farmer, 1+ hand idx。
    含 EOD 语义：每日末（step%24==23 处理后）farmer 归位 (4,4)、hands 清空。"""
    farmer = [4, 4]
    hands = []
    steps = []
    for i, step in enumerate(route):
        day = i // 24
        if i % 24 == 0:
            farmer = [4, 4]
            hands = []
        # HIRE 数按当日给定（假设全部成功；基底已验证）
        want = hires_per_day.get(day, 0)
        while len(hands) < want:
            hands.append(spawn_hand([farmer] + hands))
        ops = []
        f = step["farmer"]
        if isinstance(f, list) and f:
            if f[0] in MOVES:
                dx, dy = MOVES[f[0]]
                nx, ny = farmer[0] + dx, farmer[1] + dy
                if 0 <= nx < BS and 0 <= ny < BS:
                    farmer = [nx, ny]
            else:
                ops.append((0, tuple(f), tuple(farmer)))
        for hi, ha in enumerate(step["hands"]):
            if hi >= len(hands):
                break
            if not isinstance(ha, list) or not ha:
                continue
            if ha[0] in MOVES:
                dx, dy = MOVES[ha[0]]
                nx, ny = hands[hi][0] + dx, hands[hi][1] + dy
                if 0 <= nx < BS and 0 <= ny < BS:
                    hands[hi] = [nx, ny]
            else:
                ops.append((hi + 1, tuple(ha), tuple(hands[hi])))
        steps.append({"positions": [tuple(farmer)] + [tuple(h) for h in hands],
                      "ops": ops})
    return steps


if __name__ == "__main__":
    routes = json.load(open("/mnt/data/Code/autoC/workspace/kaggriculture/"
                            "software/kaggle_simulations/v48_hybrid/tmp/"
                            "routes_decoded.json"))
    import collections
    r = routes["default"]
    hires = collections.Counter()
    for i, s in enumerate(r):
        for o in s["market"]:
            if o[0] == "HIRE":
                hires[i // 24] += 1
    steps = simulate(r, hires)
    # d12-d13 每日 FEED 覆盖面
    for day in (11, 12):
        fed = set()
        for i in range(day * 24, day * 24 + 24):
            for who, act, tile in steps[i]["ops"]:
                if act[0] in ("FEED", "CARE"):
                    fed.add(tile)
        print(f"d{day} FEED/CARE tiles: {sorted(fed)} n={len(fed)}")
    # BUILD/PLACE 轨迹
    for day in range(11):
        for i in range(day * 24, day * 24 + 24):
            for who, act, tile in steps[i]["ops"]:
                if act[0] == "BUILD_PASTURE" or (
                        act[0] == "PLACE" and len(act) > 1
                        and act[1] in ("SHEEP", "COW", "GOOSE")):
                    print(f"step {i:3d} d{day} who={who} pos={tile} {act}")
