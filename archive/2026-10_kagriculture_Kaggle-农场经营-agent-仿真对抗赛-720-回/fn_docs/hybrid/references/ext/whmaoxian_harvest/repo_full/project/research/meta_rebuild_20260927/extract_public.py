"""Extract literal, checksum-verified public agents; never run notebook setup cells."""
from pathlib import Path
import ast,base64,gzip,hashlib,io,json,tarfile,zlib
D=Path(__file__).resolve().parent;O=D/'public_agents';O.mkdir(exist_ok=True)
records=[]
for file in (D/'sources').glob('*.json'):
    obj=json.loads(file.read_text(encoding='utf-8'))
    nb=json.loads(obj['blob'].get('source') or obj['blob']['sourceNullable']);values={};trees=[]
    for cell in nb['cells']:
        if cell['cell_type']!='code':continue
        tree=ast.parse(''.join(cell['source']));trees.append(tree)
        for node in tree.body:
            if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
                if isinstance(node.value,ast.Constant):values[node.targets[0].id]=node.value.value
    if 'AGENT_B64' in values:
        name='pipe16';raw=gzip.decompress(base64.b64decode(values['AGENT_B64']));expected=values['EXPECTED_SHA256']
    elif '_PAYLOAD' in values:
        name='metav4';raw=zlib.decompress(base64.b64decode(values['_PAYLOAD']));expected=values['EXPECTED_SHA256']
    else:
        name='dmitrii';node=next(n for t in trees for n in t.body if isinstance(n,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='ARCHIVE_BYTES' for a in n.targets))
        assert ast.unparse(node.value.func)=='base64.b64decode'
        archive=base64.b64decode(ast.literal_eval(node.value.args[0]))
        assert hashlib.sha256(archive).hexdigest()==values['EXPECTED_ARCHIVE_SHA256']
        with tarfile.open(fileobj=io.BytesIO(archive),mode='r:gz') as tf:
            assert len(tf.getmembers())<=10
            raw=tf.extractfile('main.py').read()
            notice=tf.extractfile('NOTICE.txt').read();(O/(name+'.NOTICE.txt')).write_bytes(notice)
        expected=values['EXPECTED_MAIN_SHA256']
    assert len(raw)<15000000 and hashlib.sha256(raw).hexdigest()==expected
    source=raw.decode('utf-8');tree=ast.parse(source)
    path=O/(name+'.py');assert not path.exists();path.write_bytes(raw)
    imports=sorted({ast.unparse(n) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))})
    suspect=[]
    for n in ast.walk(tree):
        if not isinstance(n,ast.Call):continue
        f=ast.unparse(n.func)
        if any(w in f for w in ('open','exec','eval','load','read','write','system','spawn','environ','getenv')):
            suspect.append((n.lineno,f,ast.get_source_segment(source,n)[:240]))
    records.append(dict(name=name,path=str(path),sha256=expected,bytes=len(raw),imports=imports,review_calls=suspect,source_ref=obj['metadata']['ref'],note='Decoded and parsed only; pending source review before execution.'))
(D/'extraction_audit.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps(records),flush=True)
