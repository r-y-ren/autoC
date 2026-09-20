# -*- coding: utf-8 -*-
"""Track-C (BC) 特征/动作 schema v1 —— 全管线唯一契约.

版本：bc-schema/1.0（2026-09-20）。本文件是样本抽取器（extract_samples）、
训练器（train_bc）、推理策略（bc_policy）与评估 harness（bc_eval）共享的
编码层；改任何枚举/布局必须 bump 版本号并重抽样本。

配对口径（与 planner/twin.replay_transition_actions 同一解读）：
  (obs, action) = (steps[t-1][seat].observation, steps[t][seat].action)
  —— steps[t] 记录的 action 驱动 t-1 -> t 转移。

特征分三组：
  A. 全局特征 G（双席可见 + 我方 private；预测我方动作时合法）；
  B. 单位特征 U（farmer 与每只 hand 各一份，拼在 G 后进单位头）；
  C. 动作编码（单位动作枚举 + 市场订单槽位枚举）。
全部数值 clip 到 [-50, 50]、log1p 缩放计数，确保纯 Python 前向数值稳定。
"""
from __future__ import annotations

import math

SCHEMA_VERSION = "bc-schema/1.2"
G_SCALE = 12.0            # 全局特征尺度归一（v1.1）

# ---- 引擎枚举（与 vendored kaggriculture.py 常数对齐，factsheet §3-§5）----
CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
            "EGG", "MILK", "WOOL", "FERTILIZER")
ANIMALS = ("GOOSE", "COW", "SHEEP")
ITEMS = PRODUCTS + ANIMALS                      # PICKUP/PLACE 可操作的 12 token
DIRS = ("NORTH", "SOUTH", "EAST", "WEST")

UNIT_OPS = ("PASS", "NORTH", "SOUTH", "EAST", "WEST",
            "DROP", "PICKUP", "PLACE", "PLANT", "WATER", "HARVEST",
            "FERTILIZE", "DIG", "BUILD_COOP", "BUILD_PASTURE",
            "FEED", "COLLECT_FERTILIZER", "CARE")
UNIT_OP_IDX = {op: i for i, op in enumerate(UNIT_OPS)}
PLANT_ARG_IDX = {c: i for i, c in enumerate(CROPS)}       # PLANT 参数
ITEM_ARG_IDX = {c: i for i, c in enumerate(ITEMS)}        # PICKUP/PLACE 参数

# 单位动作数量桶：decode 代表值；桶 0 = "省略数量"（引擎默认 n=1）
QTY_BUCKETS = ((None, 1), (1, 1), (2, 2), (3, 4), (5, 7), (8, 10),
               (11, 15), (16, 25), (26, 40), (41, 60), (61, 100),
               (101, 150), (151, 250), (251, 400))
QTY_BUCKET_IDX = {b[0]: i for i, b in enumerate(QTY_BUCKETS)}


def qty_to_bucket(n: int | None) -> int:
    """显式数量 -> 桶号（None -> 0）。"""
    if n is None:
        return 0
    for i, (lo, _) in enumerate(QTY_BUCKETS):
        if i == 0:
            continue
        if n <= QTY_BUCKETS[i][1]:
            return i
    return len(QTY_BUCKETS) - 1


def bucket_to_qty(bucket: int) -> int | None:
    """桶号 -> decode 代表数量（None = 省略）。"""
    if bucket <= 0:
        return None
    return QTY_BUCKETS[min(bucket, len(QTY_BUCKETS) - 1)][1]


# ---- 市场订单编码 ------------------------------------------------------
# 槽位制：每回合 10 槽，每槽 = (订单类, 条目, 数量桶)。订单类 NONE=不下单。
# HIRE/BUY_LAND 无条目（条目 0 占位）。decode 按槽序原样提交。
MARKET_ORDER_OPS = ("NONE", "HIRE", "BUY_LAND", "BUY_SEED", "BUY_PRODUCT",
                    "BUY_ANIMAL", "SELL")
MARKET_OP_IDX = {op: i for i, op in enumerate(MARKET_ORDER_OPS)}
# 条目空间：BUY_SEED 用 CROPS；BUY_PRODUCT 仅 WHEAT/FERTILIZER 引擎合法但
# 训练数据里有全商品（Selling 侧对手镜像），统一用 ITEMS 12 维条目枚举。
MARKET_ITEM_IDX = {c: i for i, c in enumerate(ITEMS)}
N_MARKET_SLOTS = 10


