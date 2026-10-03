"""Build standalone local test candidates; never changes an existing release."""
from pathlib import Path
import hashlib, json
D = Path(__file__).resolve().parent; R = D.parents[1]
B = D / 'bc_integration'; B.mkdir(exist_ok=True)
base = (R / 'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest() == 'b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
model_raw = (D / 'market_bc_model.json').read_bytes()
report = json.loads((D / 'market_bc_model_report.json').read_text())
assert hashlib.sha256(model_raw).hexdigest() == report['model_sha256']
model = json.loads(model_raw); features = (D / 'market_bc_features.py').read_bytes()
assert hashlib.sha256(features).hexdigest() == model['feature_source_sha256']
tail = (D / 'market_bc_policy_tail.txt').read_bytes()
common = base + b'\n' + features + ('\n_MBC_FOREST = '+repr(model['forest'])+'\n').encode() + tail
settings = [('shadow', dict(mode='shadow'))]
for threshold in (.35, .55, .75):
    for limit in (4, 16):
        settings.append((f'add_p{int(threshold*100)}_q{limit}', dict(mode='active', threshold=threshold, max_extra=limit)))
settings.append(('hold_p55_q8', dict(mode='active', threshold=.55, max_extra=8, hold=True)))
manifest = []
for name, cfg in settings:
    data = common + ('\n_MBC_CFG.update('+repr(cfg)+')\n').encode()
    path = B / (name+'.py'); compile(data, str(path), 'exec')
    if path.exists(): assert path.read_bytes() == data
    else: path.write_bytes(data)
    manifest.append(dict(name=name, path=path.relative_to(R).as_posix(), sha256=hashlib.sha256(data).hexdigest(), settings=cfg))
(B/'candidates.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest), model_sha256=report['model_sha256'], released=False)), flush=True)
