# -*- coding: utf-8 -*-
"""R26 测试面：verify_r43_gates（末 callable=_route40_agent 不变/身份链）。"""
from __future__ import annotations

import pytest

from orderbook_r43 import gates_r43 as g43

PKG = str(g43.MODULE_DIR / "build")


def test_gate_entry_zero_injection():
    """零注入断言：末 callable 仍是 _route40_agent。"""
    res = g43._gate_entry(PKG)
    assert res["passed"] is True
    assert res["entry"] == "_route40_agent"


def test_gate_identity_and_lineage():
    assert g43._gate_identity(PKG)["passed"] is True
    assert g43._gate_lineage(PKG)["passed"] is True
