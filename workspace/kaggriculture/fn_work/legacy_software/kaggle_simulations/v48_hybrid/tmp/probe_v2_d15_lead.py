# -*- coding: utf-8 -*-
# 临时探针（R8-v2 F5）：对照臂重演，测 d15+ 帧的最大 lead——判定 form=0 局
# 的失配门（lead<1500 vs 回撤<2000）。产物：stdout 摘要。
import json, os, sys
sys.path.insert(0, 'gates')
import gate_common as gc
import lead_protection_gates as lpg

def main():
    import rollout_with_replay_opponent as rro
    patch = lpg._load_lp_patch()
    table = lpg._parse_corpus_md(lpg.CORPUS_DEFAULT)
    print(f"{'ep':>10} {'pk_d':>4} {'maxL_d15+':>10} {'maxL_all':>9}")
    for row in table:
        path = os.path.join(lpg.CORPUS_DEFAULT,
                            f"episode-{row['ep']}-replay.json")
        replay = lpg._load_replay(path)
        me = int(row['me_seat'])
        agent = lpg._fresh_v4b()
        box = {'l15': None, 'la': None}
        def wrapped(obs):
            step = obs.get('step', None)
            est = patch.estimate_lead_margin(gc.structify_obs(obs), 0)
            lead = est.get('lead')
            if lead is not None:
                if box['la'] is None or lead > box['la']:
                    box['la'] = lead
                day = (int(step) // 24
                       if isinstance(step, (int, float)) else None)
                if day is not None and day >= 15 and (
                        box['l15'] is None or lead > box['l15']):
                    box['l15'] = lead
            return agent(gc.structify_obs(obs))
        lpg._replay_stream_run(replay, int(row['peak_day']) * 24, wrapped, me)
        m15 = f"{box['l15']:.0f}" if box['l15'] is not None else "n/a"
        print(f"{row['ep']:>10} {row['peak_day']:>4} {m15:>10} "
              f"{box['la'] if box['la'] is not None else float('nan'):>9.0f}")

if __name__ == '__main__':
    main()
