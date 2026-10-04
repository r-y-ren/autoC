# S/simscreen rebuilt as a CPU tool, validated, and used as a pre-filter

2026-09-11, build agent (70-min box). Tool: `S/simscreen/screen.py` (+ `README.md`).
Data: `S/simscreen/full40.csv`, `S/simscreen/full40_noswitches.csv`, `S/simscreen/boards.json`.

## What was rebuilt

The 2026-09-06 tool was **not** lost with `/tmp`: the pre-wipe source survives at
`S/_recovered/simscreen/screen.py`. The rebuild keeps its engine-faithful core
(action-seat opponent, `shop_crn`, both seats, cold start) and replaces the front end:

* **pinned towns, not open-loop tapes.** Boards are `artifacts/tape_actions_town/<id>.npz`,
  which carry the episode's recorded town; `sim.eod.unlock_shop` then replaces the board's
  shop draw with the recording. This is the only regime in which the action-seat sim IS the
  engine (2026-09-09-sim-vs-leg20.md: 7 pinned rungs, mean |sim − engine| = 85 coins on
  ±20k margins, Spearman +1.00, 100 % sign agreement — versus +12k optimism and 47 % sign
  agreement on the same tapes played open-loop).
* **a frozen board list.** `S/simscreen/boards.json` is written on the first run and reused
  verbatim, so every later call ranks thetas on identical (tape, seed, seat) triples.
  Default family = `livec-holdout` (`S/livec/ids.txt` lines 43-102, the 60 held-out LIVE-C
  top-tier tapes). Seeds come from the `--seed-per-opponent` stride (`SEED_STRIDE`
  1000003, base 777001), so a screened board is a board an engine leg could have run.
* **many thetas per call, paired against one ref**, with a CSV of per-board rows.

**Reproducibility, measured:** the 400 (theta, board) cells the 40-board and the 120-board
runs have in common returned **400/400 byte-identical margins** across two separate
processes. The board freeze plus CRN means a screen result is a fact about the thetas, not
about the invocation.

Measured `shopdiff` = **0.0 % on every board of every run**: with the town pinned and
`shop_crn` on, all ten thetas saw byte-identical shop sequences. There is no lottery left
in the paired difference — which is the whole point (`shop-lottery-2026-09-06`).

## The defect that nearly sank it: the screen must play the SHIPPED composition

The first run scored the worktree's default switches. Three of the four switches the judge
and the uploaded package actually use default **False** in `arms-next`
(`TAIL_FILL_ON`, `BANK_BEFORE_LOT_ON`, `HIRE_ROW_ON`; only `OPEN_PUMP_ON` defaults True).
On the same 40 boards that changed B from 50.0 % / +1,258 to **65.0 % / +4,410** and
**flipped the validation sign**:

| pair | switches = worktree default | switches = shipped `hr` |
|---|---|---|
| flow187_g160 − B | **+312** (t +0.86) — wrong sign | **−528** (t −2.09) — right sign |
| soup2_BC − B | +781 (t +2.05) | −482 (t −2.17) |
| extrap_k15 − B | +392 (t +1.06) | −916 (t −3.38) |

`sim.rollout` reads `core.plan.*` at import time, so `screen.py` applies `--switches`
(default `OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True`,
the exact string `S/livec/run.sh` hands `on2b.py`) **before** importing `sim`. Any future
sim tool that skips this is measuring a different agent than the judge.

## Validation — two board counts, and why the second one matters

Ref = B (`flow193_g100_hr`), shipped `hr` switches, `shopdiff` 0.0 % throughout.
`full40.csv` = the first 40 boards (LIVE-C hold-out tapes 43-62 x 2 seats, 414 s);
`full120.csv` = all 120 (the full 60-tape hold-out family x 2 seats, 463 s).

