"""assemble_and_gate 真实测试（R6 编排：打包 → M1/M2 → 分档裁决）。

builders/runners 注入（tmp 假件）验证编排与分档（GATES_PASS /
BELOW_LINE / PIPELINE_BROKEN）；另含真壳冒烟（真实 build + 假门线，
验证产物落盘与 manifest 链）。
"""

import json

import pytest
from assemble_and_gate.assemble_and_gate import assemble_and_gate
from assemble_and_gate.build_candidate_package import PackageError

_MANIFEST = {
    "package_id": "fake",
    "base": {"sha256": "a" * 64, "bytes": 107008},
    "surgical_face": {"kind": "routes_blob_swap"},
    "library": {"n_routes": 2},
    "selection": {"candidate_id": "route:default#10000",
                  "selection_sha256": "b" * 64},
    "products": {"main_py": {"sha256": "c" * 64, "bytes": 100},
                 "submission_tar_gz": {"sha256": "d" * 64,
                                       "bytes": 90}},
    "paths": {"main": "/tmp/fake-main.py",
              "tar": "/tmp/fake.tar.gz",
              "manifest": "/tmp/fake-manifest.json",
              "output_dir": "/tmp/fakeout"},
}


def _fake_gates(overall="GATES_PASS", failed=()):
    def gates(payload):
        lines = {}
        for key in ("h2h", "giants", "regression", "fourgate", "econ"):
            lines[key] = {"title": key, "runnable": True, "error": None,
                          "result": {"passed": key not in failed},
                          "passed": key not in failed}
        return {
            "m1": {"games": 16, "win_rate_half_ties": 0.6875,
                   "passed": "m1" not in failed},
            "m2": {"lines": lines,
                   "passed": not failed},
            "grading": {"overall": overall},
            "paths": {"report": "/tmp/fake-report.json"},
        }
    return gates


def test_build_payload_receives_overrides(tmp_path, monkeypatch):
    """编排把 library_dir/selection_path 透传给 build，包路径回填门禁。"""
    import assemble_and_gate.assemble_and_gate as ag
    seen = {}

    def fake_build(payload):
        seen.update(payload)
        return _MANIFEST

    monkeypatch.setattr(ag, "build_candidate_package", fake_build)
    monkeypatch.setattr(ag, "run_m1_m2_gates",
                        lambda p: _fake_gates()(p))
    result = assemble_and_gate({
        "output_dir": str(tmp_path),
        "library_dir": "/tmp/lib-x",
        "selection_path": "/tmp/sel-x.json"})
    assert seen["library_dir"] == "/tmp/lib-x"
    assert seen["selection_path"] == "/tmp/sel-x.json"
    assert result["grading"]["overall"] == "GATES_PASS"


def test_build_failure_pipeline_broken(tmp_path):
    def boom(payload):
        raise PackageError("shell base drift (fail-closed)")

    result = assemble_and_gate({
        "output_dir": str(tmp_path),
        "builders": {"build_candidate_package": boom}})
    assert result["package"] is None
    assert result["gates"] is None
    assert result["grading"]["overall"] == "PIPELINE_BROKEN"
    assert any("build_candidate_package" in e
               for e in result["grading"]["errors"])


def test_grading_passthrough_below_line(tmp_path, monkeypatch):
    import assemble_and_gate.assemble_and_gate as ag
    monkeypatch.setattr(ag, "run_m1_m2_gates",
                        lambda p: _fake_gates("BELOW_LINE",
                                              failed=("h2h",))(p))
    result = assemble_and_gate({
        "output_dir": str(tmp_path),
        "builders": {"build_candidate_package": lambda p: _MANIFEST}})
    assert result["grading"]["overall"] == "BELOW_LINE"
    assert result["package"]["products"]["main_py"]["sha256"] == "c" * 64


def test_grading_passthrough_gates_pass(tmp_path, monkeypatch):
    import assemble_and_gate.assemble_and_gate as ag
    monkeypatch.setattr(ag, "run_m1_m2_gates",
                        lambda p: _fake_gates()(p))
    result = assemble_and_gate({
        "output_dir": str(tmp_path),
        "builders": {"build_candidate_package": lambda p: _MANIFEST}})
    assert result["grading"]["overall"] == "GATES_PASS"
    assert result["gates"]["m1"]["win_rate_half_ties"] == 0.6875


def test_gates_runner_exception_pipeline_broken(tmp_path, monkeypatch):
    import assemble_and_gate.assemble_and_gate as ag

    def boom(payload):
        raise RuntimeError("channel gone")

    monkeypatch.setattr(ag, "run_m1_m2_gates", boom)
    result = assemble_and_gate({
        "output_dir": str(tmp_path),
        "builders": {"build_candidate_package": lambda p: _MANIFEST}})
    assert result["grading"]["overall"] == "PIPELINE_BROKEN"
    assert result["package"] is not None      # 包已出，门禁不可执行
    assert any("run_m1_m2_gates" in e
               for e in result["grading"]["errors"])


def test_real_shell_build_with_fake_gates(tmp_path, monkeypatch):
    """真壳冒烟：真实 build_candidate_package（真基底+真库+真最终件）
    + 假门线（避免引擎依赖）——产物三件落盘、manifest 可读、
    gates 拿到的包路径即真实产物。"""
    import assemble_and_gate.assemble_and_gate as ag
    seen = {}

    def fake_gates(payload):
        seen["package_main"] = payload.get("package_main")
        seen["output_dir"] = payload.get("output_dir")
        return _fake_gates()(payload)

    monkeypatch.setattr(ag, "run_m1_m2_gates", fake_gates)
    result = assemble_and_gate({"output_dir": str(tmp_path / "cand")})
    assert result["grading"]["overall"] == "GATES_PASS"
    out = tmp_path / "cand"
    assert (out / "main.py").stat().st_size == \
        result["package"]["products"]["main_py"]["bytes"]
    manifest = json.loads((out / "manifest.json").read_text(
        encoding="utf-8"))
    assert manifest["surgical_face"]["kind"] == "routes_blob_swap"
    assert seen["package_main"] == str(out / "main.py")
    assert seen["output_dir"] == str(out / "gates")
