"""Test documented execution-guard settings on existing public route proxies."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'guard_ablations';out.mkdir(exist_ok=True)
roster=json.loads((D/'study_opponents.json').read_text(encoding='utf-8'))
design=json.loads((D/'extended_design.json').read_text(encoding='utf-8'))
seeds=design['seeds'][:2]
opponents=[r for r in design['roster'] if r['family'] in ('r2','fieldcraft','top_style_03')]
assert len(opponents)==3
settings=[('default',{}),('no_budget',{'budget_guard':False}),('no_dead',{'dead_stock':False}),('minimal',{'budget_guard':False,'dead_stock':False,'sell_lead':False}),('trace_market',{'budget_guard':False,'dead_stock':False,'sell_lead':False,'clamp_sells':False,'room_guard':False})]
manifest=[];jobs=[]
for proxy in roster:
    source=(R/proxy['path']).read_bytes();assert hashlib.sha256(source).hexdigest()==proxy['sha256']
    text=source.decode('utf-8');marker='_PROXY=make_agent({0:_DEMO})'
    assert text.count(marker)==1
    for label,options in settings:
        replacement='_PROXY=make_agent({0:_DEMO}'+''.join(','+k+'='+repr(v) for k,v in options.items())+')'
        candidate_text=text.replace(marker,replacement)
        path=out/(proxy['family']+'_'+label+'.py');compile(candidate_text,str(path),'exec')
        if path.exists():assert path.read_bytes()==candidate_text.encode('utf-8')
        else:path.write_bytes(candidate_text.encode('utf-8'))
        candidate=path.relative_to(R).as_posix();sha=hashlib.sha256(path.read_bytes()).hexdigest()
        manifest.append(dict(path=candidate,sha256=sha,source=proxy['path'],source_sha256=proxy['sha256'],settings=options,scope='Local reactive replay proxy, not the original private agent.'))
        for opponent in opponents:
            for seed in seeds:
                for seat in (0,1):
                    job=dict(candidate=candidate,opponent=opponent['path'],seed=seed,seat=seat,family=opponent['family'],panel='guard_development',candidate_sha256=sha,opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest())
                    job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
assert len(manifest)==50 and len(jobs)==600
(D/'guard_ablations_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(D/'guard_ablations_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest),games=len(jobs),worlds=len(seeds),opponents=len(opponents),new_release=False)),flush=True)
