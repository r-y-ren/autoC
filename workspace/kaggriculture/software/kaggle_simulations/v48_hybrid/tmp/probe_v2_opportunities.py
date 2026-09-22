# -*- coding: utf-8 -*-
# tmp/probe_v2_opportunities.py —— v2 前置测量：纯 v48 孪生轨迹上的补发机会
# 只读探针（不改任何现存文件）：对 seeds 11/22/33 双席纯 v48 自打，逐步记录
# d13-25 窗口内 v2 候选补发（空窗 + 清判据 + 库存>0）与假想量/收入。
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HYB = os.path.dirname(HERE)
GATES = os.path.join(HYB, "gates")
for p in (GATES,):
    if p not in sys.path:
        sys.path.insert(0, p)

import gate_common as gc  # noqa: E402
sys.path.insert(0, os.path.join(HYB, "patches"))
import midgame_sell_layer as msl  # noqa: E402

# 联合 6 变体的 tape 卖单日历（由 _V48_ROUTES 解码推导，v2 模块将内嵌同表）
import re
import base64
import zlib

src = open(os.path.join(gc.KSIM, "v48_derivative", "main.py"),
           "r", encoding="utf-8").read()
idx = src.index("_V48_ROUTES = json.loads")
end = src.index(')).decode("utf-8"))', idx)
blob = "".join(re.findall(r"'([^']*)'", src[idx:end]))
routes = json.loads(zlib.decompress(base64.b85decode(blob)).decode("utf-8"))

tape_days = {}
for name, steps in routes.items():
    for i, act in enumerate(steps or []):
        for o in (act or {}).get("market", []) or []:
            if isinstance(o, (list, tuple)) and o and o[0] == "SELL":
                tape_days.setdefault(o[1], set()).add(i // 24)
TAPE_SELL_DAYS = {k: sorted(v) for k, v in tape_days.items()}
print("TAPE_SELL_DAYS(union):", json.dumps(TAPE_SELL_DAYS))

HORIZON = 3
CAP = 6


def free_window(item, day):
    days = TAPE_SELL_DAYS.get(item, [])
    return not any(day <= d <= day + HORIZON for d in days)


rows = []
for seed in (11, 22, 33):
    def on_step(seat, obs, action):
        so = gc.structify_obs(obs)
        step = int(so.get("step") or 0)
        day = step // 24
        hour = step % 24
        if not (13 <= day < 26):
            return
        # 注：不去除反克隆/终局让位——镜像自打中双方农场相同，
        # clone_distance≈0 会 mask 全部 step≥160 机会；这里测原始机会集。
        shed = so.get("private", {}).get("shed", {}) if isinstance(
            so.get("private"), dict) else {}
        prices = so.get("market", {}).get("prices", {}) if isinstance(
            so.get("market"), dict) else {}
        shops = so.get("town", {}).get("unlocked_shops", []) if isinstance(
            so.get("town"), dict) else []
        sells_now = {o[1] for o in (action.get("market") or [])
                     if isinstance(o, (list, tuple)) and o
                     and o[0] == "SELL"} if isinstance(action, dict) else set()
        for item in msl.PLANNER_ITEMS:
            if item in sells_now:
                continue
            stock = shed.get(item, 0)
            if not isinstance(stock, (int, float)) or stock <= 0:
                continue
            if not free_window(item, day):
                continue
            obs2 = {"step": step, "prices": prices, "shed": shed,
                    "money": so.get("farms", [{}, {}])[0].get("money")
                    if isinstance(so.get("farms"), list) else None,
                    "unlocked_shops": shops}
            try:
                verdict = msl._verdict(item, {"prices": prices, "flow": {}},
                                       msl.DEFAULT_CONFIG)
            except Exception:
                verdict = "ERR"
            absorb = msl._town_daily_demand(shops).get(item, 1)
            qty = min(int(stock), max(1, absorb), CAP)
            rows.append({"seed": seed, "seat": seat, "step": step,
                         "day": day, "hour": hour, "item": item,
                         "stock": stock, "absorb": absorb, "qty": qty,
                         "price": prices.get(item), "verdict": verdict})

    gc.twin_selfplay([lambda: gc.load_agent(gc.BASE_MAIN),
                      lambda: gc.load_agent(gc.BASE_MAIN)], seed,
                     on_step=on_step)
    print(f"seed {seed} done, rows so far {len(rows)}", flush=True)

with open(os.path.join(HERE, "v2_opportunities.json"), "w") as h:
    json.dump(rows, h, indent=1)

from collections import defaultdict
agg = defaultdict(lambda: {"n": 0, "qty": 0, "money_est": 0.0})
for r in rows:
    if r["verdict"] != "clear" or r["hour"] not in (6, 12, 18):
        continue
    k = (r["seed"], r["seat"], r["day"], r["item"])
    agg[k]["n"] += 1
    agg[k]["qty"] = r["qty"]          # 同日同线只发一批（时点首个命中）
    agg[k]["money_est"] += r["qty"] * (r["price"] or 0)
tot_money = sum(v["money_est"] for v in agg.values())
print(f"== 补发汇总（清判据+整点）：候选批次 {len(agg)} 个，估计收入 "
      f"{tot_money:.0f}")
by_item = defaultdict(lambda: [0, 0.0])
for (seed, seat, day, item), v in agg.items():
    by_item[item][0] += 1
    by_item[item][1] += v["money_est"]
for item, (n, m) in sorted(by_item.items()):
    print(f"   {item:12s} batches={n:4d} est_money={m:9.0f}")
