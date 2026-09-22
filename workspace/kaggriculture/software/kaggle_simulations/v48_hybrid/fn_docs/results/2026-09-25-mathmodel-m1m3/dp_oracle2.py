"""M3 v2：卖侧先知最优（margin 目标 + 联合棚容修复 + 策略族）。

- 引擎 _commit_unit 打点：逐转精确记录双席各品实现卖量/卖价。
- DP 逐转逐品：状态=累计已卖 m；目标=我方收入−对手收入位移
  （对手量沿磁带固定；其单价随 cf_inv+m 移动；我席 0 时同转我卖在前）。
- bound[t]=总流曲线 I(t)；联合棚容 ≤100 由修复模拟器强制。
- 策略族（孪生复算，引擎精确）：tape/nosell/dump/dawn/h23 + DP 修复排程。
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
ORIG_COMMIT = MOD._commit_unit
_price_cache = {}


def price_tbl_np(item):
    if item not in _price_cache:
        pad = np.full(40000, 1, dtype=np.float64)
        for v in range(30001):
            pad[v] = MOD.market_price(item, v)
        _price_cache[item] = pad
    return _price_cache[item]


def non_sells(action):
    if not isinstance(action, dict):
        return []
    m = action.get("market")
    if not isinstance(m, list):
        return []
    return [o for o in m if not (isinstance(o, (list, tuple)) and o and o[0] == "SELL")]


class Recorder:
    def __init__(self):
        self.seat_farm = {}
        self.cur = {}
        self.log = []
        MOD._commit_unit = self._commit

    def bind(self, state):
        obs0 = state.seats[0].observation
        for i, f in enumerate(obs0.farms):
            self.seat_farm[id(f)] = i

    def _commit(self, op, item, price, farm, private, market, shed_capacity=100):
        ok = ORIG_COMMIT(op, item, price, farm, private, market, shed_capacity)
        if ok and op == "SELL":
            seat = self.seat_farm.get(id(farm), -1)
            d = self.cur.setdefault(seat, {}).setdefault(item, [0, 0.0])
            d[0] += 1
            d[1] += price
        return ok

    def tick(self):
        snap, self.cur = self.cur, {}
        self.log.append(snap)

    def close(self):
        MOD._commit_unit = ORIG_COMMIT


def run_policy(replay, inject, me, policy=None, keep_tape=False, rec=None):
    """policy(t)->{item:qty}；keep_tape=True 时我席磁带原样（含原 SELL）。"""
    acts = replay_actions(replay)
    state = twin.build_state_from_replay(replay, inject, BUNDLE)
    if rec is not None:
        rec.bind(state)
    t, trunc_total = inject, 0
    while not state.env.done and t < len(acts):
        if rec is not None:
            rec.tick()
        if keep_tape:
            mine = acts[t][me]
        else:
            sells = policy(t) or {}
            orders = [["SELL", it, int(q)] for it, q in sorted(sells.items()) if q > 0]
            base = acts[t][me] if isinstance(acts[t][me], dict) else {}
            total = list(non_sells(acts[t][me])) + orders
            trunc_total += max(0, len(total) - 10)
            mine = dict(base)
            mine["market"] = total[:10]
        pair = [acts[t][1 - me]] * 2
        pair[me] = mine
        twin.step(state, pair)
        t += 1
    return {"finals": twin.final_money(state), "trunc": trunc_total}


def dp_margin(item, turns, cf_inv, opp_sell, bound, me, cap_alloc):
    tbl = price_tbl_np(item)
    if not turns:
        return 0.0, {}
    M = int(max(bound.get(t, 0) for t in turns))
    if M <= 0:
        return 0.0, {}
    Ms = np.arange(M + 1)
    dp = np.zeros(M + 1)
    choice = np.zeros((len(turns), M + 1), dtype=np.int32)
    for idx in range(len(turns) - 1, -1, -1):
        t = turns[idx]
        bd = int(bound.get(t, 0))
        b = int(min(M, bd))
        L = int(min(b, max(0, bd - max(0, int(cap_alloc)))))
        v0 = int(cf_inv.get(t, 10000))
        ot = int(opp_sell.get(t, 0))
        A = np.concatenate(([0.0], np.cumsum(tbl[v0:v0 + M + 1])[:-1]))
        if ot > 0:
            cs = np.concatenate(([0.0], np.cumsum(tbl[v0:v0 + M + 1 + ot])))
            Ov = (cs[ot:ot + M + 1] - cs[:M + 1])
        else:
            Ov = np.zeros(M + 1)
        G = A - Ov + dp if me == 0 else A + dp
        suf = np.full(M + 1, -np.inf)
        arg = np.full(M + 1, b, dtype=np.int32)
        if b >= 0:
            gv = G[: b + 1]
            cm = np.maximum.accumulate(gv[::-1])[::-1]
            suf[: b + 1] = cm
            ar = np.arange(b + 1)
            marked = np.where(gv == cm, ar, -1)
            arg[: b + 1] = np.maximum.accumulate(marked[::-1])[::-1]
        lo = np.maximum(Ms, L)
        idxs = np.minimum(lo, b)
        dp = np.where(Ms <= b, suf[idxs], G) - A - (Ov if me == 1 else 0.0)
        choice[idx] = np.where(Ms <= b, arg[idxs], Ms)
    sched, m = {}, 0
    for idx, t in enumerate(turns):
        x = int(choice[idx][m])
        if x > m:
            sched[t] = x - m
        m = x
    return float(dp[0]), sched


def repair_joint(sched, turns, arrivals, shed0, prices_now):
    shed = dict(shed0)
    out = {}
    for t in turns:
        for it in PRODUCTS:
            shed[it] = shed.get(it, 0) + arrivals.get(it, {}).get(t, 0)
        want = {}
        for it, q in sched.get(t, {}).items():
            q = min(int(q), shed.get(it, 0))
            want[it] = q
            shed[it] = shed.get(it, 0) - q
        tot = sum(shed.values())
        if tot > SHED_CAP:
            order = sorted(shed, key=lambda it: (prices_now.get(it, {}).get(t, 9999),
                                                 -shed.get(it, 0)))
            need = tot - SHED_CAP
            for it in order:
                if need <= 0:
                    break
                d = min(need, shed.get(it, 0))
                want[it] = want.get(it, 0) + d
                shed[it] -= d
                need -= d
        if any(q > 0 for q in want.values()):
            out[t] = {k: v for k, v in want.items() if v > 0}
    return out


def main():
    ex = json.load(open(os.path.join(OUT, "extract.json")))
    results = {}
    rec = Recorder()
    try:
        for (ep, me, om, oppf, pd, pa) in CORPUS:
            key = str(ep)
            d = ex[key]
            inject, logs = d["inject"], d["logs"]
            replay = load_replay(ep)
            turns = [inject + i for i in range(len(logs))]
            # dump（总流/到达曲线/下界）
            r_dump = run_policy(replay, inject, me,
                                lambda t: {it: 10 ** 6 for it in PRODUCTS}, rec=rec)
            arrivals, It = {it: {} for it in PRODUCTS}, {it: {} for it in PRODUCTS}
            prev = 0
            for i in range(len(rec.log)):
                t = turns[i]
                s = rec.log[i].get(me, {})
                qt = s.get("WHEAT", (0, 0))[0]  # 占位不用
                for it in PRODUCTS:
                    v = s.get(it, (0, 0.0))
                    arrivals[it][t] = 0
                prev = 0
            # arrivals 从 log 重建
            arrivals = {it: {} for it in PRODUCTS}
            It = {it: {} for it in PRODUCTS}
            prev = {it: 0 for it in PRODUCTS}
            for i in range(len(rec.log)):
                t = turns[i]
                s = rec.log[i].get(me, {})
                for it in PRODUCTS:
                    q = s.get(it, (0, 0.0))[0]
                    arrivals[it][t] = max(0, q - prev[it])
                    prev[it] = q
                    It[it][t] = q
            prices_now = {it: {} for it in PRODUCTS}
            for i, t in enumerate(turns):
                for it in PRODUCTS:
                    prices_now[it][t] = MOD.market_price(it, logs[i]["inv"].get(it, 10000))
            active = [it for it in PRODUCTS if max(It[it].values()) > 0]
            cap_alloc = {it: max(6, SHED_CAP // max(1, len(active))) for it in active}
            scheds_raw, model_tot = {}, 0.0
            for it in active:
                cf_inv = {turns[i]: logs[i]["inv"].get(it, 10000) for i in range(len(turns))}
                opp_sell = {turns[i]: logs[i]["opp_sell"].get(it, 0) for i in range(len(turns))}
                rv, s = dp_margin(it, turns, cf_inv, opp_sell, It[it], me, cap_alloc[it])
                model_tot += rv
                for t, q in s.items():
                    scheds_raw.setdefault(t, {})[it] = q
            sched_fix = repair_joint(scheds_raw, turns, arrivals, logs[0]["shed"], prices_now)
            fam = [
                ("tape", dict(keep_tape=True)),
                ("dump", dict(policy=lambda t: {it: 10 ** 6 for it in PRODUCTS})),
                ("dawn", dict(policy=lambda t: {it: 10 ** 6 for it in PRODUCTS} if t % 24 == 0 else None)),
                ("h23", dict(policy=lambda t: {it: 10 ** 6 for it in PRODUCTS} if t % 24 == 23 else None)),
                ("dp", dict(policy=lambda t, s=sched_fix: s.get(t))),
            ]
            res = {"me": me, "peak_day": pd, "orig_margin": d["orig_margin"],
                   "opp_final_orig": oppf, "dp_model_margin": model_tot,
                   "active_items": active, "my_total_flow": {it: int(max(It[it].values())) for it in active}}
            best_name, best_m = None, -1e18
            for name, kw in fam:
                r = run_policy(replay, inject, me, rec=rec, **kw)
                m = r["finals"][me] - r["finals"][1 - me]
                res[name] = {"finals": r["finals"], "margin": m, "trunc": r["trunc"]}
                if m > best_m:
                    best_name, best_m = name, m
            res["best"] = {"policy": best_name, "margin": best_m}
            results[key] = res
            cols = " ".join(f"{n}={res[n]['margin']:.0f}" for n, _ in fam)
            print(f"ep {ep} orig={d['orig_margin']:.0f} {cols} dpM={model_tot:.0f} "
                  f"best={best_name}:{best_m:.0f} {'SAVABLE' if best_m > 0 else 'no'}", flush=True)
    finally:
        rec.close()
    json.dump(results, open(os.path.join(OUT, "oracle2.json"), "w"))
    print("written", os.path.join(OUT, "oracle2.json"))


if __name__ == "__main__":
    main()
