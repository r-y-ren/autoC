import json, math
R = json.load(open('/tmp/fullmodel/M5/arm_results.json'))
ARMS = ['PLACEBO','A1','A2','A3','A4','COMBO']

def mann_whitney_exact(x, y):
    # exact permutation on ranks for small n (normal approx w/ tie correction)
    nx, ny = len(x), len(y)
    al = sorted([(v,0) for v in x]+[(v,1) for v in y])
    # ranks with ties
    ranks = []
    i = 0
    while i < len(al):
        j = i
        while j < len(al) and al[j][0] == al[i][0]: j += 1
        r = (i+1+j)/2
        for k in range(i,j): ranks.append((r, al[k][1]))
        i = j
    U1 = sum(r for r,b in ranks if b==0)
    mu = nx*ny/2
    N = nx+ny
    # tie-corrected sigma
    from collections import Counter
    cnt = Counter(v for v,_ in al)
    tie = sum(t**3-t for t in cnt.values())
    import statistics
    sigma = math.sqrt(nx*ny/12*((N+1)-tie/(N*(N-1))))
    z = (U1-mu)/sigma if sigma else 0
    return U1, z, 2*(1-0.5*(1+math.erf(abs(z)/math.sqrt(2))))

def mean_se(xs):
    n = len(xs); m = sum(xs)/n
    var = sum((x-m)**2 for x in xs)/(n-1)
    return m, math.sqrt(var/n)

defL = [ep for ep,r in R.items() if r['kind']=='defeat']
winL = [ep for ep,r in R.items() if r['kind']=='win']
def deltas(eps, a):
    return [r:=R[ep]['arms'][a]['margin']-R[ep]['arms']['B']['margin'] for ep in eps]

pl = deltas(defL, 'PLACEBO')
print('PLACEBO defeats: |d| list:', sorted(round(abs(x)) for x in pl))
print('  mean %.0f  median|.| %.0f  p90|.| %.0f' % (sum(pl)/len(pl), sorted(abs(x) for x in pl)[len(pl)//2], sorted(abs(x) for x in pl)[int(len(pl)*0.9)]))
print()
print('arm  | defeat: mean(SE), t-vs-placebo(mean), MW-p, pos/n | win: mean(SE), t-vs-0, neg/n')
for a in ARMS:
    d = deltas(defL, a); w = deltas(winL, a)
    m, se = mean_se(d)
    pm, pse = mean_se(pl)
    tdiff = (m-pm)/math.sqrt(se**2+pse**2)
    U, z, p = mann_whitney_exact(d, pl)
    wm, wse = mean_se(w)
    tw = wm/wse if wse else 0
    print(f"{a:>7}| {m:>7.0f}({se:.0f}) t={tdiff:5.2f} MWp={p:5.3f} pos={sum(1 for x in d if x>0)}/14 "
          f"| {wm:>7.0f}({wse:.0f}) t0={tw:5.2f} neg={sum(1 for x in w if x<0)}/8")

# mechanism checks: end herd & counters for A1/A3
print()
print('=== mechanism audit (defeats): end herd, counters ===')
for ep in defL:
    r = R[ep]
    for a in ('A1','A3','COMBO'):
        c = r['arms'][a]['counters']
        print(ep, a, c)
