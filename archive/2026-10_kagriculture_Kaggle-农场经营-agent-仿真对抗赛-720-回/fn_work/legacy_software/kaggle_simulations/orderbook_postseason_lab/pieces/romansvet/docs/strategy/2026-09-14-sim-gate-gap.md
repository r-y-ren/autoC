# SIM-GATE-GAP — why flow214/flow215's in-sim fitness does not reach the real gate

*2026-09-14, read-only diagnostic on flow214 (crop-mix, 7,020) and flow215 (crop-day, 7,065).
All remote files pulled to `S/simgate/remote/`, all scripts in `S/simgate/`.*

## VERDICT

**There is no in-sim gain to transfer.** The only number that moved in-sim is `mean_win`, which
is (a) the *population* win rate, (b) measured on **153 frozen games** — one deterministic episode
per pinned tape rung, on a seed word that is a blake2b digest of the rung name and therefore
identical in every generation forever (`--pinned-once --pinned-fixed-seed`,
`src/kagg3/es/train.py:1324-1347`, `:4543-4567`) — and (c) documented by the trainer itself as a
**diagnostic that is ladder-relative and sits near 0.5 by construction**
(`scripts/train.py:3005-3009`; `src/kagg3/es/train.py:14-20`: it "saturates in ~100 generations and
then decays back to 0.5", and correlated **−0.17** with absolute strength over a 13 h run).

The coin yardstick measured on the *same* ladder (`abs`, and its "holdout" twin `hold`) did **not**
move: 102,294 at gen 10 → 103,163 at gen 130, inside its own ±600 wobble. So the arm bought ~6.6
win flips on 153 fixed boards and zero coins.

At the gate, the centre is walking **downhill, monotonically with generation**:

| flow214 candidate | gate win | gate mean margin | paired Δmargin (62 boards) | SE | t |
|---|---:|---:|---:|---:|---:|
| seed (B, gen 0 record) | 57.3 % | +3,028 | — | — | — |
| gen 10 record | 54.8 % | +2,621 | **−406** | 238 | −1.71 |
| gen 100 periodic (= the search centre) | 56.5 % | +2,534 | **−494** | 252 | −1.96 |
| gen 130 record | 58.1 % | +2,351 | **−677** | 291 | −2.32 |

while `mean_win` over the same span goes 0.5678 → 0.5925 → 0.6110. The two curves are
**anti-correlated**, which is exactly the relationship `src/kagg3/es/train.py:14-20` warned about.

flow215 is the same picture with the volume turned up: its *population* never even reaches the
seed's level (`mean_win` 0.28–0.38 against flow214's 0.57–0.61 at the same sigma), and its gate
readings are −2,619 (t −7.95) and −2,634 (t −5.75) coins a board. That arm is not overfitting; it
is broken by the size of the `cd` step (§5, H2).

Killed on the way: it is **not** the win-vs-margin quantisation, and **not** the sigmoid's
saturation. Applying the arm's *own* objective — `sigmoid(margin / margin_scale)`, the whole
fitness because `--abs-weight 0` (`src/kagg3/es/train.py:585-602`, `:674-676`) — to the gate's own
62 boards prefers the **incumbent** at every scale tried (3k / 6k / 25k / 100k), for every
candidate of both arms (`S/simgate/objective_on_gate.txt`). Under any reading the run has, on
unseen boards, the candidate is worse.

## 1. The training ladder vs the gate set

`S/simgate/rung_vs_gate.py`, from `artifacts/flow214/config.json` (identical in flow215 except
`seed`/`run`/`init_theta`).

| block | rungs | ids | weight each | share of the objective | per rung |
|---|---:|---|---:|---:|---:|
| top-ten tapes (TOPB2 "in-sample") | 20 | 107000107..107015773 | 10.2 | **36.8 %** | 1.84 % |
| LIVE-C tapes | 42 | 107427438..107462861 | 4.0 | 30.3 % | 0.72 % |
| older tapes + 6 ymg_aq (1088*) | 91 | 105228357..108826138 | 2.0 | 32.9 % | 0.36 % |
| hand archetypes (expander/rusher/rancher/patient_grower) | 4 | — | **0.0** | 0 % | 0 % |
| **total** | **157 (153 live — matches `rungs 153/157`)** | | 554 | 100 % | |

