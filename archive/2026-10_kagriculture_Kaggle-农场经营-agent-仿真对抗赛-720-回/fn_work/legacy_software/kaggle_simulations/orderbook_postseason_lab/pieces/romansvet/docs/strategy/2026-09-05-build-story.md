# 2026-09-05 — the day we found out what we were fighting, and what we were measuring

Build-story entry. Sources: the dated verdicts log
(`docs/strategy/2026-09-04-verdicts.txt`), the analyst reports `S/lossanat`,
`S/lossanat10` (+ `tomato_mechanism.md`), `S/select`, `S/simspike`,
`S/blueprint`, `S/today8`, and the memory notes `es-noise-floor-2026-09-05`,
`tape-action-seat-2026-09-05`, `kaggle-clone-family-2026-09-05`,
`counterfactuals-overstate`.

---

## 1. Where we stood at 14:00Z

Live on Kaggle: submission 56028553, theta `flow102_g280`, uploaded ~09:05Z. At
14:26Z we sat at **1952, rank 878**; #1 was 3055, #5 2891, #10 2828. The target —
top 5, 2891 — translates on our paired protocol to ≥90 % vs the band/wall/flood
tapes and ≥60 % vs the top-10 tapes. We were not close.

Two evolution-strategy arms ran on the remote 3090s: **flow106** (GPU0, verbatim
tape rung, margin-scale 15000, 7 top-tier gate tapes) and **flow111** (GPU1,
margin-scale 3000, gate on band6 + 4 top-tier). Between 12:12Z and 13:54Z flow106
produced three "records" — g20, g90, g300 — and the local paired protocol rejected
all three on the band (pooled 51.6 → 44.5 %, 49.7 → 46.0 %, 49.7 → 45.5 %).
flow111 had no record past generation 0. Twelve arms in a row (flow96–flow111) had
the same shape.

At 14:26Z the user cut the loop short: *"WHY NOT IMPROVE ES TRAINING?"* and *"DO
RESEARCHES CONTINUOSLY ON AGENT IMPROVEMENTS"*. The standing rule that came out of
it: every loop firing carries at least two improvement streams in flight;
monitoring is a side task. Three went out at once — opponent-supply forecast, ES
signal audit, top-tier economy blueprint.

## 2. What the opponent actually is

**It is one agent.** The band (1950–2110), the wall (1850–2025), 18 of the 20
top-10 tapes, and 7 of the 8 opponents that beat us today (1786–1907) are **one
open-loop clone family**, almost certainly a public-notebook fork. Signature:
hands-at-day-10 = 11, 12 melon tiles, 0 tomato, day-0 wheat pump of 22–62 units.
Opening frames jitter, so the opening key is a poor detector; the book is not.

Its book, days 0–28, is fixed to within a few percent whatever we do (top-10 panel
means, extracted from tape *action lists*; the band panel, measured from realised
fills, reads 350/350/264/263/176/72/0 — the ~10 % spread is the extraction basis,
not two different books):

| WHEAT | FERT | STRAW | MILK | WOOL | MELON | TOMATO |
|---|---|---|---|---|---|---|
| 386 | 320 | 259 | 244 | 178 | **72** | **0.2** |

Melon is *exactly* 72 units — 60 on day 10, 12 on day 11, ~17,440 coins at 242/u —
in all 20 top-10 and all 6 band tapes, on every board, against every theta. The
only other families are Crop Dusta (carrot/egg, 2 tapes, we win 100 %) and one new
build seen today, 105850738 "Planned Economy" (70 tomato, 186 egg, 84 wheat),
which we beat 84 %.

Paired on identical boards LIVE beats the clone 45–50 %, and the previous champion
`flow58_g450` does the same: on today's seven clone tapes LIVE 47.3 %, base 47.8 %.
**The wall has not moved all week. The population is the clone spreading.**

**What decides a game.** Variance over 576 band boards × 3 thetas: policy 46.4 %,
board draw 40.2 %, opponent identity 13.4 %; on the 18 top-10 clones, policy
44.8 %, board 47.2 %, opponent 7.9 %. The engine is deterministic, so the policy
term is pure signal. Nothing separates a win board from a loss board before day 8
(0.4 % of the eventual separation); 73 % of it lands on days 26–29 in the band,
76 % by day 27 in the top-10. The day-10 melon dump puts us 11–15 k behind on
*every* board, wins included — a constant tax worth 4.9 % of the separation, not a
discriminator.

The separating event: **our day-25-29 liquidation running into the clone's own
book.** On win boards we sell 79 u tomato at 155/u and keep milk off the floor; on
loss boards 17 u tomato and 255 u strawberry head-on against their 264. Same
board, same tape, different theta: on 512043734 f106 sells 62 strawberries instead
of 276 and *their* revenue falls 47.5k → 13.5k, a 38.9 k swing.

The implied ceiling is large: an oracle picking the best of three near-identical
thetas already on disk scores **79.5 %** on the band boards (LIVE 49.7 %) and
67.8 % on the top-10 clones (LIVE 45.0 %). 59 % of the boards LIVE loses are
already won by another theta we hold.

**Why the late price moves so much — the pot hinge.** `market_price` is a hinge on
a single shared inventory pot. For tomato (base 60, T=200) the day-29 price is 84
at pot 9800, 144 at 9700, 300 at 9600, 552 at 9500. No opponent touches tomato, so
`potD29 = 10000 − townTomatoConsumption + ourUnitsSold`, verified exactly on six
runs. On board 745775319 LIVE realised 99 c/u on 116 units, f106 423 c/u on 128 —
a 42,640-coin swing. But **~80 % of that gap is which shops the town drew (3
tomato-carrying slots vs 5), ~20 % is our schedule**: holding the town fixed,
LIVE's best possible schedule is 173/u (+8.5 k), not 423/u. Milk mirrors it on the
other side of the hinge — our own ~228 units tip the pot past 10000 and the price
floors.

**And the town draw is partly ours.** The engine's only RNG is
`random.Random((seed * 1_000_003) ^ day)` at end of day, consumed by one draw per
**empty tile on both farms**, then by the shop choice. The day-3 shop is therefore a
pure function of the seed (identical across all three thetas on 288/288 boards),
but the day-6 shop matches across thetas only 7.6 % of the time, day 9 only 2.8 %;
change the empty-tile count by ±1 and the drawn shop agrees 35 % of the time, by
±2, 13 % (chance). The seed is scrubbed from observations by design. Two
consequences: any counterfactual on a day-6-or-later shop observable is invalid,
and "leave a tile empty to re-roll tomorrow's shop" is a verified, **unmeasured**
lever. Difficulty *is* exogenous at day 3 — a YARN_STORE board is +10.6 k / 64 %
for all thetas, SMOOTHIE_SHOP and BRUNCH_SPOT 39–41 % — but *which* theta wins is
not predictable from it: the best honest day-3 rule gains +2.8 pts, 95 % CI
[−2.1, +7.6]. Not shippable.

## 3. Why the ES track had produced nothing

Three separate defects, all found today.

**The gradient was a coin flip.** `S/esaudit/noise.py`, pop 16 antithetic, two
independent seed sets, measured at production settings:

| sigma | episodes | spearman between seed sets | antithetic sign agreement |
|---|---|---|---|
| 0.005 | 64 | −0.04 | 0.50 |
| 0.02 | 64 | +0.08 | 0.55 |
| 0.04 | 64 | **+0.41** | 0.62 |

At the setting every arm since flow96 had used, the gradient sign reproduced 50 %
of the time. It was a random walk, and every "record" was the gate sampling noise.
Sigma, not episode count, is the binding constraint; the recommendation was
0.04 / 128 (2× cost, agreement ≈0.68). Larger sigma has a real cost: every
perturbed member sits 2–12 win-points below the centre, a sharp in-sim optimum.

**Gate defect #1: mean comparison.** The real gate compared leg *means* against a
raw min-gain and deleted per-game rows before pairing. Fixed on `es-signal-audit`
(a65af1c) with `--real-gate-paired-t T`: paired t on identical (seed, opponent,
seat) rows.

**Gate defect #2: unpaired replicate — and the case that exposed it.** flow112 ran
the new paired-t gate and produced a g10 candidate at +5.2 pts (44.4 % vs a 39.2 %
incumbent, n=480), confirmed on replicate at 49.6 %, pooled 47.0 % on n=960. The
local read: band6 pooled over three seed bases, **49.7 % → 41.0 %, t −4.31 on 576
boards**. Its log gave the mechanism: the replicate round replayed only the
*candidate* on the fresh base — `_fresh_leg` skipped the incumbent whenever
`prev_incumbent.theta` was None — so confirmation was unpaired, and one round where
LIVE happened to score 39.2 % (against 49–54 % everywhere else) promoted a theta
that loses 8.7 points locally. Fixed at 18:43Z (f3e6bfc): the replicate now replays
both legs, confirmation is a pooled paired t over both rounds, 84 gate tests pass.

**The fitness was a different game.** The ES "tape rung" is a *flow surrogate*:
one seat's per-day SELL/BUY aggregate replayed through `market.apply_flow`, with a
generic archetype behind it. On 288 bit-exact band boards, sim-vs-engine margin
correlates only **spearman 0.25 per theta, 0.12 within-board**, and the surrogate
plays far stronger than the real tape (sim margins −6…−10 k where the engine gives
+1…+3 k). The sim-chosen theta realises 49.7 % on the engine — exactly
always-LIVE, 0 of the 29.8-point oracle gap captured. Our own seat is bit-exact
(10/10 parity), so this is entirely the opponent seat.

The fix was built the same evening: an **action-replay opponent seat**
(`src/kagg3/es/tape_actions.py`, branch `tape-action-seat` 944dde8), cutting a
packaged tape's 719 frames into day-major int32 op tables spliced into
`rollout.run_day`. Parity: 8/8 boards byte-exact on both seats vs tape 105443859,
7/8 vs 105442685 (one 4-coin miss at day 28, a below-floor SELL-meets-BUY collision
— the one known gap). 0.44 s/game against 0.22 for the flow rung. The noise sweep
re-run on this rung gave spearman +0.52 and sign agreement 0.68 at sigma 0.04 —
better than the flow rung — but the perturbed members now sit 21.5 win-points below
the centre instead of 9.3: real opponents make the landscape sharper.

## 4. Eleven planner levers, eleven rejections

All measured paired against LIVE on identical boards, mostly band6 at seed base
777001 (192 boards), several on more. (The log's running tally reads 7 at 16:56Z
and 11 by 20:12Z; the count depends on whether the two sell-lot modes are one lever
or two. Eleven rows, ten switch families.)

| lever | result |
|---|---|
| MELON_OPEN_ON alone (plant 12 melon d0, tile total preserved) | 54.2 → **15.1 %**, −17,554, t −12.8, theirs +12.9 k |
| Herd survival (CARE_FILL + 4 hops + TAIL_FILL) | band 54.2 → 50.0 %, margin +575 — ours +3.5 k *and* theirs +2.9 k; top10 level |
| Sell-lot mode B + lot re-projection fix | 54.2 → 39.6 %, t −22.7 |
| Sell-lot mode A21 + fix | 53.6 % level; top10 48.3 → 48.3 % |
| Late tomato tile budget | 12 tiles 54.2 → 43.8 % t −5.0; 6 tiles 45.8 % t −3.4 (dose-responsive) |
| Late strawberry cap | pooled 3 bases 49.7 → 48.6 %, t −1.8; flood level |
| Opponent-supply forecast v1 | scale 1.0 54.2 → 46.9 % t −3.8; scale 0.5 → 43.2 % t −4.8 |
| Opponent-aware late mix | day-12 gate inert (175/192 identical); day-8 54.2 → 53.1 % |
| Tomato hold to d27-29 | 54.2 → 47.9 % t −10.3; top10 48.1 → 46.2 % t −16.9 |
| Opponent-supply forecast v2 (executed curve, turn-resolved) | 54.2 → 45.8 % t −3.9; scale 0.5 t −4.4 |
| Front-run mode F (lots at 3/9/17) | 54.2 → 48.4 %, t −10.2, 0/11 boards; unsold 3.6 → 35.9 u/game |

Several were the *best* candidates the analysis produced — the tomato schedule from
the pot-hinge mechanism, the supply forecast from the clone's fixed book, the herd
bundle from a measured 16→9 herd collapse in 16 of 16 games. They lost anyway.

Two lessons they share. First, **the shipped theta plus planner is single-switch
locally optimal**: no one flag moves it, and most failures carry double-digit
t-statistics. Second, **the pot is shared**, so nearly every change to our sell
schedule moves the opponent's revenue as much as ours, usually upward. The herd
bundle is the clean illustration — it added 3.5 k to us and 2.9 k to them, and the
win rate fell. The supply forecast is the other: any forecast inside
`projected_inv` makes the greedy allocator vacate the lot and the clone takes the
quote. Front-run mode F closed the sell side for good — our crew's h9/h17
deliveries land *behind* the lot, leaving 36 units a game unsold.

Same lesson `counterfactuals-overstate` has accumulated all week: a ledger, a
regression over finished games, or a price model is a hypothesis with a number
attached, never a value. Only a paired engine run counts, and expect the sign to
flip.

## 5. What is running now

At 18:53Z flow112 and flow113 were killed (surrogate fitness, unpaired replicate)
and two arms launched on `~/stage_ta` (trunk 8ca1fc6), the first whose fitness *is*
the engine outcome against real Kaggle opponents:

* **flow114** — GPU0, sigma 0.04 / 128 episodes, seed 214
* **flow115** — GPU1, sigma 0.02 / 256 episodes, seed 215

Both train on **action-replay** rungs only — band6 (weight 3), flood6 (1), wall6
(1), six top-tier tapes (2), no flow rungs — and gate with paired t ≥ 1.7 on 24
games plus a 48-game *paired* replicate. flow114's gen-1 mean win on the ladder was
0.39: the real opponents are harder than the archetypes. Its gen-0 baseline (the
LIVE init) reads 46.0 % on n=480, provisional.

Success means the promotion protocol, unchanged: **band level or better, top-10
up, flood not worse — all paired on identical boards**, across at least three seed
bases, using `--seed-per-opponent`. A remote gate acceptance is a nomination, never
a promotion; flow112_g10 is the latest theta to prove why.

## 6. Open questions and the queue

* **Sigma for the action rung.** Signal is better (0.68 at 0.04) but the members sit
  21.5 points below the centre. If flow114's candidates keep failing the gate, sigma
  comes down. The 0.02 cell of sweep #2 is still pending.
* **Full-theta.** `~/launch_flow116.sh` is drafted (flow114 recipe, `--train-only
  all`, sigma 0.01) and deliberately **not** launched: full-theta ES has been a
  simulator exploit twice and needs its own sigma sweep on the faithful rung first.
* **The gate's board set.** flow112's gate boards (seed base 20260904) disagreed with
  777001/777002 by 15 points. The statistic is fixed; the fixed board set is not.
* **The empty-tile shop re-roll.** Verified mechanism, never measured — the only
  identified way to touch the ~80 % of the tomato/milk price gap that is the town
  lottery.
* **The oracle gap.** 30 points on the band, 23 on the top-10, sitting in thetas we
  already have. No simple rule finds it. If ES on faithful fitness cannot close it,
  the next idea has to be a different shape.

## What a reader should take away

Two things were wrong at once, and each hid the other. We were fighting a single
open-loop clone that has spread across the whole 1786–2828 band — one fixed book,
one melon clock, zero tomato — while believing we faced a population; and we were
measuring candidates against a market-flow surrogate through a gate that compared
unpaired means, so twelve arms of "records" were noise about a game we were not
playing. Fixing the measurement was worth more than any of the eleven levers built
from good mechanistic analysis, all of which lost, several badly, because in a
shared price pot a change that earns us coins usually earns the opponent more. We
now know exactly what we are fighting, we know a 30-point ceiling sits in thetas
already on disk, and we have — for the first time — a fitness signal that is the
same game as the engine. Whether that is enough is tomorrow's measurement, not
today's claim.


---

# 2026-09-06 — the day the levers ran out and the sim became the engine

Build-story entry, same log. Evidence: `S/glut/verdicts.log` (20:44Z–14:05Z);
`S/select2`, `S/select3`, `S/crn2`, `S/escurve`, `S/esstep`, `S/esstep2`,
`S/coupling`, `S/top5anat`, `S/jesse_anat`, `S/taskdiff`, `S/shopcrn`; worktrees
`pump-aware`, `melon10`, `ramp11`, `sheep9`, `quad3`, `latesheep`, `wool13`,
`dropearly`; memory `sim-equals-engine-2026-09-06`, `shop-lottery-2026-09-06`.

## 7. The sim became the engine

One fidelity bug remained: at 21:13Z (`tape-act-cold`, 6acd08d) `warm_frac 0.25` was
still reaching action-rung episodes — our theta won **96 %** of warm openings against
**51 %** of cold ones, inflating the sim centre to 0.61 where the engine read 0.50.
Cold-only rungs put per-rung sim win within 8 points of the engine (0.500 vs 0.497).
`S/select2` then measured the corrected seat on 288 band6 boards × 3 thetas × 2
seats. **The sim is the engine**: margin sign matches
**99.5 %** of games, **82.5 %** are byte-exact on final coins, Spearman .9997,
within-board contrasts 99.5 %. Every offline counterfactual on a known board is now
exact, and ES fitness is the engine's verdict.

It did not buy a policy. Sim-argmax over three thetas we already hold realises the
oracle — **79.5 % / +12.5 k** against always-LIVE 49.7 %, **+29.9 points** (CI
+24.8…+34.9) — but only with the true seed; on other boards of the same tape the pick
is worth 40–51 %, and truncation loses it (day-20 cut 66.5 %). Seed inference is dead
(Kaggle seeds are ~31-bit randoms scrubbed by `resolve_episode_seed`, leaking ~2.6
bits per three days), and `S/select3` closed the family from the other side: the
mid-game `State` splice is exact (0/192 mismatches), but switching at each shop reveal
with K random futures never clears +5 points with confidence (best day-21 K=16: +5.2
[+1.0, +10.4]) and the split-half reliability of the theta contrast at days 6–12 is
≈ 0. **The +29.9-point oracle is max-of-three on end-of-day draw noise.** Theta
selection, day-0 or adaptive, is closed.

## 8. Three measurements of the ES gradient

**The signal was in a space we were not training.** The CRN audit (`es-crn`, 75a1336)
confirmed boards are already shared across candidates and antithetic pairs, then found
that every sweep showing signal — including 0.734 sign agreement at sigma 0.02 — had
run with `train_only="all"`, the full 4,188-coord theta. The **535-coord bias space
flow114–119 trained reads 0.37/0.44 at sigma 0.02 = chance**, and `S/crn2` bought
reproducibility there only by paying displacement: 0.73 sign agreement at sigma 0.04
but −26 points below centre, 0.86 at 0.12 for −52.

**A reproducible direction is not an improving direction.** `S/esstep`: that bias
0.04 cell did not replicate on a second seed pair (Spearman −0.04), and one
trainer-exact generation (pop 128, E=32, fresh 192-episode paired eval) left the centre
level-to-down at every learning rate in both spaces (full lr 0.03: −20 pts, t −7.9)
while **a random step of identical norm beat the gradient in both** (+7.3 / +5.2).

**E is the lever, and it still does not transfer.** `S/escurve` (1,536 shared
episodes) showed the full-theta gradient at sigma 0.02 *is* real: half-split Spearman
0.33/0.48/0.61/0.74/0.83/0.86 at E = 32/64/128/256/512/768, against 0.15…0.58 for bias
at 0.04; bias-only training closed. Then `S/esstep2` stepped that E=1536 gradient on
fresh boards: it **never beat a norm-matched random step** (‖0.3‖: 0.0 vs +2.0 pts;
‖1.0‖: −9.2 vs −5.1), the +5.5 at Adam lr 0.001 was a max-of-8 that vanished on
replication, and a second step lost 4.8 points (t −3.6). The gate agreed all day:
gen-10 candidates at −8.7 and −10.6 points, a gen-150 at −19, all paired at n=480.
"Reproducible but useless" has an exact cause, below: **on fixed boards the shop
lottery is deterministic, so the gradient was learning which tile layouts had drawn
good shops.**

## 9. The shop lottery

`S/coupling` asked why every rejected lever ends with *"theirs +15 k"*. Under our
switches the clone's executed units are **byte-identical** — its coin change is 100 %
price — and ~100 % of that appears **after the first divergent shop draw**: before it
+27 / +4 / +11 / +2 coins, after it +27.4 k / −4.4 k / −2.8 k / +25.8 k. Mechanism,
reproduced 8/8: `_end_of_day` builds `Random((seed * 1_000_003) ^ day)` and consumes
**one draw per empty tile — ours, then theirs** — before `rng.choice(sorted(SHOPS))`
every third day, so any lever that changes our empty-tile count re-rolls every later
shop. YARN_STORE, the only wool sink (~70 % of games), pays the clone's 195 wool
25–27 k.

Two consequences: paired ON/OFF legs carry an **unpaired, zero-mean ±25 k term**
whenever tile usage differs — t > 5 rejections stand, |t| < 3 verdicts may be lottery,
and today's "theirs +16 k" figures are that term, not a gift we handed over — and ES
candidates inherit it, which is what forced E ≥ 512.

The fix landed at 13:05Z (`shopcrn` a85b008 → trunk): `--shop-crn` draws the shop
from stream word 400 (`SHOP_CRN_BASE`, past any weed walk), OFF staying 4/4
byte-exact. Half-split gradient Spearman at E_half 32/64/128/256 goes
**0.34/0.48/0.62/0.72 → 0.83/0.89/0.93/0.95**, pair-difference sd 0.9–1.1 → 0.2–0.4,
**episodes to |t| = 2 per pair 295 → 41** — with per-episode fitness variance
unchanged (ratio 1.01), only its correlation across candidates.

## 10. Climbing a hill that was not the gate

At 10:00Z the arms confessed: flow120's in-sim mean win rose 0.49 (g26) → 0.56
(g176) **while its engine gate fell 49 % → 30 %**. The mix it was climbing — 24 tapes
plus `kagg2_flow`, archetypes and anchors under a margin-shaped score — is not what
the gate measures. flow123 launched with **gate-only rungs** (band6 w3 + four
top-tier gate tapes w2, `--arch-frac 0`); gen 1 mean win 0.27, a visibly harder
ladder.

