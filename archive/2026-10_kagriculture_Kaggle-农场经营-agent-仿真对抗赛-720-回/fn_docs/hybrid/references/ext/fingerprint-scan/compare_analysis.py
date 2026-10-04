#!/usr/bin/env python3
"""compare_analysis.py —— 时间窗指纹对比 + C_final/S8 拆分 + 磁带签名对照（2026-10-01）"""
import json, sys, glob, csv, statistics as st
from collections import defaultdict, Counter
import orjson

BASE = '/mnt/data/Code/autoC/workspace/kaggriculture/fn_docs/hybrid/references/ext/fingerprint-scan'

def load(paths):
    recs = []
    for p in paths:
        with open(p) as f:
            for line in f:
                recs.append(orjson.loads(line))
    return recs

# episode -> date（ashok 用 episodes.parquet；其他源固定）
def build_date_map():
    import pandas as pd
    e = pd.read_parquet(f'{BASE}/raw/ashok205-meta/episodes.parquet')
    m = {}
    for eid, date in zip(e['episode_id'], e['date']):
        m[int(eid)] = str(date)
    return m

def main():
    feats = sys.argv[1]
    out = sys.argv[2]
    recs = load([feats] if '*' not in feats else sorted(glob.glob(feats)))
    dmap = build_date_map()
    # Cfinal / S8 episode id 集（CSV 尾部混入 CLI 提示行，只取数字行）
    def _ids(path):
        out = set()
        for line in open(path):
            head = line.split(',', 1)[0].strip()
            if head.isdigit(): out.add(int(head))
        return out
    c_ids = _ids(f'{BASE}/raw/episodes-Cfinal-56697824.csv')
    s_ids = _ids(f'{BASE}/raw/episodes-S8-56708866.csv')

    # 收集 (team, sub, date, player)
    rows = []
    for r in recs:
        eid = r.get('episode_id')
        date = dmap.get(eid, '2026-09-28' if r.get('src') == 'unzipped' else None)
        if eid in c_ids and eid in s_ids:
            sub = 'BOTH'
        elif eid in c_ids:
            sub = 'Cfinal'
        elif eid in s_ids:
            sub = 'S8'
        else:
            sub = None
        for pl in r['players']:
            rows.append({'team': pl['team'], 'sub': sub, 'date': date,
                         'ep': eid, 'pl': pl, 'teams': r['teams'],
                         'opp': r['teams'][1 - r['teams'].index(pl['team'])] if len(r['teams']) == 2 and r['teams'].count(pl['team']) == 1 else None})

    def stats(plies, label):
        if not plies: return None
        sigs_m = []; sigs_f = []
        for pl in plies:
            sm = ['|'.join(mt) for ft, mt in pl['day0_8']]
            sf = ['|'.join(ft) for ft, mt in pl['day0_8']]
            sigs_m.append(sm); sigs_f.append(sf)
        def stability(sigs):
            k = 8
            stabs = []
            for i in range(k):
                c = Counter(s[i] for s in sigs)
                stabs.append(c.most_common(1)[0][1] / len(sigs))
            return round(sum(stabs) / k, 4)
        modal_m = []
        for i in range(8):
            modal_m.append(Counter(s[i] for s in sigs_m).most_common(1)[0][0])
        def med(f):
            vs = [pl[f] for pl in plies if pl[f] is not None]
            return round(st.median(vs), 1) if vs else None
        def mnn(f):
            vs = [pl[f] for pl in plies if pl[f] is not None]
            return round(st.mean(vs), 2) if vs else None
        thirds = {k: round(st.mean([pl['sell_third'][k] for pl in plies if pl.get('sell_third', {}).get(k) is not None]), 3)
                  for k in ('early', 'mid', 'late')}
        prods = Counter()
        for pl in plies:
            for p_, c_ in pl['sell_top_prods']: prods[p_] += c_
        return {
            'label': label, 'n': len(plies),
            'tape_m': stability(sigs_m), 'tape_f': stability(sigs_f),
            'modal_m8': modal_m,
            'first_sell_med': med('first_sell'), 'sell_qty_mean': mnn('sell_qty_mean'),
            'sell_orders_avg': mnn('sell_orders'),
            'thirds': thirds, 'sell_top': prods.most_common(5),
            'bp_orders_avg': mnn('bp_orders'), 'bp_first_med': med('bp_first'),
            'ba_first_med': med('ba_first'), 'first_coop_med': med('first_coop'),
            'first_coop_p25': (lambda vs: round(sorted(vs)[len(vs)//4], 1) if vs else None)(
                [pl['first_coop'] for pl in plies if pl['first_coop'] is not None]),
            'first_pasture_med': med('first_pasture'),
            'first_hire_med': med('first_hire'), 'hire_n_avg': mnn('hire_n'),
            'buy_seed_first_med': med('buy_seed_first'),
            'land_first_med': (lambda vs: round(st.median(vs), 1) if vs else None)(
                [min(pl['buy_land_steps']) for pl in plies if pl['buy_land_steps']]),
        }

    report = {}
    # 目标队 × {全期, 近窗(>=09-19)}
    TARGETS = ['Majkel1337', 'mtmr_s1', 'Alperen Aydın', 'SpaTaro', 'DECEM',
               'tetsu2131', 'shiiin9', 'renyxin', 'DSM', 'Unknown Mother-Goose', 'Boey',
               'ymg_aq', 'Crop Dusta', 'THIRD FARM CLUB', '吃白饭的大肥鱼', 'Fourth Quadrant',
               'M & M & P & Q', 'Vadim Vasilenko', 'KawattaTaido', 'tetsuya & yuanzhe & guoqi',
               'Victor @ Tufa Labs', 'Victor Mercklé @ Tufa Labs']
    for t in TARGETS:
        tr = [x for x in rows if x['team'] == t]
        if not tr: continue
        rep = {}
        rep['all'] = stats([x['pl'] for x in tr], f'{t}:all(n={len(tr)})')
        rec7 = [x for x in tr if x['date'] and x['date'] >= '2026-09-19']
        if len(rec7) >= 8:
            rep['recent7d'] = stats([x['pl'] for x in rec7], f'{t}:recent7d(n={len(rec7)})')
        report[t] = rep

    # renyxin 按 sub 拆
    for sub in ('Cfinal', 'S8'):
        tr = [x for x in rows if x['team'] == 'renyxin' and x['sub'] == sub]
        if tr:
            report[f'renyxin[{sub}]'] = {'all': stats([x['pl'] for x in tr], f'renyxin[{sub}](n={len(tr)})')}

    # 签名对照：C_final modal vs 各队 modal（逐步相等率）+ 各队局对我方 modal 的命中率
    cf = report.get('renyxin[Cfinal]', {}).get('all') or report.get('renyxin', {}).get('all')
    if cf:
        cf_modal = cf['modal_m8']
        sig_match = {}
        for t in TARGETS:
            tr = [x for x in rows if x['team'] == t]
            if not tr: continue
            rec7 = [x for x in tr if x['date'] and x['date'] >= '2026-09-19']
            use = rec7 if len(rec7) >= 8 else tr
            hits = []
            for x in use:
                sm = ['|'.join(mt) for ft, mt in x['pl']['day0_8']]
                hits.append(sum(1 for i in range(8) if sm[i] == cf_modal[i]) / 8)
            other = report.get(t, {}).get('recent7d') or report.get(t, {}).get('all')
            om = other['modal_m8'] if other else None
            modal_eq = sum(1 for i in range(8) if om and om[i] == cf_modal[i]) / 8 if om else None
            sig_match[t] = {
                'mean_hit_vs_cf_modal': round(st.mean(hits), 4),
                'frac_eps_ge7of8': round(sum(1 for h in hits if h >= 0.875) / len(hits), 4),
                'modal_vs_cf_modal_step_eq': round(modal_eq, 4) if modal_eq is not None else None,
                'n': len(hits),
            }
        report['_sig_vs_Cfinal'] = sig_match

    with open(out, 'w') as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
    print('written', out)

    # 控制台
    print(f"\n{'team':28s} {'win':5s} tape_m tape_f  1st_sell qty   e/m/l      bp    modal_eq_cf")
    for t in TARGETS + ['renyxin[Cfinal]', 'renyxin[S8]']:
        if t not in report: continue
        r = report[t].get('recent7d') or report[t]['all']
        s = report.get('_sig_vs_Cfinal', {}).get(t, {})
        print(f"{t:28s} {r['n']:<5d} {r['tape_m']:<6.3f} {r['tape_f']:<6.3f} "
              f"{str(r['first_sell_med']):>6s} {str(r['sell_qty_mean']):>6.6s} "
              f"{r['thirds']['early']:.2f}/{r['thirds']['mid']:.2f}/{r['thirds']['late']:.2f} "
              f"{str(r['bp_orders_avg']):>6.6s} {str(s.get('modal_vs_cf_modal_step_eq')):>8s}")

if __name__ == '__main__':
    main()
