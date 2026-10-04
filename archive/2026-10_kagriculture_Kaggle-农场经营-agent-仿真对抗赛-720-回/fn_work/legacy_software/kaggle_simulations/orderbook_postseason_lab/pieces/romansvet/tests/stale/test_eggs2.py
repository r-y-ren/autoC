"""EGGS2: GEESE_HERD_FIRST_ON gates the goose floor on days the cow/sheep lanes ask nothing; OFF is inert."""
import types

import numpy as np

from kagg3 import spec
from kagg3.core import plan

G = 2 + 5 + plan._A_GOOSE          # wheat, fert, 5 seed lanes, then the animal lanes


def _run(monkeypatch, a_want, a_have, ok, herd_first, head=0, target=5):
    monkeypatch.setattr(plan, "GEESE_TARGET", target)
    monkeypatch.setattr(plan, "GEESE_FIRST_DAY", None)
    monkeypatch.setattr(plan, "GEESE_HERD_FIRST_ON", herd_first)
    monkeypatch.setattr(plan, "_seed_room",
                        lambda xp, m, nf, sf, ah: (np.asarray(a_want, np.int32), np.int32(10)))
    kind = np.zeros(100, np.int32); occ = np.full(100, -1, np.int32)
    kind[:head] = spec.KIND_COOP; occ[:head] = plan._A_GOOSE
    view = types.SimpleNamespace(day=np.int32(12), seeds=np.zeros(5, np.int32), kind=kind, occ=occ)
    macro = plan.Macro(*[None] * len(plan.Macro._fields))._replace(plant_target=np.zeros(5, np.int32))
    out = plan._wants(np, view, macro, np.int32(20), np.int32(0), np.asarray(a_have, np.int32),
                      np.asarray(ok, bool), np.int32(0), np.int32(0))
    return out.tolist()


def test_herd_first_blocks_floor_when_herd_asks(monkeypatch):
    # cow lane open and asking 1: the floor waits (gated goose want is closed)
    ok = [False, True, False]
    assert _run(monkeypatch, [7, 2, 0], [3, 1, 0], ok, False)[G] == 2
    assert _run(monkeypatch, [7, 2, 0], [3, 1, 0], ok, True)[G] == 0


def test_herd_first_passes_floor_when_herd_idle(monkeypatch):
    ok = [False, False, False]
    assert _run(monkeypatch, [7, 2, 2], [3, 1, 1], ok, True)[G] == 2     # floor 5 - 3, cows/sheep gated shut


def test_off_is_inert():
    assert plan.GEESE_HERD_FIRST_ON is False and plan.GEESE_HANDS_ON is False
    assert plan.GEESE_TARGET == 0      # both EGGS2 blocks sit under GEESE_TARGET > 0


def test_goose_last_walk():
    # goose (lane 0) wants 3, cow 2, sheep 2 over 4 free tiles
    want = np.asarray([3, 2, 2], np.int32)
    assert plan._share(np, want, 4, plan.BEFORE_ALL).tolist() == [3, 1, 0]
    assert plan._share(np, want, 4, plan.BEFORE_GLAST).tolist() == [0, 2, 2]
    assert plan.GEESE_TILE_LAST_ON is False


def test_free_add_off():
    assert plan._BRAIN.GEESE_FREE_ADD is None
