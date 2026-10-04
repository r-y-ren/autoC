#!/usr/bin/env python3
"""analysis14 addendum v2: volume-vs-price decomposition, late window d24-d29,
6 r33 late-fade losses. Appends 'volume_price_decomp' to the snapshot.

Key mechanic discovered (verified on 112831515 d29): opponents submit
'sell-everything' orders with qty far above holdings; only inventory-backed
portion executes. Submitted order qty is NOT volume. Therefore:
- actual volume per item = inventory-drop accounting on each seat's private
  (shed + farmer inventories): drop = max(0, inv_before - inv_after), summed
  over steps where that seat submitted a SELL of that item. Production
  (harvest) adds, usage (fertilizing) subtracts -> small contamination, noted.
- actual income = money_delta + seed_spend (engine truth for earnings, net
  of seed buys; both windows have no land/build spends for either side).
- avg realized px = drop-valued income / drop volume (same-step prices).
- d24-start inventory: shed+carried valued at d23-end prices; field crops
  valued with engine tile yield_units x price; animals counted not valued.
"""
import json

R33 = [112831515, 112835052, 112835161, 112844429, 112851433, 112856307]
OUR = 'renyxin'
W0, W1 = 24 * 24, 30 * 24  # steps 576..719
SEED_VAL = {'WHEAT': 10, 'CARROT': 20, 'TOMATO': 50, 'STRAWBERRY': 100, 'MELON': 80}


def jl(x):
    return json.loads(x) if isinstance(x, str) else x


def tot_inv(priv):
    s = dict(priv.get('shed') or {})
    for inv in (priv.get('inventories') or []):
        for k, v in (inv or {}).items():
            s[k] = s.get(k, 0) + v
    return {k: v for k, v in s.items() if v}


def bucket(item):
    return item if item in ('WHEAT', 'CARROT') else 'other'


rows = {}
for eid in R33:
    d = json.load(open(f'/tmp/r33audit/episode-{eid}-replay.json'))
    names = d['info']['TeamNames']
    seat = names.index(OUR)
    oseat = 1 - seat
    opp = names[oseat]
    steps = d['steps']
    n = len(steps)
    hi = min(W1, n) - 1  # last index with a following step for delta math

    def obs(si, who):
        return steps[si][who]['observation']

    def money(si, who):
        return jl(obs(si, who)['farms'])[who]['money']

    exec_qty = {seat: {}, oseat: {}}
    sub_qty = {seat: {}, oseat: {}}
    drop_val = {seat: 0.0, oseat: 0.0}
    seed_spend = {seat: 0, oseat: 0}
    for si in range(W0, hi):
        prices = (obs(si, seat).get('market') or {}).get('prices') or {}
        for who in (seat, oseat):
            act = steps[si][who].get('action') or {}
            sold_items = set()
            for m in (act.get('market') or []):
                if not (isinstance(m, list) and len(m) >= 3):
                    continue
                if m[0] == 'SELL':
                    sub_qty[who][m[1]] = sub_qty[who].get(m[1], 0) + m[2]
                    sold_items.add(m[1])
                elif m[0] == 'BUY_SEED':
                    seed_spend[who] += m[2] * SEED_VAL.get(m[1], 0)
            if not sold_items:
                continue
            ib = tot_inv(jl(obs(si, who).get('private') or {}))
            ia = tot_inv(jl(obs(si + 1, who).get('private') or {}))
            for item in sold_items:
                drop = ib.get(item, 0) - ia.get(item, 0)
                if drop > 0:
                    exec_qty[who][item] = exec_qty[who].get(item, 0) + drop
                    drop_val[who] += drop * prices.get(item, 0)
    m23 = money(23 * 24 + 23, seat), money(23 * 24 + 23, oseat)
    m29 = money(min(29 * 24 + 23, n - 1), seat), money(min(29 * 24 + 23, n - 1), oseat)
    dmoney = {seat: m29[0] - m23[0], oseat: m29[1] - m23[1]}
    income = {w: dmoney[w] + seed_spend[w] for w in (seat, oseat)}
    vq = {w: sum(exec_qty[w].values()) for w in (seat, oseat)}
    sq = {w: sum(sub_qty[w].values()) for w in (seat, oseat)}
    avg_px = {w: round(drop_val[w] / vq[w], 2) if vq[w] else None for w in (seat, oseat)}

    p575 = (obs(23 * 24 + 23, seat).get('market') or {}).get('prices') or {}
    farms575 = jl(obs(23 * 24 + 23, seat)['farms'])
    inv = {}
    for who, lab in ((seat, 'our'), (oseat, 'opp')):
        priv = jl(obs(23 * 24 + 23, who).get('private') or {})
        iv = tot_inv(priv)
        shed_only = {k: v for k, v in (priv.get('shed') or {}).items() if v}
        fv, cnt, yu, animals = 0.0, {}, 0, {}
        for row in farms575[who]['tiles']:
            for v in row:
                if not isinstance(v, dict):
                    continue
                c = v.get('crop')
                if c:
                    y = v.get('yield_units') or 0
                    cnt[c] = cnt.get(c, 0) + 1
                    yu += y
                    fv += y * p575.get(c, 0)
                if 'animal' in v:
                    a = v['animal']
                    animals[a] = animals.get(a, 0) + 1
        carryval = sum(v * p575.get(k, 0) for k, v in iv.items())
        inv[lab] = {'held_items': iv, 'sellable_now_value': round(carryval, 0),
                    'shed': shed_only,
                    'crop_tiles': cnt, 'total_yield_units': yu,
                    'field_value_est': round(fv, 0), 'animals': animals,
                    'sellable_plus_field_value': round(carryval + fv, 0)}

    def bq(w):
        e = exec_qty[w]
        return {'WHEAT': e.get('WHEAT', 0), 'CARROT': e.get('CARROT', 0),
                'other': vq[w] - e.get('WHEAT', 0) - e.get('CARROT', 0)}

    rows[str(eid)] = {
        'opp': opp, 'window': 'd24-d29 (steps 576-719)',
        'exec_qty_by_bucket': {'our': bq(seat), 'opp': bq(oseat)},
        'exec_qty_items': {'our': exec_qty[seat], 'opp': exec_qty[oseat]},
        'exec_qty_total': {'our': vq[seat], 'opp': vq[oseat], 'opp_minus_our': vq[oseat] - vq[seat]},
        'submitted_qty_total': {'our': sq[seat], 'opp': sq[oseat],
                                'note': 'submitted >> executed for opp: sell-everything re-quotes; only inventory-backed part fills'},
        'income_net_of_seeds': {'our': round(income[seat], 0), 'opp': round(income[oseat], 0),
                                'opp_minus_our': round(income[oseat] - income[seat], 0)},
        'money_delta': {'our': round(dmoney[seat], 0), 'opp': round(dmoney[oseat], 0)},
        'seed_spend': {'our': seed_spend[seat], 'opp': seed_spend[oseat]},
        'avg_realized_px_dropval_basis': {'our': avg_px[seat], 'opp': avg_px[oseat],
                                          'basis': 'sum(drop_qty*step_price)/sum(drop_qty); shared price series -> gap = item mix + timing'},
        'drop_valued_income': {'our': round(drop_val[seat], 0), 'opp': round(drop_val[oseat], 0)},
        'inv_d24_start': inv, 'price_snap_d23end': p575,
    }
    r = rows[str(eid)]
    print(f"{eid} {opp[:16]:16} execQty {vq[seat]:>5}/{vq[oseat]:>5} (d={vq[oseat]-vq[seat]:>+5}) "
          f"submQty {sq[seat]:>5}/{sq[oseat]:>6} "
          f"income {income[seat]:>7.0f}/{income[oseat]:>7.0f} (d={income[oseat]-income[seat]:>+6.0f}) "
          f"px {avg_px[seat] or 0:>6.2f}/{avg_px[oseat] or 0:>6.2f} "
          f"inv24 {inv['our']['sellable_plus_field_value']:>7.0f}/{inv['opp']['sellable_plus_field_value']:>7.0f} "
          f"yu {inv['our']['total_yield_units']}/{inv['opp']['total_yield_units']} anim {sum(inv['our']['animals'].values())}/{sum(inv['opp']['animals'].values())}")

