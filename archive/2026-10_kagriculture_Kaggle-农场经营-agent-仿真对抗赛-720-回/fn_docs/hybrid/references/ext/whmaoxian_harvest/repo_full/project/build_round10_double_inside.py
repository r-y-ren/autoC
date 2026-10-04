"""Ablate whether the second market pass needs the slack-worker wrapper."""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "submissions/release_v9/main.py"
TARGET = ROOT / "experiments/round10_double_inside.py"
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == "6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3"
source = SOURCE.read_text(encoding="utf-8")
old = """        result=_v44y_reorder(observation,action)
        _R9M_REPORT['changes']+=int(result!=action)"""
new = """        result=_v44y_reorder(observation,action)
        result=_v44y_reorder(observation,result)
        _R9M_REPORT['changes']+=int(result!=action)"""
assert source.count(old) == 1
content = source.replace(old, new)
if TARGET.exists():
    assert TARGET.read_text(encoding="utf-8") == content
else:
    TARGET.write_text(content, encoding="utf-8")
print(TARGET.relative_to(ROOT), hashlib.sha256(TARGET.read_bytes()).hexdigest())
