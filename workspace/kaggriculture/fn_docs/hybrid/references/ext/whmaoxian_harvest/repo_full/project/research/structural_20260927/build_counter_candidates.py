"""Build hash-frozen commodity counterplay candidates for local evaluation."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
checks=json.loads((P/'counter_model_checks.json').read_text());assert checks['passed']
model=(P/'counter_market_model.txt').read_bytes()
assert hashlib.sha256(model).hexdigest()==checks['source_sha256']
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
policy=(P/'counter_market_policy.txt').read_bytes();out=P/'counter_candidates';out.mkdir(exist_ok=True)
variants=[]
for mode in ('mirror','mixture'):
    for similarity in (.85,.95):
        for lot in (24,48):
            settings=dict(mode=mode,similarity=similarity,lot=lot,min_gain=1.0,max_loss=8,risk=2.0)
            constants=f'\n_MC_MODE={mode!r}\n_MC_SIMILARITY={similarity}\n_MC_LOT={lot}\n_MC_MIN_GAIN=1.0\n_MC_MAX_LOSS=8\n_MC_RISK=2.0\n'
            data=base+b'\n'+model+constants.encode()+policy+b'\nkaggle_submission_agent=counter_market_agent\n'
            path=out/f'{mode}_s{int(similarity*100)}_q{lot}.py';compile(data,str(path),'exec')
            if path.exists():assert path.read_bytes()==data
            else:path.write_bytes(data)
            variants.append(dict(path=path.relative_to(R).as_posix(),settings=settings,sha256=hashlib.sha256(data).hexdigest()))
(P/'counter_manifest.json').write_text(json.dumps(variants,indent=2))
print(json.dumps(dict(variants=len(variants),model_verified=True,release=False)),flush=True)
