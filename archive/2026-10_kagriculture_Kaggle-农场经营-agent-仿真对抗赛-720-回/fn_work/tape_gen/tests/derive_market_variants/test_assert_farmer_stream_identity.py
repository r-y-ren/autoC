"""assert_farmer_stream_identity 真值测试：farmer 流恒等 + 市场差分账。"""

import pytest

from derive_market_variants.assert_farmer_stream_identity import \
    assert_farmer_stream_identity

N = 30


def _step(t, market=()):
    return {"farmer": ["NORTH"] if t % 2 else ["SOUTH"],
            "hands": [["WEST"]] if t % 3 else [],
            "market": [list(m) for m in market]}


def _route(market_at=None):
    return [_step(t, (["SELL", "WHEAT", 2],) if market_at == t else ())
            for t in range(N)]


def test_identical_streams_pass_with_empty_market_diff():
    route = _route()
    result = assert_farmer_stream_identity({"route": route,
                                            "backbone": _route()})
    assert result["ok"] is True
    assert result["first_divergence"] is None
    assert result["checked_steps"] == N
    assert result["market_changed_steps"] == 0
    assert result["market_diff"] == []
    assert result["farmer_sha256"]["route"] == \
        result["farmer_sha256"]["backbone"]


def test_market_only_difference_passes_and_ledgers():
    """市场单差异不破坏恒等（市场编辑算子只许动 market）。"""
    backbone = _route(market_at=5)
    variant = _route(market_at=5)
    variant[5]["market"] = [["SELL", "WHEAT", 9]]
    variant[8]["market"] = [["HIRE"]]
    result = assert_farmer_stream_identity({"route": variant,
                                            "backbone": backbone})
    assert result["ok"] is True
    assert result["market_changed_steps"] == 2
    by_step = {d["step"]: d for d in result["market_diff"]}
    assert by_step[5]["added"] == [["SELL", "WHEAT", 9]]
    assert by_step[5]["removed"] == [["SELL", "WHEAT", 2]]
    assert by_step[8]["added"] == [["HIRE"]]


def test_farmer_divergence_fails_with_first_divergence():
    backbone = _route()
    variant = _route()
    variant[11]["farmer"] = ["EAST"]
    result = assert_farmer_stream_identity({"route": variant,
                                            "backbone": backbone})
    assert result["ok"] is False
    assert result["first_divergence"] == 11
    assert result["farmer_sha256"]["route"] != \
        result["farmer_sha256"]["backbone"]


def test_hands_divergence_fails_and_strict_raises():
    backbone = _route()
    variant = _route()
    variant[4]["hands"] = [["DIG"], ["DIG"]]
    result = assert_farmer_stream_identity({"route": variant,
                                            "backbone": backbone})
    assert result["ok"] is False
    assert result["first_divergence"] == 4
    with pytest.raises(AssertionError, match="identity violated"):
        assert_farmer_stream_identity({"route": variant,
                                       "backbone": backbone,
                                       "strict": True})


def test_length_mismatch():
    route = _route()
    with pytest.raises(AssertionError, match="length mismatch"):
        assert_farmer_stream_identity({"route": route[:-3],
                                       "backbone": route, "strict": True})
    soft = assert_farmer_stream_identity({"route": route[:-3],
                                          "backbone": route})
    assert soft["ok"] is False
    assert soft["length_mismatch"] == [N - 3, N]


def test_fail_closed_missing_streams():
    with pytest.raises(ValueError, match="fail-closed"):
        assert_farmer_stream_identity({"route": None,
                                       "backbone": _route()})
