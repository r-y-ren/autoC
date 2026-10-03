"""Finite new-candidate league. Print results directly as simulations finish."""
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor,as_completed
import argparse,contextlib,io,json,sys,time
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/macro_population_20260927'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import arena

def score(rows):
    out=[];groups=defaultdict(list)
    for r in rows:groups[(r['candidate'],r.get('family',''))].append(r)
    for (candidate,family),rr in sorted(groups.items()):
        valid=[r for r in rr if r.get('valid')]
        out.append(dict(candidate=candidate,family=family,n=len(rr),invalid=len(rr)-len(valid),wins=sum(r['margin']>0 for r in valid),losses=sum(r['margin']<0 for r in valid),ties=sum(r['margin']==0 for r in valid),mean_margin=sum(r['margin'] for r in valid)/max(1,len(valid)),max_action_seconds=max([r['max_seconds'] for r in valid] or [0]),plan_breaks=sum(r.get('macro',{}).get('_MP_REPORT',{}).get('plan_breaks',0) for r in valid)))
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('output');p.add_argument('--workers',type=int,default=2)
    args=p.parse_args();manifest=Path(args.manifest).resolve();output=Path(args.output).resolve()
    assert manifest.is_relative_to(R) and output.is_relative_to(R)
    jobs=json.loads(manifest.read_text());assert len({r['id'] for r in jobs})==len(jobs)
    rows=[];started=time.perf_counter()
    with output.open('x',encoding='utf-8') as f,ProcessPoolExecutor(max_workers=max(1,min(6,args.workers))) as pool:
        print(json.dumps(dict(event='start',cases=len(jobs))),flush=True)
        futures=[pool.submit(arena.run_job,j) for j in jobs]
        for future in as_completed(futures):
            row=future.result();rows.append(row);f.write(json.dumps(row)+'\n');f.flush()
            if len(jobs)<=32:
                print(json.dumps(dict(candidate=row['candidate'],seed=row['seed'],seat=row['seat'],valid=row.get('valid'),margin=row.get('margin'),telemetry=row.get('macro',{}).get('_MP_REPORT',{}),exception=row.get('exception','')[-500:])),flush=True)
            elif len(rows)%64==0 or not row.get('valid'):
                print(json.dumps(dict(event='progress',done=len(rows),total=len(jobs),invalid=sum(not r.get('valid') for r in rows))),flush=True)
    summary=dict(event='complete',cases=len(rows),invalid=sum(not r.get('valid') for r in rows),elapsed=time.perf_counter()-started,groups=score(rows))
    output.with_suffix('.summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary),flush=True)
