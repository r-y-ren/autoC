"""Download public match records; never upload or change Kaggle submissions."""
from pathlib import Path
import concurrent.futures, importlib.util, json
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('collector', ROOT/'research/round10/collect_leaderboard.py')
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)
collector.ROOT = OUT
teams = json.loads((OUT/'opponent_team_selection.json').read_text(encoding='utf-8'))
views = []
for team in teams:
    sid = team['submissionId']
    destination = OUT/f'episodes_{sid}.json'
    data = collector.post('competitions.EpisodeService/ListEpisodes', {'submissionId': sid})
    destination.write_text(json.dumps(data), encoding='utf-8')
    selected = []
    for episode in data.get('episodes', []):
        agents = episode.get('agents', [])
        own = [a for a in agents if a['submissionId'] == sid]
        if episode.get('state') != 'COMPLETED' or len(agents) != 2 or len(own) != 1:
            continue
        selected.append(dict(team=team['team_name'], rating=float(team['displayScore']),
            submission=sid, episode=episode['id'], seat=own[0].get('index', 0),
            role='study' if not selected else 'unseen_trace'))
        if len(selected) == 2:
            break
    views.extend(selected)
    print('Selected', team['rank'], sid, len(selected), flush=True)
(OUT/'current_views.json').write_text(json.dumps(views, ensure_ascii=False, indent=2), encoding='utf-8')
rows = json.loads((OUT/'v10_public_summary_rows.json').read_text(encoding='utf-8'))
losses = [r for r in rows if r['margin'] < 0]
ids = sorted({r['episode'] for r in views + losses})
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(collector.public_replay, ids))
(OUT/'replay_provenance.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print('Completed public downloads', len(results), flush=True)
