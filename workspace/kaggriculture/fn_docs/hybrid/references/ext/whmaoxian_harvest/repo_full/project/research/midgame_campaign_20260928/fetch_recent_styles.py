"""Read recent public top-ten demonstrations; do not submit or execute downloaded code."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import collections,gzip,hashlib,json,requests
D=Path(__file__).resolve().parent;R=D.parents[1];O=D/'recent_replays';O.mkdir(exist_ok=True)
board=json.loads((R/'research/v10_top10_20260926/latest_public_board.json').read_text())
def select(team):
    url='https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes'
    response=requests.post(url,json={'submissionId':team['submission']},timeout=(10,35));response.raise_for_status()
    data=response.json();(O/f"episodes_{team['submission']}.json").write_text(json.dumps(data))
    chosen=[]
    for e in sorted(data.get('episodes',[]),key=lambda e:e.get('endTime',''),reverse=True):
        a=e.get('agents',[]);own=[x for x in a if x['submissionId']==team['submission']]
        if e.get('state')!='COMPLETED' or len(a)!=2 or len(own)!=1:continue
        chosen.append(dict(team=team['team'],rank=team['rank'],submission=team['submission'],episode=e['id'],seat=own[0].get('index',0),end=e.get('endTime'),role='development_demonstration'))
        if len(chosen)==2:break
    return chosen
def download(eid):
    url=f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json'
    response=requests.get(url,timeout=(10,45));response.raise_for_status();raw=response.content
    game=json.loads(raw);assert game['info']['EpisodeId']==eid and len(game['steps'])==720
    path=O/f'{eid}.json.gz';path.write_bytes(gzip.compress(raw))
    return dict(episode=eid,sha256=hashlib.sha256(raw).hexdigest(),url=url)
if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=3) as pool:views=sum(pool.map(select,board['top10']),[])
    (D/'recent_selection.json').write_text(json.dumps(dict(captured_utc=datetime.now(timezone.utc).isoformat(),views=views,selection='Two latest completed non-self episodes per captured top-ten submission; chosen before content inspection.'),indent=2))
    with ThreadPoolExecutor(max_workers=3) as pool:receipts=list(pool.map(download,sorted({v['episode'] for v in views})))
    (D/'recent_receipts.json').write_text(json.dumps(receipts,indent=2));profiles=[]
    for v in views:
        game=json.loads(gzip.decompress((O/f"{v['episode']}.json.gz").read_bytes()));seat=v['seat'];snapshots=[]
        for step in (144,240,360,480,600,719):
            farm=game['steps'][step][seat]['observation']['farms'][seat];mix=collections.Counter()
            for row in farm['tiles']:
                for tile in row:
                    if isinstance(tile,dict):mix[tile.get('animal') or tile.get('crop') or tile.get('kind')]+=1
            snapshots.append(dict(step=step,cash=farm['money'],land=farm['unlocked_quadrants'],mix=dict(mix)))
        idle=0;slots=collections.Counter()
        for step in range(719):
            obs=game['steps'][step][seat]['observation'];farm=obs['farms'][seat];a=game['steps'][step+1][seat]['action']
            idle+=sum(c==['PASS'] for c in a.get('hands',[])[:len(farm['hands'])])
            slots[len(a.get('market',[]))]+=1
        profiles.append(dict(v,rewards=game['rewards'],snapshots=snapshots,idle_worker_turns=idle,market_slot_counts=dict(slots)))
    (D/'recent_style_profiles.json').write_text(json.dumps(profiles,indent=2))
    print(json.dumps(dict(views=len(views),episodes=len(receipts),teams=len({v['team'] for v in views}),profiles=[dict(team=p['team'],reward=p['rewards'][p['seat']],day10=p['snapshots'][1]['mix']) for p in profiles])),flush=True)
