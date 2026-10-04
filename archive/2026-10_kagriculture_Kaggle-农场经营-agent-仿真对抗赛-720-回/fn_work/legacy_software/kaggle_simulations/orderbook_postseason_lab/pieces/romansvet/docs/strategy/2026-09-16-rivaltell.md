# RIVALTELL — the public-market rival-sale detector, measured against the engine's own ledger

2026-09-16, 08:26–09:0xZ. Telemetry only. No coins claimed, no switch written, nothing
under `src/` touched. Tools + data: `S/rivaltell/`. Candidate #5 / verdict item 3 of
`2026-09-16-v45-notebook.md`.

**Headline.** The inventory-delta estimator is **exact**, not approximate: on 50 real
engine games (323,550 turn-item cells) the identity
`inv[t+1]−inv[t] = our_sell₁₊ + riv_sell₁₊ − our_buy − riv_buy − town(t)` holds with
**zero residual**, so the town-tick model contributes **0 errors**. Detection of
"rival sold ≥1 unit this turn" is **precision 1.0000, recall 0.976–0.981**, and
**100 % of the misses are turns on which the rival also BOUGHT that item** — the net
cancels. That single blind spot is exactly the V45 step-0 round trip: **0 of 6
same-turn round trips are detected**, so this detector is *not* a fix for
`OPEN_PUMP_TELL_KEEP0`. A different, also-free turn-0 tell is (§5).

---

## 1. Instrument

| piece | file |
|---|---|
| collector (one real `kaggle_environments` game per board) | `S/rivaltell/collect.py` |
| estimator (pure numpy, re-derived from the engine) | `S/rivaltell/infer.py` |
| scorer | `S/rivaltell/score.py` → `S/rivaltell/metrics.json` |
| per-board arrays | `S/rivaltell/data/<set>_<episode>_s<seat>.npz` (50 files, 600 KB) |

Ground truth is the engine's own per-unit commit ledger: `kaggriculture._commit_unit` is
wrapped and each committed unit tagged with the player that owns the `farm` dict — the
instrument of `S/v45leg/trace0.py`. Boards are the leg rows themselves
(`S/lossflip/flow193_g100_hr_v45.csv`, `..._band180.csv`, seat-0 rows, first 30 / 20
distinct episodes), replayed with the pinned town registries
`S/v45leg/town_schedules.json` / `S/band180/town_schedules.json`, theta
`flow193_g100_hr`, shipped switch string of `S/judge7065/run_v45.sh`.
**30 V45LEG boards (post-09-15 clone tapes) + 20 BAND180 boards**, 719 steps each.

## 2. The identity, and the three engine lines it stands on

`kaggle_environments/envs/kaggriculture/kaggriculture.py`:

* `:652-661` `_commit_unit` SELL → `market["inventory"][item] += 1` **only when `price > 1`**.
* `:662-674` `BUY_PRODUCT` → `market["inventory"][item] -= 1`.
* `:728-751` `_town_consume`: on `step % 4 == 0` every **instance** of every unlocked shop
  eats `2 if len(products)==1 else 1` of each of its products; on `step % 24 == 0` one of
  every product except FERTILIZER.
* `:894-946` order inside one step: unit ops → `_process_market` → `_town_consume` → decay
  → `_end_of_day`. So the pot a seat reads at the top of step *t+1* already carries step
  *t*'s market **and** step *t*'s town tick, and `24 % 4 == 0` makes `step % 4 == hour % 4`.

Hence `infer.rival_net()`:

    riv_net(t) = inv[t+1] − inv[t] + town(t) − our_sell₁₊(t) + our_buy(t)
               = riv_sell₁₊(t) − riv_buy(t)

## 3. Accuracy

`.venv/bin/python S/rivaltell/score.py`. "own side = commits" uses our realised units;
"own side = orders" uses only the quantities we put in our own market row (what the
planner has without any extra state). Truth = rival credited SELL units.

| set | own side | precision | recall | exact-net cells | tp / fp / fn |
|---|---|---:|---:|---:|---|
| V45LEG 30 | commits | **1.0000** | **0.9764** | **1.0000** | 8203 / 0 / 198 |
| V45LEG 30 | orders | 1.0000 | 0.9681 | 0.9980 | 8133 / 0 / 268 |
| V45LEG 30 | commits, items we did not trade | 1.0000 | **0.9868** | 1.0000 | 7418 / 0 / 99 |
| BAND180 20 | commits | **1.0000** | **0.9812** | **1.0000** | 5493 / 0 / 105 |
| BAND180 20 | orders | 1.0000 | 0.9739 | 0.9982 | 5452 / 0 / 146 |
| BAND180 20 | commits, items we did not trade | 1.0000 | 0.9893 | 1.0000 | 5009 / 0 / 54 |

Per item, V45LEG / BAND180 (own side = commits):