def encode_unit_action(action) -> tuple[int, int, int]:
    """单条单位动作 -> (op_idx, arg_idx, qty_bucket)。arg 无关 op 恒 0。"""
    if not action:
        return UNIT_OP_IDX["PASS"], 0, 0
    op = action[0]
    op_i = UNIT_OP_IDX.get(op, UNIT_OP_IDX["PASS"])
    arg_i = 0
    if op == "PLANT" and len(action) >= 2:
        arg_i = PLANT_ARG_IDX.get(action[1], 0)
    elif op in ("PICKUP", "PLACE") and len(action) >= 2:
        arg_i = ITEM_ARG_IDX.get(action[1], 0)
    qty = int(action[2]) if len(action) >= 3 else None
    return op_i, arg_i, qty_to_bucket(qty)


def decode_unit_action(op_i: int, arg_i: int, qty_b: int):
    """(op, arg, qty桶) -> 引擎动作 list。桶 0 = 省略数量。"""
    op = UNIT_OPS[op_i] if 0 <= op_i < len(UNIT_OPS) else "PASS"
    if op in ("PLANT",):
        out = [op, CROPS[arg_i % len(CROPS)]]
    elif op in ("PICKUP", "PLACE"):
        out = [op, ITEMS[arg_i % len(ITEMS)]]
    else:
        return [op]
    qty = bucket_to_qty(qty_b)
    if qty is not None:
        out.append(qty)
    return out


def encode_market_orders(orders) -> list[tuple[int, int, int]]:
    """订单列表 -> 长度 N_MARKET_SLOTS 的槽位三元组（多余丢弃=引擎同语义）。"""
    slots = [(0, 0, 0)] * N_MARKET_SLOTS
    for i, o in enumerate(orders[:N_MARKET_SLOTS]):
        if not isinstance(o, (list, tuple)) or not o:
            continue
        op = o[0]
        if op == "INVALID":
            continue
        op_i = MARKET_OP_IDX.get(op, 0)
        item_i = MARKET_ITEM_IDX.get(o[1], 0) if len(o) >= 2 else 0
        qty_b = qty_to_bucket(int(o[2]) if len(o) >= 3 else None)
        slots[i] = (op_i, item_i, qty_b)
    return slots


def decode_market_slots(slots) -> list[list]:
    """槽位三元组 -> 订单 list（NONE 槽跳过）。"""
    out = []
    for op_i, item_i, qty_b in slots:
        op = MARKET_ORDER_OPS[op_i] if op_i else "NONE"
        if op == "NONE":
            continue
        if op in ("HIRE", "BUY_LAND"):
            out.append([op])
            continue
        qty = bucket_to_qty(qty_b)
        qty = 1 if qty is None else qty
        out.append([op, ITEMS[item_i % len(ITEMS)], qty])
    return out


# ---- 特征提取 ----------------------------------------------------------
def _clip(x: float) -> float:
    return max(-50.0, min(50.0, x))


def _l(v: float) -> float:
    """log1p 缩放（计数/钱），再 clip。"""
    return _clip(math.log1p(max(0.0, float(v))))


def _tile_kind_code(tile) -> int:
    """tile -> kind 码 {0 none/locked, 1 empty-soil, 2 crop, 3 weed,
    4 coop, 5 pasture, 6 structure-with-animal}。"""
    if not isinstance(tile, dict):
        return 0
    crop = tile.get("crop")
    if crop:
        return 2
    kind = tile.get("kind")
    if kind == "WEED":
        return 3
    if kind == "COOP":
        return 4
    if kind == "PASTURE":
        return 5
    if "animal" in tile:
        return 6
    return 1


