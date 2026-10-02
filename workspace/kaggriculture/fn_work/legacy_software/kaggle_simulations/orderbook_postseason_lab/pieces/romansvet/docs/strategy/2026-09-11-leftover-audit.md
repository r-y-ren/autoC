# Leftover-in-storage audit — 96 live Kaggle replays (2026-09-11T21:02Z)

**Observation audited (user):** "in all the games I checked where we lose, we still have
something in storage at the end; why not sell it, and why is fertilizer not all used?"

**Verdict: the observation is real and the lever is worthless.** The leftover is
**always fertilizer**, it averages **47 coins** and never exceeded **260 coins** in 96
games, against a mean loss margin of **5,186** (median 3,332, narrowest 99). In
**0 of 48 losses** would selling the leftover have changed the result.

## Method

`S/leftover/audit.py` reads the raw Kaggle replay JSON (`S/ep_<episode>.json`,
credential-free) and reports, per seat: the end-of-game shed and unit inventories valued
at the **final** market price, the day-29 SELL rows offered vs stock held, and the whole
fertilizer chain (collected / bought / applied / sold / left / still uncollected on
tiles). Executed sell units and revenue come from the validated engine re-simulation in
`scripts/replay_profile.py::_simulate_market`, not from an estimate. 96 games:
48 for sub 56161192 (candidate B) and 48 for sub 56143250 (hr), 24 wins + 24 losses each,
most recent first (through 2026-09-11T20:40Z).

Tables: `S/leftover/audit.md`. Raw rows: `S/leftover/rows.csv` (192 seat-rows).

## The three ways stock can survive to the final step

1. **Unsellable by law — day-29 unit inventory.** A day-29 harvest lands in a unit's
   inventory and day 29 has no end-of-day banking (`src/kagg3/core/plan.py:259`), so it
   is bankable only through an explicit DROP. **This is not our problem: our mean
   end-of-game unit inventory is 0 units in all 96 games.** `DROP_ON` is doing its job —
   we walk home, DROP and sell the day-29 harvest.
2. **Blocked by a cap or the price curve — does not exist.** `_commit_unit` sells one
   unit at a time straight out of the shed for as long as the shed has stock; the only
   refusal is an empty shed. Price sinks along the curve but never below 1, and sales at
   $1 do not even raise market supply. The one real cap is `maxMarketOrdersPerTurn = 10`
   rows/turn, and we never used more than 7 of the 9 sellable products in a turn.
   **No unit in this audit was blocked.**
3. **The planner chose not to offer it — this is all of it.** Every leftover coin we
   left on the table is fertilizer that our last day-29 sell lot never listed.

## Mechanism, walked through: episode 107922863 (loss, −2,866)

Our seat 1, day 29 (step = engine step index; the action recorded at step *t* executes
from the observation at *t−1*):

| step | hour | shed FERT | unit-inv FERT | FERT price | shed total | our market rows |
|---|---|---|---|---|---|---|
| 696 | 0 | 14 | 0 | 25 | 86 | — |
| 697 | 1 | 14 | 0 | 25 | 86 | **7 rows incl. `["SELL","FERTILIZER",14]`** |
| 698 | 2 | 0 | 0 | 23 | 0 | — (shed emptied, money 110,984 → 116,313) |
| 699–710 | 3–14 | 0 | 1 → 10 | 21 | 0 | — (13 `COLLECT_FERTILIZER` ops by the hands) |
| 711–714 | 15–18 | 0 → 12 | 13 → 1 | 21 | 9 → 90 | 10 `DROP`s bank the harvest + the fertilizer |
| 714 | 18 | 12 | 1 | 21 | 90 | **5 rows — WHEAT/CARROT/STRAWBERRY/EGG/MILK/WOOL, no FERTILIZER** |
| 715 | 19 | **13** | 0 | 21 | 13 | — (shed 90 → 13, money 116,313 → 120,516) |
| 716–719 | 20–23 | **13** | 0 | 20 | 13 | **no market rows at all** |

Lot 1 at turn 1 sells the hour-0 shed **including all 14 fertilizer**. The hands then
collect 13 more units of fertilizer during the day and DROP them into the shed. Lot 3 at
turn 18 is built from the items the decode reserved a lot for, and fertilizer is not one
of them — its hour-0 stock was already zero by then — so 5 rows go out, the crops clear,
and **13 fertilizer × 20 = 260 coins** sit in the shed for the last 5 turns with no order
to move them. Four rows of the 10-row budget went unused. This is a *reservation /
lot-composition* miss, not a cap and not the terminal law.

