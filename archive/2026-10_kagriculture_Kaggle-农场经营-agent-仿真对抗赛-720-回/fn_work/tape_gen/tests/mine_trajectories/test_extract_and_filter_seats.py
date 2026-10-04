import json

import pytest

from mine_trajectories.extract_and_filter_seats import \
    CloneReferenceError, extract_and_filter_seats, load_clone_signatures
from mine_trajectories.load_replay_corpus import load_replay_corpus

OWN = "AlphaTeam"  # 仅测试数据用；被测代码须从语料实测而非硬编码


def _action(t, salt):
    return {"farmer": ["PASS"] if (t + salt) % 3 else ["WEST"],
            "hands": [["NORTH"]] if (t + salt) % 5 else [],
            "market": [["HIRE"]] if (t + salt) % 7 else
            [["BUY_SEED", "WHEAT", 1]]}


def fake_routes():
    return {"routeA": [_action(t, 77_000) for t in range(719)],
            "routeB": [_action(t, 88_000) for t in range(719)]}


def write_replay(dir_path, episode_id, teams, rewards, salt=0,
                 n_steps=720, clone_seat=None, clone_route=None):
    steps = []
    for t in range(n_steps):
        entry = []
        for seat in range(2):
            if clone_seat == seat and clone_route is not None \
                    and 1 <= t <= 51:
                act = clone_route[t - 1]  # route[t-1] == steps[t].action
            else:
                act = _action(t, salt + seat * 1000)
            entry.append({"action": act, "observation": {}})
        steps.append(entry)
    doc = {"info": {"TeamNames": teams, "EpisodeId": episode_id},
           "rewards": rewards, "steps": steps}
    path = dir_path / f"episode-{episode_id}-replay.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


@pytest.fixture
def extracted(tmp_path):
    d = tmp_path / "corpus"
    d.mkdir()
    routes = fake_routes()
    # g1：我方席 vs 对手；g2：对手席 vs 克隆席（1-51 步逐字节 routeA）；
    # g3：自博弈（双我方）；g4：截断流（非我方、非克隆 -> other）。
    write_replay(d, 101, [OWN, "BetaOpp"], [90.0, 40.0], salt=1)
    write_replay(d, 102, ["GammaOpp", "CloneBot"], [10.0, 60.0], salt=2,
                 clone_seat=1, clone_route=routes["routeA"])
    write_replay(d, 103, [OWN, OWN], [50.0, 55.0], salt=3)
    write_replay(d, 104, ["DeltaOpp", "EpsOpp"], [1.0, 2.0], salt=4,
                 n_steps=100)
    manifest = load_replay_corpus([d])
    result = extract_and_filter_seats(manifest, clone_reference=routes)
    return result, routes


def test_own_team_detected_from_corpus_not_hardcoded(extracted):
    result, _ = extracted
    assert result["own_team"] == OWN  # 3 席频次最高（其余各 1）


def test_clone_filter_recall_and_route_label(extracted):
    result, _ = extracted
    clone = [s for s in result["seats"]
             if s["episode_id"] == 102 and s["seat"] == 1][0]
    assert clone["verdict"] == "clone_v48"
    assert clone["clone"] is True
    assert clone["clone_routes"] == ["routeA"]
    assert "actions" not in clone  # 剔除席不留流
    # 召回旁证：routeA 前缀签名确实在参照集内
    sigs = load_clone_signatures(fake_routes())
    assert clone["opening_sig"] in sigs


def test_own_seats_excluded(extracted):
    result, _ = extracted
    verdicts = {(s["episode_id"], s["seat"]): s["verdict"]
                for s in result["seats"]}
    assert verdicts == {
        (101, 0): "own_team", (101, 1): "kept",
        (102, 0): "kept", (102, 1): "clone_v48",
        (103, 0): "own_team", (103, 1): "own_team",
        (104, 0): "other", (104, 1): "other",
    }


def test_kept_seat_metadata_and_stream_shape(extracted):
    result, _ = extracted
    kept = [s for s in result["seats"]
            if s["episode_id"] == 101 and s["seat"] == 1][0]
    assert kept["opponent"] == OWN
    assert kept["result"] == "L" and kept["final_margin"] == -50.0  # 席位视角
    assert kept["category"] == "full"
    assert len(kept["actions"]) == 719
    for step in kept["actions"]:
        assert set(step) == {"farmer", "hands", "market"}  # 单位/市场分列
    assert result["summary"]["total_seats"] == 8
    assert result["summary"]["kept"] == 2
    assert result["summary"]["excluded"] == {
        "own_team": 3, "clone_v48": 1, "other": 2}


def test_deterministic_double_run(extracted, tmp_path):
    result, _ = extracted
    again = extract_and_filter_seats(
        load_replay_corpus([tmp_path / "corpus"]),
        clone_reference=fake_routes())
    canon = lambda r: json.dumps(r, sort_keys=True,
                                 ensure_ascii=False, default=str)
    assert canon(result) == canon(again)


def test_missing_clone_reference_fails_closed(tmp_path):
    d = tmp_path / "corpus"
    d.mkdir()
    write_replay(d, 1, [OWN, "X"], [1.0, 2.0])
    manifest = load_replay_corpus([d])
    with pytest.raises(CloneReferenceError, match="fail-closed"):
        extract_and_filter_seats(manifest,
                                 clone_reference=tmp_path / "nope.json")