def _scan_farm(farm: dict) -> dict:
    """公开 farm dict -> 计数摘要（一次遍历；tile 字段名经回放实测：
    PLANT={crop,watered_today,yield_units,consecutive_unwatered,
    fertilized_until_day,...}；COOP/PASTURE={animal,fed_today,
    cared_today,yield_units,...}）。"""
    counts = {"crop": {c: 0 for c in CROPS}, "animal": {a: 0 for a in ANIMALS},
              "weed": 0, "soil": 0, "coop": 0, "pasture": 0,
              "watered": 0, "fertilized": 0, "crop_stage": [0, 0, 0],
              "harvestable": 0, "thirsty": 0}
    for row in farm.get("tiles") or []:
        for tile in row:
            if not isinstance(tile, dict):
                if tile is None:
                    counts["soil"] += 1
                continue
            kind = tile.get("kind")
            crop = tile.get("crop")
            if kind == "PLANT" and crop in counts["crop"]:
                counts["crop"][crop] += 1
                yu = tile.get("yield_units") or 0
                if yu >= 2:
                    counts["crop_stage"][2] += 1      # 可收
                elif yu >= 1:
                    counts["crop_stage"][1] += 1
                else:
                    counts["crop_stage"][0] += 1      # 幼苗
                if tile.get("watered_today"):
                    counts["watered"] += 1
                if (tile.get("consecutive_unwatered") or 0) >= 1:
                    counts["thirsty"] += 1
                if (tile.get("fertilized_until_day") or -1) >= 0:
                    counts["fertilized"] += 1
            elif kind == "WEED":
                counts["weed"] += 1
            elif kind == "COOP":
                counts["coop"] += 1
            elif kind == "PASTURE":
                counts["pasture"] += 1
            animal = tile.get("animal")
            if animal in counts["animal"]:
                counts["animal"][animal] += 1
            if (tile.get("yield_units") or 0) > 0:
                counts["harvestable"] += 1
    return counts


