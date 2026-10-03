"""Mechanical self-contained wrappers for external evaluation programs."""
from pathlib import Path
import ast,base64,hashlib,json,zlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];D=OUT/'notebooks/extracted'
records=[]
folder=D/'shoprouter';text=(folder/'notebook_code.py.txt').read_text(encoding='utf-8').split('\n',1)[1]
blob=base64.b85encode(zlib.compress((folder/'actions.json').read_bytes(),9)).decode()
old='self.tapes = json.loads((Path(folder) / "actions.json").read_text())'
new='self.tapes = json.loads(__import__("zlib").decompress(__import__("base64").b85decode('+repr(blob)+')))'
assert text.count(old)==1;text=text.replace(old,new)
path=folder/'single_file.py';path.write_text(text,encoding='utf-8');compile(text,str(path),'exec')
records.append(dict(name='shoprouter',path=path.relative_to(ROOT).as_posix(),role='additional_development',sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
for name,role in [('aurax','additional_development'),('marketshock','sealed_opponent')]:
    path=D/name/'main.py';text=path.read_text(encoding='utf-8');tree=ast.parse(text)
    prohibited=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and ast.unparse(node.func) in ('os.system','subprocess.run','requests.get','socket.socket'):
            prohibited.append(node.lineno)
    assert not prohibited,(name,prohibited)
    records.append(dict(name=name,path=path.relative_to(ROOT).as_posix(),role=role,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(OUT/'additional_programs.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('Packaged comparison programs',[(r['name'],r['role']) for r in records],flush=True)
