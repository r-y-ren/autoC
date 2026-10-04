"""Isolate the final clone-model market reordering assumption in V9."""
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parent
source = root / 'submissions/release_v9/main.py'
target = root / 'experiments/round10_no_final_reorder.py'
assert hashlib.sha256(source.read_bytes()).hexdigest() == '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'
text = source.read_text(encoding='utf-8')
start = text.index('def round9_final_market_agent(observation,configuration=None):')
end = text.index('round9_final_market_agent.telemetry', start)
old = text[start:end]
needle = "if int(observation['step'])>=216 and _ig_standard(configuration):"
assert old.count(needle) == 1
text = text[:start] + old.replace(needle, "if False and int(observation['step'])>=216 and _ig_standard(configuration):") + text[end:]
if target.exists():assert target.read_text(encoding='utf-8') == text
else:target.write_text(text,encoding='utf-8')
print(target.relative_to(root),hashlib.sha256(target.read_bytes()).hexdigest())
