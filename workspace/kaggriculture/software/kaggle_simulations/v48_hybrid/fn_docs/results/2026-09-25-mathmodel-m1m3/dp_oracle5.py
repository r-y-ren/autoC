"""M3 v5（终判）：逐局局部搜索（capture 族参数网格）+ dp_accel（理想前移）。
dp_accel：逐品 DP，约束 累计卖(t) ≥ 磁带累计卖(t) ∀t（只许前移不许迟滞）
→ 现金流不劣于磁带（近似），棚容自动可行（卖更多只腾空间）。
capture(θ,N,hour,γ)：磁带卖单 + 棚≥θ 或 末日N天 时附加清仓
  （hour 过滤捕获时点；γ=仅捕获现价≥γ·base 的品，防砸薄市场）。
判决 = 全族（含 tape/dp_accel/16 网格）最优 margin。
"""
import os, sys, json, itertools
import numpy as np
sys.path.insert(0, "/tmp/mathmodel")
from common import (OUT, CORPUS, STEPS_PER_DAY, PRODUCTS, load_twin, load_replay,
                    replay_actions)
import dp_oracle2 as D2
import dp_oracle4 as D4

twin = D2.twin
MOD = D2.MOD


def run_capture(replay, inject, me, acts, tape_sells, θ, N, hourmode, γ,
                base, rec=None):
    state = twin.build_state_from_replay(replay, inject, D2.BUNDLE)
    if rec is not None:
        rec.bind(state)
    t, trunc = inject, 0
    while not state.env.done and t < len(acts):
        if rec is not None:
            rec.tick()
        h = t % 24
        sells = dict(tape_sells.get(t, {}))
        shed_now = state.seats[me].observation.private["shed"]
        trig = (sum(shed_now.values()) >= θ) or (t >= 719 - N * STEPS_PER_DAY)
        if trig and (hourmode == "any" or h >= 20):
            for it in PRODUCTS:
                extra = shed_now.get(it, 0) - sells.get(it, 0)
                if extra > 0 and (γ <= 0 or
                                  MOD.market_price(it, state.seats[0].observation.
                                                   market["inventory"].get(it, 10000))
                                  >= γ * base.get(it, 1e9)):
                    sells[it] = shed_now.get(it, 0)
        orders = [["SELL", it, int(q)] for it, q in sorted(sells.items()) if q > 0]
        base_a = acts[t][me] if isinstance(acts[t][me], dict) else {}
        keep = [o for o in (base_a.get("market") or [])
                if not (isinstance(o, (list, tuple)) and o and o[0] == "SELL")]
        total = keep + orders
        trunc += max(0, len(total) - 10)
        mine = dict(base_a)
        mine["market"] = total[:10]
        pair = [acts[t][1 - me]] * 2
        pair[me] = mine
        twin.step(state, pair)
        t += 1
    return {"finals": twin.final_money(state), "trunc": trunc}


def dp_accel_sched(turns, cf_inv_by_item, arrivals_cum_by_item, tape_cum_by_item):
    sched = {}
    for it in PRODUCTS:
        ac = arrivals_cum_by_item.get(it, {})
        tc = tape_cum_by_item.get(it, {})
        ci = cf_inv_by_item.get(it, {})
        M = int(max(ac.get(t, 0) for t in turns)) if turns else 0
        if M <= 0:
            continue
        tbl = D2.price_tbl_np(it)
        Ms = np.arange(M + 1)
        dp = np.zeros(M + 1)
        choice = np.zeros((len(turns), M + 1), dtype=np.int32)
        for idx in range(len(turns) - 1, -1, -1):
            t = turns[idx]
            bd = int(ac.get(t, 0))
            b = int(min(M, bd))
            L = int(min(b, tc.get(t, 0)))   # 前移下界=磁带累计
            v0 = int(ci.get(t, 10000))
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


