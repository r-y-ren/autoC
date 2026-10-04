# -*- coding: utf-8 -*-
"""R26 测试面：run_r43_iteration（预绑定分叉）+写面隔离（09-28 事故钉）。

写路径纪律（09-28 证据覆写事故教训）：测试一律经 evidence_dir 把台账写路径
钉死在 tmp——模板占位（"aa"*32/"bb"*32）不得落真实候选目录 evidence。
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import tarfile
from pathlib import Path

from orderbook_r43 import run_r43 as r43

KSIM = Path(r43.MODULE_DIR).parent


def _mk_build():
    return {"main_path": "/tmp/x/main.py", "main_sha256": "aa" * 32,
            "tar_sha256": "bb" * 32, "placebo": False}


def test_run_r43_negative_fork(monkeypatch, tmp_path):
    monkeypatch.setattr("orderbook_r43.build_r43.build_r43",
                        lambda *a, **k: _mk_build())
    monkeypatch.setattr(
        "orderbook_r43.judge_r26.judge_r26",
        lambda *a, **k: {"pass": False, "arms": {}, "criteria": {}})
    ev_dir = tmp_path / "evidence"
    out = r43.run_r43_iteration({"out_dir": str(tmp_path),
                                 "evidence_dir": str(ev_dir)})
    assert out["verdict"]["verdict"] == "NEGATIVE"
    assert out["gates"] == {"skipped": True, "overall": False}
    led = json.loads((ev_dir / "archive_ledger.json").read_text(
        encoding="utf-8"))
    assert led["entry"]["verdict"] == "NEGATIVE"


def test_run_r43_positive_fork(monkeypatch, tmp_path):
    monkeypatch.setattr("orderbook_r43.build_r43.build_r43",
                        lambda *a, **k: _mk_build())
    monkeypatch.setattr(
        "orderbook_r43.judge_r26.judge_r26",
        lambda *a, **k: {"pass": True, "arms": {}, "criteria": {}})
    monkeypatch.setattr("orderbook_r43.gates_r43.verify_r43_gates",
                        lambda *a, **k: {"overall": {"passed": True}})
    ev_dir = tmp_path / "evidence"
    out = r43.run_r43_iteration({"out_dir": str(tmp_path),
                                 "evidence_dir": str(ev_dir)})
    assert out["verdict"]["verdict"] == "POSITIVE"
    led = json.loads((ev_dir / "launch_ledger.json").read_text(
        encoding="utf-8"))
    assert led["entry"]["description"].startswith("public derivative")


# --------------------------- 写面隔离（09-28 证据覆写事故 P2 回归钉） ----

def _snapshot_tree(root: Path):
    """树字节快照：relpath→sha256（跳过 __pycache__/.pytest_cache）。"""
    snap = {}
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if "__pycache__" in rel.parts or ".pytest_cache" in rel.parts:
            continue
        snap[str(rel)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return snap


def _mk_pkg(pkg: Path):
    """最小身份链合法包（main.py+_cxs_agent+tar+manifest）。"""
    pkg.mkdir(parents=True, exist_ok=True)
    main_bytes = b"def _cxs_agent(obs):\n    return {}\n"
    (pkg / "main.py").write_bytes(main_bytes)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        info = tarfile.TarInfo("main.py")
        info.size = len(main_bytes)
        tar.addfile(info, io.BytesIO(main_bytes))
    tar_bytes = buf.getvalue()
    (pkg / "submission.tar.gz").write_bytes(tar_bytes)
    (pkg / "build_manifest.json").write_text(json.dumps({
        "candidate": "isolation-test",
        "main_sha256": hashlib.sha256(main_bytes).hexdigest(),
        "main_bytes": len(main_bytes),
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_bytes": len(tar_bytes),
    }), encoding="utf-8")


def test_write_surface_isolation(monkeypatch, tmp_path):
    """写面隔离：跑判决+门禁流程（模板输入）后兄弟候选目录字节不变。

    09-28 事故复现形态：模板占位 sha（"aa"*32/"bb"*32）+空 judgment 经
    run_r43_iteration 与 gate_launch_fourgate_l1.run 跑全流程——模板占位只
    落调用方 evidence_dir/包内 evidence，收档件（archive_ledger/
    launch_ledger/run_summary）拒写，r42/r39/r40 等兄弟目录零字节漂移。
    """
    before = _snapshot_tree(KSIM)
    # ①判决编排（模板输入=事故复现形态）
    monkeypatch.setattr("orderbook_r43.build_r43.build_r43",
                        lambda *a, **k: _mk_build())
    monkeypatch.setattr(
        "orderbook_r43.judge_r26.judge_r26",
        lambda *a, **k: {"pass": True, "arms": {}, "criteria": {}})
    monkeypatch.setattr("orderbook_r43.gates_r43.verify_r43_gates",
                        lambda *a, **k: {"overall": {"passed": True}})
    ev_dir = tmp_path / "ev_r43"
    r43.run_r43_iteration({"out_dir": str(tmp_path / "build"),
                           "evidence_dir": str(ev_dir)})
    # ②门禁流程（gate_launch_fourgate_l1.run：身份链+写点；慢门桩替，
    #   写点/守卫/落点为真）
    l1_dir = KSIM / "orderbook_l1_derivative"
    if str(l1_dir) not in sys.path:
        sys.path.append(str(l1_dir))
    import gate_launch_fourgate_l1 as l1g  # noqa: WPS433

    pkg = tmp_path / "pkg"
    _mk_pkg(pkg)

    class _FakeCheck:
        TMP_DIR = str(tmp_path / "fake_tmp")
        DERIV_MAIN = str(pkg / "main.py")

        def gate2_gate3(self):
            return {"gate2_full_episodes_ok": True,
                    "gate2_step_budget_ms": 1,
                    "gate3_determinism_ok": True, "gate3_hashes": [],
                    "_obs_series_seed101": []}

        def gate1(self, obs_series):
            return {"gate1_official_load_ok": True, "n_obs_replayed": 0,
                    "isolated_vs_local_action_mismatches": [],
                    "evidence": {"last_callable_name": "_cxs_agent",
                                 "non_stdlib_imports": []}}

    monkeypatch.setattr(l1g, "_redirect_check", lambda p: _FakeCheck())
    res = l1g.run(pkg_path=str(pkg))
    assert res["evidence_path"].startswith(str(pkg))
    # ③兄弟目录字节不变（含历史事故目录 r42/r39/r40 面）
    assert _snapshot_tree(KSIM) == before
    # ④模板占位只落调用方 evidence_dir（真实目录 evidence 未被污染）
    led = json.loads((ev_dir / "launch_ledger.json").read_text(
        encoding="utf-8"))
    assert led["entry"]["main_sha256"] == "aa" * 32
    # ⑤收档件只读：已存在台账拒绝覆写（判决机器+门禁机器双写点）
    try:
        r43.write_record(ev_dir / "launch_ledger.json", {"x": 1})
        raise AssertionError("判决机器收档件覆写未被拒绝")
    except RuntimeError as exc:
        assert "收档件只读" in str(exc)
    try:
        l1g.run(pkg_path=str(pkg),
                evidence_path=str(ev_dir / "launch_ledger.json"))
        raise AssertionError("门禁机器收档件覆写未被拒绝")
    except RuntimeError as exc:
        assert "收档件只读" in str(exc)
