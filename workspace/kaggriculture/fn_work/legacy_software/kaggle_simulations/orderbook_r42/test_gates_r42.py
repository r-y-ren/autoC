# -*- coding: utf-8 -*-
"""R25 测试面：verify_r42_gates（末 callable/身份链/谱系/h2h+净经济）。"""
from __future__ import annotations

import pytest

from orderbook_r42 import gates_r42 as g42

PKG = str(__import__("pathlib").Path(g42.MODULE_DIR) / "build")


def test_gate_entry_on_real_build():
    res = g42._gate_entry(PKG)
    assert res["passed"] is True and res["entry"] == "_route42_agent"


def test_gate_identity_and_lineage():
    ident = g42._gate_identity(PKG)
    assert ident["passed"] is True
    assert set(g42.CHAIN_ANCHORS) <= set(ident["chain"])
    lin = g42._gate_lineage(PKG)
    assert lin["passed"] is True


def test_gate_h2h_health_monkeypatched(monkeypatch):
    def _mk(margins):
        def _play(specs, cfg):
            n = len(list(specs))
            return [{"margin": margins[i % len(margins)]} for i in range(n)]
        return _play
    monkeypatch.setattr("orderbook_r42.judge_r25._play",
                        _mk([100, 50, 20]))
    res = g42._gate_h2h_and_health(PKG, "/tmp")
    assert res["passed"] is True and res["h2h_rate"] == 1.0
    monkeypatch.setattr("orderbook_r42.judge_r25._play",
                        _mk([-10, -20]))
    with pytest.raises(g42.GateR42Error):
        g42._gate_h2h_and_health(PKG, "/tmp")
