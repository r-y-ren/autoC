"""ACTIONRL2 -- the residual action head: a tiny MLP over the dawn features.

One module, three consumers, and they must agree to the bit:

* the **file agent** inside the Kaggle package, which has numpy and no JAX and
  calls `numpy_fn(load(path))` to get the callable `plan.RESIDUAL_FN` wants;
* the **sim rollout** under `jit`, which calls the same `forward` with
  `xp = jax.numpy` and samples from the logits with a key;
* the **trainer** (`S/actionrl/ppo.py`), which differentiates `forward`.

So every function here is written against an `xp` module (`numpy` or
`jax.numpy`) and touches no library-specific API.  The parameters are a flat
dict of float32 arrays, which is both a valid JAX pytree and an `.npz`.

TWO LAYOUTS [ACTIONRL11].  `HEAD_LAYOUT` (env `KAGG3_HEAD_LAYOUT`) picks which
one `init_params` and `noop_override` build; everything else INFERS the layout
from the array it is handed (`b3`/`logits` width, `acts` width), so a v1 head
and a wide head can live in one process and `load()` needs no argument:

    v1   (default, the SHIPPED head_940 -- byte-identical to what shipped)
      slot  0..4   d_plant[crop]    9 actions  ->  -4 .. +4   (day >= 1 only)
      slot  5..7   d_animal[kind]   5 actions  ->  -2 .. +2   (GOOSE, COW, SHEEP)
      slot  8      d_hire           5 actions  ->  -2 .. +2
      slot  9..17  hold_num[prod]   3 actions  ->  x0, x0.5, x1 of the gene's hold
      18 slots, 92 logits

    wide (ACTIONRL11 -- the WIDE-ASK head, ENGTAIL/VOLUMEHI/OPSCENSUS)
      slot  0..4   d_plant[crop]   13 actions  ->  -6 .. +6
      slot  5..7   d_animal[kind]   5 actions  ->  -2 .. +2
      slot  8      d_hire           9 actions  ->  -4 .. +4
      slot  9      ask_fill         5 actions  ->  keep / 25 / 50 / 75 / 100 %
                                                   of `n_free` as a FLOOR on the
                                                   day's plant ask (d >= 10)
      slot 10      seed_buy         4 actions  ->  keep / +1 / +2 / +4 units on
                                                   the day's seed want
      slot 11..19  hold_num[prod]   3 actions
      20 slots, 125 logits

The wide layout exists because the high-band tail is -11.6k VOLUME / -11.3k
PRICE, all d10-19, and the cause is the Macro plant ASK: `n_free` is 26-38
plantable tiles and `macro.plant_target` asks for 0-9 (`brain.py:1061-1094`,
`n_dev = _qfloor(dev_frac * n_free)`).  A +-4 tile nudge cannot close a 20-tile
gap, and the two things that fund the gap -- the crew and the seed -- were not
in the action space at all.

Both layouts carry a scalar VALUE head (`wv`, `bv`) off the same trunk -- the
per-dawn baseline GAE needs so the advantage is not one constant per episode.
`wv`/`bv` are zero at init and never touch the logits, so the value head is
invisible to the file agent and to the identity contract below; `numpy_fn`
does not even evaluate it.

The head is a RESIDUAL: `init_params` puts `ZERO_BIAS` on the no-op action of
every slot and zeros the last layer, so a fresh head is the frozen planner to
the coin and PPO has to earn every departure from it.  That is the same
contract `MELON_PLATE_TILES = 0` has, and it holds in BOTH layouts: `ask_fill`
and `seed_buy` have "keep" as their no-op, and `plan._residual_override` turns
"keep" into the OFF program, not into a zero-sized fill.
"""
from __future__ import annotations

import os

import numpy as np

#: Feature width `plan._residual_features` emits.  A head trained against a
#: different width is a different head; `forward` asserts it.
N_FEAT = 64

#: Hidden width, both layers (ACTIONRL1: 2 x 64 ~ 6 k params).
N_HIDDEN = 64

