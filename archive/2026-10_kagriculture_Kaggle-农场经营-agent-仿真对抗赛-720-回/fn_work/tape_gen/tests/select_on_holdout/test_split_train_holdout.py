"""split_train_holdout 真实测试（R5：对手级不相交分离）。

tmp 伪造轨迹库+回放文件：验证不相交、留出占比 ≥30%、种子可复现、
挖掘源圈禁、席位互补、fail-closed。
"""

import json

import pytest
from select_on_holdout.split_train_holdout import (
    MINING_SOURCE_OPPONENTS,
    split_train_holdout,
)


def _fake_world(tmp_path, n_opponents=20, games_each=1):
    store_dir = tmp_path / "corpus"
    store_dir.mkdir(exist_ok=True)
    replay_dir = tmp_path / "rounds" / "round27"
    replay_dir.mkdir(parents=True, exist_ok=True)
    lines = []
    for i in range(n_opponents):
        team = f"Opponent{i:03d}"
        for g in range(games_each):
            eid = 1000 + i * 10 + g
            episode = f"episode-{eid}-replay.json"
            (replay_dir / episode).write_text("{}", encoding="utf-8")
            lines.append(json.dumps({
                "episode_id": eid, "seat": g % 2, "team": team,
                "opponent": "renyxin", "result": "W",
                "final_margin": 1.0, "actions": [ {"farmer": ["PASS"],
                                                  "hands": [], "market": []} ],
            }))
    # 附加一条挖掘源对手（backbone 来源 Anton Tikhonov）的局
    eid = 9999
    (replay_dir / f"episode-{eid}-replay.json").write_text("{}",
                                                           encoding="utf-8")
    lines.append(json.dumps({
        "episode_id": eid, "seat": 0, "team": "Anton Tikhonov",
        "opponent": "renyxin", "result": "W", "final_margin": 1.0,
        "actions": [{"farmer": ["PASS"], "hands": [], "market": []}],
    }))
    store = store_dir / "trajectory_store.jsonl"
    store.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"store_path": str(store),
            "replay_dirs": [str(replay_dir)]}


def test_split_opponent_disjoint_and_fraction(tmp_path):
    payload = _fake_world(tmp_path, n_opponents=20)
    split = split_train_holdout({**payload, "min_holdout_games": 5,
                                 "output_dir": str(tmp_path / "out")})
    proof = split["proof"]
    train_set = set(split["train"]["opponents"])
    hold_set = set(split["holdout"]["opponents"])
    # 对手级不相交（证明字段+独立复核）
    assert proof["intersection"] == []
    assert not (train_set & hold_set)
    # 留出对手 ≥30%（ceil(0.30×21)=7）
    assert proof["n_opponents_total"] == 21
    assert proof["holdout_opponent_fraction"] >= 0.30
    assert proof["n_holdout_opponents"] == 7
    # 局随对手走：无跨界局
    assert {g["opponent"] for g in split["train"]["games"]} <= train_set
    assert {g["opponent"] for g in split["holdout"]["games"]} <= hold_set
    # 座位互补（seated 注入位）
    assert proof["seat_complement_ok"]
    for game in split["train"]["games"] + split["holdout"]["games"]:
        assert game["me_seat"] == 1 - game["opp_seat"]
    assert split["paths"]["split"].startswith(str(tmp_path))


def test_split_seed_reproducible_and_sensitive(tmp_path):
    payload = _fake_world(tmp_path, n_opponents=20)
    a = split_train_holdout({**payload, "seed": 42, "min_holdout_games": 5})
    b = split_train_holdout({**payload, "seed": 42, "min_holdout_games": 5})
    c = split_train_holdout({**payload, "seed": 43, "min_holdout_games": 5})
    assert a["split_sha256"] == b["split_sha256"]  # 同种子同分离
    assert a["holdout"]["opponents"] == b["holdout"]["opponents"]
    assert c["holdout"]["opponents"] != a["holdout"]["opponents"]


def test_split_mining_sources_forced_to_train(tmp_path):
    payload = _fake_world(tmp_path, n_opponents=20)
    split = split_train_holdout({**payload, "min_holdout_games": 5})
    hold = set(split["holdout"]["opponents"])
    for source in MINING_SOURCE_OPPONENTS:
        if source in {g["opponent"] for g in split["train"]["games"]
                      + split["holdout"]["games"]}:
            assert source not in hold
    # Anton Tikhonov 在伪造库中存在——必入训练
    assert "Anton Tikhonov" in split["train"]["opponents"]
    assert split["proof"]["mining_sources_in_holdout"] == []


def test_split_fail_closed_insufficient_holdout(tmp_path):
    payload = _fake_world(tmp_path, n_opponents=3)  # 3+1 对手，留出 2 局
    with pytest.raises(ValueError, match="fail-closed"):
        split_train_holdout({**payload, "min_holdout_games": 30})


def test_split_fail_closed_missing_replay(tmp_path):
    payload = _fake_world(tmp_path, n_opponents=5)
    # 抽走一个回放文件 → 保留席缺回放即 fail-closed
    victim = (tmp_path / "rounds" / "round27").glob("episode-1000-*.json")
    next(victim).unlink()
    with pytest.raises(ValueError, match="replay file missing"):
        split_train_holdout(payload)
