#!/usr/bin/env python3
"""r32/r33 loss x leftover-seeds audit. Parses /tmp/r33audit replays,
writes /tmp/kagr_root/audit_rows.json with per-game rows + aggregates.
Conventions follow /tmp/r31b/audit2.py (SEED_VALUE engine constants)."""
import json, glob, os, random, statistics as st
from math import comb

SEED_VALUE = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
OUR = 'renyxin'
META = json.load(open('/tmp/kagr_root/meta_summary.json'))
ep2tag = {}
for tag in ('r32', 'r33'):
    lst = json.load(open(f"/tmp/kagr_root/episodes-{tag}-{META[tag]['ref']}.json"))
    for e in lst:
        if 'PUBLIC' in e.get('type', ''):
            ep2tag[e['id']] = tag

def jload(x):
    return json.loads(x) if isinstance(x, str) else x

def band(f):
    return 'weak<60k' if f < 60000 else ('mid60-90k' if f < 90000 else 'strong>=90k')

def day_end_money(steps, seat, day):  # end-of-day money: hour 23 of day d
    si = day * 24 + 23
    if si >= len(steps): si = len(steps) - 1
    f = jload(steps[si][0]['observation']['farms'])
    return f[seat]['money']

def fisher_2sided(a, b, c, d):
    n = a + b + c + d; r1 = a + b; c1 = a + c
    def prob(x): return comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)
    lo = max(0, c1 - (n - r1)); hi = min(r1, c1)
    p0 = prob(a)
    return sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= p0 * 1.0000001)

games = []
for fp in sorted(glob.glob('/tmp/r33audit/episode-*-replay.json')):
    d = json.load(open(fp))
    eid = d['info']['EpisodeId']
    names = d['info']['TeamNames']
    if OUR not in names:
        games.append({'episode': eid, 'tag': ep2tag.get(eid), 'error': f'renyxin not in {names}'}); continue
    seat = names.index(OUR); oseat = 1 - seat
    opp = names[oseat]
    steps = d['steps']
    r = d['rewards']
    our_r, opp_r = r[seat], r[oseat]
    if our_r is None or opp_r is None:
        games.append({'episode': eid, 'tag': ep2tag.get(eid), 'error': f'reward None {r}'}); continue
    res = 'W' if our_r > opp_r else ('L' if our_r < opp_r else 'T')
    last = steps[-1][seat]['observation']
    priv = jload(last['private'])
    seeds = priv.get('seeds', {})
    end_seeds = {k: v for k, v in seeds.items() if v}
    dead_full = sum(SEED_VALUE.get(k, 0) * v for k, v in seeds.items())
    dead_w = SEED_VALUE['WHEAT'] * seeds.get('WHEAT', 0)
    dead_c = SEED_VALUE['CARROT'] * seeds.get('CARROT', 0)
    dead_o = dead_full - dead_w - dead_c
    farms = jload(last['farms'])
    ourF, oppF = farms[seat]['money'], farms[oseat]['money']
    # opp leftovers + animals at end
    opriv = jload(steps[-1][oseat]['observation'].get('private', {}))
    oseeds = opriv.get('seeds', {})
    opp_dead = sum(SEED_VALUE.get(k, 0) * v for k, v in oseeds.items())
    oanimals = {}
    oseed_buys = oanimal_buys = osells = 0
    oland = 0; obuild = 0; ohire = 0
    for si, stp in enumerate(steps):
        act = stp[oseat].get('action') or {}
        for m in (act.get('market') or []):
            if isinstance(m, list) and len(m) >= 3 and m[0] == 'BUY_SEED': oseed_buys += m[2]
            elif isinstance(m, list) and len(m) >= 3 and m[0] == 'BUY_ANIMAL': oanimal_buys += m[2]
            elif isinstance(m, list) and len(m) >= 2 and m[0] == 'SELL': osells += 1
        fat = act.get('farmer') or []
        for c in fat:
            if not isinstance(c, str): continue
            if c == 'BUY_LAND': oland += 1
            elif c.startswith('BUILD'): obuild += 1
        for h in (act.get('hands') or []):
            for c in (h if isinstance(h, list) else [h]):
                if not isinstance(c, str): continue
                if c == 'BUY_LAND': oland += 1
                elif c.startswith('BUILD'): obuild += 1
                elif c == 'HIRE': ohire += 1
    for row in farms[oseat]['tiles']:
        for v in row:
            if isinstance(v, dict) and 'animal' in v:
                oanimals[v['animal']] = oanimals.get(v['animal'], 0) + 1
    # opp money trajectory (shared obs, our seat's view is fine)
    o_d10, o_d20 = day_end_money(steps, oseat, 10), day_end_money(steps, oseat, 20)
    m_d10, m_d20 = day_end_money(steps, seat, 10), day_end_money(steps, seat, 20)
    fam = []
    if oanimal_buys >= 4: fam.append('animal-heavy')
    if oseed_buys >= 150: fam.append('seed-heavy')
    if osells >= 400: fam.append('sell-heavy')
    if oland >= 2: fam.append('land-expander')
    games.append({
        'episode': eid, 'tag': ep2tag.get(eid), 'opp': opp, 'seat': seat, 'res': res,
        'margin': round(our_r - opp_r, 1), 'ourF': ourF, 'oppF': oppF,
        'end_seeds': end_seeds, 'end_seeds_value': dead_full,
        'dead_wheat': dead_w, 'dead_carrot': dead_c, 'dead_other': dead_o,
        'modeB_carrot_left': seeds.get('CARROT', 0) > 0,
        'end_shed': {k: v for k, v in (priv.get('shed') or {}).items() if v},
        'opp_dead_seeds_value': opp_dead, 'opp_end_seeds': {k: v for k, v in oseeds.items() if v},
        'opp_band': band(oppF), 'opp_family': fam or ['passive/low-activity'],
        'opp_actions': {'seed_buys': oseed_buys, 'animal_buys': oanimal_buys, 'sells': osells,
                        'land': oland, 'build': obuild, 'hire': ohire},
        'opp_animals_end': oanimals,
        'margin_d10': round(m_d10 - o_d10, 0), 'margin_d20': round(m_d20 - o_d20, 0),
        'oppF_d10': o_d10, 'oppF_d20': o_d20,
        'statuses': d.get('statuses'),
    })

