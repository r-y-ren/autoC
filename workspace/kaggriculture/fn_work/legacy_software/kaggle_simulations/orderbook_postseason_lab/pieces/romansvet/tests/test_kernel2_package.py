"""[V56PACK1] KERNEL2 packaging contract.  Named-file test: .venv/bin/python -m pytest tests/test_kernel2_package.py
* a build without --kernel2 emits the pre-KERNEL2 main.py byte for byte (the OFF contract);
* --kernel2 only swaps the act line to pass `configuration` (the V56 kernel reads it);
* the embedded kernel is S/v56leg/main.py verbatim under a one-line provenance header, and loads to e410_agent;
* a bare build follows plan.KERNEL2_ON's default; --kernel2 on an OFF tree is refused."""
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))
import package_submission as pkg  # noqa: E402


def test_off_main_is_the_template():
    assert pkg.main_source(0, True) == pkg.main_source(0, True, False)
    assert "rt.act(observation)\n" in pkg.main_source(0, True)


def test_kernel2_main_passes_configuration_only():
    off, on = pkg.main_source(0, True), pkg.main_source(0, True, True)
    assert on == off.replace("rt.act(observation)\n", "rt.act(observation, configuration)\n")


def test_embedded_kernel_is_v56_verbatim():
    raw = (ROOT / "src/kagg3/agent/v56kernel.py").read_bytes()
    head, body = raw.split(b"\n", 1)
    assert head.startswith(b"# kagg3 V56PACK1 provenance:")
    assert b"Apache License" in body[:5000]
    assert hashlib.sha256(body).hexdigest().startswith("a1ad0fd1d174477e")


def test_kernel_loads_fresh_per_call():
    from kagg3.agent import runtime as R
    a, b = R.kernel2_load(), R.kernel2_load()
    assert a.__name__ == b.__name__ == "e410_agent" and a is not b and a.__globals__ is not b.__globals__


def test_bare_build_follows_plan_default(tmp_path):
    """A bare build ships the kernel iff KERNEL2_ON defaults True; --kernel2 on an OFF tree is refused."""
    import tarfile
    out = tmp_path / "x.tar.gz"
    r = subprocess.run([sys.executable, str(ROOT / "scripts/package_submission.py"), "--out", str(out)],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    with tarfile.open(out) as tf:
        names = tf.getnames()
        main = tf.extractfile("main.py").read().decode()
    on = pkg.kernel2_default()
    assert ("kagg3/agent/v56kernel.py" in names) == on
    assert ("rt.act(observation, configuration)" in main) == on
    if not on:
        r = subprocess.run([sys.executable, str(ROOT / "scripts/package_submission.py"), "--out", str(out), "--kernel2"],
                           cwd=ROOT, capture_output=True, text=True)
        assert r.returncode != 0 and "KERNEL2_ON default is False" in r.stderr
