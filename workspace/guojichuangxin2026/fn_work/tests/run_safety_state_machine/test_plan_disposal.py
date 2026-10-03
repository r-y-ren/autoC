"""plan_disposal 单测。"""
from __future__ import annotations

CTX_OK = {"position": (32.0, 118.8), "home": (32.001, 118.8), "battery_remaining": 80,
          "wind_ms": 0, "gps_ok": True, "link_ok": True,
          "alternates": [(32.0005, 118.8, True)]}


def test_normal_prefers_rtl_by_energy():
    from run_safety_state_machine.plan_disposal import plan_disposal
    out = plan_disposal("S3", {}, CTX_OK)
    assert out["action"] == "返航"
    assert any(o["name"] == "原地安全降落" and o["ok"] for o in out["options"])


def test_low_battery_headwind_forbids_rtl():
    from run_safety_state_machine.plan_disposal import plan_disposal
    ctx = dict(CTX_OK, battery_remaining=8, wind_ms=9, position=(32.05, 118.8))
    out = plan_disposal("S3", {}, ctx)
    rtl = [o for o in out["options"] if o["name"] == "返航"][0]
    assert not rtl["ok"] and "禁止" in rtl["why"]
    assert out["action"] != "返航"


def test_dual_degrade_forbids_remote_dependent():
    from run_safety_state_machine.plan_disposal import plan_disposal
    ctx = dict(CTX_OK, gps_ok=False, link_ok=False)
    out = plan_disposal("S4", {}, ctx)
    rtl = [o for o in out["options"] if o["name"] == "返航"][0]
    assert not rtl["ok"] and "禁依赖远程" in rtl["why"]
