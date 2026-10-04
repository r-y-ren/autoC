# CODEX-DEFECTS: four decoder defects audited on candidate B (2026-09-11)

Independent code review flagged four defects in the kagg3 policy decoder. Every
cite below is the **arms-next worktree**
(`/mnt/e/_work/kaggriculture3/.claude/worktrees/arms-next`), which is the tree the
arms and the judge run; nothing under any `src/` was modified.

**Measurement** — candidate B (`artifacts/kagg2_games/thetas/flow193_g100_hr.npy`,
6,789 genes) replayed day by day on the first **10 frozen TOPB2 boards**
(`S/simscreen/boards_topb2.json` = 5 pinned-town top-tier tapes x both seats,
`shop_crn` on, hr switches `OPEN_PUMP_ON,TAIL_FILL_ON,BANK_BEFORE_LOT_ON,HIRE_ROW_ON`),
re-deriving each day's Macro in **numpy** from the very state the jitted rollout is
about to plan from, then running `plan.build_day` on it. 300 board-days, 600
`_largest_remainder` calls. Driver: the scratch replay (staged output
`S/defects/breplay.pkl`, `S/defects/breplay2.pkl`, logs `S/defects/replay10*.log`).
`S/wall/mk_pin.py`'s tables are the WALL's hand-written tape pins, not B's decode,
so they could not be reused; this replay is B's own per-day Macro.
Caveat: 10 boards = 5 tapes in both seats, so the day-counts below pair up
(2 boards per tape) -- read them as ~5 independent trajectories.

---

## 1. `_largest_remainder` tie-break is decided by crop index — **VERIFIED, rank 1**

`brain.py:831-851`, key line **`brain.py:850`**:

    key = -(frac * (2 * n) + (n - 1 - xp.arange(n, dtype=frac.dtype)) / n)

The fraction term spans `frac * 2n`, the index term `(n-1)/n = 0.8` for n=5. One
index step (0.2) therefore outranks any fraction gap below `1/(2n^2) = 0.02`, and
the full span outranks any gap below 0.08. Reproduced in arms-next:
`_largest_remainder(np, [.19,.20,.20,.20,.21], total=1, n=5)` -> `[1,0,0,0,0]`
(the tile goes to WHEAT, the crop with the *smallest* weight); `total=19` ->
`[3,4,4,4,4]`. Docstring says "ties going to the lower index" — the code applies
that rule to near-ties as well as exact ties.

**Measured on B (300 board-days):**

| call | calls | with a leftover tile | index-decided | tiles moved by the fix |
|---|---|---|---|---|
| `plant_target` (n=5, `brain.py:1026`) | 300 | 260 | **14 (4.7 % of board-days, 5.4 % of live calls)** | 14 (exactly 1 per changed day) |
| `animal_want` (n=3, `brain.py:946`) | 300 | 80 | **4 (1.3 %)** | 4 (1 per changed day) |

* **18 / 300 board-days = 6.0 %** have at least one tile placed by crop index
  rather than by weight; 14 of the 18 fall on **d3-d15**, the board-building window
  (days 3,4,5,7,8,14,15 for plants; 9,11 for animals — each on 2 paired boards).
* Direction is one-sided: under the fix **WHEAT loses all 14 tiles**
  (STRAWBERRY +8, MELON +4, CARROT +2); for animals SHEEP +4 (COW -2, GOOSE -2).
  Index 0 = WHEAT is the systematic beneficiary, which is exactly the bias the
  key builds in.
* Example (board 0, d5): fracs `[.3584, .2421, .0392, .3606, .0001]`, total 19 ->
  `[8,0,0,11,0]`; STRAWBERRY's fraction is the larger one and still loses the
  tile. Fixed: `[7,0,0,12,0]`.

**Judgement:** a real defect and the cheapest of the four to test — one tile a
season on 6 % of B's day-decisions, always taken from the crop the weights ranked
below wheat, in the days that set the board for the rest of the game. Patch staged
(`S/defects/fix_tiebreak.patch`, index term scaled 1e-6 so it breaks exact ties
only); paired engine legs staged in `S/defects/engine.sh` (NOT run).
Caveat before spending legs: B was trained *with* this key, so the fix moves B off
its own optimum (cf. ISEARCH §76, B is a strict local optimum at integer radius
1-2) — the honest test is the paired leg, and a re-train is the real fix.

