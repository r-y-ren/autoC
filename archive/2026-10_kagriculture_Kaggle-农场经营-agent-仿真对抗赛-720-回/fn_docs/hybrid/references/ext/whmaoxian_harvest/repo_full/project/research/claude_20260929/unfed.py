"""From online replays: our animals left unfed at hour 23 each day, and when R2 hires.
usage: unfed.py team ep1 ep2 ..."""
import sys, collections
from surrogate import load

PROD = {'SHEEP': 'WOOL', 'COW': 'MILK', 'GOOSE': 'EGG'}
tot = collections.Counter(); val = collections.Counter(); caredunfed = collections.Counter()
hire_hours = collections.Counter(); hires_per_day = []
n = 0
for e in sys.argv[2:]:
    g = load(int(e)); n += 1
    me = g['info']['TeamNames'].index(sys.argv[1])
    for d in range(30):
        o = g['steps'][d * 24 + 23][me]['observation'] if 'farms' in g['steps'][d * 24 + 23][me]['observation'] else g['steps'][d * 24 + 23][0]['observation']
        f = o['farms'][me]
        prices = g['steps'][d * 24 + 23][0]['observation']['market']['prices']
        for row in f['tiles']:
            for t in row:
                if isinstance(t, dict) and t.get('animal') and not t.get('fed_today'):
                    tot[(t['animal'], d // 10)] += 1
                    val[t['animal']] += prices[PROD[t['animal']]]
                    if t.get('cared_today'):
                        caredunfed[t['animal']] += 1
        hires_per_day.append(f.get('hires_today', 0))
    for t in range(1, 720):
        a = g['steps'][t][me]['action'] or {}
        k = sum(1 for m in (a.get('market') or []) if m and m[0] == 'HIRE')
        if k:
            hire_hours[(t - 1) % 24] += k
print('games', n)
for a in PROD:
    print(a, 'unfed-days/game by decade', [round(tot[(a, k)] / n, 1) for k in range(3)], 'cared&unfed/game', round(caredunfed[a] / n, 1), 'avg price', round(val[a] / max(1, sum(tot[(a, k)] for k in range(3))), 1))
print('hire hours', sorted(hire_hours.items()))
print('hires/day avg', round(sum(hires_per_day) / len(hires_per_day), 1), 'max', max(hires_per_day))
