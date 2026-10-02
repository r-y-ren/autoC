# How we built the agent

State of the campaign at 2026-09-08 09:25Z. Repo HEAD `0a933e5`.

Sources: `docs/strategy/2026-09-05-build-story.md` (the chronological log, entries
for 2026-09-05 through 2026-09-08), the dated verdict lines in `S/glut/verdicts.log`,
and the memory index. Every number below is quoted from one of those; where the log is
ambiguous, this document says so.

This is the narrative for a reader who knows the game but did not watch the work: what
the objective was, how we learned to measure it, what failed, what finally moved, and
what is still open.

---

## 1. The objective, and the measurement discipline that took a week to build

The target is the Kaggle leaderboard: top 10 by 2026-09-23, with the top-5 rating around
2891 and the top-10 cutoff around 2880. The standing generality clause is that the agent
must beat *any* opponent, not one tape: the immutable `kagg2` yardstick and the
archetype opponents are regression tests, never the objective.

The single most valuable thing we built is not a policy. It is the protocol.

**Paired real-engine boards, win rate first.** A candidate is judged against the
currently live build on *identical* boards, with `--seed-per-opponent`, across six legs:

| leg | opponents | n boards |
|---|---|---|
| band6 @777001 | 6 band tapes | 192 |
| band6 @777002 | same, second seed base | 192 |
| top10 @777001 | 20 top-10 tapes | 640 |
| jesse4 @777001 | 4 hard clone variants | 128 |
| flood6 @777001 | 6 flood tapes | 96 |
| today41 @777001 | 41 tapes cut from the live sub's own losses | 656 |
| **pooled** | | **1,904** |

The promotion bar has not changed since 2026-09-05: **band level or better, top-10 up,
flood not worse, all paired, across at least three seed bases**, with win rate read
before margin. A remote gate acceptance is a nomination, never a promotion. Two
candidates in the campaign (flow93_g10, flow112_g10) were promoted by a gate and later
found to lose 5 to 9 points locally, which is why the rule exists.

**The shop lottery, and why a cheap screen had to be validated before it could be
trusted.** The engine's only RNG is `Random((seed * 1_000_003) ^ day)` at end of day. It
is consumed by **one draw per empty tile, ours then theirs**, before
`rng.choice(sorted(SHOPS))` every third day. So any lever that changes our empty-tile
count re-rolls every later shop. Reproduced 8 out of 8: before the first divergent shop
draw the opponent's coins move by +27 / +4 / +11 / +2; after it, by +27.4k / -4.4k /
-2.8k / +25.8k. YARN_STORE, the only wool sink, pays the clone 25k to 27k on its own.
Practical consequence: every ON/OFF pair carries an unpaired, zero-mean plus or minus 25k
term whenever tile usage differs. Engine board-level sd is about 8k. A `t` above 5
survives it; anything under 3 may be lottery.

The fix was `--shop-crn` (draw the shop from stream word 400, past the weed walk; OFF
stays byte-exact). Combined with the byte-exact action-replay opponent seat, this gave a
simulator that **is** the engine: margin sign agrees on 99.5 % of games, 82.5 % of games
are byte-exact on final coins, Spearman .9997. Under CRN the paired sd falls 5.4x (8,374
to 1,441) and the episodes needed to reach |t| = 2 per pair fall from 295 to 41. A
planner switch can be screened on 576 paired boards in about five minutes, roughly 26x
cheaper than engine legs.

The screen was validated, not assumed. It reproduced the `passa` engine legs
board-for-board (163 of 192 band6 boards byte-exact) and, when re-run on the eleven
already-rejected hand levers, confirmed every one of them as a genuine loss rather than a
lottery artefact. It also demoted one of its own headline results: `passa`'s "+766 /
+6.2 pts on jesse4" collapsed to -161 (t -1.1) once the shop draw was held fixed. The
headline had been the yarn lottery.

**The two-purse rule**, adopted 2026-09-08 after the reservation-floor failure: read our
purse and the opponent's purse separately, before the margin. Two distinct failure
signatures recur, and the margin alone hides both. *Displacement*: our own purse falls
because a mix rewrite conserves tiles, so the new crop comes off a better one.
*Denial handed back*: our purse is flat and the opponent's rises, because we moved
resources out of the window where our activity was suppressing their quotes.

**Counterfactuals overstate.** A ledger, a regression over finished games, or a price
model is a hypothesis with a number attached. Only a paired engine run counts, and the
sign flips often enough that this has become a standing rule.

---

## 2. What did not work

### 2a. Seventeen sizing and structural hand levers

Every one measured paired, most with double-digit `t`. A representative sample:

