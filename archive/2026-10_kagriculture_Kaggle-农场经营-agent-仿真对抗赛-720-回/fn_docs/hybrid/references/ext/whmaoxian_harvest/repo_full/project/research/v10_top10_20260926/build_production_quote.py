"""Study marginal-price integration in the existing verified tomato production plan."""
from pathlib import Path
import ast,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'production_quote';out.mkdir(exist_ok=True)
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
text=raw.decode('utf-8');tree=ast.parse(text)
function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_t19_qualifies')
original=ast.get_source_segment(text,function);manifest=[]
for minimum_shops in (2,3,4):
    for integral in (False,True):
        patch=original.replace('if demand<4:',f'if demand<{minimum_shops}:')
        if integral:
            old="quote=max(1,_r37_market_price('TOMATO',forecast))"
            new="quote=sum(max(1,_r37_market_price('TOMATO',forecast-72+unit)) for unit in range(72))/72.0"
            assert patch.count(old)==1;patch=patch.replace(old,new)
        assert 'return incremental_value>=500' in patch and "farm['money']<18000" in patch
        source=raw+b'\n# Marginal-price production development; scheduling and cash guards unchanged.\n'+patch.encode('utf-8')
        source+=b'\nagent=phase_b_agent\nkaggle_submission_agent=phase_b_agent\n'
        path=out/f'shops{minimum_shops}_integral{int(integral)}.py';compile(source,str(path),'exec')
        if path.exists():assert path.read_bytes()==source
        else:path.write_bytes(source)
        manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(source).hexdigest(),minimum_known_shops=minimum_shops,integrated_marginal_quote=integral,min_cash=18000,min_predicted_incremental_profit=500,unknown_future_shop_demand=0,minimum_rival_future_tomato_units=152))
(D/'production_quote_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest),scope='Development ablation, not an approved release.')),flush=True)
