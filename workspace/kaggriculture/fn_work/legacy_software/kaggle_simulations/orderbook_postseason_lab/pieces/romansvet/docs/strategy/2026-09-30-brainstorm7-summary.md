# BRAINSTORM7 session summary — round 3 (astra brainstorm16, 2026-09-30 10:02Z)

Session: round 1 = P48TAPE103 judge (docs/strategy/2026-09-30-brainstorm7.md); round 2 = astra brainstorm14 (wool-gate validity, first confirmation cell); interlude = astra brainstorm15 (executor gap split); round 3 = this summary over the whole 07:00Z-10:00Z stream log (memory project-streams-0927.md). Next session opens with the question in section 3. Prompt: scratchpad astra_bs16/prompt.md.

1) **0 candidates are upload-qualified at ~10:20Z.** Selection gate **15:00Z**, verified uploads target **17:00Z**, hard cutoff **18:00Z**. Preserve the existing pair unless a frozen replacement passes.
**56687235 / 56687774:** 224/224 games replayed exactly, zero errors/timeouts; terminal-deposit switch fired 0/224. Their different records reflect different opponent exposure.
**100% programmes in the top 39:** programme performance matters; the second upload’s 88/100 overall record does not establish programme strength.
**142 P48 tapes:** live baseline 39/142. Exact baseline reproduction establishes a replay anchor, not counterfactual fidelity.
**342 effective wool-gate flips across 42/103 games** invalidated RS2’s fixed-tape equivalence; recompute sales, inventory and downstream dependencies for both candidate and anchor.
**23/24 PQ4 games exact:** exclude or repair the mismatched game; this bank contains no direct MMPQ/DECEM/Victor matches. Deduplicate pooled games.
**P48 losses:** late L–W margin difference −26.6k, including our price loss −19.3k; reducing glut helps both purses. K16 own +4,156, rival +3,357, margin +798, t=0.39.
**PQ4 losses:** d10–14 melon-wave deficit −23.4k; late recovery +8.5k. This is not the P48 late-glut mechanism.
**0.804 → 0.805 → 0.847 → 0.904:** planner rulebook, direct executor, crew router, crewF4Sbc HOLD20 coin ratios. PFS itself scored **0.934** on the earlier MMPQ-seat comparison.
**0.904 coins / 0.787 fixed-price product value:** the latest body crosses one surrogate threshold; it has not recovered MMPQ execution or demonstrated superiority to PFS.
**328 versus 421 harvests/game; 136.8–137.8k revenue across crop mixes:** current bottleneck is productive work per labour unit. MMPQ performs ~176 actions +122 moves/day versus our ~155 +132.
**161 versus 160 wheat plantings, 148 versus 173 harvests, 3.91 versus 4.68 units/harvest:** survival and realized yield explain missing output; seed starvation does not.
**0.3 seed-starved tile-days/game:** seed hypothesis falsified. Death reduction 36.5→20.2 buys only +0.003 coin ratio; copying carrot/tomato allocation adds +0.008, t=1.2, while displacing wheat.
**bs15’s 148/80/66-unit allocation was provisional, not causal fact.** Later interventions show that restoring acreage, survival or one product can consume labour needed elsewhere.
**Closed for today:** sale timing (24/24 precadence cells negative; HOLD −742, t=−3.09), strawberry supply cuts, Q4 expansion (all nine cells lose), route replay, bundle dispatcher, seed/acreage/death/crop-mix fixes alone, gene descent and greedy TAPERL1.
**Still moving:** BC-led combinations, class-latched deployment, RS product/family repairs, unscreened switches and sampled-policy execution. No new broad reconstruction campaign is justified before selection.

2) **Ranked by chance of changing today’s pair.** Thresholds below are proposed selection gates, not achieved results; “kill” means no upload today, with the diagnosis retained.
**Common final gate:** frozen candidate versus frozen PFS on reacting V panels and valid programme/OTH panels; positive paired win-score gain with **95% lower bound >0**, resampled by board/tape, using weights fixed before results.
**V protection:** no paired win-score regression on either set; retain at least **37/40 and 12/21**, and any stronger contemporaneous PFS baseline. No other family loses **>5 percentage points**.
**Execution:** zero runtime/invalid-action failures, OFF identity and artifact reproducibility verified; pooled margin significance cannot rescue a failed family, HOLD or win-score gate.

