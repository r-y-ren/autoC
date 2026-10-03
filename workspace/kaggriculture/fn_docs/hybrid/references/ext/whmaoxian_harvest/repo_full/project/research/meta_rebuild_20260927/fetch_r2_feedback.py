"""Read R2 public ladder metadata and recent losses; never upload a submission."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import gzip,hashlib,json,requests
D=Path(__file__).resolve().parent;O=D/'r2_feedback';O.mkdir(exist_ok=True);SID=56581759
url='https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes'
r=requests.post(url,json={'submissionId':SID},timeout=(10,35));r.raise_for_status();data=r.json()
(O/'metadata.json').write_text(json.dumps(data),encoding='utf-8');rows=[]
for e in data.get('episodes',[]):
    a=e.get('agents',[]);mine=[x for x in a if x['submissionId']==SID]
    if e.get('state')!='COMPLETED' or e.get('type')!='EPISODE_TYPE_PUBLIC' or len(a)!=2 or len(mine)!=1:continue
    me=mine[0];other=next(x for x in a if x is not me)
    rows.append(dict(episode=e['id'],end=e.get('endTime',''),seat=me.get('index',0),margin=me['reward']-other['reward'],rating=me.get('updatedScore'),opponent_initial_rating=other.get('initialScore'),opponent_submission=other['submissionId'],opponent_team=other['teamId']))
rows.sort(key=lambda x:x['end']);losses=[x for x in rows if x['margin']<0]
chosen=losses[-6:]
if rows and rows[-1] not in chosen:chosen.append(rows[-1])
(O/'selection.json').write_text(json.dumps(chosen,indent=2))
def fetch(row):
    url=f"https://www.kaggle.com/competitions/episodes/{row['episode']}/replay.json"
    r=requests.get(url,timeout=(10,45));r.raise_for_status();game=r.json()
    assert len(game['steps'])==720 and game['info']['EpisodeId']==row['episode']
    path=O/f"{row['episode']}.json.gz";path.write_bytes(gzip.compress(r.content))
    return dict(row,url=url,sha256=hashlib.sha256(r.content).hexdigest(),rewards=game['rewards'])
with ThreadPoolExecutor(max_workers=3) as pool:receipts=list(pool.map(fetch,chosen))
bins={}
for low,high in ((0,1800),(1800,2000),(2000,2200),(2200,2400),(2400,2600),(2600,10000)):
    group=[x for x in rows if isinstance(x['opponent_initial_rating'],(int,float)) and low<=x['opponent_initial_rating']<high]
    bins[f'{low}-{high}']=dict(games=len(group),wins=sum(x['margin']>0 for x in group),losses=sum(x['margin']<0 for x in group),ties=sum(x['margin']==0 for x in group))
report=dict(captured_utc=datetime.now(timezone.utc).isoformat(),submission=SID,public_games=len(rows),wins=sum(x['margin']>0 for x in rows),losses=len(losses),latest=rows[-1:] or None,rating_bins=bins,receipts=receipts,scope='Public episode listing as returned; rating is not a forecast or final stable skill estimate.')
(O/'rows.json').write_text(json.dumps(rows,indent=2));(O/'summary.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report),flush=True)
