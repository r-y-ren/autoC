"""Build source-frozen commodity pressure ablations, preserving historical agents."""
from pathlib import Path
import ast, hashlib, itertools, json
D=Path(__file__).resolve().parent; R=D.parents[1]
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
text=raw.decode('utf-8'); tree=ast.parse(text)
function=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_adv_apply'][-1]
advance=ast.get_source_segment(text,function)
old='range(1,_V10_ADV_HORIZON+1)'; assert advance.count(old)==1
advance=advance.replace(old,'range(1,max(_V10_ADV_HORIZON,_PP_MAX_LOOK)+1)')
helpers,entry=(D/'product_pressure_tail.txt').read_text().split('_PP_ENTRY_PARENT =',1)
out=D/'product_pressure'; out.mkdir(exist_ok=True); manifest=[]
for horizon,stock,ratio in itertools.product((24,36,48),(4,12),(.5,1.0)):
    constants=f'\n_PP_MAX_LOOK={horizon}\n_PP_STOCK_MIN={stock}\n_PP_CAPACITY_RATIO={ratio}\n'
    data=raw+constants.encode()+helpers.encode()+('\n'+advance+'\n_PP_ENTRY_PARENT ='+entry).encode()
    target=out/f'h{horizon}_k{stock}_r{int(ratio*100)}.py'; compile(data,str(target),'exec')
    if target.exists():assert target.read_bytes()==data
    else:target.write_bytes(data)
    manifest.append(dict(path=target.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),horizon=horizon,stock=stock,ratio=ratio))
(D/'product_pressure_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'variants':len(manifest),'parent_preserved':True}),flush=True)
