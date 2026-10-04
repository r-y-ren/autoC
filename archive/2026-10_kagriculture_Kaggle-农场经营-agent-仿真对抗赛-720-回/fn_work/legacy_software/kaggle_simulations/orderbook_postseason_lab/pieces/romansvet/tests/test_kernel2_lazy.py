"""[STEP0TIME1] KERNEL2_PRELOAD=False = lazy V56 kernel.  Named-file test: .venv/bin/python -m pytest tests/test_kernel2_lazy.py
Ship config (KERNEL2_ON, NOOP_H0=False, INHERIT) with KERNEL2_PRELOAD=False:
* step 0: PFS plays its real h0, the V56 source is never exec'd (no kernel callable, no v56 module in sys.modules);
* step 1 on a fired seat (rival cash <= KERNEL2_CASH_MAX, not in ZERO_CASH): the kernel is built exactly once, then played;
* step 1 on a V / excluded-ZERO seat: the kernel is never built;
* control: KERNEL2_PRELOAD=True (the vrp14_k2real default) builds it at step 0.
The loader is counted (wrapping the real `kernel2_load`); INHERIT is switched off here only so step 1 needs no full obs
(the real-obs inherit path is proved coin-exact in S/step0time1)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
R = pytest.importorskip("kagg3.agent.runtime")
if not hasattr(R, "kernel2_load"):
    pytest.skip("tree without KERNEL2 (runs on k2lazy / ship_vrp14_* trees)", allow_module_level=True)
from kagg3.core import plan as P  # noqa: E402

SENT = {"farmer": ["PASS"], "hands": [], "market": [["SELL", "WHEAT", 1]]}


def _obs(step, rival_cash, player=0):
    farms = [{"money": 1409}, {"money": 1409}]
    farms[1 - player]["money"] = rival_cash
    return {"step": step, "day": step // 24, "hour": step % 24, "player": player, "farms": farms}


@pytest.fixture
def loads(monkeypatch):
    calls = []
    real = R.kernel2_load

    def counted():
        calls.append(1)
        fn = real()
        assert fn.__name__ == "e410_agent"
        return lambda obs, config=None: dict(SENT)
    monkeypatch.setattr(R, "kernel2_load", counted)
    for k, v in dict(KERNEL2_ON=True, KERNEL2_NOOP_H0=False, KERNEL2_INHERIT=False, KERNEL2_PRELOAD=False,
                     KERNEL2_CASH_MAX=2550, KERNEL2_ZERO_CASH="488|1088|1303|1409", KERNEL2_ZERO_BACK=False,
                     KERNEL2_FIRE_CASH="26|29|2046|2338|2438").items():   # PACK20: the vrp18 list keeps the fired-seat mechanics tested
        monkeypatch.setattr(P, k, v)
    return calls


def _v56_mods():
    return [m for m, mod in list(sys.modules.items()) if "v56" in m.lower()
            or str(getattr(mod, "__file__", "") or "").endswith("v56kernel.py")]


def test_lazy_step0_builds_nothing(loads):
    rt = R.Runtime(lambda *a, **k: None)
    assert rt._kernel2(_obs(0, 1409), None) is None          # PFS plays its real h0
    assert loads == [] and rt.k2_fn is None and _v56_mods() == []


@pytest.mark.parametrize("cash", [2438, 29, 2338])
def test_lazy_fired_step1_builds_once(loads, cash):
    rt = R.Runtime(lambda *a, **k: None)
    rt._kernel2(_obs(0, 1409), None)
    assert rt._kernel2(_obs(1, cash), None) == SENT and rt.k2_mode == "v56" and len(loads) == 1
    assert rt._kernel2(_obs(2, cash), None) == SENT and len(loads) == 1   # latched, not rebuilt
    assert _v56_mods() == []                                              # exec'd, never imported


@pytest.mark.parametrize("cash", [2800, 488, 1303])
def test_lazy_unfired_never_builds(loads, cash):
    rt = R.Runtime(lambda *a, **k: None)
    rt._kernel2(_obs(0, 1409), None)
    assert rt._kernel2(_obs(1, cash), None) is None and rt.k2_mode == "pfs"
    assert rt._kernel2(_obs(30, cash), None) is None
    assert loads == [] and rt.k2_fn is None


@pytest.mark.parametrize("cash", [26, 29, 190, 2046, 2338, 2438, 938])
def test_vrp20_default_never_fires(loads, monkeypatch, cash):
    """PACK20: under the tree default KERNEL2_FIRE_CASH "99999" no live h1 fires, nothing V56 is ever built."""
    import re
    dflt = re.search(r'^KERNEL2_FIRE_CASH = "([^"]*)"', Path(P.__file__).read_text(), re.M).group(1)   # the tree default (no reload)
    assert dflt == "99999"
    monkeypatch.setattr(P, "KERNEL2_FIRE_CASH", dflt)
    rt = R.Runtime(lambda *a, **k: None)
    rt._kernel2(_obs(0, 1409), None)
    assert rt._kernel2(_obs(1, cash), None) is None and rt.k2_mode == "pfs"
    assert rt._kernel2(_obs(30, cash), None) is None
    assert loads == [] and rt.k2_fn is None


def test_preload_control_builds_at_step0(loads, monkeypatch):
    monkeypatch.setattr(P, "KERNEL2_PRELOAD", True)
    rt = R.Runtime(lambda *a, **k: None)
    assert rt._kernel2(_obs(0, 1409), None) is None and len(loads) == 1 and rt.k2_fn is not None
    assert rt._kernel2(_obs(1, 2800), None) is None and rt.k2_fn is None      # V seat drops it
