"""R9 instruments + R10 sitl：抽象接口桩+后端继承链。"""

from __future__ import annotations

import pytest

from linkbench.instruments import b210_backend, pyvisa_backend
from linkbench.sitl import bridge


def test_backends_inherit_base_interface():
    j = b210_backend.B210Jammer()
    a = b210_backend.B210Monitor()
    vj = pyvisa_backend.PyVisaJammer("TCPIP0::x")
    jammer_api = ("set_style", "set_power_db", "on", "off")
    for obj in (j, vj):
        for m in jammer_api:
            assert callable(getattr(obj, m)), f"{type(obj).__name__}.{m}"
    assert callable(a.get_spectrum)


def test_off_is_stub_safe():
    with pytest.raises(NotImplementedError):
        b210_backend.B210Jammer().off()


def test_sitl_stub():
    with pytest.raises(NotImplementedError):
        bridge.inject_profile("runs/x")
