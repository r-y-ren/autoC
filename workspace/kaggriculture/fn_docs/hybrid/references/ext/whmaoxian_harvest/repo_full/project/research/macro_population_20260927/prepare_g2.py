"""Select completed generation-one elites, then freeze fresh offspring tests."""
from pathlib import Path
import hashlib,json,random
from report import summarize,load
from build_population import build,space,default
D=Path(__file__).resolve().parent;R=D.parents[1];BASE='submissions/release_v10_r2/main.py'
report=summarize('g1_results.jsonl');rows=load('g1_results.jsonl')
assert len(rows)==len(json.loads((D/'g1_jobs.json').read_text()))==1296
variants=json.loads((D/'population_g1.json').read_text());by_path={v['path']:v for v in variants}
good=[g for g in report['groups'] if g['candidate'] in by_path and not g['invalid'] and g['families']['r2']['points']>=.5]
def key(g):
    external=[v for k,v in g['families'].items() if k!='r2']
    return (g['external_gain'],min(v['gain'] for v in external),sum(v['margin_gain'] for v in external))
elites=[];signatures=set()
for g in sorted(good,key=key,reverse=True):
    signature=tuple((r['opponent'],r['seed'],r['seat'],tuple(r['money'])) for r in sorted((r for r in rows if r['candidate']==g['candidate']),key=lambda r:(r['opponent'],r['seed'],r['seat'])))
    if signature in signatures:continue
    signatures.add(signature);elites.append(by_path[g['candidate']])
    if len(elites)==4:break
assert elites
invalid_caps={by_path[g['candidate']]['genome']['hire_cap'] for g in report['groups'] if g['candidate'] in by_path and g['invalid']}
allowed={k:[v for v in values if k!='hire_cap' or v not in invalid_caps] for k,values in space.items()}
rng=random.Random(27102026);offspring=[];seen=[v['genome'] for v in variants]
while len(offspring)<8:
    a,b=rng.choices(elites,k=2);g={k:rng.choice([a['genome'][k],b['genome'][k]]) for k in space}
    for k in rng.sample(list(space),rng.choice([1,2])):g[k]=rng.choice(allowed[k])
    if any(g[k] not in allowed[k] for k in space) or g in seen:continue
    seen.append(g);offspring.append(build(g))
all_valid=[g for g in report['groups'] if g['candidate'] in by_path and not g['invalid'] and g['changed_economic_cases']>0]
parents=sorted(all_valid,key=key,reverse=True)[:2]
roster=json.loads((D/'roster.json').read_text())
roster += [dict(path=g['candidate'],family='evolved_'+str(i+1),panel='evolved_population') for i,g in enumerate(parents)]
worlds=json.loads((D/'worlds.json').read_text())['g2']
selected=elites+offspring;paths=[v['path'] for v in selected]+[BASE];jobs=[]
for candidate in paths:
    for opponent in roster:
        for seed in worlds:
            for seat in (0,1):
                j=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for k in ('candidate','opponent'):j[k+'_sha256']=hashlib.sha256((R/j[k]).read_bytes()).hexdigest()
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'population_g2.json').write_text(json.dumps(selected,indent=2))
(D/'g2_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'g2_design.json').write_text(json.dumps(dict(elites=elites,offspring=offspring,invalid_hire_caps_excluded=sorted(invalid_caps),roster=roster,worlds=worlds,g1_ledger_sha256=report['sha256'],jobs=len(jobs),scope='Fresh developmental worlds; not final confirmation.'),indent=2))
print(json.dumps(dict(elites=len(elites),offspring=len(offspring),jobs=len(jobs),excluded_caps=sorted(invalid_caps),parent_opponents=len(parents))),flush=True)
