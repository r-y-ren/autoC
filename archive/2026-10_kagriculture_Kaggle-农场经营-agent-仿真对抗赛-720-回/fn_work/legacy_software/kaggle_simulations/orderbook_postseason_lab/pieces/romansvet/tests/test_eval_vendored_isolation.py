"""A packaged opponent must run its *own* vendored `kagg3`, not this tree's.

`scripts/eval_vs_baselines.py` seats packaged submissions as file agents. The
engine loader appends the agent's directory to `sys.path` while it execs
`main.py`, and the packaged `main.py` only prepends its directory when it is not
already on the path -- so with `src` at `sys.path[0]` the package's
`from kagg3 import ...` silently resolved to the working tree. Every panel
number then compared thetas under one planner instead of the packaged agents
as shipped. `_vendored_imports` must make the package's copy the one imported.
"""
import os, pathlib, sys, tarfile, tempfile

import numpy as np
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
os.chdir(ROOT)                      # the runner locates `src` relative to cwd
sys.path.insert(0, str(ROOT / "src"))
sys.path.append(str(ROOT / "scripts"))
import package_submission as pkg
import eval_vs_baselines as E


@pytest.fixture(scope="module")
def packaged():
    theta = ROOT / "artifacts" / "theta.npy"
    if not theta.exists():
        pytest.skip("no theta yet")
    d = tempfile.mkdtemp()
    out = pkg.build(theta, pathlib.Path(d) / "submission.tar.gz")
    with tarfile.open(out) as tf:
        tf.extractall(d)
    # Mark the vendored copy so the test can tell it from the tree's module.
    marker = pathlib.Path(d) / "kagg3" / "core" / "plan.py"
    marker.write_text(marker.read_text() + "\nVENDORED_MARKER = True\n")
    return os.path.join(d, "main.py")


def test_file_agent_imports_its_own_kagg3(packaged):
    from kaggle_environments.agent import get_last_callable
    import kagg3.core.plan as tree_plan
    assert not hasattr(tree_plan, "VENDORED_MARKER")
    with E._vendored_imports(True):
        get_last_callable(open(packaged).read(), path=packaged)
        loaded = sys.modules["kagg3.core.plan"]
        assert getattr(loaded, "VENDORED_MARKER", False), loaded.__file__
        assert os.path.dirname(os.path.dirname(loaded.__file__)) == \
            os.path.join(os.path.dirname(packaged), "kagg3")
    # Restored: the tree's modules and path are back for the next game.
    assert sys.modules["kagg3.core.plan"] is tree_plan
    assert any(os.path.abspath(p) == E._SRC for p in sys.path)


def test_isolation_is_a_no_op_without_file_agents():
    import kagg3.core.plan as tree_plan
    path = list(sys.path)
    env = dict(os.environ)
    with E._vendored_imports(False):
        assert sys.modules["kagg3.core.plan"] is tree_plan
        assert sys.path == path
        assert dict(os.environ) == env


# --- and its *environment* must not leak either ------------------------------
#
# A packaged kagg3 submission does more than import its own modules: the
# `KAGG3_OPENING` splice has to reach `os.environ` before the agent object is
# built, so `package_submission.py` emits an `os.environ.setdefault(...)` at
# the top of `main.py`. That write outlives the game. Hiding modules and paths
# does nothing about it, and the next game the worker plays builds *our* seat
# through `runtime.make_agent` -> `opening.from_env`, which reads that variable
# and silently splices the opponent's opening in front of the candidate theta.
# Measured 2026-09-03: with `artifacts/panel_opp/open16_pkg/main.py` in the
# `--opponents` list, our seat's row on seed 479691604 went 66,609 -> 149,629
# coins. Symmetrically, a `KAGG3_OPENING` we set for our own seat must not
# reach the packaged agent, whose `setdefault` would then keep *our* tape
# instead of the one it ships.

_FAKE_MAIN = '''\
import inspect, os, sys

_HERE = os.path.dirname(os.path.abspath(inspect.currentframe().f_code.co_filename))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

os.environ.setdefault("KAGG3_OPENING", os.path.join(_HERE, "tape.py") + ":16")

from kagg3.agent import runtime as _rt

assert getattr(_rt, "VENDORED_MARKER", None) == _HERE, _rt.__file__


def agent(observation, configuration=None):
    return {}
'''


def _fake_package(root):
    """A minimal kagg3-*shaped* submission: own `kagg3` image + own opening.

    Stands in for `artifacts/panel_opp/open16_pkg` so the case costs
    milliseconds instead of the ~8 s a real game takes. It reproduces the two
    things that matter: a vendored `kagg3.agent.runtime` that shadows ours, and
    the `os.environ.setdefault("KAGG3_OPENING", ...)` the packager emits.
    """
    root = pathlib.Path(root)
    (root / "kagg3" / "agent").mkdir(parents=True, exist_ok=True)
    (root / "kagg3" / "__init__.py").write_text("")
    (root / "kagg3" / "agent" / "__init__.py").write_text("")
    (root / "kagg3" / "agent" / "runtime.py").write_text(
        f"VENDORED_MARKER = {str(root)!r}\n"
        "def make_agent(macro_fn):\n"
        "    return lambda obs, config=None: {}\n")
    (root / "tape.py").write_text(
        "def agent(observation, configuration=None):\n    return {}\n")
    (root / "main.py").write_text(_FAKE_MAIN)
    return str(root / "main.py")


