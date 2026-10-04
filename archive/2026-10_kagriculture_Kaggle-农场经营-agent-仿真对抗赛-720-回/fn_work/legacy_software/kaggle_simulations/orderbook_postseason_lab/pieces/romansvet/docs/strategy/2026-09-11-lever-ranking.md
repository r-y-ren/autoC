# Lever ranking — everything not closed by paired real-engine evidence (2026-09-11, read-only)

Historical ranking. The P6 fertilizer-arbitrage premise was withdrawn on
September 12 after checking all thirteen original raw replays: early quotes
are 77–100, not 8–30, and the quoted revenue attribution is not net profit.
See [correction](2026-09-12-fertilizer-premise-correction.md).

Scope: a census of every direction that could still move the ladder rating, with the archive's
closing evidence attached where it exists. Read-only agent, no engine runs; every number quoted is
an archive paired-engine or calibration result, cited to file.

## 0. The measuring stick used throughout

* **Judge legs (paired, real engine, against candidate B = `flow193_g100_hr`, LIVE sub 56161192).**
  B's own base rates, from the auto-judge lines of 2026-09-11 (`S/glut/verdicts.log:381-397`):
  TOPB2 **32.5 %** (40 games), LIVEC-H30 **63.3 %** (60), LIVEC-H30B **83.3 %** (60), pooled
  hold-out 43-102 **73.3 %**, LIVE62 88.7 % (tuning set, dropped from promotion by §24 of
  `2026-09-10-consensus.md`).
* **Rating conversion.** 298 rating points per logit of judge-set win rate
  (`2026-09-10-rating-calibration-C.md`, CI 182-686; refit `2026-09-11-ladder-calibration.md`).
  At the pooled hold-out base p = 0.733, dlogit/dp = 1/(p(1−p)) = 5.1, so **+1 hold-out point ≈
  +15 rating points**, and one board flipped on a 60-board set (1.67 pts) ≈ **+25 rating**.
  Top-10 (2956) needs pooled hold-out **82.8 %** = +9.5 points = **≈ 6 boards of 60**.
* **TOPB2 is a floor, not a gauge** (`2026-09-10-rating-calibration.md` / `-B.md` agree): it cannot
  resolve 10 pp, so a TOPB2-only gain is never a promotion and a TOPB2-only loss is a veto signal.
* **Cost unit.** A full four-leg paired judge on one theta is ~7-10 minutes wall
  (auto-judge stamps 11:43:25Z → 11:50:31Z, `S/glut/verdicts.log:378-382`), 1.85 s/game
  (`2026-09-10-consensus.md` §9). A four-arm inference experiment therefore costs well under an hour
  of machine time; the agent-hours below are dominated by build and bookkeeping, not by games.

## 1. Planner / hand levers that are NOT closed

Everything else in the planner is closed with paired evidence — the two switch screens
(`S/glut/verdicts.log:35` TOPB 20 switches, `:76` LIVE-C22 15 switches) found **HIRE_ROW_ON as the
only built switch that pays anywhere**, and the labour, melon, wool, mix-rule, shop-adaptive,
purse-top-up, fertilizer, land-veto, cash-reserve, GROW_MAX, compact and sell-cadence families each
have their own closing document. What remains:

