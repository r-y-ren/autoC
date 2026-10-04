"""Development followups reuse frozen control outcomes; never edit release files."""
from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parent;R=S.parents[1];D=R/'research/meta_rebuild_20260927'
sha=lambda b:hashlib.sha256(b).hexdigest();design=json.loads((S/'extended_design.json').read_text())
timing=json.loads((S/'timing_candidates.json').read_text())
seeds=[1205068858,1402772681,2095943143,2140042026]
pred=json.loads((D/'predictor_fixed_design.json').read_text())['variants']
pred=[v for v in pred if v['name'] in ('fixed_pred_gate6','fixed_pred_gate12','fixed_pred_off','fixed_advance_off')]
def manifest(name,variants,chosen_seeds):
    jobs=[]
    for v in variants:
        assert sha((R/v['path']).read_bytes())==v['sha256']
        for op in design['roster']:
            for seed in chosen_seeds:
                for seat in (0,1):
                    j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                    j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
    report=dict(variants=variants,roster=design['roster'],seeds=chosen_seeds,cases=len(jobs),scope='Development only. Timing worlds selected to exercise observed gate, not estimated population win rate; predictor worlds are the first eight frozen uniform worlds. R2 controls in extended_results.jsonl.')
    for suffix,data in [('jobs',jobs),('design',report)]:
        p=S/f'{name}_{suffix}.json';text=json.dumps(data,indent=2)
        if p.exists():assert p.read_text()==text
        else:p.write_text(text)
    print(json.dumps(dict(batch=name,cases=len(jobs))),flush=True)
manifest('timing',timing,seeds)
manifest('forecast',pred,design['seeds'][:8])
