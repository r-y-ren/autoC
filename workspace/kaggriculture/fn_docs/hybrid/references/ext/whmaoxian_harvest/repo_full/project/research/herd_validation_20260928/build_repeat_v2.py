"""Freeze a cash-guard correction and explicit minimum cow capacity."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
raw=(R/'submissions/release_v10_r2/main.py').read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'repeat_herd_tail.txt').read_text()
old="""        elif len(order)>2 and order[0] in ('BUY_SEED','BUY_PRODUCT'):
            prices={'WHEAT':25,'FERTILIZER':100} if order[0]=='BUY_PRODUCT' else {'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}
            budget+=max(0,int(order[2]))*prices.get(order[1],0)"""
new="""        elif order[0]=='BUY_PRODUCT':
            _HG28_REPORT['cash_veto']+=1;return None
        elif len(order)>2 and order[0]=='BUY_SEED':
            budget+=max(0,int(order[2]))*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}.get(order[1],0)"""
assert tail.count(old)==1;tail=tail.replace(old,new)
needle="    eligible=eligible and local['allocated']<_HG28_CFG['max_swaps']"
replacement="    cows=sum(isinstance(t,dict) and t.get('animal')=='COW' for row in observation['farms'][seat]['tiles'] for t in row)\n    eligible=eligible and cows>=_HG28_CFG['min_cows']\n"+needle
assert tail.count(needle)==1;tail=tail.replace(needle,replacement)
(D/'repeat_herd_v2_tail.txt').write_text(tail)
common=dict(start=72,stop=288,max_swaps=2,no_milk=True,ratio=0,gain=-1000000,reserve=100,min_cows=4)
settings=[('repeat_two_v2',{}),('repeat_four_v2',dict(max_swaps=4)),('early_two_v2',dict(min_cows=3)),('repeat_after_two_shops_v2',dict(start=144))]
variants=[]
for name,patch in settings:
    cfg=dict(common,**patch);data=raw+('\n_HG28_CFG='+repr(cfg)+'\n').encode()+tail.encode()
    p=D/(name+'.py');compile(data,str(p),'exec')
    if p.exists():assert p.read_bytes()==data
    else:p.write_bytes(data)
    variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(data),config=cfg))
(D/'repeat_v2_candidates.json').write_text(json.dumps(variants,indent=2))
print(json.dumps(dict(variants=len(variants),change='V1 BUY_PRODUCT fixed-price assumption removed; swaps vetoed on such turns.')),flush=True)
