"""make_portable_bundle 单测（lite 模式：结构+SHA）。"""
from __future__ import annotations

import hashlib
import tarfile
from pathlib import Path


def test_lite_bundle_structure_and_sha(tmp_path):
    from make_portable_bundle.make_portable_bundle import make_portable_bundle
    r = make_portable_bundle(str(tmp_path), lite=True)
    tgz = Path(r["bundle"])
    assert tgz.exists() and r["mode"] == "lite"
    with tarfile.open(tgz) as tar:
        names = tar.getnames()
    for want in ("ahyd_portable/src", "ahyd_portable/portable_demo.sh",
                 "ahyd_portable/用户手册.md", "ahyd_portable/requirements.txt"):
        assert any(n == want or n.startswith(want + "/") or n.startswith(want)
                   for n in names), want
    sha = hashlib.sha256(tgz.read_bytes()).hexdigest()
    recorded = Path(str(tgz) + ".sha256").read_text().split()[0]
    assert sha == recorded
