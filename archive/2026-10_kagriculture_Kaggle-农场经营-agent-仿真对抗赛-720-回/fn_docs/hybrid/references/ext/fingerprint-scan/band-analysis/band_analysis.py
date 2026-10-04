#!/usr/bin/env python3
"""band_analysis.py —— 羊系带内梯度 + 三强独特面 + 磁带分叉 + h2h（2026-10-01 band-deepcut）

输入：band-analysis/feats-band.jsonl + feats-renyxin-band.jsonl
输出：band-analysis/band-report.json（全部分析产物）+ 控制台梯度摘要
"""
import json, os, statistics as st
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
FE = os.path.join(HERE, 'feats-band.jsonl')
FE_R = os.path.join(HERE, 'feats-renyxin-band.jsonl')

# 榜分（2026-09-30T17:41:44Z 快照，ext/lb-20261001/）
LB = {
    'Driz Lo': 2625.3, 'THIRD FARM CLUB': 2611.8, 'redblackbst': 2508.5,
    'pensukesan': 2376.4, 'Hello San Francisco': 2236.7, 'kanno': 2111.0,
    'Terry Luo': 2039.8, 'renyxin': 1796.2, 'carlos-tagosaku': 1724.2,
    'アルモンド': 1647.9, 'Thomas Tschinkel': 1379.4,
}
BAND7 = ['Driz Lo', 'THIRD FARM CLUB', 'redblackbst', 'pensukesan',
         'Hello San Francisco', 'kanno', 'Terry Luo']
LOW3 = ['carlos-tagosaku', 'アルモンド', 'Thomas Tschinkel']
ALLT = BAND7 + ['renyxin'] + LOW3
ELITE = ['DECEM', 'M & M & P & Q', 'DSM', 'Vadim Vasilenko', 'mtmr_s1',
         'Smackaveli', 'Azat Akhtyamov', 'Orbital Terraformer', 'Majkel1337',
         'Kaggledew Valley 🏆', '吃白饭的大肥鱼', 'Unknown Mother-Goose']


def load():
    rows = []
    for path, sub_default in [(FE, None), (FE_R, None)]:
        with open(path) as f:
            for line in f:
                r = json.loads(line)
                eid = r['episode_id']
                sub = r.get('sub')
                for pl in r['players']:
                    if pl['team'] not in LB:
                        continue
                    opp = None
                    if len(r['teams']) == 2:
                        if r['teams'].count(pl['team']) == 1:
                            opp = r['teams'][1 - r['teams'].index(pl['team'])]
                    rows.append({
                        'team': pl['team'], 'pl': pl, 'ep': eid,
                        'date': r.get('date'), 'sub': sub,
                        'opp': opp, 'teams': r['teams'],
                        'rewards': r['rewards'],
                    })
    return rows


def sigs(pl):
    sm = ['|'.join(mt) for ft, mt in pl['day0_24'][:8]]
    sf = ['|'.join(ft) for ft, mt in pl['day0_24'][:8]]
    return sm, sf


