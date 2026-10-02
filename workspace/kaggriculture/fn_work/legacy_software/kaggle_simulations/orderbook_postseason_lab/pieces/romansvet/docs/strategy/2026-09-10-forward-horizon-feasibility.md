# 2026-09-10 — forward-horizon planner: feasibility spike (read-only, no engine runs)

Question: can `plan.py` be made to price hands, animals, the plant cap and the route
against a projected d+1..d+k task set, cheaply enough to be worth 3 engineer-days?

Base tree for every line number: `.claude/worktrees/ship-pair-hr/src/kagg3/core/` (the
shipped lineage — it already carries `_derive(forward=)` and the `g11` gene). The old
`fwd-admit` tree (`_forward_admit`, a 3-tuple) is superseded, ~4 lines offset. Nothing was
run; every measurement quoted is an archive paired-engine result, cited.

## 1. Where each decision is priced against TODAY

The single derivation is `_derive` (plan.py:4869), signature
`(xp, view, macro, price_table, hire_bill, terminal, reserve, rev1=None, forward=None)`.
`forward=k` (plan.py:5007-5024) widens exactly three masks — `bonus_water`,
`want_water`, `harvest_one` — by `age + k`. It is called three times a day:

**A** scan pass, zero bill, plan.py:6000, no horizon. **B** scan pass, *projected*,
plan.py:6024, horizon `fwd_days` (plan.py:6020). **C** the plan pass — the day that is
actually played — plan.py:6142, **no horizon**.

| stage | file:line | exact quantity read | sees horizon? |
|---|---|---|---|
| hire enumeration | plan.py:6028 `n_tasks0 = sum(d_sc.task)`; :6029 `order0 = task_order(d_sc.task, d_sc.tile_value, d_sc.tier)`; :6030 `cum_est0 = cumsum((d_sc.n_ops + EST_MOVES)[order0])`; :6031 `cum_val0`; cap :6108 `n_adm = min(count_le(cum_est0, turns_h), n_tasks0)` | projected task count / op-turn curve / value curve | **YES** (the only one) |
| hire — pickups, BUY row | plan.py:6041 `n_kinds0 = _pickup_kinds(d0)`; :6048 `pre_early0`; :6056 `pack_orders0` | today's `d0` by design (comment :6017-6019) | no |
| animal wants | plan.py:4722 `_wants(...)` ← :5354 `wants_pre`, :5356 `wants_land`; inputs `want_raw = max(macro.plant_target - view.seeds, 0)` (:4743), `n_free`, `sfree`, `a_have` | today's board + a **spatial** projection only (`n_free + n_pros`, :5353-5356) | no (no time axis) |
| plant cap `n_dev` | brain.py:922 `n_dev = _qfloor(dev_frac * n_free)`; :924 `animal_count`; :946 `animal_want`; :947 `plant_total = n_dev - sum(animal_want)`; :1026 `plant_target` | `n_free = n_free_slots(obs, land=land_ok)` (brain.py:915) — today's empty tiles | no |
| admit stage | plan.py:6369 `n_tasks = sum(d.task)`; :6436 `order_v`; :6438 `cum_est`; :6439 `pick_masks`; :6444 `labour = n_units*(turn_budget - max(_pickup_kinds(d), land_lead) - EST_LEAD)`; :6472 `n_admit = min(count_le(cum_est, labour), n_tasks)` | pass-C `d` = today | no |
| route / placement | plan.py:6490 `admitted = d.task & (rank_v < n_admit)`; :6491 `order`; :6516 `_routes(d.chain_op, d.chain_a, d.chain_q, d.n_ops, order, n_admit, pick_masks, ...)`; `_routes` def plan.py:6939, per-unit cut gated on `idx < n_tasks` | pass-C `d` chains | no |
| sell | plan.py:6606 `wheat_reserved = sum(d.want_feed)`; :6607 `avail = view.shed[:N_PRODUCTS]`; :6639 `SELL.allocate(..., avail, hold, macro.press)`; sell.py:138 `take = (sum(lots) < avail) & ...`; provisional copy plan.py:5178 | hour-0 shed, today | no (`proj_eod`, plan.py:6660, projects **stock** one day but only to force overflow sales) |

So exactly one of the six consumes `forward`, and it consumes it only as a *value/turn
curve* — the day that is actually played (pass C) never sees it. That is the mechanism
behind the archive line: the extra hands PASS.

