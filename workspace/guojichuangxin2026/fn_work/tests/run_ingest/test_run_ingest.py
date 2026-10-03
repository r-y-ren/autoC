"""run_ingest 单测（FakeSitlConn 合成源，SITL 语义等价数据流）。"""
from __future__ import annotations

import json

from conftest import FakeSitlConn


def test_ingest_produces_20hz_frames_and_files(tmp_path):
    from run_ingest.run_ingest import run_ingest
    cfg = {"run": {"hz": 20, "duration_s": 1.5, "home": [32.0, 118.8], "endpoint": "synthetic"}}
    conn = FakeSitlConn(duration_s=1.5)
    frames = list(run_ingest(cfg, tmp_path, conn=conn))
    assert 25 <= len(frames) <= 35            # ~30 帧（1.5s × 20Hz）
    ts = [f["t"] for f in frames]
    hz = (len(ts) - 1) / (ts[-1] - ts[0])
    assert hz >= 18                            # 帧率达标（容差）
    lines = (tmp_path / "frames" / "frames.jsonl").read_text().splitlines()
    assert len(lines) == len(frames)
    assert (tmp_path / "raw" / "raw.jsonl").exists()
    # 低速源字段经携带回填：lat 覆盖率高且掩码新鲜
    lat_ok = sum(1 for f in frames if f.get("lat") is not None) / len(frames)
    assert lat_ok > 0.9
    assert frames[-1].get("margins", {}).get("nav", {}).get("norm") is not None


def test_stop_condition_and_injest_error(tmp_path):
    from run_ingest.run_ingest import IngestError, run_ingest
    cfg = {"run": {"hz": 20, "duration_s": 2.0, "endpoint": "synthetic"}}
    frames = list(run_ingest(cfg, tmp_path, conn=FakeSitlConn(2.0),
                             stop_condition=lambda n, f: n >= 5))
    assert len(frames) == 5
    class Dead:
        def recv_match(self, **kw):
            return None
        def close(self):
            pass
    import pytest
    with pytest.raises(IngestError):
        list(run_ingest({"run": {"hz": 20, "endpoint": "udp:127.0.0.1:1"}},
                        tmp_path / "x"))  # 不可达端点→建链失败
