# ASTRA BRAINSTORM 7 — third participant: BRAINSTORM4 round-1 review (STRAW_FERT_FULL ledger repair, three volume audits)
Date: 2026-09-29 16:15-16:18Z | Model: gpt-6-astra (reasoning high, read-only, ephemeral) | Prompt: S/astra_bs7/prompt.md

**1. STRAW_FERT_FULL: admit a corrected ledger, then a build.** I withdraw BRAINSTORM6’s aggregate purse estimates; the unit replay supersedes them. STRAW_WAIT1 is closed.

The fertilizer trade is already material in the reported results:

| D=21 | Extra strawberries | Strawberry Δown / Δrival | Fertilizer Δown / Δrival | Total Δown / Δrival / Δmargin |
|---|---:|---:|---:|---:|
| v21 | 24.2 | +7 / −3,749 | −1,021 / +969 | −1,014 / −2,780 / +1,766 |
| m40, 37 retained | 22.2 | +117 / −2,777 | −824 / +910 | −706 / −1,867 / +1,160 |

Thus v21’s strawberry denial is **3,749**, of which fertilizer rent returned to V56 consumes **969, or 26%**. Diverting 24.2 fertilizer at approximately 48.5 sacrifices approximately **1,174 gross receipts**; repricing our remaining fertilizer sales partly offsets that. The strawberry column already reprices our existing late book: **+7 total**, not 24.2 multiplied by the sale quote. [Book decomposition](/mnt/e/_work/kaggriculture3/S/brainstorm4/res/fertled_v21.md)

**The pre-screen is not yet an executable counterfactual.**

- On a strawberry production night, dawn age must be **10/12/14/16**. Yield becomes `min(4, held + 1 + watered_and_fertilized)`. An application expires at **application day+2**, so it can cover **two** production nights. Extra yield is zero when the held-yield cap binds. [Engine](/mnt/e/_work/kaggriculture3/src/kagg3/sim/eod.py:80)
- The census uses **pre-h17** fertilizer status, not production-night status; applications during h17–23 can make supposed omissions disappear. It does not establish watering, harvest, transport or sale availability.
- Funding searches fertilizer sales from **d−2 onward without an upper deadline**. Later sales cannot supply an earlier application.
- Fertilizer repricing uses **0.2×later units**, losing removed units at their average lot price; it does not replay purchases, integer quotes, simultaneous commitments or floor behaviour exactly. [Pre-screen](/mnt/e/_work/kaggriculture3/S/brainstorm4/fertled.py:1)

YIELD1 found **zero unfertilized strawberry production nights through d17** on another 21-game sample. Different opponents can explain this, but first reconcile **sample, clock and actual EOD state**. [YIELD1](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-29-yield1.md)

**Transfer:** −2,780 is not portable. Scaling only the −3,749 strawberry effect by late-wave size gives these illustrative sensitivities:

| Rival | Late strawberries | Scaled strawberry denial | Net rival change if fertilizer gain remained +969 |
|---|---:|---:|---:|
| P48 | 155 | −2,794 | −1,825 |
| PQ4 | 168 | −3,028 | −2,059 |
| Majkel | 189 | −3,407 | −2,438 |

These are **not forecasts**: sale order, demand, floors and our production differ. Their late fertilizer sales—approximately **90/83/75**—confirm a rent transfer remains; the complete subsequent book determines its size. Majkel has no faithful closed-loop judge. Clones selling approximately **65–76 late strawberries** cannot certify transfer against 155–189. [Family books](/mnt/e/_work/kaggriculture3/docs/strategy/2026-09-29-topaudit2.md:29)

**Resources:** 24.2 additional applications would require at least **24.2 unit-actions**, plus any pickup, travel, water and harvest actions. Two-event coverage could reduce applications. Fertilizer must be carried to apply it. Retained fertilizer and added strawberries both enter the capacity calculation; require **zero additional overflow/displaced deposits** and preserve animal work.