## 11. The clone gap, and eight more levers down

`S/top5anat` put 18 top-5 games (17W-1L) beside 8 of ours on the same clone book,
engine-exact. Margin by band, top-5 vs ours: days 0–9 +923 / +2,594; **days 10–19
+2,422 / −17,451 (t −10.5)**; days 20–29 +6,697 / +3,830. The whole gap is d10–19, in
three parts: the **melon pot race**, 54 % of the deficit — the clone buys 12 melon
seed at d0h0 and holds 54 melons by d10h08 (the first 72 melons pay 16.8 k, the next
72 only 9.4 k) where we ship d13h12 at 161 average, −5.9 k (t −18); the **hand ramp**,
max hands d1–11 of 1/3/4/4/7/3/5/7/7/7 against 3.5/4/5/4/5/8/8/10/10/11 and **not
cash-bound** (5.0 k in hand at d9); and the **plate**, 47 worked tiles d14–19 vs
59–60, 1,260 units sold vs 1,518. The crop book is not the problem.

A correction at 04:35Z (`S/jesse_anat`): the four "Jesse Bullard" tapes replay *his
opponents*, both seats running the clone book — Jesse is a clone variant whose hard
form differs by **four extra sheep** (8 by d10 vs 4) → 262–274 wool units vs 138–187,
wool correlating −0.996 with our margin. The sheep audit graded rather than split it:
over 24 sampled wins and all 59 losses, reweighted win rate is **72 % / 65 % / 56 %**
at ≤5 / 6–7 / 8+ sheep by d10.

Every lever built from that anatomy lost:

| lever (worktree) | result | why |
|---|---|---|
| MELON_D10 (`melon10` abea3f2) | band6 54.2 → **17.2 %**, −18.6 k t −13.6 | one excursion per unit per day → 66 u dumped at turn 18 at 180/u, and the melon board drops our d0 pump |
| MELON_D10B (25d933f) | board+cap → **13.0 %** t −15.5; cap-only 43.2 % t −4.8 | pump *not* displaced; the plate displaces our **animal line** (COW 3→1, egg 2/day vs 5–12) — a price gift reaching +31 k by d27 |
| Crew ramp (`ramp11` c5e7f40) | band6 55.0 → 52.5 %; top10 69.4 → 55.6 %, t −3.0 | hires are capped by **task count, never cash**: forcing the curve raises PASS 15 → 37 % of unit-turns and cuts revenue 112.8 k → 67.3 k, and hire bills price land off the purse → no third quadrant |
| SHEEP_D9 (`sheep9` 6def10c) | jesse4 60.2 → 67.2 % (t 0.4); band6 54.2 → 49.0 % | forced sheep sit in the shed — no empty tile until our d13 quadrant; wool sells d19–29 at mean 18 |
| QUAD3 early land (`quad3` b5c3f47) | d8 band6 47.9 % t −4.0; d6 44.3 %; d10 inert | we were **not** behind on land (clones buy d6h6/d11h1, we d5/d11–12); it displaced 5 tomato for 6 carrot and gave the tape +8.0 k |
| LATE_SHEEP_CAP d11 (`latesheep` 77fa87a) | band6 54.2 → 42.7 % (t −7.3); top10 45.5 % t −8.8 | the sheep are waste (3,000 coins buy 70 wool worth 944) but zeroing `animal_want[SHEEP]` shrinks the fill reserve → wheat eats the pastures: one dropped sheep = +32 wheat, milk −79 u, −33,557 coins |

The two levers that hold tiles fixed came back **inert**, 192/192 pairs identical:
WOOL_DUMP d13 (`wool13` ca56556) because the planner is already a same-day liquidator
over `SELL_TURNS` 3/10/18, and DROP_EARLY (`dropearly` 11ce87f) because we sell 84 %
of revenue at h1 and moving the h18 lot earlier costs 272 coins at h10, 1,111 at h3 —
the town drains the pot through the day, closing the sell-timing family. The
**pump-aware hour-1 row** (`pump-aware` 62baf5e) is likewise 392/392 bit-identical to
OFF now `OPEN_PUMP_SLOT0` ships, and a **second price attack** died on the engine
quoting `BUY_SEED` at a fixed `CROPS[item]['seed']` (kaggriculture.py:603).

`S/taskdiff` (18 loss replays) explained the plate without a new lever: per hand-turn
we are **level** (0.44 vs 0.43 task-units, d10–14). The clone wins by owning 11 hands
to our 7 at d10 and idling 6 % against our 15 %, spending the surplus on wheat
rotation (WATER +149, t 29), **hourly PLACE+SELL pairs** (7.4–8.3 sell hours a day
against our three fixed `SELL_TURNS`), and selling fertiliser where we apply it. Every
named class is closed or previously lost except that cadence taken as a *pair* — the
one thing still standing on the planner side.

## 12. The Kaggle record

Submission 56028553 (`flow102_g280`) played all night and slid: rating 1861 →
**1840**, tally 81W-39L (67.5 %) at 20:44Z to 105W-69L (60.6 %) at 13:15Z, the
leaderboard entry moving from the older 56013041 (rank 967 / 1895) to 56028553 at rank
1025 / 1851 and then **1036 / 1837**. About thirty losses were cut into opponent tapes
overnight, the pattern unchanged — the clone book, 47–50 % against it — the worst run
(13 losses in three hours around 05:00Z) being the 8-sheep variant plus poor boards
where both sides finish under 80 k.

## 13. What is open at 14:05Z

* **flow124** (GPU0) = gate-only rungs, full theta, E 256, **`--shop-crn`**, gen 1
  mean win 0.26, against **flow123** (GPU1) as the identical no-CRN control — the
  first pair whose fitness noise has had the lottery removed.
* **`S/esstep3`**, the CRN-gradient transfer test. If this gradient does not transfer
  either, ES on this fitness is finished and the next idea must be a different shape.
* **Trunk test debt** at 6acd08d, seen by two agents on untouched base trees:
  `test_archetype_ladder.py::test_mixed_ranch_is_the_eighth_slot_and_the_runner_up_of_the_cold_yardstick`
  and `test_warm_start.py::test_a_handicap_with_no_rung_to_land_on_is_refused`. Fix in
  `S/wt_testfix`.
* **Unpriced price attacks**: strawberry d4 30 u (+8.4 k modelled), fertiliser
  +27–40/u — both move tile usage, so both need ≥3 seed bases and a win-rate read.

**What a reader should take away.** Yesterday's fix — make the simulator the game —
worked completely and bought nothing directly: the sim now agrees with the engine on
99.5 % of margin signs, and the +30-point ceiling it exposed was max-of-three on
noise. Today's finding is that the same noise sat underneath everything else. One RNG
draw per empty tile means any change to our plate re-rolls the town's shops — which is
why the ES gradient was reproducible and useless, why the structural levers kept
coming back with "and theirs +15 k", and why the levers that hold tiles fixed measure
cleanly and turn out inert. The planner's single-switch space is exhausted, with a mechanism
attached to every rejection: the crew follows the plate, the plate follows the
reserves, and the reserves punish any single switch. What is left is a fitness with
the lottery removed, and one untested cadence.

### 2026-09-07 — joint plate lever, flow125 first record

- **JOINT_PLATE** (worktree `joint`, 3839aed): the top-5 sizing rule written as one
  target — carrot plate from the shop draw, sheep/cow floors from wool/milk sinks,
  crew from the plate's task count, land bias when the plate over-asks. Rejected at
  every dose (band6 54 → 1 % at scale 1.0, 13 % at 0.5, 10 % without the crew floor).
  Mechanism: the crew floor hires against an intention with no tasks — 7 hands on
  day 6 with PASS 58 %, a quadrant bought on day 0 and left unstaffed. The pass-A
  land-reach repair is real but not binding (level alone, moves the joint lever by
  30 coins). Lesson after 15 hand levers: sizing numbers must be derived from the
  task list after `_derive`, never written above it.
- **flow125 gen-0 record**: the gate's first incumbent is a sigma-scale perturbation
  of the init (cold-start init nomination lost the race). The lottery-free sim screen
  puts it below LIVE on band6 (48.6 vs 51.6 %, −908/game, t −6.2) and on the hard
  tapes (62.5 vs 65.1 %, t −3.8). Rejected without engine legs. The gate bar is
  therefore below LIVE and the local screen stays the judge.
- Spike in flight: can the CRN sim screen judge planner switches (reproduce the
  passa engine deltas)? If yes, a 26x cheaper lever screen makes a knob sweep
  feasible in place of hand-built levers.

### 2026-09-07 — the tape arms were self-play (configuration bug found)

- An audit of why flow125's population mean win fell 0.44 → 0.27 while training
  found that `--arch-frac 0.0` gives the archetype block, which holds every action
  tape rung, zero episode slots (`src/kagg3/es/train.py:583`). flow123 through
  flow127 therefore trained on 100 % self-play; their rung weights were inert and
  the logged win rate was self-play win. flow114–122 had 25 % tape slots. The
  objective itself is a soft win bit (rank of mean sigmoid(margin/3000), corr +0.94
  with win); the sharp mean-win crash at gen 131 was the re-centre's sigma bump.
- Consequence: every "ES on action tapes is board-specific / flat" verdict taken
  from a remote arm since flow123 is void. flow128 (41 Kaggle-loss tapes + band6)
  and flow129 (band6 + hard variants) relaunched with `--arch-frac 0.9`, the four
  archetypes weighted 0, and the sigma bump disabled.
- Same day: the crew-from-tasks lever (crew sized from the derived task list)
  lost at every dose that hires more than the gene's ramp — extra hands only PASS.
  Labour is not this planner's binding constraint; the admitted task list is.
- The lottery-free sim re-screen confirmed all eleven rejected hand levers as
  genuine losses.

### 2026-09-07 11:35Z — first positive sim lever is level in the engine

The admit/route pair (ADMIT_PICK_SHARED=True, EST_HOME=7) that the lottery-free sim
scored +3.1 pts / +427 per board on band6 went through the full engine protocol
against the LIVE build (theta flow102_g280, six legs, 1,904 paired boards):

| leg | n | win OFF → ON | margin | t |
|---|---|---|---|---|
| band6 @777001 | 192 | 54.2 → 47.4 | −630 | −1.1 |
| top10 @777001 | 640 | 48.1 → 50.2 | +294 | +0.9 |
| band6 @777002 | 192 | 49.0 → 52.6 | +92 | +0.2 |
| jesse4 @777001 | 128 | 60.2 → 60.2 | −506 | −0.8 |
| flood6 @777001 | 96 | 59.4 → 59.4 | +491 | +0.5 |
| today41 @777001 | 656 | 55.2 → 53.0 | +444 | +1.4 |
| **pooled** | **1,904** | **52.6 → 52.3** | **+188** | **+1.0** |

Level on win rate everywhere, margin a hair up. The sim gain sits inside the shop
lottery (engine sd 8k/board vs 1.4k in the sim): band6 across both bases came out
−269 ± 412, 1.7 se below the sim's +427. Not promoted; the switch stays available as
a free rider for the next bundle. Lesson: a sim lever needs to clear ~+800/board
before the engine can confirm it at n≈2k, or it needs a 5k-board engine run.

### 2026-09-07 12:40Z — shop-gated carrot sizing is not the top-2 edge

The #1/#2 agents' carrot tiles track the carrot-sink draw (+26 per PET_CAFE/FARMERS_MARKET
shop). Built as CARROT_SINK_ON (hold base + per-sink carrot tiles from day 12, mix rewrite in
the ENDGAME_TOMATO shape, OFF byte-identical 576/576) and screened on the lottery-free sim:

| setting | band6 win | margin | t |
|---|---|---|---|
| PER=20 | 51.6 → 27.8 % | −9,283 | −24.6 |
| PER=12 | 51.6 → 27.4 % | −8,912 | −24.3 |
| PER=3, BASE=0 | 51.6 → 47.2 % | −1,608 | −10.2 |
| PER=3, BASE=0 (jesse4) | 65.1 → 61.7 % | −1,664 | −8.1 |

The loss is our own purse, not the opponent's gain, and it grows with the sink count: a
carrot-rich town is where our softmax already tilts to carrot, so the rule's headroom is
largest where the displaced wheat/strawberry tile was worth most. The regression counted
plantings over a season; keiz holds ~3 tiles per sink, plants from day 17 and sells at
day 26. The transferable half, if any, is carrot timing, not carrot count.

### 2026-09-07 14:30Z — tomato abstention: the planner already does the half that matters

The #2 agent plants no tomato with fewer than two tomato buyers by day 9. Built as
TOMATO_GATE_ON (tomato share handed back to the mix, OFF byte-identical 576/576):

| leg | n | win OFF → ON | margin | t |
|---|---|---|---|---|
| band6, SHOPS=2 | 576 | 51.6 → 52.1 % | −135 | −4.1 |
| band6, SHOPS=1 | 576 | 51.6 → 51.6 % | +2 | +0.6 (570/576 identical) |
| jesse4, SHOPS=2 | 384 | 65.1 → 65.1 % | −130 | −4.2 |

Split by the draw: boards with two or more buyers are untouched, zero-buyer boards are
already abstained by the planner, and the whole loss sits on one-buyer towns, where a
single shop plus the town centre is a real pot we sell into. The other seat gains
nothing; the loss is our own purse. Second shop-gated sizing lever rejected today with
the same signature: the top agents' shop rules describe their season, not a marginal
tile in ours.

### 2026-09-07 14:50Z — the tape rungs pay: flow129 gen-40 promoted

The first ES arms with the action-tape rungs actually live (the arch-frac slot bug was
fixed this morning) produced a record at generation 40 on both GPUs. Both arms' gate
incumbent turned out to be the LIVE theta itself, so the remote paired reads were direct
comparisons: flow128 +11.2 win pts, flow129 +4.9 pts on the band6+hard rung (n=384).
The remote gate rejected flow129's on its margin t-rule; the local sim screen put both
at +2.7-2.9k per board (t 15-16) against LIVE, and the engine agreed:

| flow129 gen-40 vs LIVE | n | win OFF → ON | margin | t |
|---|---|---|---|---|
| band6 @777001 | 192 | 54.2 → 57.8 % | +506 | +0.5 |
| band6 @777002 | 192 | 49.0 → 60.4 % | −237 | −0.2 |
| top10 @777001 | 640 | 48.1 → 58.3 % | +2,187 | +2.9 |
| jesse4 @777001 | 128 | 60.2 → 78.9 % | +3,080 | +2.6 |
| flood6 @777001 | 96 | 59.4 → 60.4 % | −311 | −0.2 |
| today41 @777001 | 656 | 55.2 → 61.3 % | +2,196 | +2.9 |
| **pooled** | **1,904** | **52.6 → 61.0 %** | **+1,710** | **+4.1** |

Win rate up on every leg, margin up where it matters (top10, today's losses). The theta
wins by denial: our own purse falls 1.5k per game, the opponent's falls 3.2k, with 40-100
more unit moves per game. Packaged on HEAD 0a933e5 as dist/submission_flow129_g40.tar.gz
(md5 0d5539f4), smoke clean, handed over for upload. flow128's gen-40 (band +10.4 pts,
top10 +10.2 pts on the first two legs) is still in the engine and may supersede it.

Addendum 15:50Z: flow128's gen-40 finished its six legs at the same pooled reading
(52.6 → 61.0 %, +1,350, t 3.4; band +11.9 pts, top10 +10.2, today41 +2.9). Head to head on
the same 2,000 boards the two are level on win rate (62.3 vs 62.1 %), flow129 a little
better on margin and on today's losses, flow128 better on the band. Two independent
seeds, two rung mixes, one answer: the tape-rung ES signal is real. flow129 stays the
upload; flow128 is packaged as the alternate (md5 e086b74a). flow129's gen-100 record
(+24.7 win pts at the gate) is in the sim screen.

### 2026-09-07 16:45Z — herd latency: the lag is a flow, not a gate

The #1 agent locks its herd the day after a wool or milk shop unlocks; ours locks 3-5
days late. The diagnosis found no shop, cash, admission or pasture gate: the brain emits a
per-day animal flow as a fraction of free tiles, never a herd level, and that want has
collapsed to a tenth of an animal a day by the time the sinks unlock. The full rule
(intercept plus slope) front-loads ten head onto 600-coin boards and loses 5.8k per board;
the slope-only arm is +363 (t 4.8), a day-15 gate trims it to +261, and jesse4 reads +206.
On every leg our purse is flat and the opponent's falls: a pure denial lever, a third of
the bar. Parked, committed OFF. That closes the shop-rule family from the top-5 analysis:
carrot count, tomato gate, endgame tomato, herd latency all lost or fell short.

### 2026-09-07 19:15Z — flow129 gen-100 supersedes gen-40

Sixty generations later on the same arm, the gate read +24.7 win pts against LIVE and the
engine confirmed it on the full six-leg protocol:

| flow129 gen-100 vs LIVE | n | win | margin | t |
|---|---|---|---|---|
| band6, two bases | 384 | 51.6 → 68.8 % | +2,291 | +2.6 |
| top10 | 640 | 48.1 → 66.9 % | +4,152 | +5.8 |
| jesse4 | 128 | 60.2 → 81.2 % | +3,996 | +2.9 |
| flood6 | 96 | 59.4 → 68.8 % | +1,694 | +0.9 |
| today41 | 656 | 55.2 → 70.1 % | +4,409 | +6.3 |
| **pooled** | **1,904** | **52.6 → 69.4 %** | **+3,731** | **+9.2** |

Head to head with gen-40 on the same boards it is +7.7 win pts and +1,867 per game
(t 4.8). Packaged as dist/submission_flow129_g100.tar.gz (md5 5a6967b6), smoke clean,
handed over in place of gen-40. The trajectory of one arm, gen 0 → 40 → 100, is
+0 → +8.4 → +16.8 win pts against the live build, all under a weight decay that the
autopsy says costs about 5k per game by itself; flow130 now runs the recipe without it.

### 2026-09-07 21:50Z — the ES edge cannot be lifted into a mix rule

Copying the promoted theta's strawberry race into an explicit planner rule (14 tiles by
day 6, sell as it ripens, no late strawberry) lost on both the live theta (51.6 → 40.8 %,
−4.9k) and on gen-100 itself (73.1 → 56.8 %, −5.8k, with the clone gaining 2.8k). The
sell part is byte-inert: this build already sells ripe strawberry the day it lands, so the
theta's extra early units are supply, not carry. The plant part is the whole loss and it
is displacement: a mix rewrite conserves tiles, so the 14th strawberry comes off day-0-6
wheat and melon, and the damage is monotone in how much of the opening it takes. The
theta reached the same tile count while planting more wheat, paid for by earlier hiring
and more unit moves. Five mix-rule levers lost today with the same signature; the hand
planner's mix stage is closed and the campaign's engine is the tape-rung ES.

Addendum 23:40Z: flow129 gen-180 finished its six legs at 52.6 → 70.9 % (+4,278, t 10.1)
against LIVE, and this time our own purse is level (−37) while the opponent's falls 4.3k:
the arm has started converting denial into a clean edge. Head to head with gen-100 on the
same 2,000 boards it is +1.3 win pts and +408 (band +3.6 pts, top10 −1.7), inside noise.
Packaged (md5 aa68182a), smoke clean; offered as the file to upload if gen-100 is not yet
up, otherwise not worth a rating restart. The arm's trajectory: gen 0/40/100/180 =
+0 / +8.4 / +16.8 / +18.3 win pts over the live build.

Addendum 2026-09-08 01:50Z: the decay-off arm's first record (flow130 gen-40, from recB)
reads +15.9 win pts over LIVE on the six-leg protocol but is level with its own starting
theta and 2.4 pts behind gen-180 head to head. Removing weight decay has not yet shown an
engine-visible gain in 40 generations; the gate's paired +6.5 pts against recB did not
survive the 1,904-board read. Not promoted. gen-180 (or gen-100, whichever is uploaded)
remains the live recommendation.

### 2026-09-08 05:50Z — the decay-off arm takes the lead: flow130 gen-130

flow130 was launched from flow129's post-gen-100 record with weight decay switched off,
after the autopsy showed the promoted thetas were 0.9 × LIVE plus a residual. Its gen-40
record was level with its start; its gen-130 record is the new best on every leg:

| flow130 gen-130 vs LIVE | n | win | margin | t |
|---|---|---|---|---|
| band6, two bases | 384 | 51.6 → 75.3 % | +4,969 | +5.7 |
| top10 | 640 | 48.1 → 71.7 % | +6,153 | +8.1 |
| jesse4 | 128 | 60.2 → 78.1 % | +4,808 | +3.2 |
| flood6 | 96 | 59.4 → 78.1 % | +4,611 | +2.5 |
| today41 | 656 | 55.2 → 76.1 % | +6,365 | +9.6 |
| **pooled** | **1,904** | **52.6 → 74.7 %** | **+5,819** | **+14.2** |

Our own purse is up 241 per game while the opponent's falls 5.6k. Head to head with
gen-180 on the same 2,000 boards it is +3.8 win pts and +1,664 (t 4.7), significant on
top10 (+6.5 pts) and today's losses (+4.0 pts). Packaged as
dist/submission_flow130_g130.tar.gz (md5 8abf84da), smoke clean, handed over as the
upload. The campaign's climb over the live build now reads gen 0/40/100/180 of flow129
at +0/+8.4/+16.8/+18.3 win pts, and flow130 gen-130 at +22.1.

### 2026-09-08 07:45Z — the carrot timing is not a reservation

Copying gen-130's carrot re-timing into a reservation floor (hold carrot below 1.25-2×
base in days 10-24, then liquidate) lost on both the live theta and gen-130 itself,
monotone in the dose and insensitive to the window. The two-purse read explains it: our
purse is flat, the clone's rises. Deferring carrot cash out of the mid-game starves the
hires and land that suppress the clone's strawberry and wool quotes, so the lever hands
denial back; on gen-130, whose sell gate already holds carrot, the explicit floor pushes
past the optimum and loses 2.6× harder. Rule adopted for every future screen: read the
two purses separately before the margin. Six hand levers have now lost today with one
of two signatures: displacement of our better crop, or denial handed back.

