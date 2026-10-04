# The purse side of the engine tape seat: instrumented, and the hire-cash hypothesis is REFUTED

Settles the "Next" item of `docs/strategy/2026-09-14-tape-map.md` §8 ("the next experiment is the purse side --
the five boards under 0.5 are all 'the tape cannot afford its own recorded row' ... log `money` alongside `owed`
and count the turns where an owed hire is dropped for cash rather than for roster parity") and §6's
"the residual is the cash spiral named in the hire-fix doc §4".
Built and measured 2026-09-14 10:01-10:21Z.

**VERDICT: REFUTED. Cash-dropped hires are NOT the first divergence on any of the 18 TOPB3 boards, and they are
not the residual at all: instrumented over all 36 games, HIRE-STICKY already lands EXACTLY the source episode's
season hire count on every board (286/286, 285/285, 263/263 ... `landed == owed`, 18/18 boards, both seats), and
the tape is short by only 0-142 hand-hours out of ~7,000. The first divergence is at step 0 -- day 0, hour 0, on
18 of 18 boards -- and it is a PRICE difference on the tape's own first recorded `BUY_ANIMAL,BUY_PRODUCT` row:
our seat pays 562 coins for what the source paid 533-565 for, because B, not the tape's original opponent, is
quoting against it. The first cash REFUSAL is a `BUY_SEED` at day 0 hour 20 on 12 of 18 boards (we hold 4 coins,
the seed costs 10 -- 6 coins short); the first cash-dropped HIRE is always later (d1h1 or d7h1) and always
recovered the same day. The repair was built anyway (`TAPE_PURSE_FIX=1` / `--hire-sticky-purse`, default OFF,
36/36 coin-identical off AND on, 60/60 on NEXTHIGH) and it is a measured no-op -- which is the evidence.
The residual is REVENUE, not the purse: the cash-OUT side is within 2 % of the source on every board
(-2,734 .. +570 coins over a season) while cash-IN is down 15,299-105,505, and the SELL-only rows of
108807571 earn 33,693 here against 106,922 in the source. The tape is open-loop and B denies its price.
No purse-side repair can make Majkel1337 readable; TOPB3 should be cut to its 9 readable boards.**

## 1. The instrument

`TAPE_PURSE_DEBUG=<dir>` (off unless set; pure observation, changes no action, sibling of `TAPE_MAP_DEBUG`) makes
the emitted package write one jsonl row per step carrying the map-side fields plus the purse side: `money` and
`hires_today` as the seat sees them at the START of the turn, `cost` = the engine's `_hire_cost`
(`mult * _fib(hires_today)`, kaggriculture.py:698) for the next hire this day, `afford`, `short` = `cost - money`,
and `ops` = the op names on the tape's own recorded market row. The 18 packages were re-cut with it
(`S/topb3/tapepurse/recut.sh`, 18/18 `frozen-identical`) and the whole leg re-run: **+26,829 leg mean margin,
36/36 rows coin-identical to `S/lossflip/topb3_Bmapfix.csv`** -- the instrument changes nothing.

The source episode's own purse at every step comes straight from the replay JSON
(`S/topb3/tapepurse/srcmoney.py` -> `srcmoney.json`): `steps[t][0]["observation"]["farms"][seat]["money"]` is the
opening purse of engine step `t`, the same counter the tape indexes by, so the two curves are directly comparable
and `money[s+1] - money[s]` is the cash step `s` produced on each side.

## 2. The hire side is already whole (`S/topb3/tapepurse/pursestats.txt`)

| episode | team | first hour the roster is short | cause | short | our purse | source purse | hires landed | hires owed | hand-hours short |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 108790149 | Majkel1337 | d1h1 | ROW | – | 0 | 0 | 285 | 285 | 6 |
| 108795516 | Majkel1337 | d1h1 | ROW | – | 0 | 0 | 286 | 286 | 142 |
| 108801472 | Majkel1337 | d1h1 | ROW | – | 0 | 1 | 286 | 286 | 6 |
| 108807571 | Majkel1337 | d7h2 | **CASH** | 20 | 14 | 174 | 286 | 286 | 37 |
| 108819121 | Majkel1337 | d7h2 | **CASH** | 13 | 21 | 27 | 286 | 286 | 28 |
| 108825010 | Majkel1337 | d7h2 | **CASH** | 6 | 28 | 0 | 286 | 286 | 29 |
| 108790159 | ymg_aq | – | – | – | – | – | 279 | 279 | 0 |
| 108806291 | ymg_aq | – | – | – | – | – | 263 | 263 | 0 |
| 108807563 | ymg_aq | – | – | – | – | – | 289 | 289 | 0 |
| 108814574 | ymg_aq | – | – | – | – | – | 277 | 277 | 0 |
| 108820106 | ymg_aq | – | – | – | – | – | 272 | 272 | 0 |
| 108826138 | ymg_aq | – | – | – | – | – | 286 | 286 | 0 |
| 108741964 | DSM | – | – | – | – | – | 287 | 286 | 0 |
| 108751325 | DSM | d7h4 | **CASH** | 28 | 6 | 61 | 286 | 286 | 20 |
| 108784054 | DSM | – | – | – | – | – | 287 | 286 | 0 |
| 108790144 | DSM | d1h1 | ROW | – | 0 | 0 | 286 | 286 | 6 |
| 108795512 | DSM | d8h2 | **CASH** | 34 | 0 | 27 | 286 | 286 | 1 |
| 108813021 | DSM | d7h2 | **CASH** | 9 | 25 | 290 | 287 | 286 | 4 |

* **`landed == owed` on 18/18 boards.** Every hire the source episode landed, the tape lands here. The `+1`s on
  the three DSM boards are the seat out-hiring its source by one, the `_MAP` pin the TAPE-MAP work fixed.
* The shortfalls are 6-34 coins, because `_hire_cost` is `1 * _fib(hires_today)` and a 10-hand day costs 143
  coins in total. A dropped hire means the seat is at zero, not that hiring is expensive.
* `cause ROW` at d1h1 is a one-turn lag, not a loss: the source is credited with the hand at the hour it
  computed the order, we land it an hour later.
* The damage is a LAG, and it is small: 0-142 hand-hours short out of ~7,000 hand-hours a season, i.e. at most
  2 % on the worst board (108795516) and 0.5 % on the median one.
* On the SIX ymg_aq boards -- the six that retain 1.02 -- the roster is never short for a single hour.

**So the hire-cash hypothesis cannot be the residual: there is no residual hire deficit to repair.**

## 3. What diverges first, with the step (`firstdiv.txt`, `firstrefuse.txt`)

**First divergence -- step 0, day 0 hour 0, on 18 of 18 boards, and it is a BUY price:**

| team | boards | our net change at step 0 | source's | gap | the row |
|---|---:|---:|---|---:|---|
| Majkel1337 | 6 | −562 | −533 .. −536 | −26 .. −29 | `BUY_ANIMAL,BUY_PRODUCT` |
| DSM | 6 | −562 | −533 .. −565 | −29 .. +3 | `BUY_ANIMAL,BUY_PRODUCT` |
| ymg_aq | 6 | −2,113 | −2,114 .. −2,189 | +1 .. +76 | `BUY_PRODUCT,SELL,HIRE×4,BUY_ANIMAL×2,BUY_SEED×2` |

Our figure is identical on all 18 boards (same board, same day-0 town, same theta B): the variation is entirely
the *source's*, i.e. what its original opponent was doing to the price at that instant. This is the shared pot,
and it is present before a single hand exists.

**First CASH REFUSAL** -- unambiguous, on rows whose market ops are all `BUY_*` so nothing can pay in mid-turn
and the source's purse falls while ours does not move at all (`_do_buy_*` is `if money < price: return`,
kaggriculture.py:663/674/680, silent exactly like `_do_hire`):

