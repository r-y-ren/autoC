"""Aggregate per-transaction-type diffs (opponent minus R2) over episodes.
usage: cmpagg.py sid ep1 ep2 ..."""
import sys, io, contextlib, collections, json
import resim as R
from concurrent.futures import ProcessPoolExecutor
def one(args):
    sid, eid = args
    with contextlib.redirect_stdout(io.StringIO()):
        agg = R.resim(eid)
    g = json.load(__import__('gzip').open(f'replays/{eid}.json.gz'))
    # which seat is sid? use eplist
    return eid, [dict((k, tuple(v)) for k, v in a.items()) for a in agg]
if __name__ == '__main__':
    sid = int(sys.argv[1]); eps = [int(e) for e in sys.argv[2:]]
    ep = json.load(open(f'eplists/{sid}.json'))['episodes']
    seat = {}
    for e in ep:
        for i, a in enumerate(e['agents']):
            if a['submissionId'] == sid: seat[e['id']] = i
    tot = collections.defaultdict(lambda: [0, 0.0, 0, 0.0])
    with ProcessPoolExecutor(28) as p:
        for eid, agg in p.map(one, [(sid, e) for e in eps]):
            me, op = agg[seat[eid]], agg[1 - seat[eid]]
            for k in set(me) | set(op):
                a = me.get(k, (0, 0)); b = op.get(k, (0, 0))
                tot[k][0] += a[0]; tot[k][1] += a[1]; tot[k][2] += b[0]; tot[k][3] += b[1]
    n = len(eps)
    print(f'{"per game":22s} {"me n":>7s} {"me $":>9s} {"op n":>7s} {"op $":>9s} {"op-me $":>9s}')
    for k in sorted(tot, key=lambda k: -abs(tot[k][3] - tot[k][1])):
        a = tot[k]
        print(f'{k:22s} {a[0]/n:7.1f} {a[1]/n:9.0f} {a[2]/n:7.1f} {a[3]/n:9.0f} {(a[3]-a[1])/n:9.0f}')
