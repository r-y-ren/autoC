"""The recorded town: extraction, the tape's new key, the sim, the engine seam.

The end-of-day shop unlock is the engine's only randomness anyone plays *for*,
and it cannot be reproduced by seeding: `_end_of_day` drains its per-day
generator weeds-first, one `random()` per EMPTY unlocked tile of each seat, so
which shop the town gains depends on how the two seats played that day. A
recorded opponent planted for the shops HIS game unlocked; replayed under a
freshly drawn town he farms for buyers who are not there. These tests cover the
four pieces that carry the recording's own town through instead.
"""

import json
import os
import subprocess
import sys

import numpy as np
import pytest

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
# The editable install writes the MAIN checkout's `src` into site-packages, so
# inside a git worktree a bare `import kagg3` reads the other tree. Put this
# tree's first: these tests are about code that only exists here.
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, os.path.join(_ROOT, "scripts"))

from kagg3 import spec                                               # noqa: E402
from kagg3.es import tape_actions as TA                              # noqa: E402

import tape_opponent as TO                                           # noqa: E402
import town_inject as TI                                             # noqa: E402


def _replay(unlocks):
    """A replay-shaped dict whose town grows on the given `(day, shop)` list."""
    steps, shops = [], []
    by_day = {}
    for day, name in unlocks:
        by_day.setdefault(int(day), []).append(name)
    for step in range(spec.N_DAYS * spec.TURNS_PER_DAY):
        day, hour = divmod(step, spec.TURNS_PER_DAY)
        if hour == 0:
            shops = shops + by_day.get(day, [])
        steps.append([{"observation": {"day": day, "hour": hour, "step": step,
                                       "town": {"unlocked_shops": list(shops)}}},
                      {"observation": {}}])
    return {"steps": steps}


SCHEDULE = [[3, "SMOOTHIE_SHOP"], [6, "BAKERY"], [9, "ICE_CREAM_SHOP"],
            [12, "SMOOTHIE_SHOP"], [15, "BAKERY"], [18, "PET_CAFE"],
            [21, "SMOOTHIE_SHOP"], [24, "BRUNCH_SPOT"]]


def test_extract_town_reads_the_unlock_days():
    """One `(day, shop)` per unlock, `day` = the day the shop is first visible.

    Repeats matter: shops are drawn WITH replacement and each copy consumes, so
    SMOOTHIE_SHOP appearing three times is three consumers, not one.
    """
    assert TO.extract_town(_replay(SCHEDULE)) == SCHEDULE


def test_town_array_round_trip():
    town = TA.town_array(SCHEDULE)
    assert town.shape == (spec.N_DAYS,) and town.dtype == np.int32
    assert town[3] == spec.SHOP_NAMES.index("SMOOTHIE_SHOP")
    # Every day the recording did NOT unlock on is marked, not merely absent:
    # `unlock_shop` reads the row in both directions.
    assert (town[[0, 1, 2, 4, 5, 27, 29]] == TA.NO_UNLOCK).all()
    assert TA.town_schedule(town) == SCHEDULE


def test_town_array_refuses_a_shop_it_cannot_place():
    with pytest.raises(ValueError):
        TA.town_array([[3, "NOT_A_SHOP"]])
    with pytest.raises(ValueError):
        TA.town_array([[3, "BAKERY"], [3, "PET_CAFE"]])


def _tape(town=None):
    frames = [{"farmer": ["PASS"], "hands": [], "market": []} for _ in range(719)]
    return TA.build(frames, episode=1, town=town)


def test_npz_key_is_optional_both_ways(tmp_path):
    """A tape cut without `--with-town` is the six-array file it always was, and
    still loads; one cut with it round-trips the schedule."""
    plain, rich = tmp_path / "plain.npz", tmp_path / "rich.npz"
    TA.save(plain, _tape())
    TA.save(rich, _tape(SCHEDULE))
    assert "town" not in np.load(plain).files
    assert TA.load(plain).town is None
    assert TA.town_schedule(TA.load(rich).town) == SCHEDULE


def test_stack_mixes_tapes_with_and_without_a_town():
    """A batch is legal as soon as ANY member carries a town; the others get an
    all-`NO_UNLOCK` row, which `unlock_shop` reads as "draw as usual"."""
    assert TA.stack([_tape(), _tape()]).town is None
    town = TA.stack([_tape(SCHEDULE), _tape()]).town
    assert town.shape == (2, spec.N_DAYS)
    assert (town[1] == TA.NO_UNLOCK).all()
    assert TA.town_schedule(town[0]) == SCHEDULE


# ------------------------------------------------------------------ the sim

