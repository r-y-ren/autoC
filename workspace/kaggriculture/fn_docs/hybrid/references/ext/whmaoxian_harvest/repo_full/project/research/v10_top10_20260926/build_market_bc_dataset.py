"""Own-player market decisions from the declared public study split only."""
from pathlib import Path
import contextlib,copy,gzip,hashlib,io,json,sys
import numpy as np
D=Path(__file__).resolve().parent; R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
import market_bc_features as ft
split=json.loads((D/'replay_split.json').read_text());views=split['study']
assert not {v['episode'] for v in views}.intersection(v['episode'] for v in split['heldout'])
entry=fa.load('submissions/release_v10_r2/main.py');ns=entry.__globals__
X=[];Y=[];episode_ids=[];amounts=[];sources=[];checks=0
for episode in sorted({v['episode'] for v in views}):
    path=D/f'study_replays/{episode}.json.gz';raw=path.read_bytes()
    game=json.loads(gzip.decompress(raw));sources.append(dict(episode=episode,sha256=hashlib.sha256(raw).hexdigest()))
    assert len(game['steps'])==720
    for view in [v for v in views if v['episode']==episode]:
        seat=view['seat'];history={}
        for step in range(719):
            obs=game['steps'][step][seat]['observation'];obs['step']=step;obs['player']=seat
            action=game['steps'][step+1][seat]['action']
            projected=ns['projected_shed'](action,ns['FarmView'](obs))
            if step%97==0:
                farm=copy.deepcopy(obs['farms'][seat]);private=copy.deepcopy(obs['private'])
                commands=[action.get('farmer',['PASS'])]+list(action.get('hands',[]))
                for actor,command in enumerate(commands[:len(farm['hands'])+1]):
                    fa.engine._apply_unit_action(farm,private,actor,command,10,step//24,24,100)
                assert all(projected.get(k,0)==private['shed'].get(k,0) for k in set(projected)|set(private['shed'])),(episode,seat,step)
                checks+=1
            context=ft._mbc_context(obs,action,projected,history);sold={}
            for item in ft._MBC_ITEMS:
                available=max(0,int(projected.get(item,0)))
                requested=sum(max(0,int(o[2])) for o in action.get('market',[])[:10] if len(o)>=3 and o[:2]==['SELL',item])
                quantity=min(available,requested);sold[item]=quantity
                if available:
                    features=ft._mbc_features(context,item);assert len(features)==ft.MBC_FEATURE_COUNT
                    X.append(features);Y.append([int(quantity>0),quantity/available])
                    episode_ids.append(episode);amounts.append(available)
            ft._mbc_commit(context,sold)
    print(json.dumps(dict(episode=episode,samples=len(X),projection_checks=checks)),flush=True)
target=D/'market_bc_dataset.npz';assert not target.exists()
np.savez_compressed(target,X=np.asarray(X,dtype=np.float32),Y=np.asarray(Y,dtype=np.float32),episode=np.asarray(episode_ids,dtype=np.int64),available=np.asarray(amounts,dtype=np.float32))
manifest=dict(samples=len(X),features=ft.MBC_FEATURE_COUNT,outputs=['sell_probability','unconditional_sale_fraction'],source_files=sources,feature_source_sha256=hashlib.sha256((D/'market_bc_features.py').read_bytes()).hexdigest(),dataset_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),projection_checks=checks,input_scope=ft.MBC_INPUT_SCOPE,heldout_used=False)
(D/'market_bc_dataset_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(samples=len(X),features=ft.MBC_FEATURE_COUNT,projection_checks=checks,heldout_used=False)),flush=True)