| theta | Δ vs B, 40 boards | t | Δ vs B, 120 boards | t | engine's read |
|---|---|---|---|---|---|
| **B (ref)** | — | — | — | — | live candidate |
| flow194_g100_hr (C) | −314 | −1.09 | **+247** | +1.35 | ≈ B ("inside the noise": C +1 hold-out board, TOPB2 −2) |
| flow187_g160 (seat) | **−528** | **−2.09** | **−134** | −0.74 | B > seat (h2h +292 TOPB2 / +554 H30 / +270 H30B) |

**The brief's gate is met on its own terms and no more.** On 40 boards the screen
reproduces the engine's `B > seat` sign at |t| = 2.09. On the full 120-board hold-out family
it keeps the sign but the separation collapses to −134 (t −0.74): the 40-board t was a lucky
subset, not a stable reading. `C ≈ B` is reported honestly at both widths (−314 and +247,
neither significant), which is exactly the engine's own verdict.

The right way to read this is that **the true `B − seat` difference is small**, and the
engine says so too: B's head-to-head against the seat is +554 on 60 LIVEC-H30 games
(t ≈ 1.8) and +270 on H30B (t ≈ 0.9), with pooled hold-out wins **equal at 44/60**. B was
promoted over the seat on TOPB2 (+3/−0), a board family this screen does not play. So the
screen is not contradicting the engine; it is measuring a genuinely near-zero gap and
refusing to call it. Treat every |t| < 2 row below as "level", including the seat.

The variance claim does hold: paired sd ≈ 1,800-2,100 on boards whose own margins run
±20k, with the shop sequence byte-identical across all ten thetas.

## Screened ranking — 120 boards (the full LIVE-C hold-out family), ref = B

| rank | theta | win % | mean margin | Δ vs B | paired t | engine read on record |
|---|---|---|---|---|---|---|
| 1 | flow200_g30_hr | 71.7 | +5,665 | **+386** | **+2.20** | **LEVEL vs B** (TOPB2 −61 t −0.09, LIVEC-H30 +158 t 0.60, H30B +209 t 0.54) |
| 2 | flow194_g100_hr (C) | 74.2 | +5,526 | +247 | +1.35 | ≈ B |
| 3 | extrap_k05_hr | 73.3 | +5,464 | +185 | +1.14 | no vsB line was run; vs shipped base TOPB2 +623 against B's +903 |
| 4 | soup2_BC_hr | 70.0 | +5,292 | +13 | +0.08 | **below B** on the hold-out (H30 −236 t −0.8, H30B −170 t −0.5, TOPB2 +76) |
| 5 | *flow193_g100_hr (B)* | 71.7 | +5,279 | 0 | — | live |
| 6 | flow187_g160 (seat) | 73.3 | +5,145 | −134 | −0.74 | below B |
| 7 | flow201_g10_hr | 75.0 | +5,105 | −174 | −0.87 | **LOSS vs B** (TOPB2 −1,815 t −2.56, LIVEC-H30 −430 t −1.19, H30B −42) |
| 8 | soup3_BCS_hr | 70.0 | +5,041 | −238 | −1.27 | never judged (not queued after soup2 closed E1) |
| 9 | extrap_k15_hr | 71.7 | +4,877 | −402 | −2.06 | vs shipped base TOPB2 +36 against B's +903 |
| 10 | extrap_k25_hr | **30.8** | −8,455 | **−13,734** | **−22.21** | never judged |

Only two rows clear |t| = 2: flow200_g30 above B and extrap_k25 (catastrophically) below.
Everything between ranks 2 and 8 is one pooled standard error wide — the screen's honest
statement is that C, k05, soup2, the seat, flow201_g10 and soup3 are all **level with B on
this board family**, in that order of point estimate.

### Agreement with the two arm records the brief names

