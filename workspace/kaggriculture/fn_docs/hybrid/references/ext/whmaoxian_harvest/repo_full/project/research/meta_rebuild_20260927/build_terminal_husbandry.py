"""Late-husbandry ablations; count changed requests separately from realized gain."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'terminal_feed_tail.txt').read_text(encoding='utf-8').replace("'feed_saved'","'feed_requests_removed'")
variants=[]
for name,feed,care in [('late_feed',True,False),('late_care',False,True),('late_both',True,True)]:
    data=base+f'\n_TF_FEED={feed}\n_TF_CARE={care}\n'.encode()+tail.encode()
    path=D/f'candidates/{name}.py';compile(data,str(path),'exec')
    assert not path.exists();path.write_bytes(data)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),feed=feed,care=care))
(D/'husbandry_candidates.json').write_text(json.dumps(variants,indent=2))
design=json.loads((D/'value_extended_design.json').read_text());jobs=[]
for v in variants:
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest())
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'husbandry_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'husbandry_design.json').write_text(json.dumps(dict(variants=variants,seeds=design['seeds'],roster=design['roster'],jobs=len(jobs),scope='End-of-episode husbandry development; saved requests are not automatically saved units or won matches.'),indent=2))
print(json.dumps(dict(candidates=len(variants),new_games=len(jobs))),flush=True)
