# Verify F5 — "the discretionary purchase allocator has no cash-retention alternative"

Independent check of finding 5 of `docs/2026-09-10-planner-findings.md` (detail:
`docs/reviews/planner-2026-09-10/REVIEW.md` §6). Read-only: no worktree `src/` was
touched, probes ran in memory, engine budget spent 4 full games / 143 s.

**Code description: PARTLY CONFIRMED** — literally true of `budget.grant` and the
five *seed* lists, too broad for the allocator as a whole (4 of the 10 lists carry
value-vs-cost gates upstream, land is a two-way compare, cash has a structural
floor). **Implication ("compare with retaining cash"): (a) already measured and
dead** in every form the archive has run, with one narrow untested residual (a
strict `values > costs` eligibility) whose modelled ceiling is ~361 coins/game —
below the promotion bar before any displacement.

## 1. What the source actually does

Tree read: `.claude/worktrees/ship-pair/src/kagg3/` (sha256 of `plan.py`
`ac731e50…` = both `dist/submission_flow172_g940_pair.tar.gz` and
`…_g1000_pair.tar.gz`). **Difference from the CURRENT shipped `ship-pair-hr`:
exactly one line**, `plan.py:3523 HIRE_ROW_ON = False → True`; `budget.py` and
`brain.py` are byte-identical and every line number below is the same in both, so
finding 5 transfers unchanged.

- `core/budget.py:164` — `live = (j < wants[:, None]) & (values > 0)`. Eligibility
  is positive value, never value ≥ cost; cost is only the ranking denominator
  (`:165`), and the docstring is explicit that "top-ups then spend what the
  threshold left, one item per round until nothing fits" (`budget.py:8-11`, loop
  `:222-246`). **No "keep the coins" candidate exists.**
- The brakes are quantity and affordability, not profitability:
  `plan.py:5163` `money = max(view.money - hire_bill - reserve, 0)`;
  `plan.py:5387` `purse = money - buy_land*land_gap`; `plan.py:5409`
  `n_buy = BUD.grant(xp, values, costs, wants, purse, room)`.
- `cash_reserve` (`plan.py:3599`) does **not** play the missing role. It is
  `HIRE_BILLS[n_hire+1]` — a structural floor for tomorrow's crew, zero from
  `pay_day()`, unlearned and not a value comparison. A day that hires nobody
  holds back 1 coin.
- `dev_weight` (`brain.py:1069`) scales *route* development value and `press`
  (`plan.py:3427`) is the sell side; neither reaches `_candidates`.
- **But four of the ten lists do gate on cost**, which the finding does not say:
  - fertilizer — `plan.py:5210` `fert_cand = is_plant & (t_fert < day) & (fert_val > fert_bar)`;
  - the three animal lists — `plan.py:5308` `acquire_ok = ub_coins > spec.ANIMAL_COST`
    (an *optimistic* upper bound: today's prices, no labour);
  - wheat feeds are a survival shortfall, not discretionary; land is the explicit
    two-way compare `land_value + land_bias > 0` (`plan.py:5384`).
  The five **seed** lists are the ones with no cost test at all: their want is the
  learned `plant_target` clipped to tiles (`_wants`, `plan.py:4722-4765`).

**"Value 6 for cost 80" — units and horizon.** Value is *gross* coins of projected
sale revenue for every unit the k-th purchase yields by `VAL.pay_day()` (day 28, or
29 under `HORIZON_DROP`), read off that product's own price curve from projected
hour-0 inventory plus the farm's own committed pipeline (`_stream_rev`
`plan.py:4074`, `_pipeline_units` `:4087`, `new_plant_units` `valuation.py:181`),
scaled by the learned `grow_mult` (0–4x, `brain.py:1054`, `plan.py:4823`). It
excludes the seed's own cost, labour, tile displacement, opponent supply and the
opponent's price impact. So "6" is 6 coins of season-gross revenue; "cost 80" is
the melon seed price (`spec.CROP_SEED_COST = [10,20,50,100,80]`).

## 2. Reproduction, and the same states under the trained theta

Both probes reproduce exactly on `ship-pair` (`probe.py` logic re-run in memory):

| probe | result | note |
|---|---|---|
| allocator-only | `grant[L_SEED0+4] = 1`, value 6, cost 80, net −74 | **hand-written arrays** passed straight to `B.grant` — not a state the planner produced |
| full-plan carrot | seed bought 1, value 5, cost 20, 1 plant op | real code path, but on a market pinned to carrot's **1-coin price floor**; purse 999, reserve 1 |

At purse 79 the same item is refused (affordability, not net); with a +500/20
competitor at purse 80 the melon drops out for cash, never for its net.

**Under the trained theta** (`artifacts/kagg2_games/thetas/flow172_g1000.npy`,
md5 of the packaged copy f091deb2 = `dist/submission_flow172_g1000_pair.tar.gz`):

- On the carrot probe state, `brain.decide` returns `plant_target [0,0,0,2,0]`
  (zero carrot) and `grow_mult[CARROT] = 55` = 0.21x, which prices the carrot
  candidate at **1** coin. The trained policy buys 2 strawberry seeds + 1 goose:
  **3 granted units, 0 of them negative-net.** Same board at normal prices:
  4 units, 0 negative-net. *The trained policy does not make either probe purchase.*
