# Strategist: the three best next experiments — 2026-09-11T22:4xZ

Written after reading consensus §55-§91 in full, the two codex blind reviews (§74) and
`2026-09-11-codex-astra-advice2.md`, `-timing-prize.md §Judgement`, `-leftover-audit.md §fertilizer`,
`-ladder-projection.md`, `-b-toptier-ledger.md`, `-margin-scale-AB.md`, and the last 13
`AUTOJUDGE-vsB` lines of `S/glut/verdicts.log`.

**The finding the ranking rests on.** Our measurement stack is *bimodal in opponent strength and has a
hole exactly where the next 450 Elo points live.* Training objective mass (`launch_flow209.sh` body,
line 140): top-ten rungs (TOPB2 ids, opponents **2953-3081**) **37.2 %**; 2300-2700 **30.6 %**;
1900-2100 **17.9 %**. Promotion gate: LIVE-C hold-out (live opponents, ≤ ~2500) + TOPB2 (2953-3081).
And Kaggle matchmaking (`-ladder-projection.md §1`) draws opponents at **own rating ± 45 with no tail**:
B's pool is 2324 ± 49 (max ever met 2433), hr's is 2470 (max 2675); **neither file has ever played an
opponent rated ≥ 2700.** The band 2550-2800 — the only band that can carry us from 2495/2614 to the
2967 cutoff — is **0 % of the objective and 0 % of the gate.**

---

## 1. NEXT-BAND: build the missing rung (2550-2750) and test the judge on it with B vs hr

**Hypothesis.** Every promotion and lineage decision is currently made on a band we have outgrown
(LIVE-C/LIVE62, opponents ≤ ~2500) plus a band we cannot reach for 450 points (TOPB2, 2953-3081).
If the judge's ordering is band-dependent, the incumbent (B), the seed choice (flow209 over flow210)
and every refusal of the last three days were decided on the wrong opponents.

**Not covered by a closed family.** §23 ("fresh-board objective — NEGATIVE; field-change ledger
closed") added 30 *more boards of the same live band*: it changed board identity, not opponent tier.
§27/flow198 added the 2900+ tier — the far side of the hole. §21's own rule licenses this exactly:
"a changed field means new boards, **opponents** or seats". Nobody has ever measured us at 2550-2750.

**Cheapest falsifier (~2 h CPU + ~2 h legs, no GPU).** Pull ~30 public replays of teams rated
2550-2750 (credential-free `ListEpisodes`, the pipeline that built `S/livec/`), convert to pinned-town
action tapes, run **one paired engine leg of B vs hr** on them.

**Pre-registered bar.** B > hr at |t| ≥ 1.5 (as on LIVE-C and TOPB2) ⇒ judge is band-invariant, NEXT30
becomes a free 5th leg. hr ≥ B at t ≥ 1.5 ⇒ **band-dependent**: re-make the incumbent and seed choices.
Neither ⇒ underpowered; extend to 60 boards once, then stop.

**Expected size.** 0 coins; up to **~160 Kaggle points** of lineage choice (equilibria B 2562 vs hr
2722) because it decides which lineage we breed and ship — and it is a precondition for pricing any
candidate against 2967.

## 2. GATE-vs-LADDER: put one TOPB2-refused, live-band-positive record on the ladder

**Hypothesis.** The gate's TOPB2 clause taxes us 450 points early and refuses the one direction that
pays at our actual rating. The records say so: of the last 13 `AUTOJUDGE-vsB` reads, **12 lost wins on
TOPB2 while 8 gained wins on held-out LIVE62** — flow206_g10 and flow205_g10 at **+6/−0**,
flow198_g10 at +10/−2, flow200_g100p at +8/−2. That is a systematic band gradient, not noise.

**Not covered.** Every closure in §55-§91 is a *lever* closure; nothing has tested the **gate** against
the ladder. §37/§40 tested the judge's B/A/hr ordering by replaying ladder boards *through the same
tape judge*, never against ladder outcomes. LIVE62 was dropped from promotion (§24) on ONE datum —
hr's +0.64 LIVE62 logit "never reached the ladder" — and §45 then showed the two live files' ratings
are pool-confounded and indistinguishable on common support, so that datum is itself confounded.

**Cheapest falsifier.** Sim-screen the 3-4 stored refused records on the NEXT30 boards (5 min), pick
the one with the best live-band win delta and no NEXT30 regression, upload it into **B's slot** (the LB
entry is hr at 2608, so B's slot costs nothing), read at 80 games (~8 h at B's 11.8 games/h).
**Needs user approval** (upload). Not a promotion — an instrument test.

**Pre-registered bar.** ≥ 2550 at g80 with mean opponent ≥ 2300 ⇒ the TOPB2 clause is mis-weighted at
our rating; LIVE62 and live-band win flips return to the promotion rule. ≤ 2450 ⇒ the gate is right and
this line closes permanently.

**Expected size.** ±0 to **+150 Kaggle points** on the slot, and it re-opens or permanently closes a
whole class of refused candidates. Highest information per hour on the board.

## 3. flow211: the third arm, seeded by #1, with the rungs re-pointed at the band we face

