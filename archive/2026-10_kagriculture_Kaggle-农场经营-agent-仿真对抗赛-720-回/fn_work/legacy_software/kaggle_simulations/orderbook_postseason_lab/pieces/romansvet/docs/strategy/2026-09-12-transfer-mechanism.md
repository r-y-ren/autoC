# §111 — WHY the flow209 step buys the top tier and sells the band

Dispatched 2026-09-12T02:1xZ against consensus §107/§110
(`docs/strategy/2026-09-12-objective-vs-judge.md`, `2026-09-12-objective-gate.md`).

**The question.** The ES step from candidate B (`submission/theta.npy`, md5
7fcf3948) to flow209's g20/g30 centres (md5 5e102d64 / f96f617e) gains ~+506 on
the 20 trained TOPTEN rungs and ~+597 on the ten LOSS10 rungs and pays for it
with ~−344 on LIVEC42 and ~−216 on W2. What does it change in the decoded plan,
and why does that change pay against 2800-2950 opponents and cost against
2300-2600 ones?

**The answer in one line.** The step is a **uniform, non-conditional
re-aiming of the late-game market dump**: it moves grow priority off
FERTILIZER / MELON / EGG / WHEAT onto MILK / WOOL / TOMATO / STRAWBERRY and
lowers `press` (sell pressure) on essentially every product. Both effects are
**denial** trades, and which of them pays is decided entirely by **which product
the opponent's own late liquidation runs through** — milk and the mixed engine
for the top tier, carrot and wheat for the band clone. It is not conditioned on
anything, and nothing observable in the rung data predicts which side a board
lands on.

Deliverables: `S/transfer/{rungs.md,decode.md,ledger.md,rungs.py,decode.py,ledger.py,freshword.py,*.csv,*.npz}`.

---

## 1. Per-rung, two-purse (`S/transfer/rungs.md`, `rungs_two_purse.csv`)

Δ = g20 − B, coins/episode, mean of the four `--word-offset` weed replicates of
the §110 gate. `ΔOURS` = our money moving, `ΔTHEIRS` = the opponent's.

| family (rating tier) | rungs | ΔOURS | ΔTHEIRS | **Δmargin** | t | which purse moves |
|---|---:|---:|---:|---:|---:|---|
| LOSS10 (2175-2381) | 10 | +49 | **−548** | **+597** | +2.41 | **92 % pure DENIAL** |
| TOPTEN (2821-2954) | 20 | +277 | **−229** | **+506** | +2.99 | 55 % denial / 45 % ours |
| NEXT30 (2650-2750) | 30 | +99 | −84 | +183 | +0.90 | denial |
| W2 band (≈2100-2400) | 85 | **−282** | −65 | **−216** | −1.43 | **our purse falls** |
| LIVEC42 (2300-2600) | 42 | −87 | **+257** | **−344** | −1.70 | **75 % THEIR purse RISES** |
| TOP50 (2700-2850) | 9 | +256 | +880 | −624 | −0.69 | their purse rises |

So **the gain at the top of the ladder is money taken OFF the opponent, and the
loss in the band is denial we stop performing** (LIVEC42) or our own revenue
we stop collecting (W2). Both sides of the trade are the same lever seen from
two ends. Aggregates: BOUGHT (TOPTEN+LOSS10) 30 rungs +536 SE 138 t +3.90;
SOLD (LIVEC42+W2) 127 rungs −259 SE 121 t −2.14; all 196 rungs −86 SE 98.

Top-10 / bottom-10 rungs with the purse split are in `S/transfer/rungs.md` §2.
Neither tail is a TOPTEN rung: TOPTEN's +506 is a small consistent shift of
every rung (25 % negative, per-rung SD 760) while the band's −344/−216 is a wide
two-sided spread (61-64 % negative, SD ~1,300) with ±3-5k tails.

