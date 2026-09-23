"""build_route_library 真值测试：端到端编排 + 产物确定性 + v48 载入兼容。"""

import json
import sys
from pathlib import Path

import pytest

from build_route_library.build_route_library import LibraryError, \
    build_route_library

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_V48_MODULES = (_CAMPAIGN_ROOT / "fn_docs" / "hybrid" / "results"
                / "2026-09-23-v48-coordination-deepread" / "modules")

N = 120
EVENT_STEP = 40


def _step(t, salt):
    return {"farmer": ["NORTH"] if (t + salt) % 2 else ["SOUTH"],
            "hands": [["WEST"]] if (t + salt) % 3 else [],
            "market": [["HIRE"]] if (t + salt) % 5 else
            [["SELL", "WHEAT", t % 7 + 1]]}


def _walk(salt=0, fork_at=None, salt_after=77):
    return [_step(t, salt_after if (fork_at is not None and t >= fork_at)
                  else salt) for t in range(N)]


def _kept(eid, seat, actions, margin):
    return {"verdict": "kept", "episode_id": eid, "seat": seat,
            "team": "Opp", "opponent": "Other", "result":
            "W" if margin > 0 else "L", "final_margin": margin,
            "actions": actions}


def write_replay(dir_path, episode_id, unlock_plan):
    steps = []
    shops, seen = [], set()
    for t in range(N + 1):
        for e, shop in unlock_plan:
            if t == e and shop not in seen:
                seen.add(shop)
                shops = shops + [shop]
        entry = {"action": {}, "observation": {
            "step": t, "town": {"unlocked_shops": list(shops)}}}
        steps.append([entry, dict(entry)])
    path = dir_path / f"episode-{episode_id}-replay.json"
    path.write_text(json.dumps({"steps": steps}), encoding="utf-8")


@pytest.fixture
def corpus(tmp_path):
    store = tmp_path / "trajectory_store.jsonl"
    seats = [
        _kept(2, 0, _walk(salt=0), margin=9.0),                    # 骨干候选（家族）
        _kept(3, 1, _walk(salt=0), margin=0.5),                    # 全同走位
        _kept(4, 0, _walk(fork_at=EVENT_STEP + 1, salt_after=9), margin=8.0),
        _kept(5, 1, _walk(fork_at=EVENT_STEP + 1, salt_after=9), margin=6.0),
        _kept(6, 0, _walk(salt=5), margin=-1.0),                   # 外人
    ]
    store.write_text("\n".join(json.dumps(s) for s in seats) + "\n",
                     encoding="utf-8")
    replays = tmp_path / "replays"
    replays.mkdir()
    write_replay(replays, 4, [(EVENT_STEP, "YARN_STORE")])
    write_replay(replays, 5, [(EVENT_STEP, "FARMERS_MARKET")])
    return {"store": store, "replays": replays}


def test_end_to_end_products_and_manifest(tmp_path, corpus):
    out = tmp_path / "lib"
    manifest = build_route_library({
        "store_path": corpus["store"], "output_dir": out,
        "replay_dirs": [corpus["replays"]]})
    routes = json.loads((out / "routes.json").read_text(encoding="utf-8"))
    assert set(routes) == {"default", f"fork_s{EVENT_STEP + 1}_e{EVENT_STEP}"}
    assert all(len(steps) == N for steps in routes.values())
    # 骨干=家族内边际最高者（走位并列 -> margin 消解）
    assert manifest["backbone_election"]["backbone"] == "2:0"
    assert manifest["fidelity"]["all_ok"] is True
    assert manifest["fork_events"]["shared_prefix"] == EVENT_STEP + 1
    assert manifest["fork_events"]["trigger_step"] == EVENT_STEP
    # manifest 文件与 routes 文件齐备且可复析
    on_disk = json.loads((out / "library_manifest.json").read_text(
        encoding="utf-8"))
    assert on_disk["routes_sha256"] == manifest["routes_sha256"]


def test_double_run_byte_identical(tmp_path, corpus):
    out1, out2 = tmp_path / "run1", tmp_path / "run2"
    m1 = build_route_library({"store_path": corpus["store"],
                              "output_dir": out1,
                              "replay_dirs": [corpus["replays"]]})
    m2 = build_route_library({"store_path": corpus["store"],
                              "output_dir": out2,
                              "replay_dirs": [corpus["replays"]]})
    assert m1["routes_sha256"] == m2["routes_sha256"]
    for name in ("routes.json", "library_manifest.json"):
        assert (out1 / name).read_bytes() == (out2 / name).read_bytes()


def test_fail_closed_too_few_kept(tmp_path):
    store = tmp_path / "tiny.jsonl"
    store.write_text(json.dumps(_kept(1, 0, _walk(), 1.0)) + "\n",
                     encoding="utf-8")
    with pytest.raises(LibraryError, match="fail-closed"):
        build_route_library({"store_path": store,
                             "output_dir": tmp_path / "lib",
                             "replay_dirs": [tmp_path]})


def test_fail_closed_missing_store(tmp_path):
    with pytest.raises(LibraryError, match="fail-closed"):
        build_route_library({"store_path": tmp_path / "nope.jsonl",
                             "output_dir": tmp_path / "lib"})


def test_v48_load_path_compatibility(tmp_path, corpus):
    """真值 v48 解码件（只读）载入我们产出的 routes.json：前缀不变量与
    回放器逐字回放（RouteLibrary + replay_policy 语义）。"""
    if not _V48_MODULES.is_dir():
        pytest.skip("v48 reference modules unavailable")
    sys.path.insert(0, str(_V48_MODULES))
    try:
        from v23.policy_library import RouteLibrary, shared_prefix_length
        from scripts.v21_route_memory_search import replay_policy
    finally:
        sys.path.remove(str(_V48_MODULES))

    out = tmp_path / "lib"
    manifest = build_route_library({"store_path": corpus["store"],
                                    "output_dir": out,
                                    "replay_dirs": [corpus["replays"]]})
    routes = json.loads((out / "routes.json").read_text(encoding="utf-8"))
    # v48 不变量：共享前缀 ≥ 触发步（RouteLibrary.__post_init__ 强制）
    trigger = manifest["fork_events"]["trigger_step"]
    assert shared_prefix_length(routes) >= trigger
    library = RouteLibrary(routes=routes, default="default",
                           trigger_step=trigger)
    agent = library.policy(lambda obs, cfg: "default")
    for t in (0, 1, trigger, trigger + 1, N - 1):
        obs = {"player": 0, "step": t}
        assert agent(obs) == routes["default"][min(t, N - 1)]
    # v21 replay_policy 逐字回放：route[t] == actions[t]
    policy = replay_policy(routes["default"])
    assert policy({"step": 0}) == routes["default"][0]
    assert policy({"step": N - 1}) == routes["default"][N - 1]
