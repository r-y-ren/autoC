"""Build six bounded public-wealth risk controls; do not change frozen releases."""
from pathlib import Path
import hashlib,json,subprocess,sys
C=Path(__file__).resolve().parent;D=C.parent;W=D.parent;R=W.parents[1]
selection=json.loads((D/'phase_b/selection.json').read_text())
original=(R/selection['candidate']).read_text(encoding='utf-8')
tail=(C/'risk_tail.py.txt').read_text(encoding='utf-8')
variants=[('wealth500',True,500,216),('wealth1500',True,1500,216),
 ('wealth3000',True,3000,216),('cash1500',False,1500,216),
 ('cash3000',False,3000,216),('latewealth1500',True,1500,480)]
manifest=[]
for name,wealth,buffer,start in variants:
    old='aggressive=_B_SIM_GATE<=0 or _r37_similarity(observation)>=_B_SIM_GATE'
    assert original.count(old)==1
    source=original.replace(old,'aggressive=(_B_SIM_GATE<=0 or _r37_similarity(observation)>=_B_SIM_GATE) and _d_allow_advance(observation)')
    source+=tail+f'\n_D_BUFFER={buffer}\n_D_WEALTH={wealth!r}\n_D_START={start}\n'
    compile(source,name,'exec');dest=C/f'{name}.py';dest.write_text(source,encoding='utf-8')
    manifest.append(dict(name=name,path=dest.relative_to(R).as_posix(),wealth=wealth,buffer=buffer,
                         start=start,sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
(C/'risk_candidates.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
preparer=(C/'prepare_development.py').read_text(encoding='utf-8')
preparer=preparer.replace("'candidates.json'","'risk_candidates.json'").replace('[:8]','[:4]')
preparer=preparer.replace('development_jobs.json','risk_jobs.json').replace('DEVELOPMENT_PROTOCOL.md','RISK_PROTOCOL.md')
preparer=preparer.replace('cargo readiness','estimated-wealth risk controls')
(C/'prepare_risk_jobs.py').write_text(preparer,encoding='utf-8')
subprocess.run([sys.executable,str(C/'prepare_risk_jobs.py')],check=True)
