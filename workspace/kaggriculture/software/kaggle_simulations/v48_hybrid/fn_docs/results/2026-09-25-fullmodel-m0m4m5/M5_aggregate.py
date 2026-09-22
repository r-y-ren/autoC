import json, statistics as st
R = json.load(open('/tmp/fullmodel/M5/arm_results.json'))
ARMS = ['PLACEBO','A1','A2','A3','A4','COMBO']
print(f"{'game':>10} {'kind':>7} {'B_marg':>8} " + ' '.join(f"{a:>9}" for a in ARMS))
agg = {a: {'deltas': [], 'flips': 0, 'winloss': 0} for a in ARMS}
win_reg = {a: [] for a in ARMS}
for ep, rec in sorted(R.items(), key=lambda kv: (kv[1]['kind'], kv[1]['arms']['B']['margin'])):
    B = rec['arms']['B']
    row = []
    for a in ARMS:
        m = rec['arms'][a]['margin']
        d = m - B['margin']
        row.append(d)
        if rec['kind'] == 'defeat':
            agg[a]['deltas'].append(d)
            if B['margin'] < 0 and m > 0: agg[a]['flips'] += 1
        else:
            win_reg[a].append(d)
            if B['margin'] > 0 and m <= 0: agg[a]['winloss'] += 1
    print(f"{ep:>10} {rec['kind']:>7} {B['margin']:>8.0f} " + ' '.join(f"{x:>9.0f}" for x in row))
print()
print('=== DEFEATS (n=14): delta = margin(arm) - margin(B) ===')
print(f"{'arm':>8} {'sum':>9} {'mean':>8} {'med':>8} {'min':>9} {'max':>9} {'pos':>4} {'flips':>5} {'noise>p50c':>9}")
for a in ARMS:
    ds = agg[a]['deltas']
    pd = sorted(abs(x) for x in agg['PLACEBO']['deltas'])
    thr = pd[len(pd)//2] if pd else 0
    print(f"{a:>8} {sum(ds):>9.0f} {st.mean(ds):>8.0f} {st.median(ds):>8.0f} {min(ds):>9.0f} {max(ds):>9.0f} "
          f"{sum(1 for x in ds if x>0):>4} {agg[a]['flips']:>5} {sum(1 for x in ds if abs(x)>max(thr,300)):>9}")
print()
print('=== WIN REGRESSION (n=8) ===')
print(f"{'arm':>8} {'sum':>9} {'mean':>8} {'med':>8} {'min':>9} {'max':>9} {'neg':>4} {'winloss':>8}")
for a in ARMS:
    ds = win_reg[a]
    print(f"{a:>8} {sum(ds):>9.0f} {st.mean(ds):>8.0f} {st.median(ds):>8.0f} {min(ds):>9.0f} {max(ds):>9.0f} "
          f"{sum(1 for x in ds if x<0):>4} {agg[a]['winloss']:>8}")
