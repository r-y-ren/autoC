# -*- coding: utf-8 -*-
# 【中文】income_selfcheck_v6.py —— R9-G2 收入峰自检（临时脚本，落 giant_route/）
# 自打两局（seeds 101/102，与四门同种子）+ 构造 yarn≥2 分支局（seed 141，
# 商铺抽取 d3/d6 双 YARN_STORE → step88 锁 yarn_fast 路由），
# 逐日收入曲线（SELL 侧现金流入，步级正增量求和）与 d14-17 峰 vs 12.7k 门。
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HYBRID = os.path.dirname(HERE)
SOFTWARE = os.path.dirname(os.path.dirname(HYBRID))
sys.path.insert(0, SOFTWARE)
sys.path.insert(0, "/tmp/v6kag")

V6 = os.path.join(HYBRID, "v6", "main.py")
GATE = 12700
SEEDS = [101, 102, 141]


def main() -> int:
    from kaggle_environments import make
    out = {}
    for seed in SEEDS:
        env = make("kag"+"griculture", debug=False,
                   configuration={"seed": seed})
        env.run([V6, V6])
        h = env.steps
        money = [h[i][0]["observation"]["farms"][0]["money"]
                 for i in range(len(h))]
        income = []
        for d in range(30):
            lo, hi = d * 24, min(d * 24 + 24, len(money) - 1)
            inc = sum(max(0.0, money[i + 1] - money[i])
                      for i in range(lo, hi))
            income.append(round(inc, 1))
        peak = max(income[14:18]) if len(income) >= 18 else None
        shops = h[88][0]["observation"].get("town", {}).get(
            "unlocked_shops", [])
        out[str(seed)] = {
            "rewards": [s.reward for s in env.state],
            "statuses": [s.status for s in env.state],
            "shops_by_step88": shops[:2],
            "income_curve": income,
            "peak_d14_17": peak,
            "peak_day": (14 + income[14:18].index(peak)) if peak else None,
            "gate_12700": bool(peak is not None and peak >= GATE),
        }
        print(f"seed {seed}: rewards={out[str(seed)]['rewards']} "
              f"shops@88={shops[:2]} peak_d14_17={peak} "
              f"@d{out[str(seed)]['peak_day']} gate≥{GATE}: "
              f"{out[str(seed)]['gate_12700']}")
        print(f"  income: {income}")
    with open(os.path.join(HERE, "..", "tmp", "probes_v6",
                           "v6_income_selfcheck.json"), "w",
              encoding="utf-8") as h:
        json.dump(out, h, ensure_ascii=False, indent=1)
    print("out -> tmp/probes_v6/v6_income_selfcheck.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
