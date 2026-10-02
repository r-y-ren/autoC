# S/snr/step_cosine.py — does the ES step direction persist across blocks?

Built 2026-09-11 for the flow209 / flow210 SGD arms (§72/§73 reading rule).

## What it measures

The trainer saves the champion theta every 10 generations as
`artifacts/<run>/cands/gNNNNN_record.npy`. Differencing consecutive records
gives a **block delta** — under `--optimizer sgd` that is `lr` times the sum of
ten momentum-smoothed gradient estimates, i.e. the block's gradient up to a
constant. The tool restricts each delta to the genes the run was actually
allowed to move and reports, per block:

- `|d| train` / `|d| untr` — step norm on trained vs held genes,
- `cos(k,k+1)` — **the statistic**: does the next block point the same way,
- `cos(k,tot)` — alignment with the whole run's net displacement,
- `cos(-th)` — alignment with `-theta_0`, i.e. how much of the step is just
  decoupled weight decay pulling toward the origin (a shared component in every
  block would inflate the consecutive cosine spuriously),
- the same consecutive cosine **per gene block** (`gp, dh, ds, g5, gb5, w3, b3,
  b1` for these arms), so a persistence carried by one block is visible.

The trained index set is read from the run's own `config.json` `train_only`
and re-derived through `kagg3.es.train.train_mask` × `policy.live_mask` in the
arms-next tree — the same product `Trainer.mask` applies to the perturbation
and the update. For flow209/flow210 that is **1,191 of 6,789**. The tool also
asserts the untrained genes are byte-identical across records (they are:
`Trainer.step` ends `theta = where(mask > 0, upd, theta)`, so held genes do not
even take decay).

## The null — 1/sqrt(d) is NOT it

`Trainer.step` applies momentum to **both** optimizers:
`m = beta1*m + (1-beta1)*grad`, `beta1 = 0.9`; `--optimizer sgd` only swaps the
numerator (`delta = lr*m`, no `sqrt(vhat)` divide). Momentum e-folds over ~9.5
generations, so two consecutive 10-generation block deltas are built from
**heavily overlapping momentum state**. Their cosine is strongly positive even
when every gradient estimate is pure noise.

Three nulls are printed; the verdict must clear all three:

