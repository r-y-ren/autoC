"""Select disjoint study and validation episodes from local public JSON snapshots."""
from pathlib import Path
from datetime import datetime, timezone
import json
ROOT = Path(__file__).resolve().parent
def select():
    top = json.loads((ROOT / 'top10.json').read_text(encoding='utf-8'))
    study, heldout, eligible = [], [], {}
    for team in top:
        sid = team['submission']
        listing = json.loads((ROOT / f'episodes_{sid}.json').read_text(encoding='utf-8'))
        eligible[sid] = []
        for episode in listing.get('episodes', []):
            agents = episode.get('agents', [])
            own = [a for a in agents if a.get('submissionId') == sid]
            if episode.get('state') != 'COMPLETED' or len(agents) != 2 or len(own) != 1:
                continue
            me = own[0]
            other = next(a for a in agents if a is not me)
            eligible[sid].append(dict(team=team['team'], rank=team['rank'], submission=sid,
                episode=episode['id'], seat=me.get('index', 0), rating=me.get('initialScore'),
                opponent_rating=other.get('initialScore'), opponent_submission=other['submissionId']))
        study.extend(eligible[sid][:3])
    study_ids = {row['episode'] for row in study}
    for team in top:
        heldout.extend([row for row in eligible[team['submission']] if row['episode'] not in study_ids][:2])
    assert not study_ids.intersection(row['episode'] for row in heldout)
    return dict(created_utc=datetime.now(timezone.utc).isoformat(), study=study, heldout=heldout)

if __name__ == '__main__':
    result = select()
    (ROOT / 'replay_split.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({key: len(result[key]) for key in ('study', 'heldout')}), flush=True)
