import json, statistics as st
R = json.load(open('/tmp/fullmodel/M5/arm_results.json'))
ARMS = ['PLACEBO','A1','A2','A3','A4','COMBO']
defL = sorted([ep for ep,r in R.items() if r['kind']=='defeat'])
winL = sorted([ep for ep,r in R.items() if r['kind']=='win'])
res = {'defeats': {}, 'wins': {}, 'decomposition': {}, 'invalid_baseline': [], 'placebo_floor': {}}
pl = [R[ep]['arms']['PLACEBO']['margin']-R[ep]['arms']['B']['margin'] for ep in defL]
res['placebo_floor'] = {'median_abs': sorted(abs(x) for x in pl)[7], 'p90_abs': sorted(abs(x) for x in pl)[12], 'max_abs': max(abs(x) for x in pl),
                        'note': 'bimodal: 7/14 games |d|<300 (no divergence), tail to +/-21k (market-regime flip)'}
for a in ARMS:
    d = [R[ep]['arms'][a]['margin']-R[ep]['arms']['B']['margin'] for ep in defL]
    w = [R[ep]['arms'][a]['margin']-R[ep]['arms']['B']['margin'] for ep in winL]
    res['defeats'][a] = {'sum': round(sum(d)), 'mean': round(st.mean(d)), 'median': round(st.median(d)),
                         'pos': sum(1 for x in d if x>0), 'flips': sum(1 for ep in defL if R[ep]['arms']['B']['margin']<0 and R[ep]['arms'][a]['margin']>0),
                         'per_game': {ep: round(x) for ep,x in zip(defL,d)}}
    res['wins'][a] = {'sum': round(sum(w)), 'mean': round(st.mean(w)), 'median': round(st.median(w)),
                      'neg': sum(1 for x in w if x<0),
                      'flips_to_loss': sum(1 for ep in winL if R[ep]['arms']['B']['margin']>0 and R[ep]['arms'][a]['margin']<=0),
                      'per_game': {ep: round(x) for ep,x in zip(winL,w)}}
    dec = {}
    for kind, eps in (('def',defL),('win',winL)):
        o = [R[ep]['arms'][a]['ours']-R[ep]['arms']['B']['ours'] for ep in eps]
        p = [R[ep]['arms'][a]['opp']-R[ep]['arms']['B']['opp'] for ep in eps]
        dec[kind] = {'ours_med': round(st.median(o)), 'opp_med': round(st.median(p))}
    res['decomposition'][a] = dec
for ep, r in R.items():
    if not r.get('valid'): res['invalid_baseline'].append({'ep': ep, 'kind': r['kind'], 'B_margin': r['arms']['B']['margin'], 'tape': r['tape_rewards']})
res['mechanism_audit'] = {
  'A1_d6_wool': 'all 22 games already 23-24 units at d6 (cow arrives d4, not d0): pure window already banked in r26 agent; M4 cow_d0=1 claim describes r27 tapes, not this corpus',
  'A2_d10_wheat': '0 SELL WHEAT orders d10-11 in all 14 defeat tapes; d10 already melon-flush 42-48 units (winner med 44.2) - premise absent',
  'A2_full_clear': 'd28-29 clear sold 125-272 units for ~0 gain (+101 in probe); strips feed wheat -> 8/8 negative on wins (t0=-2.7) via lost d28 EOD care-bonus production',
  'A3_direct': 'trimmed 23-43 ext wheat units/game (~$600-1100 direct saving) but replan+market re-roll swamps it (placebo tail 21k)',
  'A4_care': 'care already saturated: all fills redundant, delta=0.0 EXACTLY in 22/22 games; care_day ~= herd_day in tapes',
}
res['verdict'] = {
  'A1': 'REJECT as adjustment (mechanism already implemented by r26 agent; measured +/-20k deltas are market-regime re-rolls)',
  'A2': 'REJECT (premise absent at d10; endgame full-clear actively harmful on wins)',
  'A3': 'NOT VALIDATABLE at margin level (direct ~800 saving real but below chaos floor; win regression opp-driven)',
  'A4': 'REJECT (zero headroom; care saturated)',
  'COMBO': 'REJECT (defeats +6.3k mean but wins -15.3k mean t0=-3.09, 4/8 flip to loss; asymmetry is regression-to-mean of favorable regimes, dominated by opponent-side price gains)',
  'meta': 'margin-level twin counterfactuals have chaos floor p90 ~9k / max ~21k (lockstep shared market price-regime flips; strawberry cliff +62, wool +59, milk +76 are knife-edges). M4-derived +0.8-2k/game hypotheses are unidentifiable at margin level with n=14. Mechanism-level audits are the reliable instrument.',
}
json.dump(res, open('/tmp/fullmodel/M5/m5_results.json','w'), ensure_ascii=False, indent=1)
print('saved m5_results.json')
for a in ARMS:
    d = res['defeats'][a]; w = res['wins'][a]
    print(f"{a:>7} DEF sum={d['sum']:>7} med={d['median']:>6} flips={d['flips']} | WIN sum={w['sum']:>7} med={w['median']:>6} neg={w['neg']}/8 to_loss={w['flips_to_loss']}")
