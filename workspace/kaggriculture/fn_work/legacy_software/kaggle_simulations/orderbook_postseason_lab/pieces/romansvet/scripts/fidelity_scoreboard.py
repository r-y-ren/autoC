#!/usr/bin/env python
"""Which in-sim statistic ranks thetas the way the real engine does?

The run selects on **one** number -- the `kagg2_flow` rung's margin on the
selection half of the fixed seeds, at the centre of the rung's randomisation
(`Trainer.absolute_report`, `Trainer.selection_score`). Whether that number is
the *right* one is an empirical question, and `artifacts/kagg2_track.tsv` plus
`artifacts/kagg2_games/` is the only place it can be answered: every row there
is a theta measured in the **real** engine against kaggriculture2, and since
2026-08-27 08:08 the theta itself is archived beside its per-game CSV.

So: take every archived theta that has a real row, compute a menu of candidate
in-sim statistics for each, and rank-correlate each statistic against the real
margin and the real win rate. A statistic that cannot reproduce the ordering
the real engine gave is not a yardstick, however cheap it is to measure.

Nothing here is a training run and nothing here writes to a run directory. The
Trainer is built with the live runs' flags (see `~/launch_flow6.sh`), resumed
**read-only** from a checkpoint for its ladder, and then only asked questions.

Usage (on the GPU host, from the repo root):

    XLA_PYTHON_CLIENT_PREALLOCATE=false CUDA_VISIBLE_DEVICES=0 \
        .venv/bin/python scripts/fidelity_scoreboard.py --resume artifacts/flow4

Add `--tsv PATH` to keep the table, `--verify-determinism` to re-measure one
theta and print the largest disagreement.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import math
import os
import sys
import time

import numpy as np

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (os.path.join(_ROOT, "src"), os.path.join(_ROOT, "scripts")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import jax.numpy as jnp                                         # noqa: E402

from kagg3.es import archetypes as AR                           # noqa: E402
from kagg3.es import kagg2_flow as K2F                          # noqa: E402
from kagg3.es.train import (Config, Trainer, cold_starts,       # noqa: E402
                            place_handicap, win_scores)
# `scripts/train.py` is guarded by `if __name__ == "__main__"`, so importing it
# gets the flag parsing and the resume/anchor helpers without running anything.
# They are imported rather than copied on purpose: a fidelity check built on a
# *replica* of the live construction would be measuring the replica.
import train as T                                               # noqa: E402

#: The opponent column of an `eval_vs_baselines.py --csv` file names the
#: packaged agent by path; anything that is not the engine's builtin is kagg2.
STARTER = "starter"

#: The flow rung's centre: scale 1.0 (in thousandths) and no day shift. This is
#: what `Trainer.absolute_report` measures at, and what statistic (a) is.
CENTRE = (1000, 0)

#: The seed the whole campaign draws its fixed things from -- the absolute
#: seed set (`Trainer.__init__`) and, here, the flow ensemble's draws.
FIXED_SEED = 20260823


# --------------------------------------------------------------------- trainer

def build_trainer(resume=None, seed=61, quiet=False):
    """A Trainer carrying the live runs' ladder, built the way they build it.

    The flags are `~/launch_flow6.sh`'s, in the order `scripts/train.py:main`
    applies them: Config -> Trainer (which appends the flow rung) -> resume
    (which restores the checkpoint's archetypes) -> anchors.

    Only the *ladder* matters here -- `absolute_report` reads `archetypes`,
    `arch_handicap`, `rung_weights`, `holdout_thetas` and `abs_words`, and
    nothing else -- but the resume is taken through `load_resume` anyway so
    that a ladder difference between this and the live runs is impossible
    rather than merely unlikely.
    """
    anchors = (("anchor", "artifacts/feed2/best_abs.npy"),
               ("anchor3", "artifacts/feed3/best_abs.npy"),
               ("anchor4", "artifacts/kagg2_games/thetas/flow3_g7833.npy"),
               ("anchor5", "artifacts/kagg2_games/thetas/flow4_g10133.npy"))
    anchor_weight = tuple((n, 1.0) for n, _ in anchors)
    cfg = Config(pop=128, episodes=64, chunk=8192,
                 n_archetypes=9, arch_frac=0.5,
                 abs_weight=0.3, abs_every=25, abs_pairs=64,
                 rung_weight=(("kagg2_flow", 6.0), ("anchor", 1.0)),
                 proxy_handicap=T.parse_handicap("1:87000"),
                 select_metric="margin:kagg2_flow", best_gate="both",
                 stall_sigma_mult=1.0, restart_stall=1500,
                 kagg2_flow=True, kagg2_flow_scale=(0.5, 1.5),
                 kagg2_flow_jitter=2)
    # `--rung-weight anchor=1` is stated on the command line but the anchor is
    # not in the ladder `Trainer.__init__` binds against, so `main` splits it
    # out and hands it to `add_anchor_rungs`. Mirrored here: `cfg.rung_weight`
    # holds `kagg2_flow=6` only.
    cfg = cfg._replace(rung_weight=(("kagg2_flow", 6.0),))
    tr = Trainer(cfg, seed=seed, pending_rungs=[n for n, _ in anchors])
    if resume:
        start_gen, how, _ = T.load_resume(tr, resume)
        if not quiet:
            print(f"# ladder resumed from {resume} via {how} (gen {start_gen})")
    T.add_anchor_rungs(tr, anchors, anchor_weight)
    if not quiet:
        print("# rungs: " + ", ".join(
            f"{n}(w={w:g})" for n, w in zip(tr.archetype_names, tr.rung_weights)))
        print(f"# holdout rungs: {', '.join(h[0] for h in tr.holdout_thetas)}")
        print(f"# abs_pairs={cfg.abs_pairs} n_abs_sel={tr.n_abs_sel} "
              f"flow_rung={tr.flow_rung} margin_scale={cfg.margin_scale:,.0f}")
    return tr


# ----------------------------------------------------------------- measurement

def abs_batch(tr, theta, scale_milli=1000, shift=0):
    """`Trainer.absolute_report`'s batch, with the flow rung's level as an argument.

    Byte-for-byte the layout `absolute_report` builds -- same rung order, same
    seed/seat decomposition, same handicap side, same fixed seed set -- with one
    change: the flow rung's `(scale, shift)` is a parameter instead of being
    pinned to the centre. At `CENTRE` this reproduces `absolute_report` exactly,
    which `stats_for` asserts rather than assumes.

    Returns `(money[total, 2], rung index[total], seed index[total])`. Per game,
    not aggregated: every statistic below is some other reduction of this array,
    so one batch answers all of them.
    """
    arch = list(tr.archetypes)
    held = list(tr.holdout_thetas)
    rungs = arch + [h[1] for h in held]
    starts = np.concatenate([
        np.asarray(tr.arch_handicap, np.int32).reshape(-1, 2),
        np.asarray([h[2] for h in held], np.int32).reshape(-1, 2)])
    r = len(rungs)
    n_pairs = int(tr.abs_words.shape[0])
    total = 2 * n_pairs * r
    k = np.arange(total)
    a_idx = k % r
    seat = ((k // r) % 2).astype(np.int32)
    widx = k // (2 * r)
    nq, mo = cold_starts(total)
    nq, mo = place_handicap(nq, mo, 1 - seat.astype(np.int64), starts[a_idx])
    money = np.asarray(tr._eval(
        tr.tables,
        jnp.broadcast_to(theta, (total, theta.shape[0])),
        jnp.stack([rungs[i] for i in a_idx]),
        tr.abs_words[jnp.asarray(widx)],
        jnp.asarray(seat), jnp.asarray(nq), jnp.asarray(mo),
        flow=tr.flow_words(a_idx == tr.flow_rung, 1 - seat,
                           int(scale_milli), int(shift))))
    return money, a_idx, widx


def ensemble_draws(cfg, k=4, seed=FIXED_SEED):
    """`k` fixed `(scale_milli, shift)` pairs, drawn as `Trainer.episode_flow` draws.

    Same generator, same two calls in the same order, so an ensemble member is
    a level a training episode could actually have been played at rather than a
    grid someone chose.
    """
    rng = np.random.default_rng(seed)
    lo, hi = cfg.kagg2_flow_scale
    j = int(cfg.kagg2_flow_jitter)
    scale = np.rint(rng.uniform(lo, hi, k) * 1000).astype(np.int32)
    shift = rng.integers(-j, j + 1, k).astype(np.int32)
    return list(zip([int(x) for x in scale], [int(x) for x in shift]))


def _sig(x, scale):
    return float(np.mean(1.0 / (1.0 + np.exp(-np.asarray(x, float) / scale))))


def parse_grid_point(text):
    """`"1250"` -> (1250, 0); `"1250:2"` -> (1250, 2)."""
    scale, _, shift = text.strip().partition(":")
    return int(scale), int(shift or 0)


def stats_for(tr, theta, draws, grid=(), check=True):
    """Every candidate statistic for one theta. -> dict[str, float].

    One `abs_batch` at the centre answers (a), (b), (c), (f), (g), (h) and (i);
    one per ensemble draw answers (d) and (e). `absolute_report` is called once
    more as a cross-check that this file's replica of its batch is the same
    measurement, because a fidelity table computed off a subtly different batch
    would be a table about this file.
    """
    cfg = tr.cfg
    a = len(tr.archetypes)
    f = tr.flow_rung
    n_sel = tr.n_abs_sel
    out = {}

    money, a_idx, widx = abs_batch(tr, theta, *CENTRE)
    m = money[:, 0] - money[:, 1]
    win = np.asarray(win_scores(money[:, 0], money[:, 1]))
    sel = widx < n_sel
    isf = a_idx == f

    # (a) today's statistic, (b) all 64, (c) the holdout half.
    out["a_flow_margin_sel"] = float(m[isf & sel].mean())
    out["b_flow_margin_all64"] = float(m[isf].mean())
    out["c_flow_margin_hold"] = float(m[isf & ~sel].mean())
    # (f) the same rung's win rate, and its sigmoid at scales that actually
    # have slope over a +-15k margin (the shipped `margin_scale` is 100k).
    out["f1_flow_win_sel"] = float(win[isf & sel].mean())
    out["f2_flow_sig10k_sel"] = _sig(m[isf & sel], 10_000.0)
    out["f3_flow_sig20k_sel"] = _sig(m[isf & sel], 20_000.0)
    out["f4_flow_win_all64"] = float(win[isf].mean())
    # (i) the whole ladder, flat and as the yardstick weights it, plus the
    # worst rung -- a theta that beats the flow rung by collapsing against
    # everything else is what the min is here to catch.
    per_rung = np.array([m[(a_idx == i) & sel].mean() for i in range(a)])
    out["i1_mean_margin_rungs"] = float(per_rung.mean())
    out["i1w_wmean_margin_rungs"] = float(np.average(per_rung, weights=tr.rung_weights))
    out["i2_min_margin_rungs"] = float(per_rung.min())
    # The opponent holdout: rungs nothing selects on, whole seed set.
    for i, (label, _, _) in enumerate(tr.holdout_thetas):
        h = a_idx == a + i
        out[f"o_hold_{label.split('@')[0]}_margin"] = float(m[h].mean())

    # (d)/(e) the randomised ensemble. Each draw is a whole 64-pair reading, so
    # the CVaR is over draw means rather than over games: the question is which
    # *level of the opponent* the theta is weakest against.
    per_draw = []
    for scale, shift in draws:
        dm, da, _ = abs_batch(tr, theta, scale, shift)
        per_draw.append(float((dm[:, 0] - dm[:, 1])[da == f].mean()))
    if per_draw:   # `--draws 0` sweeps the level grid alone
        out["d_flow_margin_ens"] = float(np.mean(per_draw))
        out["e_flow_margin_ens_cvar2"] = float(np.mean(sorted(per_draw)[:2]))
        out["e2_flow_margin_ens_min"] = float(min(per_draw))
    # Each ensemble member on its own, so a table can answer "is it the
    # averaging that helps, or just this one level?" -- with `default_rng`'s
    # first four draws all landing under scale 1.0, that is not a rhetorical
    # question: the ensemble mean is also a *weaker* flow rung than the centre.
    for (scale, shift), v in zip(draws, per_draw):
        out[f"k_draw_s{scale}_d{shift:+d}"] = v

    # A deterministic sweep of the flow rung's level at no day shift. The
    # ensemble above answers "does randomising help"; this answers the cheaper
    # question underneath it -- "is the *centre* simply the wrong level?" --
    # because its mean is symmetric about the centre where the drawn one is not.
    per_level = []
    for scale, shift in grid:
        gm, ga, _ = abs_batch(tr, theta, scale, shift)
        v = float((gm[:, 0] - gm[:, 1])[ga == f].mean())
        per_level.append(v)
        out[f"l_level_s{scale}_d{shift:+d}"] = v
    if per_level:
        out["d2_grid_mean"] = float(np.mean(per_level))
        out["e3_grid_cvar2"] = float(np.mean(sorted(per_level)[:2]))

    # (g)/(h) straight off the live report, so they are the numbers the run
    # itself would print for this theta.
    rep = tr.absolute_report(theta)
    out["g_holdout_coins"] = float(rep.holdout)
    out["g2_abs_coins_sel"] = float(rep.coins)
    out["g3_holdout_win"] = float(rep.holdout_win)
    out["h_selection_score"] = float(tr.selection_score(rep))
    out["h2_holdout_selection"] = float(tr.holdout_selection_score(rep))
    out["h3_abs_score_100k"] = float(rep.score)
    # (j) the shape `fitness` blends at, evaluated on the yardstick instead of
    # on a population: `abs_weight` on coins, the rest on the margin sigmoid.
    # Not a selection metric today -- `--select-metric margin:kagg2_flow` reads
    # one rung -- but it is the blend the *gradient* sees, so it belongs here.
    out["j_blend_abs0.3"] = float(
        cfg.abs_weight * math.log1p(max(rep.coins, 0.0)) / math.log1p(200_000.0)
        + (1.0 - cfg.abs_weight) * _sig(m[isf & sel], 20_000.0))

    if check:
        want = rep.mine[f] - rep.theirs[f]
        got = out["a_flow_margin_sel"]
        if abs(want - got) > 1.0:
            raise SystemExit(
                f"replica disagrees with absolute_report on the flow rung: "
                f"{got:,.1f} vs {want:,.1f}. The batch in `abs_batch` is no "
                f"longer the batch `absolute_report` builds; fix it before "
                f"reading anything below as a fidelity result.")
    return out


# ----------------------------------------------------------------------- truth

def _digest(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


def read_track(path):
    """`artifacts/kagg2_track.tsv` -> list of dicts, comment lines dropped."""
    rows, cols = [], None
    with open(path) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.lstrip("# ").split("\t")
            if parts[0] == "ts":
                cols = parts
                continue
            if cols is None or line.startswith("#"):
                continue
            rows.append(dict(zip(cols, parts)))
    return rows


def read_games(path):
    """The kagg2 games of one `eval_vs_baselines.py --csv`. -> (margins, wins)."""
    margins, wins = [], []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["opponent"] == STARTER:
                continue
            mine, theirs = float(r["mine"]), float(r["theirs"])
            margins.append(mine - theirs)
            wins.append(1.0 if mine > theirs else (0.5 if mine == theirs else 0.0))
    return margins, wins


def archived_panel(art):
    """Every archived theta with its per-game CSVs, deduplicated by content.

    `remote_eval_kagg2.sh` copies the measured `best_abs.npy` to
    `kagg2_games/thetas/<run>_g<gen>.npy` beside `kagg2_games/<run>_<gen>.csv`,
    so the pairing is by name. Two archived files are routinely the *same*
    theta (a snapshot run re-measuring a record its parent never beat), and
    those are one panel entry with two real readings, not two.
    """
    tdir = os.path.join(art, "kagg2_games", "thetas")
    by_hash = {}
    for fn in sorted(os.listdir(tdir)):
        if not fn.endswith(".npy"):
            continue
        stem = fn[:-4]
        run, _, gen = stem.rpartition("_g")
        csv_path = os.path.join(art, "kagg2_games", f"{run}_{gen}.csv")
        if not os.path.isfile(csv_path):
            print(f"# skip {fn}: no per-game CSV at {csv_path}")
            continue
        path = os.path.join(tdir, fn)
        h = _digest(path)
        e = by_hash.setdefault(h, {"path": path, "names": [], "csvs": []})
        e["names"].append(stem)
        e["csvs"].append(csv_path)
    return by_hash


def inferred_panel(art, track, runs, live):
    """`artifacts/<run>/best_abs.npy` for runs whose last real row still describes it.

    Only thetas archived after 2026-08-27 08:08 sit in `kagg2_games/thetas/`;
    before that the tracker measured `best_abs.npy` in place and the file was
    free to move on afterwards. A dead run's file can still be matched to its
    last row, but only when all four of these hold, and the run is dropped
    rather than guessed at when any of them does not:

    * the run is not training right now (its theta would be moving under us);
    * the last row's generation is the run's last logged generation, which is
      the generation `remote_eval_kagg2.sh` labels a row with;
    * `best_abs.npy` has not been written since that row was measured;
    * the row's per-game CSV is still on disk.
    """
    out = {}
    for run in runs:
        if run in live:
            print(f"# skip {run}: still training")
            continue
        theta = os.path.join(art, run, "best_abs.npy")
        log = os.path.join(art, run, "log.jsonl")
        rows = [r for r in track if r["run"] == run]
        if not rows or not os.path.isfile(theta) or not os.path.isfile(log):
            print(f"# skip {run}: no theta, log or row")
            continue
        row = rows[-1]
        with open(log, "rb") as fh:
            fh.seek(max(0, os.path.getsize(log) - 4096))
            tail = fh.read().decode(errors="replace").strip().splitlines()[-1]
        gen = tail.partition('"gen":')[2].partition(",")[0].strip()
        if gen != row["gen"]:
            print(f"# skip {run}: last row is gen {row['gen']}, log ends at {gen}")
            continue
        row_ts = time.mktime(time.strptime(row["ts"][:19], "%Y-%m-%dT%H:%M:%S"))
        if os.path.getmtime(theta) > row_ts:
            print(f"# skip {run}: best_abs.npy was written after its last row")
            continue
        csv_path = os.path.join(art, "kagg2_games", f"{run}_{row['gen']}.csv")
        if not os.path.isfile(csv_path):
            print(f"# skip {run}: no per-game CSV at {csv_path}")
            continue
        out[_digest(theta)] = {"path": theta, "names": [f"{run}_g{row['gen']}"],
                               "csvs": [csv_path]}
    return out


def build_panel(art, infer, live):
    """The measured thetas, merged by content hash and given their real numbers.

    A theta's truth is the **largest** single real reading it has (the 96-game
    snapshot row where there is one, the 48-game row otherwise); `pooled_*` is
    every distinct reading it has, which is the same thing when there is only
    one. Two byte-identical CSVs are one reading -- the tracker re-measures a
    theta whose record has not moved, and a repeat of a deterministic
    measurement is not new evidence.
    """
    panel = archived_panel(art)
    for h, e in inferred_panel(art, read_track(os.path.join(art, "kagg2_track.tsv")),
                               infer, live).items():
        if h in panel:
            for c in e["csvs"]:
                if c not in panel[h]["csvs"]:
                    panel[h]["csvs"].append(c)
        else:
            panel[h] = e
    out = []
    for h, e in panel.items():
        seen, readings, pooled_m, pooled_w = set(), [], [], []
        for c in sorted(e["csvs"]):
            d = _digest(c)
            if d in seen:
                continue
            seen.add(d)
            mg, wn = read_games(c)
            readings.append((os.path.basename(c), len(mg), float(np.mean(mg)),
                             100.0 * float(np.mean(wn))))
            pooled_m += mg
            pooled_w += wn
        if not readings:
            continue
        best = max(readings, key=lambda r: r[1])
        out.append({
            "name": sorted(e["names"], key=len)[0],
            "aka": [n for n in sorted(e["names"]) if n != sorted(e["names"], key=len)[0]],
            "path": e["path"], "hash": h, "readings": readings,
            "n": best[1], "real_margin": best[2], "real_win": best[3],
            "pooled_n": len(pooled_m), "pooled_margin": float(np.mean(pooled_m)),
            "pooled_win": 100.0 * float(np.mean(pooled_w))})
    return sorted(out, key=lambda e: e["real_margin"])


# ------------------------------------------------------------------ statistics

def rankdata(x):
    """Average ranks, ties shared -- what a Spearman on 8 points needs."""
    x = np.asarray(x, float)
    order = np.argsort(x, kind="mergesort")
    r = np.empty(len(x), float)
    r[order] = np.arange(1, len(x) + 1, dtype=float)
    for v in np.unique(x):
        m = x == v
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a - a.mean(), b - b.mean()
    d = math.sqrt(float((a * a).sum()) * float((b * b).sum()))
    return float((a * b).sum() / d) if d > 0 else float("nan")


def spearman(x, y):
    return pearson(rankdata(x), rankdata(y))


def perm_p(x, y, n_perm=20000, seed=7):
    """Two-sided permutation p for a Spearman on a handful of points.

    n is 8. The normal approximation everyone quotes for rho is not valid
    there, and a permutation over the actual ranks is exact enough and costs
    milliseconds.
    """
    rx, ry = rankdata(x), rankdata(y)
    obs = abs(pearson(rx, ry))
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(n_perm):
        if abs(pearson(rx, rng.permutation(ry))) >= obs - 1e-12:
            hits += 1
    return (hits + 1) / (n_perm + 1)


def loo_spearman(x, y):
    """(min, max) Spearman over the n leave-one-out subsets."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    vals = [spearman(np.delete(x, i), np.delete(y, i)) for i in range(len(x))]
    return float(min(vals)), float(max(vals))


