"""verify_replay_fidelity 真值测试：回放金标准（route[t]==源席流逐字节）。"""

import pytest

from build_route_library.verify_replay_fidelity import replay_step, \
    safe_action, verify_replay_fidelity

N = 60


def _step(t, salt=0):
    return {"farmer": ["NORTH"] if (t + salt) % 2 else ["SOUTH"],
            "hands": [["WEST"]] if t % 3 else [],
            "market": [["SELL", "WHEAT", t % 5 + 1]] if t % 2 else []}


def _stream(n=N, salt=0):
    return [_step(t, salt) for t in range(n)]


def test_exact_backbone_pass():
    source = _stream()
    result = verify_replay_fidelity({
        "routes": {"default": [dict(s) for s in source]},
        "sources": {"default": {"actions": source, "aligned_from": 0}}})
    assert result["all_ok"] is True
    entry = result["fidelity"]["default"]
    assert entry["ok"] and entry["mismatches"] == 0
    assert entry["checked_steps"] == N


def test_splice_semantics_prefix_vs_suffix_sources():
    """分叉路由：t<f 逐字节=骨干源（prefix_actions），t≥f=成员源。"""
    backbone, member = _stream(), _stream(salt=3)
    fork = 20
    route = [dict(s) for s in backbone[:fork]] \
        + [dict(s) for s in member[fork:]]
    result = verify_replay_fidelity({
        "routes": {"fork": route},
        "sources": {"fork": {"actions": member, "aligned_from": fork,
                             "prefix_actions": backbone}}})
    assert result["all_ok"] is True
    # 拼接若把成员市场带进前缀段（t<f）应失配：构造错误前缀
    bad = [dict(s) for s in member[:fork]] + [dict(s) for s in member[fork:]]
    result_bad = verify_replay_fidelity({
        "routes": {"fork": bad},
        "sources": {"fork": {"actions": member, "aligned_from": fork,
                             "prefix_actions": backbone}}})
    assert result_bad["all_ok"] is False
    assert result_bad["fidelity"]["fork"]["first_mismatch"] < fork


def test_detects_corruption_and_reports_first_mismatch():
    source = _stream()
    route = [dict(s) for s in source]
    route[7] = {"farmer": ["PASS"], "hands": [], "market": []}
    route[8] = {"farmer": ["PASS"], "hands": [], "market": []}
    result = verify_replay_fidelity({
        "routes": {"default": route},
        "sources": {"default": {"actions": source, "aligned_from": 0}}})
    assert result["all_ok"] is False
    entry = result["fidelity"]["default"]
    assert entry["first_mismatch"] == 7
    assert entry["mismatches"] == 2


def test_market_byte_difference_is_a_mismatch():
    source = _stream()
    route = [dict(s) for s in source]
    route[1]["market"] = [["SELL", "WHEAT", 99]]
    result = verify_replay_fidelity({
        "routes": {"default": route},
        "sources": {"default": {"actions": source, "aligned_from": 0}}})
    assert result["all_ok"] is False
    assert result["fidelity"]["default"]["first_mismatch"] == 1


def test_missing_source_fails_closed():
    with pytest.raises(ValueError, match="fail-closed"):
        verify_replay_fidelity({"routes": {}, "sources": {}})
    result = verify_replay_fidelity({
        "routes": {"default": _stream()},
        "sources": {"default": None}})
    assert result["all_ok"] is False
    assert "error" in result["fidelity"]["default"]


def test_replay_semantics_matches_v48_units():
    """v21 replay_policy 同义：索引钳位 + 深拷贝；v23 safe_action 缺省补全。"""
    route = _stream(4)
    assert replay_step(route, -9) == route[0]         # 钳位到 0
    assert replay_step(route, 999) == route[-1]       # 钳位到末步
    mutated = replay_step(route, 1)
    mutated["farmer"] = ["EAST"]
    assert route[1]["farmer"] != ["EAST"]             # 深拷贝防串改
    padded = safe_action({"farmer": ["WEST"]})
    assert padded["hands"] == [] and padded["market"] == []
    assert safe_action("junk")["farmer"] == ["PASS"]  # 非 dict -> 全缺省