| gate | value |
|---|---|
| opponents | 62 packaged tape opponents, `artifacts/panel_opp_town/opponent_tape_<id>/main.py` |
| ids | 107448662..107507032 |
| games | 62 × 2 seats = **124 deterministic pinned-town games**, seed base 20260904 |
| weighting | flat — every opponent is 1.61 % of the win count and of the mean margin |
| **overlap with the 153 training rungs** | **0 ids** (asserted again here; also asserted at launch, `docs/strategy/2026-09-14-flow215-launch.md` §4) |
| accept rule | `--real-gate-metric win` + `--real-gate-min-flips 5`: net flips ≥ 5 **and** strictly more wins (`src/kagg3/es/train.py:2801-2845`) |

Two structural mismatches fall straight out of the table:

* **weighting.** In sim, 20 top-ten boards from a single 15-minute Kaggle window carry 36.8 % of
  the objective and each is worth 5.1× a weight-2 board. At the gate every board is worth the
  same, and ten of the gate's ids sit *inside* the LIVE-C id range, i.e. the gate is the same
  Kaggle population, a later slice.
* **what a board is.** A sim rung is one episode on a frozen seed word, scored by
  `sigmoid(margin/3000)` — saturated past ±6k, where 31 of the gate's 62 boards live. A gate board
  is a deterministic engine game scored by a win bit and, for the record, by mean coins.

## 2. Per-opponent, gen 100 candidate vs the seed (`S/simgate/flow214_per_opponent.txt`)

Full 62-row tables for gen 10 / 100 / 130 (flow214) and gen 10 / 60 (flow215) are in
`S/simgate/flow214_per_opponent.txt` / `flow215_per_opponent.txt`. Headline shape:

| leg | boards improved | sum | boards worsened | sum | own coins | opponent coins |
|---|---:|---:|---:|---:|---|---|
| gen 10 | 21 | +28,349 | 41 | −53,547 | 102,927 → 101,714 | 99,900 → 99,092 |
| gen 100 | 28 | +30,431 | 34 | −61,065 | 102,927 → 102,756 | 99,900 → 100,222 |
| gen 130 | 23 | +28,485 | 39 | −70,471 | 102,927 → 102,699 | 99,900 → **100,348** |

Many small gains (the biggest is +2,416 at gen 100), a few large losses (−7,879, −4,753, −4,634,
−4,235, −4,126). Note the last column: by gen 130 the candidate is **raising the opponent's**
coins — the shared-pot signature (memory: *Counterfactuals overstate* / *Kaggle population
autopsy*), i.e. it is trading more through the pot, not out-earning anyone.

The gen-100 flip ledger is `+2 flips / −3 drops` on 124 games (`107457053/0,1` won;
`107470160/1 107496859/0,1` lost) — 5 games of 124 moved at all. The gate cannot accept that under
`min_flips 5` no matter how the coins fell.

## 3. Engine legs on the two board classes (the decisive measurement)

`S/simgate/run_insample_vs_heldout.sh` ran the flow214 **gen-100 candidate** (md5
`742cacea77a9ef4b6cc418d92f629807`, `S/simgate/cands/flow214/g00100_periodic.npy`) on the TOPB2
family's two twin legs — identical recipe, single contrast = the id list
(`S/topb2/run_insample.sh`, `S/topb2/run.sh`, `S/topb2/insample.md`):

| leg | boards | what they are | Δ vs B | SE | t | win B → cand | W/L |
|---|---:|---|---:|---:|---:|---|---|
| **IN-SAMPLE top-ten** | 20 × 2 | the 20 `w10.2` rungs = **36.8 % of flow214's own objective** | **−139** | 556 | −0.25 | 40.0 → 40.0 % | 1/1 |
| **HELD-OUT TOPB2** | 20 × 2 | 20 never-trained 3000+ boards (also 20 of the gate's 62, at TOPB2's own towns/seeds) | **−308** | 642 | −0.48 | 32.5 → 30.0 % | 0/1 |
| gate | 62 × 2 | the 62 held-out boards, gate towns/seed base | **−494** | 252 | −1.96 | 57.3 → 56.5 % | +2/−3 |