#: Logit the no-op action carries at init.  Large enough that a fresh head is
#: the planner on ~98 % of dawn-slots, small enough that the entropy bonus can
#: still move it.
ZERO_BIAS = 4.0

#: `seed_buy` action -> extra units asked on the day's seed want.  Coarse and
#: super-linear on purpose: the seed shortfall the ask gap opens is a handful
#: of units a crop, and a uniform 1/2/4 ladder covers it in three bits.
SEED_STEPS = (0, 1, 2, 4)

#: `ask_fill` action -> quarters of `n_free` the day's plant ask is FLOORED at.
#: The denominator lives in `plan.RESIDUAL_ASK_STEPS` too; both must agree.
ASK_STEPS = 4


# ------------------------------------------------------------------ layouts

class Layout(tuple):
    """`(name, SLOTS, N_ACT, N_LOGIT, OFFSET, NOOP)` -- a plain value object.

    A tuple subclass rather than a NamedTuple so it hashes and compares by
    value with no import beyond numpy, and every table is derived ONCE at
    module import: `slot_logits` reads `OFFSET` inside a per-slot loop that the
    file agent runs on every dawn, and a property that recomputed a `cumsum`
    there would pay for it 600 times a game.
    """

    __slots__ = ()

    def __new__(cls, name, slots):
        slots = tuple(slots)
        n_act = tuple(n for _, n, _ in slots)
        return super().__new__(cls, (
            name, slots, n_act, int(sum(n_act)),
            tuple(int(x) for x in np.cumsum((0,) + n_act[:-1])),
            tuple(z for _, _, z in slots)))

    name = property(lambda self: self[0])
    SLOTS = property(lambda self: self[1])
    N_ACT = property(lambda self: self[2])
    N_LOGIT = property(lambda self: self[3])
    OFFSET = property(lambda self: self[4])
    NOOP = property(lambda self: self[5])
    N_SLOT = property(lambda self: len(self[1]))
    wide = property(lambda self: self[0] == "wide")


#: (name, n_actions, no-op action index) per slot, in wire order.
V1 = Layout("v1",
            tuple((f"d_plant{c}", 9, 4) for c in range(5))
            + tuple((f"d_animal{a}", 5, 2) for a in range(3))
            + (("d_hire", 5, 2),)
            + tuple((f"hold{p}", 3, 2) for p in range(9)))

WIDE = Layout("wide",
              tuple((f"d_plant{c}", 13, 6) for c in range(5))
              + tuple((f"d_animal{a}", 5, 2) for a in range(3))
              + (("d_hire", 9, 4), ("ask_fill", 5, 0), ("seed_buy", 4, 0))
              + tuple((f"hold{p}", 3, 2) for p in range(9)))

LAYOUTS = {"v1": V1, "wide": WIDE}

#: Which layout `init_params`/`noop_override` build.  "v1" by default, so
#: `head_940.npz` and the shipped package are byte-identical to what shipped.
HEAD_LAYOUT = os.environ.get("KAGG3_HEAD_LAYOUT", "v1")
if HEAD_LAYOUT not in LAYOUTS:
    raise ValueError(f"KAGG3_HEAD_LAYOUT={HEAD_LAYOUT!r} not in {sorted(LAYOUTS)}")
LAYOUT = LAYOUTS[HEAD_LAYOUT]

#: Module-level aliases, so every consumer that reads `head.N_SLOT` (ppo.py's
#: `act_hist` column block) follows the env switch without an edit.
SLOTS = LAYOUT.SLOTS
N_SLOT = LAYOUT.N_SLOT
N_ACT = LAYOUT.N_ACT
N_LOGIT = LAYOUT.N_LOGIT
OFFSET = LAYOUT.OFFSET
NOOP = LAYOUT.NOOP

#: `_layout` code written into the npz, so a checkpoint names its own layout
#: instead of being identified by a width.  Legacy heads have no such field and
#: fall back to the width, which is unique (92 vs 125).
_LAYOUT_KEY = "_layout"
_LAYOUT_CODE = {"v1": 0.0, "wide": 1.0}
_CODE_LAYOUT = {0: V1, 1: WIDE}
_BY_LOGIT = {lay.N_LOGIT: lay for lay in LAYOUTS.values()}
_BY_SLOT = {lay.N_SLOT: lay for lay in LAYOUTS.values()}


