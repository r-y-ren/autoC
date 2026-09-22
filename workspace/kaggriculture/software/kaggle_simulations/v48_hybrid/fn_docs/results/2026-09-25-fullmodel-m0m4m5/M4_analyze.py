#!/usr/bin/env python3
"""M4 analysis: winner template vs tape baseline, crossover days, tiers."""
import json, glob, statistics as st

DAYS = 30
LEAD_IDS = set()
for p in glob.glob('/mnt/data/Code/autoC/workspace/kaggriculture/software/kaggle_simulations/v48_hybrid/fn_docs/results/replays-lead-collapse/episode-*-replay.json'):
    LEAD_IDS.add(int(p.rsplit('/',1)[1].replace('episode-','').replace('-replay.json','')))

def q(vals, p):
    v = sorted(x for x in vals if x is not None)
    if not v: return None
    i = min(len(v)-1, max(0, int(round(p*(len(v)-1)))))
    return v[i]

def med(vals): return q(vals, 0.5)
def dist(vals):
    """small integer distribution dict"""
    d = {}
    for v in vals:
        if v is not None: d[v] = d.get(v, 0) + 1
    return d

games = json.load(open('/tmp/fullmodel/M4/all_games.json'))

def seat_metrics(s):
    m = {}
    m['team'] = s['team']; m['final'] = s['reward']
    m['quad_day'] = dict(s['quad_day'])
    m['n_quad_at'] = {d: len([q for q, dd in s['quad_day'].items() if dd <= d]) for d in (5,10,15,20,25,29)}
    herd_tot = [sum((s['herd_day'][d] or {}).values()) for d in range(DAYS)]
    m['herd_at'] = {d: (s['herd_day'][d] or {}) for d in (5,10,15,20,25,29)}
    m['herd_tot_at'] = {d: herd_tot[d] for d in (5,10,15,20,25,29)}
    m['herd_peak'] = max(herd_tot); m['herd_peak_day'] = herd_tot.index(max(herd_tot))
    m['herd_final'] = herd_tot[29]
    peak_day = m['herd_peak_day']
    m['herd_peak_mix'] = s['herd_day'][peak_day] or {}
    m['buys_total'] = {}
    for d in range(DAYS):
        for a, n in s['animal_buys_day'][d].items():
            m['buys_total'][a] = m['buys_total'].get(a, 0) + n
    m['hires_at'] = {d: s['hires_day'][d] for d in (5,10,15,20,25,29)}
    m['hires_peak'] = max(s['hires_day']); m['hires_total'] = sum(s['hires_day'])
    m['builds_at'] = {d: s['cum_builds'][d] for d in (10,15,20,25,29)}
    m['income_at'] = {d: s['income_total_day'][d] for d in (5,10,15,20,25,29)}
    m['income_peak'] = max(s['income_total_day'])
    m['income_peak_day'] = s['income_total_day'].index(m['income_peak'])
    m['income_cum_final'] = s['income_cum'][29]
    lines = {k: 0.0 for k in ('crops','dairy','wool','eggs','fertilizer')}
    for d in range(DAYS):
        for k, v in s['income_line_day'][d].items():
            lines[k] = lines.get(k, 0) + v
    tot = sum(lines.values()) or 1
    m['income_line_share'] = {k: round(v/tot, 3) for k, v in lines.items()}
    m['endgame_dump_share'] = round((s['income_total_day'][28] + s['income_total_day'][29]) / tot, 3)
    m['buy_wheat_total'] = sum(s['buy_wheat_day'])
    m['feed_total'] = sum(s['feed_day'])
    m['buy_wheat_days'] = sum(1 for x in s['buy_wheat_day'] if x > 0)
    m['ext_feed_ratio'] = round(m['buy_wheat_total'] / max(1, m['feed_total']), 3)
    m['spend_total'] = {}
    for d in range(DAYS):
        for k, v in s['spend'][d].items():
            m['spend_total'][k] = m['spend_total'].get(k, 0) + v
    m['money_at'] = {d: s['money_end'][d] for d in (6,10,13,16,20,24,29)}
    return m

def cede_lock(ours_m, win_m):
    """margin = our money - winner money (day-end). cede: first day margin<0
    and never positive again. lock: first day |margin| >= 50% |final margin|."""
    margin = [(ours_m['money_at_day'][d] if False else None) for d in range(0)]
    return margin

