"""fork_routes_on_events 真值测试：商店事件对齐 + 嵌缀树构造（tmp 假轨迹）。"""

import json

import pytest

from build_route_library.fork_routes_on_events import fork_routes_on_events, \
    resolve_replay_path, shop_events

N = 120
EVENT_STEP = 40          # 假语料首店事件步（观测面 unlocked_shops 首现）


def _step(t, salt, market=None):
    step = {"farmer": ["NORTH"] if (t + salt) % 2 else ["SOUTH"],
            "hands": [["WEST"]] if (t + salt) % 3 else [],
            "market": [["HIRE"]] if (t + salt) % 5 else []}
    if market is not None:
        step["market"] = market
    return step


def _walk(salt=0, fork_at=None, salt_after=77, market_from=None, n=N):
    steps = []
    for t in range(n):
        salt_t = salt_after if (fork_at is not None and t >= fork_at) \
            else salt
        market = None
        if market_from is not None and t >= market_from:
            market = [["SELL", "WHEAT", 3]]
        steps.append(_step(t, salt_t, market))
    return steps


def _rec(eid, seat, actions, margin=0.0):
    return {"episode_id": eid, "seat": seat, "team": "T",
            "final_margin": margin, "actions": actions}


def write_replay(dir_path, episode_id, unlock_plan, n_steps=N + 1):
    """unlock_plan: [(事件步, 店名)]，写 observation.town.unlocked_shops。"""
    steps = []
    shops = []
    seen = set()
    for t in range(n_steps):
        for e, shop in unlock_plan:
            if t == e and shop not in seen:
                seen.add(shop)
                shops = shops + [shop]
        entry = {"action": {},
                 "observation": {"step": t,
                                 "town": {"unlocked_shops": list(shops)}}}
        steps.append([entry, dict(entry)])
    path = dir_path / f"episode-{episode_id}-replay.json"
    path.write_text(json.dumps({"steps": steps}), encoding="utf-8")
    return path


@pytest.fixture
def replay_dir(tmp_path):
    d = tmp_path / "replays"
    d.mkdir()
    return d


def test_aligned_fork_builds_spliced_route(tmp_path, replay_dir):
    """分叉步=事件步+1（本语料实测 gap=1）-> 嵌缀路由 + 前缀不变量。"""
    backbone = _rec(1, 0, _walk(salt=0), margin=1.0)
    m1 = _rec(2, 1, _walk(fork_at=EVENT_STEP + 1, salt_after=9,
                          market_from=10), margin=50.0)
    m2 = _rec(3, 0, _walk(fork_at=EVENT_STEP + 1, salt_after=9), margin=2.0)
    write_replay(replay_dir, 2, [(EVENT_STEP, "YARN_STORE")])
    write_replay(replay_dir, 3, [(EVENT_STEP, "FARMERS_MARKET")])

    result = fork_routes_on_events({
        "backbone": backbone, "trajectories": [backbone, m1, m2],
        "replay_dirs": [replay_dir]})
    name = f"fork_s{EVENT_STEP + 1}_e{EVENT_STEP}"
    assert name in result["routes"]
    assert result["shared_prefix"] == EVENT_STEP + 1
    assert result["trigger_step"] == EVENT_STEP
    assert result["prefix_invariant_ok"] is True
    # 嵌缀拼接：[0,f) 逐字节=骨干全步（市场不同也强制回填骨干市场）
    route = result["routes"][name]
    assert route[:EVENT_STEP + 1] == backbone["actions"][:EVENT_STEP + 1]
    assert m1["actions"][10]["market"] != route[10]["market"]  # 成员源市场被替换
    assert route[EVENT_STEP + 1:] == m1["actions"][EVENT_STEP + 1:]
    # 代表=组内边际最高者
    row = next(r for r in result["fork_table"]
               if r.get("route_name") == name)
    assert row["route_source"] == "2:1"
    assert row["gap"] == 1


def test_unaligned_fork_excluded(tmp_path, replay_dir):
    """分叉步距事件 35 步（> 窗 16）-> excluded_unaligned，不出路由。"""
    backbone = _rec(1, 0, _walk(salt=0))
    m1 = _rec(2, 0, _walk(fork_at=EVENT_STEP + 35, salt_after=9), margin=9.0)
    m2 = _rec(3, 1, _walk(fork_at=EVENT_STEP + 35, salt_after=9), margin=8.0)
    write_replay(replay_dir, 2, [(EVENT_STEP, "BAKERY")])
    write_replay(replay_dir, 3, [(EVENT_STEP, "BAKERY")])
    result = fork_routes_on_events({
        "backbone": backbone, "trajectories": [backbone, m1, m2],
        "replay_dirs": [replay_dir]})
    assert list(result["routes"]) == ["default"]
    row = result["fork_table"][0]
    assert row["status"] == "excluded_unaligned"


