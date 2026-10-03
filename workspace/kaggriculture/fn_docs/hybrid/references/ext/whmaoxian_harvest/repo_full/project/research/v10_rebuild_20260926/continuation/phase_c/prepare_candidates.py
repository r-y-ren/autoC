"""Finite public-state cargo-readiness ablations; frozen releases stay untouched."""
from pathlib import Path
import hashlib,json
C=Path(__file__).resolve().parent; D=C.parent; W=D.parent; R=W.parents[1]
selection=json.loads((D/'phase_b/selection.json').read_text())
original=(R/selection['candidate']).read_text(encoding='utf-8')
assert hashlib.sha256((R/selection['candidate']).read_bytes()).hexdigest()==selection['sha256']
tail=(C/'readiness_tail.py.txt').read_text(encoding='utf-8')
variants=[('ready0',0,True,.9),('ready2',2,True,.9),('ready6',6,True,.9),
          ('ready12',12,True,.9),('advance_only2',2,False,.9),('unrestricted2',2,True,0)]
manifest=[]
for name,window,sellnow,similarity in variants:
    source=original
    old='if int(stock.get(item, 0)) >= max(_V10_ADV_THRESHOLD, 2 * demand):'
    assert source.count(old)==1
    source=source.replace(old,'if _c_ready(obs, item, stock.get(item, 0)) >= max(_V10_ADV_THRESHOLD, 2 * demand):')
    if sellnow:
        old='if debts is None or int(st["stock"].get(item, 0)) < _OR2_SN_K:'
        assert source.count(old)==1
        source=source.replace(old,'if debts is None or _c_ready(observation, item, st["stock"].get(item, 0)) < _OR2_SN_K:')
    source+=tail+f'\n_C_DELIVERY_WINDOW={window}\n_B_SIM_GATE={similarity}\n'
    compile(source,name,'exec')
    destination=C/f'{name}.py'; destination.write_text(source,encoding='utf-8')
    manifest.append(dict(name=name,path=destination.relative_to(R).as_posix(),window=window,
                         sellnow=sellnow,similarity=similarity,sha256=hashlib.sha256(destination.read_bytes()).hexdigest()))
(C/'candidates.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest),flush=True)
