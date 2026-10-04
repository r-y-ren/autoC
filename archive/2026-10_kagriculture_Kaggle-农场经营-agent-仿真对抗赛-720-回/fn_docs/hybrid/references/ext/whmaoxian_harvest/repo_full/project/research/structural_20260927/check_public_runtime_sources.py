"""Review literal embedded unit-model sources and require optional inputs absent."""
from pathlib import Path
import ast,hashlib,json,os
P=Path(__file__).resolve().parent
reports=[]
for name in ('farm2945.py','yield_v37.py'):
    path=P/'public_programs'/name;source=path.read_text(encoding='utf-8');tree=ast.parse(source)
    embedded=[];env_keys=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and ast.unparse(n.func)=='exec':
            assert n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str)
            code=n.args[0].value;inner=ast.parse(code)
            imports=[ast.unparse(x) for x in ast.walk(inner) if isinstance(x,(ast.Import,ast.ImportFrom))]
            calls=[ast.unparse(x.func) for x in ast.walk(inner) if isinstance(x,ast.Call) and (ast.unparse(x.func) in ('open','exec','eval','__import__') or ast.unparse(x.func).startswith(('os.','subprocess.','requests.','socket.')))]
            embedded.append(dict(sha256=hashlib.sha256(code.encode()).hexdigest(),imports=imports,review_calls=calls))
        if isinstance(n,ast.Call) and '.environ.get' in ast.unparse(n.func):
            assert n.args and isinstance(n.args[0],ast.Constant)
            env_keys.append(n.args[0].value)
    present=[k for k in env_keys if k in os.environ]
    reports.append(dict(file=name,embedded=embedded,optional_environment_keys=env_keys,present=present))
print(json.dumps(reports,ensure_ascii=True),flush=True)
(P/'public_notebooks/runtime_review.json').write_text(json.dumps(reports,indent=2))
assert all(not r['present'] and all(not x['review_calls'] for x in r['embedded']) for r in reports)
