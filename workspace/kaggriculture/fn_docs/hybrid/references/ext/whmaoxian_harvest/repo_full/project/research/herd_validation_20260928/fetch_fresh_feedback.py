"""Prospective public R2 feedback sample, selected before reading replay contents."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import gzip,hashlib,json,requests
D=Path(__file__).resolve().parent;O=D/'fresh_feedback';O.mkdir(exist_ok=True)
submission=56581759
response=requests.post('https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes',json={'submissionId':submission},timeout=(10,45))
response.raise_for_status();metadata=response.json()
(O/'metadata.json').write_text(json.dumps(metadata),encoding='utf-8')
selected=[]
for episode in sorted(metadata.get('episodes',[]),key=lambda e:e.get('endTime',''),reverse=True):
    agents=episode.get('agents',[])
    own=[a for a in agents if a.get('submissionId')==submission]
    if episode.get('state')!='COMPLETED' or len(agents)!=2 or len(own)!=1:continue
    me=own[0];rival=next(a for a in agents if a is not me)
    selected.append(dict(episode=episode['id'],seat=me.get('index',0),end=episode.get('endTime'),own_agent=me,rival_agent=rival))
    if len(selected)==20:break
selection=dict(captured_utc=datetime.now(timezone.utc).isoformat(),submission=submission,selection='Latest20 completed non-self episodes, chosen before replay inspection; wins and losses both retained.',views=selected)
(O/'selection.json').write_text(json.dumps(selection,indent=2),encoding='utf-8')
def download(view):
    url=f"https://www.kaggle.com/competitions/episodes/{view['episode']}/replay.json"
    r=requests.get(url,timeout=(10,45));r.raise_for_status();raw=r.content;game=json.loads(raw)
    assert len(game['steps'])==720 and game['info']['EpisodeId']==view['episode']
    (O/f"{view['episode']}.json.gz").write_bytes(gzip.compress(raw))
    return dict(episode=view['episode'],url=url,sha256=hashlib.sha256(raw).hexdigest(),seed=game['info']['seed'],rewards=game['rewards'])
with ThreadPoolExecutor(max_workers=3) as pool:receipts=list(pool.map(download,selected))
(O/'receipts.json').write_text(json.dumps(receipts,indent=2),encoding='utf-8')
print(json.dumps(dict(captured_utc=selection['captured_utc'],episodes=len(receipts),newest=selected[0],rewards=receipts)),flush=True)
