"""derive_market_variants 真值测试：编排+恒等断言+差分账本+确定性。"""

import json

import pytest

import derive_market_variants.derive_market_variants as dmv
from derive_market_variants.derive_market_variants import \
    derive_market_variants

N = 160


def _backbone():
    route = [{"farmer": ["NORTH"] if t % 2 else ["SOUTH"],
              "hands": [["WEST"]] if t % 3 else [], "market": []}
             for t in range(N)]
    route[10]["market"] = [["SELL", "WHEAT", 5], ["HIRE"]]
    for t in range(80, 89):                # 第 1 天卖压 270 > 日帽 240
        route[t]["market"] = [["SELL", "WHEAT", 30]]
    return route


def test_default_plan_eight_variants_all_identity_ok(tmp_path):
    out = tmp_path / "lib"
    result = derive_market_variants({"backbone_route": _backbone(),
                                     "output_dir": out})
    assert result["n_variants"] == 8 and result["n_rejected"] == 0
    assert set(result["variants"]) == {
        "shift_dp1", "shift_dm1", "shift_dp2", "shift_dm2",
        "scale_r0p75", "scale_r1p25", "cap_c120", "cap_c240"}
    for entry in result["ledger"]:
        assert entry["status"] == "ok"
        assert entry["farmer_identity"]["ok"] is True
        assert entry["changes"]["quantity_before"] > 0
    # 产物落盘且可复析
    on_disk = json.loads((out / "market_variants.json").read_text(
        encoding="utf-8"))
    assert set(on_disk) == set(result["variants"])
    ledger = json.loads((out / "variants_ledger.json").read_text(
        encoding="utf-8"))
    assert ledger["n_variants"] == 8
    assert ledger["backbone_sha256"] == result["backbone_sha256"]


def test_farmer_stream_byte_identical_in_every_variant(tmp_path):
    backbone = _backbone()
    result = derive_market_variants({"backbone_route": backbone,
                                     "output_dir": tmp_path})
    ref = [(s["farmer"], s["hands"]) for s in backbone]
    for name, route in result["variants"].items():
        assert [(s["farmer"], s["hands"]) for s in route] == ref
        assert len(route) == N
        # 每变体至少一处市场差分（确实是编辑而非复制）
        changed = sum(1 for a, b in zip(route, backbone)
                      if a["market"] != b["market"])
        assert changed >= 1, name


def test_shift_variants_conserve_quantity(tmp_path):
    result = derive_market_variants({"backbone_route": _backbone(),
                                     "output_dir": tmp_path})
    for name in ("shift_dp1", "shift_dm1", "shift_dp2", "shift_dm2"):
        entry = next(e for e in result["ledger"] if e["name"] == name)
        ch = entry["changes"]
        assert ch["quantity_after"] == ch["quantity_before"], name
        assert ch["orders"]["dropped"] == 0, name


def test_max_variants_cap(tmp_path):
    result = derive_market_variants({"backbone_route": _backbone(),
                                     "output_dir": tmp_path,
                                     "max_variants": 3})
    assert result["n_variants"] == 3
    assert [e["name"] for e in result["ledger"]] == [
        "shift_dp1", "shift_dm1", "shift_dp2"]


def test_operator_error_rejected_and_ledgered(tmp_path):
    plan = [{"name": "bad_op", "operator": "no_such_operator",
             "params": {}}]
    result = derive_market_variants({"backbone_route": _backbone(),
                                     "output_dir": tmp_path, "plan": plan})
    assert result["n_variants"] == 0
    assert result["rejected"][0]["status"] == "rejected_operator_error"


def test_identity_violation_rejected_and_ledgered(tmp_path, monkeypatch):
    """算子返回破坏走位流的磁带 -> 剔除留痕不熔断（跳过留痕纪律）。"""
    def broken_operator(payload):
        route = [dict(s) for s in payload["route"]]
        route[3]["farmer"] = ["EAST"]
        return {"route": route, "changes": {
            "operator": "broken", "params": {}, "band": None,
            "steps_touched": [3],
            "orders": {"moved": 0, "rescaled": 0, "capped": 0,
                       "dropped": 0},
            "quantity_before": 0, "quantity_after": 0}}
    monkeypatch.setattr(dmv, "apply_market_edit_operators", broken_operator)
    plan = [{"name": "broken_v", "operator": "broken", "params": {}}]
    result = derive_market_variants({"backbone_route": _backbone(),
                                     "output_dir": tmp_path, "plan": plan})
    assert result["n_variants"] == 0
    rejected = result["rejected"][0]
    assert rejected["status"] == "rejected_identity_violation"
    assert rejected["farmer_identity"]["first_divergence"] == 3


def test_double_run_byte_identical(tmp_path):
    backbone = _backbone()
    r1 = derive_market_variants({"backbone_route": backbone,
                                 "output_dir": tmp_path / "a"})
    r2 = derive_market_variants({"backbone_route": backbone,
                                 "output_dir": tmp_path / "b"})
    assert r1["variants_sha256"] == r2["variants_sha256"]
    for name in ("market_variants.json", "variants_ledger.json"):
        assert (tmp_path / "a" / name).read_bytes() == \
            (tmp_path / "b" / name).read_bytes()


def test_backbone_from_routes_json_default(tmp_path):
    lib = tmp_path / "library"
    lib.mkdir()
    backbone = _backbone()
    lib.joinpath("routes.json").write_text(
        json.dumps({"default": backbone}), encoding="utf-8")
    result = derive_market_variants({"library_dir": lib,
                                     "output_dir": tmp_path / "out"})
    assert result["n_variants"] == 8


def test_fail_closed_no_backbone(tmp_path):
    empty = tmp_path / "empty_lib"
    empty.mkdir()
    with pytest.raises(ValueError, match="fail-closed"):
        derive_market_variants({"library_dir": empty,
                                "output_dir": tmp_path})
    with pytest.raises(ValueError, match="fail-closed"):
        derive_market_variants({"backbone_route": [],
                                "output_dir": tmp_path})
