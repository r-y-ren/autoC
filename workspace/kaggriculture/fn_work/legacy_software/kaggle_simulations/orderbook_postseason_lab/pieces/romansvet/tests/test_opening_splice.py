"""`KAGG3_OPENING` splices a recorded opening in front of the planner.

Three things have to hold for the spike to mean anything:

* with the variable unset the factory hands back the plain planner, on the
  same code path it always used -- the switch has to be free when it is off;
* with it set, the first `K` days are the tape's own aligned actions and day
  `K` is the planner's, on the board the tape left behind;
* a roster shorter than the recording's does not invalidate the turn -- the
  tape's `hands` list is truncated to the live crew, which is the one runtime
  repair `scripts/tape_opponent.py` builds into every tape it cuts.

The tape here is generated in-process from that script's own template, so the
test needs no artifact on disk and still exercises the exact module image the
engine loads.
"""
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np

import tape_opponent
from kagg3.agent import opening, runtime

SEED = 20260821
K = 2
#: One full engine day, so a K=2 tape covers days 0 and 1 exactly.
TURNS_PER_DAY = 24


def _theta():
    p = ROOT / "artifacts" / "theta.npy"
    if not p.exists():
        pytest.skip("no theta yet")
    return np.load(p).astype(np.float32)


def _macro():
    import plan_stats
    return plan_stats.make_macro(_theta())


def _tape_frames(n=K * TURNS_PER_DAY + 1):
    """Frames distinguishable from anything the planner would emit -- the
    farmer paces north/south and three hands stand idle -- and one frame past
    the splice, so day K has a tape action to be compared against."""
    return [{"farmer": ["NORTH" if s % 2 else "SOUTH"],
             "hands": [["PASS"], ["PASS"], ["PASS"]],
             "market": []}
            for s in range(n)]


@pytest.fixture(scope="module")
def tape_main(tmp_path_factory):
    src = tape_opponent.render_main(_tape_frames(), episode=0, seat=0,
                                    team="fixture", opp_team="fixture",
                                    final_money=0)
    path = tmp_path_factory.mktemp("opening") / "main.py"
    path.write_text(src)
    return path


def _trainer_obs():
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": SEED})
    return env.train([None, "starter"])


def test_unset_env_returns_the_bare_planner(monkeypatch):
    """Off is not a wrapper around the planner, it *is* the planner."""
    monkeypatch.delenv(opening.ENV_VAR, raising=False)
    macro = _macro()
    agent = runtime.make_agent(macro)
    assert not isinstance(agent, opening.OpeningSplice)

    obs = _trainer_obs().reset()
    assert agent(obs) == runtime.Runtime(macro).act(obs)


def test_tape_drives_the_first_k_days_then_the_planner(monkeypatch, tape_main):
    """Days 0..K-1 are the tape's aligned frames; day K is the planner's."""
    monkeypatch.setenv(opening.ENV_VAR, f"{tape_main}:{K}")
    spliced = runtime.make_agent(_macro())
    assert isinstance(spliced, opening.OpeningSplice)

    ns = {}
    exec(compile(tape_main.read_text(), str(tape_main), "exec"), ns)  # noqa: S102
    align, hand_count, step_of = ns["_align"], ns["_hand_count"], ns["_step"]

    trainer = _trainer_obs()
    obs = trainer.reset()
    for _ in range(K * TURNS_PER_DAY):
        act = spliced(obs)
        assert act == align(ns["_TAPE"][step_of(obs)], hand_count(obs)), \
            f"day {obs.get('day')} hour {obs.get('hour')} strayed from the tape"
        obs, _, done, _ = trainer.step(act)
        assert not done

    assert int(obs["day"]) == K and int(obs["hour"]) == 0
    monkeypatch.delenv(opening.ENV_VAR)
    planner = runtime.make_agent(_macro())
    handover = spliced(obs)
    assert handover == planner(obs), "day K did not come from the planner"
    assert handover != align(ns["_TAPE"][step_of(obs)], hand_count(obs))


@pytest.mark.parametrize("roster", [0, 1, 2, 3, 5])
def test_hands_are_truncated_to_the_live_roster(monkeypatch, tape_main, roster):
    """A refused HIRE shortens the crew; the engine rejects an action whose
    `hands` list outruns the farm's, so the tape's three orders are clipped."""
    monkeypatch.setenv(opening.ENV_VAR, f"{tape_main}:{K}")
    spliced = runtime.make_agent(_macro())
    obs = {"player": 0, "day": 0, "hour": 5, "step": 5,
           "farms": [{"hands": [{}] * roster}, {"hands": []}]}
    act = spliced(obs)
    assert len(act["hands"]) == roster
    assert all(order == ["PASS"] for order in act["hands"])
    assert act["farmer"] == ["NORTH"]


def test_spec_parsing():
    assert opening.parse_spec("/a/b/main.py:10") == ("/a/b/main.py", 10)
    with pytest.raises(ValueError):
        opening.parse_spec("/a/b/main.py")