**The widened task set is not executable.** `_derive(forward=k)` emits
`harvest_one = is_plant & (c_ongoing==0) & (age + k >= harvest_age)` (plan.py:5024). The
engine refuses that op: `sim/units.py:185` `h_plant = (op==OP_HARVEST) & is_pl & (yld>0)
& (age>=c_first)` — the turn is spent, nothing is harvested. The widened
`want_water` (plan.py:5023) does fire, but `in_window` (units.py:180) is false, so it
adds 0 yield and burns the tile's daily water slot. **Feeding the projected `Prefix`
into pass C is therefore not "risky", it is semantically wrong**: it converts idle hands
into refused ops. Any route-side change has to be a *pull-forward of ops legal today*
(BUILD / PLACE / DIG / plant / fertilize / land pickup), not the widened masks.

## 2. The minimal joint design

**P (projection).** `_horizon(xp, view, macro, k) -> Horizon`, an unrolled `k`-step
roll-forward of tile state (`FWD_DAYS_MAX = 6`, brain.py:721, so the loop is
shape-static and jit-safe), emitting three vectors, none of them ops:
`work[j]` hand-turns tile-demand on day+j; `ready[j][N_PRODUCTS]` units landing by day+j;
`free[j]` tiles that become plantable by day+j. Inputs: `view` (kind/occ/age/water/yield),
`spec` crop clocks, `price_table`. It emits *quantities to size against*, never a `Prefix`.

**Four consumers.** (1) hire scan, plan.py:6020-6031 — replace the widened-`_derive`
curve with `work[1..k]`, discounted, and hard-clamp the intent to hands whose route can
be loaded today (`HIRE_ROW_ON`, plan.py:3523, is already True in this tree). (2) `_wants`,
plan.py:4722 via :5354/:5356 — credit the coop/pasture a `free[j]`/`ready[j]` animal will
need, so the structure is built ahead of the purchase. (3) plant cap — widen `n_free` at
the clip inside `_wants` (plan.py:4743-4760), **not** at brain.py:922: `brain` sees only
`PolicyObs`, so doing it in the decode costs a new obs channel in `policy.py` plus a
fixture migration. (4) route — a *pull-forward tier*: ops legal today whose value lands
within k, added to `d.task` with a discounted `tile_value` so `route_tier` (plan.py:6473)
ranks them below today's real work.

**k = 0 byte-identity — and the trap.** The Python-level guard already exists
(`_static_horizon(fwd_days) != 0`, plan.py:6022), and at `k = 0` the three widened
expressions are their unwidened twins term for term (plan.py:5017-5024, integer
arithmetic). **But `k` is not 0 for the shipped theta**: `macro.forward_days` decodes to
mean 0.9 days with the `FWD_DAYS_MAX` ceiling hit on ~30 % of days for
`flow172_g940/g1000` (2026-09-10-planner-wall-audit.md §1 table). Re-using `g11` for
three new consumers therefore **changes the shipped theta's play**. The joint change
needs its own zero-init gene (`g13`, with a measured decode slope at σ0.02 before launch
— the flow151/flow184 rule) or its own module switch defaulting False. This is the one
requirement the task brief got wrong, and it is not optional.

**Size.** plan.py +180-260 lines (this file's comment density is ~3:1; `_horizon` is
~60 lines of code), brain.py +0 (deliberately), policy.py +12 if the gene route is
taken, tests +150-200 (byte-identity on the 2,400-obs fixture, `k=0` decode equality,
a slope check). Engineer-hours: projection 6-8, hire consumer 1, wants/plant cap 3-4,
route pull-forward tier 8-12, tests + gene slope 6-8 → **24-33 h ≈ 3-4 engineer-days**,
before any judge wallclock. A sixth `_derive`-class pass per planned day is also an ES
throughput cost that has not been measured.

**Riskiest piece: yes, route placement** — for the reason in §1, not for its size. It
phases cleanly: **Phase 1** = P + consumers 1-3, no route change, byte-identical at gene 0
and judgeable alone (~14-18 h). **Phase 2** = the pull-forward tier.

## 3. Acceptance test

