"""Build public-state order-forecast data from the existing declared study split."""
from pathlib import Path
import contextlib,copy,gzip,hashlib,io,json,sys
import numpy as np
D=Path(__file__).resolve().parent;R=D.parents[1];T=R/'research/v10_top10_20260926'
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
sys.path.append(str(R/'.venv/Lib/site-packages'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
import cycle_features as ft
split=json.loads((T/'replay_split.json').read_text());index=json.loads((T/'demonstrations_index.json').read_text())
assert not {v['episode'] for v in split['study']} & {v['episode'] for v in split['heldout']}
entry=fa.load('submissions/release_v10_r2/main.py');ns=entry.__globals__
X=[];Y=[];groups=[];receipts=[];checks=0
for episode in sorted({v['episode'] for v in split['study']}):
    path=T/f'study_replays/{episode}.json.gz';raw=path.read_bytes();game=json.loads(gzip.decompress(raw))
    receipts.append(dict(episode=episode,sha256=hashlib.sha256(raw).hexdigest()))
    for view in [v for v in split['study'] if v['episode']==episode]:
        seat=view['seat'];history={}
        record=next(v for v in index if v['episode']==episode and v['seat']==seat)
        demo_raw=(R/record['path']).read_bytes();assert hashlib.sha256(demo_raw).hexdigest()==record['sha256']
        demo=json.loads(gzip.decompress(demo_raw))
        for t in range(719):
            obs=game['steps'][t][1-seat]['observation'];obs['step']=t;obs['player']=1-seat
            target=game['steps'][t][seat]['observation'];target['step']=t;target['player']=seat
            actual=game['steps'][t+1][seat]['action'];orders=demo['actions'][t]['market'][:10]
            projected=ns['projected_shed'](actual,ns['FarmView'](target))
            for item in ft._CY_ITEMS:
                buys=[o for o in orders if len(o)>=3 and o[:2]==['BUY_PRODUCT',item]]
                sells=[o for o in orders if len(o)>=3 and o[:2]==['SELL',item]]
                b=sum(max(0,int(o[2])) for o in orders[:2] if len(o)>=3 and o[:2]==['BUY_PRODUCT',item]) if not sells else 0
                s=min(max(0,int(projected.get(item,0))),sum(max(0,int(o[2])) for o in orders[:2] if len(o)>=3 and o[:2]==['SELL',item])) if not buys else 0
                X.append(ft.cycle_features(obs,item,history));Y.append([int(b>0),int(s>0),min(40,b)/40,min(40,s)/40]);groups.append(episode)
            ft.cycle_commit(obs,history)
            if t%101==0:
                farm=copy.deepcopy(target['farms'][seat]);private=copy.deepcopy(target['private'])
                commands=[actual.get('farmer') or ['PASS']]+list(actual.get('hands') or [])
                for i,c in enumerate(commands[:len(farm['hands'])+1]):fa.engine._apply_unit_action(farm,private,i,c,10,t//24,24,100)
                assert all(private['shed'].get(k,0)==projected.get(k,0) for k in ft._CY_ITEMS)
                checks+=1
    print(json.dumps(dict(episode=episode,samples=len(X))),flush=True)
X=np.asarray(X,dtype=np.float32);Y=np.asarray(Y,dtype=np.float32)
assert X.shape[1]==ft.CYCLE_FEATURE_COUNT and np.isfinite(X).all() and np.isfinite(Y).all()
path=D/'cycle_dataset.npz';assert not path.exists()
np.savez_compressed(path,X=X,Y=Y,episode=np.asarray(groups,dtype=np.int64))
manifest=dict(samples=len(X),features=ft.CYCLE_FEATURE_COUNT,outputs=['early_pure_buy_probability','early_pure_sell_probability','early_buy_quantity_div40','early_sell_quantity_div40'],label_means=Y.mean(axis=0).tolist(),sources=receipts,feature_sha256=hashlib.sha256((D/'cycle_features.py').read_bytes()).hexdigest(),dataset_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),projection_checks=checks,heldout_used=False,input_scope=ft.CYCLE_INPUT_SCOPE)
(D/'cycle_dataset_manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(samples=len(X),means=manifest['label_means'],projection_checks=checks)),flush=True)
