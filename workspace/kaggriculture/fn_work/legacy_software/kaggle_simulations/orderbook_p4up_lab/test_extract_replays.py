# -*- coding: utf-8 -*-
"""test_extract_replays —— 抽取管线判例（命令构造/SQL/ID 收集；不执行 duckdb）。"""
import json
import os
import tempfile

from orderbook_p4up_lab import extract_replays as E


class TestCmdBuild:
    def test_bwrap_sandbox_template(self):
        cmd = E.build_bwrap_cmd("SELECT 1", duckdb="/opt/duckdb")
        assert cmd[0] == "bwrap"
        assert "--unshare-net" in cmd and "/opt/duckdb" in cmd
        assert cmd[-2] == "-c" and cmd[-1] == "SELECT 1"
        # 根只读 + /tmp 可写
        assert cmd.count("--ro-bind") == 1 and "/tmp" in cmd

    def test_sql_copy_json(self):
        sql = E.build_extract_sql(["/a/x.parquet", "/a/y.parquet"],
                                  [1, 2, 3], "/tmp/out.json")
        assert sql.startswith("COPY (SELECT episode_id, replay_json")
        assert "read_parquet(['/a/x.parquet', '/a/y.parquet'])" in sql
        assert "episode_id IN (1, 2, 3)" in sql
        assert sql.endswith("(FORMAT JSON)")

    def test_sql_escapes_quotes(self):
        sql = E.build_extract_sql(["/a/b'c.parquet"], [9], "/tmp/o.json")
        assert "b''c.parquet" in sql


class TestCollectIds:
    def _feats(self, path):
        rows = [
            {"src": "s1.parquet", "episode_id": 11,
             "players": [{"team": "TFC"}, {"team": "X"}]},
            {"src": "s2.parquet", "episode_id": 22,
             "players": [{"team": "Y"}, {"team": "TFC"}]},
            {"src": "s1.parquet", "episode_id": 33,
             "players": [{"team": "Z"}, {"team": "W"}]},
        ]
        with open(path, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r) + "\n")

    def test_collect_by_team_and_src(self):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "f.jsonl")
            self._feats(p)
            assert E.collect_episode_ids(p, "TFC") == [11, 22]
            assert E.collect_episode_ids(p, "TFC", src="s1.parquet") == [11]
            assert E.collect_episode_ids(p, "TFC", limit=1) == [11]
            assert E.collect_episode_ids(p, "NOPE") == []