def run_sched(replay, inject, me, acts, sched, rec=None):
    state = twin.build_state_from_replay(replay, inject, D2.BUNDLE)
    if rec is not None:
        rec.bind(state)
    t, trunc = inject, 0
    while not state.env.done and t < len(acts):
        if rec is not None:
            rec.tick()
        sells = dict((sched or {}).get(t, {}))
        orders = [["SELL", it, int(q)] for it, q in sorted(sells.items()) if q > 0]
        base_a = acts[t][me] if isinstance(acts[t][me], dict) else {}
        total = list(D2.non_sells(acts[t][me])) + orders
        trunc += max(0, len(total) - 10)
        mine = dict(base_a)
        mine["market"] = total[:10]
        pair = [acts[t][1 - me]] * 2
        pair[me] = mine
        twin.step(state, pair)
        t += 1
    return {"finals": twin.final_money(state), "trunc": trunc}


def main():
    ex = json.load(open(os.path.join(OUT, "extract.json")))
    base = {it: MOD.MARKET_PARAMS[it]["base"] for it in PRODUCTS}
    results = {}
    rec = D2.Recorder()
    grid = list(itertools.product([85, 95], [2, 4], ["any", "h20"], [0.0, 0.5]))
    try:
        for (ep, me, om, oppf, pd, pa) in CORPUS:
            key = str(ep)
            d = ex[key]
            inject, logs = d["inject"], d["logs"]
            replay = load_replay(ep)
            acts = replay_actions(replay)
            turns = [inject + i for i in range(len(logs))]
            rec.log = []
            r_tape = D4.run_p(replay, inject, me, acts, "tape", rec=rec)
            tape_log = rec.log
            arrivals, cum = {it: {} for it in PRODUCTS}, {it: 0 for it in PRODUCTS}
            arrivals_cum, tape_cum = {it: {} for it in PRODUCTS}, {it: {} for it in PRODUCTS}
            shed0 = logs[0]["shed"]
            tape_rev = 0.0
            for i in range(len(tape_log)):
                t = turns[i]
                s = tape_log[i].get(me, {})
                for it in PRODUCTS:
                    q = s.get(it, (0, 0.0))[0]
                    arrivals[it][t] = q
                    cum[it] += q
                    arrivals_cum[it][t] = cum[it] + shed0.get(it, 0)
                    tape_cum[it][t] = cum[it]
                for it, (q, r) in s.items():
                    tape_rev += r
            tape_sells = {}
            for t in turns:
                so = D4.tape_sell_orders(acts, me, t)
                if so:
                    tape_sells[t] = so
            cf_inv = {it: {turns[i]: logs[i]["inv"].get(it, 10000)
                           for i in range(len(turns))} for it in PRODUCTS}
            sched_accel = dp_accel_sched(turns, cf_inv, arrivals_cum, tape_cum)
            res = {"me": me, "peak_day": pd, "orig_margin": d["orig_margin"],
                   "tape_rev_post": tape_rev, "runs": {}}
            cands = [("tape", r_tape["finals"]),
                     ("dp_accel", run_sched(replay, inject, me, acts,
                                            sched_accel, rec=rec)["finals"])]
            for (θ, N, hm, γ) in grid:
                r = run_capture(replay, inject, me, acts, tape_sells, θ, N, hm, γ,
                                base, rec=rec)
                cands.append((f"cap{θ}_{N}_{hm}_{γ}", r["finals"]))
            best_name, best_m, best_f = None, -1e18, None
            for name, fins in cands:
                m = fins[me] - fins[1 - me]
                res["runs"][name] = {"finals": fins, "margin": m}
                if m > best_m:
                    best_name, best_m, best_f = name, m, fins
            res["best"] = {"policy": best_name, "margin": best_m, "finals": best_f}
            results[key] = res
            print(f"ep {ep} orig={d['orig_margin']:.0f} tapeRev={tape_rev:.0f} "
                  f"best={best_name}:{best_m:.0f} "
                  f"dp_accel={res['runs']['dp_accel']['margin']:.0f} "
                  f"{'SAVABLE' if best_m > 0 else 'no'}", flush=True)
    finally:
        rec.close()
    json.dump(results, open(os.path.join(OUT, "oracle5.json"), "w"))
    savable = sum(1 for r in results.values() if r["best"]["margin"] > 0)
    print(f"\nSAVABLE COUNT = {savable}/14")


if __name__ == "__main__":
    main()