| episode | team | first refusal | our purse | the source paid | refusals all season | first cash-dropped HIRE |
|---|---|---|---:|---:|---:|---|
| 108790149 / 108795516 / 108801472 | Majkel1337 | **d0h20 `BUY_SEED`** | 4 | 10 | 11 / 11 / 9 | d1h1 |
| 108807571 / 108819121 / 108825010 | Majkel1337 | **d0h20 `BUY_SEED`** | 4 | 10 | 10 / 9 / 10 | d7h1 |
| all six | ymg_aq | **none, all season** | – | – | **0** | none |
| 108741964 / 108751325 / 108795512 / 108813021 | DSM | d0h20 `BUY_SEED` | 4 | 10 | 5 / 7 / 4 / 3 | – / d7h3 / d8h1 / d7h1 |
| 108784054 | DSM | d7h17 `BUY_SEED` | 27 | 50 | 2 | – |
| 108790144 | DSM | d2h13 `BUY_SEED` | 99 | 100 | 2 | d1h1 |

The traced day-0 sequence on 108795516 (`S/topb3/tapepurse/dbg_off.tar.gz`), our purse vs the source's:

```
 d  h     ourM     srcM       dM  live src  ops
 0  0     3000     3000        0     0   0  BUY_ANIMAL,BUY_PRODUCT   <== -562 vs -533: the price gap opens here
 0  1     2438     2467      -29     0   0  SELL,HIRE,HIRE,HIRE,HIRE,BUY_ANIMAL,BUY_ANIMAL
 0  2      564      588      -24     4   4  SELL
 ...                                        the -22 gap is carried, untouched, for 18 hours
 0 20        4       27      -23     4   4  BUY_SEED                 <== the source buys, we cannot: 6 coins short
 0 21        4       17      -13     4   4  BUY_SEED                 <== and again
 0 22        4        7       -3     4   4
 1  0        4        7       -3     0   0  HIRE x8                  <== 3 of 8 land; hire-sticky re-issues the 4th
 1  1        0        0        0     3   4
```

