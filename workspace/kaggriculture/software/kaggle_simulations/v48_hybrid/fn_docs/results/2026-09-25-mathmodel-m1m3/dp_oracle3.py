"""M3 v3（判决版）：孪生精确策略族 + 收入型 DP 候选。
策略族（全部引擎精确复算，margin=我终局−对手终局）：
  tape          磁带原样（= 原局）
  dump          每转全抛
  late20        仅 h∈{20..23} 全抛（吸收事件后）
  h0late        h∈{0,20..23} 全抛（含 EOD 批次）
  hold3/7/14    持有 X 日（不卖）后全抛+随到随抛
  dp            收入型逐转 DP（到达上界+棚容配额+联合修复）
  tape_capture  磁带卖单 + 棚近满(h>=90)时额外清 + 末日清
输出逐局最优与判决。
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


def run_policy2(replay, inject, me, policy=None, keep_tape=False, rec=None, extra_capture=False):
    """policy(t, state)->{item:qty}；keep_tape 时磁带原样；
    extra_capture: 在磁带市单之外附加卖单（tape_capture 用）。"""
    acts = replay_actions(replay)
    state = twin.build_state_from_replay(replay, inject, D2.BUNDLE)
    if rec is not None:
        rec.bind(state)
    t, trunc_total = inject, 0
    last_t = len(acts)
    while not state.env.done and t < len(acts):
        if rec is not None:
            rec.tick()
        if keep_tape and not extra_capture:
            mine = acts[t][me]
        else:
            sells = {}
            if extra_capture:
                shed_now = state.seats[me].observation.private["shed"]
                h = t % 24
                last2 = t >= 719 - 2 * STEPS_PER_DAY
                if sum(shed_now.values()) >= 90 or last2 or h == 23:
                    sells = {it: shed_now.get(it, 0) for it in PRODUCTS
                             if shed_now.get(it, 0) > 0}
            else:
                sells = policy(t, state) or {}
            orders = [["SELL", it, int(q)] for it, q in sorted(sells.items()) if q > 0]
            if keep_tape:  # tape_capture：磁带市单在前，追加捕获卖单
                base_m = acts[t][me] if isinstance(acts[t][me], dict) else {}
                total = list(base_m.get("market") or []) + orders
                base = dict(base_m)
            else:
                base = acts[t][me] if isinstance(acts[t][me], dict) else {}
                total = list(D2.non_sells(acts[t][me])) + orders
            trunc_total += max(0, len(total) - 10)
            mine = dict(base)
            mine["market"] = total[:10]
        pair = [acts[t][1 - me]] * 2
        pair[me] = mine
        twin.step(state, pair)
        t += 1
    return {"finals": twin.final_money(state), "trunc": trunc_total}


def dp_rev_schedule(turns, logs, It, arrivals, me, cap_alloc):
    from dp_oracle2 import dp_margin
    scheds_raw = {}
    for it in PRODUCTS:
        if max(It[it].values()) <= 0:
            continue
        cf_inv = {turns[i]: logs[i]["inv"].get(it, 10000) for i in range(len(turns))}
        opp0 = {t: 0 for t in turns}   # 收入型：无对手项（me==1 路径 Ov=0）
        rv, s = dp_margin(it, turns, cf_inv, opp0, It[it], 1, cap_alloc[it])
        for t, q in s.items():
            scheds_raw.setdefault(t, {})[it] = q
    prices_now = {it: {} for it in PRODUCTS}
    for i, t in enumerate(turns):
        for it in PRODUCTS:
            prices_now[it][t] = MOD.market_price(it, logs[i]["inv"].get(it, 10000))
    return D2.repair_joint(scheds_raw, turns, arrivals, logs[0]["shed"], prices_now)


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
            turns = [inject + i for i in range(len(logs))]
            # dump：到达曲线/总流（rec.log 每 run 独立段）
            rec.log = []
            r_dump = run_policy2(replay, inject, me,
                                 lambda t, s: {it: 10 ** 6 for it in PRODUCTS}, rec=rec)
            dump_log = rec.log
            arrivals, It = {it: {} for it in PRODUCTS}, {it: {} for it in PRODUCTS}
            prev = {it: 0 for it in PRODUCTS}
            for i in range(len(dump_log)):
                t = turns[i]
                s = dump_log[i].get(me, {})
                for it in PRODUCTS:
                    q = s.get(it, (0, 0.0))[0]
                    arrivals[it][t] = max(0, q - prev[it])
                    prev[it] = q
                    It[it][t] = q
            active = [it for it in PRODUCTS if max(It[it].values()) > 0]
            cap_alloc = {it: max(6, SHED_CAP // max(1, len(active))) for it in active}
            sched_dp = dp_rev_schedule(turns, logs, It, arrivals, me, cap_alloc)

            def hold_policy(X):
                def pol(t, s):
                    if t < inject + X * STEPS_PER_DAY:
                        return None
                    return {it: 10 ** 6 for it in PRODUCTS}
                return pol

            fam = [
                ("tape", dict(keep_tape=True)),
                ("dump", dict(policy=lambda t, s: {it: 10 ** 6 for it in PRODUCTS})),
                ("late20", dict(policy=lambda t, s: {it: 10 ** 6 for it in PRODUCTS}
                                if t % 24 >= 20 else None)),
                ("h0late", dict(policy=lambda t, s: {it: 10 ** 6 for it in PRODUCTS}
                                if (t % 24 == 0 or t % 24 >= 20) else None)),
                ("hold3", dict(policy=hold_policy(3))),
                ("hold7", dict(policy=hold_policy(7))),
                ("hold14", dict(policy=hold_policy(14))),
                ("dp", dict(policy=lambda t, s, sc=sched_dp: sc.get(t))),
                ("tape_capture", dict(keep_tape=True, extra_capture=True)),
            ]
            res = {"me": me, "peak_day": pd, "orig_margin": d["orig_margin"],
                   "opp_final_orig": oppf,
                   "my_total_flow": {it: int(max(It[it].values())) for it in active}}
            best_name, best_m = None, -1e18
            for name, kw in fam:
                r = run_policy2(replay, inject, me, rec=rec, **kw)
                m = r["finals"][me] - r["finals"][1 - me]
                res[name] = {"finals": r["finals"], "margin": m, "trunc": r["trunc"]}
                if m > best_m:
                    best_name, best_m = name, m
            res["best"] = {"policy": best_name, "margin": best_m}
            results[key] = res
            cols = " ".join(f"{n}={res[n]['margin']:.0f}" for n, _ in fam)
            print(f"ep {ep} orig={d['orig_margin']:.0f} {cols} "
                  f"best={best_name}:{best_m:.0f} {'SAVABLE' if best_m > 0 else 'no'}",
                  flush=True)
    finally:
        rec.close()
    json.dump(results, open(os.path.join(OUT, "oracle3.json"), "w"))
    savable = sum(1 for r in results.values() if r["best"]["margin"] > 0)
    print(f"\nSAVABLE COUNT = {savable}/14")
    print("written", os.path.join(OUT, "oracle3.json"))


if __name__ == "__main__":
    main()
