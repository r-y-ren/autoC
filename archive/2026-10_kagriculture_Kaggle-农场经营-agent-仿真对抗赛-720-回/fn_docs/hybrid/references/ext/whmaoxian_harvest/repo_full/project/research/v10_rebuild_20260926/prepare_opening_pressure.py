"""Bounded opening variants for functional screening, not release selection."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[1]
DEST=OUT/'generation3';DEST.mkdir(exist_ok=True)
base=(OUT/'candidates/open_5.py').read_bytes()
template=(OUT/'opening_pressure_template.py.txt').read_text(encoding='utf-8')
records=[]
for quantity in (4,8,16,24):
    for front in (True,False):
        for slots in (1,3):
            name=f'q{quantity}_'+('front' if front else 'last')+f'_s{slots}'
            text=template.replace('_R3_QUANTITY = 8',f'_R3_QUANTITY = {quantity}')
            text=text.replace('_R3_FRONT = True',f'_R3_FRONT = {front}')
            text=text.replace('_R3_SLOTS = 1',f'_R3_SLOTS = {slots}')
            raw=base+text.encode();compile(raw,name,'exec')
            path=DEST/(name+'.py');path.write_bytes(raw)
            records.append(dict(name=name,path=path.relative_to(ROOT).as_posix(),
                sha256=hashlib.sha256(raw).hexdigest(),quantity=quantity,front=front,slots=slots))
(OUT/'generation3_manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
reference=json.loads((OUT/'generation2_jobs.json').read_text(encoding='utf-8'))
cases=[r for r in reference if r['candidate']==reference[0]['candidate']]
jobs=[]
records.append(dict(name='safe_control',path='research/v10_rebuild_20260926/candidates/open_5.py',
    sha256=hashlib.sha256(base).hexdigest()))
for candidate in records:
    for case in cases:
        job=dict(case,candidate=candidate['path'],candidate_sha256=candidate['sha256'],prefix_only=True)
        job.pop('id',None)
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
        jobs.append(job)
(OUT/'generation3_prefix_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print('Prefix-only functional checks',len(jobs),'not full matches',flush=True)
