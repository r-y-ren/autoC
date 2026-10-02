# Review: "optimise harvest → deposit → sell → reinvest together" (2026-09-10)

Read-only. Line cites are the **arms-next** worktree (`plan.py` 8,128 lines); main is
8,010 and lacks `FORWARD_ADMIT_ON`, so its numbers run ~118 lower (the intraday review's
`plan.py:6457-6460` is `arms-next:6575-6583`). Builds on
`2026-09-10-intraday-controller-review.md`.

## 1. The routing evidence the proposal cites

`2026-09-10-melon-route-capacity.md`: one pinned board (107056463), theta
`flow172_g170c`, patched-copy **sim, descriptive**. Under the forced melon opening the
binding constraint is neither sell rows (`SELL_TURNS = (3,10,18)` + `MELON_LOT_TURNS =
(11,13,15)`, `ops.py:126,137`), nor `SHED_CAPACITY` (100 > 72), nor hands, nor harvest
cadence — it is **deposit turn**. With `MIDDAY_PLACE_V2_ON` 66/72 units bank and sell the
same day (72 u / 12,537 vs the clone's 72 / 17,440 at avg 233); without it two melon lots
ask 48 units into an empty shed and 35 ride to d11 at 121. Verdict in the doc itself:
"the route model is **not** the wall … the pot is not the win", five builds lose 15-20 k
over d12-29. It is evidence *against* a melon arm, not for one.

## 2. The three "isolated change" claims

| claim | verdict | measured evidence |
|---|---|---|
| extra workers can remain idle | **TRUE** | RAMP11 forcing the clone crew curve: band6 55.0→52.5 %, top10 69.4→55.6 %, −4.3k t −3.0; PASS share 15→37 % of unit-turns, revenue 112.8k→67.3k (`2026-09-04-verdicts.txt:384-385`). Mechanism is *cash*, not idleness: the hire bill + `cash_reserve` come off the purse that prices land, so the third quadrant is never bought. Forced-opening ramp: 94→22-26 %, 0 hands d1-5 because hire enumeration prices hands on **today's** tasks and melon emits none for 6 days (`2026-09-05-build-story.md:927`). The fix was built twice and lost: `FORWARD_ADMIT` HELD42 −8,676 (t −12), narrow rebuild −2,628 / LEG20 −1,456 / +0−8 flips, and the trained `g11` gene decodes to 0 days on the base theta (`plateau-review-verdicts.md` §54). |
| earlier sale orders can hit an empty shed | **TRUE, and already priced at hour 0** | `EARLY_SELL_MODE=B` 54.2→39.6 % (t −22.7) — "all three lots quote the same shelf → shed dumped at h2" (`2026-09-04-verdicts.txt:278`). But the shipped planner already reserves: `avail` is the hour-0 shed net of feed wheat and the day's fertilizer (`plan.py:6575-6583`), and the sale cannot hit an empty shed by accident. The residual is a one-day lag, ~600 coins/game pooled, and every lever aimed at it failed (`build-story.md:947,959`). Sell-hour headroom under g60 = **zero**; the turn-1 sale is now worth −77 (`2026-09-10-sell-hour-headroom.md`, §52). |
| forced melon production displaces the animal economy | **TRUE** | `MELON_OPEN_ON` alone band6 54.2→15.1 %, −17,554 t −12.8, theirs **+12.9k**; +`MIDDAY_PLACE_V2` −18,561 t −11.3; pinned judge 130 tapes 1.9 %, −19,557. `MELON_D10B` names the mechanism: COW 3→1, egg 2/day vs 5-12 → a price gift reaching **+31k by d27** (`build-story.md:371`, `verdicts:386`). Family closed in all three forms (§51/§54/§56, `2026-09-11-additive-melon.md`). |

All three are true **and already in the archive**. Restating them is not new evidence.

## 3. The chain, in code

`build_day` (`plan.py:5745`) is one hour-0 pass:

1. **Harvest → unit inventory** (`sim/units.py:185+`, HARVEST branch). Goods stay on the
   unit all day.
2. **Deposit → shed**: only `drop_inventories` at end of day (`sim/eod.py:210,266`), or a
   per-unit *excursion* — `BANK_BEFORE_LOT` / the melon excursion, mutually exclusive by
   `assert` (`plan.py:2483`), one excursion clock per block.
3. **Sale allocation**: `SELL.allocate` once at dawn (`plan.py:6613`, `sell.py:100`)
   against `avail` (`:6575`), greedy on `hold`/`press` (`sell.py:85-138`).
4. **Cash → purchases**: `BUD.grant` (`plan.py:5383`, second fill pass `:5409`,
   `budget.py:146`) walks value-per-coin down a purse already net of the hire bill and
   `cash_reserve` (`plan.py:3573`). Hire count is an enumerated argmax in `_plan_and_stats`
   (`:5876,:5952`), capped by task count, never by cash.

**Hard constants** (not theta): `SELL_TURNS`, `MELON_LOT_TURNS` (`ops.py:126,137`),
`BANK_MIN_VALUE = 400`, `BANK_MAX_TURNS = 9` (`plan.py:1863,1870`), `TAIL_HOPS = 2`
(`:2595`).

## 4. Knob inventory: what the ES already decides

`Macro` (`plan.py:3392-3405`), decoded in `brain.decide` (`brain.py:1145-1157`), 12 genes:
`plant_target`, `animal_want`, `land_bias`, `hold`, `press`, `grow_mult`, `compact`,
`dev_weight`, `hire_bias`, `crew_target`, `animal_defer`, `forward_days`.

- Sale timing/quantity → `hold` + `press` (`brain.py:1051-1053`). **PRESENT.**
- Reinvestment priority → `grow_mult`, `dev_weight`, `land_bias`, `hire_bias`,
  `animal_defer` re-weight every arm of `BUD.grant`. **PRESENT.**
- Crew ramp → `crew_target`/`ramp` (`brain.py:1106-1110`). **PRESENT.**
- Hire horizon → `forward_days` (`:1140`), trained, decodes to **0**. **PRESENT, refuted.**
- **MISSING: deposit turn.** Nothing in `Macro` moves an excursion. That is the single
  genuine gap, and it is exactly what §1's routing doc identifies as binding.

So "optimise together" *is* what ES does — jointly, on one fitness, on all four arms. The
proposal reduces to one missing knob. The tail pair is not a "starting point": it is
measured and already promoted (H_dm +801, LEG20 +1,403, LIVE55 +875 t 3.69 alone) and
ships in `flow172_*_pair`; it is still `False` in arms-next (`:1858`, `:2589`).

## 5. Recommendation

**DO NOT RUN.** "Evaluate the complete chain" is a restatement, not a hypothesis: it names
no switch, no gene, no board set, no falsifier. Three premises are already implemented in
theta; the fourth (melon) is closed by nine paired engine reads.

The only defensible narrower arm — **a theta-decoded deposit-excursion gene** (`g12`,
zero-init, `BANK_MIN_VALUE`/`BANK_MAX_TURNS` as decoded ints, gene-slope check at the
training sigma per the standing rule) — should also **not** be run, on its own arithmetic:
`BANK_BEFORE_LOT`'s excursion fires **0.67 times per game and moves 3.4 units into lot 2**
(`plan.py:1817`), worth +165/+209/+166 across three sets. A gene over its two thresholds
cannot exceed a few hundred coins/game, against a LIVE55 SE of ~240 and the flow180/181
lineage delivering +5,382 to +6,753. It is below the noise floor of the only judge that
counts.

If it is run anyway, the judge is fixed in advance: LIVE55 (d-margin > 0, seat-grouped
|t| ≥ 2, ≥ 28/53 boards positive) plus the TOPB 20-board held-out read, drawn legs as veto
only. No sim screen promotes.
