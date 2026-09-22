"""M3 核心：卖侧先知最优。三族候选 + 孪生复算：
  L0 dump：每转全抛（下界策略；同时给出总流曲线 I(t)）
  D1：逐转 DP（库存约束=零卖反事实 cf_shed，保守可行）
  D2：逐转 DP（库存约束=总流 I(t)，+棚容100强制下限卖，宽松上界方向）
DP 逐转状态 = 累计已卖 m；转移 x∈[max(m,L), max(m,b)]；收入=前缀和差；
numpy 后缀 max + O(b) 回溯 argmax。
"""
import os, sys, json
import numpy as np
sys.path.insert(0, "/tmp/mathmodel")
from common import (OUT, CORPUS, STEPS_PER_DAY, PRODUCTS, load_twin, load_replay,
                    replay_actions)

twin = load_twin()
BUNDLE = twin.load_engine()
MOD = BUNDLE.module

SHED_CAP = 100
_price_cache = {}


def price_tbl(item):
    if item not in _price_cache:
        _price_cache[item] = [MOD.market_price(item, v) for v in range(30001)]
    return _price_cache[item]


def non_sells(action):
    if not isinstance(action, dict):
        return []
    m = action.get("market")
    if not isinstance(m, list):
        return []
    return [o for o in m if not (isinstance(o, (list, tuple)) and o and o[0] == "SELL")]


def run_policy(replay, inject, me, policy, log_stock=False):
    """policy(t) -> {item: qty}；我席 farmer/hands/非SELL 市单沿磁带，SELL 换注入。"""
    acts = replay_actions(replay)
    state = twin.build_state_from_replay(replay, inject, BUNDLE)
    logs, t, trunc_total = [], inject, 0
    sold_cum = {it: 0 for it in PRODUCTS}
    while not state.env.done and t < len(acts):
        if log_stock:
            logs.append({"shed": dict(state.seats[me].observation.private["shed"]),
                         "sold": dict(sold_cum),
                         "inv": dict(state.seats[0].observation.market["inventory"]),
                         "money": float(state.seats[me].observation.farms[me]["money"])})
        sells = policy(t) or {}
        orders = [["SELL", it, int(q)] for it, q in sorted(sells.items()) if q > 0]
        base = acts[t][me] if isinstance(acts[t][me], dict) else {}
        total = list(non_sells(acts[t][me])) + orders
        trunc_total += max(0, len(total) - 10)
        mine = dict(base)
        mine["market"] = total[:10]
        pair = [acts[t][1 - me]] * 2
        pair[me] = mine
        shed_now = state.seats[me].observation.private["shed"]
        for it, q in sells.items():
            if q > 0:
                sold_cum[it] += min(int(q), shed_now.get(it, 0))
        twin.step(state, pair)
        t += 1
    return {"finals": twin.final_money(state), "logs": logs, "trunc": trunc_total,
            "last_t": t}


def dp_schedule(item, turns, cf_inv, opp_sell, bound, force_shed_cap=True):
    """逐转 DP。返回 (model_rev, {turn: qty}, M)。"""
    tbl = price_tbl(item)
    if not turns:
        return 0.0, {}, 0
    M = int(max(bound.get(t, 0) for t in turns))
    if M <= 0:
        return 0.0, {}, 0
    Ms = np.arange(M + 1)
    dp = np.zeros(M + 1)
    choice = np.zeros((len(turns), M + 1), dtype=np.int32)
    for idx in range(len(turns) - 1, -1, -1):
        t = turns[idx]
        b = int(min(M, bound.get(t, 0)))
        L = int(max(0, bound.get(t, 0) - SHED_CAP)) if force_shed_cap else 0
        L = min(L, b)
        v0 = cf_inv.get(t, 10000) + 0.5 * opp_sell.get(t, 0)
        base_i = int(round(v0))
        prices = np.array([tbl[base_i + j] if base_i + j < 30001 else 1
                           for j in range(M + 1)], dtype=np.float64)
        A = np.concatenate(([0.0], np.cumsum(prices[:-1])))
        # A[u] = Σ_{j=0}^{u-1} p(v0 + j)；m→x 收入 = A[x]-A[m]
        G = A + dp
        # 后缀 max/argmax over [i, b]
        suf = np.full(M + 1, -np.inf)
        arg = np.full(M + 1, b, dtype=np.int32)
        if b >= 0:
            gv = G[: b + 1]
            cm = np.maximum.accumulate(gv[::-1])[::-1]
            suf[: b + 1] = cm
            ca = np.zeros(b + 1, dtype=np.int32)
            run_v, run_i = -np.inf, b
            for i in range(b, -1, -1):
                if gv[i] > run_v:
                    run_v, run_i = gv[i], i
                ca[i] = run_i
            arg[: b + 1] = ca
        lo = np.maximum(Ms, L)          # x 下限
        x_pick = np.where(Ms <= b, arg[np.minimum(lo, b)], Ms)
        val = np.where(Ms <= b, suf[np.minimum(lo, b)], G)
        dp = val - A
        choice[idx] = x_pick
    sched, m = {}, 0
    for idx, t in enumerate(turns):
        x = int(choice[idx][m])
        if x > m:
            sched[t] = x - m
        m = x
    return float(dp[0]), sched, M


