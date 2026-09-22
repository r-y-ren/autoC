# -*- coding: utf-8 -*-
# 【中文】income_selfcheck_v6b.py —— R9-G2b 收入峰自检 + 三指标逐日
# ===========================================================================
# 自打两局（seeds 101/102，与四门同种子）+ 构造 yarn≥2 分支局（种子扫描：
# 铺抽 d3/d6 双 YARN_STORE）。逐日计量：
#   * 收入曲线（SELL 侧现金流入，步级正增量求和）与 d14-17 峰 vs 12.7k 门；
#   * 羊在场数（farms tiles animal==SHEEP 计数，日末采样）；
#   * 照护率（fed_today && cared_today 的动物 tile 占比，日末采样）；
#   * 羊毛变现率（当日 SELL WOOL 单位 /（当日卖量+棚存 WOOL 日末））。
# 产物：tmp/probes_v6b/v6b_income_selfcheck.json
# ===========================================================================
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HYBRID = os.path.dirname(HERE)
SOFTWARE = os.path.dirname(os.path.dirname(HYBRID))
sys.path.insert(0, SOFTWARE)
sys.path.insert(0, "/tmp/v6kag")

V6B = os.path.join(HYBRID, "v6b", "main.py")
GATE = 12700
SELFPLAY_SEEDS = [101, 102]
OUT = os.path.join(HYBRID, "tmp", "probes_v6b",
                   "v6b_income_selfcheck.json")


def scan_yarn2_seeds(cand_range, want=2):
    """扫描种子：shops[0]=YARN 且 step 217 前累计 YARN≥2（构造 yarn≥2 局）。

    必须与 measure() 同路径（env.run 文件代理）：铺抽消耗杂草 RNG（随
    空格数推进），轨迹不同则铺抽不同——故不能用快进步进替代。
    """
    from kaggle_environments import make
    found = []
    for seed in cand_range:
        env = make("kag"+"griculture", debug=False,
                   configuration={"seed": seed})
        env.run([V6B, V6B])
        h = env.steps
        shops = h[217][0]["observation"].get("town", {}).get(
            "unlocked_shops", [])
        n_yarn = sum(1 for s in shops if s == "YARN_STORE")
        if shops and shops[0] == "YARN_STORE" and n_yarn >= 2:
            found.append(seed)
            print(f"[scan] seed {seed}: shops={shops[:4]}", flush=True)
            if len(found) >= want:
                break
        del env, h
    return found


def measure(seed):
    from kaggle_environments import make
    env = make("kag"+"griculture", debug=False,
               configuration={"seed": seed})
    env.run([V6B, V6B])
    h = env.steps
    out = {"seed": seed, "rewards": [s.reward for s in env.state],
           "statuses": [s.status for s in env.state]}
    shops = h[88][0]["observation"].get("town", {}).get(
        "unlocked_shops", [])
    out["shops_by_step88"] = shops[:2]
    seat = 0
    farms_series = [step[0]["observation"]["farms"][seat]
                    for step in h]
    money = [f["money"] for f in farms_series]
    income = []
    for d in range(30):
        lo, hi = d * 24, min(d * 24 + 24, len(money) - 1)
        inc = sum(max(0.0, money[i + 1] - money[i]) for i in range(lo, hi))
        income.append(round(inc, 1))
    out["income_curve"] = income
    peak = max(income[14:18]) if len(income) >= 18 else None
    out["peak_d14_17"] = peak
    out["peak_day"] = (14 + income[14:18].index(peak)) if peak else None
    out["gate_12700"] = bool(peak is not None and peak >= GATE)
    # 三指标逐日（日末 = 步 d*24+23）
    daily = []
    for d in range(30):
        idx = min(d * 24 + 23, len(h) - 1)
        farm = h[idx][0]["observation"]["farms"][seat]
        tiles = [t for row in farm["tiles"] for t in row]
        animals = [t for t in tiles if isinstance(t, dict)
                   and "animal" in t]
        sheep = sum(1 for t in animals if t["animal"] == "SHEEP")
        cows = sum(1 for t in animals if t["animal"] == "COW")
        cared = sum(1 for t in animals if t.get("fed_today")
                    and t.get("cared_today"))
        fed = sum(1 for t in animals if t.get("fed_today"))
        # 卖单（当日）
        sold = {}
        for t in range(d * 24, min(d * 24 + 24, len(h))):
            act = (h[t + 1][seat] or {}).get("action") if t + 1 < len(h) \
                else None
            if not act:
                continue
            for o in act.get("market", []):
                if o and o[0] == "SELL":
                    sold[o[1]] = sold.get(o[1], 0) + o[2]
        shed = h[idx][seat]["observation"]["private"]["shed"]
        wool_sold = sold.get("WOOL", 0)
        wool_pool = wool_sold + shed.get("WOOL", 0)
        daily.append({
            "day": d, "sheep": sheep, "cows": cows,
            "care_rate": round(cared / len(animals), 3) if animals else None,
            "fed_rate": round(fed / len(animals), 3) if animals else None,
            "wool_sold": wool_sold,
            "wool_monetization": round(wool_sold / wool_pool, 3)
            if wool_pool else None,
            "shed_wool": shed.get("WOOL", 0),
            "sold": sold,
        })
    out["daily"] = daily
    del env
    return out


def main() -> int:
    yarn2 = scan_yarn2_seeds(range(1, 160), want=2)
    seeds = SELFPLAY_SEEDS + yarn2
    results = {}
    for seed in seeds:
        r = measure(seed)
        results[str(seed)] = r
        tag = "yarn2-constructed" if seed in yarn2 else "selfplay"
        print(f"seed {seed} ({tag}): rewards={r['rewards']} "
              f"shops@88={r['shops_by_step88']} peak_d14_17="
              f"{r['peak_d14_17']}@d{r['peak_day']} "
              f"gate≥{GATE}: {r['gate_12700']}", flush=True)
        print(f"  income: {r['income_curve']}", flush=True)
        print("  sheep:", [e["sheep"] for e in r["daily"]])
        print("  care :", [e["care_rate"] for e in r["daily"]])
        print("  wmonet:", [e["wool_monetization"] for e in r["daily"]])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as h:
        json.dump(results, h, ensure_ascii=False, indent=1)
    print(f"out -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
