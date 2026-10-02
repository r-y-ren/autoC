"""`--pinned-fixed-seed`: a pinned rung is ONE game, weeds included.

A **pinned** rung is a `--tape-actions` tape cut `--with-town`. Its recorded
town schedule replaces the shop draw (`sim.eod.unlock_shop`), which is the
lottery worth +/-25k a game and the reason the rung is called pinned. It is not
the only thing the per-slot seed word feeds: `sim.eod.spawn_weeds` walks two
words of `eod.host_stream(seed, day)` per EMPTY unlocked tile, every day, for
both seats. So the shops are pinned and the weeds are not, and the same
candidate on the same pinned board scores differently under two generations'
seeds -- measured at spearman 0.985 on the pinned-only ranking of a 32-member
population over 16 pinned rungs, i.e. noise on 82 % of the fitness weight.

The engine's board is a draw in exactly the same way: on tape 105228357 the
sim returns 92,926 coins on the seed the paired engine leg happened to give it
(and that IS the engine's number, to the coin) and 92,870 on two other seeds.
There is no engine seed to match, either -- `eval_vs_baselines.seed_lists`
derives opponent `i`'s seed from `seed_base + SEED_STRIDE * (i + 1)`, where `i`
is the tape's POSITION in that leg's `--opponents` list, so the same tape sits
on a different board in every leg. What a pinned board has to be is *one* game,
not the engine's particular one, which is what `pinned_seed_word` gives it.

The rollout tests below play the real tape, so they pay one XLA compile.
"""
from __future__ import annotations

import os
import subprocess
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import policy as PO
from kagg3.es import tape_actions as TA
from kagg3.es.train import (Config, SlotCarry, Trainer, host_words,
                            pinned_seed_word)
from kagg3.sim import eod, rollout
from kagg3.sim.state import build_tables

# The ladder under test: two archetypes, three pinned tapes, two drawn ones.
N_ARCH, N_PIN, N_DRAWN = 2, 3, 2
N_RUNGS = N_ARCH + N_PIN + N_DRAWN
PIN = tuple(range(N_ARCH, N_ARCH + N_PIN))
NAMES = ([f"arch{i}" for i in range(N_ARCH)]
         + [f"tape_act_pin{i}" for i in range(N_PIN)]
         + [f"tape_act_drawn{i}" for i in range(N_DRAWN)])

#: A real pinned tape and two seeds it is known to separate: 4674845 is the
#: seed its row of the paired engine leg drew (and the sim returns that leg's
#: coins on it, 92,926 / 68,110), 975191099 is another leg's.
TAPE = "105228357"


def _artifacts():
    """Where the tapes live. A worktree under `<repo>/.claude/worktrees/<name>`
    checks out the tree but not the ignored artifact store, and shares the
    repo's -- so look there before giving up and skipping."""
    here = os.path.join(ROOT, "artifacts")
    if os.path.isdir(os.path.join(here, "tape_actions_town")):
        return here
    up = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "artifacts"))
    return up if os.path.isdir(os.path.join(up, "tape_actions_town")) else here


ART = _artifacts()
TAPE_DIR = os.path.join(ART, "tape_actions_town")
THETA = os.path.join(ART, "kagg2_games", "thetas", "flow135_g350_gpfwdfv.npy")
SEED_A, SEED_B = 4674845, 975191099


def _tr(pinned_fixed_seed=False, n_pool=1, rng_seed=0, **cfg):
    """A `Trainer` carrying only what the seed override reads.

    `__new__` rather than a real construction: a real one spends a minute
    probing archetypes for liveness, and what is under test is which word each
    slot gets, not what happens in the episode.
    """
    tr = Trainer.__new__(Trainer)
    tr.cfg = Config(episodes=2 * N_RUNGS, arch_frac=0.9,
                    pinned_fixed_seed=pinned_fixed_seed, **cfg)
    tr.pool = [None] * n_pool
    tr.archetypes = [None] * N_RUNGS
    tr.archetype_names = list(NAMES)
    tr.rung_weights = np.ones(N_RUNGS)
    tr.pinned_slots = PIN
    tr.slot_carry = SlotCarry() if tr.cfg.slot_rotation == "carry" else None
    tr.rng = np.random.default_rng(rng_seed)
    tr.t = 0
    return tr


def _slots():
    """One slot per rung, then one self-play slot. -> idx as `generation` builds it."""
    return np.concatenate([len(_tr().pool) + np.arange(N_RUNGS), [0]]).astype(np.int64)


# ------------------------------------------------------------- off is off

def test_off_leaves_every_word_exactly_where_the_draw_put_it():
    """The default is byte-identical: same seeds, same words, same coins.

    Both halves matter. The array one, because `pinned_seeds` is on the path of
    every generation and an unflagged run must hand `host_words` the identical
    integers it always did -- including on a ladder where every slot is pinned,
    which is the case the override would otherwise rewrite wholesale. And the
    rollout one, because the seed word is the ONLY channel the flag can move:
    the same word must still produce the same game to the coin.
    """
    assert Config().pinned_fixed_seed is False
    tr = _tr()
    idx = _slots()
    drawn = tr.rng.integers(0, 2 ** 31 - 1, len(idx))
    got = tr.pinned_seeds(drawn, idx)
    assert np.array_equal(got, np.asarray(drawn, np.int64))
    assert np.array_equal(host_words(got), host_words(drawn))
    # A ladder with nothing pinned is the same statement with the flag ON.
    on = _tr(pinned_fixed_seed=True)
    on.pinned_slots = ()
    assert np.array_equal(on.pinned_seeds(drawn, idx), np.asarray(drawn, np.int64))


