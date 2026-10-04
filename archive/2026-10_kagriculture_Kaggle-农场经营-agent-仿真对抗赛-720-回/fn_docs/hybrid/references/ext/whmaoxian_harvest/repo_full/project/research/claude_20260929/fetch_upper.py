"""Sample leaderboard teams in a rank window, list their recent completed episodes.
usage: fetch_upper.py rank_lo rank_hi n_teams per_team out.txt
Writes lines: episode_id<TAB>keep_team_name<TAB>team_score"""
import sys, json, time, random, requests
URL = 'https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes'
lo, hi, nteams, per, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
d = json.load(open('board_raw.json', encoding='utf-8'))
teams = {int(t['teamId']): t for t in d['teams']}
rows = [r for r in d['publicLeaderboard'] if lo <= int(r['rank']) <= hi and int(r['teamId']) != 16899200]
random.seed(7)
pick = random.sample(rows, min(nteams, len(rows)))
lines = []
for r in pick:
    sid = int(r['submissionId'])
    name = teams[int(r['teamId'])]['teamName']
    for attempt in range(3):
        resp = requests.post(URL, json={'submissionId': sid}, timeout=60)
        if resp.status_code == 429:
            time.sleep(60); continue
        break
    if resp.status_code != 200:
        print('fail', sid, resp.status_code); continue
    eps = [e for e in resp.json().get('episodes', []) if e.get('state') == 'COMPLETED' and e.get('type') == 'EPISODE_TYPE_PUBLIC'
           and len(e.get('agents', [])) == 2 and all(a.get('reward') is not None for a in e['agents'])]
    eps.sort(key=lambda e: e.get('endTime') or '')
    for e in eps[-per:]:
        lines.append(f"{e['id']}\t{name}\t{r['displayScore']}")
    print(r['rank'], r['displayScore'], name[:20], sid, 'eps', len(eps), flush=True)
    time.sleep(3)
open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
print('wrote', len(lines))
