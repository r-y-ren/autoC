"""Per player, per animal type: animal-days, fed-days, cared-days from a replay (end-of-day hour 23 snapshot).
usage: animals_ep.py ep1 ep2 ..."""
import sys, collections
from anal import load

for e in sys.argv[1:]:
    g = load(int(e))
    names = g['info']['TeamNames']
    out = []
    for p in range(2):
        c = collections.defaultdict(lambda: [0, 0, 0, 0])
        for t in range(23, 720, 24):
            obs = g['steps'][t][0]['observation']
            f = obs['farms'][p]
            for row in f['tiles']:
                for tile in row:
                    if isinstance(tile, dict) and tile.get('animal'):
                        a = c[tile['animal']]
                        a[0] += 1; a[1] += bool(tile.get('fed_today')); a[2] += bool(tile.get('cared_today'))
        out.append({k: tuple(v[:3]) for k, v in c.items()})
    print(e, names[0][:10], out[0], '|', names[1][:10], out[1])
