"""Declare combination search and single-mechanism replication panels."""
from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parent;R=S.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
plan=json.loads((S/'extended_design.json').read_text())
combos=json.loads((S/'combination_candidates.json').read_text())
noops=[v for v in json.loads((S/'noop_candidates.json').read_text()) if v['name'] in ('noop_care','noop_combined')]
def save(name,variants,seeds):
    jobs=[]
    for v in variants:
        assert sha((R/v['path']).read_bytes())==v['sha256']
        for op in plan['roster']:
            for seed in seeds:
                for seat in (0,1):
                    j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                    j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
    report=dict(variants=variants,roster=plan['roster'],seeds=seeds,cases=len(jobs),scope='Development selection or component replication; not the final holdout. Frozen R2 controls in extended_results.jsonl.')
    for suffix,data in [('jobs',jobs),('design',report)]:
        p=S/f'{name}_{suffix}.json';text=json.dumps(data,indent=2)
        if p.exists():assert p.read_text()==text
        else:p.write_text(text)
    print(json.dumps(dict(batch=name,cases=len(jobs))),flush=True)
save('combinations',combos,plan['seeds'][:8])
save('noop_extended',noops,plan['seeds'][4:12])
