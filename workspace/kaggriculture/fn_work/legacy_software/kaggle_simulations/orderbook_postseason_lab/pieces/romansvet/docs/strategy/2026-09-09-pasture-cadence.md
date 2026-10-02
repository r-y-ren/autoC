# 2026-09-09 — pasture cadence: why our herd is late (worktree `board-fill`)

Judge: the 3 pinned held-out boards (episodes 106401414, 106773901, 106793159),
our seat, theta `flow135_g350_gpfwdfv_gb028`. Engine replays read-only at
`scratchpad/alloc_review/rep` (`<seed>_<seat>.json`, both seat assignments =
180 hour-0 states, of which 90 are distinct: `_0` and `_1` are the same
deterministic game mirrored, identical rewards).

Instrument: `scratch/pastprobe.py` replays `plan.build_day` over each recorded
hour-0 observation — **no engine run**. Validation: the planner's `a_buy`
reproduces the recorded `BUY_ANIMAL` orders on **90 of 90** our-seat day
states, exactly. Census: `scratchpad/pastcad/census.py` → `days.csv`,
`buys.csv`.

## Status
- [x] Q1 herd / cash / hands / purchase events, both seats, d0-12
- [x] Q2 bucket attribution for our d1-10
- [x] Q3 two-purse value of their earlier animals
- [x] Q4 lever `ANIMAL_RESTOCK_ON`, built, shipping OFF

## Q1 — the herd curves (animals owned = placed + shed stock)

