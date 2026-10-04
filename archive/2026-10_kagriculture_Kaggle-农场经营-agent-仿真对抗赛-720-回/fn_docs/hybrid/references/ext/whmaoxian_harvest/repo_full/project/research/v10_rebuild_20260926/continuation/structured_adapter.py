# Local evaluation adapter. Original public files remain byte-identical.
import sys, runpy, hashlib
from pathlib import Path
_FOLDER=Path('C:\\Users\\ASUS\\Documents\\ChatGPT\\kaggriculture\\research\\v10_rebuild_20260926\\notebooks\\extracted\\structured')
_HASHES={'main.py': '21e4b79bbc7bca97ad1af6337322303987d73d95b963b08ebe80a67900bd5360', 'upstream.py': '7eb5ab6c48581c82906ab6fa6b2cc5c9607513249ef59b2c45fcd6176e8653dd', 'market_primitives.py': 'dcfade4643811388ee0264046de23a1f69e44e72cb421e9fcac0930e6a48e67c', 'sheep_admission.py': '16b34ffd055dcfdab0ff728c0ac5524c1a83aacfae2f291eba56573ee4e4e4a4', 'candidate_config.json': '9e6ed4e18fa28cf51a63475b084baba7cdf3aee69757a457266bb903a162a04c'}
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