Reproduce the diagnostic first, on the arm that produced the 94/26 numbers
(`S/_recovered/forced/run.sh`, `fwdadmit/run.sh` — the CSVs were lost with /tmp):
band6 = the six `artifacts/panel_opp/opponent_tape_{105443859,105442685,105441843,105441481,105592028,105400600}/main.py`
**in that order** (order is load-bearing under `--seed-per-opponent`), theta
`artifacts/kagg2_games/thetas/flow135_g350.npy`, `--games 6 --seed-base 777001
--seed-per-opponent` = 72 rows / 36 boards, driver `S/drainpin/on2b.py "<switches>"`,
paired with `S/bank/paired.py <base.csv> <arm.csv>` (seat-grouped `t`; ignore `t_rows`).

Legs, in order, each run twice (base switches / arm switches) and paired:

| leg | runner | boards | what it decides |
|---|---|---|---|
| L0 forced-opening | band6 as above, `OPEN_PUMP_ON=True[,MELON_OPEN_ON=True][,FWD_JOINT_ON=True]` | 72 rows | does the arm move `MELON_OPEN` 26.4 % toward base 94.4 %? |
| L1 identity | any leg, gene 0 / switch OFF | — | 0-coin, 100 % `=` rows |
| L2 target band | `S/livec/run.sh <name> <wt> <theta>` | 72 tapes / 144 games | the promotion metric |
| L3 held-out top tier | `S/topb2/run.sh <name> <wt> <theta>` | 20 tapes / 40 games | veto (retire TOPB, it is read out) |
| L4 live | `S/live62/run.sh <name> <wt> <theta>` | 62 boards / 124 games, LIVE55 rule via `S/live55/flips.py` | veto |

Pass bar, **win-rate first, coins second**:
* L1 must be exact. Any non-`=` row kills the arm.
* L0 gate: forced win rate **≥ 60 %** (from 26.4 %) *and* base arm not worse than
  −2 win points. Below 60 % the "planner cannot express the ramp" hypothesis is not
  what is costing the 68 points, and the build stops here.
* L2 promotion: **+5 win points or more on LIVE-C 72** with paired `d margin > 0`;
  a +5-point move with negative margin is a promotion candidate, the reverse is not.
* L3/L4 veto: no arm promotes with a TOPB2 or LIVE55 drop of more than 2 win points,
  or with `W/L` worse than +2/−4.

## 4. Verdict — **NO. Do not build it.**

Feasible in 3 engineer-days only as Phase 1; the ≥30 % chance of ≥+5 LIVE-C win points
is not there. My estimate is **10-15 %**. Reasoning:

1. **The exact joint change has already been measured, and it is the worst result in the
   log.** `JOINT_PLATE` (worktree `joint`, 3839aed) wrote crew, plate, floors and land
   bias as one sizing rule *above* `_derive`: band6 **54.2 → 1.0 %, −41.9k, t −27**, and
   13.0 % at half scale (2026-09-08-how-we-built-the-agent.md:96, build-story:432-437).
   The lesson recorded there is precisely this design's premise, inverted: *"sizing
   numbers must be derived from the task list after `_derive`, never written above it"*
   — and a d+1..d+k projection is by construction written above it.
2. **The hands are not the money.** `FORWARD_ADMIT_ON` alone: 94.4 → 65.3 %, −9,224,
   t −6.7, with **d-ours −13,157** (2026-09-09-verdicts.txt:919) — the loss is our own
   purse, not a handed-back edge. Independently, `HIRE_ROW_ON` (plan.py:3523) deletes all
   17.06 idle hand-days a game and moved 768 paired games by −378, t −0.75:
   idle hands are nearly free, so removing the PASSes cannot be worth points either.
3. **Even a perfectly expressed ramp loses.** With the route capacity solved
   (`MIDDAY_PLACE_V2_ON`, 66-72 of 72 units into the d10 pot at avg 174), `MELON_OPEN`
   still loses: band −18,561 t −11.3, pinned judge 1.9 % at 12 tiles
   (2026-09-10-melon-route-capacity.md §1). The 12-tile plate displaces the animal line
   (COW 3→1) for a +31k price gift by d27. `FORWARD_ADMIT` on top of it read 15.3 %,
   −27,397, **d-theirs +6,806 = denial handed back** (verdicts:919).

Top 3 ways it fails, including the two the brief names:
* **(a) Extra hands PASS again.** Phase 1 cannot fix it — pass C is untouched by design —
  so Phase 1's most likely reading is FORWARD_ADMIT's: a bigger bill, `d-ours` down, win
  rate down. Phase 2 is the only cure and it is the piece that must emit ops.