| lever | result |
|---|---|
| MELON_OPEN_ON (12 melon at day 0) | band6 54.2 to **15.1 %**, -17,554, t -12.8 |
| MELON_D10 / D10B (clone's melon clock) | 17.2 % (-18.6k, t -13.6) / **13.0 %** (t -15.5) |
| Crew ramp to the clone's curve (`ramp11`) | band6 55.0 to 52.5 %; top10 69.4 to 55.6 %, t -3.0 |
| QUAD3 early land | day-8 band6 47.9 % (t -4.0); day-6 44.3 %; day-10 inert |
| LATE_SHEEP_CAP day 11 | band6 54.2 to 42.7 % (t -7.3); top10 45.5 % (t -8.8) |
| JOINT_PLATE (plate + herd floors + crew target) | band6 54.2 to **1.0 %**, -41.9k, t -27; at half scale 13.0 % |
| CREW_FROM_TASKS (crew from `n_tasks0`) | per-hand 5: 51.6 to 39.8 % (t -28); per-hand 4: 16.3 %; per-hand 7: level |
| WOOL_DUMP d13, DROP_EARLY, pump-aware row | **inert**, 192/192 or 392/392 pairs byte-identical |

Two mechanisms explain nearly all of them. First, **the crew follows the plate**: hires
are an enumerated argmax capped by task count, never by cash, and the admission cap
`n_adm <= n_tasks0` means any hand beyond the gene's ramp simply PASSes. Forcing the
clone's hand curve raised PASS from 15 % to 37 % of unit-turns and cut revenue from
112.8k to 67.3k, while the hire bills came off the purse that prices land, so the third
quadrant was never bought. Labour is not this planner's binding constraint; the admitted
task list is. Second, **the pot is shared**, so a change that earns us coins usually
earns the opponent more.

The lesson that came out of JOINT_PLATE, at the fifteenth lever: *sizing targets cannot
be written above `_derive`*. Every crew, land and plate number has to come from the task
list after derivation, or the planner buys capacity it never uses.

A note on the count. The log's own tally is basis-dependent: on 2026-09-05 it reads 7 at
16:56Z and 11 by 20:12Z depending on whether the two sell-lot modes are one lever or two.
The figure "17" comes from the 2026-09-07 08:00Z entry, which calls CREW_FROM_TASKS the
seventeenth and describes the knob sweep as the "first positive lever in 17".

### 2b. The admit/route sweep: the first positive sim lever, level in the engine

With the CRN screen working, we swept 24 `plan.py` constants over 58 legs. Most were
inert or already at a sharp optimum. Four moved: `EST_HOME` 3 to 7 (+285, t 11.0),
`ADMIT_ROUNDS` 3 to 6 or 8, `ADMIT_PICK_SHARED=True` (+173, t 3.5), `TAIL_CARE_HOPS=2`.
The joint setting `ADMIT_PICK_SHARED + EST_HOME=7` scored band6 51.6 to 54.7 % (+427,
t 8.1) in the sim, the first positive planner lever of the campaign. Then the engine:

| leg | n | win OFF to ON | margin | t |
|---|---|---|---|---|
| band6 @777001 | 192 | 54.2 to 47.4 | -630 | -1.1 |
| top10 @777001 | 640 | 48.1 to 50.2 | +294 | +0.9 |
| band6 @777002 | 192 | 49.0 to 52.6 | +92 | +0.2 |
| jesse4 @777001 | 128 | 60.2 to 60.2 | -506 | -0.8 |
| flood6 @777001 | 96 | 59.4 to 59.4 | +491 | +0.5 |
| today41 @777001 | 656 | 55.2 to 53.0 | +444 | +1.4 |
| **pooled** | **1,904** | **52.6 to 52.3** | **+188** | **+1.0** |

Level. Band6 across both bases came out -269 plus or minus 412, which is 1.7 se below the
sim's +427. Not promoted; parked as a free rider. The calibration this bought is worth
keeping: **a sim lever needs about +800 per board to be confirmable in the engine at
n around 2,000**, or it needs a 5,000-board run. A fine sweep around the joint optimum
found nothing better, and the admit/route stage was closed.

### 2c. Five shop-rule and mix levers, all with the displacement signature

The top-5 agents visibly adapt to the shop draw. Each rule was rebuilt and screened.

| lever | result | why |
|---|---|---|
| CARROT_SINK (tiles per carrot sink) | PER=20: band6 51.6 to 27.8 % (-9,283); PER=3: 47.2 % (-1,608, t -10) | loss is our own purse, and it *grows* with the sink count; keiz holds about 3 tiles per sink, plants day 17, sells day 26 |
| TOMATO_GATE (no tomato under 2 buyers) | band6 -135 (t -4.1); jesse4 -130 (t -4.2) | 2-buyer boards inert, 0-buyer boards already abstained; the whole loss is 1-buyer towns, a real pot |
| ENDGAME_TOMATO tiles 12 / 16 | 47.9 % (-1,300) / 46.9 % (-1,721) | dose-responsive loss |
| Herd latency (lock herd to sinks) | full rule 51.6 to 37.2 % (-5,779, t -20); slope-only +363 (t 4.8), day-15 gate +261 | slope arm is pure denial, ours flat and theirs -369; a third of the +800 bar |
| STRAW_FIRST (14 strawberry by day 6) | LIVE base 51.6 to 40.8 % (-4,891, t -17); on gen-100 73.1 to 56.8 %, clone **+2,770** | the plant leg is the whole loss; the sell leg is byte-inert because this build already sells ripe strawberry same day |

The family closed on 2026-09-07. The general finding: the top agents' shop rules describe
their season, not a marginal tile in ours. And the ES theta reached the same strawberry
tile count while planting *more* wheat, paid for by earlier hiring and more unit moves, a
joint change the hand mix chain cannot express.

### 2d. The reservation floor: denial handed back

Copying gen-130's carrot re-timing into an explicit hold (carrot below 1.25x to 2x base
in days 10 to 24, then liquidate):

| base | 1.25x | 1.5x | 2x |
|---|---|---|---|
| LIVE | -66 (t -1.5) | -248 (t -4.3) | -445 (t -5.4) |
| gen-130 | | -458 (t -8.3) | -646 (t -9.7) |

Window-insensitive, monotone in the dose. Our purse flat (-140 to +43), the clone's purse
**up** on every leg (+109 to +506). Deferring carrot cash out of days 10 to 24 starves the
hires and land that were suppressing the clone's strawberry and wool quotes. On gen-130
it loses 2.6x harder because that theta's sell gate already holds carrot. This is the
lever that produced the two-purse rule.

### 2e. The ES arms that were noise

Twelve consecutive arms (flow96 through flow111) produced "records" that the local
protocol rejected. Four separate defects, found over three days:

1. **The gradient was a coin flip.** In the 535-coordinate bias space the arms were
   training, sign agreement at sigma 0.02 was 0.37 to 0.44, which is chance. The
   0.734-agreement result that had justified the setting had been measured with
   `train_only="all"`, the full 4,188-coordinate theta.
2. **The gate compared unpaired means** and, on the replicate round, replayed only the
   candidate. One round where LIVE happened to score 39.2 % promoted a theta that lost
   8.7 points locally. Both fixed (`a65af1c`, `f3e6bfc`).
3. **The fitness was a different game.** The old "tape rung" was a market-flow surrogate:
   sim-vs-engine margin correlated only Spearman 0.25 per theta. The sim-chosen theta
   realised exactly always-LIVE on the engine.
4. **The arch-frac bug.** `--arch-frac 0.0` gives the archetype block, where every action
   tape rung lives, **zero episode slots** (`src/kagg3/es/train.py:583`). flow123 through
   flow127 therefore trained on 100 % self-play; their rung weights were inert and the
   logged win rate was self-play win. flow114 through flow122 had only 25 % tape slots.
   Every "ES on action tapes is board-specific or flat" verdict from flow123 onward is
   void. The local audits (`S/escurve`, `S/esstep*`, `S/crn*`) ran at `arch_frac 1.0` and
   still stand.