**CONFIRMED: a cash-dropped hire is never the first divergence. REFUTED as the residual.** The order of events is
always the same: a price gap at step 0 -> a refused `BUY_SEED` on the evening of day 0 -> a hire dropped later and
recovered within the day.

## 4. The residual is REVENUE, not the purse (`flows.txt`)

Per-step purse changes summed into cash-IN (the positive ones: SELLs) and cash-OUT (the negative ones: BUY_*,
HIRE, BUY_LAND), ours against the source's, over the 719 steps:

| episode | team | cash-IN ours | source | **ΔIN** | cash-OUT ours | source | **ΔOUT** | SELL-only rows ours | source | retention |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 108790149 | Majkel1337 | 84,499 | 100,626 | **−16,127** | 16,065 | 17,572 | −1,507 | 52,117 | 66,284 | 0.83 |
| 108795516 | Majkel1337 | 31,065 | 83,756 | **−52,691** | 13,447 | 16,181 | −2,734 | 12,758 | 36,225 | 0.27 |
| 108801472 | Majkel1337 | 98,798 | 114,097 | **−15,299** | 15,842 | 17,205 | −1,363 | 62,054 | 72,606 | 0.85 |
| 108807571 | Majkel1337 | 58,433 | 163,938 | **−105,505** | 19,820 | 19,250 | +570 | 33,693 | 106,922 | 0.27 |
| 108819121 | Majkel1337 | 73,103 | 147,695 | **−74,592** | 17,300 | 19,923 | −2,623 | 33,141 | 77,245 | 0.44 |
| 108825010 | Majkel1337 | 53,079 | 111,068 | **−57,989** | 12,871 | 15,334 | −2,463 | 26,130 | 61,669 | 0.44 |
| 108790159 | ymg_aq | 110,275 | 109,155 | +1,120 | 27,954 | 30,957 | −3,003 | 50,613 | 52,696 | 1.05 |
| 108806291 | ymg_aq | 145,041 | 144,018 | +1,023 | 28,711 | 29,183 | −472 | 103,733 | 104,978 | 1.00 |
| 108807563 | ymg_aq | 164,323 | 162,214 | +2,109 | 36,483 | 36,678 | −195 | 86,269 | 86,413 | 1.01 |
| 108814574 | ymg_aq | 132,443 | 138,194 | −5,751 | 29,569 | 30,257 | −688 | 75,480 | 83,347 | 0.95 |
| 108820106 | ymg_aq | 96,257 | 93,564 | +2,693 | 25,786 | 27,709 | −1,923 | 61,555 | 61,529 | 1.04 |
| 108826138 | ymg_aq | 151,979 | 149,711 | +2,268 | 35,861 | 36,366 | −505 | 75,156 | 73,397 | 1.02 |
| 108741964 | DSM | 95,652 | 125,479 | **−29,827** | 15,367 | 16,568 | −1,201 | 57,524 | 76,744 | 0.73 |
| 108751325 | DSM | 54,361 | 120,516 | **−66,155** | 14,565 | 15,779 | −1,214 | 24,359 | 67,005 | 0.39 |
| 108784054 | DSM | 94,821 | 116,619 | **−21,798** | 17,235 | 16,934 | +301 | 49,249 | 59,735 | 0.77 |
| 108790144 | DSM | 119,787 | 122,325 | −2,538 | 16,801 | 18,491 | −1,690 | 67,860 | 69,723 | 0.98 |
| 108795512 | DSM | 165,493 | 167,535 | −2,042 | 18,791 | 19,240 | −449 | 96,695 | 101,201 | 0.98 |
| 108813021 | DSM | 61,671 | 78,592 | **−16,921** | 14,787 | 16,263 | −1,476 | 28,557 | 39,015 | 0.74 |