Addendum 08:40Z: the other half of the carrot mechanism, planting a few extra carrot
seeds on empty tiles in days 23-27 with no sell-side change, is the first hand lever in
this campaign to show the target signature on the live theta: +3.1 win pts, +247 per
board, our purse up, the opponent's untouched, dose-flat because the empty ground binds
before the knob. It is the only rule in the chain that raises total planting rather than
reallocating it. On gen-130 it is negative, because that theta already claims the late
ground; the switch ships OFF. Hold alone −248, fill alone +247: the ES learned a
development change, not a reservation.

### 2026-09-08 14:10Z — flow130 gen-260: the decay-off arm keeps climbing

| flow130 gen-260 vs LIVE | n | win | margin | t |
|---|---|---|---|---|
| band6, two bases | 384 | 51.6 → 81.0 % | +6,314 | +7.2 |
| top10 | 640 | 48.1 → 76.6 % | +7,043 | +9.8 |
| jesse4 | 128 | 60.2 → 89.1 % | +7,991 | +6.3 |
| flood6 | 96 | 59.4 → 85.4 % | +4,979 | +2.6 |
| today41 | 656 | 55.2 → 74.8 % | +6,778 | +9.9 |
| **pooled** | **1,904** | **52.6 → 78.2 %** | **+6,764** | **+16.8** |

Head to head with gen-130 on the same 2,000 boards: +3.7 win pts, +1,041 per game
(t 3.3), with band +5.7 and jesse4 +11 significant and today's losses level. Our own purse
is up 689 per game. Packaged as dist/submission_flow130_g260.tar.gz (md5 a51cd216), smoke
clean, handed over. The climb over the live build across the promoted records now reads
+8.4, +16.8, +18.3, +22.1 and +25.6 win pts.

Addendum 2026-09-08 23:25Z: flow133 (band6 plus hard-tape rungs, decay 0, from gen-260)
produced a gen-100 candidate at 52.6 → 79.3 % against LIVE (+7,069, t 16.6) that is level
with gen-260 head to head (+1.1 win pt, +259, t 0.9; flood −7 pts, top10 +1). Not
promoted; gen-260 stays the upload. flow130 was retired after three level gate losses
since gen-260 and replaced by a fresh-seed sigma 0.015 arm from the same theta. Two arms
from gen-260 now read about 79 % pooled, which suggests the current rung set is close to
its ceiling; the queued fresh-field rung (the 32 newest loss tapes) is the next change.

Addendum 2026-09-09 04:20Z: the third candidate seeded from gen-260 (flow135 gen-40, fresh
seed, sigma 0.015) also lands level with it: 52.6 → 79.0 % against LIVE, +1.0 win pt head
to head (band +5 pts, flood and jesse4 slightly down). With flow130's later records and
flow133's gen-100 all reading 79-80 % pooled, the current rung set has reached a ceiling.
gen-260 stays the upload. GPU1 switches to the fresh-field rung (the 32 newest Kaggle-loss
tapes plus band6, decay 0, from gen-260) to change what the search is measured against.

Addendum 2026-09-09 10:05Z: the fresh-field rung (band6 plus the 32 newest Kaggle-loss
tapes) produced a gen-40 record at 52.6 → 78.6 % against LIVE that is exactly level with
gen-260 head to head (+0.7 win pt, +4 per game). That makes four candidates from three
rung sets and two seeds all landing at about 79 % pooled. The ceiling is not the rung; it
is the search around gen-260 at population 512, 256 episodes and sigma 0.02. gen-260 stays
the upload. The next arm to stage doubles the episodes per candidate for a lower-noise
gradient rather than changing what the search is measured against.

## Addendum 2026-09-09 12:20Z — flow135 gen-200 edges gen-260 on the pooled margin

flow135 (flow130 recipe, sigma 0.015, weight decay 0, init gen-260) produced a gen-200 candidate after two gate losses. Six engine legs vs LIVE (1,904 paired boards): 52.6 → 80.0 % win, +8,155/game (t 19.3), own purse +2,085. Head-to-head against gen-260 on the identical boards: pooled 78.8 → 80.7 %, +1,261 (t 3.6, 270 W / 234 L), own purse +1,358; band and flood level within noise (47/53, 13/18), top10 +0.6 pt, today41 (the freshest field) 74.8 → 81.7 % (t 2.5). This is the first candidate since gen-260 whose head-to-head margin is significant; the previous four (flow130 g380–g500, flow133 g100, flow135 g40, flow134 g40) were all +0.7–1 pt and level. Sigma 0.015 with the same population therefore did buy a step past the gen-260 plateau, in line with the head-attribution note (0.02 sits at the ridge width; smaller sigma with more episodes). Package dist/submission_flow135_g200.tar.gz (md5 c34e4c22) smoke-clean and handed to the user as the recommended upload; LIVE is still flow102_g280, so the switch costs no rating restart. gen-260 (a51cd216) remains the fallback.

## Addendum 2026-09-09 13:30Z — fresh-field check and the next arms

Today's first three Kaggle losses of sub 56028553 (opponents rated 1693–1752, one earning 110k) were cut into tapes and measured paired on 96 boards: LIVE 44.8 %, gen-260 77.1 %, gen-200 77.1 % (12 wins each head-to-head). The field is not drifting past the ES lineage, so the recommendation stands. The queued arms were restaged from gen-200: flow137 (episodes 512, sigma 0.01) for GPU1 and flow136 (whole-field rung, sigma 0.015) for GPU0, each launched on the running arm's third gate loss. Rationale: every sigma-0.02 arm plateaued at ~79 %, and sigma 0.015 gave the first significant step past it, so the search-level lever is smaller sigma with a lower-noise gradient.

## Addendum 2026-09-09 16:35Z — flow135 gen-350: the largest step of the campaign

flow135 (sigma 0.015, weight decay 0, from gen-260) reached a gen-350 candidate that the remote gate accepted provisionally at +6.3 win points over gen-200. Six engine legs vs LIVE on 1,904 paired boards: 52.6 → 86.8 %, +9,095/game (t 21.4), own purse +2,515. Head-to-head on identical boards it beats gen-200 by 6.4 points (288 wins to 159, t 3.0 on margin) and gen-260 by 8.3 points (t 6.4). Every leg is up: band 85.9 %, top10 82.8 %, flood 89.1 %, jesse4 96.9 %, today41 89.5 %. Unlike gen-200, whose edge over gen-260 was denial, gen-350 also lifts our own purse on the band and flood legs (+5.7k and +7.0k vs LIVE), so the theta is producing more, not only starving the clone. Package dist/submission_flow135_g350.tar.gz (md5 ca6b3769) smoke-clean and handed to the user as the recommended upload, superseding gen-200 (c34e4c22). The plateau that four sigma-0.02 candidates sat on was a sigma artefact: at 0.015 the same rung and population keep climbing.

## Addendum 2026-09-09 20:10Z — flow137's first candidate confirms the search-level lever

flow137 (episodes 512, sigma 0.01, from gen-200) produced a gen-10 candidate that the remote gate accepted provisionally. On the 1,904 paired boards it scores 83.1 % vs LIVE and beats its own starting point gen-200 by 2.9 points (244 wins to 185), a gain the sigma-0.02 arms never managed in hundreds of generations. It is still 3.5 points behind gen-350 (156 to 226), so it is not promoted; gen-350 stays the recommended upload. Two independent lineages are now climbing: flow135 (sigma 0.015) from gen-350 and flow137 (sigma 0.01, lower-noise gradient) from gen-200.

## Addendum 2026-09-10 03:00Z — the remote gate is a nomination, not a verdict

flow138 (episodes 512, sigma 0.01, from gen-350) had its gen-10 candidate accepted by the remote gate at +6.5 win points over gen-350 on 384 boards and confirmed on a 768-board replicate. On the local 1,904-board protocol the same theta is 4.0 points below gen-350 (165 wins to 245 on identical boards), and on the gate's own two hard tapes it is 6.3 points below (12 to 18). The disagreement is not the opponent mix; the gate's 24- and 48-game reads swing by five to ten points between seed sets. The standing rule is therefore restated: a remote "confirmed record" is a nomination, and only the six-leg paired protocol promotes. The staged arms flow139 and flow140 double the gate's games (48 per read, 96 per replicate) to cut false records and the wasted re-centres they cause. gen-350 (md5 ca6b3769) remains the recommended upload.

## Addendum 2026-09-10 03:55Z — whole-field rung closed; gen-350 on the strongest field opponent

flow136 trained gen-350 on the whole field (band6 plus all 121 Kaggle-loss action tapes) and lost three gate reads in a row without producing a candidate above gen-350, so the rung breadth is not the lever; the 41-tape loss rung with sigma 0.015 remains the productive recipe and restarts from gen-350 as flow139 with a fresh seed and a doubled gate. Separately, today's strongest Kaggle opponent (Israa Saede, 134k coins) was cut and paired: LIVE wins 25 % of games against it, gen-350 wins 54 % with our own purse up 8.7k per game, so gen-350 turns a 3:1 loss into a coin flip by producing more, not only by denying.
Follow-up 2026-09-10 05:50Z: two more of today's strongest opponents (Panos at 135k, Harris Bashir rated 1830) paired on 96 boards: LIVE 34.4 %, gen-350 66.7 % (+10,948 per game, t 9.3). Against Panos the gain is our own production (+10.8k per game); against Harris Bashir it is denial (their purse −12.8k). Both mechanisms are present in one theta.
Follow-up 2026-09-10 08:10Z: flow138's gen-100 candidate (episodes 512, sigma 0.01, from gen-350) scores 85.3 % vs LIVE on the 1,904-board protocol but is level to slightly below gen-350 head-to-head (132 wins to 165, margin flat). The episodes-512 line reliably reaches gen-350's level and has not yet passed it; gen-350 remains the recommended upload.
Follow-up 2026-09-10 11:45Z: the first 2000+ rated opponent seen (kay.liechtenstein, 2035, 129.9k coins) paired on 48 boards: LIVE 47.9 %, gen-350 85.4 % (+9.0k per game, t 3.6), with our own purse up 10.2k and theirs unchanged — pure production, no denial needed. gen-350 beats the top band the same way it beats the field.

## Addendum 2026-09-10 12:35Z — gen-350 is a local optimum for the sigma-0.015 search

Two restarts of the recipe that produced gen-350 (flow135 itself after gen-350, and flow139 with a fresh seed from gen-350) each took three straight gate losses without a candidate above it, and the episodes-512 / sigma-0.01 line (flow138) reaches gen-350's level twice without passing it. The rung and population have found a point that small steps cannot leave. flow141 (sigma 0.015, episodes 384) is running as a lower-noise check, and flow142 (sigma 0.02, the wider step that failed on the earlier plateau but is now the untested direction from this one) is staged behind it. gen-350 remains the recommended upload; it beats the field at 86.8 %, kagg2 at 100 %, and the first 2035-rated opponent at 85 %.

## Addendum 2026-09-10 21:45Z — the arms were climbing the gate's field

Four gate-confirmed candidates from gen-350 (flow138 gen-10/100/200, flow141 gen-40) each read +4 to +6 points on the remote gate and each came out 2–4 points below gen-350 on the 1,904-board protocol. The shortfall is not spread evenly: it sits on the top-tier and jesse4 legs, opponents the 8-tape gate (band6 plus two hard clones) never plays, while the band legs are level. Doubling the gate's games did not change this, so it is field overfit rather than noise: the search finds thetas that beat the gate's eight opponents a little better and the wider field a little worse. The staged arms (flow142, flow143, flow144) now gate on twelve opponents, adding two top-tier tapes and the two strongest fresh tapes (Panos at 135k, kay.liechtenstein at 2035). The local six-leg protocol stays the only promotion judge. gen-350 remains the recommended upload.
Follow-up 2026-09-11 01:05Z: the strongest opponent yet (Lợi Trần Bảo, 152k coins) paired on 48 boards: LIVE 22.9 %, gen-350 83.3 % (+14.3k per game, t 7.1), our own purse up 11.2k. Against Arda Ceylan (116k) LIVE 29.2 %, gen-350 50.0 %, by denial (their purse −11.6k). Across the seven strongest tapes measured this week gen-350 lifts LIVE from roughly 30 % to roughly 70 %.

**2026-09-11 02:45Z — g350 goes live.** The user uploaded `dist/submission_flow135_g350.tar.gz` (md5 ca6b3769) as Kaggle sub 56098262. The previous live sub 56028553 (flow102_g280) ended at roughly 50 % after 355 games, rating ~1718. The local paired book for g350 says 86.8 % vs that theta on 1,904 boards, so the first 30-game streak is the number to watch: the top tier opened with 30/30.

**2026-09-11 03:45Z — the newest field, and one hole.** With g350 live, the five newest losses of the old sub were replayed paired: g350 covers four of them (pooled 36.9 → 58.1 %, t 3.9). The fifth, pupen_o (106773901, 123k, rating 1817), beats both LIVE and g350 about 3 games in 4 on 128 boards, and the margin between the two thetas is level. It is the first opponent since the 152k tape that g350 does not move. Its action tape goes into the fresh-field rung at weight 2; an autopsy of the Kaggle game follows before any hand lever is considered.

**2026-09-11 06:00Z — the current top 10, measured.** The leaderboard's top 10 (SpaTaro 2938 down to kaggricodex 2821) had no tapes in our set; all ten newest winning episodes were cut and synced. Against them g350 wins 81 % where LIVE won 66 %, and none is below 50 %. The weakest are Mengfei Li (56 %), Matthew Huang (62 %) and 自己找差距 (69 %), and Ad Space Available regressed from 94 to 75 %. Those four go into the fresh-field rung at weight 2, the rest at weight 1, and are being replicated on 96 boards each. Meanwhile the live g350 opened 24-1 at rating 2144.

**2026-09-11 07:55Z — the 2100 wall, and the fresh-field rung goes live.** g350 opened 24-1 on Kaggle and reached 2144, then lost six of eight games to opponents rated 2000 to 2210 and settled at 2098. Paired measurement on those tapes says most are still g350 wins on fresh boards (Mert 58 %, Calmracer 69 %, DOM 94 %), but Zyy7390 (42 %) and pupen_o (20 to 38 %) are real holes, and the current top 10 average only 73 to 81 %. The training rung was the 1950 to 2110 band of a week ago plus older losses; today's 2100 band is a different population. So the fresh-field rung, 63 action tapes including the current top 10 and every g350 live loss, replaced the redundant sigma-0.02 seed twin on GPU0 as flow144.

**2026-09-11 09:05Z — the live slide and the open-loop gap.** After 24-1, g350 went 3-10 against opponents rated 2000 to 2210 and settled near 2067. The replays show no fault on our side: every step active, no null actions, margins of 1 to 12k. Yet paired games against the action tapes of those very opponents give g350 about 62 %. The difference between 62 % on tapes and 23 % live is too large for board luck. The working hypothesis is that this band of the population, mostly submissions uploaded in the last day, plays reactively, and an open-loop tape of a reactive player is a ghost: it repeats what the player did against us once, not what it would do against the g350 in front of it. If so, the tape rung trains against ghosts and the local judge grades against ghosts. That is the campaign's next problem to measure, not the theta.

**2026-09-11 09:50Z — ghosts.** Three episodes each of seven opponents from the 2100 band, played against different people, were compared action by action. Their routes and hire ramps are byte-identical across opponents: clones. But their market orders are re-sized to what they hold and what the price is, and one hire decision around day 3 to 6 branches on the cash in hand and flips most of the later game. A frozen tape replays the branch the player took against us once. When our play starves that player of cash, the live player simply hires a step later; the tape's hire is refused and silently dropped, and the ghost stays a hand short for the rest of the game. That is why g350's denial reads 62 % on tapes and 23 % live. The fix under test is a sticky tape seat that carries a refused order forward until it clears.

**2026-09-11 12:10Z — not ghosts of refused orders; ghosts of the wrong town.** The sticky seat, which re-issues refused hires and purchases, made the tapes weaker and fired no hire at all, so that was not the leak. Feeding our own live observations back through the shipped package reproduced every one of 719 actions in three lost games: the live agent is exactly g350, on budget, deterministic. What remains is the board. Every Kaggle game starts from the same empty farm; the only randomness is the shop draw from day 3. The seven opponents' recorded divergences sit precisely on the shop-unlock steps. They plant for the shops they see, as the top-5 clones did a week ago. A tape of such a player, replayed on a different shop draw, farms for a town that does not exist, and beating that ghost 62 % of the time says nothing about the player. The faithful judge has to replay the tape together with its recorded town.

**2026-09-11 13:05Z — the network learns when harvests land.** The plateau review's fourth finding, that the strategic network sees crop counts but not crop timing, became eight new inputs per product: what our farm and the opponent's will have ready now and in one, three and seven days, read from public tiles only. They enter through two new weight blocks initialised to zero, so the upgraded g350 makes exactly the decisions g350 made: a golden dump of every macro decision over 2,400 observations matched byte for byte, and four engine games were coin-identical. The search now has 5,508 coordinates and, for the first time, information it never had. It runs as flow146 on GPU1 against the 63-tape fresh field, replacing the sigma-0.02 twin that produced no candidate in three hours.

**2026-09-11 14:10Z — the town was the ghost.** The tape generators now carry the recorded shop schedule, the simulator can pin a tape's town in place of its own draw, and a harness hook does the same in the real engine without touching the vendor code. Replaying our lost game against Cuong Le with the town pinned returned 88,202 to 99,339: the live coins exactly. The four band tapes that read 53 % on random towns read 0 of 192 on their recorded towns, which is what Kaggle had been telling us all afternoon. So the open-loop tapes were faithful all along; what they were replayed on was not. One consequence cuts both ways: a pinned tape is one game, with almost no board variance, so the rung and the judge must mix pinned and drawn towns, and every verdict against the 2100 band since the upload has to be re-read with that in mind.

**2026-09-11 15:40Z — training on the real towns.** The three branches (recorded towns, harvest-timing features, fair slot allocation with honest gate statistics) were merged into one tree and every rung tape was regenerated with the town it was played in. Two arms now train on a rung that is half pinned, forty-two tapes replayed on their recorded towns including every live loss of g350 and the current top ten, and half drawn, so the search sees both the exact games we lost and the board variety that keeps it general. The gate still draws towns, so it measures generality; a pinned band leg, where g350 scores zero by construction, becomes the local judge of whether a candidate has actually learned to beat the players who beat it.

### Addendum 2026-09-08 — the greedy allocator is not the wall

A reviewer showed a synthetic case where `budget.grant()`'s value-per-coin walk
picks a 6-coin item and prices out two 5-coin items worth more together. We
measured it on 1,344 real grant calls (g350 vs band6): the budget never binds
on 76 % of calls, an exact knapsack beats the greedy on 8 % (median gap 194
predicted coins, days 4-9 only, always "one more animal, fewer seeds"). A
repair switch that recovers 89 % of that gap lost 427 coins/board (t −3.1,
n 576) in the CRN sim. Predicted coins do not convert: the ES theta is priced
against the greedy's bias, and the crew ramp defers exactly the early animal
the optimum buys. Dropped; the diff is parked OFF.

### Addendum 2026-09-08 — the herd's shared fertilizer curve is not the wall

`_candidates()` prices goose, cow and sheep off one fertilizer curve, so a
day that buys two or three kinds over-values the herd's fertilizer (667 coins
on mixed days, 5 % of the herd's value; 54 % of buying days mix kinds). We
built the joint pricing as a switch (grant, read the mix, re-price the three
lists on one curve, grant again). It flips 0.8 % of grants, always the same
one: one near-worthless day-10 sheep dropped and its 500 coins left idle. CRN
sim on 1,152 boards: −3 coins/board, +0.35 pt, sign flipping between seed
bases. Dropped; the switch stays off in its worktree as a possible ES knob.
Same lesson as the allocator: the theta is priced against the planner's bias,
so a more correct valuation only moves decisions the network already
discounts.

### Addendum 2026-09-08 — where the 2000-2200 band's coins come from

A ledger built from the recorded state of 88 live losses (both seats, every
day, residual 0.5 % of gross flow) ranks the opponents' lead: the day-0 melon
block dumped on day 10 (+14.1k on day 10 alone; in 69 of 88 games that one
swing exceeds the final margin), daily fertilizer collection (+7.0k on an
equal herd), daily milk care (+5.1k), and board fill (+3.5k; we leave 9 unlocked
tiles empty from day 10 on, they leave 0.6). We win the egg, tomato and carrot
pots, but they are worth 5.9k together. Neither seat reacts to shop unlocks;
we are marginally the more town-adaptive one. Their edge is a fixed,
better-timed build. The 41k game was a thin town with no buyer for
strawberry, melon or wool: nothing sat unsold, we simply realised 17k under
list on 181 units nobody wanted, a 2 % tail. The study's prescription for
training: a price-walk feature for the shared melon pot, a fitness term that
rewards cash at day 10, and a rung whose opponents take the pot on day 10
with a price-reactive seat.

### Addendum 2026-09-08 — the admission shrink is not the wall either

Over 2,880 planned days the shrink fires on 21 %, dropping 24 tiles of
low-value work per game; routing the un-shrunk set instead loses 2,224 coins
a game, so the shrink earns its keep. An insertion-and-exchange oracle over
the planner's own values recovers 429 value units a game, 0.08 % of what the
route already completes. Dropped. The census did find where the pasture
coins go: fertilizer is collected in full but 186 units a game are applied
to crops instead of sold, and CARE (96 animal-days a game) and FEED (76) are
never ranked because their pay tests read the spot quote, while 83 % of our
PASS turns fall on days with nothing queued. That pairing of idle capacity
and unranked paying work is the next lever to measure.

### Addendum 2026-09-08 — hour-0 commitment refuted; the melon lot is a planting-date problem