| # | lever | mechanism (one line) | coins bucket | evidence so far | expected judge gain if it works | cost | re-run risk |
|---|---|---|---|---|---|---|---|
| **P1** | **`OPEN_PUMP_UNITS` ≥ 90 / `OPEN_PUMP_MIN_MONEY` sweep on B's theta** | the d0 h0 wheat pump moves the opponent's quote 25→32 so their second SHEEP is refused; only the size is in question | opening pump | sweep is *partial*: `S/pump/summary.txt` ran UNITS 40 / 70 and KEEP 0 / 12 on the **hr** composition — UNITS 70 was the single positive read anywhere (TOPB2 25→30 %, +299, t 0.58) while LIVE-C72 went −278 (t −0.93); KEEP 12 catastrophic (−7,036, t −13.2); `MIN_MONEY` (1584) never touched; `2026-09-10-planner-wall-audit.md:67` still lists the sizing as "never swept" | TOPB2 +2.5-5 pts if the UNITS 70 direction is real and dose-responsive; hold-out ~0 (it was −278 at 70). Rating ≈ +0-25 | 1 agent-h, 0 GPU-h (constant override, no build) | **medium** — half of it *is* the closed sweep; new only in (a) UNITS above 70, (b) MIN_MONEY, (c) B's theta rather than hr's |
| **P2** | **pumper-aware hour-0 row order** (`OPEN_PUMP_SLOT0` re-order switch) | the top tier pumps too and our own SHEEP is the one refused (−4.6k on top-10 tapes); the race is decided by row order within turn 0 | opening pump | never built. Designed with an acceptance test in `2026-09-10-forward-horizon-feasibility.md` §5 ("cheaper structural alternative", 0.5-1 eng-day, byte-identical OFF). Precedent is the only structural lever ever promoted: OPEN_PUMP panel24 64→87 %, family B 96 %, +21.7k (`dominant-strategy-2026-09-03` memory) | TOPB2 +3-7 pts (it is top-tier-specific); hold-out 0-2. Rating ≈ +0-30 (TOPB2 cannot resolve it alone, so the read is mostly a veto check) | 4-8 agent-h build + 1 h judge | low — the *on/off* and the sizing are closed, the order is not |
| **P3** | **`PRESTOCK_ON` / `MARKET_PACK_ON` / `ROUTE_EARLY_ON` — re-screen after repair** | the whole day's buying sits on one BUY row at turn 1; the top files buy on two rows a day and run the purse to 0 nightly | board fill / price-per-unit | their TOPB screen is **VOID, not negative**: "idle-agent 3,000-coin signature, switch broken on this lineage" (`S/glut/verdicts.log:35`, `2026-09-10-verdicts.txt:31`). **Cause identified: `assert not (EARLY_SELL_ON and (MARKET_PACK_ON or PRESTOCK_ON))` at `plan.py:2478`** — the shipped tree runs `EARLY_SELL_ON=True`, so these two are forbidden at runtime and are the only OFF switches in the inventory that have never been validly measured on any shipped lineage (the surviving read is −334, t −0.21, n = 24, `2026-09-09-switch-sweep.md:127`, never re-confirmed). Priors differ inside the trio and the experiment should follow them: **PRESTOCK's only read is level** (−334, t −0.21, n = 24), MARKET_PACK's old engine read is a real loss (−1,366, t −2.05, n = 384, 09-03), and **`ROUTE_EARLY_ON` is a code bug rather than a strategy read** (sim −158,893 HELD42 / −165,371 LEG20 with **0 %** of boards identical — a switch that moves every board by 160k is broken, and it deserves a code look before any leg). `ROUTE_EARLY_ON` is blocked by the sibling assert at `plan.py:2481`, so **all three void switches are locked out by the same shipped choice**: we took `EARLY_SELL_ON` and thereby closed the whole prestock / market-pack / route-early family — and `EARLY_SELL_ON=False` now measures at **zero** (−77 ± 95 HELD42, −54 ± 195 LEG20, `2026-09-10-sell-hour-headroom.md` arm 3), i.e. the concession that bought the lock-out has since been paid off by the ES. `2026-09-11-purse-topup.md` §31 names exactly this as the surviving residual ("one BUY row per day leaves the day's revenue idle ~23 h — the PRESTOCK / intraday-market family") and the 2026-08-30 idle-turn diagnosis priced PRESTOCK at +2.4-4.8k/game before the lineage changed | unknown by construction. If PRESTOCK restores +2.4k/game it is ≈ +3-6 hold-out points ≈ +45-90 rating | 2-4 agent-h to find why the switch idles the agent + 1 h judge | low — a void screen is not a verdict; the 09-11 purse-top-up closure explicitly exempts it |
| **P4** | **`SELL_SPREAD_ON` — cap units per SELL row and push the remainder to the next row** | we sell 1,600 units in ~152 rows at 9.39 u/row; the top files use 389 rows at 3.95 u/row and realise 160/unit against our 144 | price-per-unit (the TOPB d15-29 discriminator) | the *turn layout* is closed (`2026-09-10-sell-hour-headroom.md`: every legal layout level or worse; `N_SELL_ROWS` 6 → LIVE-C 68.1→63.9 %, t −5.9, **entire loss is the one row behind the DROP at turn 21**; `N_SELL_ROWS` 4 identical to the coin; diagnostic layout 5 "lots 1+2 split, lot 3 whole" **exactly level**). Within-row `LOT_SLICE` is **inert by construction** (`sim/market.py:84 sell_walk` walks one cumulative curve — consensus §12, 16:35Z). What is *not* closed: `sell.allocate`'s spread itself — the sell-hour doc's own closing line is "the next question is a reservation, not a turn — whether `sell.press` has decodable range" — **and two `EARLY_SELL_MODE` values have never been run at all**: `"B"` = all six market turns 0-5, "sell as it lands" (plan.py:2390ff; the only evidence on record is "the lot fell back to A's on 8 days in 11"), and `"A0"` = lot 1 on turn 0 packed behind that turn's hires (plan.py:2368-2374). Both are **enum overrides, zero build**, and `"B"` is the row-count direction itself | if the 144→160/unit gap is half recoverable it is the single biggest bucket in the TOPB anatomy (+8-9k/game flips 6-7 of 12 boards): TOPB2 +15-30 pts, hold-out +3-6. Rating ≈ +45-90 | first a 0.5 agent-h **gene-slope check** on `sell.press` / `hold` (no engine games); only build if the range exists (6-10 h) | **medium-high** — the "exactly level" diagnostic layout is close to a closing read; the new version differs in that it forces the cap instead of hoping the learned allocator uses the extra row |
| **P5** | **`MELON_ADD_ON`** (additive melon: buy quad 2 on d0 and add 12 melon tiles without paying for them out of the mix) | the only *unbuilt* form of the d10-14 window | d10 melon pot | spec written and argued **against** in `2026-09-11-additive-melon.md` §5 (costs 1,000 + 960 of a 3,000-coin d0 purse that traces to 145 coins left, 0 free tiles on d0); proposed as an experiment anyway by `2026-09-10-topb-loss-anatomy-g1000.md` §5. Every *built* melon form is dead: MELON_OPEN 1.9 %/−19.6k, MELON_D10B −22.1k t −15.5, FORWARD_ADMIT ×3, PLANT_FILL_LATE, ANIMAL_RESTOCK | low. The anatomy's own §2 shows d10-14 is a **flat tax, larger on the boards we win** — so even a working version need not flip a board. TOPB2 +0-5, hold-out ≤ +1 | 6-10 agent-h build + 1 h judge | **high** — nine closed melon arms; the only novelty is additive-vs-swap, and the d0 purse trace says the additive form cannot be paid for |
| **P6** | **fertilizer market row** (the clone buys 46 fert at 8-30 on d0-9 and resells at 43-56) | commodity arbitrage on a product we already produce | price-per-unit / other | `2026-09-11-fertilizer-engine.md` measures it at **−1.9k/game against us** and calls the row **untested**, then deprioritises it: at our BUY row the d0-9 purse is 4-108 coins (§31) | ≤ +1 hold-out point; more likely negative — buying drains shop inventory and *raises their* fertilizer quote = denial handed back, the signature that killed five wool switches | 2-3 agent-h | medium — the application-throttle half is closed (09-06); the market half is not, but the purse arithmetic predicts displacement |
| **P7** | **town-conditional tomato on a late PIZZA unlock** | PIZZA_SHOP on d8 = both of B's big LOSS10 wins (tomato +30.0k); d14+ or absent = every loss (tomato 0-3.6k) | other (town draw) | `2026-09-11-loss10-anatomy.md` finds the correlation and explicitly concludes **"no switch build from this anatomy"**; `ENDGAME_TOMATO_ON` is dead on both screens (−4.3k TOPB, −5.5k LIVE-C22); the shop-adaptive top-5 family is closed 2026-09-07 (tomato only with ≥2 tomato shops by d9) | ≈ 0 — the town, not the seat, decides; neither seat can move the unlock day | — | **very high** — this is the shop-adaptive family re-labelled |
| **P8** | **top-tier abstention repair** — re-enter wool/melon in d20-29 against a top-tier seat, or return the 125 units g300 moved h1→h18 | our sell-mix abstention *raises* the late wool/melon quote the top tier is over-weighted in: the gift half nearly doubles (+1,099 → +2,005) while the denial half shrinks (−3,865 → −3,132) | price-per-unit (their d15-29 purse) | `2026-09-11-top-tier-transfer.md` §3/§4 measures all three channels (WOOL +1,454, MELON +551, MILK −2,034) and names the fix ("re-enter wool/melon late") — **never built or judged**. Its own §4 caps it: 0.9k of an 8.4k TOPB deficit, and gift and denial ride the same curve so a non-adaptive seat cannot flood the band's milk and leave the top tier's wool dear | TOPB2 +2-5 pts, hold-out ≈ 0 to −2 (against the band the same units are free, so re-entering costs there). Rating ≈ 0-25 | 4-6 agent-h build + 1 h judge | **medium-high** — the wool *family* is closed five ways (consensus §7), but every closed switch withheld wool; this one adds it, and against a different opponent class |
| **P9** | **herd latency, wool-sink gated** | we lock the herd 3-5 days after the clone | pasture cadence | PARKED, not closed: +261 in sim, denial-only, and the 20 candidate boards are ones we already win 80 % of → `2026-09-10-board-schedule-losses.md:168` calls the test powerless | ≤ +1 hold-out point | 2 agent-h | medium (the family is `shop-adaptive-top5-2026-09-06`, marked PARKED not CLOSED) |

