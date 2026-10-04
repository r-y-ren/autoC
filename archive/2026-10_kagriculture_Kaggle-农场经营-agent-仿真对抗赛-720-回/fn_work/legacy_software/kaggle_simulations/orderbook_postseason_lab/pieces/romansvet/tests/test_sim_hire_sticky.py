"""The sim tape seat's HIRE-STICKY reflex (`sim.rollout.HIRE_STICKY`).

The engine drops a HIRE the tape's purse cannot pay for in silence and the tape
never retries it, so the recorded crew is short for the rest of the day and, by
the cash spiral that follows, for the rest of the game
(`docs/strategy/2026-09-14-tape-hire-fix.md`). `scripts/tape_opponent.py
--hire-sticky` repairs that in the engine seat; this is the same repair in the
simulator's tape seat, and these two tests are its two halves:

  * flag OFF, a tape that CARRIES the two new rows plays the frozen tape's game
    to the coin -- the rows are inert, which is what makes every ledger cut
    before this flag still comparable;
  * flag ON, the worst TOPB3 board (episode 108795516, source retention 0.00)
    ends day 1 on the roster the RECORDING had, not one hand short.
"""

import os
import sys

import numpy as np
import pytest

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
# The editable install writes the MAIN checkout's `src` into site-packages, so
# inside a git worktree a bare `import kagg3` reads the other tree.
sys.path.insert(0, os.path.join(_ROOT, "src"))

jnp = pytest.importorskip("jax.numpy")

from kagg3 import spec                                               # noqa: E402
from kagg3.es import tape_actions as TA                              # noqa: E402
from kagg3.sim import eod, rollout                                   # noqa: E402
from kagg3.sim.state import build_tables, initial_state              # noqa: E402

#: The board: episode 108795516 (Majkel1337), seed and seat from
#: `S/topledger3/boards.json` row 2, theta = `submission/theta.npy`'s
#: flow193_g100_hr, i.e. the TOPB3 ledger's own row.
EPISODE = 108795516
SEED = 1341060238
TAPE_SEAT = 1
PKG = os.path.join(_ROOT, "artifacts/panel_opp_town",
                   f"opponent_tape_{EPISODE}", "main.py")
THETA = os.path.join(_ROOT, "artifacts/kagg2_games/thetas/flow193_g100_hr.npy")

pytestmark = pytest.mark.skipif(not os.path.exists(PKG) or not os.path.exists(THETA),
                                reason="needs the TOPB3 tape package and B's theta")


def _tape(sticky_rows=True):
    frames = TA.tape_from_package(PKG)
    ta = TA.build(frames, EPISODE, TA.town_from_package(PKG) or None)
    if not sticky_rows:
        ta = ta._replace(src_hands=None, mlen=None)     # a tape cut before the flag
    return TA.device(jnp, TA.stack([ta])), frames


def _days(tape, sticky, n_days):
    """`n_days` days of the board; the state is returned before the last
    end-of-day, because `eod` wipes the roster every night."""
    from kagg3.core import policy as PO
    theta = np.load(THETA).astype(np.float32)
    if hasattr(PO, "pad"):
        theta = PO.pad(theta)
    thetas = jnp.asarray(np.stack([theta, theta]))
    words = jnp.asarray(np.stack([eod.host_stream(SEED, d)
                                  for d in range(spec.N_DAYS)]))
    hi_t, lo_t = eod.weed_threshold()
    tables = build_tables(jnp)
    turns = tuple(sorted(set(rollout.MARKET_TURNS) | set(tape.hours)))
    was = rollout.HIRE_STICKY
    rollout.HIRE_STICKY = sticky
    try:
        st = initial_state(jnp, None, None)
        for d in range(n_days):
            st = rollout.run_day(tables, st, jnp.int32(d), words[d],
                                 jnp.int32(hi_t), jnp.int32(lo_t), thetas,
                                 do_eod=d < n_days - 1, shop_crn=True,
                                 tape=tape, tape_ctl=jnp.asarray([TAPE_SEAT, 0],
                                                                 jnp.int32),
                                 tape_turns=turns)
    finally:
        rollout.HIRE_STICKY = was
    return st


def test_flag_off_is_the_frozen_tape_to_the_coin():
    """The two new rows are inert with the flag off.

    Same board, four days, once off a tape that carries `src_hands`/`mlen` and
    once off the same tape with both stripped (which is every `.npz` cut before
    this flag). Money, roster and shed all have to agree exactly -- if they did
    not, every ledger in `S/` would have to be re-cut before it could be
    compared with a new one.
    """
    with_rows, _ = _tape(sticky_rows=True)
    without, _ = _tape(sticky_rows=False)
    assert with_rows.src_hands is not None and without.src_hands is None
    a = _days(with_rows, sticky=False, n_days=4)
    b = _days(without, sticky=False, n_days=4)
    assert np.array_equal(np.asarray(a.money), np.asarray(b.money))
    assert np.array_equal(np.asarray(a.nhands), np.asarray(b.nhands))
    assert np.array_equal(np.asarray(a.shed), np.asarray(b.shed))


def test_flag_on_ends_day_one_on_the_recorded_roster():
    """The measurable half: the owed hire is re-issued the same day.

    Day 1 is where episode 108795516 first loses a hand -- step 24 submits 8
    HIREs and only 3 land, against 4 in the recording -- and everything after it
    is that hand's missing work. With the flag on the seat has to finish day 1
    on the source's own roster, and never above it.
    """
    tape, frames = _tape()
    src_day1 = max(len(frames[24 + h].get("hands") or []) for h in range(spec.TURNS_PER_DAY))
    off = int(np.asarray(_days(tape, sticky=False, n_days=2).nhands)[TAPE_SEAT])
    on = int(np.asarray(_days(tape, sticky=True, n_days=2).nhands)[TAPE_SEAT])
    assert off < src_day1, f"board no longer desyncs on day 1 (off {off}, src {src_day1})"
    assert on == src_day1, f"hire-sticky ended day 1 on {on}, source had {src_day1}"