This is the finding that ranks the hypotheses. The candidate is **not better on the very boards it
trains on** once the engine re-rolls their seed (−139, t −0.25), so the in-sim gain is not an
opponent-class advantage that merely fails to generalise — it does not exist outside the frozen
draw. For comparison, four earlier records showed a *real* in-sample advantage on these same two
legs (in-sample −224 vs held-out −1,274, gap **+1,050**, t +2.46 — `S/topb2/insample.md`); this
candidate's gap is +169.

## 4. Why the sim cannot see it

* `--pinned-once` gives each of the 153 tape rungs **exactly one episode** a generation, and
  `--pinned-fixed-seed` fixes that episode's seed word to `blake2b(rung name)` — "a property of
  the tape alone, stable across processes and `--resume`" (`scripts/train.py:1752-1766`;
  `src/kagg3/es/train.py:1324-1347`). The training set is therefore **153 byte-identical games,
  replayed 512 × 2 times a generation for 130 generations**. 6,228 trainable coordinates against
  153 frozen outcomes.
* The run's own generalisation check is **vacuous**. `--holdout-rungs` splits the fixed seed set
  into a selection half and a rest half (`src/kagg3/es/train.py:5686-5700`), but with the seed word
  frozen both halves are the *same deterministic game*: the log prints `abs 103129.61` /
  `hold 103,123` at gen 100, `103448.50` / `103,440` at gen 120 — a 0.006 % gap, every time.
  **Nothing between two gate legs can tell the run it is overfitting.**
* `--shop-crn` is declared "TRAINING ONLY — a common random number for the search, **never an eval
  semantic**" (`scripts/train.py:1995-2007`): in training the end-of-day shop draw is taken from a
  fixed position in the word stream, in the engine it is one draw per EMPTY tile, so a candidate
  that plants one tile more re-rolls every later shop (~25k a YARN_STORE). Any tile-count change
  the ES makes is therefore priced *without* the re-roll the gate will charge for it.
* The gate's `periodic` candidate is the **search centre itself**, not a selected record
  (`src/kagg3/es/train.py:5276-5283`, `:2330-2340`), so the gen-100 result is not a winner's-curse
  artefact of picking the best of 512 — it is where the gradient actually put the policy.
* Adam spreads the step evenly: at gen 100 ‖Δθ‖ = 2.30, of which the new crop-mix block is only
  4.4 % of the squared step (`S/simgate/theta_blocks.txt`). Per coordinate the step is ~0.029
  everywhere. **This arm is not a gene test; it is a full re-training of B**, and B is a measured
  local optimum (memory: *Dominant strategy 2026-09-03*).

## 5. Ranked hypotheses

### H1 (top) — the in-sim signal is a fixed-draw artefact: 153 frozen games, no coins behind it

*Supports:* `mean_win` +4.3 points (0.568 → 0.611) while `abs` on the same ladder is flat
(102.3k → 103.2k, ±0.6 %); `hold` ≡ `abs` to 0.006 %, so the run has no holdout at all; the same
theta is **−139 (t −0.25)** on its own 20 highest-weighted training opponents at a fresh engine
seed, **−308 (t −0.48)** on TOPB2 held-out, **−494 (t −1.96)** on the gate; the gate Δ worsens
monotonically with generation (−406 → −494 → −677) exactly as `mean_win` rises; the trainer's own
module docstring says this statistic decays back to 0.5 and correlated −0.17 with strength.
*Kills:* nothing found. The one thing that would kill it is an in-sim margin reading of the centre
on the 153 rungs that survives a seed re-draw — not measured here (see §6).

### H2 — sigma × block gain too large for the new coordinates (owns flow215 outright)