Instrumenting every market order in 128 engine games (96 drawn, 32 on
recorded towns) found no refused BUY or HIRE row and no SELL row the shed
could not fill before day 29. The only coins at stake are sell prices that
moved after hour 0, all of it opponent supply in the same product the same
day, and 40 % of that lands in the same turn as ours where no revisit can see
it. The minimal revisit, shrinking a lot to the units still clearing the
hour-0 quote, lost 4,964 coins a game with the denial signature (their purse
up 2,015). Dropped, and section 5 of the plateau diagnosis with it. The melon
ledger settles where the day-10 pot goes instead: on days 9 to 12 we harvest
nothing because nothing is ready, our first melon sale is day 18.5, and from
day 17 every harvest rides home in the hands, is dropped at the end of the
day, and sells in the next day's lot while our own quote slides from 221 to
141. Their edge is the date and size of one lot, decided at planting.

### Addendum 2026-09-08 — the global head could not see the products

The one review finding that survived measurement: the global head that sets
development fraction, animal share and crew targets reads only aggregate
market summaries. On 1,440 real decisions the best linear map from those
summaries leaves 53 % of the animal-versus-crop grow contrast unexplained
(wool grow R² 0.18), and among states whose global summaries agree to four
decimals, 18 % disagree on the best product to plant while the head emits
identical outputs. We added a zero-initialised 27×32 block that feeds the
nine product scores and press values into the global hidden layer. The
padded champion plays byte-identically over 48 engine games, and at sigma
0.015 the new block is 1.9× more decision-active than the existing global
weights, so ES can see it. flow149 trains only that block on the pinned-town
rung from the champion.

### Addendum 2026-09-08 — care and feed admission: the planner was right

Ranking the care and feed tasks the planner refuses lost 1,562 coins a board
on 576 CRN boards (t −21), all from our own purse. A care is worth one extra
unit at the next fire and only if the animal is fed; a feed costs one wheat;
by mid-season a cow's extra milk sells for 34 against wheat at 57. The pay
test on the spot quote is the only term refusing the work, and it is
correct. The opponents' extra 49 milk a game comes from cheap wheat, not
admission: they hold 23 wheat tiles at day 19 to our 11. The question moves
to why we leave nine unlocked tiles empty from day 10 on.

### Addendum 2026-09-08 — the empty tiles are the network's choice

On 2,880 planned days the board offers 13 free slots a day from day 10 and
the development head asks for six; the planner grants all six with a
five-figure purse unspent, and no purse, seed-cap, value or route term
refuses anything. Pushing that head one logit up (development fraction
0.50 to 0.71) with no planner change loses 15,277 coins a game at t −48 on
576 CRN boards, the same verdict the two PLANT_FILL switches reached from the
other side. The evolution strategy has walked this head from 0.50 to 0.80
across the lineage and stopped where it pays. The field-fill archetype is a
joint move, tiles with the hands to work them, and only training can take
it. Three studies today end at the same door: the day-10 melon lot, the
milk cadence, and the field fill are each a build decided at planting and
paid for by a larger crew, and each loses when changed alone.

### Addendum 2026-09-08 — reaching the day-10 pot is possible and does not pay

A generalised same-day excursion (harvest, deposit before the last lot, a
row for the deposit) lifts melon sold on its harvest day from 2.5 % to
55.8 % and ends the overflow. The engine charges 4,186 coins a game for it
(t −13, win rate 86.5 to 74.0), and stacking the day-0 melon opening on top
costs 19,190, worse than the opening alone. Melon's own ledger barely moves
because nothing contests the pot between our rows; the bill is the
excursion's turns taken from the day's other harvests. That is the third
form of the same lesson today: the pot, the milk and the tiles are all
bought with a crew the network has not learned to hire, and every one of
them loses when a hand lever takes it alone.

### Addendum 2026-09-08 — what the top ten actually play

A ledger over 30 recorded games of the top-10 players shows the same
opening as the 2100 band: the wheat pump we already ship, 10.7 melon seeds
at day 0, 11 hands by day 10. The difference is the second half. They are
level or behind their opponent at day 10 and win days 15 to 29 on realised
price, not volume: carrot 28 coins a unit dearer, milk 17, wool 14,
strawberry 14, sold through twice our number of rows in half-size slices,
with a wheat book they keep thin by buying and selling wheat at a wash. They
plant carrot only after a pet cafe unlocks and hold it to day 25. Crew is not
what separates them from the band; it is what separates us from everyone.
So the training signal needs two parts: the day-0 crew and melon plant to
catch the band, and late-season price per unit to beat the top, and a
day-10 coin lead on its own must never be the objective.

### Addendum 2026-09-08 — sell cadence is nothing; the day-4 carrot is something

The market has no time recovery: price is a function of inventory alone,
and the town drains after each market phase, so 30 carrot sold as one row or
twenty-four realise within 0.8 % of each other. The top ten's extra rows
buy nothing. What their ledger does show is carrot held to days 25 to 29 by
91 to 98 % of every strong cohort, sold at 85 a unit, where we sell 27
carrot on day 4 at 33 with the shed 40 % full, pushing the shared pot below
base until day 13. Carrot is the one product whose curve ends the season at
2.3 times base, so it is the one product worth holding, and the one the
uniform hold head cannot reach. The net is small, about a thousand coins a
game after the opponent's own carrot rises with the pot, and it is under
test as a narrow switch on the day-4 lot.

### Addendum 2026-09-08 — the carrot hold

Holding the day-4 carrot to day 25 loses 8,803 coins a game in the engine
(t −6.6, win rate 92 to 63) and 8,637 a board in the sim, eight times the
lever's own upper bound. The held carrot fills the shed by day 13 and the
overflow rule sells it at 40 on days 14 to 24, the worst moment available;
the crew is unchanged and the hour-0 purse on day 5 falls from 1,485 to
601. Against the open-loop tapes the opponent's purse rises 6,204, which
says our day-4 dump has been a denial weapon all along. Closed.

## Addendum 2026-09-09 — why the forced top opening loses (the ramp, not the board)

Forcing the band's opening onto our planner (`MELON_OPEN_ON`, crew ramp, `PLANT_FILL_ON`) drops the band6 win rate from 94 % to 22-26 %. The day-0 board is reproduced (19 tiles, 12 melon, 4 hires, pump). The break is day 1: we hire zero hands, the top hires four. Not cash — we wake with 222 coins against their 40. Hire enumeration in `plan.py` scores hands against today's derived task set, and a melon tile emits no task until `CROP_WINDOW_START` (day 6), so 12 of 19 tiles carry no labour demand for six days. The crew collapses to 0-1, the herd freezes at 4 while theirs doubles by day 8. On day 10 the forced build out-harvests the band (81 units vs 57) but sells at 145 per unit against 243 because our first lot stands at hour 11 and theirs at hour 9, and melon has no shop demand so the pot is not shareable. Season melon changes by +326 only. Verdict: no fitness term reaches this; the planner must admit projected d+1..d+k tasks when pricing hands and animals. Build launched under `FORWARD_ADMIT_ON`. Data in scratchpad `forced/`.

## Addendum 2026-09-09 — projected task admission fires but loses as a hand lever

`FORWARD_ADMIT_ON` (hire enumeration sees the water/harvest tasks the standing board will emit within three days; commit 3792b8e in the agent worktree) lifts the forced melon opening's crew from 0/1/1 hands on days 1/3/5 to 2/3/3, still short of the top's 4 on day 1. It loses paired in the engine: alone 94 to 65 %, with the melon opening 15 %, and against the melon opening alone the loss is entirely the opponent's gain with our purse level. The extra hands have no route work until the melon window opens, so they pass. The top's ramp is hands, animals, and tiles bought together; the animal budget and the plant cap do not see the projection. The horizon becomes a theta gene next, zero-initialised, so ES can move it jointly with hire bias and development fraction from the live theta without a gen-0 hole.

## Addendum 2026-09-09 — the melon opening costs denial, not income

`SEED_DEFER_ON` (long-window seed ranked behind the herd on day 0, commit 175aa9e in the agent worktree) recovers every coin of our own purse that the forced melon opening loses, yet the arm still trails the base by 14,772 because the opponent's purse rises by 14,670. Withdrawing our wheat, strawberry, and wool supply from the shared markets lifts the opponent's realised prices by more than the melon pot earns us. The shipped build's edge over the old band is largely that flooding. Seed deferral ships off as a companion knob for a melon-capable arm. Same day: pinned-town tapes were shown to replay the live game to the coin, giving a deterministic loss-flip judge; flow148's records flip their own training tapes and nothing else, so the queued arms gate on 72 held-out pinned tapes.

## Addendum 2026-09-09 — the live-replica judge and the day-9 gap

The most useful discovery today was that a pinned-town tape is not a sample of the live game but the live game itself. Replayed against the eight tapes of the losing streak at six seeds and two seats, g350 won none of the 96 games and reproduced every Kaggle score to the coin: Bill Fan 92,041 against 102,981. The board carries no randomness of its own: the seed lottery was always the end-of-day shop draw, which `--with-town` pins. That turned the loss archive into a judge, `S/lossflip`, reporting which live losses a candidate flips. Baseline g350 won 34.5 % of the 116 pinned boards and never split a seat, making the flip target a fixed list of 76 games. The fallbacks chained to 31.2 % for g200 and 28.4 % for g260, the ordering the drawn legs read.

Its first verdict was about itself. flow148's pending record read 42.3 % against g350's 34.2 % with 30 flips and 11 drops, and almost every flip landed on a tape in its own training rung. On the 72 boards it had never trained on it fell from 56.7 to 51.5 %, 4 flips against 11 drops; the six drawn legs and the remote gate agreed. A pinned rung is memorisable. The gate therefore moved to held-out pinned boards, one seat per board since both seats give identical coins once the town is pinned, and the training rung widened to 86 pinned tapes plus 45 drawn ones, every third pinned id reserved for the gate.

A flip could still be an artefact of replaying a recorded opponent, so the market was instrumented. Across the seven held-out flips of flow149's first candidate the opponent's committed and refused order streams were byte-identical to the base game, its refusals pre-existing, and the flip margin of 19,380 coins was 17,473 ours against 1,907 theirs — ninety per cent earned in our own purse. The flips are real.

The day's builds went into the trainer: three fitness terms landed inert by default, day-10 cash, tiles filled from day 10 to 25, and realised unit price from day 15 to 29, the first and third pulling opposite ways and never to share an arm. The forward-admit horizon became a zero-initialised gene reading zero days, so generation 0 stays byte-identical to g350; twelve forward-value features entered the global head as another zero block, taking the vector to 6,789 parameters, and the packager was verified on that layout to the coin.

Three studies asked who is beating us: the current ladder, 53 of 54 tapes recorded since the seventh, playing our own build — hands 3.8, 5.0 and 11 at days 1, 3 and 10, eight cows, the same crop counts within 0.3 of a unit. Their late milk and wool prices look better, 153 a unit against 109 and 128 against 55, but conditioning on shop counts kills that gap outright, and nobody holds inventory for an unlock. What survived is a one-day lag: lots are sized at dawn from the hour-0 shed while collections land at day's end, so every animal product sells a day after it appears, one rung down a ladder that only falls, about 600 coins a game pooled. Every lever aimed at it failed. Early milk was a no-op in its milk half and a herd ramp in its other, and two cows on days 0 to 4 displace the pump opening, 34.5 to 29.7 % on the pinned judge. Holding wool for a store overflowed the shed and dumped it at the floor for 200 coins of upside. Over-asking the last lot by the day's projected collection was correct and inert: the shear-day collections land after turn 18. A price-aware lot after the last collection is the remaining shape.

The live submission gave back its streak, falling from 2031 to 1998 at 61 wins and 60 losses, every loss cut into the pinned set, now 129 tapes and the judge's whole basis. flow149, whose single candidate three local judges rejected, is a strict subset of the queued gene arm and will be replaced by flow151 at its next gate verdict, whatever it says.

## Addendum 2026-09-09 — drawn towns, dead genes, and the first held-out gain

The judge changed again, and invalidated most of the arithmetic behind it. Ten top-ten tapes recorded in the last day, games we had never played and so free of selection bias, were replayed both ways: with the town drawn at random g350 won 81 % of them pooled, and with the live town pinned it won two of ten. Over the whole recent pinned set of 54 tapes, it won one. A tape records what an opponent did, and what they did was sell into the shops their own board offered. Draw a new town and their milk goes to a market with no milk shop and their wool to one with no yarn store, cutting their late wool from 24.1k to 12.9k and lifting our own late strawberry and milk by 19.3k. Every drawn-town figure was that illusion: 82 to 94 % on band6 against roughly 50 % live. The held-out pinned set became the judge outright, the drawn legs a secondary town-generalisation read; the remote gates switched to pinned held-out boards, and both arms still gating on drawn opponents were replaced on the spot rather than waiting out their three losses.

With the towns pinned the top ten's ledger reads like the band's. The gap opens on day 10 in seven of eight losses: day 9 stands 1.9k in our favour, day 10 turns 9.7k against, the peak is 19.5k on day 16 and the end 14.4k. It is the melon dump. They plant 8.2 melon seeds on day 0, hold twelve tiles by day 9, and sell 72 units on days 10 to 12 at about 242. We buy our first seed on day 3, reach twelve tiles on day 12, and sell the same 72 units on days 20 to 29 at 125. Of the 19.1k day-10-to-19 gap, 12.7k is pure timing, the same volume at half the price, because melon has no shop buyer and only the first dumper is paid. Taking it by hand was catastrophic: the melon opening at twelve tiles took 130 pinned tapes from 30.8 % to 1.9 %, one flip against 76 drops. Crew starvation on days 1 to 9 and denial handed back swamp the pot on live towns as on drawn ones. The family is closed; the day-10 pot is an evolution target, not a lever.

The trainer's own signal was checked next. The action-seat sim run against the engine on twelve pinned tapes agreed on all twelve outcomes and was coin-exact on both seats in six, with a median margin error of 31. All 131 pinned towns matched the engine's schedule, and the first coin lost is the tape seat's own replay leaking a refused action on day 9, not the town pin. In-sim fitness on pinned rungs is engine-faithful.

The same-day-sale family closed with two more builds. A price-aware lot at turn 22, sized on the projected shed, asked for 4,846 units and sold zero, its wool and milk ledgers byte-identical to the base. Routing the collecting unit to the shed before that lot flipped sixteen pinned boards against five, but the ledgers stayed byte-identical and the late row still sold nothing; the flips were route displacement, and drawn band6 fell 1,441. A collection enters the unit's own inventory and reaches the shed a sell can draw on only at end of day. Four builds, and the family is shut.

Two defects in the evolution signal surfaced the same evening. The forward-admit gene, appended zero-initialised so generation 0 stayed byte-identical, decoded through a squashed offset, and at the training sigma not one of 512 members decoded a single day on 200 real boards; flow151 had trained it dead for 45 generations. Re-parametrised as a plain scaled round it still holds zero at the init and puts 24.8 % of members at a day or more. Every appended gene needs a slope check at its training sigma before launch. Alongside it, pinned-once allocation gave each town-carrying rung one episode per candidate per generation, worth about 2.4 times the generations an hour, and the checkpoint guard, keyed on the in-sim best and so never writing the record under a pinned gate, was fixed. All three merged into one tree and both arms restarted on it at 160 episodes.

Between those restarts the campaign took its first honest gain: flow150, the control arm with the gene frozen, presented its generation-40 record to the held-out pinned gate and won 12 of 42 live boards against the incumbent's 9. Ten generations on, a periodic candidate at 11 was refused and the trainer re-centred on the record. The live submission ended the day at 67 wins and 64 losses, rating 2006, with 133 pinned schedules — every loss cut into the set that is now the only judge we trust.


## 2026-09-09 — the lottery day

