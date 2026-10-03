"""Screen only the executable goose opening; the starvation-prone sheep opening is rejected."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
v=next(v for v in json.loads((D/'opening_species_design.json').read_text())['variants'] if v['name']=='GOOSE')
assert sha((R/v['path']).read_bytes())==v['sha256']
source=json.loads((D/'herd_sequence_v2_jobs.json').read_text())
first=source[0]['candidate'];jobs=[]
for item in source:
    if item['candidate']!=first:continue
    j=dict(item,candidate=v['path'],candidate_sha256=v['sha256']);j.pop('id')
    j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
p=D/'opening_goose_jobs.json';text=json.dumps(jobs,indent=2)
if p.exists():assert p.read_text()==text
else:p.write_text(text)
print(json.dumps({'cases':len(jobs),'candidate':v['path']}),flush=True)
