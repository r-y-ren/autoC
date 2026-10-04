"""[PKGFIX1] A bare `python scripts/package_submission.py` packages exactly the shipped parameter files
(SHIP_VRP15_K2FIRE dist/vrp15_k2fire.tar.gz = sub 56612145 res940_vrp12_pfs params + the KERNEL2 v3 runtime): theta7659 (94a8ffd2), head_940 (769ff15e), ESWORK_THETA g30 (6928257a) and the
shipped residual_head.py module (5e833774) -- never artifacts/theta.npy (328af843).
Named-file test: .venv/bin/python -m pytest tests/test_package_defaults.py"""
import hashlib
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SHIPPED_TGZ = ROOT / "dist" / "vrp20_pfsoff.tar.gz"   # PACK20 vrp20_pfsoff LIVE sub 56652418 (md5 e5d84f03); PACKWIDE1 vrp19w_k2wide LIVE sub 56649892 (e490347d); vrp18_k2hb2046 56646827 retired (d6ed14d6); vrp17_k2hb 56643352 retired (11fd0f57); PACKV3: SHIP_VRP15_K2FIRE retired (md5 1929f224); PACKV2 vrp14_k2real 233430d3; retired vrp12_pfs 56612145 (2532e456)
WANT = {  # archive member -> md5 prefix of the shipped file
    "theta.npy": "94a8ffd2",
    "residual_head.npz": "769ff15e",
    "kagg3/core/eswork_theta.npy": "6928257a",
    "kagg3/core/residual_head.py": "5e833774",
}


def _md5(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()


def _members(tgz: Path) -> dict:
    with tarfile.open(tgz) as tf:
        return {m.name: _md5(tf.extractfile(m).read()) for m in tf.getmembers() if m.isfile()}


@pytest.fixture(scope="module")
def bare(tmp_path_factory):
    out = tmp_path_factory.mktemp("pkg") / "bare.tar.gz"   # never dist/
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "package_submission.py"), "--out", str(out)],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    return _members(out)


def test_default_source_files_are_shipped():
    sys.path.insert(0, str(ROOT / "scripts"))
    import package_submission as pkg
    assert _md5(pkg.DEFAULT_THETA.read_bytes()).startswith("94a8ffd2")
    assert _md5(pkg.DEFAULT_RESIDUAL.read_bytes()).startswith("769ff15e")
    assert _md5(pkg.RESIDUAL_HEAD_PY.read_bytes()).startswith("5e833774")


def test_bare_build_carries_shipped_parameters(bare):
    for name, want in WANT.items():
        assert name in bare, name
        assert bare[name].startswith(want), (name, bare[name])


def test_bare_build_main_turns_residual_on(bare):
    main = (ROOT / "build" / "submission" / "main.py").read_text()
    assert "_plan.RESIDUAL_ON = True" in main


@pytest.mark.skipif(not SHIPPED_TGZ.is_file(), reason="shipped tarball not in dist/ on this checkout")
def test_bare_build_equals_shipped_tree(bare):
    assert bare == _members(SHIPPED_TGZ)   # every file byte-identical (archive metadata aside)
