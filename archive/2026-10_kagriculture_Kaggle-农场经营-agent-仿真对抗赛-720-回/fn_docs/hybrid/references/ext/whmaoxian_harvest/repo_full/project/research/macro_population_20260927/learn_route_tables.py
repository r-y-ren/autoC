"""Learn a conservative shop-conditioned route choice from complete local games."""
from pathlib import Path
from collections import defaultdict
import hashlib,json,math,statistics
D=Path(__file__).resolve().parent

def points(row):return 1.0 if row['margin']>0 else .5 if row['margin']==0 else 0.0

def shop_key(shops,coarse):
    shops=tuple(shops[:2])
    if not coarse:return '|'.join(sorted(shops))
    milk=sum(s in ('PIZZA_SHOP','ICE_CREAM_SHOP','SMOOTHIE_SHOP') for s in shops)
    egg=sum(s in ('BAKERY','BRUNCH_SPOT') for s in shops)
    return 'C:'+','.join(map(str,(shops.count('YARN_STORE'),milk,egg,shops.count('PET_CAFE'),shops.count('FARMERS_MARKET'))))

def fit(rows,baseline,coarse,penalty,min_worlds,skip_world=None):
    groups=defaultdict(lambda:defaultdict(list))
    for row in rows:
        if row['seed']==skip_world or row['candidate']==baseline:continue
        original=LOOKUP[(row['opponent'],row['seed'],row['seat'])]
        if not row['valid'] or not original['valid']:continue
        key=shop_key(row['shops'],coarse)
        if key!=shop_key(original['shops'],coarse):raise ValueError('Decision context differs before route switch')
        delta=points(row)-points(original)
        margin=max(-2000,min(2000,row['margin']-original['margin']))/2000
        weight=.35 if row['family']=='r2' else 1.0
        score=weight*(delta+.08*margin)
        groups[(key,row['candidate'])][row['seed']].append(score)
    table={};evidence={}
    for (key,candidate),worlds in groups.items():
        values=[statistics.mean(v) for v in worlds.values()]
        if len(values)<min_worlds:continue
        mean=statistics.mean(values)
        sem=statistics.stdev(values)/math.sqrt(len(values)) if len(values)>1 else 1.0
        lower=mean-penalty*sem
        if lower<=.015 or mean<=.02:continue
        if key not in evidence or lower>evidence[key]['selection_score']:
            table[key]=candidate
            evidence[key]=dict(candidate=candidate,worlds=len(values),mean_score=mean,standard_error=sem,selection_score=lower)
    return table,evidence

def measure(table,coarse,world):
    rows=[r for r in BASE_ROWS if r['seed']==world];out=[]
    for original in rows:
        choice=table.get(shop_key(original['shops'],coarse),BASE)
        actual=ALL[(choice,original['opponent'],world,original['seat'])]
        out.append(dict(seed=world,family=original['family'],candidate=choice,point_delta=points(actual)-points(original),margin_delta=actual['margin']-original['margin'],valid=actual['valid']))
    return out

def summarize(rows):
    external=[r for r in rows if r['family']!='r2']
    direct=[r for r in rows if r['family']=='r2']
    gain=statistics.mean(r['point_delta'] for r in external)
    direct_gain=statistics.mean(r['point_delta'] for r in direct)
    margin=statistics.mean(max(-2000,min(2000,r['margin_delta'])) for r in external)
    return dict(external_gain=gain,direct_gain=direct_gain,clipped_margin_gain=margin,selection_score=gain+.1*direct_gain+.00004*margin,changed_games=sum(r['candidate']!=BASE for r in rows),invalid=sum(not r['valid'] for r in rows))
if __name__=='__main__':
    design=json.loads((D/'route_learning_design.json').read_text())
    raw=[json.loads(line) for line in (D/'route_learning_results.jsonl').read_text().splitlines()]
    assert len(raw)==design['total_games'] and len({r['id'] for r in raw})==len(raw)
    BASE=next(v['path'] for v in design['variants'] if v['route'] is None)
    BASE_ROWS=[r for r in raw if r['candidate']==BASE]
    assert all(r['valid'] for r in BASE_ROWS)
    LOOKUP={(r['opponent'],r['seed'],r['seat']):r for r in BASE_ROWS}
    ALL={(r['candidate'],r['opponent'],r['seed'],r['seat']):r for r in raw}
    rejected={r['candidate'] for r in raw if not r['valid']}
    rows=[r for r in raw if r['candidate'] not in rejected]
    trials=[]
    for coarse in (False,True):
        for penalty in (0.0,1.0,2.0):
            for minimum in (3,5):
                predictions=[]
                for world in design['seeds']:
                    table,_=fit(rows,BASE,coarse,penalty,minimum,skip_world=world)
                    predictions.extend(measure(table,coarse,world))
                trial=dict(coarse=coarse,penalty=penalty,min_worlds=minimum,metrics=summarize(predictions))
                trials.append(trial);print(json.dumps(trial),flush=True)
    selected=max(trials,key=lambda t:(t['metrics']['selection_score'],t['penalty'],t['min_worlds']))
    table,evidence=fit(rows,BASE,selected['coarse'],selected['penalty'],selected['min_worlds'])
    route_map={v['path']:v['route'] for v in design['variants']}
    model=dict(table={k:route_map[v] for k,v in table.items()},selected=selected,development_trials=trials,evidence=evidence,rejected_programs=sorted(rejected),baseline=BASE,source_ledger_sha256=hashlib.sha256((D/'route_learning_results.jsonl').read_bytes()).hexdigest(),validation_scope='Leave-one-world-out development for selecting settings; not final independent validation.',online_rating=None,released=False)
    (D/'route_choice_model.json').write_text(json.dumps(model,indent=2))
    print(json.dumps(dict(rules=len(table),selected=selected,independent_validation_pending=True)),flush=True)
