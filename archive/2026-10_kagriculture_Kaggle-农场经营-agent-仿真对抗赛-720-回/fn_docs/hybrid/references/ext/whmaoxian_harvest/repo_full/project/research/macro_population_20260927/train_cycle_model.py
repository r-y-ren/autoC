"""Episode-grouped development of a compact commodity-order predictor."""
from pathlib import Path
import hashlib,json
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import average_precision_score,roc_auc_score,mean_squared_error
D=Path(__file__).resolve().parent;data=np.load(D/'cycle_dataset.npz')
X=data['X'];Y=data['Y'];groups=data['episode'];manifest=json.loads((D/'cycle_dataset_manifest.json').read_text())
assert hashlib.sha256((D/'cycle_features.py').read_bytes()).hexdigest()==manifest['feature_sha256']
episodes=sorted(set(groups.tolist()),key=lambda e:hashlib.sha256(f'cycle-development-{e}'.encode()).hexdigest())
validation=episodes[:max(4,len(episodes)//4)];valid=np.isin(groups,validation);reports=[]
for depth in (7,10):
    model=ExtraTreesRegressor(n_estimators=24,max_depth=depth,min_samples_leaf=20,max_features=.9,n_jobs=2,random_state=20260927)
    model.fit(X[~valid],Y[~valid]);pred=model.predict(X[valid]);metrics=[]
    for j,name in enumerate(('buy','sell')):
        mask=pred[:,j]>=.65
        metrics.append(dict(side=name,auc=float(roc_auc_score(Y[valid,j],pred[:,j])),ap=float(average_precision_score(Y[valid,j],pred[:,j])),brier=float(mean_squared_error(Y[valid,j],pred[:,j])),confident_count=int(mask.sum()),confident_precision=float(Y[valid,j][mask].mean()) if mask.any() else None))
    row=dict(depth=depth,metrics=metrics,quantity_mae=float(np.abs(pred[:,2:]-Y[valid,2:]).mean()*40))
    reports.append(row);print(json.dumps(row),flush=True)
selected=max(reports,key=lambda r:sum(m['ap'] for m in r['metrics'])-.01*r['quantity_mae'])
model=ExtraTreesRegressor(n_estimators=24,max_depth=selected['depth'],min_samples_leaf=20,max_features=.9,n_jobs=2,random_state=20260927)
model.fit(X,Y);forest=[]
for estimator in model.estimators_:
    tree=estimator.tree_;values=tree.value[:,:,0]
    forest.append([[int(tree.feature[i]),float(tree.threshold[i]),int(tree.children_left[i]),int(tree.children_right[i]),*values[i].tolist()] for i in range(tree.node_count)])
def plain(x):
    sums=[0.0]*4
    for tree in forest:
        node=0
        while tree[node][0]>=0:
            row=tree[node];node=row[2] if x[row[0]]<=row[1] else row[3]
        for j in range(4):sums[j]+=tree[node][4+j]
    return [v/len(forest) for v in sums]
indices=np.random.default_rng(20260927).choice(len(X),min(2048,len(X)),replace=False)
actual=np.asarray([plain(x) for x in X[indices]]);expected=model.predict(X[indices])
error=float(np.abs(actual-expected).max());assert error<1e-10
output=D/'cycle_model.json';assert not output.exists()
output.write_text(json.dumps(dict(forest=forest,features=manifest['features'],feature_sha256=manifest['feature_sha256'],dataset_sha256=manifest['dataset_sha256']),separators=(',',':')))
report=dict(training_rows=int((~valid).sum()),validation_rows=int(valid.sum()),validation_episodes=validation,trials=reports,selected_depth=selected['depth'],trees=len(forest),nodes=sum(map(len,forest)),export_parity_rows=len(indices),export_error=error,model_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),input_scope=manifest['input_scope'],heldout_agent_tests_used=False,scope='Forecast validation only. No claim of strategy strength or rating.')
(D/'cycle_model_report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(nodes=report['nodes'],parity_error=error,model_sha256=report['model_sha256'])),flush=True)
