# 2026-09-11 — OPEN_PUMP constants against candidate B, and the pumper-aware row

Question, from `2026-09-10-forward-horizon-feasibility.md` §5 and consensus §176: are the
opening pump's constants (`OPEN_PUMP_UNITS/KEEP/MIN_MONEY` = 53/5/1584, plan.py:1184/1189/
1194) mis-set against the seat we actually ship — **candidate B**,
`artifacts/kagg2_games/thetas/flow193_g100_hr.npy` (md5 7fcf3948) with the hr switches — and
does a *pumper-aware* hour-0/hour-1 row buy anything against a top tier that pumps us back?

Everything below is a paired engine measurement on the judge's own legs and the judge's own
base csvs. Nothing was promoted.

## Method (the judge's pipeline, under `pump_` names)

`S/autojudge/watch.sh:legs_for_theta` picks the worktree by theta width (6789 →
`.claude/worktrees/arms-next`) and the switch string
`OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True`, then calls
`S/topb2/run.sh` (20 held-out top-tier pinned tapes × 2 seats = 40 games, seed base 777001,
`--seed-per-opponent`) and `S/livec/run_holdout.sh` (LIVE-C ids 43-72 × 2 seats = 60 games,
seed base 777001 + 1000003·42), and pairs each csv against the B base with
`S/bank/paired.py` on `(seed, opponent, seat)`, seats averaged per board for `t`.

Reproduced here with:

* a **copy** of `arms-next` (`scratchpad/pumptree`, plan.py md5 3098247432e4a18ebdd7f0008f4d0dc0
  = the judge's), so the judge's tree is never touched;
* the **same runners** under `pump_*` names, so no csv can collide with the judge's
  (`S/pump/sweep_b.sh`, driver `S/drainpin/on2b.py`, `WORKERS=6`);
* base csvs `S/lossflip/flow193_g100_hr_topb2.csv` (40 rows) and
  `S/lossflip/flow193_g100_hr_livech.csv` (60 rows) — B's own, the ones the judge's
  `AUTOJUDGE-vsB` line uses;
* constants moved the way the judge moves switches — `on2b.py` `setattr` on `kagg3.core.plan`
  before the first trace — never by editing the tree. **Identity gate:** the same run with
  `OPEN_PUMP_UNITS=53,OPEN_PUMP_KEEP=5,OPEN_PUMP_MIN_MONEY=1584` set explicitly pairs to
  **0 coins, 40/40 identical rows** against the base csv.

## The population: the top tier pumps, but small (static tape scan, no engine)

Decoding the day-0 market rows of every opponent tape in the two sets
(`scratchpad/scan_tapes.py`, `_TAPE[0]` = day 0 hour 0, `_TAPE[1]` = the hour-1 BUY row):

| set | tapes | buy wheat at h0 | typical h0 row | **net** h0 pot draw | net draw ≥ 40 |
|---|---|---|---|---|---|
| TOPB2 | 20 | 16 | BUY 13, SELL 13, BUY 13 (gross buy 26) | +13 (four at 0, two at −33) | **0** |
| LIVEC-H30 | 30 | 30 | same | +5 … +13 | **0** |

Two facts follow, and they are the load-bearing ones in this document:

1. **The tier's pump is a gross-26 / net-13 round trip, not a 53-unit draw.** Our 53 units
   are ~4× theirs, and against a coupled BUY/BUY pair the engine walks *one shared quote*
   (`sim/market.py:686-694`), so their 13 net units sit inside our own ladder.
2. **`OPEN_PUMP_TELL_MIN = 40` can never fire on this population.** The tell computes
   `theirs = MARKET_I0 − inv − OPEN_PUMP_UNITS` (plan.py:1731) = their *net* draw, which is
   at most 13 here. That — not a defect in the patch — is why `OPEN_PUMP_TELL_KEEP0_ON=True`
   was byte-identical on 124 live + 40 TOPB games on 2026-09-10 (consensus §34). The switch
   is live in the judge's path (`agent/runtime.py:42`, and `eval_vs_baselines.py:311-315`
   builds our seat through `runtime.make_agent`); its threshold is simply off by 3×.

## Where the pump's coins actually are (per-opponent split of the paired delta)

`scratchpad/bypump.py` groups each variant's paired delta by the opponent's own hour-0 row
(mean coins/board, both seats averaged):

