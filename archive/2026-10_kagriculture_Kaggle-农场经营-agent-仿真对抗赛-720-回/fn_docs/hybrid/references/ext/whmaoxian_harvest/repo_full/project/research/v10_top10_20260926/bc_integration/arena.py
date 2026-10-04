"""Explicit finite batches using unchanged official transitions; no online submission."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib, json, sys
B=Path(__file__).resolve().parent; R=B.parents[2]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as fa

def run(job):
    captured=[]; original=fa.load
    def load(path):
        entry=original(path); captured.append(entry); return entry
    fa.load=load
    try:
        row=fa.run_job(job)
        if captured:
            row['bc_telemetry']=dict(captured[0].__globals__.get('_MBC_STATS',{}))
        return row
    finally:
        fa.load=original

def batch(pool,command):
    jobs=json.loads(Path(command['manifest']).read_text(encoding='utf-8'))
    output=Path(command['output']); expected={j['id']:j for j in jobs}
    assert len(expected)==len(jobs)
    for path,digest in {(j[k],j[k+'_sha256']) for j in jobs for k in ('candidate','opponent')}:
        assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
    rows=[json.loads(s) for s in output.read_text(encoding='utf-8').splitlines()] if output.exists() else []
    assert len({r['id'] for r in rows})==len(rows)
    for row in rows:
        assert row['id'] in expected
        assert all(row.get(k)==v for k,v in expected[row['id']].items())
    done={r['id'] for r in rows}
    pending=[j for j in jobs if j['id'] not in done]
    print(json.dumps(dict(event='start',total=len(jobs),existing=len(rows))),flush=True)
    with output.open('a',encoding='utf-8') as handle:
        for future in as_completed([pool.submit(run,j) for j in pending]):
            row=future.result(); rows.append(row)
            handle.write(json.dumps(row,ensure_ascii=False)+'\n'); handle.flush()
            if len(rows)%48==0 or not row.get('valid'):
                print(json.dumps(dict(event='progress',done=len(rows),total=len(jobs),valid=row.get('valid'))),flush=True)
    print(json.dumps(dict(event='complete',total=len(rows),invalid=sum(not r.get('valid') for r in rows))),flush=True)

def ready(): return True

def main():
    with ProcessPoolExecutor(max_workers=6) as pool:
        for task in [pool.submit(ready) for _ in range(6)]: task.result()
        print('ARENA_READY',flush=True)
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('exit'): break
            batch(pool,command)
            print('ARENA_READY',flush=True)
if __name__=='__main__': main()
