"""Interactive finite batches with a reusable worker pool. No autonomous search."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib,json,sys
import fast_arena
R=fast_arena.ROOT

def batch(pool,command):
 manifest=Path(command['manifest']); output=Path(command['output'])
 jobs=json.loads(manifest.read_text(encoding='utf-8'))
 for path,digest in {(j[k],j[k+'_sha256']) for j in jobs for k in ('candidate','opponent')}:
  assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
 prior=[json.loads(s) for s in output.read_text(encoding='utf-8').splitlines()] if output.exists() else []
 assert len({r['id'] for r in prior})==len(prior)
 assert {r['id'] for r in prior}.issubset({j['id'] for j in jobs})
 done={r['id'] for r in prior}; pending=[j for j in jobs if j['id'] not in done]
 print(json.dumps(dict(event='started',jobs=len(jobs),existing=len(prior))),flush=True)
 with output.open('a',encoding='utf-8') as handle:
  futures=[pool.submit(fast_arena.run_job,j) for j in pending]
  for future in as_completed(futures):
   row=future.result(); prior.append(row)
   handle.write(json.dumps(row,ensure_ascii=False)+'\n');handle.flush()
   if len(prior)%48==0 or not row.get('valid'):
    print(json.dumps(dict(event='progress',done=len(prior),required=len(jobs),valid=row.get('valid'))),flush=True)
 print(json.dumps(dict(event='complete',jobs=len(prior),invalid=sum(not r.get('valid') for r in prior))),flush=True)
def worker_ready():
 return True

def main():
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--workers',type=int,default=8)
 args=parser.parse_args(); assert 1<=args.workers<=8
 with ProcessPoolExecutor(max_workers=args.workers) as pool:
  for future in [pool.submit(worker_ready) for _ in range(args.workers)]:future.result()
  print('ARENA_READY',flush=True)
  for line in sys.stdin:
   command=json.loads(line)
   if command.get('exit'):break
   batch(pool,command)
   print('ARENA_READY',flush=True)
if __name__=='__main__':main()
