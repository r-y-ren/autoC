"""Freeze a new episode-level research split before reading replay outcomes.

Only public replay data are downloaded. Older sealed/held-out games are excluded.
No candidate performance, rewards, or shop sequences participate in selection.
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import json
from pathlib import Path
import requests

ROOT = Path(__file__).parent
OUT = ROOT / 'research/round8/top2'
LEADERS = [('Vadim Vasilenko', 56427964), ('DSM', 56444344)]


def fetch(eid):
    dest = OUT / f'{eid}.json.gz'
    if not dest.exists():
        response = requests.get(f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json', timeout=120)
        response.raise_for_status()
        game = response.json()
        assert len(game['steps']) == 720 and game['info']['EpisodeId'] == eid
        dest.write_bytes(gzip.compress(response.content))
    return eid


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    old_rows = json.loads((ROOT/'research/round7/top2/index.json').read_text())
    old_rows += json.loads((ROOT/'research/round7/top2/study_extra_index.json').read_text())
    excluded = {r['episode_id'] for r in old_rows}
    index_file = OUT/'index.json'
    if not index_file.exists():
        rows = []
        for team, sid in LEADERS:
            response = requests.post('https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes', json={'submissionId': sid}, timeout=90)
            response.raise_for_status()
            listing = response.json()
            (OUT/('vadim_episodes.json' if team.startswith('Vadim') else 'dsm_episodes.json')).write_text(json.dumps(listing), encoding='utf-8')
            selected = Counter()
            episodes = sorted(listing['episodes'], key=lambda ep: ep.get('endTime',''), reverse=True)
            for ep in episodes:
                agents = ep.get('agents', [])
                if ep['id'] in excluded or ep.get('state') != 'COMPLETED' or len(agents) != 2 or len({a['submissionId'] for a in agents}) != 2:
                    continue
                own = next((a for a in agents if a['submissionId'] == sid), None)
                if own is None:
                    continue
                # One shared episode always has the same split, regardless of team.
                sealed = int(hashlib.sha256(('round8:'+str(ep['id'])).encode()).hexdigest()[:8], 16) % 5 == 0
                split = 'sealed' if sealed else 'study'
                quota = 5 if sealed else 24
                if selected[split] >= quota:
                    continue
                rows.append({'team':team, 'submission_id':sid, 'episode_id':ep['id'], 'seat':own.get('index',0), 'end_time':ep['endTime'], 'split':split})
                selected[split] += 1
                if selected['study'] >= 24 and selected['sealed'] >= 5:
                    break
            assert selected['study'] >= 20, (team, selected)
        index_file.write_text(json.dumps(rows, indent=2), encoding='utf-8')
        (OUT/'split_manifest.json').write_text(json.dumps({'selection':'Latest completed different-submission games, excluding every round7 episode; SHA256 round8:episode_id modulo 5 selects sealed before replay contents are read.', 'index_sha256':hashlib.sha256(index_file.read_bytes()).hexdigest(), 'old_excluded_ids':sorted(excluded), 'quota_per_team':{'study':24,'sealed':5}},indent=2),encoding='utf-8')
    rows = json.loads(index_file.read_text())
    with ThreadPoolExecutor(max_workers=3) as pool:
        for eid in pool.map(fetch, sorted({r['episode_id'] for r in rows})):
            print('downloaded', eid, flush=True)
    summaries = []
    for row in rows:
        if row['split'] != 'study':
            continue
        game = json.loads(gzip.decompress((OUT/f"{row['episode_id']}.json.gz").read_bytes()))
        seat = row['seat']
        snapshots=[]
        for t in range(23,720,24):
            obs=game['steps'][t][seat]['observation']; farm=obs['farms'][seat]
            counts=Counter(tile.get('animal') or tile.get('crop') or tile.get('kind') for line in farm['tiles'] for tile in line if isinstance(tile,dict))
            snapshots.append({'step':t,'money':farm['money'],'hands':len(farm['hands']),'land':len(farm['unlocked_quadrants']),'counts':dict(counts),'shops':obs['town']['unlocked_shops']})
        summaries.append({**row,'seed':game['info']['seed'],'rewards':game['rewards'],'daily_snapshots':snapshots})
    (OUT/'study_production.json').write_text(json.dumps(summaries,indent=2),encoding='utf-8')
    for team,_ in LEADERS:
        records=[r for r in summaries if r['team']==team]
        print(team,'study',len(records),'unique_seeds',len({r['seed'] for r in records}),flush=True)


if __name__=='__main__':
    main()