**#1 — RSFIX1:** closest demonstrated effect: pooled 220 games **+878, t=2.52**, but net flips only **+1**, OTH own **−448**, TUNE wool **−4.47 u**, m40 milk **−2.9 u**.
**Upload-worthy:** repaired frozen cell has reactive HOLD t≥2, pooled t≥2, net flips≥+3, own≥0 on every set, and protected animal-unit deltas≥0, plus common gates. **Kill:** any residual own<0 or protected-unit delta<0, pooled t<2, or net flips<+3.

**#2 — TAPERL2 sampled head_940, T=0.5:** training-game signal **+405, t=2.39**; greedy HOLD was only **+62, t=0.49**.
**Upload-worthy:** predeclared three-seed reactive HOLD result t≥2 and net flips≥+2, OTH mean margin≥0, then common gates. **Kill:** HOLD t<2, flips<+2 or OTH<0; do not select the best random seed.

**#3 — HYBRID2:** strongest route to using a programme body without exposing V seats to its known weakness; the **0.904** body still needs to outperform PFS after the latch and bridge.
**Upload-worthy:** faithful latched seats pooled t≥2 and net flips≥+3, programme own≥0, unlatched V actions **100% identical**, plus common gates on the complete deployed policy.
**Kill:** t<2, flips<+3, programme own<0, any unlatched identity mismatch, or family loss>5 points. Include false-positive latches and transition costs; do not score only correctly classified successes.

**#4 — SWITCHSWEEP1R:** **83 default-OFF switches**, with 39 screened earlier and none above t=2; this remains discovery, not confirmation.
**Upload-worthy:** freeze one survivor before independent confirmation; pooled reactive t≥2, own≥0, net flips≥+3, then common gates. **Kill:** confirmation t<2, own<0 or flips<+3; a selected screen t≥2 alone qualifies nothing.

**#5 — standalone 0.904 body:** the 0.847 body scored **0/40, −36.0k; 0/21, −31.2k** against reacting V. Extrapolation is not the pending 0.904 result.
**Upload-worthy:** actual reacting results meet common gates, including ≥37/40 and ≥12/21 without paired regression. **Kill:** either V set fails. A 0.904 fidelity ratio cannot override that; programme-only success routes to HYBRID2.

**#6 — CREWBC1 lam3:** previous BC body **0.885 coins / 0.790 value**; removing the build guard reached wheat 676 but collapsed eggs to 32.
**Panel-worthy:** HOLD20 coins and fixed-price value both≥0.90, with the complete product vector. **Upload-worthy:** common gates, or the HYBRID2 gates for latched deployment.
**Kill standalone reconstruction at noon:** either ratio<0.90 without already demonstrated competitive-panel gains; any final panel failure kills upload. Preserve useful BC components for the frozen combination.

**15:00Z freezes selection.** TAPERL2’s 16:15 runtime allowance does not authorize choosing a newly discovered checkpoint after the gate; remaining time validates and packages selected artifacts.

3) **One opening question:** “Which frozen deployable artifact has now improved paired win score over PFS on a valid reacting panel, with its 95% lower bound above zero and every family guard intact?”

4) **Oct 1–15 — five-line plan:**
**1.** Freeze eligible uploads; monitor their evaluation games by programme family, opponent version and draw. Post-cutoff builds cannot replace the eligible pair.
**2.** Build a validated reactive programme environment: P48 wool inventory/gate dynamics, PQ4 schedules, versioned tape banks and separate unseen-board/opponent holdouts.
**3.** Build a state-conditioned crew learner optimizing productive work per labour unit; measure complete product vectors, travel, missed deadlines and harvest realization.
**4.** Scale all-class best-response training beyond 576 games toward the proposed ~50k-game budget; compare greedy, sampled and class-latched policies under identical reacting opponents.
**5.** Maintain a frozen paired-win benchmark reflecting the programme-dominated field, with uncertainty by board, opponent-version drift and reproducible shadow artifacts.