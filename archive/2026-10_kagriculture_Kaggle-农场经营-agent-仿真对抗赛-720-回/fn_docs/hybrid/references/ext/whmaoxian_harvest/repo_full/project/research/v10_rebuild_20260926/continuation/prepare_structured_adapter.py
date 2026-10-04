"""Wrap the untouched multi-file public opponent; never a submission candidate."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent; W=D.parent; R=W.parents[1]
folder=W/'notebooks/extracted/structured'
files=['main.py','upstream.py','market_primitives.py','sheep_admission.py','candidate_config.json']
manifest={name:hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in files}
text='''# Local evaluation adapter. Original public files remain byte-identical.
import sys, runpy, hashlib
from pathlib import Path
_FOLDER=Path(FOLDER_LITERAL)
_HASHES=HASH_LITERAL
for _name,_sha in _HASHES.items():
    assert hashlib.sha256((_FOLDER/_name).read_bytes()).hexdigest()==_sha
sys.path.insert(0,str(_FOLDER))
try:
    import market_primitives
    _NS=runpy.run_path(str(_FOLDER/'main.py'))
finally:
    sys.path.pop(0)
_ENTRY=_NS['agent']
def structured_opponent(observation,configuration=None):
    return _ENTRY(observation,configuration)
structured_opponent.telemetry=_ENTRY.telemetry
'''.replace('FOLDER_LITERAL',repr(str(folder))).replace('HASH_LITERAL',repr(manifest))
(D/'structured_adapter.py').write_text(text,encoding='utf-8')
(D/'structured_dependencies.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Untouched structured program adapter prepared')
