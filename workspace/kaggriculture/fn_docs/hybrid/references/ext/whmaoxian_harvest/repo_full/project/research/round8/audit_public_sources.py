"""Recursive AST audit; parse/decode only, never execute downloaded Python."""
import ast,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[2];base=root/'external/round8';out=[]
sensitive_names={'exec','eval','compile','__import__','open','input','breakpoint'}
sensitive_attrs={'system','popen','Popen','run','check_call','check_output','remove','unlink','rmdir','rmtree','rename','replace','write_text','write_bytes','connect','urlopen','request','getenv','environ','load','loads'}

def audit(path,depth=0):
 raw=path.read_bytes();text=raw.decode('utf-8-sig');tree=ast.parse(text)
 rec={'path':str(path.relative_to(root)).replace('\\','/'),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'depth':depth,'imports':[],'sensitive_operations':[],'nested_sources':[]}
 for n in ast.walk(tree):
  if isinstance(n,(ast.Import,ast.ImportFrom)):rec['imports'].append({'line':n.lineno,'statement':ast.unparse(n)})
  if isinstance(n,ast.Call):
   func=ast.unparse(n.func)
   if isinstance(n.func,ast.Name) and n.func.id in sensitive_names or isinstance(n.func,ast.Attribute) and n.func.attr in sensitive_attrs:
    rec['sensitive_operations'].append({'line':n.lineno,'function':func,'expression':ast.unparse(n)[:180]})
   if isinstance(n.func,ast.Name) and n.func.id in ('exec','eval','compile'):
    value=ast.literal_eval(n.args[0])
    assert isinstance(value,(str,bytes)),(path,n.lineno)
    if isinstance(value,str):value=value.encode()
    target=path.parent/(path.stem+f'_nested_{n.lineno}.py')
    target.write_bytes(value)
    rec['nested_sources'].append(str(target.relative_to(root)).replace('\\','/'))
    audit(target,depth+1)
 out.append(rec)
for name in ('fieldcraft','master2965','icefire'):
 for fn in (['main.py','mirror_plan.py'] if name=='fieldcraft' else ['main.py']):audit(base/name/fn)
report={'method':'Notebook values read with ast.literal_eval; b85/b64 and zlib/gzip/lzma decoded; all nested executable strings parsed recursively. No notebook code executed.','sources':{name:json.loads((base/(name+'_origin.json')).read_text()) for name in ('fieldcraft','master2965','icefire')},'files':out,'review':{'network_or_process_execution':'none found','fieldcraft':'Only math and bundled mirror_plan imports; no filesystem or dynamic execution in decoded sources.','master2965_and_icefire':'Two literal embedded exec blocks implement official deterministic physical semantics and terminal route planner; recursively audited. Optional V92_SELL_LIB environment-dependent local JSON loading exists. Clear this variable for deterministic testing; no network/write operation found.','licenses':'Fieldcraft includes Notebook literal NOTICE/LICENSE copied exactly. Other two notebooks package main.py only; inherited Apache notices/license text are retained inside exact main.py bytes.','icefire_generalization_warning':'Final Water Repair layer keys on an exact whole-observation fingerprint at step 506 for a historical seed-107021 validation scenario. It is a local lookup patch, not evidence of general skill.'}}
(root/'research/round8/public_source_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
for r in out:print(r['path'],r['sha256'],len(r['imports']),'imports',len(r['sensitive_operations']),'flagged calls')
