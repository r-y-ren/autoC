"""First closed-loop comparison against newly obtained public programs."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[1]
programs=json.loads((OUT/'public_programs.json').read_text(encoding='utf-8'))
existing=['submissions/release_v9/main.py','submissions/release_v10/main.py',
          'research/v10_rebuild_20260926/candidates/open_5.py']
new=[r['path'] for r in programs]
jobs=[]
for candidate in existing+new:
    for opponent in new+existing[:2]:
        if candidate==opponent:continue
        for index in range(3):
            seed=int.from_bytes(hashlib.sha256(f'v10r2-closed-development-{index}'.encode()).digest()[:4],'big')%2000000000
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent,seed=seed,seat=seat,
                    panel='new_public_closed_loop',family=Path(opponent).parent.name)
                for key in ('candidate','opponent'):
                    job[key+'_sha256']=hashlib.sha256((ROOT/job[key]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
                jobs.append(job)
(OUT/'new_public_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print('New public comparison',len(jobs),'full matches',flush=True)