Sources: `docs/strategy/2026-09-09-verdicts.txt` (the day's one-line log),
`2026-09-09-plateau-review-verdicts.md` §0–21, and the thirteen dated studies beside them,
from `2026-09-09-judge-calibration.md` to `2026-09-09-animal-first.md`.

### Where the day started

Live was submission 56098262, theta `flow135_g350`: 78 W / 72 L, rating 2010 at 07:24Z;
82 W / 83 L, **1979.5, rank 1188** by 10:25Z after peaking near 2144. Eleven losses were cut
into tapes, all against 1830–2070 opponents. The band wall again.

Both arms sat at the noise floor, numerically: at gen 90 the per-parameter rms of θ − g350
is 0.028–0.034 in *every* block and the Adam snr is **0.17–0.19 against a pure-noise
expectation of 0.23** (plateau-review §0). The forward-admit gene was worse than undirected
— centre z = −0.196 ± 0.106, **0 days on 2400/2400 boards** — so `gb11` was re-centred to
+0.028, which holds the centre at zero days but puts ≈44 % of sigma-0.02 members at ≥1 day;
flow156 and flow152 restarted on it at sigma 0.02 and 0.03.

Six claims from the 2026-09-08 plateau diagnosis came back from time-boxed reviewers and
**none was binding**: our orders are refused 3.96 times a game, 0.07 % of acting turns and
**0 of 1,971 BUY rows**, so the intraday re-plan hook has nothing to react to; the router
already completes 99.8 % of queued value; the forecast features were in and inert. One
residual was worth an arm — **one training tape rates ≥2200**, all 20 top-ten tapes are
gate-only, and every held-out board any candidate ever bought was against a sub-1900
opponent.

### The judge was a lottery

The first crack was the block ablation: reset a candidate's new blocks to g350 and it still
reads +4/−0 on the held-out 42; keep *only* the new-block delta and it reads +4/−0 again.

Then flow156_g20 cleared the +6 bar — held-out 21.4 → 28.6 %, **six flips, no drops** — and
all six drawn legs came back down (top10 −5.1, jesse4 96.9 → 85.9, today41 89.5 → 80.8).
Not promoted.

The calibration study explains both. Across 24 near-neighbour arms **every flip and every
drop lands in the same 15 of 42 boards**; the other 27 never change hands. Net flips has
mean +2.8 and **sd 3.1**, so "+6" is one standard deviation of a lottery. Of the seven arms
with both reads, **all seven lost the legs** (−2.7 to −9.1 pts over 1,808 games); the rule
fired on four and all four lost — **zero true positives**. The best ordering statistic was
not on the held-out set at all: the paired Δ margin over the 20 pinned games against the ten
tapes the drawn legs also play (ρ 0.64–0.75). That is LEG20, wired into
`S/lossflip/leg_family.py`, with `judge.sh` paying for legs only if `LEG20 > 0 && H_dm ≥ 0`.
flow156_g20 read LEG20 −1,243: the signature was there before the legs were bought.

At 09:06Z the user asked for the general case — scan the code for lottery sites instead of
measured facts. The 494-line audit ranked fourteen; the worst four:

| rank | site | threshold vs noise |
|---|---|---|
| 1 | `--real-gate-recentre 1` (`train.py:2310-2323`) | one 24-game refusal, ~50 % under the null — the only site where noise **steers θ** |
| 2 | `S/bank/paired.py:26-28`, paired t over rows | seats are near-duplicates → **every published t inflated 1.40×** |
| 3 | net flips (`train.py:2791`, `judge.sh:15-19`) | sd 3.1, 0 true positives in 4 fires |
| 4 | `_accept_best --best-margin 0.005` | 0.14 SE — the promoted record is the luckiest of ~3,000 readings |

Below them: gate power (MDE ≈ +10 win pts), band6 and jesse4 as accept legs (MDE 4.0–4.6k),
and — thirteenth — **LEG20 itself**, a zero-threshold sign test with SE ≈ 1,340 fitted at
n = 7 with no positive control. Four fixes landed within the hour: re-centre 3 with a gate
every 100; `paired.py` seat-grouped (grouped t = t_rows / 1.40, turning flow156_g20's top10
−4.05 into −2.90); `judge.sh` reading the *last* LEG20 line instead of silently rejecting;
`--best-margin 0.04` queued. Re-reading 48 verdict lines decided on 1.7 ≤ |t| < 3.0 changed
**no decision** — but the crew-ramp rejection has no supporting statistic left and should
read "not measured", and every t logged before today divides by 1.40: **a logged 2.8 is the
new 2.0**.

### What the planner ledger actually says

Four premises carried over from the loss ledger. Measuring them inverted three, and the
fourth had the wrong sign.

| ledger premise | what the measurement says |
|---|---|
| we pass while animals go uncared | per-animal output is level (1.13 vs 1.24 d10–19); their +57 units a game are +49.6 care-bonus units funded by a wheat rotation, 532 crop-days to our 257 |
| units run out of wheat to feed | FEED emitted equals fed_today exactly (254.2); the cut is 13.3 animal-days rationed at the budget grant |
| we plant fewer tiles than the clone | **inverted**: at d10 we plant 44.5 to their 33.1 on 40 of 42 boards; 99.4 % of 647 idle tile-days are the dev cap `floor(dev_frac · n_free)` (`brain.py:921`) |
| the herd is starved from day 1 | **inverted**: we lead 6–4 on d1–4, fall behind d6–10, freeze at d12; the +12k line is 1.9× too high at **+6,372/game, 72 % after d12** |

Fertilizer had the wrong sign. Our 179 applications net **+16,815/game**, the clone's 79 net
+12,444, nothing negative. The "−4.1k" is an income-line artefact: they *sell* 15.1k of
fertilizer to our 10.0k because they burn 79 where we burn 179, so we are +4,404 ahead on
the trade. Dropping our 86 wheat applications gains 3,098 and loses 7,184 as the wheat quote
climbs 28 → 43. Closed.

The day's six Kaggle losses reproduce **byte-exact in both seats**, and 148 of 168 pinned
tapes are one clone. Universal in 6/6: the d10 melon dump, d10 cash 2.2–3.7k against 15–18k,
PASS 15–17 % against 6–10 %. The −22.2k outlier was milk — 129 units against 239 at the same
191/u, four cows against eight, after a day-3 YARN_STORE pulled our mix to 12 sheep on a
board that later opened five milk sinks. That sharpened pasture into **herd composition**,
decided at `brain.py:999-1008` from today's shops alone: we follow the last unlock a day
late on 6/6 boards while the clone is open-loop cow-first. Matching their cow share prices
at +2,227 a game — as denial (ours −6,469, theirs −14,012 on the worst board).

### The levers, and what the pinned judge did to them

| lever | pinned held-out (42 boards, base 9/42) | verdict |
|---|---|---|
| `SELL_CADENCE_ON`, 6 / 4 rows | +0/−0, d-margin −324 / −348 | closed |
| melon block, 4 / 6 tiles | 21.4 → 9.5 % (+0/−10) / 6.0 % (+0/−13) | closed |
| `PLANT_MIX_DRAIN_ON` 0.5 / 1.0 / 2.0 | −2,458 / −6,243 / −9,198 | dose-responsive loss |
| `CARE_FILL_ON`, +`CARE_HOLD_ON` | +0/−0 (LEG20 +46); +2/−0 (LEG20 −277) | off |
| `FEED_RESERVE_ON` | engine −2,666 us / +812 them | off |
| `CARE_WITH_FEED` | +2/−0, H_dm −24, **LEG20 −258** | level in the lottery band |
| `PLANT_FILL_LATE_ON` | 21.4 → 9.5 % (+0/−10, LEG20 −6,551) | board-fill family closed |

Three more are built, OFF and byte-identical, queued behind the probe chain:
`ANIMAL_RESTOCK_ON` (planner animals 88 → 122, PASS −52), `ANIMAL_MIX_DRAIN_ON` and
`ANIMAL_FIRST` (animals 88 → 126, **seeds −153, PASS +419**), the last showing its
displacement in the planner's own A/B before an engine game is played. Sell cadence is the
cleanest null: market rows do not consume unit-turns (`spec.py:216,234-240`), so the clone's
8–10 sell rows across 7–8 hours were free to copy — and copying them moved nothing. Their
edge is which products they sell, not when.

### The arms

flow156 accepted one record at g20 then lost g55/g84/g105. flow152 at sigma 0.03 walked its
centre to a 1.28-day forward horizon — in-sim mean_win 0.17 against flow156's 0.45 at the
same generation — into the region hand probes had shown loses (`FORWARD_ADMIT_ON`
94 → 65 %), and lost g10/g50/g100. flow158, the top-ten-tapes-in-training arm, rejected
g10/g20/g40. flow159 and flow160 died to the audit and came back as flow162/flow163 with the
fixed flags; flow162 was killed after one loss to free GPU0 for **flow164**, the flow161
recipe with the shaping terms off, since tile-fill rewards exactly the idle-land planting
`PLANT_FILL_LATE` had just lost 6k with.

That leaves **flow161**, whose gate is the day's finding: `--real-gate-metric leg20`
(worktree `gate-leg20` 8b535ec, 51 tests) accepts only if the paired Δ margin over the 20
family games is positive and the all-games delta is not negative, flips demoted to a screen.
Never taken on a real round before today, it refused three records in a row. The second is
the one to keep: at gen 20 its wins went **30 → 34 (+6/−2), which the old rule would have
accepted**, while leg20 read −44,888 over 20 games and all-games −205,442 over 98. Three
records running leg20-negative by 2.2–2.8k a game say the in-sim objective is pulling away
from the leg family — now its own diagnosis stream.

### What this day adds to the standing rules

* **A held-out flip is not a signal**: fifteen boards carry every flip, sd 3.1, zero true
  positives in four fires. Require the leg-family margin first.
* **An income-line delta on an input is not a loss.** "Fertilizer −4.1k" was us +4,404 ahead
  on the trade.
* **Hand levers on structure lose by displacement**, and the planner A/B says so before the
  engine does: seeds −153, PASS +419 is the whole verdict on `ANIMAL_FIRST`.
* **Measure before theorising.** Four ledger premises: three inverted, one changed sign.
* **Price the statistic before acting on it.** Every earlier t divides by 1.40.

### Open at end of day

* flow161 (leg20 gate, re-centred once) and flow164 (unshaped) on the GPUs; flow165 queued.
* Probe chain to report: restock closed inert at 13:35Z (+0/−0, LEG20 0) → animal-mix drain → animal-first still to read.
* The judge-calibration chain over the 13 arms with legs but no pinned read — the only route
  to a positive control, and why the LEG20 rule is provisional.
* The sim-vs-leg20 divergence diagnosis: why in-sim records are leg20-negative.
* Unfixed: the `S/knobsweep` / `S/rescreen` comparator is likely inflated by the same 1.40×.
* Live: 82 W / 83 L, 1979.5, rank 1188 — the band wall, top-10 target 14 days out.

## 2026-09-09, second half — the population fix

Sources: `docs/strategy/2026-09-09-verdicts.txt` from 10:46Z on,
`2026-09-09-plateau-review-verdicts.md` §22–31, and the ten dated studies beside them.

### Four planner verdicts

Pasture timing got its cause and its price. The planner replays the recorded `BUY_ANIMAL` orders
exactly on 90 of 90 our-seat day states: on 4 of the 15 trailing mornings the purse held the
cheapest wanted animal and `budget.grant` ranked seed above it. The ledger line was re-priced from
+12k to **+6.4k a game, 72 % of it after day 12**. Herd composition asked which animal:
cow-versus-sheep value is board-specific, but revenue per animal-day tracks the *season* sink
(+0.98 wool, +0.89 milk), while the only sink-shaped column the mix softmax reads is *today's*
demand. `ANIMAL_MIX_DRAIN_ON` read +4/−0, LEG20 +335 at gain 1.0 — the **first knob all day to
clear the LEG20 > 0, H_dm ≥ 0 rule**, though +17 a game against an SE of 1,340; its first drawn
leg read 82.8 → 82.5 %, t 1.42.

Fertilizer's "−4.1k" is an income-line artifact: our 179 applications net
**+16,815 a game** to the clone's 79 at +12,444, and dropping the 86 wheat ones loses 4.1k
as the wheat quote climbs 28 → 43. `ANIMAL_FIRST_ON`, the direct fix for the pasture finding,
collapsed the season: **21.4 → 0.0 % (+0/−18), H_dm −52,957, LEG20 −56,864** — the −153 tiles and
+419 PASS its planner A/B had priced before an engine game was played. Grant-order family closed.

### The population was the bug

Why every in-sim record read negative through the leg20 gate was not the sim. flow161's rungs were
106 town-pinned tapes and 15 open-loop ones; the gate plays 49 pinned tapes, only 22 of them
rungs, and the only weighted rungs it played were the 13 open-loop ones. **94 % of the training
weight sat on boards the gate never plays**; the 42 non-family gate tapes carried 5.6 %, the 10
judged tapes zero. On the same theta and tape, town-pinned rungs err 58–85 coins with perfect sign
agreement; open-loop rungs err 14–15k, **+12k optimistic, sign right 47–60 % of the time**. The
sim reported the family loss; the fitness did not count it.

Weighted in-sim margin improved −5,850 → −3,271 over generations 10–50, 94 % of it on
gate-invisible rungs, while in the engine at gen 40 every set read −0.7k to −2.4k a board:
**no set improved**. A pinned-town sim screen
settled it without an engine leg: over 92 CRN boards the gen-59 theta is **−2,202 a board (t
−5.42) worse than its init**.

flow166 is that diagnosis as four edits: repoint the 15 open-loop rungs at their
`tape_actions_town` twins, add the 27 gate tapes that were no rung, raise all 38 non-family gate
tapes to weight 2 (5.6 % → 36 % of the weight), drop a byte-identical duplicate. The family stays
at weight 0, which — `AbsReport` being rung-weighted — keeps it out of record nomination as well
as training. flow164, the same recipe on the old population, refused three gates and was killed,
freeing a GPU for **flow167** at sigma 0.015.

### The first records under the leg-family rule

flow166 refused three gates of its own and re-centred, its all-games delta turning positive at gen
30 — the first of the day. Four candidates followed in ninety minutes:

| candidate | remote gate (leg20, all-games) | local pinned | LOSS12 (engine) | verdict |
|---|---|---|---|---|
| flow166 g50 (σ 0.02) | +203, +733/game; wins 28→36 | 21.4→35.7 % (+12/−0), family +208 | 4/24, **+722/game** | accepted |
| flow166 g80 | +454, +434/game | — | 4/24, **−509/game** | accepted |
| flow167 g60 (σ 0.015) | +210, **+1,765**/game; wins 28→34 | — | 4/24, **+676/game** | accepted |
| flow166 g130 | −543, +1,129/game; wins 32→40 | — | 4/24, **+1,381/game** | refused |

Two arms at different sigmas each turned 4 of 24 never-trained games at about +0.7k: the fix
generalises off its boards. The ordering is not the gate's, though: g80 beat g50 on the family but
reads 1.2k a game *behind* it on the fresh losses, and g130, refused on the family rule alone,
posted the day's best fresh-loss read. The g50 anatomy argues against it: the record is **one
fixed day-0 change on all 44 boards** — one wheat tile to carrot, one sheep to cow — plus sheep
6.2 → 5.3 from day 10, hires and sell rows identical. Priced at the day's quotes — wool −5,768,
milk +2,640, carrot +1,369 — **our own ordered value is −3,963 a game**, two-purse ours −1,925,
theirs −2,137, carried by 3 of 10 boards at t +0.25 — denial with our purse down.

### The fresh-loss leg, and what it exposed in the sim

flow166 trains on all 42 held-out gate tapes, so that line stopped being held out the moment it
launched. **LOSS12** replaced it: twelve pinned-town tapes cut from today's live losses, verified
absent from every launch script and from the leg family, 10 of the 12 exact to the coin against
their Kaggle replay. The live theta loses all 24 at −8,106 a game, so a flip is a gain on a board
no arm has seen.

The sim disagreed with it: +722 a game in the engine, +6 in the sim. Four tapes miss by 6.5–7.5k
with the tape seat's purse 2.8–5.9k low; eight are within 100 coins. The cause is a **sim bug**:
`sim/units.py` resolves every PICKUP against the hour-start shed before any DROP into it, while
the engine walks `[farmer, *hands]` in index order with immediate mutation. On a same-turn
hand-off — unit 5 DROPs a cow, unit 6 PICKUPs it — the sim's pickup finds an empty shed and the
animal is stranded for the season. One cow is 22 days of milk: on 107089992 the divergence starts
day 7 hour 11 and ends with the tape's purse −4,785 and ours +2,496. The four bad tapes have three
*animal* hand-offs each, the clean ones none, and our planner never hand-offs within a turn —
which is why the family tapes were always exact. The sim's LOSS12 column is withdrawn, the engine
leg is the judge, and a per-unit scan of the shed stage is being built: freshly cut tapes feed the
training schedule.

### A sim harness, and the first switch it found

`S/simprobe/run.sh` runs a planner knob on the engine's exact pinned boards — 122 of them, both
seats — at ~10–13 minutes an arm, four at once, and it reproduces two engine reads (`CARE_FILL`
+64 against +54, the drain tilt −6,109 against −6,243), flips on the same boards, worst gap 134
coins.

All 29 shipped-OFF switches were classified and the unmeasured ones screened. One pair survived:
`TAIL_FILL_ON` at held-out +775 (t 3.3) and family +1,366 (t 2.6), with `BANK_BEFORE_LOT_ON`
adding +165/+209 and no interference. The engine confirmed TAIL_FILL at
**+2/−0, H_dm +748, LEG20 +1,365 a game**, within 30 coins of the sim. The rest lost or were
inert: `SAME_DAY_FERT` −30.7k, `OPEN_DENY` −30k, `ANIMAL_DEFER` −40.7k, `FORWARD_ADMIT` −6.4k
(reproducing the 94 → 65 % hand probe), `OPP_MIX` and `SHED_OVERFLOW` inert. `ROUTE_EARLY_ON` read
−159k to −165k on every set — a broken switch, not a strategy verdict. `ENDGAME_TOMATO_SHOPS=1`
closed the hand tomato family again: 21.4 → 11.9 %, LEG20 −13,301.

### The drain-mix gene

The census behind it: **14 of the 20 top-ten tapes open exactly like the 2000-band clone**, and
after a control for opponent supply their surviving edge is late shop-adaptive mix — tomato with a
tomato sink +3.8k, carrot +3.7k, geese with egg sinks +2.8k. Every hand lever on that mix has
lost, so the constant becomes a parameter: blocks `gd` (32 × 8) and `gbd` (8) take `N_PARAMS`
6,789 → 7,053, decoding as `clip(5 · mixd · drain_share, ±3)` into the herd softmax and both plant
branches — one coefficient per product, off the global hidden layer. Byte-identical at zero-init,
change-fraction 24.4 % at sigma 0.02 — inside the gene rule's band. flow168 is staged on it, the
ten family tapes moved *into* training at w2 and the engine gate's held-out set becoming the
twelve fresh loss tapes; flow169 is queued at `--abs-weight 0.5`, because the first accepted
record was denial with our own purse down.

### Open at end of day

* flow166 (record g80, σ 0.02) and flow167 (record g60, σ 0.015) on the GPUs; flow168 deploys
  once the sim shed fix lands; flow169 queued.
* Judge queue, serial: g50's drawn legs (band6 86.5 → 83.3 %, level), then g80, g60, g130, then
  the herd-mix and TAIL_FILL legs; promotion needs top10 + today41 pooled positive at grouped
  |t| ≥ 2.
* Unfixed: the sim shed stage, the four tapes it mis-replays, LOSS12's seed index, eight
  unscreened switches.
* The family-strict rule now refuses candidates level on the family and up everywhere else
  (g130). Promotion authority stays local; the remote gate only nominates.
* Live: 83 W / 87 L, **48.8 %, rating 1966**; eighteen losses cut today, the first twelve
  reserved as the judge leg.

## 2026-09-10 — the live set and the first hand-over

Sources: `docs/strategy/2026-09-09-verdicts.txt` from the 14:42Z family-volatility line on,
`2026-09-09-plateau-review-verdicts.md` §34–49 and its "What we use", and the twenty dated studies
beside them.

### The gate was a coin flip

Sixteen gate rounds reconstructed from `real_gate.log` priced the leg-family statistic built the
day before.
The per-tape spread within a round is 3,006 coins a game, so the twenty-game family sum has
SE ≈ **17.7k** and every accept — +4,060 to +11,768 — was **0.2 to 0.7 of one SE**. Four of five
break under a single tape deletion, and against the fresh-loss reads every family variant has
Spearman ≤ 0.

Both arms were killed and restarted from their best fresh-loss thetas — flow170 from flow166
gen 170, flow171 from flow167 gen 150 — with the twelve fresh loss tapes as the held-out gate and
the family moved into training; thirty-five minutes later they were killed again, because the sim
shed fix had landed and is mandatory, and came back as **flow172** and **flow173**. Twelve boards is
no better a judge: per-board sd 4–7k puts the SE at 1.2–2.0k a game, the two leaders **+88 coins
apart**. The eight losses cut later extended it to **LOSS20**.

### What has ever predicted Kaggle

Nothing local. The account has sat at 1,957–1,996 since 09-04. flow102_g280 was promoted on the
drawn-leg shape — top10 pooled +7.6 pts at t 5.2, band level — and settled **−265**; flow135_g350's
six legs read +34 points and it settled on the same wall. Drawn legs became a **non-regression veto
only**.

The 52 % was not real either. Over 180 episodes it came from a 19W–1L ramp against opponents
averaging rating 1,403; post-ramp against the ≥1800 field the submission reads 44.0 % (09-08) and
41.7 % (09-09), p 0.77 for a change, on a field 57 rating points *weaker*, our coins flat.
Settled rate **42.9 %**: the gap to parity is four wins in seventy-two, not ten points.

### The live pinned set

The submission played 72 games that day — 30 wins, 42 losses, 41.7 %, both pools drawn from the
same rating band: the board and the shop draw decide, not the seat. A loss-only leg is conditioned
on the outcome — a lost board can only move up — so all 42 losses **and** 20 of the 30 wins were cut
as pinned-town tapes; intersecting those 62 with the launch scripts found **7 already training
rungs**.

The judge is the remaining **55 boards**: win rate first, d-margin positive excluding the two
non-byte-exact tapes, grouped |t| ≥ 2, 15 of 20 positive on the LOSS20 prefix, paired against the
live theta. Pinned seats replay the identical game, so every "110-game" live read is really 55
boards.

### The candidates

| candidate | remote gate | LOSS20 (excl-2) | LIVE55 win / margin | drawn veto |
|---|---|---|---|---|
| flow166 g170 | accept, leg20 +221 vs g150 | +4,855, t 4.71, 16/20 | 34.5 → **52.7 %**, +3,145, t 4.88 | **clear**: pooled +355, t 0.57 |
| flow167 g150 | refused by the family rule | +3,261, t 4.07, 15/20 | 34.5 → 50.9 %, +3,391, t 6.20 | running |
| flow172 g60 | accept, wins 44→53, fresh-12 +1,748 | +5,181, t 4.62 | 34.5 → **58.2 %**, +4,834, t 8.35 | running |
| flow172 g90 | accept vs g60, fresh-12 +281, wins −2 | pending | pending | pending |

g170's +2,797 a game is ours +1,745 and theirs −1,052 — **62 % growth, 38 % price denial**, pure
growth on the boards the live theta already won and broad at 84 of 110 board-seats up. It is one
day-0 change plus a ramp: sheep 2 → 1, cow 3 → 4, one wheat seed to carrot, hires on day 1 from 1
to 4 — +1,240 of growth on d5–9, +2,848 of price attack after d19.

flow167_g150 gets there on one mechanism, 19.6 sell rows moved to hour 18 at +3 coins a unit, for
+3,249 = ours **+3,644**, theirs +395 — the opponent's purse untouched. Head-to-head they are one
board apart, paired difference +471 at t 0.95, but g150 carries half the downside (worst five
−17.6k against −37.7k). Both drop 107117102 the same way: our extra d16–28 supply lifts the quotes
the tape sells into — denial handed back.

### The bug under the sim

`sim/units.py` resolved every PICKUP against the hour-start shed before any DROP into it; the engine
walks `[farmer, *hands]` in index order with immediate mutation. The file's own comment dismissed
the case as unreachable — true of our planner, false of a tape seat. Two prefix sums became one
seventeen-step walk carrying the shed level: the four fresh tapes that had diverged by 2.8–5.9k now
sit **−165 to −682** from the engine and 34 of 44 boards are byte-identical. It is why every sim
number here can be quoted — the g170 anatomy agrees with the engine to ~125 coins a tape.

### The switch pair

`TAIL_FILL_ON` and `BANK_BEFORE_LOT_ON` had sat inert in the tree since 09-03. They ship together
because the halves are lopsided in opposite directions: the filler alone reads LOSS12 **−354**, the
bank half +166 inside its own noise, the pair +575. The engine confirmed +801 held-out margin and
+1,403 a game, a sim screen sixteen coins away. On the live theta the pair **alone** reads
34.5 → 40.0 % (+6 boards, no drops), +875 a game at t 3.69; on top of g170 it adds +873 of margin
and no further wins.

### The gene arms

The drain-mix gene had been sized against the old champion. Re-checked on the padded g170 record it
read a change fraction of 40.2 % per board at sigma 0.02 — above the 35 % ceiling — and 31.1 % at
0.015, so flow168 launched at the lower sigma. Its first gate then refused a step that
took the live family from 98 wins to 108 (+14 flips, −4 drops) because the margin read −608 a game:
a margin-only rule can be the exact opposite of the rule the record is kept on.

That produced `--real-gate-metric winfirst`: net family **boards**, seats grouped, above a
threshold, with a bounded margin slack. Calibration showed the first threshold mis-set — eleven of
the 36 losing boards sit within 3k of the win line against one of nineteen wins, so zero-mean noise
has a **positive null mean** of +2.7 to +5.2 boards, and six net boards is cleared by noise 11–45 %
of the time. The deployed gate is nine, at zero slack.

Then the decode killed the arm. After 54 generations the gene block had moved 0.72 sigma — the same
as every other block. Its logits look sink-following, the top-ten census direction, but a **random
block of the same rms reproduces every statistic**: isotropic drift, not learning. The replacement
is flow178, `--train-only gd,gbd`, 264 parameters — the only run that can say whether the
residual-drain tilt pays.

### The harness

Every remote accept had been judged by hand at one to three hours of latency.
`S/autojudge/watch.sh` tails each arm's gate log over ssh, matches only the record line, fetches
`real_gate_pending.npy`, md5-checks it against the previous record and runs LIVE62 → LIVE55 →
LOSS20 under a lock. Replayed against flow166's finished log it matched all five record accepts and
none of the detail lines; its first live use had flow172_g60's legs running inside the minute.

The second change came from g170's one bad drawn leg. Its today41 dip (−5.8 points, McNemar p 0.025)
sits entirely in the **ceiling bucket** — the twenty tapes the base beats 8 of 8 on drawn towns,
where a candidate can only give margin back and never gain a win; on pinned boards the base wins,
g170 drops one in 45. A drawn win dip no longer vetoes when the panel margin is level, and
`paired.py` prints a contested-tape column, under which five of six legs are up and today41 reads
+3.0 points.

Three operator slips. The recipe generator appended the twelve gate packages to the header
*comment* mentioning `--real-gate-opponent` rather than to the option, so flow170/171 and the first
flow172/173 died at startup: read the generated file, not the generator. Restarting the
auto-judge on its tail phrase killed the monitor sharing that text, and re-chaining the judge queue
orphaned g170's eval workers — the kill-by-PID rule, twice in an hour.

### The hand-over

At 17:20Z, veto clear, the first hand-over of the campaign: **flow166 g170**,
`dist/submission_flow166_g170_v2.tar.gz` md5 `7f9e540bf3439348c638ac5b88f75353`, ready now; beside
it `dist/submission_flow172_g60_v2.tar.gz` md5 `1e7bea9e3299b5fdac335670cd93d4b3`, stronger on every
live read and worth the wait its veto legs need, and `dist/submission_flow167_g150_v2.tar.gz` md5
`935eeb4ead3576e8742d9efb3fd01db9`, the growth-only alternative. The pair variant `2e00efaa`
awaits its own veto. All are equivalence-played against their judge csv to the coin.

The caveats travel with them. A re-upload restarts the rating, ~150 games of re-climb. The edge is
late-season — 108 % of g150's margin opens after day 20 — so a market shift costs it. And calling a
seven-point step against the 43 % baseline needs ~200 post-ramp games, so nothing the first day
shows will settle it.

### Open at end of day

* flow172 (gen 90 accepted, auto-judged) on GPU1, flow178 (gene-only) on GPU0; flow174/175/169
  queued.
* Veto legs running for flow172_g60, flow167_g150 and the switch pair; the live set to grow toward
  ~120 boards, ten of today's wins still uncut.
* Unresolved: whether the residual-drain tilt pays anything, and whether any of this moves a rating
  — no local read has yet predicted one.
* Live: 89 W / 98 L, 41.9 % post-ramp against the ≥1800 field, p 0.81 against the 43 % baseline;
  27 losses cut today; the top-ten target 13 days out.

*Addendum, 2026-09-10 evening.* Two reads landed after the chapter was written. flow172_g90's auto-judge read the same LIVE55 flip set as g60 (+28/−2, +4,966 per game, t 7.6) and LOSS20 0 → 25 % (+5,382, t 4.8); its veto is queued behind g60's. The g60 live anatomy (docs/strategy/2026-09-10-flow172-g60-live-anatomy.md) found g60 = g170 plus a later-day sell mix: opening, pump and hires identical, 91 % of the +1,825 over g170 in our own purse, half of g170's tail. Open items are unchanged: the veto legs, the user's upload.

## 2026-09-10 evening — the refused candidate

Sources: `docs/strategy/2026-09-09-verdicts.txt` from the 17:55Z g90 line on,
`2026-09-09-plateau-review-verdicts.md` §50–54, and the dated studies named below.

### What sixty generations bought

Engine, 55 pinned live boards, both seats: the live theta −286 a game at 34.5 %, g170 +2,482 at
52.7 %, **g60 +4,306 at 58.2 %**. The step over g170 is +1,825 at t 8.9, **91 % of it our own
purse** (+1,652 ours, −173 theirs), flat across boards won and lost (+1,733, +1,890) — no new
denial channel.

It changed no structure: the d0 basket is byte-identical on all 110 board-seats (GOOSE 1 / COW 4 /
SHEEP 1, seed WHEAT 9 / CARROT 10), hires d0–d4 at 4/4/4/5/4. One lever moved, and it is
execution — sell rows at hour 1 105.8 → 99.4, at hour 18 32.2 → 38.0, realised price per unit
92.38 → 93.47, **+1,995 of revenue on +5 units**. Nothing before day 9 (−13); **+1,145 in d15–19**.
The tail halves: worst-five −22,585 against −43,067, 14 of 110 boards negative against 26.

Those are sim numbers, quotable because the shed fix landed: mean |sim − engine| 154 coins, W/L
agreement 100 %.

### The gate refused the best candidate

Three remote verdicts in forty minutes: g130 refused, then **g170 refused** on a LEG20 leg of
−4,210 over 24 games — a coin flip at SE ≈ 18k — while its pinned screen was the largest ever
recorded: 120 games, wins **51 → 67, +16/−0**, margin −547 → +99, +647 a game.

It was fetched by hand from `real_gate_pending.npy` (md5 `e8176b69`), named **flow172_g170c**, and
read on the local judge: LIVE55 34.5 → **65.5 %**, flips +36/−2, excl-2 +5,930, SE 669,
**t 8.87**, 48 of 53 positive; LOSS20 0 → 35 %, +5,822, t 4.34. The campaign's best live read was a
candidate the gate had thrown away.

The rule that follows is cheap: **fetch and read every gate candidate locally, whatever the
verdict**; a watcher on `real_gate.log` now does it. Twenty-nine minutes later g200 was *accepted*
(wins 51 → 63, margin +375, LEG20 +1,532) and read 65.5 %, +5,850, t 9.02, 48/53 — the **same flip
set**. Accept and refusal landed on the same candidate; the gate's sign was the noise.

### One residual, three closed levers

g60 wins 5 of LOSS20 and loses 15, and the twenty tapes are one opponent: d0 7 WHEAT + 12 MELON,
5 HIRE, 21–22 hires by d4. All twenty have gap(d14) between +15.0k and +22.8k, the five wins
included; corr(final gap, gap_d14) +0.06, corr(final gap, d14→d29 recovery) **−0.86**. One band is
the loss: d10–14 revenue −22.7k, of which the **d10–11 melon pot is about −15k** (theirs 233 units
at 143.8, ours 92 at 117; we hold no melon before d10 and sell from d18 at 220 falling to 113).

Three levers were priced against it on live boards, all closed:

| lever | read | verdict |
|---|---|---|
| sell-hour layout (sim, 122 seats) | (3,10,21) −165 t −0.9; a fourth row −77; early sale off −77 | no headroom |
| herd mix (`ANIMAL_MIX_DRAIN` 1.0) | LIVE55 +4 flips, excl-2 +149, t 0.60 | dead (+261 in the sim) |
| `OPP_SUPPLY_ON` on g150 + pair | +1 flip, margin level | dead |

That left `FORWARD_ADMIT`, the way to put melon in the ground on d0. It **already existed** in
arms-next, the switch sweep had read it at HELD42 −8,676 (t −12), and its horizon gene g11 decodes
`forward_days = 0` **every day**: given the lever free, the ES declined it and raised the crew
target to 11 by day 10 instead. The narrower rebuild reads HELD42 −2,628 (t −8.0), LOSS12 −6,403,
flips +0/−8. The pot is not a hiring problem, and the lesson costs more than the verdict: grep
`docs/strategy` for a knob name before building it.

### The pair composes

The `TAIL_FILL_ON` + `BANK_BEFORE_LOT_ON` drawn legs cleared: 2,592 pooled games, 85.0 → 86.4 %,
+483 a game. On g170 the pair reads LIVE55 52.7 %, excl-2
+4,018, t 5.87 — **+873 a game**, its standalone +875 intact. On g170c:
**66.4 %**, +37/−2, excl-2 +6,579, **t 10.15**, 49 of 53 — the best read of the campaign.

Each package played one pinned game against `opponent_tape_107056463`:

| package | md5 | judge row |
|---|---|---|
| `flow172_g170c_pair` | `bdb718c3f09768a9f7604355a03d36c8` | 100461 / 106312 — exact |
| `flow172_g170c_v2` | `645d39bc5a40230f60c1212df17c4392` | 100101 / 105975 — exact |
| `flow166_g170_pair` | `2e00efaa3fdaa0d7c92c7b5b96ad6a1d` | verified |
| `flow172_g60_v2` | `1e7bea9e3299b5fdac335670cd93d4b3` | exact |

### What g170c actually is

g170c − g60 is **+942 a game (t 3.5) = −39 ours, −981 theirs**: pure denial. Nothing structural
moved (basket, pump, hires d0–d3, d10 tiles identical); the step prices our basket **0.7 coins a
unit cheaper** (93.47 → 92.80) and takes 1,025 off their revenue on identical opponent units and
rows. It opens in d20–29 and **d10–14 moves +226** — the melon pot untouched.

The price is the tail: worst-five −36,470 against −22,585, 43 of 110 board-seats regress against
g60, and 107088554 sits at −19,595 with the opponent's purse *rising* +3,505. Two fewer losing
boards than g60, a twice-deeper tail.

The choice, stated rather than fudged: ship g170c for win rate (66.4 % with the pair), hold g60
(58.2 %, half the tail) if the tail matters. Neither buys d10–14.

### The GPU0 swap

flow178, the gene-only arm (`--train-only gd,gbd`, 264 live parameters), answered its question. Its
gen-10 gate refused (47.1 % against 47.6 %, win rate down, margin up +181) and its gen-100 gate
refused again (family flips +2/−2, net **0** against a minimum of 9, margin +845).
**The drain-mix block alone moves margin, not wins**; the arm was stopped rather than held for a
third refusal.

**flow179** took the GPU: the flow172 recipe from flow172_g170c, 7,053 parameters zero-padded from
6,789, gate every 100 with `--real-gate-metric winfirst`, min-flips 6, slack 0, over
flow172's own 60 pinned gate tapes **minus the 12 that are LIVE55 boards** — 48 opponents. That
exclusion is the point: flow178's gate played all 55 LIVE55 boards, which makes the judge in-sample
for its own candidates. Two slips at launch — a parenthesised opponent list is a bash syntax error,
and the first attempt ran in the wrong tree, since only `~/stage_draingene` carries the winfirst
metric and `stage_leg20`, where flow172 runs, does not.

### LIVE-B

Every candidate of the evening was selected on LIVE55 or LOSS20, or trained on a flow16x–17x rung.
LIVE-B is the disjoint remainder: 208 town tapes minus LIVE62, LOSS20, the 55, and the 147
`--tape-actions` ids across the flow160–179 launch scripts — **6 ids**, and the five newest live
losses took it to 11. It is loss-weighted and under its own
threshold of 15, so it is directional evidence, not a gate.

The field it draws from was re-checked: LIVE55's opponents at 1991 ± 52, 100 % ≥ 1800, against the
ten games after the cut at 1967 ± 55, win 36.4 → 40.0 % at z 1.34. Representative — and 0 of those
10 repeat a LIVE55 team: the roster is a distribution to sample, not a pool to regress against.

### Four operator lessons

**Read the generated file, not the generator.** The flow179 draft appended its gate list to the
header *comment* that mentions `--real-gate-opponent` — the failure that killed flow170/171 the day
before — and a second pass found the list was 60 tapes, not 72.

**Two watchers on one log do the work twice.** The auto-judge fetched g200 (md5 `20b6a2ee`) and
started its legs; the fetch-every-gate watcher fetched the same theta and started a duplicate read,
killed by PID. It now acts on REFUSED verdicts only.

**Trust the verifier, not its log.** 107224642 was dropped from LIVE-B as not byte-exact, then
restored: `cutloss.sh` clips log lines near 100 characters and a long opponent name pushed
`, verified` off the end.

**Box the agents and mean it.** The FORWARD_ADMIT build ran two hours over; the ship-pair suite ran
four, and was capped to one failure inside twenty minutes.

### Open at end of the evening

* Hand-over: **SAFE** `flow166_g170_pair` `2e00efaa`, veto clear; **AGGRESSIVE**
  `flow172_g170c_pair` `bdb718c3` (66.4 %, +6,579, t 10.2), its drawn legs queued behind g60's;
  **FALLBACK** `flow172_g60_v2` `1e7bea9e`.
* Veto queue: g60 (5 of 6 legs in, no veto), then g170c, then g90; g200 in its legs.
* Remote: flow172 at gen 293, flow179 at gen 26 with one refusal. Streams: the melon-route probe, and the
  LIVE-B chain behind the veto pipeline.
* Untouched by every candidate: the d10–14 melon pot, with FORWARD_ADMIT dead.
* Live: ~90–104 games, rating 1947, at baseline. A re-upload restarts it (~150 games of re-climb);
  the honest post-ramp baseline is 43 %.

## 2026-09-11 — the honest judges and the generation-300 record

Sources: `docs/strategy/2026-09-09-verdicts.txt` from the 20:36Z LIVE-B line to the end,
`2026-09-09-plateau-review-verdicts.md` §55–62, the update blocks of
`2026-09-10-upload-dossier.md`, and the eight dated `2026-09-1x` studies beside them.

### The pair composes on the safe theta too

The switch pair had composed on g170c; the night began by putting it on the cautious theta. On
flow172 g60 it reads LIVE55 34.5 → **64.5 %**, +33 flips and **zero drops**, excl-2 +5,382
(t 8.87), 48 of 53 positive — two win points under the aggressive file with none of its tail, and
both halves veto-clear standing alone. `dist/submission_flow172_g60_pair.tar.gz` md5 `bcb2f3b020625a6b287299ff4622cd03` then played one
pinned game against `opponent_tape_107056463`: 102,004 / 108,602 over 2,852 moves, the judge row
to the coin. `g170c_pair` `bdb718c3` was verified the same way.

### LIVE-B, the leg that grows with every loss

LIVE-B is the disjoint remainder — town tapes in no training rung, no gate, no judge — and it is
loss-weighted, so the live theta wins one board in eleven. Every loss cut that night joined it:
11 boards, then 13, then 17, and 22 by the time g400 was read.

| boards | g170c | g200 | g60 |
|---|---|---|---|
| 11 | 81.8 % / +6,885 (t 6.97) | 72.7 % / +6,448 | 63.6 % / +5,464 |
| 13 | 76.9 % / +6,563 | 61.5 % / +5,876 | 53.8 % / +4,854 |
| 17 | 70.6 % / +7,482 (t 7.0) | 58.8 % / +6,816 | 52.9 % / +5,591 |

Every candidate is positive on nearly every board, and the ranking never moves — LIVE55's own
order, on boards nothing selected on. At 17 it passed its n ≥ 15 threshold and stopped being
merely directional: out of sample the aggressive file leads the safe one by four boards.

### The melon family, closed in its last two forms

`2026-09-10-melon-route-capacity.md` asked whether the route model could reach the day-10 pot at
all. It can: forced melon plus mid-day placement sells 66 of 72 units on the day, 12,537 against
the clone's 17,440 at an average 233, the gap all **deposit turn** and worth ~4.2k. It still does
not pay — the second dumper takes ~174, and the archive's five forced melon builds lose 15–20k
over d12–29 as the 12 tiles displace the animal and wheat denial.

That left melon **additive** to the day-0 board, and no knob expresses it: the melon opening
preserves the plant-target sum by construction. The arithmetic argued first anyway — an extra
quad plus twelve seeds costs ~1,960 out of a purse we already spend down from 3,000 to 145,
against a ~12.5k pot at the second dumper's price. Spec written, not built. **The family is closed
in all three forms**, and the d10–14 gap is the price of the day-0 basket the ES chose.

An adjacent alarm cleared the same way: the shipped tree's 7 tile-write collisions all come from
`TAIL_CARE_ON`'s care hop pairing two *distinct* animal operations that write disjoint arrays. The
gate over-counts; there is no fidelity hole.

### The top tier, measured honestly

The twenty pinned top-ten tapes gave every candidate +4.5–6k a game and 5–15 win points, and still
had them losing two games in three. Then the caveat: **all twenty are flow172 training rungs**. No
held-out top-tier tape existed anywhere, so twenty fresh ones were cut, two per top-ten team, 40
of 40 byte-exact and overlapping none of the 323 excluded ids. That is **TOPB**.

| candidate | TOP20 (in-sample) | TOPB (held out) |
|---|---|---|
| g60 + pair | 20 → 35.0 %, +5,424, t 4.84 | 25 → 35 %, +2,890, t 1.87, 15/20 |
| g170c + pair | 20 → 30.0 %, +6,067, t 5.46 | 25 → 30 %, +3,174, t 1.92, 12/20 |

Direction agrees, magnitude **halves**, and both passes become fails: about half the measured
top-tier edge was training-set fit. TOP20 is a diagnostic from here, TOPB is the judge.

The drift study cleared g200 of turning away from the top tier — its TOPB gap to g170c is −824 at
t −1.1 — and found something worse and lineage-wide. Against the band the flow172 line takes about
**2.2k off the opponent's purse; against the top tier it hands them +0.8–1.1k**, already at g60.
The band margin overstates the top-tier margin about twofold.

`2026-09-11-rating-equilibrium.md` priced it. A tier logistic fit, bias-corrected by the ~200
points it undershoots the live theta's real ~1950 by, puts **g60_pair at ~2700–2750, g170c_pair at
~2650–2700**, both under the ~2880 cutoff. Holding 2880 needs ~52–53 % against the 2700–2950 tier
where the reads are 30–35 %: **350–400 rating points** still missing, all in the wall.

### The GPU swaps

flow179's gen-100 gate refused (family flips +0/−3 against a minimum of 6, wins 59 → 53), its
second, so the pre-logged rule stopped it and **flow180** took GPU0: the same recipe trained with
the pair *on*, in a new `drain-pair` branch of two clean cherry-picks with `N_PARAMS` 7053 intact.
The pair transfers to the search: the same theta reads +1,064 a game pair-off on the 96 gate
boards, **+1,530** pair-on. Its gen-10 gate then refused (+3/−3, net 0), the first of two.

**flow181** was drafted behind it: flow180 with only the twenty top-ten rung weights changed,
3 → 10.2, lifting the top-tier share of the episode budget from 17.1 % to exactly 40.0 %. It
trades band signal for top-tier, so the recipe gates it on **LIVE55 and TOPB together**.

### The auto-judge, and four ways to lose a candidate

The auto-judge grew a LIVE-B stage for every arm and an in-sample annotation on the LIVE55 line
when an arm's gate family overlaps it. Four slips cost real work anyway.

**The g400 skip.** On an accept the trainer consumes `real_gate_pending.npy` and `best_abs` lags,
so the watcher fetched a file still holding the g300 theta, matched the md5 and skipped the
record; fixed with a materialise wait. By hand, g400 reads LIVE55 65.5 % — below g300 despite the
accept.

**The g420 loss.** g420 was refused by LEG20 on −954 over 24 games while its pinned screen read
wins 65 → 67. The tail-based watcher never fired, and the pending file was deleted at the next
checkpoint — present 22:32Z, gone by 22:38Z — before a hand judge reached it. The candidate is
gone; its replacement polls the gate log every 60 seconds.

**The tail that dropped in silence.** That same watcher's ssh tail had exited 1 with no output an
hour earlier: a tail is not a subscription.

**The duplicate judge.** A four-hour-old wait chain re-ran the finished flow167_g150 judge for 45
minutes, holding `judge.lock` while the g170c veto queued for two and a half hours. And beside it
a label trap: g260's pending file was overwritten by g300's, so everything logged `flow172_g260`
is the g300 theta.

### Generation 300

The remote accepted g300 on pinned wins 61 → 68. The local judge made it the best candidate of the
campaign: LIVE55 34.5 → **69.1 %** (+40/−2), excl-2 +6,158 (t 9.10); with the pair **70.9 %**,
+6,753 (t 9.95), 47 of 53; LOSS20 0 → 40 %; LIVE-B at 17 boards 76.5 % / +8,119; TOPB +3,730 at
**t 2.12** — the campaign's first top-tier read to clear significance.

The anatomy says why to prefer it: g300 − g170c on LIVE55 is +433 = **+312 ours / −121 theirs**,
72 % growth, reversing g170c's pure-denial signature, spent where we lose (+876 on the loss
boards). Nothing structural moved again — basket, pump and hires d0–d3 identical, 19 more units at
92.80 → 91.92 apiece. The step is one day band, d15–19 +359; d10–14 moves +45 and stays −1,221
against the live theta.

