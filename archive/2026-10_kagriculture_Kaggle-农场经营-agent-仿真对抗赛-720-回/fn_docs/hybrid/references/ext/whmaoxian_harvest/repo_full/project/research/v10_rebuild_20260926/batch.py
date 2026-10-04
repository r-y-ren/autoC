"""Finite, resumable screening batches with frozen manifests and bounded workers."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import argparse, hashlib, json, statistics
import fast_arena
ROOT=fast_arena.ROOT

def main():
    p=argparse.ArgumentParser()
    p.add_argument('manifest'); p.add_argument('output'); p.add_argument('--workers',type=int,default=6)
    a=p.parse_args(); manifest=Path(a.manifest); out=Path(a.output)
    jobs=json.loads(manifest.read_text(encoding='utf-8'))
    for job in jobs:
        for key in ('candidate','opponent'):
            raw=(ROOT/job[key]).read_bytes()
            assert hashlib.sha256(raw).hexdigest()==job[key+'_sha256'],job[key]
    prior=[json.loads(line) for line in out.read_text(encoding='utf-8').splitlines()] if out.exists() else []
    done={r['id'] for r in prior}; pending=[j for j in jobs if j['id'] not in done]
    print(json.dumps(dict(total=len(jobs),existing=len(prior),pending=len(pending))),flush=True)
    with ProcessPoolExecutor(max_workers=a.workers) as pool, out.open('a',encoding='utf-8') as handle:
        futures={pool.submit(fast_arena.run_job,job):job for job in pending}
        for future in as_completed(futures):
            row=future.result(); prior.append(row)
            handle.write(json.dumps(row,ensure_ascii=False)+'\n'); handle.flush()
            if len(prior)%12==0 or not row.get('valid'):
                print(json.dumps(dict(done=len(prior),total=len(jobs),valid=row.get('valid'),
                    candidate=Path(row['candidate']).name,margin=row.get('margin'))),flush=True)
    summary={}
    for name in sorted({row['candidate'] for row in prior}):
        panels={}
        for panel in sorted({row.get('panel','unspecified') for row in prior if row['candidate']==name}):
            group=[r for r in prior if r['candidate']==name and r.get('panel','unspecified')==panel]
            good=[r for r in group if r.get('valid')]
            panels[panel]=dict(games=len(group),invalid=len(group)-len(good),
                wins=sum(r['margin']>0 for r in good),ties=sum(r['margin']==0 for r in good),
                mean_margin=statistics.mean(r['margin'] for r in good) if good else None)
        summary[name]=panels
    out.with_suffix('.summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary),flush=True)
if __name__=='__main__':
    main()
