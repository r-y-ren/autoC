# Top-tier overfit or anti-top-tier direction? (2026-09-12)

**Question (§95, `docs/strategy/2026-09-11-band-gradient.md`).** Across 19 judged ES
records the paired margin vs candidate **B** is **−2,991 (t −9.41)** on the 3000+ TOPB2
tapes, carried by 107460230 (−7,746) and 107465299 (−3,643) — while the arms **train** on
20 *other* top-ten tapes (2821-2954) at **32.7 %** of the objective
(`docs/strategy/2026-09-11-rung-allocation.md` §2). Do the records **gain** on the tapes
they train on while losing on the held-out ones (tape-specific overfit), or do they lose
on **both** (the direction itself is anti-top-tier)?

**Answer in one line: neither — the records are LEVEL on the tapes they train on
(−224 coins, t −0.91) and WORSE on the held-out ones (−1,274, t −3.66).** No record gains
on its own top-ten training rungs, so there is no memorised in-sample gain being traded
away; the gap in-sample − held-out is +1,050 (SE 427, t +2.46).

## 1. Method

New leg `S/topb2/run_insample.sh` (+ `S/topb2/insample_ids.txt`, `S/topb2/insample.md`):
the 20 `--rung-weight 10.2` top-ten rungs played exactly as `S/topb2/run.sh` plays the 20
held-out TOPB2 boards — pinned towns, both seats, `--seed-per-opponent`, `--games 1` = 40
games, shipped switches, tree `.claude/worktrees/arms-next`, `WORKERS=4`, seed base
300777601. Pairing = `S/bank/paired.py` (board-level t, seats averaged). Held-out side =
the existing `S/lossflip/<record>_topb2.csv` against B's `flow193_g100_hr_topb2.csv`.

Records: `flow200_g200p_hr` (full live-mask arm, lr 3e-3, ‖Δθ‖ = 1.630),
`flow209_g10_hr` (the §73 block-SNR arm: `--train-only` 1,191 of 5,997 live genes, sgd
lr 1.8e-4, ‖Δθ‖ = 0.0071), `flow206_g10_hr` and `flow205_g10_hr` (lr 3e-4 full-mask,
‖Δθ‖ = 0.0888 / 0.0888). B = `submission/theta.npy` = `flow193_g100_hr` (md5 7fcf3948).
**Note for the decode-diff read:** flow200's trained set was the FULL live mask (5,997
genes moved), not the flow209 train-only subspace — its decode differences are therefore
much broader by construction and must not be compared one-for-one with flow209's.

## 2. The record table — in-sample vs held-out, paired vs B

Paired vs B per board, `S/bank/paired.py`, both seats averaged into one observation.
"flips" = games the record wins that B lost / loses that B won.

| record | ‖Δθ‖ vs B | genes moved | IN-SAMPLE top-ten Δ | SE | t | flips | HELD-OUT TOPB2 Δ | SE | t | flips |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---|
| `flow200_g200p_hr` | 1.6303 | 5,997 (full live mask) | **−330** | 599 | −0.55 | +1/−1 | **−1,080** | 711 | −1.52 | +0/−1 |
| `flow209_g10_hr` | 0.0071 | 1,191 (train-only) | **+28** | 513 | +0.05 | +0/−1 | **−385** | 493 | −0.78 | +0/−1 |
| `flow206_g10_hr` | 0.0888 | 5,997 | **−112** | 378 | −0.30 | +0/−0 | **−1,721** | 714 | −2.41 | +0/−7 |
| `flow205_g10_hr` | 0.0888 | 5,997 | **−481** | 491 | −0.98 | +0/−0 | **−1,910** | 825 | −2.32 | +0/−3 |
| **pooled, 80 board-cells** | | | **−224** | 247 | **−0.91** | +1/−2 | **−1,274** | 348 | **−3.66** | +0/−12 |

**Gap (in-sample − held-out) = +1,050, SE 427, t +2.46.** Per record: flow200 +751
(t +0.81), flow209 +413 (t +0.58), flow206 +1,609 (t +1.99), flow205 +1,429 (t +1.49).

Win rates: on the in-sample set B wins 40.0 % and every record stays at 37.5-40.0 %; on
the held-out set B wins 32.5 % and the records fall to 15.0-30.0 % (net game flips
+0/−12 pooled, against +1/−2 in sample).

**The base rates matter as much as the deltas.** B itself is **+927 mean margin / 40.0 %
wins** on the 20 tapes it was trained on and **−1,654 / 32.5 %** on the 20 held-out
3000+ tapes. The training set is a set the incumbent has already absorbed; there is
about 2,580 coins/board of B-level "in-sample advantage" sitting in it before any record
moves a gene, and the arms add nothing on top of it.

Per-board tables: `S/topb2/insample.md`.

