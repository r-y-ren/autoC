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
