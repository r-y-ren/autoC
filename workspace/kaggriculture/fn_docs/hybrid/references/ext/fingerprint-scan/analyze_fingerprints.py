#!/usr/bin/env python3
"""analyze_fingerprints.py —— 指纹聚合与对比（2026-10-01 fingerprint-scan）

输入：feats-*.jsonl（fingerprint_scan.py 产物）
输出：teams_report.json + 控制台摘要。

指标：
  tape_stab_m / tape_stab_f：day0 前 8 步市场/农民序列"逐步众数稳定率"
    （每步取该队所有局中最常见的规范化 token 串，计算各局命中该众数的比例，再对 8 步平均）
  modal_sig_m8：市场磁带众数签名（逐步众数串拼接）
  sell / buy 聚合：中位数与均值。
  vs 我方 C_final：market-tape 逐步命中率、day0 签名相等率、卖流画像距离。
"""
import json, sys, glob, statistics as st
from collections import defaultdict, Counter

def load(paths):
    recs = []
    for p in paths:
        with open(p) as f:
            for line in f:
                recs.append(json.loads(line))
    return recs

def step_tokens_sig(day0_8):
    """day0_8（8 步 × [ft, mt]）→ (市场 sig 列表, 农民 sig 列表)"""
    sig_m, sig_f = [], []
    for ft, mt in day0_8:
        sig_m.append('|'.join(mt))
        sig_f.append('|'.join(ft))
    return sig_m, sig_f

