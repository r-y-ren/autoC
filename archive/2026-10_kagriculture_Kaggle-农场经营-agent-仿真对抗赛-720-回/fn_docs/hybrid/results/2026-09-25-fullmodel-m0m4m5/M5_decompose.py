import json, statistics as st
R = json.load(open('/tmp/fullmodel/M5/arm_results.json'))
ARMS = ['A1','A2','A3','COMBO']
defL = sorted([ep for ep,r in R.items() if r['kind']=='defeat'])
winL = sorted([ep for ep,r in R.items() if r['kind']=='win'])
print('=== Δ decomposition: ours vs opp (defeats | wins) ===')
for a in ARMS:
    d_ours, d_opp = [], []
    w_ours, w_opp = [], []
    for ep in defL:
        r = R[ep]; B = r['arms']['B']; X = r['arms'][a]
        d_ours.append(X['ours']-B['ours']); d_opp.append(X['opp']-B['opp'])
    for ep in winL:
        r = R[ep]; B = r['arms']['B']; X = r['arms'][a]
        w_ours.append(X['ours']-B['ours']); w_opp.append(X['opp']-B['opp'])
    print(f"{a:>5} DEF ours med {st.median(d_ours):>8.0f} (pos {sum(1 for x in d_ours if x>0)}/14) | opp med {st.median(d_opp):>8.0f} (pos {sum(1 for x in d_opp if x>0)}/14)")
    print(f"      WIN ours med {st.median(w_ours):>8.0f} (pos {sum(1 for x in w_ours if x>0)}/8) | opp med {st.median(w_opp):>8.0f} (pos {sum(1 for x in w_opp if x>0)}/8)")