**Switch-inventory coverage.** Every boolean switch in `plan.py` now carries a paired verdict except
the three above (P3): the 09-10 screens covered CARE_FILL, CARE_HOLD, HARVEST_FIRST, LATE_STRAW_CAP,
MELON_LOT_EARLY, SHED_OVERFLOW, OPP_MIX, ENDGAME_TOMATO, PLANT_FILL, MIDDAY_PLACE(+V2),
WHEAT_VOLUME, FERT_FLOOR, MIDDAY_DROP, FORWARD_ADMIT, OPEN_DENY, ANIMAL_DEFER and HIRE_ROW, and
SAME_DAY_FERT (−29.6k), OPP_SUPPLY (−2,972/−3,616 dose-responsive), OPEN_PUMP_TELL_KEEP0
(byte-identical), LATE_SELL_FILL (inert), COMPACT_SOFT, the land-veto trio, WOOL_SPLIT_CAP,
SHEEP_FLOOR and IDLE_PURSE_TOPUP were each judged separately. A switch-by-switch audit of all 41 module-level switches
(39 in `plan.py`, 1 in `brain.py`, 1 in `agent/book_straw.py`) closes the census at **9 shipped ON,
4 shipped by package override, 8 inert, 15 dead**. The only residue beyond the `EARLY_SELL_ON`
lock-out (P3) is: the two unrun `EARLY_SELL_MODE` values (folded into P4), `MELON_LOT_EARLY_TURNS`
(never exercised because its gate is a byte-identical no-op), `SEED_BEFORE_HERD` in
`agent/book_straw.py` (off the shipped path), and a long list of never-swept companion constants
(`BANK_MIN_VALUE`, `BANK_LOT`, `TAIL_HOPS`, `CARE_FILL_HOPS`, `ADMIT_ROUNDS`, `EST_MOVES`,
`EST_LEAD`, `LAND_OWN_DEN`, `DEV_DAYS`, `OPP_MIX_*`, `OPEN_PUMP_MIN_MONEY` …) — but the 12:19Z
constant screen (`2026-09-10-verdicts.txt:78`) already measured the four the wall audit ranked
highest (HIRE_BIAS_MAX, CREW_TARGET_PUSH, CHAIN_MAX, STREAM_MAX) and none was a lever, so the prior
on the rest is poor. **One reconciliation for the record:** `S/livec/chain_summary.txt` shows
`CREW_TARGET_PUSH` 300 at +749 (t 2.15) and 200 at +529 (t 1.74) against `g1000pair`, which reads
like an unconfirmed positive — it is not: the 12:19Z screen against the shipped hr composition on
TOPB + LIVE-C22 read **300 → −1.2k / −174 and 200 → −735 / −394**. Closed.
Two switches carry an owed-confirmation footnote that does not change their verdict:
`OPP_SUPPLY_ON` (pinned sim +617 t 2.54 against engine −2,972 t −3.80 — the engine wins) and
`OPEN_PUMP_TELL_KEEP0_ON` (byte-identical on 124 live + 40 TOPB games because the tell never fires;
its only ON data is a 4-seed probe, +6.4k/+5.4k against −38k/−24k, and the sim cannot read it).