## 3. The two worst held-out boards, day by day

Replayed in the pinned-town sim (`S/simscreen/screen.py` recipe: recorded town, `shop_crn`
on, the engine leg's own seed from `S/simscreen/boards_topb2.json`, tape-action opponent
seat) with `st.money` scanned out per day. **Fidelity check: the sim reproduces the engine
leg to the coin** on all eight of these games, e.g. B on 107460230 = −3,725 / +2,151 and
on 107465299 = +5,749 / +6,549 in both the sim and `S/lossflip/*_topb2.csv`.

Δ(ours − theirs) vs B **accrued inside each day band**, mean of the two seats:

| board | record | d0-9 | d10-14 | d15-29 | final |
|---|---|---:|---:|---:|---:|
| 107460230 (Otter Vibe 3032) | `flow200_g200p_hr` | +437 | −174 | **−11,214** | −10,951 |
| 107460230 | `flow209_g10_hr` | +408 | −56 | **−9,014** | −8,662 |
| 107460230 | `flow206_g10_hr` | +463 | −316 | **−11,660** | −11,512 |
| 107465299 (SpaTaro 3081) | `flow200_g200p_hr` | +16 | **−2,078** | −2,556 | −4,618 |
| 107465299 | `flow209_g10_hr` | +14 | −224 | −94 | −305 |
| 107465299 | `flow206_g10_hr` | +86 | **−2,170** | −4,383 | −6,467 |

**Nothing is lost before day 10 on either board** — the day-0/opening block is a small
*gain* (+14…+463). The two boards then fail in two different ways:

* **107460230 — a self-inflicted late-sale loss, opponent untouched.** Every record is
  level with B through d17 and then drops 3.2-4.2k **in one day, d18**, and never
  recovers. Splitting the margin: at d29 our own money is **−7,538 (flow209) / −9,581
  (flow200) / −9,042 (flow206)** against B, while the opponent's money moves **−361
  (flow209)** / +2,503 / +1,393. For the train-only arm the opponent is *unchanged*: the
  record simply realises 7.5k less from its own d18+ crop. (Only the two full-mask arms
  additionally hand the opponent 1.4-2.5k.)
* **107465299 — a denial failure that starts at d10.** Our money is roughly flat
  (−775…−1,931 at d29) while **the opponent's rises +3,172 (flow200) / +4,119 (flow206)**,
  already +1,585 by d14. The small-step flow209 barely moves this board at all
  (−305 final, opponent −73) — which is why it is the only record that does not lose it.

**What the decoder actually changes on these boards** (both thetas decoded on B's own
trajectory, so the difference is the decoder's and not the board's):

* A direction **all three records share on both boards**: `grow_mult[0..2]` **up** and
  `grow_mult[8]` **down** on 22-30 of the 30 days, with `press[4]`, `press[7]`, `hold[6/7]`
  and `hire_bias` drifting alongside. Signs of the shared components agree across three
  arms that differ in lr, optimiser and trained subspace.
* The two **full-mask** records (flow200_g200p, flow206_g10) also cross the **day-0
  SWITCH0 cell** (`consensus` §66): `plant_target[0]` 11 → **10** and `animal_want[1]`
  4 → **5** at d0 — one more animal, one fewer wheat tile. flow209 (train-only) does
  **not** flip either and still loses 107460230 by 8.7k, so the day-0 switch is **not**
  the cause of the 3000+ penalty; it is a second, independent change the full-mask arms
  make.
* Breadth scales with the trained subspace, as expected: of 42 decoded knob columns
  flow200 moves 38 on both boards, flow206 32-33, flow209 (1,191 genes) 27 — but flow209's coarse
  counts (`plant_target`, `animal_want`, `crew_target`, `compact`, `forward_days`) are
  almost entirely unchanged, so its −8.7k comes through the ratio knobs alone.

## 4. The three answers

**(i) Neither classic overfit nor a clean anti-top-tier direction: the records are LEVEL
in sample and WORSE out of sample.** In-sample on the 20 top-ten rungs they train on at
32.7 % weight, the pooled Δ vs B is **−224 coins (SE 247, t −0.91)** over 80 board-cells,
with net game flips +1/−2 and the win rate unmoved (B 40.0 %, records 37.5-40.0 %). No
record gains: the best is flow209_g10_hr at **+28 (t +0.05)**, the worst flow205_g10_hr at
−481. On the 20 held-out 3000+ TOPB2 boards the same four records are **−1,274 (SE 348,
t −3.66)**, flips +0/−12, win rate 32.5 % → 15-30 %. The difference between the two sides
is **+1,050 (SE 427, t +2.46)** — a real generalisation gap, but one that runs from
*level* to *worse*, not from *better* to *worse*. Memorising a training game's shop draw
would show up as an in-sample gain; there is none to find. The honest description is
**"the step is worthless where it trains and costly where it does not"**, and the
anti-top-tier component is the out-of-sample half: −1,274 on 2953-3081 against §95's
−477 pooled across all bands.

