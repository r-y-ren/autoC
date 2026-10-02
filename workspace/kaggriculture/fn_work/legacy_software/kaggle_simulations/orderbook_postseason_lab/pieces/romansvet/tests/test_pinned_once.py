"""`--pinned-once`: one episode per pinned board, weight in the fitness.

A **pinned** rung is a `--tape-actions` tape cut `--with-town`. Its recorded
town schedule fixes the shop draws, so the rung is one deterministic board: the
sim reproduces the engine and the live game to the coin, and both seats return
the same numbers for the same theta. The only per-episode variation left is the
candidate's own perturbation -- which the pair does not resolve either, since a
candidate plays its own theta on both seats.

The allocator did not know that. Reconstructed from the live 384-episode arms'
launcher (86 pinned rungs at weight 2 + 15 drawn at weight 1 + 4 zero-weight
archetypes, `--arch-frac 0.9`), 173 of the 192 pairs went to the ladder and each
pinned rung took about two of them -- four episodes of the same game per
candidate, so **75% of the pinned budget was replay of identical outcomes**.

What is pinned here:

* off is off: the default allocation is the one the untouched module-level
  allocator produces, generation after generation, and `shaped_advantage`
  takes the `mean` it always took;
* on, every pinned rung gets exactly one episode and the residual budget
  (`--episodes` minus the pinned count) is divided among the drawn tapes, the
  archetypes and self-play by the same carry logic as before;
* the seat alternates, so the mirroring a pair used to do inside a generation
  happens across two;
* the weight scales the *board's* contribution, not its replay count: one
  episode at weight `2 * w` is arithmetically the four identical episodes a
  weight-2 rung used to buy;
* `--episodes` below the pinned count warns rather than truncating the block.

Arithmetic only -- no engine, no rollouts.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import jax.numpy as jnp
import numpy as np
import train as T

from kagg3.es.train import (EPISODES_PER_PAIR, Config, SlotCarry, Trainer,
                            arch_pairs,
                            opponent_slots, shaped_advantage)

# ---------------------------------------------------------- the flow151 arm
#: The ladder the live arms train on, reconstructed from their launcher: four
#: archetypes at weight 0 (yardstick only), then 86 pinned tapes at weight 2,
#: then 15 drawn tapes at weight 1. `--episodes 384`, `--arch-frac 0.9`,
#: `--slot-rotation carry`.
N_ARCH, N_PIN, N_DRAWN = 4, 86, 15
N_RUNGS = N_ARCH + N_PIN + N_DRAWN
EPISODES, ARCH_FRAC = 384, 0.9
#: Ladder indices. The pinned block is contiguous only because that is how the
#: launcher lists it; nothing below assumes it.
PIN = tuple(range(N_ARCH, N_ARCH + N_PIN))
DRAWN = tuple(range(N_ARCH + N_PIN, N_RUNGS))
WEIGHTS = np.array([0.0] * N_ARCH + [2.0] * N_PIN + [1.0] * N_DRAWN)


def _tr(pinned_once=False, pinned=PIN, weights=WEIGHTS, n_pool=1,
        episodes=EPISODES, **cfg):
    """A `Trainer` carrying only what the allocator and the objective read.

    `__new__` rather than a real construction: a real one spends a minute
    probing 105 archetypes for liveness, and what is under test is which
    episode each rung gets, not what happens in it.
    """
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(episodes=episodes, arch_frac=ARCH_FRAC,
                    pinned_once=pinned_once, **cfg)
    tr.pool = [None] * n_pool
    tr.archetypes = [None] * len(weights)
    tr.archetype_names = ([f"arch{i}" for i in range(N_ARCH)]
                          + [f"tape_act_pin{i}" for i in range(N_PIN)]
                          + [f"tape_act_drawn{i}" for i in range(N_DRAWN)])
    tr.rung_weights = np.asarray(weights, float)
    tr.pinned_slots = tuple(pinned)
    tr.slot_carry = SlotCarry() if tr.cfg.slot_rotation == "carry" else None
    tr.t = 0
    return tr


def _reference_rows(gens, n_pool=1):
    """Today's opponent rows, from the module functions the change did not
    touch -- `SlotCarry`, `arch_pairs`, `opponent_slots`. This is the same
    reconstruction `scratchpad/rungcov/probe.py` used to measure the defect."""
    n_pairs = EPISODES // 2
    carry = SlotCarry()
    k = arch_pairs(n_pairs, N_RUNGS, ARCH_FRAC)
    rows = []
    for _ in range(gens):
        take = carry.take(k, WEIGHTS)
        rows.append(opponent_slots(n_pairs, n_pool, N_RUNGS, ARCH_FRAC,
                                   WEIGHTS, take=take))
    return rows


# ------------------------------------------------------------- off is off

def test_the_flag_defaults_to_off():
    assert Config().pinned_once is False
    assert _tr().pinned_block() is None, "no flag, no pinned block"
    # And a run WITH the flag but no `--with-town` tape has nothing to pin.
    assert _tr(pinned_once=True, pinned=()).pinned_block() is None


def test_the_default_allocation_is_the_one_the_arms_run_today():
    """Byte-identical, five generations deep, on the flow151 configuration.

    The reference is built from the untouched module-level allocator, so this
    fails if `opponent_index`'s new `drop` argument leaked into the unflagged
    path -- including through the carry credit, which is why it runs five
    generations rather than one.
    """
    tr = _tr()
    n_pairs = EPISODES // 2
    for want in _reference_rows(5):
        got = tr.opponent_index(n_pairs)
        assert np.array_equal(got, want)
        # ... and so is what the gen line reads off it.
        eps = tr.rung_episodes(n_pairs, got)
        assert sum(eps.values()) == EPISODES
        assert eps["_pool"] + eps["_theta"] == 2 * (n_pairs - 173)

    # The defect itself, so the fix has something to be a fix of: a weight-2
    # pinned rung takes ~2 pairs = ~4 episodes of ONE deterministic board.
    eps = tr.rung_episodes(n_pairs, tr.opponent_index(n_pairs))
    pinned = np.array([eps[tr.archetype_names[i]] for i in PIN])
    assert pinned.min() >= 2 and pinned.mean() > 3.5
    # 86 boards, one distinct outcome each, and this many episodes spent on
    # them: everything past the first episode of each is replay.
    assert 1 - N_PIN / pinned.sum() > 0.7, "the 75% this flag removes"


def test_shaped_advantage_without_weights_is_the_mean_it_always_took():
    cfg = Config()
    mine = jnp.asarray(1e3 * np.arange(24, dtype=np.float32).reshape(4, 6))
    theirs = jnp.asarray(1e3 * np.arange(24, 0, -1, dtype=np.float32).reshape(4, 6))
    a = shaped_advantage(mine, theirs, cfg)
    b = shaped_advantage(mine, theirs, cfg, None, None, None)
    assert np.array_equal(np.asarray(a), np.asarray(b))


# ------------------------------------------------------------- on: the split

def test_each_pinned_rung_gets_exactly_one_episode_and_the_rest_is_carried():
    """The headline. 86 pinned boards, one episode each; 384 - 86 = 298
    episodes left, allocated as today among the drawn tapes, the four
    archetypes and self-play."""
    tr = _tr(pinned_once=True)
    pin = tr.pinned_block()
    assert pin == PIN

    n_pairs = (EPISODES - len(pin)) // 2
    assert n_pairs == 149
    idx = np.concatenate([len(tr.pool) + np.asarray(pin),
                          tr.opponent_index(n_pairs, drop=pin)])
    keep = tr.pinned_keep(pin, n_pairs)
    eps = tr.rung_episodes(len(pin) + n_pairs, idx, keep)

    assert len(keep) == EPISODES == sum(eps.values())
    for i in PIN:
        assert eps[tr.archetype_names[i]] == 1, tr.archetype_names[i]
    carried = sum(v for k, v in eps.items()
                  if k not in {tr.archetype_names[i] for i in PIN})
    assert carried == EPISODES - N_PIN == 298
    # The freed budget went to the rungs that still need repeated boards, not
    # back to the pinned ones: 15 drawn tapes now take ~18 episodes each where
    # they took ~2, and the zero-weight archetypes still take none.
    drawn = np.array([eps[tr.archetype_names[i]] for i in DRAWN])
    assert drawn.min() >= 16 and drawn.sum() == 2 * arch_pairs(
        n_pairs, N_RUNGS, ARCH_FRAC)
    assert all(eps[tr.archetype_names[i]] == 0 for i in range(N_ARCH))


def test_the_pinned_seat_alternates_across_generations():
    """One episode cannot mirror a board inside a generation, so the mirror
    moves across generations -- and the `+ i` stagger keeps each generation's
    block half on each seat instead of swinging as one."""
    tr = _tr(pinned_once=True)
    seats = []
    for t in range(4):
        tr.t = t
        seats.append(tr.pinned_seats(N_PIN))
    for a, b in zip(seats, seats[1:]):
        assert not np.array_equal(a, b), "the seat has to move"
        assert np.array_equal(a, 1 - b), "and move for every board"
    assert np.array_equal(seats[0], seats[2]), "period 2"
    # Half the block on each seat in any one generation.
    assert abs(int(seats[0].sum()) - N_PIN // 2) <= 1
    # The block's episodes really are the seats it named.
    keep = tr.pinned_keep(PIN, 4)
    assert np.array_equal(keep[:N_PIN] % 2, seats[-1])
    assert np.array_equal(keep[:N_PIN] // 2, np.arange(N_PIN))
    assert np.array_equal(keep[N_PIN:], 2 * N_PIN + np.arange(8))


# ------------------------------------------------- on: the weight moves house

def test_the_weight_scales_the_board_not_its_replay_count():
    """Same board, same theta => same coins, so the four episodes a weight-2
    pinned rung used to buy were four copies of one number. One episode at
    weight `EPISODES_PER_PAIR * 2` contributes exactly what they did.

    Four candidates, because the objective is rank-normalised and two would
    make every reordering the same reordering.
    """
    cfg = Config()
    # Column 0 is the pinned board (deterministic: one value per candidate);
    # columns 1-2 are ordinary mirrored episodes.
    pin_mine = np.array([130e3, 118e3, 126e3, 121e3], np.float32)
    pin_theirs = np.array([120e3, 140e3, 106e3, 133e3], np.float32)
    rest_mine = 1e3 * np.array([[100., 102], [118., 116],
                                [96., 98], [122., 120]], np.float32)
    rest_theirs = 1e3 * np.array([[152., 106], [160., 90],
                                  [106., 148], [134., 122]], np.float32)

    once = shaped_advantage(
        jnp.asarray(np.column_stack([pin_mine, rest_mine])),
        jnp.asarray(np.column_stack([pin_theirs, rest_theirs])),
        cfg, None, None,
        np.array([EPISODES_PER_PAIR * 2.0, 1.0, 1.0], np.float32))

    # The same generation the old way: the pinned board replayed four times.
    four = shaped_advantage(
        jnp.asarray(np.column_stack([np.tile(pin_mine[:, None], 4), rest_mine])),
        jnp.asarray(np.column_stack([np.tile(pin_theirs[:, None], 4), rest_theirs])),
        cfg)
    assert np.allclose(np.asarray(once), np.asarray(four), atol=1e-6)

    # And the trainer builds exactly that weight vector: 2 episodes per pair
    # times the rung weight on the block, 1.0 on everything else.
    tr = _tr(pinned_once=True)
    w = tr.pinned_weights(PIN, EPISODES)
    assert np.array_equal(w[:N_PIN], np.full(N_PIN, 4.0, np.float32))
    assert np.array_equal(w[N_PIN:], np.ones(EPISODES - N_PIN, np.float32))


# ------------------------------------------------------------ the startup line

def test_the_startup_line_states_the_budget_and_warns_when_it_is_short():
    assert T.pinned_once_notes(384, 86, 105)[0] == (
        "pinned-once: 86 pinned rungs x 1 episode + 298 episodes carried")
    assert len(T.pinned_once_notes(384, 86, 105)) == 1, "no warning at 384"

    # --episodes below the pinned count: warned, never truncated.
    short = T.pinned_once_notes(64, 86, 105)
    assert short[0].startswith("pinned-once: 86 pinned rungs x 1 episode + 0")
    assert len(short) == 2 and short[1].startswith("WARNING:")
    assert "--episodes 64" in short[1] and "plays 88" in short[1]

    # Thin but legal, and the inert case.
    assert T.pinned_once_notes(120, 86, 105)[1].startswith("WARNING:")
    assert T.pinned_once_notes(384, 0, 105) == [
        "WARNING: --pinned-once but no rung on this ladder is pinned: none of "
        "the --tape-actions tapes carries a `town` key (cut them with "
        "--with-town). The flag is inert."]
