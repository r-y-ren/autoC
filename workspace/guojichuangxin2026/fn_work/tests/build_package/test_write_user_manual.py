"""write_user_manual 单测。"""
from __future__ import annotations


def test_four_sections(tmp_path):
    from build_package.write_user_manual import write_user_manual
    p = write_user_manual(str(tmp_path / "m" / "用户手册.md"))
    text = open(p, encoding="utf-8").read()
    for sec in ("安装", "一键演示", "控制台操作", "常见故障排查"):
        assert sec in text, sec
    assert "127.0.0.1:8000" in text and "ahyd-demo" in text
