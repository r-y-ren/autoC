"""Decode public data literals only; do not execute notebook code."""
from pathlib import Path
import ast, base64, gzip, hashlib, io, json, tarfile, zlib
OUT=Path(__file__).resolve().parent/'notebooks'
DEST=OUT/'extracted'; DEST.mkdir(exist_ok=True)
def node(source,name):
    return next(n.value for n in ast.parse(source).body if isinstance(n,ast.Assign)
                and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
def literal(source,name): return ast.literal_eval(node(source,name))
def save_archive(name,data):
    folder=DEST/name; folder.mkdir(exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as archive:
        for member in archive.getmembers():
            target=folder/member.name
            if not member.isfile() or not target.resolve().is_relative_to(folder.resolve()):
                raise ValueError('Unsafe archive member')
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
    return folder
source=(OUT/'nathanjacob__kaggriculture-pipe-5-terminal-boost_5.py.txt').read_text(encoding='utf-8')
raw=gzip.decompress(base64.b64decode(literal(source,'AGENT_GZ_B64')))
assert hashlib.sha256(raw).hexdigest()==literal(source,'EXPECTED_SHA256')
folder=DEST/'pipe5';folder.mkdir(exist_ok=True);(folder/'main.py').write_bytes(raw)
source=(OUT/'tetsutani__market-smart-farming-kaggriculture_9.py.txt').read_text(encoding='utf-8')
data=base64.b64decode(literal(source,'ARCHIVE_B64'))
assert hashlib.sha256(data).hexdigest()==literal(source,'EXPECTED_ARCHIVE_SHA256')
folder=save_archive('market_smart',data)
assert hashlib.sha256((folder/'main.py').read_bytes()).hexdigest()==literal(source,'EXPECTED_MAIN_SHA256')
source=(OUT/'pilkwang__kaggriculture-structured-economic-policy_3.py.txt').read_text(encoding='utf-8')
expression=node(source,'archive_bytes')
assert isinstance(expression,ast.Call) and ast.unparse(expression.func)=='base64.b64decode'
data=base64.b64decode(ast.literal_eval(expression.args[0]))
assert hashlib.sha256(data).hexdigest()==literal(source,'EXPECTED_ARCHIVE_SHA256')
folder=save_archive('structured',data)
for name,digest in literal(source,'EXPECTED_FILES').items():
    assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest
source=(OUT/'hakdevelopment__kaggriculture-2887-score-fieldcraft-agent_4.py.txt').read_text(encoding='utf-8')
folder=DEST/'fieldcraft';folder.mkdir(exist_ok=True)
for name,payload in literal(source,'PAYLOADS').items():
    assert (folder/name).resolve().is_relative_to(folder.resolve())
    (folder/name).write_bytes(zlib.decompress(base64.b85decode(payload)))
(folder/'NOTICE.txt').write_text(literal(source,'NOTICE'),encoding='utf-8')
(folder/'LICENSE.txt').write_text(literal(source,'LICENSE'),encoding='utf-8')
(folder/'release.json').write_text(json.dumps(literal(source,'RELEASE'),indent=2),encoding='utf-8')
summary=[]
for path in DEST.rglob('*.py'):
    text=path.read_text(encoding='utf-8'); tree=ast.parse(text)
    imports=[ast.unparse(n) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
    suspicious=[(i+1,line[:240]) for i,line in enumerate(text.splitlines())
        if any(s in line for s in ('subprocess','os.system','requests.','urlopen','socket.','__import__','eval(','open('))]
    summary.append(dict(path=path.relative_to(DEST).as_posix(),bytes=path.stat().st_size,
        sha256=hashlib.sha256(path.read_bytes()).hexdigest(),imports=imports,suspicious=suspicious))
(OUT/'extraction_review.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary),flush=True)
