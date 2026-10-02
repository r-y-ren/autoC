# LIVE-C72: does the pinned town schedule decide the 23 lost boards?

2026-09-10, read-only (no engine runs; one `scripts/replay_profile.py` pass over six stored replays).
File under test: **theta `flow172_g1000` + tail pair + `HIRE_ROW_ON`** (`S/livec/g1000pair_hr.log`).
Judge **LIVE-C72**, results `S/lossflip/g1000pair_hr_livec.csv` (144 rows = 72 boards x 2 seats).
Deliverables: `S/boardsched/features.csv` (72 x 132) + `build_features.py`; analysis scripts
`univariate.py`, `permutation.py`, `twopurse.py`, `nested_loo.py`, `tape_fingerprint.py`,
`tape_summary.py`, and `replay_profile_6boards.csv`, all durable under `S/boardsched/`.

## 0. Headline

The outcome *is* deterministic, and the shop schedule *is* an exogenous cause of our margin — but it is
a **weak** cause (best r = -0.51, ~26 % of margin variance) and it does **not** classify the 23 losses.
The mechanism is the opposite of the hypothesis: **we are the shop-adaptive seat and the clone is not.**
The clone runs one book on 67/72 boards; its single schedule reaction (wool sink -> sheep) fires on the
boards we *win*. What costs us is our own rotation into the schedule's cash crop, paid out of wool and
fertiliser volume.

## 1. The determinism fact, quantified

Both seats return **identical coins on 61/72 boards**; on the 11 that differ the seat gap is mean 970 /
median 638 / max 2,351, and **no board changes winner** (`seat_split`, 0/72). Against a board-to-board
margin sd of **8,155**, turn order is worth <0.3 sd. With the town pinned the (schedule, tape, board)
triple fixes the game to the coin — a fact about *determinism*, not about the *schedule*: town and tape
are confounded one-to-one here.

Loss margins are tight — 23 losses, median -3,510, 12 of 23 inside 3.6 k; wins median +7,884, overall
mean +3,965: the file wins by being +4 k on average, not by winning a separable class of board.

## 2. features.csv — how the features were derived

Rows: `S/livec/ids.txt` order (load-bearing; index -> seed). Schedule: `S/band2100p/town_schedules.json`
keyed by episode id, value `[[day, SHOP_NAME] x 8]` — all 352 rows are exactly 8 unlocks on days
3,6,...,24 (`SHOP_UNLOCK_INTERVAL = 3`, `MAX_SHOP_INSTANCES = 8`). All 72 ids present.

Shop semantics (`src/kagg3/spec.py`, cross-read against the engine): a shop unlocked on day *d* is live
for days *d..29* and drains the **shared market inventory** every `SHOP_SELL_INTERVAL = 4` turns
= 6 ticks/day; a single-product shop (YARN_STORE, PET_CAFE) drains **2** units/tick, a multi-product
shop 1 per product, so the board's lifetime price support for product *p* is

    dem_p = sum over shops s of SHOP_CONSUME[s, p] * 6 * (30 - day_s)   [units]

Columns: `dem_<P>`, `first_<P>` (first day P is demanded; **30 = never**, not a 99 sentinel — see §7),
`nshop_<P>`, `demrate_d10_<P>` / `demrate_d29_<P>` (units/day live by that day), `n_<SHOP>` /
`first_<SHOP>`, per-day `shops_active_d10..29` / `demtot_d10..29`, shares (`straw_share`, `wool_share`,
`herd_share`, `crop_share`), outcome, per-seat margins, and the opponent's Kaggle `initialScore` from
`S/livec/eps*.json` / `rows_new*.json` (72/72 covered).

## 3. Univariate separation — and the multiplicity correction

