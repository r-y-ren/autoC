"""Isolated complete ranch experiments; forced variants test mechanism, not release."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
tail=(R/'research/macro_population_20260927/ranch_tail.py.txt').read_text()
tail=tail.replace('if demand<9:return None','if demand<9 and not _RX_FORCE:return None')
tail=tail.replace('4*n for d,n','sum(map(len,_RX_GROUPS))*n for d,n')
tail=tail.replace('feed=4*days*','feed=sum(map(len,_RX_GROUPS))*days*')
tail=tail.replace('fertilizer=4*max','fertilizer=sum(map(len,_RX_GROUPS))*max')
tail=tail.replace("capital=4000+4*_HD2_SPEC","capital=4000+sum(map(len,_RX_GROUPS))*_HD2_SPEC")
tail=tail.replace("['BUY_ANIMAL',_RX_ANIMAL,4]","['BUY_ANIMAL',_RX_ANIMAL,sum(map(len,_RX_GROUPS))]")
tail=tail.replace("day==_RX_DAY and can_request","_RX_DAY<=day<_RX_DAY+3 and can_request")
original='_RX_GROUPS=(((5,5),(6,5)),((5,6),(6,6)))'
assert original in tail
out=P/'ranches';out.mkdir(exist_ok=True);variants=[]
for animal in ('SHEEP','COW','GOOSE'):
    for day in (11,14):
        for size in (4,8):
            groups=(((5,5),(6,5)),((5,6),(6,6))) if size==4 else (((5,5),(6,5),(7,5),(8,5)),((5,6),(6,6),(7,6),(8,6)))
            constants=f'\n_RX_ANIMAL={animal!r}\n_RX_DAY={day}\n_RX_MIN_NET=-1000000\n_RX_FORCE=True\n'
            code=tail.replace(original,'_RX_GROUPS='+repr(groups))
            data=base+constants.encode()+code.encode()+b'\n_MP_REPORT=_RX_REPORT\n'
            path=out/f'{animal.lower()}_d{day}_n{size}.py';compile(data,str(path),'exec')
            if path.exists():assert path.read_bytes()==data
            else:path.write_bytes(data)
            variants.append(dict(path=path.relative_to(R).as_posix(),animal=animal,day=day,animals=size,sha256=hashlib.sha256(data).hexdigest(),scope='Exploratory activation; not release-approved'))
(P/'ranch_manifest.json').write_text(json.dumps(variants,indent=2))
print(json.dumps(dict(variants=len(variants),complete=True,release=False)),flush=True)
