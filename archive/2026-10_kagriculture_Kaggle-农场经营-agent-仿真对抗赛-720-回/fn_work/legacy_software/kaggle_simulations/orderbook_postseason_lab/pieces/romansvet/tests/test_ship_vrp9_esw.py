"""STACKESW1: res940_vrp9_esw = res940_vrp8_jit (vrp7 + compiled router kernels route_vrp_c.so + deep RR 150/10/ON)
+ the ESWORK1 g15 centre (relay wheat 2/4/2/3 plantings/day d10-14/15-19/20-24/25-27, EST_LEAD 5 -> 3 on d10+).
Named-file test: KAGG3_ROOT=$PWD PYTHONPATH=src python -m pytest tests/test_ship_vrp9_esw.py"""
import hashlib
from pathlib import Path
import numpy as np
from kagg3.core import plan as P
from kagg3.agent import route_vrp as RV

HERE = Path(P.__file__).resolve().parent


def test_both_hunk_sets_present():
    assert hashlib.md5((HERE / "eswork_theta.npy").read_bytes()).hexdigest().startswith("470cf405")
    assert P.ESWORK_THETA is not None and P.ESWORK_THETA.shape == (10,)
    assert (P.ROUTE_VRP_RR_ITERS, P.ROUTE_VRP_RR_K, P.ROUTE_VRP_RR_RESOLVE_ON, P.ROUTE_VRP_JIT_ON) == (150, 10, True, True)
    so = HERE.parent / "agent" / "route_vrp_c.so"
    assert hashlib.md5(so.read_bytes()).hexdigest().startswith("f7b5941b")


def test_jit_live_and_deep_knobs():
    assert RV.jit_live()
    assert tuple(RV._rr_knobs(20)) == (150, 10, True)


def test_eswork_levers():
    assert int(P._est_lead(np, 9)) == P.EST_LEAD == 5 and int(P._est_lead(np, 10)) == 3

    class V:  # the only field _mr_want reads
        pass
    got = []
    for d in range(30):
        v = V(); v.day = np.int32(d); got.append(int(P._mr_want(np, v)))
    assert got[:10] == [0] * 10 and set(got[10:15]) == {2} and set(got[15:20]) == {4} and set(got[20:25]) == {2}
    assert all(g in (0, 3) for g in got[25:28]) and got[28:] == [0, 0]


def test_router_file_is_vrp8_jit():
    # route_vrp.py / .c / .so are byte-equal to the routerjit1 (vrp8_jit, sub 56580780) files
    md5 = lambda p: hashlib.md5((HERE.parent / "agent" / p).read_bytes()).hexdigest()
    assert md5("route_vrp.py").startswith("eb919fb1") and md5("route_vrp_c.c").startswith("03012333")
