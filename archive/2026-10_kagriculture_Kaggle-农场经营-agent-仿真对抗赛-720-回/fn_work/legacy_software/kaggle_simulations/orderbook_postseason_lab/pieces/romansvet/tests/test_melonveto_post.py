"""Post-ACTIONRL flooded-melon veto."""
from __future__ import annotations

import ast
import inspect

import _pin

_pin.bootstrap()

import numpy as np
from test_herd_ramp import _pmacro, _pview
from test_residual import _fn
from test_route_early import PIN_SEEDS, _digest, _plan, _seeded_case

from kagg3 import spec
from kagg3.core import plan as P


def _own_digests():
    return {str(seed): _digest(_plan(*_seeded_case(seed)))
            for seed in PIN_SEEDS[:2]}


def test_off_is_default_and_byte_identical_to_shipped():
    assert P.MELONVETO_POST_ON is False
    assert P.MELONVETO_POST_K == P.MELON_VETO_FLOOD_K == 60
    assert P.SWITCH_GENES[-1] == "MELONVETO_POST_ON"
    assert _own_digests() == _pin.tree_digests(__file__)


def test_post_veto_follows_residual_merge_and_removes_restored_melon(monkeypatch):
    tree = ast.parse(inspect.getsource(P._plan_and_stats))
    calls = [(n.lineno, ast.unparse(n)) for n in ast.walk(tree)
             if isinstance(n, ast.Call)]
    residual_line = next(n for n, call in calls
                         if call == "_residual_override(xp, view, macro)")
    veto_lines = [n for n, call in calls
                  if call.startswith("_melon_veto(xp, view, macro")]
    assert max(veto_lines) > residual_line

    view = _pview(P.MELON_VETO_FLOOD_DAY, P.MELON_VETO_FLOOD_K)
    before = P._melon_veto(np, view, _pmacro())
    monkeypatch.setattr(P, "RESIDUAL_FN", _fn(d_plant=4))
    after_head = P._residual_override(np, view, before)[0]
    after_post = P._melon_veto(np, view, after_head)
    assert int(before.plant_target[spec.I_MELON]) == 0
    assert int(after_head.plant_target[spec.I_MELON]) == 4
    assert int(after_post.plant_target[spec.I_MELON]) == 0


def test_post_k_is_independent_of_original_veto_k():
    macro = _pmacro()
    view = _pview(P.MELON_VETO_FLOOD_DAY, 60)
    assert int(P._melon_veto(np, view, macro, 40).plant_target[spec.I_MELON]) == 0
    assert int(P._melon_veto(np, view, macro, 80).plant_target[spec.I_MELON]) > 0


if __name__ == "__main__":
    for name, digest in _own_digests().items():
        print(name, digest)
