#!/usr/bin/env python3
"""M5 Task1: capital allocation model (marginal NPV / payback / stop-times / d0-d10 schedule).

Pricing (endogenous, winner-observed): per-day marginal price = median winner-seat
lockstep revenue per unit (M4 all_games, n=50 usable winner games; single-item lines
MILK/WOOL/EGG/FERTILIZER direct; crops line decomposed on dominant-crop days; else
engine price curve at mild-glut inventory -- M0 params). Feed wheat = $26 (buy at I0).
"""
import json

M0 = json.load(open('/tmp/fullmodel/M0/economy_model.json'))
AN = M0['animals']; CR = M0['crops']
FEED = 26.0
FERT_CR = {0: 0.5, 5: 0.5, 10: 0.5, 15: 0.5, 20: 0.4, 25: 0.2, 29: 0.0}  # collection rate
# observed marginal price path (winner med rev/unit; None->engine curve fallback)
PRICE = {
 # direct: single-item lines
 'MILK':   {10: 201, 15: 8, 20: 22, 25: 3},
 'WOOL':   {6: 207, 10: 37, 15: 12, 20: 52, 25: 42, 29: 52},
 'EGG':    {15: 53, 20: 54, 25: 56, 29: 58},
 'FERTILIZER': {3: 96, 10: 79, 15: 56, 20: 43, 25: 24, 29: 3},
 # crops-line decomposition (dominant-crop days) + engine-curve sanity
 'MELON':      {10: 200, 12: 180, 20: 150, 29: 100},
 'STRAWBERRY': {14: 40, 20: 15, 29: 5},
 'WHEAT':      {20: 21, 29: 19},
 'CARROT':     {29: 22},
 'TOMATO':     {20: 35},
}
BASE = {k: v['base_$'] for k, v in M0['market']['products'].items()}
def mprice(item, d):
    d = max(0, min(29, d))
    tab = PRICE.get(item, {})
    if d in tab: return float(tab[d])
    ks = sorted(tab)
    if not ks: return float(BASE[item])
    if d < ks[0]: 
        # before first observation: fresh-market regime (scarcity or base)
        return float(BASE[item]) if item not in ('MILK','WOOL','EGG') else float(max(BASE[item], tab[ks[0]]))
    prev = max(k for k in ks if k <= d)
    return float(tab[prev])

def fert_rate(d):
    ks = sorted(FERT_CR)
    prev = max(k for k in ks if k <= d)
    return FERT_CR[prev]

# ---------- animals ----------
def animal_events(a, p):
    A = AN[a]; itv = A['production_interval_days']; cap = A['standing_yield_cap_units']
    ev = []; d = p + A['first_harvest_day_after_placement']
    while d <= 29:
        prev = ev[-1][0] if ev else p
        ev.append((d, min(cap, 1 + min(itv, d - prev))))
        d += itv
    return ev
PROD = {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}
def animal_eval(a, p):
    prod = PROD[a]; ev = animal_events(a, p)
    if not ev: return None
    rev = sum(n * mprice(prod, d) for d, n in ev)
    last = ev[-1][0]
    feed = (last - p + 1) * FEED
    fert = sum(fert_rate(d) * mprice('FERTILIZER', d) for d in range(p, last + 1))
    npv = rev + fert - feed - AN[a]['cost_$']
    cash = -AN[a]['cost_$']; pay = None; evd = dict(ev)
    for d in range(p, last + 1):
        cash -= FEED
        cash += evd.get(d, 0) * mprice(prod, d) + fert_rate(d) * mprice('FERTILIZER', d)
        if pay is None and cash >= 0: pay = d - p
    return npv, pay, rev, fert

# ---------- crops ----------
def crop_cycles(c, p):
    C = CR[c]; out = []
    if not C['ongoing']:
        d = p
        while d + C['max_yield_day'] <= 29:
            y = C['yield_units_with_fertilizer'] if c in ('WHEAT', 'CARROT') else C['yield_units_no_fertilizer']
            out.append((d + C['max_yield_day'], y)); d += C['cycle_days']
    else:
        for i in range(C['production_events_total']):
            d = p + C['first_yield_day'] + i * C['interval_days']
            if d > 29: break
            out.append((d, C['per_event_units_fert_and_watered_same_day']))
    return out
def crop_npv(c, p):
    return sum(y * mprice(c, d) for d, y in crop_cycles(c, p)) - CR[c]['seed_cost_$']

# ---------- land / hire ----------
LANDP = {'NE': 1000, 'SW': 2000, 'SE': 4000}
def tile_value(p):
    return max(crop_npv(c, p) for c in ('MELON', 'STRAWBERRY', 'WHEAT', 'CARROT'))
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
def hire_max_rank(d):
    lam = max(15.0, 0.3 * 6 * mprice('MELON', d))
    k = 0
    while k + 1 < len(FIB) and FIB[k + 1] <= 20 * lam: k += 1
    return k, round(lam)