* **(b) The melon opening hands denial back.** Any horizon long enough to reach
  `CROP_WINDOW_START[MELON]=6` re-prices the board toward the melon plate, and the plate
  is a *swap* by construction (`_melon_open` preserves `sum(plant_target)`,
  2026-09-11-additive-melon.md §3): our animal/wheat denial goes, their purse rises. The
  shared pot means our +X is usually their +more.
* **(c) The gene collision.** `g11` is live in the shipped theta (mean 0.9 days, ceiling
  on 30 % of days). A joint consumer on the same gene silently re-plays the champion;
  a new zero-init gene needs its own slope proof and 200+ generations before it decodes
  anything (flow184: 165 coordinates moving, decoded floor 0.0000 on 2,400 obs).

## 5. Cheaper structural alternative — **the pumper-aware hour-0 row**

Not another sizing rule. `OPEN_PUMP` is the one *promoted* structural lever we have
(panel24 64 → 87 %, family B 96 %, +21.7k, the whole measured content of the splice), and
the archive's open item against the target band is: **the top tier already pumps — top10
tapes cost us −4.6k and our own sheep is the one refused.** The quote is `base + sqrt(n)`
(plan.py:1179-1184), the shipped row is `[HIRE×n, BUY_PRODUCT WHEAT 53]` at index 0
(`OPEN_PUMP_SLOT0`), and `OPEN_PUMP_UNITS/KEEP/MIN_MONEY` (53/5/1584, plan.py:1184/1189/
1194) have **never been swept** (2026-09-10-planner-wall-audit.md §2). Against a pumping
opponent this is a two-sided race whose order was already measured order-by-order
(`scratchpadCR`/pumpracer). Build: one row-order switch plus a 3-point sizing sweep,
~0.5-1 engineer-day, zero planner semantics, byte-identical OFF.

Why it targets the same money: the clone's day 0 ends on ~50 coins with 1,960 already
spent (2026-09-11-additive-melon.md §2). Denial at d0 h0 is the only lever that has ever
moved the top tier, and it does not require us to express their ramp at all. *(A melon-
**seed** pump is dead on inspection: `CROP_SEED_COST` is a constant, spec.py:49 — only
`BUY_PRODUCT` quotes move with `sqrt(n)`.)*

**Acceptance test.** Arms: shipped / `SLOT` re-order / `UNITS` ∈ {53, 72, 96} — legs L1
(identity, OFF), then L3 `S/topb2/run.sh` and L2 `S/livec/run.sh` **first** (this lever is
top-tier-specific, so the veto leg is also the read), then L4 `S/live62/run.sh` before any
upload. Pass: ≥ +3 win points on TOPB2 *and* ≥ +3 on LIVE-C 72, no LIVE55 drop > 2 points.
Kill: any arm whose `d-theirs` is positive — that is denial handed back, the same
signature that killed the melon family.

## 6. Dead ends and caveats recorded

* `fv`, the forward-harvest **observation** feature (f2904c5, N_PARAMS 6,405 → 6,789), is
  not a candidate: already trained in the shipped theta — `flow172_g1000.npy[6405:6789]`
  L2 **2.25**, max 0.38 (measured here). The head has been told when the board pays for
  the whole flow172 lineage and the ramp did not appear.
* Trained-gene disagreement: plateau §54 has `g11` decoding 0 every day (narrow rebuild);
  the wall audit has mean 0.9 / ceiling on 30 % of days (`flow172_g940/g1000`). Different
  thetas — do not merge the claims.
* `S/spo/measure.sh` no longer exists (lost with /tmp). The archived copy is
  `S/_recovered/spo/measure.sh` and it is heredoc-escaped, i.e. not runnable as-is; use
  `S/livec|topb2|live62/run.sh` + `S/bank/paired.py` instead.
* `S/livec/run.sh`'s header says "20 pinned tapes"; `S/livec/ids.txt` is **72** — stale
  header, not a stale set. And melon-route-capacity §3's "both seats ~22 hires by d4" is a
  cumulative count on another board and theta than the forced diagnostic's "0 hands d1";
  not a contradiction, but do not quote the two together.
* No engine run was made for this document; every number is an archive paired result.
