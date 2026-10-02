"""EGGDOSE1: the GEESE_TARGET gate bypass is capped at the floor; OFF is byte-identical."""
import os
import subprocess
import types
from pathlib import Path

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import plan

G = 2 + 5 + plan._A_GOOSE          # wheat, fert, 5 seed lanes, then the animal lanes


def _run(monkeypatch, target, a_want, a_have, ok, first=None, head=0):
    monkeypatch.setattr(plan, "GEESE_TARGET", target)
    monkeypatch.setattr(plan, "GEESE_FIRST_DAY", first)
    monkeypatch.setattr(plan, "_seed_room",
                        lambda xp, m, nf, sf, ah: (np.asarray(a_want, np.int32), np.int32(10)))
    kind = np.zeros(100, np.int32); occ = np.full(100, -1, np.int32)
    kind[:head] = spec.KIND_COOP; occ[:head] = plan._A_GOOSE
    view = types.SimpleNamespace(day=np.int32(12), seeds=np.zeros(5, np.int32), kind=kind, occ=occ)
    macro = plan.Macro(*[None] * len(plan.Macro._fields))._replace(plant_target=np.zeros(5, np.int32))
    out = plan._wants(np, view, macro, np.int32(20), np.int32(0), np.asarray(a_have, np.int32),
                      np.asarray(ok, bool), np.int32(0), np.int32(0))
    return out.tolist()


def test_target1_with_3_geese_is_zero(monkeypatch):
    # 3 geese standing, decode wants 2 more, gate closed: before the fix the lane was 2 (whole want bypassed)
    assert _run(monkeypatch, 1, [2, 0, 0], [0, 0, 0], [False] * 3, head=3)[G] == 0
    assert _run(monkeypatch, 1, [2, 0, 0], [0, 0, 0], [True] * 3, head=3)[G] == 2   # gated want still flows


def test_floor_is_a_stock(monkeypatch):
    # target 5, 3 standing, 1 in the shed, gate closed: buy 5 - 3 - 1 = 1
    assert _run(monkeypatch, 5, [7, 0, 0], [1, 0, 0], [False] * 3, head=3)[G] == 1
    # target met on the board: nothing bypasses
    assert _run(monkeypatch, 5, [7, 0, 0], [0, 0, 0], [False] * 3, head=5)[G] == 0


def test_floor_part_bypasses_rest_gated(monkeypatch):
    assert _run(monkeypatch, 5, [7, 2, 2], [3, 1, 1], [False] * 3)[G] == 2      # floor 5 - 3
    assert _run(monkeypatch, 5, [7, 2, 2], [3, 1, 1], [True] * 3)[G] == 4       # gate open: whole want
    assert _run(monkeypatch, 5, [7, 2, 2], [6, 1, 1], [False] * 3)[G] == 0      # floor met


def test_first_day(monkeypatch):
    assert _run(monkeypatch, 5, [7, 2, 2], [3, 1, 1], [False] * 3, first=13)[G] == 0
    assert _run(monkeypatch, 5, [7, 2, 2], [3, 1, 1], [False] * 3, first=12)[G] == 2


def test_off_is_inert():
    assert plan.GEESE_TARGET == 0 and plan.GEESE_FIRST_DAY is None
    assert plan._geese_day0() == plan.GEESE_DAY0


# OFF byte-parity vs master (9f6d1290) on 3 dev boards in the exact V56 sim (slow; EGGDOSE1_SLOW=1).
MASTER_ROWS = Path(__file__).resolve().parents[1] / "S/eggdose1/out/parity_master_0.tsv"


@pytest.mark.skipif(not os.environ.get("EGGDOSE1_SLOW"), reason="slow sim parity")
def test_off_parity_3_boards(tmp_path):
    wt = Path(__file__).resolve().parents[1]
    out = tmp_path / "off.tsv"
    env = dict(os.environ, JAX_PLATFORMS="cpu", KAGG3_SRC=str(wt / "src"),
               KAGG3_PPO_SW_EXTRA="RESIDUAL_RIVAL_PURSE_ON=True")
    subprocess.run([str(Path("/mnt/e/_work/kaggriculture3/.venv/bin/python")), str(wt / "S/eggdose1/screen.py"),
                    "dev", "0", "3", str(out)], check=True, env=env)
    cut = lambda p: [l.split("\t")[:6] for l in Path(p).read_text().splitlines()]
    assert cut(out) == cut(MASTER_ROWS)
