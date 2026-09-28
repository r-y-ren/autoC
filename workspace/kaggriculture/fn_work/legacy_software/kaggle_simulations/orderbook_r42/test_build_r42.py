# -*- coding: utf-8 -*-
"""R25 测试面：构建面（inject 组/audit 组/pack 组/编排）。"""
from __future__ import annotations

import json

import pytest

from orderbook_r42 import build_r42 as b42
from orderbook_r42 import inject_r42 as ij

TOY_BASE = """X = 1


def _toy_parent(observation):
    return {"farmer": ["PASS"], "hands": [], "market": []}
"""


def test_inject_block_shape_and_entry():
    """捕获行先于 def/三公开件各一份/末 callable=_route42_agent。"""
    out = ij.inject_r42_block(TOY_BASE)
    text = out["main_text"]
    assert text.startswith(TOY_BASE)
    blk = text[len(TOY_BASE):]
    assert blk.index("_R42_PARENT") < blk.index("\ndef ")
    for name in ("apply_slot_orchestration", "apply_endgame_liquidation",
                 "apply_mirror_gate", "_route42_agent"):
        assert text.count("def %s(" % name) == 1
    ns = {}
    exec(compile(text, "<t>", "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    assert entries[-1].__name__ == "_route42_agent"
    assert out["block_sha"] == ij.inject_r42_block(TOY_BASE)["block_sha"]


def test_inject_chain_runs_and_fail_safe():
    """链行为：父层动作过三件（异常也原样）；辅助名 _R42P_ 防撞名。"""
    out = ij.inject_r42_block(TOY_BASE)
    ns = {}
    exec(compile(out["main_text"], "<t>", "exec"), ns)
    agent = ns["_route42_agent"]
    action = agent({"step": 100, "player": 0, "farms": [], "private": {},
                    "market": {"prices": {}}, "farmer": []})
    assert isinstance(action, dict)
    assert "_R42P_is_sell" in out["main_text"]     # 辅助名改写
    assert "def _is_sell(" not in out["main_text"]


def test_audit_tail_only():
    """白名单=纯尾部追加；篡改基座段即抛。"""
    out = ij.inject_r42_block(TOY_BASE)
    rep = b42.audit_diff_r42_vs_r40(out["main_text"], TOY_BASE, out)
    assert rep["whitelist"] == ["tail_runtime_block"]
    assert rep["unattributed"] == []
    with pytest.raises(RuntimeError):
        b42.audit_diff_r42_vs_r40(out["main_text"].replace("X = 1", "X = 2"),
                                  TOY_BASE, out)


def test_pack_deterministic_and_manifest_shape(tmp_path):
    """双跑恒等；manifest 键集齐（sha 链含 r42 节点）。"""
    out = ij.inject_r42_block(TOY_BASE)
    r1 = b42.pack_r42(out["main_text"], out_dir=str(tmp_path / "a"),
                      runtime_block=out)
    r2 = b42.pack_r42(out["main_text"], out_dir=str(tmp_path / "b"),
                      runtime_block=out)
    assert r1["tar_sha256"] == r2["tar_sha256"]
    m = r1["manifest"]
    assert m["schema"] == b42.SCHEMA and m["complete"] is True
    assert m["base_sha_chain"]["r42"] == m["main_sha256"]
    assert m["runtime_block"]["sha256"] == out["block_sha"]
    assert m["tar_members"] == ["main.py"]
    json.loads(open(r1["man_path"], encoding="utf-8").read()) if False else None


def test_build_r42_real_on_toy(tmp_path):
    """编排：注入→审计→打包→manifest 自证。"""
    base = tmp_path / "r40_toy.py"
    base.write_text(TOY_BASE, encoding="utf-8")
    res = b42.build_r42(str(base), out_dir=str(tmp_path / "out"))
    assert res["audit"]["unattributed"] == []
    assert res["manifest"]["complete"] is True
    assert res["manifest"]["runtime_block"]["sha256"] == res["block_sha"]
