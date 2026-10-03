"""replay_check 单测。"""
from __future__ import annotations

import json
from pathlib import Path


def _write_frames(d: Path, hz: float, n=60):
    (d / "frames").mkdir(parents=True, exist_ok=True)
    with open(d / "frames" / "frames.jsonl", "w", encoding="utf-8") as fh:
        for i in range(n):
            f = {"t": round(i / hz, 3), "roll": 0.1, "pitch": 0, "yaw": 0,
                 "voltage": 14.8, "battery_remaining": 80, "lat": 32.0, "lon": 118.8,
                 "hdop": 0.8, "rssi": -50, "quality_mask": {"roll": 1}}
            fh.write(json.dumps(f) + "\n")


def test_pass_at_20hz(tmp_path, capsys):
    from run_ingest.replay_check import replay_check
    d = tmp_path / "ok"; _write_frames(d, 20.0)
    assert replay_check(str(d)) == 0
    assert "PASS" in capsys.readouterr().out
    assert (d / "frames" / "replay_report.json").exists()


def test_fail_at_10hz_and_missing_dir(tmp_path):
    from run_ingest.replay_check import replay_check
    d = tmp_path / "slow"; _write_frames(d, 10.0)
    assert replay_check(str(d)) == 1
    assert replay_check(str(tmp_path / "nope")) == 2
