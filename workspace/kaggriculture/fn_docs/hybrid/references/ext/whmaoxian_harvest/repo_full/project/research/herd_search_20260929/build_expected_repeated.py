"""Reuse the audited expected-demand model at the new purchase opportunities."""
from pathlib import Path
import ast,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];T=R/'research/v10_top10_20260926'
raw=(R/'submissions/release_v10_r2/main.py').read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
text=raw.decode();node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='_hd2_ev')
original=ast.get_source_segment(text,node);prefix=original[:original.index('    def path(with_new):')]
replacement=(prefix+(T/'herd_expectation_body.txt').read_text()).replace('def _hd2_ev(', 'def _K29_expected_ev(')
helpers=(T/'herd_expectation_helpers.txt').read_text()
footer='''
_K29_EXPECTED_NATIVE=_hd2_ev
def _hd2_ev(option,k,obs,st):
    if st is _CS_STATE.get(int(obs['player'])) and _CS_OPTIONS==('SHEEP',):
        return _K29_expected_ev(option,k,obs,st)
    return _K29_EXPECTED_NATIVE(option,k,obs,st)
'''
footer+='\ndef expected_repeat_agent(observation,configuration=None):\n    if int(observation["step"])==0:\n        for key in _HE_REPORT:_HE_REPORT[key]=0\n    return repeated_herd_agent(observation,configuration)\nagent=expected_repeat_agent\nkaggle_submission_agent=expected_repeat_agent\n'
repeat=json.loads((D/'repeated_design.json').read_text());wide=json.loads((D/'herd_extended_design.json').read_text())
base=next(v for v in repeat['variants'] if v['name']=='repeat_ev');variants=[];jobs=[]
for risk in (0.0,0.25):
    for cash in (0,650):
        cfg=dict(base['config'],milk=True,cash=cash,care_model=True)
        params='\n_K29_CFG='+repr(cfg)+f'\n_HE_INCLUDE_STOCK=True\n_HE_RISK={risk}\n'
        source=raw+params.encode()+(D/'repeated_herd_tail.txt').read_bytes()+('\n'+helpers+'\n'+replacement+footer).encode()
        p=D/'candidates'/f'expected_repeat_r{int(risk*100)}_cash{cash}.py';compile(source,str(p),'exec')
        if p.exists():assert p.read_bytes()==source
        else:p.write_bytes(source)
        variants.append(dict(name=p.stem,path=p.relative_to(R).as_posix(),sha256=sha(source),risk=risk,cash=cash))
seeds=[1799657451]+wide['seeds'][:4]
for v in variants:
    for op in wide['roster']:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('expected_repeated_jobs.json',jobs),('expected_repeated_design.json',dict(variants=variants,seeds=seeds,roster=wide['roster'],scope='Reused outcome-scenario model at earlier/repeated purchases; development only.'))]:
    p=D/name;s=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==s
    else:p.write_text(s)
print(json.dumps(dict(variants=len(variants),cases=len(jobs))),flush=True)