* **Cash-OUT tracks the source within 2 % on every board of all three teams (−3,003 .. +570 coins on a
  12,871-36,483 season spend).** The tape buys what it recorded, hires what it recorded and pays what it
  recorded. The purse is not the constraint on what the tape DOES; the 2-11 refused seeds a season cost
  20-110 coins directly.
* **The entire retention gap is cash-IN.** On the six ymg_aq boards ΔIN is +1,023 .. +2,693 (five of six are
  *better* here than in the source) and retention is 1.02. On 108807571 the identical recorded SELL orders earn
  33,693 against 106,922 -- a third.
* So retention on the Majkel1337 and the low DSM boards measures **B denying their price**, not a defect of the
  seat. The recorded player would have re-routed to another buyer; a tape cannot. That is an open-loop ceiling
  and no repair inside `scripts/tape_opponent.py` can lift it.
* Corroboration (`float.txt`): the six ymg_aq boards spend **0** hours of 719 under 10 coins here (their source
  spends 0-7), while the Majkel1337 boards spend 11-49 (their source 5-22). The team whose recording holds a
  float is the team whose retention is 1.00; the team that runs to the last coin converts the price gap into
  refused orders. But even that is the second-order term: the first-order term is the crushed SELL price.

## 5. The repair, built and measured as a no-op

`scripts/tape_opponent.py --hire-sticky-purse` bakes `_PURSE_FIX_DEFAULT = True`; `TAPE_PURSE_FIX=0/1` wins at
run time (no `KAGG3_` prefix -- `eval_vs_baselines._vendored_imports` clears that namespace for file agents).
Default **OFF**, and inert unless hire-sticky is on.

What it changes: plain hire-sticky caps the owed-hire re-issue at `room = _src_hands(step + 1) - live`, and at
the day's LAST hour `_src_hands(step + 1)` is already the next day's empty roster, so hour 23 is blacked out and
an owed hire never gets its final try. With the repair on, that one hour is capped at `_src_hands(step)` -- the
source's roster at THIS hour -- so the re-issue happens at every later hour of the same day, the last included.