agg = {
    'exec_qty_opp_minus_our': sum(rows[e]['exec_qty_total']['opp_minus_our'] for e in rows),
    'income_opp_minus_our': sum(rows[e]['income_net_of_seeds']['opp_minus_our'] for e in rows),
    'income_our_total': sum(rows[e]['income_net_of_seeds']['our'] for e in rows),
    'income_opp_total': sum(rows[e]['income_net_of_seeds']['opp'] for e in rows),
    'inv24_our_total': sum(rows[e]['inv_d24_start']['our']['sellable_plus_field_value'] for e in rows),
    'inv24_opp_total': sum(rows[e]['inv_d24_start']['opp']['sellable_plus_field_value'] for e in rows),
    'yield_units_our': sum(rows[e]['inv_d24_start']['our']['total_yield_units'] for e in rows),
    'yield_units_opp': sum(rows[e]['inv_d24_start']['opp']['total_yield_units'] for e in rows),
    'animals_our': sum(sum(rows[e]['inv_d24_start']['our']['animals'].values()) for e in rows),
    'animals_opp': sum(sum(rows[e]['inv_d24_start']['opp']['animals'].values()) for e in rows),
}
print('AGG:', json.dumps(agg))

snap_path = '/tmp/kagr_root/analysis14_snapshot.json'
snap = json.load(open(snap_path))
snap['volume_price_decomp'] = {
    'window': 'd24-d29', 'rows': rows, 'aggregate_opp_minus_our': agg,
    'method_notes': [
        'submitted SELL qty overcounts: opponents re-quote sell-everything orders; only inventory-backed part fills (verified 112831515 step 696: submitted 2000, held 87)',
        'actual volume = inventory-drop accounting per item on sell-steps (production/usage contamination small)',
        'income = money_delta + seed_spend (net earnings truth; no land/build spends in window)',
        'avg px basis: drop qty x same-step shared market price',
        'field value at d24 uses engine tile yield_units (future yield) x d23-end prices; growing crops may add yield later -> snapshot lower bound',
    ]}
json.dump(snap, open(snap_path, 'w'), indent=1, ensure_ascii=False)
print('appended ->', snap_path)
