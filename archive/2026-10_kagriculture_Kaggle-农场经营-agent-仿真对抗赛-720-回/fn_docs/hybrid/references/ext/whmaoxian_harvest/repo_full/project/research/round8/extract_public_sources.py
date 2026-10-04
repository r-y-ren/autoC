"""Static extraction only: no notebook or extracted source is executed here."""
import ast,base64,gzip,zlib,lzma,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'external/round8'

def literals(path):
 t=ast.parse(path.read_text(encoding='utf-8-sig'));out={}
 for node in t.body:
  if isinstance(node,ast.Assign):
   try:value=ast.literal_eval(node.value)
   except (ValueError,TypeError):continue
   for target in node.targets:
    if isinstance(target,ast.Name):out[target.id]=value
 return out

f=literals(OUT/'fieldcraft_cell4.txt')
dest=OUT/'fieldcraft';dest.mkdir(exist_ok=True)
for name,payload in f['PAYLOADS'].items():
 assert name in ('main.py','mirror_plan.py')
 raw=zlib.decompress(base64.b85decode(payload))
 expected=f['RELEASE']['compact_source_sha256'][name]
 assert hashlib.sha256(raw).hexdigest()==expected
 (dest/name).write_bytes(raw)
for name in ('NOTICE','LICENSE'):
 (dest/f'{name}.txt').write_text(f[name],encoding='utf-8',newline='\n')
for name,var,decoder in [('master2965','AGENT_B64',lambda x:gzip.decompress(base64.b64decode(x))),('icefire','PAYLOAD_B85',lambda x:lzma.decompress(base64.b85decode(x)))]:
 cell={'master2965':3,'icefire':23}[name]
 d=literals(OUT/f'{name}_cell{cell}.txt');raw=decoder(d[var]);dest=OUT/name;dest.mkdir(exist_ok=True)
 (dest/'main.py').write_bytes(raw)
 for other in OUT.glob(name+'_cell*.txt'):
  try:data=literals(other)
  except SyntaxError:continue
  for key,value in data.items():
   if ('NOTICE' in key.upper() or 'LICENSE' in key.upper()) and isinstance(value,str):
    (dest/(key+'.txt')).write_text(value,encoding='utf-8')
 print(name,len(raw),hashlib.sha256(raw).hexdigest())
print('fieldcraft',[(p.name,p.stat().st_size) for p in (OUT/'fieldcraft').iterdir()])
