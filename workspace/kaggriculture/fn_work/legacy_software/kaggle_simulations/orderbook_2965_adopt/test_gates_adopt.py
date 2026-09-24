# -*- coding: utf-8 -*-
"""R16 单测：gates_adopt（fail-closed 全跑语义/门函数接线参数/在飞件身份链/
门序完整性）。门禁真跑由 CLI 编排（测试不跑引擎，monkeypatch 替身）。"""
import json
import os

import pytest

from orderbook_2965_adopt import gates_adopt as G


def _fake_result(passed=True, **kw):
    base = {"passed": passed}
    base.update(kw)
    return base


def test_run_gate_exception_fail_closed():
    entry, result = G._run_gate("boom", lambda: 1 / 0)
    assert entry["passed"] is False and entry["executed"] is False
    assert "ZeroDivisionError" in entry["error"] and result is None


def test_run_gate_pass_and_fail():
    ok, _ = G._run_gate("ok", lambda: _fake_result(True))
    assert ok["passed"] is True and ok["executed"] is True
    red, _ = G._run_gate("red", lambda: _fake_result(False))
    assert red["passed"] is False and red["executed"] is True


def _tmp_pkg(tmp_path, main_text="def _cxd_agent(o):\n    return {}\n"):
    pkg = tmp_path / "pkg"
    pkg.mkdir(parents=True)
    (pkg / "main.py").write_text(main_text, encoding="utf-8")
    return str(pkg)


def test_verify_ref_package_ok_and_tamper(tmp_path):
    import hashlib
    pkg = tmp_path / "ref"
    pkg.mkdir()
    main = b"def _cxs_agent(o):\n    return {}\n"
    (pkg / "main.py").write_bytes(main)
    import io
    import gzip
    import tarfile
    buf = io.BytesIO()
    gz = gzip.GzipFile(filename="", mode="wb", fileobj=buf, mtime=0)
    with tarfile.open(fileobj=gz, mode="w") as tar:
        info = tarfile.TarInfo("main.py")
        info.size = len(main)
        info.mode = 0o644
        info.mtime = 0
        info.uid = 0
        info.gid = 0
        tar.addfile(info, io.BytesIO(main))
    gz.close()
    (pkg / "submission.tar.gz").write_bytes(buf.getvalue())
    manifest = {"main_sha256": hashlib.sha256(main).hexdigest(),
                "main_bytes": len(main),
                "tar_sha256": hashlib.sha256(buf.getvalue()).hexdigest(),
                "tar_bytes": len(buf.getvalue())}
    (pkg / "build_manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8")
    assert G._verify_ref_package(str(pkg), "ref")["match"] is True
    # 篡改盘上 main → 身份链红
    (pkg / "main.py").write_bytes(main + b"# tampered\n")
    with pytest.raises(G.GateAdoptError):
        G._verify_ref_package(str(pkg), "ref")


def test_verify_one_fail_closed_all_gates(tmp_path, monkeypatch):
    calls = []

    def fake_launch(pkg_dir, evidence_dir):
        calls.append("launch")
        return {"passed": True, "gates": {"load": True}}

    def fake_h2h(r34_main, evidence_path):
        calls.append("h2h")
        return {"passed": True, "n": 16, "wins": 10, "losses": 6, "ties": 0,
                "rate": 0.625, "threshold": 0.55, "evidence_path": "x"}

    def fake_lineage(r34_main, evidence_path):
        calls.append("lineage")
        return {"passed": True, "per_opponent": {}, "evidence_path": "x"}

    def fake_starve(r34_main, ref_main, evidence_path):
        calls.append("starve")
        return {"passed": True, "starve_free": True, "n_games": 26,
                "n_errors": 0, "n_starve_red_games": 0, "subset": True}

    def fake_audit(r34a_main, r34b_main, evidence_path):
        calls.append("audit")
        return {"passed": False, "attribution": {}}

    monkeypatch.setattr(G, "_gate_launch_fourgate", fake_launch)
    monkeypatch.setattr(G, "_gate_h2h_vs_r33", fake_h2h)
    monkeypatch.setattr(G, "_gate_lineage", fake_lineage)
    monkeypatch.setattr(G, "_gate_starve_subset", fake_starve)
    monkeypatch.setattr(G, "_gate_diff_audit", fake_audit)
    monkeypatch.setattr(G, "_verify_ref_package",
                        lambda pkg_dir, what: {"match": True})
    monkeypatch.setattr(G, "_sha256_file", lambda p: "sha")
    pkg = _tmp_pkg(tmp_path)
    a_main = _tmp_pkg(tmp_path / "a2")
    b_main = _tmp_pkg(tmp_path / "b2")
    summary = G._verify_one("a", pkg, a_main, b_main)
    # 全跑不短路：五门都执行了（含红的 diff_audit）
    assert set(calls) == {"launch", "h2h", "lineage", "starve", "audit"}
    assert summary["gates"]["diff_audit"]["passed"] is False
    assert summary["overall"] is False
    # 台账落盘
    ev = pkg_evidence = os.path.join(pkg, "evidence")
    assert os.path.isfile(os.path.join(ev, "verify_summary_r34a.json"))