And the tail g170c had doubled closes: worst-five −21,627 against −36,470, fifteen shallow
negative boards where g170c had twelve at mean −4,378. The step is below the live noise floor
(t 0.56) but sign-consistent on all four judges, and its package replayed 106581754 to the coin.

### The hand-over

| order | package | md5 | state |
|---|---|---|---|
| AGGRESSIVE | `flow172_g300_pair` | `82d0a198a3263e7dbf9768f5b343f877` | leads every leg; veto running |
| second | `flow172_g170c_pair` | `bdb718c3f09768a9f7604355a03d36c8` | 66.4 %, +6,579, t 10.15 |
| SAFE | `flow172_g60_pair` | `bcb2f3b020625a6b287299ff4622cd03` | cleared, zero drops, lowest tail |

What the rating model promises is worth stating plainly: from ~1950 these files should climb and
stop near 2650–2750, short of the ~2880 the top ten needs, at the cost of ~150 games of re-climb
because a re-upload restarts the rating. What would close the rest is the top-tier wall, and no
file here touches it.

### Open at end of the night

* Hand-over as tabled above, with two drawn vetoes still running.
* Remote: flow172 past gen 419 (record g400, accepted on margin with wins down); flow180 at gen 15
  with one refusal of two; flow181 staged behind it.
* Judges: LIVE-B at 22 boards and growing; TOPB the only honest read of the wall. Closed tonight:
  melon in all three forms, the collision gate, the g200 drift scare.
* Unresolved and now quantified: **350–400 rating points** of top-tier strength, all of it in the
  day-10 melon dump and the late adaptive mix — the ES lineage's problem, not a knob's.
* Live: 98–112, 46.7 %, rating 1940 and slipping; the top-ten target 12 days out.

## 2026-09-10 — the reboot, generation 1000, and the switch that pays the top tier

