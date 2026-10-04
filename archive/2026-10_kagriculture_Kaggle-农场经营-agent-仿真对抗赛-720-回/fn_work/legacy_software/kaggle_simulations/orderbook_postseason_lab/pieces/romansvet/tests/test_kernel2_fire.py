"""[KERNEL2FIRE1] the whitelist form of the KERNEL2 step-1 gate (`plan.KERNEL2_FIRE_CASH`, default "" = OFF).
Named-file test: .venv/bin/python -m pytest tests/test_kernel2_fire.py  (src = $KAGG3_SRC or <repo>/src)
* the "|"-list parses to exact ints (str or a lone int from the gene parser); "" is empty;
* OFF (FIRE_CASH "") = the legacy latch: v56 iff cash <= CASH_MAX and cash not in ZERO_CASH;
* ON: v56 iff the rival's step-1 cash is in the list; CASH_MAX and ZERO_CASH are ignored; unseen values -> PFS."""
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, os.environ.get("KAGG3_SRC") or str(Path(__file__).resolve().parents[1] / "src"))
from kagg3.agent import runtime as R  # noqa: E402
from kagg3.core import plan as P  # noqa: E402

V56 = {"farmer": ["V56"], "hands": [], "market": []}


def _obs(cash, player=0):
    farms = [{"money": 1500}, {"money": 1500}]
    farms[1 - player]["money"] = cash
    return {"day": 0, "hour": 1, "step": 1, "player": player, "farms": farms}


def _mode(cash, player=0):
    """Run the real Runtime._kernel2 step-1 latch on a stub self; return ("v56"|"pfs", action)."""
    me = SimpleNamespace(k2_mode=None, k2_buf=None, k2_fn=lambda o, c=None: dict(V56))
    a = R.Runtime._kernel2(me, _obs(cash, player), None)
    assert (a is None) == (me.k2_mode == "pfs")
    return me.k2_mode, a


@pytest.fixture(autouse=True)
def _switches(monkeypatch):
    monkeypatch.setattr(P, "KERNEL2_CASH_MAX", 2550)
    monkeypatch.setattr(P, "KERNEL2_ZERO_CASH", "")
    monkeypatch.setattr(P, "KERNEL2_ZERO_BACK", False)
    monkeypatch.setattr(P, "KERNEL2_H0_MERGE", True)
    monkeypatch.setattr(P, "KERNEL2_FIRE_CASH", "")
    monkeypatch.setattr(P, "KERNEL2_NOOP_H0", True)    # PACKV3: pin the kernel2v3 defaults this latch test was written under
    monkeypatch.setattr(P, "KERNEL2_INHERIT", False)   # (the ship tree defaults NOOP_H0=False/INHERIT=True need a full obs)


def test_default_is_off():
    # PACKV3 ship tree (ship_vrp15_k2fire): the default is the v3 real-h0 whitelist, not OFF (kernel2v3 asserted "").
    import importlib
    src = Path(P.__file__).read_text()
    assert '\nKERNEL2_FIRE_CASH = "99999"  # SHIP_VRP20_PFSOFF' in src   # PACK20 (vrp18 = 26|29|2046|2338|2438)
    assert importlib.reload(P) and P.KERNEL2_FIRE_CASH == "99999"


def test_parse():
    assert R.kernel2_cash_list("33|55|2339|2467") == {33, 55, 2339, 2467}
    assert R.kernel2_cash_list("55| 2339 |2467|") == {55, 2339, 2467}
    assert R.kernel2_cash_list(2467) == {2467}       # a lone value comes back from the gene parser as an int
    assert R.kernel2_cash_list("") == set()


def test_off_is_legacy(monkeypatch):
    for cash in (0, 33, 967, 1409, 2467, 2550):
        assert _mode(cash)[0] == "v56"
    for cash in (2551, 2857, 3000):
        assert _mode(cash)[0] == "pfs"
    monkeypatch.setattr(P, "KERNEL2_ZERO_CASH", "433|1033")
    assert _mode(433)[0] == "pfs" and _mode(1033)[0] == "pfs" and _mode(434)[0] == "v56"


def test_on_whitelist(monkeypatch):
    monkeypatch.setattr(P, "KERNEL2_FIRE_CASH", "33|55|2339|2467")
    for cash in (33, 55, 2339, 2467):
        for seat in (0, 1):
            m, a = _mode(cash, seat)
            assert m == "v56" and a["farmer"] == ["V56"]
    for cash in (0, 32, 34, 433, 967, 1033, 1303, 1409, 2338, 2466, 2468, 2550, 2857, 2867):
        assert _mode(cash) == ("pfs", None)


def test_on_ignores_cash_max_and_zero_cash(monkeypatch):
    monkeypatch.setattr(P, "KERNEL2_FIRE_CASH", "55|2339|2467|2857")
    monkeypatch.setattr(P, "KERNEL2_CASH_MAX", 100)
    monkeypatch.setattr(P, "KERNEL2_ZERO_CASH", "55|967")
    assert _mode(2857)[0] == "v56"                   # above CASH_MAX: fires
    assert _mode(55)[0] == "v56"                     # in ZERO_CASH: fires
    assert _mode(967)[0] == "pfs" and _mode(33)[0] == "pfs"


def test_on_int_value(monkeypatch):
    monkeypatch.setattr(P, "KERNEL2_FIRE_CASH", 2467)
    assert _mode(2467)[0] == "v56" and _mode(2339)[0] == "pfs"
