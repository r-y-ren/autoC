"""Build a bounded courier experiment; retain all upstream notices verbatim."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / "external/one_more_wheat.py").read_bytes()
extension = b'''

# Local experimental modification, 2026-09-22, Apache-2.0.
# EGG and TOMATO also have no downstream farm-input use. Existing courier
# eligibility proves that the worker has no productive tape work left today;
# use those already-idle workers to return these goods before the last market.
# All existing cash, warehouse and action-count guards remain in the parent.
V9_COURIER_ITEMS = ("STRAWBERRY", "MILK", "WOOL", "MELON", "EGG", "TOMATO")
'''
target = root / "experiments/round7_local_courier.py"
target.write_bytes(source + extension)
print(target)
