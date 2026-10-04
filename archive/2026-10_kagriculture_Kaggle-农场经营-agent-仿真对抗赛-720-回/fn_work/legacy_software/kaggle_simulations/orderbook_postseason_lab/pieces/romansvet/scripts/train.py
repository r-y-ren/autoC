"""ES training driver.

Run under tmux/nohup -- this is a multi-hour job. Checkpoints theta and the
opponent pool every `--ckpt-every` generations so a dropped connection or a
crash costs at most that many.
"""
import argparse, hashlib, json, math, os, signal, sys, time
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, "src")

import numpy as np
import jax
import jax.numpy as jnp

from kagg3 import spec
from kagg3.core import policy as PO
from kagg3.es import archetypes as AR
from kagg3.es import kagg2_flow as K2F
from kagg3.es import kaggle_flow as KGF
from kagg3.es import tape_actions as TPA
from kagg3.es import tape_flow as TPF
from kagg3.es.train import (CandidateKeeper, Config, LATE_PRICE_DAYS, RealGate,
                            TAPE_SCORES, TILE_FILL_DAYS, Trainer,
                            MARGIN_PREFIX, NO_BEST, SOFTWIN_PREFIX,
                            flow_ensemble_draws, select_spec, train_mask)

STOP = False

#: Largest flow-scale upper bound `sim.market.FLOW_K` is sized for. `FLOW_K` is
#: `2 * max(busiest day over every registered table) + 1`, so this cap covers
#: `--kagg2-flow-scale`, `--kaggle-flow-scale` and `--tape-flow-scale` alike --
#: a tape's table raises `FLOW_K` when it is registered, so the cap is a cap on
#: the *multiplier*, whatever table it is applied to.
FLOW_SCALE_MAX = 2.0


def parse_rung_weights(items, names):
    """`["NAME=W", ...]` -> `(("NAME", W), ...)`, refused early and by name.

    A typo'd rung name is the failure worth catching here: silently ignored it
    would leave the operator watching a run they think is weighted and is not,
    for the hours it takes to notice. `names` is the ladder this invocation
    will actually build, so "not in the list" also covers `--n-archetypes`
    stopping short of the rung being weighted.
    """
    out = []
    for item in items or []:
        name, sep, raw = item.partition("=")
        if not sep:
            raise SystemExit(f"--rung-weight {item}: expected NAME=WEIGHT.")
        try:
            w = float(raw)
        except ValueError:
            raise SystemExit(f"--rung-weight {item}: {raw!r} is not a number.")
        if not math.isfinite(w) or w < 0.0:
            raise SystemExit(f"--rung-weight {item}: the weight is a share of "
                             f"the archetype episode slots, so it must be "
                             f"finite and non-negative.")
        if name not in names:
            raise SystemExit(
                f"--rung-weight {item}: no rung called {name!r} in this run's "
                f"ladder, which is: {', '.join(names) or '(none)'}.")
        out.append((name, w))
    seen = [n for n, _ in out]
    dup = sorted({n for n in seen if seen.count(n) > 1})
    if dup:
        raise SystemExit(f"--rung-weight names {', '.join(dup)} more than once.")
    if out and sum(w for _, w in out) + (len(names) - len(out)) <= 0:
        raise SystemExit("--rung-weight zeroes every rung; there would be no "
                         "archetype slots at all. Use --arch-frac 0 to say that.")
    return tuple(out)


def parse_rung_thetas(items):
    """`["NAME=PATH.npy", ...]` -> `(("NAME", "PATH"), ...)`, refused early.

    An **anchor** is a frozen trained theta pinned into the ladder by name. It
    defaults to holdout -- weight 0, so it takes no episode slot and no share of
    the yardstick mean, exactly what `AR.HOLDOUT_RUNGS` is for the two held-out
    openings -- and `--rung-weight NAME=W` pulls it into the objective. The name
    is refused against the ladder's own labels because those are pins: an anchor
    that shadowed `mixed_ranch` would silently replace the rung every measured
    number on record is stated against.

    Existence is checked here, next to the format, because the alternative is a
    typo'd path discovered after the run directory exists and the ladder has
    been probed.
    """
    out = []
    for item in items or []:
        name, sep, path = item.partition("=")
        if not sep or not name:
            raise SystemExit(f"--rung-theta {item}: expected NAME=PATH.npy.")
        if name in AR.NAMES or name.startswith(("sampled", "rung")):
            raise SystemExit(f"--rung-theta {item}: {name!r} is a ladder rung "
                             f"label ({', '.join(AR.NAMES)}, sampledN, rungN); "
                             f"give the anchor a name of its own.")
        if name in [n for n, _ in out]:
            raise SystemExit(f"--rung-theta names {name} more than once.")
        if not os.path.isfile(path):
            raise SystemExit(f"--rung-theta {item}: no such file {path!r}.")
        out.append((name, path))
    return tuple(out)


def parse_handicap(raw):
    """`"NQUAD:MONEY"` -> `(int, int)`, refused early."""
    lhs, sep, rhs = str(raw).partition(":")
    if not sep:
        raise SystemExit(f"--proxy-handicap {raw}: expected NQUAD:MONEY, "
                         f"e.g. 3:20000 (the default {AR.NO_HANDICAP[0]}:"
                         f"{AR.NO_HANDICAP[1]} is the engine's own day 0).")
    try:
        nquad, money = int(lhs), int(rhs)
    except ValueError:
        raise SystemExit(f"--proxy-handicap {raw}: NQUAD and MONEY are integers.")
    n_quad = int(spec.LAND_PRICES.shape[0]) + 1
    if not 1 <= nquad <= n_quad:
        raise SystemExit(f"--proxy-handicap {raw}: NQUAD must be 1..{n_quad}; "
                         f"the board has {n_quad} quadrants.")
    if money < spec.STARTING_MONEY:
        raise SystemExit(f"--proxy-handicap {raw}: MONEY must be at least the "
                         f"engine's own opening purse of {spec.STARTING_MONEY}. "
                         f"A handicap can only ever add.")
    return (nquad, money)


def rung_names(n_archetypes, kagg2_flow=False, kaggle_flow=False, tapes=(),
               tape_acts=()):
    """The labels `Trainer` will give its archetype slots, without building it.

    The flow rungs append the same way `Trainer._build_archetypes` appends them
    -- past `--n-archetypes`, at the end, `kagg2_flow` first, then
    `kaggle_flow`, then the `--tape-rung` tables in the order they were named,
    then the `--tape-actions` tables in theirs -- so `--rung-weight
    kagg2_flow=3` validates against the ladder the run will actually have, and
    turning on a later rung moves no existing index.
    """
    named = list(AR.NAMES[:max(n_archetypes, 0)])
    out = named + [f"sampled{i}" for i in range(max(n_archetypes, 0) - len(named))]
    out = out + ([K2F.RUNG_NAME] if kagg2_flow else [])
    out = out + ([KGF.RUNG_NAME] if kaggle_flow else [])
    out = out + [str(n) for n in tapes]
    return out + [str(n) for n in tape_acts]


def parse_tape_rungs(items):
    """`--tape-rung` paths -> (paths, rung names).

    Each flag may carry several comma-separated paths, so one rung per replay
    does not mean one flag per replay. The tables are *loaded* here rather than
    only recorded: a missing file or a mislabelled table has to be refused
    before a multi-hour run starts, and the names are needed anyway to validate
    `--rung-weight` and `--select-metric` against the ladder this run will
    hold.
    """
    paths = []
    for item in items or ():
        paths.extend(p for p in str(item).split(",") if p)
    try:
        tapes = TPF.load_many(paths)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"--tape-rung: {exc}")
    return tuple(paths), tuple(t.name for t in tapes)


def pinned_once_notes(episodes, n_pinned, n_rungs):
    """What `--pinned-once` did to the episode budget. -> [str]

    A list of lines rather than prints, so the startup banner and the tests
    read the same sentences. The first line is always the budget itself --
    "N pinned rungs x 1 episode + M episodes carried" -- because that is the
    number an operator checks against the launcher; the rest are the two ways
    a configuration can make the flag mean something other than it says.

    Nothing here refuses. `--episodes` below the pinned count is a *warning*,
    not an error, because the pinned block is never truncated: truncating it
    would silently drop boards, which is the opposite of the flag's promise.
    Such a run simply spends more than `--episodes` says, and the line says
    how much.
    """
    if n_pinned <= 0:
        return ["WARNING: --pinned-once but no rung on this ladder is pinned: "
                "none of the --tape-actions tapes carries a `town` key (cut "
                "them with --with-town). The flag is inert."]
    carried = episodes - n_pinned
    out = [f"pinned-once: {n_pinned} pinned rungs x 1 episode + "
           f"{max(carried, 0)} episodes carried"]
    if carried < 0:
        out.append(
            f"WARNING: --pinned-once with --episodes {episodes} and "
            f"{n_pinned} pinned rungs: the pinned block alone needs "
            f"{n_pinned} episodes, so this run plays {n_pinned + 2} per "
            f"candidate per generation, not {episodes}. Raise --episodes "
            f"above {n_pinned} or load fewer pinned tapes.")
    elif carried < 2 * n_pinned:
        out.append(
            f"WARNING: --pinned-once leaves {carried} episodes for "
            f"{max(n_rungs - n_pinned, 0)} unpinned rung(s) and self-play, "
            f"against {n_pinned} pinned boards -- at this ratio the drawn "
            f"rungs and the pool are sampled thinly.")
    return out


def parse_tape_actions(items):
    """`--tape-actions` paths -> (paths, rung names).

    Loaded here, not merely recorded, for `parse_tape_rungs`' two reasons: a
    missing or malformed `.npz` has to stop the run at the command line, and
    the names are needed to validate `--rung-weight` against the ladder this
    run will hold.
    """
    paths = []
    for item in items or ():
        paths.extend(p for p in str(item).split(",") if p)
    try:
        acts = TPA.load_many(paths)
    except (OSError, ValueError, KeyError) as exc:
        raise SystemExit(f"--tape-actions: {exc}")
    return tuple(paths), tuple(TPA.rung_name(a.episode) for a in acts)


def parse_flow_scale(raw, flag="--kagg2-flow-scale"):
    """`LO:HI` -> (float, float), refusing the ranges that would be silent."""
    try:
        lo, hi = (float(x) for x in str(raw).split(":", 1))
    except ValueError:
        raise SystemExit(f"{flag} {raw}: expected LO:HI, e.g. 0.5:1.5.")
    if lo <= 0 or hi < lo:
        raise SystemExit(f"{flag} {raw}: need 0 < LO <= HI.")
    if hi > FLOW_SCALE_MAX:
        # `sim.market.FLOW_K` is sized off the busiest day of either measured
        # table times this cap, and the walk clamps rather than reading out of
        # bounds -- so a bigger scale would quietly stop scaling.
        raise SystemExit(
            f"{flag} {raw}: HI is capped at {FLOW_SCALE_MAX}; past "
            f"that the quote walk in sim.market.apply_flow clamps and the "
            f"scale silently stops applying.")
    return (lo, hi)


def parse_int_range(raw, flag, lo_min=None, hi_max=None):
    """`LO:HI` -> (int, int), for the yardstick's two ensemble ranges.

    Integers rather than `parse_flow_scale`'s floats: the yardstick's levels
    have to be exactly reproducible from the flag string forever (they are in
    the ladder signature, and two runs comparing records compare them), and
    thousandths are the units the engine's control word already carries. So
    `--abs-flow-scale 500:1500` says what `--kagg2-flow-scale 0.5:1.5` says,
    with no decimal to round.
    """
    try:
        lo, hi = (int(x) for x in str(raw).split(":", 1))
    except ValueError:
        raise SystemExit(f"{flag} {raw}: expected LO:HI, two integers.")
    if hi < lo:
        raise SystemExit(f"{flag} {raw}: need LO <= HI.")
    if lo_min is not None and lo < lo_min:
        raise SystemExit(f"{flag} {raw}: LO must be at least {lo_min}.")
    if hi_max is not None and hi > hi_max:
        raise SystemExit(f"{flag} {raw}: HI is capped at {hi_max}.")
    return (lo, hi)


def save_atomic(path, arr):
    """`np.save` writes in place, so a reader can observe a half-written file.

    The packager, the release gates and the eval scripts all read
    `artifacts/theta.npy` while training is still checkpointing into it. Write
    to a sibling temp file and rename: on POSIX that swap is atomic, so a reader
    sees either the old weights or the new ones, never a truncated prefix.
    """
    tmp = path + ".tmp.npy"
    with open(tmp, "wb") as fh:
        np.save(fh, arr)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def _array_identity(value):
    a = np.ascontiguousarray(np.asarray(value))
    h = hashlib.sha256()
    h.update(a.dtype.str.encode("utf-8"))
    h.update(str(a.shape).encode("utf-8"))
    h.update(a.tobytes())
    return {"shape": list(a.shape), "dtype": str(a.dtype),
            "sha256": h.hexdigest()}


def _stable_training_value(value):
    if isinstance(value, float) and not np.isfinite(value):
        return {"nonfinite_float": str(value)}
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(k): _stable_training_value(value[k])
                for k in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_stable_training_value(x) for x in value]
    try:
        a = np.asarray(value)
        if a.dtype != object:
            return _array_identity(a)
    except Exception:
        pass
    raise TypeError(f"unsupported training-state value: {type(value).__name__}")


_SCOPE_STATE_FIELDS = (
    "theta", "champion", "pool", "archetypes", "archetype_names",
    "archetype_coins", "rung_weights", "arch_handicap", "m", "v",
    "best_abs_theta", "best_sim_theta", "champion_score", "t", "adam_t",
    "best_abs", "best_hold", "sigma", "sigma_restarts", "sigma_steps",
    "last_improve", "replicate_rejects", "history", "abs_history",
    "last_day_metrics", "last_centre_fwd", "last_real_gate",
    "last_recentre", "last_rung_episodes",
)


def scope_training_snapshot(tr):
    """Complete stable snapshot of state a no-update diagnostic may touch."""
    out = {name: _stable_training_value(getattr(tr, name))
           for name in _SCOPE_STATE_FIELDS if hasattr(tr, name)}
    for name in ("theta", "champion", "pool", "m", "v", "t", "adam_t"):
        if name not in out:
            raise RuntimeError(f"trainer state is missing {name}")
    out["key_data"] = _stable_training_value(jax.random.key_data(tr.key))
    out["slot_credit"] = _stable_training_value(
        None if tr.slot_carry is None else tr.slot_carry.credit)
    out["rng_bit_generator_state"] = _stable_training_value(
        tr.rng.bit_generator.state)
    return out


def _flatten_scope_arrays(prefix, value, output):
    """Flatten array-bearing NamedTuple/list trees into an NPZ namespace."""
    if value is None:
        return
    if hasattr(value, "_fields"):
        for name in value._fields:
            _flatten_scope_arrays(f"{prefix}__{name}", getattr(value, name), output)
        return
    if isinstance(value, dict):
        for key in sorted(value, key=str):
            _flatten_scope_arrays(f"{prefix}__{key}", value[key], output)
        return
    if isinstance(value, (tuple, list)):
        for i, item in enumerate(value):
            _flatten_scope_arrays(f"{prefix}__{i}", item, output)
        return
    a = np.asarray(value)
    if a.dtype == object:
        raise TypeError(f"scope evidence {prefix} has object dtype")
    output[prefix] = a


def scope_runtime_metadata():
    devices = jax.devices()
    return {
        "jax_version": jax.__version__,
        "jaxlib_version": getattr(jax.lib, "__version__", None),
        "backend": jax.default_backend(),
        "devices": [{"platform": d.platform,
                     "device_kind": getattr(d, "device_kind", None),
                     "id": int(d.id)} for d in devices],
        "jax_enable_x64": bool(jax.config.jax_enable_x64),
        "jax_default_matmul_precision": str(
            jax.config.jax_default_matmul_precision),
        "jax_enable_compilation_cache": bool(
            jax.config.jax_enable_compilation_cache),
        "environment": {name: os.environ.get(name) for name in (
            "CUDA_VISIBLE_DEVICES", "JAX_PLATFORMS", "JAX_ENABLE_X64",
            "JAX_DEFAULT_MATMUL_PRECISION", "JAX_ENABLE_COMPILATION_CACHE",
            "JAX_COMPILATION_CACHE_DIR", "XLA_FLAGS",
            "XLA_PYTHON_CLIENT_PREALLOCATE")},
    }


def save_scope_diagnostic(out, tr, diagnostic, before, after):
    """Atomically publish raw no-update diagnostic evidence into fresh `out`."""
    if before != after:
        raise RuntimeError("scope diagnostic mutated trainer state")
    arrays = {}
    _flatten_scope_arrays("field", diagnostic.field, arrays)
    for name in ("masks", "masked_noise", "money", "own", "relative",
                 "own_rank", "relative_rank", "advantage", "gradients"):
        _flatten_scope_arrays(name, getattr(diagnostic, name), arrays)
    p = int(diagnostic.pairs)
    for name in ("own", "relative", "advantage"):
        values = getattr(diagnostic, name)
        arrays[f"paired_difference__{name}"] = np.asarray(
            values[:, :p] - values[:, p:])
    arrays["raw_interaction__own"] = np.asarray(
        (diagnostic.own[2, :p] - diagnostic.own[2, p:])
        - (diagnostic.own[1, :p] - diagnostic.own[1, p:])
        - (diagnostic.own[0, :p] - diagnostic.own[0, p:]))
    arrays["raw_interaction__relative"] = np.asarray(
        (diagnostic.relative[2, :p] - diagnostic.relative[2, p:])
        - (diagnostic.relative[1, :p] - diagnostic.relative[1, p:])
        - (diagnostic.relative[0, :p] - diagnostic.relative[0, p:]))
    for name, value in arrays.items():
        if not np.all(np.isfinite(value)):
            raise RuntimeError(f"scope evidence {name} is nonfinite")
    def difference_summary(values):
        values = np.asarray(values, dtype=np.float64)
        return {"pairs": int(values.size),
                "ties": int(np.count_nonzero(values == 0)),
                "nonzero": int(np.count_nonzero(values)),
                "mean": float(values.mean()),
                "rms": float(np.sqrt(np.mean(values * values)))}

    scope_summaries = {
        scope: {name: difference_summary(arrays[f"paired_difference__{name}"][i])
                for name in ("own", "relative", "advantage")}
        for i, scope in enumerate(diagnostic.scopes)
    }
    npz_path = os.path.join(out, "scope_diagnostic.npz")
    tmp = npz_path + ".tmp"
    with open(tmp, "wb") as fh:
        np.savez(fh, **arrays)
        fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, npz_path)
    meta = {
        "schema": 1,
        "mode": "generation_zero_antithetic_scope_diagnostic",
        "scopes": list(diagnostic.scopes),
        "scope_blocks": {"M": ["mh", "ms"], "H": ["w2", "b2"],
                         "J": ["mh", "ms", "w2", "b2"]},
        "pairs_per_scope": int(diagnostic.pairs),
        "candidates_per_scope": 2 * int(diagnostic.pairs),
        "sigma": float(tr.sigma),
        "fitness_weights": {"own": float(tr.cfg.abs_weight),
                            "relative": 1.0 - float(tr.cfg.abs_weight)},
        "scope_summaries": scope_summaries,
        "raw_interaction_summaries": {
            name: difference_summary(arrays[f"raw_interaction__{name}"])
            for name in ("own", "relative")
        },
        "episodes": int(diagnostic.field.episodes),
        "rung_episodes": diagnostic.field.rung_episodes,
        "state_before": before,
        "state_after": after,
        "state_unchanged": before == after,
        "field_presence": {
            name: getattr(diagnostic.field, name) is not None
            for name in diagnostic.field._fields
        },
        "runtime": scope_runtime_metadata(),
        "arrays": {name: _array_identity(value)
                   for name, value in sorted(arrays.items())},
        "npz_sha256": hashlib.sha256(open(npz_path, "rb").read()).hexdigest(),
        "limitations": [
            "raw own/relative components support cross-scope interaction; ranked values are scope-local",
            "this is a no-update training-field diagnostic, not strength or held-out evidence",
        ],
    }
    if not meta["state_unchanged"]:
        raise RuntimeError("scope diagnostic mutated trainer state")
    path = os.path.join(out, "scope_diagnostic.json")
    tmp = path + ".tmp"
    with open(tmp, "x") as fh:
        json.dump(meta, fh, indent=2, sort_keys=True, allow_nan=False)
        fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, path)


def save_scope_refusal(out, before, after, exc):
    path = os.path.join(out, "scope_diagnostic_refused.json")
    payload = {"schema": 1, "verdict": "REFUSED",
               "error_type": type(exc).__name__, "error": str(exc),
               "state_before": before, "state_after": after,
               "state_unchanged": before == after}
    tmp = path + ".tmp"
    with open(tmp, "x") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True, allow_nan=False)
        fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, path)


def _fit_layout(arr, run_dir, what):
    """Zero-extend an older-layout checkpoint array to the current layout.

    Every parameter block is *appended* to `policy.SHAPES`, never interleaved,
    so a checkpoint written under an older layout is a prefix of the current one
    and the missing tail is exactly the genes that did not exist when it was
    trained. `policy.pad` is what fills it -- zeros for every block that decodes
    to its own no-op, and the season-constant `hire_bias` copied into its day
    buckets, which is the one appended block whose zero is not what the older
    checkpoint said. The same rule `policy.unpack` applies at inference.

    The padding has to happen *here* and not at decode time: `Trainer` sizes its
    perturbation, its Adam moments, its live mask and its decay mask off
    `theta.shape[0]`, so resuming a short theta unpadded would leave every gene
    added since it was written frozen at zero for the whole run, silently. This
    function used to refuse that case outright; padding is strictly better,
    because a run whose ladder took hours to build should not have to be thrown
    away to pick up a new input block.

    Applied to every array in the checkpoint that is indexed by parameter --
    theta, champion, `best_abs_theta`, the pool, the restored archetypes and
    both Adam moments -- so the trainer stays internally consistent. Zeroed
    moments for a new coordinate are what a cold start would have given it.

    A *longer* array is a newer layout this build cannot interpret and there is
    nothing safe to drop, so that half of the old refusal stays.
    """
    n = arr.shape[-1]
    if n == PO.N_PARAMS:
        return arr
    if n > PO.N_PARAMS:
        raise SystemExit(
            f"--resume {run_dir}: {what} has {n} params, more than this build's "
            f"layout of {PO.N_PARAMS}. That checkpoint was written by a newer "
            f"policy layout; nothing here can interpret the extra block.")
    return PO.pad(arr)


def _legacy_none(x):
    """Read a pre-2026-08-27 "none yet" forward. -> float

    `-1.0` was that sentinel for `best_abs` and `champion_score` while every
    selectable metric was positive. It is now `NO_BEST` (`-inf`), and the
    difference matters on the checkpoint that stopped before its first
    measurement: carried literally, `-1.0` is a *record* of minus one coin, and
    the resumed run would print "best_abs carried over: -1.0" and ship its
    untrained init as `best_abs.npy`.

    The test is exact equality, and what it can cost is a real record that
    happens to read -1.0 exactly. That is a mean of 32 float margins landing on
    a whole number, which does not happen; the other side of the trade -- an
    init theta promoted as `best_abs.npy` -- happens on every checkpoint that
    stopped inside its first `--abs-every` generations.
    """
    return NO_BEST if x == -1.0 else x