What it deliberately does NOT change: a hire owed at midnight is not carried over. The engine wipes `hands` and
`hires_today` every night (kaggriculture.py:880-882), the next day's owed list is recomputed from the source's
own roster, and carrying a debt would let the tape out-hire the seat it is impersonating -- the one invariant
hire-sticky exists to keep. It gives the tape no money and touches no engine file.

* **Default-off equivalence: 36/36 TOPB3 rows coin-identical to `S/lossflip/topb3_Bmapfix.csv`**
  (`rowdiff.py` -> `0 differ`), leg mean margin +26,829 -- and the 18 re-cut packages are 18/18
  `frozen-identical` (`verify_frozen_match`, 10,815 (step, roster) pairs each).
* **Repair ON: also 36/36 coin-identical, +26,829.** A measured no-op, on every board, both seats. This is the
  quantitative form of the verdict: there was no hire the purse was still losing.
* **NEXTHIGH non-regression, 30 tapes re-cut (30/30 frozen-identical), hire-sticky + map fix + purse fix all
  ON: 60 of 60 games coin-identical** to `nexthigh_nhmapfix.csv` AND to `nexthigh_Bhire.csv`
  (`rowdiff.py` -> `0 differ` both ways), retention 0.99, leg mean margin +2,045, win 53.3 %.

## 6. Retention, TOPB3, 18 boards, theta B = `flow193_g100_hr` (`submission/theta.npy`), switches
`OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON,HIRE_ROW_ON`

`S/topb3/tapemap/retain3.py` -> `S/topb3/tapepurse/retain3.txt`. FROZEN = `S/lossflip/topb3_B.csv`;
+REMAP = `topb3_Bmapfix.csv`; +PURSE = `topb3_Bpursefix.csv`.

| team | n | frozen | sticky + REMAP (before) | sticky + REMAP + PURSE (after) |
|---|---:|---|---|---|
| Majkel1337 | 6 | 0.25, 0/6 ≥ 0.85, 0/6 ≥ 0.95 | 0.52, 1/6, 0/6 | **0.52, 1/6, 0/6** |
| ymg_aq | 6 | 1.02, 6/6, 6/6 | 1.02, 6/6, 6/6 | **1.02, 6/6, 6/6** |
| DSM | 6 | 0.65, 1/6, 1/6 | 0.78, 2/6, 2/6 | **0.78, 2/6, 2/6** |
| ALL | 18 | 0.64, 7/18, 7/18 | 0.78, 9/18, 8/18 | **0.78, 9/18, 8/18** |

Unchanged board for board and coin for coin. **9 of 18 readable, below the 12/18 bar, so the B baseline on the
readable set is quoted only for completeness** (it is the TAPE-MAP number, unmoved):

| leg | boards | games | win | mean margin | sd | t |
|---|---:|---:|---:|---:|---:|---:|
| frozen | 7 | 14 | 0.0 % | −12,599 | 6,019 | −5.54 |
| **+REMAP +PURSE** | **9** | **18** | **22.2 %** | **−7,139** | **13,324** | **−1.61** |

Per team on the readable set: ymg_aq 6 boards, 0 % win, **−13,751/board (sd 5,684, t −5.93)**; DSM 2 boards,
50 % win, −2,551; **Majkel1337 1 board (108801472, ret 0.86), 100 % win, +23,359 -- still n = 1.**

**B vs Majkel1337, the rank-1 file (sub 56156662, 3204.4), remains UNMEASURED.** The only statistically real
reading TOPB3 supports is B vs ymg_aq: −13,751/board, t −5.93, 0 wins in 12 games.

## 7. Files

