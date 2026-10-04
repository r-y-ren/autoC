"""Repair a demonstrated 15-coin opening shortfall by market slot ordering."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / 'experiments/round7_routes/vadim_111917373_v2.py').read_text(encoding='utf-8')
extension = '''
# Local experimental repair, 2026-09-22, Apache-2.0.
# The original first-step COW purchase delays the five-wheat buy until market
# slot 1, after a rival's opening grain purchases raise its quote. Put the
# necessary grain purchase in slot 0; preserve all original quantities and
# productive worker actions. The cow is available on exactly the same turn.
_R7_OPENING_MARKET = _DEMO_TAPE[0]["market"]
assert _R7_OPENING_MARKET == [["BUY_ANIMAL", "COW", 1], ["BUY_PRODUCT", "WHEAT", 5]]
_DEMO_TAPE[0]["market"] = [_R7_OPENING_MARKET[1], _R7_OPENING_MARKET[0]]
'''
(root / 'experiments/round7_improved.py').write_text(source + extension, encoding='utf-8', newline='\n')
