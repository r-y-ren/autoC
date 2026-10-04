"""Ablate the final sell ordering's start time on isolated V9 bytes."""
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parent
source = root / 'submissions/release_v9/main.py'
target = root / 'experiments/round10_market_early.py'
assert hashlib.sha256(source.read_bytes()).hexdigest() == '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'
code = source.read_text(encoding='utf-8')
start = code.index('def round9_final_market_agent(observation,configuration=None):')
end = code.index('round9_final_market_agent.telemetry', start)
block = code[start:end]
needle = "if int(observation['step'])>=216 and _ig_standard(configuration):"
assert block.count(needle) == 1
code = code[:start] + block.replace(needle, "if _ig_standard(configuration):") + code[end:]
if target.exists():assert target.read_text(encoding='utf-8') == code
else:target.write_text(code,encoding='utf-8')
print(target.relative_to(root),hashlib.sha256(target.read_bytes()).hexdigest())
