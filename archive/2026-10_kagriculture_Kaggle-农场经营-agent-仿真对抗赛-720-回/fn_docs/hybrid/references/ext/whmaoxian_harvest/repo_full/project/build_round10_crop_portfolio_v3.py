"""Keep a four-strawberry insurance tranche for unknown future shop demand."""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT / "experiments/round10_crop_portfolio_v2.py"
TARGET = ROOT / "experiments/round10_crop_portfolio_v3.py"
EXPECTED = "9a982d7e340f3ca2714f10203e8e11ec54024f2fc3856cc4718737c7efa4ed23"
assert hashlib.sha256(PARENT.read_bytes()).hexdigest() == EXPECTED

source = PARENT.read_text(encoding="utf-8")
old = "candidates = [(value(k),k) for k in (5,9,13)]"
new = "candidates = [(value(k),k) for k in (5,9)]"
assert source.count(old) == 1
content = source.replace(old, new)
compile(content, str(TARGET), "exec")
if TARGET.exists():
    assert TARGET.read_text(encoding="utf-8") == content
else:
    TARGET.write_text(content, encoding="utf-8")
print(TARGET.relative_to(ROOT), hashlib.sha256(TARGET.read_bytes()).hexdigest())