@pytest.fixture(scope="module")
def fake_pkgs():
    d = pathlib.Path(tempfile.mkdtemp())
    return [_fake_package(d / "A"), _fake_package(d / "B")]


def _spec_of(main_py):
    return os.path.join(os.path.dirname(main_py), "tape.py") + ":16"


def test_file_agent_env_does_not_reach_our_next_agent(fake_pkgs):
    from kaggle_environments.agent import get_last_callable
    from kagg3.agent import opening, runtime
    main_py = fake_pkgs[0]

    before = dict(os.environ)
    with E._vendored_imports(True):
        get_last_callable(open(main_py).read(), path=main_py)
        # Its own image, intact: the splice it ships is the one in force.
        assert os.environ[opening.ENV_VAR] == _spec_of(main_py)
    assert dict(os.environ) == before, "the game leaked environment variables"

    # The next game in this worker builds our seat from the tree's runtime,
    # and gets the bare planner -- not the opponent's opening spliced in front.
    assert sys.modules["kagg3.agent.runtime"] is runtime
    assert not hasattr(runtime, "VENDORED_MARKER")
    assert not isinstance(runtime.make_agent(lambda *a: None), opening.OpeningSplice)


def test_our_env_does_not_reach_a_file_agent(fake_pkgs, monkeypatch):
    """And the other direction: a packaged agent keeps the opening it ships."""
    from kaggle_environments.agent import get_last_callable
    from kagg3.agent import opening
    main_py = fake_pkgs[0]

    monkeypatch.setenv(opening.ENV_VAR, "/nowhere/ours.py:9")
    with E._vendored_imports(True):
        get_last_callable(open(main_py).read(), path=main_py)
        assert os.environ[opening.ENV_VAR] == _spec_of(main_py)
    assert os.environ[opening.ENV_VAR] == "/nowhere/ours.py:9"


def test_one_file_agent_does_not_reach_the_next(fake_pkgs):
    """Two packaged opponents in one worker each keep their own opening."""
    from kaggle_environments.agent import get_last_callable
    from kagg3.agent import opening
    for main_py in fake_pkgs:
        with E._vendored_imports(True):
            get_last_callable(open(main_py).read(), path=main_py)
            assert os.environ[opening.ENV_VAR] == _spec_of(main_py)
        assert opening.ENV_VAR not in os.environ


# --- and the package has to be one the engine can actually exec --------------
#
# `--me` names what `package_submission.py` writes and what Kaggle takes: a
# `.tar.gz`. `kaggle_environments` reads *any* existing path as Python source,
# so the gzip bytes compiled to a SyntaxError, `build_agent` swallowed it and
# returned the raw string every turn, and the engine recorded no action at all
# -- statuses DONE, no error anywhere, and our seat finished every game on its
# untouched starting 3000 coins. Measured 2026-09-04 against every opponent at
# --workers 1 and 2 with `dist/submission_flow58_g450_pump.tar.gz`, a package
# that was live on Kaggle at 46W-6L. `_unpack_agent` seats the `main.py`
# inside the archive -- which is also what lets `_is_file_agent`, and with it
# the whole guard above, see a packaged agent at all.

START_MONEY = 3000
SHORT_GAME = 20                     # steps: under a day, enough to spend money


@pytest.fixture(scope="module")
def packaged_tar(tmp_path_factory):
    theta = ROOT / "artifacts" / "theta.npy"
    if not theta.exists():
        pytest.skip("no theta yet")
    return pkg.build(theta, tmp_path_factory.mktemp("me") / "submission.tar.gz")


def test_play_seats_a_packaged_tarball(packaged_tar, monkeypatch):
    """The harness's own `--me` path, over one short game in the real engine."""
    import kaggle_environments as ke
    real_make, envs = ke.make, []

    def short_make(name, *a, configuration=None, **k):
        env = real_make(name, *a, configuration=dict(configuration or {},
                                                     episodeSteps=SHORT_GAME), **k)
        envs.append(env)
        return env

    monkeypatch.setattr(ke, "make", short_make)
    me = E._unpack_agent(str(packaged_tar))
    assert E._is_file_agent(me), me      # or the vendored-import guard never arms
    _, mine, _, *_ = E._play((12345, "pass", 0, None, False, me, None))
    assert [a.status for a in envs[-1].state] == ["DONE", "DONE"]
    assert mine != START_MONEY, "the packaged seat never acted"


def test_unpack_agent_refuses_what_the_engine_would_read_as_source(tmp_path):
    """A path that is neither: loud here beats a silent 3000 forty games later."""
    junk = tmp_path / "theta.npy"
    junk.write_bytes(b"\x93NUMPY")
    with pytest.raises(SystemExit):
        E._unpack_agent(str(junk))
