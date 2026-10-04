"""Build frozen study candidates containing arithmetic forest data only."""
from pathlib import Path
import base64,hashlib,json,zlib
N=Path(__file__).resolve().parent;R=N.parents[1];DEST=N/'flow_candidates_v2';DEST.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
features=(N/'flow_features.py').read_text(encoding='utf-8');model=json.loads((N/'flow_model.json').read_text())
assert hashlib.sha256((N/'flow_features.py').read_bytes()).hexdigest()==model['feature_source_sha256']
forest=json.dumps(model['forest'],separators=(',',':')).encode()
blob=base64.b85encode(zlib.compress(forest,9)).decode()
configs=[('observe','observe',.2,216),('filter20','filter',.2,216),('filter40','filter',.4,216),
    ('replace20','replace',.2,216),('replace40','replace',.4,216),('replace20_late','replace',.2,360),
    ('reorder','reorder',.2,216),('combined20','combined',.2,216)]
manifest=[]
for name,mode,threshold,start in configs:
    source=base.decode('utf-8')
    if mode in ('filter','replace','combined'):
        old='if debts is None or int(st["stock"].get(item, 0)) < _OR2_SN_K:'
        new='if debts is None or not _mp_allow_sn(observation,item) or int(st["stock"].get(item, 0)) < _OR2_SN_K:'
        assert source.count(old)==1;source=source.replace(old,new)
    source+='\n'+features
    source+='\nimport base64,json,zlib\n_MP_FOREST=json.loads(zlib.decompress(base64.b85decode('+repr(blob)+')))\n'
    source+=f'_MP_MODE={mode!r}\n_MP_THRESHOLD={threshold!r}\n_MP_START={start}\n_MP_VOLUME_SCALE=2.0\n_MP_REORDER_MIN=2.0\n'
    source+=(N/'flow_policy_tail.py.txt').read_text(encoding='utf-8')
    target=DEST/(name+'.py');compile(source,str(target),'exec');target.write_bytes(source.encode('utf-8'));compile(target.read_bytes(),str(target),'exec')
    manifest.append(dict(name=name,path=target.relative_to(R).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),mode=mode,threshold=threshold,start=start))
(N/'flow_candidates_v2_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest),forest_bytes=len(forest))),flush=True)