| variant / set | pumpers (h0 gross ≥ 26) | small draw (0 < gross < 26) | idle at h0 (gross 0) |
|---|---|---|---|
| UNITS 35, TOPB2 | n=6, −15 | n=10, **−1,806** | n=4, −43 |
| UNITS 70, TOPB2 | n=6, −668 | n=10, **+1,513** | n=4, +1 |
| UNITS 35, LIVEC-H30 | n=25, −16 | n=5, +29 | — |
| UNITS 70, LIVEC-H30 | n=25, −219 | n=5, **−658** | — |

Two readings, and they pull against each other:

* **Sizing is irrelevant against a seat that never touches the wheat pot on day 0** (±40 coins
  on the four such TOPB2 tapes, whose hour-0 *and* hour-1 market rows carry no wheat at all).
  There is no denial channel to size: the pump only reaches a seat that buys wheat while our
  ladder is standing, and our 48 units are back in the pot at index 0 of the hour-1 BUY row.
* **The whole TOPB2 movement sits on the ten small-draw tapes, and it does not replicate.**
  The same group on the hold-out set moves the other way at UNITS 70 (+1,513 on 10 TOPB2
  boards, −658 on 5 LIVEC-H30 boards). With |t| ≈ 1 on the set, this is the seed-set lottery
  the archive keeps recording, not a sizing law.

## Results — every row paired against B's own base csv, same boards, same seeds

Base = candidate B as shipped: TOPB2 **32.5 %** (20 boards / 40 games), LIVEC-H30 **63.3 %**
(30 boards / 60 games). "flips" = boards won that the base lost / lost that it won.

| variant | set | boards | win% base→variant | flips +/− | Δmargin/game | t | verdict |
|---|---|---|---|---|---|---|---|
| identity (53/5/1584 set explicitly) | TOPB2 | 20 | 32.5 → 32.5 | 0/0 | **0** | — | **gate passed**, 40/40 rows identical |
| `UNITS` 35 | TOPB2 | 20 | 32.5 → 25.0 | 0/−3 | −916 | −1.96 | negative, at the kill line |
| `UNITS` 35 | LIVEC-H30 | 30 | 63.3 → 63.3 | 0/0 | −9 | −0.05 | level |
| `UNITS` 70 | TOPB2 | 20 | 32.5 → 35.0 | +1/0 | +556 | +1.02 | not significant |
| `UNITS` 70 | LIVEC-H30 | 30 | 63.3 → 63.3 | 0/0 | −292 | −1.27 | not significant, negative |
| `UNITS` 90 | TOPB2 | 20 | 32.5 → 25.0 | 0/−3 | **−1,686** | **−2.01** | **DEAD — kill rule** |
| `UNITS` 90 | LIVEC-H30 | 30 | 63.3 → 63.3 | 0/0 | +75 | +0.31 | level |
| `MIN_MONEY` 1200 | TOPB2 | 20 | 32.5 → 32.5 | 0/0 | **0** | — | **byte-identical no-op** |
| `MIN_MONEY` 2000 | TOPB2 | 20 | 32.5 → 32.5 | 0/0 | **0** | — | **byte-identical no-op** |
| `MIN_MONEY` 2000 | LIVEC-H30 | 30 | 63.3 → 63.3 | 0/0 | **0** | — | **byte-identical no-op** (60/60) |
| `MIN_MONEY` 3001 (control) | TOPB2 | 20 | 32.5 → 32.5 | +2/−2 | −228 | −0.40 | **= `OPEN_PUMP_ON=False` byte-for-byte** |
| `OPEN_PUMP_ON=False` (lever off) | TOPB2 | 20 | 32.5 → 32.5 | +2/−2 | −228 | −0.40 | the whole lever is worth ≈ +228 ± 400 here |
| `OPEN_PUMP_ON=False` (lever off) | LIVEC-H30 | 30 | 63.3 → 63.3 | 0/0 | +20 | +0.06 | the lever is worth **nothing** on the hold-out |
| `TELL_KEEP0` + `TELL_MIN` 5 (hour-1 row) | TOPB2 | 20 | 32.5 → 30.0 | 0/−1 | −569 | −1.54 | fires on 12/20 boards, negative |
| `TELL_KEEP0` + `TELL_MIN` 5 (hour-1 row) | LIVEC-H30 | 30 | 63.3 → 63.3 | 0/0 | +22 | +0.33 | fires on 25/30 boards, level |
| `SLOT0_ON=False` (hour-0 row order) | TOPB2 | 20 | 32.5 → 32.5 | 0/0 | +349 | +0.87 | not significant |
| `SLOT0_ON=False` (hour-0 row order) | LIVEC-H30 | 30 | 63.3 → 63.3 | 0/0 | −293 | −1.27 | not significant |