**Grid/bar amendment:** retain **OFF, D17, D21**; exclude D26, whose v21 gain over D21 is only **65**. First repair all **61** traces, including the three omitted m40 cases, and deduplicate coverage using actual EOD events. Require corrected ledger margin **≥1,000 on each set** before building. Then OFF identity **6/6** and closed-loop v21/m40: margin **≥1,000, paired t≥2**; wins **≥15/21 and ≥38/40**; mean own **≥−1,200**; late egg/wool/milk units each **≥PFS**. Freeze one arm before clone checks; each 80-game clone set requires own **≥500, t≥2**, plus margin **≥0**.

Subjective **P(pass V56)=25%**; **P(pass all clone checks | V56 pass)=20%**; approximately **5% combined**. The m40 ledger has only **160** margin headroom above the bar.

**2. Three remaining volume audits, ordered by implementation cost**

All switches are OFF through d9. Counts below distinguish measured opportunities from audit targets.

| Lever and exact switch | Ledger read that kills it | Margin arithmetic |
|---|---|---|
| **`STRAW_FERT_FULL=17`**: apply only to verified uncovered production events d12–17, with carried stock, watering and sale by d18; recompute subsequent coverage. | No actual uncovered EOD events; unavailable fertilizer/action; corrected paired margin <1,000. | Reported bulk result: **15 units×104.5 net margin=1,568**. This is preferable to extrapolating the isolated **204/unit**. |
| **`CARE_COMPLETE_18`**: d10–17, add CARE on already-fed existing animals only when banked bonus survives the next production cap and produces a sale by d18; replace only route-feasible PASS actions. Rank by paired book value. | Every eligible animal is already cared, bonus clips, or harvest/sale cannot complete by d18. CARE on production day banks for the **following** event. | Audit targets: **5 early wool×199≈995**, or **21 eggs×48≈1,008**, before displaced work. Eligible counts are unmeasured; the prior includes **0**. |
| **`PRE_FIRE_CLEAR_18`**: d10–17, harvest an existing tile before a production event only when doing so prevents clipping and the recovered increment sells by d18; preserve care/feed/water actions. | No baseline clipping, or the intervention merely advances an existing sale without increasing terminal sold units. | **5 strawberries×204≈1,020** or **6 early wool×199≈1,194**, before costs. YIELD1 measured **0 crop cap loss**: crop-side expectation on that sample is **204×0=0**. Animal clipping remains to census. |

These are three audits, not three established sources of supply. Generic replant fill remains behind CARROTFLAT/WHEATLATE’s failures; a strawberry planted d10 cannot yield before d20. ENGTAIL’s under-request finding does not establish spare executable work on these PFS traces.

**3. Round 2:** repair the agent’s fertilizer ledger, then run D17/D21 only if it clears; census CARE_COMPLETE alongside it, with round 3 reserved for that cell only if it identifies approximately **1,000 net margin** of feasible units.

**4. Slot:** unchanged—retain the two PFS copies; neither these ledgers nor P48GRAPH4’s d1–3 replay changes the **2026-09-30 18:00Z** upload cutoff.

## Prompt

## ASTRA BRAINSTORM 7 (2026-09-29 16:15Z) — third participant: BRAINSTORM4 round 1 review

You are the standing third participant of BRAINSTORM4 (fresh Opus agent + orchestrator + you). Repo /mnt/e/_work/kaggriculture3 (read-only). Read first: docs/strategy/2026-09-29-astra-brainstorm6.md (your BRAINSTORM3 verdict and the STRAW_WAIT1 seed, incl. the prompt with the full context), S/astra_bs7/round1_excerpt.md (BRAINSTORM4 round 1), docs/strategy/2026-09-29-cloned0_1.md (the clone hoards from d4: 2-3x P48's purse; the BC-rival line is closed), docs/strategy/2026-09-29-clonemkt1.md, and the tail of S/p48graph4/checkpoint.txt (the port: the cash-guarded d1-3 replay holds 16/16 with real-like cash at the d2-3 cow hours, but d4 lacks the wheat sale and the d8 milk slips to d9 because the engine's care bonus counts fed-and-cared days).