# ------------------------------------------------ on: one board, one game

@pytest.fixture(scope="module")
def coins():
    """`(seed) -> (mine, theirs)` for the live theta on `TAPE`, seat-symmetric."""
    for p in (os.path.join(TAPE_DIR, f"{TAPE}.npz"), THETA):
        if not os.path.exists(p):
            pytest.skip(f"missing {p}")
    theta = np.load(THETA).astype(np.float32)
    if theta.shape != (PO.N_PARAMS,):
        pytest.skip(f"theta is {theta.shape}, this tree wants {PO.N_PARAMS}")
    tape = TA.load(os.path.join(TAPE_DIR, f"{TAPE}.npz"))
    assert tape.town is not None, f"{TAPE} carries no town -- not a pinned rung"
    stacked = TA.stack([tape])
    dev = TA.device(jnp, stacked)
    turns = tuple(sorted(set(rollout.MARKET_TURNS) | set(stacked.hours)))
    hi_t, lo_t = eod.weed_threshold()
    tables = build_tables(jnp)
    th = jnp.stack([jnp.asarray(theta), jnp.asarray(theta)])
    ctl = jnp.asarray(np.array([1, 0], np.int32))

    @jax.jit
    def play(words):
        money, _, _ = rollout.episode(tables, th, words, jnp.int32(hi_t),
                                      jnp.int32(lo_t), tape=dev, tape_ctl=ctl,
                                      tape_turns=turns)
        return money

    cache = {}

    def run(seed):
        if seed not in cache:
            w = jnp.asarray(np.stack([eod.host_stream(int(seed), d)
                                      for d in range(spec.N_DAYS)]))
            m = np.asarray(play(w))
            cache[seed] = (int(m[0]), int(m[1]))
        return cache[seed]

    return run


def test_on_a_pinned_rung_plays_one_game_whatever_the_generation_drew(coins):
    """Two generations, two draws, one board.

    The premise first: this tape's coins DO move between `SEED_A` and `SEED_B`
    with the flag off (92,926 vs 92,870 for the live theta -- 56 coins of pure
    weed walk, which is small per board and is the entire residual the pinned
    block's 82 % of the fitness weight was carrying). Then the flag: two
    trainers whose `self.rng` is seeded differently draw different words for
    every slot, and the same word for the pinned ones -- so the coins are equal,
    not merely close.
    """
    a, b = coins(SEED_A), coins(SEED_B)
    assert a != b, "premise gone: this tape no longer moves with the seed"

    idx = _slots()
    ta, tb = _tr(pinned_fixed_seed=True, rng_seed=1), _tr(pinned_fixed_seed=True,
                                                          rng_seed=2)
    sa = ta.pinned_seeds(ta.rng.integers(0, 2 ** 31 - 1, len(idx)), idx)
    sb = tb.pinned_seeds(tb.rng.integers(0, 2 ** 31 - 1, len(idx)), idx)
    for r in PIN:
        assert sa[r] == sb[r], "two generations put the pinned rung on two boards"
        assert coins(int(sa[r])) == coins(int(sb[r])), "pinned board moved"
    # ... and it is the tape's own word, not some slot's leftover.
    assert sa[PIN[0]] == pinned_seed_word(NAMES[PIN[0]])


def test_a_drawn_rung_and_self_play_still_take_the_generation_word():
    """The flag is narrow: only rungs whose shops are already pinned.

    A drawn tape has no town, so its board is a draw in the sim exactly as it
    is in the engine, and freezing it would turn a sampled opponent into a
    single memorised game. Self-play out of the pool is the same argument.
    """
    idx = _slots()
    ta, tb = _tr(pinned_fixed_seed=True, rng_seed=1), _tr(pinned_fixed_seed=True,
                                                          rng_seed=2)
    da = ta.rng.integers(0, 2 ** 31 - 1, len(idx))
    db = tb.rng.integers(0, 2 ** 31 - 1, len(idx))
    sa, sb = ta.pinned_seeds(da, idx), tb.pinned_seeds(db, idx)
    free = [i for i in range(len(idx)) if i not in PIN]
    assert free, "the fixture lost its unpinned slots"
    for i in free:
        assert sa[i] == da[i] and sb[i] == db[i], "an unpinned slot was frozen"
        assert sa[i] != sb[i], "two generations drew the same word"
    # The pinned ones did not merely happen to agree with the draw.
    assert not any(sa[r] == da[r] for r in PIN)


def test_the_fixed_word_is_the_same_number_in_every_process():
    """`hash()` is salted per process; this must not be.

    A resumed run, a second GPU in the same sweep and a local reproduction all
    have to put a pinned tape on the SAME board, or the flag buys determinism
    inside one process and loses it across the campaign.
    """
    names = [NAMES[r] for r in PIN] + ["tape_act_105228357"]
    mine = [pinned_seed_word(n) for n in names]
    assert all(0 <= w < 2 ** 31 - 1 for w in mine)
    assert len(set(mine)) == len(mine), "two tapes collided on one board"
    prog = ("import sys; sys.path.insert(0, %r);"
            "from kagg3.es.train import pinned_seed_word as p;"
            "print([p(n) for n in %r])" % (os.path.join(ROOT, "src"), names))
    outs = []
    for salt in ("0", "1", "random"):
        env = dict(os.environ, PYTHONHASHSEED=salt, JAX_PLATFORMS="cpu")
        outs.append(subprocess.run([sys.executable, "-c", prog], env=env,
                                   capture_output=True, text=True,
                                   check=True).stdout.strip())
    assert outs == [str(mine)] * 3, outs