### The sizing curve is not a curve

−916 (35) → 0 (53) → +556 (70) → −1,686 (90) on TOPB2, with the two ends at |t| ≈ 2 and the
middle at |t| ≈ 1. Nothing is dose-responsive, and the 2026-09-10 sweep on the **hr**
composition read the same shape from the other side (UNITS 40 −236 / 70 +299 on TOPB2, 40
−189 / 70 −278 on LIVEC-C72). The one direction both compositions agree on is that *below* the
default is worse on the top tier and *above* it is worse on the hold-out.

### Why: unrelated day-0 changes land on the same board outcome

Per-row paired deltas, correlated across variants (`n` = rows the variant moves at all):

| set | pair | Pearson r |
|---|---|---|
| LIVEC-H30 | `UNITS 70` vs `SLOT0 OFF` | **1.000** (−292 vs −293, sd 1,291 both) |
| TOPB2 | `UNITS 70` vs `SLOT0 OFF` | 0.676 |
| TOPB2 | `UNITS 35` vs `TELL_MIN 5` | 0.909 |
| TOPB2 | `UNITS 35` vs `UNITS 70` | 0.012 |

Sharper than the correlation: across the 60 hold-out games `UNITS 70` and `SLOT0 OFF` differ
from each other by a mean of **2.2 coins** (max 10) while each differs from the base by a mean
of **900**. Two changes with nothing in common — one resizes the hour-0 order, the other moves
it behind the hires — play out the same season to within a coin, while two sizes of the *same*
order are uncorrelated. That is the shop-draw lottery in the `shop-lottery-2026-09-06` memory:
what a day-0 change does to the season is decided by whether it perturbs a tile at all (which
re-rolls every later shop), not by how much it perturbs it. It is the cleanest demonstration
of that mechanism in the archive, and it is why none of these reads can be tuned on.

## The pumper-aware row (experiment 3) — already closed, and now explained

The brief's third experiment ("detect the opponent's hour-0 draw at hour 1 and resize our own
row so the sheep is not refused") **is a closed experiment**, and it must not be rebuilt:

> `2026-09-09-verdicts.txt:347` — *2026-09-05 22:40Z PUMP-AWARE ROW (worktree `pump-aware`,
> branch `pump-aware-row` 62baf5e, inert): tell fires on 16/20 top10 tapes and re-sequences the
> h1 row (animals first), but **392/392 boards bit-identical to OFF** → with `OPEN_PUMP_SLOT0`
> shipped the row already clears; the 'sheep refused 498 vs 500 / −4.6k' symptom was
> **pre-SLOT0 and is DEAD**. Lever closed, switch left off, not merged.*

So the symptom the brief (and lever-ranking P2) quotes as the motive — *our own second SHEEP
is the one refused, −4.6k on top-10 tapes* — was fixed by `OPEN_PUMP_SLOT0_ON` in 2026-09-04
and has not existed since. What was *not* known is the size of what SLOT0 is worth against B:
turning the order back off is **+349 (t 0.87) on TOPB2 and −293 (t −1.27) on the hold-out**,
i.e. the shipped order is not measurably better than the old one either — and on the hold-out
it is the same lottery draw as `UNITS 70` (r = 1.000 above). P2 can be closed with this.

What *was* worth doing, and is new here, is the calibration of the one hour-1 patch that does
ship in the judge's path. `OPEN_PUMP_TELL_MIN = 40` is mis-set by a factor of three against
this population (net hour-0 draws are 5-13, never ≥ 40), which is the mechanism behind the
2026-09-10 byte-identical no-op. Re-set to 5 the patch really fires — 12/20 TOPB2 boards,
25/30 hold-out boards — and it is **negative on the top tier (−569, t −1.54) and level on the
hold-out (+22)**, concentrated on the ten small-draw tapes (−1,182/board) with the six real
pumpers +72. Keeping none of the five feed units is not a better trade even against a seat
that pumped us; the switch stays OFF, and its threshold is now explained rather than mysterious.