def layout_of(params) -> Layout:
    """The layout a parameter dict belongs to -- its `_layout` field if it has
    one, else its `b3` width, which is unique across layouts."""
    code = params.get(_LAYOUT_KEY)
    if code is not None:
        try:
            return _CODE_LAYOUT[int(np.asarray(code).reshape(-1)[0])]
        except Exception:                # a traced leaf has no concrete value
            pass
    # `.shape` and not `np.asarray(...).shape`: `jax_fn` resolves the layout
    # INSIDE a `jit` trace, where `b3` is a tracer and any conversion to numpy
    # is an error.  The width is static either way.
    return _BY_LOGIT[int(params["b3"].shape[-1])]


def _lay_logits(logits, lay=None) -> Layout:
    """Layout of a flat logit vector -- static in JAX (`shape`, not a value)."""
    return lay if lay is not None else _BY_LOGIT[int(logits.shape[-1])]


def _lay_acts(acts, lay=None) -> Layout:
    return lay if lay is not None else _BY_SLOT[int(acts.shape[-1])]


# ---------------------------------------------------------------- parameters

def init_params(seed: int = 0, n_feat: int = N_FEAT, hidden: int = N_HIDDEN,
                lay: Layout = None):
    """A near-identity residual head.

    `w3` is exactly zero and `b3` is `ZERO_BIAS` on each slot's no-op, so the
    first rollout is the frozen planner's own plan on every dawn -- the PPO
    baseline is then the shipped agent and the advantage is a true residual.
    """
    lay = LAYOUT if lay is None else lay
    rng = np.random.default_rng(seed)
    b3 = np.zeros(lay.N_LOGIT, np.float32)
    for s in range(lay.N_SLOT):
        b3[lay.OFFSET[s] + lay.NOOP[s]] = ZERO_BIAS
    return {
        "w1": (rng.normal(size=(n_feat, hidden)) / np.sqrt(n_feat)).astype(np.float32),
        "b1": np.zeros(hidden, np.float32),
        "w2": (rng.normal(size=(hidden, hidden)) / np.sqrt(hidden)).astype(np.float32),
        "b2": np.zeros(hidden, np.float32),
        "w3": np.zeros((hidden, lay.N_LOGIT), np.float32),
        "b3": b3,
        # The VALUE head rides the same trunk (`wv`, `bv` -> scalar). Zero at
        # init, so the first update's GAE is exactly the old constant
        # per-episode advantage and the identity contract above is untouched:
        # the value head cannot reach the logits, only the advantage.
        "wv": np.zeros((hidden, 1), np.float32),
        "bv": np.zeros(1, np.float32),
    }


def save(path, params, **state):
    """Write the npz, with the layout named in `_layout`.

    `_layout` is written but never returned by `load` -- the trainer's Adam
    walks `jax.tree_util.tree_map` over EVERY leaf of the params dict, so a
    bookkeeping leaf inside it would be differentiated and stepped like a
    weight.  The file names the layout; the pytree stays weights only.
    """
    out = {k: np.asarray(v, np.float32) for k, v in params.items()
           if k != _LAYOUT_KEY}
    out[_LAYOUT_KEY] = np.asarray(
        [_LAYOUT_CODE[layout_of(params).name]], np.float32)
    out.update({"_" + k: np.asarray([v], np.float32)
                for k, v in state.items()})
    np.savez(path, **out)


def load(path):
    """The params dict, layout resolved automatically and `_layout` stripped.

    A head saved before `_layout` existed (`head_940.npz`) loads as v1 by its
    92-wide `b3`, which is the layout it was trained in.
    """
    with np.load(path) as z:
        raw = {k: np.asarray(z[k], np.float32) for k in z.files}
    layout_of(raw)                      # raises on an unknown width/code
    raw = {k: v for k, v in raw.items() if not k.startswith("_")}
    return raw


