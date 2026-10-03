"""Expected marginal game value over all remaining binary product-demand draws."""
from pathlib import Path
import ast,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'herd_expectation';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes();text=base.decode('utf-8')
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='_hd2_ev')
original=ast.get_source_segment(text,node);prefix=original[:original.index('    def path(with_new):')]
replacement=prefix+(D/'herd_expectation_body.txt').read_text(encoding='utf-8')
helpers=(D/'herd_expectation_helpers.txt').read_text(encoding='utf-8')
footer='''
def herd_expectation_agent(observation,configuration=None):
    if int(observation['step'])==0:
        for key in _HE_REPORT:_HE_REPORT[key]=0
    return herd_allocation_agent(observation,configuration)
herd_expectation_agent.telemetry=_HE_REPORT
agent=herd_expectation_agent
kaggle_submission_agent=herd_expectation_agent
'''
manifest=[]
for risk in (0.0,.25):
    for stock in (False,True):
        params=f'\n_CS_OPTIONS=("GOOSE","SHEEP")\n_CS_SHOP_RULE=None\n_CS_RATIO=1.15\n_CS_MIN_GAIN=600\n_HE_RISK={risk}\n_HE_INCLUDE_STOCK={stock}\n'
        raw=base+params.encode()+(D/'herd_allocation_tail.txt').read_bytes()+(helpers+'\n'+replacement+footer).encode('utf-8')
        path=out/f'risk{int(risk*100)}_stock{int(stock)}.py';compile(raw,str(path),'exec')
        if path.exists():assert path.read_bytes()==raw
        else:path.write_bytes(raw)
        manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),risk_penalty=risk,current_stock_in_forecast=stock))
(D/'herd_expectation_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(variants=len(manifest))),flush=True)
