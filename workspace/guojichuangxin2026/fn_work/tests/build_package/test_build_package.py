"""build_package 单测（skip-build 路径：pyproject 生成+包清单）。"""
from __future__ import annotations


def test_pyproject_generation_skip_build(tmp_path):
    from build_package.build_package import build_package
    out = build_package(str(tmp_path), skip_build=True)
    assert out["post_install_test"] == "skipped"
    pt = open(out["pyproject"], encoding="utf-8").read()
    assert "anhang-yundun" in pt and "ahyd-demo" in pt
    assert "shared" in out["packages"] and "batch_eval" in out["packages"]
    assert (tmp_path / "用户手册.md").exists()
    assert out["hygiene"]["ignore_runs"] and not out["hygiene"]["tracked_artifacts"]  # R24


def test_r24_hygiene_guard_can_fail(monkeypatch, tmp_path):
    """C1 反例：守卫必须可失败——模拟产物在库时 BuildError。"""
    import subprocess as sp
    from build_package.build_package import BuildError, build_package
    real = sp.run

    def fake_run(cmd, **kw):
        if cmd[:2] == ["git", "ls-files"]:
            class R:
                returncode, stdout, stderr = 0, "fn_work/runs_x/1/metrics.jsonl\n", ""
            return R()
        return real(cmd, **kw)
    monkeypatch.setattr(sp, "run", fake_run)
    import pytest
    with pytest.raises(BuildError, match="产物在库"):
        build_package(str(tmp_path), skip_build=True)