games.sort(key=lambda g: (g.get('tag', ''), g['episode']))

# ---- sampling rule (both files >30 public): losses + equal random wins ----
rng = random.Random(20260924)
sample = []
per_tag_note = {}
for tag in ('r32', 'r33'):
    tg = [g for g in games if g.get('tag') == tag and 'error' not in g]
    L = [g['episode'] for g in tg if g['res'] == 'L']
    W = [g['episode'] for g in tg if g['res'] == 'W']
    T = [g['episode'] for g in tg if g['res'] == 'T']
    ws = rng.sample(W, min(len(W), len(L)))
    per_tag_note[tag] = {'total': len(tg), 'L': len(L), 'W': len(W), 'T': len(T),
                         'rule_sample': {'losses': len(L), 'random_wins': len(ws)}}
    sample += L + ws + T

# ---- enrichment (full population AND rule-sample) ----
def enrich(rows, label):
    out = {}
    for scope, ids in (('full', None), ('rule_sample', set(sample))):
        gg = [g for g in rows if (ids is None or g['episode'] in ids)]
        L = [g for g in gg if g['res'] == 'L']; W = [g for g in gg if g['res'] == 'W']
        lpos = sum(1 for g in L if g['end_seeds_value'] > 50)
        wpos = sum(1 for g in W if g['end_seeds_value'] > 50)
        lv = [g['end_seeds_value'] for g in L]; wv = [g['end_seeds_value'] for g in W]
        p = fisher_2sided(lpos, len(L) - lpos, wpos, len(W) - wpos) if L and W else None
        out[scope] = {
            'nL': len(L), 'nW': len(W),
            'L_dead_gt50': f"{lpos}/{len(L)}", 'W_dead_gt50': f"{wpos}/{len(W)}",
            'L_rate': round(lpos / len(L), 3) if L else None,
            'W_rate': round(wpos / len(W), 3) if W else None,
            'fisher_p_2sided': round(p, 4) if p is not None else None,
            'L_dead_med': st.median(lv) if lv else None, 'W_dead_med': st.median(wv) if wv else None,
            'L_dead_mean': round(st.mean(lv), 0) if lv else None,
            'W_dead_mean': round(st.mean(wv), 0) if wv else None,
            'L_dead_max': max(lv) if lv else None, 'W_dead_max': max(wv) if wv else None,
        }
    return out

enrichment = {tag: enrich([g for g in games if g.get('tag') == tag and 'error' not in g], tag)
              for tag in ('r32', 'r33')}
enrichment['pooled'] = enrich([g for g in games if 'error' not in g], 'pooled')

# ---- flippability ----
flips = []
for g in games:
    if 'error' in g or g['res'] != 'L': continue
    m = g['margin']; full = g['end_seeds_value']; c = g['dead_carrot']
    flips.append({
        'episode': g['episode'], 'tag': g['tag'], 'opp': g['opp'], 'margin': m,
        'dead_full': full, 'dead_carrot': c, 'dead_wheat': g['dead_wheat'],
        'flip_full': m + full >= 0, 'flip_carrotonly': m + c >= 0,
        'shortfall_after_full': round(m + full, 0), 'shortfall_after_carrot': round(m + c, 0),
        'oppF': g['oppF'], 'opp_band': g['opp_band'], 'opp_family': g['opp_family'],
    })

out = {'games': games, 'sampling_note': per_tag_note, 'enrichment': enrichment, 'flips': flips}
json.dump(out, open('/tmp/kagr_root/audit_rows.json', 'w'), indent=1, ensure_ascii=False)

# ---- console summary ----
for tag in ('r32', 'r33', None):
    gg = [g for g in games if 'error' not in g and (tag is None or g.get('tag') == tag)]
    if not gg: continue
    lab = tag or 'pooled'
    W = sum(1 for g in gg if g['res'] == 'W'); L = sum(1 for g in gg if g['res'] == 'L')
    T = len(gg) - W - L
    print(f"[{lab}] n={len(gg)} W={W} L={L} T={T} wr={W/len(gg):.3f}")
    for r in 'WLT':
        v = [g['end_seeds_value'] for g in gg if g['res'] == r]
        if v: print(f"   {r}: dead med={st.median(v):.0f} mean={st.mean(v):.0f} min={min(v)} max={max(v)} >50: {sum(1 for x in v if x>50)}/{len(v)}")
print('FLIPS:')
for f in flips:
    print(f"  {f['tag']} {f['episode']} {f['opp'][:18]:18} m={f['margin']:>8.0f} dead={f['dead_full']:>5} (c={f['dead_carrot']:>4},w={f['dead_wheat']:>3}) flipFull={f['flip_full']} flipC={f['flip_carrotonly']} afterFull={f['shortfall_after_full']:>7.0f}")
