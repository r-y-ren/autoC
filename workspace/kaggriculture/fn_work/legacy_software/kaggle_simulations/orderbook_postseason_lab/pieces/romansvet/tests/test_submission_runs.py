"""The packaged submission must never raise inside kaggle_environments.

kaggle_environments catches agent exceptions and quietly substitutes a default
action, so a broken agent does not crash the episode -- it just stops playing and
finishes on its starting money. That failure mode is invisible unless you check
agent status explicitly, which is exactly what this does.
"""
import os
import pathlib
import sys
import tarfile
import tempfile
import importlib.util

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import pytest
from kaggle_environments import make

import package_submission as pkg


def _package_verifier():
    path = ROOT / "S/unitorder/verify_momentum_package.py"
    spec = importlib.util.spec_from_file_location("verify_momentum_package_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

SEEDS = [20260821, 1, 7, 424242]


@pytest.fixture(scope="module")
def packaged():
    theta = ROOT / "artifacts" / "theta.npy"
    if not theta.exists():
        pytest.skip("no theta yet")
    d = tempfile.mkdtemp()
    out = pkg.build(theta, pathlib.Path(d) / "submission.tar.gz")
    with tarfile.open(out) as tf:
        tf.extractall(d)
    return os.path.join(d, "main.py")


@pytest.mark.parametrize("seed", SEEDS)
@pytest.mark.parametrize("opponent", ["starter", "random"])
def test_agent_never_errors(packaged, seed, opponent):
    env = make("kaggriculture", configuration={"seed": seed})
    env.run([packaged, opponent])
    for i, step in enumerate(env.steps):
        assert step[0].status in ("ACTIVE", "DONE", "INACTIVE"), \
            f"seed {seed} vs {opponent}: agent status {step[0].status} at step {i}"
    farms = env.steps[-1][0].observation["farms"]
    # A silently-crashed agent finishes on exactly its starting money, having
    # taken no action all season.
    assert farms[0]["money"] != 3000.0, "agent appears to have taken no action"


def test_agent_plays_both_seats(packaged):
    env = make("kaggriculture", configuration={"seed": 5150})
    env.run(["starter", packaged])
    for step in env.steps:
        assert step[1].status in ("ACTIVE", "DONE", "INACTIVE")
    assert env.steps[-1][0].observation["farms"][1]["money"] != 3000.0


def test_archive_is_self_contained(packaged):
    """The archive must run with the working tree unreachable.

    The tests above put `src/` on sys.path, so an extracted archive still
    imports the *repo's* kagg3 -- a module missing from `INCLUDE` is invisible
    to them and the submission fails only on Kaggle. Here the agent runs in a
    subprocess whose import path cannot see the repo, which is how the
    competition actually loads it.
    """
    import json
    import subprocess

    d = os.path.dirname(packaged)
    script = (
        "import json, sys\n"
        "from kaggle_environments import make\n"
        "env = make('kaggriculture', configuration={'seed': 20260821})\n"
        f"env.run([{packaged!r}, 'starter'])\n"
        "farms = env.steps[-1][0].observation['farms']\n"
        "heavy = [m for m in ('jax','torch','tensorflow') if m in sys.modules]\n"
        "print(json.dumps({'money': farms[0]['money'], 'heavy': heavy}))\n"
    )
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    p = subprocess.run([sys.executable, "-c", script], cwd=d, env=env,
                       capture_output=True, text=True, timeout=600, check=False)
    assert p.returncode == 0, f"subprocess failed:\n{p.stderr[-2000:]}"
    out = json.loads(p.stdout.strip().splitlines()[-1])
    assert out["money"] != 3000.0, (
        "packaged agent took no action when the repo was unreachable -- "
        "a module it imports is missing from package_submission.INCLUDE")
    assert not out["heavy"], f"submission imported {out['heavy']}"


def test_archive_is_byte_reproducible():
    """Same inputs must give the same bytes.

    `build` sorts entries and zeroes mtime/uid/gid on the *tar* members, but
    "w:gz" also writes the current time into the gzip header, so two builds of
    identical inputs differed. Without this, the sha256 printed at build time
    cannot be used to confirm that the archive uploaded is the archive tested.
    """
    import hashlib

    theta = ROOT / "artifacts" / "theta.npy"
    if not theta.exists():
        pytest.skip("no theta yet")
    d = tempfile.mkdtemp()
    h = [hashlib.sha256(pkg.build(theta, pathlib.Path(d) / f"s{i}.tar.gz").read_bytes()).hexdigest()
         for i in range(2)]
    assert h[0] == h[1], "archive is not byte-reproducible"


def test_candidate_package_requires_native_finite_float32_theta(tmp_path):
    verifier = _package_verifier()
    valid = np.arange(6855, dtype=np.float32)
    path = tmp_path / "theta.npy"
    np.save(path, valid)
    assert verifier.checked_theta(path, 6855).tobytes() == valid.tobytes()

    for bad in (valid.astype(np.float64), valid[:-1],
                np.where(np.arange(6855) == 17, np.nan, valid).astype(np.float32)):
        np.save(path, bad)
        with pytest.raises(ValueError, match="finite float32"):
            verifier.checked_theta(path, 6855)


def test_candidate_package_manifest_is_closed_before_evidence_reads():
    verifier = _package_verifier()
    incomplete = {name: None for name in verifier.CANDIDATE_FIELDS}
    incomplete.update(schema=2, mode=verifier.CANDIDATE_MODE, seed=405658696,
                      timeout_seconds=600, replay=verifier.RECORDED_REPLAY,
                      input_sha256={})
    with pytest.raises(ValueError, match="input map is missing"):
        verifier.candidate_evidence(incomplete)

    malformed = dict(incomplete)
    malformed["unexpected"] = True
    with pytest.raises(ValueError, match="schema mismatch"):
        verifier.candidate_evidence(malformed)
