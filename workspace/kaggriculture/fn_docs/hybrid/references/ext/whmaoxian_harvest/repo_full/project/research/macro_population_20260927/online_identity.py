"""Read public submission evidence; no login, private endpoint, or online upload."""
from pathlib import Path
from datetime import datetime,timezone
import contextlib,copy,gzip,hashlib,io,json,sys,requests
D=Path(__file__).resolve().parent;R=D.parents[1];T=R/'research/v10_top10_20260926'
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as fa
board=json.loads((T/'latest_public_board.json').read_text())
sid=board['own_team_board_entries'][0]['submissionId']
url='https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes'
response=requests.post(url,json={'submissionId':sid},timeout=40);response.raise_for_status()
data=response.json();(D/f'public_submission_{sid}.json').write_text(json.dumps(data))
rows=[]
for e in data.get('episodes',[]):
    agents=e.get('agents',[]);own=[a for a in agents if a.get('submissionId')==sid]
    if e.get('state')!='COMPLETED' or len(agents)!=2 or len(own)!=1:continue
    me=own[0];other=next(a for a in agents if a is not me)
    if not isinstance(me.get('reward'),(int,float)) or not isinstance(other.get('reward'),(int,float)):continue
    rows.append(dict(episode=e['id'],end=e.get('endTime',''),seat=me.get('index',0),margin=me['reward']-other['reward'],rating=me.get('updatedScore'),opponent_initial_rating=other.get('initialScore')))
rows.sort(key=lambda r:r['end']);chosen=rows[-1:]
losses=[r for r in rows if r['margin']<0]
if losses and losses[-1] not in chosen:chosen.append(losses[-1])
checks=[]
for row in chosen:
    url=f"https://www.kaggle.com/competitions/episodes/{row['episode']}/replay.json"
    response=requests.get(url,timeout=60);response.raise_for_status();game=response.json()
    assert len(game['steps'])==720
    (D/f"public_{row['episode']}.json.gz").write_bytes(gzip.compress(response.content))
    matches={}
    for version in ('release_v10_r2','release_v10'):
        entry=fa.load(f'submissions/{version}/main.py');same=0;first=[]
        for t in range(719):
            obs=copy.deepcopy(game['steps'][t][row['seat']]['observation']);obs['step']=t
            action=entry(obs,game['configuration']);recorded=game['steps'][t+1][row['seat']]['action']
            if action==recorded:same+=1
            elif len(first)<5:first.append(t)
        matches[version]=dict(matching_actions=same,total=719,first_difference_steps=first)
    checks.append(dict(row,source_url=url,replay_sha256=hashlib.sha256(response.content).hexdigest(),parity=matches))
report=dict(captured_utc=datetime.now(timezone.utc).isoformat(),submission_id=sid,
    board_capture=board['captured_utc'],public_games=len(rows),wins=sum(r['margin']>0 for r in rows),
    losses=len(losses),ties=sum(r['margin']==0 for r in rows),latest=rows[-1:] or None,
    opponent_rating_ranges={str(bound):sum(isinstance(r['opponent_initial_rating'],(int,float)) and r['opponent_initial_rating']>=bound for r in rows) for bound in (2000,2400,2600,2800)},
    checked_replays=checks,scope='Post-game rating and exact recorded-action checks, not a current rating guarantee.')
(D/'online_identity.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report),flush=True)
