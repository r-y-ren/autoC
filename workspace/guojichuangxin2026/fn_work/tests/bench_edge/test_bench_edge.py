"""bench_edge 单测。"""
from __future__ import annotations

import pytest

from bench_edge.bench_edge import BenchError, bench_edge


def test_dryrun_finite_percentiles():
    r = bench_edge("dryrun")
    assert r["mode"] == "dryrun" and 0 < r["p50_ms"] < 500
    assert r["p95_ms"] >= r["p50_ms"]


def test_deploy_requires_host():
    with pytest.raises(BenchError):
        bench_edge("deploy")
    r = bench_edge("deploy", {"jetson_host": "jetson@192.168.1.10"})
    assert r["commands"] and "manual" in r["note"]