def n_params(params) -> int:
    return int(sum(np.asarray(v).size for v in params.values()
                   if not isinstance(v, str)))


# ------------------------------------------------------------------ forward

def trunk(xp, params, feats):
    """float32[..., N_HIDDEN]: the shared body of the policy and value heads."""
    h = xp.tanh(feats @ params["w1"] + params["b1"])
    return xp.tanh(h @ params["w2"] + params["b2"])


def forward(xp, params, feats):
    """float32[N_LOGIT]: the flat logits for one dawn.

    `feats` is float32[N_FEAT] (or [..., N_FEAT]; the matmuls broadcast).
    """
    h = trunk(xp, params, feats)
    logits = h @ params["w3"] + params["b3"]
    return _fixes_logits(xp, params, h, logits)


def _fixes_logits(xp, params, hidden, logits):
    """Apply an optional 25-gene state-conditioned plant-bin-8 adapter."""
    if "fixes_coeff" not in params:
        return logits
    pcs = (hidden - params["fixes_pc_mean"]) @ params["fixes_pc_components"].T
    basis = xp.concatenate([xp.ones(pcs.shape[:-1] + (1,), pcs.dtype), pcs], -1)
    delta = basis @ params["fixes_coeff"].T
    scatter = np.zeros((5, V1.N_LOGIT), np.float32)
    for slot in range(5):
        scatter[slot, V1.OFFSET[slot] + 8] = 1.0
    return logits + delta @ xp.asarray(scatter)


def value(xp, params, feats):
    """float32[...]: the per-dawn state value V(s), one scalar per dawn.

    Heads saved before the value head existed have no `wv`/`bv`; they read as
    V = 0, which is what a policy-only head's baseline was.
    """
    if "wv" not in params:
        return xp.zeros(xp.shape(feats)[:-1], xp.float32)
    return (trunk(xp, params, feats) @ params["wv"] + params["bv"])[..., 0]


def forward_value(xp, params, feats):
    """`(logits, V)` off ONE trunk pass -- what the PPO loss differentiates."""
    h = trunk(xp, params, feats)
    logits = _fixes_logits(xp, params, h, h @ params["w3"] + params["b3"])
    return logits, (h @ params["wv"] + params["bv"])[..., 0]


def slot_logits(logits, s: int, lay: Layout = None):
    """The `s`-th slot's logits out of the flat vector (static slicing)."""
    lay = _lay_logits(logits, lay)
    return logits[..., lay.OFFSET[s]:lay.OFFSET[s] + lay.N_ACT[s]]


def log_softmax(xp, z):
    z = z - xp.max(z, axis=-1, keepdims=True)
    return z - xp.log(xp.sum(xp.exp(z), axis=-1, keepdims=True))


def logp_entropy(xp, logits, acts, lay: Layout = None):
    """`(sum_s log pi(a_s), sum_s H_s)` -- the joint log-prob of the taken
    action and the policy entropy, both summed over the layout's slots.
    """
    lay = _lay_logits(logits, lay)
    lp = xp.zeros(logits.shape[:-1], logits.dtype)
    ent = xp.zeros(logits.shape[:-1], logits.dtype)
    for s in range(lay.N_SLOT):
        ls = log_softmax(xp, slot_logits(logits, s, lay))
        a = acts[..., s]
        lp = lp + xp.take_along_axis(ls, a[..., None], axis=-1)[..., 0]
        ent = ent - xp.sum(xp.exp(ls) * ls, axis=-1)
    return lp, ent


def greedy_acts(xp, logits, lay: Layout = None):
    """int32[N_SLOT]: the argmax action per slot -- what the file agent flies."""
    lay = _lay_logits(logits, lay)
    return xp.stack([xp.argmax(slot_logits(logits, s, lay), axis=-1)
                     for s in range(lay.N_SLOT)], axis=-1).astype(xp.int32)


def sample_acts(jnp, jrandom, key, logits, lay: Layout = None):
    """int32[..., N_SLOT] sampled per slot.  JAX only (training rollout)."""
    lay = _lay_logits(logits, lay)
    keys = jrandom.split(key, lay.N_SLOT)
    return jnp.stack(
        [jrandom.categorical(keys[s], slot_logits(logits, s, lay), axis=-1)
         for s in range(lay.N_SLOT)], axis=-1).astype(jnp.int32)