def order_ok(names, values, wanted):
    """Does this statistic put `wanted` in the order it is written in?"""
    idx = {n: i for i, n in enumerate(names)}
    have = [values[idx[w]] for w in wanted if w in idx]
    if len(have) < len(wanted):
        return None
    return all(a > b for a, b in zip(have, have[1:]))


# ---------------------------------------------------------------------- report

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--artifacts", default="artifacts")
    ap.add_argument("--resume", default="artifacts/flow4",
                    help="checkpoint to take the ladder from, read-only")
    ap.add_argument("--seed", type=int, default=61)
    ap.add_argument("--draws", type=int, default=4, help="flow ensemble members")
    ap.add_argument("--grid", default="",
                    help="comma-separated flow levels to sweep: SCALE (thousandths, "
                         "shift 0) or SCALE:SHIFT, e.g. 500,750,1250:2,1500:-2")
    ap.add_argument("--infer", default="feed1,feed3,feed4",
                    help="runs whose best_abs.npy still matches their last row")
    ap.add_argument("--live", default="flow5,flow6",
                    help="runs training right now; never inferred from")
    ap.add_argument("--order", default="flow4_g10133,flow3_g7833,flow5_g14510",
                    help="the ordering a yardstick has to recover")
    ap.add_argument("--tsv", default=None, help="write the theta x statistic table here")
    ap.add_argument("--verify-determinism", action="store_true",
                    help="measure one theta twice and print the worst disagreement")
    args = ap.parse_args()

    art = args.artifacts
    panel = build_panel(art, [r for r in args.infer.split(",") if r],
                        {r for r in args.live.split(",") if r})
    if len(panel) < 3:
        raise SystemExit(f"only {len(panel)} measured thetas; nothing to correlate.")
    print(f"# panel: {len(panel)} distinct thetas")
    for e in panel:
        aka = f"  (= {', '.join(e['aka'])})" if e["aka"] else ""
        print(f"#   {e['name']:<22} {e['hash']}  n={e['n']:<3} "
              f"margin={e['real_margin']:+8.0f} win={e['real_win']:4.1f}%{aka}")
        for fn, n, mg, wn in e["readings"]:
            print(f"#       {fn:<34} n={n:<3} {mg:+8.0f} {wn:4.1f}%")

    tr = build_trainer(args.resume, args.seed)
    draws = ensemble_draws(tr.cfg, args.draws)
    grid = tuple(parse_grid_point(x) for x in args.grid.split(",") if x.strip())
    print(f"# flow ensemble draws (scale_milli, shift): {draws}")
    if grid:
        print(f"# flow level sweep (scale_milli, shift): {list(grid)}")

    t0 = time.time()
    for e in panel:
        theta = jnp.asarray(np.load(e["path"]).astype(np.float32))
        e["stats"] = stats_for(tr, theta, draws, grid)
        print(f"# measured {e['name']} in {time.time() - t0:6.1f}s", flush=True)

    if args.verify_determinism:
        e = panel[-1]
        again = stats_for(tr, jnp.asarray(np.load(e["path"]).astype(np.float32)),
                          draws, grid)
        worst = max(((abs(again[k] - e["stats"][k]), k) for k in again),
                    key=lambda p: p[0])
        print(f"# determinism: re-measuring {e['name']} moved "
              f"{worst[1]} by {worst[0]:.6g}")

    keys = [k for k in panel[0]["stats"] if not k.startswith("_")]
    names = [e["name"] for e in panel]
    wanted = [w for w in args.order.split(",") if w]

    # ---- theta x statistic
    print("\n## theta x statistic (rows sorted by real margin, worst first)\n")
    head = ["statistic"] + [n.replace("_g", "\ng") for n in names]
    w0 = max(len(k) for k in keys) + 2
    print(f"{'real_margin':<{w0}}" + "".join(f"{e['real_margin']:>12,.0f}" for e in panel))
    print(f"{'real_win%':<{w0}}" + "".join(f"{e['real_win']:>12.1f}" for e in panel))
    print(f"{'real_n':<{w0}}" + "".join(f"{e['n']:>12d}" for e in panel))
    print(f"{'theta':<{w0}}" + "".join(f"{n[-11:]:>12}" for n in names))
    print("-" * (w0 + 12 * len(names)))
    for k in keys:
        print(f"{k:<{w0}}" + "".join(f"{e['stats'][k]:>12,.4g}" for e in panel))

    # ---- correlations
    print("\n## rank correlation against the real engine "
          f"(n={len(panel)}; LOO = leave-one-out range)\n")
    print(f"{'statistic':<{w0}}{'rho_margin':>11}{'p':>8}{'LOO_margin':>20}"
          f"{'rho_win':>9}{'p':>8}{'order':>8}")
    rows = []
    for k in keys:
        v = [e["stats"][k] for e in panel]
        rm = spearman(v, [e["real_margin"] for e in panel])
        rw = spearman(v, [e["real_win"] for e in panel])
        lo, hi = loo_spearman(v, [e["real_margin"] for e in panel])
        ok = order_ok(names, v, wanted)
        rows.append((rm, k, rw, lo, hi, ok))
        print(f"{k:<{w0}}{rm:>11.3f}"
              f"{perm_p(v, [e['real_margin'] for e in panel]):>8.4f}"
              f"{f'[{lo:+.2f}, {hi:+.2f}]':>20}{rw:>9.3f}"
              f"{perm_p(v, [e['real_win'] for e in panel]):>8.4f}"
              f"{('yes' if ok else 'NO') if ok is not None else '-':>8}")

    print(f"\n## order to recover: {' > '.join(wanted)}")
    for rm, k, rw, lo, hi, ok in sorted(rows, reverse=True):
        if ok:
            print(f"   {k:<{w0}} rho_margin={rm:+.3f} rho_win={rw:+.3f} "
                  f"LOO=[{lo:+.2f}, {hi:+.2f}]")

    if args.tsv:
        with open(args.tsv, "w") as fh:
            fh.write("statistic\t" + "\t".join(names) + "\treal_margin_rho\treal_win_rho\n")
            fh.write("real_margin\t" + "\t".join(f"{e['real_margin']:.1f}" for e in panel)
                     + "\t\t\n")
            fh.write("real_win\t" + "\t".join(f"{e['real_win']:.1f}" for e in panel)
                     + "\t\t\n")
            for k in keys:
                v = [e["stats"][k] for e in panel]
                fh.write(k + "\t" + "\t".join(f"{x:.6g}" for x in v)
                         + f"\t{spearman(v, [e['real_margin'] for e in panel]):.4f}"
                         + f"\t{spearman(v, [e['real_win'] for e in panel]):.4f}\n")
        print(f"\n# wrote {args.tsv}")


if __name__ == "__main__":
    main()
