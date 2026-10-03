"""Pair actual complete-game route outcomes with causal day-six observations."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import copy,hashlib,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/macro_population_20260927'
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as fa
from features import features,FEATURE_COUNT

def prefix(job):
    own=fa.load(job['baseline']);other=fa.load(job['opponent'])
    entries=[own,other] if job['seat']==0 else [other,own]
    state,env=fa.new_game(job['seed']);hashes=[hashlib.sha256(),hashlib.sha256()]
    for step in range(144):
        for seat,entry in enumerate(entries):
            state[seat].observation.step=step
            action=entry(copy.deepcopy(state[seat].observation),env.configuration)
            state[seat].action=copy.deepcopy(action)
            hashes[seat].update(json.dumps(action,sort_keys=True).encode())
        fa.engine.interpreter(state,env)
    obs=copy.deepcopy(state[job['seat']].observation);obs.step=144
    x=features(obs);assert len(x)==FEATURE_COUNT
    return dict(job,x=x,shops=list(obs['town']['unlocked_shops']),
                prefix_actions=[h.hexdigest() for h in hashes],
                observation_sha256=hashlib.sha256(json.dumps(obs,sort_keys=True).encode()).hexdigest())

if __name__=='__main__':
    design=json.loads((M/'route_learning_design.json').read_text())
    jobs=json.loads((M/'route_learning_jobs.json').read_text())
    rows=[json.loads(s) for s in (M/'route_learning_results.jsonl').read_text().splitlines()]
    expected={j['id']:j for j in jobs};assert len(rows)==len(expected)==design['total_games']
    assert len({r['id'] for r in rows})==len(rows) and all(r['valid'] for r in rows)
    for row in rows:assert all(row[k]==v for k,v in expected[row['id']].items())
    variants=design['variants'];baseline=next(v['path'] for v in variants if v['route'] is None)
    for v in variants:assert hashlib.sha256((R/v['path']).read_bytes()).hexdigest()==v['sha256']
    bycase={}
    for row in rows:bycase.setdefault((row['opponent'],row['seed'],row['seat']),{})[row['candidate']]=row
    tasks=[dict(opponent=k[0],seed=k[1],seat=k[2],baseline=baseline) for k in bycase]
    output=D/'prefixes.jsonl';assert not output.exists(),'Preserve prior prefix evidence'
    samples=[]
    with ProcessPoolExecutor(max_workers=6) as pool,output.open('w',encoding='utf-8') as handle:
        for future in as_completed([pool.submit(prefix,j) for j in tasks]):
            p=future.result();case=bycase[(p['opponent'],p['seed'],p['seat'])]
            assert all(r['shops'][:2]==p['shops'][:2] for r in case.values())
            p['family']=case[baseline]['family'];p['panel']=case[baseline]['panel']
            p['outcomes']=[dict(margin=case[v['path']]['margin'],money=case[v['path']]['money']) for v in variants]
            samples.append(p);handle.write(json.dumps(p)+'\n');handle.flush()
            if len(samples)%48==0:print(json.dumps(dict(prefixes=len(samples),required=len(tasks))),flush=True)
    report=dict(samples=len(samples),features=FEATURE_COUNT,worlds=len(design['seeds']),variants=variants,
      source_ledger_sha256=hashlib.sha256((M/'route_learning_results.jsonl').read_bytes()).hexdigest(),
      feature_sha256=hashlib.sha256((D/'features.py').read_bytes()).hexdigest(),
      dataset_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
      scope='Complete-game supervised route outcomes. All data are development, not final confirmation.')
    (D/'dataset_manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report),flush=True)
