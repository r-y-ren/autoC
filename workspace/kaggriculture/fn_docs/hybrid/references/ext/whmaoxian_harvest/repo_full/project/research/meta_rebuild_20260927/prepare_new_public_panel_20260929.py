"""Benchmark reviewed public programs as separate opponents, not inferred rating anchors."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];O=D/'public_review_20260929';sha=lambda b:hashlib.sha256(b).hexdigest()
reviews=json.loads((O/'runtime_review.json').read_text(encoding='utf-8'))
assert {r['label'] for r in reviews}>={'v37','salem','jaxa'}
worlds=json.loads((D/'herd_extended_design_20260929.json').read_text())
paths=['submissions/release_v10_r2/main.py','research/midgame_campaign_20260928/candidates/stack_all_gate.py','research/meta_rebuild_20260927/candidates/sequence_v2_early3_nomilk.py','research/production_upgrade_20260928/candidates/fused_herd_finish.py']
variants=[dict(path=p,sha256=sha((R/p).read_bytes())) for p in paths]
roster=[dict(path=(O/(name+'.py')).relative_to(R).as_posix(),family=name,panel='additional_public_program',sha256=sha((O/(name+'.py')).read_bytes())) for name in ('v37','salem','jaxa')]
jobs=[];seeds=worlds['seeds'][:8]
for v in variants:
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=op['sha256'])
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,obj in [('additional_public_jobs_20260929.json',jobs),('additional_public_design_20260929.json',dict(variants=variants,roster=roster,seeds=seeds,scope='New public-source opponent panel. Notebook titles and authors reported scores are NOT authenticated online rating anchors. Review verified literal embedded runtime code and no external I/O.'))]:
    path=D/name;text=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
print(json.dumps(dict(variants=len(variants),opponents=len(roster),games=len(jobs))),flush=True)