**Hypothesis.** flow209 and flow210 differ only in seed; their *field* is identical and contains no
2550-2800 opponent. The §21-legal field change is to insert the NEXT30 tapes at w10.2 and drop the 20
top-ten rungs to w4 (objective mass: top-ten 37.2 → ~15 %, 2550-2800 0 → ~20 %), everything else
byte-identical to `launch_flow209.sh`, seeded from the winner of #1.

**Not covered.** §21 re-weighted the *same* boards by *outcome* (selection on the measurement) and was
negative; re-weighting by opponent **rating** is an exogenous covariate. §22 was seats, §23 same-band
boards, and the margin-scale A/B closed the fitness *shaping* (κ flat 0.00-0.016 at every scale), not
the opponent field.

**Cheapest falsifier BEFORE spending days.** The §84 SNR reader on flow209/flow210 at g30 (CPU,
minutes): if both sit on the momentum null (mean 0.51, p95 0.55) the optimiser carries no direction at
any field and **no third arm is warranted** — go to #1/#2 only. Only a > 0.60 read buys flow211 a card.

**Pre-registered bar (legs).** Net win flips ≥ +4 of 60 on LIVEC-H30 + H30B, ≥ 0 on NEXT30, TOPB2 not
worse than −1 win (TOPB2 demoted from clause to veto).

**Expected size.** ~**+80-150 Kaggle points** at the 298 pts/logit calibration if it clears; P(clears)
≤ 20 % given §59 (records lose in-sample) and §77 (two ES draws at B are orthogonal).

## (d) Do nothing new — run flow209/flow210, judge each 10-gen record, read the g30 SNR

Cost zero (both already running, GPU0/GPU1). But §60/§77 predict level records, and §79 records that
the recipe's own settling test **could not clear the block list** (the §73 blocks and the SWITCH0 cliff
subspace are indistinguishable under the only available label; gp and dh flip sign at σ 0.02). So the
premise of flow209/210 is unvalidated, and they answer the seed question and nothing else.
P(a record clears the 4-leg bar) ≈ 15 %, worth +50-150 points if it lands ⇒ **EV ≈ +10-25 points over
the remaining 12 days.** That is the floor, not a plan.

**Does anything beat it?** #1 and #2 do, decisively: they cost **no GPU**, run alongside the arms, and
repair the instrument that every remaining decision (including the arms' own records) is read through.
#3 does **not** beat (d) until the g30 SNR read says the arms carry a direction — if it reads noise,
the honest campaign for the last 12 days is #1 + #2 plus a decision about which of B/hr to breed, not
another arm.

---

## Claims I checked, and where

1. **Objective mass by opponent tier** — `S/flow209/launch_flow209.sh:140`: top-ten 37.2 %, 2300-2700
   30.6 %, 1900-2100 17.9 %; TOPB2 opponents are **2953-3081** (`:149`). Nothing at 2550-2900.
2. **Matchmaking has no tail** — `docs/strategy/2026-09-11-ladder-projection.md §1`: opponents drawn at
   own rating ± 45; B max opponent ever 2433, hr 2675; the 2800+ bin is *structurally empty*.
3. **Band gradient in the records** — last 13 `AUTOJUDGE-vsB` lines in `S/glut/verdicts.log`: TOPB2
   wins down in 12/13, LIVE62 wins up in 8/13 (flow206_g10, flow205_g10 at +6/−0).
4. **LIVE62 is held out of training** — `launch_flow209.sh:141` ("LIVE62 stays held out for the local
   judge"), so those gains are not in-sample; §59's in-sample decline is a separate measurement.
5. **Objective *shaping* is closed, the *field* is not** — `2026-09-11-margin-scale-AB.md`: κ 0.00-0.016
   at margin_scale 3000/30k/100k/linear, cos 0.83-0.91 between them; shaping decides ≤ 15 % of the step.
6. **Codex's "market-curve features use DEFAULT_MARKET_PARAMS, not observation" (§74 review 2) is
   VOID** — `src/kagg3/spec.py:371` + `es/archetypes.py:297`: `sample_market_params` is a *training*
   regulariser and "**the competition runs the defaults**", so the constants ARE the truth at inference.
   No experiment here. (§78 claim 4 refuted the rest of the observation class; it did not cover this.)
7. **Fertilizer** — `2026-09-11-leftover-audit.md`: leftover 47 coins/game, covers 0/48 loss margins;
   the +7.1k/game revenue gap is §57's family (margin +400-1,100 on every leg, **wins level**) = closed.
8. **Sell timing closed in both directions** — §89 (later pays, earlier does not), §90 (SELL21 hands the
   opponent +1,383, screen t −8.9), §91 (SELL5 engine +35/+44/+52, **0 flips in 320 paired games**).
9. **Lattice and decode closed** — §76 (0/24 radius-1/2 integer edits gain), §77 (pinned one-step
   κ 0.012-0.027, two draws orthogonal, cos 0.014 vs null 0.013), §80 (dither κ ≈ 0), §87 (LOTS +d never
   gains held-out).
10. **The gap is d15-29 and two-thirds of it is THEIR purse** — `2026-09-11-b-toptier-ledger.md §1-2`:
    d10-14 is a flat tax (win/loss swing +70), separation is d15-29; §55/§65/§68 show our sell book
    cannot move their late price against a fixed tape. This is why #1/#2 are measurement experiments,
    not another lever.