**Three covariates fail to explain the split** (196 pinned rungs, Spearman):
opponent's money under B −0.033 (p 0.65); our money under B −0.018; B's margin
−0.016; best of 16 town-shop features −0.111 (p 0.12); best of 40 opponent-play
features read off the tapes (per-product sell volume in three day bands, hires,
hires d0, animals, plants per crop, fertilize ops) +0.128 (p 0.07, uncorrected
over 40 tests). Family membership — i.e. the identity of the tape — is the only
predictor of the sign.

## 2. Decode: what the step changes in the plan (`S/transfer/decode.md`)

B vs g30 decoded on **common observations** over 8 boards × 30 days (4 TOPTEN
where the gain is largest, 4 LIVEC42 where the loss is largest), shipped switch
string, the same machinery as `S/snr/g10_diff.py`. Seat convention verified
against the trainer's own `B_margin` (max err 895 on margins of 0.25-15k; 6 of 8
boards seat-symmetric).

Indices are `spec.PRODUCTS` = WHEAT, CARROT, TOMATO, STRAWBERRY, MELON, EGG,
MILK, WOOL, FERTILIZER; `plant_target` is over `spec.CROPS`; `animal_want` over
GOOSE, COW, SHEEP.

| knob | product | board-days differing | direction |
|---|---|---:|---|
| `grow_mult[8]` | **FERTILIZER** | 239/240 (99.6 %) | **down** (mean 2.31) |
| `grow_mult[4]` | **MELON** | 229 (95.4 %) | **down** (4.11) |
| `grow_mult[0]` | WHEAT | 221 (92.1 %) | down (24 up / 197 dn) |
| `grow_mult[2]` | **TOMATO** | 207 (86.2 %) | **up** (171/36) |
| `grow_mult[7]` | WOOL | 196 (81.7 %) | up (127/69) |
| `grow_mult[3]` | **STRAWBERRY** | 178 (74.2 %) | **up** (5.17) |
| `grow_mult[6]` | **MILK** | 155 (64.6 %) | **up** (3.69) |
| `grow_mult[5]` | EGG | 143 (59.6 %) | down (0/143, unanimous at g30) |
| `grow_mult[1]` | CARROT | 142 (59.2 %) | down (45/97) — **flipped** from up at g20 |
| `press[4]`, `press[8]`, press[*] | MELON, FERT, most | 150 / 132 | **down** |
| `hire_bias` | — | 138 (57.5 %) | **up** (126/12) |
| `dev_weight` | — | 87 (36.2 %) | **up** (87/0) |
| **coarse** `plant_target[0]`→`[3]` | WHEAT→STRAWBERRY | 22 dn / 21 up, d3-5,10,12-15,22,27 | one tile swapped |
| **coarse** `forward_days` | — | 8/8 boards, **day 0**, 2→3 | +1 day of look-ahead |
| **coarse** `crew_target`, `plant_target[4]` MELON, `animal_want` | — | ≤7 board-days | mixed |

**The decode change is UNIFORM, not family-conditional.** Every knob with more
than a handful of hits moves the same way at the same rate on the 4 TOPTEN and
the 4 LIVEC42 boards (grow_mult[8] 119/120 vs 120/120 down; grow_mult[2] 91/18
vs 80/18 up; plant_target[0]→[3] 13/11 vs 9/10; `forward_days` 4/4 vs 4/4). The
only knobs that "differ by family" are ≤5 board-days of rounding-boundary noise.
g30 continues §93's g20 moves and pushes them further; nothing new appears, and
only EGG (mixed → unanimously down) and CARROT (up → down) change sign.

## 3. Ledger: where the coins move (`S/transfer/ledger.md`, `ledger_money.csv`)

Pinned-town sim, the replay that reproduces the engine to the coin (§101); the
ledger reproduces the trainer's own `B_margin` and `d_margin` to 0-40 coins on
six boards and to within one weed draw on the two noisy ones.

