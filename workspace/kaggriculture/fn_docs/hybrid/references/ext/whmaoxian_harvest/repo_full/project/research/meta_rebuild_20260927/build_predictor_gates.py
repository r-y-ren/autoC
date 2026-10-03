"""Test forecast confidence and independent speculative-layer removals."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
settings=[('pred_off',True,0,0,-100000,False),
 ('pred_gate6',False,6,.5,0,False),('pred_gate12',False,12,.65,5,False),
 ('pred_gate_loose',False,4,.35,-5,False),
 ('advance_off',False,0,0,-100000,True),('both_pred_advance_off',True,0,0,-100000,True)]
variants=[]
for name,off,match,precision,score,no_advance in settings:
    constants=f'\n_PG_OFF={off}\n_PG_MATCH={match}\n_PG_PRECISION={precision}\n_PG_SCORE={score}\n'
    if no_advance:constants+='\n_ADV_FROM=720\n_B_AGGRESSIVE_K=0\n'
    source=base+constants.encode()+(D/'predictor_gate_tail.txt').read_bytes()
    path=D/f'candidates/{name}.py';compile(source,str(path),'exec')
    assert not path.exists();path.write_bytes(source)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(source).hexdigest(),off=off,minimum_matches=match,precision=precision,minimum_score=score,no_advance=no_advance))
(D/'predictor_candidates.json').write_text(json.dumps(variants,indent=2))
design=json.loads((D/'value_extended_design.json').read_text());jobs=[]
for v in variants:
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest())
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'predictor_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'predictor_design.json').write_text(json.dumps(dict(variants=variants,seeds=design['seeds'],roster=design['roster'],jobs=len(jobs),scope='Declared development-layer ablations. Changes do not constitute a release or a rating estimate.'),indent=2))
print(json.dumps(dict(candidates=len(variants),new_games=len(jobs))),flush=True)