- Incidence in real play — 4 instrumented engine games (`flow172_g1000`, tapes
  107233845 / 107244033, both seats, pinned towns, the `games.py` recipe), 120
  day-plans, every granted unit audited against its own cost: **1,215 units
  granted, 14 (1.2 %) with modelled value < cost, on 7 of 120 day-plans**; modelled
  shortfall **1,445 coins / 4 games = 361 a game**; those 14 cost 3,684 of the
  65,998 coins spent. The 14 are 8 herd units (goose day 11 at 174/300, the 3rd and
  4th sheep on day 10 at 423/500 and **120/500**), 4 fertilizer units at 70/71
  (−1 coin each: the labelled flat-quote-vs-curve gap at `plan.py:5210`), and 2
  strawberry seeds at 75/100 — i.e. mostly the lists that *do* have a break-even
  gate, whose optimistic bounds the marginal k-th unit slips through.
- **The purse was nearly exhausted (<20 coins left) on 8 of 120 days**, median
  purse 4,462 against median spend 261: cash is not the binding constraint, the
  wants are. The finding's "when cash is available" framing is right; its implicit
  scale is not.

## 3. What the archive already measured

- **`cash_reserve` scale** (`S/cashreserve/`, `S/glut/verdicts.log` 09:53–10:15Z,
  `docs/strategy/2026-09-10-consensus.md` §4): built as one switch site, default
  byte-identical; 0.5/0.0 → TOPB level (+248 t 0.6 / −46), LIVE62 wins 89.1 → 86.4 %.
  **CLOSED**: "the reserve is a correctly-sized rule, not a wall."
- **Reservation floor** (hold carrot cash days 10-24;
  `docs/strategy/2026-09-08-how-we-built-the-agent.md` §2d): LIVE −66 / −248 / −445
  at 1.25x / 1.5x / 2x, gen-130 −458 / −646, monotone in dose; our purse flat
  (−140…+43), the clone's purse **up** on every leg (+109…+506) — the origin of the
  **two-purse rule**: retained cash is not saved, it stops suppressing the
  opponent's quotes.
- **Fertilizer value bar** (`FERT_VOLUME_ON`, the one live "require value > cost"
  threshold, 384 paired games/mode): best mode +636 t 1.50 vs a +1,500 / t 2 bar,
  `base` −1,103, `FERT_MARGINAL_ON` −1,745 t −3.09. Shelved.
- **Land veto** (the same comparison loosened, not tightened): ZERO arm TOPB
  −16,640 t −9.4, LIVE55 34.5 → 15.5 % −8,148 t −9.3. DEAD both tiers.
- **`GROW_MAX` 6/8**: engine byte-identical on 40 TOPB games although the decode
  moves `grow_mult` on 330/600 obs — the capped candidate is already top-ranked.
- **Plant-mix drain tilt** (`2026-09-09-plateau-review-verdicts.md` §13): 14.3 % /
  14.3 % / 6.0 % and −2,458 / −6,243 / −9,198 at gain 0.5 / 1.0 / 2.0. Dose-responsive
  loss — the shape every purse-restricting lever in this family has followed.

No lever of the form "spend less / hold coins / raise a purchase threshold" has a
positive paired read anywhere in the archive.
## 4. Verdict and the exact residual test

- **Code description: PARTLY.** True and reproducible for `budget.grant` and the
  seed lists; false as stated for fertilizer, animals and land. `cash_reserve`
  is a floor, not the missing alternative; `dev_weight`/`press` are elsewhere.
- **Implication: (a) already measured and dead** in four independent forms, with a
  mechanism (two-purse) that explains the sign. The policy's own learned channel
  for "do not buy this" is `grow_mult` → 0.21x and `plant_target` → 0, which is
  why it declines the probe purchases.
- **Residual, untested in this exact form:** a strict eligibility rule in
  `budget.py:164`, `live = (j < wants) & (values > costs)`. Ceiling at the model's
  own numbers: 361 coins/game, 76 % of it two sheep on one board — against a
  +1,500 / t 2 bar. Low prior, cheap to run.
- **Exact paired test if it is ever run** — one switch `NET_PURCHASE_ON`
  (default OFF ⇒ byte-identical), built in a fresh worktree, then:
  `S/topb2/run.sh netbuy <wt> artifacts/kagg2_games/thetas/flow172_g1000.npy` (held-out
  top tier, 40 games), `S/livec/run.sh netbuy <wt> …` (mid tier, 40 games), and
  `S/live62/run.sh netbuy <wt> …` (124 live boards); compare with
  `S/bank/paired.py S/lossflip/g1000pair_hr_*.csv S/lossflip/netbuy_*.csv`.
  Promote only on ≥ +1,500 / t 2 with the LIVE62 win rate not falling.

## Dead ends and assumptions recorded

- The allocator-only probe proves a *contract* of `B.grant`, not a planner state:
  its value/cost arrays are written by hand. Do not cite it as incidence.
- The carrot probe needs the market pinned to carrot's 1-coin floor to make the
  candidate lose money; at the default table that state grants nothing negative.
- Assumption: `brain.decide` on the probe state was fed a synthesised opponent
  context (opponent board = ours, opp money = ours, no shops), so those decodes are
  indicative; the 4-game audit uses real decodes and is the load-bearing evidence.
- Assumption: 4 games / 120 day-plans (the review's own sample) bounds the
  incidence; it does not price the lever.