def test_verify_one_exception_gate_red(tmp_path, monkeypatch):
    monkeypatch.setattr(G, "_gate_launch_fourgate",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("nope")))
    monkeypatch.setattr(G, "_gate_h2h_vs_r33",
                        lambda *a, **k: _fake_result(True))
    monkeypatch.setattr(G, "_gate_lineage",
                        lambda *a, **k: _fake_result(True))
    monkeypatch.setattr(G, "_gate_starve_subset",
                        lambda *a, **k: _fake_result(True))
    monkeypatch.setattr(G, "_gate_diff_audit",
                        lambda *a, **k: _fake_result(True))
    monkeypatch.setattr(G, "_verify_ref_package",
                        lambda pkg_dir, what: {"match": True})
    monkeypatch.setattr(G, "_sha256_file", lambda p: "sha")
    pkg = _tmp_pkg(tmp_path)
    summary = G._verify_one("b", pkg, pkg, pkg)
    assert summary["gates"]["launch"]["executed"] is False
    assert summary["gates"]["launch"]["passed"] is False
    assert summary["overall"] is False
    assert os.path.isfile(os.path.join(pkg, "evidence",
                                       "verify_summary_r34b.json"))


def test_h2h_gate_wires_expected_callables(tmp_path, monkeypatch):
    captured = {}

    def fake_run(l1_main, verbatim_main, seeds=None, evidence_path=None,
                 l1_expected_names=None, verbatim_expected_names=None):
        captured.update(cand=l1_main, opp=verbatim_main,
                        cand_names=set(l1_expected_names),
                        opp_names=set(verbatim_expected_names))
        return {"n": 16, "wins": 12, "losses": 4, "ties": 0, "rate": 0.75,
                "passed": True, "evidence_path": evidence_path}

    monkeypatch.setattr(G._h2h_base, "run", fake_run)
    res = G._gate_h2h_vs_r33("/x/main.py", str(tmp_path / "ev.json"))
    assert captured["cand_names"] == {"_cxd_agent"}
    assert captured["opp_names"] == {"_cxs_agent"}
    assert captured["opp"].endswith("variant_tuned/main.py")
    assert res["passed"] is True and res["rate"] == 0.75


def test_lineage_gate_opponents_and_redirect(tmp_path, monkeypatch):
    captured = {}

    def fake_run(l1_main, opponents, per_opponent_n=8):
        captured.update(main=l1_main, opponents=dict(opponents), n=per_opponent_n)
        # 落点改指生效性：evidence 落点应为 fake 写入的 EVIDENCE_PATH
        os.makedirs(os.path.dirname(G._lin.EVIDENCE_PATH), exist_ok=True)
        with open(G._lin.EVIDENCE_PATH, "w", encoding="utf-8") as fh:
            fh.write("{}")
        return {"per_opponent": {"v48-pure": {"losses": 0}},
                "passed": True, "evidence_path": G._lin.EVIDENCE_PATH}

    monkeypatch.setattr(G._lin, "run", fake_run)
    ev = str(tmp_path / "sub" / "lineage_evidence.json")
    res = G._gate_lineage("/x/main.py", ev)
    assert set(captured["opponents"]) == {"v48-pure", "v4b"}
    assert captured["n"] == 8
    assert res["evidence_path"] == ev and os.path.isfile(ev)
    # 还原：改指退出后 L1 模块落点回原值
    assert G._lin.EVIDENCE_PATH != ev


def test_gate_order_complete():
    assert G._GATE_ORDER == ("launch", "h2h_vs_r33", "lineage",
                             "starve_subset", "diff_audit")


def test_verify_2965_gates_requires_built(tmp_path):
    with pytest.raises(G.GateAdoptError):
        G.verify_2965_gates(str(tmp_path))
