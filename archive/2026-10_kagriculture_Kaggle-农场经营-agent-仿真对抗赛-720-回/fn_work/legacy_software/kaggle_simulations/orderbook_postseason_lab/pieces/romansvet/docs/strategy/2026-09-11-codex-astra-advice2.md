# Codex (gpt-6-astra) follow-up advice — 2026-09-11T17:50Z

**Prioritize a clean pinned-training pilot if it passes; otherwise switch to direct policy edits. Stop allocating substantial compute to selling variants.** The pasture-reservation defect is actionable, but its correction and the training experiment need separate attribution.

1. **If PASS: train a constrained, auditable pilot.**

   Pin the same 12 coarse fields to B’s decode **on the current observation**; free only the tested 30 coin-scaled fields. Freeze the reference decoder and reservation-fix version. If the fix changes behavior, establish its paired-engine baseline and repeat the gradient check there before extrapolating the old PASS.

   Keep sigmoid(margin/3000), rank normalization, and CRN initially: changing objectives now confounds the test. Use independent direction batches across generations and balance seats and tape families. Choose an initial step supported by the successful directional readout; do not automatically restore the old Adam step.

   Pre-register paired-engine reads at generations 5 and 10 against the frozen starting policy. Continue to 20 only if training-panel improvement transfers to a separate development panel; reserve confirmation for one selected finalist. Judge promotion by paired win changes, with margins diagnostic.

   Refuse unpinning, simultaneous objective changes, or long runs justified by simulator fitness alone. **Biggest failure:** a reproducible local gradient exploits particular tapes/shop paths and disappears on independent engine boards. A one-step PASS establishes a direction, not a durable optimization regime.

2. **If FAIL: first test whether pinning actually removed disruptive action changes.**

   “NO-GO ⇒ ties were not binding” is too strong. Thirty integer outputs remain free, and later affordability, ranking, and scheduling thresholds can still dominate. Inspect existing perturbation traces: count changed decoded fields and locate first action divergence. Then test a few single-field offsets. Useful isolated edits alongside failed joint perturbations implicate search geometry.

   Rank the remaining falsifiers:

   - **Shop-path divergence:** use existing paired traces to separate pairs before/after their empty-tile counts diverge. Re-evaluate a frozen action-changing candidate on several independent valid towns/seeds. Stable improvement across changed shop paths weakens this explanation; first divergence alone proves nothing. Do not freeze draws contrary to engine rules.
   - **Seat cancellation:** split existing directional effects by seat and tape family. Consistent opposite signs justify seat-conditioned controls, if seat is observable. Same-sign effects weaken cancellation.
   - **Fixed-panel dependence:** repeat one frozen direction on disjoint valid boards. Loss or reversal falsifies transfer from that panel.
   - **Objective mismatch:** reweight existing perturbation outcomes using sigmoid margin, raw win changes, and near-zero-margin emphasis; compare resulting directions on the same independent engine panel. Wins being flat while margins move establishes mismatch for those edits, not a useful win gradient.

3. **Direct integer search: prefer a small context-conditioned policy search to 6,789-gene ES.**

   Forty-two outputs do **not** mean 42 global decisions: they are recomputed across observations and interact through legality and downstream state.

   **Day 1:** expose 6–10 interpretable controls as offsets or overrides to B’s decoded policy: affordable pasture reservation, one staffing date/count, one planting allocation, and selected cash thresholds. Use fixed observable conditions. Test ±1 for counts/days and economically meaningful steps for coin fields. Apply feasibility checks after edits.

   **Day 2:** screen coordinates on a balanced development panel. Retain at most three candidates; test combinations only where individual effects or traces support an interaction. Expand survivors across boards before expanding the beam.

   **Day 3:** freeze one finalist and run paired-engine confirmation, both seats, with mid-tier regression checks. Bound candidate count before starting; spend most engine budget resolving finalists.

   Split by opponent/tape identity and town, not seat alone. Previously examined tapes are development data. Seek fresh valid tapes/towns or executable opponents; without them, report limited generalization evidence. Never add tape IDs or unavailable future features to the policy.

4. **Retire late-price denial as the main thesis; allow one diagnostic for another mechanism.**

   Production matching could supply substantially more of the opponent’s exposed commodity; earlier capital pressure could change their later inventory or sale schedule. Both require an actionable exposure or affordability threshold in traces. Existing pump and production-family failures lower their priority.

   Before building, identify one concrete intervention capable of changing meaningful opponent volume, capital, or timing. If none exists, close this branch. Merely reshuffling shops creates an outcome change, not an expected advantage.

   Prioritize increasing **our** terminal coins on near-loss boards. The melon-window deficit remains relevant despite being flat across wins/losses: an affordable recovery can flip games. Reopen it only for a specific schedule not already tested.

5. **Use Elo arithmetic to set ambition, not to extrapolate mid-tier results.**

   Against a fixed opponent distribution, +250 Elo multiplies win odds by approximately **4.22**:

   | Starting win rate | Required after +250 Elo |
   |---|---:|
   | 32.5% | 67.0% |
   | 63% | 87.8% |
   | 83% | 95.4% |

   These are alternative reference populations, not additive gains. Improving already-winning mid-tier margins gives no direct Elo benefit. Flipping mid-tier losses helps climbing, but approaching 3000 requires performance against the opponents encountered there. Current upward drift is not equilibrium strength.

