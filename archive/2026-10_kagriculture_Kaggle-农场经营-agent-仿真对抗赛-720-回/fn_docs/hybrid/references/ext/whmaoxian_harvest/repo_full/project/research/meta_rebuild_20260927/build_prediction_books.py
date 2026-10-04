"""Ablate which observer receives the emitted-order correction."""
from pathlib import Path
import ast,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
raw=(R/'submissions/release_v10_r2/main.py').read_bytes();source=raw.decode('utf-8');tree=ast.parse(source)
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
def extract(name):return ast.get_source_segment(source,next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name))
variants=[]
for mode in ('predictors','race','both'):
    functions=[]
    if mode in ('predictors','both'):
        for name in ('_v92_p_update','_v92_q_update'):
            s=extract(name);assert s.count('_V9_RACE.get(player)')==1
            functions.append(s.replace('_V9_RACE.get(player)','_PB_BOOK.get(player)'))
    if mode in ('race','both'):
        s=extract('_v9_race_update');assert s.count('prev = st["prev"]')==1
        functions.append(s.replace('prev = st["prev"]','prev = _PB_BOOK.get(int(obs["player"]),{}).get("prev")'))
    data=raw+b'\n'+('\n\n'.join(functions)+'\n').encode()+(D/'prediction_book_tail.txt').read_bytes()
    path=D/f'candidates/book_{mode}.py';compile(data,str(path),'exec')
    assert not path.exists();path.write_bytes(data)
    variants.append(dict(name=path.stem,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),mode=mode))
(D/'book_candidates.json').write_text(json.dumps(variants,indent=2))
design=json.loads((D/'value_extended_design.json').read_text());jobs=[]
for v in variants:
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest())
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'book_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'book_design.json').write_text(json.dumps(dict(variants=variants,seeds=design['seeds'],roster=design['roster'],jobs=len(jobs),scope='Observer-channel ablations on declared development worlds. No new holdout opened.'),indent=2))
print(json.dumps(dict(candidates=len(variants),new_games=len(jobs))),flush=True)