def test_unlock_shop_follows_the_recording_not_the_draw():
    """The whole point: the same words, the same day, a different town.

    Also checks the "off" direction -- a day the recording did not unlock on
    must not unlock here either, whatever the draw says -- and that a row of
    all -1 leaves the drawn behaviour untouched.
    """
    import jax.numpy as jnp
    from kagg3.sim import eod
    from kagg3.sim.state import initial_state

    st = initial_state(jnp)
    words = jnp.asarray(eod.host_stream(20260911, 2))
    drawn = eod.unlock_shop(jnp, st, words, 0, 2)
    town = jnp.asarray(TA.town_array(SCHEDULE))
    forced = eod.unlock_shop(jnp, st, words, 0, 2, town=town)

    want = spec.SHOP_NAMES.index("SMOOTHIE_SHOP")     # day 3 in SCHEDULE
    assert int(forced.nshops) == 1 and int(forced.shops[want]) == 1
    assert int(drawn.nshops) == 1
    # `host_stream` is the engine's own generator, so `drawn` is a real draw;
    # the test is only interesting while it disagrees with the recording.
    assert int(jnp.argmax(drawn.shops)) != want

    # Day 3 -> day 4: not a shop-unlock day in either regime.
    assert int(eod.unlock_shop(jnp, st, words, 0, 3, town=town).nshops) == 0
    # A day the DRAW would unlock on but the recording did not: day 26 -> 27.
    empty = jnp.asarray(TA.town_array([]))
    assert int(eod.unlock_shop(jnp, st, words, 0, 26).nshops) == 1
    assert int(eod.unlock_shop(jnp, st, words, 0, 26, town=town).nshops) == 0
    # An all-NO_UNLOCK row is "no town on this board": the draw is untouched.
    assert int(eod.unlock_shop(jnp, st, words, 0, 26, town=empty).nshops) == 1


def test_end_of_day_without_a_town_is_unchanged():
    """`town=None` must stay the static "no such code" case: a rung cut before
    the flag existed has to keep scoring exactly what it scored, so the whole
    end-of-day state has to come back identical, not merely the shop count."""
    import jax.numpy as jnp
    from kagg3.sim import eod
    from kagg3.sim.state import initial_state

    st = initial_state(jnp)
    hi_t, lo_t = eod.weed_threshold()
    args = (jnp, st, 2, jnp.asarray(eod.host_stream(4242, 2)),
            jnp.int32(hi_t), jnp.int32(lo_t))
    before = eod.end_of_day(*args)
    after = eod.end_of_day(*args, town=None)
    for a, b in zip(before, after):
        assert np.array_equal(np.asarray(a), np.asarray(b))
    # And the tape carries the switch: no `town` key, no forcing.
    assert TA.device(jnp, TA.stack([_tape()])).town is None


# --------------------------------------------------------------- the engine

def test_prefix_table_is_cumulative_and_ordered():
    table = TI.prefix_table(SCHEDULE)
    assert table[3] == ["SMOOTHIE_SHOP"]
    assert table[6] == ["SMOOTHIE_SHOP", "BAKERY"]
    assert len(table[24]) == spec.MAX_SHOP_INSTANCES


def test_load_schedule_picks_the_entry_for_this_tape(tmp_path):
    path = tmp_path / "towns.json"
    path.write_text(json.dumps({"opponent_tape_9/": SCHEDULE, "default": []}))
    assert TI.load_schedule(path, "/a/b/opponent_tape_9/main.py") == SCHEDULE
    assert TI.load_schedule(path, "/a/b/opponent_tape_8/main.py") == []
    flat = tmp_path / "flat.json"
    flat.write_text(json.dumps(SCHEDULE))
    assert TI.load_schedule(flat, "anything") == SCHEDULE


def test_engine_town_is_pinned_and_the_hook_is_off_by_default():
    """The seam, end to end, in the real engine.

    `_end_of_day` is called through the module globals, so rebinding the name on
    the imported module is enough -- nothing in site-packages is edited. The
    wrapper runs the original first (weeds and the draw consume exactly the
    words they did) and only then overwrites `unlocked_shops`, so a pinned game
    differs from an unpinned one in the town and nothing else.
    """
    from kaggle_environments import make

    def town_of(seed):
        env = make("kaggriculture", configuration={"seed": seed})
        env.run(["pass", "pass"])
        return list(env.steps[-1][0].observation["town"]["unlocked_shops"])

    seed = 20260911
    TI.install(None)
    drawn = town_of(seed)
    assert len(drawn) == spec.MAX_SHOP_INSTANCES

    TI.install(SCHEDULE)
    pinned = town_of(seed)
    assert pinned == [name for _, name in SCHEDULE]
    assert pinned != drawn          # the pin is what changed it, not the seed

    # Unpinning restores the engine: the wrapper stays installed but inert.
    TI.install(None)
    assert town_of(seed) == drawn


def test_install_from_env_is_a_no_op_without_the_variable(monkeypatch):
    monkeypatch.delenv(TI.ENV_PATH, raising=False)
    assert TI.install_from_env() is None


def test_generator_flags_are_opt_in(tmp_path):
    """`--with-town` off must leave both generators emitting what they emitted.

    The package is the interesting one: it is what the engine execs, and a tape
    cut before the flag existed carries no `_TOWN` at all.
    """
    root = _ROOT
    replay = _replay(SCHEDULE)
    replay["info"] = {"TeamNames": ["Them", "OurTeam"], "EpisodeId": 7}
    for step in replay["steps"]:
        step[0]["observation"]["farms"] = [{"money": 1.0}, {"money": 2.0}]
        step[0]["action"] = step[1]["action"] = None
    path = tmp_path / "ep_7.json"
    path.write_text(json.dumps(replay))

    def cut(*flags):
        out = tmp_path / ("pkg" + "".join(flags).replace("-", ""))
        subprocess.run([sys.executable, os.path.join(root, "scripts", "tape_opponent.py"),
                        str(path), "--seat", "0", "--no-verify",
                        "-o", str(out) + ".tar.gz", "--out-dir", str(out), *flags],
                       check=True, capture_output=True)
        return TA.town_from_package(os.path.join(str(out), "main.py"))

    assert cut() == []
    assert cut("--with-town") == SCHEDULE