def main():
    ex = json.load(open(os.path.join(OUT, "extract.json")))
    results = {}
    for (ep, me, om, oppf, pd, pa) in CORPUS:
        key = str(ep)
        d = ex[key]
        inject, logs = d["inject"], d["logs"]
        replay = load_replay(ep)
        turns = [inject + i for i in range(len(logs))]
        # L0 dump（下界 + 总流）
        r_dump = run_policy(replay, inject, me,
                            lambda t: {it: 10 ** 6 for it in PRODUCTS}, log_stock=True)
        It = {it: {} for it in PRODUCTS}
        for i, row in enumerate(r_dump["logs"]):
            for it in PRODUCTS:
                It[it][turns[i]] = row["shed"].get(it, 0) + row["sold"].get(it, 0)
        scheds = {"d1": {}, "d2": {}}
        dp_models = {}
        for it in PRODUCTS:
            cf_inv = {turns[i]: logs[i]["inv"].get(it, 10000) for i in range(len(turns))}
            opp_sell = {turns[i]: logs[i]["opp_sell"].get(it, 0) for i in range(len(turns))}
            cf_shed = {turns[i]: logs[i]["shed"].get(it, 0) for i in range(len(turns))}
            rev1, s1, _ = dp_schedule(it, turns, cf_inv, opp_sell, cf_shed, False)
            rev2, s2, _ = dp_schedule(it, turns, cf_inv, opp_sell, It[it], True)
            dp_models[it] = {"rev_d1": rev1, "rev_d2": rev2,
                             "total_flow": int(max(It[it].values())) if It[it] else 0}
            for t, q in s1.items():
                scheds["d1"].setdefault(t, {})[it] = q
            for t, q in s2.items():
                scheds["d2"].setdefault(t, {})[it] = q
        runs = {"d1": run_policy(replay, inject, me, lambda t, s=scheds["d1"]: s.get(t, {})),
                "d2": run_policy(replay, inject, me, lambda t, s=scheds["d2"]: s.get(t, {}))}
        res = {"me": me, "peak_day": pd, "orig_margin": d["orig_margin"],
               "opp_final_orig": oppf}
        res["dump"] = {"finals": r_dump["finals"],
                       "margin": r_dump["finals"][me] - r_dump["finals"][1 - me]}
        for k in ("d1", "d2"):
            res[k] = {"finals": runs[k]["finals"],
                      "margin": runs[k]["finals"][me] - runs[k]["finals"][1 - me],
                      "trunc": runs[k]["trunc"]}
        res["dp_models"] = dp_models
        res["dp_model_d2_total"] = sum(v["rev_d2"] for v in dp_models.values())
        results[key] = res
        best = max(res["dump"]["margin"], res["d1"]["margin"], res["d2"]["margin"])
        print(f"ep {ep} orig={d['orig_margin']:.0f} dump={res['dump']['margin']:.0f} "
              f"d1={res['d1']['margin']:.0f} d2={res['d2']['margin']:.0f} "
              f"dp_model_d2={res['dp_model_d2_total']:.0f} best={best:.0f} "
              f"{'SAVABLE' if best > 0 else 'no'}")
    json.dump(results, open(os.path.join(OUT, "oracle.json"), "w"))
    print("written", os.path.join(OUT, "oracle.json"))


if __name__ == "__main__":
    main()
