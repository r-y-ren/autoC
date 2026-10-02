"""The planner must only emit ops the simulator actually implements.

One engine branch is still deliberately absent from `sim/units.py`:

  * PLACE's shed-deposit fallthrough (kaggriculture.py:393-410) -- the sim
    implements only the animal-placement branch.

DROP (kaggriculture.py:343-356) used to be the other one. It landed in
`sim/units.py` on 2026-08-30 with the engine's exact discard semantics
(shed-adjacent only, whole inventory, capacity enforced at drop time, overflow
destroyed) and is pinned against the real engine by `tests/test_drop_op.py`.

A missing branch is safe *today* only because `core/plan.py` never emits an op
that would reach it. That is a property of the planner, not of the simulator, and
nothing else in the suite enforces it: add such an op to the planner's candidate
table and every existing gate still passes, while the sim silently diverges from
the engine the first time a unit reaches the branch.

The divergence would be quiet in the worst way -- the engine banks the items in
the shed, the sim drops them on the floor. No reward difference on the day it
happens, just a shed that slowly drifts out of sync and compounds through every
later sale.

What this file does NOT cover: the PLACE guard is checked at plan time by the
planner and at execution time by the engine. These tests pin the op *set*; they
do not prove the guard still holds hours later in the day. That case is argued
structurally instead -- BUILD cannot fail (it costs nothing and tests only
`tile is None`), and an inventory shortfall returns inside the tile-match branch
rather than falling through to the shed.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kagg3.core import ops as O

# Ops with a branch in sim/units.py. Nothing is excluded any more; keep this in
# sync with the simulator, and see the module docstring before adding anything.
UNIMPLEMENTED = frozenset()
IMPLEMENTED = frozenset(O.OP_NAMES) - UNIMPLEMENTED


def test_every_op_code_is_classified():
    """A newly added op code must be explicitly implemented or excluded.

    Without this, `OP_FOO = 18` lands in the table, the planner starts emitting
    it, and the subset check below still passes because nobody listed it as
    unimplemented.
    """
    assert set(O.OP_NAMES) == IMPLEMENTED | UNIMPLEMENTED
    assert len(O.OP_NAMES) == O.N_OPS


def test_planner_never_references_an_unimplemented_op():
    """`plan.py` is the only source of unit ops, so its source is the whole surface.

    A static read rather than a simulated one on purpose: it cannot be fooled by
    an op that only appears on a rare board state, which is exactly the case a
    rollout-based check would miss.
    """
    src = (ROOT / "src" / "kagg3" / "core" / "plan.py").read_text()
    referenced = set(re.findall(r"\bO\.(OP_[A-Z_]+)\b", src))
    bad = {n for n in referenced if getattr(O, n) in UNIMPLEMENTED}
    assert not bad, (
        f"plan.py emits {sorted(bad)}, which sim/units.py does not implement. "
        "Either add the branch to the simulator or drop it from the planner -- "
        "see this module's docstring for why the mismatch is silent."
    )
    # Guard against the regex silently matching nothing (a rename of the `O`
    # alias would make the test vacuously pass).
    assert "OP_PLACE" in referenced and "OP_PLANT" in referenced


def test_every_implemented_op_has_a_simulator_branch():
    """The simulator's source is the other half of the pairing.

    `IMPLEMENTED` is a hand-maintained list, so it has to be checked against the
    file it claims to describe -- otherwise emptying `UNIMPLEMENTED` is enough to
    make the test above pass with the branch still missing.
    """
    src = (ROOT / "src" / "kagg3" / "sim" / "units.py").read_text()
    referenced = set(re.findall(r"\bO\.(OP_[A-Z_]+)\b", src))
    attr = {getattr(O, n): n for n in dir(O) if n.startswith("OP_") and n != "OP_NAMES"}
    assert set(attr) == set(O.OP_NAMES), "an op code has no OP_* constant"
    missing = {attr[c] for c in IMPLEMENTED if attr[c] not in referenced}
    assert not missing, f"sim/units.py has no branch for {sorted(missing)}"