87 non-degenerate features. **The town draw is exogenous** (not a function of either seat's play), so a
univariate association here is causal, not selection — the only question is precision.

| what is tested | statistic | family-wise p (300 label shuffles) |
|---|---|---|
| separates the 23 L from the 49 W | max abs Welch t = 2.42 (`first_MILK`) | **0.43 — nothing** |
| moves the continuous margin | max abs r = 0.456 (`first_STRAWBERRY`) | **0.003 — real** |

The schedule shifts the margin, but not enough to make the L set a schedule class. Opponent strength does
not explain it either — **rating L 2,501 vs W 2,488**, r(rating, margin) -0.22, rating-only LOO R² -0.015.

### Top 5 features by coins carried (median split, hi minus lo)

| # | feature | r with margin | margin hi-lo | L-rate lo -> hi | our purse | their purse |
|---|---|---|---|---|---|---|
| 1 | `n_single_shops` (YARN_STORE+PET_CAFE instances) | +0.33 | **+5,469** | 38 % -> 15 % | -9,370 | -14,839 |
| 2 | `dem_STRAWBERRY` (lifetime strawberry demand) | -0.42 | **-4,519** | 22 % -> 45 % | +17,483 | +22,003 |
| — | `straw_share` (best composite) | **-0.51** | **-4,796** | 19 % -> 44 % | — | — |
| 3 | `nshop_CARROT` | +0.25 | **+4,278** | 40 % -> 17 % | -9,431 | -13,709 |
| 4 | `demrate_d10_WOOL` (wool units/day live by d10; in {0,12,24}) | +0.35 | **+4,196** | 37 % -> 20 % | +10,608 | +6,413 |
| 5 | `first_STRAWBERRY` (day the first strawberry buyer opens) | +0.46 | **+3,777** | 39 % -> 25 % | -13,779 | -17,556 |

`early3_single` (a single-product shop by d9) shows +11,378 and 0/7 losses — **n = 7, do not price it.** All coin ledgers here are **descriptive** (what the boards did), never counterfactual.

### Tiny model, honestly

LOO on two *pre-registered* features (`straw_share`, `wool_share`): **R² 0.181**, sign accuracy 0.667.
Nested LOO, selection re-run inside each fold: R² 0.159 (k=1), 0.252 (k=2: `first_STRAWBERRY` 72/72 and
`dem_TOMATO` 71/72), then degrading (k=3 0.015, k=5 -0.042 — the selector loads up on collinear
strawberry variants). **Classification never beats the majority baseline**: nested-LOO W/L accuracy
0.625-0.653 vs 0.681 for "always predict W". In-sample R² 0.79 on all 87 features collapses to 0.05 out
of fold — that is the overfitting floor, and why only the two-feature model is quoted.

## 4. Reading the tapes: who is actually shop-adaptive

All 72 `artifacts/tape_actions_town/<id>.npz` fingerprinted (op codes from `src/kagg3/core/ops.py`).
**Caveat: tape market quantities are *requests*, not units** — `mq = 1000` / `100` are dump sentinels the
engine clamps to the shed, so unit counts below come from the replays instead.

Across 72 boards the clone plays plant book **163/31/0/33/12 on 67 of them**, 12 melon tiles planted d0
on **72/72**, 0 tomato on **72/72**, 260 hires on 57/72, herd (COW,SHEEP,GOOSE) = (6,4,2) on 57/72.
Correlation of clone behaviour with the schedule — it reacts on **exactly one axis**:

    vs demrate_d10_WOOL:  SHEEP +0.76  COW -0.73  GOOSE -0.77  pasture +0.75  coop -0.73  hires +0.71
    vs first_YARN_STORE:  SHEEP -0.63        straw planted vs dem_STRAWBERRY -0.04 (i.e. NONE)
    carrot planted vs dem_CARROT +0.08 (NONE)          melon tiles: constant 12 everywhere

When a YARN_STORE opens by d6-9 the clone swaps 2 COW + 2 GOOSE for 4-5 SHEEP, builds pasture not coop,
and hires 276. **On every other axis it is open-loop** — no reaction to strawberry, carrot or tomato
demand. The hypothesis as stated is therefore **false for features #2/#5 (strawberry) and #3 (carrot)**,
and for #1/#4 (wool sinks) the clone's one reaction lands on boards **we win** (+4,196).

## 5. What WE do — six live replays

`scripts/replay_profile.py` over `S/ep_<id>.json` for the 3 highest-`dem_STRAWBERRY` losses
(107481349, 107486647, 107441233) and 3 lowest-`dem_STRAWBERRY` wins (107505884, 107438287, 107474031).
**Provenance caveat:** these are the *live* Kaggle games of sub 56140532 (`flow172_g940` + tail pair) on
drawn boards, not the pinned judge games of the shipped file — same town, different board and theta, so
read them for *behaviour*, not for the margin. Our seat's book swings with the schedule; theirs does not:

| board (schedule) | our plants W/C/T/S/M | our herd G/C/S | clone plants | clone herd |
|---|---|---|---|---|
| 107481349 straw x4, YARN d12 | 91/19/**5**/**41**/13 | 3/8/**4** | 160/31/0/33/12 | 3/8/6 |
| 107486647 straw x4, YARN d12 | 90/14/2/**43**/13 | 3/10/**3** | 160/31/0/33/12 | 3/8/6 |
| 107505884 PET_CAFE x3 | 89/**122**/1/16/17 | 5/6/6 | 160/31/0/33/12 | 3/8/6 |
| 107438287 YARN x4 (d6,9,15,21) | 130/9/2/16/17 | 1/5/**17** | 162/31/0/33/12 | 0/6/**11** |

Per-product revenue, ours minus theirs (live engine ledgers):

* **Strawberry boards — we win strawberry and lose the engine.** 107486647: STRAWBERRY **+17,067**
  (338 u @195 vs their 249 @196) but WOOL **-18,492** (75 u vs 161), FERT **-8,459** (167 u vs 325),
  MELON -4,551, CARROT -2,611. Same shape on 107481349 (+16,115 / -12,571 / -11,188) and 107441233
  (+8,780 / -3,811 / -8,645).
* **Wool boards — we out-wool them and win.** 107438287 WOOL **+21,193** (358 u @244 vs 273 @243);
  107474031 WOOL **+19,058**; 107505884 (3x PET_CAFE) our 122 carrot tiles return CARROT **+25,870**.

The price support is enormous — strawberry clears at **195-203 coins/unit** on a 4-strawberry-shop town
and **8.8-45** on a wool town; wool likewise 244-249 vs 47-66. Both seats get it. The clone banks it
passively on a fixed 33-strawberry / 6-sheep book; we *chase* it, take the larger share of that product,
and pay for the tiles and crew out of the wool herd and fertiliser loop the clone runs identically
everywhere. **On strawberry towns that trade is a net loss.** (Melon is a constant -2.5..-4.6 k leak on
all six, already ledgered in `2026-09-10-livec-loss-anatomy.md` §1; family closed.)

### Does a planner rule exist that should fire?

Yes — two, both **OFF by default and off in the shipped file**:

* `LATE_STRAW_CAP_ON` (`plan.py:1438`, `LATE_STRAW_CAP_DAY = 15`) is *exactly* this lever: from d15 stop
  committing tiles to strawberry, moving the share onto the crops the brain also chose. It has never been
  read on a shop-schedule split — it was built from the 1950-2110 band anatomy (`2026-09-09-verdicts.txt`
  2026-09-05 15:36Z, same signature) and screened without conditioning on the town's strawberry sinks.
* `ENDGAME_TOMATO_ON` (`plan.py:1362`) is the tomato analogue and is **closed dose-responsively**
  (TILES 12 -1,300 t -4.7; TILES 16 -1,721 t -4.4). `dem_TOMATO` sits in my top 5 with the *opposite*
  sign to a "plant more tomato" lever (more tomato demand -> **+3,403** for us already): do not reopen.

Otherwise the shop -> mix response is not a rule at all in the shipped file — it is learned inside theta
via `brain.py` residual_drain, whose slope the prior diagnosis (`2026-09-09-verdicts.txt` 2026-09-09T06:48Z;
ADAPTIVE5 2026-09-06 16:20Z) measured as "roughly right" but 3-5 days late (keiz herd R² .92 vs ours .57).
**The six replays agree with that, which makes this an independent reproduction on a held-out set.**

## 6. Test designs (not run)

Pass bar in every case: **win rate first** on LIVE-C72, then paired mean margin (`S/bank/paired.py`)
against the standing base `S/lossflip/g1000pair_hr_livec.csv`. Two-purse rule: report **d-ours and
d-theirs separately**; a lever that only moves d-theirs is denial and has always been handed back.

1. **LATE_STRAW_CAP on a schedule split** (the only candidate the data supports).
   `S/livec/run.sh strawcap15 <wt> <flow172_g1000.npy>
   "OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True,LATE_STRAW_CAP_ON=True"`
   — 144 games, ~5 min at WORKERS=10. **Read it split by the `straw_share` median** (36/36 from
   `features.csv`): pre-registered prediction is a gain confined to the high-share half, inert on the
   low half. Bar: base is 49/72 boards, so the honest bar is "no board lost in the low half, >= +2
   boards in the high half". Expected signature **own purse** — d-ours up on high-`straw_share` boards
   with d-theirs flat (they never see the tiles we did not plant); if only d-theirs moves it is denial,
   reject. Confirm on `S/topb2/run.sh` and `S/live62/run.sh` (saturated, expect inert).
2. **Sweep `LATE_STRAW_CAP_DAY` 12 / 15 / 18** only if (1) passes, same runner and split — a dose-response is the only thing separating a lever from a seed draw.
3. **Herd latency, wool-sink gated — skip.** We lock the herd 3-5 days after the clone does, but the
   family is **PARKED / denial-only** (+261 sim) and the only boards it could act on
   (`demrate_d10_WOOL = 24`, n = 20) are ones we already win 80 % of: the test is powerless.
4. **Do not test**: carrot-count levers (closed 2026-09-07, -1.6 k..-9.3 k), tomato abstention (closed,
   -135 sim), wool sell-timing / herd switches (closed 2026-09-10), melon opening (closed twice).
   `nshop_CARROT` and `dem_TOMATO` carry the sign that says *those boards are already good for us*.

## 7. Verdict

**Schedule-determinism is real but small, and it is not what makes the 23 boards losses.**

* Real: outcome deterministic given the pinned town (61/72 seat-identical, 0 seat flips); the town draw
  is exogenous, so `straw_share` -> margin at r = -0.51 (family-wise p 0.003) is causal, worth about
  **±4.8 k of an 8.2 k sd**.
* Not the explanation: the schedule cannot classify W from L (family-wise p **0.43**; no model beats the
  68.1 % baseline out of fold), and neither can opponent strength (rating L 2,501 vs W 2,488, LOO R²
  negative). Most of the 8.2 k residual is our own play against a near-identical opponent book.
* Not the hypothesised mechanism: the clone is open-loop on 67/72 boards. **We** are the adaptive seat, and
  on strawberry towns our rotation buys the contested crop with wool and fertiliser volume — net negative.
* Exploitable? One lever, `LATE_STRAW_CAP_ON`, exists, is OFF, and has never been read on a
  strawberry-sink split. Ceiling if it recovered the whole gap on the high half: ~4.8 k x 36 boards —
  **descriptive**; price the displacement (where the freed crew goes) before believing any of it.

### Dead ends recorded

* `first_*` = 99 sentinel for "shop never appears": one board has no strawberry buyer, and 99
  extrapolated to a 72,708-coin LOO error, flipping single-feature LOO R² from +0.12 to -0.99. Fixed to
  30. Any future schedule feature must use a *physical* absent-value.
* **Board wealth is not the axis.** r(ours, theirs) = **0.929**, seat sd 21.7 k vs margin sd 8.2 k:
  schedule richness lifts both purses almost equally, r(wealth, margin) = **0.011**, L-rate 33/33/29 %
  across wealth tertiles. Every "hi-lo ours/theirs" number in §3 is mostly wealth, not a lever.
* `herd_share` / `crop_share` are **exactly** r = 0.000 with margin: the axis is strawberry-vs-everything.
* All-87-feature ridge: in-sample R² 0.79, LOO R² 0.053 — recorded so nobody re-runs it. Tape `mq` is a
  request with 1000/100 dump sentinels, so unit counts cannot be read off the npz at all.
