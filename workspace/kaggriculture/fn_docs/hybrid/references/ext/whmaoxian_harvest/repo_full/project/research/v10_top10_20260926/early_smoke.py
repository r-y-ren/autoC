"""Bounded full-game functional audit; no release or online submission."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import contextlib, hashlib, io, json, sys
D=Path(__file__).resolve().parent; R=D.parents[1]
def run(job):
    sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        import fast_arena as fa
    original=fa.load; entries={}
    def observed(path):
        entry=original(path); entries[path]=entry
        return entry
    fa.load=observed
    try:
        result=fa.run_job(job)
        entry=entries.get(job['candidate'])
        if entry:
            ns=entry.__globals__
            result['production_report']=dict(ns.get('_EP_REPORT',{}))
            result['forecast']=dict(ns.get('_EP_LAST_FORECAST',{}))
            result['production_state']={str(k):{a:v for a,v in st.items() if a in ('eligible','committed','t19_enabled','day')} for k,st in ns.get('_EP_STATE',{}).items()}
        return result
    finally:fa.load=original
def main():
    variants=json.loads((D/'early_production_manifest.json').read_text())
    candidates=[v['path'] for v in variants]+['submissions/release_v10_r2/main.py']
    design=json.loads((D/'route_expansion_design.json').read_text())
    roster=[x for x in design['roster'] if x['family'] in ('fieldcraft','top_style_03')]
    seeds=[*design['seeds'][:2],688041503]
    jobs=[]
    for candidate in candidates:
        for opponent in roster:
            for seed in seeds:
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel='functional_development',seed=seed,seat=0)
                for key in ('candidate','opponent'):job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
    target=D/'early_smoke_results.jsonl'
    assert not target.exists(),'Do not overwrite an earlier run'
    (D/'early_smoke_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
    with ProcessPoolExecutor(max_workers=4) as pool,target.open('w',encoding='utf-8') as handle:
        for future in as_completed([pool.submit(run,j) for j in jobs]):
            row=future.result();handle.write(json.dumps(row)+'\n');handle.flush()
            print(json.dumps({k:row.get(k) for k in ('candidate','family','seed','valid','margin','production_report','forecast','production_state')}),flush=True)
if __name__=='__main__':main()
