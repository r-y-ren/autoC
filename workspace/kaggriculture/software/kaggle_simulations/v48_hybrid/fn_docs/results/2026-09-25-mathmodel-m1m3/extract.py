"""M3 步骤 1：控制重演（验证孪生） + 零卖反事实（提取外生流）。
对每局：build_state_from_replay(replay, inject) 后两遍跑：
  A) control: 双席磁带 -> finals 应等于原件 rewards（孪生保真复验）
  B) cf: 我席 SELL 单剔除（其余原样）-> 逐转日志
     cf_inv[t][item]（转开始市库存）、cf_shed[t][item]（转开始我棚）、
     cf_money、opp_sells[t][item]（磁带对手 SELL 量）、
     my_non_sell[t]（我席非 SELL 市单数）、shops_by_day、absorb/day。
写 /tmp/mathmodel/<ep>.json
"""
import os, sys, json
sys.path.insert(0, "/tmp/mathmodel")
from common import (CAMP, REPLAY_DIR, OUT, CORPUS, STEPS_PER_DAY, PRODUCTS,
                    load_twin, load_replay, replay_actions)

twin = load_twin()
BUNDLE = twin.load_engine()
MOD = BUNDLE.module
SHOPS = MOD.SHOPS
TOWN_CENTER_PRODUCTS = MOD.TOWN_CENTER_PRODUCTS

EPISODE_STEPS = 720
LAST_STEP = 717   # 允许市处理的最后转移（718 解释器置 DONE 前一步）；保守取 717
SELL_HOUR = 23
LAST_DAY_HOUR = 22  # day29 h22 = step 718 前；实际从 control 验证后取


def strip_my_sells(action, t=None):
    if not isinstance(action, dict):
        return action
    m = action.get("market")
    if not isinstance(m, list):
        return action
    keep = [o for o in m if not (isinstance(o, (list, tuple)) and o and o[0] == "SELL")]
    if len(keep) == len(m):
        return action
    a2 = dict(action)
    a2["market"] = keep
    return a2


def run_variant(replay, inject, me, my_mutator, log=False):
    acts = replay_actions(replay)
    state = twin.build_state_from_replay(replay, inject, BUNDLE)
    log_rows = []
    t = inject
    while not state.env.done and t < len(acts):
        obs0 = state.seats[0].observation
        if log:
            row = {
                "inv": dict(obs0.market["inventory"]),
                "shed": dict(state.seats[me].observation.private["shed"]),
                "money": [float(f["money"]) for f in obs0.farms],
                "opp_sell": {},
                "shops": list(obs0.town.get("unlocked_shops", [])),
            }
            for o in (acts[t][1 - me] or {}).get("market", []) if isinstance(acts[t][1 - me], dict) else []:
                if isinstance(o, (list, tuple)) and len(o) >= 3 and o[0] == "SELL" and o[1] in PRODUCTS:
                    try:
                        row["opp_sell"][o[1]] = row["opp_sell"].get(o[1], 0) + max(0, int(o[2]))
                    except (TypeError, ValueError):
                        pass
            log_rows.append(row)
        pair = [acts[t][1 - me]] * 2
        mine = my_mutator(acts[t][me], t)
        pair[me] = mine
        twin.step(state, pair)
        t += 1
    finals = twin.final_money(state)
    return finals, log_rows, t


def main():
    out = {}
    for (ep, me, om, oppf, pd, pa) in CORPUS:
        replay = load_replay(ep)
        inject = pd * STEPS_PER_DAY
        # A) control
        finals_c, _, last_t = run_variant(replay, inject, me, lambda a, t: a)
        ok = abs(finals_c[0] - replay["rewards"][0]) < 1e-6 and abs(finals_c[1] - replay["rewards"][1]) < 1e-6
        # B) counterfactual (strip my SELLs)
        finals_z, logs, _ = run_variant(replay, inject, me, strip_my_sells, log=True)
        # 日吸收（确定性：商店实例×6 事件 + 镇心 1）
        days = sorted({i // STEPS_PER_DAY for i in range(inject, len(logs) + inject)})
        absorb = {}
        for d in days:
            shops = []
            for i, row in enumerate(logs):
                if (inject + i) // STEPS_PER_DAY == d:
                    shops = row["shops"]  # 同日不变
                    break
            a = {it: 1 if it in TOWN_CENTER_PRODUCTS else 0 for it in PRODUCTS}
            for s in shops:
                prods = SHOPS[s]
                mult = 2 if len(prods) == 1 else 1
                for it in prods:
                    a[it] = a.get(it, 0) + 6 * mult
            absorb[d] = a
        out[str(ep)] = {
            "me": me, "peak_day": pd, "inject": inject,
            "orig_rewards": replay["rewards"], "orig_margin": om, "opp_final": oppf,
            "control_finals": finals_c, "control_ok": ok, "last_t": last_t,
            "cf_finals": finals_z,
            "logs": logs, "absorb": absorb,
        }
        print(f"ep {ep} me={me} peak_d={pd} control_ok={ok} "
              f"ctrl={finals_c} orig={replay['rewards']} cf={finals_z}")
    json.dump(out, open(os.path.join(OUT, "extract.json"), "w"))
    print("written", os.path.join(OUT, "extract.json"))


if __name__ == "__main__":
    main()
