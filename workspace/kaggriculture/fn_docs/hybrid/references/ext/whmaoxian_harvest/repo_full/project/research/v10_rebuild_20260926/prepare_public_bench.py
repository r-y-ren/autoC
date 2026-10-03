"""Mechanical single-file packaging and review of public comparison programs."""
from pathlib import Path
import ast, hashlib, json
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
source=OUT/'notebooks/extracted'
programs=[]
for name in ('pipe5','market_smart','fieldcraft'):
    text=(source/name/'main.py').read_text(encoding='utf-8')
    if name=='fieldcraft':
        assert text.count('from mirror_plan import TAPE')==1
        text=(source/name/'mirror_plan.py').read_text(encoding='utf-8')+'\n'+text.replace('from mirror_plan import TAPE','')
    tree=ast.parse(text)
    forbidden=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            namecall=ast.unparse(node.func)
            if namecall in ('eval','__import__','open','os.system','subprocess.run'):
                forbidden.append([node.lineno,namecall])
    assert not forbidden, forbidden
    destination=source/name/'single_file.py'
    destination.write_text(text,encoding='utf-8')
    programs.append(dict(name=name,path=destination.relative_to(ROOT).as_posix(),
        sha256=hashlib.sha256(destination.read_bytes()).hexdigest(),mechanical_flattening=name=='fieldcraft',
        source_hash=hashlib.sha256((source/name/'main.py').read_bytes()).hexdigest()))
(OUT/'public_programs.json').write_text(json.dumps(programs,indent=2),encoding='utf-8')
print(json.dumps(programs),flush=True)