def _num(x, places):
    """A log-record number, or `null` for the "none yet" sentinel. -> float|None

    `best_abs` and `champion_score` start at `-inf` (see `train.NO_BEST`)
    because a margin metric can be negative and no finite sentinel is safe.
    `-inf` is not JSON, though -- `json.dumps` emits a bare `-Infinity` that a
    strict reader refuses -- and `-1.0` cannot come back: a tracker reading
    `best_abs: -1.0` off a margin run cannot tell the sentinel from a policy
    that lost by one coin. `null` is the only value that says "not measured"
    and stays readable.
    """
    return None if x is None or not math.isfinite(x) else round(float(x), places)


def _fwd_read(tr):
    """The forward-admit gene as this generation decoded it. -> (fwd, frac, centre)

    All three are `None` on a tree whose layout has no `g11` block, and on a
    run whose evaluator is a stub -- `Trainer.day_metric_means` then returns
    the four-tuple it always returned, so this is the one place that has to
    know the tuple can be short. `centre` is `None` on top of that for every
    generation that took no absolute reading, since it is read off that
    measurement and nothing else (`Trainer.last_centre_fwd`).
    """
    dm = getattr(tr, "last_day_metrics", None)
    if dm is None or len(dm) < 6:
        return None, None, None
    return dm[4], dm[5], getattr(tr, "last_centre_fwd", None)


def _fwd_fields(tr):
    """The gene's three numbers as `log.jsonl` keys. -> dict"""
    fwd, frac, centre = _fwd_read(tr)
    return {"fwd_days": _num(fwd, 3), "fwd_frac": _num(frac, 3),
            "fwd_days_centre": _num(centre, 3)}


def _fwd_line(tr):
    """The gene's segment of the gen line, or `""`. -> str

    `fwd` is the mean decoded horizon in days over (member, episode, day) and
    `fwd>0` the fraction of members whose own mean is above zero -- the number
    that says whether the search can *see* the gene at all, since a population
    in which no member decodes a day has nothing to select between. `/ctr` is
    the centre theta's own horizon on the measurement boards, printed only on
    the generations that measured it.
    """
    fwd, frac, centre = _fwd_read(tr)
    if fwd is None:
        return ""
    return (f"  fwd {fwd:.2f}  fwd>0 {frac:.2f}"
            + ("" if centre is None else f"/ctr {centre:.2f}"))


def ladder_signature(tr):
    """What the absolute yardstick *is*, in a form two runs can compare.

    `best_abs` is a coin count (or a score, or one rung's margin) earned against
    one specific ladder: these rungs, at these weights, with these openings,
    read through one `--select-metric`. Change any of the four and the number
    means something else -- the 11-rung weighted ladder measures around 132k
    where the 9-rung one measured 150k, and a margin is a different quantity
    from a coin total *entirely*, negative where the other is six figures -- so
    an inherited best is not a bar the new run can clear, it is a bar it can
    never clear, and the run goes its whole length never writing
    `best_abs.npy`.

    The metric is in here rather than in a check of its own because a
    yardstick is the pair (what is measured, against what): a resume that
    switches to `margin:kagg2_flow` has changed the yardstick exactly as
    decisively as one that adds a rung, and the existing reset path already
    says the right thing about it. The whole metric *string* goes in, which is
    why `softwin:<rung>:<tau>` carries its tau here rather than on a flag of
    its own: a resume that rewidens the tanh from 3000 to 10000 is reading a
    different quantity, and the record it inherited was earned on the old one.

    The signature is therefore checkpointed next to the number it qualifies, and
    a resume compares it. Names, weights, openings, the metric and *how the
    yardstick reads them* only: the rung **thetas** are already carried by the
    checkpoint, and the archetype coins are a measurement (the planner moves
    them) rather than a statement of what the ladder is.

    `--best-replicate` is deliberately *not* in here: it is a rule about how a
    record is taken, like `--best-margin` and `--best-gate`, not a statement of
    what the yardstick measures. An inherited record is still a bar in the same
    units, and a resume that turns replication on tightens the next record
    rather than invalidating the last one.

    `tape_score` is in here for the same reason the metric is, and it is the
    same kind of change: under `--tape-score ours` a tape rung's `score` column
    is our coins on a bounded scale rather than a margin against a seat
    credited with revenue it never earned, so a `best_abs` inherited across the
    switch was earned reading a different quantity on those rungs.

    `flow_ensemble` and `abs_select` are in here for the same reason the metric
    is. The flow rung read at the centre and the same rung read as the mean of
    ten drawn levels are two different opponents, several thousand coins apart
    on the same theta; and a statistic on 32 pairs is not the statistic on 64.
    An inherited record is a bar measured under the old one, so switching
    either has to retire it. The **draw list** rather than just `K`, because
    the levels move with `--abs-flow-scale` / `--abs-flow-shift` at a fixed
    `K` -- and recentring the family on scale 1.3 is exactly the change an
    operator would make and exactly the one that invalidates the record.
    """
    fresh = bool(getattr(tr.cfg, "abs_fresh_draws", False))
    draws = ([] if fresh else
             flow_ensemble_draws(tr.cfg.abs_flow_draws,
                                 tr.cfg.abs_flow_scale, tr.cfg.abs_flow_shift))
    ens = {"k": int(tr.cfg.abs_flow_draws),
           "draws": [[int(s), int(d)] for s, d in draws]}
    if fresh:
        # `fresh` and the *family*, never the levels: under
        # `--abs-fresh-draws` the levels are redrawn every measurement, so a
        # list of them would retire the record at every checkpoint. What has to
        # carry is that the yardstick is a drawn one and which family it draws
        # from -- recentring that family (`--abs-flow-scale 800:1800`) is the
        # same change to a fresh yardstick that it is to a fixed one.
        #
        # Absent rather than `false` on a run without the flag, so a signature
        # written before this field and one written by an unflagged run after
        # it are the same bytes and no resume is retired by its arrival.
        ens["fresh"] = True
        ens["family"] = [[int(x) for x in tr.cfg.abs_flow_scale],
                         [int(x) for x in tr.cfg.abs_flow_shift]]
    return {"names": [str(n) for n in tr.archetype_names],
            "weights": [round(float(w), 6) for w in tr.rung_weights],
            "handicap": [[int(a), int(b)]
                         for a, b in np.asarray(tr.arch_handicap).reshape(-1, 2)],
            "select": str(tr.cfg.select_metric),
            "tape_score": str(tr.cfg.tape_score),
            "flow_ensemble": ens,
            "abs_select": str(tr.cfg.abs_select)}


def _read_signature(sig):
    """A checkpoint's signature, in this build's shape. -> dict

    Signatures written before `select` existed get `coins`, which is what every
    one of them was in fact measured under: it is the default, and the field
    was added in the same commit that gave `--select-metric` anything else
    worth resuming into. Defaulting to the *current* metric instead would make
    the change this field exists to catch invisible on exactly the checkpoints
    that need it caught.
    """
    out = dict(sig)
    out.setdefault("select", "coins")
    # Same rule for the yardstick's two 2026-08-27 fields: every signature
    # written before them was written by a run that read the flow rung at its
    # centre, on the selection half. Those are the defaults, so a checkpoint
    # missing the fields and a run not passing the flags compare equal.
    out.setdefault("flow_ensemble", {"k": 0, "draws": []})
    out.setdefault("abs_select", "sel")
    # And the same rule again for 2026-09-04's: every signature written before
    # it was written by a run that scored its tape rungs on the margin, which
    # is the default, so an older checkpoint and an unflagged run compare equal.
    out.setdefault("tape_score", "margin")
    return out


def _ladder_diff(old, new):
    """One line naming the part of the yardstick that moved. -> str."""
    bits = []
    if old.get("select", "coins") != new["select"]:
        # First, because it is the one change that makes the inherited number
        # not merely a different level but a different *quantity*.
        bits.append(f"select metric {old.get('select', 'coins')} -> "
                    f"{new['select']}")
    on, nn = list(old["names"]), list(new["names"])
    if on != nn:
        added = [n for n in nn if n not in on]
        gone = [n for n in on if n not in nn]
        moved = ([f"+{','.join(added)}"] if added else []) + \
                ([f"-{','.join(gone)}"] if gone else [])
        bits.append("rungs " + (" ".join(moved) if moved
                                else f"reordered {len(on)} -> {len(nn)}"))
    ow, nw = dict(zip(on, old["weights"])), dict(zip(nn, new["weights"]))
    shifted = [f"{n} {ow[n]:g}->{nw[n]:g}" for n in nn
               if n in ow and ow[n] != nw[n]]
    if shifted:
        bits.append("weights " + ", ".join(shifted))
    oh = dict(zip(on, [tuple(x) for x in old["handicap"]]))
    nh = dict(zip(nn, [tuple(x) for x in new["handicap"]]))
    hand = [f"{n} {oh[n][0]}:{oh[n][1]}->{nh[n][0]}:{nh[n][1]}" for n in nn
            if n in oh and oh[n] != nh[n]]
    if hand:
        bits.append("handicap " + ", ".join(hand))
    oe = old.get("flow_ensemble", {"k": 0, "draws": []})
    ne = new["flow_ensemble"]
    if oe.get("fresh", False) != ne.get("fresh", False):
        # First among the ensemble's changes, because it is the one that says
        # the *kind* of statistic moved: a max over one fixed set of levels and
        # a max over levels redrawn each time are not the same record, however
        # similar the two families are.
        bits.append("flow ensemble draws "
                    + ("fixed -> fresh" if ne.get("fresh") else "fresh -> fixed"))
    elif oe != ne:
        # `K` and the levels separately: an operator who recentred the family
        # (`--abs-flow-scale 800:1800`) kept the same K, and "flow ensemble
        # 10 -> 10" would read as no change at all.
        bits.append(
            f"flow ensemble K {oe.get('k', 0)} -> {ne['k']}"
            if oe.get("k") != ne["k"] else
            # Under `fresh` the levels are not in the signature at all, so the
            # family is what moved and the levels line would read `[] -> []`.
            f"flow ensemble family {oe.get('family')} -> {ne.get('family')}"
            if oe.get("family") != ne.get("family") else
            f"flow ensemble levels {oe.get('draws')} -> {ne['draws']}")
    if old.get("abs_select", "sel") != new["abs_select"]:
        bits.append(f"abs seeds {old.get('abs_select', 'sel')} -> "
                    f"{new['abs_select']}")
    if old.get("tape_score", "margin") != new["tape_score"]:
        bits.append(f"tape score {old.get('tape_score', 'margin')} -> "
                    f"{new['tape_score']}")
    return "; ".join(bits) or "ladder changed"


def reset_best_if_ladder_changed(tr, force=False):
    """Drop an inherited `best_abs` when this run's yardstick is not the one it
    was measured on. -> the one-line explanation, or None if the best carries.

    Called twice, because the ladder is assembled in two steps: once at the end
    of `load_resume` (which is where `--kagg2-flow` extends a restored ladder)
    and once after `add_anchor_rungs`. It compares against the *checkpoint's*
    signature both times, so the second call simply confirms the first, and a
    run whose ladder only changes at the anchor step is still caught.

    Only `best_abs` and `best_abs_theta` move. Theta, sigma and its restart
    count, the Adam moments, the generation, the elapsed, the PRNG key and the
    host RNG are the trajectory, and the trajectory is valid whatever the
    yardstick says. `best_abs_theta` follows the number because the two are one
    claim -- "this theta scored this" -- and because `_maybe_restart` jumps the
    run back onto it: restarting onto a theta whose only credential was earned
    on a ladder this run does not use is exactly the wrong jump. It becomes
    `tr.theta`, which is what a cold start holds before its first measurement.
    """
    seen = getattr(tr, "ckpt_rungs", None)      # None: not a state.npz resume
    ckpt = getattr(tr, "ckpt_ladder", None)     # None: a checkpoint predating this
    ckpt = None if ckpt is None else _read_signature(ckpt)
    if seen is None and not force:
        # A cold start has no record to retire, and nothing to compare: the
        # signature is not even computed, so a trainer that never checkpointed
        # (or a test stub) does not need the weights to exist yet.
        return None
    cur = ladder_signature(tr)
    if force:
        why = "forced by --reset-best"
    elif seen is None:
        return None
    elif ckpt is None:
        # Written before the signature existed. The rung *count* is the part of
        # the change that actually happened on this machine -- every ladder that
        # grew, grew by the flow rung and the anchors -- so it is the fallback,
        # and a same-count ladder is trusted rather than reset on a guess.
        if seen == len(cur["names"]) and cur["select"] == "coins":
            return None
        why = (f"checkpoint predates the ladder signature and its rung count "
               f"moved {seen} -> {len(cur['names'])}"
               if seen != len(cur["names"]) else
               f"checkpoint predates the ladder signature, so its best_abs is "
               f"a coin total, and this run selects on {cur['select']}")
    elif ckpt == cur:
        return None
    else:
        why = _ladder_diff(ckpt, cur)
    # The *first* reset's number, not this call's: the check runs twice (the
    # anchors confirm what the flow rung already did), and the second call
    # would otherwise report the sentinel the first one just wrote.
    had = getattr(tr, "best_reset_from", tr.best_abs)
    tr.best_reset_from = had
    # The theta that number belonged to, kept aside rather than dropped with
    # it. A yardstick change invalidates the *number* -- 133k of coins is not a
    # margin, a centre reading is not an ensemble one -- but it says nothing
    # about the iterate, and `--from-best` is an explicit instruction to
    # continue from that iterate. Without this, every flag that moves the
    # yardstick (a new rung, `--abs-flow-draws`, `--abs-select`) would make
    # `--from-best` refuse to start on the very resume that needs it, because
    # `load_resume` runs this reset before `main` gets to the jump.
    if not hasattr(tr, "best_reset_theta"):
        tr.best_reset_theta = tr.best_abs_theta
    tr.best_abs, tr.best_abs_theta = NO_BEST, tr.theta
    # The champion is the same claim on a coarser schedule -- `_measure_champion`
    # reads the very same `selection_score` -- so a score earned on the old
    # yardstick would otherwise sit as an unbeatable incumbent in
    # `champion.npy` for the rest of the run.
    tr.champion_score = NO_BEST
    # `best_hold` is the same claim's other half -- "this theta scored this on
    # the seeds nothing selects on" -- and it was earned on the same ladder, so
    # it goes with the number rather than surviving to gate the next record.
    tr.best_hold = NO_BEST
    was = f"{had:,.1f}" if math.isfinite(had) else "none yet"
    note = (f"best_abs reset to 'none yet' (was {was}): {why}. The first "
            f"measurement of this run becomes the new best.")
    tr.best_reset_note = note
    return note


def jump_to_best(tr, run_dir):
    """`--from-best`: continue from the checkpoint's best theta, not its last.

    The jump half of `Trainer._maybe_restart`, on demand. A run that is
    wandering below its own record does not need a bigger step to be rescued --
    it needs to be put back on the record and let go again -- and the operator
    can usually see that long before `--restart-sigma-on-stall` fires, or on a
    run that never passed the flag at all.

    Everything but theta and the Adam moments carries: the generation, the
    elapsed, sigma and its restart count, both RNG streams, the pool, and
    `best_abs` itself. The moments go for the same reason the restart drops
    them -- they are the curvature of the basin around the iterate being
    abandoned. `t` stays, because it is the generation counter every schedule
    and every log line reads; the *bias-correction* counter `adam_t` does not,
    it is zeroed with the moments it corrects. Keeping it at `t` is what
    a run cannot afford: `1 - beta**t` with t in the thousands is 1, so the
    correction stops correcting and the first step on the freshly zeroed
    moments is 3.16x `lr` per coordinate -- ||theta|| 17.6 -> 46 and the policy
    gone in five generations, which is what `--from-best` did to flow2 twice
    before this was found.

    A yardstick change is not a reason to refuse the jump. `load_resume` runs
    `reset_best_if_ladder_changed` before this, so on a resume that adds a rung
    or switches to the flow ensemble `best_abs` is already the sentinel by the
    time we get here -- but what that reset invalidated is the *number*, and
    `--from-best` is an instruction about the *theta*. So the retired theta is
    picked up from `best_reset_theta` and the jump goes ahead, onto a record
    that this run will then have to earn again from scratch.
    """
    had, best = tr.best_abs, tr.best_abs_theta
    if not math.isfinite(had):
        had = getattr(tr, "best_reset_from", NO_BEST)
        best = getattr(tr, "best_reset_theta", None)
    if best is None or not math.isfinite(had):
        raise SystemExit(
            f"--from-best {run_dir}: this checkpoint has no best_abs_theta yet "
            f"(best_abs is 'none yet'), so there is nothing to jump to. Resume "
            f"without it, or drop --reset-best if that is what cleared it.")
    tr.theta = best
    tr.m = jnp.zeros(tr.n)
    tr.v = jnp.zeros(tr.n)
    tr.adam_t = 0
    retired = ""
    if not math.isfinite(tr.best_abs):
        # The sentinel pairs with "best_abs_theta is the current theta", which
        # a cold start also holds; keep that true across the jump so a later
        # `_maybe_restart` cannot land on the iterate just left behind.
        tr.best_abs_theta = tr.theta
        retired = ", retired by this run's yardstick and to be re-earned"
    return (f"--from-best: theta <- best_abs_theta ({had:,.1f}{retired}), Adam "
            f"moments cleared; gen, sigma {tr.sigma:g}, step {tr.t} and both "
            f"RNGs kept")


def load_resume(tr, run_dir):
    """Restore a Trainer from a checkpoint directory, in place.

    The full state is `state.npz`. Older runs (and any run killed before the
    first checkpoint under the new code) only left the three bare `.npy` files,
    so those are accepted as a fallback: weights and ladder carry over, the Adam
    moments restart from zero. That costs a few generations of re-warming the
    optimiser, which is far cheaper than discarding the ladder -- rebuilding a
    12-rung opponent pool is what actually takes hours.
    """
    npz = os.path.join(run_dir, "state.npz")
    if os.path.isfile(npz):
        d = np.load(npz)
        # The yardstick this checkpoint's `best_abs` was earned against, read
        # before anything below rebuilds the ladder. `ckpt_rungs` is the
        # fallback for checkpoints written before the signature: it is set even
        # when the signature is missing, and its being set at all is how
        # `reset_best_if_ladder_changed` tells a state.npz resume from a cold
        # start or a bare-.npy one (which restores no best at all).
        tr.ckpt_ladder = (json.loads(str(d["ladder_sig"]))
                          if "ladder_sig" in d else None)
        tr.ckpt_rungs = int(np.asarray(d["archetypes"]).shape[0]) \
            if "archetypes" in d else 0
        def fit(a, what):
            return _fit_layout(a, run_dir, what)

        old_n = int(d["theta"].shape[-1])
        tr.theta = jnp.asarray(fit(d["theta"], "theta"))
        tr.champion = jnp.asarray(fit(d["champion"], "champion"))
        tr.champion_score = _legacy_none(float(d["champion_score"]))
        tr.pool = [jnp.asarray(x) for x in fit(d["pool"], "pool")]
        tr.m, tr.v = jnp.asarray(fit(d["m"], "m")), jnp.asarray(fit(d["v"], "v"))
        tr.t = int(d["t"])
        # Checkpoints written before `adam_t` existed used `t` for the bias
        # correction, so falling back to `t` continues exactly the trajectory
        # they were on -- which for a checkpoint whose moments are warm (all of
        # them, bar one written in the few generations after a clear) is the
        # trajectory anyone resuming one wants.
        tr.adam_t = int(d["adam_t"]) if "adam_t" in d else tr.t
        tr.key = jax.random.wrap_key_data(jnp.asarray(d["key"]))
        if "archetypes" in d and d["archetypes"].shape[0] > 0:
            tr.archetypes = [jnp.asarray(a) for a in fit(d["archetypes"], "archetypes")]
            # Names come back with the thetas because `--rung-weight` and
            # `--proxy-handicap` are stated *by name*: without them a resumed
            # run would weight rung 3 rather than `mixed_ranch`. Checkpoints
            # written before this field fall back to `reprobe_archetypes`'
            # positional `rung{i}` labels, which is why a weighted resume of one
            # of those is refused by name rather than mis-applied.
            if "archetype_names" in d:
                tr.archetype_names = [str(x) for x in d["archetype_names"]]
            # The set just swapped underneath the probe `Trainer.__init__` ran,
            # and a checkpoint older than 2026-08-25 carries the dead
            # `wheat_farmer`. Re-measure, and refuse rather than resume a
            # yardstick with a 0-coin rung in it.
            tr.reprobe_archetypes()
        if "best_abs_theta" in d:
            tr.best_abs = _legacy_none(float(d["best_abs"]))
            tr.best_abs_theta = jnp.asarray(fit(d["best_abs_theta"], "best_abs_theta"))
            # Checkpoints written before the gate existed carry no holdout for
            # their record. `-inf` is the honest value for "not measured": it
            # lets the first record of the resumed run be taken on its
            # selection number alone, which is what the run that wrote the
            # checkpoint was doing anyway, and every record after it is gated.
            tr.best_hold = float(d["best_hold"]) if "best_hold" in d else NO_BEST
        # Checkpoints written before `--best-replicate` refused nothing, which
        # is what 0 says.
        tr.replicate_rejects = int(d["replicate_rejects"]) \
            if "replicate_rejects" in d else 0
        # Checkpoints written before `--slot-rotation` carry no credit, and a
        # resume that changed the ladder's width gets it re-centred rather than
        # mis-aligned (`SlotCarry.resize`). Both are a rotation that restarts,
        # which is only ever one generation's worth of unfairness.
        if tr.slot_carry is not None and "slot_credit" in d:
            c = np.asarray(d["slot_credit"], float)
            if c.size:
                tr.slot_carry.credit = c
        # Sigma is trainer state, not config, once --restart-sigma-on-stall can
        # double it: resuming from `cfg.sigma` alone would silently undo the
        # restart and put the run back in the basin it just climbed out of.
        # What carries over is the *restart count*, applied on top of whatever
        # `--sigma` this invocation asks for -- so an operator who resumes with
        # a deliberately larger sigma still gets it, and a restarted run
        # resumed with the same flags is unchanged.
        #
        # The multiplier comes from *this* invocation's `--stall-sigma-mult`
        # rather than the checkpoint, for the same reason `--sigma` does: it is
        # the knob an operator reaches for precisely when the restart the
        # checkpoint recorded was the wrong size. Same flags, same sigma; a
        # resume that lowers the multiplier lowers the restored sigma with it.
        #
        # The exponent is the count of restarts that *stepped* sigma, not of
        # restarts: at `--stall-sigma-mult 1.0` the restart is a pure jump back
        # onto `best_abs_theta` and repeats, so its count is not a number of
        # step-ups and raising it to a new multiplier's power would return a
        # five-times-jumped run at 32x its own sigma. Checkpoints written
        # before the field fall back to the restart count, which is what they
        # meant: back then the restart could only fire once.
        if "sigma_restarts" in d:
            tr.sigma_restarts = int(d["sigma_restarts"])
            tr.sigma_steps = int(d["sigma_steps"]) if "sigma_steps" in d \
                else tr.sigma_restarts
            tr.last_improve = int(d["last_improve"])
            tr.sigma = float(tr.cfg.sigma) * (
                float(tr.cfg.stall_sigma_mult) ** tr.sigma_steps)
        # The host generator draws the episode seeds, the warm starts and the
        # market jitter. Left out of the checkpoint it restarts from `--seed`
        # and the resumed run replays generations 1..k's seeds -- CRN's
        # between-generation resampling silently lost after every resume.
        # Checkpoints older than this field fall back to the seeded stream.
        if "rng_state" in d:
            tr.rng.bit_generator.state = json.loads(str(d["rng_state"]))
        elapsed = float(d["elapsed"]) if "elapsed" in d else 0.0
        # After the ladder is whole (`reprobe_archetypes` above extended it by
        # the flow rung and rebound the weights), so the comparison is against
        # the ladder this run will actually measure on.
        reset_best_if_ladder_changed(tr)
        how = "state.npz"
        if old_n != PO.N_PARAMS:
            how += f" (zero-padded {old_n} -> {PO.N_PARAMS} params)"
        return int(d["gen"]), how, elapsed

    theta_p = os.path.join(run_dir, "theta.npy")
    if not os.path.isfile(theta_p):
        raise SystemExit(f"--resume {run_dir}: no state.npz and no theta.npy")
    tr.theta = jnp.asarray(_fit_layout(np.load(theta_p), run_dir, "theta"))
    champ_p = os.path.join(run_dir, "champion.npy")
    if os.path.isfile(champ_p):
        tr.champion = jnp.asarray(_fit_layout(np.load(champ_p), run_dir, "champion"))
    pool_p = os.path.join(run_dir, "pool.npy")
    if os.path.isfile(pool_p):
        tr.pool = [jnp.asarray(x)
                   for x in _fit_layout(np.load(pool_p), run_dir, "pool")]
    # Unknown against the ladder we are about to keep training against, so let
    # the next champion measurement establish it rather than trusting a score
    # earned against a pool we cannot verify.
    tr.champion_score = NO_BEST
    return 0, "legacy .npy (Adam state reset)", 0.0