# ---------- d0-d10 schedule: greedy marginal NPV/$ under money/op/tile constraints ----------
def schedule():
    """Greedy marginal-NPV schedule d0-d10 under money AND op constraints.
    Op demand: herd x 2 ops/day (feed+care+harvest amortized) + crop tiles x 0.9 op/day.
    Op supply: farmer 22 + hands x 20. Land bought only if new tiles workable within ops."""
    daily_inc = [0, 397, 393, 387, 0, 1036, 4719, 358, 469, 2401, 11065]
    money = 3000.0
    st = dict(sheep=0, cow=0, goose=0, quads=1, hands=2, tiles=8)  # d0: plant 8 melon in NW
    log = []
    for d in range(0, 11):
        cands = []
        for a in ('SHEEP', 'COW', 'GOOSE'):
            r = animal_eval(a, d)
            if r and r[0] > 0:
                cands.append((r[0] / AN[a]['cost_$'], 'buy_' + a, AN[a]['cost_$']))
        nxt = ['NE', 'SW', 'SE'][st['quads'] - 1]
        net = 25 * tile_value(d) - LANDP[nxt]
        if net > 0:
            cands.append((net / LANDP[nxt], 'buy_land_' + nxt, LANDP[nxt]))
        cands.sort(reverse=True)
        notes = []
        for npv_per, name, cost in cands:
            if money < cost: continue
            new_animal = 1 if name.startswith('buy_') and 'land' not in name else 0
            new_tiles = 25 if 'land' in name else 0
            # feasible only if ops cover the ADDITION at target utilization
            herd = st['sheep'] + st['cow'] + st['goose'] + new_animal
            tiles = st['tiles'] + (6 if new_tiles else 0)  # only ~6 of 25 new tiles workable soon
            need = herd * 2.5 + tiles * 2.6
            have = 22 + st['hands'] * 20
            if need > have:
                extra = int((need - have) // 20) + 1
                hc = sum(FIB[i + 1] for i in range(extra))
                if hc <= 20 * 15 * extra:  # hire profitable at $15/op shadow
                    if money >= cost + hc:
                        st['hands'] += extra; money -= hc; notes.append(f'hire+{extra}@${hc}')
                else:
                    continue
            money -= cost
            if name == 'buy_SHEEP': st['sheep'] += 1
            elif name == 'buy_COW': st['cow'] += 1
            elif name == 'buy_GOOSE': st['goose'] += 1
            else:
                st['quads'] += 1; st['tiles'] += 8
            notes.append(f'{name}@${cost}')
        st['tiles'] = min(st['tiles'] + 3, int((22 + st['hands'] * 20 - (st['sheep']+st['cow']+st['goose']) * 2.5) / 2.6))  # tiles only as ops allow
        log.append((d, round(money), dict(st), notes))
        money += daily_inc[d]
    return log

if __name__ == '__main__':
    out = {'marginal_price_path': {it: {str(d): mprice(it, d) for d in (0, 6, 10, 15, 20, 25, 29)} for it in PRICE},
           'animals': {}, 'crops': {}, 'land': {}, 'hire': {}}
    print('=== marginal price path (winner-observed medians; fallback engine curve) ===')
    for it in ('MELON', 'WOOL', 'MILK', 'STRAWBERRY', 'WHEAT', 'EGG', 'FERTILIZER'):
        print(f"{it:>11}: " + '  '.join(f"d{d}={round(mprice(it, d)):>4}" for d in (0, 3, 6, 10, 15, 20, 25, 29)))
    print()
    print('=== animals: NPV/payback/stop-time (care-fed; feed $26/d; fert credit) ===')
    for a in ('COW', 'SHEEP', 'GOOSE'):
        rows = {}; stop = None
        for p in range(30):
            r = animal_eval(a, p)
            rows[p] = None if r is None else (round(r[0]), r[1])
            if r and r[0] > 0: stop = p
        out['animals'][a] = {'stop_day': stop, 'npv_payback_by_day': {str(k): v for k, v in rows.items() if v}}
        sel = [(p, rows[p]) for p in (0, 4, 8, 12, 16, 18, 19, 20, 21, 22) if rows[p]]
        print(f"{a}: stop d{stop}; (p: NPV, payback-days): {sel}")
    print()
    print('=== crops: per-tile NPV / stop-time ===')
    for c in ('MELON', 'WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY'):
        stop = None
        for p in range(30):
            if crop_npv(c, p) > 0: stop = p
        out['crops'][c] = {'stop_day': stop, 'npv': {str(d): round(crop_npv(c, d)) for d in (0, 10, 15, 17, 20, 25)}}
        print(f"{c:>11}: d0={crop_npv(c,0):>6.0f} d10={crop_npv(c,10):>6.0f} d15={crop_npv(c,15):>6.0f} "
              f"d17={crop_npv(c,17):>6.0f} d20={crop_npv(c,20):>6.0f} stop=d{stop}")
    print()
    print('=== land: 25 tiles x best-use NPV - price ===')
    for q in ('NE', 'SW', 'SE'):
        stop = None
        for p in range(30):
            if 25 * tile_value(p) - LANDP[q] > 0: stop = p
        out['land'][q] = {'stop_day': stop, 'tile_npv_d10': round(tile_value(10))}
        print(f"{q} (${'{:,}'.format(LANDP[q])}): stop=d{stop}  (tile value d10 ~${tile_value(10):.0f})")
    print()
    print('=== hire: profitable same-day rank cap (fib vs 20 ops x shadow) ===')
    for d in (0, 6, 10, 15, 20, 25, 28, 29):
        k, lam = hire_max_rank(d)
        out['hire']['d%d' % d] = {'max_rank': k, 'op_shadow_$': lam}
        print(f"d{d:>2}: rank<= {k:>2} (op shadow ~${lam}; 11th=$89, 12th=$144, 13th=$233)")
    print()
    print('=== d0-d10 greedy marginal schedule (money from winner income path) ===')
    for d, m, st, notes in schedule():
        print(f"d{d:>2}: money_after_spends={m:>7} herd(s/c/g)={st['sheep']}/{st['cow']}/{st['goose']} "
              f"quads={st['quads']} hands={st['hands']} tiles={st['tiles']} buys: {'; '.join(notes) if notes else '-'}")
    json.dump(out, open('/tmp/fullmodel/M5/stop_times.json', 'w'), indent=1)
    print('saved stop_times.json')
