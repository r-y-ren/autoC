# 2026-09-14 — what removes the sheep and cows under `MELON_OPEN_ON`: the day-0 purse

**Sim, descriptive, paired, CRN.** First three rows of `S/simscreen/boards_topb2.json`, theta B
= `flow193_g100_hr`, action-replay opponent seat. No engine games, no training arm, no `src/`
edit. Tool `S/melon_mech/trace.py` (a cut-down `S/melon_decomp/ledger.py` that re-runs
`brain.decide` + `plan.build_day` on the dawn state the day is planned from and records the
whole animal path); raw `tr_<arm>.npz`, report `report.py`. Arms: `Bnb` (the melon arms' true
control, `OPEN_PUMP_ON,TAIL_FILL_ON,HIRE_ROW_ON`), `M4`, `M12` (`+MELON_OPEN_ON`,
`MELON_OPEN_TILES` 4 / 12). Follows `2026-09-14-melon-decomposition.md`, which measured the loss
(−23,517/board at 12 tiles, displacement of the animal line) but did not trace it. Rows 0 and 1
are one tape+seed in the two seats and give the identical farm: **two** boards.

## 1. Verdict

**Candidate (b), and the refusal is by COINS, not tiles or turns:** the melon seed bill is paid
out of the very purse that buys the opening herd, on day 0, inside one `budget.grant` walk.
**(a) refuted** — the decode is identical on day 0. **(c)** costs one animal of nine. **(d)**
happens, one day late, and is itself a consequence of (b).

## 2. Board 0, days 0-12 (Bnb | M4 | M12 in each cell)

`want` = `macro.animal_want`; `rows` = BUY_ANIMAL units emitted; `got` = units the market
delivered; `free` = `brain.n_free_slots`. G/C/S. (d2 and d4 omitted: identical to d1 / d3 in
every column.)

| d | money | free | want | rows | got | alive | quad |
|---|---|---|---|---|---|---|---|
| 0 | 3000 \| 3000 \| 3000 | 25\|25\|25 | 1/4/1 \| **1/4/1** \| **1/4/1** | 1/4/1 \| 1/4/1 \| **1/4/0** | 1/4/1 \| **1/4/0** \| **1/3/0** | 0/0/0 | 1\|1\|1 |
| 1 | 146 \| 406 \| 286 | 0\|0\|1 | 0/0/0 | 0/0/0 | 0/0/0 | 1/4/1 \| 1/4/0 \| 1/3/0 | 1\|1\|1 |
| 3 | 614 \| 746 \| 586 | **8\|4\|1** | 0/0/0 | 0/0/0 | 0/0/0 | 1/4/1 \| 1/4/0 \| 1/3/0 | 1\|1\|1 |
| 5 | **1370 \| 1191 \| 764** | 1\|1\|1 | 0/1/0 \| 0/1/0 \| 0/0/0 | 0/1/0 \| 0/1/0 \| 0/0/0 | same | 1/4/1 \| 1/4/0 \| 1/3/0 | 1\|1\|1 |
| 6 | 859 \| 902 \| 2025 | 9\|12\|1 | 0/0/0 \| 0/0/0 \| **0/1/0** | 0/0/0 \| 0/0/0 \| **0/0/0** | 0/0/0 | 1/5/1 \| 1/5/0 \| 1/3/0 | **2\|2\|1** |
| 7 | 744 \| 615 \| **250** | 6\|6\|**12** | 0/0/1 \| 0/1/0 \| **0/1/0** | 0/0/0 \| 0/0/0 \| **0/0/0** | 0/0/0 | 1/5/1 \| 1/5/0 \| 1/3/0 | 2\|2\|2 |
| 8 | 1995 \| 739 \| **501** | 10\|9\|**14** | 0/1/2 \| 0/1/2 \| **0/2/1** | 0/1/2 \| **0/1/0** \| **0/0/0** | = rows | 1/5/1 \| 1/5/0 \| **0**/3/0 | 2\|2\|2 |
| 9 | 1288 \| 777 \| **441** | 10\|11\|8 | 1/1/0 \| 1/1/1 \| **0/1/1** | 1/1/0 \| **0/0/1** \| **0/0/0** | = rows | 1/6/1 \| 1/6/0 \| 0/3/0 | 2\|2\|2 |
| 10 | 6679 \| 6313 \| 4687 | 1\|8\|16 | 1/1/2 \| 1/1/3 \| 1/1/2 | granted in full, all arms | | **2/7/3 \| 1/6/1 \| 0/3/0** | 2\|2\|2 |
| 11 | 4763 \| 7996 \| 11478 | 13\|1\|8 | 1/0/0 \| 1/0/1 \| 1/1/1 | granted in full | | 3/8/5 \| 2/7/4 \| 1/4/2 | **3\|2\|2** |
| 12 | 6292 \| 9289 \| 13000 | 7\|13\|20 | 0/0/0 \| 1/0/0 \| 1/0/1 | granted in full | | 4/8/5 \| 3/7/5 \| 2/5/3 | 3\|3\|3 |

