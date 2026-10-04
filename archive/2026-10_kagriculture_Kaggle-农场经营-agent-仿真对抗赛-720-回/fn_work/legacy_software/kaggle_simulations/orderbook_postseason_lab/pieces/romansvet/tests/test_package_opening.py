"""`--opening` makes the submission archive carry its own opening tape.

Kaggle runs the archive with none of our environment, so a package that wants
the splice has to switch it on from inside `main.py`.  Three things have to
hold:

* off is free -- with no `--opening` the emitted `main.py` is the string the
  packager always emitted, and the archive gains no file, so an unrelated
  rebuild cannot silently change what we upload;
* on, the spec names the *bundled* tape by absolute path (the engine execs
  `main.py` with a bare globals dict from an arbitrary cwd, so a relative name
  would not resolve) and the K the build asked for, and `opening.parse_spec`
  reads it back;
* the loader still finds the right callable: `kaggle_environments` takes the
  last callable in the exec namespace, so `agent` has to stay the final
  top-level definition even though the splice now wraps it.
"""
import ast
import importlib.util
import pathlib
import sys
import tarfile

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kagg3.agent import opening  # noqa: E402

TAPE = '''"""Stub tape."""


def agent(observation, configuration=None):
    return {"farmer": ["PASS"], "hands": [], "market": []}
'''


def _packager():
    spec = importlib.util.spec_from_file_location(
        "package_submission", ROOT / "scripts" / "package_submission.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def pkg():
    return _packager()


@pytest.fixture(scope="module")
def theta():
    p = ROOT / "artifacts" / "theta.npy"
    if not p.exists():
        pytest.skip("no theta yet")
    return p


@pytest.fixture
def tape(tmp_path):
    p = tmp_path / "tape_main.py"
    p.write_text(TAPE)
    return p


def _names(out):
    with tarfile.open(out, "r:gz") as tf:
        return set(tf.getnames())


def test_off_build_is_the_package_we_always_shipped(pkg, theta, tmp_path):
    out = pkg.build(theta, tmp_path / "off.tar.gz")
    names = _names(out)
    assert pkg.TAPE_NAME not in names
    assert "kagg3/agent/opening.py" not in names
    with tarfile.open(out, "r:gz") as tf:
        main = tf.extractfile("main.py").read().decode()
    assert main == pkg.MAIN
    assert opening.ENV_VAR not in main
    assert pkg.main_source(0) == pkg.MAIN


def test_on_build_points_the_spec_at_the_bundled_tape(pkg, theta, tape, tmp_path):
    out = pkg.build(theta, tmp_path / "on.tar.gz", tape, 16)
    names = _names(out)
    assert pkg.TAPE_NAME in names
    assert "kagg3/agent/opening.py" in names
    with tarfile.open(out, "r:gz") as tf:
        main = tf.extractfile("main.py").read().decode()
        assert tf.extractfile(pkg.TAPE_NAME).read().decode() == TAPE
    assert ('os.environ.setdefault(\n    "%s", os.path.join(_HERE, "%s") + ":16")'
            % (opening.ENV_VAR, pkg.TAPE_NAME)) in main
    # ...and it is set before the agent is built, not after.
    assert main.index(opening.ENV_VAR) < main.index("from_env")

    here = "/kaggle_simulations/agent"
    path, k = opening.parse_spec(f"{here}/{pkg.TAPE_NAME}:16")
    assert (path, k) == (f"{here}/{pkg.TAPE_NAME}", 16)


def test_agent_stays_the_last_definition(pkg, tape):
    """The loader takes the final callable in the namespace, so `agent` is last."""
    tree = ast.parse(pkg.main_source(16))
    assert isinstance(tree.body[-1], ast.FunctionDef)
    assert tree.body[-1].name == "agent"
    # A `def`, not the splice object: core.py trims the call's arguments by
    # `agent.__code__.co_argcount`, which a callable instance does not have.
    assert [a.arg for a in tree.body[-1].args.args] == ["observation", "configuration"]
