"""Archive a bounded fresh public demonstration set; never executes downloaded code."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import gzip,hashlib,json,requests
D=Path(__file__).resolve().parent;R=D.parents[1];OUT=D/'top10_dev_20260928';OUT.mkdir(exist_ok=True)
board=json.loads((R/'research/v10_top10_20260926/latest_public_board.json').read_text(encoding='utf-8'))
def select(team):
    url='https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes'
    response=requests.post(url,json={'submissionId':team['submission']},timeout=(10,40));response.raise_for_status()
    data=response.json();(OUT/f"episodes_{team['submission']}.json").write_text(json.dumps(data))
    chosen=[]
    for episode in sorted(data.get('episodes',[]),key=lambda e:e.get('endTime',''),reverse=True):
        agents=episode.get('agents',[]);own=[a for a in agents if a['submissionId']==team['submission']]
        if episode.get('state')!='COMPLETED' or len(agents)!=2 or len(own)!=1:continue
        chosen.append(dict(team=team['team'],rank=team['rank'],submission=team['submission'],episode=episode['id'],seat=own[0].get('index',0),end=episode.get('endTime'),role='development_only'))
        if len(chosen)==2:break
    return chosen

def download(eid):
    url=f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json'
    response=requests.get(url,timeout=(10,45));response.raise_for_status();raw=response.content
    assert len(raw)<40000000,'Unexpected replay size'
    game=json.loads(raw);assert game['info']['EpisodeId']==eid and len(game['steps'])==720
    (OUT/f'{eid}.json.gz').write_bytes(gzip.compress(raw))
    return dict(episode=eid,sha256=hashlib.sha256(raw).hexdigest(),url=url)
if __name__=='__main__':
    assert not (OUT/'selection.json').exists(),'Keep existing selection immutable.'
    with ThreadPoolExecutor(max_workers=3) as pool:views=sum(pool.map(select,board['top10']),[])
    selection=dict(board_captured_utc=board['captured_utc'],selected_utc=datetime.now(timezone.utc).isoformat(),views=views,scope='Latest two completed public non-self episodes per captured top-ten entry; chosen before replay inspection. Development, not validation.')
    (OUT/'selection.json').write_text(json.dumps(selection,indent=2),encoding='utf-8')
    with ThreadPoolExecutor(max_workers=3) as pool:receipts=list(pool.map(download,sorted({v['episode'] for v in views})))
    (OUT/'receipts.json').write_text(json.dumps(receipts,indent=2),encoding='utf-8')
    print(json.dumps(dict(views=len(views),episodes=len(receipts),teams=len({v['team'] for v in views}),directory=str(OUT))),flush=True)