**Not listed because closed with paired evidence** (cite before re-proposing): melon opening incl.
FORWARD_ADMIT and MELON_D10B (`2026-09-10-melon-route-capacity.md`, consensus §1/§6), wool in five
forms (consensus §7), mix rules and shop-adaptive top-5 (`dominant-strategy-2026-09-03`,
`shop-adaptive-top5-2026-09-06`), purse top-up and the whole labour/capital hand family
(`2026-09-11-purse-topup.md` §31), fertilizer application (`2026-09-11-fertilizer-engine.md`),
land veto / cash_reserve / GROW_MAX / COMPACT_SOFT (consensus §4, 12:57Z), the six planner findings
(consensus §14), strawberry cap (`S/strawcap/summary.txt`, dose-responsive denial hand-back),
intraday reactive control (consensus §2), forward-horizon rewrite (consensus §12, P ≈ 10-15 %),
LATE_SELL_FILL (inert), OPEN_PUMP_TELL_KEEP0 (byte-identical), sell cadence (consensus §12, 17:35Z).

## 2. ES-side levers

The controlling fact: **plain continuation is dead and every rung-mix arm so far reads below B.**
flow196 (B's own recipe continued from B) was flat for 172 generations and lost three straight
judge reads (`S/glut/verdicts.log`, consensus §36); flow197 (mid-band rotation) lost three
(§38/§39) with the drift signature — gains on the LIVE62 *tuning* set, losses on the hold-out.
Against that, the only mechanism that has ever produced a promotable theta is the
**gate-filtered lottery**: independent short seeds from a good seat, each judged at ~g100
(flow187 g160 → flow193 g100 = B, flow194 g100 = C; consensus §15, §23).

| # | ES lever | mechanism | evidence so far | expected judge gain | cost | re-run risk |
|---|---|---|---|---|---|---|
| **E1** | **Theta soup: average the independent passing draws** ((B + C)/2, and (B + C + flow187_g160)/3) | B (`flow193_g100_hr`) and C (`flow194_g100_hr`) are two *independent* 100-generation draws from the same g160 seat that both passed the hold-out rule (consensus §15). Averaging cancels the draw-specific noise and keeps the shared direction | **never tried** — no doc in `docs/strategy/` mentions theta averaging, soup or interpolation. The premise is measured: B's advantage is real on boards it was never selected on (`2026-09-11-hr-ladder-paired.md`: B vs hr +10/−2 flips, +1,579/board, t 3.5 on 60 fresh ladder boards) | +2 to +6 hold-out points if the noise half is as large as the two arms' disagreement (C beat B on the hold-out by +1 and lost TOPB2 by 2 — i.e. they differ mostly in noise). Rating **+30 to +90** | **0.3 agent-h**, 0 GPU-h (one numpy line + one judge run) | **none** — no closing doc exists |
| **E2** | **Step extrapolation / dose-response along the accepted direction**: θ(k) = θ_g160 + k·(B − θ_g160), k ∈ {0.5, 1.5, 2.5} | if the accepted 100-gen displacement is signal rather than a lottery ticket, more of it pays; if B overshot, k = 0.5 beats B | **never tried**. Two archive facts pull opposite ways: the direction is real on fresh boards (§40), but the one-step curvature fit priced the optimal step at h* 0.024-0.083 → lr 0.0003-0.0011, i.e. **steps are already 3-10× too large** (consensus §17 row 2) — which predicts k = 0.5 wins and k > 1 loses | a dose-response either way is worth more than its cost: k = 0.5 winning means every future arm should halve its accepted step (a permanent rate multiplier on the only mechanism that works) | **0.5 agent-h**, 0 GPU-h | **none** — distinct from the lr A/B, which varied the *per-generation* step at g1000, not the scale of an accepted 100-gen displacement |
| **E3** | **Re-run the σ / population / margin-scale A/Bs at B's centre** | §20 is explicit: "the pop / sigma / margin_scale A/Bs were measured **where there was nothing to find**" (at the g1000 peak, κ ≤ 0.014). At g940 the same estimator had κ = 0.040 and its step beat 16/16 randoms held-out | the one-step antisymmetric test is the validated instrument (`es-noise-floor-2026-09-05` memory; `2026-09-11-recentre-onestep.md`); 22 batch evaluations on the remote | not a theta, a **rate**: if σ or P resolves a gradient at B, the arms stop being lotteries. Indirect, but it is the only thing that changes the 1-board/day pace | 1-2 agent-h + ~2 GPU-h | low — same *experiment*, different *centre*, and §20 pre-authorises the re-run |
| **E4** | **More parallel independent seeds from B at g100** (the measured productive mechanism, applied wider) | the lottery has a hit rate; hits are what ship | measured pace ≈ 1 useful board/day across three arms (consensus §26); pace "scales ~linearly with arms" | +1.5-2 hold-out points per hit; ~6 boards needed for top 10 | 0 agent-h beyond scheduling; **GPU-bound** (3 arms is the hardware) | none, but it is what is already running |
| **E5** | **Optimizer A/B (Adam vs SGD)** | flow184's provenance note records that the default Adam was used where the builder prescribed `--optimizer sgd`, and this was never A/B'd (consensus §6, audit 15:50Z) | untested; Adam's diffusion is the suspected cause of a lineage "walking off its peak within 40 gens" (flow187 g200p/g300p/g313 → consensus §15) | a lineage that holds its peak is worth the same as a lottery hit, repeatedly | 1 agent-h stage + 3-6 GPU-h | low |
| **E6** | **Weight-decay / trust-region on the accepted step** (clip ‖Δθ‖ per 100 gens) | the same overshoot hypothesis as E2, applied inside the arm | implied by the h* pricing (§17 row 2); never run as an arm | as E2 | 1 agent-h + a GPU arm | low |
| **E7** | **Distillation from top-tier tapes** (fit θ to reproduce the top files' macro decisions) | the top tier is one template (`2026-09-11-top50-patterns.md`: 24/50 files are one clone; Majkel/SpaTaro one line) | the behaviour is known not to be worth copying where it has been forced: forced opening 94→26 % (`forced-opening-ramp-2026-09-09`), melon-in-theta on the probe board 50.7k vs 109.1k (`2026-09-10-planner-ceiling-B.md`), labour does not compound (`2026-09-11-labour-compounding.md`) | low, and the target behaviour is measured to be *worse* for our planner | 2-3 agent-days | **high** — this is the forced-opening family |
| **E8** | **Train on top-tier boards only** | make the 20 top-ten rungs the whole objective | already run in effect and rejected: the 20 top-ten rungs carry 37 % of the mass at w10.2 (consensus §11) and TOPB2, their held-out twin, sits at 25-32.5 %; n = 20 gate-field overfit is a standing memory item (`es-noise-floor-2026-09-05`: gate-confirmed thetas lose 2-4 pts on legs the gate never plays) | negative | — | **high** |

| **E9** | **`W_lost` re-weighting at B's / g940's centre** | weight lost rungs ×2-4 so the objective sees the boards we lose | measured **negative at g1000 only** (`2026-09-11-lost-board-objective.md`, consensus §21: held-out −956/−786 margin, win −6.7/−10.0 pt) — and g1000 is precisely the peak where §20 showed *nothing* resolves. The doc's own "not tried" list names "×2 mild re-weighting; W_lost on the flow172_g940 centre" | if the estimator resolves at B, this is the one objective change aimed at the 27 % of boards we lose | 1 agent-h + 2 GPU-h (one-step test only) | **medium** — consensus §23 declares the field-change ledger closed, so this needs E3 to come back positive first, or it is a re-run |
| **E10** | **coordinate-ranked subspace ES** | rank the 5,997 live coordinates by pooled \|g\| over the ten gradient draws already saved, then step only in the high-mass subspace | `2026-09-10-pop-spearman.md:115` names it as the next step; never run. The only subspace ever tried was hand-picked (535 bias coords, −1.6k) | would raise the per-draw SNR without paying P^0.5 in compute; no direct coin estimate | 2-3 agent-h + 2 GPU-h | medium — may be moot if \|g\| is itself noise, which §16 suggests at a peak |
| **E11** | **clone-specialist arm (flow199) + the generality assumption** | the matched pool is one clone family (24/50 of the top 50, and all ten of B's 2200-2400 losses — `2026-09-11-top50-patterns.md`, `2026-09-11-loss10-anatomy.md`); a family specialist may outrank a generalist on *this* ladder | consensus §17 row 7 lists "generality matters on this ladder" as **untested and load-bearing**; flow199 (the ten LOSS10 tapes at w4, md5 b78196de) has been staged since 10:05Z and **never launched**, queued behind flow200/201/202 | LOSS10 is the coin-flip half of the ladder below 2400: B goes 11W-10L there where the judge predicts 73 %. Closing that half is worth more rating than TOPB2 is | 0 agent-h (already staged); 1 GPU slot | low — but it competes with flow202 for the same GPU |
| **E12** | **remote gate redesign (240 boards, or paired Δmargin with a t-threshold)** | the record filter still runs 62 opponents / 124 games at `min_flips 5` | `2026-09-10-record-gate-calibration.md` + consensus §18 decided the change; `2026-09-11-flow201-staging.md:29` and `-flow202-staging.md:29` show the gate field still byte-identical. P(false accept) 16.7 %; power 50 % at +4.8 pts; the shipped g940 theta was net **+0** | saves GPU-hours, produces no theta; matters only because the arms are the bottleneck | 2 agent-h | low |

**Today's arms mapped to the levers above.** flow196 = E4 control (exhausted, 3 losses, stopped
g172). flow197 = rung rotation, mid-band (exhausted, 3 losses, stopped g140). flow198 = rung
rotation, top-tier, local (1 loss at g10, resumed g38). flow199 = LOSS10 tapes at w4 (fallback,
never launched). flow200 = flow199 + 9 new-template tapes, GPU0 (1 loss at g10, g30 judging).
flow201 = flow200 + 40 B-ladder opponent tapes, GPU1 (launched 12:12Z). flow202 = flow201 + 60
hr-ladder top-tier tapes, staged (md5 ea732ba5). **All seven are the same lever — the rung mix —
and none of them is E1, E2, E3, E5 or E6.** Eight judge reads from four arms since B, zero above B.

## 3. Ranked shortlist — top 5 by expected rating gain per agent-hour

Each is designed to yield a paired real-engine verdict on **TOPB2 + LIVEC-H30 (+ H30B)** against
candidate B's own csvs inside three hours, using `S/topb2/run.sh` and `S/livec/run_holdout*.sh`
with `S/bank/paired.py`.

1. **E1 — theta soup (B + C)/2.** Build `0.5*(flow193_g100_hr + flow194_g100_hr)` (and the 3-way
   with `flow187_g160`) — all three files are on disk (md5 `7fcf3948` / `e11df4a9` / `9dfb20c2`) —
   and judge each on TOPB2 + LIVEC-H30 + LIVEC-H30B against B's csvs. ~20 minutes
   of games for a direction nobody has measured, on the one axis where two independent passing
   draws already exist. Promote on the standing rule (pooled hold-out ≥ B + 5, TOPB2 not down).
2. **E2 — extrapolation dose-response.** Judge θ(k) = θ_g160 + k·(B − θ_g160) at k = 0.5, 1.5, 2.5
   on the same three legs. Either k = 0.5 wins (B overshot → halve every future accepted step, a
   permanent rate multiplier confirming the h* pricing) or k > 1 wins (a free theta), and a flat
   dose-response closes the axis for good.
3. **P3 — screen PRESTOCK in the only composition that is legal.** No build: the switch is
   forbidden beside `EARLY_SELL_ON` by `assert plan.py:2478`, and `EARLY_SELL_ON=False` is itself
   measured at **−77 ± 95 / −54 ± 195, i.e. zero** (`2026-09-10-sell-hour-headroom.md` arm 3), so
   the composition is affordable. Run a three-arm ladder of constant overrides through the existing
   screen harness (`S/drainpin/on2b.py "<switches>"`, the same one `S/topb2/run.sh` uses): B, then
   B + `EARLY_SELL_ON=False`, then B + `EARLY_SELL_ON=False,PRESTOCK_ON=True`, judged on TOPB2 +
   LIVEC-H30 against B's csvs. The middle arm prices the concession so the third arm's read is
   clean; kill on any positive d-theirs.
4. **E3 — one-step σ/P test at B's centre.** Run the validated antisymmetric one-step test
   (`2026-09-11-recentre-onestep.md` harness) at candidate B with σ ∈ {0.01, 0.02, 0.04} and
   P ∈ {512, 2048}, reading held-out κ and the ±d win deltas. It does not produce a theta; it says
   whether the three running arms are hill-climbing or buying lottery tickets, which decides how
   the remaining 12 days of GPU time are spent.
5. **P4-lite — the two `EARLY_SELL_MODE` values nobody has ever run.** Override
   `EARLY_SELL_MODE="B"` (all six market turns 0-5, "sell as it lands") and `"A0"` on B's theta and
   judge on TOPB2 + LIVEC-H30. Zero build — these are enum values the tree already accepts — and
   `"B"` is the row-count direction itself, the largest measured behavioural gap to the top tier
   (their 389 rows × 3.95 u at 160 coins/unit against our 152 × 9.39 u at 144). Run **P1 in the same
   hour** as a second override ladder (`OPEN_PUMP_UNITS` ∈ {90, 120}, `OPEN_PUMP_MIN_MONEY` ∈
   {0, 2400}): UNITS 70 on TOPB2 (+299, t 0.58) was the only positive direction in the 09-10 sweep,
   and this asks whether it is dose-responsive or noise. Kill either on a positive d-theirs.

Deliberately **not** shortlisted: MELON_ADD_ON (P5 — nine closed arms, and the bucket it targets is
a flat tax bigger on the boards we win), the tomato/town response (P7 — the shop-adaptive family),
distillation and top-tier-only training (E7/E8 — forced-opening and gate-field-overfit families).

## 4. Is 2950 reachable by 2026-09-23?

Honestly: **possible but unlikely — call it 20-25 %, and the trend since candidate B is against
it.** The arithmetic is not brutal on its face: B sits at 73.3 % pooled hold-out and top 10 needs
82.8 % (`2026-09-11-ladder-calibration.md`), which is +9.5 points = about six board flips of sixty,
and the measured pace up to 09-11 was roughly one useful board per day across three arms
(consensus §26, which projected top 10 on 09-19…09-23 at P ≈ 30 %). What has changed in the last
twelve hours is that the pace stopped: **eight paired judge reads from four arms (flow196 g10/g60/
g100, flow197 g10/g100/g140, flow198 g10, flow200 g10) are all below B**, the control arm was flat
for 172 generations, and the two rotation arms produced the drift signature — gains on the LIVE62
tuning set, losses on the hold-out. Every one of those arms varies the same thing, the rung mix, so
the campaign currently has one hypothesis in flight and it is failing; meanwhile the cheap axes
that nobody has touched (theta averaging, step scaling, the σ/P test at a centre where a gradient
might actually be resolvable) are worth hours, not days. The slope's own uncertainty makes this
worse rather than better: at the CI's upper end (686 pts/logit) six boards would be enough, at the
lower end (182) the same six boards buy 100 rating points and top 10 is out of reach by 09-23
regardless of how many arms run.

**The single result that would change the answer:** a paired read in which a theta *derived from B
without new training* — the soup (E1) or an extrapolated step (E2) — clears B by ≥ +5 pooled
hold-out points with TOPB2 not down. That would mean the accepted ES displacements contain
re-usable signal that costs minutes rather than GPU-days to exploit, converting the remaining
twelve days from three lottery tickets a day into a directed search, and it would push 2950 to
better than even. The symmetric result — soup and both extrapolations level or down, and E3 finding
κ ≈ 0 at B's centre — would say B is the same kind of peak g1000 was, that the rung-mix arms are
buying tickets at ~8 h each, and that the honest answer for 09-23 is no.
