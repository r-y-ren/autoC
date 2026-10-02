# LOTS: a 130-gene sell-lot block, staged and inert (2026-09-11)

**Claim under test** — not "this lever pays" but *"the gene set is not
expressive enough"*. The ES at B is dimension-limited (`es-noise-floor` §72:
cosine 0.039 = P/(P+d) → cut **d**), and a blind review ranked the sell
interface the first bottleneck. Each product states one `hold` and one
**non-negative** `press`; lot marginals are
`quote − press × lot_index + externality`: one monotone ramp, same shape and
sign for every product. `lots` states two **independently signed** coin offsets
per product, on lots 1 and 2. Lot 0 is pinned at 0 — a *common* offset on all
three lots is the reservation, which already exists.

**Copy tree only** (`/root/wt_lots`); `src/` in `arms-next` and main untouched,
both `git diff --stat src/` empty. Patch `S/lots/policy_lots.patch` (8 files,
`patch -p1` dry-run clean, md5 db2fe4ef).

One block `("lots", (65, 2))` appended **last** in `policy.py` — 64 rows off the
shared encoder hidden `h` (the one `press` reads) plus a bias row: **130 genes,
6,789 → 6,919**, `offset == 6789`. One block, not a `w4`/`b4` pair, so
`--train-only lots` *is* the whole gene. `brain.py` decodes
`round(LOTS_GAIN·z)`, `LOTS_GAIN = 8.0`, clipped ±`COIN_CAP`. `sell.py` adds it
**outside** the existing expression (`lot_off=None` compiles the original line
and no add). `Macro.lot_off` is `int[3, 9]`, not the brief's `[9, 2]` — sell's
arrays are lot-major and `[9, 2]` costs a transpose inside the 100-round
allocator loop; threaded to all three sites that rank a lot marginal.

**Inert at zero — proved.** B padded decodes byte for byte against the pristine
tree: 300 decisions × *every* Macro integer **and** 3 full self-play seasons
(per-day money, per-day rows, end kind/occ/shed/money). 19 arrays, **0
differences**; 20/20 checks PASS.

**Decodable at σ — measured** (`gene-slope-check`; flow151's gene was 100 %
dead). sd(z) = σ√(‖h‖²+1) = 0.0572 at σ 0.01 (‖h‖ = 5.63 on B). **27.3 %** of
(product, day, board, member) cells decode ≥ 1 coin (2.2 M cells; per-board
p10/p50/p90 0.23/0.27/0.32) — `FWD_DAYS_GAIN`'s own minority band.

**The arm.** `S/lots/launch_flow208.sh` (md5 749f7a85), **NOT launched**:
flow206's recipe with six tokens moved — `~/stage_lots`, `--train-only lots`,
`--sigma 0.01`, `--lr 2e-3 --optimizer sgd`, `--weight-decay 0`, fresh
seed/run. Decay needs no new flag: `apply_gradient` ends
`theta = where(mask > 0, upd, theta)`, so the mask scopes decay, step and
perturbation to the 130 coordinates. `lr` is derived, not measured:
‖g‖ ≈ √(256·0.25·130)/(512·0.01) = 17.8 and ‖δ‖ ≈ σ√130/3 = 0.038 give 2.1e-3
→ **2e-3** (±30 %).

**Caveat that bites first.** `S/simscreen`, `S/seedroom`, `S/onestep_pin`,
`S/dither`, `S/autojudge/watch.sh` pin the `arms-next` tree at 6,789 and will
**refuse** a 6,919 candidate. Nothing else pins the length.

**Side finding.** `test_backend_agreement.py` fails on `hire_bias numpy=33
jax=32` — identically in untouched `arms-next`, on a 4,848-long theta.
Pre-existing numpy/XLA cliff, left alone. 163/164 repo tests pass.

**No fitness claim.** Expressible, inert, decodable — flow208 measures the rest.
