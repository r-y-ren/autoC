"""Add spaced historical study games without touching original held-out IDs."""
import concurrent.futures
import gzip
import json
from research_round7_top2 import OUT, LEADERS, fetch, counts

original = json.loads((OUT/'index.json').read_text())
excluded = {r['episode_id'] for r in original}
chosen, summaries = [], []
for team, sid, rating in LEADERS:
    name = 'vadim' if team.startswith('Vadim') else 'dsm'
    data = json.loads((OUT.parent/f'{name}_episodes.json').read_text())
    eligible = []
    for ep in data['episodes']:
        agents = ep.get('agents', [])
        if ep.get('state') != 'COMPLETED' or len(agents)!=2 or len({a['submissionId'] for a in agents})!=2:
            continue
        own = next((a for a in agents if a['submissionId']==sid), None)
        if own is not None:
            eligible.append((ep, own))
    print(team, 'eligible', len(eligible), flush=True)
    for pos in [6,12,18,24,30,36]:
        if pos >= len(eligible):
            continue
        ep, own = eligible[pos]
        if ep['id'] in excluded:
            continue
        chosen.append({'team':team,'submission_id':sid,'rating_snapshot':rating,'episode_id':ep['id'],'seat':own.get('index',0),'agents':ep['agents'],'end_time':ep['endTime'],'split':'study_extra','historical_position_zero_based':pos})
(OUT/'study_extra_index.json').write_text(json.dumps(chosen,indent=2),encoding='utf-8')
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for eid in pool.map(fetch, sorted({r['episode_id'] for r in chosen})):
        print('downloaded extra',eid,flush=True)
for row in chosen:
    game = json.loads(gzip.decompress((OUT/f"{row['episode_id']}.json.gz").read_bytes()))
    snapshots = []
    for t in list(range(0,720,72))+[719]:
        obs = game['steps'][t][row['seat']]['observation']
        farm = obs['farms'][row['seat']]
        snapshots.append({'step':t,'money':farm['money'],'hands':len(farm['hands']),'land':len(farm['unlocked_quadrants']),'counts':counts(farm),'shops':obs['town']['unlocked_shops']})
    summaries.append({**row,'seed':game['info']['seed'],'rewards':game['rewards'],'snapshots':snapshots,'shops':snapshots[-1]['shops']})
    print(row['team'],row['episode_id'],snapshots[-1]['shops'],flush=True)
(OUT/'study_extra_production.json').write_text(json.dumps(summaries,indent=2),encoding='utf-8')
