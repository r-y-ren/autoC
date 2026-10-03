"""Outcome-based macro selector; grouped development and arithmetic tree export."""
from pathlib import Path
import hashlib,json
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import GroupKFold
D=Path(__file__).resolve().parent

def metrics(choice,win,margin,family):
    ix=np.arange(len(choice));delta=win[ix,choice]-win[:,0]
    external=family!='r2';direct=~external
    groups={str(f):float(delta[family==f].mean()) for f in np.unique(family)}
    return dict(external_gain=float(delta[external].mean()),direct_gain=float(delta[direct].mean()),
       external_wins=float(win[ix[external],choice[external]].sum()),baseline_wins=float(win[external,0].sum()),
       external_games=int(external.sum()),family_gain=groups,changed=int((choice!=0).sum()),
       clipped_margin_gain=float(np.clip(margin[ix,choice]-margin[:,0],-5000,5000)[external].mean()))

def choose(prediction,threshold):
    score=prediction.copy();score[:,0]=0.0
    best=np.argmax(score,axis=1)
    best[score[np.arange(len(best)),best]<threshold]=0
    return best

if __name__=='__main__':
    manifest=json.loads((D/'dataset_manifest.json').read_text())
    assert hashlib.sha256((D/'prefixes.jsonl').read_bytes()).hexdigest()==manifest['dataset_sha256']
    rows=[json.loads(s) for s in (D/'prefixes.jsonl').read_text().splitlines()]
    X=np.asarray([r['x'] for r in rows],dtype=np.float32)
    margins=np.asarray([[o['margin'] for o in r['outcomes']] for r in rows])
    wins=(margins>0).astype(float)+.5*(margins==0)
    family=np.asarray([r['family'] for r in rows]);world=np.asarray([r['seed'] for r in rows])
    target=wins-wins[:,0,None]+.08*np.clip((margins-margins[:,0,None])/4000,-1,1)
    weight=np.where(family=='r2',.4,1.0)
    folds=list(GroupKFold(n_splits=8).split(X,target,world));trials=[];predictions={}
    for depth in (4,7,10):
        for leaf in (8,20,40):
            pred=np.zeros_like(target)
            for train,test in folds:
                forest=ExtraTreesRegressor(n_estimators=96,max_depth=depth,min_samples_leaf=leaf,
                    max_features=.8,n_jobs=2,random_state=927)
                forest.fit(X[train],target[train],sample_weight=weight[train]);pred[test]=forest.predict(X[test])
            predictions[(depth,leaf)]=pred
            for threshold in (.025,.075,.15):
                choice=choose(pred,threshold);m=metrics(choice,wins,margins,family)
                score=m['external_gain']+.2*m['direct_gain']+.000005*m['clipped_margin_gain']
                score-=.5*max(0,-min(m['family_gain'].values())-.05)
                row=dict(depth=depth,leaf=leaf,threshold=threshold,metrics=m,score=score)
                trials.append(row);print(json.dumps(row),flush=True)
    best=max(trials,key=lambda r:(r['score'],r['leaf'],-r['depth'],r['threshold']))
    model=ExtraTreesRegressor(n_estimators=96,max_depth=best['depth'],min_samples_leaf=best['leaf'],
        max_features=.8,n_jobs=2,random_state=927)
    model.fit(X,target,sample_weight=weight);export=[]
    for estimator in model.estimators_:
        tree=estimator.tree_;values=tree.value[:,:,0]
        export.append([[int(tree.feature[i]),float(tree.threshold[i]),int(tree.children_left[i]),
            int(tree.children_right[i]),*values[i].tolist()] for i in range(tree.node_count)])
    def plain(x):
        sums=np.zeros(target.shape[1])
        for tree in export:
            node=0
            while tree[node][0]>=0:
                f,t,left,right=tree[node][:4];node=left if x[f]<=t else right
            sums+=tree[node][4:]
        return sums/len(export)
    difference=float(np.max(np.abs(np.asarray([plain(x) for x in X])-model.predict(X))))
    assert difference<1e-10
    held_family=[]
    for f in np.unique(family):
        train=family!=f;test=~train
        check=ExtraTreesRegressor(n_estimators=96,max_depth=best['depth'],min_samples_leaf=best['leaf'],
            max_features=.8,n_jobs=2,random_state=927)
        check.fit(X[train],target[train],sample_weight=weight[train])
        choice=choose(check.predict(X[test]),best['threshold']);ix=np.arange(int(test.sum()))
        held_family.append(dict(family=str(f),games=int(test.sum()),
            gain=float((wins[test][ix,choice]-wins[test,0]).mean()),changed=int((choice!=0).sum())))
    exported=dict(forest=export,routes=[v['route'] for v in manifest['variants']],
        threshold=best['threshold'],features=manifest['features'],feature_sha256=manifest['feature_sha256'])
    (D/'model.json').write_text(json.dumps(exported,separators=(',',':')),encoding='utf-8')
    report=dict(best=best,trials=trials,leave_family_out=held_family,parity_max_difference=difference,
        samples=len(X),worlds=len(set(world.tolist())),feature_count=X.shape[1],
        oracle_external_win_points=float(np.max(wins[family!='r2'],axis=1).sum()),
        baseline_external_win_points=float(wins[family!='r2',0].sum()),
        scope='Grouped out-of-fold DEVELOPMENT after settings selection, not independent confirmation or rating.',
        model_sha256=hashlib.sha256((D/'model.json').read_bytes()).hexdigest())
    (D/'training_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(dict(best=best,leave_family_out=held_family,parity=difference)),flush=True)
