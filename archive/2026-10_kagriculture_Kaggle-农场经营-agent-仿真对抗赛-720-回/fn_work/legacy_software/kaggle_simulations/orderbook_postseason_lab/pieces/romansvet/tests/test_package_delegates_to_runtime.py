"""The packaged `main.py` must not own a second copy of the turn loop.

`package_submission.MAIN` used to spell out `Runtime.act` by hand: parse the
view, build the day's plan at hour 0, render the turn. The copy then fell one
edit behind the original -- `runtime.py` grew the `open_pump_tell_keep0` hour-1
patch and the template did not -- and nothing noticed, because the switch that
patch serves is off. A promoted switch would have shipped without its
behaviour.

So the template no longer contains a turn loop at all: it builds the macro
closure and hands every turn to the *vendored* `kagg3.agent.runtime.Runtime`,
the same class every local evaluation drives. These two tests are what keeps it
that way -- one reads the emitted source and refuses any act-logic in it, the
other plays real engine observations through the packaged entry point and
through `Runtime.act` and demands the same action dicts.
"""
import ast
import copy
import importlib.util
import pathlib
import sys
import tarfile
from types import SimpleNamespace

import numpy as np
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

THETA = ROOT / "artifacts" / "theta.npy"

#: Names that only a hand-written turn loop would mention. `turn_action` and
#: `build_day` are the two halves of `Runtime.act`; the `open_pump_tell_*` pair
#: is the patch the old copy had already lost.
ACT_LOGIC = ("turn_action", "build_day", "open_pump_tell_armed",
             "open_pump_tell_keep0")


def _packager():
    spec = importlib.util.spec_from_file_location(
        "package_submission", ROOT / "scripts" / "package_submission.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def packaged(tmp_path_factory):
    """An unpacked archive, built the way `scripts/submit.py` builds one."""
    if not THETA.exists():
        pytest.skip("no theta yet")
    d = tmp_path_factory.mktemp("pkg")
    out = _packager().build(THETA, d / "submission.tar.gz")
    with tarfile.open(out) as tf:
        tf.extractall(d)
    return d


def test_main_has_no_act_logic_of_its_own(packaged):
    src = (packaged / "main.py").read_text()
    tree = ast.parse(src)

    for name in ACT_LOGIC:
        assert name not in src, (
            f"packaged main.py mentions {name}: it is re-implementing "
            "Runtime.act instead of calling it, which is exactly the drift "
            "this test exists to prevent")
    assert not [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)], \
        "packaged main.py defines a class -- no Runtime lookalikes"
    assert "runtime as _runtime" in src, \
        "packaged main.py no longer imports the vendored runtime"

    # `agent` is the entry point kaggle_environments picks: the last callable
    # in the exec namespace. Its whole body must be seat bookkeeping plus the
    # delegating return.
    fn = tree.body[-1]
    assert isinstance(fn, ast.FunctionDef) and fn.name == "agent", \
        "`agent` must remain the last definition in the module"
    assert [a.arg for a in fn.args.args] == ["observation", "configuration"], \
        "the Kaggle entry-point signature changed"
    assert len(fn.body) <= 5, "the entry point grew a turn loop"
    ret = fn.body[-1]
    assert isinstance(ret, ast.Return) and isinstance(ret.value, ast.Call) \
        and isinstance(ret.value.func, ast.Attribute) \
        and ret.value.func.attr == "act", \
        "the entry point does not end in a delegation to Runtime.act"


def test_archive_still_carries_the_runtime_it_delegates_to(packaged):
    """Delegation only helps if the module is inside the tarball."""
    assert (packaged / "kagg3" / "agent" / "runtime.py").is_file()
    assert (packaged / "kagg3" / "agent" / "runtime.py").read_bytes() == \
        (ROOT / "src" / "kagg3" / "agent" / "runtime.py").read_bytes()


def _observations():
    """Real engine observations, one per seat, replayed across turns.

    `env.reset` is the recorded state -- a genuine day-0 board from the engine,
    with `private`, `town` and `market` as the agent would receive them. The
    hour and day are then walked by hand so that all three of `Runtime.act`'s
    branches are exercised: the hour-0 build, the cached replay, and the
    day-change rebuild. Both paths see byte-identical input dicts, so any
    difference in the action is a difference in the code.
    """
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": 20260821})
    env.reset(2)
    out = []
    for player in (0, 1):
        base = env.state[player].observation
        for day in (0, 1):
            for hour in (0, 1, 2, 23):
                obs = copy.deepcopy(dict(base))
                obs["player"], obs["day"], obs["hour"] = player, day, hour
                out.append(obs)
    return out