#: The encoder trunk `--trunk-from` carries across a lineage break. `dh` is the
#: residual-drain input block and belongs with `w1`; `ds` does not -- it writes
#: straight onto the grow and sell scores, which is a head.
TRUNK_BLOCKS = ("w1", "b1", "g1", "gb1", "dh")


def install_init_theta(tr, init):
    """Make `init` the theta this lineage starts from -- everywhere it lives.

    `Trainer.__init__` seats its random He-init theta on ladder rung 0
    (`self.pool = [self.theta]`) and `_snapshot` never evicts rung 0, so a run
    that only replaced `tr.theta` kept playing 12 of every 64 episodes against
    a policy nobody chose: flow96-flow105 (2026-09-04/05) all spent that share
    on a random opponent. The init theta is the anti-collapse anchor the gate
    compares against, so it is what rung 0 has to hold -- the same rule
    `warm_trunk` already applies.
    """
    tr.theta = jnp.asarray(init)
    # A cold start holds "best_abs_theta is the current theta"; keep it.
    tr.best_abs_theta = tr.theta
    if getattr(tr, "pool", None):
        tr.pool[0] = tr.theta


def warm_trunk(tr, path):
    """Copy an older theta's encoder trunk (`TRUNK_BLOCKS`) into a fresh
    lineage; every head stays at its fresh init -- the re-typed outputs
    (section 2) must not inherit biases trained under the old decode.

    Rung 0 of the ladder is rebound too. `Trainer.__init__` seeds
    `self.pool = [self.theta]`, so without that the pool's first opponent
    would stay the *un-warmed* init while `tr.theta` moved -- a rung the run
    never meant to keep, and one that quietly makes the early win rates look
    better than they are.
    """
    old = np.load(path)
    if old.ndim != 1:
        raise SystemExit(
            f"--trunk-from {path}: expected a flat theta vector, got shape "
            f"{old.shape}. A checkpoint directory's state.npz or a stacked "
            f"pool.npy is not a theta -- pass that run's theta.npy.")
    old = old.astype(np.float32)
    new = np.asarray(tr.theta).copy()
    for name in TRUNK_BLOCKS:
        off = PO.offset(name)
        n = int(np.prod(dict(PO.SHAPES)[name]))
        if off >= old.shape[0]:
            # An older layout that predates this block entirely: it is a prefix
            # of the current one, so there is nothing to carry across and the
            # fresh init stands. `dh` is the first trunk block this can happen
            # to -- warming from any pre-2026-08-26 theta hits it.
            continue
        if off + n > old.shape[0]:
            raise SystemExit(
                f"--trunk-from {path}: theta ends inside block {name} "
                f"({old.shape[0]} params). A shorter *layout* ends between "
                f"blocks; ending inside one means the file is truncated.")
        new[off:off + n] = old[off:off + n]
    tr.theta = jnp.asarray(new)
    if getattr(tr, "pool", None):
        tr.pool[0] = tr.theta


def add_anchor_rungs(tr, anchors, weights):
    """Pin each `--rung-theta` theta into `tr.archetypes` as a named rung.

    Appended *after* the ladder, and after `--resume` has restored it, so every
    hand-set rung keeps its index and the yardstick's existing per-rung columns
    keep their meaning. A name already in the ladder rebinds that rung's theta
    instead of appending a second copy: the anchor round-trips through
    `state.npz` with the rest of the archetypes, so a resumed run passing the
    same flags has to be idempotent.

    `reprobe_archetypes` then re-runs the liveness probe over the whole set.
    That is not belt and braces -- it rebinds `rung_weights` (the anchor's
    default 0 among them) and refills `archetype_coins`, which
    `absolute_report` requires to be the same length as `archetypes` or every
    `keep` ratio silently reads 0 and `--collapse-floor` drops the ladder.
    """
    tr.cfg = tr.cfg._replace(rung_weight=tuple(tr.cfg.rung_weight) + tuple(weights))
    for name, path in anchors:
        arr = np.load(path)
        if arr.ndim != 1:
            raise SystemExit(
                f"--rung-theta {name}={path}: expected a flat theta vector, got "
                f"shape {arr.shape}. A stacked pool.npy is not a theta.")
        theta = jnp.asarray(_fit_layout(arr.astype(np.float32), path,
                                        f"the --rung-theta {name} anchor"))
        if name in tr.archetype_names:
            tr.archetypes[tr.archetype_names.index(name)] = theta
        else:
            tr.archetype_names.append(name)
            tr.archetypes.append(theta)
    tr.reprobe_archetypes()
    # An anchor appends a rung and re-divides every weight, so it moves the
    # yardstick exactly as the flow rung does; same rule.
    return reset_best_if_ladder_changed(tr)


def record_theta_ready(best_abs, gate):
    """Has `best_abs_theta` earned `best_abs.npy`? -> bool

    Two different questions wearing one name, and conflating them cost
    flow150 its record. Ungated, `best_abs_theta` moves only when
    `_accept_best` moves `best_abs`, so "a measurement has happened" IS
    `math.isfinite(best_abs)` -- without it the file would ship the untrained
    init.

    Under `--real-gate` the two come apart. `best_abs` is the *in-sim*
    threshold, which keeps moving so a gate rejection cannot wedge the
    nomination stream; `best_abs_theta` is the *gated* record, and
    `Trainer._poll_real_gate` is its only writer. So `gate.have_record` --
    "the real engine has accepted something" -- is the whole of the question,
    and `and math.isfinite(best_abs)` on top of it is the ungated rule applied
    to a quantity that no longer governs the file.

    They disagree on exactly the resume that retires the in-sim record: a
    ladder change or `--reset-best` puts `best_abs` back to `NO_BEST` while
    `setup_real_gate` hands the gate its record theta back out of
    `best_abs.npy` and re-arms `have_record`. A run in that state accepts
    records normally -- the log says "-> best_abs.npy" and `best_abs_theta`
    does move -- and every checkpoint after it refuses to write the file,
    because `best_abs` is still the sentinel. That is the only way flow150
    could log an ACCEPT at gen 42 and leave `best_abs.npy` byte-identical to
    its init, and the cost is not cosmetic: the run's deliverable stays the
    init theta, and the next resume reads that file back as the theta the bar
    was measured on and pairs every verdict against it (`RealGate.load`).
    """
    if gate is not None:
        return bool(gate.have_record)
    return math.isfinite(best_abs)


def save_state(run_dir, tr, gen, elapsed=0.0):
    """One self-consistent snapshot of the whole trainer, written atomically.

    `elapsed` is the run's cumulative wall-clock across every resume, so the
    budget disclosure section 7 asks for reads off the last log line instead
    of being summed by hand over segments."""
    tmp = os.path.join(run_dir, "state.npz.tmp")
    with open(tmp, "wb") as fh:
        np.savez(fh, theta=np.asarray(tr.theta), champion=np.asarray(tr.champion),
                 champion_score=np.float64(tr.champion_score),
                 pool=np.asarray(jnp.stack(tr.pool)),
                 archetypes=(np.asarray(jnp.stack(tr.archetypes)) if tr.archetypes
                             else np.zeros((0, tr.n), np.float32)),
                 # A fixed width, so an empty ladder still round-trips (`np.str_`
                 # on `[]` lands on a zero-width dtype `savez` cannot restore).
                 archetype_names=np.array(list(tr.archetype_names), dtype="<U64"),
                 # What `best_abs` below was measured against, so a resume that
                 # changes the ladder can tell that it did -- see
                 # `reset_best_if_ladder_changed`.
                 ladder_sig=np.str_(json.dumps(ladder_signature(tr))),
                 m=np.asarray(tr.m), v=np.asarray(tr.v), t=np.int64(tr.t),
                 # Separate from `t`: how many steps the *current* `m`/`v` have
                 # taken, which is what Adam's bias correction divides by.
                 adam_t=np.int64(tr.adam_t),
                 key=np.asarray(jax.random.key_data(tr.key)), gen=np.int64(gen),
                 best_abs=np.float64(tr.best_abs), best_abs_theta=np.asarray(tr.best_abs_theta),
                 # The holdout half's number for that same theta, so a resume
                 # under `--best-gate both` gates against the record it
                 # inherited and not against a fresh `-inf`.
                 best_hold=np.float64(tr.best_hold),
                 rng_state=np.str_(json.dumps(tr.rng.bit_generator.state)),
                 sigma=np.float64(tr.sigma), sigma_restarts=np.int64(tr.sigma_restarts),
                 # How many of those restarts multiplied sigma, which is what a
                 # resume rebuilds it from. The two differ only at
                 # `--stall-sigma-mult 1.0`, where the restart repeats.
                 sigma_steps=np.int64(getattr(tr, "sigma_steps", tr.sigma_restarts)),
                 last_improve=np.int64(tr.last_improve),
                 # How many candidates `--best-replicate` refused. Run state,
                 # not a derived one: it counts the times this run's screening
                 # measurement was a lucky reading, and a resume that restarted
                 # it at 0 would make the flag look free on the second segment
                 # of every long run.
                 replicate_rejects=np.int64(getattr(tr, "replicate_rejects", 0)),
                 # `--slot-rotation carry`'s running credit, one entry per
                 # rung. Run state, not config: it is *where in the rotation*
                 # the ladder is, and a resume that restarted it at zero would
                 # hand the low-numbered rungs the leftovers all over again --
                 # which is the defect the rotation exists to remove. An empty
                 # array under `--slot-rotation fixed`.
                 slot_credit=(np.asarray(tr.slot_carry.credit, np.float64)
                              if tr.slot_carry is not None
                              else np.zeros(0)),
                 elapsed=np.float64(elapsed))
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, os.path.join(run_dir, "state.npz"))


#: `--residual`: the FROZEN residual action head [ACTIONRL8], flown by the sim
#: rollout's seat 0 while ES searches theta around it -- the theta pass of the
#: alternating loop. Module level so the head module and its (constant) params
#: are loaded once and closed over by the hook the whole run traces through.
RESIDUAL_HEAD_PY = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "S", "actionrl", "head.py")


def arm_residual_sim(head_npz, head_py=None):
    """Install the frozen head as `plan.RESIDUAL_FN` for the SIM rollout.

    Called once, before anything traces: `plan.residual_on()` is read at trace
    time (`plan.build_day`), so the hook has to be in place before the first
    `jax.jit` of `sim.rollout.episode` and it is then compiled into every
    program the run uses -- the population evaluation, the archetype probe and
    the absolute report alike. The head is FROZEN, so its weights are device
    constants and there is no per-generation re-trace.

    GREEDY, not sampled. `S/actionrl/ppo.py` samples because it is training the
    head and needs the log-prob of the action it took; this pass trains THETA
    against a head that is already chosen, and the agent that will be judged
    and shipped is `head.numpy_fn` -- argmax per slot, deterministic
    (`package_submission.py --residual`). Sampling here would optimise theta
    against a policy nobody flies.

    SEAT. `plan.RESIDUAL_FN` is module level and has no seat argument, and
    `rollout.run_day` builds the two seats' days in one list comprehension,
    seat 0 (ours) first and seat 1 (the tape / self-play opponent) second. So
    the hook counts its calls and hands every SECOND one `head.noop_override`,
    i.e. the plain shipped planner -- ACTIONRL6's fix, the same contract
    `head.jax_fn` implements for PPO, written as a parity rather than a
    one-shot latch because `rollout.episode` traces two day bodies (the scan
    and the shortened last day) and a latch would leak the head into the
    opponent of the second one. Every traced day contributes exactly two calls
    in that order, so the parity is the seat index.
    """
    import importlib.util
    from kagg3.core import plan as PL
    path = os.path.abspath(head_py or RESIDUAL_HEAD_PY)
    if not os.path.isfile(path):
        raise SystemExit(f"--residual: no head module at {path}")
    sp = importlib.util.spec_from_file_location("kagg3_residual_head", path)
    HEAD = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(HEAD)
    raw = HEAD.load(head_npz)
    # The feature vector is the contract between the two halves: a head trained
    # against a different width is a different head, and under `jit` a silent
    # broadcast would be a wrong number rather than an error.
    if int(HEAD.N_FEAT) != int(PL.RESIDUAL_N_FEAT) or \
            int(raw["w1"].shape[0]) != int(PL.RESIDUAL_N_FEAT):
        raise SystemExit(
            f"--residual {head_npz}: feature width "
            f"{int(raw['w1'].shape[0])} / head.N_FEAT {int(HEAD.N_FEAT)} vs "
            f"plan.RESIDUAL_N_FEAT {int(PL.RESIDUAL_N_FEAT)}")
    params = {k: jnp.asarray(v, jnp.float32) for k, v in raw.items()}
    seen = [0]

    def fn(obs_features, macro_fields):
        seen[0] += 1
        if seen[0] % 2 == 0:                       # seat 1: the plain planner
            return HEAD.noop_override(jnp)
        feats = jnp.asarray(obs_features, jnp.float32).reshape(-1)
        logits = HEAD.forward(jnp, params, feats)
        return HEAD.decode(jnp, HEAD.greedy_acts(jnp, logits))

    PL.RESIDUAL_ON = True
    PL.RESIDUAL_HEAD = os.path.abspath(head_npz)
    PL.RESIDUAL_FN = fn
    if not PL.residual_on():
        raise SystemExit(f"--residual {head_npz}: the head did not arm")
    print(f"residual: {head_npz} armed on sim seat 0 "
          f"({HEAD.n_params(raw):,} params, greedy, frozen); module {path}",
          flush=True)
    return HEAD


