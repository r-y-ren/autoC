"""Reconstruct executed rival sales from explicitly designated development replays."""
from pathlib import Path
import contextlib,gzip,hashlib,io,json,sys
from array import array
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'));sys.path.insert(0,str(D))
import rival_features_20260929 as features
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
files=sorted((D/'recent_replays').glob('*.json.gz'))+sorted((D/'top10_dev_20260928').glob('*.json.gz'))
seen=set();all_x=[];all_y=[];all_groups=[];receipts=[];original=fa.engine._commit_unit
for path in files:
    raw=gzip.decompress(path.read_bytes());game=json.loads(raw);episode=game['info']['EpisodeId']
    if episode in seen:continue
    seen.add(episode);steps=len(game['steps'])
    if steps!=720 or any(s['status']!='DONE' for s in game['steps'][-1]):continue
    state,env=fa.new_game(game['info']['seed'],game['configuration']);identity={id(f):i for i,f in enumerate(state[0].observation.farms)}
    sales=[[[0,0,0,0] for _ in range(2)] for _ in range(719)];episode_x=[];indices=[];history=[]
    def commit(op,item,price,farm,private,market,shed_capacity=100):
        ok=original(op,item,price,farm,private,market,shed_capacity)
        if ok and op=='SELL' and item in features._K29F_TARGETS:
            sales[turn][identity[id(farm)]][features._K29F_TARGETS.index(item)]+=1
        return ok
    try:
        fa.engine._commit_unit=commit
        for turn in range(719):
            for seat in (0,1):state[seat].observation.step=turn
            now=features._k29f_snapshot(state[0].observation)
            if 144<=turn<696:
                for target in (0,1):
                    for item_index,item in enumerate(features._K29F_TARGETS):
                        if now['prices'][item]<=1:continue
                        episode_x.append(features._k29f_vector(now,target,item,history));indices.append((turn,target,item_index))
            history.append(now);history=history[-8:]
            for seat in (0,1):state[seat].action=game['steps'][turn+1][seat]['action']
            fa.engine.interpreter(state,env)
        actual=[f['money'] for f in state[0].observation.farms]
        expected=[s['observation']['farms'][i]['money'] for i,s in enumerate(game['steps'][-1])]
        assert actual==expected,(episode,actual,expected)
        width=len(episode_x[0]);x=array("f",(v for row in episode_x for v in row))
        y=array("f",[sales[t][target][item]+sales[t+1][target][item] for t,target,item in indices])
        all_x.append(x);all_y.append(y);all_groups.append(array("q",[episode]*len(y)))
        receipts.append(dict(episode=episode,file=path.relative_to(R).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),rows=len(y),positive8=sum(v>=8 for v in y),replay_reproduced=True))
        print(json.dumps(receipts[-1]),flush=True)
    finally:fa.engine._commit_unit=original
assert len(receipts)>=20
X=array("f");y=array("f");groups=array("q")
for part in all_x:X.extend(part)
for part in all_y:y.extend(part)
for part in all_groups:groups.extend(part)
for name,data in [('X.f32',X),('y.f32',y),('groups.i64',groups)]:
    with (D/('rival_dataset_20260929_'+name)).open('wb') as handle:data.tofile(handle)
report=dict(episodes=len(receipts),rows=len(y),features=width,target='Executed premium-product units this turn plus next turn',feature_scope='Only public farm, market, shop and past public snapshots. No private inventory, future snapshots, identity, rating or seed features.',source_scope='Only recent_replays and top10_dev_20260928, both already designated DEVELOPMENT. No reserved replay views opened.',receipts=receipts)
(D/'rival_dataset_manifest_20260929.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='receipts'}),flush=True)
