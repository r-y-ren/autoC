"""Fit and export arithmetic trees; episode split is predictive development only."""
from pathlib import Path
import hashlib,json
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import average_precision_score,roc_auc_score,mean_squared_error
D=Path(__file__).resolve().parent
arrays=np.load(D/'market_bc_dataset.npz');X=arrays['X'];Y=arrays['Y'];groups=arrays['episode'];available=arrays['available']
manifest=json.loads((D/'market_bc_dataset_manifest.json').read_text())
assert hashlib.sha256((D/'market_bc_features.py').read_bytes()).hexdigest()==manifest['feature_source_sha256']
assert X.shape[1]==manifest['features'] and np.isfinite(X).all()
unique=sorted(set(groups.tolist()),key=lambda e:hashlib.sha256(f'own-market-predictive-split-{e}'.encode()).hexdigest())
validation=unique[:max(4,len(unique)//4)];valid=np.isin(groups,validation);train=~valid
reports=[]
for depth in (9,12):
    model=ExtraTreesRegressor(n_estimators=24,max_depth=depth,min_samples_leaf=25,max_features=.9,n_jobs=2,random_state=20260927)
    model.fit(X[train],Y[train]);pred=model.predict(X[valid]);confident=pred[:,0]>=.9
    metrics=dict(depth=depth,auc=float(roc_auc_score(Y[valid,0],pred[:,0])),ap=float(average_precision_score(Y[valid,0],pred[:,0])),brier=float(mean_squared_error(Y[valid,0],pred[:,0])),fraction_mae=float(np.abs(pred[:,1]-Y[valid,1]).mean()),quantity_mae=float((np.abs(pred[:,1]-Y[valid,1])*available[valid]).mean()),high_confidence_count=int(confident.sum()),high_confidence_precision=float(Y[valid,0][confident].mean()) if confident.any() else None)
    reports.append(metrics);print(json.dumps(metrics),flush=True)
selected=max(reports,key=lambda x:x['ap']-.05*x['fraction_mae'])
model=ExtraTreesRegressor(n_estimators=24,max_depth=selected['depth'],min_samples_leaf=25,max_features=.9,n_jobs=2,random_state=20260927)
model.fit(X,Y);forest=[]
for estimator in model.estimators_:
    tree=estimator.tree_;values=tree.value[:,:,0]
    forest.append([[int(tree.feature[i]),float(tree.threshold[i]),int(tree.children_left[i]),int(tree.children_right[i]),*values[i].tolist()] for i in range(tree.node_count)])
def plain(x):
    sums=[0.0,0.0]
    for tree in forest:
        node=0
        while tree[node][0]>=0:
            row=tree[node];node=row[2] if x[row[0]]<=row[1] else row[3]
        for i in range(2):sums[i]+=tree[node][4+i]
    return [v/len(forest) for v in sums]
indices=np.random.default_rng(20260927).choice(len(X),size=min(2048,len(X)),replace=False)
error=float(np.max(np.abs(np.asarray([plain(x) for x in X[indices]])-model.predict(X[indices]))));assert error<1e-10
export=dict(forest=forest,features=manifest['features'],feature_source_sha256=manifest['feature_source_sha256'],dataset_sha256=manifest['dataset_sha256'])
output=D/'market_bc_model.json';assert not output.exists()
output.write_text(json.dumps(export,separators=(',',':')),encoding='utf-8')
report=dict(training_samples=int(train.sum()),predictive_validation_samples=int(valid.sum()),predictive_validation_episodes=validation,trials=reports,selected_depth=selected['depth'],trees=len(forest),nodes=sum(len(t) for t in forest),export_parity_samples=len(indices),export_max_difference=error,model_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),input_scope=manifest['input_scope'],heldout_agent_replays_used=False,scope='Predictive imitation accuracy is not match strength or a leaderboard rating. Final model refitted on declared study data only.')
(D/'market_bc_model_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(samples=len(X),nodes=report['nodes'],parity_error=error,selected_depth=selected['depth'])),flush=True)
