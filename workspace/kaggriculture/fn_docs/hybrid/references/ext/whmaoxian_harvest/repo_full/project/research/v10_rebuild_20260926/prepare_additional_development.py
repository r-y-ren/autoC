"""Evaluate newly acquired real programs separately from reconstructed traces."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
programs=[r for r in json.loads((OUT/'additional_programs.json').read_text()) if r['role']=='additional_development']
candidates=['submissions/release_v9/main.py','submissions/release_v10/main.py',
 'research/v10_rebuild_20260926/generation2/h12_observed4.py',
 'research/v10_rebuild_20260926/combinations/observed4_h24.py',
 'research/v10_rebuild_20260926/combinations/observed4_q16.py']
jobs=[]
for candidate in candidates:
    for opponent in programs:
        for index in range(8):
            seed=int.from_bytes(hashlib.sha256(f'v10r2-closed-development-{index}'.encode()).digest()[:4],'big')%2000000000
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],seed=seed,seat=seat,
                    panel='additional_public_program',family=opponent['name'])
                for key in ('candidate','opponent'):
                    job[key+'_sha256']=hashlib.sha256((ROOT/job[key]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
                jobs.append(job)
(OUT/'additional_development_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print('Additional development match jobs',len(jobs),flush=True)
