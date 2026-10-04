"""Read public leader replays; keep analysis split isolated from held-out games."""
import concurrent.futures
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import requests

ROOT = Path(__file__).parent
OUT = ROOT / 'research/round7/top2'
LEADERS = [('Vadim Vasilenko', 56427964, 3097.8), ('DSM', 56444344, 3092.8)]

def get_team(item):
    team, sid, rating = item
    name = 'vadim' if team.startswith('Vadim') else 'dsm'
    dest = OUT.parent / f'{name}_episodes.json'
    if not dest.exists():
        req = requests.post('https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes', json={'submissionId': sid}, timeout=60)
        req.raise_for_status()
        dest.write_text(json.dumps(req.json()), encoding='utf-8')
    data = json.loads(dest.read_text(encoding='utf-8'))
    rows = []
    for ep in data['episodes']:
        agents = ep.get('agents', [])
        if ep.get('state') != 'COMPLETED' or len(agents) != 2 or len({a['submissionId'] for a in agents}) == 1:
            continue
        own = next((a for a in agents if a['submissionId'] == sid), None)
        if own is None:
            continue
        rows.append({'team': team, 'submission_id': sid, 'rating_snapshot': rating, 'episode_id': ep['id'], 'seat': own.get('index', 0), 'agents': agents, 'end_time': ep['endTime'], 'split': 'study' if len(rows) < 3 else 'heldout'})
        if len(rows) == 6:
            break
    return rows

def fetch(eid):
    dest = OUT / f'{eid}.json.gz'
    if not dest.exists():
        req = requests.get(f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json', timeout=90)
        req.raise_for_status()
        obj = req.json()
        assert len(obj['steps']) == 720 and obj['info']['EpisodeId'] == eid
        dest.write_bytes(gzip.compress(req.content))
    return eid

def counts(farm):
    return dict(Counter(t.get('animal') or t.get('crop') or t.get('kind') for row in farm['tiles'] for t in row if isinstance(t, dict)))

def summarize(row):
    game = json.loads(gzip.decompress((OUT / f"{row['episode_id']}.json.gz").read_bytes()))
    seat = row['seat']
    actions = [s[seat]['action'] for s in game['steps'][1:]]
    snapshots = []
    for t in [23, 47, 71, 143, 239, 359, 479, 599, 719]:
        obs = game['steps'][t][seat]['observation']
        farm = obs['farms'][seat]
        snapshots.append({'step': t, 'money': farm['money'], 'land': len(farm['unlocked_quadrants']), 'hands': len(farm['hands']), 'counts': counts(farm), 'shed': obs['private']['shed'], 'shops': obs['town']['unlocked_shops']})
    land_steps = []
    last_land = 1
    for t, state in enumerate(game['steps']):
        f = state[seat]['observation']['farms'][seat]
        if len(f['unlocked_quadrants']) > last_land:
            land_steps.append(t)
            last_land = len(f['unlocked_quadrants'])
    hires = [max(len(s[seat]['observation']['farms'][seat]['hands']) for s in game['steps'][d*24:min((d+1)*24,720)]) for d in range(30)]
    ops = Counter(op[0] for a in actions for op in [a['farmer']]+a.get('hands', []) if op)
    market_ops = Counter(op[0] for a in actions for op in a.get('market', []) if op)
    crops = Counter(op[1] for a in actions for op in [a['farmer']]+a.get('hands', []) if op and op[0]=='PLANT')
    return {**row, 'seed': game['info']['seed'], 'rewards': game['rewards'], 'snapshots': snapshots, 'land_acquired_steps': land_steps, 'daily_hands_max': hires, 'operations': dict(ops), 'market_operations': dict(market_ops), 'plantings': dict(crops), 'opening': actions[:12], 'farmer_hands_digest': [hashlib.sha256(json.dumps([a['farmer'], a.get('hands',[])], sort_keys=True).encode()).hexdigest()[:16] for a in actions]}

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        rows = [r for batch in pool.map(get_team, LEADERS) for r in batch]
        study_ids = {r['episode_id'] for r in rows if r['split']=='study'}
        for row in rows:
            if row['episode_id'] in study_ids:
                row['split'] = 'study'
        (OUT / 'index.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
        for eid in pool.map(fetch, sorted({r['episode_id'] for r in rows})):
            print('downloaded', eid, flush=True)
    output = [summarize(r) for r in rows if r['split']=='study']
    (OUT / 'study_production.json').write_text(json.dumps(output, indent=2), encoding='utf-8')
    for r in output:
        print(r['team'], r['episode_id'], r['rewards'][r['seat']], 'land', r['land_acquired_steps'], 'hires', r['daily_hands_max'], 'day10', r['snapshots'][4]['counts'], flush=True)
