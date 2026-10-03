"""Combine learned macro selection with an independently tested idle-action module."""
from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
D=Path(__file__).resolve().parent;R=D.parents[1]
model_agent=(D/'learned.py').read_bytes()
assert hashlib.sha256(model_agent).hexdigest()=='35afe4072485a06f2ffb1e1ac7d55c3bb2cc0110c50a5292d0a611d0fab150e5'
tail=(R/'research/v10_top10_20260926/micro_opportunities_tail.txt').read_text()
assert tail.count('_U_PARENT=phase_b_agent')==1
assert "_U_START" in tail and "_U_ACTIONS" in tail
tail=tail.replace('_U_PARENT=phase_b_agent','_U_PARENT=route_value_agent')
constants="\n_U_ACTIONS=('care','water','harvest','fertilizer')\n_U_START=144\n"
source=model_agent+constants.encode()+tail.encode()
path=D/'combined.py';assert not path.exists();compile(source,str(path),'exec');path.write_bytes(source)
record=dict(candidate=path.relative_to(R).as_posix(),sha256=hashlib.sha256(source).hexdigest(),
    created_utc=datetime.now(timezone.utc).isoformat(),parent_sha256=hashlib.sha256(model_agent).hexdigest(),
    macro_model='model.json',model_weights_changed=False,released=False,
    scope='Research combination. External tests and independent confirmation are still required.')
(D/'combined_manifest.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record),flush=True)
