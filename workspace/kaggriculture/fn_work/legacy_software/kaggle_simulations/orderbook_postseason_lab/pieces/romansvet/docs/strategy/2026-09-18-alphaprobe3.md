# ALPHAPROBE3 — select under shop UNCERTAINTY: two thirds of the search gain was shop hindsight

2026-09-18, branch `alphafarm`. `S/alphafarm/search_probe.py --robust-select S`, rows `run24rb_a/_b/_all`,
`rb_exact_exact.json`. With [[alphaprobe2]], [[mpcfeas]], [[planselect]], [[shop-lottery]].

## 1. The falsifier
[[alphaprobe2]] proved `--shop-crn` is dead code on pinned-town boards — but that is exactly the charge it leaves
open: on a pinned town the recorded shop schedule *replaces* the word draw, so all S=4 selection streams and the
held-out stream see the **same future shops**. The searcher was choosing macros while knowing the shop calendar.
`--robust-select S` splits knowledge from truth: at each dawn every candidate is rolled to game end on S streams
that each **draw** their own shops (town recording dropped → unlock back on the `2*used` cursor, distinct weed
seeds), the mean two-purse score picks the macro, and that macro is **committed on the ACTUAL episode — the pinned
town, the judge's own board, the baseline's own held-out stream**. Selection rollouts also replay the opponent tape
into a town it never saw; that breakage is candidate-symmetric, so it costs resolution, not sign.

*Byte-exact check first*: `--robust-select 4 --K 1` (zero jitter, 2 boards, 30 dawns) reproduces the pure policy on
both purses — `EXACT CHECK PASS`, so the harness swap moved nothing but the selection world.

## 2. The table — same 24 boards, same K=8/S=4, same seeds as [[alphaprobe2]]
| condition | Δmargin | se | t | Δours | Δtheirs | up | Σ in-sample | transfer |
|---|---|---|---|---|---|---|---|---|
| pinned selection (ALPHAPROBE2) | **+2,371** | 349 | **6.79** | +2,138 | −233 | 23/24 | +2,642 | **0.90** |
| **robust selection (this)** | **+763** | 400 | **1.91** | +722 | −41 | 14/24 | **+19,081** | **0.04** |
| paired (robust − pinned), 24 boards | **−1,608** | 421 | **−3.82** | | | | | |

Split: engine loss tail **+1,304 se 630 t 2.07** (theirs −145, 8/12); BAND250 **+222 se 469 t 0.47** (theirs +63,
6/12). cand-0 rate 0.63 (pinned 0.725) — under a drawn shop the scorer chases noise, so it leaves the policy's own
macro *more* often than the informed one did. Σ in-sample +19,081/board against a realised +763 is the
[[planselect]] / [[mpcfeas]] signature to the letter: the dawn score is measuring the lottery, not the macro.

## 3. Shop-hindsight share
**+2,371 − +763 = +1,608/board, 68 % of the ALPHAPROBE/ALPHAPROBE2 search gain, paired t −3.82.** It is not a
modelling artefact and not [[tape-fidelity]] noise: the paired difference is per board, same tape, same seat, same
candidate rng, same held-out stream, and only the selection world moves.

## 4. Verdict — **ALPHAFARM CLOSED**
Pre-registered bar: robust pinned gain ≥ +1,000/board, t ≥ 3, Δtheirs ≤ 0. Result **+763, t 1.91** — gift-free
(−41) but under both thresholds, and the surviving engine-tail read (+1,304 t 2.07) is itself below +2,000, the
arrival test [[p4premise]] sets for a planner. **No GO**: the offline-distillation path is not worth its build,
because the labels it would harvest are two-thirds a shop calendar the shipped policy can never read. What survives
is cheap and already ours: the jitter family has a small positive mean effect even when selected at random
(+763 with an effectively blind scorer), which is an argument for ordinary ES on those same Macro fields, not for a
search. Search-inside-the-episode is now CLOSED on every axis measured here — [[mpcfeas]] (rollout planner),
[[planselect]] (plan choice), ALPHAPROBE3 (dawn-by-dawn macro choice).