def spearman(pairs):
    """pairs: [(score, value)] -> (rho, p_approx_n2)。手写 Spearman。"""
    def rank(vs):
        idx = sorted(range(len(vs)), key=lambda i: vs[i])
        r = [0.0] * len(vs)
        i = 0
        while i < len(vs):
            j = i
            while j + 1 < len(vs) and vs[idx[j + 1]] == vs[idx[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[idx[k]] = avg
            i = j + 1
        return r
    xs = [p[0] for p in pairs]; ys = [p[1] for p in pairs]
    if len(set(ys)) < 3:
        return None
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    rho = 1 - 6 * d2 / (n * (n * n - 1))
    return round(rho, 3)


def team_stats(rows, team):
    tr = [x for x in rows if x['team'] == team]
    # Cfinal 口径：renyxin 只用 C_final 局
    if team == 'renyxin':
        tr = [x for x in tr if x['sub'] == 'Cfinal']
    n = len(tr)
    pls = [x['pl'] for x in tr]
    out = {'n': n, 'window': [min(x['date'] for x in tr if x['date']),
                              max(x['date'] for x in tr if x['date'])] if any(x['date'] for x in tr) else None}

    def med(f, flt=None):
        vs = [p[f] for p in pls if p.get(f) is not None and (flt is None or flt(p))]
        return round(st.median(vs), 1) if vs else None

    def mnn(f, flt=None):
        vs = [p[f] for p in pls if p.get(f) is not None and (flt is None or flt(p))]
        return round(st.mean(vs), 2) if vs else None

    # 磁带
    sig_m = [sigs(p)[0] for p in pls]
    sig_f = [sigs(p)[1] for p in pls]
    modal_m = [Counter(s[i] for s in sig_m).most_common(1)[0][0] for i in range(8)]
    modal_f = [Counter(s[i] for s in sig_f).most_common(1)[0][0] for i in range(8)]
    out['modal_m8'] = modal_m
    out['modal_f8'] = modal_f
    # 磁带稳定率（自身）
    out['tape_stab_m'] = round(sum(Counter(s[i] for s in sig_m).most_common(1)[0][1] for i in range(8)) / (8 * n), 3)
    # 三段卖占比（由分日数据重算）
    def thirds(p):
        o = p['sell_orders_per_day']
        e = sum(o[:10]); m_ = sum(o[10:20]); l = sum(o[20:])
        t = e + m_ + l or 1
        return e / t, m_ / t, l / t
    th = [thirds(p) for p in pls]
    out['thirds'] = [round(st.mean(t[i]), 3) for i in range(3) for t in [None]] if False else [
        round(st.mean([t[0] for t in th]), 3), round(st.mean([t[1] for t in th]), 3), round(st.mean([t[2] for t in th]), 3)]
    # 卖流
    out['first_sell_med'] = med('first_sell')
    out['sell_orders_per_day'] = round(mnn('sell_orders') / 30, 2)
    out['sell_qty_mean'] = mnn('sell_qty_mean')
    out['sell_qty_max_med'] = med('sell_qty_max')
    out['sell_vol_med'] = med('sell_vol')
    # 分日节奏（图数据）：逐日平均卖单数
    ndays = max(len(p['sell_orders_per_day']) for p in pls)
    curve_o, curve_q = [], []
    for d in range(ndays):
        curve_o.append(round(st.mean([p['sell_orders_per_day'][d] for p in pls if len(p['sell_orders_per_day']) > d]), 2))
        curve_q.append(round(st.mean([p['sell_qty_per_day'][d] for p in pls if len(p['sell_qty_per_day']) > d]), 1))
    out['sell_orders_day_curve'] = curve_o
    out['sell_qty_day_curve'] = curve_q
    # 分段节奏
    out['rhythm'] = {
        'day0_orders': round(st.mean([p['sell_orders_per_day'][0] for p in pls if p['sell_orders_per_day']]), 2),
        'd1_4_orders': round(st.mean([sum(p['sell_orders_per_day'][1:5]) for p in pls]), 2),
        'd5_9_orders': round(st.mean([sum(p['sell_orders_per_day'][5:10]) for p in pls]), 2),
        'd10_19_orders': round(st.mean([sum(p['sell_orders_per_day'][10:20]) for p in pls]), 2),
        'd20_29_orders': round(st.mean([sum(p['sell_orders_per_day'][20:30]) for p in pls if len(p['sell_orders_per_day']) >= 30]), 2),
        'd20_29_qty': round(st.mean([sum(p['sell_qty_per_day'][20:30]) for p in pls if len(p['sell_qty_per_day']) >= 30]), 1),
    }
    # 买侧 / 建设 / 雇工
    out['bp_orders'] = mnn('bp_orders')
    out['bp_first_med'] = med('bp_first')
    out['buy_seed_first_med'] = med('buy_seed_first') if pls and 'buy_seed_first' in pls[0] else None
    out['first_pasture_med'] = med('first_pasture')
    out['bp_third'] = {k: round(st.mean([p['bp_third'].get(k, 0) for p in pls]), 1) for k in ('early', 'mid', 'late')}
    out['ba_orders'] = mnn('ba_orders')
    out['hire_n'] = mnn('hire_n')
    coop_vs = [p['first_coop'] for p in pls if p['first_coop'] is not None]
    out['coop_pct'] = round(len(coop_vs) / n, 2)
    out['first_coop_med'] = round(st.median(coop_vs), 1) if coop_vs else None
    out['coop_n_med'] = med('coop_n')
    land_first = [min(p['buy_land_steps']) for p in pls if p['buy_land_steps']]
    out['land_pct'] = round(len(land_first) / n, 2)
    out['land_first_med'] = round(st.median(land_first), 1) if land_first else None
    out['land_n_med'] = med('buy_land_n') if pls and 'buy_land_n' in pls[0] else None
    out['land_total'] = round(st.mean([len(p['buy_land_steps']) for p in pls]), 2)
    # 终局段
    out['late'] = {k: round(st.mean([p['late'].get(k, 0) for p in pls]), 1)
                   for k in ('sell_n', 'sell_qty', 'sell_qty_max', 'buyland', 'hire', 'plant', 'harvest')}
    out['last_day'] = {k: round(st.mean([p['last_day'].get(k, 0) for p in pls]), 1)
                       for k in ('sell_n', 'sell_qty')}
    # 钱轨迹
    def m_at(k):
        vs = [p['money_at'].get(str(k)) for p in pls if p['money_at'].get(str(k)) is not None]
        return round(st.median(vs), 0) if vs else None
    out['money_med'] = {str(k): m_at(k) for k in [0, 24, 120, 240, 360, 480, 600, 660, 690, 719]}
    out['reward_med'] = med('reward')
    out['reward_iqr'] = [round(st.quantiles([p['reward'] for p in pls if p['reward'] is not None], n=4)[0], 0),
                         round(st.quantiles([p['reward'] for p in pls if p['reward'] is not None], n=4)[2], 0)] if n >= 4 else None
    # 卖品结构（份额）
    pc = Counter()
    for p in pls:
        for prod, c in p['sell_top_prods']:
            pc[prod] += c
    tot = sum(pc.values()) or 1
    out['sell_mix'] = [[k, v, round(v / tot, 3)] for k, v in pc.most_common(6)]
    # day0 后段（步 8-23）行为标记
    marks = defaultdict(int)
    for p in pls:
        seen = set()
        for ft, mt in p['day0_24'][8:24]:
            for t in ft + mt:
                k = t.split(':')[0] if ':' in t else t
                if t.startswith('PLANT_'): k = 'PLANT:' + t[6:].split(':')[0]
                if t.startswith('BUY_SEED'): k = 'BUY_SEED:' + t.split(':')[1]
                seen.add(k)
        for k in seen:
            marks[k] += 1
    out['day0_s8_23_marks'] = {k: round(v / n, 2) for k, v in sorted(marks.items(), key=lambda kv: -kv[1])[:12]}
    return out


def tape_fork_analysis(rows):
    """对每队：逐步 modal 与我方 C_final modal 的对比 + 分叉内容。"""
    ours = [x for x in rows if x['team'] == 'renyxin' and x['sub'] == 'Cfinal']
    om = team_stats(rows, 'renyxin')
    our_m, our_f = om['modal_m8'], om['modal_f8']
    res = {'our_modal_m8': our_m, 'our_modal_f8': our_f}
    for t in BAND7 + LOW3:
        tr = [x for x in rows if x['team'] == t]
        pls = [x['pl'] for x in tr]
        sig_m = [sigs(p)[0] for p in pls]
        sig_f = [sigs(p)[1] for p in pls]
        entry = {'n': len(pls)}
        # stepwise：team modal vs our modal；team 内各局对 our modal 命中率
        step_eq, step_alt = [], []
        for i in range(8):
            c = Counter(s[i] for s in sig_m)
            cf = Counter(s[i] for s in sig_f)
            tm = c.most_common(1)[0][0]
            tf = cf.most_common(1)[0][0]
            eq_m = (tm == our_m[i])
            eq_f = (tf == our_f[i])
            step_eq.append({'i': i, 'm_eq': eq_m, 'f_eq': eq_f,
                            'team_m': tm, 'team_f': tf,
                            'our_m': our_m[i], 'our_f': our_f[i],
                            'm_modal_hit': round(c.most_common(1)[0][1] / len(pls), 2)})
            # 分叉步上该队的动作分布（市场侧）
            if not eq_m:
                step_alt.append({'i': i, 'team_m_top3': c.most_common(3),
                                 'our_m': our_m[i]})
        entry['steps'] = step_eq
        entry['fork_m_steps'] = [i for i in range(8) if not step_eq[i]['m_eq']]
        entry['fork_f_steps'] = [i for i in range(8) if not step_eq[i]['f_eq']]
        entry['fork_content'] = step_alt
        # 每局逐步命中（市场+农民合并口径）
        hits = []
        for sm, sf in zip(sig_m, sig_f):
            h = sum(1 for i in range(8) if sm[i] == our_m[i]) / 8
            hits.append(h)
        entry['hit_vs_ours_m'] = round(st.mean(hits), 3)
        hits_f = [sum(1 for i in range(8) if sf[i] == our_f[i]) / 8 for sm, sf in zip(sig_m, sig_f)]
        entry['hit_vs_ours_f'] = round(st.mean(hits_f), 3)
        entry['hit_ge7of8'] = round(sum(1 for h in hits if h >= 0.875) / len(hits), 3)
        res[t] = entry
    return res


def h2h(rows, all_index):
    """带内互殴 + 带内 vs 精英队。all_index: ep -> [{'team','reward'},...]（全队）"""
    out = {'band_pairs': defaultdict(list), 'vs_elite': defaultdict(lambda: [0, 0])}
    seen_ep = set()
    for x in rows:
        ep = x['ep']
        if ep in seen_ep:
            continue
        teams = x['teams']
        if len(teams) != 2 or teams[0] == teams[1]:
            continue
        seen_ep.add(ep)
        both = all_index.get(ep, [])
        if len(both) != 2:
            continue
        (t0, r0), (t1, r1) = both
        if r0 is None or r1 is None:
            continue
        key_teams = {t0, t1}
        if key_teams <= (set(LB) | set(ELITE)) and (key_teams & set(LB)):
            w = t0 if r0 > r1 else t1
            l_ = t1 if r0 > r1 else t0
            margin = abs(r0 - r1)
            if key_teams <= set(LB):  # 带内（含低分参照）互殴
                key = tuple(sorted((t0, t1)))
                out['band_pairs'][f'{key[0]}|{key[1]}'].append(
                    {'ep': ep, 'winner': w, 'loser': l_, 'margin': margin,
                     'rw': max(r0, r1), 'rl': min(r0, r1), 'date': x['date']})
            else:  # band vs elite
                bt = next(t for t in key_teams if t in LB)
                et = next(t for t in key_teams if t in ELITE)
                win = (bt == (t0 if r0 > r1 else t1))
                out['vs_elite'][bt][0 if win else 1] += 1
                out['vs_elite'][f'{bt}::{et}'][0 if win else 1] += 1
    return out


def gradient(rows, stats_by_team):
    """参数 vs 榜分 Spearman（11 队）。"""
    params = {}
    keys = [('first_sell_med', 'first_sell_med'), ('sell_orders_per_day', 'sell/day'),
            ('sell_qty_mean', 'qty/order'), ('sell_qty_max_med', 'qty_max'),
            ('bp_orders', 'bp_orders'), ('hire_n', 'hire_n'),
            ('coop_pct', 'coop_pct'), ('first_coop_med', 'first_coop'),
            ('land_total', 'land_n'), ('land_first_med', 'land_first'),
            ('ba_orders', 'ba_orders'), ('reward_med', 'reward_med'),
            ('tape_stab_m', 'tape_stab'), ('hit_vs_ours_m', 'tape_hit_vs_ours')]
    def getv(team_st, k):
        if k == 'hit_vs_ours_m':
            return None  # 单独注入
        return team_st.get(k)
    for k, label in keys:
        pairs = []
        for t in ALLT:
            v = stats_by_team[t].get(k)
            if k == 'hit_vs_ours_m':
                continue
            if v is not None:
                pairs.append((LB[t], v))
        params[label] = {'spearman': spearman(pairs), 'n': len(pairs)}
    # 三段占比与 money 检查点
    for idx, nm in [(0, 'third_early'), (1, 'third_mid'), (2, 'third_late')]:
        pairs = [(LB[t], stats_by_team[t]['thirds'][idx]) for t in ALLT]
        params[nm] = {'spearman': spearman(pairs), 'n': len(pairs)}
    for k in ['240', '480', '600', '660', '690', '719']:
        pairs = [(LB[t], stats_by_team[t]['money_med'][k]) for t in ALLT
                 if stats_by_team[t]['money_med'][k] is not None]
        params[f'money@{k}'] = {'spearman': spearman(pairs), 'n': len(pairs)}
    for k in ('sell_n', 'sell_qty', 'sell_qty_max', 'buyland', 'hire'):
        pairs = [(LB[t], stats_by_team[t]['late'][k]) for t in ALLT]
        params[f'late_{k}'] = {'spearman': spearman(pairs), 'n': len(pairs)}
    # 后段增益：719-480
    pairs = [(LB[t], (stats_by_team[t]['money_med']['719'] or 0) - (stats_by_team[t]['money_med']['480'] or 0)) for t in ALLT]
    params['gain_480_719'] = {'spearman': spearman(pairs), 'n': len(pairs)}
    # tape hit vs ours（7 band + 3 low，不含 renyxin 自身）
    if 'hit_vs_ours_m' in {k for k, _ in keys} or True:
        pairs = [(LB[t], stats_by_team[t]['hit_vs_ours_m']) for t in BAND7 + LOW3
                 if stats_by_team[t].get('hit_vs_ours_m') is not None]
        params['tape_hit_vs_ours'] = {'spearman': spearman(pairs), 'n': len(pairs)}
    return params


def drift_check(rows):
    """队内前后半窗参数对比（版本漂移检查）。"""
    out = {}
    for t in BAND7:
        tr = [x for x in rows if x['team'] == t]
        tr = [x for x in tr if x['date']]
        tr.sort(key=lambda x: (x['date'], x['ep']))
        if len(tr) < 10:
            continue
        half = len(tr) // 2
        def half_stats(sub):
            pls = [x['pl'] for x in sub]
            return {
                'n': len(pls),
                'window': [sub[0]['date'], sub[-1]['date']],
                'first_sell_med': st.median([p['first_sell'] for p in pls if p['first_sell'] is not None]) if any(p['first_sell'] is not None for p in pls) else None,
                'sell_qty_mean': round(st.mean([p['sell_qty_mean'] for p in pls]), 1),
                'sell_orders_per_day': round(st.mean([p['sell_orders'] for p in pls]) / 30, 1),
                'coop_pct': round(sum(1 for p in pls if p['first_coop'] is not None) / len(pls), 2),
                'bp_orders': round(st.mean([p['bp_orders'] for p in pls]), 1),
                'reward_med': st.median([p['reward'] for p in pls if p['reward'] is not None]),
            }
        out[t] = {'early_half': half_stats(tr[:half]), 'late_half': half_stats(tr[half:])}
    return out


def main():
    rows = load()
    print('loaded player-rows:', len(rows))
    # 全队索引（h2h 用）
    all_index = defaultdict(list)
    for path in (FE, FE_R):
        with open(path) as f:
            for line in f:
                r = json.loads(line)
                if len(r['teams']) == 2:
                    all_index[r['episode_id']] = list(zip(r['teams'], r['rewards']))
    stats_by_team = {t: team_stats(rows, t) for t in ALLT}
    fork = tape_fork_analysis(rows)
    # tape hit vs ours 注入 gradient
    for t in BAND7 + LOW3:
        stats_by_team[t]['hit_vs_ours_m'] = fork[t]['hit_vs_ours_m']
    params = gradient(rows, stats_by_team)
    h = h2h(rows, all_index)
    drift = drift_check(rows)

    report = {
        'lb_scores': LB,
        'team_stats': stats_by_team,
        'gradient_spearman': params,
        'tape_fork': fork,
        'h2h': {k: v for k, v in h['band_pairs'].items()},
        'vs_elite': {k: {'w': v[0], 'l': v[1]} for k, v in h['vs_elite'].items()},
        'drift': drift,
    }
    with open(os.path.join(HERE, 'band-report.json'), 'w') as f:
        json.dump(report, f, indent=1, ensure_ascii=False)

    # 控制台梯度表
    hdr = f"{'team':22s}{'lb':>7s}{'n':>5s}{'fsell':>6s}{'s/d':>6s}{'qty':>6s}{'e/m/l':>15s}{'bp':>7s}{'coop%':>7s}{'cstep':>7s}{'land':>6s}{'Rmed':>9s}{'hit8':>7s}"
    print(hdr)
    for t in sorted(ALLT, key=lambda t: -LB[t]):
        s = stats_by_team[t]
        hit = s.get('hit_vs_ours_m')
        print(f"{t[:22]:22s}{LB[t]:>7.1f}{s['n']:>5d}{str(s['first_sell_med']):>6s}"
              f"{s['sell_orders_per_day']:>6.1f}{s['sell_qty_mean']:>6.1f}"
              f"{s['thirds'][0]:>5.2f}/{s['thirds'][1]:.2f}/{s['thirds'][2]:.2f}"
              f"{s['bp_orders']:>7.1f}{s['coop_pct']:>7.2f}{str(s['first_coop_med']):>7s}"
              f"{s['land_total']:>6.1f}{s['reward_med']:>9.0f}{str(hit):>7s}")
    print('\nSpearman vs LB score:')
    for k, v in sorted(params.items(), key=lambda kv: -(abs(kv[1]['spearman']) if kv[1]['spearman'] is not None else 0)):
        print(f"  {k:18s} rho={v['spearman']}  n={v['n']}")
    print('\nh2h pairs:')
    for k, v in sorted(h['band_pairs'].items()):
        wins = Counter(g['winner'] for g in v)
        marg = [g['margin'] for g in v]
        print(f"  {k}: n={len(v)} wins={dict(wins)} margin_med={st.median(marg):.0f}")
    print('\nvs elite:')
    for k, v in sorted(h['vs_elite'].items()):
        if '::' not in k:
            print(f"  {k}: W{v[0]} L{v[1]}")
    print('\ndrift (early vs late half):')
    for t, d in drift.items():
        e, l = d['early_half'], d['late_half']
        print(f"  {t}: [{e['window']}]->[{l['window']}] fsell {e['first_sell_med']}->{l['first_sell_med']} "
              f"qty {e['sell_qty_mean']}->{l['sell_qty_mean']} s/d {e['sell_orders_per_day']}->{l['sell_orders_per_day']} "
              f"coop {e['coop_pct']}->{l['coop_pct']} R {e['reward_med']:.0f}->{l['reward_med']:.0f}")


if __name__ == '__main__':
    main()