From d10 the melon cash lands and rows are granted again — but the herd is nine animals behind
and never catches up inside the window milk/wool/egg pays in.

## 3. Day 0 in coins — the whole mechanism in one line

`macro.plant_target` is **identical** in all three arms (`[11,11,0,0,0]`) and so is
`macro.animal_want` (`[1,4,1]`). Only the bill differs:

| arm | day-0 seed bought | seed coins | animal coins paid | herd at dawn d1 |
|---|---|---|---|---|
| Bnb | 11 WH, 8 CA | **270** | 300+1,600+500 = **2,400** | 1/4/1 |
| M4 | 11 WH, 4 CA, **4 ME** | **510** (+240) | 300+1,600+**0** = **1,900** | 1/4/**0** |
| M12 | 7 WH, **12 ME** | **1,030** (+760) | 300+**1,200**+0 = **1,500** | 1/**3**/**0** |

Melon seed is 80 a tile against carrot 20 and wheat 10 (`spec.CROP_SEED_COST`), so 12 melon
tiles cost **+760 coins** of a 3,000-coin day-0 purse and the herd comes out exactly **900
coins** smaller (one COW + one SHEEP); M4 is +240 of seed against −500 of herd. The purse
identity closes to the coin (Bnb spends 2,854 on day 0; M4 2,594 = 2,854+240−500; M12 2,714 =
2,854+760−900) — which is why `2026-09-14-melon-decomposition.md` read **dawn cash d1-d5 as
unchanged**: the coins the herd did not cost are still sitting in the purse. Flat dawn cash
refuted *starvation*; it never refuted *substitution*.

**The two gates, exactly.**

* **M12's SHEEP never reaches a market row** (d0 `rows` 1/4/**0**). The greedy drops it:
  `budget.grant` walks one candidate vector holding the five seed lists and the three animal
  lists together (`plan._wants` :4696-4741 builds it, `plan.py:5426` slices `a_buy` out of the
  grant) by value per coin down `purse` (:5361). Twelve melon seeds at 80 outrank the 500-coin
  SHEEP.
* **M4's SHEEP and M12's fourth COW are emitted and then refused by the engine** (`rows` 1/4/1 →
  `got` 1/4/0). The market clips each BUY slot to the money standing when it resolves
  (`sim/market.process_slot`), and the seed rows are ahead of the animal rows in `plan._market`
  (:7677, :7816).
* **SHEEP goes first** because it is last in the shared walk: `_place_split` (:4400) and
  `a_buy`'s `_share` (:5426) serve GOOSE, COW, SHEEP out of one budget via `BEFORE_ALL` (:4168)
  — want `[1,2,2]` against a shared room of 0..5 is served `[0,0,0] [1,0,0] [1,1,0] [1,2,0]
  [1,2,1] [1,2,2]` (checked directly). Hence SHEEP collapsing at **4** tiles (3.26→0.68) while
  COW bends.

## 4. Days 1-9: cash drought, not tile budget

`CROP_FIRST_YIELD_DAY[MELON] = 10`, `CROP_ONGOING[MELON] = 0` against WHEAT 2/4 and CARROT 2/3,
and `brain.n_free_slots` (:164-180) / `plan._derive`'s `free_slot` (:4978, :5143) free a one-
time crop only at `age >= clip(pay_day − t_day, first, sat)` — d10 for melon, d4 for wheat, d3
for carrot — so the plate pays nothing and frees nothing before d10. M12 runs 4-7 wheat tiles on
d5-d9 where the control runs 11-19 and holds **250 / 501 / 441** coins at dawn d7/d8/d9 against
744 / 1,995 / 1,288; every `animal_want` of d6-d9 is emitted as **zero** rows. Tiles are **not**
what binds: at d7/d8/d9 M12 has **12 / 14 / 8** free slots against 6 / 10 / 10 and still buys
nothing. The tile squeeze is real but confined to d1-d6 (M12 `free` 1,1,1,8,1,1 vs
0,0,8,13,1,9), where the decoded want is 0 anyway.