| item | turns rival sold | recall | MAE, all turns | MAE, sold turns |
|---|---:|---:|---:|---:|
| WHEAT | 1692 / 1013 | .9758 / .9694 | 0.399 / 0.251 | 0.638 / 0.747 |
| FERTILIZER | 2501 / 1589 | .9372 / .9534 | 0.088 / 0.070 | 0.359 / 0.248 |
| CARROT, TOMATO, STRAWBERRY, MELON, EGG, MILK, WOOL | 280/210, 7/82, 1151/726, 215/154, 438/341, 1199/912, 918/571 | **1.0000** all | **0.000** all | **0.000** all |

**Seven of the nine products are recovered exactly, unit for unit, on every turn of
every board.** Only WHEAT and FERTILIZER lose anything, and only where the rival trades
both ways in one turn.

## 4. Where it errs

* **The town tick never errs.** 0 error turns out of 21,570 (V45LEG) and 14,380
  (BAND180); mean |err| 0.00000 on `step%24==0` (600 + 900 turns), on
  `step%4==0, %24≠0` (3,000 + 4,500) and on `step%4≠0` (10,780 + 16,170). Shops drawn
  **with replacement** must be counted as instances, not as a set — `parse.parse_town`
  (`src/kagg3/agent/parse.py:177-182`) already returns counts in `spec.SHOP_NAMES` order,
  which is `sorted(SHOPS)`, verified equal to the engine's table.
* **Every miss is a same-turn rival BUY of the same item.** V45LEG 198 missed cells
  (WHEAT 41, FERTILIZER 157), BAND180 105 (WHEAT 31, FERTILIZER 74) — **100.0 %** of them
  have `riv_buy ≥ 1` on that item that turn. The estimator is a *net*; it has no way to
  split the two legs from the pot alone.