## 2. `CREW_TARGET_PUSH = 400` cannot buy the top of the fib ladder — **VERIFIED (narrower than claimed), rank 2**

`plan.py:3157` (`CREW_TARGET_PUSH = 400`), used at `plan.py:6096-6099`:

    crew_push = (CREW_TARGET_PUSH * xp.minimum(xp.asarray(h, i32), macro.crew_target))
    gain = (_cum_take(...) - bills[h] + macro.hire_bias * h + crew_push)

with `HIRE_BILLS = concatenate([[0], cumsum(spec.HIRE_COST)])` (`plan.py:3570`) and
`spec.HIRE_COST[n] = fib(n)` (`spec.py:257-258`): the marginal hand costs
1,1,2,3,5,8,13,21,34,55,89,144,**233 (13th), 377 (14th), 610 (15th), 987 (16th)**.
So 400 covers every hand *through the 14th* and nothing above it; the reviewer's
"~987" is the 16th hand only. Affordability (`plan.py:6107`) also gates on
`bills[h] + cash_reserve(xp, h, day) <= view.money`.

**Measured on B** (`n_hire` = the enumeration's own intent, recovered by
instrumenting `plan.cash_reserve`'s call order; `hires` = the HIRE market row):

* `crew_target` is non-zero on **228/300** board-days (mean 8.1, max 13); the ramp
  switches on at d7-d8 and tops out at 12-13 from d13.
* **`crew_target > n_hire` on 46/300 = 15.3 % of board-days**, mean shortfall
  **1.09 hands**, mean target 12.7 against 11.6 taken — i.e. the refusals sit
  exactly on the 13th-15th hand, where the fib marginal (233/377/610) meets the
  flat 400 and the cash reserve. All refusals fall on **d11-d20**; cash at
  refusal averages 18.8k (min 1.4k), so it is not purely a purse limit.
* `crew_target == n_hire` on 132/300 (44 %) — the ramp *does* land the argmax on
  the target on the days the fib price is under 400, so the gene is not inert.
* Separately, `HIRE_ROW_ON` clamps the row below the intent on **150/300 = 50 %**
  of board-days (mean 1.43 hands): half the days B enumerates hands that carry no
  route at all.

**Judgement:** a real ceiling, but on 15 % of days and 1 hand deep, and it argues
*against* itself: 50 % of days already buy intent the route cannot load, and
LABOUR-DOES-NOT-COMPOUND (2026-09-11) killed the last "more hands" lever. Worth an
engine test only as "size the push off `HIRE_COST[h]` instead of a constant"
(a switch, not a retune of 400), and only after claim 1.

## 3. Terminal liquidation / forced overflow discard the learned `hold` — **VERIFIED, but it is the LAW, rank 3 (no test)**

* `plan.py:6597-6599`: `hold = _sell_hold(xp, price_table, where(terminal, SELL.LIQUIDATE, macro.hold), terminal)`
  — on the terminal day the whole decoded `hold` vector is replaced by
  `SELL.LIQUIDATE = -spec.COIN_CAP` (`sell.py:48`, `sell.py:130-132`).
  `terminal = day > O.LAST_SHED_DAY` (`plan.py:5924`, `ops.py:349` = 28), i.e. **day 29 only**.
* `plan.py:5220-5222`: the same substitution in the purchase-side projection.
* `plan.py:6616-6689`: shed-overflow forced sale — `deficit` units are sold
  "on top of the gated sale, cheapest marginal unit first", ranked by projected
  marginal quote with `# ties: lower index`, and placed in **bulk** on the
  best-adjusted lot (the comment at 6672-6688 documents the unit-by-unit
  continuation as measured +3.4 % coins at -5.2 % throughput, deliberately not shipped).

**Measured on B, days 25-29 (50 board-days, 4,728 units sold).** Counterfactual:
re-plan each of those days with `macro.hold` forced to `+spec.COIN_CAP`, so only
sales the reservation cannot stop survive — an **upper bound** on the forced share
(with no voluntary sale the projected shed is fuller, so the deficit grows):

| day | units sold | survive with hold=+CAP | share |
|---|---|---|---|
| 25 | 706 | 490 | 69.4 % |
| 26 | 610 | 472 | 77.4 % |
| 27 | 762 | 544 | 71.4 % |
| 28 | 732 | 604 | 82.5 % |
| 29 | 1,918 | 1,918 | 100 % (terminal, `hold` replaced by LIQUIDATE) |
| **25-29** | **4,728** | **4,028** | **≤ 85.2 %** |

B's decoded `hold` on those days is tiny anyway (mean 9 coins, max 58), so the
gene is not saying much that the law overrides.

**Judgement:** verified as described but **not a defect**: day-29 stock is worth
exactly zero (LAW 0.4) and the overflow sale is the shed cap (LAW 0.9) — a
reservation there would burn units, not save them. The only arguable coin is the
bulk placement, already priced at +3.4 % of the forced lot against -5.2 %
throughput. No engine test.

## 4. `PolicyObs.t_yield` unused, opponent ages absent, no hour/history — **MOSTLY REFUTED, rank 4 (no test)**

* `features()` (`brain.py:521-596`) reads `mkt_inv, price, kind, occ, opp_kind,
  opp_occ, shed, seeds, shops, money, opp_money, day, nquad, opp_nquad` and
  **never** `t_day`/`t_yield`/`opp_t_day`/`opp_t_yield` — that half of the claim is
  true of `features()` itself.
* But `decide()` (`brain.py:864-870`) does not feed the network from `features()`
  alone: `board_forecasts` (`brain.py:430-442`) reads **our** `t_day`/`t_yield`
  *and* the opponent's (`brain.py:439-441`), and both readings —
  `production_forecast` (`brain.py:492`) and `forward_value` (`brain.py:444`) —
  are passed into `PO.forward`. So crop ages, standing yield and the opponent's
  clock all reach the policy. B's weight blocks for them are live, not zero:
  `fh (8,64)` rms 0.114, `fs (8,2)` rms 0.183, `fv (12,32)` rms 0.124 — 100 %
  non-zero. **Refuted.**
* **Confirmed:** `PolicyObs` (`brain.py:80-122`) carries no hour and no history —
  no previous-day state, no opponent action trace. `rollout.run_day`
  (`rollout.py:210-211`) calls `brain.decide` exactly once per day at hour 0, so
  the Macro is a whole-day plan by construction; everything intraday is the
  planner's. That is a design boundary, not a decoder bug, and it is the same
  boundary the OPP_SUPPLY/OPP_FRONTRUN refusals already probed (§55, §68).

**Judgement:** no defect in the t_yield/opponent-age half. The real observation
gap — nothing about *what the opponent did yesterday* — is the standing open
question, not a fix.

---

## Ranked

1. **Tie-break (claim 1)** — 6.0 % of B's board-days, 1 tile each, all from WHEAT,
   in d3-d15. Patch + legs staged, not run.
2. **CREW_TARGET_PUSH (claim 2)** — binds 15.3 % of board-days, 1.09 hands, at the
   13th-15th hand. Test only as a fib-sized push, and only after 1.
3. **Forced sales (claim 3)** — verified, but the substitution is the law. No test.
4. **Observation (claim 4)** — refuted for t_yield / opponent ages (B's `fh/fs/fv`
   are live); hour/history absent by design. No test.

## Staged, NOT run

* `S/defects/fix_tiebreak.patch` — one line in `brain._largest_remainder`, index
  term scaled `1e-6` (exact ties still go to the lower index). Apply with
  `patch -p3` inside a COPY tree (`/root/wt_defects`), never in arms-next.
* `S/defects/engine.sh` — the four paired judge legs (TOPB2, LIVEC-H30,
  LIVEC-H30B, LIVE62) vs B under the `S/seedroom/engine.sh` convention: one
  `flock -w 1800 /root/kagg3_judge.lock` per runner, never nested, base csvs
  `S/lossflip/flow193_g100_hr_*.csv`. Run as `bash S/defects/engine.sh all`.
