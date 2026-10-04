"""Extract only explicit main.py cells and report syntax for manual security review."""
from pathlib import Path
import ast,hashlib,json
P=Path(__file__).resolve().parent;N=P/'public_notebooks';O=P/'public_programs';O.mkdir(exist_ok=True)
specs=[('thomastschinkel__the-2945-farm-96-vs-the-top-10-public-bots.json',5,'farm2945.py'),('ahmedberatozer__more-yield-smarter-labor.json',4,'yield_v37.py')]
reports=[]
for filename,index,target in specs:
    document=json.loads((N/filename).read_text(encoding='utf-8'))
    notebook=json.loads(document['blob'].get('source') or document['blob']['sourceNullable'])
    cell=notebook['cells'][index]['source'];cell=''.join(cell) if isinstance(cell,list) else cell
    lines=cell.splitlines();assert lines[0].strip()=='%%writefile main.py'
    source='\n'.join(lines[1:])+'\n';tree=ast.parse(source)
    imports=[ast.get_source_segment(source,node) for node in ast.walk(tree) if isinstance(node,(ast.Import,ast.ImportFrom))]
    suspicious=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            text=ast.unparse(node.func)
            if text in ('open','eval','exec','compile','__import__') or text.startswith(('os.','subprocess.','requests.','socket.','shutil.')):
                suspicious.append(dict(line=node.lineno,call=text,context=ast.get_source_segment(source,node)[:240]))
    path=O/target;data=source.encode('utf-8')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    report=dict(path=path.relative_to(P.parents[1]).as_posix(),sha256=hashlib.sha256(data).hexdigest(),lines=len(source.splitlines()),imports=imports,review_calls=suspicious,ending=source[-3500:])
    reports.append(report)
(N/'source_review.json').write_text(json.dumps(reports,indent=2,ensure_ascii=True))
print(json.dumps(reports,ensure_ascii=True),flush=True)