Sources: `S/glut/verdicts.log` 07:35Z–10:48Z (the day's copy is `docs/strategy/2026-09-10-verdicts.txt`),
`2026-09-10-consensus.md`, and the eleven stream documents beside it.

### 07:17Z — the judge burned down

The machine rebooted and took `/tmp` with it, and with `/tmp` the entire scratchpad judge toolkit:
the auto-judge, LIVE62/LIVE55/LOSS20 and the leg runners, `paired.py`, every lossflip csv, the
Kaggle watcher. No theta or package was lost — those are in the repo — but the instrument that tells one from another was.

It was rebuilt durably: `S/` now sits at the repo root, git-excluded.
**1,386 files** came back out of the session transcripts into `S/_recovered`, `on2b.py` was rebuilt
by hand, the LIVE62 ids were re-cut from the live episode list (72 games, 30W/42L before
09-09 15:14Z → 62 tapes, 55 held out; the 7 training ids matched the old doc), and the town schedule
was re-fetched from the remote (md5 `086c9c23`).

Then the question that mattered: does it read the same numbers? Base
flow135_g350 scored **34.5 %** on the 110 held-out games — the pre-reboot base to the digit. On the
re-cut LIVE55, `g300pair` read **70.9 %, +6,753, SE 679, t 9.95, 47/53** — yesterday's line to the
coin. Rebuilt TOPB gave g300pair **+3,730 at t 2.12** against yesterday's +3,730 / t 2.1. The
judge is a set of ids and a procedure, and both survived in the transcript; only the csvs were mortal.

### Generations 940 and 1000

The remote had not stopped while the local half burned. flow172 accepted g700, g740, g850 and
**g940** (remote gate 63.3 % / +3,865 on 120 games; md5 `958f100d`). The local judge made it the
largest live read of the campaign: LIVE55 34.5 → **81.8 %** (+52/−0), +8,734, t 14.99; with the tail
pair **83.6 %** (+54/−0), +9,130, t 14.19, 52/53; LOSS20 **65 %**, +10,634, t 10.4 against
g300pair's 45 %. TOPB — the held-out top tier — went 25 → 35 %, **+5,578, t 3.32**, no board
dropped: the top-tier edge is growing with the lineage, not being traded away for band wins.
Packaged as `dist/submission_flow172_g940_pair.tar.gz` md5 `f142fadf`, with the packaged agent
replayed coin-exact 124/124 against the judge csv on the 62 live boards.

An hour later g1000 was accepted (66.7 % / +4,294 vs g940's 63.3 % / +3,865; md5 `f091deb2`) and
beat it again on the band: LIVE55 **89.1 %** (+60/−0), +9,293, t 13.7; TOPB 25 → **40 %**, +5,758,
t 3.3. Head to head against g940pair on LIVE62 the margin was **+191, t 0.65 — level**, so the recommendation was HOLD: an unresolvable margin does not buy the ~150 games a re-upload costs in re-climb.

The user uploaded both files anyway, and kept both live: **56139820** = `g60_pair` `bcb2f3b0` at
08:15Z, then **56140532** = `g940_pair` `f142fadf` at 08:25Z. The ladders separated immediately.
The safe file climbed 1362 (11W-2L) → 1475 → 1627 → 1697 (35W-9L). The g940 file went **14W-0L for
2079** — past the old file's ceiling in fourteen games — then 27W-5L 2429, 31W-7L 2457, and
**2473 within about three hours**, past every ceiling this campaign has had. The file it replaced (56098262) had ground to 123W-143L, 46.2 %, rating 1916.5, rank 1389, and
the ladder had moved *up* underneath us: #1 3062, #5 2980.5, **#10 2950.4** against the ~2880 cutoff we had been pricing.

### flow180: 517 generations with nothing to show

GPU0's flow180 looked healthy — every candidate since g130 beat the 96-game bar, g500 reading
71.9 % / +5,287 against the incumbent's 61.5 % / +1,530, net +10 boards — but its winfirst family
net was +5 against `min_flips 6`, so all 16 were refused. Fetching g500 by hand exposed the real
defect: `real_gate_cand.npy` was **flow172_g170c zero-padded** (first 6,789 weights identical, the
264-weight tail all zeros). The trainer never writes a refused candidate, and flow180 re-centres to
the incumbent on every third refusal. 517 generations with the theta pinned to its init, and the promising 65.5 % local read was g170c's own line. **A refused candidate does not exist; only
what the gate accepts is recoverable.**

flow180 was killed. **flow181b** took GPU0 — top-ten rungs at 40 % of the episode budget in the
pair-ON tree, init = flow172_g940 padded to 7,053 (`16635eb5`), `--real-gate-min-flips 3`, seed 281,
gen-0 gate 65.6 % / +5,157. It was killed at gen 119 after three straight refusals (63.5 %, 64.6 %,
68.8 % / +4,794 against that bar) under the same rule. **flow182** replaced it:
`launch_flow172.sh` verbatim from init flow172_g1000, seed 282. My own slip: the first launch went out with a mis-substituted init path and had to be relaunched — GPU0 minutes spent on a run that would have trained from the wrong theta.

### Consensus: a blind second reviewer for every planner claim

The user's rule, at 09:23Z: every planner-logic review gets an independent second reviewer with no
access to the first document, and nothing is acted on until the pair agrees. Four blind B-reviews
ran; `2026-09-10-consensus.md` holds the tables.

**Chain optimisation** and the **intraday market controller** both came back DO NOT RUN from both sides, and each pair proposed the same narrower experiment. Both narrower
experiments were then played the same morning and both died: HARVEST_FIRST_ON on TOPB
**−229, t −1.0**, and OPEN_PUMP_TELL_KEEP0_ON **byte-identical** on all 124 live-board games and all
40 TOPB games. The intraday family is closed.

**TOPB loss anatomy** agreed on the shape and B sharpened the mechanism: the d10–14 melon hole is
a **flat tax** (−19.6k, as large on boards we win), and 87 % of the win/loss difference is the
*opponent's* d15–29 purse (+18.8k, late wool +8.9k). B added the price half — we match wool volume
and sheep count and lose the price, **144 vs 160 a unit**, sell-day 19.7 vs 18.2, 22 units before
d16 against their 46.

**The wall audit** agreed on three findings: `land_bias` saturated (A: −256 on 27/30 days in all
seven lineage thetas; B: exactly −land_price on 30–71 % of days), `compact` on DIST_MAX, and
`cash_reserve` as the largest unmeasured constant. B added GROW_MAX on the rail 52–55 % of days and
melon `plant_target` at 0 in 16,800/16,800 decisions.

### The switch screen, and the first thing to pay in two days

Every planner switch in the tree had been judged on *band* boards; TOPB did not exist when they were built. So all 20 default-OFF switches were re-screened on top of g1000+pair against the
20 held-out top-tier boards. Seven were byte-level no-ops (CARE_FILL, CARE_HOLD, HARVEST_FIRST,
LATE_STRAW_CAP, MELON_LOT_EARLY, SHED_OVERFLOW, OPP_MIX); nine were negative, from MIDDAY_DROP
−2.9k to OPEN_DENY −21k and ANIMAL_DEFER −28k; three (MARKET_PACK, PRESTOCK, ROUTE_EARLY) were
**void, not measured** — our seat ends all 40 games at exactly 3,000 coins, the idle-agent
signature, so those switches are simply broken on this lineage.

One survived. **HIRE_ROW_ON**: TOPB **+815/game, SE 1,506, t 2.92**, own purse +935, no board
dropped; LIVE62 head-to-head **+453/game, SE 1,049, t 3.59**, wins 87.1 → 88.7 %; LIVE55 against
base 34.5 → **90.9 %** (+62/−0), +9,734, t 14.8, 53 of 53 positive; and on the new mid-tier set
LIVE-C, 50 → **75 %**. A switch that had been closed on band boards pays against the top tier once
the theta underneath it is strong enough — switch verdicts are theta-conditional, and the archive's
"closed" only ever meant closed on the boards it was judged on. Packaged as
`dist/submission_flow172_g1000_pair_hr.tar.gz` md5 **`8274d577`**, coin-exact 124/124 in pkgcheck.

### The wall that was not a lever

The audit's one real wall was the saturated land gene, and the paired reads refuted it as a lever
in three forms. An unpaired probe had been seductive — own coins 116k → 173k with the veto off —
and it lied. **LAND_BIAS_ZERO**: TOPB **−16,640, t −9.4** (12 drops; ours −8.5k, theirs +8.1k);
LIVE55 34.5 → 15.5 %, −8,148, t −9.3. **FLOOR 0.1**: TOPB −16.7k, LIVE55 17.3 %, −8,056, t −9.2.
**ZERO + MIN_DAY 2**: −6,217, t −6.8 — the whole probe gain had been the day-0 quadrant, and quad 4
is still never bought. The saturated gene is the **optimum's edge**, not a training defect. A
saturated gene is a hypothesis; only a paired read is a verdict.

The rest of the audit's shortlist closed the same morning. **CASH_RESERVE_SCALE** (one site,
`plan.py:3624-3631`, default byte-identical by 30-day state hash): TOPB +248 / −46 at 0.5 / 0.0,
LIVE55 89.1 → 86.4 % at 0.5 — a correctly-sized rule. **GROW_MAX** 6 and 8: byte-identical on all
40 TOPB games although the decode moves `grow_mult` on 330/600 observations — the capped product is
already top-ranked, so raising the cap re-orders nothing. **LATE_SELL_FILL_ON**: TOPB +5 (36/40
identical), LIVE62 level — the plateau review's "19 units short" was DROP's deliberate day-29
over-ask, as the builder and reviewer predicted. **WOOL_FIRST_LOT_ON**, the consensus
lever, moved the sell *turn* (14 → 2.7) but not the sell *day* (median 23 → 23): TOPB −17, LIVE55
89.1 → 81.8 %. Its day variant **WOOL_SINK_HOLD** is a no-op by construction — wool's hold decodes
0–87 against a best marginal of 160–200, so a wool sale is never refused. The day gap is about when
wool *lands*, which is the herd family, closed as a hand lever and owned by the `animal_want` gene.

The **tile-collision** alarm cost a stream to confirm 0 coins: the 7 hits are a route op against the
deliberate `TAIL_CARE_ON` hop, distinct ops writing disjoint day flags, 9 in 300 planned days, and
the fix is to key the gate on `(tile, op)`. My miss: it was already adjudicated in
`2026-09-11-sim-tile-collision-gate.md` and I dispatched without checking the archive, which is the
standing rule. A second pre-existing failure on the shipping branch (`test_backend_agreement`,
hire_bias numpy 33 vs jax 32 on 2 of 2,400) is logged and unexplained.

### LIVE-C, and what is open

The live file now plays opponents rated 2300–2500 — between LIVE55's band and TOPB's top tier, and in no judge. So sub 56140532's games against opponents ≥ 2300 were cut into pinned tapes: **LIVE-C**, 8 boards (4 losses, 4 wins, median 2427), 16/16 byte-exact, held out of
every training rung. It reproduces the live outcomes 8/16 and it discriminates
(flow135_g350 reads 25 %, −6,041, t −8.2), and three of the four losses are coin flips
(−115, −560, −2,705). Directional at n = 8, and it grows with every live game.

Open going into 2026-09-11: `8274d577` ready to upload behind the g940 file's ramp; flow182 on GPU0
from g1000 and flow172 past gen 1167 with g1000 still the record; the **slope-repair build** —
COMPACT_SOFT_ON plus a zero-init per-crop `plant_floor` gene block (N_PARAMS +9) with the mandatory
sigma-0.02 slope check — as the training-arm answer to the two saturations the audit found, for
flow182's successor. Every hand lever the audit surfaced is now closed. The top tier is still lost
in days 15–29, on the opponent's purse.



### Addendum — 11:00Z–14:40Z: the inference side runs out, and the judge becomes the project

Sources: `S/glut/verdicts.log` 11:03Z–14:33Z, `2026-09-10-consensus.md` §5–7, the two
rating-calibration documents, `-slope-repair-review.md`, the two flow184 gene checks, the two
LIVE-C63 anatomies and `-town-visibility.md`.

### Three screens, and the end of the planner's inventory

The morning's TOPB screen had found one payer among 20 default-OFF switches; the afternoon asked
twice more, same answer. On **LIVE-C22**, the mid-tier set, 15 switches on g1000+pair produced **no
positive**: five byte-level no-ops, CARE_HOLD −154 and HARVEST_FIRST −302, then a dead tail from
MIDDAY_PLACE −2.4k through FORWARD_ADMIT −4.5k to OPEN_DENY −29.7k on every board. Then the
**constant screen**, taking wall-audit B's unmeasured list with no build at all: `HIRE_BIAS_MAX` 600
read −2.0k/−1.9k (4 of 8 drops) and 800 read −9.9k/−13.2k on all boards — the ±400 ceiling is right
where it is; `CREW_TARGET_PUSH` 300 and 200 gave −1.2k/−174 and −735/−394; `CHAIN_MAX` 8 and
`STREAM_MAX` 48 were byte-identical, they never bind. With that list measured the inference side of
the planner was exhausted.

The survivor is **HIRE_ROW_ON**, and by 11:39Z four judges agreed: TOPB +815 (t 2.9), LIVE62 +453 (t
3.6), LIVE-C22 **+990/game, SE 926, t 5.0**, wins 50 → 63.6 % (+6/−0), LIVE55 90.9 %. Its package
`dist/submission_flow172_g1000_pair_hr.tar.gz`, md5 **`8274d577`**, went up at 11:34Z as **sub
56143250**. Two minutes later the user set a standing constraint — **only two active submissions** —
so 56139820 (the safe g60 file, ended at 1764) was dropped.

### Rebuilding the judge sets under the calibration

TOPB had carried some 45 candidate reads, so a fresh twin was cut: **TOPB2**, 20 boards, two per
current top-ten team, ratings **2953–3081**, 40/40 byte-exact, zero overlap with 432 known ids. Its
verdict was blunt: hire-row's **margin replicated (+899, t 3.1) while the win rate did not move — 25
%, the same 25 % every file we own reads**. Against today's leaders we win one board in four.

LIVE-C went the other way. It grew 8 → 22 boards at 11:34Z (+7 losses, +7 wins, opponents 2353–2552,
28/28 byte-exact), and calibration B named the defect: of 33 eligible ≥2300 episodes the cut took
**11 L + 11 W from a pool that was 11 L / 22 W = 66.7 %** — a balanced-cut artifact worth `272 × ln
2` = **+188 rating points** of built-in pessimism. The cut was completed: **LIVE-C63**, the entire
≥2300 pool of sub 56140532, 24 L / 39 W = 61.9 %, 82/82 verified, remote towns 290 → 331. It
reproduces itself — the live theta replays to **62.7 % against the pool's own 61.9 %** — and
discriminates: g1000pair 61.1 %, the shipped hire-row file **68.3 %** (+13/−6, +731 t 2.6). Both
LIVE-C63 anatomies reproduce the csv 126/126 byte-exact, and the 6,954-wide judge path was proved by
identity: g1000 zero-padded under `PLANT_FLOOR_ON=True` is byte-identical to g1000pair on all 40
TOPB games.

### What the ladder says the judge is worth

Two blind calibrations agree on the number that matters. The slope is **272 points per logit**
(0.00368/pt; 9.2 win points per 100 rating points, not Elo's 14) over 352–375 games, and flow135's
fitted crossover of **1923** lands on its realised 1924. Our judge reads **100–190 points
pessimistic** — A puts the in-band offset at +97 (88–107), B derives +110 for LIVE55 and +188 for
LIVE-C22 structurally. **TOPB2 is a floor, not a gauge**: it credits flow135 with 15 % where the
curve says 1.9 %, `p = 0.13 + 0.74σ` reproduces every file, and at n=40 it cannot resolve a
150-point step. **LIVE-C is the instrument** — a 2960 file needs 77–84 % there against today's 63.6
%, so the target is **≈ 80 %** and the shipped file sits at 68 %. Both predict sub 56143250 settles
**2650–2730, not top ten**. At game 45 it read 35W-10L, 2291, games 11–45 about 75 % — **below A's
85 % falsifier, inside B's 72–82 % band** — so B's slower convergence is the live hypothesis,
rechecked at game 58. The slope's own CI (170–620) moves the LIVE-C target between 63 and 87 %:
ladder games above 2500 are worth more than another judge board.

### The training arm: three kills and a gene that was switched off

flow172 was killed at gen 1287 under rule 4 — three straight refusals (g1100 67.5 %, g1110, g1200
64.2 % against the 66.7 % bar) with no record since g1000. **flow183** took GPU1: the same recipe
with the 20 top-ten tape rungs raised 3 → 10.2, **40 % of the episode budget**, leg20 gate, seed
283. It died the same way at gen 69 (63.3 %, 65.0 %, 63.3 %) — the top-tier weighting did not lift
the gate. Its successors are **flow185b** (GPU1, gate = all 83 target-band boards, LIVE-C63 + TOPB2,
166 games/eval, gen-0 seat 50.0 %/+1,015) and **flow185c** (GPU0, the 42-board variant, 34.5
%/−1,227): both arms are now selected on the boards we are trying to beat.

Between them ran the **slope-repair build** (worktree `slope-repair` 6486bac): a per-crop
`plant_floor` gene behind `PLANT_FLOOR_ON`, **N_PARAMS 6,789 → 6,954**, zero-pad identity with 0
mismatches on 2,400 boards, and, per the standing gene rule, a measured slope at sigma 0.02: the
melon floor moves on **19.1 % of member-boards, any crop 62.6 %** (the reviewer re-measured
19.2/61.6). The review cleared it and forbade one thing: do **not** bundle `COMPACT_SOFT_ON`, which
changes the plan on 202 of 300 boards while `--train-only g12,gb12` never touches `g6` — a behaviour
change with no trainable slope. Its fix-first — print the switches in the startup banner — closed
the silent-flow151 hole. An inference read closed compact-soft anyway (TOPB2 −327, LIVE-C22 −162).

**flow184** trained the gene and the gene lost. Both checks agree it was alive — L2 0.1974, all 165
coordinates moving, prefix byte-identical — and **selected against**: every floor logit driven below
the decode threshold, melon at −7.6σ (B: z −3.64, four crops jointly 0 of 200,000 null draws),
population expression 19 % → 0.12 %, with **wheat, the crop the incumbent already plants, the
untouched control**. Its gen-10 record judged as the shipped file with the floor switched off (TOPB2
−69, LIVE-C22 +133, LIVE62 +20). Consensus kept **flow184b** as a short test of the other half —
whether the sign flips when the top tier carries 40 % of the budget — on a gen-50 bar. It was met at
**gen 1**: its seat, g1000 plus a forced 2/16 melon floor, scored **10.0 %/−12,824** against g1000's
66.7 %/+4,294, and its first candidate reached 18.3 % only by turning the floor back down. **The
melon family is now closed inside the ES as well as outside it.**

The **auto-judge** was rebuilt so records are judged minutes after ACCEPT, not at the hourly firing
(parser replay 11/11, self-test byte-identical to the shipped csvs). It then hit a checkpoint race:
flow184's ACCEPT fired at gen 18, *before* the gen-20 checkpoint, so the watcher fetched the
**seat** and judged it as a record. The fix waits for `best_abs.npy`'s md5 to change after an
ACCEPT, derives the seat md5 from the launcher's `--init-theta`, and requires three csvs with data
rows.

### Where the mid-tier losses actually are

Both anatomies land on the same split. The d10–14 melon hole is **−22 k on boards we win and boards
we lose alike (t −0.44)** — a flat tax. **All** the separation is d15–29 (t −8.94), and **62 % of it
is our own purse**. Of 27 product×band buckets only two clear: WOOL d15–29 (t −4.0) and TOMATO
d15–29 (t −3.7); fertiliser is level, which retracts the 4-board "−7.9k displacement" as a constant.
They cluster on the **town draw** — tomato sink 170 on losses against 270 on wins, B's sink index
correlating +0.41 with margin — while our day-9 cash is identical to the coin (6,165 vs 6,163). The
pair split on mechanism: A reads wool **price** at equal units (≈4.3k/board), B **volume**, our
sheep count a step function against their flat 6–8.6. Both switches are being built
(`WOOL_SPLIT_CAP`, `SHEEP_FLOOR`). The blindness hypothesis died before it cost a gene: the theta
**does** see the draw — one more YARN_STORE moves wool `grow_mult` +26.7 %, `hold` +64 % and `press`
−70 % — so no observation block, and the losses are the ES's to fix.

### What I got wrong

Four in one afternoon. A `ps | grep` pattern matched **my own ssh shell** and killed it — the
standing rule is to kill by PID. flow184's first launch died on argparse because the arms-next
trainer has no `leg20` gate family, costing GPU0 minutes. `watch.sh --legs` was handed a
**relative** theta path while its runners `cd` into the worktree, so the first real flow184 record
failed all three legs. And the checkpoint race meant a leg set was spent **judging the seat as if it
were a record** — after the morning's flow182 relaunch on a mis-substituted init path. The pattern
repeats: the judge and the launcher are as much a part of the experiment as the theta.



## 2026-09-10 20:30Z → 2026-09-11 02:00Z — the peak, the lottery, and the first theta to pass

Sources: `S/glut/verdicts.log` 20:37Z–01:55Z, `2026-09-10-consensus.md` §16–§23,
`2026-09-10-pop-spearman-B.md`, `2026-09-10-record-gate-calibration.md`, `2026-09-11-margin-scale-AB.md`,
`2026-09-11-sigma-AB.md`, `2026-09-11-recentre-onestep.md`, the three objective-field reports
(`-lost-board-`, `-seat-swap-`, `-fresh-board-objective.md`) and `2026-09-11-livec-extension.md`.

### The inventory: what had never been measured

At 20:37Z the user asked what we were assuming without measuring, and the answer (consensus §17) was
uncomfortable. Eight load-bearing assumptions had no measurement behind them, and the first was the
project itself: **that the ES step makes progress at the current centre**. Every arm since flow172 had
been launched on the belief that one Adam generation moves the theta uphill; the belief rested on the
lineage's history (g60 → g940, LIVE55 34.5 → 83.6 %) and on nothing measured at g1000. Beside it sat
sigma, lr and Adam — never swept for progress, only argued — the abs-probe record selector's hit rate,
the gate's false-accept and false-refuse rates (9 and 1 decisions), the stop rule's power (30 hold-out
boards, where +5 points is 1.5 boards), the judge-to-ladder slope above 2700 (CI 182–686), that
generality matters on a one-family ladder, and any progress rate that reaches the 09-23 target. The
measured-and-trusted column was long — sim = engine on pinned towns, tape fidelity, two-purse
signatures, board determinism, every planner closure — but none of it was about the optimiser.

Two log-based measurements closed the same evening (`2026-09-10-record-gate-calibration.md`, 53
decisions). The record selector — `abs_score` in `log.jsonl` — has **no size signal** against the gate
(Pearson −0.02, Spearman −0.37, n 25) and a weak sign signal (records net > 0 in 64 % vs a 44 % null, p
0.035); `abs_score` rises monotonically past g1000 while the gate margin falls from +4,294, the
signature of overfit to the probe. And the gate is **under-powered both ways**: 89.6 % of changed
boards move both seats, so 124 games are ≈ 62 independent boards; with p̂(flip) 0.098 and sd(net) 4.86,
P(net ≥ 5 | null) = 16.7 % and a 5 % false-accept needs net ≥ 9, while the power at min_flips 5 is 50 %
at +4.8 points and 80 % at +8.1. The decisive row: the shipped theta g940 read **net +0** on flips — its
gain was margin (+3,314 → +3,865) — so a flips gate at any threshold would have refused the campaign's
best candidate. The gate was **demoted to a logger** at 20:49Z; every record, accepted or refused, is
kept under `cands/` and judged by the local legs on print. The auto-judge was rewritten to match every
`(record) pinned:` line, and the four records the ACCEPT-only watcher had skipped were queued as backfill.

### One step, twenty-two evaluations — blind review B

The pop curve had landed at 20:35Z (consensus §16): two-seed Spearman rising from −0.028 at P = 64 to
+0.015 at 2048, cosine +0.026 first clearing the null at 2.0 sd, ‖g‖ ∝ P^−0.500, a fit of cos = P/(P+c)
with c ≈ 76–108k putting Spearman 0.9 at **P ≈ 0.7 M**, and the curve running ~5× below the
linear-fitness ceiling. The on-file "half-split Spearman 0.93–0.96" was retracted the same hour — it had
varied episodes with eps fixed, which is ≈ 1 by construction under pinned-once. Pop was not the lever.

Blind review B (`2026-09-10-pop-spearman-B.md`, closed 21:05Z) reproduced A's every number (‖g‖ to
0.05 %) and then overturned the instrument. E[g] ∝ μ at any noise level, so a two-seed cosine near zero
bounds one draw's signal-to-noise, not progress, and rank normalisation makes ‖g‖(P) blind to ‖μ‖. The
cosine resolves κ ≥ 0.161; the antisymmetric one-step test resolves κ ≥ 0.031 — **five times the
instrument** for 22 batch evaluations against A's ~2,900 member-generations. So B ran the test on the
remote with the arm's own trainer: P = 512, two seeds, a step of ‖d‖ = 0.2323 — exactly one Adam
generation at lr 0.003 — with 8 random ± pairs as controls, scored in-sample (159 episodes) and on the
held-out LIVE-C 43–72 (both seats, 60 games). **Every direction loses.** A random step costs 2.3 points
of in-sample win rate and **7.1 points held-out**; +d and −d both lose (curvature-dominated, as
corr(a⁺, a⁻) = +0.385 had predicted); the ES step is *worse* than random in-sample (19 %/38 % percentile,
its curvature part z −3.0/−1.1 — the estimator loads onto brittle directions) and marginally better
held-out (69 %/62 %) while still a net loss. κ measured directly: **+0.004 ± 0.009 in-sample, +0.011 ±
0.009 held-out**. And yet |∇F|·‖d‖ = 0.53/1.16 — the objective is steep; the estimate finds ~1 % of it.
flow172_g1000 is a sharp local maximum of the flow187 objective even on boards it never trained on. The
|g|-ranked `--train-only` subspace idea died in the same document: selection on noise, no concentration
at any scale.

### The lr decision, and flow188 → flow190

B priced one change. Net gain per step is h(κ|∇F| − Ch); the optimum h* is 0.024–0.083, i.e. **lr
0.0003–0.0011 against 0.003 today**, which is justified only at κ's 95 % upper bound. At 21:15Z flow188
hit its third straight refusal (g10 −2, g20 −1, g60 −4, at g178) and was replaced on GPU0 by **flow190**:
flow188 verbatim, `--lr 0.001`, seed 292 — an A/B with flow187 (lr 0.003, g182, gate g10 −2 / g70 +2 /
g160 +2, margin +1,948 → +2,692 rising) kept as the control on GPU1. Locally, flow189e had spent 40
minutes inside the gen-10 abs probe after two OOMs on the 8 GB card and was killed; **flow189f**
(`--abs-pairs 32`, lr 0.001, seed 293) became the second lr-0.001 arm and, at 22:14Z, the first local
arm past gen 10 after five OOM lineages (probe 602 s against 104 s/gen, 5.4 GB).

### Two process lessons: a lock and a clock

From 20:51Z to 21:10Z zero legs ran. `flock` reported the judge lock BUSY with no Linux holder, the lock
lived on the 9p drive, and I wrote it up as a leaked Windows-side handle, moved the lock to
`/root/kagg3_judge.lock`, killed the waiters and restarted the watcher. Ten minutes later the stall
recurred on ext4. The real cause was a **nested flock**: `S/gatecal/backfill.sh` wrapped `watch.sh
--legs` in its own `( flock 9; … ) 9>judge.lock` while `--legs` takes the same lock inside — the
wrapper held it and its own child waited forever, with the watcher's g160 judge queued behind. 9p locks
are merely invisible in `/proc/locks`. The fix is one line (call the self-locking script directly) and
the rule is simpler still: never wrap a self-locking script in the same lock (consensus §19). The
misdiagnosis cost twenty minutes of judge time and a half-true log line that had to be corrected.

The second lesson is smaller and more embarrassing. Seven verdict lines stamped 22:12Z…23:18Z had been
written with estimated times that ran up to **52 minutes ahead of UTC**; at 22:31Z they were re-anchored
to the watcher stamps and file mtimes (21:48…22:26Z). The rule since: read `date -u` before every line.

### Margin-scale and sigma: two non-levers, measured

B's one hypothesis (not a change) was that `--margin-scale 3000` saturates the sigmoid past ±9k, so the
ES ranks on a near-binary win bit — the only 4/4-consistent signal in its cells was on raw coins, κ
0.012–0.017. The A/B (`2026-09-11-margin-scale-AB.md`, 21:52Z) found the description **true** — 28 % of
member-episodes saturate at 3000, 20 % of antithetic twins on the same side, 0.2 % at 30k, none at
100k/linear — and the lever **false**: re-shaping the same P = 512 rollouts leaves the direction at cos
0.84–0.91 to the 3000 gradient, and κ does not rise (held-out +0.009/+0.014/+0.001/+0.004 for
3000/30k/100k/linear, se 0.009); the coin κ is flat and positive in 8/8 cells whatever the shaping. The
weak coin signal is a property of the step, not of the shaping. Sigma went the same way
(`2026-09-11-sigma-AB.md`, 22:22Z): σ ∈ {0.01, 0.02, 0.04, 0.08} at the same centre, held-out κ
+0.012/+0.008/−0.002/−0.005 with every |z| ≤ 1.45, all eight +d steps losing held-out win rate (−3…−13
points, 0.08 worst); σ 0.01's in-sample antisymmetry (z 3.9/5.0) is the −d side losing, not the +d side
gaining; cross-seed cos(g) ≤ 0.035 at every σ, ‖g‖·σ ≈ 1. The ES-knob ledger at g1000 read: pop no,
margin_scale no, sigma no, lr priced.

### The re-centre test: g940 has signal, g1000 is a reached peak

The knob ledger begged a question. Every knob was a non-lever *at flow172_g1000*, yet the lineage had
made real progress g60 → g940. Was the no-signal finding a property of the estimator, or of where we were
standing? B's rig was repeated at flow172_g400 and flow172_g940 (`2026-09-11-recentre-onestep.md`,
23:18Z). F(centre) is monotone up the lineage — held-out win 50.0 / 60.0 / 66.7 % — and **the ES step
has signal at g940 that it lacks at g1000**: in-sample κ 0.040 (z +3.1) against 0.009; the net step
F(+d) − F(c) at g940 is **+0.0067 in-sample / +0.0043 held-out, beating 16/16 random steps in both**
(margin +617 against random −121, z +2.4), where at g1000 it is −0.019 / −0.007. Random steps lose 44 %
of the time at g400, 94 % at g940 and **100 % at g1000**; the curvature term is 3× larger there; and
|∇F|·‖d‖ is equal at all three centres — the objective is not flatter at the top, the estimate simply
stops resolving it. The pop, sigma and margin-scale A/Bs had been run where there was nothing to find.
A second seed (9002, 00:19Z) replicated every row: held-out κ +0.035, net +0.0102, 16/16 randoms, margin
+466; pooled two seeds at g940 κ +0.039 ± 0.002 in-sample / +0.029 ± 0.007 held-out, margin +541 ± 75,
**32/32 randoms beaten held-out**; g1000 pooled κ ≤ 0.014, net gain negative in all six cells.

