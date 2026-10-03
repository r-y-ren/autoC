"""Re-evaluate the final market order after V9's spare-hand sales."""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "submissions/release_v9/main.py"
TARGET = ROOT / "experiments/round10_post_slack_reorder.py"
EXPECTED = "6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3"
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED

SUFFIX = '''

# Round 10 isolated ablation: make final sales permutation see V9's slack credits.
_R10PS_PARENT = round9_slack_agent
_R10PS_REPORT = {'changes': 0, 'errors': 0}

def round10_post_slack_reorder_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for key in _R10PS_REPORT:
            _R10PS_REPORT[key] = 0
    action = _R10PS_PARENT(observation, configuration)
    if int(observation['step']) >= 216 and _ig_standard(configuration):
        try:
            result = _v44y_reorder(observation, action)
            _R10PS_REPORT['changes'] += int(result != action)
            return result
        except Exception:
            _R10PS_REPORT['errors'] += 1
    return action

round10_post_slack_reorder_agent.telemetry = _R10PS_REPORT
'''

content = SOURCE.read_text(encoding="utf-8") + SUFFIX
if TARGET.exists():
    assert TARGET.read_text(encoding="utf-8") == content
else:
    TARGET.write_text(content, encoding="utf-8")
print(TARGET.relative_to(ROOT), hashlib.sha256(TARGET.read_bytes()).hexdigest())
