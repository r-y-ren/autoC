# IDLE_PURSE_TOPUP_ON — build, identity, paired judge, verdict (2026-09-11)

Candidate (1) of `2026-09-11-labour-compounding.md` §5/§6 (consensus §30): spend the coins
the day's greedy leaves idle overnight on days 0-9 on the cheapest positive-value plantings
legal today, so the hire enumeration that follows prices an enlarged task list and the crew
follows the work. Built as a default-OFF switch, judged paired on candidate B's theta.

Worktree `.claude/worktrees/purse-topup` (branch `purse-topup` off `ship-pair-hr` b1bde4f),
commit **6548777**. Theta `artifacts/kagg2_games/thetas/flow193_g100_hr.npy` (candidate B).
Nothing merged, shipped, or launched; the ES and launchers untouched.

## 1. Mechanism as implemented (`src/kagg3/core/plan.py`, worktree line numbers)

* Constants `:4338-4368` (block comment `:4338-4359`): `IDLE_PURSE_TOPUP_ON = False`, `IDLE_PURSE_TOPUP_DAYS = 10`
  (fires on days `< DAYS`), `IDLE_PURSE_TOPUP_KEEP = 200` (coins left on top of the
  structural `cash_reserve`), `IDLE_PURSE_TOPUP_LAND_HOLD = True` (hold `land_gap` back on a
  day the land valuation wants a quadrant it cannot fund: `nquad < 4 & ~terminal & buy_land
  == 0 & land_value + land_bias > 0`).