def setup_real_gate(args, tr, out, resume_dir=None):
    """Attach the real-engine record gate to `tr` (`--real-gate`), or `None`.

    Called once the ladder is final and any `--resume` has been restored,
    because two of the three things it needs come from there: the record theta
    it has to establish a baseline for, and the gate's own saved state.

    The baseline is the subtle half. The gate accepts a candidate only if it
    beats the incumbent's *real* numbers, so the incumbent has to have some;
    a run that inherits a record from a checkpoint written without the flag
    has none, and its first candidate would walk in against nothing. So that
    record is nominated first. It is nominated, not waited on: it takes the
    single slot, and the run's first in-sim candidate waits behind it in the
    one pending place.
    """
    if not args.real_gate:
        if getattr(args, "real_gate_every", 0):
            raise SystemExit("--real-gate-every requires --real-gate: without "
                             "the gate there is nothing to nominate to.")
        if getattr(args, "real_gate_replicate", False) or \
                getattr(args, "real_gate_reset", False) or \
                getattr(args, "real_gate_fresh", False) or \
                getattr(args, "real_gate_recentre", 0):
            raise SystemExit("--real-gate-replicate, --real-gate-reset and "
                             "--real-gate-recentre require --real-gate: there "
                             "is no gate to replicate for, reset, or be "
                             "steered by.")
        if getattr(args, "real_gate_replicate_games", None) is not None:
            raise SystemExit("--real-gate-replicate-games requires "
                             "--real-gate: there is no replicate round "
                             "without the gate that runs one.")
        if getattr(args, "real_gate_paired_t", 0.0):
            raise SystemExit("--real-gate-paired-t requires --real-gate: it "
                             "is the significance test the gate's own paired "
                             "rounds are decided by, and without the gate "
                             "there are no rounds.")
        if getattr(args, "real_gate_min_gain", 0.0):
            raise SystemExit("--real-gate-min-gain requires --real-gate: it "
                             "is the size of the improvement the gate insists "
                             "on, and without the gate nothing is measured to "
                             "insist about.")
        if getattr(args, "real_gate_win_floor", None) is not None:
            raise SystemExit("--real-gate-win-floor requires --real-gate: it "
                             "is the win-rate drop the gate refuses to trade "
                             "for coins, and without the gate nothing is "
                             "measured to trade.")
        if getattr(args, "keep_candidates", False):
            raise SystemExit("--keep-candidates requires --real-gate: it keeps "
                             "the thetas the gate is handed, and without the "
                             "gate nothing is handed to one.")
        if getattr(args, "real_gate_pinned", None):
            raise SystemExit("--real-gate-pinned requires --real-gate: it is "
                             "the set the gate judges on, and without the "
                             "gate nothing is judged.")
        if getattr(args, "real_gate_min_flips", 1) != 1:
            raise SystemExit("--real-gate-min-flips requires --real-gate: it "
                             "is how many live games a candidate has to turn "
                             "round before the gate moves the record.")
        if int(getattr(args, "real_gate_pinned_seats", 2)) != 2:
            raise SystemExit("--real-gate-pinned-seats requires --real-gate: "
                             "it is how many seats of each pinned board the "
                             "gate's own eval plays, and without the gate "
                             "there is no eval.")
        if getattr(args, "real_gate_seed_per_opponent", False):
            raise SystemExit("--real-gate-seed-per-opponent requires "
                             "--real-gate: it is how the gate's own eval draws "
                             "its seeds, and without the gate there is no "
                             "eval.")
        return None
    if getattr(args, "real_gate_every", 0) < 0:
        raise SystemExit("--real-gate-every must be >= 0 (0 = off).")
    if getattr(args, "real_gate_fresh", False) and not getattr(
            args, "real_gate_replicate", False):
        # The paired decision is confirmed on a *second* fresh base; without
        # the replicate there is no second round and the record would be taken
        # on one paired reading, which is the noise the replicate exists for.
        raise SystemExit("--real-gate-fresh requires --real-gate-replicate: "
                         "the confirmation is the second fresh base.")
    if getattr(args, "real_gate_recentre", 0) and not args.real_gate_every:
        # It counts refusals of *periodic* candidates, and without the cadence
        # there are none: the counter would never move and the flag would be a
        # silent no-op for the length of the run.
        raise SystemExit("--real-gate-recentre requires --real-gate-every: it "
                         "counts refused centre candidates, and only the "
                         "cadence produces those.")
    # A comma-separated *field*: one packaged agent is one thing to overfit,
    # and the evaluator plays every member of the field on the same seeds into
    # the one CSV the gate pools. A single path is the field of one it was.
    field = RealGate.as_field(args.real_gate_opponent)
    if not field:
        raise SystemExit("--real-gate-opponent: expected at least one main.py "
                         "(comma-separated for a field of them).")
    for one in field:
        if not os.path.isfile(one):
            raise SystemExit(
                f"--real-gate-opponent {one}: no such file. "
                f"The gate seats a packaged agent in the real engine, so this "
                f"has to be a main.py, and the path is resolved from the repo "
                f"root. The flag takes a comma-separated field of them.")
    if args.real_gate_games < 1 or args.real_gate_workers < 1:
        raise SystemExit("--real-gate-games and --real-gate-workers must both "
                         "be at least 1.")
    if (getattr(args, "real_gate_paired_t", 0.0) or 0.0) < 0:
        raise SystemExit("--real-gate-paired-t must be >= 0 (0 = off).")
    rg = getattr(args, "real_gate_replicate_games", None)
    if rg is not None and int(rg) < 1:
        raise SystemExit("--real-gate-replicate-games must be >= 1 (omit it "
                         "to play --real-gate-games on the replicate too).")
    if rg is not None and not getattr(args, "real_gate_replicate", False):
        raise SystemExit("--real-gate-replicate-games requires "
                         "--real-gate-replicate: without it there is no "
                         "replicate round to size.")
    pinned = getattr(args, "real_gate_pinned", None) or None
    if pinned is not None and not os.path.isfile(pinned):
        raise SystemExit(
            f"--real-gate-pinned {pinned}: no such file. It is the town "
            f"schedule a scripts/tape_opponent.py --with-town run wrote -- a "
            f"JSON object keyed by episode id -- and the path is resolved "
            f"from the repo root.")
    if int(getattr(args, "real_gate_min_flips", 1)) < 0:
        raise SystemExit("--real-gate-min-flips must be >= 0 (0 = a candidate "
                         "that flips nothing may still take the record on the "
                         "strict win count).")
    if int(getattr(args, "real_gate_min_flips", 1)) != 1 and pinned is None:
        raise SystemExit("--real-gate-min-flips requires --real-gate-pinned: "
                         "flips are games of the pinned live-replica set that "
                         "changed hands, and an unpinned leg draws different "
                         "games every round so there is nothing to flip.")
    if int(getattr(args, "real_gate_pinned_seats", 2)) != 2 and pinned is None:
        # Only a pinned board is seat-invariant. On a drawn one the two seats
        # are two different games and the pair is what cancels the seat bias,
        # so dropping a seat there would not save a measurement -- it would
        # throw half of one away.
        raise SystemExit("--real-gate-pinned-seats requires "
                         "--real-gate-pinned: only a pinned board returns the "
                         "same coins in either seat, and on a drawn one the "
                         "second seat is the half of the pair that cancels "
                         "the seat bias.")
    if (getattr(args, "real_gate_paired_t", 0.0) or 0.0) > 0 and pinned is None \
            and not getattr(args, "real_gate_fresh", False):
        raise SystemExit("--real-gate-paired-t requires --real-gate-fresh: "
                         "only a fresh round plays the incumbent on the "
                         "candidate's own seed base, and without that second "
                         "leg there is no game to pair with.")
    if (getattr(args, "real_gate_min_gain", 0.0) or 0.0) < 0:
        raise SystemExit("--real-gate-min-gain must be >= 0 (0 = the strict "
                         "rule: any improvement takes the record).")
    win_floor = getattr(args, "real_gate_win_floor", None)
    if win_floor is not None:
        # Only the margin metric drops the win rate from the decision, so only
        # it has a win rate to put a floor under. Under `win` the flag would
        # be a no-op on a rule the win rate already decides, which is worse
        # than an error: it reads like a protection that is not there.
        if args.real_gate_metric != "margin":
            raise SystemExit(
                "--real-gate-win-floor requires --real-gate-metric margin: "
                "the win metric already ranks on the win rate, so there is "
                "nothing for a floor to protect (use --real-gate-min-gain to "
                "ask that metric for a bigger gap).")
        if win_floor < 0:
            raise SystemExit("--real-gate-win-floor must be >= 0 (0 = the win "
                             "rate may not drop at all; omit the flag for no "
                             "floor).")
    gate = RealGate(out, field,
                    games=args.real_gate_games,
                    workers=args.real_gate_workers,
                    seed_base=args.real_gate_seed_base,
                    metric=args.real_gate_metric,
                    every=getattr(args, "real_gate_every", 0),
                    replicate=getattr(args, "real_gate_replicate", False),
                    recentre=getattr(args, "real_gate_recentre", 0),
                    fresh=getattr(args, "real_gate_fresh", False),
                    fresh_seed=getattr(args, "seed", 0) or 0,
                    min_gain=getattr(args, "real_gate_min_gain", 0.0) or 0.0,
                    paired_t=getattr(args, "real_gate_paired_t", 0.0) or 0.0,
                    replicate_games=getattr(
                        args, "real_gate_replicate_games", None),
                    pinned=pinned,
                    min_flips=int(getattr(args, "real_gate_min_flips", 1)),
                    pinned_seats=int(getattr(args, "real_gate_pinned_seats",
                                             2)),
                    win_floor=win_floor,
                    seed_per_opponent=getattr(
                        args, "real_gate_seed_per_opponent", False),
                    # The frozen head travels with the candidate: the gate has
                    # to play the agent the packager would ship [ESHEAD1].
                    residual=getattr(args, "residual", None),
                    residual_head_py=getattr(args, "residual_head_py", None))
    if getattr(args, "keep_candidates", False):
        # Attached after construction rather than passed in: it is a place to
        # write copies, not part of what the gate measures, so it stays out of
        # the constructor, out of `real_gate.json` and out of every resume
        # comparison the flags above go through.
        gate.keeper = CandidateKeeper(out)
    had = None
    if resume_dir:
        had = gate.load(resume_dir, fit=lambda a: _fit_layout(
            a, resume_dir, "the pending real-gate candidate"))
        sim = os.path.join(resume_dir, "best_sim.npy")
        if os.path.isfile(sim):
            tr.best_sim_theta = jnp.asarray(
                _fit_layout(np.load(sim), resume_dir, "best_sim"))
    if had is not None:
        saved = RealGate.field_of(had)
        if saved and saved != gate.opponents and not getattr(
                args, "real_gate_reset", False):
            # The bar is a measurement against a *field*, so a segment that
            # changes the field is comparing this field's reading against the
            # last one's -- which is not a comparison at all. Refuse, rather
            # than let the record drift onto games nobody meant to change.
            raise SystemExit(
                f"--real-gate-opponent {','.join(gate.opponents)}: the resumed "
                f"gate's bar was measured against {','.join(saved)}. The two "
                f"numbers are not comparable; pass --real-gate-reset to drop "
                f"the saved bar and re-measure the record theta against this "
                f"field, or resume with the field the bar was taken on.")
        saved_gain = RealGate.min_gain_of(had)
        if saved_gain != gate.min_gain:
            # Not a refusal, unlike the field above. The field is part of what
            # the bar *is* -- change it and the saved number stops being a
            # comparable measurement -- whereas the threshold is only how much
            # of a gap this segment wants to see before it moves the record.
            # A segment is entitled to change its mind about that; it just
            # should not do so silently, because the acceptance rate of the
            # rows in log.jsonl changes with it.
            print(f"[real gate: acceptance threshold "
                  f"{saved_gain:g} -> {gate.min_gain:g} "
                  f"({'win-rate points' if gate.metric == 'win' else 'coins'})"
                  f"; the saved bar itself is unchanged]", flush=True)
        saved_t = RealGate.paired_t_of(had)
        if saved_t != gate.paired_t:
            # A threshold like the two above, and legal to change mid-run for
            # the same reason: it is what this segment insists on seeing, not
            # part of what the saved bar measured.
            print(f"[real gate: paired t threshold "
                  f"{saved_t:g} -> {gate.paired_t:g}"
                  f"; the saved bar itself is unchanged]", flush=True)
        saved_floor = RealGate.win_floor_of(had)
        if saved_floor != gate.win_floor:
            # Same reasoning as the threshold above: a floor is what this
            # segment will tolerate, not part of what the bar measured, so the
            # change is legal and only has to be said out loud -- the rows
            # after this line are accepted under a different rule. `None` and
            # 0.0 are different settings and print differently.
            print(f"[real gate: win floor "
                  f"{'off' if saved_floor is None else f'{saved_floor:g}'}"
                  f" -> "
                  f"{'off' if gate.win_floor is None else f'{gate.win_floor:g}'}"
                  f"; the saved bar itself is unchanged]", flush=True)
        saved_spo = RealGate.seed_per_opponent_of(had)
        if saved_spo != gate.seed_per_opponent:
            # Also not a refusal. It changes which seeds the *next* leg draws,
            # so the saved bar stays the measurement it was -- but a bar taken
            # on one shared seed list and a challenger taken on a list per
            # opponent are two different draws, and the acceptance rate of the
            # rows after this line changes with it.
            print(f"[real gate: seeds "
                  f"{'per opponent' if saved_spo else 'shared'} -> "
                  f"{'per opponent' if gate.seed_per_opponent else 'shared'}"
                  f"; the saved bar itself is unchanged]", flush=True)
        saved_pinned = had.get("pinned")
        if (saved_pinned or None) != gate.pinned:
            # Unlike the thresholds above this one IS part of what the bar
            # measured -- a pinned bar is a count over one fixed set of live
            # replicas and an unpinned one is a mean over a seed draw -- so
            # the note says the numbers are not comparable. It is not a
            # refusal (the field check above already covers the case where the
            # opponents themselves changed), but the first candidate after
            # this line is judged against a bar from a different measurement,
            # and --real-gate-reset is the way to re-take it.
            print(f"[real gate: pinned set "
                  f"{saved_pinned or 'off'} -> {gate.pinned or 'off'}"
                  f"; the saved bar was taken on the other one -- "
                  f"--real-gate-reset re-measures the record here]",
                  flush=True)
        saved_seats = int(had.get("pinned_seats") or 2)
        if gate.pinned and saved_seats != gate.pinned_seats:
            # Part of what the bar IS, like the pinned set itself: a bar taken
            # on 2N games and one taken on N boards are the same rates but
            # different counts, and `--real-gate-min-flips` is read in counts.
            print(f"[real gate: pinned seats {saved_seats} -> "
                  f"{gate.pinned_seats}; the saved bar was counted over the "
                  f"other one -- its rates carry over, its game count does "
                  f"not]", flush=True)
        saved_flips = int(had.get("min_flips") or 1)
        if gate.pinned and saved_flips != gate.min_flips:
            # A threshold, like --real-gate-min-gain: the command line owns it
            # and a segment may change it, out loud.
            print(f"[real gate: min flips {saved_flips} -> {gate.min_flips}"
                  f"; the saved bar itself is unchanged]", flush=True)
    if gate.pinned:
        # Said at startup, not only in real_gate.log: pinned mode changes what
        # the gate measures (a fixed set of live replicas, not a seed draw) and
        # silently makes half a dozen flags on the command line inert, so the
        # operator reads which ones before the run rather than after it.
        print(f"[real gate: PINNED on {gate.pinned} -- "
              f"{len(gate.opponents)} opponents x {gate.seats} seat"
              f"{'' if gate.seats == 1 else 's'} = "
              f"{len(gate.opponents) * gate.seats} deterministic games a leg, "
              f"seed base "
              f"{gate.seed_base}; accept on net flips >= {gate.min_flips}"
              + ("" if gate.metric == "win"
                 else f" (metric margin: min gain {gate.min_gain:g} coins)")
              + "]", flush=True)
        if gate.pinned_ignored:
            print("[real gate: pinned mode ignores "
                  + ", ".join(gate.pinned_ignored)
                  + " -- the game is deterministic, so a seed count, a "
                    "replicate and a significance test all answer a lottery "
                    "that is not being run]", flush=True)
        try:
            with open(gate.pinned) as fh:
                keys = json.load(fh)
            keys = list(keys) if isinstance(keys, dict) else []
        except (OSError, ValueError):
            keys = []
        if keys:
            loose = [o for o in gate.opponents
                     if not any(k != "default" and k in o for k in keys)]
            if loose:
                # Not a refusal: an unpinned tape still plays, it just draws
                # its own town and stops being a replica of the live game --
                # which is the whole reason the set is deterministic.
                print(f"[real gate: {len(loose)} of {len(gate.opponents)} "
                      f"opponents have NO entry in the schedule and will draw "
                      f"their own town: "
                      + ", ".join(loose[:4])
                      + (" ..." if len(loose) > 4 else "") + "]", flush=True)
    if had is not None and getattr(args, "real_gate_reset", False):
        # `--real-gate-reset`: the saved bar is dropped and the segment starts
        # as though the gate had never run here -- so the record theta is
        # re-nominated below and whatever it scores *now* becomes the bar. Any
        # nomination the checkpoint carried goes with it; it was nominated
        # against a number that no longer exists, and the run will nominate
        # again within `--abs-every` generations.
        gate.forget_incumbent()
        had = None
    tr.real_gate = gate
    retired = False
    if not math.isfinite(tr.best_abs) and gate.have_record:
        # The inherited record was retired between the resume and here (a
        # ladder change, or `--reset-best`), which put `best_abs_theta` back on
        # the live theta -- so the gate holds numbers but no longer holds the
        # theta that earned them. The bar stands, because it is a real-engine
        # number and the ladder change did not move the real engine; what goes
        # is the claim that `best_abs.npy` holds a gated record, which would
        # otherwise let the next in-sim record write an unmeasured theta there.
        # Only *because the theta is missing*, though -- if it turns up below
        # in `best_abs.npy` the record is whole again and this is undone.
        gate.have_record = False
        retired = True
    # A theta the run was *given* is a candidate like any other, and the gate
    # has to measure it before the search walks away from it. flow29 started
    # from a champion that pools 84.4% on the gate's two seed bases; the gate
    # never saw it, took gen 10's in-sim record (ten ES steps downhill, 70.8%
    # pooled) as its first bar, and `--real-gate-recentre` then pulled the
    # search back onto *that*. `best_abs_theta` is the init theta on a cold
    # start, so this is the same nomination the inherited-record path makes --
    # only the reason for having a theta worth measuring differs. `best_abs`
    # is still `NO_BEST` here and stays that way until the first in-sim
    # measurement; it is the in-sim threshold and has nothing to say about it.
    # Whose theta is the bar? Under `--real-gate` the gate is the only writer
    # of `best_abs.npy`, so the checkpoint's own file *is* the theta the
    # incumbent's numbers were measured on -- and it stays that theta across
    # the resume that retires the in-sim record, where `best_abs_theta` has
    # been put back on the live theta and is emphatically not it. flow27h
    # resumed with an 83.3% bar and no theta for it: `--real-gate-fresh` then
    # had nothing to pair against and decided its first verdicts off the
    # pooled fallback, which is the flag switched off. Only a missing file
    # leaves the bar theta-less (`_revert` and the pairing both cope).
    # `RealGate.load` has already read `best_abs.npy` for a resume whose state
    # claims a confirmed record; this is the rest of the cases -- a bar
    # inherited from a state that claims none, and a gate that was never
    # loaded at all.
    if gate.record_theta is None:
        gate.theta_source = "unknown"
        if gate.win is not None:
            best = (os.path.join(resume_dir, "best_abs.npy") if resume_dir
                    else None)
            if best is not None and os.path.isfile(best):
                gate.record_theta = np.asarray(
                    _fit_layout(np.load(best), resume_dir, "best_abs"),
                    np.float32)
                gate.theta_source = "best_abs.npy"
            elif gate.have_record:
                gate.record_theta = np.asarray(tr.best_abs_theta, np.float32)
                gate.theta_source = "best_abs_theta"
    if gate.theta_source == "best_abs.npy" and not gate.have_record:
        # The theta turned up, so the record is whole again: the
        # incumbent's real-engine numbers *and* the theta they were
        # measured on.
        # `have_record` went out above only because the pair was
        # broken; the file put the missing half back, so the claim it
        # withdrew is true again and both halves go back on.
        #
        # This is not bookkeeping. `have_record` is what arms
        # `RealGate.recentre_due` and `Trainer._gate_restart_check`,
        # so leaving it False after the theta has been found disarms
        # every route the run has back to the theta the real engine
        # actually prefers. flow30c resumed exactly here -- gate at
        # 0.807 from gen 80, `--real-gate-recentre 3` -- and sat
        # through 6 periodic rejections of its centre without one
        # recentre firing.
        #
        # `best_abs_theta` moves with it because the recentre and the
        # stall restart both jump to `best_abs_theta`
        # (`_restart_from_record`), and the retirement had left that
        # on the live centre they are trying to leave. It is still a
        # gate-measured theta -- it *is* `best_abs.npy`'s own contents
        # -- so the invariant behind the checkpoint's write guard
        # holds: with `best_abs` at `NO_BEST` the file is not rewritten
        # until an in-sim measurement lands, and when one does the
        # write puts the file back exactly as it found it.
        #
        # Keyed on `have_record` being off, not on *this* setup having
        # switched it off: flow30d resumed flow30c, whose own
        # real_gate.json already carried `have_record: false` from the
        # retirement one segment earlier, so a `retired`-only guard
        # left it off again and the run sat through 8 rejections.
        # Under `--real-gate` the gate is the only writer of
        # best_abs.npy, so a file found next to a saved bar is the
        # bar's theta whichever segment retired the in-sim record.
        tr.best_abs_theta = jnp.asarray(gate.record_theta)
        gate.have_record = True
    cold_init = bool(getattr(args, "init_theta", None)) and not resume_dir
    if gate.win is None and had is None and (math.isfinite(tr.best_abs)
                                             or cold_init):
        gate.propose(tr.best_abs_theta, tr.t)
    return gate


