"""Fit outcome differences, grouped by simulation world; not imitation or rating."""
from pathlib import Path
import hashlib,json
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import GroupKFold
D=Path(__file__).resolve().parent;R=D.parents[1];V=R/'research/value_policy_20260927'
rows=[json.loads(s) for s in (V/'training_results.jsonl').read_text().splitlines()]
jobs=json.loads((V/'training_jobs.json').read_text());expected={j['id']:j for j in jobs}
assert len(rows)==len(jobs)==len({r['id'] for r in rows})
X=[];Y=[];groups=[]
for r in rows:
    assert r['valid'] and all(r[k]==v for k,v in expected[r['id']].items())
    assert r['control']['money']==r['baseline']['money']
    for s in r['samples']:
        assert s['branch']['valid']
        X.append(s['features']);Y.append([s['gain'],float(s['gain']>0)]);groups.append(r['seed'])
X=np.asarray(X);Y=np.asarray(Y);groups=np.asarray(groups)
assert X.shape[1]==48 and np.isfinite(X).all() and np.isfinite(Y).all()
trials=[]
for depth,leaf in ((4,12),(6,8),(8,6)):
    pred=np.zeros_like(Y)
    for train,test in GroupKFold(4).split(X,Y,groups):
        model=ExtraTreesRegressor(n_estimators=48,max_depth=depth,min_samples_leaf=leaf,max_features=.9,random_state=20260927,n_jobs=2)
        model.fit(X[train],Y[train]);pred[test]=model.predict(X[test])
    mask=(pred[:,0]>5)&(pred[:,1]>.55)
    rec=dict(depth=depth,leaf=leaf,accepted=int(mask.sum()),sum_gain=float(Y[mask,0].sum()),mean_gain=float(Y[mask,0].mean()) if mask.any() else 0,negative=int((Y[mask,0]<0).sum()),mae=float(np.abs(pred[:,0]-Y[:,0]).mean()))
    trials.append(rec);print(json.dumps(rec),flush=True)
best=max(trials,key=lambda r:r['sum_gain'])
model=ExtraTreesRegressor(n_estimators=48,max_depth=best['depth'],min_samples_leaf=best['leaf'],max_features=.9,random_state=20260927,n_jobs=2).fit(X,Y)
forest=[]
for estimator in model.estimators_:
    t=estimator.tree_;values=t.value[:,:,0]
    forest.append([[int(t.feature[i]),float(t.threshold[i]),int(t.children_left[i]),int(t.children_right[i]),*values[i].tolist()] for i in range(t.node_count)])
def plain(x):
    total=np.zeros(2)
    for tree in forest:
        i=0
        while tree[i][0]>=0:
            n=tree[i];i=n[2] if x[n[0]]<=n[1] else n[3]
        total+=tree[i][4:]
    return total/len(forest)
error=float(np.abs(np.asarray([plain(x) for x in X])-model.predict(X)).max())
assert error<1e-10
feature=R/'research/v10_top10_20260926/market_bc_features.py'
record=dict(forest=forest,features=48,feature_sha256=hashlib.sha256(feature.read_bytes()).hexdigest(),training_sha256=hashlib.sha256((V/'training_results.jsonl').read_bytes()).hexdigest())
out=D/'value_model.json';assert not out.exists();out.write_text(json.dumps(record,separators=(',',':')))
report=dict(samples=len(X),worlds=len(set(groups)),trials=trials,selected=best,export_error=error,model_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),nodes=sum(map(len,forest)),scope='World-grouped predictive development, not closed-loop strength or rating. Single-intervention labels; repeated decisions require new games.')
(D/'value_training_report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report),flush=True)
