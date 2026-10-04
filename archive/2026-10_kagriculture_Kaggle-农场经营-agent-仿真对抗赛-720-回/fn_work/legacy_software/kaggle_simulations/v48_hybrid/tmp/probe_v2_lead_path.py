# -*- coding: utf-8 -*-
# 临时探针（R8-v2 F5）：逐日 lead 路径追踪（对照臂），验证回撤臂失配细节。
import os, sys
sys.path.insert(0, 'gates')
import gate_common as gc
import lead_protection_gates as lpg

def main():
    import rollout_with_replay_opponent as rro
    patch = lpg._load_lp_patch()
    for ep in (111421048, 111653327):
        path = os.path.join(lpg.CORPUS_DEFAULT, f"episode-{ep}-replay.json")
        replay = lpg._load_replay(path)
        row = next(r for r in lpg._parse_corpus_md(lpg.CORPUS_DEFAULT)
                   if r['ep'] == ep)
        me = int(row['me_seat'])
        agent = lpg._fresh_v4b()
        daily = {}
        def wrapped(obs):
            step = obs.get('step', None)
            est = patch.estimate_lead_margin(gc.structify_obs(obs), 0)
            lead = est.get('lead')
            if lead is not None and isinstance(step, (int, float)):
                day = int(step) // 24
                if day not in daily:
                    daily[day] = (float(lead), float(lead))
                else:
                    lo, hi = daily[day]
                    daily[day] = (min(lo, float(lead)), max(hi, float(lead)))
            return agent(gc.structify_obs(obs))
        lpg._replay_stream_run(replay, int(row['peak_day']) * 24, wrapped, me)
        print(f"ep {ep} (peak d{row['peak_day']}, seat {me}):")
        peak_run = None
        for day in sorted(daily):
            lo, hi = daily[day]
            peak_run = hi if peak_run is None or hi > peak_run else peak_run
            dd = peak_run - lo
            mark = ''
            if day >= 15 and lo >= 1500 and dd >= 2000:
                mark = ' <-- arm-A window'
            print(f"  d{day:>2}: lead [{lo:>8.0f}, {hi:>8.0f}] runpeak "
                  f"{peak_run:>8.0f} dd {dd:>7.0f}{mark}")

if __name__ == '__main__':
    main()