* Helper `_purse_topup` `:4371-4417`: a second `budget.grant` over the five seed lists alone
  (non-seed wants zero) on `purse_t = spend(seed part of n_buy) + extra_purse`, where
  `extra_purse = max(purse_left − hold − KEEP, 0)` on days `< DAYS`; each crop's want is
  `n_buy[c] + room_t`, `room_t = seed_cap − Σ min(fill_target, seeds + seed_buy)` (free tiles
  after today's builds and plantings, via `_seed_room`); `extra = max(n_top − n_buy, 0)`
  prefix-clipped in crop order to `room_t` (the `_wants` cumsum trick). Returns `n_buy`,
  `fill_target` and `purse_left` with the extra seed added.
* Hook `:5553-5560`, immediately after `purse_left` (the grant's leftover, already net of
  hire bill, `cash_reserve` and `land_gap`: `money` `:5244-5245`, `land_gap` `:5446`, `purse`
  `:5468`, `BUD.grant` `:5490`, `purse_left` `:5552`) and before `plant_eff = min(fill_target,
  seeds + seed_buy)` `:5564`, so the extra seed rides into the BUY row (`seed_buy` →
  `_market`) and the plant clip (`plant_here` / `p_cum`), and both `_derive` passes of the
  hire enumeration (`:6089` pass A on bill 0; `:6231` pass B on the winner's bill) see
  the enlarged task list.
* Funding rule is `PLANT_FILL_ON`'s (`:4238-4336`): seeds re-solved over their own coins plus
  the leftover, non-seed lists frozen, so the two walks never pass `purse`. OFF, the helper is
  never called and every expression downstream is the one it was.

## 2. Identity (must be byte-exact) — PASS

LIVE-C boards 43-45, both seats, `OPEN_PUMP_ON=True`, seed base 777001 + 1000003·42, candidate
B, worktree vs `ship-pair-hr`: csv `diff` empty (6 rows, every column). The same rows match
`S/lossflip/flow193_g100_hr_livech.csv` to the coin, validating it as the pairing base (it came
from `arms-next`, whose only diff to `ship-pair-hr` is the three switch defaults the run forced
ON). `S/drainpin/on2b.py` splits the switch string on **commas**, not spaces.

## 3. Judge — paired against candidate B's own csvs (`S/bank/paired.py`, `ALL` rows)

`purseB` = `OPEN_PUMP_ON=True,IDLE_PURSE_TOPUP_ON=True` (KEEP 200, DAYS 10, LAND_HOLD on):

```
leg                  n   off     on     d-margin  sd    t      d-ours d-theirs  +  -  =  boards t_rows
LIVE-C 43-72   ALL   60  63.3%   60.0%     -266   1927  -0.76    -105     162   0  2  8    30   -1.07
LIVE-C 73-102  ALL   60  83.3%   80.0%     -457   1464  -1.74      54     511   0  2  8    30   -2.42
TOPB2          ALL   40  32.5%   32.5%     -178   2211  -0.38    -109      69   0  0  2    20   -0.51
```

Pooled hold-out 43-102: 120 games, 73.3 % → 70.0 % (−3.3 win points), d-margin −361/game,
flips +0/−4, 16 rows (8 boards) identical to the coin. csvs `S/lossflip/purseB_{livech,livech2,topb2}.csv`.

`purseC` = KEEP 0, DAYS 12 (the variant the mechanism check below motivates — d10 is the one
day with both idle coins and free tiles), same legs, same base:

```
LIVE-C 43-72   ALL   60  63.3%   43.3%    -4426   4160  -5.80   -1448    2978   0 12  0    30   -8.24
LIVE-C 73-102  ALL   60  83.3%   53.3%    -5245   5587  -5.11   -2101    3144   0 18  0    30   -7.27
TOPB2          ALL   40  32.5%   20.0%    -4400   5551  -3.52   -1494    2907   0  5  0    20   -5.01
```

Pooled hold-out: 73.3 % → 48.3 % (−25 points), −4,836/game, flips +0/−30; TOPB2 −12.5 points.
csvs `S/lossflip/purseC_{livech,livech2,topb2}.csv`.

## 4. Read-out — KILL (both configurations), and the premise does not hold

`purseB`: pass needed pooled ≥ +3 win points with d-margin > 0 and TOPB2 not down > 2 games; got −3.3
points, d-margin −361, TOPB2 level. Kill rule: d-theirs > 0 on all three legs (+162 / +511 /
+69) and d-ours < 0 with win rate down on 43-72 — displacement plus opponent handed back.
At t −0.8 / −1.7 / −0.4 with one or two seeds changed a game, most of the spread is the shop
re-roll (one RNG draw per empty tile); either way there is no positive evidence.

`purseC` (KEEP 0, DAYS 12) is the kill in its strongest form: d-ours −1.4-2.1k **and**
d-theirs +2.9-3.1k on every leg, t −5.8 / −5.1 / −3.5, 30 of 60 hold-out boards flipped to
losses, none the other way. Replay diff vs OFF (three boards): with KEEP 0 the 80-100 coin
hour-1 leftovers buy +3 wheat on d3, +5-7 wheat on d5 (quad 2 day), +2-4 MELON seeds (250c
each — the ratio walk reaches melon once wheat's stream saturates) on d6; those tiles then
displace the d8-9 plantings (WHEAT −3/−4, STRAWBERRY −1/−2, MELON −1/−2), hands move ±1 only
(+1 d3/d7, −1 d8-9), end-of-day cash trails OFF by 1.5-2.3k from d14, and the opponent ends
+0.8-5.9k richer (board 2079139712: theirs 85,834 → 91,690). This is `PLANT_FILL_ON` v2's
post-mortem (`plan.py:4238-4336`, −9,085 t −10) reproduced: an extra crop tile is bought with
the herd's tiles and the herd's labour, and the fertilizer/egg/wool lines it evicts are the
opponent's prices handed back.

**Mechanism check (pass-B `_derive` internals + replay diff, three boards, `scratchpad/mech/`).**
The "0.6-5.7k idle overnight on d2-9" is an *end-of-day* purse. At the hour-1 BUY row — the
only point the planner spends — the leftover after bill, reserve, land gap and grant
(`purse_left`) is **4-108 coins on d1-6 and d9**, 290-390 on d7-8 (three boards, e.g.
144/23/96/83/32/28/330/389/70). The end-of-day cash is the day's sales landing at turns 3/10/18
*after* the BUY row; the next morning's greedy spends it (d5: 1,440-1,460 → quad 2, 17-38
left; d10: quad 3). It idles ~23 hours because the planner buys once a day, not because wants
are exhausted. And free-tile room after builds and plantings (`room_t`) is **0-3 on d0-4 and
d6-9** (8 on d5, eaten by quad 2): the board is full. So the top-up fired on d7-8 only (+1
wheat / +1 melon seed), never on board 2097576449 (94,079 → 94,337 / +0 / 87,869 → 88,935 on
the three boards); HIRE counts identical d0-6; `LAND_HOLD` inert (hold 0: `land_value` is 0
off the buy day).

From d10 the picture inverts: `purse_left` is 1,850-4,850 coins on d10-12 with room 10-12 on
d10 (post quad 3) and 1-3 on d11-12 — the idle purse is real there and it is *tile-bound*
(`plant_target` exhausted and no land left to buy at the price). That is the ES's plate
choice, and the one day the switch could act on is d10; `purseC` tests exactly that.

## 5. What next

* **Close IDLE_PURSE_TOPUP** — do not tune KEEP/DAYS further. As specified (KEEP 200, d0-9)
  it is inert-to-slightly-negative because the overnight purse is intra-day revenue the next
  morning's greedy already spends and the board has no free tiles on d1-9; with the floor
  removed (KEEP 0, d0-11) the 80-100 coin crumbs buy wheat/melon tiles that displace the herd
  and lose −4.4k to −5.2k a game at t −5. The labour/capital family closes with melon, wool
  and mix (labour-compounding §6's own stop rule: displacement → close). Switch stays in the
  worktree as the measured negative; nothing to merge.
* What stands: the planner buys once, at hour 1, and the day's revenue (0.6-2k on d3-9) waits
  23 hours — a PRESTOCK / intraday-market question (`PRESTOCK_ON` exists, asserted incompatible
  with `EARLY_SELL_ON`), not a planting one, and it still needs free tiles, which d1-9 lack
  except on the land days (d5, d10). d10-12's idle 1.9-4.8k sits against 1-3 free tiles: the
  slack there is tile-bound, i.e. land/plate sizing (theta), not cash.

Files: `scratchpad/mech/` (per-day tables, planner internals); `S/lossflip/purse{B,C}_*.csv`;
`S/livec/purse{B,C}_holdout*.log`, `S/topb2/purse{B,C}.log`.
