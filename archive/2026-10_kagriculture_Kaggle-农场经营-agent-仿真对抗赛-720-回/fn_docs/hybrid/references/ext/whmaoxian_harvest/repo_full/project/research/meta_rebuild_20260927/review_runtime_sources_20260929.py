"""Recursively inspect literal exec payloads; no source is executed by this review."""
from pathlib import Path
import ast,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];O=D/'public_review_20260929'
base_tree=ast.parse((R/'submissions/release_v10_r2/main.py').read_text(encoding='utf-8'))
base_hashes={hashlib.sha256(ast.dump(n).encode()).hexdigest() for n in base_tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
records=[]
def inspect_source(text,label,depth=0):
    assert depth<=4 and len(text)<15000000
    tree=ast.parse(text);constants={}
    for n in tree.body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and isinstance(n.value,ast.Constant):constants[n.targets[0].id]=n.value.value
    imports=sorted({ast.unparse(n) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))})
    calls=[];children=[]
    for n in ast.walk(tree):
        if not isinstance(n,ast.Call):continue
        func=ast.unparse(n.func)
        if func=='exec':
            arg=n.args[0]
            if isinstance(arg,ast.Call) and isinstance(arg.func,ast.Name) and arg.func.id=='compile':arg=arg.args[0]
            if isinstance(arg,ast.Call) and isinstance(arg.func,ast.Attribute) and arg.func.attr=='decode' and isinstance(arg.func.value,ast.Name):
                value=constants[arg.func.value.id].decode('utf-8')
            else:value=arg.value if isinstance(arg,ast.Constant) else constants.get(arg.id) if isinstance(arg,ast.Name) else None
            assert isinstance(value,str),('unresolved exec',label,n.lineno)
            child=label+'_exec'+str(n.lineno);(O/(child+'.py.txt')).write_text(value,encoding='utf-8')
            children.append(child);inspect_source(value,child,depth+1)
        elif any(w in func.lower() for w in ('open','eval','read','write','system','spawn','environ','getenv','getattr','setattr')):calls.append((n.lineno,func,ast.get_source_segment(text,n)[:180]))
    funcs=[dict(name=n.name,line=n.lineno,unchanged_r2=hashlib.sha256(ast.dump(n).encode()).hexdigest() in base_hashes) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
    records.append(dict(label=label,imports=imports,calls=calls,children=children,functions=funcs))
for name in ('v37','salem','jaxa'):inspect_source((O/(name+'.py')).read_text(encoding='utf-8'),name)
(O/'runtime_review.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps(records),flush=True)
