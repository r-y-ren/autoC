"""Single successful herd substitution: timing, affordability and plan retries."""
from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parent;R=S.parents[1];D=R/'research/meta_rebuild_20260927'
raw=(R/'submissions/release_v10_r2/main.py').read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(D/'midgame_herd_tail_20260928.txt').read_text()
tail=tail.replace('_CS_MIN_GAIN)', '_CS_MIN_GAIN,_CS_FROM,_CS_TO)')
tail=tail.replace('global _CS_OPTIONS,_CS_SHOP_RULE,_CS_RATIO,_CS_MIN_GAIN','global _CS_OPTIONS,_CS_SHOP_RULE,_CS_RATIO,_CS_MIN_GAIN,_CS_FROM,_CS_TO')
tail=tail.replace('_CS_MIN_GAIN=_K28_HERD_NATIVE','_CS_MIN_GAIN,_CS_FROM,_CS_TO=_K28_HERD_NATIVE')
tail=tail.replace('if eligible and 144<=step<192:', 'if eligible and _K28_BEGIN<=step<_K28_END and observation["farms"][int(observation["player"])]["money"]>=_K28_CASH:\n        _CS_FROM=_K28_BEGIN;_CS_TO=_K28_END\n        cs=_CS_STATE.get(int(observation["player"]))\n        if _K28_RETRY and cs and not cs.get("mode"):cs["decided"]=False')
configs=[('early500',72,216,500,True,0),('early800',72,216,800,True,0),('early_selective',72,216,500,True,600),('retry_late',144,264,800,True,0),('late_selective',144,264,800,True,600),('late_single',144,264,800,False,600)]
folder=S/'candidates';folder.mkdir(exist_ok=True);variants=[]
for name,begin,end,cash,retry,gain in configs:
    parameters=f'\n_K28_NO_MILK=True\n_K28_RATIO=0\n_K28_GAIN={gain}\n_K28_BEGIN={begin}\n_K28_END={end}\n_K28_CASH={cash}\n_K28_RETRY={retry!r}\n'
    source=raw+parameters.encode()+tail.encode();p=folder/(name+'.py')
    compile(source,str(p),'exec')
    if p.exists():assert p.read_bytes()==source
    else:p.write_bytes(source)
    variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(source),begin=begin,end=end,cash=cash,retry=retry,gain=gain))
p=S/'timing_candidates.json';text=json.dumps(variants,indent=2)
if p.exists():assert p.read_text()==text
else:p.write_text(text)
print(json.dumps(dict(candidates=len(variants))),flush=True)
