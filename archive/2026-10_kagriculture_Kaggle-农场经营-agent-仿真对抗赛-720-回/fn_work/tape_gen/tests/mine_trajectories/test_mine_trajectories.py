import json
from pathlib import Path

import pytest

from mine_trajectories.mine_trajectories import mine_trajectories

OWN = "AlphaTeam"


def _action(t, salt):
    return {"farmer": ["PASS"] if (t + salt) % 3 else ["WEST"],
            "hands": [["NORTH"]] if (t + salt) % 5 else [],
            "market": [["HIRE"]] if (t + salt) % 7 else
            [["BUY_SEED", "WHEAT", 1]]}


def _fake_routes():
    return {"routeA": [_action(t, 77_000) for t in range(719)],
            "routeB": [_action(t, 88_000) for t in range(719)]}


def _write_replay(dir_path, episode_id, teams, rewards, salt,
                  clone_seat=None, clone_route=None):
    steps = []
    for t in range(720):
        entry = []
        for seat in range(2):
            if clone_seat == seat and clone_route is not None \
                    and 1 <= t <= 51:
                act = clone_route[t - 1]
            else:
                act = _action(t, salt + seat * 1000)
            entry.append({"action": act, "observation": {}})
        steps.append(entry)
    doc = {"info": {"TeamNames": teams, "EpisodeId": episode_id},
           "rewards": rewards, "steps": steps}
    (dir_path / f"episode-{episode_id}-replay.json").write_text(
        json.dumps(doc), encoding="utf-8")


@pytest.fixture
def payload(tmp_path):
    d = tmp_path / "corpus"
    d.mkdir()
    routes = _fake_routes()
    # 12 局：3 自博弈 / 3 克隆命中 / 6 常规（层状抽样各取前 4 -> 12 局）。
    for i in range(3):
        _write_replay(d, 900 + i, [OWN, OWN], [50.0, 55.0], salt=i)
    for i in range(3):
        _write_replay(d, 910 + i, ["Opp%d" % i, "Clone%d" % i],
                      [10.0, 60.0], salt=10 + i,
                      clone_seat=1, clone_route=routes["routeA"])
    for i in range(6):
        _write_replay(d, 920 + i, [OWN, "Mixed%d" % i],
                      [30.0 + i, 40.0 - i], salt=20 + i)
    routes_path = tmp_path / "routes.json"
    routes_path.write_text(json.dumps(routes), encoding="utf-8")
    return {"corpus_dirs": [d], "clone_reference": str(routes_path),
            "output_dir": tmp_path / "out"}


def test_store_summary_and_audit_written(payload):
    result = mine_trajectories(payload)
    out = Path(result["paths"]["store"])
    assert out.is_file() and out.name == "trajectory_store.jsonl"
    lines = out.read_text(encoding="utf-8").splitlines()
    assert len(lines) == result["store_lines"] == 24  # 12 局 × 双席
    kept = [json.loads(x) for x in lines
            if json.loads(x)["verdict"] == "kept"]
    assert kept and all(len(s["actions"]) == 719 for s in kept)
    # 摘要数字自洽：总席 = 保留 + 剔除分解
    s = result["summary"]
    assert s["total_seats"] == s["kept"] + sum(s["excluded"].values())
    assert s["excluded"] == {"own_team": 12, "clone_v48": 3, "other": 0}
    assert result["corpus_hash"] and result["store_sha256"]
    audit = Path(result["paths"]["audit"]).read_text(encoding="utf-8")
    assert "过滤抽查清单" in audit and "前51步哈希" in audit
    assert audit.count("| 9") >= 10  # ≥10 局逐席可核


def test_deterministic_double_run_byte_identical(payload, tmp_path):
    first = mine_trajectories(payload)
    second = mine_trajectories(dict(payload, output_dir=tmp_path / "out2"))
    assert Path(first["paths"]["store"]).read_bytes() == \
        Path(second["paths"]["store"]).read_bytes()
    assert first["store_sha256"] == second["store_sha256"]
    assert first["corpus_hash"] == second["corpus_hash"]
    # 同目录重跑亦逐字节一致
    mine_trajectories(payload)
    assert Path(first["paths"]["store"]).read_bytes() == \
        Path(second["paths"]["store"]).read_bytes()


def test_fail_closed_propagates_from_loader(tmp_path):
    with pytest.raises(Exception, match="fail-closed"):
        mine_trajectories({"corpus_dirs": [tmp_path / "missing"],
                           "output_dir": tmp_path / "out"})