* **$1 sales are structurally invisible** (`:653-659`, "Sales at $1 do not increase market
  supply"): the rival dumps 2,842 units on 731 turns (V45LEG) and 1,580 on 357 turns
  (BAND180) that the pot never sees. They cost almost nothing here (6 of 198 misses)
  because they co-occur with credited sales of the same item, but any *volume* read must
  be documented as "units that moved the price", not "units sold".
* **Using our order row instead of our commits** costs 0.2 % of cells and ~1 pt of recall
  — and is free: on the V45's own usage (only items we did not trade this turn) the two
  are identical.

## 5. Step 0 — the question KEEP0 could not answer

`OPEN_PUMP_TELL_KEEP0` reads `10000 − pot@hour1 − OPEN_PUMP_UNITS(53)` and fires at
`OPEN_PUMP_TELL_MIN = 40` (`src/kagg3/core/plan.py:1301,1398`).

| | KEEP0 tell | inventory-delta `riv_net(0)` for WHEAT | rival's real step-0 WHEAT row |
|---|---:|---:|---|
| 6 same-turn round trips (≥40 both legs) | 1, 10, 14 | **−13, −9, 0 — never ≥1** | e.g. BUY 70/SELL 70, BUY 86/SELL 86, BUY 89/SELL 80 |
| all 50 boards | range **[1, 15]**, fires on **0 / 50** | — | 16 boards buy ≥40 wheat at step 0 |
| correlation with rival step-0 wheat units touched | **0.137** | — | — |

**So the inventory-delta detector is blind to the round trip too** — for a perfect round
trip the two legs cancel in the pot exactly as they cancel in KEEP0's single reading, and
for a partial one (BUY 43 / SELL 30) the net is *negative*, so a "sold ≥ 1" test fails.
`nbintel` §6.1 and `v45leg` §3.1 are confirmed a third way, and candidate #5 is **not**
the replacement tell for turn 0.

**What does see it: our own realised fill price.** With our opening fixed
(`BUY WHEAT 53` + 4 HIRE) and `inv0 = 10000` on all 50 boards, define
`excess = (our money at step 0 − at step 1) − Σ_{j<53} price(WHEAT, 10000−j)`.
The board with no rival wheat at all gives the constant hire bill, `excess = 14`;
subtracting it, every distinct rival step-0 wheat row in the 50 boards:

| rival step-0 WHEAT row | boards | `excess−14` | KEEP0 |
|---|---:|---:|---:|
| none | 1 | 0 | 1 |
| BUY 5 / SELL 0 | 1 | 0 | 6 |
| BUY 14 / SELL 0 | 1 | 0 | 15 |
| BUY 2 / SELL 1 | 1 | 6 | 2 |
| BUY 15 / SELL 15 (V42-V44) | 18 | 26 | 1 |
| BUY 27 / SELL 27 | 1 | 35 | 1 |
| BUY 24 / SELL 12 | 1 | 53 | 13 |
| BUY 13 / SELL 0 | 5 | 56 | 14 |
| BUY 26 / SELL 13 | 5 | 56 | 14 |
| BUY 43 / SELL 30 | 8 + 1 | 56 / **104** | 14 |
| BUY 73 / SELL 60 | 1 | 56 | 14 |
| BUY 40 / SELL 27 | 1 | 101 | 14 |
| BUY 62 / SELL 49, **BUY 70 / SELL 70** (×2), BUY 86 / SELL 86, BUY 89 / SELL 80 | 6 | **106** | 14, **1**, 1, 10 |

`corr(excess−14, rival step-0 wheat units touched) = 0.787` against **0.137** for KEEP0.
Cut at **≥56** → precision 0.615, **recall 1.000** for "rival bought ≥40 wheat at step 0";
cut at **≥101** → **precision 1.000**, recall 0.438.

Three things the table says plainly. (a) `excess−14 = 106` on every V45-sized opening is
*exactly* the +106 `v45leg` §3.1 measured as the rival's round-trip profit: **the excess
is our gift, and it is readable at hour 1.** (b) It is **not** monotone in their volume —
13 pure buys cost us 56 while 15 buys-and-sells cost 26, and two boards with the identical
`BUY 43 / SELL 30` totals give 56 and 104 — because the engine interleaves **per order
index**, so what the excess measures is how much of their row sits in the slot our ladder
occupies, not how many units they moved. (c) KEEP0 and the excess disagree in the worst
possible direction: the three openings KEEP0 reads as `1` (the most innocent value it can
print) are the 15/15, the 70/70 and the 86/86 — two of which are the racers.
All inputs are ours (`obs["farms"][player]["money"]` at hours 0 and 1, the hour-0 pot, our
own order row); no opponent field is needed.

## 6. What our observation actually exposes (so this is implementable at turn time)

Engine `:948-956` assigns `obs0.farms / market / town` to **every** seat's observation, so
these are public to both players; only `observation.private` (`shed`, `seeds`,
`inventories`) is per-seat.

| field | our decoder |
|---|---|
| `obs["market"]["inventory"][item]`, `["prices"][item]` | `parse.parse_market(obs) → (inv[9], price[9])`, `parse.py:166-175`; on the view as `mkt_inv`, `price` (`parse.py:89-90`) |
| `obs["town"]["unlocked_shops"]` (list, **with replacement**) | `parse.parse_town(obs) → counts[8]`, `parse.py:177-182`; view field `shops` |
| `obs["farms"][1-player]` — `money`, `tiles` (crop, `yield_units`, `watered_today`, …), `hands`, `hires_today`, `unlocked_quadrants` | already read: `parse.parse_opp_commit` (`parse.py:102`), `parse.parse_opp_ripe` (`parse.py:134`) |
| `obs["step"] / ["day"] / ["hour"] / ["player"]` | `runtime.Runtime.act` (`runtime.py:35-38`) |
| previous inventory | `Runtime.prev_mkt_inv` / `dawn_mkt_inv` already exist (`runtime.py:33,44-54`) but rotate **per day**; a per-turn tell needs a per-turn rotation |

The plan is built once at hour 0 and replayed for 23 turns, and there is already exactly
one turn-time patch hook on the cached plan — `P.open_pump_tell_armed` /
`P.open_pump_tell_keep0` (`runtime.py:57-64`). A rival-sale tell is a second instance of
that same pattern: one `np.int32[9]` of state per turn, ~20 flops.

## 7. Spec for the follow-up reactive arm (10 lines)

1. State in `Runtime`: `prev_turn_inv[9]`, `riv_sold_hist` = a 6-turn rolling bool[6,9].
2. Each turn, before rendering: `net = prev_inv − inv + town_tick(step−1, shops) − our_ordsell(t−1) + our_ordbuy(t−1)` (sign per `infer.rival_net`); push `net ≥ 1`.
3. Decision it gates: `plan.SELL_SLOT_PRIORITY_ON`'s `batch` term in `plan.sell_slot_scores` (`plan.py:3986`), which today prices contestedness from `parse_opp_ripe` — *visible standing yield*, a proxy. Replace it with the rival's **measured** sale rate for that item.
4. `batch[item] = clip(mean units/turn over the last 6 turns the rival sold it, 8, 24)`; fall back to `opp_ripe` when the history is empty (days 0-1).
5. Gate: apply the reorder only to items with `riv_sold_hist[-6:, item].sum() ≥ 2` (V45 uses 4-of-6 for its clone gate; 2-of-6 keeps recall at 0.99 by §3).
6. Skip WHEAT and FERTILIZER in the gate — they are the only two items with recall < 1 and 100 % of the misses (§4); use them only as `opp_ripe` today.
7. Do **not** wire it to `OPEN_PUMP`: §5 shows it cannot see the opening. If the opening is retested, the instrument is the `excess` tell (recall 1.000 at ≥56, precision 1.000 at ≥101), not the pot.
8. Ship behind `RIVAL_TELL_ON=False`; the tell changes no order, no quantity and no turn by itself, so the first leg must be `assert`-level telemetry parity (0 coins on every board).
9. Screen on `S/simscreen/screen.py`, then ENG22, then BAND180 reading **margin**.
10. Judge caveat: byte-exact replay seats cannot react to us, so a *gate* measured on them is faithful (the tell reads their tape) while any *counter-reaction* is not — `nbintel` §6.2.

## 8. What this closes

* The town-tick model is not an approximation to be tuned — it is exact, and the
  estimator has **no free parameter**.
* The detector is a **net**, and therefore shares KEEP0's one defect on same-turn round
  trips. Candidate #5 stays open as a *sale-rate* instrument (7 of 9 items exact) and is
  **closed as an opening tell**; §5's `excess` is the opening instrument if one is ever
  wanted.
