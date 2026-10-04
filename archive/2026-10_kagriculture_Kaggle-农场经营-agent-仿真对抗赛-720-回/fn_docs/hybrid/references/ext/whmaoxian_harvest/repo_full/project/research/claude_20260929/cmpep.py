"""Per-episode revenue diff (opponent minus us) for main products.
usage: cmpep.py sid ep1 ep2 ..."""
import sys, io, contextlib, json
import resim as R
from concurrent.futures import ProcessPoolExecutor

KEYS = ['SELL:STRAWBERRY', 'SELL:MELON', 'SELL:MILK', 'SELL:WOOL', 'SELL:TOMATO', 'SELL:EGG', 'SELL:CARROT',
        'SELL:WHEAT', 'SELL:FERTILIZER', 'HIRE:', 'LAND:', 'BUY_PRODUCT:WHEAT', 'BUY_PRODUCT:FERTILIZER']


def one(eid):
    with contextlib.redirect_stdout(io.StringIO()):
        agg = R.resim(eid)
    return eid, [dict((k, tuple(v)) for k, v in a.items()) for a in agg]


if __name__ == '__main__':
    sid = int(sys.argv[1]); eps = [int(e) for e in sys.argv[2:]]
    seat = {}
    for e in json.load(open(f'eplists/{sid}.json'))['episodes']:
        for i, a in enumerate(e['agents']):
            if a['submissionId'] == sid:
                seat[e['id']] = i
    print('ep        ' + ' '.join(k.split(':')[1][:5] or k[:5] for k in KEYS))
    with ProcessPoolExecutor(8) as p:
        for eid, agg in p.map(one, eps):
            me, op = agg[seat[eid]], agg[1 - seat[eid]]
            row = []
            for k in KEYS:
                a = me.get(k, (0, 0)); b = op.get(k, (0, 0))
                row.append(f'{b[1] - a[1]:5.0f}')
            print(eid, ' '.join(row))
