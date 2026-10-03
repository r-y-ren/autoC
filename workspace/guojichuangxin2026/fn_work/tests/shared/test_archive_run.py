"""archive_run 单测。"""
from __future__ import annotations

import json

import pytest

from shared.archive_run import archive_run


def _run(tmp, name):
    d = tmp / "sc" / name
    (d / "frames").mkdir(parents=True)
    (d / "metrics.jsonl").write_text('{"key": "a", "value": 1}\n', encoding="utf-8")
    (d / "manifest.json").write_text('{"scenario": "sc"}', encoding="utf-8")
    return d


def test_archive_copies_and_manifest(tmp_path):
    src = _run(tmp_path, "r1")
    dest = archive_run(str(src), str(tmp_path / "res"))
    assert (tmp_path / "res" / "sc" / "r1" / "metrics.jsonl").exists()
    assert src.exists(), "只拷不移：原件保留"
    m = json.loads((tmp_path / "res" / "sc" / "r1" / "manifest.json")
                   .read_text(encoding="utf-8"))
    assert m["archived_to"] == dest


def test_collision_suffix_and_missing(tmp_path):
    src = _run(tmp_path, "r1")
    d1 = archive_run(str(src), str(tmp_path / "res"))
    d2 = archive_run(str(src), str(tmp_path / "res"))
    assert d1 != d2 and d2.endswith("+2")
    with pytest.raises(FileNotFoundError):
        archive_run(str(tmp_path / "nope"))
