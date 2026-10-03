"""Decode public literal packages without running notebook cells."""
from pathlib import Path
import ast,base64,gzip,hashlib,json,lzma
OUT=Path(__file__).resolve().parent;N=OUT/'notebooks';DEST=N/'extracted'
def value(source,name):
    return ast.literal_eval(next(n.value for n in ast.parse(source).body if isinstance(n,ast.Assign)
        and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)))
source=(N/'leoprovorov__a-song-of-ice-and-fire-fixed-flexible_22.py.txt').read_text(encoding='utf-8')
raw=lzma.decompress(base64.b85decode(value(source,'PAYLOAD_B85')))
assert hashlib.sha256(raw).hexdigest()==value(source,'EXPECTED_MAIN_SHA256')
folder=DEST/'marketshock';folder.mkdir(exist_ok=True);(folder/'main.py').write_bytes(raw)
source=(N/'yhay81__shop-router-0909_3.py.txt').read_text(encoding='utf-8')
files=json.loads(gzip.decompress(base64.b64decode(value(source,'data_payload'))))
folder=DEST/'shoprouter';folder.mkdir(exist_ok=True)
for name,content in files.items():
    target=folder/name
    assert target.resolve().is_relative_to(folder.resolve())
    target.parent.mkdir(exist_ok=True,parents=True);target.write_text(content,encoding='utf-8')
code=(N/'yhay81__shop-router-0909_1.py.txt').read_text(encoding='utf-8')
(folder/'notebook_code.py.txt').write_text(code,encoding='utf-8')
summary=[]
for name in ('aurax','marketshock','shoprouter'):
    folder=DEST/name
    print(name,[(p.name,p.stat().st_size) for p in folder.iterdir()],flush=True)
    for path in folder.glob('*.py'):
        text=path.read_text(encoding='utf-8');tree=ast.parse(text)
        summary.append(dict(path=path.relative_to(DEST).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            imports=[ast.unparse(n) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]))
(OUT/'additional_decoded_manifest.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary),flush=True)