def test_fork_before_event_never_aligns(tmp_path, replay_dir):
    """fork 早于事件=因果不可能（f<e 一律不对齐）。"""
    backbone = _rec(1, 0, _walk(salt=0))
    m1 = _rec(2, 0, _walk(fork_at=EVENT_STEP - 5, salt_after=9), margin=9.0)
    m2 = _rec(3, 1, _walk(fork_at=EVENT_STEP - 5, salt_after=9), margin=8.0)
    write_replay(replay_dir, 2, [(EVENT_STEP, "BAKERY")])
    write_replay(replay_dir, 3, [(EVENT_STEP, "BAKERY")])
    result = fork_routes_on_events({
        "backbone": backbone, "trajectories": [backbone, m1, m2],
        "replay_dirs": [replay_dir]})
    assert result["fork_table"][0]["status"] == "excluded_unaligned"


def test_aligned_singleton_excluded(tmp_path, replay_dir):
    """对齐但成员 1 < min_group_size=2 -> excluded_singleton。"""
    backbone = _rec(1, 0, _walk(salt=0))
    lone = _rec(2, 0, _walk(fork_at=EVENT_STEP + 2, salt_after=9), margin=9.0)
    write_replay(replay_dir, 2, [(EVENT_STEP, "PIZZA_SHOP")])
    result = fork_routes_on_events({
        "backbone": backbone, "trajectories": [backbone, lone],
        "replay_dirs": [replay_dir]})
    row = result["fork_table"][0]
    assert row["status"] == "excluded_singleton"
    assert row["event_aligned"] is True
    assert list(result["routes"]) == ["default"]


def test_walk_identical_members_are_corroboration_not_forks(tmp_path,
                                                            replay_dir):
    backbone = _rec(1, 0, _walk(salt=0), margin=1.0)
    twin = _rec(2, 1, _walk(salt=0), margin=2.0)   # 全同走位（市场可异）
    twin["actions"] = [dict(s, market=[["HIRE"]]) for s in twin["actions"]]
    result = fork_routes_on_events({
        "backbone": backbone, "trajectories": [backbone, twin],
        "replay_dirs": [replay_dir]})
    assert result["walk_identical_count"] == 1
    assert list(result["routes"]) == ["default"]
    assert result["fork_table"] == []


def test_gap_zero_aligns_v48_yarn_third_anchor(tmp_path, replay_dir):
    """gap=0（fork==事件步）对齐——v48 yarn_third 216↔216 实证锚。"""
    backbone = _rec(1, 0, _walk(salt=0))
    m1 = _rec(2, 0, _walk(fork_at=EVENT_STEP, salt_after=9), margin=4.0)
    m2 = _rec(3, 1, _walk(fork_at=EVENT_STEP, salt_after=9), margin=3.0)
    write_replay(replay_dir, 2, [(EVENT_STEP, "YARN_STORE")])
    write_replay(replay_dir, 3, [(EVENT_STEP, "YARN_STORE")])
    result = fork_routes_on_events({
        "backbone": backbone, "trajectories": [backbone, m1, m2],
        "replay_dirs": [replay_dir]})
    name = f"fork_s{EVENT_STEP}_e{EVENT_STEP}"
    assert name in result["routes"]
    assert result["routes"][name][EVENT_STEP] == m1["actions"][EVENT_STEP]


def test_shop_events_extraction_and_resolution(tmp_path, replay_dir):
    path = write_replay(replay_dir, 77, [(10, "A_SHOP"), (30, "B_SHOP")])
    assert resolve_replay_path(77, [replay_dir]) == path
    assert resolve_replay_path(999, [replay_dir]) is None
    events = shop_events(path, 1)
    assert [(e, s) for e, s, _ in events] == [(10, "A_SHOP"), (30, "B_SHOP")]
    assert events[1][2] == ["A_SHOP", "B_SHOP"]
    assert shop_events(replay_dir / "missing.json", 0) == []


def test_fail_closed_missing_inputs():
    with pytest.raises(ValueError, match="fail-closed"):
        fork_routes_on_events({"backbone": None,
                               "trajectories": [_rec(1, 0, _walk())]})
    with pytest.raises(ValueError, match="fail-closed"):
        fork_routes_on_events({"backbone": _rec(1, 0, _walk()),
                               "trajectories": []})
