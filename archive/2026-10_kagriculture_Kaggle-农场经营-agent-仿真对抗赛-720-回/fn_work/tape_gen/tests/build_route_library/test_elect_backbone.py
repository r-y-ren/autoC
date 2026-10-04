"""elect_backbone 真值测试：骨干选举（走位共享/市场不计/并列消解/确定性）。"""

import pytest

from build_route_library.elect_backbone import elect_backbone, \
    movement_stream, shared_prefix_len

N = 120


def _step(t, salt, salt_h=0):
    return {"farmer": ["NORTH"] if (t + salt) % 2 else ["SOUTH"],
            "hands": [["WEST"]] if (t + salt + salt_h) % 3 else [],
            "market": [["HIRE"]] if (t + salt) % 5 else
            [["SELL", "WHEAT", t % 7 + 1]]}


def _walk(n=N, salt=0, fork_at=None, salt_after=77):
    steps = []
    for t in range(n):
        salt_t = salt
        if fork_at is not None and t >= fork_at:
            salt_t = salt_after
        steps.append(_step(t, salt_t))
    return steps


def _rec(eid, seat, actions, margin=0.0, team="T"):
    return {"episode_id": eid, "seat": seat, "team": team,
            "final_margin": margin, "actions": actions}


def test_market_differences_do_not_break_sharing():
    """同走位不同市场单：仍算共享（v48 机制——市场单不构成共享约束）。"""
    walk = _walk()
    fam = [
        _rec(1, 0, [dict(s, market=[["BUY_SEED", "MELON", t]])
                    for t, s in enumerate(walk)], margin=-5.0),
        _rec(2, 1, walk, margin=10.0),
        _rec(3, 0, walk, margin=3.0),
    ]
    outsider = _rec(4, 0, _walk(salt=5), margin=99.0)
    result = elect_backbone({"trajectories": fam + [outsider]})
    # 家族内胜局边际最大者当选（走位并列 -> margin 消解）
    assert result["backbone_key"] == "2:1"
    assert result["supporters"] == 2
    assert result["backbone"]["final_margin"] == 10.0


def test_bigger_family_wins_over_high_margin_singletons():
    """supporters@51 优先于边际：大家族成员击败高分孤狼。"""
    big = [_rec(100 + i, i % 2, _walk(salt=1), margin=-10.0 - i)
           for i in range(4)]
    lone_high = [_rec(5, 0, _walk(salt=9), margin=5000.0)]
    result = elect_backbone({"trajectories": big + lone_high})
    assert result["backbone_key"] == "100:0"
    assert result["supporters"] == 3


def test_shared_prefix_threshold_excludes_short_openings():
    """共享 < min_shared_prefix 的开局不计 supporters（51 步窗口先例）。"""
    fam = [_rec(1, 0, _walk(salt=0), margin=1.0),
           _rec(2, 1, _walk(salt=0), margin=1.0)]
    short = [_rec(3, 0, _walk(salt=0, fork_at=10, salt_after=3))
             for _ in range(3)]
    result = elect_backbone({"trajectories": fam + short,
                             "min_shared_prefix": 51})
    assert result["supporters"] == 1
    assert result["backbone_key"] in {"1:0", "2:1"}


def test_determinism_same_input_same_output():
    trajs = [_rec(1, 0, _walk(salt=0), margin=7.0),
             _rec(2, 1, _walk(salt=0), margin=7.0),
             _rec(3, 0, _walk(salt=4), margin=1.0)]
    r1 = elect_backbone({"trajectories": trajs})
    r2 = elect_backbone({"trajectories": trajs})
    assert r1 == r2
    # 边际并列 -> (episode_id, seat) 升序消解
    assert r1["backbone_key"] == "1:0"


def test_streams_and_prefix_helpers():
    a, b = movement_stream(_walk()), movement_stream(_walk())
    c = movement_stream(_walk(fork_at=7, salt_after=43))
    assert shared_prefix_len(a, b) == N
    assert shared_prefix_len(a, c) == 7


def test_fail_closed_empty_trajectories():
    with pytest.raises(ValueError, match="fail-closed"):
        elect_backbone({"trajectories": [{"episode_id": 1, "seat": 0}]})
