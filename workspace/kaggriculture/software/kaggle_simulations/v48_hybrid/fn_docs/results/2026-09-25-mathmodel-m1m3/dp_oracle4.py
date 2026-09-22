"""M3 v4（修正账户版）：到达曲线=每转打点累计；策略族含磁带小时重定时。
策略族（孪生精确）：
  tape / final2 / capture / dump / late20 / h0late / tape_h23 / dp
U_rev 宽上界 = Σ 流量×各品 cf 路径最高价。判决=族内最优 margin。
"""
import os, sys, json
import numpy as np
sys.path.insert(0, "/tmp/mathmodel")
from common import (OUT, CORPUS, STEPS_PER_DAY, PRODUCTS, load_twin, load_replay,
                    replay_actions)
import dp_oracle2 as D2

twin = D2.twin
MOD = D2.MOD
SHED_CAP = 100


def tape_sell_orders(acts, me, t):
    a = acts[t][me] if isinstance(acts[t][me], dict) else {}
    out = {}
    for o in (a.get("market") or []):
        if isinstance(o, (list, tuple)) and len(o) >= 3 and o[0] == "SELL":
            try:
                out[o[1]] = out.get(o[1], 0) + max(0, int(o[2]))
            except (TypeError, ValueError):
                pass
    return out


def run_p(replay, inject, me, acts, mode, sched=None, tape_sells_by_day=None,
          rec=None):
    """mode: tape|final2|capture|dump|late20|h0late|tape_h23|dp"""
    state = twin.build_state_from_replay(replay, inject, D2.BUNDLE)
    if rec is not None:
        rec.bind(state)
    t, trunc = inject, 0
    while not state.env.done and t < len(acts):
        if rec is not None:
            rec.tick()
        h = t % 24
        if mode == "tape":
            mine = acts[t][me]
        else:
            sells = {}
            if mode in ("dump",):
                sells = {it: 10 ** 6 for it in PRODUCTS}
            elif mode == "late20" and h >= 20:
                sells = {it: 10 ** 6 for it in PRODUCTS}
            elif mode == "h0late" and (h == 0 or h >= 20):
                sells = {it: 10 ** 6 for it in PRODUCTS}
            elif mode == "final2":
                sells = dict(tape_sells_by_day.get(t, {}))
                if t >= 719 - 48:
                    shed_now = state.seats[me].observation.private["shed"]
                    for it in PRODUCTS:
                        if shed_now.get(it, 0) > sells.get(it, 0):
                            sells[it] = shed_now.get(it, 0)
            elif mode == "capture":
                sells = dict(tape_sells_by_day.get(t, {}))
                shed_now = state.seats[me].observation.private["shed"]
                if sum(shed_now.values()) >= 90 or t >= 719 - 48:
                    for it in PRODUCTS:
                        if shed_now.get(it, 0) > sells.get(it, 0):
                            sells[it] = shed_now.get(it, 0)
            elif mode == "tape_h23":
                sells = dict(tape_sells_by_day.get(t, {})) if h == 23 else {}
            elif mode == "dp":
                sells = dict((sched or {}).get(t, {}))
            orders = [["SELL", it, int(q)] for it, q in sorted(sells.items()) if q > 0]
            base = acts[t][me] if isinstance(acts[t][me], dict) else {}
            if mode in ("final2", "capture", "tape_h23"):
                # 保留磁带全部市单（含其 SELL）再附加/替换——重定型时去掉磁带原 SELL
                keep = [o for o in (base.get("market") or [])
                        if not (isinstance(o, (list, tuple)) and o and o[0] == "SELL")]
                total = keep + orders
            else:
                total = list(D2.non_sells(acts[t][me])) + orders
            trunc += max(0, len(total) - 10)
            mine = dict(base)
            mine["market"] = total[:10]
        pair = [acts[t][1 - me]] * 2
        pair[me] = mine
        twin.step(state, pair)
        t += 1
    return {"finals": twin.final_money(state), "trunc": trunc}


def dp_rev(turns, cf_inv, arrivals_cum, cap_alloc):
    """收入型逐转 DP（me==1 语义：无对手项）。返回 sched。"""
    tbl = D2.price_tbl_np("WHEAT")  # 占位
    sched = {}
    for it in PRODUCTS:
        M = int(max(arrivals_cum.get(t, 0) for t in turns)) if turns else 0
        if M <= 0:
            continue
        tbl = D2.price_tbl_np(it)
        Ms = np.arange(M + 1)
        dp = np.zeros(M + 1)
        choice = np.zeros((len(turns), M + 1), dtype=np.int32)
        for idx in range(len(turns) - 1, -1, -1):
            t = turns[idx]
            bd = int(arrivals_cum.get(t, 0))
            b = int(min(M, bd))
            L = int(min(b, max(0, bd - int(cap_alloc))))
            v0 = int(cf_inv.get(t, 10000))
            A = np.concatenate(([0.0], np.cumsum(tbl[v0:v0 + M + 1])[:-1]))
            G = A + dp
            suf = np.full(M + 1, -np.inf)
            arg = np.full(M + 1, b, dtype=np.int32)
            if b >= 0:
                gv = G[: b + 1]
                cm = np.maximum.accumulate(gv[::-1])[::-1]
                suf[: b + 1] = cm
                marked = np.where(gv == cm, np.arange(b + 1), -1)
                arg[: b + 1] = np.maximum.accumulate(marked[::-1])[::-1]
            lo = np.maximum(Ms, L)
            idxs = np.minimum(lo, b)
            dp = np.where(Ms <= b, suf[idxs], G) - A
            choice[idx] = np.where(Ms <= b, arg[idxs], Ms)
        m = 0
        for idx, t in enumerate(turns):
            x = int(choice[idx][m])
            if x > m:
                sched.setdefault(t, {})[it] = x - m
            m = x
    return sched