**(ii) What the 3000+ tapes punish: the late game, not the opening.** On both worst boards
every record is at or ahead of B through day 9 (+14…+463) and loses everything from d10
onward — 107460230 loses **−9.0k to −11.7k inside d15-29 alone**, opening with a 3.2-4.2k
drop **in the single day d18**; 107465299 loses **−2.1k/−2.2k inside d10-14** and the rest
after. The two boards fail by two different mechanisms: on 107460230 it is **our own
money** that falls (−7.5k to −9.6k at d29) with the opponent untouched for the train-only
arm (−361) — the record under-realises its own d18+ crop; on 107465299 it is **the
opponent's money that rises** (+3,172 / +4,119, already +1,585 by d14) while ours is
nearly flat — a denial failure, the same d15-29 "denial of THEIR price" signature the
loss anatomy calls the top-tier discriminator. In the decoder, the direction all three
records share on both boards is a re-weighting of the grow_mult vector (`grow_mult[0..2]`
up, `grow_mult[8]` down on 22-30 of 30 days) with `press[4]`, `press[7]`, `hold[6/7]` and
`hire_bias` drifting alongside; the two full-mask arms additionally cross the day-0
SWITCH0 cell (`plant_target[0]` 11→10, `animal_want[1]` 4→5), which the train-only arm
does **not** do while still losing 107460230 by 8.7k. So the penalty is carried by the
ratio knobs that govern growth weighting and late selling pressure, not by the opening
integer counts.

**(iii) For flow211 (top-ten 32.7 % → 10 %, NEXT30 38 %): cutting the weight removes a
target that is paying nothing, and the TOPB2 risk it carries is not measurable in this
data.** The 32.7 % clause buys **−224 coins** of measured play against the very opponents
it weights, so 22.7 points of objective mass are currently being spent for nothing — that
is the strongest argument in the study for the cut. It is **not** an overfit target in the
memorisation sense (there is no in-sample gain to give back), so cutting it cannot release
a stored gain either; it frees mass, no more. The risk that cutting it enlarges the
−1,274 held-out loss cannot be resolved here, and the data leans mildly against it: the
records that hurt TOPB2 most are the full-mask ones (flow206 −1,721, flow205 −1,910) and
the one that hurts it least is flow209 (−385), whose *distinguishing* feature is a 230×
smaller step in a 1,191-gene subspace, not a different rung mix — i.e. within this sample
the TOPB2 damage tracks **step size and subspace**, not top-ten weight. The operational
consequence is the same either way: **flow211 must keep TOPB2 held out and keep judging
on it**, because it is the only leg where records separate from B at |t| > 2 per record,
and §95's finding that no record of 19 gains net wins there still stands.

## 5. Caveats

1. **The in-sample leg is not the training objective.** The arms score these 20 tapes as a
   rung-weighted *margin* through a `margin_scale 3000` sigmoid, one episode per rung per
   generation with the seat alternating, on the trainer's own seed schedule. This leg
   scores them as raw coins on a fixed engine seed, both seats, in the shipped switch
   composition. It measures **whether the records play the training opponents better**, not
   the exact scalar the ES maximised. A record can raise the sigmoid objective while
   losing coins (margin saturation, `2026-09-11-margin-scale-AB.md`), so "no in-sample
   coin gain" does not by itself prove the ES failed to climb its own objective — it
   proves the climb did not reach coins against those opponents.
2. **One seed per board.** 20 boards × 2 seats × 1 engine seed per leg. The shop draw is
   pinned only in the town sense; the end-of-day shop re-roll is still the ±25k zero-mean
   noise of the *shop-lottery* memory, which pairing removes only to the extent both
   thetas keep the same tile occupancy.
3. **The 20 top-ten rungs are not 20 independent games.** Several are the same team's
   near-identical clone openings (e.g. 107014983 / 107000107 differ by 1,000 coins of the
   tape's own result; 107014982 / 107014375 are statistically identical in
   `S/express/census.md`), so the effective board count is smaller than 20 and the SE is
   optimistic. All 20 action tapes are byte-distinct.
4. **Four records, not nineteen.** §95's −2,991 is pooled over 19 records; this study
   re-measures four of them (the three requested plus flow205) on both sides. The
   held-out numbers reproduce §95's sign and ordering for all four.
5. **Sim replay, not the engine, for §3.** The day-band and decode tables come from the
   pinned-town sim. It reproduced all eight of these games' final margins to the coin
   against the engine csvs, which is the strongest fidelity check available, but the
   per-day split itself is not independently engine-verified (the engine leg writes no
   per-day money).