6. **Correct the inference chain.**

   The census explains why broad perturbations are destructive; it does not prove every ES estimator has zero signal. Recentring failure rejects that intervention, not all behavioral stabilization. Late opponent price remains a correlate, not an established causal discriminator. Zero flips supports closing these tested levers under the deadline; it does not prove zero population benefit. Finally, engine-exact coin agreement has already failed to guarantee transferable win rankings: preserve real-engine confirmation throughout.
---
## Delta brief
# Follow-up brief (2026-09-11 ~17:50Z) — read brief.md first (the original state), then this delta. Your earlier answer is in astra_answer.md.

## What happened since (all paired real-engine unless noted)
1. YOUR direction 1 (opponent-aware selling): built as OPP_FRONTRUN (intraday order + overnight hold vs their fixed late rows; front-running their rows is impossible — 449/450 tape-days open with their SELL at h0-2 before our first turn; but 45 % of their units land at h18-23 after our lot 3, and the market stock is monotone with no intraday recovery, so ORDER is the lever). Engine vs B: margin +250 on both mid-tier hold-outs (t 1.6-1.7), LIVE62 −365 (t −3.4, our purse fell more than theirs), pooled mid-tier WINS 44/60 → 44/60 (zero flips), their d15-29 price/unit fell 0.5-0.8 of a 16 c/u target, and on B's LOSS boards our purse fell more than theirs. Half dose: monotone, smaller. Verdict LEVEL/closed. Every attempt to move their late price through our sell book (shrink lots, time lots, hold overnight) has now failed with the same signature: margin up, wins level.
2. YOUR direction 2 (audit the switch) — done and it was an implementation defect, as you suspected: brain.py `animal_count = floor(animal_share*n_dev)` sits at 6.9913 vs the 6.9999 boundary at B. A perturbed theta that WANTS a 7th animal (never bought: unaffordable that day; herd identical every day) makes `_seed_room` reserve a pasture tile before the purse prices anything, which evicts the 11th day-0 WHEAT tile (planted 19→18, +10 coins kept) — worth −1,774 coins/board on the top tier by day 29 (28/40 games), coin flip on the mid tier. Confirmed on 12 boards across both families. Recentring B was REFUTED: B sits in a cell only 0.012-0.02 wide bounded by many such floor ties; a recentred B plays at 5 % win. A purse-aware `_seed_room` fix (reserve pasture only for affordable animals) is being built and screened now.
3. TIE CENSUS at B: 68 discretisations in the theta→plan decode (55 floor entries, 5 absorb thresholds, 8 argsort keys). 46 lie within σ=0.02 of B. At σ 0.02 each ES population member flips ~34 floor cells; 0 of 64 members decode B's plan (0/64 at σ 0.005 too). ~60 decisions/game ⇒ ~10³ cell draws behind one fitness number. This is why the ES is a noise walk (records lose even on their own training rungs) and why the one-step gradient test reads a coin. The entire theta→plan interface ("Macro") is 42 integers; 12 coarse fields (tiles/hands/days, 429 genes) vs 30 coin-scaled fields (6,360 genes).
4. PINNED MODE: a decode mode KAGG3_PIN_INTS that holds the 12 coarse integer fields at B's decoded values (recomputed on the same observation, so counts track the board) while the 30 coin-scaled fields stay free. Verified inert when unset. A pinned one-step antisymmetric gradient test at B (σ 0.02, pop 512/2048, directions restricted to the free subspace, 8 random + 4 permuted-advantage controls, engine-exact read-out at α 0.1/0.03) is RUNNING on the local GPU now (~2 h). Pre-registered: PASS = κ ≥ 0.03 and +d beats both control families on both tape families; NO-GO ⇒ ties were not the binding constraint.
5. lr 3e-4 re-cuts of the two remote arms (B-seeded control; fresh top-tier rungs) launched 17:33Z as the direct test of "does the in-sample decline stop"; expectation from the census: still a cell lottery, level at best.
6. Kaggle: B 79W-25L 2461 and climbing ~+5/game; hr 150W-64L 2615. Cutoff 2967, rank 5 3003. 12 days left.

## Ask
Given 1-5, advise:
(a) If the pinned one-step test PASSES: how to turn it into a training run that can be judged (what to pin, what objective, how many gens before a paired read, what would you refuse), and the biggest failure mode.
(b) If it FAILS: what is the next binding constraint to test (shop re-roll noise, seat, fitness = sigmoid margin vs wins, evaluation on fixed seeds) and the cheapest falsifier for each.
(c) The 42 integer decisions themselves: since the plan is really 42 integers per day-context, is a DIRECT search over those integers (coordinate/beam search, engine-judged, board-panel) better than ES over 6,789 genes? How would you structure it in 2-3 days of compute, and how would you keep it from overfitting the 50 pinned tapes?
(d) The top-tier discriminator (their late price) is unreachable via our sell book. What ELSE could reach it, or should we stop trying and instead widen the mid-tier margin where B already wins 63-83 %? What is the Elo arithmetic for each?
(e) Anything in our chain of inference that looks wrong.
Be concrete and ranked; ≤900 words.