def repair(sched, turns, arrivals, shed0, prices_now):
    shed = dict(shed0)
    out = {}
    for t in turns:
        for it in PRODUCTS:
            shed[it] = shed.get(it, 0) + arrivals.get(it, {}).get(t, 0)
        want = {}
        for it, q in sched.get(t, {}).items():
            q = min(int(q), shed.get(it, 0))
            want[it] = q
            shed[it] -= q
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
        out[t] = {k: v for k, v in want.items() if v > 0}
    return out


def main():
    ex = json.load(open(os.path.join(OUT, "extract.json")))
    results = {}
    rec = D2.Recorder()
    try:
        for (ep, me, om, oppf, pd, pa) in CORPUS:
            key = str(ep)
            d = ex[key]
            inject, logs = d["inject"], d["logs"]
            replay = load_replay(ep)
            acts = replay_actions(replay)
            turns = [inject + i for i in range(len(logs))]
            # tape 跑：到达曲线 + 每转卖单账
            rec.log = []
            r_tape = run_p(replay, inject, me, acts, "tape", rec=rec)
            tape_log = rec.log
            arrivals = {it: {} for it in PRODUCTS}
            cum = {it: 0 for it in PRODUCTS}
            arrivals_cum = {it: {} for it in PRODUCTS}
            tape_units, tape_rev = {}, 0.0
            shed0 = logs[0]["shed"]
            for i in range(len(tape_log)):
                t = turns[i]
                s = tape_log[i].get(me, {})
                for it in PRODUCTS:
                    q = s.get(it, (0, 0.0))[0]
                    arrivals[it][t] = q
                    cum[it] += q
                    arrivals_cum[it][t] = cum[it] + shed0.get(it, 0)
                for it, (q, r) in s.items():
                    tape_units[it] = tape_units.get(it, 0) + q
                    tape_rev += r
            tape_sells_by_day = {}
            for t in turns:
                so = tape_sell_orders(acts, me, t)
                if so:
                    tape_sells_by_day[t] = so
            active = [it for it in PRODUCTS if arrivals_cum[it][turns[-1]] > 0]
            cap_alloc = {it: max(8, SHED_CAP // max(1, len(active))) for it in active}
            cf_inv = {it: {turns[i]: logs[i]["inv"].get(it, 10000)
                           for i in range(len(turns))} for it in active}
            sched_dp_raw = dp_rev(turns, {it: cf_inv[it] for it in active},
                                  {it: arrivals_cum[it] for it in active}, 10 ** 9)
            # cap_alloc=∞：纯到达约束（可 HOLD）→ 再用修复器强制联合棚容
            prices_now = {it: {} for it in PRODUCTS}
            for i, t in enumerate(turns):
                for it in active:
                    prices_now[it][t] = MOD.market_price(it, logs[i]["inv"].get(it, 10000))
            sched_dp = repair(sched_dp_raw, turns, arrivals, shed0, prices_now)
            # U_rev 宽上界
            U_rev = 0.0
            for it in active:
                best_p = max(prices_now[it].values())
                U_rev += arrivals_cum[it][turns[-1]] * best_p
            fam = ["tape", "final2", "capture", "dump", "late20", "h0late",
                   "tape_h23", "dp"]
            res = {"me": me, "peak_day": pd, "orig_margin": d["orig_margin"],
                   "opp_final_orig": oppf, "tape_rev_post": tape_rev,
                   "tape_units": tape_units,
                   "flow": {it: int(arrivals_cum[it][turns[-1]]) for it in active},
                   "U_rev": U_rev, "peak_money": logs[0]["money"][me]}
            best_name, best_m = None, -1e18
            for mode in fam:
                kw = {}
                if mode in ("final2", "capture", "tape_h23"):
                    kw["tape_sells_by_day"] = tape_sells_by_day
                if mode == "dp":
                    kw["sched"] = sched_dp
                r = run_p(replay, inject, me, acts, mode, rec=rec, **kw)
                m = r["finals"][me] - r["finals"][1 - me]
                res[mode] = {"finals": r["finals"], "margin": m, "trunc": r["trunc"]}
                if m > best_m:
                    best_name, best_m = mode, m
            res["best"] = {"policy": best_name, "margin": best_m}
            results[key] = res
            cols = " ".join(f"{n}={res[n]['margin']:.0f}" for n in fam)
            print(f"ep {ep} orig={d['orig_margin']:.0f} tapeRev={tape_rev:.0f} "
                  f"Urev={U_rev:.0f} {cols} best={best_name}:{best_m:.0f} "
                  f"{'SAVABLE' if best_m > 0 else 'no'}", flush=True)
    finally:
        rec.close()
    json.dump(results, open(os.path.join(OUT, "oracle4.json"), "w"))
    savable = sum(1 for r in results.values() if r["best"]["margin"] > 0)
    print(f"\nSAVABLE COUNT = {savable}/14")


if __name__ == "__main__":
    main()
