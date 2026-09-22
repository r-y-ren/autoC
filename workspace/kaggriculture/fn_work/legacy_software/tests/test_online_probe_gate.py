"""Next-round online sampling gate: official replays only, not local quickwin."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from kgenv.online_probe import (
    FIRST_SAMPLING_ROUND,
    OnlineProbeError,
    assert_next_round_allowed,
    build_sampling_payload,
    classify_replay,
    next_round_gate,
    validate_sampling,
)


SOFTWARE_ROOT = Path(__file__).resolve().parents[1]


def _replay(teams, rewards, nsteps=720, episode_id=1):
    steps = []
    for t in range(nsteps):
        day = t // 24
        hour = t % 24
        step = []
        for _seat in (0, 1):
            step.append({
                "observation": {
                    "day": day,
                    "hour": hour,
                    "farms": [
                        {"money": 100.0, "tiles": [], "hands": []},
                        {"money": 100.0, "tiles": [], "hands": []},
                    ],
                },
                "action": {"farmer": ["PASS"], "hands": [], "market": []},
            })
        steps.append(step)
    return {
        "info": {"EpisodeId": episode_id, "TeamNames": teams},
        "rewards": rewards,
        "statuses": ["DONE", "DONE"],
        "steps": steps,
    }


def _launch(round_no=21, ref=56006990, status="PENDING"):
    return {
        "schema": "online-probe-ledger/1.0",
        "round": round_no,
        "candidate": {
            "label": "probe",
            "pkg_sha256": "a" * 64,
            "main_sha256": "b" * 64,
            "git_ref": "deadbee",
            "submission_ref": ref,
            "status": status,
        },
        "local_gates": {"quickwin": "+1.23%"},
        "verdict": "SUBMITTED",
    }


def _sampling_from_replays(round_no, ref, replays, public_score=544.2):
    games = [classify_replay(r) for r in replays]
    return build_sampling_payload(
        round_no=round_no,
        submission_ref=ref,
        launch_ledger=_launch(round_no, ref),
        games=games,
        public_score=public_score,
        source={
            "channel": "kaggle-cli",
            "replay_dir": f"references/data/online-replays/round{round_no}",
            "replays_are_local_selfplay": False,
        },
        captured_at_utc="2026-09-04T07:20:00Z",
    )


def test_classify_splits_validation_and_public():
    val = classify_replay(_replay(["renyxin", "renyxin"], [51000.0, 50900.0], episode_id=1))
    pub = classify_replay(_replay(["ashsah", "renyxin"], [113377.0, 67999.0], episode_id=2))
    assert val["kind"] == "validation"
    assert val["won"] is None
    assert pub["kind"] == "public"
    assert pub["won"] is False
    assert pub["opp_name"] == "ashsah"
    assert pub["margin"] == 67999.0 - 113377.0


def test_local_selfplay_cannot_complete_sampling():
    replays = [
        _replay(["opp", "renyxin"], [40000.0, 50000.0], episode_id=i)
        for i in range(3)
    ]
    games = [classify_replay(r) for r in replays]
    with pytest.raises(OnlineProbeError, match="self-play"):
        build_sampling_payload(
            round_no=21,
            submission_ref=56006990,
            launch_ledger=_launch(),
            games=games,
            public_score=544.2,
            source={"replays_are_local_selfplay": True, "channel": "local-engine"},
            captured_at_utc="2026-09-04T07:20:00Z",
        )


def test_quickwin_percent_is_not_a_sampling_verdict():
    replays = [
        _replay(["opp", "renyxin"], [40000.0, 50000.0], episode_id=i)
        for i in range(3)
    ]
    payload = _sampling_from_replays(21, 56006990, replays)
    assert payload["status"] == "COMPLETE"
    assert payload["local_quickwin_not_adjudication"] is True
    assert payload["public_sampling"]["record"] == "3W-0L"
    assert "+1.23%" not in payload["verdict"]
    assert validate_sampling(payload, min_public=3) == []


def test_gate_blocks_pending_latest_round(tmp_path):
    online = tmp_path / "kaggle_simulations"
    online.mkdir()
    dest = tmp_path / "exports" / "online"
    dest.mkdir(parents=True)
    (dest / "round21_ledger.json").write_text(
        json.dumps(_launch()), encoding="utf-8")
    report = next_round_gate(tmp_path, min_public=3)
    assert report["pass"] is False
    assert report["latest_round"] == 21
    assert any("no sampling record" in r for r in report["reasons"])
    with pytest.raises(OnlineProbeError, match="sampling"):
        assert_next_round_allowed(tmp_path)


def test_gate_passes_when_latest_official_sample_is_complete(tmp_path):
    (tmp_path / "kaggle_simulations").mkdir()
    dest = tmp_path / "exports" / "online"
    samp = dest / "sampling"
    dest.mkdir(parents=True)
    samp.mkdir()
    (dest / "round21_ledger.json").write_text(
        json.dumps(_launch()), encoding="utf-8")
    replays = [
        _replay(["oppA", "renyxin"], [40000.0, 50000.0], episode_id=10 + i)
        for i in range(3)
    ]
    payload = _sampling_from_replays(21, 56006990, replays)
    (samp / "round21_sampling.json").write_text(
        json.dumps(payload), encoding="utf-8")
    report = next_round_gate(tmp_path, min_public=3)
    assert report["pass"] is True
    assert report["latest_round"] == 21


def test_gate_blocks_undersized_latest_sample(tmp_path):
    (tmp_path / "kaggle_simulations").mkdir()
    dest = tmp_path / "exports" / "online"
    samp = dest / "sampling"
    dest.mkdir(parents=True)
    samp.mkdir()
    (dest / "round21_ledger.json").write_text(
        json.dumps(_launch()), encoding="utf-8")
    replays = [_replay(["opp", "renyxin"], [1.0, 2.0], episode_id=9)]
    payload = _sampling_from_replays(21, 56006990, replays)
    (samp / "round21_sampling.json").write_text(
        json.dumps(payload), encoding="utf-8")
    report = next_round_gate(tmp_path, min_public=3)
    assert report["pass"] is False
    assert any("public_games=1" in r for r in report["reasons"])


def test_repository_round20_21_sampling_closes_the_live_gate():
    report = next_round_gate(SOFTWARE_ROOT, min_public=3)
    assert FIRST_SAMPLING_ROUND == 20
    r20 = SOFTWARE_ROOT / "exports" / "online" / "sampling" / "round20_sampling.json"
    r21 = SOFTWARE_ROOT / "exports" / "online" / "sampling" / "round21_sampling.json"
    assert r20.exists(), "round-20 official sampling missing"
    assert r21.exists(), "round-21 official sampling missing"
    s20 = json.loads(r20.read_text(encoding="utf-8"))
    s21 = json.loads(r21.read_text(encoding="utf-8"))
    assert s20["status"] == "COMPLETE"
    assert s21["status"] == "COMPLETE"
    assert s20["source"]["replays_are_local_selfplay"] is False
    assert s21["public_sampling"]["public_games"] >= 3
    assert report["pass"] is True, report["reasons"]