There is also a genuine negative result underneath all this, and it should not be lost:
the CRN gradient in the full theta space is reproducible (half-split Spearman 0.83 at
E = 512) but a single step from LIVE **never beat a norm-matched random step** on fresh
boards. What eventually worked was not a better gradient estimate at one point. It was
many generations of selection against an honest fitness.

---

## 3. What worked

### 3a. Action-tape rungs plus the arch-frac fix

The action-replay opponent seat (`src/kagg3/es/tape_actions.py`) cuts a packaged Kaggle
tape's 719 frames into day-major int32 op tables spliced into `rollout.run_day`. Parity
is byte-exact on 8 of 8 boards for one tape, 7 of 8 for another. With
`--arch-frac 0.9`, the four archetypes weighted 0 and `--stall-sigma-mult 1.0`, flow128
and flow129 became the first remote arms since flow122 whose fitness was the engine's
verdict against real Kaggle opponents. flow128's generation-1 population mean win against
47 live tape rungs was 0.329, a real tape number for the first time.

The result arrived within 40 generations.

### 3b. The promoted sequence

All figures are win rate versus the live build (`flow102_g280`), six legs, 1,904 paired
boards.

| leg (LIVE baseline) | flow129 g40 | flow129 g100 | flow129 g180 | flow130 g130 |
|---|---|---|---|---|
| band6, both bases (51.6) | 59.1 | 68.8 | 72.4 | **75.3** |
| top10 (48.1) | 58.3 | 66.9 | 65.2 | **71.7** |
| jesse4 (60.2) | 78.9 | 81.2 | 81.2 | 78.1 |
| flood6 (59.4) | 60.4 | 68.8 | **80.2** | 78.1 |
| today41 (55.2) | 61.3 | 70.1 | 72.1 | **76.1** |
| **pooled (52.6)** | **61.0** | **69.4** | **70.9** | **74.7** |
| gain in win points | +8.4 | +16.8 | +18.3 | **+22.1** |
| margin per game | +1,710 | +3,731 | +4,278 | **+5,819** |
| pooled t | 4.1 | 9.2 | 10.1 | **14.2** |

Head to head on the same boards: g100 beats g40 by +7.7 points (t 4.8); g180 beats g100 by
+1.3 points (t 1.1, inside noise); g130 beats g180 by +3.8 points and +1,664 per game
(t 4.7), significant on top10 (+6.5) and today's losses (+4.0), and beats g100 by +5.1
points (t 6.4). The remote gate and the local engine agree: flow130's g231 gate
replicated the g130 record at 75.1 % pooled 77.1 %, against 74.7 % locally.

Artefacts: `dist/submission_flow130_g130.tar.gz`, md5 `8abf84daa6125601416d31234f02fadd`,
sha256 `1c5cacf0...`, theta md5 `8b7b0c29`, saved as
`artifacts/kagg2_games/thetas/flow130_g130.npy`. The three flow129 thetas are alongside it
(`flow129_g40.npy`, `flow129_g100.npy`, `flow129_g180.npy`), with packages
`dist/submission_flow129_g40.tar.gz` (md5 `0d5539f4`),
`dist/submission_flow129_g100.tar.gz` (md5 `5a6967b6`) and
`dist/submission_flow129_g180.tar.gz` (md5 `aa68182a`). Smoke for g130: 8 games, 720
steps, DONE/DONE, 0 nulls, 4/4 versus tape 105443859 (+8,732) and 4/4 versus the starter.

### 3c. Weight decay, and where the gain actually lives

The autopsy of g40 found the promoted theta was **0.898 x LIVE plus a residual**
(correlation 0.996, residual rms 0.021). The shrink is exactly `--weight-decay 0.003`
compounded over 40 generations (0.997^40 = 0.887). Screened alone, 0.90 x LIVE scores
40.1 % (-4,953, t -12) and 0.80 x scores -9,182: the decay costs about 470 per game per
1 % of shrink, and the ES residual re-earns about 7.7k to net +2.8k. The obvious repair,
scaling a promoted theta back toward LIVE's norm, is dose-negative: g100 x 1.1 scores
73.1 to 57.6 % (-5,265, t -17). The residual is adapted to the shrunken scale.

flow130 was launched from flow129's post-g100 record with decay off. Over 130 generations
its scale stopped moving (alpha 1.0095, 100 % direction) and it produced the best theta of
the campaign. The rule adopted: **weight decay 0, initialise from the best
engine-verified theta**. A control arm with decay 0.0015 resumed from g180 (flow132) was
killed at generation 39 for continuing to pay the shrink tax.

The head-group attribution study (23 candidates on 384 shared CRN boards) says the gain
cannot be decomposed:

| probe | effect |
|---|---|
| remove any one head group from g180 | costs +1.4k to +25.7k |
| add any one group alone to LIVE | loses -1.1k to -21.9k |
| sum of parts versus the whole | overshoots 9x in both directions |
| pure contraction (0.625 x LIVE) | -17.9k |
| pure direction, no contraction | -21.4k |
| both together | **+5.1k** |
| step-scale ridge 0.5d / g40 / g100 / g180 / 1.5d | +1.8k / +2.6k / +4.7k / +5.1k / **-22.6k** |

The gain is joint, and it sits on a ridge with a cliff half a step away. Two direct
recommendations followed and were adopted: no `--train-only` arm (biases alone read
-1.6k), and do not raise sigma, since 0.02 already gives a perturbation norm of about 1.3,
comparable to a whole DRAIN-sized move.

### 3d. What the thetas actually learned

**Generations 40 to 180: denial.** Across 28 paired replays, the tape opponents sell
*identical unit counts*; their entire loss is price. Strawberry accounts for -8,552 of it
(261 units, 121.6 down to 88.9, about 80 % of their -10.6k), wool for -2,845. The theta
gets there by planting 14 strawberry by day 6 instead of 9 and selling 17 more units in
days 12 to 17 and 43 fewer after day 18: **first into the contested pot, out before the
clone's day 15 to 22 dump**. It funds this with 430 more early hiring and 47 more unit
moves, and it gives up late strawberry, tomato (8.1 to 5.7 tiles) and three sheep, buying
instead in the crops nobody contests: egg +3,500 (geese 1.6 to 3.9), milk +1,271, carrot
+997. Through this phase our own purse was falling too, just more slowly than theirs
(g40: ours -1.5k, theirs -3.2k).

