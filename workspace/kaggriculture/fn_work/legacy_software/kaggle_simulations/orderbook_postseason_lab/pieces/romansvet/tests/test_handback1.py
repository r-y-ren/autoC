"""[HANDBACK1] the KERNEL2 hand-back (`plan.KERNEL2_HANDBACK_DAY`, default 0 = OFF): V56 plays d0 h1 .. d(D-1), PFS from the dawn of D.
Named-file test: .venv/bin/python -m pytest tests/test_handback1.py  (src = $KAGG3_SRC or <repo>/src)
* default 0 in the source; OFF the V56 latch never returns and the runtime's dawn history is untouched;
* ON: every kernel dawn before D rotates prev/dawn market inventory (PFS's first dawn reads the d(D-1) -> dD draw), the dawn of D
  flips the latch to "back" (PFS plays, VRP bank + fill ledger reset), a PFS-latched seat is unaffected;
* 3 boards (real engine, S/handback1/res/ctl_base.csv from S/handback1/run_all.sh): HANDBACK_DAY=0 on the handback1 tree reproduces
  the banked v2/v4g kernel rows (S/judgeall1/runs/mh4v2/band_on.csv) coin for coin (skipped when the control file is absent)."""
import csv
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

sys.path.insert(0, os.environ.get("KAGG3_SRC") or str(Path(__file__).resolve().parents[1] / "src"))
from kagg3.agent import runtime as R  # noqa: E402
from kagg3.core import plan as P  # noqa: E402
from kagg3 import spec  # noqa: E402

V56 = {"farmer": ["V56"], "hands": [], "market": []}
MAIN = Path(os.environ.get("HB_MAIN", "/mnt/e/_work/kaggriculture3"))


def _obs(day, hour, inv=None):
    return {"day": day, "hour": hour, "step": day * spec.TURNS_PER_DAY + hour, "player": 0,
            "farms": [{"money": 1500}, {"money": 2438}], "_inv": inv}


def _me():
    return SimpleNamespace(k2_mode="v56", k2_buf=None, k2_fn=lambda o, c=None: dict(V56), k2_back_checked=True,
                           pass_prev_mkt_inv=True, prev_mkt_inv=None, dawn_mkt_inv=np.zeros(9, np.int64),
                           vrp_saved=77, vrp_fill={"x": 1})


@pytest.fixture(autouse=True)
def _switches(monkeypatch):
    monkeypatch.setattr(P, "KERNEL2_NOOP_H0", False)
    monkeypatch.setattr(P, "KERNEL2_INHERIT", True)
    monkeypatch.setattr(P, "KERNEL2_ZERO_BACK", False)
    monkeypatch.setattr(P, "KERNEL2_FIRE_CASH", "26|29|2338|2438")
    monkeypatch.setattr(P, "KERNEL2_HANDBACK_DAY", 0)
    monkeypatch.setattr(R.parse, "parse_market", lambda o: (np.asarray(o["_inv"]),))


def test_default_is_off():
    import importlib
    # PACKHB1 ship tree (ship_vrp17_k2hb): the default is D18 (handback1 asserted 0 = OFF)
    assert "\nKERNEL2_HANDBACK_DAY = 18  # SHIP_VRP17_K2HB" in Path(P.__file__).read_text()
    assert importlib.reload(P) and P.KERNEL2_HANDBACK_DAY == 18


def test_off_never_hands_back():
    me = _me()
    for d in (1, 8, 10, 15, 29):
        for h in (0, 5):
            assert R.Runtime._kernel2(me, _obs(d, h, [d] * 9), None) == V56
    assert me.k2_mode == "v56" and me.prev_mkt_inv is None and not me.dawn_mkt_inv.any() and me.vrp_saved == 77


@pytest.mark.parametrize("D", [8, 10, 12, 15])
def test_on_hands_back_at_dawn(monkeypatch, D):
    monkeypatch.setattr(P, "KERNEL2_HANDBACK_DAY", D)
    me = _me()
    for d in range(1, D):
        for h in (0, 7, 23):
            assert R.Runtime._kernel2(me, _obs(d, h, [100 * d + h] * 9), None) == V56
    assert me.k2_mode == "v56"
    assert list(me.dawn_mkt_inv) == [100 * (D - 1)] * 9          # the d(D-1) dawn, recorded on a kernel turn
    assert R.Runtime._kernel2(me, _obs(D, 0, [100 * D] * 9), None) is None
    assert me.k2_mode == "back" and me.k2_fn is None and me.vrp_saved == 0 and me.vrp_fill == {} and me.k2_back_day == D
    assert list(me.dawn_mkt_inv) == [100 * (D - 1)] * 9          # PFS's own dawn rotation turns it into prev at dD
    assert R.Runtime._kernel2(me, _obs(D, 1, [0] * 9), None) is None and me.k2_mode == "back"


def test_on_pfs_seat_untouched(monkeypatch):
    monkeypatch.setattr(P, "KERNEL2_HANDBACK_DAY", 10)
    me = _me(); me.k2_mode = "pfs"
    for d in (1, 9, 10, 11):
        assert R.Runtime._kernel2(me, _obs(d, 0, [d] * 9), None) is None
    assert me.k2_mode == "pfs" and me.prev_mkt_inv is None and me.vrp_saved == 77


def test_three_boards_off_is_banked_kernel():
    ctl, base = MAIN / "S/handback1/res/ctl_base.csv", MAIN / "S/judgeall1/runs/mh4v2/band_on.csv"
    if not ctl.exists() or not base.exists():
        pytest.skip("HANDBACK1 control rows not present")
    B = {r["label"]: r for r in csv.DictReader(open(base))}
    rows = [r for r in csv.DictReader(open(ctl)) if not r["err"]]
    assert len(rows) == 3
    for r in rows:
        assert (int(r["ours"]), int(r["theirs"])) == (int(B[r["label"]]["ours"]), int(B[r["label"]]["theirs"])), r["label"]
