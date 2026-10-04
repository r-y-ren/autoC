# -*- coding: utf-8 -*-
"""R17 测试面：gates_r35（五门编排 fail-closed 全跑）。"""
import json

import pytest

from orderbook_r35 import gates_r35 as G


@pytest.fixture()
def fake_pkg(tmp_path):
    pkg = tmp_path / "r35"
    pkg.mkdir()
    (pkg / "main.py").write_text("def agent(o, c=None):\n    return {}\n")
    (pkg / "submission.tar.gz").write_bytes(b"tar")
    (pkg / "build_manifest.json").write_text("{}")
    return pkg


def _gate(result_overrides=None, raise_exc=None):
    base = {"passed": True, "n": 16, "wins": 12, "losses": 2, "ties": 2,
            "rate": 0.75, "mean_margin": 120.0, "per_opponent": {},
            "starve_free": True, "n_games": 26, "n_errors": 0,
            "n_starve_red_games": 0, "subset": True, "attribution": {},
            "gates": {"load": True, "full_episodes": True, "determinism": True,
                      "package": True}}

    def thunk(*a, **k):
        if raise_exc:
            raise raise_exc
        out = dict(base)
        out.update(result_overrides or {})
        return out
    return thunk


def test_verify_all_green(fake_pkg, monkeypatch):
    monkeypatch.setattr(G, "_gate_launch_fourgate", _gate())
    monkeypatch.setattr(G, "_gate_h2h_vs_r34a", _gate())
    monkeypatch.setattr(G, "_gate_lineage", _gate())
    monkeypatch.setattr(G, "_gate_starve_subset", _gate())
    monkeypatch.setattr(G, "_gate_diff_audit", _gate())
    monkeypatch.setattr(G, "_verify_ref_package",
                        lambda d, w: {"what": w, "match": True})
    summary = G.verify_r35_gates(str(fake_pkg))
    assert summary["overall"] is True
    assert set(summary["gates_passed"].values()) == {True}
    ev = fake_pkg / "evidence" / "verify_summary_r35.json"
    assert ev.is_file()
    assert json.loads(ev.read_text())["protocol"] == "verify-r35/1.0"


def test_verify_fail_closed_all_gates_run(fake_pkg, monkeypatch):
    """一门红也全跑不短路；红门入台账；overall=False。"""
    called = []

    def wrap(name, thunk):
        def inner(*a, **k):
            called.append(name)
            return thunk(*a, **k)
        return inner

    monkeypatch.setattr(G, "_gate_launch_fourgate",
                        wrap("launch", _gate(raise_exc=RuntimeError("boom"))))
    monkeypatch.setattr(G, "_gate_h2h_vs_r34a",
                        wrap("h2h", _gate({"passed": False, "rate": 0.5})))
    monkeypatch.setattr(G, "_gate_lineage", wrap("lineage", _gate()))
    monkeypatch.setattr(G, "_gate_starve_subset",
                        wrap("starve", _gate({"passed": False})))
    monkeypatch.setattr(G, "_gate_diff_audit", wrap("diff", _gate()))
    monkeypatch.setattr(G, "_verify_ref_package",
                        lambda d, w: {"what": w, "match": True})
    summary = G.verify_r35_gates(str(fake_pkg))
    assert called == ["launch", "h2h", "lineage", "starve", "diff"]
    assert summary["gates"]["launch"]["executed"] is False
    assert summary["gates"]["launch"]["passed"] is False
    assert summary["gates"]["h2h_vs_r34a"]["passed"] is False
    assert summary["overall"] is False


def test_verify_ref_identity_error_forces_h2h_red(fake_pkg, monkeypatch):
    """r34a 在飞件身份链不符 → h2h 门红（fail-closed）。"""
    monkeypatch.setattr(G, "_gate_launch_fourgate", _gate())
    monkeypatch.setattr(G, "_gate_h2h_vs_r34a", _gate())
    monkeypatch.setattr(G, "_gate_lineage", _gate())
    monkeypatch.setattr(G, "_gate_starve_subset", _gate())
    monkeypatch.setattr(G, "_gate_diff_audit", _gate())

    def broken(pkg_dir, what):
        raise G.GateR35Error("identity mismatch")
    monkeypatch.setattr(G, "_verify_ref_package", broken)
    summary = G.verify_r35_gates(str(fake_pkg))
    assert summary["gates"]["h2h_vs_r34a"]["passed"] is False
    assert "ref_identity_error" in summary["gates"]["h2h_vs_r34a"]
    assert summary["overall"] is False


def test_verify_requires_built_main(tmp_path):
    with pytest.raises(G.GateR35Error):
        G.verify_r35_gates(str(tmp_path))


def test_gate_h2h_passthrough(fake_pkg, monkeypatch):
    """h2h 门复用 gate_h2h_vs_verbatim.run 重定向+装载身份集。"""
    captured = {}

    def fake_run(l1_main, verbatim_main, seeds=None, evidence_path=None,
                 l1_expected_names=None, verbatim_expected_names=None):
        captured["l1"] = l1_main
        captured["opp"] = verbatim_main
        captured["l1_names"] = set(l1_expected_names)
        captured["opp_names"] = set(verbatim_expected_names)
        return {"passed": True, "n": 16, "wins": 10, "losses": 4, "ties": 2,
                "rate": 0.625, "mean_margin": 88.0,
                "evidence_path": evidence_path}

    monkeypatch.setattr(G._h2h_base, "run", fake_run)
    res = G._gate_h2h_vs_r34a(str(fake_pkg / "main.py"), "/tmp/ev.json")
    assert res["passed"] is True and res["rate"] == 0.625
    assert captured["l1_names"] == {"agent"}
    assert captured["opp_names"] == {"_cxd_agent"}
    assert captured["opp"].endswith("orderbook_2965_adopt/a/main.py")
