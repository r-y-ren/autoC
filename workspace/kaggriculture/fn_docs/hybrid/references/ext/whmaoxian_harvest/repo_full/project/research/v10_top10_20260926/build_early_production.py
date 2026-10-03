"""Re-time the existing 19-plot physical controller without retiming its parent."""
from pathlib import Path
import ast,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'early_production';out.mkdir(exist_ok=True)
raw=(R/'submissions/release_v10_r2/main.py').read_bytes();base=(R/'submissions/release_v10_r2/main.py').read_text(encoding='utf-8')
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tree=ast.parse(base)
def extract(name):return ast.get_source_segment(base,[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name][-1])
assign=extract('_t19_assign').replace('_t19_assign','_ep_assign').replace('_T19_REPORT','_EP_REPORT')
request=extract('_v219_request')
start=request.index('    if step==432:');end=request.index("    pending=state.pop('t19_pending',None)")
request=request[:start]+request[end:]
late_start=request.index('    if day==18 and hour>1:');late_end=request.index('    if hour>',late_start+1)
request=request[:late_start]+"    if day==18 and hour>1:\n        state['eligible']=False\n        return action\n"+request[late_end:]
request=request.replace('_v219_request','_ep_request').replace('_t19_assign','_ep_assign').replace('_T19_REPORT','_EP_REPORT').replace('_v219_native_day(native,day)','_v219_native_day(native,day-_EP_SHIFT)')
worker=extract('_v219_worker')
fallback="    if not role.get('t19'):\n        return _T19_WORKER(obs,state,actor,role)\n"
assert fallback in worker;worker=worker.replace(fallback,'').replace('_v219_worker','_ep_worker').replace('_T19_REPORT','_EP_REPORT')
helpers='\nimport itertools as _ep_itertools\n'+(D/'early_production_forecast.txt').read_text(encoding='utf-8')+'\n'+assign+'\n'+request+'\n'+worker+'\n'+(D/'early_production_controller.txt').read_text(encoding='utf-8')
manifest=[]
for day in (12,14,16):
    for risk in (0,.5):
        constants=f'\n_EP_START={day}\n_EP_SHIFT={18-day}\n_EP_RIVAL=80\n_EP_RISK={risk}\n_EP_MIN_NET=2000\n'
        data=raw+constants.encode()+helpers.encode('utf-8');path=out/f'day{day}_risk{int(risk*10)}.py';compile(data,str(path),'exec')
        if path.exists():assert path.read_bytes()==data
        else:path.write_bytes(data)
        manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),start_day=day,risk=risk))
(D/'early_production_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(variants=len(manifest),parent_clock_unchanged=True)),flush=True)
