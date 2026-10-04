"""Compose separately screened mechanisms without global-parent name collisions."""
from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parent;R=S.parents[1];D=R/'research/meta_rebuild_20260927';sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
parts={
 'nomilk':(D/'candidates/midgame_yarn_nomilk.py','_K28_HERD_PARENT=phase_b_agent','midgame_herd_agent'),
 'gate':(D/'candidates/fixed_pred_gate6.py','_K28_PRED_PARENT=phase_b_agent','predictor_gate_agent'),
 'care':(S/'candidates/noop_care.py','_K28N_PARENT=phase_b_agent','noop_recovery_agent'),
 'all':(S/'candidates/noop_combined.py','_K28N_PARENT=phase_b_agent','noop_recovery_agent'),
 'late':(D/'candidates/late_both.py','_TF_PARENT=phase_b_agent','terminal_feed_agent')}
settings=[('stack_care_gate',('gate','care')),('stack_all_gate',('gate','all')),
 ('stack_care_nomilk',('nomilk','care')),('stack_full',('nomilk','gate','all')),
 ('stack_care_late',('care','late')),('stack_all_gate_late',('gate','all','late'))]
variants=[]
for name,components in settings:
    source=raw;entry='phase_b_agent'
    for key in components:
        path,parent,new_entry=parts[key];data=path.read_bytes();assert data.startswith(raw)
        tail=data[len(raw):].decode();assert tail.count(parent)==1,(key,parent)
        tail=tail.replace(parent,parent.split('=')[0]+'='+entry);source+=tail.encode();entry=new_entry
    p=S/'candidates'/(name+'.py');compile(source,str(p),'exec')
    if p.exists():assert p.read_bytes()==source
    else:p.write_bytes(source)
    variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(source),components=components))
(S/'combination_candidates.json').write_text(json.dumps(variants,indent=2))
print(json.dumps(dict(candidates=len(variants))),flush=True)