rows = []
for g in games:
    r0, r1 = g['rewards']
    if r0 is None or r1 is None: continue
    if g['teams'][0] == g['teams'][1]:   # mirror
        continue
    winner = 0 if r0 > r1 else 1
    ours = 1 - winner if 'renyxin' in g['teams'] else None
    if ours is None: continue
    w, o = g['seats'][winner], g['seats'][ours]
    # margin curve
    margin = [ (o['money_end'][d] or 0) - (w['money_end'][d] or 0) for d in range(DAYS)]
    fin = margin[29]
    cede = None
    for d in range(DAYS):
        if margin[d] < 0 and all(margin[x] < 0 for x in range(d, DAYS)):
            cede = d; break
    lock = None
    if fin != 0:
        for d in range(DAYS):
            if abs(margin[d]) >= 0.5*abs(fin): lock = d; break
    # income crossover
    inc_w, inc_o = w['income_total_day'], o['income_total_day']
    cum_w, cum_o = w['income_cum'], o['income_cum']
    first_cross = next((d for d in range(DAYS) if inc_w[d] > inc_o[d]), None)
    sustain = None
    for d in range(DAYS):
        if all(cum_w[x] >= cum_o[x] for x in range(d, DAYS)) and cum_w[d] > cum_o[d]:
            sustain = d; break
    # income lead above 1k/day sustained 3d
    strong = None
    for d in range(DAYS-3):
        if all(inc_w[x] - inc_o[x] > 500 for x in (d, d+1, d+2)):
            strong = d; break
    rows.append({
        'ep': g['episode_id'], 'r26': '/r26full/' in g['source'],
        'lead_collapse': g['episode_id'] in LEAD_IDS,
        'winner_team': w['team'], 'our_seat': ours, 'winner_seat': winner,
        'our_final': o['reward'], 'winner_final': w['reward'],
        'tier': 'giant' if w['reward'] >= 85000 else ('mid' if w['reward'] >= 60000 else 'low'),
        'outcome': 'L',  # our seat lost (winner defined)
        'cede_day': cede, 'lock_day': lock,
        'inc_first_cross': first_cross, 'inc_sustain_day': sustain, 'inc_strong_day': strong,
        'winner': seat_metrics(w), 'ours': seat_metrics(o),
        'gap': {
            d: {
                'herd': sum((w['herd_day'][d] or {}).values()) - sum((o['herd_day'][d] or {}).values()),
                'quads': len(w['quad_day']) - len([q for q, dd in o['quad_day'].items() if dd <= d]) if False else (sum(1 for _, dd in w['quad_day'].items() if dd <= d) - sum(1 for _, dd in o['quad_day'].items() if dd <= d)),
                'hires': w['hires_day'][d] - o['hires_day'][d],
                'income': round(w['income_total_day'][d] - o['income_total_day'][d], 1),
                'cum_income': round(w['income_cum'][d] - o['income_cum'][d], 1),
                'money': round((w['money_end'][d] or 0) - (o['money_end'][d] or 0), 1),
            } for d in (10, 15, 20, 25)
        },
    })

# wins for renyxin: winner seat is renyxin
wins = []
for g in games:
    r0, r1 = g['rewards']
    if r0 is None or r1 is None or g['teams'][0] == g['teams'][1]: continue
    if 'renyxin' not in g['teams']: continue
    if (r0 > r1) == (g['teams'][0] == 'renyxin'):
        winner = 0 if r0 > r1 else 1
        wins.append({'ep': g['episode_id'], 'r26': '/r26full/' in g['source'],
                     'winner_final': g['rewards'][winner],
                     'winner': seat_metrics(g['seats'][winner])})