The agent recommended keeping init g1000 — it leads g940 by 6.7 held-out points and one g940 step
recovers only 1.7 — and changing the objective field instead. I did the opposite on one GPU and both on
the campaign. flow187 was over its 300-generation budget at g313 with three refusals and nothing since
g160, so at 23:18Z GPU1 went to **flow191**: the flow190 recipe from flow172_g940, seed 294 (consensus
§20). The reasoning: the card was otherwise idle, and flow191 is the empirical form of the agent's own
counterfactual — does a climb from g940 under the target-band objective retrace to the g1000 hilltop
(records ≤ base) or reach a different, higher point (records above the shipped base on the legs)? It is
falsifiable at its g100/g200 records. Its gen-0 seat read 58.1 % / +1,909 on the 124-game gate field,
eleven wins below the g1000 seat, as the test predicted.

### Three changed fields, one ledger

The agent's principled lever — a field where g1000 is not already a peak — was then tried three ways on
B's rig, each with the same rule: stage flow192 only on held-out gain > 0 and ≥ 12/16 randoms beaten.

**Lost boards** (`2026-09-11-lost-board-objective.md`, 23:47Z). g1000 loses 41 of 147 pinned rungs
(13/20 top-ten, 11/42 LIVE-C), already 38 % of the objective mass; W_lost (lost ×4, barely-won ×2, won
×0.5) took that to 79 %. It turned the direction 26° (cos 0.87–0.90) and resolved an in-sample gradient
on the new field (κ 0.024/0.037) — and **held-out the W_lost step lost on both seeds and by more than the
current step** (obj −0.034/−0.015 vs −0.006/−0.012; win −6.7/−10.0 vs −3.3/−6.7 points), flipping 0/30
held-out losses up and paying 10/7 previously-won rungs for 2/3 recovered ones. **Seat swap**
(`2026-09-11-seat-swap-objective.md`, 00:25Z) died on a fact about the trainer: it already alternates
the pinned seat every generation (`pinned_seats = (t+i) % 2`), so the other seat is the same field —
per-rung margins correlate 0.994 across seats, cos(g_seat0, g_seat1) = +0.98 on both seeds, every step
loses held-out. **Fresh boards** (`2026-09-11-fresh-board-objective.md`, 01:54Z) was the honest version:
the 30 new LIVE-C tapes (below) added as weight-4 rungs are a real change — the centre loses the same
9/30 in the sim as in the engine — but they rotate the gradient only 11° (cos 0.983, 18 % of the mass),
and the held-out step still loses (obj −0.012, win −6.7 points against A's −0.007, −3.3). On the fresh
slice both directions gain margin (z +2.0…+3.5) — the g1000 direction generalising to boards it already
wins, not the rungs teaching anything. **Ledger closed (consensus §23): re-weight, re-seat, fresh boards,
all negative; the g1000 objective is not to be changed further.**

### LIVE-C to 102 boards, and a fourth leg

Between the seat-swap and fresh-board streams, the stop rule got the power the inventory said it
lacked. Thirty fresh pinned-town tapes were cut from the live entry's latest ladder games (sub 56140532,
opponents 2512–2685, live 20W-10L, created 19:12Z…00:08Z), 30/30 coin-exact, town schedules 352 → 382,
base csv 144 → 204 rows with the existing rows byte-identical (`2026-09-11-livec-extension.md`, 00:34Z).
The shipped base reads **70.0 % / +5,694 on ids 73–102** against 63.3 % / +2,951 on 43–72 — the highest
of any set, because these are the most recent opponents the live file has been beating. The auto-judge
now runs **four legs** for the hold-out arms (TOPB2, LIVEC-H30, LIVEC-H30B, LIVE62), the held-out line
is 60 boards / 120 games, and the rule reads the pooled 43–102: ≥ +5 points there, LIVE62 ≥ base, TOPB2
not down. Two tooling defects surfaced on the way (a hard-coded `FIRST=62` and a wiped scratchpad path
in `extend_new.sh`; a repro gate that depended on a missing `bc`) and a third the next hour, when the
H30 leg ran ids 43–102 because `run_holdout.sh` had no upper bound — capped at 72 so the halves stay
disjoint.

### The first theta to pass

flow187's g160 record had been judged at 21:27Z on three legs: TOPB2 25.0 → 25.0 % (+610, t 1.3),
hold-out 43–72 63.3 → 66.7 % (+6/−4, +218), LIVE62 88.7 → 90.3 % (+4/−2, +614, t 2.0). Level-to-up on
every leg, none down, the first flow187 record that was non-negative everywhere — and **+3.3 hold-out
points, short of the +5 rule**. The backfill around it was a clean ledger: g10 and g70 down, flow188's
g10/g20/g60 down, six correct refusals and zero false ones at lr 0.003.

At 00:36Z the fourth leg ran on it. **LIVEC-H30B 70.0 → 80.0 %, +6/−0, +761, board-t 2.1.** Pooled
hold-out 43–102: 40/60 → 44/60, **66.7 → 73.3 % (+6.7 points, flips +12/−4, sign p ≈ 0.04)**; LIVE62
+1.6 (+4/−2, t 2.0); TOPB2 level (+610). All three clauses of the stop rule true — the first candidate
in the campaign to pass it. Against the theta actually on the ladder (g940_pair) the read is stronger:
LIVE62 **80.6 → 90.3 % (+12/−0, +1,258/game, t 4.3)**, hold-out 43–72 58.3 → 66.7 % (+6/−1, +1,349, t
2.5), TOPB2 level (+1,245, t 1.9, no drops) — and for scale the hr base itself reads only +644 (t 2.2)
over g940_pair on LIVE62. Caveats stated with it: first use of the 60-board rule, and the base it passed
against (g1000 + hr) trails g940_pair on the ladder (2522 vs 2622).

Packaged at 00:39Z from the `ship-pair-hr` worktree (commit b1bde4f: OPEN_PUMP / TAIL_FILL /
BANK_BEFORE_LOT / HIRE_ROW defaults) as `dist/submission_flow187_g160_hr.tar.gz`, md5 **`3ec658f2`**,
23 entries in the layout of the hr package. Smoke at 00:53Z: the package in our seat on the 62 LIVE
boards, **124/124 coin-exact** against the judge csv, 112 wins both, mean 106,615 both. Handed to the
user at 00:57Z as the replacement for the hr sub 56143250 (the weaker of the two active files), keeping
56140532. The falsifier: at least the g940_pair rating at the same game count by game 60. The theta
itself deserves the note: the remote gate had **refused** it at net +2. Under the pre-20:49Z watcher it
would never have been judged.

### The tail, the lottery, and re-seeding

flow187 had been killed at g313 with no record after g160, so its periodic checkpoints were fetched and
judged on four legs. **g200: level-to-down** (hold-out 43–72 60.0 %, fresh 70 → 70, LIVE62 +2/−8).
**g300: level-to-down** (LIVE62 +4/−10). **g313, the final theta: down on every leg** (LIVE62 88.7 →
83.9 %, 0/−6, t −2.2). The arm ended below where it started and g160 was its peak. This is review B's
diffusion picture read off the arm itself: at lr 0.003 the walk reaches a gate-filtered high point and
walks off it within 40 generations; the record cadence (`--abs-every 10`) is right, and the gap that
matters is the checkpoints between records — g160 → g200 had none. The fresh-board tally across all
eight records made the same point from the other side: 187 g160 **+6/−0**, 187 g70 +4/−2, 191 g20 +2/−0,
190 g150 +4/−0, 190 g50 0/−2, and every g10 level — the new boards discriminate and are not a free win
field, and only the flow187 lineage was up on both hold-out halves.

The lr A/B closed against B's priced optimum. flow190 (lr 0.001 from g1000) reached three straight
refusals (g10 −3, g50 −2, g150 −6, all level-to-down locally — g150: LIVE62 +4/−10) with no record after
g150, and was killed at g210 at 01:32Z; flow189f (lr 0.001, local) had one record in 118 generations,
g10, level-to-down. **328 arm-generations at lr 0.001 produced no record ≥ base; lr 0.003 produced the
theta that passed.** B's pricing assumed a fixed κ; what the arms actually harvest is gate-filtered
draws, and those favour the larger step (consensus §17 row 2). Both slots were re-seeded from the only
theta that passed: **flow193** on GPU0 (flow187 recipe verbatim, lr 0.003, seed 296, init flow187_g160
md5 9dfb20c2; gen-1 mean_win 0.601 against flow187's 0.557 from g1000) and **flow194** locally (the same
with seed 297 and `--abs-pairs 32`) — two independent lottery draws around g160, every record judged on
four legs against the shipped base.

### Where this leaves the campaign

At 01:32Z the ladder read g940_pair **2621** (peak 2617.9 → 2621.0 across the night's firings) and the hr
file 2542.7, against a top-ten cutoff last read at **2939–2944** on the leaderboard and ≈ 2951 on the
calibration line — the target that needs LIVE-C ≈ 80 % against the shipped 63–70 %. The candidate
`3ec658f2` is with the user, not yet uploaded; its falsifier is ≥ the g940_pair rating at the same game
count by game 60, and the ladder-calibration refit (`2026-09-11-ladder-calibration.md`, in flight) will
put bands on that at games 40/60/100. Three arms run: **flow193** (GPU0, g160 seed, lr 0.003),
**flow191** (GPU1, the g940 re-centre, g50/g100 records due), **flow194** (local, g160 seed). The rig
streams are closed — pop, sigma, margin-scale, three objective fields — and the honest summary of the
night is that the estimator has no resolvable gradient at the peak we shipped from, that the gains we
have came from a filtered lottery judged on held-out boards, and that the judge is now wide enough (112
independent boards, four legs, every record) to tell a draw from a step.

## 2026-09-11 morning — what the top of the ladder actually is

Candidate B (flow193 g100 + hr switches) went live as sub 56161192 at 07:41Z; Kaggle retired the higher-rated g940_pair entry rather than the hr one, so the public score dipped to 2547 while B climbs (20-4 at 2189 by 09:05Z). Three arms now run a clean design off the same seed theta: flow196 (control, GPU0), flow197 (42 fresh mid-band training boards replacing the memorised LIVE-C 1-42, GPU1, launched 09:00Z), flow198 (20 fresh top-tier tapes replacing the fixed top-ten rungs, local, queued). The judge pairs every record against B now; flow196's g10 and g60 are both below B.

Three measurements changed the picture of the opposition (docs/strategy/2026-09-11-spataro-vs-ours.md, -majkel-vs-spataro.md, -labour-compounding.md; consensus §28-§30):

1. **Rank 1 is a streak artefact.** SpaTaro's 3108 rests on a 30-0 opening run; its form is 76-78 % against 2850-3050 and 0-5 against the two files above 3050. Majkel1337 (3092, rising) and feel the agi are the form leaders.
2. **The top tier is one template, won on spend.** Majkel runs SpaTaro's farm line for line — purse to zero nightly for nine days, 12-melon pot dumped day 10, herd from hour 0, 200+ sell turns — and beats it 6-0 without out-earning it: it buys 4-7k of feed wheat where SpaTaro buys 14-22k, holds strawberry off the day-20 collapse, grows tomato, and is behind at day 10 in every game and ahead from day 11 in every game. Market attacks between them are worth about 20 coins.
3. **Labour does not compound; capital does.** Hire cost is Fibonacci per hire-of-day with no wage and a nightly reset. SpaTaro's six day-0 hands pass 41-47 % of their turns; ours are the busiest hands of the three files. The top files' day 11-20 edge is coins per productive hand-hour — more standing tiles and animals per hand — and our measurable slack is 0.6-5.7k of cash idle overnight on days 2-9 against their 0-200. This closes the "hire earlier" family for good (FORWARD_ADMIT dead ×3) and opens a narrower one: spend the leftover purse on work legal today. IDLE_PURSE_TOPUP_ON was built (identity byte-exact), judged paired on B's theta and killed the same morning: the "idle cash" is revenue landing after the day's single BUY row (4-108 coins actually spendable at the row on days 1-6, 0-3 free tiles), so the switch had nothing to buy; forcing it displaced plantings and handed 3k to the opponent. The hand-and-purse family is closed; the residual is architectural (one BUY row a day) and needs free tiles to matter.

Time projection at the measured pace (§26): top 10 by 09-23 near 30 %, top 5 near 10-15 %, top 1 not by this mechanism.

**2026-09-11T10:05Z — the counter class that wasn't.** B's ten ladder losses to 2175-2381 files re-played 1/20 on pinned towns, and for an hour the log called it a counter class the judge had never sampled. The anatomy (§33) dissolved it: one public clone under ten names, the same file B beats under 2500-2600 names; the ten towns are the ones where the pizza shop comes late, so our tomato recovery never arrives and the clone's d10 melon pot stands. Lesson kept: a loss-selected board set measures the selection, not the opponent. What survives is useful — a fifth judge leg made of the coin-flip half of the ladder, flow199 with those towns at band weight, and one open ledger question (why our fertilizer runs at half the clone's with more cows).

**2026-09-11T10:26Z — the field in thirteen templates.** At the user's request an agent read one to two wins from each of the top 50 files and sorted them by their first two days of actions: half the top 50 is the public clone we already train against, the rest fall into a dozen variants and five singletons, and only the two leaders adapt to anything. Nine of the new shapes became pinned-town tapes, and flow200 stages them next to the loss towns at band weight, so the next arm trains against the whole ladder rather than the one clone.

**The control arm that went nowhere (2026-09-11T10:49Z).** We asked the simplest question in the book: if candidate B's own recipe is just continued from B, does it climb? Three paired reads in 172 generations said no — the g10 and g60 records and the g100 snapshot all sat below B on every leg, and the remote gate refused every candidate along the way. That is the third-loss rule, so flow196 came off GPU0 and flow200 took its place: the same seed and recipe, but with the ten LOSS10 towns and the nine new-template tapes from the top-50 catalogue in the training mix. Whatever the ladder still has to teach us, it will come from changing what the population plays against, not from more generations of the same boards.

**Was the judge lying to us? (2026-09-11T10:59Z)** B went live and its rating sat two hundred points below the file it replaced, then lost three ladder games in a row. Before touching a switch we did the only honest thing: we took every one of B's fifty ladder games, pinned each town, replayed each opponent's exact actions, and put B, the old file and candidate A in B's seat. B reproduced the ladder to the game, fifty out of fifty. The old file lost three of B's wins and won none of B's losses, six flips against it across both seats; A was level. The rating gap was Elo bookkeeping — seventeen placement wins that pay nothing and a young rating — not strength. The judge stands, and we have forty new tapes of the opponents the ladder actually deals us.

**Two arms down, one question answered (2026-09-11T12:12Z).** The rotation arm followed the control arm out: three reads below B, each gaining on the boards it trained near and losing on the ones it never saw. Its GPU went to flow201, whose rungs are the forty opponents the ladder actually dealt B. And the question that started the morning — is B really weaker than the file it replaced? — got the strongest answer we can give: on the sixty boards hr itself just played against 2400-2650 opponents, B wins forty-three where hr won thirty-five, flipping ten of hr's losses and giving back two. The old file loses to B at every rating band, most of all at the top. The judge was right; the ladder is slow.