**Generation 130: the own purse comes back.** The g100-to-g130 autopsy on 1,904 boards
reads our purse **+1,722** (t 3.6) with theirs unchanged (-351, effectively zero). It keeps
all of the denial and adds our side back. On the 800 boards outside both rung sets the
gain is +1,963 (t 3.6), so this is not rung memorisation. The mechanism is carrot sell
timing: the clone sells about 10 carrot all game, so *our* supply sets the quote. Gen-130
withholds about 11 units through days 10 to 20 (quote 44 to 62 to 84), plants 3.6 more
seed in days 23 to 27, hires 2.3 more after day 24, and sells 61 units at 83 in days 25 to
29 against gen-100's 33 at 61, worth +3,025 per game. The wheat lump is broken across days
18 to 28 (+871) and melon moves two days earlier (+890), funded by dropping the strawberry
tail, tomato and one cow (about -2k). It is a later, more patient liquidation.
`cos(g130 - g100, g100 - LIVE) = +0.33`: a new direction, not more of the same.

**Generality.** The gain is not confined to the clone family it trained on.

| yardstick | n | LIVE | gen-130 (or gen-180) | gain |
|---|---|---|---|---|
| panel24, 24 older and varied tapes (gen-180) | 384 | 86.2 % | 93.0 % | +6.8 pts (+2,135, t 1.9) |
| freshest 32 loss tapes, cut after today41 | 512 | 48.4 % | 72.9 % | +24.5 pts (+6,551, t 8.0) |
| kagg2 + wheat_clone_v3 + wool_specialist_v2 | 96 | 100 % | 100 % | level (margin -1,203, t -0.5) |

The freshest-field number is also the diagnosis of the live submission's slide: LIVE reads
only 48.4 % against the newest opponents.

---

## 4. The current recipe and what is running

| setting | value |
|---|---|
| rungs | 41 Kaggle-loss action tapes of sub 56028553, weight 1, plus band6, weight 1 |
| archetypes | four archetypes present but weighted 0, `--arch-frac 0.9` |
| sigma | 0.02, `--stall-sigma-mult 1.0` (no re-centre bump) |
| population | 512 |
| episodes per member | 256 |
| common random numbers | `--shop-crn` (shop drawn from stream word 400) |
| gate | paired-t on identical (seed, opponent, seat) rows, with a paired replicate |
| weight decay | **0** |
| init | the best engine-verified theta, not a cold start |

Running as of 2026-09-08 06:55Z:

* **flow130** (GPU0), the arm that produced g130, continuing past generation 200 on the
  loss-tapes plus band6 rungs with decay off.
* **flow131** (GPU1, seed 231), launched 06:40Z: the flow130 recipe plus **26 cow-clone
  tapes at rung weight 2**, decay 0, initialised from `flow130_g130`. The rung choice comes
  from the loss autopsy, which found a family-level split under gen-100: cow clone 60.8 %
  versus sheep clone 70.4 % (z 2.4).
* Killed: flow129 at generation 358 (population mean win 0.47 and falling, records banked),
  flow132 at generation 39 (decay 0.0015 from an alpha-0.63 theta).

The recommended upload is `dist/submission_flow130_g130.tar.gz`. It supersedes g180 and
g100 even at the cost of a rating restart, since a Kaggle resubmission restarts the rating
and the head-to-head margin over g180 is significant.

---

## 5. Open questions, honestly stated

**Gate resolution and mirror seats.** The gen-100 loss autopsy found that mirror seats are
bit-identical in 69 % of pairs, so the gate's effective sample is roughly half its nominal
n. The recommendation is to double `--games` for the same wall clock, moving the gate CI
from about plus or minus 24 points to plus or minus 17. The log records this as a
recommendation; it does not record it landing. Until it does, gate verdicts on close
candidates stay weak, which is exactly the failure mode that produced flow125's sub-LIVE
incumbent.

**How much of the early gain was contraction.** The head attribution says pure contraction
alone is -17.9k and pure direction alone -21.4k, but the two together are +5.1k. So the
shrink that weight decay produced was part of the working theta, not simply a tax, even
though decay was costing about 470 per game per 1 % and even though scaling a theta back
after the fact is dose-negative. The campaign's answer, decay 0 from a shrunken init, is
supported by g130 but not cleanly: flow130's own generation-40 record was *level with its
starting theta*, so 40 decay-free generations added nothing the engine could see, and the
gain only appeared by generation 130. Whether decay 0 is right in general, or right only
because the init already carried a 0.77 shrink, is not settled by anything in the log.

**The late-seed lever is base-specific.** Planting a few extra carrot seeds on empty tiles
in days 23 to 27, with no sell-side change, is the first hand lever in the campaign with
the target signature: on LIVE, +3.1 win points and +247 per board, our purse up, the
opponent's untouched, dose-flat because the empty ground binds before the knob. On gen-130
it is -234 (t -6.6), because that theta already claims the late ground (seed 35.8 to 39.4).
It ships OFF. Read alongside the reservation floor, which lost at every dose, the pair
gives a clean decomposition: hold alone -248, fill alone +247. **The ES learned a
development change, not a reservation.** That is a template for the next hand levers, but
it also means hand levers now have to be tuned against the specific theta they ship with.

**Denial looks saturated.** The g130 autopsy's own follow-up note says so, and prescribes
rung diversity as the next axis. flow131 is the first test of that.

**The hand-planner families are closed, not solved.** Admit/route is closed at its ceiling.
The mix stage is closed after five rejections. Crew and plate sizing is closed after
seventeen. The open planner item carried over from `S/taskdiff` is the clone's *cadence*
taken as a pair, hourly PLACE plus SELL against our three fixed `SELL_TURNS`, and it has
not been built.

**The leaderboard has not confirmed any of this.** Everything above is measured on paired
boards against tapes. The live submission (56028553, `flow102_g280`) slid from 1843 to
1773 while flow130_g130 was being verified. The upload is in the user's hands.

---

## What a reader should take away