def _stop(*_):
    global STOP
    STOP = True
    print("\n[stop requested; checkpointing then exiting]", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", type=int, default=10000)
    ap.add_argument("--pop", type=int, default=128)
    ap.add_argument("--episodes", type=int, default=64)
    ap.add_argument("--sigma", type=float, default=0.02)
    ap.add_argument("--lr", type=float, default=0.02)
    ap.add_argument("--weight-decay", type=float, default=0.003, metavar="WD",
                    help="decoupled weight decay: theta <- (1 - WD) * theta "
                         "each generation, applied to every live column but "
                         "the head/aux biases (they are clipped to "
                         "--bias-clip's box instead). It sets the equilibrium "
                         "norm the run settles at, ~lr * sqrt(n / (2 * WD)), "
                         "so it is not independent of --lr: an A/B that moves "
                         "lr and leaves WD alone has moved the norm as well as "
                         "the step, and the two effects cannot be told apart "
                         "afterwards. Scale it as WD ~ lr^2 to hold the norm "
                         "(lr 0.02 -> 0.003 is the default pair; lr 0.005 "
                         "wants 0.0001875). Default 0.003.")
    ap.add_argument("--optimizer", choices=("adam", "sgd"), default="adam",
                    help="the ES step rule. 'adam' (default) divides by "
                         "sqrt(v) per coordinate, so *every* live coordinate "
                         "moves by about --lr each generation whether or not "
                         "its gradient carried any signal -- lr*sqrt(gens) of "
                         "random walk away from a seeded champion. 'sgd' is "
                         "plain momentum (m = beta1*m + (1-beta1)*grad; theta "
                         "+= lr*m): the step scales with the gradient "
                         "magnitude, so noise generations take small steps and "
                         "only a measured direction moves theta far. Decoupled "
                         "weight decay and the bias clip are unchanged. lr is "
                         "no longer scale-free under sgd and has to be retuned "
                         "to the gradient magnitude.")
    ap.add_argument("--train-only", default="all", metavar="SPEC",
                    help="restrict the ES update to a subset of theta. "
                         "'all' (default) is every live coordinate, i.e. the "
                         "behaviour of every run before this flag. 'biases' is "
                         "the head, aux and development biases (gb2/gb5/gb6) "
                         "-- the coordinates that state a discrete decision, "
                         "9 of them once the dead head slots are dropped. "
                         "'all-biases' widens that to every bias block in the "
                         "layout, including the heads appended since "
                         "(gb7/gb8/gb9/gb10/gb11) and the encoder's. A "
                         "comma-separated list of parameter-block names "
                         "(w1,b1,w2,b2,g1,gb1,g2,gb2,...,g11,gb11) names them "
                         "directly -- 'gp' is the global head's product "
                         "residual alone (864 coordinates), 'g11,gb11' the "
                         "forward-admit horizon gene alone (33), and "
                         "'g1,gb1,g11,gb11' moves that gene together with the "
                         "global head it reads. "
                         "Coordinates outside the subset are neither "
                         "perturbed nor stepped and stay exactly as loaded, "
                         "which is the point on a champion-seeded run.")
    ap.add_argument("--chunk", type=int, default=256)
    ap.add_argument("--market-jitter", type=float, default=0.0,
                    help="marketParams domain randomisation strength (0 = defaults)")
    ap.add_argument("--warm-frac", type=float, default=0.25,
                    help="share of episode pairs opening with 2-4 quadrants and extra cash")
    ap.add_argument("--tape-act-warm", action="store_true",
                    help="let --tape-actions rungs take the --warm-frac start too "
                         "(off: an action tape replays a cold-start game, so its "
                         "pairs open on the engine's day 0)")
    ap.add_argument("--n-archetypes", type=int, default=4,
                    help="hand-set strategy opponents kept beside the pool "
                         "(on --resume, the checkpoint's saved archetypes take "
                         "precedence over this flag)")
    ap.add_argument("--arch-frac", type=float, default=0.5,
                    help="share of episode slots that face an archetype; the rest "
                         "round-robin over the self-play pool and theta")
    ap.add_argument("--slot-rotation", choices=("fixed", "carry"),
                    default="carry",
                    help="how the archetype block's episode slots are divided "
                         "between the rungs. `carry` (default) rotates the "
                         "leftover slots across generations, so every rung's "
                         "cumulative share tracks its weight to within one "
                         "slot and a ladder wider than the block still covers "
                         "its tail; `fixed` is the old pure largest-remainder "
                         "rounding, where the same rungs take the leftovers "
                         "every generation and 127 tapes at 256 episodes never "
                         "sample the last 12. Both draw one opponent row per "
                         "generation for the whole population, so common "
                         "random numbers are the same either way.")
    ap.add_argument("--pinned-once", action="store_true",
                    help="play every PINNED rung exactly once per candidate "
                         "per generation, whatever its --rung-weight. A pinned "
                         "rung is a --tape-actions tape cut --with-town: the "
                         "recorded town schedule fixes the shop draws, so the "
                         "rung is one deterministic board and both seats "
                         "return the same coins for the same theta. Measured "
                         "on the live 384-episode arms, 86 such rungs at "
                         "weight 2 took ~4 episodes each -- 75%% of the pinned "
                         "budget replaying identical outcomes. The freed "
                         "episodes go to the drawn tapes, the archetypes and "
                         "self-play through the usual carry logic, and each "
                         "rung's weight moves to the fitness aggregation, "
                         "where it scales the board's contribution instead of "
                         "its replay count. The seat alternates per generation "
                         "(staggered by rung), so the mirroring a pair used to "
                         "do inside one generation happens across two. Off by "
                         "default, and off is byte-identical to before.")
    ap.add_argument("--pinned-fixed-seed", action="store_true",
                    help="play every PINNED rung on a FIXED seed word derived "
                         "from the tape, not on the generation's drawn one. A "
                         "--with-town tape pins the SHOPS; it does not pin the "
                         "weed walk, which still eats two words per empty tile "
                         "out of the per-slot seed, so the same candidate on "
                         "the same pinned board scored two different totals "
                         "under two seeds (pinned-only ranking spearman 0.985 "
                         "across two CRN seeds, on 82%% of the fitness "
                         "weight). On, the word is a blake2b digest of the "
                         "rung name -- a property of the tape alone, stable "
                         "across processes and --resume -- so a pinned rung is "
                         "one game the way the engine's replay of it is one "
                         "game. Drawn tapes, archetypes and self-play keep the "
                         "drawn word. Off by default, and off is "
                         "byte-identical to before.")
    ap.add_argument("--require-tape-slots", action="store_true",
                    help="refuse to start when the configuration loads tape "
                         "rungs and then gives them no episode slots (the "
                         "--arch-frac 0 trap that made flow123-127 pure "
                         "self-play). Without the flag this is a startup "
                         "warning.")
    ap.add_argument("--pool-every", type=int, default=100,
                    help="generations between opponent-pool snapshots")
    ap.add_argument("--margin-scale", type=float, default=100_000.0,
                    help="coins per unit of the shaped relative term")
    ap.add_argument("--abs-weight", type=float, default=0.6,
                    help="fitness weight on mean log1p(own coins); 1-w goes on the margin")
    ap.add_argument("--d10-cash-weight", type=float, default=0.0,
                    help="coins of shaped margin per coin of the day-D purse "
                         "lead, added to the margin before the sigmoid. 0 "
                         "(the default) is exactly inert: the ranking input "
                         "is the identical expression, not a zeroed term. "
                         "A ledger over 88 losses to the 2000-2200 band found "
                         "the day-9 -> day-10 coin swing larger than the final "
                         "margin in 69 of them, so 1.0 (day D counts like the "
                         "finish) is an upper bound and ~0.5 a starting arm.")
    ap.add_argument("--d10-cash-day", type=int, default=10,
                    help="which end-of-day purse --d10-cash-weight reads "
                         "(0-based). 10 is where the band's lead opens.")
    ap.add_argument("--tile-fill-weight", type=float, default=0.0,
                    help="COINS PER NET FILLED TILE: adds w * mean over days "
                         "10-25 of (planted tiles - idle unlocked tiles) for "
                         "our seat to the margin. 0 (the default) is exactly "
                         "inert. The band holds ~17.5 net tiles more than we "
                         "do from day 10 on and leads by ~17.5k coins over "
                         "days 10-19, so ~1,000 coins/tile is the measured "
                         "ceiling; 200 prices a tile at a fifth of that, which "
                         "makes the term a tie-breaker rather than the "
                         "objective.")
    ap.add_argument("--late-price-weight", type=float, default=0.0,
                    help="COINS OF MARGIN PER COIN OF REALISED UNIT PRICE: "
                         "adds w * (our mean coins per unit sold over days "
                         "15-29 minus theirs). 0 (the default) is exactly "
                         "inert. A ledger of 30 recorded top-10 games (2820-"
                         "2940) found them level or BEHIND at day 10 (paired "
                         "gap -459) and winning the second half on price: "
                         "+19k income d15-29 at flat volume, carrot +28/unit, "
                         "milk +17, wool +14, strawberry +14, sold through "
                         "2.1x our SELL rows in half-size slices. ~950 is "
                         "where the term would be worth the coins it "
                         "measures; 150 makes it a tie-breaker. NOTE this "
                         "pulls AGAINST --d10-cash-weight, which targets the "
                         "2100 band's opposite edge -- do not set both "
                         "without a reason.")
    ap.add_argument("--fitness-manifest", action="store_true",
                    help="print the effective objective as one line at "
                         "startup: both blend weights, the margin scale, both "
                         "day-10 terms, the decay, how much of theta is live "
                         "and how many rungs the ladder has.")
    ap.add_argument("--rung-weight", action="append", metavar="NAME=W",
                    help="repeatable: give archetype NAME a share W of the "
                         "archetype episode slots (default: every rung 1). "
                         "e.g. --rung-weight kagg2_proxy=3 --rung-weight mixed_ranch=2")
    ap.add_argument("--rung-theta", action="append", metavar="NAME=PATH.npy",
                    help="repeatable: pin the frozen theta at PATH into the "
                         "ladder as a rung called NAME. Scored and logged like "
                         "every other rung but held out of the gradient and of "
                         "the yardstick mean (weight 0) unless --rung-weight "
                         "NAME=W pulls it in.")
    ap.add_argument("--proxy-handicap", default=f"{AR.NO_HANDICAP[0]}:{AR.NO_HANDICAP[1]}",
                    metavar="NQUAD:MONEY",
                    help=f"opening the `{AR.PROXY_NAME}` rung plays from, on its "
                         f"own seat only (default {AR.NO_HANDICAP[0]}:"
                         f"{AR.NO_HANDICAP[1]}, the engine's day 0 = no handicap; "
                         f"fitted {AR.PROXY_HANDICAP[0]}:{AR.PROXY_HANDICAP[1]})")
    ap.add_argument("--select-metric", default="coins", metavar="METRIC",
                    help=f"what best_abs / the champion / --promote select on. "
                         f"`coins` (default) is the rung-weighted yardstick coin "
                         f"total; `score` is the weighted expected tournament "
                         f"score; `{MARGIN_PREFIX}NAME` is the mean (own - "
                         f"theirs) on the single rung NAME -- e.g. "
                         f"`{MARGIN_PREFIX}{K2F.RUNG_NAME}`, which is the only "
                         f"one of the three that ranks our thetas the way the "
                         f"real engine ranks them against kagg2 (Spearman +1.00 "
                         f"against 0.00 for the coin total, measured 2026-08-27). "
                         f"A margin is routinely negative; best_abs, best_sel "
                         f"and champ in log.jsonl are then negative too, and "
                         f"`null` until the first measurement. "
                         f"`{SOFTWIN_PREFIX}NAME:TAU` is that same rung read "
                         f"through a tanh -- mean tanh((own - theirs) / TAU) "
                         f"over the games, a smooth win rate in [-1, +1] -- "
                         f"e.g. `{SOFTWIN_PREFIX}{K2F.RUNG_NAME}:3000`. TAU is "
                         f"in coins and is the width over which it turns a "
                         f"margin into a win: it selects for winning more games "
                         f"rather than for winning by more the ones already "
                         f"won, which is what a Bradley-Terry field scores.")
    ap.add_argument("--select-coin-floor", type=float, default=0.0,
                    help="a candidate under this many yardstick coins is not "
                         "selectable whatever it scores (0 = off); needs a "
                         "--select-metric other than coins")
    ap.add_argument("--best-gate", choices=("sel", "both"), default="sel",
                    help="what a new best_abs has to clear. `sel` (default) is "
                         "the rule every checkpoint on disk was written under: "
                         "beat the record on the selection half of the fixed "
                         "seeds. `both` additionally requires the *holdout* "
                         "half not to fall, which refuses the lucky-seed "
                         "reading a max over a noisy sequence otherwise keeps "
                         "-- the record is ~3-4k optimistic without it.")
    ap.add_argument("--best-margin", type=float, default=0.0, metavar="X",
                    help="how far a candidate has to clear the record before it "
                         "takes it, in whatever --select-metric selects on "
                         "(default 0.0 = strictly greater, the old rule). "
                         "Applies under both --best-gate modes. Mind the units: "
                         "under `coins` or `margin:NAME` this is coins (a few "
                         "hundred is a real bar), under `score` it is a "
                         "probability, and under `softwin:NAME:TAU` it is in "
                         "tanh units on [-1, +1], where 0.01 is already a "
                         "meaningful step and 500 is a bar nothing can clear.")
    ap.add_argument("--collapse-floor", type=float, default=0.0,
                    help=f"drop from the yardstick any rung keeping less than "
                         f"this share of its zero-theta coins against the "
                         f"incumbent (0 = report only; {AR.COLLAPSE_KEEP} is the "
                         f"measured separation between a live rung and a free win)")
    ap.add_argument("--kagg2-flow", action="store_true",
                    help=f"add the `{K2F.RUNG_NAME}` rung: one extra archetype "
                         f"slot, past --n-archetypes, whose own SELL and "
                         f"BUY_PRODUCT orders are blanked and replaced by "
                         f"kagg2's measured per-day market flow (see "
                         f"kagg3.es.kagg2_flow). It is the only rung that "
                         f"reproduces kagg2's supply mix, and so the only one "
                         f"whose quotes are the ones the real matchup pays. "
                         f"Off by default; `--rung-weight {K2F.RUNG_NAME}=N` "
                         f"weights it like any other rung. On --resume into a "
                         f"checkpoint whose ladder predates the rung, the "
                         f"ladder is *extended* by it -- theta, sigma, the Adam "
                         f"moments, the pool, the generation and the RNG all "
                         f"carry over untouched.")
    ap.add_argument("--kagg2-flow-scale", default="0.5:1.5", metavar="LO:HI",
                    help="uniform scale on every product of the flow table, "
                         "drawn per episode pair (default 0.5:1.5). The table "
                         "is a measurement of 64 games, not a script; training "
                         "against 1.0:1.0 would fit that calendar. Needs "
                         "--kagg2-flow.")
    ap.add_argument("--kagg2-flow-jitter", type=int, default=2, metavar="DAYS",
                    help="uniform day shift of the whole flow calendar, +- this "
                         "many days, drawn per episode pair (default 2; 0 pins "
                         "the calendar). Needs --kagg2-flow.")
    ap.add_argument("--kagg2-flow-shift", default=None, metavar="LO:HI",
                    help=f"the inclusive range, in whole days, the "
                         f"`{K2F.RUNG_NAME}` rung's calendar shift is drawn "
                         f"from during *training*, replacing the symmetric "
                         f"--kagg2-flow-jitter draw. The jitter is centred on "
                         f"the table's own calendar, i.e. on shift 0; the "
                         f"calibration sweep puts the real matchup near +2 "
                         f"days (and scale ~1.3), so a jitter can only widen "
                         f"the band around a centre that is wrong. `0:4` "
                         f"centres the gradient on +2 with the jitter's width. "
                         f"Mutually exclusive with a non-default "
                         f"--kagg2-flow-jitter, and needs --kagg2-flow.")
    ap.add_argument("--kaggle-flow", action="store_true",
                    help=f"add the `{KGF.RUNG_NAME}` rung: the same kind of "
                         f"opponent as --kagg2-flow, replaying the *Kaggle "
                         f"field's* measured per-day market flow instead of "
                         f"kagg2's ({KGF.N_GAMES} replays of the games our "
                         f"champion lost, {len(KGF.OPPONENTS)} different "
                         f"opponents, measured {KGF.MEASURED}; see "
                         f"kagg3.es.kaggle_flow). Those are the quotes the "
                         f"ladder actually has to beat. Appended *after* "
                         f"`{K2F.RUNG_NAME}`, so every existing rung index and "
                         f"`--rung-weight` keeps its meaning; "
                         f"`--rung-weight {KGF.RUNG_NAME}=N` weights it. Its "
                         f"scale and day shift default to whatever the kagg2 "
                         f"rung is drawing. On --resume into an older ladder "
                         f"the ladder is *extended* by it, exactly as "
                         f"--kagg2-flow extends one.")
    ap.add_argument("--kaggle-flow-scale", default=None, metavar="LO:HI",
                    help=f"uniform scale on every product of the "
                         f"`{KGF.RUNG_NAME}` table, drawn per episode pair. "
                         f"Default: whatever --kagg2-flow-scale is, since the "
                         f"two rungs are the same kind of randomisation. Needs "
                         f"--kaggle-flow.")
    ap.add_argument("--kaggle-flow-shift", default=None, metavar="LO:HI",
                    help=f"the inclusive range, in whole days, the "
                         f"`{KGF.RUNG_NAME}` rung's calendar shift is drawn "
                         f"from. Default: whatever the kagg2 rung is drawing "
                         f"(--kagg2-flow-shift if set, else the symmetric "
                         f"draw of +/- --kagg2-flow-jitter). Needs "
                         f"--kaggle-flow.")
    ap.add_argument("--tape-actions", action="append", default=[], metavar="NPZ",
                    help="add one rung per `scripts/make_tape_actions.py` "
                         "table: a recorded Kaggle seat replayed ACTION for "
                         "ACTION in the simulator -- its units, its market "
                         "rows, its hires and its land, all simulated through "
                         "the code paths our own seat uses. Where --tape-rung "
                         "replays that seat's daily market aggregates through "
                         "a surrogate board (spearman 0.25 against the engine, "
                         "8-12k coins too strong), this reproduces the engine "
                         "byte for byte on 15 of 16 paired boards "
                         "(scripts/check_tape_actions.py). Repeatable, and "
                         "comma-separated paths are accepted. The rung is "
                         "labelled tape_act_<episode> and is weighted with "
                         "--rung-weight like any other. Scored on the margin: "
                         "--tape-score is a --tape-rung flag and does not "
                         "reach these.")
    ap.add_argument("--tape-rung", action="append", default=[], metavar="NPZ",
                    help="add one rung per `scripts/make_tape_rung.py` table: "
                         "the measured per-day market flow of a **single** "
                         "Kaggle replay seat, rather than the mean over a bot "
                         "(--kagg2-flow) or over a field (--kaggle-flow). "
                         "These are the class-A opponents that hold the "
                         "champion to 50% and that the ladder has never "
                         "trained against. Repeatable, and comma-separated "
                         "paths are accepted. The rung is labelled "
                         f"`{TPF.RUNG_PREFIX}<episode>`, so "
                         f"`--rung-weight {TPF.RUNG_PREFIX}103254816=3` "
                         "weights it and `--select-metric "
                         f"margin:{TPF.RUNG_PREFIX}103254816` selects on it. "
                         "Appended after both measured-mean rungs, so no "
                         "existing index moves; on --resume an older ladder is "
                         "extended by them.")
    ap.add_argument("--tape-flow-scale", default=None, metavar="LO:HI",
                    help="uniform scale on every product of a --tape-rung "
                         "table, drawn per episode pair. Default: whatever "
                         "--kagg2-flow-scale is. A tape table is one game, so "
                         "this is the flag that keeps the rung an opponent "
                         "rather than a recording. Needs --tape-rung.")
    ap.add_argument("--tape-flow-shift", default=None, metavar="LO:HI",
                    help="the inclusive range, in whole days, a --tape-rung's "
                         "calendar shift is drawn from. Default: whatever the "
                         "kagg2 rung is drawing (--kagg2-flow-shift if set, "
                         "else the symmetric draw of +/- "
                         "--kagg2-flow-jitter). Needs --tape-rung.")
    ap.add_argument("--shop-crn", action="store_true",
                    help="take the end-of-day shop draw from a fixed position "
                         "in the day's word stream instead of from just past "
                         "the weed walk, so it no longer depends on how many "
                         "EMPTY tiles the two seats left. TRAINING ONLY -- a "
                         "common random number for the search, never an eval "
                         "semantic. The engine draws once per empty tile "
                         "before choice(sorted(SHOPS)), so a candidate that "
                         "plants one tile more re-rolls every later shop; a "
                         "YARN_STORE (the only wool sink) swings ~25k, which "
                         "lands on the ES gradient as a zero-mean +/-25k "
                         "lottery between antithetic pairs. The draw is "
                         "uniform over the eight shops either way, so the "
                         "expectation of fitness is unchanged. Off (the "
                         "default) the sim is byte-identical to the engine "
                         "and to every run before this flag -- keep it off "
                         "for any fidelity or replay check.")
    ap.add_argument("--tape-flow-backed", action="store_true",
                    help="a flow seat may only sell what its shed actually "
                         "holds: clamp the table's sell count to the seat's "
                         "stock BEFORE its revenue and the market's inventory "
                         "advance are taken, not only on the drain. Off (the "
                         "default) the table is exogenous -- the seat is paid "
                         "for, and the book is flooded with, goods it never "
                         "grew, which is worth ~14k of phantom coins a season "
                         "on a clone tape selling products a wheat board "
                         "cannot hold. Applies to every flow rung "
                         "(--kagg2-flow, --kaggle-flow, --tape-rung). "
                         "The clamp alone was not usable -- a flow rung's "
                         "board is a wheat clone, so it deleted the opponent "
                         "rather than shrinking it (tape seat ~8k against the "
                         "real 101.8k). It now also CREDITS the flow seat "
                         "with the production its table implies (the `grow` "
                         "row a re-cut --tape-rung carries), so the seat "
                         "sells what it grew at the sim's prices: calibrated "
                         "2026-09-05 with --tape-flow-spread over 14 tapes, "
                         "the flow seat banks 76-97k against the engine's "
                         "92-107k. A --tape-rung table cut before `grow` "
                         "existed is REFUSED under this flag, by name; "
                         "re-cut it with scripts/make_tape_rung.py.")
    ap.add_argument("--tape-flow-spread", action="store_true",
                    help="spend a flow table's day across the day's market "
                         "turns (`sim.rollout.MARKET_TURNS`, one `row // n` "
                         "share each with the remainder on the last) instead "
                         "of dumping the whole day into the book at hour 0, so "
                         "the tape trades at the hours we trade at rather than "
                         "always ahead of us. The day-boundary quote both "
                         "planners read, and the seat's own masked market "
                         "slots, are unchanged. Applies to every flow rung.")
    ap.add_argument("--tape-score", choices=TAPE_SCORES, default="margin",
                    help="how a --tape-rung's episodes are scored. `margin` "
                         "(the default) reads them like every other rung: our "
                         "coins minus the flow seat's. `ours` reads our coins "
                         "alone. EVIDENCE (calibration against the real "
                         "engine, 2026-09-04): the flow seat is credited "
                         "25-48k a tape for products its board never grows, so "
                         "a tape rung's margin is offset from the engine's by "
                         "a per-tape 4k-41k, and it ranks small theta changes "
                         "5/6 the way the engine does on OUR coins but 3/6 -- "
                         "a coin flip -- on the opponent's. Applies to the "
                         "update fitness and to the `score` column selection "
                         "reads; --select-metric margin:<tape> and "
                         "softwin:<tape> name a margin explicitly and are left "
                         "alone. Every other rung is untouched either way. "
                         "Needs --tape-rung.")
    ap.add_argument("--abs-flow-draws", type=int, default=0, metavar="K",
                    help=f"measure the `{K2F.RUNG_NAME}` rung of the *yardstick* "
                         f"at K fixed levels of its randomisation and average "
                         f"them, instead of reading the single centre of the "
                         f"family (scale 1.0, no day shift). The levels are "
                         f"drawn once from a fixed seed and never move, so the "
                         f"statistic stays deterministic in theta. Against the "
                         f"real engine over eight archived thetas the centre "
                         f"ranks them at Spearman 0.738 and inverts the top "
                         f"three; K=10 ranks them at 0.976 (K=4: 0.929). Costs "
                         f"K extra blocks of that one rung's episodes per "
                         f"measurement. 0 (default) = the centre, as before. "
                         f"Needs --kagg2-flow.")
    ap.add_argument("--abs-flow-scale", default="500:1500", metavar="LO:HI",
                    help="the range, in thousandths, --abs-flow-draws draws its "
                         "scales uniformly from (default 500:1500, the range "
                         "the gradient trains on). Set it to recentre the "
                         "yardstick's family: the real engine's margins matched "
                         "the sim's around scale 1.3, not 1.0, so `800:1800` "
                         "centres on 1.3 with the same width. Needs "
                         "--abs-flow-draws.")
    ap.add_argument("--abs-flow-shift", default="-2:2", metavar="LO:HI",
                    help="the range, in whole days, --abs-flow-draws draws its "
                         "calendar shifts uniformly from (default -2:2). The "
                         "day shift is a first-order knob, not a jitter: "
                         "`0:4` centres the yardstick on +2 days, which is "
                         "where the real matchup measured. Needs "
                         "--abs-flow-draws.")
    ap.add_argument("--abs-fresh-draws", action="store_true",
                    help="re-draw --abs-flow-draws' K levels for every "
                         "measurement, from a stream seeded by the generation, "
                         "instead of holding one fixed set for the whole run. "
                         "A fixed set is a static target and best_abs is a max "
                         "over it: measured 2026-08-27, the record climbed "
                         "+12.9k -> +17.8k in 150 gens at K=10 while the same "
                         "theta's centre margin sat at ~-5k and the real "
                         "engine scored the 'best' at -3,255 (the run's start "
                         "theta: +2,465). Fresh levels make the record a max "
                         "over readings the optimiser could not aim at. Gives "
                         "up comparability between two measurements' exact "
                         "levels, so it retires an inherited best_abs. Needs "
                         "--abs-flow-draws.")
    ap.add_argument("--best-replicate", type=int, default=0, metavar="N",
                    help="before a candidate takes best_abs, re-measure it N "
                         "times on levels AND seed pairs it was not screened "
                         "on, and take the record only if the mean of those "
                         "also clears best_abs + --best-margin -- at that "
                         "mean, not at the screening reading, which selection "
                         "has biased upward. The replicates always use freshly "
                         "drawn levels even without --abs-fresh-draws "
                         "(replicating on the levels that produced the reading "
                         "would re-measure the luck), and always fresh seed "
                         "pairs. Costs N extra measurements per accepted "
                         "candidate, nothing per generation. 0 (default) = the "
                         "screening reading takes the record, as before.")
    ap.add_argument("--real-gate", action="store_true",
                    help="an in-sim record only *nominates*: the candidate is "
                         "played against --real-gate-opponent in the REAL "
                         "engine (an async scripts/eval_vs_baselines.py; the "
                         "trainer never waits on it) and best_abs.npy / "
                         "best_abs_theta move only if that beats the "
                         "incumbent's own gated numbers. The in-sim record "
                         "keeps moving either way and its theta is kept as "
                         "best_sim.npy, so a rejection blocks nothing. Off = "
                         "the in-sim selector decides, as before -- which "
                         "measurably stops tracking the real engine after "
                         "~1.5k generations.")
    ap.add_argument("--real-gate-opponent", default="../kaggriculture2/main.py",
                    metavar="MAIN_PY[,MAIN_PY...]",
                    help="the packaged agent(s) the gate's real-engine games "
                         "are played against (default: the tracked "
                         "submission). Comma-separated for a FIELD: every "
                         "member is played --real-gate-games seeds in both "
                         "seats and the whole lot is pooled into one reading, "
                         "so the bar stops being one opponent's opinion. "
                         "Changing the field on a --resume needs "
                         "--real-gate-reset (the saved bar was measured "
                         "against the old one).")
    ap.add_argument("--real-gate-games", type=int, default=24, metavar="N",
                    help="seeds per gate eval PER OPPONENT; every seed is "
                         "played in both seats, so 24 (default) is 48 games "
                         "against one opponent and 192 against a field of "
                         "four, ~3 min per opponent on 4 workers -- the same "
                         "row the tracker takes")
    ap.add_argument("--real-gate-workers", type=int, default=4, metavar="N",
                    help="processes the gate eval runs its games on (default "
                         "4). The trainer is GPU-bound and these are CPU, but "
                         "they are not free: keep a core for the host.")
    ap.add_argument("--real-gate-seed-base", type=int, default=20260825,
                    metavar="N",
                    help="seed base for the gate's games (default 20260825, "
                         "the tracker's -- so a gate row and a tracker row are "
                         "the same games and can be compared paired)")
    ap.add_argument("--real-gate-every", type=int, default=0, metavar="N",
                    help="also nominate the SEARCH CENTRE (theta, the ES mean) "
                         "to the gate every N generations, whenever no eval is "
                         "in flight and nothing is waiting. In-sim records dry "
                         "up after ~1.5k generations, so a gate fed by records "
                         "alone idles while the centre keeps moving and "
                         "best_abs.npy ages; this keeps the record contested. "
                         "A record nominating on the same generation wins the "
                         "slot. Requires --real-gate. 0 (default) = off, "
                         "records only. Each nomination costs one real-engine "
                         "eval (~3 min on --real-gate-workers cores), so keep "
                         "N well above the eval's length in generations.")
    ap.add_argument("--real-gate-replicate", action="store_true",
                    help="re-measure every ACCEPTED candidate on a fresh seed "
                         "base (--real-gate-seed-base + 1) and keep the "
                         "incumbent's numbers as the pooled reading over both "
                         "evals. The record is a max over noisy n=48 draws, so "
                         "the bar drifts up to the luckiest one the run ever "
                         "made -- flow28b accepted at 85.4%% and replicated at "
                         "74.5%% on 192 games, an ~11pp bar nothing honest "
                         "could clear. The replicate jumps the queue (it IS "
                         "the bar) and never moves best_abs.npy, since the "
                         "theta has not changed. Costs one extra eval per "
                         "acceptance. It also makes acceptance PROVISIONAL: "
                         "one n=48 draw against a pooled n=96 bar is not a "
                         "fair comparison (flow27c took the record at 79.2%%, "
                         "replicated at 60.4%% and left the run pooled at "
                         "69.8%%, below the 78.1%% it displaced), so "
                         "best_abs.npy and the stall clock move only once the "
                         "candidate's own POOLED pair beats the incumbent's; "
                         "otherwise the incumbent is restored.")
    ap.add_argument("--real-gate-fresh", action="store_true",
                    help="draw a FRESH seed base for every nomination "
                         "(deterministic from --seed) and replay the "
                         "INCUMBENT on that same base, so the decision is a "
                         "paired reading on games neither theta was selected "
                         "on. Two fixed bases are two things to overfit: "
                         "flow27g's confirmed record pooled 83.3%% on the "
                         "gate's own bases and 62.5%% on another (n=192), "
                         "while the champion is 76-85%% everywhere. The "
                         "confirmation is a second fresh base, paired again "
                         "and pooled over both. The incumbent's leg is skipped "
                         "when it has already been played on that base. Costs "
                         "up to 2 evals per nomination and 4 per acceptance. "
                         "Requires --real-gate-replicate.")
    ap.add_argument("--real-gate-reset", action="store_true",
                    help="on --resume, drop the saved incumbent's real "
                         "numbers: best_abs_theta stays, but it is re-"
                         "nominated at startup and whatever it scores now "
                         "becomes the bar. For a segment whose saved bar is no "
                         "longer comparable -- a repackaged opponent, a "
                         "changed --real-gate-games, a changed "
                         "--real-gate-opponent field (which a resume refuses "
                         "without this flag), or a bar so lucky that nothing "
                         "has passed it since.")
    ap.add_argument("--real-gate-recentre", type=int, default=0, metavar="K",
                    help="after K consecutive PERIODIC candidates have been "
                         "refused (or reverted) since the last confirmation, "
                         "put the search back on the gated record: theta <- "
                         "best_abs_theta, Adam cleared, sigma stepped exactly "
                         "as a --restart-sigma-on-stall restart does. The gate "
                         "otherwise only filters -- on flow27c/28c/27d every "
                         "centre candidate after the record scored 52-77%% "
                         "against pooled bars of 62-76%%, because the gradient "
                         "that moves the centre is in-sim and the bar is not. "
                         "Requires --real-gate-every. 0 (default) = off.")
    ap.add_argument("--real-gate-metric", choices=("win", "margin"),
                    default="win",
                    help="what the gate ranks on: `win` (default) is the real "
                         "win rate with the mean margin as tie-break, `margin` "
                         "is the mean margin alone")
    ap.add_argument("--real-gate-min-gain", type=float, default=0.0,
                    metavar="PTS",
                    help="minimum improvement in the gate metric a candidate "
                         "must show over the incumbent to be accepted "
                         "(win-rate points for --real-gate-metric win, coins "
                         "for margin); the tie-break on the other quantity "
                         "still applies only when the primary is exactly "
                         "equal AND min_gain is 0. The gate reads 128-256 "
                         "games, where the win rate has an sd of 3-4 points, "
                         "so the default rule -- any excess at all -- moves "
                         "the record on ONE extra win (flow59 accepted a "
                         "paired 47.7%% over 46.9%% and confirmed it at "
                         "46.1%%, against an incumbent that had read 53.5%%). "
                         "0.03 is ~one sd. Applies to both legs: the "
                         "provisional paired verdict and the pooled "
                         "confirmation. A --resume may change it freely (it "
                         "is a threshold, not a measurement); the change is "
                         "logged. 0 (default) = the strict rule, unchanged.")
    ap.add_argument("--real-gate-paired-t", type=float, default=0.0,
                    metavar="T",
                    help="require the candidate to beat the incumbent by T "
                         "standard errors of the PER-GAME paired difference, "
                         "on top of --real-gate-min-gain. Both legs of a "
                         "--real-gate-fresh round play the same seed base "
                         "against the same field, so every game has a twin in "
                         "the other leg's CSV; differencing the twins removes "
                         "the board from the comparison and gives the gate a "
                         "MEASURED standard error instead of a guessed "
                         "threshold. --real-gate-min-gain is a fixed bar that "
                         "cannot know how noisy this particular pair of "
                         "readings was; this does. The test is a one-sample t "
                         "on the paired differences of the selected metric "
                         "and is applied to both the provisional verdict and "
                         "the pooled confirmation. The confirmation is the "
                         "stricter of the two: BOTH rounds must be paired "
                         "(the replicate re-plays the incumbent on its own "
                         "fresh base, not only the candidate), the t is "
                         "pooled over both rounds' games at once, and the "
                         "pooled paired WIN difference must be positive "
                         "whatever the metric ranks on -- flow112 promoted a "
                         "theta on one lucky 240-board round against a bar "
                         "that read 39.2%% there and 49-54%% everywhere "
                         "else. "
                         "T=1.7 is ~p<0.05 one-sided at these game counts; "
                         "2.0 is stricter. A round whose two legs share no "
                         "game is REFUSED, not waved through. Requires "
                         "--real-gate-fresh (an unpaired round has nothing to "
                         "pair). A --resume may change it freely and the "
                         "change is logged. 0 (default) = off: no per-game "
                         "rows are read and the gate decides exactly what it "
                         "decided before this flag.")
    ap.add_argument("--real-gate-replicate-games", type=int, default=None,
                    metavar="N",
                    help="games per opponent for the REPLICATE round, instead "
                         "of --real-gate-games. The replicate is the reading "
                         "that actually decides -- a provisional acceptance "
                         "only buys the right to be re-measured -- so it is "
                         "the round worth spending on. Both legs of the round "
                         "play N, so the pair stays a pair. Omitted "
                         "(default) = --real-gate-games, which is what every "
                         "run before this flag played on both rounds.")
    ap.add_argument("--real-gate-win-floor", type=float, default=None,
                    metavar="PTS",
                    help="with --real-gate-metric margin, also refuse any "
                         "candidate whose real win rate is more than PTS "
                         "below the incumbent's, however many coins it "
                         "brought. The margin stays the primary statistic -- "
                         "it is continuous and better powered than a 128-256 "
                         "game win rate -- but on the margin alone a "
                         "candidate can buy coins with the head-to-head bit "
                         "the leaderboard actually scores. 0 = the win rate "
                         "may not drop at all; 0.03 allows a 3-point drop "
                         "(~one sd of the gate's own read). Applies to both "
                         "legs, like --real-gate-min-gain, and never *makes* "
                         "an acceptance: it can only veto one, so the first "
                         "reading of all still takes the record unopposed. "
                         "A --resume may change it freely and the change is "
                         "logged. Omitted (default) = no floor, the margin "
                         "alone.")
    ap.add_argument("--real-gate-pinned", default=None,
                    metavar="SCHEDULE_JSON",
                    help="judge on the PINNED LIVE-REPLICA set instead of a "
                         "seed draw. SCHEDULE_JSON is the town schedule a "
                         "scripts/tape_opponent.py --with-town run wrote (a "
                         "JSON object keyed by episode id); it is handed to "
                         "the gate's own eval as KAGG3_TOWN_SCHEDULE, which "
                         "is what pins the engine's end-of-day shop draw "
                         "(scripts/town_inject.py). With the town pinned a "
                         "--with-town opponent package REPLAYS the real "
                         "Kaggle game: the outcome is the live one in either "
                         "seat and on any seed (the coins move by a fraction "
                         "of a percent between seed bases, because the weeds "
                         "are still seed-keyed -- which is why both legs of a "
                         "round play the one fixed base and are the identical "
                         "board), so the gate stops estimating a win "
                         "rate and starts answering the only question the "
                         "leaderboard asks: WHICH of the games we actually "
                         "played would this candidate have flipped. Every "
                         "--real-gate-opponent is therefore played exactly "
                         "once per seat played (both by default; see "
                         "--real-gate-pinned-seats) on the fixed "
                         "--real-gate-seed-base, the incumbent replays the "
                         "same set, and the verdict is a count of flips and "
                         "drops written per tape id into real_gate.log. "
                         "IGNORES --real-gate-games, "
                         "--real-gate-replicate-games, --real-gate-fresh, "
                         "--real-gate-seed-per-opponent and "
                         "--real-gate-paired-t, and makes "
                         "--real-gate-replicate a no-op: replicating a "
                         "deterministic game re-measures the same number. "
                         "Said once at startup and once in real_gate.log. "
                         "Omitted (default) = the seed-draw gate, unchanged.")
    ap.add_argument("--real-gate-min-flips", type=int, default=1, metavar="N",
                    help="with --real-gate-pinned, the NET flips (games the "
                         "incumbent did not win and the candidate did, minus "
                         "the reverse) a candidate must show over the pinned "
                         "set before the record moves; it must also win "
                         "strictly more of the set. 1 (default) is the "
                         "weakest rule that still says something -- one live "
                         "game turned round and none given back. Requires "
                         "--real-gate-pinned; under --real-gate-metric margin "
                         "the coins rule (--real-gate-min-gain) decides "
                         "instead and this is not read.")
    ap.add_argument("--real-gate-pinned-seats", type=int, choices=(1, 2),
                    default=2, metavar="N",
                    help="with --real-gate-pinned, how many seats of every "
                         "pinned board a leg plays. 2 (default) is the gate "
                         "that shipped before this flag, byte for byte: each "
                         "tape is played in seat 0 and in seat 1. 1 plays "
                         "seat 0 only. Measured 2026-09-09: with the town "
                         "pinned, BOTH SEATS of a pinned tape return the same "
                         "coins for our agent -- the seat order stops "
                         "mattering once the shop draw is fixed -- so the "
                         "second seat re-measures the first, doubles the wall "
                         "clock and double-counts every board. Under 1 a game "
                         "IS a board: games, wins, flips, drops and therefore "
                         "--real-gate-min-flips are all counted once per live "
                         "replica. Requires --real-gate-pinned (only a pinned "
                         "board is seat-invariant; on a drawn one the second "
                         "seat is the half of the pair that cancels the seat "
                         "bias). Said at startup and in real_gate.log.")
    ap.add_argument("--real-gate-seed-per-opponent", action="store_true",
                    help="give every member of the --real-gate-opponent field "
                         "its own seed list (deterministic from "
                         "--real-gate-seed-base and the field position) "
                         "instead of playing them all on the same "
                         "--real-gate-games seeds. A leg then samples "
                         "games*len(field) distinct seeds instead of games, "
                         "for the same number of games and the same wall "
                         "clock. The seed is what the reading is noisy in: "
                         "the per-seed paired win difference between two "
                         "thetas has an sd of ~0.165 and correlates only "
                         "weakly across opponents, so a 9-opponent x 12-seed "
                         "x 2-seat leg is +/-4.8 points on twelve seeds and "
                         "+/-1.6 on 108. Off by default; a --resume may turn "
                         "it on or off freely (it is a draw, not a "
                         "measurement) and the change is logged.")
    ap.add_argument("--keep-candidates", action="store_true",
                    help="keep every theta the real gate is handed. Each "
                         "nomination is copied to "
                         "<run>/cands/g{gen:05d}_{record|periodic}.npy before "
                         "its eval starts and never deleted, and every "
                         "verdict appends a line to <run>/cands/index.jsonl "
                         "(gen, kind, file, md5, verdict, the candidate's "
                         "win/margin, the paired incumbent's, and the bar it "
                         "had to clear). The gate itself keeps only "
                         "real_gate_cand.npy, overwritten per eval, so "
                         "without this the refused thetas are unrecoverable "
                         "-- their numbers are in log.jsonl and their weights "
                         "are nowhere. Costs one theta-sized .npy per "
                         "nomination; requires --real-gate. Off by default, "
                         "and off it changes nothing.")
    ap.add_argument("--abs-select", choices=("sel", "hold", "all"), default="sel",
                    help="which of the --abs-pairs fixed seed pairs best_abs, "
                         "the champion and --promote are selected on. `sel` "
                         "(default) is the first half, the rule every "
                         "checkpoint on disk was written under, with the "
                         "second half held out; `hold` swaps the two; `all` "
                         "selects on every pair, which halves the statistic's "
                         "variance and gives up the held-out ratchet (so it "
                         "cannot be combined with --best-gate both).")
    ap.add_argument("--no-holdout-rungs", dest="holdout_rungs", action="store_false",
                    help="skip the two held-out opponent rungs "
                         + ", ".join(r[0] for r in AR.HOLDOUT_RUNGS)
                         + " (they are reported, never trained or selected on)")
    ap.add_argument("--abs-every", type=int, default=25,
                    help="generations between absolute-strength measurements")
    ap.add_argument("--champ-every", type=int, default=10,
                    help="generations between internal champion measurements; "
                         "set this and --abs-every above the final generation "
                         "to skip these reports in final-centre-only runs")
    ap.add_argument("--abs-pairs", type=int, default=64,
                    help="fixed seed pairs the absolute measurement plays (x2 seats); "
                         "the first half selects, the second half is the holdout")
    ap.add_argument("--restart-sigma-on-stall", type=int, default=0, metavar="N",
                    help="if best_abs has not improved for N generations, restart "
                         "from best_abs_theta with sigma multiplied by "
                         "--stall-sigma-mult, once (0 = off)")
    ap.add_argument("--stall-sigma-mult", type=float, default=2.0, metavar="MULT",
                    help="what --restart-sigma-on-stall multiplies sigma by "
                         "(default 2.0, the IPOP doubling; must be >= 1.0). Pass "
                         "1.0 on a ladder where the larger step is a collapse "
                         "rather than an escape, to keep the restart's jump back "
                         "onto best_abs_theta and its Adam reset without the "
                         "step-up. Applied on resume too: the restored restart "
                         "count is raised to this multiplier, not the old one.")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--run", default=time.strftime("%Y%m%dT%H%M%S"),
                    help="run directory, taken relative to artifacts/; an absolute "
                         "path is used as-is, which is how a smoke run keeps its "
                         "artifacts out of the repo")
    ap.add_argument("--antithetic-scope-diagnostic", action="store_true",
                    help="evaluate the fixed generation-zero M/H/J scope field, "
                         "save raw evidence, and exit without an update")
    ap.add_argument("--ckpt-every", type=int, default=10)
    ap.add_argument("--resume", metavar="RUN_DIR",
                    help="continue from a checkpoint directory "
                         "(e.g. artifacts/run3), keeping weights and opponent pool")
    ap.add_argument("--reset-best", action="store_true",
                    help="on --resume, drop the checkpoint's best_abs and "
                         "best_abs_theta so this run's first absolute "
                         "measurement becomes its new best. This happens by "
                         "itself whenever the ladder (rung names, --rung-weight, "
                         "--proxy-handicap) differs from the one the checkpoint "
                         "was measured on; the flag forces it when the ladder is "
                         "unchanged but the numbers are not -- a planner change "
                         "moves every coin count without touching a rung name.")
    ap.add_argument("--init-theta", default=None,
                    help="cold start only: begin from this theta (.npy) instead "
                         "of the random init. Unlike --resume, the ladder is "
                         "built from this invocation's flags, so it is how a "
                         "champion is put in front of new rungs.")
    ap.add_argument("--from-best", action="store_true",
                    help="on --resume, continue from the checkpoint's "
                         "best_abs_theta instead of its last iterate, with the "
                         "Adam moments cleared -- the jump half of a stall "
                         "restart, on demand, when the operator can see the run "
                         "wandering but does not want to wait out "
                         "--restart-sigma-on-stall or change sigma. Everything "
                         "else carries: gen, elapsed, sigma, both RNGs, the "
                         "pool, best_abs and the Adam step count.")
    ap.add_argument("--trunk-from", metavar="THETA_NPY",
                    help="fresh lineage: copy this theta's encoder trunk (w1, b1, g1, gb1), "
                         "leave every head at its fresh init")
    ap.add_argument("--residual", default=None, metavar="HEAD_NPZ",
                    help="train theta with the FROZEN residual action head "
                         "flown by our seat [ACTIONRL8]: the head is armed in "
                         "the sim rollout (greedy, seat 0 only) and passed "
                         "through to the real gate's candidate, so the agent "
                         "selected is the agent package_submission.py "
                         "--residual ships. The head is never updated here.")
    ap.add_argument("--residual-head-py", default=None, metavar="HEAD_PY",
                    help="the head module (default: this checkout's "
                         "S/actionrl/head.py)")
    ap.add_argument("--promote", action="store_true",
                    help="also write artifacts/theta.npy, the path the packager reads. "
                         "Off by default so concurrent runs cannot clobber each other.")
    args = ap.parse_args()
    if args.champ_every < 1:
        ap.error("--champ-every must be positive")

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)
    # A tmux server dying, or an ssh session closing on a run started without
    # nohup, delivers SIGHUP; unhandled, that kills the process between
    # checkpoints. Treat it as one more "stop cleanly".
    signal.signal(signal.SIGHUP, _stop)

    # `--resume` restores theta, the pool and the Adam moments as one
    # consistent state; `--trunk-from` then overwrites four blocks of that
    # theta while `tr.m`/`tr.v` keep the moments of the weights it just
    # replaced, and the next step drives the warmed trunk with a stale
    # first/second moment. There is no sane meaning to give the combination,
    # so refuse it rather than half-honouring one of the two.
    # Before every other check, because it has to be before every TRACE: the
    # head is part of the agent this run evaluates, not a knob on top of it.
    if args.residual:
        if not os.path.isfile(args.residual):
            raise SystemExit(f"--residual: no head at {args.residual}")
        arm_residual_sim(args.residual, args.residual_head_py)
    elif args.residual_head_py:
        raise SystemExit("--residual-head-py requires --residual: it names the "
                         "module the head is loaded from, and without a head "
                         "there is nothing to load.")

    if args.resume and args.trunk_from:
        raise SystemExit(
            "--resume and --trunk-from are mutually exclusive: --resume brings "
            "back Adam moments for the theta it restored, and --trunk-from "
            "would overwrite that theta's encoder trunk underneath them. "
            "Resume the run, or cold-start a fresh lineage with --trunk-from.")

    # Both are blend weights, and both are silently meaningless outside [0, 1]:
    # an --abs-weight of 2 makes the margin term's coefficient negative, i.e.
    # the run would spend 13 hours learning to lose. Refuse before the run
    # directory exists, like the flag-pair check above.
    if not 0.0 <= args.abs_weight <= 1.0:
        raise SystemExit(f"--abs-weight {args.abs_weight}: must be in [0, 1] "
                         f"(it is the weight on the absolute anchor; 1 - w goes "
                         f"on the margin term).")
    if not 0.0 <= args.arch_frac <= 1.0:
        raise SystemExit(f"--arch-frac {args.arch_frac}: must be in [0, 1] "
                         f"(it is the share of episode slots facing archetypes).")
    if args.arch_frac >= 1.0 and args.n_archetypes > 0:
        raise SystemExit(
            "--arch-frac 1.0 leaves no episode slot for the self-play pool or "
            "for theta itself. Against a purely frozen opponent set the rank "
            "signal saturates and the ladder stops being a ladder; use 0.9.")
    if args.margin_scale <= 0:
        raise SystemExit(f"--margin-scale {args.margin_scale}: must be positive.")
    # The season is days 0..29; an out-of-range day would read a purse that
    # does not exist, and under jit that is a silent clamp, not an error.
    if not 0 <= args.d10_cash_day < spec.N_DAYS:
        raise SystemExit(f"--d10-cash-day {args.d10_cash_day}: the season is "
                         f"days 0..{spec.N_DAYS - 1}.")
    # `1 - wd` is a multiplier on theta every generation: at 1 it erases the
    # weights in one step and past 1 it flips their sign, neither of which is
    # a decay. Negative is decoupled *growth*, which diverges.
    if not 0.0 <= args.weight_decay < 1.0:
        raise SystemExit(f"--weight-decay {args.weight_decay}: must be in "
                         f"[0, 1) -- theta is multiplied by (1 - WD) each "
                         f"generation, so 1.0 erases it and a negative one "
                         f"grows it without bound.")

    # The win-tracking flags, refused in the same place and for the same
    # reason: a run whose weighting or selection rule is quietly a no-op is a
    # run whose result cannot be attributed to anything. The flow shaping flags
    # come first because they are the same failure: a scale or a jitter with no
    # rung to apply to shapes nothing.
    defaults = {"kagg2_flow_scale": "0.5:1.5", "kagg2_flow_jitter": 2,
                "kagg2_flow_shift": None}
    if not args.kagg2_flow:
        set_anyway = [f"--{k.replace('_', '-')}" for k, v in defaults.items()
                      if getattr(args, k) != v]
        if set_anyway:
            raise SystemExit(f"{', '.join(set_anyway)} without --kagg2-flow: "
                             f"there is no flow rung for it to shape.")
    flow_scale = parse_flow_scale(args.kagg2_flow_scale)
    if not 0 <= args.kagg2_flow_jitter < spec.N_DAYS:
        raise SystemExit(f"--kagg2-flow-jitter {args.kagg2_flow_jitter}: must be "
                         f"in [0, {spec.N_DAYS}) days.")
    # Mutually exclusive rather than one silently winning: they are two ways of
    # saying what the same draw is, and an operator who passed both stated a
    # centre and a width that disagree about where the centre is.
    if args.kagg2_flow_shift is not None and args.kagg2_flow_jitter != 2:
        raise SystemExit(
            f"--kagg2-flow-shift {args.kagg2_flow_shift} with "
            f"--kagg2-flow-jitter {args.kagg2_flow_jitter}: both set the same "
            f"draw. The jitter is the symmetric range +-{args.kagg2_flow_jitter} "
            f"about shift 0; the range says where the family sits outright. "
            f"Pass one -- `--kagg2-flow-shift "
            f"{-args.kagg2_flow_jitter}:{args.kagg2_flow_jitter}` is the "
            f"jitter, written as a range.")
    flow_shift = (None if args.kagg2_flow_shift is None else
                  parse_int_range(args.kagg2_flow_shift, "--kagg2-flow-shift",
                                  lo_min=-(spec.N_DAYS - 1),
                                  hi_max=spec.N_DAYS - 1))

    # The second flow rung, refused the same way: a shaping flag with no rung
    # to shape is a flag the operator believes did something. Both default to
    # `None`, which is "share the kagg2 rung's draw" -- not a range, so there
    # is nothing to validate when the rung is off beyond it being unset.
    kaggle_defaults = {"kaggle_flow_scale": None, "kaggle_flow_shift": None}
    if not args.kaggle_flow:
        set_anyway = [f"--{k.replace('_', '-')}" for k, v in kaggle_defaults.items()
                      if getattr(args, k) != v]
        if set_anyway:
            raise SystemExit(f"{', '.join(set_anyway)} without --kaggle-flow: "
                             f"there is no {KGF.RUNG_NAME} rung for it to shape.")
    kaggle_scale = (None if args.kaggle_flow_scale is None else
                    parse_flow_scale(args.kaggle_flow_scale, "--kaggle-flow-scale"))
    kaggle_shift = (None if args.kaggle_flow_shift is None else
                    parse_int_range(args.kaggle_flow_shift, "--kaggle-flow-shift",
                                    lo_min=-(spec.N_DAYS - 1),
                                    hi_max=spec.N_DAYS - 1))

    # The tape rungs, refused the same way once more. Loading them here also
    # means a missing `.npz` or a table whose columns are not `spec.PRODUCTS`
    # stops the run at the command line rather than after the liveness probe.
    tape_paths, tape_names = parse_tape_rungs(args.tape_rung)
    tape_defaults = {"tape_flow_scale": None, "tape_flow_shift": None,
                     "tape_score": "margin"}
    if not tape_paths:
        set_anyway = [f"--{k.replace('_', '-')}" for k, v in tape_defaults.items()
                      if getattr(args, k) != v]
        if set_anyway:
            raise SystemExit(f"{', '.join(set_anyway)} without --tape-rung: "
                             f"there is no tape rung for it to shape.")
    elif args.n_archetypes <= 0:
        raise SystemExit(
            f"--tape-rung with --n-archetypes {args.n_archetypes}: the tape "
            f"rungs are appended to the archetype ladder, and a run with no "
            f"ladder plays none of them.")
    # The action rungs, the same way. They take none of the shaping flags
    # above -- there is nothing to scale or shift in a verbatim replay -- so
    # there is no "set anyway" check to make, only the ladder one.
    act_paths, act_names = parse_tape_actions(args.tape_actions)
    if act_paths and args.n_archetypes <= 0:
        raise SystemExit(
            f"--tape-actions with --n-archetypes {args.n_archetypes}: the "
            f"action rungs are appended to the archetype ladder, and a run "
            f"with no ladder plays none of them.")
    tape_scale = (None if args.tape_flow_scale is None else
                  parse_flow_scale(args.tape_flow_scale, "--tape-flow-scale"))
    tape_shift = (None if args.tape_flow_shift is None else
                  parse_int_range(args.tape_flow_shift, "--tape-flow-shift",
                                  lo_min=-(spec.N_DAYS - 1),
                                  hi_max=spec.N_DAYS - 1))

    # The yardstick's flow ensemble. Same rule as the shaping flags above and
    # for the same reason -- a range with no draws to place is a flag the
    # operator believes did something -- with the extra one that the draws
    # themselves need a rung to be drawn for.
    if args.abs_flow_draws < 0:
        raise SystemExit(f"--abs-flow-draws {args.abs_flow_draws}: must not be "
                         f"negative; 0 reads the flow rung at its centre.")
    if args.abs_flow_draws and not args.kagg2_flow:
        raise SystemExit("--abs-flow-draws without --kagg2-flow: there is no "
                         "flow rung in this run's yardstick to average over.")
    abs_ranges = {"abs_flow_scale": "500:1500", "abs_flow_shift": "-2:2"}
    set_anyway = [f"--{k.replace('_', '-')}" for k, v in abs_ranges.items()
                  if getattr(args, k) != v]
    if set_anyway and not args.abs_flow_draws:
        raise SystemExit(f"{', '.join(set_anyway)} without --abs-flow-draws: "
                         f"the range is what the ensemble's levels are drawn "
                         f"from, and this run draws none.")
    abs_flow_scale = parse_int_range(args.abs_flow_scale, "--abs-flow-scale",
                                     lo_min=1,
                                     hi_max=int(FLOW_SCALE_MAX * 1000))
    abs_flow_shift = parse_int_range(args.abs_flow_shift, "--abs-flow-shift",
                                     lo_min=-(spec.N_DAYS - 1),
                                     hi_max=spec.N_DAYS - 1)
    if args.abs_fresh_draws and not args.abs_flow_draws:
        raise SystemExit("--abs-fresh-draws without --abs-flow-draws: there "
                         "are no levels to re-draw. The flag redraws the K "
                         "levels of the flow family every measurement, and "
                         "this run reads that rung at its single centre.")
    if args.best_replicate < 0:
        raise SystemExit(f"--best-replicate {args.best_replicate}: must not be "
                         f"negative; 0 means the screening reading takes the "
                         f"record.")
    if args.abs_select == "all" and args.best_gate == "both":
        raise SystemExit(
            "--abs-select all with --best-gate both: `all` selects on every "
            "fixed seed pair, so the holdout half the gate reads is part of "
            "the selected set and the gate would be comparing a statistic "
            "against a piece of itself. Pick one -- `--abs-select all` for the "
            "lower-variance statistic on 64 pairs, or `--best-gate both` for "
            "the held-out ratchet on 32.")

    anchors = parse_rung_thetas(args.rung_theta)
    anchor_names = [n for n, _ in anchors]
    # The flow rung is appended by `Trainer` and the anchors by
    # `add_anchor_rungs` after it, so the ladder a `--rung-weight` name is
    # validated against is `[--n-archetypes rungs] + [kagg2_flow] +
    # [kaggle_flow] + [--tape-rung tables] + [anchors]` -- the order the run
    # will actually hold them in.
    names = rung_names(args.n_archetypes, args.kagg2_flow, args.kaggle_flow,
                       tape_names, act_names)
    rung_weight = parse_rung_weights(args.rung_weight, names + anchor_names)
    # An anchor is a *holdout* rung unless weighted: 0 slots in `opponent_slots`
    # and 0 weight in every `absolute_report` headline, i.e. measured without
    # being trained or selected on. The two lists are kept apart because
    # `Trainer.__init__` binds `cfg.rung_weight` against the ladder it builds
    # from `--n-archetypes` (plus the flow rung), and the anchors are not in it
    # yet.
    anchor_weight = tuple((n, dict(rung_weight).get(n, 0.0)) for n in anchor_names)
    rung_weight = tuple((n, w) for n, w in rung_weight if n not in anchor_names)
    proxy_handicap = parse_handicap(args.proxy_handicap)
    if proxy_handicap != AR.NO_HANDICAP and AR.PROXY_NAME not in names:
        raise SystemExit(
            f"--proxy-handicap {args.proxy_handicap} with --n-archetypes "
            f"{args.n_archetypes}: `{AR.PROXY_NAME}` is rung "
            f"{AR.NAMES.index(AR.PROXY_NAME) + 1} of the ladder, so nothing "
            f"would carry the handicap. Use --n-archetypes "
            f"{AR.NAMES.index(AR.PROXY_NAME) + 1}.")
    # Shape only. Whether the rung *exists* is a question about the ladder,
    # which on --resume comes from the checkpoint rather than from these flags,
    # so `Trainer._check_select_rung` owns it -- and answers it at construction
    # and again after every step that can grow the ladder.
    try:
        select_spec(args.select_metric)
    except ValueError as e:
        # `select_spec` owns the grammar -- the shape of the string, the tau,
        # and every message about them -- so a form added there is refused
        # here without this line moving. What it cannot know is the ladder.
        # Its own `select_metric '...':` prefix is dropped: the flag is named
        # once, the way an operator typed it.
        why = str(e).split(": ", 1)[-1].rstrip(".")
        raise SystemExit(
            f"--select-metric {args.select_metric}: {why}. Expected `coins`, "
            f"`score`, `{MARGIN_PREFIX}NAME` or `{SOFTWIN_PREFIX}NAME:TAU` "
            f"naming one rung of this run's ladder (e.g. "
            f"`{MARGIN_PREFIX}{K2F.RUNG_NAME}`, "
            f"`{SOFTWIN_PREFIX}{K2F.RUNG_NAME}:3000`).") from None
    if args.select_coin_floor < 0:
        raise SystemExit(f"--select-coin-floor {args.select_coin_floor}: "
                         f"must not be negative.")
    if args.select_coin_floor > 0 and args.select_metric == "coins":
        raise SystemExit(
            "--select-coin-floor with --select-metric coins does nothing: the "
            "floor guards a score or margin selection against promoting a "
            "policy that bought its margin by burning the market down, and "
            "selecting on coins already maximises the number the floor is a "
            "floor on. Pass --select-metric score, "
            f"{MARGIN_PREFIX}NAME or {SOFTWIN_PREFIX}NAME:TAU, or drop the "
            f"floor.")
    if args.best_margin < 0:
        raise SystemExit(
            f"--best-margin {args.best_margin}: must not be negative -- it is "
            f"how far a candidate has to clear the record, and a negative one "
            f"would hand best_abs to readings that are worse than it.")
    if args.reset_best and not args.resume:
        raise SystemExit("--reset-best without --resume: a cold start has no "
                         "inherited best_abs, and its first measurement is "
                         "already its first best.")
    if args.init_theta and args.resume:
        raise SystemExit("--init-theta with --resume: the checkpoint already "
                         "carries a theta (use --from-best to pick its record).")
    if args.from_best and not args.resume:
        raise SystemExit("--from-best without --resume: a cold start has no "
                         "best_abs_theta to start from -- its theta is the "
                         "fresh init, which is already where it begins.")
    # Below 1.0 the "restart" would *shrink* the step on a run that has stopped
    # moving, which is the opposite of what the stall detector fires for, and
    # `sigma * mult ** restarts` in `load_resume` would keep shrinking it on
    # every resume. 1.0 is the floor and means "jump, do not step up".
    if args.stall_sigma_mult < 1.0:
        raise SystemExit(f"--stall-sigma-mult {args.stall_sigma_mult}: must be "
                         f">= 1.0 -- it multiplies sigma when the run stalls, "
                         f"and a stalled run does not need a smaller step. Pass "
                         f"1.0 to keep sigma and take only the jump back onto "
                         f"best_abs_theta.")
    if not 0.0 <= args.collapse_floor < 1.0:
        raise SystemExit(f"--collapse-floor {args.collapse_floor}: must be in "
                         f"[0, 1) -- it is the share of its own zero-theta "
                         f"coins a rung has to keep to stay in the yardstick.")

    # Refused here rather than at `Trainer.__init__`, so a typo costs the
    # operator nothing: the run directory is not created and no checkpoint is
    # touched. `train_mask` is the single source of truth for what is legal.
    try:
        train_mask(args.train_only)
    except ValueError as exc:
        raise SystemExit(f"--train-only {args.train_only!r}: {exc}")

    out = os.path.join("artifacts", args.run)
    if args.antithetic_scope_diagnostic:
        incompatible = []
        for flag, active in (("--resume", args.resume),
                             ("--from-best", args.from_best),
                             ("--trunk-from", args.trunk_from),
                             ("--real-gate", args.real_gate),
                             ("--promote", args.promote)):
            if active:
                incompatible.append(flag)
        if incompatible:
            raise SystemExit("--antithetic-scope-diagnostic is incompatible "
                             f"with {', '.join(incompatible)}")
        if not args.init_theta:
            raise SystemExit("--antithetic-scope-diagnostic requires "
                             "--init-theta")
        if args.pop != 4096 or args.episodes != 124 or args.sigma != 0.01:
            raise SystemExit("--antithetic-scope-diagnostic requires "
                             "--pop 4096 --episodes 124 --sigma 0.01")
        try:
            os.mkdir(out)
        except FileExistsError:
            raise SystemExit(f"diagnostic output already exists: {out}")
    else:
        os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "config.json"), "w") as fh:
        json.dump(vars(args), fh, indent=2)

    cfg = Config(pop=args.pop, episodes=args.episodes, sigma=args.sigma,
                 lr=args.lr, weight_decay=args.weight_decay,
                 chunk=args.chunk, market_jitter=args.market_jitter,
                 warm_frac=args.warm_frac, tape_act_warm=args.tape_act_warm,
                 n_archetypes=args.n_archetypes,
                 arch_frac=args.arch_frac, slot_rotation=args.slot_rotation,
                 pinned_once=args.pinned_once,
                 pinned_fixed_seed=args.pinned_fixed_seed,
                 pool_every=args.pool_every,
                 margin_scale=args.margin_scale, abs_weight=args.abs_weight,
                 d10_cash_weight=args.d10_cash_weight,
                 d10_cash_day=args.d10_cash_day,
                 tile_fill_weight=args.tile_fill_weight,
                 late_price_weight=args.late_price_weight,
                 abs_every=args.abs_every, abs_pairs=args.abs_pairs,
                 champ_every=args.champ_every,
                 restart_stall=args.restart_sigma_on_stall,
                 stall_sigma_mult=args.stall_sigma_mult,
                 rung_weight=rung_weight, proxy_handicap=proxy_handicap,
                 select_metric=args.select_metric,
                 select_coin_floor=args.select_coin_floor,
                 best_gate=args.best_gate, best_margin=args.best_margin,
                 collapse_floor=args.collapse_floor,
                 holdout_rungs=args.holdout_rungs,
                 kagg2_flow=args.kagg2_flow,
                 kagg2_flow_scale=flow_scale,
                 kagg2_flow_jitter=args.kagg2_flow_jitter,
                 kagg2_flow_shift=flow_shift,
                 kaggle_flow=args.kaggle_flow,
                 kaggle_flow_scale=kaggle_scale,
                 kaggle_flow_shift=kaggle_shift,
                 tape_rungs=tape_paths,
                 tape_actions=act_paths,
                 tape_flow_scale=tape_scale,
                 tape_flow_shift=tape_shift,
                 tape_score=args.tape_score,
                 shop_crn=args.shop_crn,
                 tape_flow_backed=args.tape_flow_backed,
                 tape_flow_spread=args.tape_flow_spread,
                 abs_flow_draws=args.abs_flow_draws,
                 abs_flow_scale=abs_flow_scale,
                 abs_flow_shift=abs_flow_shift,
                 abs_select=args.abs_select,
                 abs_fresh_draws=args.abs_fresh_draws,
                 best_replicate=args.best_replicate,
                 train_only=args.train_only,
                 optimizer=args.optimizer)

    # The anchors are loaded further down (their thetas are files, and the
    # Trainer has to exist to fit their layout), so their names go in ahead of
    # them: `--select-metric margin:<anchor>` is validated against the ladder
    # this run *will* hold, not the one it holds this instant.
    tr = Trainer(cfg, seed=args.seed, pending_rungs=anchor_names)
    start_gen, elapsed0 = 0, 0.0
    if args.resume:
        start_gen, how, elapsed0 = load_resume(tr, args.resume)
        print(f"resumed from {args.resume} via {how}: gen {start_gen}, "
              f"pool {len(tr.pool)}, {elapsed0:.0f}s already spent", flush=True)
        if args.from_best:
            # Under the gate `best_abs_theta` is the *gated* record, and a
            # gated checkpoint that never accepted one holds the theta the run
            # started from instead. Jumping onto that is a silent reset, so it
            # is refused rather than performed.
            if args.real_gate and not RealGate.record_in(args.resume):
                raise SystemExit(
                    f"--from-best --real-gate {args.resume}: this checkpoint's "
                    f"gate never accepted a record, so its best_abs_theta is "
                    f"not a real-engine record but the theta that run began "
                    f"with. Resume without --from-best.")
            print(f"[{jump_to_best(tr, args.resume)}]", flush=True)
    elif args.init_theta:
        init = np.load(args.init_theta).astype(np.float32)
        padded = ""
        if init.ndim == 1 and init.shape[0] < tr.n:
            # A theta from an older layout, padded the way `policy.unpack`
            # would have decoded it -- inert zeros for the appended blocks, and
            # the season-constant `hire_bias` carried into its day buckets. So
            # a champion can be put in front of genes it never had and play the
            # first generation exactly as it played its last.
            padded = f", zero-padded from {init.shape[0]}"
            init = PO.pad(init)
        if init.shape != (tr.n,):
            raise SystemExit(f"--init-theta {args.init_theta}: shape "
                             f"{init.shape}, this layout needs ({tr.n},).")
        install_init_theta(tr, init)
        print(f"[--init-theta: theta <- {args.init_theta} "
              f"(|theta| {float(np.linalg.norm(init)):.2f}{padded})]", flush=True)
    if args.trunk_from:
        warm_trunk(tr, args.trunk_from)
        print(f"trunk warm-started from {args.trunk_from}", flush=True)
    if anchors:
        add_anchor_rungs(tr, anchors, anchor_weight)
        print("anchor rungs: " + "  ".join(
            f"{n}={p} (weight {w:g})"
            for (n, p), (_, w) in zip(anchors, anchor_weight)), flush=True)
    if args.antithetic_scope_diagnostic:
        before = scope_training_snapshot(tr)
        try:
            diagnostic = tr.antithetic_scope_diagnostic(32)
            after = scope_training_snapshot(tr)
            if before != after:
                raise RuntimeError("scope diagnostic mutated trainer state")
            save_scope_diagnostic(out, tr, diagnostic, before, after)
        except BaseException as exc:
            after = scope_training_snapshot(tr)
            save_scope_refusal(out, before, after, exc)
            raise
        print(f"scope diagnostic PASS: {out}/scope_diagnostic.json", flush=True)
        raise SystemExit(0)
    # The ladder is final here -- resume, then the flow rung, then the anchors --
    # so this is where `--reset-best` can be honoured and where the verdict of
    # the two automatic checks above is worth printing: one line, and only when
    # something was actually dropped.
    reset_best_if_ladder_changed(tr, force=args.reset_best)
    # The `--arch-frac 0` trap, made loud. flow123-127 each ran for hours with
    # their tape rungs loaded, registered, listed at startup -- and zero
    # episode slots, so they were pure self-play and their tape verdicts were
    # void. Nothing said so. Now something does, and `--require-tape-slots`
    # turns it into a refusal.
    complaint = tr.tape_slot_complaint()
    if complaint:
        if args.require_tape_slots:
            raise SystemExit(f"--require-tape-slots: {complaint}")
        print(f"WARNING: {complaint} Pass --require-tape-slots to make this "
              f"a refusal.", flush=True)
    # What `--pinned-once` actually did to the budget, before the first
    # generation rather than after it: the number an operator has to be able to
    # check against the launcher is "how many boards, how many episodes left".
    if args.pinned_once:
        for line in pinned_once_notes(cfg.episodes, len(tr.pinned_slots),
                                      len(tr.archetypes)):
            print(line, flush=True)
    if args.pinned_fixed_seed:
        # Same reason as the block above: an operator has to be able to see,
        # before generation 0, whether the flag found anything to pin.
        n = len(tr.pinned_slots)
        print(f"pinned-fixed-seed: {n} pinned rung(s) on their own fixed board"
              if n else
              "WARNING: --pinned-fixed-seed but no rung on this ladder is "
              "pinned: none of the --tape-actions tapes carries a `town` key "
              "(cut them with --with-town). The flag is inert.", flush=True)
    best_note = getattr(tr, "best_reset_note", None)
    if best_note:
        print(f"[{best_note}]", flush=True)
    elif args.resume and math.isfinite(tr.best_abs):
        print(f"best_abs carried over: {tr.best_abs:,.1f} in {args.select_metric} "
              f"(same ladder and metric as the checkpoint was measured on)",
              flush=True)
    # After the ladder, the resume and `--reset-best`, because the gate's
    # baseline is the record theta *this* run inherited -- and after the
    # jump-to-best above, whose refusal above depends on the same state.
    gate = setup_real_gate(args, tr, out,
                           resume_dir=args.resume if args.resume else None)
    if gate is not None:
        inc = ("none yet; the first result to land takes it"
               if gate.win is None else
               f"{gate.win * 100:.1f}% / {gate.margin:+,.0f} coins"
               + (f" (gen {gate.record_gen})" if gate.record_gen is not None
                  else ""))
        print(f"real gate: every in-sim record is played "
              f"{gate.games * 2 * len(gate.opponents)} games "
              f"vs {', '.join(gate.opponents)} in the real engine "
              f"on {gate.workers} workers "
              f"(seed base {gate.seed_base}), ranked on {gate.metric}"
              + (f" (min gain {gate.min_gain:g})" if gate.min_gain else "")
              + (f" (win floor {gate.win_floor:g})"
                 if gate.win_floor is not None else "")
              + f"; "
              f"incumbent {inc}; incumbent theta: "
              f"{getattr(gate, 'theta_source', 'unknown')}", flush=True)
        if gate.pending is not None:
            print(f"[real gate: re-nominating gen {gate.pending[1]}'s "
                  f"candidate, which the last segment left unmeasured]",
                  flush=True)
    # The three numbers an lr A/B is about, on one line: the step, the spread
    # it is taken over, and the decay that sets the norm they settle at
    # (~lr * sqrt(n / (2 * wd))), which is the one that silently moves when
    # only lr does.
    print(f"run={args.run}  params={tr.n}  pop={cfg.pop}  episodes={cfg.episodes}"
          f"  lr={cfg.lr:g}  sigma={tr.sigma:g}  wd={cfg.weight_decay:g}"
          f"  opt={cfg.optimizer}",
          flush=True)
    if args.fitness_manifest:
        # The whole objective on one line. Every arm this campaign has run
        # differs from its neighbour in some subset of these numbers, and until
        # now the only record of which subset was the launcher script on a
        # machine that gets rewritten -- which is why the plateau review could
        # not say what half the flowNNN runs were actually optimising.
        # Printed, not merely written to log.jsonl, so it is in the nohup tail.
        print(f"fitness-manifest: abs_weight={cfg.abs_weight:g}"
              f"  margin_scale={cfg.margin_scale:g}"
              f"  d10_cash_weight={cfg.d10_cash_weight:g}"
              f"@day{cfg.d10_cash_day}"
              f"  tile_fill_weight={cfg.tile_fill_weight:g}"
              f"(coins/tile, days {TILE_FILL_DAYS[0]}-{TILE_FILL_DAYS[1]})"
              f"  late_price_weight={cfg.late_price_weight:g}"
              f"(coins/unit-coin, days {LATE_PRICE_DAYS[0]}-{LATE_PRICE_DAYS[1]})"
              f"  weight_decay={cfg.weight_decay:g}"
              f"  train_only={cfg.train_only}:{tr.n_live}/{tr.n}"
              f"  rungs={len(tr.archetype_names)}"
              f"  tape_score={cfg.tape_score}", flush=True)
    if cfg.train_only not in ("", "all"):
        # How much of theta is actually in play, in the units the flag is
        # argued in: a subset that turns out to be three coordinates is a
        # different experiment from one that is three hundred, and the
        # difference is not visible from the spec string.
        print(f"train-only {cfg.train_only}: {tr.n_live} of {tr.n} "
              f"coordinates live", flush=True)
    if tr.abs_draws:
        # The levels themselves, once, at the top of the log: they are half of
        # what `best_abs` means for the rest of the run, and they are derived
        # from two flags rather than stated by one.
        print(f"yardstick flow ensemble: K={len(tr.abs_draws)} over "
              f"scale {abs_flow_scale[0]}:{abs_flow_scale[1]} milli, shift "
              f"{abs_flow_shift[0]}:{abs_flow_shift[1]} days -> "
              + (", ".join(f"{s}/{d:+d}" for s, d in tr.abs_draws)
                 if not args.abs_fresh_draws else
                 # The fixed set is still built (it is what `--abs-fresh-draws`
                 # replaces), but under the flag no measurement ever plays it,
                 # so printing it here would name the wrong levels.
                 "re-drawn every measurement")
              + f"; selected on {args.abs_select} of {cfg.abs_pairs} pairs",
              flush=True)
    if args.best_replicate:
        print(f"record replication: a candidate is re-measured "
              f"{args.best_replicate}x on unseen levels and seed pairs, and "
              f"recorded at that mean", flush=True)
    # `champ` is the champion's coins against the fixed archetype yardstick, on
    # the selection half of the fixed seeds -- the same quantity `best_abs`
    # tracks and `--promote` ships, on a coarser schedule. It replaced the
    # ladder win rate on 2026-08-25: over a 13 h run that correlated -0.17 with
    # absolute strength. `mean_win` is still logged, but as a diagnostic --
    # it is ladder-relative and sits near 0.5 by construction.
    log = open(os.path.join(out, "log.jsonl"), "a")
    # The objective this run was selected under, on its first record, so a
    # tracker row read off `log.jsonl` can always be attributed to the rule
    # that produced it -- `best_abs` is a coin count under one `select_metric`
    # and a bounded score under the other, and the file name does not say which.
    head = {"gen": start_gen, "select_metric": args.select_metric,
            "select_coin_floor": args.select_coin_floor,
            # `_mode`, because the per-generation records below spend the bare
            # `best_gate` key on the decision the gate reached that generation.
            "best_gate_mode": args.best_gate, "best_margin": args.best_margin,
            "margin_scale": args.margin_scale, "abs_weight": args.abs_weight,
            # The two day-10 shaping terms, always written even at 0, so a
            # tracker can tell an inert arm from a shaped one without the
            # argv.
            "d10_cash_weight": args.d10_cash_weight,
            "d10_cash_day": args.d10_cash_day,
            "tile_fill_weight": args.tile_fill_weight,
            "late_price_weight": args.late_price_weight,
            # Beside them because it moves the same objective: under `ours` a
            # tape rung's relative term is our coins, not a margin.
            "tape_score": args.tape_score,
            # Beside the step it is not independent of: the equilibrium norm is
            # ~lr * sqrt(n / (2 * wd)), so a tracker comparing two runs' curves
            # has to be able to see whether they settled at the same one.
            "lr": args.lr, "sigma": args.sigma,
            "weight_decay": args.weight_decay,
            "collapse_floor": args.collapse_floor,
            "proxy_handicap": list(proxy_handicap),
            "rung_weight": {n: w for n, w in rung_weight + anchor_weight},
            # The yardstick every `best_abs` on the lines below is a number
            # against, and whether this run inherited one or started its own.
            "ladder": list(tr.archetype_names),
            # What the yardstick *is*, so a tracker can tell a centre-read
            # `best_abs` from an ensemble one without re-deriving it from the
            # flags: K, the fixed levels themselves, and which seed pairs the
            # record was selected on.
            # Where the *gradient's* flow family sits, beside where the
            # yardstick's does: `null` for the symmetric jitter every run
            # before 2026-08-28 trained under.
            "kagg2_flow_shift": (None if flow_shift is None
                                 else [int(x) for x in flow_shift]),
            # And whether the *Kaggle field's* table is in this run's ladder at
            # all, with its own family if it was given one.
            "kaggle_flow": bool(args.kaggle_flow),
            "kaggle_flow_scale": (None if kaggle_scale is None
                                  else [float(x) for x in kaggle_scale]),
            "kaggle_flow_shift": (None if kaggle_shift is None
                                  else [int(x) for x in kaggle_shift]),
            "abs_flow_draws": args.abs_flow_draws,
            # The fixed set, or `null` under `--abs-fresh-draws` where there is
            # no one set to name -- each measurement's own levels ride on its
            # own row (`flow_levels`) instead.
            "abs_flow_levels": (None if args.abs_fresh_draws else
                                [[s, d] for s, d in tr.abs_draws]),
            "abs_fresh_draws": bool(args.abs_fresh_draws),
            "best_replicate": args.best_replicate,
            "abs_select": args.abs_select,
            # What decided `best_abs.npy` on this segment: `null` is the in-sim
            # selector alone, a dict is the real engine with the incumbent's
            # numbers as the segment inherited them.
            "real_gate": (None if gate is None else
                          {"opponent": list(gate.opponents),
                           "games": gate.games,
                           "workers": gate.workers, "metric": gate.metric,
                           "seed_base": gate.seed_base, "every": gate.every,
                           "replicate": gate.replicate, "n": gate.n,
                           "recentre": gate.recentre, "fresh": gate.fresh,
                           "win": gate.win, "margin": gate.margin,
                           "record_gen": gate.record_gen}),
            "best_abs_reset": best_note or False}
    log.write(json.dumps(head) + "\n")
    if tr.archetype_coins:
        probe = dict(zip(tr.archetype_names, [round(c, 1) for c in tr.archetype_coins]))
        log.write(json.dumps({"gen": start_gen, "archetype_probe": probe}) + "\n")
        print("archetype probe (coins vs the zero theta): "
              + "  ".join(f"{k} {v:,.0f}" for k, v in probe.items()), flush=True)
    log.flush()
    t0 = time.time()
    # The restart is watched by its *counter*, not by sigma: with
    # `--stall-sigma-mult 1.0` the sigma is deliberately unchanged, and gating
    # the line on sigma would make exactly that restart the silent one.
    sigma0, restarts0 = tr.sigma, tr.sigma_restarts
    for g in range(start_gen + 1, start_gen + args.gens + 1):
        gt = time.time()
        mean, best, abs_coins, rep = tr.generation()
        if not bool(jnp.all(jnp.isfinite(tr.theta))):
            # Refuse to checkpoint garbage over the last good state; the run
            # resumes from that checkpoint with a fresh RNG split.
            raise SystemExit(f"gen {g}: theta is non-finite; not checkpointing. "
                             f"Resume from {out} (last checkpoint is intact).")
        elapsed = elapsed0 + time.time() - t0
        rec = {"gen": g, "mean_win": mean, "best_win": best,
               # The two raw day-10 shaping quantities, population means, at
               # every weight including 0 -- an unshaped arm's log is the
               # baseline a shaped arm's is read against. `null` when the
               # evaluator is a 2-column stub.
               "d10_cash": (None if tr.last_day_metrics is None
                            else round(tr.last_day_metrics[0], 1)),
               "tile_fill": (None if tr.last_day_metrics is None
                             else round(tr.last_day_metrics[1], 3)),
               "late_price": (None if tr.last_day_metrics is None
                              else round(tr.last_day_metrics[2], 2)),
               "sell_rows_per_day": (None if tr.last_day_metrics is None
                                     else round(tr.last_day_metrics[3], 2)),
               # The forward-admit gene as the generation actually decoded it.
               # `null` on a tree with no `g11` block and on a stubbed
               # evaluator, exactly as the four above are.
               **_fwd_fields(tr),
               "secs": round(time.time() - gt, 2),
               "elapsed": round(elapsed, 1), "pool": len(tr.pool),
               # `null`, not a sentinel: under `--select-metric margin:<rung>`
               # these are margins, so every finite sentinel is a number a real
               # reading can take, and `-inf` is not JSON. Both stay `null`
               # until the first measurement gives them a value.
               "champ": _num(tr.champion_score, 1),
               "abs": abs_coins, "best_abs": _num(tr.best_abs, 1),
               "sigma": round(tr.sigma, 6),
               # What the gradient actually faced this generation, by rung
               # name: {name: episodes}, plus `_pool` and `_theta` for the
               # self-play half. One line per generation, so the coverage
               # question section 2 of the 2026-09-08 plateau review asks --
               # "did this tape get any episodes at all, ever?" -- is answered
               # by `jq` over log.jsonl rather than by re-deriving the
               # allocation by hand.
               "rung_episodes": tr.last_rung_episodes}
        if rep is not None:
            # Both sides of the yardstick, per archetype: a mean alone cannot
            # separate "earned more" from "the opponent collapsed". `abs_win`
            # is the win term, kept visible now that selection is on coins, and
            # `abs_holdout` is the half of the fixed seeds nothing selects on --
            # it diverging from `abs_measured` is what overfitting the seed set
            # would look like.
            rec.update({"abs_measured": round(rep.coins, 1),
                        "abs_win": round(rep.win, 4),
                        "abs_holdout": round(rep.holdout, 1),
                        "abs_holdout_win": round(rep.holdout_win, 4),
                        "abs_mine": [round(x, 1) for x in rep.mine],
                        "abs_theirs": [round(x, 1) for x in rep.theirs]})
            # The win-tracking half of the record. `best_sel` and `sel_metric`
            # say what `best_abs.npy` currently holds and by what rule.
            rec.update({"sel_metric": args.select_metric,
                        "best_sel": _num(tr.best_abs, 6),
                        "abs_score": round(rep.score, 6),
                        "abs_holdout_score": round(rep.holdout_score, 6),
                        "abs_keep": [round(x, 4) for x in rep.keep],
                        "abs_dropped": [n for n, ok in zip(tr.archetype_names,
                                                           rep.live) if not ok]})
            if rep.softwin:
                # Only a `softwin:` run fills this. `best_sel` is then one of
                # these numbers, and the per-rung block below carries only the
                # margins it is *not* -- a tracker could not otherwise see the
                # quantity the record was taken on.
                rec["abs_softwin"] = [round(x, 4) for x in rep.softwin]
                rec["abs_holdout_softwin"] = [round(x, 4)
                                              for x in rep.holdout_softwin]
            # The de-biased flow reading and the one it replaced, side by side.
            # `best_abs` is the *ensemble* -- it is what `abs_mine`/`abs_theirs`
            # carry on that rung once the flag is on -- and the centre rides
            # along so a filter can watch the gap: the two diverging is the run
            # climbing one level of the flow family rather than the family.
            if rep.flow_draws:
                rec.update({"flow_draws": rep.flow_draws,
                            "flow_ens_margin": round(rep.flow_ens_margin, 1),
                            "flow_centre_margin": round(rep.flow_centre_margin, 1)})
                # Which levels this row was read at. Only under
                # `--abs-fresh-draws`: with the fixed set they are the run
                # header's `abs_flow_levels` on every row, and a column that is
                # constant for a whole run belongs in the header.
                if args.abs_fresh_draws:
                    rec["flow_levels"] = [[int(sc), int(dy)]
                                          for sc, dy in rep.flow_levels]
            # What the record gate decided on this measurement, and on which
            # two numbers -- the pair whose *gap* is the seed luck `best_abs`
            # would otherwise be a max over. Logged on measurement generations
            # only, because that is when there is a decision to log.
            g_ = tr.last_best_gate
            rec["best_gate"] = {
                "sel": _num(g_["sel"], 6), "hold": _num(g_["hold"], 6),
                "accepted": g_["accepted"]}
            # The two readings `--best-replicate` compares, and which way it
            # went. `abs_screen` is the measurement the generation took;
            # `abs_replicate` is the mean of the N re-measurements on games it
            # was not screened on, and is `null` on a generation that never
            # cleared the bar (there was nothing to replicate) or whose
            # replicate the coin floor blocked. `best_gate.sel` is the number
            # the record was actually decided on, which under this flag is the
            # replicate mean -- so the *gap* between the two columns is the
            # winner's curse, in the units the run selects in.
            if args.best_replicate:
                r_ = tr.last_replicate
                rec.update({"abs_screen": _num(g_["sel"] if r_ is None
                                               else r_["screen"], 6),
                            "abs_replicate": (None if r_ is None
                                              else _num(r_["replicate"], 6)),
                            "replicate_rejected": bool(r_ is not None
                                                       and r_["rejected"]),
                            "replicate_rejects": int(tr.replicate_rejects)})
            # The three numbers denial collapse is visible in. `proxy_*` is the
            # rung the real matchup is calibrated against -- a win rate that
            # is not pinned at 1.00 and a margin that is not pinned at +50k.
            # `abs_vs_weakest` is the in-sim `coins_vs_starter`: our coins
            # against the *least* suppressive rung, where there is no market
            # worth burning, so a policy buying margin by burning one shows up
            # here and nowhere else.
            if rep.mine:
                weakest = int(np.argmax(rep.mine))
                rec.update({"abs_vs_weakest": round(rep.mine[weakest], 1),
                            "abs_weakest_rung": tr.archetype_names[weakest]})
            if AR.PROXY_NAME in tr.archetype_names:
                i = tr.archetype_names.index(AR.PROXY_NAME)
                rec.update({"proxy_win": round(rep.wins[i], 4),
                            "proxy_margin": round(rep.mine[i] - rep.theirs[i], 1),
                            "proxy_mine": round(rep.mine[i], 1),
                            "proxy_theirs": round(rep.theirs[i], 1)})
            # The anchors, by name: they are ordinary rungs of `abs_mine` /
            # `abs_theirs`, but a frozen trained theta is the comparison the
            # run was started to watch, so it gets a column of its own rather
            # than an index the reader has to count out.
            if anchor_names:
                rec["anchor_rungs"] = {
                    n: {"mine": round(rep.mine[i], 1),
                        "theirs": round(rep.theirs[i], 1),
                        "margin": round(rep.mine[i] - rep.theirs[i], 1),
                        "win": round(rep.wins[i], 4)}
                    for n, i in ((n, tr.archetype_names.index(n))
                                 for n in anchor_names)}
            if rep.holdout_rungs:
                rec["holdout_rungs"] = {
                    label: {"mine": round(m, 1), "theirs": round(t, 1),
                            "margin": round(g, 1), "win": round(w, 4)}
                    for label, m, t, g, w in rep.holdout_rungs}
        # The gate's verdict, on the generation it *landed* -- the eval is
        # asynchronous, so the candidate it judged is `real_gate_gen`, some
        # hundreds of generations back, and the two columns have to be read
        # together. Present only on the handful of generations that have one.
        r_ = tr.last_real_gate
        if r_ is not None:
            rec.update({"real_gate_gen": r_["gen"],
                        # "record" (the in-sim selector nominated it),
                        # "periodic" (--real-gate-every offered the centre) or
                        # "replicate" (--real-gate-replicate re-measuring the
                        # incumbent; the record does not move on those).
                        "real_gate_source": r_.get("source", "record"),
                        "real_gate_win": r_["win"],
                        "real_gate_margin": (None if r_["margin"] is None
                                             else round(r_["margin"], 1)),
                        "real_gate_accepted": bool(r_["accepted"]),
                        "real_gate_games": r_["games"],
                        "real_gate_incumbent_win": r_["incumbent_win"],
                        "real_gate_incumbent_margin": (
                            None if r_["incumbent_margin"] is None
                            else round(r_["incumbent_margin"], 1))})
            if r_.get("base") is not None:
                # The fresh base this verdict was decided on, and what the
                # incumbent scored on the *same* games -- the paired pair.
                # `real_gate_incumbent_*` beside it is the incumbent's running
                # pooled record over every base, which is a report, not the
                # comparison.
                rec["real_gate_base"] = int(r_["base"])
                if r_.get("paired_win") is not None:
                    rec["real_gate_paired_win"] = round(r_["paired_win"], 4)
                    rec["real_gate_paired_margin"] = round(
                        r_["paired_margin"], 1)
            if r_.get("pinned_n") is not None:
                # `--real-gate-pinned`: the count the verdict was made on.
                # The win rate beside it is the same fact as a fraction, but
                # the flips are the ones an operator can go and read: each is
                # a live episode that changed hands (the ids are in
                # real_gate.log, which is where a 100-tape list belongs).
                rec.update({"real_gate_pinned_games": r_["pinned_n"],
                            "real_gate_flips": r_["pinned_flips"],
                            "real_gate_drops": r_["pinned_drops"],
                            "real_gate_pinned_wins": r_["pinned_wins"],
                            "real_gate_pinned_incumbent_wins":
                                r_["pinned_incumbent_wins"]})
            if r_.get("replicate_win") is not None:
                # The pooled bar the next candidate now has to beat, not this
                # eval's own reading (`real_gate_win`, beside it).
                rec["real_gate_replicate_win"] = round(r_["replicate_win"], 4)
                rec["real_gate_replicate_margin"] = round(
                    r_["replicate_margin"], 1)
            if r_.get("reverted"):
                # The provisional record could not clear the incumbent on its
                # pooled numbers, so `best_abs.npy` never moved.
                rec["real_gate_reverted"] = True
                rec["real_gate_restored_gen"] = r_["restored_gen"]
            if r_.get("provisional"):
                rec["real_gate_provisional"] = True
            if r_.get("error"):
                rec["real_gate_error"] = r_["error"]
            was = ("no incumbent" if r_["incumbent_win"] is None else
                   f"{r_['incumbent_win'] * 100:.1f}%/"
                   f"{r_['incumbent_margin']:+,.0f}")
            if r_.get("paired_win") is not None:
                # The decision is paired (incumbent replayed on the same
                # fresh seeds); say the number it was actually taken on, and
                # keep the stored bar in brackets for continuity.
                was = (f"{r_['paired_win'] * 100:.1f}%/"
                       f"{r_['paired_margin']:+,.0f} paired (bar {was})")
            got = ("FAILED (" + r_["error"] + ")" if r_.get("error") else
                   f"{r_['win'] * 100:.1f}%/{r_['margin']:+,.0f} "
                   f"on n={r_['games']}")
            verdict = ("ACCEPTED -> best_abs.npy" if r_["accepted"] else
                       "ACCEPTED provisionally, awaiting its replicate"
                       if r_.get("provisional") else
                       "rejected, record stands")
            kind = r_.get("source", "record")
            if kind == "replicate" and r_.get("reverted"):
                print(f"[gen {g}: real gate -- gen {r_['gen']}'s record "
                      f"failed its replicate "
                      f"(pooled {r_['replicate_win'] * 100:.1f}%/"
                      f"{r_['replicate_margin']:+,.0f} < "
                      f"{r_['restored_win'] * 100:.1f}%/"
                      f"{r_['restored_margin']:+,.0f}): reverted to gen "
                      f"{r_['restored_gen']}]", flush=True)
            elif kind == "replicate":
                pooled = ("the bar stands unpooled"
                          if r_.get("replicate_win") is None else
                          f"pooled {r_['replicate_win'] * 100:.1f}%/"
                          f"{r_['replicate_margin']:+,.0f}")
                print(f"[gen {g}: real gate -- replicate of gen "
                      f"{r_['gen']}'s record: {got}; {pooled}, confirmed "
                      f"-> best_abs.npy]", flush=True)
            else:
                print(f"[gen {g}: real gate -- gen {r_['gen']}'s {kind} "
                      f"candidate scored {got} against {was}: {verdict}]",
                      flush=True)
        # The re-centre this generation, if the gate ran out of patience with
        # the centre (`--real-gate-recentre`). Not a verdict -- no eval landed
        # -- so it is its own row rather than a field of one.
        rc_ = tr.last_recentre
        if rc_ is not None:
            rec["real_gate_recentred"] = True
            rec["real_gate_recentre_gen"] = rc_["record_gen"]
            rec["real_gate_recentre_count"] = rc_["count"]
            print(f"[gen {g}: real gate -- {rc_['count']} periodic candidates "
                  f"rejected since gen {rc_['record_gen']}'s record: "
                  f"re-centred on it]", flush=True)
        log.write(json.dumps(rec) + "\n"); log.flush()
        # `proxy` is the only column on this line that is allowed to be a loss.
        # If it ever pins at 1.00 the way every other rung's win rate does, the
        # ladder has stopped posing the question it was rebuilt to pose.
        proxy = ("" if "proxy_win" not in rec else
                 f"  proxy {rec['proxy_win']:.2f}/{rec['proxy_margin']:+,.0f}")
        anchor = "".join(f"  {n} {v['win']:.2f}/{v['margin']:+,.0f}"
                         for n, v in rec.get("anchor_rungs", {}).items())
        # `flow` is the number the run is now selected on; `ctr` is the old
        # centre reading of the same rung, printed beside it rather than
        # instead of it because every earlier log line and every archived
        # theta's number is a centre reading.
        flow = ("" if "flow_ens_margin" not in rec else
                f"  flow {rec['flow_ens_margin']:+,.0f}"
                f"/ctr {rec['flow_centre_margin']:+,.0f}")
        # `-` before the first measurement: the champion has no score yet, and
        # `-inf` formats as a number-shaped `-inf` in a column of coin totals.
        champ_s = (f"{tr.champion_score:,.0f}"
                   if math.isfinite(tr.champion_score) else "-")
        # How much of the ladder the gradient actually faced this generation.
        # `log.jsonl`'s `rung_episodes` has the full name -> episodes map; this
        # is the one number that says whether a rung is being starved --
        # `rungs 103/127` on a 127-tape run is the coverage defect on screen.
        re_ = {k: v for k, v in rec["rung_episodes"].items()
               if not k.startswith("_")}
        rungs = ("" if not re_ else
                 f"  rungs {sum(1 for v in re_.values() if v)}/{len(re_)}")
        # The four raw quantities the day-10 / late-price terms pay for,
        # printed whether or not any weight is on: `d10` the mean day-D coin
        # lead, `fill` the mean net filled tiles (planted - idle, days 10-25,
        # our seat), `price` our realised coins per unit sold over days 15-29
        # minus theirs, and `rows/d` our SELL rows per day we sold on -- the
        # slicing number the top-10 ledger read at 9.6 against our 4.5.
        day = ("" if tr.last_day_metrics is None else
               f"  d10 {tr.last_day_metrics[0]:+,.0f}"
               f"  fill {tr.last_day_metrics[1]:+.2f}"
               f"  price {tr.last_day_metrics[2]:+.1f}"
               f"  rows/d {tr.last_day_metrics[3]:.1f}") + _fwd_line(tr)
        print(f"gen {g:5d}  mean_win {mean:.4f}  best {best:.4f}  "
              f"champ {champ_s}  {rec['secs']:.1f}s  "
              f"pool {len(tr.pool)}{rungs}  "
              f"abs {abs_coins if abs_coins is not None else '-'}"
              + (f"  hold {rep.holdout:,.0f}" if rep is not None else "")
              + day + flow + proxy + anchor, flush=True)
        if tr.sigma_restarts != restarts0:
            print(f"[gen {g}: no best_abs improvement for "
                  f"{args.restart_sigma_on_stall} gens -- restarted from "
                  f"best_abs_theta with Adam cleared and sigma {sigma0:g} -> "
                  f"{tr.sigma:g} (x{args.stall_sigma_mult:g})]", flush=True)
            sigma0, restarts0 = tr.sigma, tr.sigma_restarts
        if g % args.ckpt_every == 0 or STOP or g == start_gen + args.gens:
            save_atomic(os.path.join(out, "theta.npy"), np.asarray(tr.theta))
            save_atomic(os.path.join(out, "champion.npy"), np.asarray(tr.champion))
            save_atomic(os.path.join(out, "pool.npy"), np.asarray(jnp.stack(tr.pool)))
            # Only write once a measurement has actually happened -- otherwise
            # best_abs_theta is still the init theta and best_abs.npy would
            # ship a policy that never earned the "best" label. Under the gate
            # the same rule applies one step later, and to the gate's own
            # record rather than to the in-sim one: a nomination is not a
            # record, so the file waits for the real engine's first verdict.
            record = record_theta_ready(tr.best_abs, gate)
            if record:
                save_atomic(os.path.join(out, "best_abs.npy"), np.asarray(tr.best_abs_theta))
            if gate is not None:
                # The in-sim record, which under the gate is no longer the same
                # theta and would otherwise be lost -- it is what an operator
                # comparing the two selectors after the run needs.
                if math.isfinite(tr.best_abs):
                    save_atomic(os.path.join(out, "best_sim.npy"),
                                np.asarray(tr.best_sim_theta))
                gate.save()
            save_state(out, tr, g, elapsed)
            if args.promote and record:
                # Ship `best_abs_theta`: the iterate with the most coins against
                # the fixed archetype yardstick, on the selection half of the
                # fixed seeds. It used to ship `tr.theta`, the last iterate,
                # while `best_abs.npy` was written and then ignored -- and ES on
                # this objective is not monotone, so the last iterate is not the
                # best one. `tr.champion` now selects on the same number at a
                # coarser cadence, so it can only ever tie this, never beat it.
                # Nothing is promoted before the first measurement: until then
                # `best_abs_theta` is the untrained init.
                save_atomic(os.path.join("artifacts", "theta.npy"),
                            np.asarray(tr.best_abs_theta))
        if STOP:
            break
    log.close()
    if gate is not None:
        # An eval in flight owns --real-gate-workers engine processes in its
        # own session; nothing else would reap them. `atexit` holds the same
        # call for the paths that never reach here (a raise, a SystemExit).
        gate.close()
    print("done", flush=True)
