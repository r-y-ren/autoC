"""Pin the engine's town to a recorded schedule, from outside the engine.

Why
---
The end-of-day town unlock is the engine's only randomness that anybody plays
*for*.  `_end_of_day` keys `random.Random((seed * 1_000_003) ^ day)` and drains
it weeds-first -- one `random()` per EMPTY unlocked tile, player 0's board then
player 1's -- and only then calls `choice(sorted(SHOPS))`.  So which shop the
town gains is a function of how many tiles the two seats left empty that day,
not of the seed alone, and no amount of seeding reproduces a recorded town while
one of the seats is a different agent.

That matters because our opponents are *recordings*.  A tape replays a player
who planted strawberries because HIS town drew SMOOTHIE_SHOP; replayed under a
freshly drawn town it grows produce nobody buys, and we beat the ghost far more
easily than we beat the player (2026-09-11: 62 % against the tapes of the same
2100-band opponents we were losing to 3-in-13 live).  Pinning the town is one
half of closing that gap -- the other half is the tape's own reactivity.

The seam
--------
`_end_of_day` is a module-level function called through the module globals
(`kaggriculture.py:946`), so rebinding the name on the imported module is enough
and nothing under `vendor/` (or in site-packages) is edited.  The wrapper calls
the original -- weeds, plant/animal refresh, shed drop and the draw itself all
run exactly as they did, consuming exactly the words they did -- and then
*overwrites* `town["unlocked_shops"]` with the recorded prefix for the day that
is about to start.  Overwriting after the fact rather than intercepting the
draw is deliberate: the RNG cursor stays where the engine put it, so the weeds
of every later day are untouched and a pinned game differs from an unpinned one
in the town and nothing else.

Because the recorded list is written whole, it is authoritative in both
directions: a day the recording did not unlock on does not unlock here either,
and `MAX_SHOP_INSTANCES` is respected by construction (the recording obeyed it).

Opt-in
------
Off unless `KAGG3_TOWN_SCHEDULE` names a file.  `scripts/eval_vs_baselines.py`
calls `install_from_env()` once per game, before the game starts and before
`_vendored_imports` clears the `KAGG3_*` namespace; with the variable unset it
returns `None` and the engine is not touched at all.

The file is either

  * a JSON list of `[day, "SHOP_NAME"]` pairs -- what a
    `scripts/tape_opponent.py --with-town` package carries as `_TOWN`; or
  * a JSON object mapping a tape name to such a list, plus an optional
    `"default"` key.  The entry used is the first whose key appears in
    `KAGG3_TOWN_TAPE` (which the harness sets to the opponent path), else
    `"default"`.  That is what lets ONE evaluation run several tapes, each under
    its own recorded town.

`day` is the day the shop is first visible, i.e. the engine's `next_day` -- the
same convention `es.tape_actions.town_array` uses.
"""

from __future__ import annotations

import json
import os

#: Names a JSON schedule file; unset (or empty) means the engine is untouched.
ENV_PATH = "KAGG3_TOWN_SCHEDULE"

#: Selects an entry from a multi-tape schedule file. The harness sets it to the
#: opponent it is about to play; matching is "key is a substring of the value",
#: so an episode id is enough.
ENV_TAPE = "KAGG3_TOWN_TAPE"

#: Set on the module once wrapped, so a second install is a no-op rather than a
#: second layer of wrapper (workers play many games in one process).
_MARK = "_kagg3_town_wrapped"

_MODULE = "kaggle_environments.envs.kaggriculture.kaggriculture"

#: The live schedule: `{day: [shops visible from that day]}` prefix table, or
#: `None` while nothing is pinned. Rebound per game by `install`.
_PREFIX: dict | None = None


def load_schedule(path, tape=None):
    """Read the schedule file and pick the entry for `tape`.

    Returns `[[day, "SHOP_NAME"], ...]`, or `None` when the file has nothing for
    this tape -- which leaves the engine drawing its own shops, the behaviour a
    run without the variable gets.
    """
    with open(path) as fh:
        blob = json.load(fh)
    if isinstance(blob, list):
        return [list(row) for row in blob]
    if not isinstance(blob, dict):
        raise ValueError(f"{path}: expected a list of [day, shop] or an object")
    if tape:
        for key, rows in blob.items():
            if key != "default" and key in str(tape):
                return [list(row) for row in rows]
    rows = blob.get("default")
    return None if rows is None else [list(row) for row in rows]


def prefix_table(schedule):
    """`[[day, shop], ...]` -> `{day: unlocked_shops as of that day}`.

    The engine's `unlocked_shops` is cumulative and ordered, and repeats are
    meaningful (shops are drawn with replacement and each copy consumes), so the
    prefix is built by appending in the recording's own order.
    """
    out, acc = {}, []
    for day, name in sorted(schedule, key=lambda r: int(r[0])):
        acc = acc + [str(name)]
        out[int(day)] = list(acc)
    return out


def install(schedule):
    """Pin `schedule` for every game this process plays from now on.

    Idempotent in the wrapper (it is installed once) and rebindable in the
    schedule (the module-level `_PREFIX` is what the wrapper reads), so a worker
    can switch tapes between games. `install(None)` unpins.
    """
    global _PREFIX
    _PREFIX = None if schedule is None else prefix_table(schedule)
    if _PREFIX is None:
        return None

    import importlib
    mod = importlib.import_module(_MODULE)
    if not getattr(mod, _MARK, False):
        original = mod._end_of_day

        def _end_of_day(state, env, day, _original=original):
            _original(state, env, day)
            table = _PREFIX
            if table is None:
                return
            # `day + 1` is the day the refresh has just rolled into, and the day
            # `town_array` / `_TOWN` index by. Below the first unlock the town is
            # empty; past the last recorded one it holds the final list.
            nd = day + 1
            want = table.get(nd)
            if want is None:
                keys = [d for d in table if d <= nd]
                want = table[max(keys)] if keys else []
            state[0].observation.town["unlocked_shops"] = list(want)

        mod._end_of_day = _end_of_day
        setattr(mod, _MARK, True)
    return _PREFIX


def install_from_env(tape=None):
    """`install` driven by `KAGG3_TOWN_SCHEDULE` / `KAGG3_TOWN_TAPE`.

    Returns the pinned schedule table, or `None` when nothing is pinned -- which
    is the default and leaves the engine exactly as it ships.
    """
    path = os.environ.get(ENV_PATH)
    if not path:
        # Still unpin: a worker that pinned a previous game must not leak it.
        if _PREFIX is not None:
            install(None)
        return None
    tape = tape if tape is not None else os.environ.get(ENV_TAPE)
    return install(load_schedule(path, tape))