| day | 106401414 o/t | 106773901 o/t | 106793159 o/t |
|---|---|---|---|
| 1 | **6**/4 | **6**/4 | **6**/4 |
| 3 | **6**/5 | 5/5 | **6**/5 |
| 5 | 6/6 | 4/6 | 6/6 |
| 7 | 7/**8** | 6/**8** | 7/**8** |
| 8 | 7/**10** | 6/**10** | 7/**10** |
| 9 | 9/**13** | 6/**13** | 9/**12** |
| 10 | 10/**14** | 6/**14** | 10/**13** |
| 11 | 14/16 | 8/16 | 14/16 |
| 12 | 14/17 | 10/17 | 15/17 |

**The brief's premise is off**: we are not at 4 animals on day 8 against their
12. We *lead* on days 1–4 (6 v 4) and fall behind in one window, **d6→d10**,
where they add 8 animals and we add 3. By d11–12 we are 2–3 behind, not 8.

Cash at hour 0 (ours / theirs): d8 2,403/321, 2,347/434, 2,698/145 — **we are
the richer seat all the way to d10**, and they are the poorer one buying more
animals. Their cash only explodes on d11 (15.6k–17.7k = the melon dump).
Hands (`farm["hands"]` is re-hired every morning; count taken at hour 2):
ours 4–10, theirs 4–11 over d0–10 — level to slightly behind, not the driver.

Purchase events (`buys.csv`, 67 rows). The shape difference is not the money,
it is **the row**:

- **We buy animals only in the day's BUY row at hour 2.** Every one of our 21
  `BUY_ANIMAL` orders across the three games is at hour 2.
- **They buy all day**: hours 2, 4, 7, 9, 11, 17, 18, 21. Their d2/d3 cows go
  in at hour 17–18 on 113–229 coins of cash, i.e. on the day's *sale* proceeds.

## Q2 — why no animal was bought, our d1-10, on days our herd trails

Rows are the 15 our-seat day-states in d1–10 where our herd is below theirs;
`animals lost` is `sum(w_anim) - sum(a_buy)` on that day.

| bucket | day-states | animals lost |
|---|---|---|
| (c) want > 0, **budget grant ranked seeds above it** | **4** | **14** |
| (a) cash below price | 1 | 2 |
| (b) want zero (brain's `animal_want` = 0) | 1 | 1 |
| (d) BUY row had no slot / shed room | 0 | 0 |
| (e) other | 0 | 0 |
| — bought everything it wanted | 9 | 0 |

Per board: 106401414 c×1; 106773901 a×1 b×1 c×2; 106793159 c×1.

The four (c) days, verbatim from the trace:

| board | d | `animal_want` | bought | purse | spent | on |
|---|---|---|---|---|---|---|
| 106401414 | 7 | 1 goose, 1 cow, 1 sheep | 0 | 568 | 417 | 2 wheat, 1 strawberry, 1 melon |
| 106773901 | 8 | **4 cow, 1 sheep** | 0 | 1,780 | 1,397 | **12 strawberry** (100 ea) |
| 106773901 | 9 | 2 cow, 1 sheep | 0 | 415 | 400 | 5 wheat, 2 strawberry, 1 melon |
| 106793159 | 7 | 1 cow, 2 sheep | 0 | 580 | 580 | 1 wheat, 3 strawberry, 1 melon |

So on the decisive days the purse **was** large enough for the cheapest wanted
animal (568 ≥ 300; 1,780 ≥ 400; 580 ≥ 400) and `budget.grant` bought seed with
it. The animal is not deferred by a rule — the crew ramp is inert here
(`a_keep == DEFER_ONE == 256` on every one of the 30 day-states, because
`crew_now >= crew_target` throughout) and `acquire_ok` is true on all three
kinds every day. It simply loses the value-per-coin race to strawberry.

Secondary, structural: `sfree` (free standing structures) is `[0,0,0]` on 27 of
30 states, so **every animal we buy needs a build**, and the build takes a free
tile ahead of every planting (`n_build`, `plan.py:5576-5580`). Their d7 jump is
6→13 pastures in one day.



## Q3 — what their earlier animals are worth, two purses apart

Per-animal-day production and realised prices from the same replays
(`scratchpad/carecov/animal_days.csv`, quotes from `carecov/px.py`).

| window | animal-days o/t | our product value | theirs | delta |
|---|---|---|---|---|
| d0–11 | 264 / 310 | 34,063 | 39,892 | +1,943/game |
| d0–14 | 387 / 457 | 46,712 | 66,289 | **+6,526/game** |
| d0–28 | 958 / 1,101 | 118,910 | 148,837 | **+9,976/game** |

Net of what the extra animals cost them: feed **−2,471/game** (963 wheat fed
against our 761, at the 36.7 mean quote) and purchase price **−1,133/game**
(51 animals bought against our 44, 21,900 against 18,500 coins). So the
opponent's herd advantage is worth **+6,372/game net**, not +12k. **+12k is
about 1.9× too high**; +6.4k is the right order.

And it is **not a day-8 timing item**. Herd-days ahead, per game:

| through | theirs ahead | ours ahead |
|---|---|---|
| d11 | 20.0 | 5.0 |
| d14 | 31.0 | 5.0 |
| d19 | 47.7 | 5.0 |
| d29 | 71.7 | 16.3 |

**72 % of the herd-day gap accrues after day 12.** The herd counts *freeze* at
d12 and the gap never closes: d12→d24 ours 14/10/15-16 against their 17/17/17.

Denial vs displacement, two purses:

- **d-theirs** is the +6.4k above, and it is real product in their shed.
- **Denial** is large but shared: our own animal revenue is 39,637/game at the
  realised banded quotes against 54,627/game at the d0–9 quotes, i.e. the
  season price decay costs us **15.0k/game** on animal product alone (WOOL
  208.8 → 128.7 → 72.8). Their 1,101 animal-days are 53 % of the two seats'
  2,059, so roughly half of that decay is theirs to own — but the town's own
  drain curve is in it too and this replay set cannot separate the two.
- **d-ours** on the four (c) days is *not* a loss handed back: we spent those
  coins on strawberry (12 seeds at 100 on 106773901 d8) at a d10–19 quote of
  206.1. The (c) days are `budget.grant` making a defensible value call, and
  the two-purse rule says a lever that simply flips it is displacement. **That
  is why the lever below does not touch them.**

## Q4 — the lever: `ANIMAL_RESTOCK_ON`

Built, shipping OFF: `src/kagg3/core/plan.py:4355-4404` (doc) and `:4830-4838`
(**9 lines of code**); tests `tests/test_animal_restock.py` (10 tests, all pass,
OFF pinned on `test_route_early`'s `PIN_SEEDS` digests).

Claim, straight off the trace: `macro.animal_want` is `[0,0,0]` on **45 of the
90** day-states, and on **33** of the 90 a COOP or a PASTURE we already built is
standing **empty**. On 106773901 one free coop and one free pasture stand idle
from **d14 to d28** while the purse runs 2,258 → 84,088 and the day's whole
spend is 30–930 coins. We do not refuse that goose on price or on land; the
flow model never prices it at all.

```python
w_anim = xp.where(acquire_ok, xp.maximum(a_want - a_have, 0), 0)
if ANIMAL_RESTOCK_ON:               # [SWITCH]
    r_fs, _ = _place_split(xp, xp.full(spec.N_ANIMALS, ANIMAL_RESTOCK_MAX, i32),
                           xp.zeros((), i32), sfree)
    r_fs = xp.where(view.day >= ANIMAL_RESTOCK_FROM_DAY, r_fs, 0).astype(i32)
    w_anim = xp.where(acquire_ok,
                      xp.maximum(w_anim, xp.maximum(r_fs - a_have, 0)),
                      w_anim).astype(i32)
```

`n_free = 0` in the `_place_split` is the whole safety argument: only structures
that already **stand** may be asked for, jointly clipped across cow and sheep by
the very split the acquisition uses. Neither recorded failure mode can fire:

- **It cannot spend the ramp cash.** `ANIMAL_RESTOCK_FROM_DAY = 12` keeps it off
  the ramp; `acquire_ok` still refuses an animal that cannot pay before
  `VAL.pay_day()`; `grant` still prices it against every seed.
- **It cannot PASS-starve the crew** — measured, not argued (below).
- **It takes no tile**: `b_want` is still clipped to `macro.animal_want`, and
  `seed_cap` comes from `_seed_room`, which this is outside of.

### Planner A/B over the 180 pinned states (`scratch/pastprobe.py`)

OFF path: **0 of 180** states differ from the pre-switch planner on
`a_buy / n_build / seed_buy / plant_eff / spend / purse_left / w_anim / n_buy /
buy_land / shortfall`.

| | OFF | ON | delta |
|---|---|---|---|
| animals wanted (`w_anim`) | 166 | 204 | +38 |
| **animals bought (`a_buy`)** | 88 | **122** | **+34** |
| structures built (`n_build`) | 86 | 86 | **0** |
| seeds bought | 1,029 | 1,029 | **0** |
| tiles planted (`plant_eff`) | 1,039 | 1,039 | **0** |
| coins spent | 106,719 | 118,519 | +11,800 |

18 of 180 states move, all on 106773901, all d14–d22, all against purses of
2,258–49,013 with an OFF spend of 30–932.

Verbs, all 24 turns rendered at each state's real crew size (1,540 hand-days):

| verb | OFF | ON | delta |
|---|---|---|---|
| **PASS** | 8,923 | **8,871** | **−52** |
| PLACE | 88 | 122 | +34 |
| PICKUP | 1,681 | 1,713 | +32 |
| PLANT | 1,027 | 1,025 | −2 |
| WATER | 5,142 | 5,130 | −12 |
| CARE | 1,415 | 1,411 | −4 |
| FEED | 1,525 | 1,523 | −2 |

**PASS goes down, not up** — the restocked animals absorb idle turns; the crew
levers' failure mode is the opposite sign. Total displaced work is ~20 tasks
against 34 placements.

### NOT VERIFIED

- **No paired engine run** (the brief reserves engine reads). The A/B is static:
  each state is frozen, so the same standing structure is re-stocked on nine
  consecutive traced days. In a live game it is filled **once**, on d14, and
  `sfree` then drops to 0 — so the real per-game effect is ~2 animals bought at
  700 coins on d14, filling structures that would otherwise sit empty 15 days
  ≈ **+30 animal-days**, against the measured 47.7-animal-day/game gap.
- The switch fires only on 106773901 of the three boards; on the other two
  `sfree` is 0 from d12 on, so it is a no-op there. Wider coverage unmeasured.
- The denial/displacement split of the 15.0k price decay cannot be separated
  from the town's own drain curve in these replays.
- `ANIMAL_RESTOCK_FROM_DAY = 12` and `MAX = 1` are the traced values, not swept.