### Round-1 result
Your STRAW_WAIT1 is killed by the exact ledger on 61 PFS-vs-V56 traces (final money = the control rows 61/61): 0 deferrals in 61/61 because next-24h demand (7-43 units) never exceeds twice the conservative rival estimate (32-77) + 2; the oracle version gains +42..+49 margin at most; the unconditional hold-and-release-d26 variants gain +287..+762 margin but overflow the shared shed (peak 141-159, 13-23 units displaced per game; room-enforced +10..+36); your aggregate sensitivity overstated both purses 6-7x (the exact replay: lockstep walk, $1-floor units add no supply, drain taken from the trace). Timing is closed against V56: no same-day-earlier or +24 h move of a unit gains more than +7.3 margin/unit over the 7 products; your invariant holds (strawberry d23-28 +24 h: +21.3 own / +18.8 rival). The agent's new finding: THE MARGIN IS IN VOLUME - one extra strawberry sold d14-18 is worth +204 margin at +3 own (pure denial), a wool unit d10-13 +199, an egg +48. Its round-2 cell STRAW_FERT_FULL=D: force a fertilizer application on every unfertilized strawberry yield event from d12 to D (PFS fertilizes 97 of 128 such events per game while SELLING 119 fertilizer units at 48.5; its fertilizer rule counts only our own coins, ~0 per extra strawberry vs V56). Ledger: v21 D=21 own -1,014 / rival -2,780 / margin +1,766 (19/21 traces positive; D=17 +1,568; D=26 +1,831); m40 D=21 own -706 / rival -1,867 / margin +1,160 (26/37 positive). Grid D in {17, 21}; bar V56 v21 + m40 margin >= +1,000 at t >= 2, W >= 15/21 and >= 38/40, own >= -1,200, late egg/wool/milk units >= PFS; then own >= +500 t >= 2 vs p48c / pq4c / g0capsfix. Engine facts to weigh: fertilizer applied to a tile raises the next yield (find the exact yield rule in src/kagg3/spec.py / sim); fertilizer sells at ~48.5 into a book that never recovers in-game (first seller takes the rent: our fert sales also DENY the rival's fert price - PFS's live fertilizer gap vs the programme is -5.2k); one fert unit applied = one fert unit not sold; the strawberry book: V56 sells 208 units d18-29, P48 155, PQ4 168; our own late strawberries (191 units on v21) are repriced by our extra supply too. Prior art: FERT_DUMP (fertilizer allocation from d5), CARROTFLAT/WHEATLATE (volume-by-fill cells closed on price), ENGTAIL (we under-request), the five established points of BRAINSTORM3 (no d3-9 slack; the wall; late animal volume; clones blind; nothing beat PFS).

### Deliver (markdown, ≤ 1,200 words, numbers not adjectives)
1. STRAW_FERT_FULL critique: the exact trade (fert units not sold at ~48.5 and the fert-book rent we then leave to the rival vs strawberry units gained and their own/rival price effects incl. our own late book), where the ledger's -1,014 own / -2,780 rival comes from by book, whether the rival's -2,780 survives against P48/PQ4 (155/168-unit waves, and they also sell fertilizer) and against Majkel; the shed/labour cost of the extra applications; amend the grid/bars if needed (exact). P(pass) for the V56 screen and for the clone checks.
2. Given "the margin is in volume" and "no d3-9 slack": list the three cheapest VOLUME levers left on PFS that add units sold d10-18 WITHOUT touching d3-9 purse/tiles (e.g. fertilizer allocation by book value incl. denial, care/water completion on existing tiles, harvest timing, seed choice on replants d10+), each with an exact switch, the ledger read that kills it, and expected margin per unit x units.
3. One line: what BRAINSTORM4 round 2 should run (the agent's cell, one of yours, or both), and the round-3 fallback.
4. Slot: unchanged or not (1 sentence); and whether any of this changes the 09-30 18:00Z cutoff for the two PFS copies.