| null | what it is | value on flow209/210 (d=1,191, sgd) |
|---|---|---|
| analytic | `1/sqrt(d_train)`, correct only for `beta1 = 0` | 0.029 |
| permutation | p95 of \|cos\| over 1,000 sign-flips of 64 contiguous units of `d_k` (units start as the run's gene blocks, split largest-norm-first) | run-dependent, ~0.05–0.15 |
| **optimizer** | 200 pure-noise simulations of the run's own optimizer, betas and **its actual record schedule** | **mean +0.51, p95 +0.55** |

The optimizer null binds. It is computed per pair, so it handles `m = 0` at
gen 0 (the first block is a warm-up and has a *lower* null) and uneven record
gaps.

## Validation: flow201 and flow200 (Adam, no held-out gain)

These arms were retired with no held-out gain, so their block cosines are an
empirical null — and they land on the simulated null to two decimals.

```
== flow201  optimizer=adam lr=0.003 sigma=0.02 pop=512  train_only='all' -> d_train=5997
   untrained genes: byte-identical across all records (OK)
   OPTIMIZER NULL (adam, beta1=0.9): consecutive cos under PURE NOISE = +0.2899 (p95 +0.4409)
            block  gens   |d| train   |d| untr  cos(k,k+1)  optnull  cos(k,tot)   perm95  cos(-th)
   g00000->g00010    10     0.88374   0.00e+00      0.4375   0.4241      0.4255   0.1296    0.0138
   g00010->g00020    10     0.54622   0.00e+00      0.1561   0.1557      0.4641   0.0485    0.0456
   g00020->g00140   120     2.43882   0.00e+00          --       --      0.9023       --    0.0375
VERDICT flow201: NOISE -- mean consecutive cos +0.2968 inside the optimizer-momentum null
                 (optimizer +0.2899 p95 +0.4409, analytic 0.0129, perm95 0.1351) over 2 pair(s)
   in-sample: mean_win 0.6107 -> 0.6303 over 206 gens (+0.0195, in-sample, NOT held out)

== flow200  optimizer=adam lr=0.003  records at gens [0, 10, 30]
   g00000->g00010    10     0.86226   0.00e+00      0.3257   0.3350      0.8041   0.0961    0.0212
VERDICT flow200: PENDING -- only 1 consecutive pair (mean cos +0.3257); need >=2 block deltas
```

Observed 0.4375 vs null 0.4241, 0.1561 vs null 0.1557, 0.3257 vs null 0.3350.
Two independent Adam arms sit **on** the momentum null: their steps carried no
direction beyond momentum overlap, which is exactly what their held-out reads
said. The per-gene-block table on flow201 shows no single block above its own
null either — the persistence is uniform momentum, not a live gene.

`cos(-th)` is 0.01–0.05 everywhere, so decoupled weight decay contributes
nothing to the consecutive cosine at these `wd`.

## How to read flow209 / flow210 at g30

Three records (g00000, g00010, g00020, g00030 → note g0 is the seed, so g30
gives **three** block deltas and two consecutive pairs). Run:

```
export JAX_PLATFORMS=cpu
.venv/bin/python S/snr/step_cosine.py --run flow209 --fetch
.venv/bin/python S/snr/step_cosine.py --run flow210 --fetch
```

The bar is **not** 0.029. For the flow209/210 schedule the simulated SGD null
is mean **+0.51**, p95 **+0.55** per pair. So:

- mean consecutive cos **> ~0.55** on both pairs → PERSISTENT: a real gradient
  is being found and the §73 train-only recipe is the first thing at B that
  beats the momentum null. Check the per-gene-block row to see which of
  `gp / dh / ds / g5 / gb5 / w3 / b3 / b1` carries it.
- mean cos **0.45–0.55** → NOISE, indistinguishable from momentum overlap —
  the same verdict flow200/flow201 got. Do not read a positive cosine as
  signal.
- mean cos **below ~0.45** → worse than momentum overlap: the gradient is
  actively anti-correlated across blocks (an overshooting `lr`).

At g30 with only two pairs the sampling sd of the null mean is about 0.02, so
a verdict needs a margin of ~0.05 over p95 to be worth acting on; at g60
(five pairs) it tightens. `cos(k,tot)` climbing toward 1.0 while `cos(k,k+1)`
sits on the null means the net displacement is dominated by one block, not by
a consistent direction.

## Files

- tool: `S/snr/step_cosine.py`
- fetched records: `S/snr/<run>/{config.json,log.jsonl,cands/}` (never overwritten)

## Checkpoint series (`--source records|states|both`, added 2026-09-12)

**The records series has holes.** `Trainer.step` writes
`cands/gNNNNN_record.npy` *only* when the absolute probe accepts a new in-sim
record (`src/kagg3/es/train.py`, the `accepted` branch). A run that is not
improving writes nothing: at 00:15Z flow210 had records at g0 and g10 and
none at g20, so the records series could not produce a second block delta at
all.

**The centre is checkpointed unconditionally.** `scripts/train.py:save_state`
writes `artifacts/<run>/state.npz` every `--ckpt-every` (10) generations, and
that file is **overwritten** each time. Its keys:

| key | what it is |
|---|---|
| **`theta`** | **the ES centre** — `tr.theta`, the iterate the perturbations are drawn around. **This is the series.** |
| `champion` | `tr.champion`, the coarse-cadence selection on `best_abs`. Not the centre (it happened to equal `theta` on flow210 g20). |
| `best_abs_theta` | the record — what `best_abs.npy` ships. **Not** the centre. |
| **`m`** | **the optimizer momentum buffer** (`m = beta1*m + (1-beta1)*grad`), 1,191 nonzero = exactly `d_train`; masked like the update. |
| `v` | Adam's second moment — all zeros under `--optimizer sgd`, which never touches it. |
| `gen`, `t`, `adam_t` | the generation this snapshot is (all 20 on flow210's g20 file). |
| `sigma`, `key`, `rng_state`, `pool`, `archetypes`, `ladder_sig`, `best_abs`, `best_hold`, `last_improve`, `elapsed`, … | resume state, not read here. |

**The two series are the same quantity.** The record file is
`self.theta` at the generation it was nominated, so where both exist they must
agree — and they do byte-for-byte: flow209's `cands/g00010_record.npy` is
identical to `theta` in `state_g00010.npz` (‖diff‖ = 0.0). `g00000` in a states
series is taken from the gen-0 record, which is the centre before the first
step. So `states` is strictly the better-sampled view of the identical object;
use it whenever a record is missing.

### Keeping the checkpoints: `S/snr/keep_state.sh <run>`

```
S/snr/keep_state.sh flow210            # scp ~/stage_hr/artifacts/flow210/state.npz
S/snr/keep_state.sh flow209 user@remote-host ~/stage_hr/artifacts
```

It reads `gen` out of the fetched file and stores it as
`S/snr/<run>/state_g<gen:05d>.npz`, **never overwriting** an existing
generation (a second call between two checkpoints is a no-op), and adopts any
`state_latest.npz` the coordinator dropped in the run directory first. Run it
once per checkpoint — a generation whose `state.npz` is overwritten before it
is copied is gone.

### Reading it

```
export JAX_PLATFORMS=cpu
S/snr/keep_state.sh flow210
.venv/bin/python S/snr/step_cosine.py --run flow210 --source states
```

`--source both` (the default) runs each series that is present and tags the
second verdict `VERDICT <run> [states]`; `--source records` is unchanged in
behaviour (flow201 reproduces 0.4375 / 0.1561 against nulls 0.4241 / 0.1557 to
the digit). The optimizer null is re-simulated **on the gaps of whichever
series is read**, so a states series sampled at [0, 20] is judged against a
20-generation null, not a 10-generation one.

### The momentum readout

When the newest state file is at the series' last generation, the tool prints
the cosine between the last block's centre delta and the **saved `m`**, with
its own simulated null:

```
   MOMENTUM (state_g00020.npz key 'm'): cos(block g00000->g00020, m) = +0.9206
                                        null +0.6264 (p95 +0.6522)
```

**How to read it.** `m` is the direction the *next* step takes (`theta +=
lr*m`), and the block delta is the sum of the `m`s that end on this one, so the
null is high by construction — never compare it to 0. Above p95 means the run
is still being pushed the way the block just went; below means the block's
final generations already turned away from it.

**Do not promote flow210's +0.92 on its own.** The null above is isotropic
(iid standard-normal gradient estimates). Re-simulating it with per-coordinate
gradient *scales* taken from the observed delta lifts p95 to +0.78, and with
the square of that profile to +0.98 — i.e. a purely heteroscedastic noise
gradient, with no mean at all, reproduces +0.92. The readout is a cheap
first look, not a verdict; the consecutive-block cosine at g30/g40 remains the
statistic that decides §84.

### First states read (2026-09-12 00:28Z)

`--source states` on **flow209** at [g0, g10, g20] — a series the records path
could not build, because g20 never earned a record file:

```
   g00000->g00010    10     0.00710   0.00e+00      0.8168   0.5122      0.9403   0.2466   -0.0237
   g00010->g00020    10     0.00914   0.00e+00          --       --      0.9644       --   -0.0267
   per gene block: gp 0.7231  dh 0.8809  ds 0.9980  g5 0.8607  gb5 0.9983  w3 0.7574  b3 1.0000  b1 0.9078
VERDICT flow209 [states]: PENDING -- only 1 consecutive pair (mean cos +0.8168)
```

**+0.8168 against an optimizer-null p95 of +0.5443** (perm95 0.2466), and every
one of the eight trained gene blocks is above its own null — the first block
cosine in this campaign to clear the momentum null. The anisotropy objection
that sinks the momentum readout does **not** sink this one: re-simulating the
pair null with per-coordinate scales from the observed deltas moves p95 only
+0.5452 → +0.6068 (the squared profile, which is not a credible scale model,
reaches +0.8921). Two blocks of a 20-generation run are still one pair, so the
verdict stays PENDING until g30 gives a second.

flow210 at [g0, g20] has one block and no pair; its `cos(block, m)` = +0.9206
is inside the anisotropic null and carries nothing on its own.