# ------------------------------------------------------------------- decode

def decode(xp, acts, lay: Layout = None):
    """The override dict `plan.RESIDUAL_FN` must return.

    Every value is already inside the clamp `plan._residual_override` asserts
    again -- the planner does not trust this module, because a half-trained
    head writing a negative `plant_target` would be a silent invariant break
    rather than an error (ACTIONRL1 section 1: there is no plan validator).

    The v1 dict carries FOUR keys and the wide dict carries six.  The two extra
    keys are the switch `plan._residual_override` reads: it tests `"ask_fill"
    in o` with a PYTHON `in`, so under v1 the wide block does not exist in the
    traced expression at all and a v1 head decodes byte for byte.
    """
    lay = _lay_acts(acts, lay)
    a = acts.astype(xp.int32)
    if not lay.wide:
        return {
            "d_plant": (a[..., 0:5] - 4).astype(xp.int32),
            "d_animal": (a[..., 5:8] - 2).astype(xp.int32),
            "d_hire": (a[..., 8] - 2).astype(xp.int32),
            "hold_num": a[..., 9:18].astype(xp.int32),
        }
    steps = xp.asarray(SEED_STEPS, xp.int32)
    return {
        "d_plant": (a[..., 0:5] - 6).astype(xp.int32),
        "d_animal": (a[..., 5:8] - 2).astype(xp.int32),
        "d_hire": (a[..., 8] - 4).astype(xp.int32),
        # `ask_fill` is the action INDEX (0 = keep, k = k quarters of n_free);
        # `plan` owns the arithmetic because only `plan` knows `n_free`.
        "ask_fill": a[..., 9].astype(xp.int32),
        # `seed_buy` is already in UNITS -- the ladder is this module's.
        "seed_buy": xp.take(steps, a[..., 10]).astype(xp.int32),
        "hold_num": a[..., 11:20].astype(xp.int32),
    }


def noop_override(xp, lay: Layout = None):
    """`decode` of the no-op action of every slot: the IDENTITY planner.

    [ACTIONRL6] Self-play needs seat 1 to fly the PLAIN shipped planner while
    seat 0 flies the head, and `plan.RESIDUAL_FN` is module-level -- it has no
    seat argument and fires once per seat.  Returning this from the second call
    of a dawn is what makes the opponent head-free, and it is exactly the
    override a fresh head emits (`ZERO_BIAS` on each no-op), so nothing in
    `_residual_override`'s clamp chain sees a new case.  In the wide layout the
    no-ops are `ask_fill = 0` and `seed_buy = 0` units, which `plan` turns into
    the OFF program rather than into a zero-sized fill.
    """
    lay = LAYOUT if lay is None else lay
    return decode(xp, xp.asarray(lay.NOOP, xp.int32), lay)


def act_hist(acts, lay: Layout = None):
    """list[list[int]]: per-slot action counts over a batch, for `log.tsv`."""
    a = np.asarray(acts)
    lay = _lay_acts(a, lay)
    a = a.reshape(-1, lay.N_SLOT)
    return [np.bincount(a[:, s], minlength=lay.N_ACT[s]).tolist()
            for s in range(lay.N_SLOT)]


# ------------------------------------------------------- the file-agent path

def numpy_fn(params):
    """`plan.RESIDUAL_FN` for the SUBMISSION: numpy, greedy, no JAX.

    Greedy and not sampled on purpose -- the package must be deterministic, so
    the engine gate replays the same plan the trainer's argmax head scored.
    """
    lay = layout_of(params)
    params = {k: np.asarray(v, np.float32) for k, v in params.items()
              if k != _LAYOUT_KEY}

    def fn(obs_features, macro_fields):
        feats = np.asarray(obs_features, np.float32).reshape(-1)
        return decode(np, greedy_acts(np, forward(np, params, feats), lay), lay)

    return fn


