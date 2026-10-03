"""Compare reviewed public cores with the same net opening inventory as R2."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
audit={x['name']:x for x in json.loads((D/'extraction_audit.json').read_text())};variants=[]
for core,buy in [('dmitrii',5),('dmitrii',8),('pipe16',5),('metav4',5)]:
    raw=(D/f'public_agents/{core}.py').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==audit[core]['sha256']
    source=raw+f'\n_RB_BUY={buy}\n'.encode()+(D/'rebase_opening_tail.txt').read_bytes()
    path=D/f'candidates/{core}_net{buy}.py';compile(source,str(path),'exec')
    assert not path.exists();path.write_bytes(source)
    variants.append(dict(name=path.stem,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(source).hexdigest(),core=core,buy=buy,upstream_sha256=audit[core]['sha256']))
(D/'rebased_candidates.json').write_text(json.dumps(variants,indent=2))
design=json.loads((D/'value_extended_design.json').read_text());jobs=[]
for v in variants:
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest())
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'rebased_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'rebased_design.json').write_text(json.dumps(dict(variants=variants,seeds=design['seeds'],roster=design['roster'],jobs=len(jobs),scope='Development of public-core derivatives; these cores are related, not independent policy families.'),indent=2))
print(json.dumps(dict(candidates=len(variants),new_games=len(jobs))),flush=True)