* `scripts/tape_opponent.py` -- module docstring (:39-48); `_farm` helper (:166-171) and `_hand_count` on top of
  it (:173-174); `_PURSE_FIX_DEFAULT` template constant (:131-133); `_fib` (:256-262) and the extended
  `_debug_log` with the `TAPE_PURSE_DEBUG` branch (:264-306, off unless the variable names a directory);
  `_purse_fix_on` (:337-370); the `room` branch in `_hire_sticky_agent` (:434-441); the farm/mult arguments at
  the `_debug_log` call site (:444-445); `render_main(purse_fix=...)` (:567/:578); `--hire-sticky-purse`
  (:682-689, :715, :742).
* `tests/test_tape_purse_fix.py` -- 9 tests: default-off equivalence against the pre-purse package with the map
  fix both off and on, over a roster sequence that keeps a hire owed through hour 23; the frozen path untouched
  with both switches forced on (`verify_frozen_match`); the synthetic purse sequence (hour 23 re-issues only
  with the repair, hours 1-22 identical either way); owed NOT carried across midnight; never hiring past the
  source roster.
  `JAX_PLATFORMS=cpu .venv/bin/python -m pytest tests/test_tape_purse_fix.py tests/test_tape_map_fix.py
  tests/test_tape_hire_sticky.py -q` -> `..........................` (26 passed).
* `S/topb3/tapepurse/` -- `recut.sh` + `recut.log`/`recut2.log`/`recut_nh.log`, `run.sh`, `run_nexthigh.sh`,
  `srcmoney.py` + `srcmoney.json` (the source purse curves), `pursestats.py` + `pursestats.txt`,
  `firstdiv.py` + `firstdiv.txt`, `firstrefuse.py` + `firstrefuse.txt`, `flows.py` + `flows.txt`,
  `daycurve.py` + `daycurve.txt`, `float.py` + `float.txt`, `retain3.txt`, `legs.log`, `logs/`,
  `dbg_off.tar.gz` (36 jsonl, the whole instrumented leg; `tar xzf` it in place and every analysis script
  above re-runs against `dbg_off/`), `tapes/` (18 TOPB3 + 30 NEXTHIGH packages).
* `S/lossflip/topb3_Bpurseoff.csv` (repair off) and `S/lossflip/topb3_Bpursefix.csv` (repair on) -- both 36/36
  identical to `topb3_Bmapfix.csv`; `S/lossflip/nexthigh_nhpursefix.csv`.

## 8. Recommendation and next

1. **Cut TOPB3 to its 9 readable boards and quote it as such** -- 6 ymg_aq, 2 DSM, 1 Majkel1337 -- exactly the
   contingency `2026-09-14-tape-map.md` §8 named. The unreadable nine are not broken seats: their cash-OUT
   reproduces the recording to within 2 % and their roster to the hire. They are measuring B's price denial
   against an opponent that cannot re-route, which inflates B's margin, so leaving them in would make TOPB3 read
   BETTER than B is.
2. **Stop repairing the tape seat.** Three repairs (hand truncation, hire-sticky, map remap) have taken the seat
   from 7/18 to 9/18 readable; the fourth is a measured no-op; and the decomposition says the remainder is not
   in the seat at all. The ceiling is open-loop-ness.
3. **The next experiment is a price-neutral or closed-loop instrument for the rank-1 file**, not another tape
   flag. Two candidates, in order of cost:
   * *Sell-side neutrality probe*: replay the 6 Majkel1337 boards with B's own SELL orders suppressed (or routed
     to a different product) and read the tape's retention. If retention goes to ~1.0, the 0.52 is B's denial
     and TOPB3's Majkel boards are quantifying a real lever rather than a defect -- which would make "how much
     of B's +89,834 margin is price denial" the interesting number, measurable directly.
   * *Closed-loop reconstruction*: Majkel1337's recorded behaviour is a `BUY_ANIMAL`/`BUY_SEED`-heavy ramp that
     runs the purse to the last coin every day; a reconstruction in our own planner's terms (unlike the class-A
     clones, this one has a visible and simple ramp) would re-route and would be a real gate.
