# -*- coding: utf-8 -*-
"""R26 测试面：构建面（编排/audit 白名单/pack 双跑恒等/安慰剂恒等）。"""
from __future__ import annotations

import pytest

from orderbook_r43 import build_r43 as b43

R40 = "/tmp/kagr_root/fn_work/legacy_software/kaggle_simulations/" \
      "orderbook_r40/build/main.py"


def test_placebo_identity():
    """组件全关=纯重编码→与 r40 字节恒等（编解码无损证）。"""
    res = b43.build_r43(R40, out_dir="/tmp/r43_placebo_test",
                        config={"drain": False, "gran": False,
                                "sheep": False})
    assert res["placebo"] is True
    base = open(R40, encoding="utf-8").read()
    assert open(res["main_path"], encoding="utf-8").read() == base
    assert res["manifest"]["main_sha256"] == \
        b43.BASE_CHAIN["r40"]


def test_audit_outside_blob_raises():
    text = open(R40, encoding="utf-8").read()
    with pytest.raises(RuntimeError):
        b43.audit_diff_r43_vs_r40(text.replace("X = 1", "X = 2", 1)
                                  if "X = 1" in text else text + "\n# t",
                                  text, {})


def test_pack_deterministic(tmp_path):
    text = "X = 1\n"
    r1 = b43.pack_r43(text, out_dir=str(tmp_path / "a"), meta={})
    r2 = b43.pack_r43(text, out_dir=str(tmp_path / "b"), meta={})
    assert r1["tar_sha256"] == r2["tar_sha256"]
    m = r1["manifest"]
    assert m["schema"] == b43.SCHEMA and m["complete"] is True
    assert m["base_sha_chain"]["r43"] == m["main_sha256"]


def test_build_r43_real_all_components():
    """真跑全件构建：审计白名单过+变更行>0+manifest 自证。"""
    res = b43.build_r43(R40)
    assert res["placebo"] is False
    assert res["audit"]["whitelist"] == ["tape_blob_surgery"]
    assert res["audit"]["kinds"] == ["drain_align", "granularity",
                                     "sheep_lifecycle"]
    assert res["audit"]["change_rows"] > 0
    assert res["manifest"]["complete"] is True
    assert res["manifest"]["base_sha_chain"]["r40"] == b43.BASE_CHAIN["r40"]
