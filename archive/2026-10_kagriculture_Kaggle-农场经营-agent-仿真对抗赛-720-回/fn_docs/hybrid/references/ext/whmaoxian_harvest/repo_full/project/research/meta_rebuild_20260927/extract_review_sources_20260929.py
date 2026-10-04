"""Literal public-source extraction and static inventory; no downloaded code execution."""
from pathlib import Path
import ast,base64,gzip,hashlib,json
D=Path(__file__).resolve().parent/'public_review_20260929';records=[]
for name,file in [('v37','ahmedberatozer__more-yield-smarter-labor.json'),('salem','salemali7__kaggriculture-2900.json'),('jaxa','jaxa623__2780-beyond-48-0-128-128-worlds-with-95-cis.json')]:
    obj=json.loads((D/file).read_text(encoding='utf-8'));nb=json.loads(obj['blob'].get('source') or obj['blob']['sourceNullable'])
    code=[''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code'];constants={}
    for cell in code:
        if cell.startswith('%%'):continue
        tree=ast.parse(cell)
        for node in tree.body:
            if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
                try:constants[node.targets[0].id]=ast.literal_eval(node.value)
                except (ValueError,TypeError):pass
    if name!='jaxa':
        cell=next(c for c in code if c.startswith('%%writefile main.py'))
        raw=cell.split('\n',1)[1].encode()
        if 'EXPECTED_MAIN_SHA256' in constants:assert hashlib.sha256(raw).hexdigest()==constants['EXPECTED_MAIN_SHA256']
    else:
        blobs=[v for v in constants.values() if isinstance(v,str) and len(v)>100000]
        assert len(blobs)==1
        raw=gzip.decompress(base64.b85decode(blobs[0]));assert hashlib.sha256(raw).hexdigest()==constants['MAIN_SHA256']
    target=D/(name+'.py')
    if target.exists():assert target.read_bytes()==raw
    else:target.write_bytes(raw)
    text=raw.decode();tree=ast.parse(text);imports=sorted({ast.unparse(n) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))})
    calls=[dict(line=n.lineno,call=ast.unparse(n.func)) for n in ast.walk(tree) if isinstance(n,ast.Call) and any(s in ast.unparse(n.func).lower() for s in ('open','exec','eval','load','read','write','system','spawn','environ','getenv'))]
    records.append(dict(name=name,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),imports=imports,calls=calls))
    notes='\n\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type']=='markdown')
    (D/(name+'_notes.md')).write_text(notes,encoding='utf-8')
(D/'static_source_review.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps(records),flush=True)