def extract_global_features(obs_seat: dict, seat: int) -> list[float]:
    """obs（本席视角 dict）-> 全局特征向量 G。

    布局（167 维；实测 tile 字段名见 _scan_farm 注释）：
      [0:3]    step/720, day/30, hour/24
      [3]      我方 money log；[4] 对手 money log
      [5:10]   我方 crop 计数 log（CROPS 序）；[10:15] 对手
      [15:18]  我方 crop 产量段分布 log（yu=0 / yu=1 / yu>=2）；[18:21] 对手
      [21:25]  我方 weed/soil/fertilized/thirsty log；[25:29] 对手
      [29:33]  我方 coop/pasture/watered/harvestable log；[33:37] 对手
      [37:40]  我方 animal 计数 log（ANIMALS 序）；[40:43] 对手
      [43:46]  我方 unlocked_quadrants/hires_today/hands 数 log
      [46:49]  对手同上
      [49:58]  market prices /100（PRODUCTS 序）
      [58:67]  market inventory log
      [67]     unlocked_shops 计数
      [68:77]  我方 shed log（PRODUCTS 序）；[77:80] 我方 shed 动物 log
      [80:85]  我方 seeds（CROPS 序，clip 50）
      [85:94]  我方随身库存合计 log（PRODUCTS 序）；[94:97] 随身动物 log
      [97:99]  我方 farmer 坐标 /10；[99:101] 对手 farmer 坐标
      [101:126] 我方 5×5 粗网格单位热图；[126:151] 对手
      [151:163] 差分特征：money/crop/animal/hands 的我−对手差（12 维）
    """
    farms = obs_seat.get("farms") or []
    me = farms[seat] if seat < len(farms) else {}
    opp = farms[1 - seat] if len(farms) == 2 else {}
    market = obs_seat.get("market") or {}
    town = obs_seat.get("town") or {}
    private = obs_seat.get("private") or {}
    day = obs_seat.get("day") or 0
    hour = obs_seat.get("hour") or 0
    # 框架语义：obs.step 只写在 seat0（twin.Observation 同构）；seat1 用
    # day*24+hour 推导，保证双席特征一致。
    steps = obs_seat.get("step")
    if steps is None:
        steps = day * 24 + hour

    out: list[float] = []
    out += [steps / 720.0, day / 30.0, hour / 24.0]
    out += [_l(me.get("money", 0)), _l(opp.get("money", 0))]
    me_c = _scan_farm(me)
    op_c = _scan_farm(opp)
    out += [_l(me_c["crop"][c]) for c in CROPS]
    out += [_l(op_c["crop"][c]) for c in CROPS]
    out += [_l(x) for x in me_c["crop_stage"]]
    out += [_l(x) for x in op_c["crop_stage"]]
    out += [_l(me_c["weed"]), _l(me_c["soil"]), _l(me_c["fertilized"]),
            _l(me_c["thirsty"])]
    out += [_l(op_c["weed"]), _l(op_c["soil"]), _l(op_c["fertilized"]),
            _l(op_c["thirsty"])]
    out += [_l(me_c["coop"]), _l(me_c["pasture"]), _l(me_c["watered"]),
            _l(me_c["harvestable"])]
    out += [_l(op_c["coop"]), _l(op_c["pasture"]), _l(op_c["watered"]),
            _l(op_c["harvestable"])]
    out += [_l(me_c["animal"][a]) for a in ANIMALS]
    out += [_l(op_c["animal"][a]) for a in ANIMALS]
    out += [_l(len(me.get("unlocked_quadrants") or ())),
            _l(me.get("hires_today", 0)), _l(len(me.get("hands") or ()))]
    out += [_l(len(opp.get("unlocked_quadrants") or ())),
            _l(opp.get("hires_today", 0)), _l(len(opp.get("hands") or ()))]
    prices = market.get("prices") or {}
    inv = market.get("inventory") or {}
    out += [_clip(float(prices.get(p, 0)) / 100.0) for p in PRODUCTS]
    out += [_l(inv.get(p, 0)) for p in PRODUCTS]
    out += [_l(len(town.get("unlocked_shops") or ()))]
    shed = private.get("shed") or {}
    out += [_l(shed.get(p, 0)) for p in PRODUCTS]
    out += [_l(shed.get(a, 0)) for a in ANIMALS]
    seeds = private.get("seeds") or {}
    out += [_clip(float(seeds.get(c, 0))) for c in CROPS]
    carried = [0.0] * len(PRODUCTS)
    carried_a = [0.0] * len(ANIMALS)
    for invs in private.get("inventories") or []:
        if not isinstance(invs, dict):
            continue
        for j, p in enumerate(PRODUCTS):
            carried[j] += float(invs.get(p, 0) or 0)
        for j, a in enumerate(ANIMALS):
            carried_a[j] += float(invs.get(a, 0) or 0)
    out += [_l(x) for x in carried]
    out += [_l(x) for x in carried_a]

    fm = me.get("farmer") or [0, 0]
    fo = opp.get("farmer") or [0, 0]
    out += [float(fm[0]) / 10.0, float(fm[1]) / 10.0]
    out += [float(fo[0]) / 10.0, float(fo[1]) / 10.0]

    def grid(farm):
        g = [0.0] * 25
        units = [farm.get("farmer")] + list(farm.get("hands") or ())
        for u in units:
            if not u:
                continue
            x, y = int(u[0]), int(u[1])
            gx, gy = min(4, x // 2), min(4, y // 2)
            g[gy * 5 + gx] += 1.0
        return [min(4.0, v) / 4.0 for v in g]

    out += grid(me)
    out += grid(opp)
    # 差分（对称化信息，帮 MLP 少学一层减法）
    out += [
        _l(me.get("money", 0)) - _l(opp.get("money", 0)),
        *(_l(me_c["crop"][c]) - _l(op_c["crop"][c]) for c in CROPS),
        *(_l(me_c["animal"][a]) - _l(op_c["animal"][a]) for a in ANIMALS),
        _l(len(me.get("hands") or ())) - _l(len(opp.get("hands") or ())),
        _l(len(me.get("unlocked_quadrants") or ()))
        - _l(len(opp.get("unlocked_quadrants") or ())),
        _l(me_c["harvestable"]) - _l(op_c["harvestable"]),
        _l(me_c["harvestable"]),
        _l(op_c["harvestable"]),
        _l(me_c["thirsty"]),
        _l(op_c["thirsty"]),
    ]
    # v1.1 尺度归一：G 原始幅度可达 ~12（log1p money），U 特征 <=1.7——
    # 首跑（1.0）单网 op acc 仅 36% 且评估期 PASS 52%/WATER 0，根因是
    # 第一层 tanh 被 G 饱和、局部信号被淹没。统一除 G_SCALE 压到 O(1)。
    return [v / G_SCALE for v in out]


N_GLOBAL_FEATURES = 167          # 实测布局长度（见上）；与 assert 对齐


def extract_unit_features(obs_seat: dict, seat: int, unit_pos) -> list[float]:
    """单位局部特征 U（19 维，v1.2）：站位/邻格/到棚距离/随身/本格维护状态.

    棚几何（引擎 _shed_access_tiles 实测）：访问格 = 中心 2×2
    (4,4),(5,4),(4,5),(5,5)；站在其上才能 DROP/PICKUP/PLACE 入棚。

      [0:2]  相对坐标 /10（0-1）
      [2:4]  到最近访问格曼哈顿距离 /10；是否站访问格
      [4:6]  站位 tile kind 码 /6；站位含 crop 的索引 /5
      [6:8]  随身 wheat log、随身 fertilizer log
      [8:12] 四邻 tile kind 码 /6（N E S W 序，越界=0）
      [12:14] 邻格我方单位数 clip /4；我方单位总数 log
      [14:19] v1.2 新增——本格维护状态（票 03 第 2 轮：泊车缺陷归因于
              "已浇/已喂/可收"信号缺失——专家在已维护完的格子上会移走，
              v1.1 特征区分不了"待浇水作物"与"已浇过作物"，闭环即泊车）：
              watered_today(0/1) / consecutive_unwatered clip3 /3 /
              yield_units clip6 /6 / fed_today(0/1) / cared_today(0/1)
              （非作物/非动物格相应位 = 0）
    """
    farms = obs_seat.get("farms") or []
    me = farms[seat] if seat < len(farms) else {}
    tiles = me.get("tiles") or []
    x, y = int(unit_pos[0]), int(unit_pos[1])
    out: list[float] = []
    out += [x / 10.0, y / 10.0]
    shed_d = min(abs(x - a) + abs(y - b) for a in (4, 5) for b in (4, 5))
    on_shed = 1.0 if shed_d == 0 else 0.0
    out += [min(10.0, float(shed_d)) / 10.0, on_shed]
    tile = (tiles[y][x] if 0 <= y < len(tiles) and 0 <= x < len(tiles[y])
            else None)
    kind_code = _tile_kind_code(tile) / 6.0
    crop_idx = 0.0
    if isinstance(tile, dict) and tile.get("crop") in CROPS:
        crop_idx = (CROPS.index(tile["crop"]) + 1) / 5.0
    out += [kind_code, crop_idx]
    private = obs_seat.get("private") or {}
    unit_inv = {}
    invs = private.get("inventories") or []
    # unit_pos 与 inventories 的对应关系不可靠（回放不标 unit id），
    # 保守取"全体随身合计"做近似——版本 1 已知局限，登记在 schema 注释。
    for d in invs:
        if isinstance(d, dict):
            for k, v in d.items():
                unit_inv[k] = unit_inv.get(k, 0) + float(v or 0)
    out += [_l(unit_inv.get("WHEAT", 0)), _l(unit_inv.get("FERTILIZER", 0))]
    neigh = []
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        nx, ny = x + dx, y + dy
        t = (tiles[ny][nx] if 0 <= ny < len(tiles) and 0 <= nx < len(tiles[ny])
             else None)
        neigh.append(_tile_kind_code(t) / 6.0)
    out += neigh
    units = [me.get("farmer")] + list(me.get("hands") or ())
    near = sum(1 for u in units
               if u and abs(int(u[0]) - x) + abs(int(u[1]) - y) == 1)
    out += [min(4.0, float(near)) / 4.0, _l(len(units))]
    # v1.2：本格维护状态（tile dict 字段经回放实测，见 _scan_farm 注释）
    if isinstance(tile, dict):
        out += [
            1.0 if tile.get("watered_today") else 0.0,
            min(3.0, float(tile.get("consecutive_unwatered") or 0)) / 3.0,
            min(6.0, float(tile.get("yield_units") or 0)) / 6.0,
            1.0 if tile.get("fed_today") else 0.0,
            1.0 if tile.get("cared_today") else 0.0,
        ]
    else:
        out += [0.0, 0.0, 0.0, 0.0, 0.0]
    return out


N_UNIT_FEATURES = 19
