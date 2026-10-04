"""Learn virtual-game order-slot quantities from study replays; held-out games stay sealed."""
from pathlib import Path
import gzip,hashlib,json
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import average_precision_score,mean_squared_error
import flow_features as flow
N=Path(__file__).resolve().parent
arrays=np.load(N/'flow_dataset.npz');X=arrays['X'];episodes=arrays['episode']
split=json.loads((N/'replay_split.json').read_text());labels=[]
for episode in sorted({row['episode'] for row in split['study']}):
    game=json.loads(gzip.decompress((N/f'study_replays/{episode}.json.gz').read_bytes()))
    for view in [row for row in split['study'] if row['episode']==episode]:
        seat=view['seat']
        for step in range(144,717):
            obs=dict(game['steps'][step][seat]['observation']);obs['step']=step
            action=game['steps'][step+1][seat]['action'];stock=flow.flow_project(obs,action)
            by_item={item:[0.0]*10 for item in flow.FLOW_ITEMS}
            for slot,order in enumerate(action.get('market',[])[:10]):
                if len(order)<3 or order[0]!='SELL' or order[1] not in by_item:continue
                item=order[1];quantity=min(max(0,int(order[2])),stock.get(item,0))
                stock[item]=stock.get(item,0)-quantity;by_item[item][slot]=min(40,quantity)/20.0
            labels.extend(by_item[item] for item in flow.FLOW_ITEMS)
    print(json.dumps(dict(episode=episode,samples=len(labels))),flush=True)
Y=np.asarray(labels,dtype=np.float32);assert len(Y)==len(X)
old=json.loads((N/'flow_model_report.json').read_text());valid=np.isin(episodes,old['predictive_validation_episodes']);reports=[]
for depth in (7,10):
    model=ExtraTreesRegressor(n_estimators=24,max_depth=depth,min_samples_leaf=30,max_features=.8,n_jobs=2,random_state=27092026)
    model.fit(X[~valid],Y[~valid]);prediction=model.predict(X[valid]);target=Y[valid]
    active=target.sum(axis=1)>0
    record=dict(depth=depth,ap=float(average_precision_score((target>0).ravel(),prediction.ravel())),
        quantity_rmse=float(np.sqrt(mean_squared_error(target*20,prediction*20))),
        dominant_slot_accuracy=float(np.mean(np.argmax(target[active],axis=1)==np.argmax(prediction[active],axis=1))))
    reports.append(record);print(json.dumps(record),flush=True)
best=max(reports,key=lambda r:r['ap']);model=ExtraTreesRegressor(n_estimators=24,max_depth=best['depth'],min_samples_leaf=30,max_features=.8,n_jobs=2,random_state=27092026)
model.fit(X,Y);forest=[]
for estimator in model.estimators_:
    tree=estimator.tree_;values=tree.value[:,:,0]
    forest.append([[int(tree.feature[i]),float(tree.threshold[i]),int(tree.children_left[i]),int(tree.children_right[i]),*values[i].tolist()] for i in range(tree.node_count)])
def plain(x):
    total=[0.0]*10
    for tree in forest:
        node=0
        while tree[node][0]>=0:
            row=tree[node];node=row[2] if x[row[0]]<=row[1] else row[3]
        for k in range(10):total[k]+=tree[node][4+k]
    return [x/len(forest) for x in total]
indices=np.random.default_rng(26092026).choice(len(X),2048,replace=False)
error=float(np.max(np.abs(model.predict(X[indices])-np.asarray([plain(x) for x in X[indices]]))))
assert error<1e-10,error
export=dict(forest=forest,features=31,outputs=10,
    feature_source_sha256=hashlib.sha256((N/'flow_features.py').read_bytes()).hexdigest(),
    dataset_sha256=hashlib.sha256((N/'flow_dataset.npz').read_bytes()).hexdigest())
(N/'slot_model.json').write_text(json.dumps(export,separators=(',',':')),encoding='utf-8')
report=dict(samples=len(X),internal_validation_samples=int(valid.sum()),trials=reports,selected_depth=best['depth'],
    trees=24,nodes=sum(map(len,forest)),export_parity_samples=2048,export_max_difference=error,
    model_sha256=hashlib.sha256((N/'slot_model.json').read_bytes()).hexdigest(),
    no_private_inputs=True,heldout_replays_used=False,
    scope='Internal predictive development only; not agent win-rate or score evidence.')
(N/'slot_model_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(fitted_samples=len(X),depth=best['depth'],nodes=report['nodes'],parity_error=error)),flush=True)