def main():
    feats_files = sys.argv[1:-1]
    out_path = sys.argv[-1]
    recs = load(feats_files)
    print('episodes loaded:', len(recs))

    # 聚合：team -> list of player-records
    team_players = defaultdict(list)
    ep_of = {}
    for r in recs:
        for pl in r['players']:
            ep_of[id(pl)] = (r.get('episode_id'), r.get('seed'), pl['pi'])
            team_players[pl['team']].append(pl)

    teams_report = {}
    for team, pls in team_players.items():
        # 每局只留一份（episode_id, pi 唯一）
        seen = set(); uniq = []
        for pl in pls:
            key = ep_of[id(pl)]
            if key in seen: continue
            seen.add(key); uniq.append(pl)
        n = len(uniq)
        # 磁带稳定率
        sigs_m, sigs_f = [], []
        for pl in uniq:
            sig_m, sig_f = step_tokens_sig(pl['day0_8'])
            sigs_m.append(sig_m); sigs_f.append(sig_f)
        def step_modal_stability(sigs):
            if not sigs: return None
            k = len(sigs[0])
            stabs = []
            for i in range(k):
                c = Counter(s[i] for s in sigs)
                top, cnt = c.most_common(1)[0]
                stabs.append(cnt / len(sigs))
            return round(sum(stabs) / k, 4)
        tape_m = step_modal_stability(sigs_m)
        tape_f = step_modal_stability(sigs_f)
        # 众数签名
        modal_m8 = None
        if sigs_m:
            modal_m8 = []
            k = len(sigs_m[0])
            for i in range(k):
                modal_m8.append(Counter(s[i] for s in sigs_m).most_common(1)[0][0])
        modal_f8 = []
        if sigs_f:
            k = len(sigs_f[0])
            for i in range(k):
                modal_f8.append(Counter(s[i] for s in sigs_f).most_common(1)[0][0])
        def med(field, flt=lambda x: x is not None):
            vals = [pl[field] for pl in uniq if flt(pl[field])]
            return round(st.median(vals), 1) if vals else None
        def mean(field, flt=lambda x: x is not None):
            vals = [pl[field] for pl in uniq if flt(pl[field])]
            return round(st.mean(vals), 2) if vals else None
        teams_report[team] = {
            'n_eps': n,
            'tape_stab_m': tape_m, 'tape_stab_f': tape_f,
            'modal_m8': modal_m8, 'modal_f8': modal_f8,
            'first_sell_med': med('first_sell'),
            'sell_qty_mean_avg': mean('sell_qty_mean'),
            'sell_orders_avg': mean('sell_orders'),
            'sell_orders_per_day': round(mean('sell_orders') / 30, 2) if mean('sell_orders') is not None else None,
            'sell_third_early': None,  # 填充见下
            'sell_third_mid': None, 'sell_third_late': None,
            'sell_top_prods': None,
            'bp_orders_avg': mean('bp_orders'), 'bp_first_med': med('bp_first'),
            'ba_first_med': med('ba_first'),
            'first_coop_med': med('first_coop'), 'first_pasture_med': med('first_pasture'),
            'first_hire_med': med('first_hire'), 'hire_n_avg': mean('hire_n'),
            'buy_land_first_med': None,
            'buy_seed_first_med': med('buy_seed_first'),
            'plant_top': None,
        }
        # 三段占比均值
        for key, fld in [('sell_third_early', 'early'), ('sell_third_mid', 'mid'), ('sell_third_late', 'late')]:
            vals = [pl['sell_third'].get(fld) for pl in uniq if pl.get('sell_third') and pl['sell_third'].get(fld) is not None]
            teams_report[team][key] = round(st.mean(vals), 3) if vals else None
        # 品类 Top（按局聚合）
        pc = Counter()
        for pl in uniq:
            for prod, c in pl['sell_top_prods']:
                pc[prod] += c
        teams_report[team]['sell_top_prods'] = pc.most_common(6)
        pc2 = Counter()
        for pl in uniq:
            for prod, c in pl['plant_top']:
                pc2[prod] += c
        teams_report[team]['plant_top'] = pc2.most_common(6)
        # buy_land 首步
        vals = [min(pl['buy_land_steps']) for pl in uniq if pl['buy_land_steps']]
        teams_report[team]['buy_land_first_med'] = round(st.median(vals), 1) if vals else None
        # 磁带众数命中率（用众数签名对每局逐步比对）
        if sigs_m and modal_m8:
            hits = [sum(1 for i in range(len(s)) if s[i] == modal_m8[i]) / len(s) for s in sigs_m]
            teams_report[team]['modal_hit_m'] = round(st.mean(hits), 4)

    # 胜率（episode 级）
    winrate = defaultdict(lambda: [0, 0])
    for r in recs:
        pls = r['players']
        if len(pls) == 2 and pls[0]['reward'] is not None and pls[1]['reward'] is not None:
            a, b = pls
            if a['reward'] > b['reward']: winrate[a['team']][0] += 1; winrate[b['team']][1] += 1
            elif b['reward'] > a['reward']: winrate[b['team']][0] += 1; winrate[a['team']][1] += 1
    for team, (w, l) in winrate.items():
        if team in teams_report:
            teams_report[team]['wins'] = w; teams_report[team]['losses'] = l
            teams_report[team]['winrate'] = round(w / (w + l), 3) if w + l else None

    with open(out_path, 'w') as f:
        json.dump(teams_report, f, indent=1, ensure_ascii=False)
    print('teams:', len(teams_report), '->', out_path)
    # 控制台摘要（目标队）
    for t in ['Majkel1337', 'mtmr_s1', 'Alperen Aydın', 'SpaTaro', 'DECEM', 'tetsu2131', 'shiiin9', 'renyxin']:
        if t in teams_report:
            r = teams_report[t]
            print(f"{t}: n={r['n_eps']} tape_m={r['tape_stab_m']} tape_f={r['tape_stab_f']} "
                  f"first_sell={r['first_sell_med']} qty={r['sell_qty_mean_avg']} "
                  f"3rd(e/m/l)={r['sell_third_early']}/{r['sell_third_mid']}/{r['sell_third_late']} "
                  f"bp={r['bp_orders_avg']} coop={r['first_coop_med']} wr={r.get('winrate')}")

if __name__ == '__main__':
    main()
