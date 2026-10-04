# Open-lever census — what the archive has NOT closed (2026-09-14, read-only)

Scope: every direction that could still move B's rating, with its closing evidence
attached where it exists. Read-only research; no games, no training, no source edits.
Sources: `2026-09-12-HANDOFF-RESTART.md` (whole file), `2026-09-10-consensus.md`
(§1–§185, the decision record the restart doc appends to), `2026-09-12-HANDOFF.md`,
`docs/strategy/2026-09-0[89]-*` / `-09-1[0-4]-*`, `S/glut/verdicts.log`, `GOAL.md`.

## 0. The gap, stated honestly

B = `flow193_g100_hr`, sub 56161192. Latest authoritative read
(`2026-09-12-HANDOFF-RESTART.md:21`, 06:11Z 09-14): **rank 165, 2767.3**, fifth 2996.6
→ **229 rating points**. At §115's 298 pts/logit that is **≈ +4,600 coins of pooled band
margin per game**; at hr's own fitted slope of 369 (`2026-09-12-HANDOFF.md` §7.6) it is
≈ +3,700. No candidate since B has ever cleared **+450** pooled (§115's bar), and the
largest single promotion ever measured (B over hr) was ≈ **+800** coins (§119).
So the target is **≈ 6 B-sized promotions**, not one lever.

**The headline finding of this census is not a lever.** It is a selection-rule defect:

| | displacement from its parent | judged at | verdict |
|---|---|---|---|
| flow193 → **B** (the only promotable theta ever produced) | **‖Δθ‖ = 2.435** over 100 gens, 5,997 coords (measured here from `artifacts/kagg2_games/thetas/`) | g10 | **level/negative**, remote gate REFUSED it (`S/glut/verdicts.log:300`) |
| same run | same | g100 | **PASSED everything** → shipped as B (`:312`) |
| flow194 → C | ‖Δθ‖ = 2.392 | g10 | level (`:303`) |
| same | same | g100 | best pooled read ever, +8.3 pts (`:319`) |
| flow215_w00 (09-12) | **‖Δθ‖ = 0.0141**, 1,191 coords (consensus §139) | g10 | rejected |
| flow209 g20 (09-12) | ‖Δθ‖ = 0.0155 = **0.045 of one σ draw** (`verdicts.log` 01:07Z 09-12) | g20/g30 | rejected |
| flow213, C313/C314, H311/H312, J311/J312, seed309/310 (09-12→09-14) | 130–1,191 coords, sgd lr 1.8e-4, **10 generations** | g10 | all rejected |

Every arm since the 09-12 restart moves **≈ 1/170 of B's own accepted step** and is then
judged against a judge whose pooled SE is ±218 coins/board (§115). **B's own lineage would
have been killed by the current stop rule.** Nothing in the archive tests whether the
10-generation read is informative; the one prepared continuation (H gens 11–20) was
cancelled *because* g10 was negative (`HANDOFF-RESTART.md:14-20`).

## 1. Ranked table

Rank = plausible coins/game against the ~4,600 gap × probability the archive leaves it open.
Status key: **ENGINE-CLOSED** (paired real-engine legs) · **SIM-CLOSED** · **PARKED** ·
**UNBUILT** (proposed, never implemented) · **NEVER EXAMINED**.

| # | direction | status | best coin estimate (provenance) | source | 1–2 day test |
|---|---|---|---|---|---|
| 1 | **Generation budget: 100-gen lottery draws from the `flow187_g160` seat, judged at g100** | **NEVER EXAMINED since 09-11** (it is the only mechanism that ever produced a promotable theta; 2 hits in 3 draws) | +800 to +1,600 (B and C's own g100 judge reads: pooled +6.7 / +8.3 pts) | `verdicts.log:300,303,312,319,321,323`; consensus §15/§23 | relaunch the exact flow193 launcher (lr 3e-3, init `flow187_g160`, fresh seeds) on both GPUs, ~19 h/arm; judge only at g100 |
| 2 | **Market-row cadence — train *with* the extended row layout** | family ENGINE-CLOSED at B's frozen theta; **the trained version NEVER EXAMINED** | ceiling 78.3 % of top-tier market coin (5.33 M ref coin / 29 tapes); realised gain of every hand form ≈ 0 | `2026-09-11-expressibility.md:52-120`; §85/§87/§89/§90/§108 | build an arm on the SELL21/SELL5 row layout (`S/sell21/sell21.patch`) so the ES re-optimises around the turns; 10 gens is not enough — see #1 |
| 3 | **Shop-conditional per-product response (SMOOTHIE), LEARNED not hand-coded** | hand guard ENGINE-CLOSED (§124); **learned route UNBUILT** | **+475…+975 pooled band coins** (§121, 120 sim games, cross-sectional = ceiling) | consensus §121, `2026-09-12-band-winloss-ledger.md:110-116,186-232` | free `g5/gb5/press` (never pin press, §121) and train with smoothie/non-smoothie boards balanced; read `press3`/`grow_mult3` drift |
| 4 | **The 2953+ fertilizer-ENGINE class (half the top-five population)** | **NEVER EXAMINED as a lever** | none. B wins 32.5 % of TOPB2; no judge leg covers 2750–2950 | consensus §118, §115 ("gap: no leg covers 2750-2950 = the whole remaining climb"), §114 (milk floor) | cut a 2953+ engine-class leg (the 22 cluster-1 tapes exist) and measure B's per-product margin against it before designing anything |
| 5 | **`CREW_TARGET_PUSH` sized off `HIRE_COST[h]` instead of the constant 400** | verified ceiling, **fix UNBUILT, upward direction NEVER MEASURED** | binds on 46/300 board-days (15.3 %), mean 1.09 hands short, cash 18.8k at refusal | `2026-09-11-codex-defects.md:64-98`; consensus §78 | one switch (push = fib marginal cost), paired legs vs B; ~3 h |
| 6 | **P3: repair the `ROUTE_EARLY` double-subtraction, then screen PRESTOCK / MARKET_PACK legally** | screens are **VOID, not negative**; bug diagnosed 09-11, **never repaired or re-screened** | PRESTOCK priced +2.4–4.8k/game in the 08-30 idle-turn note; only read is −334 ± 95 (n 24, level) | `2026-09-11-route-early-bug.md`; `2026-09-11-lever-ranking.md:43`, shortlist item 3 | one-line fix at `plan.py:6404/6412`, then the three-arm ladder B / +`EARLY_SELL_ON=False` / +`PRESTOCK_ON` |
| 7 | **Expert-replay initialization (target round-trip audit first)** | **UNBUILT**; broad version has one negative engine test | wall imitation lost **−24,209/TOPB2 board** | `2026-09-13-expert-distillation-frontier.md`; `2026-09-13-partial-expert-action-probe.md`; `2026-09-11-wall-imitation.md` | the no-game round-trip audit on the 29 frozen tapes. **Conflicts with `GOAL.md`** ("no imitation") — needs a user decision first |
| 8 | **Post-sale extra HIRE working existing assets** | static census only; seed-only sibling ENGINE-CLOSED negative | 12 routes / 7 episode-days (d1–9); 21 routes (d1–26) = ~12 tile-yield units | consensus §148/§155; `2026-09-12-post-sale-hire-census.md`; §132 (seed hook −257 t −1.32) | default-off hook + one H30 engine pilot; the pool looks too small to reach +450 |
| 9 | **E10 coordinate-ranked subspace ES** | **NEVER RUN** | none | `2026-09-11-lever-ranking.md` E10; `2026-09-10-pop-spearman.md:115` | rank saved gradients, mask the top-mass subspace, one no-update cross-seed cosine gate |
| 10 | **Maturity-value feature → 132-coordinate new block** | hypothesis 1 **FALSIFIED**, so #2 not activated | — | `2026-09-13-improvement-research.md`; `2026-09-13-tomato-maturity-economics.md` | closed unless a different observable disagreement is found |
| 11 | **Early-stock PICKUP advance** | BUILT and JUDGED, not promoted (mixed) | LIVE62 +4/−2, LOSS10 +4/−1; TOPB2 −1, H30B −2, NEXT30 −2 | `HANDOFF-RESTART.md:876-889` | done; re-open only with a band-restricted trigger |
| 12 | **Integer lattice around B** | **SIM-CLOSED**, hold-out never spent, radius ≤ 2, singles only | best survivor +302 TOPB2 / −377 LIVE-C (refused) | `2026-09-11-integer-search.md:110-236,317-321` | only `land_bias` is untouched and has a real observable (§70) |
| 13 | **Additive melon (`MELON_ADD_ON`)** | **UNBUILT**; forced-plate forms ENGINE-CLOSED on an *older* lineage | costs 1,960 of a 3,000-coin d0 purse; gross ceiling ~12.5k, the "≈4,200 timing cost" is **withdrawn** | `2026-09-11-additive-melon.md:41-74`; `2026-09-10-melon-route-capacity.md:5-11,20-24`; `2026-09-13-melon-sigma-reachability.md:5-26` | not worth a slot: the d10–14 pot is a flat tax on wins and losses alike (§118, `topb-loss-anatomy:56-58`) |
| 14 | **Fertilizer market row / storage buy** | **UNBUILT and its premise RETRACTED** | the −1.9k "purchases re-sold" term is a gross-revenue artefact | `2026-09-12-fertilizer-premise-correction.md:3-38` | do not run; quotes are 77–100 on d0–9, not 8–30 |
| 15 | **FORWARD_ADMIT / projected task admission** | **ENGINE-CLOSED**, four independent negatives | −9,224 t −6.7 (engine band6, 72 rows); best-case reshape −1,456 | `2026-09-10-forward-admit.md:69-89`; `2026-09-09-verdicts.txt:919-920` | none. Also: the ES set `forward_days = 0` itself when given the free gene |
| 16 | **`_largest_remainder` tie-break fix** | **ENGINE-CLOSED, LEVEL** on B's lattice; from-scratch retrain untested | −488 / +20 / +24 / −192 across 4 paired legs (284 board rows) | `2026-09-11-codex-defects.md:23-62`; consensus §78 | only meaningful bundled into a from-scratch arm (patch `S/defects/fix_tiebreak.patch`) |
| 17 | **Forced-sale drop-hold** | closed by ANALYSIS only, **no engine test** | none; B's decoded `hold` on d25–29 averages 9 coins | `2026-09-11-codex-defects.md:100-134` | not worth a slot — day-29 stock is worth zero by rule |

## 2. Per-direction notes

**#1 Generation budget.** `verdicts.log:300` — "flow193_g10_hr JUDGED … Pooled hold-out
43-102: 40→40 (+10/−10) = level … Not promotable"; `:312` — "*** flow193_g100_hr PASSES
THE STOP RULE *** … pooled hold-out 40→44/60 = +6.7 pts". flow194 repeats it exactly
(`:303`, `:319`, +8.3 pts). flow195 (same recipe, seed 298) produced no record and was
retired at its 300-gen budget (`:321`, `:323`) — so the measured hit rate of the
"g160-seat, 100-generation" mechanism is **2 of 3**, and it has not been attempted since
2026-09-11. Re-seeding *from B* is different and has failed (flow196 flat for 172 gens,
consensus §36). I measured the displacements directly from the shipped thetas:
`‖flow193_g100_hr − flow187_g160_hr‖ = 2.4353` over 5,997 non-zero coordinates, against
consensus §139's 0.0141 for flow215_w00 g10. That is the whole story of the last two days.

**#2 Market-row cadence.** `2026-09-11-expressibility.md:52-60`: shipped switches express
30.3 % of top-tier market rows but only **17.9 % of the coin**; the union of *every*
switch setting still reaches only 49.6 %. §3 of the same doc: "sale timing outside our
four lot turns = **81.9 % of the inexpressible coin**". Every attempt to buy it at B's
frozen theta failed — LOTS one-step NO-GO (§87), SELL5 (§89/§90: the ledger's +911 became
−1,134 on the screen), SELL21C (`verdicts.log` 01:59Z 09-12: "≈ +12/game over 120, LEVEL
both legs"), `EARLY_SELL_MODE="B"` (−7,976 TOPB2 t −9.8). §108's mechanism argument —
"press/hold price OUR curve, the loss is THEIR curve rising, invisible to our fitness at
fixed f" — is the reason a *hand* dose cannot work, and is exactly the argument for
letting the optimiser hold the extra turns. No arm has ever trained on a layout with more
than four sell turns. UNVERIFIED whether the trainer's sim supports the SELL21 layout
without a port.

**#3 Smoothie / shop-conditional.** §121 is the only decomposition in the archive that
finds a promotion-sized prize that is not the shop lottery: "+675 strawberry for −3,252
tomato, −2,745 wool, −1,567 carrot, −1,133 egg … Reachable pool ≈ 1.9-3.9k per smoothie
board ≈ **+475…+975 pooled band coins** if half is captured (vs the §119 +600 bar)". The
hand guard built from it was judged and refused (§124: NEXT30 +87, H30B −60, NEXTHIGH −81)
— which is evidence about *that guard*, not about the conditional response. `st.shops` is
already in `PolicyObs` (`band-winloss-ledger.md:230-232`), so no interface work is needed.
Caveat the doc states itself: "cross-section = selection; +700 is a ceiling on where to
look, not a predicted gain".

**#4 The 2953+ engine class.** §118: the 2780–2950 band is **30/30 band clone, 0 engine**;
the fertilizer-and-mixed-crop engine appears only at 2953+ and is 22 of 100 catalogued
tapes (TOPB2 10/20 + TOPTEN 11/20). §115 states the measurement gap outright: "no leg
covers 2750-2950 = the whole remaining climb". §114 found the one mechanism that ever
gained against that tier (extra milk volume floors their d20–29 milk price: −4,864 off
them for −2,140 of ours on 107014447) and §118 says the engine answer "is owed after the
band arm". **Nobody has built it.** This is the population that actually occupies the top
five, and B has never met an opponent above 2631 on the live ladder (§119 caveat).

**#5/#6 Decoder and planner defects.** Of the codex blind review's three: the tie-break
was fixed in a copy tree and **measured level in the engine** (four legs, 284 rows —
consensus §78: "B does not lean on the bug"); `CREW_TARGET_PUSH` was verified as a real
but narrow ceiling (15.3 % of board-days, 1 hand deep) and the proposed fix — size the
push off `HIRE_COST[h]` — was **never built**, while the only sweep ever run moved the
constant *downward* (300 → −1.2k, 200 → −735); forced-sale drop-hold was ruled "the law"
with **no engine test**. Separately, `ROUTE_EARLY_ON` subtracts the same `early` vector
twice when `ROUTE_SPLIT_ON` (shipped True) is on (`plan.py:6404` + `:6412`) — diagnosed
2026-09-11, never repaired, and it is the reason the PRESTOCK/MARKET_PACK/ROUTE_EARLY
screens read VOID rather than negative. All three switches are default-OFF, so none of
this is a defect in shipped play; the value is that P3 becomes measurable.

**Majkel's bought wheat.** The finding is real at the opponent-vs-opponent level —
Majkel buys 117–190 wheat units (4.1–7.2k) against SpaTaro's 375–535 (14–21.7k), the whole
−8.8k median spend gap (`2026-09-11-majkel-vs-spataro.md:20-23`). Its *generalization* was
tested with a pre-frozen stop rule on 09-13 and **failed**: template medians of purchased
wheat per animal-output unit are Majkel 0.174, Otter Vibe 0.260, SpaTaro 0.401, feel the
agi 0.441, c0nrad 0.899 — "zero supporters, so the stop fires"
(`2026-09-13-top5-wheat-accounting.md:56-62`). **B's own bought-wheat spend in COINS has
never been measured**, and B was deliberately excluded from that table (`:66-67`). B's
*units* are known incidentally: 105–198/game over 13 live replays
(`2026-09-11-loss10-anatomy.md:38-51`), i.e. already inside Majkel's band and far below
SpaTaro's — so the likely finding is that B is already on the efficient side. Cheap to
close: one replay-accounting pass, no games. I mark the "B is already efficient" reading
**UNVERIFIED** — no document states it.

**Opponent-conditional play.** Four distinct closures, none of them general:
shop-adaptive herd closed on a read the archive itself labels a lottery
(`2026-09-09-verdicts.txt:446`, opposite signs by base; `2026-09-09-lottery-audit.md:301`);
shop-adaptive top-5 mix closed on **sim only**, herd latency **PARKED**; adaptive
theta-switching closed on a reliability argument (sim); town-conditional tomato explicitly
"no switch build from this anatomy". And the premise was inverted on 09-10: "**we are the
shop-adaptive seat and the clone is not**" (`2026-09-10-board-schedule-losses.md:14`) —
though Majkel1337 and SpaTaro *are* adaptive from step 1 (consensus §423). §78/§92 declare
the observation/opponent-model class empty, and §114 verdict (c) says the tier difference
is "not conditionable on anything observable". That is a claim about *hand* switches; the
learned conditional response (#3) is the surviving form.

**What the rank-1 file actually does** (`HANDOFF-RESTART.md:1052-1070`, three replays of
Majkel1337/56156662, 230W-25L = 90.2 %): first melon planting **day 0** (B: days 9/11/9);
first SELL order **day 10** (B: days 20/22/20); 242–294 new-plant transitions (B 173–205);
11 hands by day 10 (B 8–9); **356–436 SELL commands spread across all 24 hours** against
B's 125–152 confined to hours 1/10/18; explicit PASS 0.89–0.94 % against B's 10.0–10.9 %.
Three of those five gaps are the market-row cadence (#2). The fourth — the day-0 melon
plate — is the one thing that has been forced and lost repeatedly (wall imitation
−24.2k/board), and the reachability probe found **zero** day-0 melon targets in 8,192
perturbations (`2026-09-13-melon-sigma-reachability.md:160-161`).

## 3. Where the archive contradicts itself

1. **Fertilizer arbitrage.** §34 priced the clone's d0–9 fertilizer buys at quotes of
   8–30; §137 / `2026-09-12-fertilizer-premise-correction.md:3-7` checked all thirteen raw
   replays and found quotes of **77–100**, first reaching 30 on days 21–25. The premise is
   withdrawn; the ~1,915-coin term was a gross-revenue artefact.
2. **`CREW_TARGET_PUSH` sign.** `S/livec/chain_summary.txt` reads 300 → +749 (t 2.15),
   200 → +529 (t 1.74); the 12:19Z screen on the shipped composition reads 300 → −1.2k,
   200 → −735. Reconciled in `lever-ranking.md:67-70` (the hr-composition screen wins), but
   the positive numbers are still on disk and were quoted downstream. **UNVERIFIED**
   whether that 12:19Z screen was engine or CRN-sim — neither doc says.
3. **B's equilibrium.** §115 built the promotion rule on "a candidate replaces hr, B stays"
   because hr was assumed stronger; §119 then found B **is the stronger file** and inverted
   the justification while keeping the rule.
4. **The rating slope.** Every coins-per-rating figure uses 298 pts/logit; hr's own free
   two-parameter fit gives **369** (§119, `HANDOFF.md` §7.6) — "+24 % on every rating Δ if
   adopted". The 4,600-coin gap in this document is therefore ±25 %.
5. **Fixed vs resampled rungs.** `GOAL.md` prescribes "Resample the seed set across
   generations. A globally fixed seed set lets the population overfit those specific
   episodes" — and every arm since flow209 runs `--pinned-once --pinned-fixed-seed`, which
   §110 then diagnosed as exactly that memorisation. The ROTBAND rotation built to fix it
   (flow215) was run for a single fixed 10-generation window and abandoned.
6. **Imitation.** `GOAL.md` states the objective is an agent "whose entire strategy is
   **learned from game outcomes alone — no imitation, no hand-written strategy, no labelled
   data**". Direction #7 (expert distillation) and every hand switch in the P-series
   violate that on its face. This needs a user ruling, not an agent decision.
7. **Dangling citation.** `2026-09-10-forward-admit.md:9` cites
   `2026-09-09-forced-opening-ramp.md`; **no such file exists**. The content is the
   2026-09-08T21:40Z entry in `2026-09-09-verdicts.txt:919`.

## 4. Top three recommended experiments

**E-A — Re-run the only mechanism that ever worked (direction #1).**
Two GPU arms, exact flow193 launcher (init `flow187_g160`, Adam lr 3e-3, 4 free-gene set),
fresh seeds, **100 generations**, judged only at g100 on the seven families. ~19 h/arm,
both GPUs, one day. Prior: 2 hits in 3 draws.
*Fastest falsifier:* reconstruct the g10→g100 curve from the **existing** flow193/flow194
lineage instead of guessing. Only `flow19{3,4}_g{10,100}_hr.npy` and `flow195_g10_hr.npy`
are on local disk; whether flow193's periodic 10-gen checkpoints survive under
`~/stage_hr/artifacts/flow193/` on the remote host is **UNVERIFIED** and is the first
thing to check (the host's artifacts were never deleted). If they do, judge g30 and g60 —
20 minutes of CPU, zero GPU. A monotone climb from level (g10) to +6.7 pts (g100) means
the 10-generation stop rule is the defect and E-A is a directed search. A flat g30/g60
means the g100 pass was a lottery draw and E-A is a 2-in-3 ticket that still beats the
0-in-15 record of the 10-generation arms. If no checkpoints survive, E-A *is* the test:
read its own g30/g60/g100 and stop only on a flat curve.

**E-B — Learn the shop-conditional per-product response (direction #3).**
One arm, `g5/gb5/press` free (press must NOT be pinned — §121 reverted that decision),
training boards balanced on SMOOTHIE_SHOP presence, run under E-A's generation budget.
*Fastest falsifier:* before any GPU time, run the sim screen (`S/objaudit/screen.py`,
ρ 0.77 with the engine, ~12 min) on a hand-set theta that moves `press3` and `grow_mult3`
in the *opposite* direction to B's measured smoothie response. If the reachable pool does
not show up as ≥ +400 on smoothie boards in the screen, the +475…+975 ceiling is
cross-sectional selection and the arm is not worth a GPU.

**E-C — Cut a 2953+ engine-class judge leg (direction #4).**
The 22 cluster-1 "fertilizer engine" tapes are already catalogued (§118,
`S/nexthigh/anatomy.py`). Cut them into a leg with the existing `S/nexthigh/` pipeline and
measure B's per-product margin against them. ~4 h, CPU only, no training.
*Fastest falsifier:* if B's per-product margin against the engine class has the same shape
as against the band clone (d15-29 dominant, strawberry/wool price lines), then §118's
"the engine answer is owed" is wrong — there is one opponent class, not two, and the whole
2750–2950 measurement gap collapses into the existing band legs. If the shapes differ,
this leg becomes the missing rung for the last 230 rating points, which no current judge
family can see.

**Not recommended:** additive melon (#13), fertilizer market row (#14), FORWARD_ADMIT
(#15), drop-hold (#17), integer search beyond `land_bias` (#12). Each has either paired
engine negatives or a retracted premise.
