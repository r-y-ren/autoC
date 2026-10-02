# REACTIVITY — what exists, why ES never found it, and the minimal build (2026-09-17 09:20Z)

USER box. Archive + code study plus one CPU decode probe on the shipped theta
(`submission/theta.npy` md5 41b87adc). No engine run, no training, no `src/` change.

## 1. INVENTORY — every rival-dependent input and what it is worth

| rival input | where it enters | which decision consumes it | measured worth |
|---|---|---|---|
| `opp_money` | `core/brain.py:580,587-588` (glob feat, and `money-opp_money`) | shared encoder → **every** Macro int | probe A: opp_money 0→60k at d10 moves `plant_target` 14→32 tiles, `hire_bias` −225→−338, `crew_target` 8→7, own board fixed. Never judged. |
| `opp_kind`/`opp_occ` producing counts | `brain.py:548,560,568-605`; drain `brain.py:239` | crop mix `w`, `absorb` gate `brain.py:1156` | probe E: rival's crop identity at 12 tiles moves plant **count** 16→23 but never the **mix** (crop 3 every time); it only cuts that product's `hold` (melon 71→1) |
| `opp_t_day`/`opp_t_yield` | `production_forecast` / `forward_value` `brain.py:443-530` (opp ready/+1d/+3d/+7d, opp units·coins ×3) | encoder + `fv` head | probe C: rival **ripe units** 0→12 move **0 of 53** Macro ints; only `press[MELON]` ±7 |
| `view.opp_commit` (tiles per product) | `plan.opp_commitment` `core/plan.py:1962` | `OPP_MIX_ON` **OFF** `plan.py:1938`; `OPP_SUPPLY_ON` **OFF** `plan.py:1873` | OPP_SUPPLY judged: 192 boards **−2,972 t −3.80**, theirs +1,131 (`plan.py:1854-1862`). OPP_MIX never judged on the engine. |
| `view.opp_ripe` (ripe units per product) | `plan.opp_ripe_yield` `plan.py:1983` | `SELL_SLOT_PRIORITY` batch term `plan.py:4492-4503` | **SHIPPED.** +459 t +7.31 POOLED180, and the only lever on record where **ours +244 / theirs −215** (`plan.py:4484-4494`) |
| rival **measured** sale rate | `agent/tell.py`, identity exact P 1.000 / R 0.976 (`2026-09-16-rivaltell.md:63,66`) | `RIVAL_TELL_ON` **OFF** `plan.py:4539` | BAND180 **−18.5 t −4.26**; 81.4 % of dawns gate nothing, 100 % of gated values sit on the MIN=8 floor (`2026-09-16-rivaltell-arm.md:16-18,34-36`) |
| market momentum `prev_mkt_inv` | `brain.market_momentum` `brain.py:128` → `mh`/`ms` genes | encoder | trained genes moved the macro on 15/120 dawns and **0 of 6 plan arrays** (`2026-09-16-momentum-review.md:18`); family CLOSED, H/J −278…−926 (:32-43) |
| — **nothing** — | `core/ops.py:126` `SELL_TURNS = (3, 10, 18)`, `LOT4_TURN = 17` `plan.py:845` | the day's sell hours | fixed on every board, every day, against every rival |

Observation is **not** the gap: the package feeds the whole rival farm to `decide`
(`scripts/package_submission.py:127-141`), the sim does the same (`sim/rollout.py:145-155`), and
swapping the rival board moves 7-9 of 14 Macro fields. The gap is that the response was never
*priced*, and the two fields carrying contention are the two the decode is nearly blind to.

## 2. WHY ES DID NOT FIND IT — ranked by evidence

1. **(d) The reachable action set is quantity and mix, and every quantity direction gifts.**
   ESJUDGE6 charged the rival's coin at 1.0 (`--abs-weight 0.0`) and the walk still decayed: pooled
   engine class **ours +1,730 / theirs +4,070**, margin −2,330 (`2026-09-17-esjudge6.md:25-29`) —
   ratio **2.35** — and MELONGIFT decomposes the transfer as **PRICE 93 % / QTY 7 %**
   (`2026-09-17-melongift.md:20-21`). More output = more gift, less = fewer coins; no reachable
   direction moves volume off their row. The three levers that *did* pass §115b are all **timing or
   order** — FERT_TIMING +2,845 t 20.8, LOT4@17, SLOTPRIO +459 t 7.31 — SLOTPRIO alone lowers their
   purse. *Falsifier:* a quantity-only arm with a gift ratio < 1.0.
2. **(c) The 41-int interface is quantised and sell-timing is not in it.** `SELL_TURNS` is a module
   constant (`ops.py:126`); of the 10 constants promoted to genes not one is sell-timing or
   rival-facing (`plan.py:7476-7487`); GENEJUDGE found **46 of 66** switches are class-C program
   shape, +188 t +1.23 REJECT (`2026-09-16-genejudge.md:14,69`); the full mask cliffs between σ
   0.001 and 0.003 (`S/esblk/launch_remote.sh:10-11`). *Falsifier:* expose one signed per-product
   row offset (+65 genes, `2026-09-11-codex-blind-genes.md:39-41`); measure its slope at σ.
3. **(b) One-class training seat.** flow221-226 face 52-56 pinned **engine** tapes at equal weight
   with the named archetypes zeroed (`S/esft2/launch_remote.sh:46-61,73-79`) and self-play cut to
   2 % (`--arch-frac 0.9`, `2026-09-17-esfix.md:46-50`); the top 10 is **one class**, 26/30 boards
   ≥120 FERTILIZE ops (`2026-09-16-topleg.md:15-17`). The condition barely varies, so a
   rival-conditioned coordinate earns what a constant earns. *Falsifier:* the same arm on a 3-class
   seat (engine / V45 / ranch) — a gene that pays only under mixed rivals.