| board | family | g30−B d0-9 / d10-14 / **d15-29** | total |
|---|---|---|---:|
| 107014447 | TOPTEN | 0 / −43 / **+2,724** | +2,681 |
| 107014983 | TOPTEN | −276 / −360 / **+1,820** | +1,184 |
| 107015397 | TOPTEN | +2,423 / −2,957 / **+1,813** | +1,279 |
| 107015773 | TOPTEN | −212 / +111 / −26 | −127 |
| 107450083 | LIVEC42 | +344 / −1,312 / **−1,372** | −2,340 |
| 107431404 | LIVEC42 | −13 / −57 / **−3,949** | −4,019 |
| 107455021 | LIVEC42 | +28 / **−1,284** / −1,369 | −2,625 |
| 107434362 | LIVEC42 | +63 / **−1,779** / −563 | −2,279 |

* **The TOPTEN gain is d15-29, unanimously**, and it is THEIR purse falling.
  On 107014447 the opponent's money is coin-identical to B until d14 and starts
  bleeding at d20-22 (145,512 → 140,644 by d29): our purse −2,140, theirs −4,864.
  **The product is MILK.** g30 puts 22 more milk units into the market over
  d19-29 and the **milk price falls 118 → 72 (−46)**; strawberry +12 and melon
  +29 move the other way, i.e. we stop competing there while crushing milk.
* **The LIVEC42 loss has two halves.** d10-14 is **our purse falling with theirs
  untouched** (ours −1,489/−1,265/−1,301, theirs +290/+19/+11) — a sale we no
  longer make. d15-29 is **their purse rising** — denial we stop performing.
  On 107431404 (−4,019, the whole of it on **day 29**) the product is **CARROT**:
  B dumps 54 more carrot units on the last day, pulling the **carrot price
  96 → 79**, taking +2,292 for itself *and* knocking 1,657 off the band clone's
  own d29 carrot liquidation. g30 simply does not make that dump. Same signature
  on 107450083 in **WOOL** (B floors the price to 1, g30 leaves it at 11).
* The plan diverges from **d3** (money differs) but the margin only moves from
  d6-d17: the step changes the build early and is paid or charged late.
* g20 and g30 decode to the same plan on 4 of the 8 boards; on the others g30 is
  a partial retreat (it keeps 60-85 % of two TOPTEN gains, throws away the whole
  107015773 gain, recovers ~40 % of the 107450083 loss).

## 4. Mechanism, and the (a)/(b)/(c) verdict

**Mechanism.** The step re-aims our end-game price attack. It takes grow
priority off FERTILIZER, MELON, EGG and WHEAT and puts it on MILK, WOOL, TOMATO
and STRAWBERRY (swapping about one wheat tile for one strawberry tile on d3-15,
one extra forward-planning day at d0, one more hand), and it lowers `press` —
the sell-pressure that produces B's hard late dumps — on nearly every product.
Against the **top tier**, who run a fertilizer-and-mixed-crop engine (128
fertilize ops, 316 units bought, 41 carrot and 6 tomato plants against the band
clone's 62 / 199 / 31 / 0) and whose late income is broad, the extra milk
volume floors the milk price they are still selling into at d20-29 and takes
~5k off them for ~2k of our own — a profitable denial. Against the **band
clone**, which is a pure wheat-and-carrot build that liquidates in one lump at
d29, the same softened `press` cancels exactly the dump that was B's single most
valuable move on those boards: B's d29 carrot (and d15+ wool) flood both earned
us the last-day revenue and destroyed the price the clone was liquidating into,
so dropping it hands the clone back ~1.3k and costs us ~1.3k more. **Same
policy, opposite sign, because the two tiers liquidate through different
products at different times.**

**Verdict: (c) — a genuine strategic difference between the tiers that one fixed
`press` vector cannot serve — with the top-tier half of it over-fitted to the 20
trained opponents. NOT (a), and NOT (b) in the board-lottery sense.**

* **Not (a).** The decode is uniform — the step changes the same knobs the same
  way on the boards it wins and the boards it loses (§2), so it is not a
  conditional the planner already runs. And nothing available to condition
  *on* separates the two sides: opponent strength ρ −0.03, town-shop mix best
  ρ −0.11, opponent per-product sell volume best ρ +0.13 (p 0.07 over 40 tests)
  across the 196 rungs. The one observable the mechanism says should matter —
  which product the opponent liquidates through — does not predict Δ even when
  read directly off the opponent's own tape, which is strictly more information
  than the planner's `PolicyObs` carries. §78's refutation of the observation
  class stands; there is no conditioning variable to buy here.
* **(c) is the real structure.** The tier difference is genuine and is about the
  opponent's *late liquidation product*, not about their skill: LOSS10's
  opponents are the same build as LIVEC42's (163 wheat plants, 0 tomato, 61-62
  fertilize ops on both) yet the step gains +597 there and loses −344 here, so
  "band vs top tier" is not a strength axis at all. A single fixed `press`
  vector has to choose which product to floor at d29, and the choice that
  denies a mixed late seller is the wrong one against a carrot/wheat
  one-lump liquidator.
