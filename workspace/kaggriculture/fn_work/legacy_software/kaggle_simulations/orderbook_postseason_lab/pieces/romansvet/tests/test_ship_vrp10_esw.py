"""SHIP_VRP10_ESW (sub 56600971): res940_vrp10_esw = vrp8_jit + the ESWORK1 run2 g30 candidate as plan.ESWORK_THETA
(kagg3/core/eswork_theta.npy md5 6928257a). Named-file test: PYTHONPATH=src python -m pytest tests/test_ship_vrp10_esw.py"""
import hashlib
from pathlib import Path
import numpy as np
import pytest
from kagg3.core import plan as P

NPY = Path(P.__file__).resolve().parent / "eswork_theta.npy"


@pytest.fixture(autouse=True)
def _shipped(monkeypatch):
    """tests/conftest.py pins every test to the None graph; this file checks the shipped default itself."""
    monkeypatch.setattr(P, "ESWORK_THETA", np.load(NPY).astype(np.float32))


def test_theta_file_and_load():
    assert hashlib.md5(NPY.read_bytes()).hexdigest().startswith("6928257a")
    th = np.load(NPY).astype(np.float32)
    assert th.dtype == np.float32 and th.shape == (10,) and np.array_equal(th, np.load(NPY).astype(np.float32))
    assert np.all(th[[4, 6, 7, 8, 9]] == 0)
    src = Path(P.__file__).read_text()
    assert "\nESWORK_THETA = np.load(" in src   # the module default is the shipped theta (byte-equal to the upload)


def test_est_lead_follows_gene5():
    off = int(np.clip(P.EST_LEAD - round(float(P.ESWORK_THETA[5])), 0, 10))
    assert int(P._est_lead(np, 9)) == P.EST_LEAD
    assert int(P._est_lead(np, 10)) == off and int(P._est_lead(np, 29)) == off


def test_relay_cadence_follows_genes0to3():
    class V:
        pass
    want = np.clip(np.round(P.ESWORK_THETA[0:4]), 0, 6).astype(int)
    for d in range(30):
        v = V(); v.day = np.int32(d)
        got = int(P._mr_want(np, v))
        if d < 10 or d > 27:
            assert got == 0, d
        else:
            assert got in (0, int(want[min((d - 10) // 5, 3)])), d


def test_none_is_off(monkeypatch):
    monkeypatch.setattr(P, "ESWORK_THETA", None)
    assert P._est_lead(np, 20) == P.EST_LEAD
