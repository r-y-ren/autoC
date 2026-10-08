"""渲染后 JS 语法门（node --check）——页面 script 块语法回归闸（评审 C1/C2 教训）。"""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from run_ground_station.register_pages import register_pages

PAGES = ("/", "/timeline", "/waterfall", "/replay", "/console")


@pytest.mark.skipif(shutil.which("node") is None, reason="node 不在 PATH")
def test_all_pages_script_blocks_parse():
    app = FastAPI()
    register_pages(app, "/tmp/jscheck")
    c = TestClient(app)
    bad = []
    for path in PAGES:
        html = c.get(path).text
        for m in re.finditer(r"<script[^>]*>(.*?)</script>", html, re.S):
            js = m.group(1)
            if not js.strip():
                continue
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
                fh.write(js)
                fp = fh.name
            r = subprocess.run(["node", "--check", fp], capture_output=True, text=True)
            if r.returncode != 0:
                bad.append((path, r.stderr.splitlines()[:2]))
    assert not bad, f"JS 语法错误: {bad}"
