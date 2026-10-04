import sys, os, json, glob
sys.path.insert(0, '/tmp/fullmodel/M5')
from _paths import V48H
allg = json.load(open('/tmp/fullmodel/M4/all_games.json'))
defeat_eps = set()
for fp in glob.glob(V48H + '/fn_docs/results/replays-lead-collapse/episode-*-replay.json'):
    defeat_eps.add(os.path.basename(fp).split('-')[1])
games = []
wins = []
for g in allg:
    ep = str(g['episode_id'])
    teams = g['teams']
    me = teams.index('renyxin') if 'renyxin' in teams else None
    if me is None: continue
    src = g.get('source')
    if not src or not os.path.exists(src): continue
    margin = g['rewards'][me] - g['rewards'][1-me]
    rec = dict(ep=int(ep), path=src, me=me, kind='?', margin=margin,
               opp=teams[1-me], src=os.path.basename(os.path.dirname(src)))
    if ep in defeat_eps:
        rec['kind'] = 'defeat'; games.append(rec)
    elif margin > 0:
        wins.append(rec)
print('defeats selected:', len(games), 'wins available:', len(wins))
# pick 8 wins: prefer r26 (verified regen), spread margins, avoid mirror-vs-self
wins26 = [w for w in wins if w['src'] == 'r26full' and w['opp'] != 'renyxin']
wins26.sort(key=lambda w: w['margin'])
n = len(wins26)
if n >= 8:
    idxs = sorted(set([int(i*(n-1)/7) for i in range(8)]))[:8]
    picked = [wins26[i] for i in idxs]
else:
    picked = wins26
    rest = [w for w in wins if w['src'] != 'r26full']
    rest.sort(key=lambda w: w['margin'])
    picked += rest[:8-len(picked)]
picked = picked[:8]
for w in picked: w['kind'] = 'win'
games += picked
json.dump(games, open('/tmp/fullmodel/M5/games.json', 'w'), ensure_ascii=False, indent=1)
for g in games:
    print(g['kind'], g['ep'], 'me=', g['me'], 'margin=', g['margin'], g['opp'], g['src'])
