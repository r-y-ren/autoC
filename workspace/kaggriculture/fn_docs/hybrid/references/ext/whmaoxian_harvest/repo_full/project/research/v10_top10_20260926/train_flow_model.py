"""Train a compact observable-flow forest; export arithmetic trees, not pickle code."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import roc_auc_score,average_precision_score,mean_squared_error
N=Path(__file__).resolve().parent
arrays=np.load(N/'flow_dataset.npz');X=arrays['X'];Y=arrays['Y'];groups=arrays['episode']
manifest=json.loads((N/'flow_dataset_manifest.json').read_text())
assert hashlib.sha256((N/'flow_features.py').read_bytes()).hexdigest()==manifest['feature_source_sha256']
unique=sorted(set(groups.tolist()),key=lambda x:hashlib.sha256(f'flow-predictive-split-{x}'.encode()).hexdigest())
validation_episodes=unique[:max(4,len(unique)//4)]
valid=np.isin(groups,validation_episodes);train=~valid
reports=[]
for depth in (6,9):
    model=ExtraTreesRegressor(n_estimators=24,max_depth=depth,min_samples_leaf=40,
        max_features=.8,n_jobs=2,random_state=20260926)
    model.fit(X[train],Y[train]);prediction=model.predict(X[valid])
    metrics=dict(depth=depth,samples=int(valid.sum()),
        auc_now=float(roc_auc_score(Y[valid,0],prediction[:,0])),
        ap_now=float(average_precision_score(Y[valid,0],prediction[:,0])),
        auc_soon=float(roc_auc_score(Y[valid,1],prediction[:,1])),
        ap_soon=float(average_precision_score(Y[valid,1],prediction[:,1])),
        brier_soon=float(mean_squared_error(Y[valid,1],prediction[:,1])),
        volume_rmse=float(np.sqrt(mean_squared_error(Y[valid,2]*20,prediction[:,2]*20))))
    reports.append(metrics);print(json.dumps(metrics),flush=True)
best=max(reports,key=lambda m:m['ap_soon']+m['ap_now'])
model=ExtraTreesRegressor(n_estimators=24,max_depth=best['depth'],min_samples_leaf=40,max_features=.8,n_jobs=2,random_state=20260926)
model.fit(X,Y)
forest=[]
for estimator in model.estimators_:
    tree=estimator.tree_;values=tree.value[:,:,0]
    forest.append([[int(tree.feature[i]),float(tree.threshold[i]),int(tree.children_left[i]),
        int(tree.children_right[i]),*values[i].tolist()] for i in range(tree.node_count)])
def predict_plain(x):
    sums=[0.0,0.0,0.0]
    for tree in forest:
        node=0
        while tree[node][0]>=0:
            row=tree[node];node=row[2] if x[row[0]]<=row[1] else row[3]
        for i in range(3):sums[i]+=tree[node][4+i]
    return [value/len(forest) for value in sums]
indices=np.random.default_rng(20260926).choice(len(X),size=2048,replace=False)
expected=model.predict(X[indices]);actual=np.asarray([predict_plain(x) for x in X[indices]])
error=float(np.max(np.abs(expected-actual)));assert error<1e-10,error
export=dict(forest=forest,feature_source_sha256=manifest['feature_source_sha256'],
    dataset_sha256=manifest['dataset_sha256'],features=31,outputs=manifest['labels'])
(N/'flow_model.json').write_text(json.dumps(export,separators=(',',':')),encoding='utf-8')
report=dict(created_utc=datetime.now(timezone.utc).isoformat(),predictive_validation_episodes=validation_episodes,
    training_samples=int(train.sum()),predictive_validation_samples=int(valid.sum()),
    trials=reports,selected_depth=best['depth'],trees=24,nodes=sum(map(len,forest)),
    export_parity_samples=2048,export_max_difference=error,
    model_sha256=hashlib.sha256((N/'flow_model.json').read_bytes()).hexdigest(),
    no_private_inputs=True,no_episode_or_team_inputs=True,final_heldout_replays_used=False,
    scope='Predictive validation is internal study-set development, not agent strength or a rating estimate.')
(N/'flow_model_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(fitted_samples=len(X),depth=best['depth'],nodes=report['nodes'],parity_error=error)),flush=True)
