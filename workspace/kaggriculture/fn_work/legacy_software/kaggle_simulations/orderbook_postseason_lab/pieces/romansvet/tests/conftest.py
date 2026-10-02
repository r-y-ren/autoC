"""[SHIP_VRP10_ESW] plan.ESWORK_THETA ships the ESWORK1 g30 theta (kagg3/core/eswork_theta.npy). Every pinned digest in
tests/ was cut on the `None` graph (vrp8_jit / vrp9_cs), so each test starts from None; tests/test_ship_vrp10_esw.py
checks the shipped default itself."""
import sys

import pytest


@pytest.fixture(autouse=True)
def _eswork_theta_none(monkeypatch):
    P = sys.modules.get("kagg3.core.plan")
    if P is not None:
        monkeypatch.setattr(P, "ESWORK_THETA", None)
    yield