* **(b) is REFUTED at the board level and survives only at the opponent level.**
  The §110 gate's four replicates re-roll weeds only, so they are not
  independent boards. `S/transfer/freshword.py` supplies the missing test: the
  20 TOPTEN rungs and the 20 **worst** LIVEC42 rungs replayed on **two fresh
  seed words**, both seats, B vs g20 vs g30, pinned towns, same switches
  (`S/transfer/freshword.csv`, `freshword.log`).

  | set | words | n | Δ(g20−B) | SE | t | Δ(g30−B) | SE | t |
  |---|---|---:|---:|---:|---:|---:|---:|---:|
  | TOPTEN (all 20) | pinned | 20 | +294 | 207 | +1.42 | +172 | 194 | +0.89 |
  | TOPTEN (all 20) | **fresh ×2** | 40 | **+239** | 219 | +1.09 | +174 | 215 | +0.81 |
  | LIVEC42 (worst 20) | pinned | 20 | −1,556 | 235 | −6.62 | −1,379 | 235 | −5.85 |
  | LIVEC42 (worst 20) | **fresh ×2** | 40 | **−1,405** | 185 | **−7.59** | **−1,218** | 181 | **−6.74** |

  Both signs survive a fresh board draw, and the band loss survives it at
  t −7.6 **even on a set selected as the worst 20 on the pinned words** — a
  seed-lottery artefact would have regressed to the family mean (−344); it
  regresses by 10 %. So the transfer is attached to the **opponent tapes**, not
  to the pinned board words: it is not the board lottery, and §107's flat
  `mean_win` is a genuine trade, not noise.

  What *is* over-fitted is the **opponent list**. The gain does not reach fresh
  top-tier opponents: held-out TOPB2 reads −197 (sim/engine, §107) and the four
  records pooled in `S/topb2/insample.md` read **−1,274 SE 348** held out against
  **−224 SE 247** in sample. The step has learned a denial that works on *these
  20 top-ten recordings* and on their boards, and that does not generalise one
  tier sideways.
* **Which side is the Kaggle ladder on? The losing side.** Our opponents at
  2400-2700 are NEXT30 (+183 SE 203, t +0.90 — level) and the LIVEC/W2 band
  (−344 / −216). The ladder's mass is the band clone, so the step's trade is
  paid for in exactly the population that determines our rating, and collected
  in a population we meet rarely (TOPTEN 2821-2954) or only when we are already
  losing (LOSS10, where +597 of denial buys 0.0 → 0.075 of a win). **The
  objective's 33 % TOPTEN weight is buying a denial that the ladder charges us
  for.** That is a recipe finding, not a theta finding: re-weight before
  re-training, which is what flow211's 10 % TOPTEN / 38 % NEXT30 ladder does.