def jax_fn(jnp, jrandom, params, key, logits_box=None, opponent_params=None,
           learner_seat=0, greedy=False):
    """`plan.RESIDUAL_FN` for ONE traced dawn of the sim rollout.

    `key` is this dawn's key (already folded with the day).  When `logits_box`
    is a list the callable appends `(feats, logits, acts)` to it, which is how
    `ppo.py` lifts the dawn's tensors out of the scan body: they are tracers
    created inside the body's own trace, so the body may return them as `ys`.

    `jrandom` is PASSED IN, not imported.  This module ships inside the Kaggle
    archive byte-identical (`package_submission.RESIDUAL_MODULE`), and
    `package_submission.forbidden_imports` is an AST scan that fails on an
    `import jax` anywhere in a packaged file -- including one nested in a
    function this half of the module never calls there.  Taking the module as
    an argument keeps the one-module contract honest instead of hiding the
    import from the gate: `head.py` imports numpy (and `os`, for the layout
    switch) and nothing else, on every line, and the gate stays as strict as it
    was.

    `sim.rollout.run_day` plans BOTH seats from this one module-level hook, seat
    0 first.  Only the FIRST call of a dawn gets the head; the second (the
    opponent's) gets `noop_override`, i.e. the plain shipped planner.  Under a
    tape that seat's plan was discarded anyway, so this changes nothing there --
    and under SELF-PLAY [ACTIONRL6] it is what keeps the opponent head-free.
    The opponent's no-op is taken in the HEAD's OWN layout, not the module
    default, so a wide run started without the env var still pairs correctly.
    """
    lay = layout_of(params)
    params = {k: v for k, v in params.items() if k != _LAYOUT_KEY}
    n_called = []

    # Keep the original closure as a literal branch.  Besides avoiding extra
    # work, this preserves the traced program and random draws of every caller
    # that predates the opponent/seat options.
    legacy_seat = (isinstance(learner_seat, (int, np.integer)) and
                   int(learner_seat) == 0)
    if opponent_params is None and legacy_seat and not greedy:
        def legacy_fn(obs_features, macro_fields):
            if n_called:                               # seat 1: plain planner
                return noop_override(jnp, lay)
            n_called.append(1)
            feats = jnp.asarray(obs_features, jnp.float32).reshape(-1)
            logits = forward(jnp, params, feats)
            acts = sample_acts(jnp, jrandom, key, logits, lay)
            if logits_box is not None:
                logits_box.append((feats, logits, acts))
            return decode(jnp, acts, lay)

        return legacy_fn

    opp = (None if opponent_params is None else
           {k: v for k, v in opponent_params.items() if k != _LAYOUT_KEY})
    if opp is not None and layout_of(opponent_params).name != lay.name:
        raise ValueError("learner and opponent head layouts differ")
    candidates = []

    def fn(obs_features, macro_fields):
        seat = len(n_called)
        n_called.append(1)
        feats = jnp.asarray(obs_features, jnp.float32).reshape(-1)
        logits = forward(jnp, params, feats)
        acts = (greedy_acts(jnp, logits, lay) if greedy else
                sample_acts(jnp, jrandom, key, logits, lay))
        candidates.append((feats, logits, acts))

        if opp is None:
            learner_out = decode(jnp, acts, lay)
            opponent_out = noop_override(jnp, lay)
        else:
            opp_acts = greedy_acts(jnp, forward(jnp, opp, feats), lay)
            learner_out = decode(jnp, acts, lay)
            opponent_out = decode(jnp, opp_acts, lay)
        is_learner = jnp.asarray(learner_seat, jnp.int32) == seat
        out = {k: jnp.where(is_learner, learner_out[k], opponent_out[k])
               for k in learner_out}

        # Both residual calls occur while run_day is traced.  Select only the
        # learner's tensors after the second call, when both candidates exist.
        if logits_box is not None and seat == 1:
            pick0 = jnp.asarray(learner_seat, jnp.int32) == 0
            logits_box.append(tuple(jnp.where(pick0, a, b)
                                    for a, b in zip(candidates[0],
                                                    candidates[1])))
        return out

    return fn
