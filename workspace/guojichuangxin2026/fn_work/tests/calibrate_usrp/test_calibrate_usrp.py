"""calibrate_usrp 单测。"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from calibrate_usrp.calibrate_usrp import CalibError, calibrate_usrp


def test_dryrun_reference_table(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[2]
    monkeypatch.chdir(root)
    r = calibrate_usrp("dryrun")
    assert r["mode"] == "replay" and "floor_db" in r
    p = Path(r["table"])
    assert p.exists() and json.loads(p.read_text(encoding="utf-8"))["cal_db"] is not None
    p.unlink()


def test_device_without_uhd_raises(monkeypatch):
    import builtins
    real_import = builtins.__import__

    def no_uhd(name, *a, **kw):
        if name == "uhd":
            raise ImportError("no uhd")
        return real_import(name, *a, **kw)
    monkeypatch.setattr(builtins, "__import__", no_uhd)
    with pytest.raises(CalibError):
        calibrate_usrp("device")
