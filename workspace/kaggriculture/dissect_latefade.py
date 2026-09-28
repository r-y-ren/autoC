#!/usr/bin/env python3
"""late-fade day-level dissection (analysis14). Per-day d12..d29 for r33 late-fade
losses; peak/fade/attribution only for r32 contrast set. Writes dissect_r33.json."""
import json

SEED_VALUE = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}
OUR = 'renyxin'
R33_LATEFADE = [112831515, 112835052, 112835161, 112844429, 112851433, 112856307]
R32_LATEFADE = [112857426]


def jload(x):
    return json.loads(x) if isinstance(x, str) else x


def dissect(eid):
    d = json.load(open(f'/tmp/r33audit/episode-{eid}-replay.json'))
    names = d['info']['TeamNames']
    seat = names.index(OUR)
    oseat = 1 - seat
    opp = names[oseat]
    steps = d['steps']
    n = len(steps)

    def obs(si):
        return steps[si][seat]['observation']

    def money(si):
        f = jload(obs(si)['farms'])
        return f[seat]['money'], f[oseat]['money']

    day_end = {}
    for dd in range(0, 30):
        si = min(dd * 24 + 23, n - 1)
        day_end[dd] = money(si)
    final_margin = day_end[29][0] - day_end[29][1]

    per_day = []
    for dd in range(12, 30):
        lo = dd * 24
        hi = min(dd * 24 + 24, n)
        om, omp = day_end[dd]
        pm, pmp = day_end[dd - 1]
        odelta, pdelta = om - pm, omp - pmp
        our_sells = opp_sells = 0
        our_sell_rev_est = 0
        seed_orders = seed_cost = seed_qty = 0
        animal_orders = animal_qty = 0
        for si in range(lo, hi):
            prices = (obs(si).get('market') or {}).get('prices') or {}
            for who in (seat, oseat):
                act = steps[si][who].get('action') or {}
                for m in (act.get('market') or []):
                    if not (isinstance(m, list) and len(m) >= 2):
                        continue
                    if m[0] == 'SELL':
                        qty = m[2] if len(m) >= 3 else 0
                        px = prices.get(m[1], 0)
                        if who == seat:
                            our_sells += 1
                            our_sell_rev_est += qty * px
                        else:
                            opp_sells += 1
                    elif who == seat and m[0] == 'BUY_SEED':
                        seed_orders += 1
                        q = m[2] if len(m) >= 3 else 0
                        seed_qty += q
                        seed_cost += q * SEED_VALUE.get(m[1], 0)
                    elif who == seat and m[0] == 'BUY_ANIMAL':
                        animal_orders += 1
                        animal_qty += m[2] if len(m) >= 3 else 0
        per_day.append({
            'day': dd, 'our_money': round(om, 0), 'opp_money': round(omp, 0),
            'our_delta': round(odelta, 0), 'opp_delta': round(pdelta, 0),
            'our_sells': our_sells, 'our_sell_rev_est': round(our_sell_rev_est, 0),
            'seed_orders': seed_orders, 'seed_qty': seed_qty, 'seed_cost': seed_cost,
            'animal_orders': animal_orders, 'animal_qty': animal_qty,
            'opp_sells': opp_sells,
        })

    lead = {dd: day_end[dd][0] - day_end[dd][1] for dd in range(0, 30)}
    peak_day = max(lead, key=lambda k: lead[k])
    peak_val = lead[peak_day]
    fade_window = f'd{peak_day}->d29'
    fw = [r for r in per_day if r['day'] > peak_day]
    # baselines: median daily delta over stable pre-peak window d8..peak_day
    base_days = [dd for dd in range(8, peak_day + 1)] or [peak_day]
    obase = sorted(day_end[dd][0] - day_end[dd - 1][0] for dd in base_days)
    pbase = sorted(day_end[dd][1] - day_end[dd - 1][1] for dd in base_days)
    our_base_med = obase[len(obase) // 2]
    opp_base_med = pbase[len(pbase) // 2]
    # per-day swing toward opponent: s = opp_delta - our_delta
    swing = {'opp_surge': 0.0, 'our_stall': 0.0, 'mixed': 0.0, 'neither': 0.0}
    big_days = []
    for r in fw:
        s = r['opp_delta'] - r['our_delta']
        surge = r['opp_delta'] > 1.5 * max(opp_base_med, 1)
        stall = r['our_delta'] < 0.5 * max(our_base_med, 1)
        spend = r['our_delta'] < 0 and r['seed_cost'] > r['our_sell_rev_est']
        if surge and stall:
            k = 'mixed'
        elif surge:
            k = 'opp_surge'
        elif stall:
            k = 'our_stall'
        else:
            k = 'neither'
        swing[k] += s
        if s > 100:
            big_days.append({'day': r['day'], 'swing': round(s, 0), 'kind': k,
                             'our_delta': r['our_delta'], 'opp_delta': r['opp_delta'],
                             'opp_sells': r['opp_sells'], 'our_sells': r['our_sells']})
    tot_fade = peak_val - final_margin
    tot_swing = sum(v for v in swing.values())
    attr = {
        'our_base_med_daily_delta': round(our_base_med, 0),
        'opp_base_med_daily_delta': round(opp_base_med, 0),
        'fade_days': len(fw),
        'total_fade': round(tot_fade, 0),
        'swing_sum_check': round(tot_swing, 0),
        'swing_share': {k: round(v / tot_swing, 3) for k, v in swing.items() if tot_swing},
        'swing_abs': {k: round(v, 0) for k, v in swing.items()},
        'spend_days_negative_delta': sum(1 for r in fw if r['our_delta'] < 0),
        'big_swing_days': big_days,
        'endgame': {
            'd28_opp_sells': next((r['opp_sells'] for r in per_day if r['day'] == 28), None),
            'd29_opp_sells': next((r['opp_sells'] for r in per_day if r['day'] == 29), None),
            'd28_our_sells': next((r['our_sells'] for r in per_day if r['day'] == 28), None),
            'd29_our_sells': next((r['our_sells'] for r in per_day if r['day'] == 29), None),
        },
    }
    return {'episode': eid, 'opp': opp, 'final_money_margin': round(final_margin, 0),
            'per_day': per_day, 'peak_day': peak_day, 'peak_lead': round(peak_val, 0),
            'fade_window': fade_window, 'attribution': attr,
            'lead_by_day': {str(k): round(v, 0) for k, v in lead.items()}}


out = {}
for eid in R33_LATEFADE:
    out[str(eid)] = dissect(eid)
    print(f'=== {eid} vs {out[str(eid)]["opp"]} peak d{out[str(eid)]["peak_day"]} '
          f'+{out[str(eid)]["peak_lead"]:.0f} final {out[str(eid)]["final_money_margin"]:.0f} '
          f'fade {out[str(eid)]["fade_window"]} attr {out[str(eid)]["attribution"]}')
for eid in R32_LATEFADE:
    out[str(eid)] = dissect(eid)
    a = out[str(eid)]
    print(f'=== r32 {eid} vs {a["opp"]} peak d{a["peak_day"]} +{a["peak_lead"]:.0f} '
          f'final {a["final_money_margin"]:.0f} fade {a["fade_window"]} attr {a["attribution"]}')
json.dump(out, open('/tmp/kagr_root/dissect_latefade.json', 'w'), indent=1)
print('written /tmp/kagr_root/dissect_latefade.json')
