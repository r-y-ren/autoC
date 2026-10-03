"""append_record 单测。"""
from __future__ import annotations

import json

import pytest

from shared.append_record import append_record


def test_event_metric_routing_and_seq(tmp_path):
    append_record(tmp_path, "event", {"type": "test", "level": 2})
    append_record(tmp_path, "event", {"type": "test2"})
    append_record(tmp_path, "metric", {"key": "demo/lead_p10_s", "value": 5.1})
    ev = [json.loads(x) for x in (tmp_path / "events.jsonl").read_text().splitlines()]
    mt = [json.loads(x) for x in (tmp_path / "metrics.jsonl").read_text().splitlines()]
    assert [e["seq"] for e in ev] == [1, 2] and ev[0]["type"] == "test"
    assert mt[0]["key"] == "demo/lead_p10_s" and mt[0]["ts"]


def test_bad_kind_rejected(tmp_path):
    with pytest.raises(ValueError):
        append_record(tmp_path, "bogus", {})