## `MIN_MONEY` is a dead constant, not an unswept one

`OPEN_PUMP_MIN_MONEY` is compared against `view.money` in the **plan pass**
(plan.py:6747-6749 in the repo tree, `_plan_and_stats`), i.e. the day's *opening* purse. On
day 0 that is `spec.STARTING_MONEY = 3000` on every judge board — `eval_vs_baselines.py`
never passes a warm start — so the guard is a constant `3000 >= X`:

* `X` ∈ {1200, 1584, 2000}: identical play. Measured, not argued — 40/40 TOPB2 rows and
  60/60 hold-out rows byte-identical to B at 2000, 40/40 at 1200.
* `X` = 3001: the pump never fires, and the leg reproduces `OPEN_PUMP_ON=False`
  **byte-for-byte** (same csv, −228, t −0.40). That is the positive control: the constant is
  live in this path, and the no-op above is the guard never binding.

There is no third behaviour. `MIN_MONEY` should be struck from the open-lever list
(`2026-09-10-planner-wall-audit.md:67`, lever-ranking P1) rather than scheduled for a sweep.

## Conclusion

1. **The constants are not mis-set against B.** On B's own promotion pair the shipped 53 is
   the best of the four sizes: 35 → −916 (t −1.96) TOPB2, 70 → +556 (t 1.02) TOPB2 but −292
   on the hold-out, 90 → **−1,686, t −2.01 = the brief's kill rule**, hold-out +75. Nothing is
   dose-responsive; the hr sweep of 2026-09-10 read the same non-curve. **Lever-ranking P1 is
   closed, with no promotion.**
2. **`MIN_MONEY` cannot be swept at all** — the day-0 purse is a flat 3,000, so every value
   below it is the same play (proved byte-identical on 100 games) and every value above it is
   just the lever turned off (3001 ≡ `OPEN_PUMP_ON=False`, byte-for-byte).
3. **The lever as a whole is worth ~nothing against the population we are now judged on:**
   `OPEN_PUMP_ON=False` is −228 (t −0.40) on TOPB2 and +20 (t 0.06) on the hold-out. The
   +21.7k / panel24 64→87 % result that promoted it was measured on the class-A / family-B
   population and should no longer be quoted as an edge against the 2100-2900 band tapes.
4. **The pumper-aware row is closed twice over.** The built hour-1 re-sequencing has been
   inert since `OPEN_PUMP_SLOT0` shipped (392/392 boards, 2026-09-05), and SLOT0 itself is
   worth +349 / −293 (|t| < 1.3) against B — so the order is no longer an open question
   either (**P2 closed**). The shipped `TELL_KEEP0` patch was a no-op only because
   `TELL_MIN = 40` is 3× the population's net hour-0 draw; recalibrated to 5 it fires on
   37 of 50 boards and **loses** (−569 TOPB2, +22 hold-out). Leave it OFF.
5. **Health warning for anyone tuning day-0 constants on these legs:** `UNITS 70` and
   `SLOT0 OFF` — two unrelated changes — move all 60 hold-out games with r = **1.000**
   (−292 vs −293). What a day-0 change does to a season is decided by *whether* it perturbs a
   tile, which re-rolls every later shop draw, not by *what* it perturbs. These sets can
   therefore falsify a pump constant (90 did) but can never select one; the next honest step
   in this family is a new mechanism, not a new number.

## Artefacts

* csvs (paired against `S/lossflip/flow193_g100_hr_{topb2,livech}.csv`):
  `S/lossflip/pump_{ident,u35,u70,u90,m1200,m2000,m3001,off,tell5,noslot0}_{topb2,livech}.csv`
* paired lines: `S/pump/sweep_b.out`; runner `S/pump/sweep_b.sh` (the judge's own leg scripts
  under `pump_` names, on a copy of `arms-next`); tape scan `scratchpad/scan_tapes.py`,
  per-opponent split `scratchpad/bypump.py`.
* Nothing in the judge's tree, csv namespace, lock or state was touched; no theta was promoted.