For most of a week the campaign built levers from good mechanistic analysis and lost with
almost every one of them, because the game has a shared price pot (a change that earns us
coins usually earns the opponent more) and an end-of-day RNG keyed to empty tiles (any
change to our plate re-rolls the town's shops, worth plus or minus 25k of unpaired noise).
The turning point was not an idea about the game. It was making the fitness the game:
byte-exact action replays of real Kaggle opponents as the training rungs, common random
numbers on the shop draw, a paired-t gate, and one configuration bug fixed that had been
quietly feeding every tape arm zero episodes. Within 40 generations of an honest objective
the ES produced the first theta in the campaign to beat the live build on every leg, and
within 130 more it went from winning by denial (cutting the clone's strawberry and wool
prices by getting into the contested pot first) to winning by denial *and* its own purse
(a later, more patient carrot liquidation in the uncontested part of the market). The
climb over the live build reads +8.4, +16.8, +18.3, +22.1 win points, it holds on tapes no
arm trained on, and it costs nothing on the immutable yardsticks. What none of it has yet
is a leaderboard rating.

---

## 2026-09-11, afternoon and evening: why the ES stopped climbing

State at 15:00Z. Two files were live: candidate **B** (`flow193_g100_hr`, sub 56161192) and
the older **hr** file (`flow172_g1000_pair_hr`, sub 56143250). Four ES arms had been retired
that morning, each because the paired judge refused their records; the top-10 cutoff had
moved to about 2967 (§45). So the afternoon was not another arm. It was finding out why the
arms do not climb, answering two questions the user asked about the action set, and
repairing the instruments every verdict is read through. Sections below are §55-§97 of
`docs/strategy/2026-09-10-consensus.md`, each naming its evidence doc under
`docs/strategy/2026-09-11-*.md`.

### 1. The plateau, diagnosed

**A noise walk, not an overfit (§59).** Each refused record was replayed against B on *its
own training rungs*, at the pinned seed and seat the ES had scored (206 rungs, shop-diff 0).
They lose there too -- flow200 g10 -646 (t -3.8), flow201 g10 -511, flow196 g100p -551; mean
-270, none reaching +300 at t >= 2 -- and in-sample and hold-out correlate at Pearson 0.66,
so there is no in/out gap to explain. The mechanism is the optimiser: Adam normalises every
coordinate to about +/- lr regardless of the gradient, so lr 0.003 over 5,997 live genes is
an isotropic random walk of ||delta|| ~ 0.23 a generation. An alpha falsifier (§62) added
that a shorter step rescues no recorded direction: alpha 0.03 is behaviourally B, alpha 0.1
carries the whole loss -- a cliff, not a slope.

**A plateau plus one day-0 switch (§60, §63, §64, §66).** In the small-step rig 14 of 56
step thetas moved 100 % of boards -- *the same 14* on two disjoint tape families: a
board-independent discontinuity, not a gradient. Its radius, ||theta - B|| in
(0.0023, 0.0035), is one lr of one coordinate and 67-100x smaller than the trainer's own
step. It was named at the line: `brain.py:624`
`animal_count = _qfloor(animal_share * n_dev)`, B's product 6.991294 against the boundary
6.999900. The crossing theta wants a 7th animal it never buys, so `_seed_room` reserves a
tile for it and the 11th wheat seed is clipped out, costing -1,774 a board on TOPB2.
Re-centring B off the edge was **refuted**: the plan holds only to c ~ 0.012 before the next
tie fires, and c = 0.02 flips 100 % of boards (win 71.7 -> 4.2 %). A census (§67) found 68
discretisations in that interface, 46 within sigma 0.02 of a boundary, and 0 of 64 members
decoding B's plan: our sigma is too *large* for the lattice (§71). One planner fix landed,
SEED_ROOM_PURSE_ON (§69), which removes 85 % of the switch's damage on the crossing theta
(+1,769/board, t 4.2) while staying byte-identical to B -- infrastructure, ON for training
arms only.

**Real but dimension-limited (§72, §73).** Re-read with disjoint halves, the saved draws
give a remainder cosine of +0.039 at sigma 0.01 against a 1/sqrt(n) null of 0.013 -- the
noiseless dimension-limited value P/(P+d). There is signal, and the binding constraint is
d = 5,997 >> P = 256 pairs. Per block, though, **no block survives multiplicity** (90 tests,
max |z| 2.81, Bonferroni p 0.45), and the sigma-0.01 leaders are exactly the day-0 cliff
subspace, their cosine collapsing as 1/sigma: a smoothed step, not a slope. Only `gp` and
`dh` sit outside it and rise with sigma. Hence the next recipe --
`--train-only gp,dh,ds,g5,gb5,w3,b3,b1` (d_train 1,191), sigma 0.01, sgd at lr 1.8e-4,
weight decay 4e-7 (scaled as lr-squared), pop 4,096 -- staged at 19:40Z as **flow209**
(seed B) and **flow210** (seed hr), the block list resting on
1.4-2.8 sigma cosines from one draw (§79).

**Three ways out, all measured, all closed.** ISEARCH (§76) raced B's own coarse integers
by offset: 0 of 24 edits gained more than 302 coins on either family, and one extra melon
tile at day 0 cost -14.4k with +11.0k of it going into *their* purse. B is a strict local
optimum in its own lattice at radius 1-2. Pinning those integers (§77) cut evaluation noise
20-fold and still found no gradient: kappa 0.027, +d losing at every alpha, two draws
orthogonal. Dithering the decode inside fitness only (§80) read margin -107 at alpha 0.1;
only alpha 1.0 "passed", which is the day-0 cliff again. flow209 and flow210 launched as
staged.

**The reading rule was wrong, and was corrected before use (§84).** `Trainer.step` applies
momentum m = 0.9 m + 0.1 g for *both* optimisers, so consecutive 10-generation block deltas
overlap by construction. Pure noise pushed through the run's own schedule gives a null of
mean +0.51, p95 +0.55, not the 1/sqrt(d) = 0.029 the recipe assumed. On the two Adam arms
that had no held-out gain, flow201 read 0.4375 against a null of 0.4241 and flow200 0.3257
against 0.3350: both *on* the null, which is §59's noise walk measured directly.

**What the first records say (§93).** At g10 the untrained 5,598 genes are byte-identical
to the seed in both arms; flow209 moved 2.1 % of one sigma-0.01 draw and flow210 3.5 %.
Decoded on 8 hold-out boards that is 14 and 20 coarse changes in 240 decisions, mostly
plant_target +/-1 -- not null, so decode will not bind at g30 and the only question there is
persistence.

### 2. The user's two questions, answered with measurements

**"Can we remake the decoder so it can express every play?"** A census of 29 top-tier tapes
(23,806 market rows) found the unit vocabulary is already ours -- 93.9 % expressible -- but
only 17.9 % of opponent *coin*, with 78.3 % failing on **time**: sales on turns we hold no
lot (§85). The band we lose to shows the same hole shifted later, its coin concentrated at
turn 21 (§88). Then the hole was priced engine-exact on 96 live replays (§89) and the
framing collapsed: moving our lots *later* pays (+759 a game on losses) and earlier loses,
and forcing the opponents' ~292 lots a game onto our four turns would have paid *them* more.
The one free move it found, lot 3 from h18 to h21, was built as SELL21 and **refused on the
screen** (§90): LIVE-C -1,134/game, t -8.87, our purse +249 and theirs +1,383 -- our units at
turn 18 were suppressing the price they sell into. The running falsifier SELL5 (rows at
turns 7 and 14) came back **LEVEL** in the engine (§91): +35/+44/+52 coins and 0 flips in
320 paired games, because the allocator declines the windows when offered them. Sell timing
is closed in both directions at B's genes.

**"Why not sell what is left in the shed, and use all the fertilizer?"** A 96-replay audit
(§86) recomputed every executed sale engine-exact. Our end-of-game leftover is 47 coins a
game, always fertilizer, with zero crop units held (DROP_ON already banks the day-29
harvest); it covers the margin in 0 of 48 losses, whose mean margin is 5,186. The cause is lot
composition: lot 3 at h18 is built from hour-0 stock, so fertilizer the hands
collect afterwards has no row to leave on. The fertilizer *gap* is real and larger -- they
realise about +7,100 coins a game more from it, in wins and losses alike -- but
that is §57's family, tested on B the same afternoon: cutting the apply/sell ratio 2/1
raised margin on all eight legs (+376 to +1,141) with wins level everywhere. Denial handed
back; not promoted.

### 3. Instruments

The judge pad (§83) makes a theta's *width* pick the judge tree and nothing else, because a
wider theta read by the old tree is silently truncated and every leg then judges a different
agent. The same firing counted the rungs the arms train on -- 178 episodes a generation, 166
of them pinned tapes carrying 99.04 % of the weight -- so `--shop-crn` is a no-op here and
the +/-25k shop lottery cannot be this recipe's noise floor. A later audit (§94) confirmed
the zero-archetype allocation is the launcher's own `--rung-weight 0` override, inherited
from flow128, and priced the objective: top-ten 32.7 %, the 1900-2100 band 27.2 %, LIVE-C
26.9 %, self-play 0.96 %.

That exposed a hole. A strategist review (§92) set objective and gate against Kaggle's
matchmaking, which draws opponents at own-rating +/- 45 with no tail: B's pool averages 2324
and it has never met an opponent above 2433. The 2550-2800 band, where the next 450 rating
points live, was 0 % of the objective and 0 % of the gate. If it were band-dependent,
both the incumbent and the seed choice were wrong. It is not
(§95): across 152 boards and five legs spanning 1827-3081 B beats hr on every leg, pooled
+802 (t 3.48), rating slope +36 coins per 100 points (t 0.56), and +1,104 on the 37 hold-out
boards already inside 2550-2750. A fresh engine read confirmed it (§96): 44 pinned-town
tapes of 2550-2750 teams, cut byte-exact, gave B 68.3 % against hr's 63.3 %, +697/board,
t +1.93, W3/L0 -- but the edge is +1,377 in 2550-2650 and +102 in 2650-2750. The ordering is
band-invariant; the size is not, which argues for re-pointing the rungs. NEXT30 was applied
at 23:15Z as a sixth, informational judge leg, promotion logic byte-identical (§97).

### 4. Dead ends of the day

| lever / route | § | why it died |
|---|---|---|
| LOTS (130 sell-lot genes) | §81, §87 | one-step: +d gains obj_w, loses margin held-out -- and it covers 0 % of §85's hole |
| SHOP_CRN on the pinned recipe | §83 | drawn-shop rungs are 0.96 % of the objective, far below the 25 % bar |
| Dither the decode in fitness | §80 | no held-out gradient at alpha <= 0.1; only alpha 1.0 "passes", which is the cliff |
| Pinned integers one-step | §77 | noise fell 20x, kappa stayed < 0.03, two draws orthogonal |
| Re-centre B off the switch | §66 | the next floor tie fires by 0.02; c = 0.02 flips every board, win 71.7 -> 4.2 % |
| Integer race around B (ISEARCH) | §76 | 0 of 24 radius-1/2 edits gain > 302 coins; 8 of 24 move zero coins |
| Wall imitation (their opening) | §70 | the planner *can* execute it and loses -24,209/board, +19,492 into their purse |
| FERT_VOLUME (sell more fertilizer) | §57 | margin up on all 8 legs, wins level everywhere -- denial handed back |
| SELL21 (lot 3 at turn 21) | §90 | screen -1,134/game, t -8.9; the turn-18 row was denial worth +1,383 to them |
| SELL5 (rows at turns 7 and 14) | §91 | engine LEVEL, 0 flips in 320 games; the allocator declines the windows |
| GATE-vs-LADDER upload | §95 | 0 of 19 refused records gain net TOPB2 wins; no candidate to upload |

### 5. Where the day ended

B was 96-32 at about 2503 and hr 163-77 at about 2615, against a top-10 cutoff of about
2967. flow209 (seed B) and flow210 (seed hr) were running the §73 recipe past g13 and g15.
Their g10 records were judged at 22:38Z and 22:47Z: flow210 is **level against its own seed**
(+32/+29/+3/-20, zero flips on 284 games) and loses 1 of 3 legs against B; flow209 reads
level-to-negative against B (-385/-32/+202/-293). Neither is a promotion, and neither was
expected to be: §60 and §77 predicted level records. flow211 was staged at 23:35Z
(`docs/strategy/2026-09-11-flow211-staging.md`): the flow209 launcher byte for byte except
for its rungs, with NEXT30 at w10.2 and the top-ten rungs cut to w4, so the pair isolates
the objective.

What decides next is the g30 persistence read against §84's momentum null. A mean
consecutive block cosine above about 0.55, with roughly 0.05 of margin over the p95 of 0.55,
is the first evidence of a usable gradient at B and keeps the arms running; 0.45-0.55 is
noise; below 0.45 is lr overshoot. If it reads noise, the optimiser side is spent and the
campaign moves to new decision dimensions or a changed objective -- and the day's instrument
work is what will make that verdict readable.

---

## 2026-09-11/12, night: the objective was the problem

State at 23:00Z. flow209 (seed B, GPU0) and flow210 (seed hr, GPU1) were running the
§73 recipe past level g10 reads, with NEXT30 newly applied as a sixth, informational
judge leg; B was live at about 2503 and hr at about 2615. The night's question was
§84's: does the direction the arms walk persist, and does it pay. It persisted. It
did not pay, at any step size or either sign. By 02:31Z both arms were retired and
both GPUs carried an A/B on the *objective* instead. Sections below are §98-§113
of `docs/strategy/2026-09-10-consensus.md`, each naming its evidence doc under
`docs/strategy/2026-09-1{1,2}-*.md`.

### 1. flow211: staged, blind-reviewed, fixed

flow211 was staged at 23:37Z (§98) as the flow209 launcher byte for byte except its
rungs: NEXT30 -- 30 pinned-town tapes of teams rated 2550-2750 -- at w10.2, 38.2 % of the
objective, top-ten cut 32.7 -> 10.0 %, the old band 27.2 -> 21.2 %, LIVE-C 1-42 26.9 ->
21.0 %. A weight-0 pinned rung still consumes its episode (`es/train.py:4413-4429`),
so 196 pinned rungs forced `--episodes 200`.

A blind pre-launch review (§100) passed 21 checks and stopped three things. **D0:**
`es/train.py:5510` uses `max(chunk, total)`, so the every-tenth-generation abs probe
runs as *one unsplit jit call* whose rows scale with the rung count -- flow209 21,760,
flow211 25,600, 3.1x the main loop's 8,192-row step, allocated beside the live arrays
on cards already at 17,974 of 24,576 MiB. "`--chunk` sets memory" is true of the main
loop only; fixed by `--abs-pairs 64 -> 54`. **D1:** flow211's NEXT30 judge column
would have been 30/30 *in sample*; fixed by judging its records on a held-out 14-board
extension. **D3:** `--seed 311 -> 309`, pairing flow211's boards with flow209's under
common random numbers. Applied at 00:08Z, precheck ALL PASS, md5 f1d71dee local =
remote (§102).

### 2. Who the 2650-2750 opponent is -- and four corrections

The band we were re-pointing at holds no new play (§99). The upper and lower halves of
NEXT30 do not separate in the mean (max |Welch t| 1.43 over 46 columns); they separate
in *dispersion* -- every upper team hires exactly 5 on day 0, plants exactly 12 melon
and 20 strawberry by day 10 and holds zero melon after day 14 (sd 0 against 0.27-22.4
below): the mistake-free version of the same clone. The margin is decided late:
d0-9 +3,029, d10-14 -20,705 (correlation 0.18 with the final margin), d15-29 +21,786
(correlation +0.93).

A blind codex review of §85-§102 (§103) landed four valid corrections. §99's
"no open knob" was a **source error** -- the trained blocks do reach hiring and crew
(`policy.py:635`, `:643-650`), and §93's own decode had shown crew_target 11 ->
12; what stands is that every *hand-built* family is closed and the ES owns those
knobs. §93's **arithmetic**: 14 coarse changes in 240 decisions is 0.058 a board-day,
not 0.6, so its "15-20 % of board-days by g30" was 10x high. §101's **dependence**:
four correlated records on the same 20 boards put the held-out TOPB2 t at about -2.05,
not -3.66, so the conclusion holds at reduced strength. §89's **upper-bound misuse**:
"+3,288 if their lots sat on our turns" ignores opponent revenue, so it bounds rather
than proves; §90's SELL21 refusal survives it (board t about -6.3), and SELL5 is
+43 coins SE 15 t 2.85 -- reproducibly positive and negligible, which makes "LEVEL"
the wrong word for a right decision.

### 3. The reader moved to checkpoints

The SNR reader was re-pointed at checkpoints (§104). `state.npz`'s `theta` is the
ES centre, and flow209's g10 record is byte-identical to it: records and states are
the same object. On [g0, g10, g20] flow209's consecutive block cosine read +0.8168
against §84's optimizer-null p95 of +0.5443 -- the first thing in the campaign to
clear that null; at g30 it held, +0.7831 against +0.5558, while the in-sample curve
stayed flat. And the same centre lost: its g20 against B read H30 -516 (t -3.0) and
H30B -645 (W0/L6), LOSS 2 of 3. The direction was real as motion and negative as play.

### 4. Family gradients: support, not direction

If the objective pulled in conflicting directions, re-weighting would be a fix. It
does not (§105). One pop-512 rollout at B on flow211's 196-rung ladder, sigma 0.01,
the 1,191 train-only genes, four episode seeds, with `ep_weight` zeroed outside each
family in turn, gave cross-seed cosines against two-seed reliabilities of 0.068-0.112.
Disattenuated, the band families run together at 0.82-0.98 and flow209's objective
against flow211's at 0.93; no pair was significantly negative. flow211 is therefore a
sampling/support A/B, not a direction A/B, and "the ES is pointed at the wrong band"
is false. Its launch was held.

### 5. The step ladder: B sits in a lattice cell

Next came a ladder along the persistent direction (§106): theta(alpha) = B +
alpha(theta_g20 - B), nonzero on the 1,191 trained genes, ||delta|| 0.0155 = 0.045 of
one sigma draw. On the screen it lost at every rung (LIVE-C/TOPB2: alpha 1 -413/-212,
16 -5,942/-6,654, alpha -4 -381/-1,288), and the engine agreed over 60 paired boards:
alpha 1 -423 (t -2.38), -4 -485, 8 NEXT30 -1,606 (t -5.1), 16 -7,329 (t -9.1, W0/L20,
win 68.3 -> 35.0 %). Loss at both signs, monotone in |alpha|: the §60/§66/§76
cell signature, every extrapolation walking off B's lattice cell. So the learning
rate stays at 1.8e-4 -- the ladder peaks where it loses *least*, not where it gains;
"persistent direction" is closed as a source of expected gain; and §59's lr 0.003
"noise walk" was retroactively the alpha ~16 cliff, not a noise floor.

### 6. The audit that renamed the problem

The other measurement asked whether judge or objective was wrong (§107). A sim
defect: refuted -- per-board sim against engine correlates at rho +0.774 with 82 %
sign agreement, and the pooled held-out reads agree (engine -580 t -3.58, sim -647).
Memorisation: refuted -- the in-sample TRAIN42 leg is -71 (t -0.27), no better than
held-out, and the loss is broad and scales with the step rather than with the board.

What was left was the trade. Through the trainer's own `_play` on all 166 pinned rungs,
the g20 centre against B reads TOPTEN +461 (t +2.0), LOSS10 +565 (t +2.1), LIVEC42
-382, the W2 band -249, self-play -543, for an objective-weighted win of 0.5904 ->
0.5859: flat. **The ES step is a transfer** -- top-ten and LOSS10 margin bought with
band margin -- the rank-normalised advantage is indifferent to it, and the judge,
band provenance apart from TOPB2, sees only the sold side.

The gate on that finding (§110) both failed and confirmed. It cannot be powered:
with-town tapes pin the *shops*, so its four replicates are one board set measured
four times, and |t| >= 2 per family would need 59 LIVEC42 boards where we have 42. In
aggregate it confirmed: BAND (127 boards) -259 t -2.14, BOUGHT (TOPTEN + LOSS10,
30 boards) +536 t +3.90, with NEXT30 on the **bought** side (+183) -- which makes
flow211 a mixed change and a band-only arm the sharper test.

### 7. The sell-timing family's last member

§103 was right that the family had been closed on a screen refusal and a frozen
allocator, with variant (c) unrefuted, so it was built (§108): SELL21C, a fraction f
of lot 3's WOOL/MILK/STRAWBERRY moved to a fourth, turn-21 lot while the turn-18 denial
row stays; inert 32/32 coin-identical. Screen at B: f 1/2 -301 (ours +83, theirs +384),
f 1 -946 (ours +90, theirs +1,036), f 1/4 -60 and positive on TOPB2 only. Three of nine
products carry 83 % of SELL21's whole loss; our purse saturates at +41/+83/+90 while
theirs is dose-responsive. The f 1/4 engine legs came back level and opposite-signed
(+138 and -114, about +12 a game). The mechanism closes it: press and hold price *our*
curve, the loss is *their* curve rising, invisible to our fitness at a fixed f, and
a per-opponent-class f is an opponent model -- a class §78/§92 found empty.

### 8. The changeover

At 02:09Z flow210's g30 centre read TOPB2 -1,886 (W0/L5), H30 -595, H30B -548 (W0/L8),
LIVE62 -921, NEXT30 -421 = LOSS 3/3, and flow211 launched on GPU1 at 02:09:46Z, pid
1006600 (§109). At 02:29Z flow209's g30 centre read H30 -470 (t -2.95), H30B -627
(W0/L6), TOPB2 -178, LIVE62 -28 = LOSS 3/3, the loss stable in size from g20 (-516/-645
there, -470/-627 here) exactly as §106's alpha ~1 reading predicts; flow212 launched
on GPU0 at 02:30:17Z, pid 1011377 (§111). The §73 arms were over: both seeds drifted
away from the held-out judge on the same objective.

The live pair tests the objective, not the step, under one shared seed-309 CRN draw:
flow211 (top-ten 10 %, NEXT30 38 %) against flow212, which puts top-ten, LOSS10 and TOP50
at `--rung-weight 0` -- still played, but contributing 0 before rank-normalisation. The
reading rule: `S/snr/centre_read.sh` at every tenth generation, judge legs on any record,
and **held-out band margin decides** -- never the block cosine alone. The first arm
whose centre gains on LIVEC-H30/H30B is the first sign the objective was the problem;
if both still sell band margin with the destinations removed, the transfer story is
wrong and the ES from B is closed outright.

### 9. New band support, and the arm behind them

BAND40 was cut at 02:44Z (§112): 48 fresh pinned-town tapes of teams rated 2374-2599,
one per team, disjoint from every existing set, 48/48 byte-exact. B against hr there
is **level** (+117 a board, t +0.33, W1/L1), continuing NEXT30's gradient (+697 at
2550-2750) down to null in the LIVE-C band; the incumbent is undisturbed. Band support
for per-family reads is now 82 boards against the ~59 §110 wanted. flow213 was staged
at 03:00Z (§113): flow212 plus BAND40 at w4, 236 pinned rungs, precheck ALL PASS,
md5 33152e42.