The generic shape: mean 7.3 fertilizer units left, mean price 5.7, so **47 coins**.
The price is the reason the number is small — everyone dumps fertilizer, the curve
saturates, and the last units are worth 1–25 each, not the 100 base.

## Opponents show the same pattern, only tidier

Opponents end with a mean of **0.4 units / 18 coins** left (median 0), but that is a
different sell cadence, not a different law: they emit market rows on **14.8 of day 29's
turns** to our **3.1** — a blanket `SELL <item> 6000` on nearly every turn — so any late
DROP is swept by the next turn's blanket row. One opponent still finished a game holding
1,129 coins of WOOL. **Leftover stock is a game property both seats run into; the size of
ours is one missing order line, worth tens of coins.**

## "Why is fertilizer not all used" — the real fertilizer finding

| set | collected | bought | applied | sold | sell revenue | left in shed | uncollected on tiles at end |
|---|---|---|---|---|---|---|---|
| us WIN | 391 | 8 | 183 | 208 | 10,393 | 7.2 | 4.8 |
| us LOSS | 386 | 8 | 188 | 197 | 10,202 | 7.3 | 5.3 |
| opp WIN | 370 | 46 | 66 | 344 | 17,174 | 0.2 | 15.1 |
| opp LOSS | 371 | 48 | 66 | 345 | 17,472 | 0.1 | 13.3 |

Our fertilizer is **not** going unused: we collect ~388/game and consume ~188 of it on
tiles, sell ~200 for ~10,300 coins, and strand 7. The opponents **apply a third of what
we do (66 vs 188)**, buy 47 more from the market, and sell 345 units for **~17,300 coins —
about +7,100 coins/game more fertilizer revenue than us**, while leaving 13–15 units
uncollected on their animal tiles. That gap is an *allocation* difference (fertilize
tiles vs sell the unit), it is the same in their wins and their losses, and it is the
only fertilizer number in this audit on the scale of a loss margin. It is a separate
question from the user's, and this audit does not settle which allocation is right —
our applications presumably buy yield — but the ~7k/game fertilizer-revenue gap is the
line worth a paired test, not the 47-coin leftover.

## Judgement

**Not a lever worth building.** The upper bound — every leftover unit sold at the final
market price, ignoring the price curve that would push it lower — is **47 coins/game on
average, 260 coins at the very worst**, against losses whose margins run 99 to 36,493
with a median of 3,332. It covered the margin in **0 of 48 losses**, and in 0 of the 14
narrow losses under 2,000. Adding a FERTILIZER line to day-29 sell lot 3 (or simply
re-offering the whole shed on the last two turns, which costs 4 unused order rows) is a
~10-line decoder change worth about **+0.04 % of a game's score**; it is below the ES
noise floor and cannot be measured by any judge we have. Log it as a free tidy-up if the
day-29 sell decode is ever touched for another reason; do not spend an arm on it.
The follow-up that *is* on a decision scale is the fertilizer **allocation** gap above.

## Caveats

- The "old vs new" split in `S/leftover/audit.md` is `min(final, day-29 hour-0)`, an
  overlap, not a provenance trace: episode 107922863 books its 13 units as "old" although
  the walk-through shows the hour-0 stock was sold at step 697 and the leftover was
  collected afterwards. Treat that column as an upper bound on "old"; the true answer for
  our seat is "collected and DROPped after the last sell lot".
- `fert_balance` (collected + bought − applied − sold − left) is 1.3 for our seat and
  7–8 for opponents: unit-op counts are of *emitted* ops, so a refused
  `COLLECT_FERTILIZER`/`FERTILIZE` inflates them slightly. It does not touch the
  leftover figures, which are read straight from the terminal private observation.

Files: `S/leftover/audit.py` (reproducible: `export JAX_PLATFORMS=cpu; python
S/leftover/audit.py S/leftover/manifest.json --out S/leftover/rows.csv -j 8` then
`--tables`), `S/leftover/audit.md`, `S/leftover/rows.csv`, `S/leftover/manifest.json`.
