"""Acquire a time-based public replay panel, without selecting by outcome."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import gzip,hashlib,json,requests
D=Path(__file__).resolve().parent;O=D/'fresh_panel';O.mkdir(exist_ok=True)
SID=56581759;COUNT=40
endpoint='https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes'
response=requests.post(endpoint,json={'submissionId':SID},timeout=(10,40));response.raise_for_status()
data=response.json();raw=response.content
(O/'metadata.json').write_bytes(raw)
choices=[]
for episode in sorted(data.get('episodes',[]),key=lambda e:e.get('endTime',''),reverse=True):
    agents=episode.get('agents',[]);mine=[a for a in agents if a['submissionId']==SID]
    if episode.get('state')!='COMPLETED' or episode.get('type')!='EPISODE_TYPE_PUBLIC' or len(agents)!=2 or len(mine)!=1:continue
    me=mine[0];other=next(a for a in agents if a is not me)
    choices.append(dict(episode=episode['id'],seat=me.get('index',0),end=episode.get('endTime'),original_margin=me['reward']-other['reward'],opponent_initial_score=other.get('initialScore'),opponent_submission=other['submissionId']))
    if len(choices)==COUNT:break
manifest=dict(captured_utc=datetime.now(timezone.utc).isoformat(),submission=SID,selection='Latest 40 completed public non-self matches returned by the public API, ordered by end time; no outcome or score filtering.',metadata_sha256=hashlib.sha256(raw).hexdigest(),rows=choices,role='Acquired before final candidate freeze; do not inspect replay contents until frozen evaluation.')
assert not (O/'selection.json').exists()
(O/'selection.json').write_text(json.dumps(manifest,indent=2))
def fetch(row):
    url=f"https://www.kaggle.com/competitions/episodes/{row['episode']}/replay.json"
    result=requests.get(url,timeout=(10,60));result.raise_for_status()
    game=result.json();assert len(game['steps'])==720 and game['info']['EpisodeId']==row['episode']
    path=O/f"{row['episode']}.json.gz";path.write_bytes(gzip.compress(result.content))
    return dict(episode=row['episode'],url=url,sha256=hashlib.sha256(result.content).hexdigest())
with ThreadPoolExecutor(max_workers=3) as pool:receipts=list(pool.map(fetch,choices))
(O/'receipts.json').write_text(json.dumps(receipts,indent=2))
print(json.dumps(dict(downloaded=len(receipts),selection=manifest['selection'],role=manifest['role'])),flush=True)