### 10. Dead ends of the night

| lever / route | § | why it died |
|---|---|---|
| LOTS one-step | §81, §87 | gains the objective, loses held-out margin; never got a GPU |
| SELL21 (lot 3 h18 -> h21) | §90, §103 | screen -1,134, board t -6.3; the turn-18 row was denial worth +1,383 to them |
| SELL5 (turns 7 and 14) | §91, §103 | +43 coins SE 15 -- positive and negligible; the allocator declines the windows |
| SELL21C at f 1/2 and f 1 | §108 | screen -301 and -946; our purse saturates at +90, theirs rises to +1,036 |
| SELL21C at f 1/4 | §108 | level: screen -60, engine about +12 a game |
| GATE-vs-LADDER upload | §95 | judge band-invariant; no refused record gains net TOPB2 wins |
| flow209 (seed B) | §111 | g30 centre LOSS 3/3 (H30 -470, H30B -627 W0/L6) |
| flow210 (seed hr) | §109 | g30 centre LOSS 3/3 (TOPB2 -1,886 W0/L5, H30B -548 W0/L8) |
| "raise lr, the direction persists" | §104, §106 | the ladder loses at both signs; alpha 16 is -7,329 a board |
| Per-family objective gate | §110 | pinned shops make four replicates one board set; needs 59 boards, we have 42 |

### 11. Where the night ended

B stood at 111-39, about 2548, and hr at 175-87, about 2628, against a top-10 cutoff of
about 2967; eleven days remain. Both GPUs carry the objective A/B, and what decides
next is their first centre reads -- g10 at roughly 04:30Z, g20 at roughly 06:30Z
-- judged on held-out band margin. The night's result is a change of name for the
problem. The step was never noise and never an overfit: it was an honest gradient
on an objective that buys top-ten and LOSS10 margin with the band margin the ladder
charges us for. Either removing those destinations turns the trade around, or the ES
from B is closed and what remains is the constraint §60, §66 and §76 have pointed
at all along -- the action interface and the lattice B sits in.