def agg(list_of_metrics, keys=None):
    out = {}
    def collect(f):
        return [f(m) for m in list_of_metrics]
    out['n'] = len(list_of_metrics)
    for key in ('herd_peak','herd_peak_day','herd_final','hires_peak','hires_total',
                'income_peak','income_peak_day','income_cum_final','ext_feed_ratio',
                'buy_wheat_total','buy_wheat_days','endgame_dump_share'):
        vals = [m[key] for m in list_of_metrics]
        out[key] = {'med': med(vals), 'p25': q(vals,0.25), 'p75': q(vals,0.75),
                    'min': min(vals), 'max': max(vals)}
    for key in ('NE','SW','SE'):
        vals = [m['quad_day'].get(key) for m in list_of_metrics]
        vals = [v for v in vals if v is not None]
        out['quad_day_'+key] = {'seen': len(vals), 'med': med(vals), 'p25': q(vals,0.25), 'p75': q(vals,0.75),
                                'dist': dist(vals)} if vals else {'seen': 0}
    for d in (10,15,20,25,29):
        out[f'herd_tot_d{d}'] = med([m['herd_tot_at'][d] for m in list_of_metrics])
        out[f'n_quad_d{d}'] = med([m['n_quad_at'][d] for m in list_of_metrics])
        out[f'hires_d{d}'] = med([m['hires_at'][d] for m in list_of_metrics])
        out[f'income_d{d}'] = med([m['income_at'][d] for m in list_of_metrics])
        out[f'builds_d{d}'] = med([sum(m['builds_at'].get(d, {}).values()) for m in list_of_metrics])
    # herd mix at peak day: aggregate sheep/cow/goose
    mix = {'SHEEP': [], 'COW': [], 'GOOSE': []}
    for m in list_of_metrics:
        for k in mix:
            mix[k].append(m['herd_peak_mix'].get(k, 0))
    out['peak_mix_med'] = {k: med(v) for k, v in mix.items()}
    buys = {'SHEEP': [], 'COW': [], 'GOOSE': []}
    for m in list_of_metrics:
        for k in buys: buys[k].append(m['buys_total'].get(k, 0))
    out['buys_total_med'] = {k: med(v) for k, v in buys.items()}
    ls = {'crops': [], 'dairy': [], 'wool': [], 'eggs': [], 'fertilizer': []}
    for m in list_of_metrics:
        for k in ls: ls[k].append(m['income_line_share'].get(k, 0))
    out['line_share_med'] = {k: round(st.mean(v),3) for k, v in ls.items()}
    sp = {'animals': [], 'seeds': [], 'hire': [], 'land': [], 'feed_wheat': []}
    for m in list_of_metrics:
        for k in sp: sp[k].append(m['spend_total'].get(k, 0))
    out['spend_med'] = {k: round(med(v)) for k, v in sp.items()}
    return out

out = {
    'meta': {
        'games': len(games), 'loss_rows': len(rows), 'our_wins': len(wins),
        'lead_collapse_games': len([r for r in rows if r['lead_collapse']]),
        'identity': 'income-spend == dmoney for 7250/7250 day-pairs; sim drift 0 on 125/125',
    },
    'winner_template_all': agg([r['winner'] for r in rows]),
    'tape_baseline_all': agg([r['ours'] for r in rows]),
    'by_tier': {},
    'crossover': {},
    'gap_tables': {},
    'per_game': rows,
    'our_win_templates': agg([w['winner'] for w in wins]) if wins else None,
}

for tier in ('giant','mid','low'):
    sel = [r['winner'] for r in rows if r['tier'] == tier]
    selo = [r['ours'] for r in rows if r['tier'] == tier]
    if sel:
        out['by_tier'][tier] = {'n': len(sel), 'winner': agg(sel)}
        out['by_tier'][tier]['ours'] = agg(selo)

# crossover distributions
for key in ('inc_first_cross','inc_sustain_day','inc_strong_day','cede_day','lock_day'):
    vals = [r[key] for r in rows if r[key] is not None]
    out['crossover'][key] = {'n': len(vals), 'med': med(vals), 'dist': dist(vals)}

# gap tables
for tier in (None,'giant','mid','low'):
    sel = rows if tier is None else [r for r in rows if r['tier']==tier]
    if not sel: continue
    label = tier or 'all'
    gt = {}
    for d in (10,15,20,25):
        gt[d] = {k: round(med([r['gap'][d][k] for r in sel]),1) for k in
                 ('herd','quads','hires','income','cum_income','money')}
    out['gap_tables'][label] = gt

with open('/tmp/fullmodel/M4/winner_template.json','w') as f:
    json.dump(out, f, indent=1)
print('rows:', len(rows), 'wins:', len(wins))
print('tiers:', {t: sum(1 for r in rows if r['tier']==t) for t in ('giant','mid','low')})
print('crossover med:', {k: out['crossover'][k]['med'] for k in out['crossover']})