**(d) land is a consequence.** `buy_land` needs `money >= land_cost − rev1` (:5339, :5358). The
control buys quadrant 2 during d5 holding 1,370 coins; M12 holds 764 and buys during d6 — one
day late — and the 1,000 coins it then spends are what refuses the d6 COW (`want` 0/1/0, `rows`
0/0/0 at 2,025 coins). Quadrant 3: d10 vs d11.

**(c) deaths: one animal, one board.** M12 board 0 loses its GOOSE between dawn d7 and d8 (1/3/0
→ 0/3/0) after emitting 3 FEED ops for 4 animals; feeds are rationed by the wheat the day could
buy (`want_feed = feed_pass & (feed_rank < wheat_avail)`, :5460) and M12's wheat line is 4-6
tiles there. No other death in either arm on either board — a secondary channel.

**(a) is refuted.** `plant_total = n_dev − sum(animal_want)` (brain.py:947) runs the other way,
and `_melon_open` (plan.py:4581-4614) rewrites `plant_target` *after* `brain.decide` returns,
inside `_plan_and_stats` (:5892), preserving `sum(plant_target)`. Measured: `plant_target` and
`animal_want` are identical across the three arms on day 0; `animal_want` first differs on
**d5** (M12) / **d7** (M4), after the herd is gone — a response to the damaged board, not its
cause.

## 5. Board 2 (tape 107450553) — same mechanism, same day

| arm | d0 want | d0 rows | d0 got | rows d0-9 | alive d10 | alive d15 | quad 2 |
|---|---|---|---|---|---|---|---|
| Bnb | 1/4/1 | 1/4/1 | 1/4/1 | 2/4/5 | **2/4/5** | 6/4/6 | d5 |
| M4 | 1/4/1 | 1/4/1 | **1/4/0** | 1/4/3 | 1/4/2 | 6/4/5 | d5 |
| M12 | 1/4/1 | **1/4/0** | **1/3/0** | 1/4/0 | **1/3/0** | 8/3/3 | d6 |

Identical day-0 seed bills (270 / 510 / 1,030) and herd bills (2,400 / 1,900 / 1,500); M12 dawn
money d7/d8/d9 = 240 / 494 / 546 against 887 / 1,698 / 1,025, and no M12 animal row on d1-d9.
Board 1 reproduces board 0 to the unit.

## 6. Is a non-displacing melon build possible?

**Not by moving the mix, and not as a decoder gene.** The binding constraint is one scalar — the
day-0 purse — and melon is the dearest seed in the game (80 vs wheat 10 / carrot 20) on the
slowest payback (d10 vs d4 / d3): 960 coins of a 3,000-coin opening, competing head-to-head with
300/400/500-coin animals inside a single `budget.grant` walk, which the greedy resolves
correctly given its inputs. The ES cannot rank animals above melon without unranking them
against every other seed too — `animal_want` and `plant_target` enter `grant` as *wants*, not
priorities, and the only genes on that walk are `grow_mult`, `hold`, `press` and `hire_bias`,
none a melon-versus-sheep dial. The one additive lever is **land**: a quadrant is 1,000 coins
for 25 tiles (`spec.LAND_PRICES`, `brain.LAND_TILES`) and `land_bias` (brain.py:895-899) *is* a
gene, so "buy quadrant 2 on day 0, melon on the new tiles" is expressible — but it does not
escape the purse: 1,000 + 960 = 1,960 of 3,000 against a 2,400-coin opening herd is the same
displacement one level up, and this trace already shows the melon arm delaying its land a day
for want of ~240 coins. An additive build needs the melon paid out of revenue the opening does
not yet have, i.e. a **later** plate (after the d10-d14 melon and strawberry cash and a third
quadrant) — a different switch from `MELON_OPEN_ON`. **For a day-0 plate the coupling is
structural: one purse, one greedy, melon at 8x wheat seed for a 10-day wait.** A hand rule
exempting the animal lists from the grant would not fix it: the coins are absent.

## 7. Limits

* Two farms, one theta, the sim. `S/melon_decomp` validated arm B against
  `S/simscreen/topb2_40.csv` on 40/40 boards at max |Δmargin| = 0 and those rows track the
  engine at |Δd| ≤ 45 coins on 6 thetas; **no engine leg of a melon arm has ever been run.**
* **UNVERIFIED:** I recorded `view.money` at dawn, not the purse the grant walks (`money −
  hire_bill − reserve − land_gap`, :5137-5141, :5361) — for d7-d9 the dawn purse is 240-546
  against a 300-500 coin animal, but not which of the three deductions closed the last coins.
  `nhands` reads 0 at every dawn in every arm (as in the earlier ledger), so hires could not be
  compared; feed counts are FEED ops emitted, not fed animals.