| theta | engine vs B | sim Δ vs B, 120 boards | agree? |
|---|---|---|---|
| flow200_g30_hr | LEVEL (LIVEC-H30 +158, H30B +209, TOPB2 −61) | **+386 (t +2.20)**, rank 1 | **yes** — sign and ordering; sim is the more positive of the two |
| flow201_g10_hr | LOSS (TOPB2 −1,815; LIVEC-H30 −430, H30B −42) | **−174 (t −0.87)**, rank 7 (below B) | **yes on sign and ordering**; the loss's magnitude lives on TOPB2, which this screen does not play |

The screen puts flow200 above B and flow201 below it — the engine's ordering exactly. It
does **not** reproduce the *size* of flow201's loss, because that loss is a TOPB2 loss and
the hold-out family scored flow201 at only −430/−42 in the engine too.

### The screen's new information

* **extrap_k25_hr is broken**: 30.8 % win rate, −13,734/board, t −22.2 on 120 boards
  (−15,359, t −14.3 on 40). θ_g160 + 2.5·(B − θ_g160) leaves the basin. It never needs an
  engine leg. This alone is ~14 min of judge lock saved on its first use.
* **the extrapolation is monotone-bad in k**: k05 +185, k15 −402, k25 −13,734. k05 is the
  only member worth a leg and it is level, not a gain.
* **soup3_BCS_hr = −238 (t −1.27)** — level-to-slightly-below B, the same shape as soup2's
  +13. The E1 soup family was closed at 14:02Z on soup2's engine read; the screen says
  soup3 would not have re-opened it.
* **flow200_g30_hr is the only theta in the set that reads above B with |t| > 2** on the
  hold-out family. The engine already called it LEVEL; the screen agrees and points at
  where a longer flow200 run would be worth judging.

## Limits (what this screen does not license)

1. It is a **pre-filter, not a verdict.** It plays 120 boards of ONE tape family
   (LIVE-C hold-out) with the tape's own recorded town. It is not TOPB2, it is not LIVE62,
   and it cannot see the ladder — and flow201_g10's real loss is a TOPB2 loss, which is
   precisely the kind of verdict this screen will miss. Add a `topb2` board file
   (`--tapes topb2 --reboard` into a second checkout of `boards.json`) before trusting it
   to refuse a candidate on top-tier grounds.
2. **Its resolution is about ±400 coins/board at 120 boards** (SE ≈ 180). It cannot
   separate thetas that sit inside that, and most of today's candidates do. Use it to
   refuse (|t| > 2 negative) and to order, not to promote.
3. It is valid **only in the composition it is given** — see the switch defect above.
4. `docs/strategy/2026-09-09-care-coverage.md:175`: the glut / `CARE_FILL_ON` family is
   outside it.
5. Never point it at `artifacts/tape_actions/` (open-loop): +12k optimism, 47 % sign.
6. `sim-equals-engine-2026-09-06` addendum: the sim under-plays the tape seat on some
   *fresh* loss tapes (4/12 on 2026-09-09). The LIVE-C hold-out tapes used here are the
   pinned family where the sim was measured coin-exact, but a newly cut tape should be
   spot-checked against one engine leg before it joins `boards.json`.

## How to use it

Rank every new record / soup / extrapolation here first — **8 min for 10 thetas x 120
boards on CPU, against ~14 min of judge lock for ONE theta's hold-out legs**. Then:

* **refuse** a leg outright on a strongly negative read (|t| > 3; k25 at −22 is the
  archetype). This is the use the evidence supports.
* **order** the queue by the point estimate, and judge the top of it first.
* **never promote** on a screen read. Nothing here substitutes for TOPB2, LIVE62 or LOSS10,
  and the one verdict in this run whose magnitude the screen missed (flow201_g10) was a
  TOPB2 verdict.

```bash
T=artifacts/kagg2_games/thetas
.venv/bin/python S/simscreen/screen.py --ref $T/flow193_g100_hr.npy \
    --thetas $T/cand_a.npy $T/cand_b.npy --boards 120 --chunk 40 --tag mytag
```