4. **(a) The fitness never paid for relative gain — FALSIFIED as the primary cause.** ESSEAT priced
   `--abs-weight 0.6` at **28 %** of the judge's statistic and 1.0 at −0.174, a *bonus* for their
   coin (`2026-09-17-esseat.md:31-36`); ESFIX found `--margin-scale 3000` saturated into the win
   bit (`2026-09-17-esfix.md:26-31`). Both fixed; the fix bought **magnitude only** (−18,661 t −11.8
   → −534…−878, same sign, `2026-09-17-esjudge4.md:44`) and at 100 % the decay got *worse*.
   ESJUDGE6's rows exclude the rest — **sim-vs-engine mismatch** (its seedmem sim read on the
   *training* boards fell too, −2,224 t −3.59, theirs +2,659, `:39-40`), **memorisation** (fresh
   seeds track train, −2,543 / −2,523, ibid.), **free-rider tapes** (the tape seat is simulated,
   not credited, `es/tape_actions.py:11-19`) — leaving (d): a real gradient (SNR 0.32/gen,
   straightness 0.714, `2026-09-17-esseat.md:44-46`) on a gifting ridge.

## 3. WHAT A REACTIVE DECISION NEEDS

- **Observation** — present and free: `opp_commit` and `opp_ripe` at dawn plus the measured sale
  rate one turn behind (`agent/tell.py`, P 1.000); day 5 is the earliest their plate is legible.
- **Decision point** — *not* a dawn quantity (that is the gifting axis, §2d) but the **within-day
  row**: which turn a lot stands on, which slots it takes, and whether a product's units go before
  or after their dump. `SELL_TURNS` / `LOT4_TURN` are the handles.
- **Rival variation fieldable today** — **891** pinned tape packages (`artifacts/panel_opp_town`,
  engine file-agents) + 737 sim action tapes; 12 hand archetypes and sampled draws
  (`es/archetypes.py:1145`); kagg2; the V45 clone (`S/v45leg/synth45.py`); self-play. Only the
  first is in the seat today, and only as one class.
- **Fitness equal to the judge** — ESSEAT's flags-only design: `--abs-weight 0.0` + a real gate of
  22 held-out boards (`2026-09-17-esseat.md:38-41,60-65`); §115b stays POOLED180 ≥ +450, t ≥ +3
  (`2026-09-17-judgekit.md:25-26`).

## 4. THE MINIMAL BUILDS, cheapest first

| # | build | cost | ceiling estimate | falsifier |
|---|---|---|---|---|
| ii | **Expose the sell row as macro ints**: two signed per-product lot offsets + one turn offset per lot, decoded like `forward_days` (`brain.py:1282`) | ~70 genes, one decode block, no new observation | SLOTPRIO — a pure permutation of the same row — was worth **+459 t 7.31** with theirs −215 (`plan.py:4484-4494`); a *turn* choice on top of a slot choice is the same family and LOT4@17 already paid | a decoded slope of 0 at the training σ (the 2026-09-09 gene-slope rule), or a paired engine leg in which both purses rise |
| iv | **Hand-written best response to the engine archetype on the losing boards**, conditional on their day-0 melon plate (visible at step 0) | one `plan` branch, no training | low: MELONRACE prices the day-10 row at ≤ +5,026 pair coins against a −16,224 bill; best case **−4,306** (`2026-09-17-melonrace.md:10-12`). The rent is not contestable by plate | already fired — treat as CLOSED unless the branch is about the *row*, not the plate |
| i | **K-plan selector at one switch day** from a rival classifier | medium; **PLANSELECT box is measuring the oracle ceiling offline — do not duplicate** | its 09-12 read: frozen gate **−130 t −1.18**, hindsight oracle **+188** (`2026-09-12-planselect-all30-result.md:11-16`) — the choice is real but was not predictable from the permitted observations; the pending box re-prices it with the rival fields | oracle ≤ +450/board, or the classifier's held-out AUC ≤ 0.62 (the 09-10 ceiling, `2026-09-10-livec63-loss-anatomy.md:63-64`) |
| iii | **Mixed live-opponent training seat** (3 classes + public-notebook agents as reactive rungs) | highest: new rung plumbing, GPU time, and every arm re-judged | unpriced. It is the only build that makes a rival-conditioned coordinate *earn* more than a constant | a gene that decodes identically under all three classes after 30 generations |

## 5. VERDICT

What is missing is neither the rival's data nor network capacity — the engine hands us the whole
opposing farm every step, the package passes it to the policy, and the policy visibly moves when
that farm changes. What is missing is a **decision worth conditioning**. Everything theta can
choose today is a quantity: tiles, crops, hands, what a unit is worth kept. In a shared pot each of
those turned up raises the rival's revenue faster than ours (2.35×, 93 % of it through price) and
each turned down costs us coins directly, so the search sits on a ridge and the best it can do is
stand still — exactly the "level on coins, 25 % of boards" reading against the top-10 class. The
one thing that ever took coins *off* them was a free permutation of a sell row that moved no units.
The hour and order of our sales — the only levers that shift revenue between purses without
shifting volume — are module constants no gene reaches and no rival field touches.

**Next box: SELLGENE** — expose `SELL_TURNS`/lot slots as decoded Macro ints conditioned on
`opp_ripe`/`opp_commit`; verify the decode slope at the training σ before any launch, then judge
one paired engine leg on the increment. Build (ii); (iii) only if (ii) decodes.
