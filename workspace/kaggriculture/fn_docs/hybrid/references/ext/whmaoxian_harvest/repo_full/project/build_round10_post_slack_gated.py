"""Isolate the extra-market-sale case from unrestricted second-pass sorting."""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT / "experiments/round10_post_slack_reorder.py"
TARGET = ROOT / "experiments/round10_post_slack_gated.py"
assert hashlib.sha256(PARENT.read_bytes()).hexdigest() == "3440d01d8d5aaf43bb5d7fe7bd08e9cc420a287063d835d951bc2f149e4b724a"
source = PARENT.read_text(encoding="utf-8")
old = """    action = _R10PS_PARENT(observation, configuration)
    if int(observation['step']) >= 216 and _ig_standard(configuration):"""
new = """    prior_sales = int(_R9S_REPORT['sales'])
    action = _R10PS_PARENT(observation, configuration)
    if (int(observation['step']) >= 216 and _ig_standard(configuration)
            and int(_R9S_REPORT['sales']) > prior_sales):"""
assert source.count(old) == 1
content = source.replace(old, new)
if TARGET.exists():
    assert TARGET.read_text(encoding="utf-8") == content
else:
    TARGET.write_text(content, encoding="utf-8")
print(TARGET.relative_to(ROOT), hashlib.sha256(TARGET.read_bytes()).hexdigest())