def _load_main(packaged):
    spec = importlib.util.spec_from_file_location(
        "packaged_main", packaged / "main.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_entry_point_matches_runtime_act(packaged):
    """The packaged agent's actions are `Runtime.act`'s actions, turn for turn."""
    import plan_stats

    from kagg3.agent import runtime

    theta = np.load(THETA).astype(np.float32)
    ref = {}
    mod = _load_main(packaged)
    assert mod.agent.__code__.co_argcount == 2

    seen = 0
    for obs in _observations():
        player = obs["player"]
        if player not in ref:
            ref[player] = runtime.Runtime(plan_stats.make_macro(theta))
        want = ref[player].act(copy.deepcopy(obs))
        got = mod.agent(copy.deepcopy(obs))
        assert got == want, (
            f"player {player} day {obs['day']} hour {obs['hour']}: "
            f"packaged {got} != runtime {want}")
        seen += 1
    assert seen == 16
    # Not vacuous: a farm that does nothing all season would pass on empty rows.
    assert any(ref[0].plan is not None for _ in (0,))


def test_runtime_rotates_market_history_once_per_dawn(monkeypatch):
    """Repeated hour zero is history-safe and later hours use the cached plan."""
    from kagg3.agent import runtime
    monkeypatch.setattr(runtime.P, "KERNEL2_ON", False)   # [V56PACK1] the PFS path's contract, whatever the default

    seen = []
    monkeypatch.setattr(runtime.parse, "parse_view",
                        lambda obs, player: SimpleNamespace(player=player))
    monkeypatch.setattr(runtime.parse, "parse_market",
                        lambda obs: (np.asarray(obs["inventory"], np.int32), None))
    monkeypatch.setattr(runtime.P, "build_day", lambda xp, view, macro: macro)
    monkeypatch.setattr(runtime.render, "turn_action",
                        lambda plan, hour, hands: {"hour": hour, "plan": plan})

    def macro(obs, player, view, previous):
        seen.append((obs["day"], np.asarray(previous).copy(),
                     np.asarray(obs["inventory"]).copy()))
        return len(seen)

    rt = runtime.Runtime(macro, pass_prev_mkt_inv=True)

    def obs(day, hour, inventory):
        return {"player": 0, "day": day, "hour": hour,
                "inventory": np.asarray(inventory, np.int32),
                "farms": [{"hands": []}]}

    dawn0 = np.arange(9, dtype=np.int32) + 100
    dawn1 = np.arange(9, dtype=np.int32) + 80
    rt.act(obs(0, 0, dawn0))
    rt.act(obs(0, 0, dawn0))
    before = len(seen)
    rt.act(obs(0, 1, dawn0 - 1))
    assert len(seen) == before
    rt.act(obs(1, 0, dawn1))
    rt.act(obs(1, 0, dawn1))

    assert [day for day, _, _ in seen] == [0, 0, 1, 1]
    for _, previous, current in seen[:2]:
        np.testing.assert_array_equal(previous, dawn0)
        np.testing.assert_array_equal(current, dawn0)
    for _, previous, current in seen[2:]:
        np.testing.assert_array_equal(previous, dawn0)
        np.testing.assert_array_equal(current, dawn1)


def test_runtime_legacy_macro_keeps_three_argument_contract(monkeypatch):
    """History remains an explicit opt-in for every existing runtime caller."""
    from kagg3.agent import runtime
    monkeypatch.setattr(runtime.P, "KERNEL2_ON", False)   # [V56PACK1] the PFS path's contract, whatever the default

    monkeypatch.setattr(runtime.parse, "parse_view", lambda obs, player: object())
    monkeypatch.setattr(runtime.P, "build_day", lambda xp, view, macro: macro)
    monkeypatch.setattr(runtime.render, "turn_action", lambda *args: {})
    seen = []

    def macro(obs, player, view):
        seen.append((obs["day"], player))
        return 1

    runtime.Runtime(macro).act(
        {"player": 0, "day": 0, "hour": 0, "farms": [{"hands": []}]})
    assert seen == [(0, 0)]
