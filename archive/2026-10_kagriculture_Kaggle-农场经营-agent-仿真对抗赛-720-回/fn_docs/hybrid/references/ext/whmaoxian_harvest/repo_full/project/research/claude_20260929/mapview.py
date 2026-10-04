import sys, collections
from anal import load

CH = {'WHEAT': 'w', 'CARROT': 'c', 'TOMATO': 't', 'STRAWBERRY': 's', 'MELON': 'm', 'GOOSE': 'G', 'COW': 'C', 'SHEEP': 'S'}


def tch(t):
    if t is None:
        return '.'
    if t == 'LOCKED':
        return ' '
    k = t['kind']
    if k == 'PLANT':
        return CH[t['crop']]
    if k == 'WEED':
        return '#'
    a = t.get('animal')
    return CH[a] if a else ('o' if k == 'COOP' else 'p')


def show(eid, name, days):
    g = load(eid)
    seat = g['info']['TeamNames'].index(name)
    for d in days:
        o = g['steps'][d * 24 + 12][seat]['observation']
        f = o['farms'][seat]
        print(f'--- day {d} h12 money {f["money"]:.0f} hands {len(f["hands"])}')
        for y in range(10):
            print('   ' + ''.join(tch(f['tiles'][y][x]) for x in range(10)))
    buys = collections.defaultdict(list)
    for t in range(719):
        a = g['steps'][t + 1][seat]['action'] or {}
        for m in a.get('market') or []:
            if m and m[0] in ('BUY_ANIMAL', 'BUY_LAND', 'BUY_SEED'):
                buys[t // 24].append((t % 24, m[0][4:], *m[1:]))
    for d in sorted(buys):
        print('d', d, buys[d])


if __name__ == '__main__':
    show(int(sys.argv[1]), sys.argv[2], [int(x) for x in sys.argv[3].split(',')])
