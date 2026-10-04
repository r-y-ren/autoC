import hashlib
import json
from pathlib import Path

import pytest

from mine_trajectories.load_replay_corpus import CorpusError, \
    load_replay_corpus


def _action(t, salt):
    return {"farmer": ["PASS"] if (t + salt) % 3 else ["WEST"],
            "hands": [["NORTH"]] if (t + salt) % 5 else [],
            "market": [["HIRE"]] if (t + salt) % 7 else
            [["BUY_SEED", "WHEAT", 1]]}


def write_replay(dir_path, episode_id, teams, rewards, salt=0,
                 n_steps=720, projection=False):
    steps = [[{"action": _action(t, salt + seat * 1000),
               "observation": {}} for seat in range(2)]
             for t in range(n_steps)]
    doc = {"info": {"TeamNames": teams, "EpisodeId": episode_id},
           "rewards": rewards, "steps": steps}
    if projection:
        doc["_min_projection"] = {"tool": "test"}
    path = dir_path / f"episode-{episode_id}-replay.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


@pytest.fixture
def corpus_dirs(tmp_path):
    a = tmp_path / "roundA"
    b = tmp_path / "roundB"
    a.mkdir()
    b.mkdir()
    write_replay(a, 2002, ["alpha", "beta"], [10.0, 5.0])
    write_replay(a, 2001, ["alpha", "gamma"], [3.0, 9.0], salt=1)
    write_replay(b, 2003, ["delta", "alpha"], [7.0, 7.0], salt=2)
    (a / "episodes.json").write_text("[]", encoding="utf-8")  # 元数据件应被忽略
    return [a, b]


def test_load_manifest_sha_order_and_fields(corpus_dirs):
    manifest = load_replay_corpus(corpus_dirs)
    games = manifest["games"]
    assert [g["episode_id"] for g in games] == [2001, 2002, 2003]
    for game in games:
        raw = json.loads(Path(game["path"]).read_text(encoding="utf-8"))
        assert game["seats"] == 2
        assert game["teams"] == raw["info"]["TeamNames"]
        assert game["rewards"] == raw["rewards"]
        assert game["n_steps"] == 720
        assert game["category"] == "full"
        assert game["sha256"] == hashlib.sha256(
            open(game["path"], "rb").read()).hexdigest()
    assert manifest["counts"] == {"games": 3, "full": 3,
                                  "projection": 0, "shadowed": 0}


def test_missing_required_dir_fails_closed(tmp_path):
    with pytest.raises(CorpusError, match="fail-closed"):
        load_replay_corpus([tmp_path / "nonexistent"])


def test_missing_projection_dir_is_optional(tmp_path, corpus_dirs):
    manifest = load_replay_corpus(
        corpus_dirs + [(tmp_path / "nonexistent", {"required": False})])
    assert manifest["counts"]["games"] == 3
    assert [s["category"] for s in manifest["skipped_dirs"]] == ["projection"]


def test_dedup_by_episode_id_full_shadows_projection(tmp_path):
    full_dir = tmp_path / "full"
    proj_dir = tmp_path / "proj"
    full_dir.mkdir()
    proj_dir.mkdir()
    write_replay(proj_dir, 3001, ["alpha", "beta"], [1.0, 2.0],
                 projection=True)
    write_replay(full_dir, 3001, ["alpha", "beta"], [1.0, 2.0])
    manifest = load_replay_corpus([proj_dir, full_dir])
    assert manifest["counts"]["games"] == 1
    winner = manifest["games"][0]
    assert winner["category"] == "full"
    assert winner["path"].startswith(str(full_dir))
    assert manifest["counts"]["shadowed"] == 1
    assert manifest["shadowed"][0]["category"] == "projection"


def test_corpus_hash_deterministic_and_content_sensitive(tmp_path, corpus_dirs):
    first = load_replay_corpus(corpus_dirs)
    assert first["corpus_hash"] == load_replay_corpus(corpus_dirs)["corpus_hash"]
    # 目录顺序不影响（存活集与件哈希不变）
    assert first["corpus_hash"] == \
        load_replay_corpus(list(reversed(corpus_dirs)))["corpus_hash"]
    # 内容变化必须改变哈希（存活件原地改写；后见重复件不改存活集）
    c = tmp_path / "roundC"
    c.mkdir()
    write_replay(c, 2001, ["alpha", "gamma"], [3.0, 9.0], salt=1)
    assert load_replay_corpus([corpus_dirs[0], c, corpus_dirs[1]]
                               )["corpus_hash"] == first["corpus_hash"]
    write_replay(corpus_dirs[0], 2001, ["alpha", "gamma"], [3.0, 9.0],
                 salt=5)  # 存活件内容异
    assert load_replay_corpus(corpus_dirs)["corpus_hash"] != first["corpus_hash"]