*Supports:* flow215's population sits ~23 win-points below flow214's at the same sigma 0.02
(`mean_win` 0.28 at gen 10, 0.38 at gen 83, vs 0.57/0.60) — the `cd` block is
`CROP_DAY_GAIN 64`, 1.28 nats of log-share per sd (`docs/strategy/2026-09-14-flow215-launch.md`
§3), so most of the population is a wrecked policy and the mean gradient is mostly noise; its gate
Δ is −2.6k a board at t −8 after 60 generations, with 17 straight drops and 0 flips. In flow214 the
`cm` block carries the largest per-coordinate step of any block (0.0376 vs 0.0289 for `w1`).
*Kills (for flow214):* flow214's population level is healthy (0.60) and its gate loss is
−494, not −2,600 — so H2 is a secondary effect there, and the whole story in flow215.

### H3 — opponent-class / weighting mismatch (20 top-ten boards = 36.8 % of the objective)

*Supports:* the objective is 36.8 % top-ten tapes from one 15-minute window, flat-weighted 62
mixed boards at the gate, 0 id overlap; four earlier records show a systematic in-sample −
held-out gap of **+1,050** coins (t +2.46, `S/topb2/insample.md`).
*Kills (as this arm's main driver):* the gen-100 candidate is flat **in-sample too** (−139, gap
+169), so the drift is not "it learned the top-ten class and the gate is a different class".

### H4 (killed) — win-count quantisation / `min_flips 5` / sigmoid saturation

*Killed:* the mean margin falls with the wins at gen 10/100/130 (t −1.71/−1.96/−2.32), and the
arm's own `sigmoid(margin/margin_scale)` objective applied to the gate's 62 boards prefers the
incumbent at margin_scale 3,000 **and** 6,000 **and** 25,000 **and** 100,000, for all five
candidate legs of both arms (`S/simgate/objective_on_gate.txt`).

## 6. The flag change that tests H1

One flag, everything else verbatim. `S/flow214/launch_flow214_remote.sh:67` reads
`--episodes 160 --pinned-once --pinned-fixed-seed --shop-crn \`; change it to:

```
-  --pinned-once --pinned-fixed-seed --shop-crn
+  --pinned-once --shop-crn
```

i.e. **drop `--pinned-fixed-seed`**. `fixed_seed` then returns the generation's drawn seed array
unchanged (`src/kagg3/es/train.py:4557-4559`), so each pinned rung's single episode is re-drawn
every generation while (a) the tape's **town stays pinned** — the town comes from the `--with-town`
tape, not from the seed word (`scripts/train.py:1755-1758`), so the opponents keep replaying to the
coin, and (b) common random numbers inside a generation are untouched: the seed list is drawn once
per generation and played by all 512 candidates (`src/kagg3/es/train.py:4569-4576`). The objective
becomes an expectation over each board's residual randomness instead of 153 frozen outcomes.

Read it at the first two gates: if `mean_win` still climbs and the gen-100 **centre** now clears
or matches the bar, the frozen draw was the artefact. If `mean_win` stops climbing altogether,
that *is* the confirmation — the +4.3 points were the frozen draw.

Second arm, if a second GPU is free: same change plus `--sigma 0.005` (H2), which is the flow215
lesson applied to flow214's `cm` block.

Cheap pre-test before either launch (15 min, no GPU): replay the 20 `w10.2` in-sample boards at a
**third** engine seed base. H1 predicts the gen-100 candidate stays flat (≈0 ± 600); H3 predicts a
positive in-sample Δ.

## 7. Files

* `S/simgate/remote/flow21{4,5}/` — `config.json`, `train.log`, `log.jsonl`, `real_gate.{log,json,csv}`, `cands_index.jsonl` (pulled 2026-09-14 12:12–12:26Z)
* `S/simgate/cands/flow21{4,5}/` — every kept candidate (`--keep-candidates`)
* `S/simgate/parse_gate.py` → `flow214_per_opponent.txt`, `flow215_per_opponent.txt`
* `S/simgate/objective_on_gate.py` → `objective_on_gate.txt` (the arm's own objective + paired board-level t on the gate)
* `S/simgate/rung_vs_gate.py` → `rung_vs_gate.txt` (ladder vs gate table, overlap 0)
* `S/simgate/theta_blocks.txt` — per-block ‖Δθ‖ for every candidate
* `S/simgate/run_insample_vs_heldout.sh`, `legs.out`, `insample10_f214g100.csv`, `f214g100_topb2.csv`
