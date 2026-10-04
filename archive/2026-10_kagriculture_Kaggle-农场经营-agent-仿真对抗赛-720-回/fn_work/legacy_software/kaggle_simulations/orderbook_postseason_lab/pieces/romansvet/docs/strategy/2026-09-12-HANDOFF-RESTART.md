# Restart handoff — live relative-J training and conditional H continuation

**September 14, 08:25 UTC — TOPB3 leg cut (docs/strategy/2026-09-14-topb3-leg.md, S/topb3/):**
18 pinned-town tapes (6 each Majkel1337 56156662, ymg_aq 56209769, DSM 56204618; all recent
wins vs 2900+, 36/36 bit-exact verify, 0 id collisions). DEFECT: 11/18 tapes DESYNC vs B —
retention (tape coins in our leg ÷ source episode) Majkel 0.25, DSM 0.65, ymg_aq 1.02;
NEXTHIGH control 0.99 → hire-heavy builds lose hand alignment after a refused HIRE (every
later action with a longer hands list becomes illegal). B baseline S/lossflip/topb3_B.csv:
all 18 = +43,057 (contaminated, do not quote); RETAINED 7 boards: B 0-14, −12,599/board
(t −5.54; ymg_aq 0-12 at −13,751, DSM 0-2 at −5,682). B vs Majkel1337 UNMEASURED.
Judge: WORKERS=4 bash S/topb3/run.sh <name> <worktree> <theta> "<hr switches>" then
S/topb3/retention.py. Not registered (inventory_entry.json is a proposal). Streams
launched: TAPE-FIX (hire-robust tape seat) and LEDGER-TOP5 (per-product ledger of the
−12.6k on the 7 retained boards). master ff-merge pending a git index lock held by a
subagent's git log on drvfs.

**September 14, 08:24 UTC — MELON-M mechanism (docs/strategy/2026-09-14-melon-animal-mechanism.md, S/melon_mech/) → MELON CLOSED:**
Decode coupling REFUTED (plant_target/animal_want identical d0 across B/M4/M12). The herd
is lost on DAY 0 by COINS: melon seed 80/tile vs carrot 20 / wheat 10; M12 = +760 seed,
−900 herd (one COW + one SHEEP), M4 = +240/−500 (one SHEEP), purse identity closes to the
coin (flat dawn cash = the unspent herd money, so "starvation refuted" was substitution).
budget.grant walks seeds and animals in ONE value-per-coin vector (plan.py:4696-4741,
:5426, :5361): 12 melon seeds outrank a 500-coin sheep; remaining animal rows are refused
by the engine market (seed rows precede animal rows, :7677/:7816). SHEEP dies first
because GOOSE→COW→SHEEP share one budget (BEFORE_ALL :4168). d1-d9 = cash drought
(melon pays nothing before d10; M12 dawn d7-9 250/501/441 vs 744/1,995/1,288 → zero
animal rows despite MORE free tiles); quad 2 slips d5→d6 and refuses the d6 COW.
A non-displacing DAY-0 plate is structurally impossible (one purse, one greedy walk,
no melon-vs-sheep gene; land_bias cannot fund it: 1,000+960 of 3,000 vs a 2,400 herd).
MELON RESOLUTION (four legs, all consistent): the d10 pot (+3k gross) cannot be taken by
our seat without paying ~2k/tile in herd, whose d15-29 price denial is worth 21-27k.
Melon is CLOSED as a lever; B's d9 melon (from d5-10 wheat cash) is the correct timing
for our design. The lever is the animal/denial line (HERD screen in flight).

**September 14, 08:15 UTC — end-game defects census (docs/strategy/2026-09-14-endgame-defects.md, S/endgame/):**
40 LIVE-C boards, sim probe with B. Animal escapes 40/40 boards, mean 5.8, 79 % on d27-28:
NOT a defect — feed_pass = feed_value > feed_price (plan.py:5132-5139), survival_pays =
day < pay_day (4952), pinned by tests/test_feed_value.py; on the loss board feeding cost
~129 to save ~3. Unsold end-state 40/40, mean 426 coins: standing crops 385 (labour limit,
MIDDAY_DROP post-mortem −1,157 → not proposed) + fertilizer 6.8 u (OP_COLLECT_FERT output
never offered on d29, plan.py:6654/6737) ≈ +41 coins/board with TERMINAL_FERT_ROW_ON.
VERDICT: no lever here (+41/board vs a 4,600 gap); park TERMINAL_FERT_ROW_ON for a bundle.

**September 14, 08:05 UTC — MELON-R reachability (docs/strategy/2026-09-14-melon-reachability.md):**
Day-0 melon = _largest_remainder(softmax(crop_logits + clip(crop_mix))) (brain.py:1083);
crop_mix = gh@cm + cb is the only zero-init crop block. At B the first melon tile costs
+2.05 nats of melon bias (+5.71 for 12); one ES draw at sigma 0.01 sits 71 sd away on
cm,cb (168 sd on cb alone) → early melon is UNREACHABLE at training sigma; only w1/w2/dh
reach it at sigma ≥ 0.05 (the lr/sigma cliff). DRAIN_CLIP and can_mature are NOT the
blocker; day 1 is not an entry point; cash is not. New default-OFF switch
brain.MELON_GENE_ON + CROP_MIX_GAIN 256 (brain.py:776-802, :1009-1013): B byte-identical
OFF and ON at zero gene; slope z=+0.01 → 1/1/8/2/16 tiles, +0.02 → 8/8/18/13/21 on 5 dawns.
tests/test_melon_gene.py (5) PASS; 6 failures in test_melon_open/test_crew_and_herd_mix are
pre-existing (verified by stash). PRECEDENT: the crop_mix W00/W01 campaigns (09-13/14) already
trained cm/cb at sigma 0.5 / lr 3.6 (equivalent reach: 302-316/4096 first-population melon
changes) and BOTH were REJECTED on all seven families → a learned crop mix at 10 gens did
not beat B even when reachable. MELON VERDICT (three legs): (1) the pot is worth +3k gross,
(2) every early-melon tile costs ~2k via animal-line collapse, (3) a reachable learned mix
found nothing. Remaining melon question = MELON-M: WHY do sheep/cows collapse with 4-12
melon tiles when cash is equal (decode coupling vs route/crew budget); if fixable, a
non-displacing melon exists, else melon is CLOSED and the animal/denial line is the lever.

**September 14, 08:00 UTC — MELON-D decomposition (docs/strategy/2026-09-14-melon-decomposition.md, S/melon_decomp/):**
68 pinned boards (40 TOPB2 + 28 LIVE-C), CRN sim, arm B reproduces topb2_40.csv to the coin.
Forced melon vs B: M4 −9,100 (20.6 %), M8 −16,826, M12 −23,517 (t −19.8), M12+LOT_EARLY
−23,610, M12+MIDDAY_PLACE −28,163 → ≈ −2,000/tile, linear. Decomposition of M12:
(a) DISPLACEMENT −26,647 = our non-melon revenue −5,491 + PRICE HANDED TO THE CLONE +21,156
(strawberry +7,680, milk +7,533, wool +3,062, fertilizer +2,160; 95 % in d15-29; their
units fixed by tape). (b) melon race WON +3,016 (our melon +1,405 at 178/u vs their 234,
denial +1,611). (c) cash starvation d0-5 ≈ 0 → REFUTED. Animal line at d10: COW 6.15→3.32,
SHEEP 3.26→0.06, GOOSE 1.71→0.84; sheep collapse even at 4 tiles = tile/route budget
d0-d10. Melon ceiling ≈ +3.0k gross vs 26.6k of animal/denial lines it must not touch.
RESOLUTION: the d10 melon pot is NOT the lever for our seat; the animal/denial line
(milk, wool, fertilizer price d15-29) is worth 7× more and is where the top-tier engine
class plays. Forced-plate and additive melon arms CLOSED; MELON-R decides only whether
the ES can express early melon (so training, not a hand rule, keeps it low or finds a
non-displacing variant).

**September 14, 07:59 UTC — E-A FALSIFIED: flow193 curve is flat-then-jump (docs/strategy/2026-09-14-flow193-curve.md):**
Host ~/stage_hr/artifacts/flow193/cands has only g0/g10/g100/g200/g300 (ES made 3 in-sim
records in 300 gens, none after g100). Pooled band vs seed flow187_g160: g10 −307 (t −1.13),
g100 +412 (t 1.51), g200 −292, g300 −108; TOPB2 −758/+292/−1,185/−915. cos(θ−seed, B−seed)
= +1.00 at g10, −0.02 at g200, 0.00 at g300 → random walk; B's edge over its seed never met
§115. The remote gate ALSO refused g100 (win metric, min_flips 5, margin-blind); B shipped
only because the watcher judged the record locally. So the 10-gen stop rule is not the
defect and 100-gen seat draws (E-A) are a lottery ticket → NOT launched. flow193_g200_hr /
g300_hr staged locally. The ES lineage cannot be the vehicle until the decoder can
express the missing behaviour (melon opening, sell cadence) → MELON-R/MELON-D govern.

**September 14, 07:39 UTC — census + top-five profile landed; three streams launched:**
docs/strategy/2026-09-14-open-lever-census.md: B's accepted step ‖flow193_g100−flow187_g160‖
= 2.435 vs 0.014-0.016 per 10 gens for every arm since 09-12; flow193 itself read
level/negative at g10 and was refused by the remote gate (S/glut/verdicts.log:300) yet
shipped at g100 → the 10-gen stop rule would have killed B's own lineage (E-A). Ranked
open: 100-gen draws from the flow187_g160 seat judged at g100; trained-in market-row
cadence (78 % of top-tier market coin on turns we cannot emit); learned shop-conditional
response; a 2953+ engine-class judge leg (no leg covers 2750-2950). FORWARD_ADMIT is
engine-closed 4× (−9,224 t −6.7); additive melon unbuilt and argued against.
docs/strategy/2026-09-14-top5-profile.md: top five = Majkel1337 3204, SpaTaro 3021,
ymg_aq 3013, DSM 3011, Mengfei Li 2997; rank-10 cut 2965. Only SpaTaro/Mengfei have
pinned tapes (TOPB2); B +2,621/board vs SpaTaro, −2,628 vs Mengfei; TOPB2 32.5 % is the
binding constraint; ≈ +2,500 coins/board vs 2953+ needed. Recommend TOPB3 tapes for
Majkel/ymg_aq/DSM (episode lists in S/ladder2/top5_20260914/).
GOAL.md rule: strategy learned from outcomes, no hand-written strategy → the melon
resolution must be REACHABILITY (can the ES express/reach a day-0 melon opening and
d10 sell cadence?), not a hand switch. Streams: MELON-R (decoder reachability + gene
slope fix), MELON-D (sim decomposition of existing MELON_OPEN switches, diagnostic
only), E-A falsifier (judge flow193 g30/g60 checkpoints if they survive on the host).

**September 14, 07:38 UTC — close loss 108806196 reviewed (docs/strategy/2026-09-14-episode-108806196-close-loss.md):**
Exact reconstruction (market error 0, cash identity residual 0, script
S/unitorder/early_gap_108806196.py). Opponent 56220308 = band clone on the opening
(12 MELON d0h7, 72 u / 17,440 from d10h9) with 413 sell rows vs B's 135. Receipts
B −3,255, spend B −1,980 → final −1,275. Bands: d0-9 +520, d10-14 −22,148, d15-29
+18,373: the melon pot is a TIMING TAX B recovers 83 % of. Residual margin = animal
products −14,236 (FERT −11,322, MILK −7,326) vs crops +10,981. B mechanical defects:
3 sheep STARVED d28h23; ~687 coins unsold end-state (14 wheat + 5 fertilizer); idle
hand-turns 10.1 % vs 6.8 %; all 60 melon sold into the glut at ≤ base (223 at d20).
One outcome-selected board, no counterfactual. USER DIRECTIVE September 14, 07:38 UTC: resolve
the melon problem to move forward → melon decomposition build launched (below).

**September 14, 07:29 UTC — J FINAL JUDGES TERMINAL: both seeds REJECTED; H continuation NOT launched:**
Final queue session 76790 completed at 07:09:57 UTC (receipt
S/unitorder/momentum_relative_joint_campaign_20260914/final_continuation/receipt.json,
status COMPLETE, both seeds STANDARD_JUDGE_COMPLETE, all audits PASS, remote/local
audits byte-equal). Seven-family paired margins vs B (coins/board, t):
J311 TOPB2 -316 (-0.69) W0 L1; LIVEC-H30 -445 (-1.73); LIVEC-H30B +170 (+0.52);
LIVE62 -225 (-0.82) W4 L0; LOSS10 -593 (-1.22) W3 L0; NEXT30 -84 (-0.48) W1 L1;
NEXTHIGH +8 (+0.03).
J312 TOPB2 -459 (-1.08) W0 L1; LIVEC-H30 -409 (-1.52); LIVEC-H30B +119 (+0.37);
LIVE62 -199 (-0.72) W4 L0; LOSS10 -593 (-1.22) W3 L0; NEXT30 -77 (-0.42) W1 L1;
NEXTHIGH +10 (+0.04).
Neither seed approaches the §115 bar (pooled band ≥ +450, t ≥ 2); the two seeds
agree, so this is not a seed lottery. H generation-10 lines were already negative on
all seven families (NEXTHIGH -575/-599 t -1.7; LOSS10 -926). DECISION: the prepared
H generation 11-20 continuation is NOT launched (no evidence the momentum family
gains at either objective); the judge-registration patch stays unapplied. The
momentum H/J family is CLOSED for promotion. Remote GPUs 0/1 idle at 07:24 UTC.
Sol crop_learning_review of loss 108806196 delivered no report; re-dispatched.
Production remains B sub 56161192 (rank 165, 2767 at 06:11 UTC; fifth 2997).

**September 14, 06:15 UTC — fresh public snapshot; J final generation still live:**
Original J controllers/trainers were process-verified06:10:31UTC with both logs
at9/10 completed. Original queue session76790 continues successful live-controller
observations; no terminal result or new judge yet. Do not restart or duplicate.

Public snapshot S/ladder2/snapshot_20260914T0611Z completed three paced200 reads.
B rank165,score2767.3,270wins/415completed games,0ties; fifth2996.6. Since0536:
three new completed games,2wins/1loss, all unchanged-B outcomes. Jlaunch embeds
snapshot hashes, summary and the new loss acquisition receipt.
New loss108806196: Bseat0/sub56161192 scores109016 vs opponentseat1/sub56220308,
team16670524 "Nat Bel ML Fun",110291. ReplaySHA
7b18505ed1358094d5bacc0bc4417d74deb11d701d63c4cedc66a7007b7da6ff,
path snapshot_20260914T0611Z/ep_108806196_replay.json (32,247,707bytes).
Only one same-team match in current B snapshot; exact episode absent both W00/W01.
This establishes new identity, not a missing strategy. Sol crop_learning_review
is RUNNING a20–30minute read-only replay review of timing/accepted sales/allocation
and late cash conversion. Root supplied identity check. No tape additions or new
benchmark; final J win results still govern the next training decision.

**September 14, 06:09 UTC — J continuation contingency reviewed, not selected:**
Original J controllers/trainers remain live and campaign/seed-matched at2026-09-14T06:09:09.704190+00:00.
Completed generations:311=8/10,312=9/10. Original final queue
session76790 remains responsible for collection/audits and both standard judges.

Jlaunch.full_state_continuation_contingency embeds the root-reviewed Sol report
SHA39b57c792f2d3438430479032a7bdbd615810a66a2c6546645b1abbdf73b3189.
No J continuation profile/code/campaign was created. If final J results warrant
continuation, generalize the existing four H wrapper/auditor helpers by closed
arm/profile dispatch; native staged trainer needs no change. Preserve J's196
active indices2368:2498+6789:6855, exact full parent state and only the three
allowed child-config changes(run/resume/init_theta). Do not copy incidental H
parent scalars such as last_improve==10 into J assertions. Full terminal/local
parent audits and both completed final judges remain prerequisites to selection.
Root verified current helper hashes and J's exact mask against its manifest.

Existing J release preparation already supports the120-dawn actual-history
NumPy/GPU macro/day-plan check and generic package verifier (prior37b3e43).
Do not repeat the old parity-label fix or substitute the history-free2400-case
fixture as proof of trained momentum behavior. No candidate release run yet.

**September 14, 06:00 UTC — training efficiency review; original J remains live:**
At05:58:02UTC original controllers1336928/1336929 and trainers1341262/1341251
were process-verified with matching campaign/seed. J311 completed7/10; J312
completed8/10. Original final queue session76790 remains live and owns final
collection/audits/sequential standard judges. No restart or additional run.

Root exact sealed-array census is embedded in Hlaunch.sealed_tape_array_identity,
artifactSHA0190c88880872a5604f06f6c9cefc2e8bf179049a095d030c5878c7657330d75.
Both W00/W01 have118 unique whole-season command tables but120 unique town
schedules and120 commands/town/hours combinations. Day0 has29/24 unique tables.
Matching openings do not establish lossless full-episode duplication; raw-array
identity also does not measure strategic diversity or accepted effects. Keep
all sealed tapes and full-season rollouts.

Sol population/update-budget review supports retaining the prepared population4096
H continuation conditionally on final J outcomes. Fresh1024x40 is not an equivalent
optimizer trajectory to4096x10: different rank groups, EMA warm-up, four measurement
cadences, and3.23% extra padded main rows. Relative win benefit remains unmeasured;
no automatic learning-rate/sigma adjustment or population change selected.
Root verified chunk/cadence code, native H timing arithmetic, and constant-gradient
EMA algebra; these are cost/mechanism evidence, not strength measurements.
Corrected report embedded in Hlaunch.population_update_budget_review, SHA
cf0b3d05ac276c3f44bd0244733a92cfac23f26cbffdb9d05cfe877a37360729.
No H launcher or deferred judge patch has been executed. Earlier launch conditions
and pinned J judge-helper source remain in force.

**September 14, 05:49 UTC — J generation 6 verified; H continuation installed, not launched:**
Current branch `feature/h-checkpoint-continuation`. Implementation commit7502f00;
sealed campaign/install5e69aa0; execution preparation987abde; latest research0328020.
Goal remains top five, not achieved. Production is still B submission56161192.

Original J controllers1336928/1336929 and trainers1341262/1341251 were verified
live with matching campaign/seed at05:45:29UTC; both completed generation6/10.
Native steady generation times623/610seconds. Final queue remains original
session76790/PID13295, with repeated successful live-controller observations.
Do not restart or duplicate any of these jobs. The four existing root judge
helpers remain pinned until BOTH original J standard judges are terminal.
The authoritative latest observation and exact read-only poll source are in
`S/unitorder/momentum_relative_joint_campaign_20260914/launch.json`.

Conditional H continuation is now implemented, tested, committed and installed:
`S/unitorder/momentum_h_continuation_campaign_20260914/manifest.json`, SHA
`91e7a1490a7eb343544f57803fb95a6e70e7658f81c4ef5fdf8d20da4b00f19f`.
The manifest binds189 inputs; its190-member bundle is1,925,145bytes, SHA
`a20620b3fcc78191b9138f97bcd84864d3d0a79241c35b5310b7a2cb8ea0ed6f`.
Local sealed project is campaign/project; remote root is
`/home/user/kagg3/artifacts/momentum_h_continuation_campaign_20260914`.
All input validation passed on both hosts. No H qualifier/trainer has run.
Transfer was covered by the user's standing approval for all training bundles.

Use each H seed's exact full generation10 state, restoring optimizer momentum,
both RNG streams, pool/ladder and schedules. `--gens 10` means ADDITIONAL steps,
so this segment runs11..20. Only run/resume/init_theta differ from original
portable parent config. Same frozen43-file source, W00 tapes, H130 coordinates,
sigma.01/lr.00018/SGD/pure-relative objective and assigned GPU per seed.
The existing helpers now support a closed resume profile, two probe calls,
qualification stopping before update11, parent-state/noise matching, and
snapshots11/20. Typed restored JAX keys are serialized via key_data. The focused
existing training-helper test file passed; no native trainer/source was edited.

Hlaunch contains independently reviewed, NOT EXECUTED controller/launcher and
qual-before-train collection/local-audit sources. It also embeds the reviewed
NOT APPLIED judge integration patch and its source prerequisites. J-terminal
and outcome-based experiment selection remain ROOT-OWNED launch conditions;
the detached launcher checks idle GPUs/fresh paths, not J result selection.
After both J judges finish, decide whether J wins favor continuing J or the
prepared H continuation. Do not launch H solely because its bundle is ready.
If selected, apply/test the prepared exact H-g20 registration only after J is
terminal; use unchanged seven-family final-centre wins versus B, separate seeds
and families. No extra controls, benchmark, pooling or automatic promotion.

New source-backed findings are embedded in Hlaunch:
- ES scaling audit found no denominator/mask bug. Root reconstructed saved
  H generation1 updates exactly and verified delta/momentum arrays. Uncorrected
  SGD EMA warm-up is intended; full-state continuation preserves it. Constant-
  gradient2.923x cumulative motion at20 vs10 is an algebraic illustration,
  NOT a predicted win gain. No sigma/lr/estimator change selected.
- Public snapshot `S/ladder2/snapshot_20260914T0536Z` has B rank166,score2763.1,
  268wins/412games; fifth2993.7. Eight new games5W3L are unchanged-B evidence.
  New losses108795103/108789953/108787343 were acquired and reviewed. Root
  directly verified accepted early melon plants and inventory-accounted sales.
- Senkin's same submission executes identical12 day0 melon plants and72 early
  sold units from both seats. Xiangyu plants14 melons on days4-6, sells84 later.
  No new mechanical bug established. More observed crop cycles and earlier
  melon sales repeat known gaps; these observations do not prove causation.
- A direct sealed-tape command census resolves the team-name coverage gap:
  W00 has119/120 day0 melon tapes (118 exactly12 commands); W01 has120/120
  (119 exactly12). Early selling is similarly dense. These are SUBMITTED
  commands, not proven accepted effects. Only108160352 has day4-6 melon
  commands in either set. No loss-selected tape additions are recommended.

H312's earlier release package is still ready but NOT uploaded; the prior
Kaggle-auth/manual-upload request remains unanswered. Do not repeat auth polls
or code requests while other authorized research/training is progressing.

Historical checkpoints below are retained; this entry supersedes their state.

**September 14, 05:07 UTC — J final queue live; W01 review finalized:**
J final continuation started once05:06:39UTC, original session76790/PID13295.
Receipt RUNNING confirms both original J controllers1336928/1336929 live and
identity-matched in TRAINING. Queue owns qual-before-train collection/local
audits and sequential unchanged7-family judges after original controllers
terminate PASS. Do not duplicate/restart it. SourceSHA828377b9eb9bfa7e15834965074cedfcc7fc7fc49657cc861326ec620c8b7445;
exact source and original handles in Jlaunch.automatic_final_continuation.
The FOUR CURRENT root judge helper hashes in Jlaunch.judge_integration are
now pinned until BOTH J standard judges terminal. Do not edit those helpers.

W01 original session98544 is terminal exit0/COMPLETE; both candidates rejected.
Sol final review (all seven expected family/key sets, outcome transitions,
per-seed W00 comparison) is embedded and root-checked in W01launch.final_judge_review.
ReportSHA3be4b081f49d733b9f20f0bf0384e7435476d40b693c98c24d9fd4f42312e0a4.
No outcome ties; ident means exact margin-delta zero, a different statistic.
Both seeds improve only LOSS10 net; broad families regress. No arbitrary
further crop tape rotations selected. Resume-state review for conditional H
continuation has arrived in /tmp/h_resume_state_contract_review_20260914.md
(SHAcef231f791c4d12dbf2003b2ad028be1ffe09a9544b2930f9339d253b263cdb5)
and awaits root review; no new continuation recipe/code/run prepared yet.


**September 14, 05:06 UTC — W01 both rejected; J judge integration passes:**
Original W01 final queue98544 exited0 with COMPLETE/313+314/no failures.
C313 saved audit PASS SHA0dda097575eeb8b58e3a41ee1093560ca098a81ef3c06a02e35a06065e2155bc.
Root verified both finalthetas and all7 candidate/base CSV hashes per seed.
C313 strict flips gained/lost: TOPB2 0/5,H30 0/7,H30B 0/7,LIVE62 2/17,
LOSS10 2/1,NEXT30 0/5,NEXTHIGH 0/8. C314 results below. Each candidate
rejected individually; no pooled score. W01launch now COMPLETE_STANDARD_JUDGES_REJECTED.

After W01 termination, applied the exact prepared relative-J registration
patch. All4 helper hashes equal reviewed post-patch identities;13 focused
cases passed, session61116 exit0. Existing7 families unchanged; no additional
control games. Jlaunch.judge_integration is REVIEWED_APPLIED_TESTED.
Bound J finalqueue /tmp/relative_J_final_continuation_20260914.py is ready,
sourceSHA828377b9eb9bfa7e15834965074cedfcc7fc7fc49657cc861326ec620c8b7445.
This entry precedes its launch; inspect Jlaunch.automatic_final_continuation
for an original session/PID before starting it. It must be started only once.


**September 14, 04:59 UTC — critique favors H continuation conditionally:**
Independent critique and root-recomputed arrays/logs are preserved in W01launch.
Crop-update W00/W01 cosine is0.99447/0.99475 by seed; H seed cosine0.98600.
These are parameter diagnostics, not strength metrics. C population mean_win
increases but available engine judges regress; no deterministic C centre
training score exists, so the failure mechanism remains unisolated.

Root will not select H-on-C, reverse ordering or block-scaled H+C merely for
new scope. If both W01 and current J pairs fail useful standard-judge win
improvement, preferred follow-up is audited H311/H312 checkpoint continuation
fromgen10 to20 with unchanged W00 relative objective and per-family judge.
No gain promised and no new recipe/code/run frozen: Sol crop_learning_review
is verifying ALL resume state, cadence and H311 post-custody provenance first.
Current J outcomes can change this conditional priority.


**September 14, 04:50 UTC — crop coordination paths verified; next recipe undecided:**
Sol scope report is preserved in W01launch.crop_coordination_scope_review.
Root verified frozen source identities and C's one-way crop-share output versus
H/J grow/sell -> gp -> global-head path. B's gp is nonzero in all864 entries,
including all576 grow/sell projections. Thus C freezes direct valuation/global
parameters; H/J can affect global decisions indirectly, subject to quantization.

The proposed conditional H-on-C continuation is NOT SELECTED. It would train
130H coordinates atop fixed165C weights, not simultaneously optimize295.
Root assigned independent critique against C-on-H or true block-scaled H+C:
starting from adverse C parents may spend the next run undoing damage. Choose
based on win potential/evidence, not easier audit implementation. Wait both
W01 and current J final judges plus review before freezing any new recipe.
Current training, judge helpers and original process handles unchanged.


**September 14, 04:46 UTC — both relative-J first generations complete:**
Direct native-log and original-process checks04:46:27UTC: J311gen1/10,
859.55seconds; J312gen1/10,854.06seconds. Original controllers1336928/1336929
and training workers1341262/1341251 all live. No restart or strength verdict.
Original W01 queue98544 is live and C313 strength_execution child9312 is
running; C314 completed/adverse as recorded below. J judge integration and
bound final queue remain pending BOTH W01 judges terminal. Sol continues
W01 outcome review and conditional joint crop/labor/expansion scope research.


**September 14, 04:43 UTC — W01 C314 judge complete, adverse; C313 starts:**
Original queue98544 observed C314 strength_execution exit0 and
STANDARD_JUDGE_COMPLETE, then C313 assembly child9185. C314 saved audit PASS
SHA5528b698b3170c269d6b3b312eaa49888ea736f27a817fc46519041643cd0c1a;
root verified exact theta and all seven candidate/base CSV hashes.
Strict wins gained/lost versus B, families separate:
TOPB2 0/5; H30 0/5; H30B 0/9; LIVE62 2/21; LOSS10 2/1;
NEXT30 2/5; NEXTHIGH 0/8. Individual C314 rejected for promotion.
C313 is pending; no pooled campaign verdict. Exact results in
W01launch.standard_judge_results.314. Keep original C313 judge running;
four helper changes and J final queue still await BOTH W01 judges terminal.


**September 14, 04:41 UTC — startup reuse reviewed and deferred:**
Sol startup_reuse_review is complete; full report and root-checked source/timing
basis are in Jlaunch.startup_reuse_review. A private qualification-derived JAX
cache could plausibly save203–206seconds of duplicated992-row initialization
in a fresh training process (~3percent/run). No cross-process hit is measured;
source/timing evidence comes from older same-runtime cold/warm receipts.
It does not remove the separate8192-row generation compile. Same-process
continuation would conflict with independent initialization and cleanup gates.
Root decision: preserve this future option, defer implementation/protocol
changes while prioritizing win experiments and structural decision-scope work.
Current J frozen cache-off contract stays unchanged. Both original J workers
were live and GPUs100percent at04:39:09UTC; native logs stillgen0.


**September 14, 04:38 UTC — four new losses reviewed; no recipe change:**
Sol's new-loss report and root verification are preserved with full source,
extracted evidence, profiler CSV and download receipts in W01
launch.fresh_loss_review_20260914T0426. All four replays directly confirm12
accepted day0 melon plants and72 inventory-accounted early melon sale units
per opponent. Largest loss108781192 repeats more crop cycles; its27607
reconstructed sales gap is not exact causal attribution (B reconerror609,
opponent0). Jesse's3605 wheat purchases/3829 sales do not prove arbitrage:
production and fertilizer spending confound gross turnover. No new strategy
switch, loss-selected training addition, or experiment-order change justified.

Original J controllers/trainers remained live04:34:52UTC, atgen0 / first
training-generation boundary; workers were using165–166 percent CPU at~04:35.
Sol startup_reuse_review examines this cost prospectively, without touching
live jobs. W01 queue90698 and C314 judge5005 remain live; C313 awaits its
sequential standard judge. Four judge helpers remain pinned and unchanged.


**September 14, 04:28 UTC — both relative-J qualifications PASS; training started:**
Direct remote observation04:28:19UTC verifies original J311/J312 controllers
1336928/1336929 live in TRAINING. Both qualification receipts complete/PASS,
one qualification generation each, both saved qualification audits PASS.
New training worker PIDs1341262/1341251 are at cold_inputs_saved. These are
children launched by the original controllers, not restarts. Observe original
handles and allow their ten-generation runs to finish. Training initial evidence
is in Jlaunch.training_initial_observation. W01 queue98544 was polled live.
No final J centre or strength result exists yet. J final queue remains deferred
until BOTH W01 judges terminal and reviewed judge integration is applied/tested.


**September 14, 04:28 UTC — J qualification live; new public snapshot:**
Original J controllers1336928/1336929 and qualification workers1336953/1336951
were directly verified live04:26:34UTC. Controllers RUNNING without errors;
qualification still cold_inputs_saved. A provisional REFUSED field in the
in-progress qualification receipt is not a terminal refusal. No restart.
W01 original queue98544 continues its standard judges; Sol w01_final_queue
reviews their exact results as they arrive (no extra games or pooled verdict).

Public snapshot S/ladder2/snapshot_20260914T0426Z made three successful paced
reads04:26:07–17UTC. Unchanged B submission56161192: rank191, score2752.3,
263wins/404completed games; fifth submission56173067 score2991.1. Since0328:
10new games,6wins/4losses. Exact receipt/summary embedded in W01launch.
Sol crop_learning_review is reviewing new loss108781192 first (new opponent
team16840439; B134879 vs148034). Other new losses108781731,108775412,
108770495 are secondary if they add evidence. No recipe or promotion change.


**September 14, 04:24 UTC — W01 training PASS; relative-J launched on both GPUs:**
W01 C313/C314 both completed10 generations, original controllers exited PASS,
remote saved audits PASS, both training archives collected and local saved audits
byte-equal PASS. Exact theta/archive/audit identities are now in W01
launch.training_collection. Original final queue98544/PID90698 remains live:
C314 strength execution child5005 is running; C313 is ready for its sequential
standard judge. No W01 strength conclusion yet; do not restart or duplicate.

The prospectively revised schedule was satisfied: both local collections PASS,
original remote controllers absent with audit hash bindings checked, and both
GPUs empty (1MiB each) at04:22:18UTC. Prepared J311/GPU0 and J312/GPU1 launched
once at04:23:04UTC. Original controller PIDs1336928/1336929; both confirmed live
in QUALIFICATION at04:23:42UTC, worker PIDs1336953/1336951, cold_inputs_saved.
The original controllers own qualification -> saved audit -> ten-generation
training -> saved audit. Observe those handles; never relaunch on timeout.
Remote root: /home/user/kagg3/artifacts/momentum_relative_joint_campaign_20260914.

Reviewed final J queue is preserved, including source, in J launch.json;
original handles are bound in /tmp/relative_J_final_continuation_20260914.py
SHA828377b9eb9bfa7e15834965074cedfcc7fc7fc49657cc861326ec620c8b7445.
It is NOT LAUNCHED: wait BOTH W01 judges terminal, then apply the already
reviewed J integration patch, run its recorded focused tests, record exact
helper hashes/status, and start that bound queue once. It collects each J
qualification before training evidence, then unchanged seven-family judges.
Four root W01 judge helpers remain untouched. No new submission/promotion.


**September 14, 04:17 UTC — overlap J training with W01 CPU judges:**
Prospective scheduling revision, recorded before J launch: launch the installed
relative-J311/J312 pair after BOTH original W01 training controllers and saved
audits are terminal PASS, both training evidence collections pass local audit,
and both remote GPUs are empty. W01 local CPU standard judges may continue.
This supersedes earlier conditions requiring W01 win outcomes / whole queue
termination before J TRAINING. J remains independently justified by adjacent
pure-relative H evidence. Recipes, inputs, final-centre selection and the
seven-family win-first judge are unchanged; no promotion decision is implied.
Root and Sol reviewed isolated paths, GPU ownership and local judge locking;
source hashes and rationale are in both campaigns' launch scheduling records.

Do NOT edit the four root judge helpers or launch J judges until BOTH W01
judges are terminal. Original queue session98544/PID90698 still owns W01 final
collection and judges. At04:15:07UTC both original W01 controllers are live,
both native logs show9/10 generations, both GPUs100 percent (9058MiB each).
J is still NOT LAUNCHED. Sol is adapting the existing continuation source for
J collection/judging in /tmp; original J handles must be bound after launch.


**September 14, 04:04 UTC — scenario review complete; W01 gen8:**
Both native W01 logs show8/10 completed generations at04:00:13UTC; original
queue session98544/PID90698 remains live and confirms original controllers
RUNNING without observation errors. Final collection/judges remain its job.

Sol scenario review is root-reviewed and saved in W01 launch.scenario_variation_review.
The120 tape identities/commands, town schedules, cold starts and derived weed
words repeat across generations and seeds313/314. Seats alternate; ES noise and
four residual episodes refresh. These two training seeds are optimizer/noise
replicates, not two independent120-board sets. A prior weed-offset study on an
older196-tape campaign weakens a weed-only explanation; W00 lacks saved final
centre training scores needed to establish train-set overfit. No new seed arm
selected. Preserve W01 and conditional pure-relative J priority. No new games,
benchmarks, GPU work, or training inputs from this review.


**September 14, 03:49 UTC — J judge integration prepared; parity setup fixed:**
The existing 120-dawn parity preparer wrongly required historical momentum_joint
candidate labels. Commit37b3e43 matches the audited campaign run by seed/arm/name
instead; ten focused parity tests passed, including wrong-label rejection.
The old2400-observation fixture has no history fields; for trained J reuse the
existing120-dawn actual-history macro/day-plan NumPy/GPU check. The generic
package verifier already supports J6855/history and needs no code change.
No candidate-specific parity or package run has occurred for prospective J.

Sol's exact registration patch is root-reviewed and passes git apply --check,
but is NOT APPLIED. Patch/review/check commands are embedded in prospective J
launch.judge_integration_prepared; patchSHA0b44b1cb7bdddc7e5bb32a04a3dd883b9aaf43b42f3fb72e083dde1bf3b24d15.
It registers onlyJ311/J312 with6855layout/196active coordinates and keeps the
seven-family judge. Apply only after both W01 judges are terminal and the J
launch decision is made. All four pinned helpers remain byte-identical.
Original W01 trainers/controllers and queue90698 verified live03:46:09UTC,
with6/10 generations complete for both seeds. No new GPU run or submission.


**September 14, 03:38 UTC — new-loss review complete; W01 halfway:**
Sol completed loss108765130 (shyjin). Root checked all report input hashes and
independently verified 12 day-0 accepted melon plants and 72 inventory-accounted
sale units on days10/11. B's melon sales occur later. The opponent's six late
SELL MELON1000 requests had no inventory effect and are not counted as fills.
The report's plant counts remain observed transitions, not a complete trace of
same-frame harvest/replant. Detailed report/source/derived data and root proof
are preserved in W01 launch.fresh_loss_review_108765130. This repeats the known
early-melon plus sustained crop-cycle mechanism; no new intervention selected.

At03:34:43 UTC both original W01 trainers had completed gen5/10 and all four
remote controller/trainer PIDs plus local final queue90698 were confirmed live.
Remaining training is approximately40–50 minutes at recent generation times,
followed by the unchanged standard judges. No new J training or submission.


**September 14, 03:34 UTC — prospective J inputs installed; public update:**
The reviewed 110,940,772-byte relative-J training bundle transferred under the
user's standing approval. All 195 members passed archive and installed-file
hash checks locally and at `/home/user/kagg3/artifacts/momentum_relative_joint_campaign_20260914`.
Both remote J input validations passed without GPU work. Bundle SHA:
`b6af985eb06cdb29c78afceccc6f9d0853f987dbaf90bd89ba49517455d247b9`.
The campaign launch.json records installation evidence and root-reviewed reused
qualification-to-training advancement plus generic qual/train collection source.
No J jobs launched. Candidate registration and the final judge queue remain
pending W01 terminal results and the launch decision. No pinned W01 helper edits.

Public reads at 03:27:35–45 UTC are cached in
`S/ladder2/snapshot_20260914T0328Z` (directory label is rounded). B rank 199,
score 2743.2, 257 wins/394 games; fifth score 2981.5. Eight new games since
02:38: seven wins and one loss. This is unchanged B's ongoing ladder play,
not a training improvement. Sol crop_learning_review is reviewing only new
loss 108765130 (B 80032 vs opponent 85675) for a distinct decision limitation.
Original W01 controllers/trainers and local queue PID90698 were verified live
this turn. Their previous gen4 progress remains the last native-log reading.


**September 14, 03:24 UTC — relative-J preparation complete; W01 still training:**
Branch feature/relative-joint-objective, implementation commit 2a95ce3. Existing
preparer supports `--joint --relative-objective --relative-arm J`; default H
behavior is retained. Eleven focused tests passed. The prospective campaign is
`S/unitorder/momentum_relative_joint_campaign_20260914`, manifest SHA
`0d3c233e9032e6f9d4a2c7e16ba09b876886634e56d24d489d82c53219c7360c`.
Both real J input validations passed (194 bound inputs, 120 tapes, 196 active
coordinates), and both legacy H controls remain accepted. Sol's independent
consumer review found no blocking issue. See its launch.json for checks.
No relative-J GPU job launched; launch still depends on W01 standard outcomes.
Do not modify the four pinned judge helpers until W01's final queue is terminal.

At 03:23:48 UTC, original W01 controllers 1299295/1299296 and trainer children
1303557/1303530 are live. Both native logs have completed generation 4 of 10;
cumulative training times 2727.7/2679.2 seconds. Population wins are not final
centre strength. Original final queue PID90698 was also verified live this turn;
it still owns collection and both standard seven-family judges. No restarts.


**September 14, 03:04 UTC — fresh losses and next-candidate priority:**
All three new losses repeat early melon production and more later crop cycles.
Direct frame checks account for 12 early melon plants and 72 sold melon units
per opponent. The visible-tile census missed one wheat plant that was accepted
and died at day end for each of yukio and track. Supplemented counts are 247
and 237 versus B's 173 and 191; Majkel has 262 versus B's 176. These are counted
accepted events, not a universally complete event trace. Full report, sources,
hashes and proofs are in W01 launch.fresh_loss_review_20260914T0238 and the
existing 023838 snapshot cache. No new market switch or loss-selected training
input follows; no game or evaluation was rerun.

Correct identities: M = mh,ms (66 momentum coordinates); H = w2,b2 (130 output
coordinates); J = both (196 coordinates). The original zero-flip result belongs
to M. Shaped H/J have mixed, matching family win-flip patterns, although some
CSV bytes differ. The earlier crop-sigma proposal mislabeled M as H; the launch
record explicitly supersedes that history. Numerical crop-state analysis remains
valid. Pure-relative H produced positive adjacent outcome evidence.

Pure-relative J has never run: the relative campaign deliberately tested only H.
If W01 produces no useful win improvement, prioritize fresh pure-relative
J311/J312 over crop sigma 0.25. Reuse the existing J mask and runtime, with a
prospective contract before edits or launch: same W00 tapes, B initialization,
seeds, sigma 0.01, learning rate 0.00018, population 4096, 124 episodes, ten
generations, and final-centre standard judge. No new campaign is launched.
Incremental momentum strength remains unproven; its history input is zero on
day 0. This is an untested objective/scope combination, not a claimed solution.

**September14, 02:49 UTC — W01 generation1 completed on both GPUs:**
Original trainerPIDs1303557/1303530 live; native log records gen1 elapsed
859.1/852.1seconds, mean populationwins.202014/.205156. BothGPUs100%/9058MiB.
These are perturbed-population summaries; no final-centre strength result yet.
Do not interpret receipt phase generation1_boundary as stalled: wrapper saves
only selected boundaries; native log.jsonl carries completed-generation records.
Original final queue98544/PID90698 continues to own collection and standard judges.


**September14 — saved crop optimizer review complete:**
Root reviewed NumPy-only source/result and matched all12 NPZ/config/log inputs
against original W00 collection custody. Recorded in W01launch.crop_sigma_review.
Mean first-population perturbation radius6.406/6.408; final displacement1.627/1.605;
cross-seed final direction cosine.942. Population growth does not establish
centre strength: no centre report was saved with abs/champ11 and10generations.
This is consistent with broad-perturbation mismatch but does not separate it
from opponent/simulator transfer. Pure-relative H311/312 DID gain wins; earlier
zero-flip evidence was M-only66, not H. Shaped H130/J196 had mixed flips. Sigma.25 remains a conditional
proposal for after W01judges/fresh-loss review, not a selected automatic launch.
Holding lr3.6 does not match effective step because estimator divides bysigma.
No new games/tests/training or changes to active W01follow from this review.


**September14, 02:42 UTC — public refresh and W01 coverage:**
Snapshot S/ladder2/snapshot_20260914T023838Z: B rank223,score2718.4,
250/386wins; fifth2989.7. Eight new games since0130:5wins/3losses.
New losses108751875,108743730,108740598 assigned to Sol tape_denial_review
using existing paced replay tools. No new candidate uploaded.
W01's30 added tapes all have full-season command sequences absent from W00,
but onlyone adds a new day0 sequence. Full-season unique sequences118 inboth;
day0 uniques29→24, largest W01identicalopeninggroup49. Recorded orders only,
not accepted actions or proof of strategy diversity. Source/hash/result in new
launch.opponent_command_coverage. Preserve current training recipe; no rotation
or dedup experiment follows from this census. Original remote trainingchildren
1303557/1303530 verified live at13:35elapsed, bothGPUs100%/9058MiB.


**Latest September14, 02:36 UTC — W01 final judge queue live:**
Both remote/local qualification saved audits PASS and byte-equal; each archive
contains58 files. Existing final continuation session98544/PID90698 launched
once and verified both original remote controllers live at generation1_boundary.
Source eaea78d282693e95a788298bca65d2c7e2c47618ad1df090092d3949ab542efe.
This queue owns final training collection, saved local audits and sequential
seven-family judges for W01 C313/314. Do not duplicate these jobs or edit the
four root judge helpers pinned in new launch.judge_integration.source_sha256.
Original remote trainerPIDs1303557(seed313)/1303530(seed314) remain the handles.
Monitor new campaign/final_continuation/receipt.json and originalsession98544.
Commits f41819a and b695f45 record launch setup and qualification collections.
Sol crop_learning_review is reviewing existing W00 evidence for perturbation-scale
mismatch; no W01 recipe changes, new games or training launches authorized by that
research. No W01 strength result yet; top-five goal remains unmet.


**Latest September14, 02:31 UTC — W01 remote training live:**
Branch feature/crop-mix-w01, implementation50b1db0 and launch preparation55ebb4c.
New campaign S/unitorder/crop_mix_w01_campaign_20260914, manifest
f410b7f152bef2addd4bd63c11f4cd2b5d1656396679d813a307190d3d5d6de6.
One-shot controllers seed313/GPU0 PID1299295 and seed314/GPU1 PID1299296
launched02:23:32UTC; both qualifications/saved audits PASS. Training began
02:27:59/02:28:00UTC; original trainer children1303530/1303557 verified in
GPU process list. Cold-input receipt uses REFUSED until final PASS by design;
controller RUNNING and live process are authoritative while work continues.
Remote root /home/user/kagg3/artifacts/crop_mix_w01_campaign_20260914.
Each controller owns qualification, saved audit, ten-generation training and
saved final audit; never launch a duplicate. Launch receipt and exact sources
are in new launch.json. Existing collection helpers adapted to W01; root collects
qualifications; Sol-adapted final collection/judge queue is prepared and reviewed,
awaiting local qualification audits before one-shot launch.
Only opponent tape window and run names differ from W00; frozen43-file stage,
cm/cb165 training mask and other recipe settings unchanged. Both W00 candidates
remain rejected. No W01 strength result yet. H312 upload still awaits user auth.


**Latest September14, 02:03 UTC — both W00 C seeds rejected; W01 implementation:**
Original queue53213 COMPLETE exit0; both standard executions/audits PASS.
C313 finished01:59:42UTC. Its separate gained/lost wins: TOPB2 0/6, H30 0/8,
H30B 0/4, LIVE62 0/19, LOSS10 0/1, NEXT30 0/5, NEXTHIGH 0/8. C314 counts
remain below. Neither candidate is promoted. Final reports in crop launch.
First replay capture82698 refused before any game because lock release preceded
the persisted final execution receipt. Preserve loss_replay/receipt.json.
Corrected capture55626/PID86770 PASS at02:02:42UTC, fresh loss_replay_retry1:
B101546/98888 and C314102695/108132 exactly reproduce the same existing judge
row, all720frames/DONE,303 bound inputs unchanged. Profiler reconstruction
error0 for allfour rows: opponent sells same aggregate quantities per product,
earns9323 more sale revenue and spends79 more on products, net+9244. Strawberry
+5916, milk+2015, wool+1268 dominate; no identical-per-turn-fill claim.
All former helper pins are RELEASED. Sol agents are now editing their owned
existing training helpers for W01; root owns focused tests/judge registration.
No new training launch yet. Branch feature/crop-mix-w01; latest prospective
contract bc8f555 and completed C313/synchronization evidence327c07d.

**Next experiment selected September14 — sealed W01 crop transfer:**
Current branch is feature/crop-mix-w01 (created from301962b). W01 seal and
existing window validator PASS for all120 tapes/exclusions. It retains W00
positions30:120 and adds30, with no standard-judge overlap. Current W00 already
embodies prior weighting remedies; this never-launched sealed rotation is the
new intervention. Prospective contract in crop launch.next_w01_experiment:
fresh B, originalseeds313/314, names crop_mix_w01_C_seed313/314, same cm/cb165,
sigma.5/lr3.6/pop4096/E124/10gens/pure-relative/final-centre recipe. Reuse portable
S/rotband/artifacts/tape_actions_town paths; no trainer/policy/planner edits.
New explicit profile crop_mix_cmcb165_w01_v1 and181 bound inputs. Sol owns
prepare+protocol and train+auditor respectively; root owns tests/judge/Git.
All helper edits still wait for current C313 judge AND queued loss capture.
Do not invoke old launch_flow215_w01.sh: it resumes a different1191-gene recipe.

**Queued diagnosis September14, 01:46 UTC:** Original C313 judge remains live.
Loss replay session82698/PID83686 waits on the existing CPU lock; it will run
only after both C judges PASS. It records B/C314 on the first lost LIVE62 row
(seed4674845, opponent107056463, seat0), requiring exact original payouts.
Source and handle are in crop launch.loss_replay_diagnostic; no new strength
comparison. Keep bound helpers unchanged until this capture also finishes.
Source reviews find dynamic opponent money is modeled. No day0 gate selected.
Next candidate hypothesis is recent disjoint training-pool coverage, pending
inventory and comparison with prior flow211/flow215 reweighting; no new run yet.

**Latest September14, 01:35 UTC — C314 regresses; C313 judge live:**
C314 standard execution and saved audit both PASS, completed01:33:57UTC.
Gained/lost wins versus B, separate families: TOPB2 0/6, LIVEC-H30 0/4,
LIVEC-H30B 0/8, LIVE62 0/22, LOSS10 0/1, NEXT30 0/3, NEXTHIGH 0/12.
Do not promote C314. Existing queue53213/PID69318 automatically started
C313 judge child80456; retain helper pins until terminal. No repeated games.
Full family report and hashes in launch.json.standard_judge_results.314.
Opponents gain1726–3637 coins per family while own earnings are nearflat or
positive in several families; this supports checking modeled market effects,
not a causal claim. Sol crop_learning_review traces trainer/theirs scoring;
tape_denial_review independently traces engine-side tape/market semantics.
No new hypothesis or training launch selected. H312 remains release-ready,
not submitted pending Kaggle authentication; B remains incumbent.

**Public status September14, 01:30 UTC:** Existing public API snapshot
S/ladder2/snapshot_20260914T013100Z records B rank242, score2709.8,
245/378wins; fifth2990.6. Since23:31,15new completedgames include9wins/6losses.
No new candidate uploaded; goal remains unmet. Snapshot hashes and episode
delta are recorded in crop launch.json.public_snapshot_20260914T0130.

**Latest September 14, 01:17 UTC — both C trainings complete; standard judge active:**
Both exact ten-generation C313/C314 runs and remote/local saved audits PASS.
Original controller sessions16964/75376 exited0; do not restart them.
Final theta SHA C313 `6e2d9261a60e9aca1d1556e9ca7ad118d30e05ff6df602738afc9ab1ac5755f6`,
C314 `a89bf7d97f7d086b15cc57928f0ea97b9f1412234481c368cf5a723a8e4bb878`.
Both collected under crop campaign/project/artifacts; training_completion and
training_collection in launch.json bind receipts, archives and native logs.
Last-generation621.47/608.91sec confirms skipped centre-report overhead; logged
population mean wins .24144/.24568 are not final-centre strength evidence.
Queue session53213/PID69318 remains the sole owner of collection and sequential
standard judges. C314 judgePID78208 started01:13:56UTC and runtime preflightPASS;
C313 locally audited and queued. Keep all four pinned root judge helpers unchanged.
Final-opening review is recorded in launch.json.final_opening_review: both C
centres emit6 wheat/13 carrot vsB11 wheat/8 carrot on episode108450468seat1d0,
with no melon and other Macro fields unchanged. Planned commands only, not
accepted actions or strength. Bound source/input hashes rechecked exact. The
5.1-second diagnostic overlapped the active judge; no game was rerun.

H312 exploratory archive remains releasePASS and NOT SUBMITTED; Kaggle CLI still
requires authentication. Exact archive, SHA, release receipts and upload command
are in relative campaign launch.json.exploratory_trial. Browserless OAuth requires
user code entry in their terminal; no code requested in chat. No browser-control
tool is exposed. The archive is255,516bytes, SHA
`0f6af5e9cf58695de1cf53d271ef7efd6e4a7835dba80fd194c9fd79fa7a8ff6`.
All release checks PASS:2400-observation NumPy/GPU,1440 recorded actions,
both-seat full-season engine smoke. H312 choice is operational custody, not
superiority overH311; B remains incumbent and the top-five goal remains unmet.

**Current continuation 2026-09-14 — crop-mix training and standard judge ready:**
Branch `feature/crop-mix-head`; core f2f6917 and frozen training setup fd8872c.
New separate cm(32,5)/cb(5) head appends165 coordinates at6855:7020;
B6789 plus231 zeros is unchanged under existing CPU/GPU trajectory checks.
Only cm/cb train; valuation, other heads and planner remain frozen. This tests
whether learned crop proportions can escape the observed tiny H perturbations;
no forced melon crop rule. Sigma0.5/lr3.6 is an exploration hypothesis, not a
proven optimum. Same120 tapes+4 archetypes,4096 population,E124,10 generations,
pure relative margin objective, final centres only, reports at11. Standard
seven-family judge stays separate by seed and family; top-five goal unmet.

Campaign `S/unitorder/crop_mix_campaign_20260914/launch.json` records custody,
commands and observations. Manifest c1d0ddcb324d01f2dc6be176344a58ae01fb7f2e910de7df7f7776806d4ee8da;
stage manifest aadd696c7c9e15f9429fb75736eb6ed812334feff13c03c92a998df74c6a9d85.
Frozen stage inherits old43 files, with only brain/policy and the7-line champion
report-cadence patch changed. Do not copy root trainer refactors into it.
Authorized1.71MB bundle transferred and installed hash-exact remotely and in
local campaign/project. Qualification313 session41986/PID1262437 onGPU0;
314 session35485/PID1262339 onGPU1. Both qualification commands and saved audits PASS. One-shot continuation source
committed3745477, sessions16964(seed313)/75376(seed314), controllerPIDs1266691/
1266633, now owns exact ten-generation launches and their final saved audits.
Training started23:22:06UTC on both GPUs; live child handles are recorded in
launch.json. No duplicate training or audit launches. Next: poll those original
sessions/processes, collect qualification/training artifacts using existing safe
archive path and audit byte equality, then standard judge each final centre.
No restart on SSH observation failure.

Judge integration is committed1849160, with exact C313/C314 candidates,
7020-coordinate frozen-prefix validation and unchanged7families/424keys.
Both qualification archives(58files each) are collected locally and existing
local audits PASS byte-equal remote; see launch qualification_collection.
Original training processes1266734/1266711 verified live; both finishedgen1
at latest23:41:40UTC poll (858.78/852.67sec). Population meanwins.195723/.198572,
best.612903/.572581; these are perturbed simulation candidates, not final centres
or public winrates. Wider search initially includes many weak policies; do not
select an intermediatecheckpoint or change active recipe. BothGPUs previously100%/9058MiB.
Final collection→local audit→sequential standard judge continuation committed
ed9456a and LIVE session53213/PID69318; source430d20952cb8dac7c0af2bbd93eb7d6113e55c51f22068b4c2513bec8b16083f.
Receipt crop_mix_campaign_20260914/final_continuation/receipt.json; both exact
remote controllers verified live. This queue owns final archives, download,
local audits and judges; no duplicate training/audit/judge launches. Root judge
helpers are now pinned for this queue; do not edit until both judges terminal.

Actual saved first-population noise now establishes broader macro exploration
on the same episode108450468seat1d0 observation: C313melon302/4096,
C314melon316/4096; anycropchange3970/3984 respectively. Exact noise, sigma0.5;
CPUdecode, oneobservation, targetsonly (notrequests/acceptedactions/wins).
Source+result and hashes are embedded in launch initial_population_reachability.
Both qualification private stages remain exact43files after diagnostic.

Fresh public snapshot S/ladder2/snapshot_20260913T233101Z: B236/363wins,
rank264,score2694.3; fifth3007.1. New20games contain8wins/12losses, all12loss episode IDs absent from exact120
training tapes and prior knownsixlosses. Three informative replays108682693/
108689537/108701698 reproduce accepted12melonplantd0 vsBfirstmelond9, plus
236–246 opponentplants vsB165–171. Sixseat cropcounts independently verified
from exact tile transitions; source/report/profile embedded in launch latest_loss_review.
Capacity review complete: in2losses, labor/land/unique planted tiles are nearly
equal but opponents plant74–76 more wheat, chiefly through repeated cycles
afterd10. Keep currentcm/cb165scope; these replays do not justify crew/land
expansion. Source/result and perday arrays embedded in launch planting_capacity_review.
Public top-five target remains unmet.

Relative-H seed311 completed all7 family games. Original execution REFUSED
because diagnostic imports generated15 undeclared bytecode files in private
stage, although all43 source bytes stayed exact. Preserved caches and original
failure receipts; existing runtime post check recovery2 PASS, supplement
POST_CUSTODY_RECOVERED. Use this composite evidence honestly, never relabel
original execution PASS. No games rerun. Gains/losses versus B: TOPB2 0/1,
H30 0/0,H30B0/0,LIVE62 4/0,LOSS10 3/0,NEXT30 1/1,NEXTHIGH0/0.
Win gains remain primary despite negative mean margins in several families.
Seed312 completed directly PASS at23:17:24UTC with saved audit PASS, final
hashes exact and lock released. Its family win gains/losses match seed311.
Queue91908/PID57332 is terminalexit1 solely from retained311originalfailure.
Both candidates retained and B remains incumbent. C judge integration is complete;
the live final-continuation queue binds the root judge helpers.
Use `-B`/PYTHONDONTWRITEBYTECODE=1 for every frozen-stage diagnostic import.


**Progress September 14 — both relative trainings complete; standard judge recovery:**
Both ten-generation final centres have byte-equal remote/local saved auditsPASS.
Original continuation55695 ended exit1: assembly omitted relative-H candidate
labels in judge_execution.py; no game ran. Fix2e66238 reviewed,36testsPASS,
merged from fix/relative-judge-contract. Existing failed assemblies preserved;
launch.json judge_recovery holds exact fresh recovery1 paths and sequential
standard seven-family commands. Reuse collected weights/audits; no retraining.
Recovery launched: original session91908/PID57332. Monitor
final_continuation/recovery_receipt.json; do not restart. B remains incumbent.

**Progress21:48 UTC — both training runs generation7, continuation queue live:**
Original queue session55695 / PID49714. Source is embedded and hashed in NEW
relative launch.json under `automatic_final_continuation`; committed fea01ae.
Future-run CLI change bae70e4 exposes --champ-every with unchanged default10;
review/config checksPASS, merged from feature/train-report-cadence. Current
frozen jobs/queue unchanged. Future final-centre-only runs can skip unused
reports by setting both champion/absolute cadences above final generation.
Both exact live helper identity probes pass. Queue owns final remote audits,
full archive collection, byte-equal local audits, then unchanged standard judges
sequentially. Preserve original training sessions74334/77794. Do not start
any duplicate final stage. Monitor original queue session55695 and
`S/unitorder/momentum_relative_objective_campaign_20260913/final_continuation/receipt.json`.
PID49714 is visible in the escalated process namespace; ordinary sandbox /proc
visibility is not proof of termination. On queue error inspect existing outputs;
this is a one-shot queue, not blindly restartable. Two setup-only failures are
preserved as observer_attempt1/2; neither reached an audit, transfer or game.

Root checked all120 frozen tape hashes:118 request12melons onday0, one1,
one0. Early-melon opponent examples are already present.29distinct complete
day0 command sequences,118distinct full-season sequences; the three matching
full-season tapes have different towns. Order census only, no new game result
or same-code claim. Existing melon doc and launch.json preserve per-tape evidence.
No new pool, reweighting or objective arm selected. Sol/root objective review
keeps the current sigmoid-margin interpretation; prior scale trials provide no
positive case for binary wins or another margin scale. Await existing final judges.

Rejected-candidate behavior review completed: old campaign
`saved_plan_trace.json.gz` contains source and full180-observation evidence.
All four candidates keep B's day0 plan; H/J pairs execute identical plans on
all180 B-trajectory dawns. Changes are sparse (27/28dawns) and mainly toward
wheat. This diagnoses observed plans, not candidate trajectory causes. Current
abs0 H pair remains the selected objective test; no new J arm selected.
The suggested H+33 sharpness follow-up is now withdrawn under the same sigma/lr/
ten-gen recipe: fixed-score day0 melon boundary needs head7 shift≈−1.435 versus
direct sigma SD≤0.05745. One-state scale evidence only; no new acceptance gate.
Root reproduced the boundary; existing melon review records scope and prior art.

**Progress September 13, 21:06 UTC — melon history reviewed:**
Both original relative H training helpers verified live, native generation3,
both GPUs busy; preserve sessions74334/77794. No new arm selected.
Fresh B snapshot: rank222,228/343wins; top-five goal unmet. All six new losses
have a reproduced frozen-B day0 trace saved with source and input hashes in
`S/ladder2/snapshot_20260913T203300Z/summary.json`. First melon suppression is
grow-score softmax/rounding; maturity and absorption gates are open.
Historical review is in `2026-09-13-melon-sigma-reachability.md`: forced openings
failed, one-tile m0p1 failed simulator development only (engine confirmation
not run), learned Flow184 floors were selected against, additive was never run.
Corrected overbroad closure and receipt arithmetic claims. Finish current H
judges first; H plus crop sharpness is an unselected follow-up, not H+D for
this specific binding decision. No extra strength metric or expression gate.
Historical-review Sol hit usage limit; root completed the review locally.
Follow-up: Sol traced m0p1; root independently reproduced all six plan hashes
on old/current source. The +1 melon target triggers land, 4 extra crop commands
and 2 fewer animals; opening wheat pump unchanged. It is not isolated one-tile
evidence. Reproduction source/results/identities are saved in the same snapshot
summary under `m0p1_review`; current launch binds its new hash. No rerun selected.

**Progress20:28 UTC — original campaign fully judged; new training live on both GPUs:**
All four original H/J candidates finished the standard seven-family judge and
saved auditsPASS. None promoted; B remains incumbent, top-five goal unmet.
J311 original24911 finished20:26:05.660483UTC, lockreleased, gains/losses:
TOPB2 0/1, H30 2/0, H30B 0/2, LIVE62 4/4, LOSS10 1/0, NEXT30 1/2,
NEXTHIGH 0/0. All7mean margin deltas negative. Full results in old launch.json.

New pure-relative H qualifications: both remote/local audits byte-equalPASS,
control initialization and all58collected regular files perseed verified.
Qualification evidence committeded31518; training handoff0c7463a.
New training original handles: seed311 session74334/PID1235441/GPU0 started
20:21:59.847528UTC; seed312 session77794/PID1235539/GPU1 started20:22:09.284738UTC.
Both exact helper commands/PIDs verified live in cold-input/compile phase.
Root owns both original training jobs and all next evidence/judges; no restart
on observation timeout. Exact commands, source, GPU IDs and adapted existing
final collection/audit/judge continuation are in NEW relative launch.json.

Relative judge integration applied after J311 terminal as0848597 (frome1308b2):
11focused semantic checks plus11previously fixture-blocked checksPASS in full
workspace. Existing families, pinned B references and primary wins unchanged.
No new worktree; extensions.worktreeConfig remains disabled for client compatibility.

Sol next_lever now researches learnable sale timing, explicitly excluding repeat
source-only 4/6-row/late-SELL/split-lot trials.30–60minutecheckpoint; no code,
games or new selected arm. H+D remains an unselected follow-up with documented
task-exhaustion and compact-coupling risks. Prior states below are historical.

**Progress20:13 UTC — transfer approved; both qualifications launched; Git compatibility restored:**
User explicitly approved: “allow transfer to remote server”. SCP53316
completed0; strict remote installation8070PASS, all195files exact. New campaign
H311 qualification session40109/PID1230287 finishedPASS20:13:12; H312
qualification session6581/PID1230384 was still live at that observation.
Sol momentum_decision_review owns both qualification saved audits, collection,
local frozen audit comparison and new relative launch.json until handback.
Root owns subsequent ten-generation launches after qualification proof.

Old H312 standard judge7340 finishedPASS20:04:59, saved-auditPASS, lockreleased.
Not promoted: gained/lost wins TOPB2 0/3, H30 2/0, H30B 0/2, LIVE62 4/4,
LOSS10 1/0, NEXT30 1/2, NEXTHIGH 0/0. All7margin deltas negative. J311
queue24911 has started its exact standard judge; preserve this original handle.

Relative-candidate judge integration committed separately as e1308b2 on
feature/relative-judge-integration,11focused semantic testsPASS. Root reviewed
the3helper changes. Do not cherry-pick until J311 releases live helper inputs.
It reuses the existing judge with fixed relative candidate/profile registration.

Root's temporary sparse worktree enabled extensions.worktreeConfig, breaking
the user's older libgit2 client. Root removed ONLY that clean temporary worktree
after commit, unset the introduced extension and restored repositoryformatversion0.
Verified no per-worktree config/other extensions or stale index.lock; root planner
still exact B; branch e1308b2 retained. Do not re-enable sparse/worktreeConfig.
This block supersedes the earlier transfer-blocked and queue-waiting states below.

**Current lead continuation — final training evidence collected; new transfer blocked:**
All four original H/J runs finished ten generations; all frozen remote/local
saved audits PASS and match byte for byte. B remains incumbent; top-five unmet.
Both final theta identities and full custody proofs are in existing launch.json.

H312 standard judge original session7340 remains live (started19:44:29 UTC).
J311 assemblyPASS,302bound inputs. Queue session24911 waits for H312 clean
terminal/lock release, then runs J311 exact standard judge once. Queue source
and one-hour deadline are recorded in old launch.json. Poll original sessions;
do not start duplicate jobs. No extra parity, control games or new metric.

Pure-relative campaign frozen in commit3ec5ebd, manifest:
`S/unitorder/momentum_relative_objective_campaign_20260913/manifest.json`,
SHA4446c34822bb013af9898e76008223df6dc1902875e99a2f202c5b7790d76fb3.
Local mirrorPASS,195regular members. Both prospective H seeds311/312 remain
selected irrespective of remaining old results. Root planner is restored to B;
training source remains the original frozen momentum stage.

Bundle `/tmp/unitorder-momentum-relative-objective-bundle-20260913.tar.gz`,
109850483bytes, SHA69a5916cb301321a414a01a88062d3af443d83737d77d957dfb2dadd29b33a93.
Automatic approval review rejected direct SCP to user@remote-host:/tmp/
with this filename, saying internal payload export lacked specific authorization.
Prior user instruction approved all training bundle transfers, but rejection
explicitly forbids retry/workaround without resolved approval. NO remote mutation,
installation, qualification or new training launch occurred. Read-only inventory
verified original remote campaign inputs and both control qualification closures
still exact. Scope reviewer handed new launch.json ownership back to root.
Resolve explicit transfer approval before dependent remote work; do not bypass.

Sol next_lever reviews one remaining learned planning bottleneck using existing
source/replays, with a30–60minute checkpoint. No new games/code/files.
Historical sections below retain earlier states; this block supersedes them.


**Progress 19:36 UTC — pickup judge complete; H312 terminal and collection begun:**
Source judge84661 ended0, execution/saved-auditPASS, lockreleased,
finished19:32:15.127438 UTC. Separate gained/lost wins versus B:
TOPB2 0/1, H30 0/0, H30B 0/2, LIVE62 4/2, LOSS10 4/1, NEXT30 0/2,
NEXTHIGH 0/0. Not promoted: useful gains in two families but regressions in
three. B remains incumbent. Full exact outcomes are in existing launch record
and `early_stock_pickup_20260913/strength/judge_evidence/saved_audit.json`.
On current relative-objective branch, commitb9e8bf4 restores root planner to
exact frozen B SHA19ad281...; early-pickup source/branch/evidence remain preserved.

Relative-objective helper commits805564c/3cc35b7/3ee5cf0 are ready: existing
prepare/train/auditor reused,20focused testsPASS; complete control qualification
artifact closure is bound. New command (NOT EXECUTED YET):
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python S/unitorder/momentum_train_prepare.py --joint --relative-objective --output S/unitorder/momentum_relative_objective_campaign_20260913`.
No new transfer or training launch yet. Freeze after H312 local terminal audit.

312H original helper is gone normally at19:34:39 watcher poll; native10,
receipt/execution/cleanupPASS, frozen remote saved-auditPASS. Remote auditSHA
`eb4167b47f5a42954f169a9383dae762ef65075128451214700e8b480ce85c31`;
finalthetaSHA`7d4666116caa116cf26cf5cd2a3535ec6bd68f294914626d80f0e87101311ffd`.
Root archive creation session99292 is live; uses the already reviewed collection
source from existing launch.json, seed312 armH. Do not rerun archive creation
without checking original session and remote file existence. Local archive/dest
were verified absent. Root owns download/hash extraction/local frozen audit and
then H312 standard judge. 311J original helper still finishing; Sol scope reviewer
retains sole remote watcher/audit ownership. Source judge lock is free.


**Prospective decision 2026-09-13T19:23:29.947067+00:00 — pure-relative H pair selected:**
Root selected BOTH fresh-B H (`w2,b2`,130 coordinates) runs at `abs_weight=0.0`,
seeds311/312, before remaining current H/J results. Run both regardless of those
remaining results. Existing same-seed H0.6 trajectories are fixed controls; do
not rerun them. Everything except objective coefficient and run/output identity
stays fixed: immutable43-file momentum stage, B/start/optimizer, seeds, ordered
120tapes+4scripted slots, schedule/CRN, pop4096/124episodes, sigma.01,
SGDlr.00018/wd4e-7, ten gens/finalcentre. Tape score remains margin, scale3000,
zero shaping. Primary decision remains wins versus B under the unchanged seven
separate judge families. Matched Hcontrol results are context, not a new metric.

Current branch **`feature/relative-objective`**, created atf2bee2a without changing
live judge bytes. It currently still includes the earlier-pickup planner trial;
the NEW TRAINING SOURCE remains the explicitly frozen ORIGINAL momentum stage,
not current root plan.py. No new training config/campaign/transfer/launch exists
yet. Sol next_lever owns minimal existing prepare/train-helper changes and tests;
Sol momentum_decision_review owns auditor/provenance review/minimal changes.
No new runner, control games, gradient/snapshot gates or broad tests. Do not
modify judge helper files while source judge84661 is live. Root owns freeze,
transfers, all training launches, local evidence and standard judges.

Original remote311J and312H are both gen9 at19:21:54 UTC; exact PIDs/cmdlines
remain live. Sol scope_protocol_review's original read-only wrapper17534 reached
its timebox; ONLY the watcher restarted as7764, training untouched. That agent
retains remote normal-terminal audits. Root will collect/audit each final run.

Earlier-pickup judge84661 continues unchanged. TOPB2 lost1/gained0 versus B;
H30 has no flips; H30B lost2/gained0. Remaining families still running; no
promotion decision. Legacy runner chain_summary compares g940pair in TOPB2,
so use the explicit protocol B reference and final saved audit, not that legacy
ALL line. Six redundant broad abs-weight rg scans from Sol research were stopped
by root (verified PIDs32799,32927,33156,33158,33245,33262); local reads became
responsive again. Use narrow named-file research, no recursive wholeS scans.


**Progress 19:04 UTC — earlier-stock-pickup candidate committed and judge launched:**
Current branch `feature/early-stock-pickup`; planner/tests commit
`8b3335297f801a2057d0e035278d858009673fd1`. Planner SHA
`e11e4e3d1e00ad6b84aea21d5ac6f86a2a664a9cb796509599e802e4d1bfb302`.
The existing ROUTE_SPLIT extension advances a fully stock-covered first PICKUP
on narrow/no-land/post-day0/nonterminal days; later pickup kinds remain post-BUY.
It checks the credited trial cut, conservatively covers suffix changes, maintains
unit-ordered product stock/prefixes, and preserves feed/fertilizer sale reserves.
Sol implementation and independent source review complete. Focused checks9PASS,
3existing wide-fixture skips; NumPy/JAX agreementPASS. Historical OFF digest test
also fails on exact frozen baseline19ad281 (first actuald43120eca5443f9b versus
stale pine086a25a8c18fb6f), so this is recorded separately, not called a pass.

Existing judge source-only eligibility commits3ba3590/1208a30 bind unchanged B
and a physical43-file source tree differing only inplan.py. Real assemblyPASS,
294inputs, normal212boards/424seat games and seven separate families. Source
manifest `S/unitorder/early_stock_pickup_source_manifest.json`, SHA
`974382bbfabdddc468272b5fc30053b472b46385b0ed90fba299d3415a0ef990`.
Stage `S/unitorder/early_stock_pickup_20260913/private_stage` is a preserved
physical copy of the frozen momentum stage plus the committed planner bytes.
Judge assembly is in its sibling `strength/` directory. Original live judge
session**84661**, started19:03:33.426379 UTC, shared lock acquired. An initial
sandbox attempt17927 failed before any games because `/root/kagg3_judge.lock`
was read-only; its terminal evidence is preserved in
`strength/sandbox_refused_evidence`. Do not restart the live84661 process.

Remote original311J/session49763/PID1213546 and312H/session34365/PID1211103
continue unchanged. Sol scope_protocol_review owns their exact-command watcher
and frozen remote audits at normal terminal10; root owns local collection/audit
and standard judges. Latest watcher18:56:03 UTC had312Hgen7 and311Jgen6.
Use native log.jsonl `gen`, not snapshots. No candidate promoted; B incumbent,
top-five objective unmet.

Sol follow-on tail-HARVEST feasibility found no reachable/carry-safe trailing-PASS
activation in87dawns across three saved B games. Two ripe unadmitted tiles in
108615219day21 and one admitted-uncovered tile in108450468day26 cannot be
reached with remaining idle turns; the former game's shed is also full. Do not
implement this unsupported next mechanism now. Method, identities, counts and
limitations are in existing top1 `summary.json` under tail_harvest_feasibility.


**Progress 18:39 UTC — both first candidates judged; next feature branch created:**
H311 original session43936 completed exit0 at18:38:44.423064 UTC; execution and
saved audit PASS, all seven families complete, shared lock released. Separate
flips versus B: TOPB2 gained0/lost1; H30 gained2/lost0; H30B gained0/lost2;
LIVE62 gained4/lost4; LOSS10 gained1/lost0; NEXT30 gained1/lost2;
NEXTHIGH gained0/lost0. Every family has a negative mean margin delta, as did
J312. Neither candidate is promoted; B remains incumbent. Full results are in
the existing launch record and candidate saved audits.

Current branch is now `feature/early-stock-pickup`, created fromdb4fd86.
No policy code has changed yet. Sol source review and existing-judge integration
review continue. The saved-B inventory/position check found106 conservatively
stock-covered pickup opportunities on22 of40 eligible narrow/no-land days,
across three games, before preserving same-hour sale reservations. This is
feasibility evidence, not a win estimate. Remote311J/session49763 and
312H/session34365 remain the original live training runs; do not restart.

**Lead continuation — planner/training dependency review:**
User explicitly delegated leadership and requested continued research and
improvements. Sol reviews confirmed that H/J grow/sell changes reach global
outputs through B's fully nonzero `gp`; frozen global weights do not mean
frozen global decisions. J also reaches product pressure through `mh` and the
frozen `w3`. Integer decoding, shared budgeting, crew enumeration, admission
and routing can remove a changed preference before it becomes an action.
Neither arm can learn arbitrary market hours or intraday replanning.

Three current B replay decodes, saved in the existing top1 summary, show
crew_target0 on days0–6 but11 on day10 while the observed crew has8–9 hands.
Animal deferral is0 throughday11. Root challenged the proposed `g10,gb10`
training arm against this and the preserved labour studies; the reviewer
withdrew it. No crew-only arm is selected or launched. The0.6 own/0.4 relative
fitness can conflict with wins, but relative-only training has already been
tried extensively with mixed transfer; no new objective diagnostic gate or
strict-win implementation is selected. Historical M-only zero-plan evidence
must not be attributed to final J312.

Explicit B PASS commands across the three replays concentrate43.4% in hours0–2
and50.6% in hours18–23, versus only5.9% in the middle. These are command counts,
not all avoidable idle work. The existing tail filler is already enabled.
The existing `judge_saved_audit.reconstruct_history_actions` reproduced all720
frames and both private/action streams of top1 episode108622009, using its
public seed without a town override. Accepted-action evidence is
`S/ladder2/top1_20260913T180901Z/ep_108622009_accepted_actions.json`, SHA256
`4b10fd9e2b2e12aef8fbe623dca06075e1c141805a0da2066eb144f4d435a20a`.
Of1437 accepted sold units,1245 were outside B's hours1/10/18; gross proceeds
were105962/117766. Startup had275 accepted nonmovement unit effects and tail
had749, including100 PLANT and85 HARVEST. This establishes physical behavior,
not marginal profit or a candidate improvement.

Concrete next hypothesis under review: advance a narrow-day worker's first
PICKUP by one turn when its supplies already exist in the dawn shed, without
changing market purchase times. Reuse the existing route-splitting machinery;
account for competing pickups, existing reservations, worker birth and spawn
positions. Sol next_lever owns source feasibility/prior-experiment review;
momentum_decision_review owns the small saved-B opportunity count. No new
policy code, branch, test, game, or training arm exists for this hypothesis yet.
H311 standard judge session43936 and remote second-pair sessions34365/49763
continue unchanged. Preserve original handles and do not restart on timeout.

**Progress 18:18 UTC — J312 judge complete, H311 running; current #1 reviewed:**
J312 original session35143 ended0 with execution/saved-audit PASS and all seven
families complete. It is not promotable: TOPB2 gained0/lost3; H30 gained2/lost0,
H30B gained0/lost2, LIVE62 gained4/lost4, LOSS10 gained1/lost0,
NEXT30 gained1/lost2, NEXTHIGH gained0/lost0. These are separate-family flips.
H311's already prepared standard judge started18:11:25.590825 UTC, root session
43936; preserve that session and the shared lock. No extra control games.
Both remote second-pair helpers remain live with exact frozen commands. Native
log.jsonl shows311J generation2 (mtime18:08:38 UTC),312H generation3
(mtime18:14:51 UTC). Generation snapshot filenames are not a current-generation
counter; scope_protocol_review corrected its initial snapshot-only inference
and returned ownership to root.

Latest top1 episode read: `S/ladder2/top1_20260913T180901Z/summary.json`.
Rank1 in17:56 leaderboard was Majkel1337/submission56156662:230wins/25losses
(90.2%), last10085wins. Installed CLI required authentication, so the existing
public API endpoint/rate limiter was used. Three top1 replays (108603604,
108616637,108622009; two wins/one loss) and three B replays (108450468,
108620902,108615219; one win/two losses) were inspected with the existing
replay profiler and direct observed tile transitions. Exact replay paths/hashes,
methods and separate episode statistics are in that same summary JSON.
Top1 first melon planting day0 and first SELL order day10 in all three;
B first planting days9/11/9 and first SELL order days20/22/20. Top1 has242–294
new-plant transitions versus B173–205,11 hands byday10 versus8–9, and356–436
SELL commands spread across all24hours versus B125–152 at hours1/10/18.
Explicit PASS commands are0.89–0.94% versus10.0–10.9%; these are command
counts, not accepted productive work. Profiler top1 money reconstruction has
64–254coin residual, so exact top1 per-product income/fills are not claimed.
Different boards/opponents prevent causal attribution or identification of
opponent forecasting/momentum. Days/hours are zero based.
User requested a subagent to identify B's limits in expressing these strategies.
Sol next_lever now owns a substantive read-only review of exact shipped switches,
theta reachability, H/J scope, budgeting/routing constraints and prior failed
levers. No policy change or additional evaluation has been introduced by this review.

**Current user direction — reuse tools, standard wins, necessary tests only:**
Read `GOAL.md` first. It now contains the reviewed existing-tool map and working
rules, including the installed Kaggle CLI's `competitions episodes`/`replay`
commands and the existing paced capture tool. Use these for Kaggle data instead
of web search. The active objective is top five; older top-ten text is superseded.

The user superseded the extra momentum-specific evaluation plan: no new control
games, alternative performance metric, or action-expression acceptance gate.
Keep the established seven-family judge and its separate outcomes against B.
The frozen training inputs remain unchanged. J312's three already-running parity
modes finishedPASS; H311 actual parity finishedPASS (session3446). No unrun H
zero/lag2 checks or J controlled games should launch. Prepared control artifacts
are preserved, not evidence of executed games. Future weight-only candidates use
existing eligibility/custody and the standard judge; test changed interfaces or
observed defects, and preserve the established release gates before submission.

Existing J312 standard judge session35143 continues; H311 is ready for its own
standard judge after the shared lock is free. Remote second-pair sessions34365
(312H/PID1211103) and49763 (311J/PID1213546) must not be restarted.
Latest public capture via existing tools is `S/ladder2/snapshot_20260913T175600Z`:
15 new B matches since14:33,7 wins/8 losses. All8 losses have new opponent
submission IDs;1 has a known team and7 have unseen teams. Episode108450468 is
already known and its generic replay path is recorded in its existing receipt.
New episode IDs do not prove different strategy/tape bytes. The comparison JSON
records this limit. Loss-content inspection remains separate from this metadata
check. Preserve the active games/training while continuing the top-five goal.

**Progress 17:49 UTC — existing strength judge running alongside history checks:**
Both second-arm helpers are verified live with exact frozen commands:
311J PID1213546/session49763 on GPU0;312H PID1211103/session34365 on GPU1.
Both reached generation1_boundary and all eight initialization artifacts match
their own qualifications byte-for-byte and semantically. Exact evidence/source
from Sol scope_protocol_review is embedded in the existing `launch.json`.

J312 actual-history parity passed all18 fields on120 states; receipt SHA256
`672da5a4355bd56da05f9f9d8d67e1924211dde72a02d83d677a3a5609b51533`.
The original local parity sequence39701 continues zero then lag2. H311 all
three manifests are prepared, but its local GPU parity remains unlaunched.
All first-pair real contracts/manifests passed independent Sol review.

The user explicitly challenged the slow feedback cycle and asked why existing
evaluation was not being used. Root checked the frozen decision_contract:
it fixes required comparisons and interpretation but does not require strength
games to wait for all snapshot history controls. With actual parityPASS and
all three manifests already prepared, the existing J312 seven-family strength
judge is now running, original session35143, concurrently with GPU parity.
All original required comparisons remain; this changes scheduling only.
The J312 controlled-assembly sequence43905 is also running; it creates no games.
Do not launch a competing strength/control judge against the shared judge lock.
Sol scope_protocol_review has a10-minute read-only runtime/progress watch on
35143; Sol momentum_decision_review awaits all3 J parityPASS receipts for the
saved-only history comparison. No H/J strength outcome or improvement claim yet.

The17:42 and earlier entries below are historical snapshots.

**Progress 17:42 UTC — first H/J centres valid; second pair launched:**
Both original first runs completed ten generations and passed the frozen remote
and local saved audits byte for byte. All65 regular archive members per arm
were collected/hash-verified in the existing local campaign mirror. Source
symlinks remain metadata only. Exact executed watcher/audit sources and stdout,
custody, terminal hashes and local audit agreement are recorded in `launch.json`.
Original SSH sessions73451/61744 returned disconnect255; complete native
execution/receipt and monitor evidence plus independent saved audits prove
normal training completion. Do not restart either finished run.

| Completed candidate | Native final theta SHA256 | Matching saved audit SHA256 |
| --- | --- | --- |
| H311 | afe6a3386c986a64e7aedbc331f37351455adb0975a59e9230f9b5d1ee25438b | 45f1ea06c32fa266a2b7ca0df39e8df1f0b2b77026aba8c989ccb7c8c19983b6 |
| J312 | 11467742dfeb6e7070dc95e8b49cf548936ce78da436c669ccc55f9232fc2536 | 668f6969a9a7cfd30ff0d28cc43844f68fd0b47a1ff8f45153f623373823c254 |

Second pair uses original frozen inner argv, fresh B and the same GPUs:
312H original SSH session34365, helper1211103, exact command live and all eight
initial raw artifacts match its own qualification;311J session49763 launched,
exact helper observation pending. Sol scope_protocol_review has a15-minute
read-only startup/initialization comparison task for these two runs. It no
longer owns any first-pair terminal audit. Do not duplicate/restart these jobs.

Both first candidates passed strength assembly (302 bound inputs each). All
six actual/zero/lag2 parity manifests were prepared from those real contracts.
Local J312 three-mode parity is running on the authorized RTX3070, original
session39701. H311 assembly/preparation session17675 completedPASS; its GPU
parity has not launched. Wait for J parity before starting H on the local GPU.
Sol momentum_decision_review is waiting for all three J parity receipts to
perform the saved-only full18-array history comparison, including day0 equality.
Sol next_lever is reviewing actual assembled contracts/manifests read-only.
No actual H/J strength judge or controlled game has run yet; no improvement over
B is established, and top five remains unmet. Current branch is still
`feature/market-momentum`; no merge, promotion or new submission.

The17:15 and earlier entries below are historical.

**Progress 17:15 UTC — generation9; decision reviews and parity preparation complete:**
At17:13:42 UTC Sol watcher reported both original helper processes live with
generation9 completed. It retains sole ownership of remote `saved_audit.json`
creation for the first pair until terminal result or explicit handoff; do not
duplicate those audits. Root owns collection, local audit agreement and opposite
arm launch. No first-arm terminal result or second-arm launch yet.

Commit628113b adds audited-contract manifest preparation to the existing parity
helper;38 focused tests passed and independent Sol review passed. The existing
launch record includes12 exact prepare argv and reviewed collection source,
all PREPARED_NOT_EXECUTED. Assemble the strength contract once and prepare all
three parity manifests before strength execution because contract validation
requires fresh judge outputs. Then run local GPU parity and frozen evaluations.
Do not mutate frozen campaign inputs or blanket-add the local evidence mirror.

Two new bounded Sol decision reviews prioritize sale reservation crossings and
crop quota/funding/labor crossings. Compare full plans and accepted engine events;
macro changes, submitted purchases and hidden budget grants are different evidence.
The old15/11 macro changes with zero plans belong to M, not current H/J.
Details and exact source references are in the qualification/training document.
No policy change, new training arm, promotion or improvement claim followed.

**Progress 16:57 UTC — both training arms at generation7; final-centre handoff prepared:**
Continue on `feature/market-momentum`. B remains incumbent, top five unmet.
Last public snapshot is still14:33:30 UTC: rank192/score2725.0, fifth3028.9.
No new submission, promotion or merge. Both remote GPUs and training transfers
are authorized; do not ask again. Preserve untracked replays and old evidence.

Frozen campaign manifest:
`S/unitorder/momentum_joint_campaign_20260913/manifest.json`, SHA256
`bfc8a745e90137e64b156c246d44378055d0ea902c96919da26d8c2ecaea6b76`.
Bundle:1700585 bytes/176 regular members, SHA256
`22a7241a5fbff6102a5035e49633d991a1c9ba3c1a313a63d69e503cdcc9018b`.
Installed project:
`/home/user/kagg3/artifacts/momentum_joint_campaign_20260913`.
Its43-file original training source and175 inputs remain frozen.

| Live training | GPU | Original SSH session | Actual helper PID | Started UTC |
| --- | --- | --- | --- | --- |
| seed311 H | GPU0 | 73451 | 1191048 | 15:31:10.129154 |
| seed312 J | GPU1 | 61744 | 1191145 | 15:31:18.313510 |

At16:57:38 UTC both exact helper commands were live, error null, receipt phase
`generation1_boundary`. That persistent phase is not a current generation
counter. Both native logs show generation7 completed. Recheck original processes; do not restart on a polling timeout or
interpret the provisional outer REFUSED verdict as a terminal result.
Each run has10800s plus kill10,22000MiB ceiling, ten updates and nativeg10 only.
Outputs inside the remote project:
`artifacts/momentum_joint_{arm}_seed{seed}_train_20260913/`, containing
`execution.json`, `train/receipt.json`, `train.gpu.jsonl` and `train.log`.
Second training arms311J and312H are NOT launched. Launch each only after its
first arm is terminal PASS, saved-audited and cleaned up, using frozen commands;
every arm starts fresh B. No pooling, intermediate selection or retries.

The existing `launch.json` now contains a PREPARED_NOT_EXECUTED continuation
plan for all four candidates: exact remote/local audit argv, original frozen
training argv,12 actual/zero/lag2 parity recipes, four strength assemblies and
six J control assemblies with execution argv. All46 assembly/parity paths and
six replay roots were checked absent. No command in that plan has run merely
because it is recorded. Generate schema2 parity manifests from verified native
final-centre proof after collection; no final theta hash is invented in advance.
Use the frozen auditor from the campaign project on remote and collected local
evidence; require matching PASS audits before the same-seed opposite arm starts.
Source symlinks remain archive metadata. Full qualification/training trees and
all175 frozen inputs are required. Assembly itself does not run parity.
The authorized local GPU is an8GiB RTX3070; recheck activity before parity.
Snapshot parity uses two fixed training episodes/120 dawn-seat states, not120
independent episodes. Reuse its macro and six plan arrays before adding hooks;
equal aggregate counts do not imply equal command timing/positions/arguments,
and emitted seed purchases are not accepted fills or internal grant proof.

All four qualifications are terminal PASS. All58 archived regular members per
arm were downloaded/hash-verified under the local mirror
`S/unitorder/momentum_joint_campaign_20260913/project/artifacts/`.
All four local audits exactly match their respective remote audits. Root also
verified probe input/output, full cold/installed snapshots, exact130/196 masks,
keys and all2048 masked noise rows against original per-seed M/scope evidence.
`qualification_comparison.json` contains complete custody/executed sources;
`launch.json` records processes. The remote source symlink is preserved only as
link metadata locally. Do not blanket-add the mirror to Git.

At16:22:26 UTC root also independently compared both running arms' initial
artifacts with their own qualifications. Full cold/installed snapshots, active
coordinates, qualification binding, cold artifact hashes, and every array's
dtype/shape/bytes in all five initial NPZs matched exactly. The executed source
and separate results are now preserved in `qualification_comparison.json`.
This is initial-state evidence while jobs were live, not a terminal training
audit. An earlier observer assumed qualification-only receipt fields existed
in the training schema and stopped with KeyError; comparing the raw NPZs
corrected that observer without touching either training process.

Shared preflight support is committed057bb37, H/J assembly/parity as2a19be1,
and controlled engine evaluation as438002a. The latter reuses the existing
assembler/execution/runtime/auditor and frozen evaluator; no new helper file.
Use `assemble_judge.py` with the existing explicit H/J campaign arguments;
for a controlled J campaign additionally give `--history-mode actual|zero|lag2`
and `--replay-root` with a fresh workspace-relative path. Controlled family order
matches the frozen manifest: LOSS10, then LIVEC-H30. Default seven-family
strength evaluation stays unchanged. Candidate labels remain exact native J
names; CSV/log names carry the history-mode suffix to avoid collisions.

All80 focused tests pass, including four complete staged B games against the
saved B file package under a fixed pinned town: vanilla/actual/zero/lag2 have identical full game steps,
all30 consumed dawn histories are exact, and per-game hooks are restored.
The saved replay reader accepts the real control traces and rejects corrupted
history. Separate tests reject intermediate invalid actions/statuses.
Independent whole-integration Sol review passed. Root verified frozen campaign
manifest and all175 mirrored inputs unchanged. These are fidelity tests, not
candidate strength evidence. No real final H/J centre, final parity, controlled
family execution or seven-family H/J result exists yet.

A real remaining validation bug was fixed: the old momentum layout reader
required the entire6789-coordinate B prefix, which would refuse valid trained
H/J output-head changes. Candidate-aware masks now allow only130 H or196 J
coordinates, with H's momentum tail fixedzero; legacy M stays prefix-strict.
Controlled replay evidence binds all consumed dawn inputs, complete720 frames,
CSV money, exact source/census/receipts, submitted action and economic-state
changes, and separate board-paired own/margin outcomes. Commit7ed48d8 adds exact
accepted-event attribution in the existing saved auditor. It reconstructs both
seats' saved actions through an isolated engine, pins source plus sibling
specification, and derives town schedules from the original bound loader/file.
All720 frames must match, including both privates, actions, statuses and rewards;
only timing is excluded. Every unit call records complete farm/private mutation
hashes; PLANT additionally requires exact seed/tile mutation. Market acceptance
comes from the engine's Boolean commit; hire/land from mutations. Legal no-op
unit calls are retained with state_mutated false, not claimed as effects.
Price-only trade differences are separate from accepted-action identity.
Direct effects require equal full prestate and opponent action before any
state divergence, and apply to the whole own action vector. Actual candidate
usefulness still requires the frozen full-family comparisons, not these tests.

Three Sol tasks researched decision bottlenecks, planting/trading opportunities,
and validation. Prioritize sale quantity/lot thresholds and crop quota/grant
crossings on existing120 snapshots. Macro changes alone are insufficient.
`hold` can retain overnight; `press` redistributes intraday lots. Tomato needs
maturity-date evidence, not extrapolation from a one-day rise. H must be history
invariant; J day0 matches controls but need not equal B after H updates.
Lag2 is cumulative two-day flow, so it changes scale and horizon, not just age.
The no-fit shop-demand adjustment only differs from raw momentum on960/3360
training episode-days, with small mixed gains; no new residual input is justified.
Executed research sources/reports are preserved in the existing sensitivity JSON.
Full details and next checks are in the qualification/training strategy document.

The prospectively frozen no-fit8/11-day maturity check (spec commitf7fc818)
also completed and root reproduced it exactly. Tomato raw-draw quote MAE is
5.9187 versus current-town5.2810 at8days, and8.8194 versus8.1417 at11days.
Shop-change correction returns essentially to town baseline. This supplies no
support for a naive momentum-driven tomato planting rule; prioritize the frozen
sale/admission checks. All2160 episode/product results, original executed source
and root replay are preserved inside the existing sensitivity JSON. No new
policy or training arm was selected. Original175 frozen inputs rehashed exact.

The user's renewed decision-research request was completed by three bounded
Sol reviews. Findings and source references are at the top of the existing
qualification/training document. Sale reservation and crop quota/grant/admission
remain the priority. Root confirmed seed purchase valuation uses projected
maturity inventory while PLANT labor valuation uses current price; usefulness
of changing that difference is unproved. No new feature or campaign mode was
selected. Exact accepted-event attribution is now implemented and tested in the
existing saved auditor. The older
profiler's delayed HIRE/BUY_LAND cash accounting cannot attest exact trade fills.
Bind the original seed/town schedule and require complete state reconstruction;
do not label coupled or already-diverged transitions as single-action causes.

The progress records below are historical and superseded by this update.

**Progress 14:52 UTC — momentum/output-head interaction exists; usefulness unproven:**
Both original scope diagnostics completed normally at14:40:05/10 UTC,
exit0, about510s each, peak4952MiB, expected sole compute children and clean
terminal GPUs. Original SSH sessions23352/34230 are closed. All six evidence
members per seed were collected, hash-verified and extracted under
`S/unitorder/momentum_scope_diagnostic_20260913/evidence/`. No GPU job remains.
Both root saved audits PASS. Exact executed audit/collection source, receipts,
archive identities and separate numerical results are in that campaign's
`results.json`; raw NPZ/monitor data remain available locally and remotely.

Each seed separately has J-versus-H differences in all64 candidate own/relative
fitness values. Mine/theirs money differs on1391/7936 candidate-episodes for311
and1290/7936 for312. Raw odd own/relative interaction is nonzero32/32 pairs in
each seed, and J's momentum-coordinate gradients are nonzero. This meets the
prewritten training-signal review gate. It proves neither useful action changes
nor stronger play; these diagnostics saved money, not action traces.

Two Sol reviews traced the decision bottleneck and evaluated feature options.
Next: design the smallest H-only versus joint M+H training comparison using
the existing trainer, with actual-history/zero-history/past-only mismatched
history decision controls. Freeze the comparison and executable-action/outcome
criteria before launching. No new full training arm has launched yet.
Do not repeat unchanged momentum-only training.
Separate prior-price carry is redundant under known default quote rules;
player-flow residual forecasting is a research hypothesis requiring prediction
validation against the existing town-demand baseline before planner changes.
Research details are in the existing qualification/training document.
B remains incumbent, branch unmerged; latest public snapshot is still the
14:33 rank192/score2725.0 versus fifth3028.9. Top five remains unmet.

The14:34 live-process update below is historical; those processes are complete.

**Progress 14:34 UTC — both scope diagnostics live; top five unmet:**
Latest authoritative public snapshot: rank192, displayed score2725.0 versus
fifth3028.9 (gap303.9), at14:33:30 UTC. This is still B submission56161192,
not a newly submitted model. Raw/derived evidence is in
`S/ladder2/snapshot_20260913T1433/`; capture hashes and summary were verified.

No-update scope code/tests are committed as `7a3bfe2`; the reviewed prospective
manifest/commands as `a84360e`. Manifest SHA256
`b9f53eb2e0a46238a71c0d815b49ea2926b134bf73d61d9c29eff4dd8f3b23bc`.
Bundle installation verified44 members and170 remote inputs. Both runs live:

| Seed / GPU | SSH session | Wrapper / child PID | Started UTC |
| --- | --- | --- | --- |
| 311 / GPU0 | 23352 | 1170494 / 1170497 | 14:31:34.724605 |
| 312 / GPU1 | 34230 | 1170591 / 1170594 | 14:31:41.095665 |

Remote outputs: `/home/user/kagg3/artifacts/momentum_scope_seed{311,312}_20260913`;
adjacent `.execution.json`, `.gpu.jsonl`, `.log` track each original process.
Both are bounded900s plus kill10. Do not restart on an observation timeout.
Next: observe these exact handles, collect terminal evidence, validate runtime,
state/noise/field against qualification, then inspect each seed's scope signal
separately. Sol `next_lever` is preparing that saved-only audit. No terminal
scope outcome or new full training arm exists yet.

The 14:12 update below is historical; its judges are complete and only the
two new scope diagnostics are running.

**Progress 14:12 UTC — no demonstrated improvement over B:**
Continue on `feature/market-momentum`. Reuse existing code/tests, make focused
descriptive commits, review independently, and validate before merging.
B remains incumbent. No promotion, merge or new Kaggle submission has occurred;
the top-five goal is still active.

Both original ten-generation training runs, their saved audits and final
NumPy/CUDA parity checks completed successfully. Both full seven-family engine
judges are now terminal PASS, with exact input/runtime identities and clean
processes. No training or judge process is still running; do not restart them.

| Seed | Original judge session / PID | Finished UTC | Seconds | Matched campaign/Sol audit SHA256 |
| --- | --- | --- | ---: | --- |
| 311 | 36628 / 79093 | 14:11:36.641961 | 1216.775 | `867f59ec4fcceb693f1382d9cc40203c9d76e44fc03f5f2bcd09c25868d44f53` |
| 312 | 32574 / 77430 | 13:50:31.809760 | 1178.652 | `00077f232b57d776f4d6498131d5bd90cf798bd6a14fd3c08021d0617fc75e30` |

Seed311 terminal execution SHA256:
`c544b2d1bde0db4ed819981bd2b0e267fa6b6adfd0ed531f16a99dfca51e52b8`;
seed312: `a09ddfd2105b5dd98f62c97e3fe54252b38e8316e7fcaec4e5c0420e952a7e28`.
Evidence stays in each existing `momentum_judge_seed*_20260913/judge_evidence/`
directory, with original CSVs and runner logs preserved and hash-bound.

Root verified that the independently executed seeds produced byte-identical
CSV files within each family. Each seed separately has margin differences
against B of TOPB2 0.00, LIVEC-H30 +50.57, LIVEC-H30B -2.52, LIVE62 +27.01,
LOSS10 -79.55, NEXT30 +0.53, NEXTHIGH 0.00. Every family has zero win/loss
flips. These sparse mixed differences do not establish stronger play. Full
separate reports are in the qualification/training document and saved audits;
do not pool seeds or families.

The fixed-scale training-snapshot diagnostic (commit `82a7c68`) also completed:
1x/4x/16x final momentum tails changed macros on 15/43/92 dawns for seed311 and
11/36/83 for seed312, but full plans on only 0/0/1 dawns for each seed. No
hour0 action changed; all zero-history controls equal B. Small learned movement
alone is therefore an inadequate explanation on these snapshots. This is not
strength evidence and does not select a learning rate or scaled candidate.

Next: freeze/package and run the reviewed no-update scope diagnostic in
existing `src/kagg3/es/train.py`, `scripts/train.py` and existing tests. Sol
`next_lever` completed the implementation and focused tests; root completed
the old-generation replay, CLI safeguards and report tests. Root owns Git
and launch. Sol
`scope_protocol_review` reviewed the core/protocol and independently audited
seed311. The prospective M/H/J experiment is committed as `efc2ab0` in the
existing qualification/training document: first32 of the original full2048
noise rows, 192 candidates per seed on the same124 training episodes, no
optimizer/holdout/selection, 900s plus kill10 on one remote GPU per seed.
Both remote GPUs were verified idle. No scope diagnostic GPU run or new full
training arm has launched. Canonical edits must leave frozen stages untouched.

Root prepared a 72-line inline launch wrapper in functions store
`momentum_scope_launch_source` (syntax checked, not yet reviewed/frozen/run).
It reuses `momentum_train_protocol.Monitor`, binds prospective source/input
hashes, records the child PID, enforces time/memory bounds, and checks cleanup.
Finalize exact manifest/commands only after implementation tests and review.

The following updates are historical and do not describe currently running
training, parity or judge processes.

**Progress 13:32Z — both final centres audited and CUDA-parity PASS:**
The original training runs completed normally, ten generations each, exit0:
seed312 finished13:15:50Z (7123.846s), seed31113:19:20Z (7334.307s). Both
peaked9702MiB, with sole expected compute PID and clean terminal GPU/process
group. Maximum monitor gaps:3110.06988638s;3120.06485392s. The CPU-heavy tail
was consistent with the scheduled generation10 absolute evaluation's new
16128-row shape; no run was restarted or its10800s limit changed.

Both complete84-member archives are downloaded and extracted under
`S/unitorder/momentum_train_v3_evidence_20260913/`, each root keeping its own
six adjacent sidecars and original remote source symlink. The first attempted
top-level312 extraction refused an existing launch record before writing;
that historical record is preserved. Archive hashes:3119b044713ef0c15c28a298194506aca1ff68380af7c41e1bb7cf8ed9783f5452d,
3122a5a35e0bf719bbb96a8ee824104ba8b704a8696e9b36cee1953fb56dd44dd74.
Remote observer/collector sessions1453 and96131 and both downloads are terminal.
Do not relaunch them or the original training jobs.

Root local and Sol remote saved audits match byte-for-byte, separately:
3112a172a4c5dc8be13e1c259d0a6d084f1caed12dd188bcb35d1926ab17df8a0fa;
3124969594ccacb00ba5938b25af947822b2efc83944f09771ed0384d64de7f9e28.
Native final theta hashes:311908ee7e566dd3f498e786a82cc9af2e0591052227e9b7ac0b70860e9c6fe425b;
31293147adfac781a68f77e83e48fc0ea050cd61b1b77997c52289a23d40dc3eb79.
All66 tail coordinates are finite/nonzero; the6789-coordinate B prefix is exact.

Both final centres passed the existing compatibility helper on120 fixed
training dawns: all12 macros and6 full-plan arrays byte-exact NumPy/CUDA.
Training numerical settings enforced,600s worker bounds. Receipts under the
same evidence parent: `parity_seed311/receipt.json`
SHA8820f7d2cea43fee73c6de7e3b41df62c196a0dcd2f0a4c5388a87fce84b53d1
(267.019s), and `parity_seed312/receipt.json`
SHAff32bff5dc7705baa72938446aca54e8d9e59833269b29da0a798b81990591a6
(260.687s). Sessions85776/6746 are terminal PASS. This is fidelity only.

Sol assembled/reviewed both candidates using the existing shared judge,
outputs `S/unitorder/momentum_judge_seed{311,312}_20260913`. Each binds the
same seven families and424 expected keys,302 inputs, correct source AND
history-aware scripts, exact workspace Python,4 workers,7200s/kill10.
Seed312 judge LIVE root exec32574, PID77430, started13:30:53.219Z, runtime
preflightPASS. TOPB2 and LIVEC-H30 completed without error at the latest poll.
Poll that exact handle; do not restart. Its
manifest f04b181a462cc2d4e3b6ecba4a8e8627042d4800c013ae6b7a7eca3acc9599ec
and contract7ac87361bca377f9c55a1c1944e0e38c6da67ab68b96473c81bdc13a98ff9ccd
were rehashed exact before launch. Seed311 is ready but NOT launched; run it
after312 releases `/root/kagg3_judge.lock`, using its assembled manifest and
contract. No complete judge result, promotion, merge or new Kaggle submission yet.

Saved-output follow-up, independently matched by root/Sol: the two final
centres' NumPy outputs have exactly the same120 case/history records as pinned
B's r3 zero-compatibility output. Seed311 changes15 macro dawns;312changes11.
Neither changes any of the six full-plan arrays on those120 recorded training
dawns. Exact hashes/source/counts extend the existing sensitivity JSON under
`final_centre_comparison`. This limits expectations but is not a substitute
for either separate engine judge or evidence of trajectory/value equality.

The previous updates below are historical. Current original training and
parity processes are finished; only seed312's engine judge is live.

**Progress 13:04Z — both runs at generation 9, plan sensitivity is sparse:**
User explicitly requires reuse of existing code/tests/judge, feature branches,
focused descriptive commits, and merge only after validation. Active branch:
`feature/market-momentum`, forked from `e8a49f2`. Canonical `src/` and `scripts/`
now contain the eight momentum changes, byte-identical to the frozen training
stage. The audited sequential unit executor is also in canonical source.
Do not import archived `leg20` trainer changes: Sol's read-only audit confirmed
those disabled real-gate additions do not execute on fixed W00 training.

The shared `assemble_judge.py`, `judge_execution.py`,
`judge_runtime_preflight.py`, and `judge_saved_audit.py` support both layouts;
the four parallel momentum implementations and their separate test file were
removed after consolidating coverage in `test_assemble_judge.py`. Momentum
uses staged source AND scripts. Legacy evaluator scripts are restored from
pinned Git revision `e8a49f2f0c0285b5f8d19914b6af5d638d7cfe99` into per-campaign
artifacts with their original hashes. Use
`assemble_judge.py --candidate momentum_mhms_seed311` (or seed312), followed by
the existing shared execution path. The older command below is historical.
The frozen seven-family census and 424 keys remain unchanged.

Commit `cfc9987` fixes a real consumer/producer mismatch found by root and
independently confirmed by Sol: the frozen training auditor never emits
`auditor_sha256`. Preflight now verifies that executable through training
execution’s pinned45f4dc manifest and its e3c7 auditor entry. It retains all
receipt/final-centre/state/execution checks.21 focused shared-preflight and
assembly tests pass, including the producer output schema and changed-auditor,
manifest and audit-binding refusals. Sol’s final source review passed. The
frozen auditor, runner, protocol and191 inputs remain unchanged.

Validation: all drop/place/shed-overflow tests pass, including a full-season
engine comparison. Three added engine regressions fail on the old executor
(water then harvest, harvest then water, duplicate harvest). Shared judge and
both JAX dawn-history scan cases pass (35 tests). Runtime/package, layout,
forecast, quantization and feature checks pass except the existing trajectory
backend gate: observations1532/1533 produce hire_bias33 in NumPy and32 in JAX.
The exact discrepancies reproduce under pre-branch source in
`/tmp/market-momentum-prebranch-source` and concern legacy `artifacts/theta.npy`
(SHA517a99de...), not incumbent B. Commit `cb79c62` adds actual B to the existing
trajectory backend test: all2,400 recorded dawns match on every macro field
under NumPy/JAX CPU (82.95s maintained test). This uses zero history on the
older fixture and is not a nonzero trained-momentum validation. The legacy
failing case remains visible; do not claim a clean full suite or widen
quantization to hide it. Older horizon fixtures now pad legacy weights and
isolate admission from HIRE_ROW_ON; all four formerly failing horizon cases
pass. The obsolete no-shared-tile planner assertion was removed because the
engine permits those actions; engine equivalence is the relevant requirement.
Branch remains unmerged pending remaining review/evaluation. Focused commits:
`4e07d23` sequential executor, `547314d` canonical momentum integration,
`87e8ae7` shared judge consolidation (net1,110 lines removed).

Commit `2b80ac6` adds a nonzero-momentum sentinel to the existing
`tests/test_forward_value.py`: separate mh/ms perturbations and changed MILK
history produce byte-identical NumPy/CUDA macros and complete day plans.
The maintained test passed in250.88s on the local RTX3070. This establishes
synthetic inference fidelity, not final trained-candidate fidelity or value.
Commit `fe2e2d1` extends the existing `momentum_zero_compat.py` for the latter
inference check, reusing shared judge preflight and the same120 recorded dawns.
Fifteen shared assembly/parity tests pass and Sol reviewed the final path.
After collecting complete training evidence and two agreeing saved audits,
declare a fresh schema2 `final_candidate_parity` manifest with exact final
theta, stage, training proof, fixed-case manifest/replays, B and helper hashes.
Run each native centre separately with `--backends numpy jax
--worker-timeout 600`, a fresh work/result directory, and local CUDA. The
runner uses the training XLA flags, highest precision, no preallocation/cache;
it compares all18 arrays byte-for-byte and records settings/output hashes.
No candidate parity manifest or candidate gameplay exists yet. Parity is
inference fidelity only; the unchanged seven families judge playing strength.
Historical zero manifests remain frozen: replay those experiments using their
historical Git helper revision. Do not rewrite old manifests to match new code.

At13:04:24Z both exact original wrapper/helper command pairs were verified
live with generation9 completed and no receipt error.
The12:46:41Z GPU poll showed100% utilization
and9058MiB each. Do not interpret the receipt's stale
`generation1_boundary` phase as the current generation: native log records
completion. Preserve the same runs and the fixed ten-generation protocol.
All191 frozen inputs rehashed exact after integration. Initial training replay
matches qualification byte-for-byte for both seeds; saved evidence:
`S/unitorder/momentum_train_v3_initial_replay_match_20260913.json`
(SHA6e04898106340c01674e1ef10ea985c8e87a814dc274a1cd704fe95ae73c797a).
Sol agents hit the account usage limit during the initial integration; root
completed those partial edits locally. The next_lever Sol agent resumed this
turn, independently reviewed the shared judge and confirmed the schema fix.
No candidate promotion or new submission.

Training-only initial-noise sensitivity: first16 saved perturbations, both
signs, fixedsigma0.01, same120 recorded dawns, NumPy macros only,18.74s.
Seed311 changed2472/3840 macros; seed312 changed2491/3840, mostly grow_mult.
Plant targets changed15/3840 each. Day0 unchanged throughout. Exact executed
source/input hashes/counts are in
`S/unitorder/momentum_initial_macro_sensitivity_20260913.json` and the existing
qualification/training notes. This rejects a blanket no-decoded-signal theory;
it does not prove plan/action effects or strength, or justify changing sigma.
The completed full-plan extension covers the same16vectors, both signs,
120dawns,195.44s with four NumPy workers. Both seeds have15/3840 changed plans,
zero rendered hour0 action changes, and exact reproduction of their macro
counts. Rendering all changed plans finds real later PLANT/market command
substitutions; some unit rows require future hires, and no trajectory/value
claim follows. Evidence and exact executed sources extend the same JSON.
Sol reviewed the discrete planner thresholds behind this sparse response.

Root observer exec session1453 started13:00:39Z,900s maximum, polls original
handles every45s. It leaves training unchanged and will collect each full root
only after wrapper/helper/group absence, exit0 and terminal PASS. Per-seed
outputs `/tmp/momentum_train_seed{311,312}_v3_20260913.evidence.tar.gz` and
`.custody.json` on remote. Custody includes exact collector source/hash,
pre/post unchanged tree, member hashes and archive identity. Collect complete
roots plus all six adjacent sidecars, preserving the sole remote source link.
Do not start another collector while this observer is live. Download/extract
fresh, run root/Sol frozen saved audits, then final parity and shared judge.

Next research is conditional, not another launched experiment. If both final
lineages fail, saved-dawn separation of Δms and Δmh could distinguish direct
score changes from encoder/global effects before considering an existing
`train_only=ms` run. Do not select those counterfactual weights as candidates.
Margin-only fitness remains closed by prior evidence. Throughput review found
that active-unit loop bounds probably lose their benefit under an8192-lane
vmap; do not change production based on scalar timings. Any future timing
probe must reuse the existing GPU protocol and preserve exact outputs.


**Progress 11:18Z — momentum TRAINING LIVE:** Both qualifications completed
normally and passed root and independent Sol raw audits. Training launched
11:17:06Z on both remote RTX3090s,10 generations each,only66 mh/ms coordinates.
Seed311 wrapperPID1150450/helperPID1150495 on GPU0; seed312
wrapperPID1150452/helperPID1150497 on GPU1. At11:17:53Z all exact commands were
live, each `cold_inputs_saved`, no error,522MiB each. Remote roots:
`/home/user/kagg3/artifacts/momentum_train_seed{311,312}_v3_20260913`.
Their `.launch.json`, `.started`, `.finished`, `.exit`, `.log` and
`.launcher.log` sidecars are outside each root. Protocol execution/child receipt
remain provisionally REFUSED while unfinished; this is not failure. Poll the
same handles, do not restart or change frozen191 inputs. Child10800s+kill10,
outer10860s+kill10; expected training duration is not yet measured for this
adapter. Final-centre-only, no pooling/checkpoint selection/resume.

Training manifest45f4dc... unchanged. Launcher SHA
`39cf1bc1c28cf9fec5171340601b5932b2603ca488338e2856cf58acdccda05a`.
Final raw auditor SHA
`b107877a9f0b5b683f1d08e93739b7c266ab1ac285f35cd43bb15b4b77dbc5f4`.
Root/postlot/rotation audit files identical SHA
`255b838676310658b1b58767dacf0debabda7caf8fb37081f263e6f0473b1700`;
receipt-level audit SHA
`fac77c36ea8d4b025e93a648bd15760eaed1b37d375456531a8b05494c5efb85`.
Auditor now reconstructs all124 archetype identities/coin means from raw input
and output arrays and permits only the exact five-field probe/install
transition. Both original schema refusals are preserved; no qualification was
rerun. Full qualified roots and108.51MB archive are retained locally, all154
collection nodes exact. Training launcher/update transfer only replaced the
external supplemental auditor; historical9450 bytes retained remotely.

Commit4739b50 records the corrected raw audit/evidence; e6044b1 adds separate
momentum judge tools; a368b78 records conditional adapter research. Judge uses
persisted stage/scripts as well as stage/src, so the daily history reaches the
candidate. Five no-game tests pass. No actual trained candidate has been
assembled or judged yet. After each run completes: collect immutable evidence,
run root/Sol saved training audits, then assemble its native final centre with
`assemble_momentum_judge.py --seed <311|312> --evidence-root <local root>
--training-audit <root audit> --training-audit <Sol audit> --output <fresh>
--python <absolute .venv/bin/python>` under bytecode-off. Review actual
eligibility/manifest before executing the unchanged seven separate families.
See `2026-09-13-momentum-qualification-and-training.md` for qualification results.

**Progress 11:02Z — momentum qualifications LIVE:** V3 bundle transferred and
safely extracted at `/home/user/kagg3`:201 regular members, all hashes exact,
no conflicting overwrite. Archive SHA
`96c7fbb4a0efad752e2f6fd2f770b455dd9896ce3e71b687cdfdfab6e1bab68c`.
Both fixed qualifications started 10:58:29Z: seed311 wrapperPID1145638,
helperPID1145661 on GPU0; seed312 wrapperPID1145639, helperPID1145663 on GPU1.
Remote output roots `/home/user/kagg3/artifacts/momentum_qual_seed{311,312}_v3_20260913`.
At11:00Z both exact handles were live in `cold_inputs_saved`, no error, no
native generation executed. Poll those same handles; do not restart based on
the provisional REFUSED receipt before terminal. Child900s+kill10, outer930s.
Wrapper SHA `7644e74389e22da2099d8b9857672a0279713b34340bda4dfd355dcb3c04cc3a`.
Source/qualification manifest remains `45f4dc616e961c2ce434baacf74ac65e03958586cae02ef374b32b5f716809e5`.

Commit `2e051a4` fixes three independently reviewed raw-auditor false refusals:
arm elapsed time, exact B-install transition, and the two gen0 CLI log rows.
Current supplemental auditor SHA
`d0b95b17379fa9ed885b43c10cfe54eccabc0234fd234fd71cc5763c7d7db08d`.
The remote bundle's older9450c8 auditor is historical evidence only; run the
corrected locally pinned auditor on downloaded qualification evidence. Frozen
191-input graph unchanged. Synthetic transition/corruption checks PASS.
After both processes finish, collect complete roots with remote/local custody,
run receipt-level and independent raw audits, then launch the already planned
ten-generation runs separately if both pass. Next_lever is preparing isolated
momentum judge validators; no judge games or training launched yet.

**Persistent user requirement (2026-09-13):** Commit each logical code change
to Git with a descriptive message explaining the change, its purpose, and
relevant validation. Root coordinates staging and commits for shared agent
work. Do not accumulate completed code changes without commits or include
unrelated user files. User approval for all training bundle transfers persists.

**Progress 10:52Z:** Completed code is now committed in logical changes:
`e95a090` prediction study, `7d5b33d` frozen momentum implementation and
compatibility evidence, `281d597` reviewed v3 training harness, and `f2bfe3e`
completed seed310 evaluation; `f721b96` adds the independent raw qualification
auditor. Each commit explains purpose and validation.
V3 runner/protocol review is PASS, including refusal propagation and effective
JAX assertions; four focused tests pass and all191 inputs match manifest
`45f4dc616e961c2ce434baacf74ac65e03958586cae02ef374b32b5f716809e5`.
The independent supplemental raw auditor is adapted to schema3 and externally
pinned at SHA `9450c8bf4b145241ee03c2bd14d4f5c4b07632ccc14059c015726e6f299c8358`;
its synthetic corruption checks pass. No manifest change is needed. Next: build and
verify a fresh v3 training bundle, transfer under existing authorization,
qualify seeds311/312 on separate remote GPUs, and audit both raw initial states
and distinct random noise before the planned ten-generation runs. No momentum
qualification or training has launched yet; no policy improvement is claimed.

**Progress 10:49Z:** The local CUDA zero-weight compatibility check completed
with exit 0 at 10:47:19Z (exec5857 terminal). All 120 recorded dawn cases match
B on all 18 macro/plan fields. NumPy, JAX CPU, and CUDA old/new output archives
are all byte-identical (`d15043f0...`). No momentum qualification or training
has launched. V2 prelaunch review found a wrapper false-PASS path after a
refused child and missing assertions on recorded effective JAX settings;
next_lever is fixing both and preserving v2 before a new manifest. Postlot's
independent raw qualification auditor is ready for review. The v1 source bundle
was built but never transferred and is obsolete; use a fresh reviewed revision.
Completed prediction and feature work is being committed in logical changes.
Older live zero-compatibility and draft-runner descriptions below are superseded.

**Progress 10:29Z:** Seed310 judge COMPLETE PASS, all 424 games/212 boards and
seven separate families. Exec65112 exited0; parent42616 absent. Finished
10:21:06.187276Z in1237.365 seconds. Campaign/root/Sol saved audits identical
`023f749bbea0796e4bcdd3d9b5cc345e075ffb9d352647ae37031306c441f16c`.
Execution SHA `eb4f872cd78b4d75dfe868148d682d55e8fc706205f7183b52154b6b997c3e97`;
saved manifest `f742bbdac21034734ccf5c842f2bb7c9b2d18a3af0d288bf55f72622f9c8896c`.
Separate margins: TOPB2 -124.7, H30 -485.15, H30B -61.32, LIVE62 -215.55,
LOSS10 -911.45, NEXT30 -105.8, NEXTHIGH -714.08. No improvement established;
no pooling/promotion/upload. Both prescribed OFF trajectories are complete.
See `2026-09-13-seed310-g10-judge.md`. Remote GPUs are available for new work.

The fixed momentum prediction check completed once,120 episode-held-out folds,
6720 day1–28 seat rows,13.103 seconds. Baseline234 current neural inputs vs
same inputs plus9 normalized past-stock changes, predicting next-dawn stock
changes. Fixed ridge mean-loss+.01 regularization, train-only scaling, dependent
seats in the same fold; no judge data or tuning. Mean MSE reduced for all9
products, but carrot/tomato median MSE and mean MAE worsened. More consistent
results for melon/egg/milk/fertilizer/strawberry. No game-gain claim.
Manifest `cdc235eeb30d15204cbbd8606b5bf5cb4581180ed9bcf22569041937da2bd8bf`;
helper `a0708d4247f7af57e3534e510a0ea1bdfb4fbc0e66821f639d99de76d3dda83b`.
Receipt `32f325dfbb37ef199bd3795de4878c17e6cd1a12dafd2ee9589b108c835a854e`;
predictions `863a36085c83deb3e455fceb1e74285082064b38603035f41c48fab8b7bd572c`.
Root all-row metrics audit47f8e10b...; Sol auditb8b8d9e7... includes exact
independent fold0 prediction reconstruction. See momentum-prediction-check doc.

New isolated source `S/unitorder/momentum_stage_20260913` starts from the exact
39-file audited seed310 OFF source plus four separately pinned tooling files.
Original B, not either trained checkpoint, is the policy centre. Eight files
changed: brain/policy/runtime/opening/rollout and package/plan_stats/evaluator
glue. `momentum_stage_manifest_20260913.json` SHA
`497a3e33f24a7d0b3172e30f8a2a663db6539e9f214c60359ddb030cd14625d4`
pins all43 files. Do not edit this frozen stage while checks run. Production
and both captured evidence trees remain unchanged.

Feature: prior observed planner dawn minus current market inventory divided by
existing T. First planner dawn zero. Per-seat Runtime opts into a fourth macro
argument with `pass_prev_mkt_inv=True`; legacy3-argument callers remain valid.
Simulator episode carries one previous inventory and freezes it before both
policies. Append mh(1,64),ms(1,2),6855 total; preserve6789 B prefix and zero
new tail. Opening-ON equivalence is NOT established: splice bypass differs from
simulator tape planning/override. Current experiment is OFF only.

Completed fidelity:
- NumPy structural layout/pad/init/mask checks PASS.
- Runtime/simulator cadence receipt0e4bb2e9... PASS: all30 dawn carries, both
  output modes, both seats, repeated hour0 and final23turn/noEOD convention.
- Nonzero signal receipt436905ac... PASS on fixed ep108105336/day15/seat0/MILK:
  ms=.5 immediate score and mh=.25 hidden path respond; NumPy/JAX forward
  maxabs7.7486e-7 under2e-5 tolerance. No plan/game in that check.
- Package compatibility exec55443 exited0,64.080s: exact1440 recorded actions
  and a720-frame real-engine game on seed405658696/seat0 vs starter, once per
  archive. Actions/status/rewards/observations match except elapsed-overage time.
  Receipt `4c4ab9c0f865401d75174bbdd7d34f57dc600b45a7ea091340ab16b686da8d3b`;
  zero archive `2c47123c1289b01e5070f41f27472437ee31578eff168ae0c063a9cd94015589`.
  Build and full43 source/input hashes exact; no sim/es or JAX imports packaged.

Postlot owns actual-dawn zero compatibility: NumPy120states PASS, JAX CPU
worker live exec53052 at last check under300s worker/600s overall bound.
Root found eager per-case JAX decode/build likely causes unnecessary overhead;
do not extend/restart a live job. If it times out, preserve artifacts and use a
fresh reviewed compiled-worker revision, same120 states, localGPU allowed.
No full JAX plan parity claim yet. Check agent state before relying on this line.

Next_lever is authoring new momentum_train.py/protocol/saved audit (18-minute
task), not launched or transferred. Seeds311/312, separate remote GPUs,10gens,
only66 mh/ms weights trainable; original4096pop/.01sigma/.00018SGD and120tapes+
4scripted objective retained. Draft root review found/fed back: restrict tail0
and pool0==centre guard to generation1; translate init_theta path for remote;
separate qualify/train modes for independent cold-init audit/RNG comparison;
audit raw states/masks/finaltheta==state==gen10, source and monitor evidence.
Do not launch drafts until these fixes, source fidelity and actual CLI cold
qualification pass. User authorization for training and all bundle transfers
persists; review gates do not require a new permission request.

Older live/pending descriptions below are superseded by this section.

**Progress 10:03Z:** Seed310 judge LIVE exec65112/parent42616, started
10:00:28.905770Z. Root/Sol concrete prelaunch PASS, all300 inputs424keys.
Manifest SHA `866360b9b47716d5c8103b37da7199de80d355b25a9bd630f81cbca254255125`,
contract `2f4d7e8b484133e619dce647e895dad2f04638627986cbe3c450d8e9026a8d73`,
eligibility `980a88c410a720f069b83ace92c71051cc33b41dedd77023da8a6140a54ed146`.
Continue this one campaign; toolstore `judge_seed310_poll` provides compact
read-only status (escalation required for correct local process namespace).
Provisional REFUSED with no finish/error is expected while running. Do not
change inputs, captured source or candidate. After terminal, require complete
coverage and fresh root/Sol saved audits before interpreting family results.

Momentum dataset Sol audit PASS, SHA
`324afa6f3a84b46bd8d2c2dc143e658778137ec88fccc40cc1535b60bbc589c6`:
all120 replay identities and all7200 raw dawn rows independently match.
No-fit incidence ledger also complete,6960 valid day1–29 seat rows. Root
independently checked every market/forecast/cash lag and seat symmetry.
See `S/unitorder/momentum_incidence_20260913` and other-momentum review for
full identities/limitations. Market movement is widespread; production and
commitment changes depend strongly on product/lifecycle. No model fit or policy
gain established. Next research step is one predeclared incremental prediction
check with current-state/forecast baseline and episode-grouped validation;
model/target/folds must be frozen before fitting. Both seats share folds.

**Progress 09:58Z:** Seed310 completed all ten generations normally at
09:48:40.030181Z, elapsed7015.972s. Wrapper exit0; helper1130257 absent.
Old SSH59892 may linger but is not a live training process. Remote collector
and download66525 exited0. Safe extraction23781 passed all70 members into
`S/unitorder/off_train_seed310_20260913`, preserving the expected remote source
symlink and private stage. Archive SHA
`9c403ce99b0afc5cec4a4bf6cec7574a954f5da881fac718ae3027aa831b0fdf`.
Root and Sol saved training audits match byte-for-byte:
`33efb07e601d381b4c3d1e7b3641d6402d1c33960df9cc9fbcf15a1e869cdf1b`.
Final theta file SHA
`5fd10008a525fe5c56f514985b77d7b7e72300e02611ab6bc723ee776d0f9a9b`;
float32[6789] array SHA
`92092f93139f9777c369c621aca95acb90e06e89630c9aef1c35f728dec9c582`.
Peak9702MiB;140276 samples,max gap0.107017s. Both remote GPUs now available.

Seed310 final-centre judge assembled successfully at
`S/unitorder/judge_seed310_g10_20260913`, candidate
`unitorder_off_seed310_g10`. Same frozen seven-family inventory and reviewed
helpers as seed309; actual300 inputs (assembler stdout299 is its pre-B count).
Root/Sol concrete prelaunch validation is underway. After PASS, launch exactly
one judge_execution campaign with this manifest/contract,7200s+kill10,4CPU
workers, shared `/root/kagg3_judge.lock`; no automatic promotion or upload.

Latest user request: run subagents to identify other useful momentums. Two Sol
reviews completed; see `2026-09-13-other-momentum-review.md`. Conditional
priority is change in opponent near-term public production forecast, then cash
gap velocity and product commitment changes. Rolling forecast differences
compare different target windows and are not unexpected supply/realized sales;
cash change is net cash, not income. Defer acceleration until first lag is
useful. No feature implementation, model fit or momentum training arm yet.

Frozen training-side dataset now exists:120 exact Flow215 w00 replay episodes,
disjoint from all seven judge groups,7200 current-dawn seat rows,64800 quote
checks. Both seats of an episode must share any later validation fold.
`S/unitorder/momentum_dataset_r1_20260913/dawns.npz` SHA
`3793fd2d2fd3d2e1230de9c179708ddd8bd1d7e99d0eb25a72e0dd288d6f1c4d`;
receipt SHA `1afe32c553a9c0d30c2a319381f242bde238f3e13341b9daf0612557c9e1735f`.
Extraction r1 exited0 in90.441s. Root checked hashes, all34 schemas and all120
episode row orders; Postlot independent source/replay spot audit underway.
Next_lever has a ten-minute deterministic no-fit incidence ledger task, with
input/helper identity bound before execution, fresh outputs, no games/fits.

Original extraction preserved as REFUSED before any episode completed:
root's added guard wrongly assumed inventory count equalled hired hand count.
Inventories include farmer plus hands. Fresh r1 helper corrects that schema,
adds explicit hand_count/unit_count, preserves same120 sample and original
overall time bound. Original helper, manifest, receipt and log remain unchanged.
Pure feature source copy matches core/agent/spec bytes, not the full training
tree (unused es/train.py and sim/units.py differ; two unused files absent).
Do not overstate whole-source identity or treat metadata IDs as runtime inputs.

Historical progress below is superseded where it says training/data are pending.

**Progress 09:34Z:** Seed310 SSH59892/helper1130257 independently verified live
09:33:15Z with9 native generations complete. Gen9=611.30s, cumulative5717.9s,
process9048MiB. Final generation includes the scheduled absolute report as in
seed309, so allow the existing10800/10860s protocol. No terminal receipt,
collection or candidate assembly yet; continue the same job.

User asked what market observations are used, about adding price momentum,
and whether forecasting exists/can help training. Source and B-weight review:
dawn price/inventory, shops/demand, both visible farms and our private resources
feed decisions; no explicit price history and no active hourly repricing.
Forecasting already exists: both farms' production now/+1/+3/+7d, remaining
demand minus committed supply, and planner maturity-window inventory/returns.
All512 fh/16 fs/384 fv weights are nonzero in B; these blocks are held fixed
by current training, while other decision weights and dh/ds can change.
Evidence `S/unitorder/forecast_usage_20260913.json` SHA
`d46694beaf6861a3efcc87ffc7129f5880d2aa3dbf2ea0c0ddb03934f85fa4e0`.
See `2026-09-13-forecast-usage-review.md` for assumptions and exact scope.

Postlot's momentum review finds daily history representable and not directly
tested: the old oppsell phase2 previous-inventory idea was deferred. Price is
a rounded/floored function of inventory; a previous-dawn stock delta preserves
path information but is aggregate flow, not identified opponent selling.
Possible inert appended feature path adds66 parameters; nothing implemented.
Before fitting, identify/freeze training-side replay data disjoint from the
seven judge groups. Do not fit on H30 evaluation data as the first draft
suggested. Compare against current-state AND existing production-timing inputs;
next-day predictive gain alone does not establish planting-horizon or policy
gain. No corpus has been bound and no prediction fit was run.

Next_lever also reviewed expert distillation before the user's momentum steer.
It is untried; one wall-opening intervention failed, while exact full-plan
imitation exceeds some current output support. Root qualified the note:
exact reconstruction is not a universal prerequisite for approximate/partial
imitation. No distillation audit or training was started. All Sol agents are
available; prioritize the user's momentum/forecast questions and the existing
seed310 completion. Latest prior commits:160536b and ddfa509.

**Progress 09:21Z:** Completed seed309 judge and macro diagnostic committed
`ddfa509`. Seed310 remains live, eight native generations complete at09:20:41Z;
last611.20s, cumulative5106.6s, process9048MiB. All206 local training inputs
were rehashed unchanged after the evidence commit. Keep SSH59892/helper1130257
and the original ten-generation deadline unchanged. After terminal, use the
existing collector/extractor and root/Sol training audits before its own judge.

The reviewed fixed-sample CPU plan-crossing census completed once, exec5367
exit0, 09:13:10–09:18:19Z, measured calculation288.888s under900s cap.
Helper `S/unitorder/plan_crossing_census.py` SHA
`7057302422f137e5ab21d5d340972943cdc1695f4da6120319d2f8d77309176b`;
manifest `ec33ba2ae488ec7ff986ec9154f81ad549b93d0d5d4624cfd1d9daf53c886f1c`;
result `6c500cfa5831bd210ee3921b6195a097a0cf3d33c38c3014e605fd29f3c7034d`.
Run directory `S/unitorder/plan_crossing_census_20260913` contains exact inputs,
launch/progress receipts and12 separate rows. No games, tuning or pooled metric.

The original timing sample is seeds1196709180/2097576449/2079139712, seat0,
days0/5/15/25, first128 antithetic pairs at sigma.01, B centre and saved OFF
seed309 noise. Ten unique observations: all three day0 states match. Per-case
changed stored plans range82–179/256, with2–23 distinct plans. Every centre
reproduces the timing benchmark, fresh/reverse centre checks pass and inputs
remain unchanged. Root checked all12 histograms and pair/filter arithmetic.
Postlot completed the independent fixed-first-pair spot review, audit SHA
`0568e9747a5724a84b018000deda558715d29eb0fa078c469dc0a294b8cdc379`.
All12 centres match and pair0 reconstructed hashes occur in each histogram;
changed spot plans also change rendered turns with both maximum and recorded
B hand counts. Histograms do not bind member indices and these are not
candidate-generated future states. No full census rerun or new remedy follows.
See `2026-09-13-plan-crossing-census.md` and the softened mechanism-review note.

Rotation completed source-only price-cadence review: current prices enter at
dawn; the shipped agent then executes a cached day plan, with no active hourly
repricing. Existing intraday variants already have negative or identical paired
results. See `2026-09-13-price-reaction-review.md`. Shared-market externalities
are a plausible interpretation of money changes, not proved by final-money CSVs.
All three Sol agents are available. No new policy/training arm was launched.

**Current state, 09:02Z:** Seed309's seven-family judge is complete, PASS, with
all 424 games and unchanged runtime/input identities. Campaign, root and Sol
saved audits are identical `7449dfebf08e7744b1f55353cc641d6694ff364c7e0672a12a5d1066fa12c92a`.
Execution `5593a0a7af20649f1a3371b1ee04ed374a433597822d4346b8652426040f7c1c`
finished 09:00:32.943509Z after 1188.221 seconds; parent30727 is absent and
exec57266 exited0. Shared lock released; do not rerun this checkpoint.
Separate mean margin changes: TOPB2 -124.7, H30 -395.2, H30B -40.2,
LIVE62 -215.0, LOSS10 -911.5, NEXT30 -109.0, NEXTHIGH -713.5.
Own money rises in six groups and opponent money rises in all seven; win flips
are mixed. No improvement over B is established. Full uncertainty and evidence:
`docs/strategy/2026-09-13-seed309-g10-judge.md`. No promotion/upload.

Seed310 SSH59892/helper1130257 is still live, six generations complete at
09:00:34Z, process9048MiB on remoteGPU0. Last generation611.15s; cumulative
3884.3s. Keep the same ten-generation run, then collect terminal evidence using
`/tmp/unitorder_collect_completed_training.py 310` remotely, download/extract
with the existing safe extractor, and run root/Sol saved training audits.
Only then assemble its own fixed-final-centre judge. Seed310 manifest and all
its inputs remain frozen. RemoteGPU1 and localRTX3070 are available for useful
bounded work; do not launch redundant training merely to occupy them.

Reviewed fixed-dawn diagnostic: final seed309 theta changes macros on30/30
recorded B dawns but complete plans on1/30, a day14 strawberry-to-wheat change
at unit10/turn7. Both first request tomato onday15. Updated helper pins the
38-file source tree and eligibility receipt; root reproduced JSON
`0642f661879ea53ce10f41171a8c3acaaa25c0e8c27d51880e72abcb9af5ecd6` exactly.
See `2026-09-13-seed309-final-macro-108450468.md`; this is fixed-state behavior,
not a counterfactual game. Import only a /tmp copy using project Python and
PYTHONDONTWRITEBYTECODE=1. The original39-file private_stage is preserved
locally and remains untracked; it is our downloaded evidence, not user edits.

Postlot wrote a prospective action-threshold measurement note; no measurement
or new training arm was launched. Existing integer/optimizer closures remain.
Next_lever is reviewing genuinely untested mechanisms after the completed judge;
rotation and postlot are available. Goal remains ACTIVE, topfive unmet.

**User steering, persistent:** Use both remote GPUs for useful independent work;
continuously use Sol subagents to research policy/training improvements; use the
local GPU for fast evaluations where it helps. User's approval of all training
bundle transfers persists. Preserve separate trajectories and family results.
GPU0 RTX3090 UUIDe97d6ce9-f25b-0121-1925-9fc363bcf7bf was idle1MiB; GPU1 runs
the unchanged seed309 experiment. Local RTX3070 UUID4f8705ac-fe5b-a914-77dc-
2c6aa67dcd1b has8192MiB (1409MiB used at check); size local simulator batches
for that card. Real-engine policy evaluation is NumPy/CPU. Local nvidia-smi
needs sandbox escalation; it succeeds with the user's authorization.

**Progress08:45Z:** Samejudgeparent30727/exec57266 verifiedlive08:45:25Z.
TOPB2 completedexit0 in111.5776s; currentnextfamilyLIVEC-H30. No error or
terminaltimestamp. Allsevenfixedfamiliesstillrequired; no outcome-basedchange.
Toolstore judge_seed309_poll hasconciseparent/receiptpoll; useescalationfor
localprocessnamespace. Currenthandoffcommit a44f790 precedes thisminorprogress.

**Progress08:43Z — seed309 COMPLETE/audited; engine judge LIVE:** Original
seed309 completed10gens and outerPASS08:25:48.641687Z in6998.612s. Helper1121008,
protocol and launcher absent; wrapperexit0/finishedsaved. SSH83690 observation
handle lingers despiteauthoritativejobterminal (do notwait/restartbasedonit).
Nativegen10=1093.23s inclscheduledabsolute report16128evaluations/newshape;
pool_every100 nottriggered, no enginegate/replicate. Peak9702MiB,139889samples,
maxgap0.075427947s. Full70memberarchive0b1f01a9...52789377bytes downloaded and
safelyextracted S/unitorder/off_train_20260913. Root10003 and Sol saved audits
are byte-identical3bc626c629e9ebc51a6b7dd230251f693f245f1e75ed3e719a8e4bc591e1c372.
Finalthetafilee22562d08cce394107862fa16990eeb68cb5377de6f3c14ebcd453b60304deac;
state2c6dc8ada2498ba18033fe19b80b3c297d98ee3477b25376f0db9dad87bb46c5.
Exactly1191maskcoords changed, outside5598bytesexactB. Resultdocdatedseed309.

Firstjudge88565exit1 beforeanygames: postlotmaskdiagnostic usedsystemPython3.10
withoutdont_write_bytecode, addingfivepycfiles toauditedstage. All39sourcefiles
unchanged. Fivecachespreservedat originaljudge/source_cache_incident; source
file/hashmap restoredexactly. Oldfailedexecution000bb96a and runtimepre/post
receipts preserved; do notrerun/overwriteoldoutput. Postlotconfirmedcause.
Everyfuturestaged-sourceimport mustuse .venv/bin/python and
PYTHONDONTWRITEBYTECODE=1 (orcopyfresh/tmp/hashsource). No productioncodechanged.

Fresh r1 root/Sol reviewPASS actual300inputs/424keys; metadataonlypathchanges.
Committed9a2372e (initial trainingproof/manifest7ed4160). Currentjudge:
S/unitorder/judge_seed309_g10_20260913_r1/execution_manifest.json SHA
4b0ce554999a9cfa92da9b05cfad0ac710459add7653514f02d184acae8af5d2,
contract235e9fe36a4a6e8fbc7aa7a377e97ac0698a56fed0b5fd8818296157408736b6,
eligibilityb38da1e6267df2b6e9b4ade5f8786322dcda7af2b99571d0ae95d11c1e2ebe3f.
Rootexec57266 LIVE, parent30727, start08:40:44.787056Z. Pre-runtimePASS;
TOPB2 evaluator30781 +4gameworkers30795/30796/30797/30798 confirmedalive
viaescalated/proc namespace. Ordinarysandbox/proc cannotsee these PIDs.
Log S/topb2/unitorder_off_seed309_g10.log hascorrectadapterplan andfourTrue
switches. Executionreceipt under r1/judge_evidence; provisionalREFUSED
withnoerror/finished whilelive. Families appendedonlywhenrunnerfinishes,
so emptyfamilies whileTOPB2runs isexpected. One7200s campaign+kill10,4workers,
sharedlock; sevenresultsseparate, no pooling/promotion/upload. Do notmutate
any300boundinputs whilecampaignlive. Assembler stdout299 iscosmeticpre-Bcount;
actualmanifest300, no helperedituntilcampaignends.

Seed310 rootSSH59892/helper1130257 LIVE at08:41:39Z with4genscomplete,
secs811.21/624.28/615.37/611.18 cumulative2662.1,process9048MiB. Preserve exact
206local/141arm/121external seed310manifest; continue same10genrunto terminal.
RemoteGPU1nowidle; GPU0 trainsseed310. No additionalGPUjobstarted.
Next_lever is doing10min fixed30dawn macrocomparison ofthisauditedfinalcentre
versusB on ep108450468, usingfresh/tmp sourcecopy and bytecodeoff. This is
behavioronly, noengine/counterfactualoutcome/candidateselection. OtherSolagents
availableforcompleted-family saved checks/finalaudits. GoalACTIVE/top5unmet;
latestrealB rank249/display2684.1, fifth3030.1 at08:07Z.

**Progress08:24Z — same original final generation still live:** RootSSH83690
has been repeatedly waited on directly (50s cells, stillsamehandle), and
helper1121008 is independently alive. Latest detailed poll08:18:33Z still9
completedrows/phasegeneration_1_boundary_pass; process9050MiB. Resourcecheck
08:23:47Z helperetime1h54m37s/CPU105%/stateRl, GPU1instantaneousutil0%,9060MiB
allocated. Native configabs_every10/abs_pairs64 and Trainer.generation includes
scheduled absolute_report before returning gen10; this can entail extra work,
but exact active phase is not instrumented. Rotation is doing5minread-only
source analysis of generation10 cadence; no debugger/signal/restart. Keep the
original10800s child/10860s outer timeout (deadline~09:29Z), no prematurekill.
Seed3101130257 remainsalive, GPU0instantaneous100%/9058MiB; latestcompletedcount1,
newcountshouldbereadnextturn. Neither tree is terminal/copied yet.

Collector /tmp/unitorder_collect_completed_training.py final fixes applied:
parseablewrapperUTC times, exactmode/run/onearm/10requested; booleanPIDabsence,
collectorhash captured before+recheckedafter, atomiccustodypublication.
Execute transferred script file afterterminal only; old functions.store
completed_training_collector string predatesthese fixes, DO NOTuseit.

Research980a26e: Sol wheat-accounting helper/result/note independently reproduced
exactbf764fcb; no >=2otherhistoricaltop5templates matchMajkel on declared
purchasedwheat/mixedproductunitratio. Rootlimits conclusion tothisproxy and10
selectedwins, not equivalentvalue/feed efficiency. Unexplained0–25residuals
makeaccountingclosureanidentity. Same-tileincidencefoundnowater-before-wheat-
harvestcollision; actionvaliditynotfullengineverification. No B selection,
newdownload/game/policypilot followed. Allthreeagentscurrentlyavailable except
rotation's short source review. GoalACTIVE, top5stillunmet(rank24908:07Z).

**Progress08:10Z:** Original seed309 PID1121008/rootSSH83690 is LIVE with9/10
native generations, last609.07s/cumulative5684.5s,9048MiB; final generation
running. Seed310 PID1130257/rootSSH59892 is LIVE withgeneration1 completed at08:10:25Z,
secs811.21/elapsed811.2/mean_win0.6137104630,9048MiB. Do not restart or copy either mutable tree.
Terminal evidence collector prepared and reviewed at
/tmp/unitorder_collect_completed_training.py (not run). It must execute as a
file on remote (binds __file__ SHA), seed309/310 positional argument. Transfer
this small helper after terminal under existing authorization; output
/tmp/unitorder_off_train_20260913.evidence.tar.gz plus .custody.json (seed310
uses its longer runbasename). It requires wrapper0+timestamps, PASS/complete/
10updates, exact mode/run/arm and absenthelperPID, pre/post tree equality,
known sole absolute work/src symlink and exact tar member hashes. Keep full
archive, download+verify custody, safely extract fresh path, move four wrapper
siblings inside local evidence root as expected by auditor. Preserve broken
remoteabsolute work/src symlink as evidence; never dereference it locally.

Fresh public Kaggle refresh succeeded with authorized network access after
sandboxDNSfailure: allthreepacedresponses200 at08:06:57/08:07:02/08:07:07Z,
S/ladder2/snapshot_20260913T0807_network. Actual teamrow rank249/display2684.1;
fifth3030.1, displayedgap346.0. B286completed/195wins/latestepisode rating
2684.192606, ended08:03:08Z. This is existing B, not a new trained submission.
Rootverified raw hashes/row membership; independent SolauditPASS. SummarySHA0884746d027c428d9b4ed024c072d0efea94f876dc4d0332dbeba059dbe68daf.

Current committed evidence89bb61e; goalremainsACTIVE.
Older objective diagnostic now reviewed root/Sol and strengthened with raw
weighted reconstruction (120tapex2+4scriptedx1=244), exact archive/probe/trainer
pins and savedgradient checks. Root46170 reproduced full JSON f4fb4c48 exactly.
It describes pre-repair population only; no objective change or blanket future
training ban follows. Nativecoinsrecord selector is not our finaltheta choice.
Next_lever updated ladderresearch note from actual fresh responses; it now
runs15min saved-only wheat massbalance review on already-fixed historical
top5 cases, no new download/game/policy or selectedBcase.

**Progress07:56Z — both remote GPUs training:** Original seed309 rootSSH83690 /
helper1121008 is alive with7 completed generations (last609.21s, cumulative4466.3s,
process9048MiB). Keep it unchanged. New seed310 initializer completed216.564110s;
root and Sol saved audits are byte-identical SHAa3f119ddfd187a1892fe0d31214fd18888810262bd3b1bb4dad4fcb4f841ddb9.
Its peak980MiB,4313samples,maxgap0.064046s; no update. Cold raw/output happen to
match seed309's fixed probe, but full seed-specific cold/post-B state differs
and is explicitly guarded. No accidental seed reuse.

Seed310 training committedbc9b3c6, root/Sol bundle auditPASS206local/141arm/
121external, preserving every original187 training input. Manifestb3fc988a126ce9b063dcc0c6fb4cfd198d5cb3b018afad1914feded69d125395,
bundle/tmp/unitorder-training-seed310-bundle-20260913.tar.gz SHA0a14861b986fe52835f8e72c5764b2a582d0960ef338e3e224177922876d0b53,
3398856bytes/207safe files. Authorized transfer and07:51:24Z preflightPASS.
RootSSH59892 started07:51:44.058052Z, helper1130257 live onGPU0 at07:52:19Z,
Initialcold passed; at07:55:21Z generation1 full-state guardPASS, process2516MiB
and helperalive. Generation1 now running; no completed positive row yet.
Canonical output/home/user/kagg3/artifacts/unitorder_off_train_seed310_20260913;
bundle root/home/user/stage_hr/S/unitorder/off_train_seed310_20260913_bundle.
One10gen child10800/outer10860 pluskill10,22000MiB threshold, no retry/resume.
Observe both runs to terminal, download complete evidence with compressed
transfer, root plus independent Sol saved audits, then judge each final centre
separately. Do not stop either live job or alter its bound inputs.

Research remains subordinate to these runs. Exact planner maturity economics
reject the new tomato-input premise on days12–14; no132-coordinate feature arm.
Root reproduced maturity JSON/CSV; rotation independently reproduced early-gap
JSON/CSV. Opponent day0 melon cycle yielded17440 gross before B's day9 cycle,
with exact dawn15 cash identity21828 revenue advantage -2387 extra spending =
19441. This does not reopen closed forced-melon families. Macro-only sigma.01
first-population check found no day0 melon target across both4096 populations;
independent Sol reproduction matched byte-for-byte. Generic judge runtime supports both audited run modes,
root11focused and Sol15combined testsPASS. Assembler is reviewed
(root full related suite27PASS), with explicit invocation in the judge plan.
No eligible final candidate or judge game yet. Next_lever continues
bounded research on exploration/objective alignment. Local8GB GPU authorized.

**Next-turn operational state08:00Z:** Goal service is ACTIVE (checked after
prior blocked transfer state resolved); keep it active, topfive not achieved.
Both remote SSH sessions remain83690(seed309) and59892(seed310). Latest full
monitor census07:57:38Z: original106141samples/maxgap0.075428s/peak9048MiB,
second7089samples/maxgap0.082644s/peak2516MiB, zero violations and exactsolePIDs.
Latest original count7gens; secondfirstgenerationguardPASS. Observe same jobs.
Reviewed judge assembler commit81d6e9f/root1290 suite27PASS; concrete invocation
in judgeplan after final saved evidence audits. Research commitad79913 preserves
all three tested episode diagnostics and handoff; immutable traincommitbc9b3c6.
Next_lever is finishing `flow215_objective_alignment.py` plus dated note: old
uncorrected generation0 population descriptive gradient audit only, root review
still pending. Root requested explicit distinction between native best-checkpoint
coins selector and OUR final-native-centre selection; no objective rerun/branch.
User replays/ remains untracked and untouched. No new candidate or enginegame.

**Earlier progress07:29Z:** Original rootSSH83690/helper1121008 verified live with5
native generations complete; latest611.16s/cumulative3245.9s, process9048MiB.
New independent seed310/GPU0 initializer bundle reviewed root/Sol PASS:
S/unitorder/seed310_init_manifest_20260913.json SHA87ef1fb0ca5ec454f5a5384e3d14684a0ba3fd7e575c6d05b9f42ce6f746652d,
193local/136arm/121external. /tmp/unitorder-training-seed310-init-bundle-20260913.tar.gz,
3287180bytes,SHA8e6b061d9cff978105e90bb3db595ba5d176a6ff600c57c7660bbc780e839da9.
One600s child/660s outer initializer onGPU0,22000MiB memory guard: actual native
seed310 cold992 plus2cached repeats, source/B/runtime/no-update proof. No new
8192 timing/general qualification. Transfer/preflight/launch next; not yet run.
Rootprotocol923230f9 and saved auditor507c19... reviewed; helper492b20c2 and
seed310 training helper21c8341e have6 focused pure testsPASS. Rotation is writing
seed310 training outer/saved auditor while root launches the initializer.

Generic judge_execution.py and judge_runtime_preflight.py are reviewed; root
72154 combined22pure testsPASS, no games. Concretecandidate manifest/eligibility
still waits for audited finalcentre. Next_lever Sol research is now available:
first note identifies planner stream-return feature versus network-input gap;
it is doing the smallest no-game economics/allocation census on ep108450468
days10–16. No model feature or training objective has been changed.

**Progress07:07:46Z:** Same helperPID1121008 verified live, three native generations
completed (802.44s,610.03s,611.06s; cumulative2023.5s). Generation3 mean_win
0.6137133837 is a training metric only. GPU process9048MiB, no wrapper exit.
Sol completed the user-requested episode108450468/submission56161192 review;
root independently validated720frames,30dawn rows and B macro reconstruction.
Exact B seat1 lost100280 to113447. Four successful tomato plantings occurred
days15/16/19/21; no opponent tomato anywhere. No tomato macro requestdays10–14
despite other crop requests. Price rose73(day15) to166(day29), but opponent
already led19441 atday15. The review distinguishes observed late/small crop
allocation from any untested profitability improvement. Evidence lives in
S/unitorder/episode_108450468/ and the dated episode review. No policy change,
counterfactual game or diversion from this single training run.

**Progress06:56:48Z:** The same helperPID1121008 is live, two native generations
completed. Generation2 took610.03s (native cumulative1412.5s), mean_win0.6182054281.
Process GPU memory9048MiB; wrapper exit absent. No completed training candidate
or B comparison yet. Judge inventory647b8b19 is root/Sol reviewed:231 bound input
hashes,424 exact row keys across seven separately checked families, no training-ID
overlap. The plan now pins local CPU settings and scopes candidate import checks
correctly around the evaluator's separately isolated opponent module images.
User requested Sol review submission56161192/episode108450468, particularly
tomato response to rising prices. postlot_mechanism has this15min read-only task;
root continues coordinating this same training. No policy edit or replay rerun.

**Earlier progress06:52Z:** RootSSH83690 and helperPID1121008 are verified live. Native
generation 1 has completed: secs=802.44, mean_win=0.6131768823. This is a training
opponent metric, not a comparison against B. The same process continues with
GPU process memory9048MiB and no terminal wrapper exit. No restart or resume.
Sol is preparing the candidate-independent fixed family/seed inventory and
checking the exact local CPU evaluation environment; no judge has launched.
The user questioned the12,000MiB memory cap because the GPU has24GB. It is a
self-imposed stop threshold, not an allocation throttle or hardware/competition
requirement. Preserve the frozen active run; revisit the overly conservative
threshold before a future run. Do not infer authorization to change this live
execution's bound code or manifest.

**Earlier progress06:42Z:** RootSSH83690 remains live, helperPID1121008. The exact OFF
initialization and full generation1 guard have passed; phase is
generation_1_boundary_pass. The first native generation is running, with no
completed positive generation log row yet. Saved monitor through06:39:03Z has
11870samples,maxgap0.063985670s,no nonpositive or>200ms gaps, solePID1121008,
peak9048MiB<=12000. Do not claim complete-generation throughput yet.
The separate-family judge saved auditor334e48c1 is reviewed, root31550 eleven
pure testsPASS including old seven-family saved-metric reproduction. The
revised judge plan uses a fresh local adapter: src links to the exact candidate
private_stage/src, scripts links to hash-bound local evaluator scripts. The
archive itself has only scripts/train.py, so private_stage alone is not a judge
worktree. Actual judge manifest/wrapper still wait for audited final training
centre and source, and must precommit source/keys before any candidate CSV.

**Latest live execution, 2026-09-13 06:31Z:** User explicitly replied
**"Approve all training bundle transfers"** to the exact training bundle request.
This authorization persists for subsequent training-bundle transfers in this
work; do not ask again merely because another training bundle/path is needed.
The unchanged f85acef7 bundle transferred successfully. Remote preflight
06:28:50.012047Z passed187local/140arm/121external bindings, audited OFF proof,
fresh canonical paths and idleGPU1 (allocated1MiB/no apps).
RootSSH83690 launched the one reviewed ten-generation training protocol at
06:29:10.029737Z. HelperPID1121008 is live in the persistent GPU monitor.
At06:31:07Z the initialization cold evaluation is running with exact OFF inputs;
the generation1 boundary has not yet passed. Observe the same execution to
terminal under10800s child/10860s outer caps plus kill grace; no duplicate,
automatic retry or resume. The transfer blockers described below are resolved.
Training output: /home/user/kagg3/artifacts/unitorder_off_train_20260913,
also via stage_hr/artifacts; helper output is loop-train/ below that root.
Existing receipt verdict REFUSED is a provisional fail-closed default during
execution, not a terminal failure. Check phase/error plus actual process/sidecars.

**Latest checkpoint (overrides the historical execution updates below):**
The user-approved OFF transfer and single GPU execution completed. RootSSH77568
returned exit0; execution ended06:10:15.046967Z after469.214404s, full outerPASS.
Root88923 and independent Sol saved-only audits PASS and are byte-identical
335adbd0d0216ddede16701b5541dc33327ca1198668be60447df00a79c93497.
Initial system-Python3.10 saved audits stopped on ISO trailing-Z parsing; unchanged
auditor reruns under project .venv/bin/python3.11 pass. No GPU rerun or evidence
rewrite. Execution46ec9f3c, receiptef5cb4cb, outputs4ea0f79e, rawinputs8f0fee66.
Peak4952MiB,9326samples,maxgap0.087961227s, successful final idle/process cleanup.
Evaluator-only ten-generation bound6426.002564s; no full-training time claim.
[Complete OFF result](2026-09-13-unit-order-off-confirmation-result.md).

Training code and exact manifest are committed51dea16 after independent review.
S/unitorder/train_off_manifest_20260913.json SHA
8197e1a58a2e5623fbdc7f1daa6edabf6b8177cdbdb9e881d4be5d7980bba301:
187local files,140exact arm inputs,121canonical external B/tapes. OFF proof uses
the passing Sol audit; identical root audit is bound as outer provenance.
Saved training auditor9e1a5b63 was independently reviewed and committed590af75
before freezing the manifest. Run saved auditors with .venv/bin/python3.11.

Reviewed local bundle /tmp/unitorder-train-off-bundle-20260913.tar.gz,
3276205bytes, SHA
f85acef7aa4d581b6c2e3b0289b48bc751c7ca262591c9b0100a7bc533517e6f.
Independent manifest/tar reviewPASS: exactly188safe regular members, all hashes
exact. Training has **not been transferred or launched**. Automatic approval
review rejected its scp transfer once: the prior user approval covered the OFF
bundle and exact path, not this new training bundle. An explicit approval question
is pending for user@remote-host:/tmp/unitorder-train-off-bundle-20260913.tar.gz.
Do not retry, reconstruct remotely or switch transports without that approval.
After approval, transfer unchanged, verify bundle/all187local+121external hashes,
fresh roots and idleGPU1, then run the one reviewed training launcher with
10800s child/10860s outer caps plus kill grace. No automatic retry or resume.

Prospective training root /home/user/stage_hr/S/unitorder/off_train_20260913_bundle;
canonical output /home/user/kagg3/artifacts/unitorder_off_train_20260913.
The exact passing OFF initialization must gate generation1. Download and audit
all ten native generations and the explicit final centre before judging.
Bounded Sol judge inventory found zero training-tape overlap with all seven
evaluation families. Use explicit family runners against persisted private_stage;
watch.sh would select the wrong worktree by width. Keep family results separate;
old pooled promotion rules and old Flow215 w01 rules are inapplicable.
No GPU workload is running. B and submitted payloads are unchanged; topfive
is unachieved. No pooling, production edit, promotion or upload.

**Latest execution update, 2026-09-13 06:03Z:** The user explicitly approved the
quoted exact private OFF bundle transfer. The unchanged bundle transferred
successfully. Remote preflight at06:02:11.153928Z passed its SHA, all173local and
121external hashes, fresh canonical paths and idle GPU1 (allocated1MiB, no apps).
Root SSH77568 launched the single reviewed OFF protocol; arm started
06:02:25.864459Z, helperPID1115094 observed in the persistent GPU monitor.
The transfer blocker is resolved. Observe this same execution to terminal;
do not launch another arm. No OFF result or training launch yet. The approval
request and blocked status described below are historical.

**Current checkpoint (2026-09-13) overrides all historical status below.**
Stay on the user's top-five goal: completed tape fidelity → completed GPU
qualification → one shipped/OFF confirmation → ten fresh training generations
→ separate-family evaluation against B. No broader simulator work or old w01.

All four NVML qualification arms passed. Execution ended at
2026-09-12T22:48:41.807289Z, wrapper exit0, elapsed2194.066737s.
Root and independent Sol saved audits agree exactly (SHA94fd559b).
The frozen comparison selects **loop**; evaluator-only ten-generation estimate
7171.768403s is within9000s. This is not measured full-training throughput.
All four helper PIDs were absent and both GPUs were observed idle afterward.
SSH tool handle92254 failed to return despite these terminal remote records;
do not treat it as a live GPU workload or rerun qualification.
[Completed result](2026-09-13-unit-order-gpu-nvml-result.md), commit6ddf80f.

The reviewed OFF confirmation and saved auditor are ready. Frozen manifest
S/unitorder/off_manifest_20260913.json SHA
768b8beda47b873e7d8357e7361f85de3035cb9e80b3fc068ca7dc4112b15003
binds173local files,135arm inputs and121canonical external B/tape inputs.
Local bundle /tmp/unitorder-off-bundle-20260913.tar.gz is2612514bytes, SHA
ba4c99891afe2075c19538216f8dadcc712a5fdbd861679969dd422217cc64bb.
It has **not been transferred or executed**. Automatic approval review rejected
the same scp transfer twice, including after read-only evidence showed the
archive/B/120tapes already match on the host. It recognizes the host/task but
requires explicit user approval for this exact private payload and destination:
user@remote-host:/tmp/unitorder-off-bundle-20260913.tar.gz.
An asynchronous approval question is pending; no answer is recorded here.
Do not retry or use another transport without that approval. After approval,
transfer the unchanged bundle, verify hashes/fresh paths/idle GPU, and run only
the reviewed one-arm OFF launcher (900s child,960s outer plus kill grace).
Download and independently audit its saved result before training.

Fresh-training helper and outer protocol are reviewed and committed **a8b7142**.
Six pure tests passed (root21821), with independent Sol final static reviewPASS.
Helper7e3584cb, protocol26423a82, launchercac41b07. The guard requires the audited
OFF execution, exact initial inputs/output and full cold/post-B state, and
rehashes all inputs immediately before native generation1. Ten native updates
and generations are audited under10800s child/10860s outer caps plus kill grace.
[Training plan](2026-09-13-unit-order-fresh-training-plan.md).
No training manifest, training launch, promotion or upload yet. B is unchanged;
top five is unachieved. Preserve the user's untracked replays/ directory.




**September 14, 09:31 UTC — EXEC-SCOPE verdict (docs/strategy/2026-09-14-macro-exec.md, S/macro_exec/, tests/test_macro_exec.py) → RAMP EXECUTABLE, CALENDAR NOT, executed plan LOSES:**
`plan.MACRO_EXEC_ON` (default False) + `KAGG3_MACRO_JSON` schedule (hands/anim/tiles/land per
day, extracted from the ymg_aq tapes). Day 0 reproduces ymg_aq's board to the tile (4 hands,
herd 0/2/3, 12 wheat + 2 melon; B stands 1/4/1, 11 wheat/8 carrot) and lands 277/277 season
hires (B 261) — first build to stand up a top-five opening (FORWARD_ADMIT reached 2 hands).
But tiles deliver 43 %, animals 60 %, idle tiles at dawn d10 = 44.0 vs B 1.1: a fixed per-day
planting calendar assumes ymg_aq's harvest cadence, ours diverges from d2. Pooled 12 ymg_aq
boards: ours 55,306 vs ymg_aq 138,009 (0.40); B 93,127 (0.87); macro arm −37,821/board vs B
(t −8.8); 68 band boards Δmargin −75,212 (t −27.5). d6 ask of 4 cows refused on cash (673/765).
BUILD FINDING: six gates, not one — beyond the hire argmax and the mix rewrite the ramp needs
(3) animal lists floored above seed lists inside the single budget.grant walk, (4) acquire_ok
skipped, (5) hire argmax clipped to hands_target, (6) HIRE_ROW_ON n_hire_row=min(n_hire,n_act)
trim excluded (with it on a 4-hand ask lands 2). Identity OFF: max |delta| 0 over 15 arrays ×
31 snapshots × 2 seats vs pristine HEAD tree; 9 tests pass; test_backend_agreement[legacy]
2/2400 hire_bias failure is PRE-EXISTING on HEAD (brain.py untouched). sell_hour extracted
but NOT consumed. NEXT (dispatching): MACRO-RAMP — site 1 writes animal_want only, brain.decide
keeps plant_target, to price the ramp alone without the calendar's idle cost.

**September 14, 09:33 UTC — TAPE-PORT verdict (docs/strategy/2026-09-14-sim-hire-sticky.md, S/sim_hire/, tests/test_sim_hire_sticky.py) → hire-sticky PORTED to the training-sim tape seat:**
`rollout.HIRE_STICKY` (default OFF; env `KAGG3_TAPE_HIRE_STICKY=1` or setattr) + optional
`src_hands`/`mlen` rows in tape_actions tables (re-cut tapes with S/sim_hire/build_tapes.py;
tapes without the rows are a static no-op even with the flag ON). Flag ON, the sim reproduces
the engine `--hire-sticky` leg to the coin on 15/18 TOPB3 boards (18/18 OFF). Measurable boards
(retention ≥ 0.95) OFF→ON: Majkel 0→0, DSM 1→2, ymg_aq 6→6, all 7→8; mean retention 0.64→0.78.
B paired margin on the 7 boards readable both ways −48/board (sd 127, t −1.0). Identity OFF:
36 TOPB3 rows + 68 band boards, 14 arrays × 31 snapshots element-identical to a frozen pre-edit
src/. NOTE S/topledger3/raw_B.npz is NOT a valid reference: it imports .claude/worktrees/arms-next
/src (older units.py, up to 103k coins off); master sim matches the engine leg 18/18, raw_B 3/18.
UNVERIFIED finding: the 3 DSM boards where sim ON ≠ engine ON have no re-issue firing at all,
so the engine's movement there is the `_MAP` half (persistent day-level assignment pins a
surplus hand to −1 → PASS for the day) — refutes "_MAP reduces to identity" and explains the
108741964 regression 0.75→0.40; fix belongs on the ENGINE side (scripts/tape_opponent.py).
Majkel boards remain unreadable in the sim (best 0.86): the Majkel-vs-B gap is still unmeasured.
Training needs BOTH halves (env flag + re-cut tapes); no train.py Config flag added.

**September 14, 09:51 UTC — MACRO-RAMP verdict (docs/strategy/2026-09-14-macro-ramp.md, S/macro_exec/report_ramp.md, raw_{hands,hands_herd,hands_herd_land}{,_band}.npz) → NO MODE BEATS B; the top's crew is NOT the top's edge:**
`plan.MACRO_MODE` ∈ {full, hands, hands_herd, hands_herd_land} selects which MACRO_EXEC_ON sites
fire (sites 5+6 always). All four land 277/277 hires on ymg_aq's exact per-day profile. 68 band
boards paired vs B (sim, CRN, action-replay seat): full −37,030 (t −19.9); hands −4,860 (t −9.1,
flips +0/−16, win 43→19 %); hands_herd −18,645 (t −12.7); hands_herd_land −18,164 (land = wash
+481). 12 ymg_aq boards: hands −2,736 (t −5.3). Residual of "hands": wage +531 (11 %), sell revenue
−4,046 — the schedule withholds 0.7/0.4/0.9 hands d3-d5 and surges +4.6 on d6, idle tiles d8 8.1 vs
B 3.3; gap accrues monotonically from d6. Δmargin ≈ 2× Δcoins because the shared-pot opponent's
coins rise 104k→108k (hands) →121k (hands_herd). hands_herd cost is mostly a BUILD DEFECT: site 1
overwrites animal_want every day so the schedule is a ceiling (herd frozen at 5.9 from d8; B
reaches 17.0 by d16); that arm is +2,588 ahead at dawn d12 and −18,644 behind at the end.
16 tests pass; OFF path character-identical. NEXT (dispatching MACRO-CHANNELS): herd as a FLOOR
(maximum(decode, schedule)) and day-0-only plate, then the unconsumed sell_hour/lot channel, each
alone vs B on the same 68+12 boards.

**September 14, 09:57 UTC — flow214 gate 1:** gen 18 real gate on gen 10's in-sim record: 54.8 %/+2,621 on n=124 vs the gen-0 seed's 57.3 %/+3,028 paired → REJECTED, record stands (the gate fires on every in-sim record, not only every 100 gens). No candidate to judge.

**September 14, 09:59 UTC — TAPE-MAP verdict (docs/strategy/2026-09-14-tape-map.md, S/topb3/tapemap/, tests/test_tape_map_fix.py) → _MAP shift CONFIRMED and REPAIRED; engine leg = sim leg 18/18; Majkel STILL unreadable (cash, not map):**
TAPE_MAP_DEBUG over all 36 TOPB3 games (25,884 steps): exactly the 3 DSM boards where sim ON ≠
engine ON (108741964, 108784054, 108813021, both seats) carry a `_MAP` pin — 1 pin each on day 1,
held 23 turns, 37 source orders executed by the wrong live hand; the other 15 boards carry none.
Correction to the mechanism: starved turns = 0/25,884 — `_settle` only appends, so the damage is a
one-place SHIFT of the whole assignment for the day, not a dropped order. Fix: `TAPE_MAP_FIX=1` /
`--hire-sticky-remap` (default OFF, inert unless hire-sticky) re-derives the map in `_settle`.
108741964: 0.40 → 0.75 = exactly the frozen value, B margin +106,932 → +30,801 = frozen margin
(the "regression" fully explained); 108784054's hire-sticky "gain" 0.78→0.87 was the same artefact.
Retention (frozen → sticky → sticky+remap): Majkel 0.25→0.52→0.52 (1/6 ≥.85), ymg_aq 1.02 (6/6),
DSM 0.65→0.74→0.78 (2/6), ALL 0.64→0.76→0.78, readable ≥.85 = 9/18. Engine leg now reproduces
the sim hire-sticky ledger 18/18 to the coin (leg-wide B +26,829, sd 43,401, t +2.62 — contaminated
by unreadable boards, do not quote). OFF: 36/36 TOPB3 rows coin-identical; ON: 60/60 NEXTHIGH rows
identical. Readable-9 B baseline: 22 % wins, −7,139 (t −1.6); the only real reading remains
B vs ymg_aq −13,751/board (t −5.9, 0/12). Majkel boards record ZERO pins — their blocker is the
purse (tape cannot afford its own recorded hire row). NEXT: purse-side repair or cut TOPB3 to its
9 readable boards; B vs Majkel1337 remains UNMEASURED.

**September 14, 10:16 UTC — CROP-DAY verdict (docs/strategy/2026-09-14-crop-day.md, S/crop_day/, tests/test_crop_day.py) → gene decodable, expressibility NOT improved; the wall is the day's development budget, not the shared softmax:**
`cd` block 5 crops × 9 day buckets appended to policy (7,020 → 7,065; N_CROP_DAY_BUCKETS=9,
CROP_DAY_BUCKETS=(1,2,3,4,5,6,11,21)); `brain.CROP_DAY_ON=False`, CROP_DAY_GAIN=64 (1.28 nats/sd at
sigma 0.02). SLOPE PASS: one coordinate moves its own bucket +1 tile at 0.17-1.7 sd (worst 4.83, all
under the 5-sd rule), zero leak into other days. EXPRESSIBILITY: with cd free and saturating
(40/45 coords non-zero) the macro fit's plant residual does not improve (share error 0.314→0.350,
volume error 4.03→4.14 tiles/day, plant MAE 3.83→3.90); d2 is already 100 % wheat in both fits
(6.00 tiles vs ymg_aq 11.33) and d3 79 % strawberry (1.01 vs 6.00): the blocks are missed on
COUNT. S/crop_day/capacity.py: 25-50 free tiles on the board every day against a 5-tile decoded
want → the wall is n_dev = dev_frac·n_free − animal_count (target 8.56, fit 5.10, B 7.78).
IDENTITY: coin delta 0 on 12 ymg_aq CRN rows OFF vs ON at cd=0; 2,400 fixture decisions
byte-identical; 7,020 thetas decode unchanged (flow214 candidates stay judgeable on this tree).
Fitted cd seed vs B, 12 rows: −70,634 (t −9.5, 0/12) — imitation seed, informational only.
Pre-existing red gates unchanged (test_backend_agreement[legacy] 2/2400 hire_bias ulp; five
crew/hire tests in test_crew_and_herd_mix). S/unitorder/momentum_train_prepare.py pins
N_PARAMS==7020 (closed family, left). NEXT: (a) flow215 = flow214 recipe + CROP_DAY_ON on remote
GPU 1 (gene passes the slope rule; outcome-only promotion), (b) DEV-SLOPE: is n_dev reachable by
theta (dev_frac / animal_share / aux[2]) and what does raising it do paired vs B.

**September 14, 10:22 UTC — TAPE-PURSE verdict (docs/strategy/2026-09-14-tape-purse.md, S/topb3/tapepurse/, tests/test_tape_purse_fix.py) → cash hypothesis REFUTED; residual is REVENUE (B's price denial); TAPE-SEAT REPAIR FAMILY CLOSED:**
Instrumented all 36 TOPB3 games: landed == owed hires on 18/18 boards (286/286, 285/285, 263/263 …);
tape short by 0-142 hand-hours of ~7,000; ymg_aq roster never short an hour. First divergence
is step 0 on 18/18 boards — a BUY price (we pay 562 where the source paid 533-565; the variation is
the source's original opponent). First cash refusal BUY_SEED d0h20 on 12/18 (hold 4, seed 10); first
cash-dropped HIRE d1h1/d7h1, recovered the same day. Flows vs source: cash-OUT within 2 % everywhere;
cash-IN Majkel −15k…−105k (108807571: 33,693 vs 106,922 on the same SELL rows), DSM −2k…−66k, ymg_aq
+1k…+3k. Repair `TAPE_PURSE_FIX=1` / `--hire-sticky-purse` (re-issue at the day's last hour, capped at
source roster) built, default OFF: OFF 36/36 and ON 36/36 coin-identical to topb3_Bmapfix.csv
(+26,829); NEXTHIGH 60/60 identical (+2,045, 53.3 %). Retention unchanged: ALL 0.78, 9/18 ≥ 0.85.
B vs Majkel1337 still n=1 (108801472, ret 0.86, +23,359). 26 tests pass. DECISIONS: (1) cut TOPB3
to its 9 readable boards (6 ymg_aq, 2 DSM, 1 Majkel) — the unreadable nine credit B for denial an
open-loop tape cannot answer, so the full leg reads better than B is; (2) stop repairing the tape
seat (fourth repair a no-op; the remainder is not in the seat); (3) B vs Majkel1337 needs a
closed-loop reconstruction or a sell-side neutrality probe — parked behind the executor work.

**September 14, 10:30 UTC — MACRO-CHANNELS verdict (docs/strategy/2026-09-14-macro-channels.md, S/macro_exec/report_channels.md) → herd floor LOSES, day-0 plate is ALREADY OURS, sale clock LOSES (pull-forward), delayed selling a WASH:**
Modes added: herd_floor (animal_want = max(decode, schedule) + sites 3/4), plate0 (d0 only),
hands_herd_floor, sell (site 7: each product's voluntary sale moved to the first lot at/after the
schedule's sell_hour; no quantity is extracted so "sell up to q" is not expressible), sell_late
(delay half only). 68 band boards paired vs B: plate0 −155 (t −0.5, +0/−3); herd_floor −1,784
(t −4.0, +0/−15; herd ends 16.7 vs B 17.0 — the ceiling defect is fixed, residual = tile
displacement paid late, crop tiles 33.6 vs 37.7 d10); hands_herd_floor −9,196 (worse than additive:
hands −4,860 + floor −1,784 = −6,644). B already buys 1 goose + 4 cows + 1 sheep on day 0 (6 head,
one more than ymg_aq's 0/2/3) and empties the 3,000 purse (165 left at dawn d1); the floor's extra
sheep is cash-refused. 12 ymg_aq boards: plate0 +1,418 (t +1.9, margin −508), herd_floor −7,987.
SALE CLOCK: sell −2,824 (t −13.4, Δmargin ≈ Δcoins = pure own-goal, no shared-pot transfer;
EGG −1,595 = 56 % of the damage — they sell eggs on 20/30 days at median hour 0, so obeying their
clock dumps the day into lot 1), sell_late −52 (t −0.4, +0/−0 = the noise floor for a sale-row
change). Our lot allocator beats their tape at the WHEN. 23 tests pass; OFF path pinned (site 6
guard gained `and _macro_site(6)` after the MACRO_EXEC_ON short-circuit). PRE-EXISTING failures
at HEAD (not this session's): tests/test_bank_before_lot.py::test_off_plan_is_byte_identical…
and 3 in tests/test_early_sell.py — PIN digests stale; to be looked at. STATUS OF THE IMITATION
CHANNELS: crew, herd, land, tile calendar, day-0 plate, sale clock all lose or wash when imposed on
B. Open: wheat re-buy, fertiliser, n_dev (DEV-SLOPE running), EGG-LOT (own-clock lot placement).

**September 14, 10:31 UTC — TOPB3-CUT (docs/strategy/2026-09-14-topb3r9-leg.md, S/topb3/{r9_ids.txt,r9_table.md,run_r9.sh,inventory_entry_r9.json}, S/lossflip/topb3r9_B.csv) → TOPB3R9 REGISTERED as the 8th judge family (informational, not a promotion gate):**
9 boards with retention ≥ 0.85 under hire-sticky + TAPE_MAP_FIX (ids.txt order is load-bearing:
Majkel 108801472; ymg_aq 108790159 108806291 108807563 108814574 108820106 108826138; DSM 108790144
108795512; retention 0.859-1.065, mean 1.00). B baseline (seats averaged, 18 rows): pooled 22.2 % board
wins, −7,139/board, sd 13,324, t −1.61 → ymg_aq 0/6 −13,751 (t −5.9), DSM 1/2 −2,551, Majkel 1/1
+23,359 (n=1, NEVER quote as "B beats the rank-1 file"). Verified: all 9 boards re-run through
run_r9.sh = 18/18 rows identical on every column to the topb3_Bmapfix.csv extraction. SE ≈ 4,400 →
resolves ~+9k/board at t ≈ 2. Run: `WORKERS=4 bash S/topb3/run_r9.sh <name> <worktree> <theta>
"<hr switches>"` then S/nexthigh/pair.py + S/topb3/retention.py. Registered in
S/unitorder/judge_family_inventory_20260913.json (family_count 8, order …NEXTHIGH, TOPB3R9);
autojudge wiring (audit_candidate.py BASE_FAMILIES + run_legs block) NOT done — §5 of the doc.
2026-09-14-topb3-leg.md carries a supersede note (its 7-board −12,599 is the pre-repair reading).

**September 14, 10:40 UTC — FLOW215 LAUNCHED (docs/strategy/2026-09-14-flow215-launch.md, S/flow215/{launch_flow215_remote.sh,remote_diff.txt,stage.log}) on remote GPU 1, pid 1384994, started 10:24:51Z:**
flow214 recipe verbatim + `brain.CROP_DAY_ON = True` (MELON_GENE_ON True kept), seed B zero-padded to
7,065 (artifacts/kagg2_games/thetas/flow193_g100_hr_pad7065.npy md5 67d7ebe8…; policy.pad == plain
zero-pad; test_crop_day 7/7 + test_melon_gene 5/5 + 90 synthetic dawns both-genes-ON vs OFF 0
mismatches), --run flow215 --seed 315, tree ~/stage_flow215 = stage_flow214 with src/scripts from
git archive 80ab2eb (6 files differ from stage_flow214 = TAPE-MAP + CROP-DAY commits, all other
flags default-off). Script md5 f6dc63bc…. Assertions: GPU 1 idle, flow214 pid 1379036 alive and
unedited, 153 rungs × 62 gate boards overlap 0, N_PARAMS 7065, train_only 6273/7065, |theta| 18.11.
~70 s/gen on both arms (no mutual cost); first real gate at gen 100 ≈ 12:30Z. Monitor armed (train.log
lines > 12, DEAD on pid). JUDGING: flow215 candidates are 7,065 floats and need policy ≥ 80ab2eb with
CROP_DAY_ON=True; flow214's are 7,020 (older layout, still decoded unchanged by HEAD). Note
S/flow215/launch_flow215_w0{0,1}.sh are an unrelated never-launched 2026-09-12 recipe.

**September 14, 10:45 UTC — DEV-SLOPE verdict (docs/strategy/2026-09-14-dev-slope.md, S/dev_slope/) → development budget LOSES both ways; B is a strict local optimum in it; the d9-d10 tile gap is LAND, not dev_frac:**
n_dev coordinates: g2[:,5]+gb2[5] (idx 3879 → head[5], dev_frac level), g5[:,2]+gb5[2] (4385 → aux[2]),
g2[:,6]+gb2[6] (animal share: re-splits only). +1 tile/day needs 87-101 sd at sigma 0.02; the whole
reachable range is +1.97 tiles/day (5.77 → 7.73 with dev_frac pinned at 1) because n_dev =
qfloor(dev_frac·n_free) is hard-clipped at n_free — +4/+8 do not exist for any theta. CORRECTION to
CROP-DAY §4: its "25-50 free tiles" counted the next LOCKED quadrant (n_free_slots(land=1)); real free
tiles d1-10 mean 7.73, B's want 5.77 = 75 % of them; ymg_aq plants 11.3 from a 6-tile dawn by
REPLANTING INSIDE THE DAY (n_dev is a dawn census; on 48 % of d1-10 dawns their n_dev exceeds our
ceiling). Gap opens d9-d10: ymg 48.8/55.2 crop tiles vs ours 38.2/38.1, their dawn n_free 15.3/16.2 vs
our 2.2/1.1 — a LAND jump (through d8 we are ahead on planted tiles with more cash, idle 0.0 d1-3).
Paired pure-theta arms on gb2[5], 68 band boards: dp1 (+0.70 t/day) −9,644 (t −13.1); dmax (+1.97)
−13,420 (t −14.2, 21.2 idle d10 — cash 39 at dawn d1, tiles not even planted); m2 (−2.00 control)
−7,042 (t −6.2); all +0/−27 flips; 12 ymg_aq boards 0 wins every arm. Anatomy: the + arms buy crops
with the herd's money (animal side −11,715; herd d10 11.1→6.9). Baselines re-run in this tree
reproduce MACRO-RAMP's B rows to the coin. NEXT (dispatching LAND): gb2[1] (head[1], land-bias coins)
swept to buy quadrants 2/3 earlier, everything else B; and land-only schedule (site 2 alone).
PARKED planner change: a second development pass after the day's harvests (intra-day replant).

**September 14, 11:06 UTC — TEST-TRIAGE verdict (docs/strategy/2026-09-14-test-triage.md, S/test_triage/) → HEAD default-off == SHIPPED PACKAGE: YES; all nine red tests already fail on the uploaded tree:**
Proofs: (1) the tarball's kagg3/ is byte-identical to src/kagg3 at b1bde4f (the ship commit in
UPLOAD.md, an ancestor of HEAD); (2) build_day six-array plan digests over 12 seeded boards identical
at HEAD, b1bde4f, 076c195; (3) six TOPB2 boards played from HEAD src and from the b1bde4f worktree =
byte-identical result CSVs. HEAD differs from the package in 4 modules, every hunk inert for theta B
(6,789 floats = offset("mh"): mh/ms/cm/cb/cd zero-pad, market_momentum term exact +0.0, crop-mix
branch falls through, HIRE_ROW gate widened only under MACRO_EXEC_ON). Bisect: bank_before_lot
OFF-identity pin, early_sell ×3, crew_and_herd_mix ×5, backend_agreement[legacy] 2/2400 ALL fail at
b1bde4f (bank_before_lot already 1/12 digests at ship^ b9b732b). Root cause of early_sell/crew tests:
HIRE_ROW_ON shipped at b1bde4f trims the HIRE row so no fixture goes wide — live assertions
invalidated, not stale pins; the bank_before_lot pin moved across ≥4 shipped-default promotions
since bdcf5f9 and cannot be attributed to one commit → NO pin updated (regenerating would launder
several moves). (c): [legacy] theta is artifacts/theta.npy (4,848 floats, not B); hire_bias 33 vs 32
on decisions 1532/1533 (d16) gives the same plan digest 200/200 boards — a score bias, no engine
action. Bonus: 076c195 fails seven test_crop_mix_* that pass at HEAD. PROCESS NOTE: a stale src copy
in the shared scratchpad ($SP/src, 2026-08-21) is picked up by tests/test_route_early.py's
sys.path.insert(0,"src") when cwd is there — isolate cwd for any scratchpad test run.

**September 14, 11:08 UTC — LAND verdict (docs/strategy/2026-09-14-land.md, S/land/) → earlier land LOSES; even ymg_aq's exact land calendar buys tiles that sit idle; two probes converge on the DAWN-CENSUS planner defect:**
Purchase days (dawn census, shows d+1): B q2 d5 (80/80 boards), q3 d10 (76/80; d9 4/68), never q4;
ymg_aq q2 d5 (5/6), q3 d8 (6/6). Only divergence = quadrant 3, two days. B's d10 is GATE-bound not
cash-bound: dawn d9 purse 2,144 vs price 2,000, both hard laws pass, but B's decoded land_frac is
−255.8/−256 (tanh saturated) so land_bias = −land_price; d0-12 dawns affordable 25.6 %, land_ok True
7.7 %. Reachability: gb2[1] idx 3875 (B −2.70); a sigma-0.02 block draw moves land_bias 0.0001 of a
price; the effective deltas are 100/200/300 sd; no "later" arm exists (already saturated). Paired
(baselines reproduce MACRO-RAMP/DEV-SLOPE to the coin, frozen src snapshot): gene arms p6/p10
(land_bias +1 price) band −16,855 (t −8.8, +0/−27; q2 dragged to d0-1 kills the opening ramp), ymg
−12,739; SCHEDULE arm (site 2 only, monkeypatched `_macro_site = lambda n: n == 2` under mode
hands_herd_land) band −881 (t −2.2, +0/−13), ymg −285 (t −0.2): q3 bought d8 and NOT PLANTED — crop
tiles d9/d10 identical to B to a tile while idle goes 2.2 → 29.2; the 2,000 coins come out of the
herd (animal product −2,466 vs crop +1,312). Δmargin ≈ 4× Δcoins (our early coins are their price).
ymg_aq's d9-d10 crop jump (48.8/55.2) is NOT land ownership: with their calendar copied our count does
not move; it is planting 11.3 tiles from a 6-tile dawn = REPLANTING INSIDE THE DAY. CONVERGENCE:
DEV-SLOPE (−9,644 for more budget) and LAND (−881 for more land) hit the same defect from opposite
sides — development is sized once at dawn from tiles free at dawn. REPLANT-SCOPE is measuring it;
build candidate = a second `_derive` development pass at a mid-day turn after harvests, first pass
unchanged (purely additive), default-off.

**September 14, 11:10 UTC — flow215 gate 1:** gen 18 real gate on gen 10's in-sim record: 53.2 %/+409 on n=124 vs the seed's 57.3 %/+3,028 → REJECTED, record stands (flow214's gen-18 gate was 54.8 %/+2,621). No candidate to judge.

**September 14, 11:21 UTC — REPLANT-SCOPE verdict (docs/strategy/2026-09-14-replant-scope.md, S/replant/) → dawn-census premise REFUTED: B already same-day replants; the real sites are HARVEST AGE and the LATE-SEASON PLANTING STOP; second development pass NOT to be built:**
plan.py:5501 `free_slot = is_empty | is_weed | harvest_one` and brain.n_free_slots (:186) count tiles
the day will harvest, so they are developable at dawn. B same-day replants 95.0 tiles/season (ymg set)
/ 94.2 (band) vs ymg_aq 159.0 / clone 147.6, with a harvest→replant gap of exactly 1 h on 95/95
(dawn route pairs HARVEST and PLANT); ymg_aq's mean gap 2.20 h. Idle tile-hours/board: B 4,124 vs
ymg 2,460 — but 92 % of B's is d20-29; over d0-19 B idles 316 vs their 661 (B is tighter for two
thirds of the season, then stops planting). Reachable d20-27 window: 2,306-2,558 tile-hours = 24-27
wheat cycles/board; hands (8 % spare unit-turns at h ≥ 12) and cash (59,791 at h12 vs a 136-coin
seed bill) are both available. Freed-but-not-replanted: 46-53/season, only 10.0 in d0-19. SITE 1:
plan.py:5313 + brain.py:185 `harvest_age = clip(VAL.pay_day() − t_day, c_first, c_sat)` — away from
the horizon this is c_sat (wheat 4 d); ymg_aq takes wheat at c_first = 2 d: it frees 12 tiles on d2 and
replants 11, B frees ZERO on d2 (its d0 planting comes back d3/d4). A k-day reduction moves free_slot,
n_free_slots and the seed want together. SITE 2: B plants 53.6 tiles d20-27 vs ymg_aq 82.7 with 60k
coins and spare hands — the gate is the value horizon (VAL.pay_day()=29 / HORIZON_DROP_ON) and
tile_value, not the dawn/mid-day distinction. NEXT (dispatching HARVEST-AGE): paired CRN k = 1, 2 and
a +1 control on 12 + 68 boards; then a horizon-relaxation arm for d20-27.

**September 14, 11:31 UTC — SELL-LOT-WOOL verdict (docs/strategy/2026-09-14-sell-lot-wool.md, S/sell_lot/) → no fixed lot beats the allocator; straw→lot 3 +524 coins but a MARGIN WASH; wool gap is PRODUCTION (shear rate + sheep-days), not selling; CORRECTION: MACRO-CHANNELS' "EGG −1,595" is MILK:**
Own-clock lot arms on 68 band boards: all products → lot 1 −4,748 (t −16.8; clean price loss, same
1,410 units at 88.0 vs 91.7), lot 2 −4,928, lot 3 −6,497 (cash-clock failures: coins/unit up to
94-97 but tiles d10 37.7 → 25.9, opponent +10.7k/+12.8k). Single-product: straw → lot 3 +524 (t +4.4,
farm untouched) but margin −231 (opponent +755, 4 flips); egg → lot 2 −9 (no-op). WOOL: we collect
116.4 and sell 116.4, 0.00 unsold (the ledger's "unsold 5.3" is other products) — no lot/hold change
can recover a unit; two thirds of the −13/−31 units is shear rate (0.929 wool per sheep-day vs
0.996/1.081), one third sheep-days d0-9 (we stand exactly 1.0 sheep d1-d8 vs their 1.9-3.3). Paired:
sheep13 (3-sheep floor d1-3) −212 band (cash-refused, sheep identical to B) / −5,186 ymg (lands
partially, wool DOWN to 113.7); ANIMAL_SAME_DAY_ON (offer the day's shear on the last lot) +6 (t +0.3;
row emitted but clipped, fleece still with the hand at turn 18). DEFECT: S/macro_exec/report_channels.py
:16 has MILK and EGG swapped vs spec.py:29 (I_EGG, I_MILK = 5, 6) → the MACRO-CHANNELS sale-clock
damage is MILK −1,595 (lot1 here: MILK −1,760 band, EGG +19); S/sell_lot/report_lot.py is the
corrected copy; wool column unaffected. New modes lot1/lot2/lot3/sheep13, SELL_LOT_PRODUCTS,
ANIMAL_SAME_DAY_ON (default off); 29 tests pass; raw_identOFF_ymg.npz byte-equal to raw_headOFF.npz
on all 15 arrays. SALE-SIDE FAMILY CLOSED (straw late-lot margin wash is the only positive coin line).

**September 14, 11:48 UTC — flow214 gate 2:** gen 108 real gate on gen 100's periodic candidate: 56.5 %/+2,534 on n=124 vs the seed's 57.3 %/+3,028 → REJECTED, record stands. Two refusals (g10 54.8 %, g100 56.5 %); no candidate to judge.

**September 14, 11:48 UTC — HARVEST-AGE verdict (docs/strategy/2026-09-14-harvest-age.md, S/harvest_age/) → harvest age LOSES on every arm; late-season planting LOSES; REPLANT-SCOPE's two sites CLOSED:**
Crop table kills it before the sim: wheat and carrot have window_start == c_first == 2 so units(a) = a
→ 1.00 units/tile-day at every legal harvest age; melon's clamp floor is already c_sat; tomato/straw
never read harvest_age. Paired (frozen git archive 21d330a, B reproduces raw_*_B bit-for-bit): k1
−3,143 band (t −6.5) / −2,473 ymg; k2 −7,474 (t −15.5, +0/−23); wheat@c_first −6,394 (t −15.1); +1
control −29,179; k2 + valuation.py:204 copy −8,695. Anatomy: yield- then hand-bound — k2 cycles +24 %
but units/harvest 3.63 → 1.89, crop units 794 → 616, coins/unit UP (pure volume loss); idle tile-hours
d0-9 255 → 1,157 because n_dev = qfloor(dev_frac × n_free) (brain.py:1008) puts back only a fraction.
LATE (develop every free tile d20-27): −4,980 band (t −20.0) / −3,442 ymg — planting d20-27 58 → 76 and
idle 2,345 → 1,665 tile-hours, yet −7.1 harvests and −44 units; latew (forced wheat) −6,562 (76 carrot
units at 64 traded for 44 wheat at 37). No arm positive anywhere; TOPB3R9 not run. SHARED CAUSE named
by the agent for DEV-SLOPE/LAND/WHEAT-SLOPE/REPLANT/HARVEST-AGE: tile supply is not the constraint,
crew-turns per sold unit are (watering spends 30 tile-days/game; wheat at c_sat is watered 3 of 4
days). NEXT (dispatching WHEAT-REBUY): the one ymg_aq channel never run — their 1,145-unit / 42k-coin
wheat market re-buy (buy 37.1, sell 37.4: "price-neutral" only for their own purse; it may set the
shared pot's wheat price against us).

**September 14, 11:53 UTC — JUDGE-PREP (docs/strategy/2026-09-14-judge7065.md, S/judge7065/) → flow215 / flow214 candidates JUDGEABLE NOW on all 8 families, no src change:**
S/drainpin/on2b.py (the wrapper every family runner calls) already routes `brain.`-prefixed switches
to kagg3.core.brain before the seat imports the sim (assert hasattr → typos fail loudly). Judge tree
= .claude/worktrees/judge-7065 (detached at 1d4e7e8, N_PARAMS 7065; needs the artifacts/kagg2_games
/thetas/flow193_g100_hr.npy symlink — made). Switch string = shipped hr string +
`brain.MELON_GENE_ON=True,brain.CROP_DAY_ON=True`. IDENTITY: B pad7065 through TOPB3R9 (18 rows) and
LOSS10 (20 rows) byte-identical to S/lossflip/topb3r9_B.csv and S/bloss/B.csv on every column;
test_crop_day + test_melon_gene 12 passed in the worktree. flow214 (7,020): do NOT pad — policy.unpack
zero-pads (policy.py:582); decode_receipt.py: pad7020 raw / policy.pad / pad7065 / B raw = 0 mismatches
on 36 dawns × 12 macro fields (rebuilt pad7020 md5 e2fc35cb = flow214's documented seed). COMMANDS:
`bash S/judge7065/fetch_flow215.sh` (ARM=flow214 for the other arm) then `WORKERS=8 bash
S/judge7065/judge_candidate.sh <theta.npy> <label> [--only FAM,FAM]` → all 8 families into their
historical csv names, TOPB3R9 retention, §115 pooled-band table (S/judge7065/pooled_band.py pools
LIVEC-H30 + LIVEC-H30B + NEXT30 as one 90-board leg via S/bank/paired.stats), audit_candidate.py.
Dry run on B pad7065 (TOPB3R9 + LOSS10) byte-identical again; pooled_band verified on
crop_mix_C_seed313 (−1,697 t −5.89, VETOED by TOPB2/LIVE62). NOT DONE: audit_candidate.py still has
7 families and S/autojudge/watch.sh still points at the 6,789 worktree with a 4-item switch string —
automatic judging of a flow215 record would silently drop cd; judge by hand with the wrapper.

## 2026-09-15T23:28:33Z — ENG22 (census E-C): B LOSES to the 2953+ engine class — the missing rung is a build class, and it is now a judge leg

Report docs/strategy/2026-09-16-eng22.md (Opus, 20 min; tools S/eng22/). Leg: `bash S/judge7065/run_eng22.sh <label> <theta>` → S/lossflip/<label>_eng22.csv (22 cluster-1 engine tapes × 2 seats, own seed base 1200780601, 2 min at WORKERS=4); registered as an INFORMATIONAL family in judge_candidate.sh:64 (not in §115/§115b — 11 of its boards are in promotion legs already: 10 TOPB2, 1 NEXT30; 11 are TOPTEN replays no family had scored).

B vs the engine class: win 36.4 %, −3,228/board (vs NEXTHIGH +2,045, NEXT30 +3,957, LIVE-C +5,224). Rating-matched TOPB2 split: clone half −1,152 (2,975) vs engine half −6,932 (3,004) — 5,780 coins at 29 rating points. Differing product lines (engine − clone, TOPB2 split; ENG22-vs-NEXTHIGH agrees on 9/10 signs): FERTILIZER +6,294 (t 5.5) in OUR favour; TOMATO −5,039 (t −2.6, sign flip); STRAWBERRY −6,279 (t −2.6); CARROT −2,179; WHEAT −3,580; MILK/WOOL the other way. Phase: d15-29 falls from +18.4k/+20.8k vs the clone to +8.2k/+11.6k vs the engine; the d10-14 melon tax is lighter. Corrections to the archive: strawberry does not flip sign (that was ymg_aq); wool is not the shared line; the 2780-2950 band is 30/30 clone and NEXTHIGH already covers it — the uncovered population is 2953+ and it is a BUILD class. CRN-sim fidelity on ENG22: mean 2 coins/board (max 39), so every board decomposes. flowq2_g150 on ENG22: +14 (t 0.02) — the +295 candidate buys nothing against the class that holds the top five.

Implication for the goal: the last ~290 rating points are held by opponents B loses to 64 % of the time, on tomato/strawberry/carrot/wheat in d15-29, while our fertilizer line beats them. Next stream: per-board decomposition of the ENG22 losses (what the engine does d15-29 that the clone does not, and what B could do about tomato/strawberry pricing) — the loss-anatomy method (docs/strategy/2026-09-08 loss anatomy) applied to this class.

## 2026-09-15T23:14:11Z — SMOOTHIE-SCREEN (census E-B falsifier): NO-GO, the +475…+975 smoothie pool is cross-sectional selection

Report docs/strategy/2026-09-16-smoothie-screen.md (Opus, 25 min; tools/thetas S/smoothie/). Structural: there is NO per-product theta coordinate for press3/grow_mult3 — press = h@w3 + scalar b3 (policy.py:319), grow shares w2/b2 across all nine products (policy.py:700-716); products differ only through their row of h. The agent took the direction by autodiff on tests/data/trajectory_obs.npz with a minimum-norm Jacobian step holding the other eight products fixed, and confirmed B's measured response (press3 12.37 → 2.51, grow_mult3 945 → 1006 on smoothie towns). Sim screen (120 frozen LIVE-C boards, 74 smoothie / 46 not, 600 episodes): opposite move −16,687 / −18,427 (dose-response the wrong way); shop-conditional version −942 (t −2.05) on smoothie boards; the WITH-B control −415. Bar was ≥ +400. Instrument check passed (screen reproduces the covariate: B +3,793 on smoothie boards vs +7,669 without). Side finding: press is a violently sensitive global lever (+0.4 decode units → −13k), so the census's "never pin press" note does not merit an arm. CLOSED; no GPU arm; direction #3 of the census done.

## 2026-09-15T23:06:28Z — BAND180 built: §115b = POOLED180 (169 boards) ≥ +450 and t ≥ 3; both +300 records REJECT again

Report docs/strategy/2026-09-16-band180.md (Opus, 36 min). Held-out corpus is exhausted at 79 new boards (not 90): every board in no judge leg AND never a training rung / gate opponent (BAND40's 40 boards are flow213/214 training data, excluded) with tape + pinned town on disk. Tiers: NEXT30-ext 14, live-top 14 (2847-2995), BAND40-ext 8, live-band 12, live-low 31 (≤2052); 48 of 79 in-band. Caveat: disjoint by episode, not by team.
Tools: `bash S/judge7065/run_band180.sh <label> <theta>` (own seed base, registry + tape preflight; → S/lossflip/<label>_band180.csv, 158 rows; ≈7 min at WORKERS=4) and `python S/judge7065/pooled_band180.py <label>` (imports pooled_band; prints pooled90, BAND180, in-band-48, POOLED180 and the §115b line). B baseline S/lossflip/flow193_g100_hr_band180.csv (B 70.9 % / +3,494).

Validation: flowq2_g150 BAND180 +249 (se 199), POOLED180 +274 (se 130, t 2.10) REJECT; flow218_g110 BAND180 +234 (se 273; +590 on the 31 low-band boards, +5 on the 48 in-band), POOLED180 +270 (se 176, t 1.54) REJECT. se fell ×0.75 as predicted. The fresh boards reproduced neither +300 nor the shrinkage's −100 — flowq2_g150's true effect is plausibly +100..+300, i.e. real-but-small and nowhere near the bar; flow218's is a low-band trade. Nothing changes: no promotion.

RULE from now: §115b — a candidate is promotable only at POOLED180 ≥ +450 with t ≥ 3 (both run_band180 and the 8-family judge). Old §115 alone no longer promotes.

## 2026-09-15T22:47:27Z — Combination thetas judged: ES-PLATEAU falsifier CONFIRMED (flowsum2 −20,103 vetoed; flowmean2 −126)

flowsum2_hr = B + d(flowq2_g150) + d(flow218_g110): POOLED −20,103 (t −25), TOPB2 −16,945, LIVE62 −21,260, 117 drops — the two norm-2.5 deltas are not additive; their sum leaves B's decode basin entirely. flowmean2_hr = B + (d1+d2)/2: POOLED −126 (t −0.59; H30 −13, H30B −140, NEXT30 −226), TOPB2 +1,116, LIVE62 −93 → REJECT, exactly the ES-PLATEAU prediction (−143 ± 200). Together with the shrinkage estimate (both records ≈ −100 true), the +295/+302 reads are selection noise. Tables: S/judge7065/flowsum2_hr_pooled.txt, flowmean2_hr_pooled.txt.

Judge chain killed after flowmean2 (flowl4_g110/g70 full judges and flowq4 hand legs dropped — same noise class; thetas kept in artifacts/kagg2_games/thetas/ if ever wanted). Local CPU goes to BAND180 (running) and the next stream. No candidate is pending promotion.

## 2026-09-15T22:40:58Z — LOT4 (fourth afternoon lot turn): built, measured paired, CLOSED

Report docs/strategy/2026-09-16-lot4.md (Opus, 28 min; tools/raws S/lot4/; reproduce `bash S/lot4/launch.sh && bash S/lot4/report.sh`). Built default-off LOT4_ON / LOT4_TURN=21 (plan.py:663-681, early_lot_turns :2791-2816, n_lots :2819-2827 replacing 15 SELL.N_LOTS sites; sell.py:100-136 allocator reads the lot count from inv_lots.shape[0]). tests/test_lot4.py (9, incl. OFF whole-plan digests on 5 boards vs a pristine git-archive tree) + shed-deficit + sell/lot_split/gates suites: 49 pass (lead re-ran).

Paired ON−OFF (two-purse, both seats, B + hr): 68 band our coins +308 (t 2.84) but margin −831 (t −4.87), their coins +1,139 (t 9.05); 12 ymg_aq margin −439; TOPB2 margin −90; LIVE-C margin −1,889. Units recovered vs the 21.6 u/game leak: none (band nightfall clip 15.37 → 15.29 u; ymg_aq worse, +3.5 u) — the fourth turn drains the dawn shed the three shipped lots already sell 0.65-0.87 of; the clipped units are the same-day inflow still in the crew's hands past every market. What it bought was price (91.45 → 91.70/unit on identical volume ≈ +350) and it lifts the opponent's book more. Turn sweep: the same row at turn 14 flips every sign (band margin +112 t 2.96, their coins −83) — sell timing moves the opponent's purse first, and earlier is the useful direction, but +112 is a quarter of the bar.

VERDICT CLOSED: no §115 leg. Every SHED-CLIP §4 candidate is now measured; the only untouched lever in the family is not reserving stock the route never reaches (want_feed / n_fert_eff, plan.py:7509-7519) — an admission question.

## 2026-09-15T22:28:58Z — ES-PLATEAU verdict: fixed-sigma ES from B is selection noise; local ES arm + watcher stopped

Report docs/strategy/2026-09-16-es-plateau.md (tools S/esplateau/; Opus, 13 min). Findings, all on existing judge CSVs:
- Per-board gains of the two +300 records correlate r +0.465 over the 90 pooled boards — but the median r between ANY two judged perturbations of B (14 controls incl. rejected momentum/crop-mix/flow216/flow219 candidates) is +0.387; after regressing out the generic "move-off-B" factor (−534 coins/board) the record-vs-record r is +0.224 with 51 % sign agreement = chance. They also win on different legs.
- Behaviour: `quads` = 3.0 on 180/180 rows for B and both candidates; hires, animal ramp and quadrant ramp identical; moves differ by 0.2 %; half the "gain" is the opponent's coins moving (one tile at d0/d15 compounding through the price table). Diffuse drift, no mechanism.
- Empirical Bayes over 22 ES-from-B checkpoints: se of one pooled read 182, spread of reads 188 → true-effect spread τ = 47 around mean −124. Shrunk: flowq2_g150 −98, flow218_g110 −97. The best of 36 candidates at +302 is BELOW the expected max of 30 pure-noise draws (+371). flow218's real-gate win paired on its own boards: +129, t 0.48. §115 as written is one 2.5σ test → 18 % chance of promoting a null theta over 30 candidates.
- Correction to my brief: `--stall-sigma-mult` is floored at 1.0 (scripts/train.py:2730-2735, verified) — no sigma-down schedule exists; the shrink was already run by hand as flowq3 (+26).
- Ranking: stop ES > more boards (180 boards: se 129, false promotion 0.7 %) > sum/average (prediction flowsum2 ≈ +126 ± 200, flowmean2 ≈ −143 ± 200 — running as the falsifier) > new seed > sigma schedule.

**Actions:** flowl4 (pid 76699) + queue_local3 (76933) stopped; autojudge watcher (50103) stopped — the local box goes to judges and research agents. Remote arms (flow219 GPU 0; flowq4 → q5 → q6 GPU 1) LEFT RUNNING as free draws: their own real gate still logs acceptances, and only a real-gate acceptance gets judged by hand from now on (no more watcher verdicts). No new fixed-sigma ES arm will be launched. §115 stays the rule for now, but any future promotion needs the extended (≥180-board) pooled band — building that board set and its B baselines is the next judge task. GPUs' next real job: the action interface (FORWARD_ADMIT / macro executor), per the report and the 2026-09-11 codex review (gene count is not the bottleneck).

## 2026-09-15T22:11:31Z — RESUMED (user 19:07Z: "Wait 3 hours, after resume the goal and work")

**Overnight-3 read (22:09Z):** flow219 (sigma 0.01 + wd) gen 229: g70 record §115 pooled −335 REJECT; g100 periodic 58.9 %/+3,185 rejected on win rate, g200 +2,131. flowq3 finished 500 gens (nothing after g60). flowq4 (sigma 0.005 from B, stage_cd4, started 20:16Z) gen 77: g10/g30/g50 records rejected (58.9 %/+2,255, 56.5 %/+2,612, 58.9 %/+2,474). flowl4 (local, sigma 0.005 from B) gen 126: g70/g110 records rejected (58.1 %/+2,702, 59.7 %/+2,473). The watcher's stage_cd4 legs do not include LIVEC-H30/H30B (flowq4 labels INCOMPLETE) — hand legs queued. No arm changed.

**Delta structure of the two +300 records (lead, 22:10Z):** |B| 18.11; |flowq2_g150 − B| 2.77; |flow218_g110 − B| 2.51; cosine between the deltas 0.010 (orthogonal); both deltas non-zero on all 6,228 unfrozen dims, max coordinate 0.16 — diffuse, seed-specific directions. Cheap additive test built: flowsum2_hr = B + d1 + d2 (md5 8ca1a112), flowmean2_hr = B + (d1+d2)/2 (md5 71e501af), both in artifacts/kagg2_games/thetas/.

**Judge chain (background, S/judge7065/resume_chain.log, pid 93708):** flowsum2_hr → flowmean2_hr → flowl4_g110_hr (md5 ec4bfe95) → flowl4_g70_hr (md5 5a899d47), full 8-family judge each, then LIVEC-H30/H30B hand legs for flowq4_g10/g30; pooled_band output in S/judge7065/<label>_pooled.txt.

**Agents dispatched (Opus, time-boxed):** LOT4 (90 min) — build the fourth afternoon lot turn as default-off LOT4_ON + tests + paired two-purse measurement; report docs/strategy/2026-09-16-lot4.md. ES-PLATEAU (75 min) — per-board gain correlation of the two +300 records, decoded behaviour, ranked options for the ES portfolio; report docs/strategy/2026-09-16-es-plateau.md.

## 2026-09-15T19:03:59Z — 09-15 19:00Z check: nothing to adjust; PAUSED

flow219 (GPU 0, sigma 0.01 + wd 1e-4) gen 76: g10 record rejected at the gate (59.7 %/+2,545), §115 pooled −190 REJECT. flowq3 gen 438/500: g400 periodic rejected, still nothing since g60; flowq4 starts in ~1 h. flowl4 (local, sigma 0.005 from B, seed 333) gen 39: g10 rejected (55.6 %/+2,122); queue_local3 (pid 76933) holds flowl3 behind it. Watcher fine (flow219_g10 judged 18:10Z). All arms too early to act on; no change. status.sh fixed: the local train.py line was hidden behind the watcher's subshells (`head -n 3`) — train and watcher/queue processes are now listed separately.

## 2026-09-15T17:20:04Z — 09-15 evening: all three live arms plateaued → cut flow218 + flowl2, fresh seeds started; PAUSED

**Training log read (17:08Z):**
- flow218 (sigma 0.005 from B, GPU 0) gen 413/1000: no acceptance since g110 (300 gens); g270 record 59.7 %/+3,133 and g400 periodic 63.7 %/+3,099 both under the g110 bar (61.3 %/+3,265); re-centred on g110 at gen 408. §115 on flow218_g270_hr (watcher legs; the watcher now writes the LIVEC-H30/H30B CSVs itself, so pooled_band.py runs directly — no hand legs needed any more): POOLED −57, t −0.23, no veto → REJECT (S/judge7065/flow218_g270_hr_pooled.txt). Lineage: g110 +302 → g270 −57.
- flowq3 (refine from flowq2 g150, sigma 0.005, GPU 1) gen 342/500: nothing since g60 (pooled +26); g100/200/300 periodic rejected; re-centred at 308. Left to finish (~3 h), then flowq4.
- flowl2 (local, sigma 0.01 from B) gen 269/500: zero acceptances (g10/30/50/90 records + g100/200 periodic all rejected).
- Pattern across flowq2 / flow218 / flowq3: a lineage's best read arrives by g110-g150 and nothing follows for 300 gens at the same sigma, even after a re-centre. More gens on a stalled lineage is the lowest-value use of a GPU; fresh seeds of the two regimes that reached +300 are the higher-value use.

**Adjustments:**
- flow218 KILLED at 17:10Z (pid 1433843, kill by PID; exit 0, best_abs.npy = g110 retained for flowq6's warm start). GPU-0 queue started flow219 at 17:10:32Z (pid 1455304): `run=flow219 params=7020 sigma=0.01 wd=0.0001 lr=0.003 seed 325`, 1000 gens, from B.
- flowl2 KILLED at 17:11Z (pid 44028, SIGTERM, graceful exit 0). Local queue started flowl3 at 17:11:58Z (pid 74921) — script rewritten a second time: sigma 0.005 FROM B, seed 332, --abs-pairs 32 (no longer the refine from flowq2 g150, which read +26 on flowq3). Header: ``. flowl4 (sigma 0.005 from B, seed 333) follows via queue_local2.sh.
- CORRECTION 2026-09-15T17:25:11Z: flowl3 did NOT start — it crashed at 17:16Z on FileNotFoundError (the local tree216 ships the seed as flow193_g100_hr_pad7065.npy; pad7020 exists only on the remote). queue_local.sh then finished and queue_local2.sh started flowl4 (sigma 0.005 from B, seed 333, pid 76699) at 17:19:59Z — verified header `run=flowl4 params=7065 sigma=0.005 wd=0`. launch_flowl3.sh fixed to pad7065; S/localarm/queue_local3.sh (pid 76933) re-runs flowl3 (seed 332) after flowl4 exits. Local order is therefore flowl4 → flowl3.
- Unattended portfolio now: GPU 0 flow219 (sigma 0.01 + wd 1e-4, seed 325); GPU 1 flowq3 → flowq4 (sigma 0.005 from B, stage_cd4, seed 321) → flowq5 (flowq2 replicate, sigma 0.01, seed 322) → flowq6 (refine from flow218 g110, sigma 0.005, seed 323); local flowl3 → flowl4 (sigma 0.005 from B, seeds 332/333). Watcher pid 50103 unchanged (covers flow219, flowq3-q6; local arms judged by hand on resume — the LIVEC-H30 legs now come from the watcher, so `python S/judge7065/pooled_band.py <label>` is the whole resume step for remote labels).

## 2026-09-15T13:55:10Z — 09-15 afternoon: first two REAL-GATE ACCEPTANCES, both §115 REJECT; flowq6 → refine-2; PAUSED

**Training log read (13:45Z):**
- flow218 (sigma 0.005 from B, GPU 0, gen 250/1000): g110 record ACCEPTED at the real gate — 61.3 %/+3,265 on the 124 pinned games vs B's 57.3 %/+3,028 paired. First candidate ever to beat B at B's own gate. g130 (61.3 %/+2,915) and g200 periodic rejected against the new bar. best_abs.npy = g110 (md5 667b13b2).
- flowq3 (refine from flowq2 g150, sigma 0.005, GPU 1, gen 172/500): g60 ACCEPTED at its gate (62.1 %/+2,984 vs the g150 incumbent's 57.3 %/+2,961); g100 periodic rejected.
- flowl2 (local, sigma 0.01, gen 172/500): g90 rejected (54.8 %/+2,394). flowq1/flowq2/flow216 finished, nothing further.

**§115 hand legs (LIVEC-H30 + H30B run 13:46-13:54Z, S/judge7065/<label>_h30.log, pooled in <label>_pooled.txt):**
- flow218_g110_hr: POOLED BAND +302, t 1.32, net flips +4 (H30 +428 t 1.08, H30B +544 t 1.10, NEXT30 −66); vetoes clear (TOPB2 +473, LIVE62 +129); NEXTHIGH +718 t 1.65, TOPB3R9 +711, LOSS10 −244. VERDICT REJECT vs +450 / t 2. Level with flowq2_g150 (+295 t 1.71) — the two best reads since flow193, from two different arms (sigma 0.01 and sigma 0.005 from B).
- flowq3_g60_hr: POOLED BAND +26, t 0.11 (H30 +40, H30B +401, NEXT30 −362); vetoes clear; LOSS10 −1,454. VERDICT REJECT. The sigma-0.005 refinement from flowq2 g150 has not added band margin in 60 gens; the gate acceptance was on the g150 incumbent's lower bar (+2,961), not on B's.
- NOTE the watcher's plain "(base hr)" NEXT30/LIVE62 lines overstate vs pooled_band (flow218_g110: watcher NEXT30 +632 / LIVE62 +773 vs pooled −66 / +129; same pattern on flowq2_g150). pooled_band.py is the §115 statistic; the watcher lines are a screen only.

**Adjustment:** flowq6 (GPU 1, after flowq5) rewritten to REFINE-2 — `--init-theta artifacts/flow218/best_abs.npy` (flow218's latest gate-accepted record at launch time; g110 now), sigma 0.005, lr 0.003, seed 323 (was sigma 0.01, lr 0.001 from B; .bak_sigma001 kept). Everything else unchanged: flow218 → flow219 (GPU 0); flowq3 → flowq4 (sigma 0.005 from B, stage_cd4) → flowq5 (flowq2 replicate) → flowq6; local flowl2 → flowl3 (refine from flowq2 g150) → flowl4 (sigma 0.005 from B). Watcher pid 50103 running.

**Resume:** run `bash S/localarm/status.sh`; for every new JUDGED label run the two H30 legs + pooled_band (command in the 10:1xZ entry). Watch flow218's later records (its lineage holds the gate record) and flowq4/flowl4 (sigma 0.005 from B, independent seeds). No hand-off file for the user: nothing passed §115.

## 2026-09-15T10:08:19Z — 09-15 mid-morning training analysis + queue adjustment (unattended; PAUSED after)

**Read of the logs (all arms on the redrawn draw, --pinned-once --shop-crn):**
- flowq2 (sigma 0.01 from B, GPU 1) finished 500 gens at 09:57Z, exit 0. No record after g150; g200/g300/g400 periodic candidates all rejected at the real gate (g400: 57.3 %/+2,609 vs bar +3,028). Judge trajectory of its records was monotone up to g150 (LIVE62 +271 → +369 → +465 → +851; NEXT30 +453 → +218 → +494 → +1,074; LIVEC22 t 3.4 → 5.6), then the arm stalled 350 gens at sigma 0.01. §115 on g150 stays REJECT (+295, t 1.71). Reading: the g150 point is a sigma-0.01 local optimum; the promotion path is refinement from it at a smaller step, not more of the same.
- flow218 (sigma 0.005 from B, GPU 0, gen 66/1000): in-sim records g10/20/40/50 all rejected at the gate (win 57-60 %, margin +2,260..+2,750 < +3,028). Judge legs mildly positive but below flowq2's trajectory at like gens (LIVE62 +276/+395/+214, NEXT30 +380/+357/+282, LOSS10 −333/−1,022/−1,409). Not clearly bad at gen 66: LEFT RUNNING; flow219 (sigma 0.01 + wd 1e-4) follows in the GPU-0 queue.
- flowl2 (local, sigma 0.01, gen 63/500): records g10/g30/g50 rejected (54-60 %, +2,412..+2,457). Local candidates are not auto-judged; judge by hand on resume.
- Every sigma-0.02 arm so far (flow216 940 gens, flowq1 500 gens, flowq1_g80 judge LIVE62 −2,103 t −4.2) produced nothing; the remaining sigma-0.02 arms in the queues (flowq3, flowq5, flowl3) were therefore rewritten before they started.

**Adjustments (scripts rewritten in place, .bak_sigma002 copies kept on the remote; repo copies updated in S/flow216 and S/localarm):**
- flowq3 (GPU 1, STARTED 09:57Z, pid 1442440): REFINE arm — `--init-theta artifacts/flowq2/cands/g00150_record.npy` (md5 b6ae6e07, 7,020 params, = artifacts/kagg2_games/thetas/flowq2_g150_hr.npy), sigma 0.005, lr 0.003, wd 0, seed 320, 500 gens, stage_flow214. Verified in train.log: `run=flowq3 params=7020 sigma=0.005 wd=0`, theta loaded (|theta| 18.35); gen-0 real gate running (incumbent = g150 itself, so the in-run bar is g150's own 57.3 %/+2,961; the §115 judge vs B decides).
- flowq5 (GPU 1, after flowq4): flowq2 REPLICATE — sigma 0.01, wd 0, lr 0.003, seed 322 (was sigma 0.02 + wd 1e-4). Tests whether the sigma-0.01 climb reproduces from B under a new seed.
- flowl3 (local, after flowl2): REFINE arm, second seed — warm start flowq2_g150_hr.npy, sigma 0.005, lr 0.003, seed 332, --abs-pairs 32 (was sigma 0.02 lr 0.001).
- Unchanged: flow218 → flow219 (GPU 0); flowq4 (sigma 0.005 from B, stage_cd4) → flowq5 → flowq6 (sigma 0.01, lr 0.001); flowl4 (sigma 0.005 from B) via queue_local2.sh after flowl3. Autojudge watcher (pid 50103) already lists flowq3 stage_flow214, so the refine arm's records are judged automatically (LIVEC-H30/H30B still by hand for pooled_band).

**Resume checklist addition:** for any flowq3/flowl3 record that the watcher marks JUDGED, run `judge_candidate.sh <theta> <label> --only LIVEC-H30,LIVEC-H30B` then `python S/judge7065/pooled_band.py <label>`; a refine candidate that clears +450 / t 2 is the first promotion candidate since flow193.

Disk on the remote: 18 GB free (99 %); fine for the queued arms. Session PAUSED until the user asks to resume.

## 2026-09-15 08:13Z — flowq2_g150 §115: REJECT, pooled band +295 (t 1.71), bar +450 / t 2 — the best candidate read since flow193; PAUSED

8-family judge complete (S/judge7065/flowq2_g150_h30.log + watcher legs): LIVEC-H30 −42 (t −0.13), LIVEC-H30B +551 (t 1.68), NEXT30 +377 (t 1.66) → POOLED BAND +295, t +1.71, net flips +1, worst leg −42, no veto (TOPB2 −106, LIVE62 +207). Informational: LOSS10 −627, NEXTHIGH +655, TOPB3R9 +7,146. Verdict REJECT under §115 (needs ≥ +450 at t ≥ 2). Positive on 7 of 9 rows and first candidate with no negative band leg: sigma 0.01 is the right neighbourhood; sigma 0.005 arms (flow218, flowq4, flowl4) and flowq2's later records are the ones to watch. Theta: artifacts/kagg2_games/thetas/flowq2_g150_hr.npy (7,020). Session paused per user; resume with `bash S/localarm/status.sh` and `python S/judge7065/pooled_band.py <label>` for each JUDGED label in S/autojudge/verdicts.txt (watcher legs omit LIVEC-H30/H30B — run `judge_candidate.sh <theta> <label> --only LIVEC-H30,LIVEC-H30B` first).

## 2026-09-15 08:10Z — Overnight training analysis and adjustment of the unattended arms (user request), then pause

Analysis (S/localarm/status.sh + S/autojudge/verdicts.txt):
- flow216 (crop-mix, sigma 0.02, redrawn): gen 940, every record refused, 3 periodic candidates rejected and re-centred (g900 56.5 %/+2,473). Killed 08:09Z.
- flowq1 (crop-day gain 16): 500 gens done, g400 54.0 %/+1,931; all records refused; local judge of g80: NEXTHIGH −2,050 (t −4.3), LOSS10 −2,448. Crop-day gene arms are worse than crop-mix (local flowl1 the same: g400 52.4 %/+2,280).
- flowq2 (sigma 0.01): g400 57.3 %/+2,609; record g150 wins 71→71, margin +2,961 (closest to the seed's +3,028 of any candidate since flow193). Watcher judge of flowq2_g150: TOPB2 +796 (t 0.84), LIVEC22 +1,532 (t 5.59), LIVE62 +851 (t 1.73), NEXT30 +1,074, NEXTHIGH +655 (t 1.42), LOSS10 −627, TOPB3R9 +7,146 (t 0.92, informational). The §115 pooled band is INCOMPLETE because the watcher runs the LIVEC22 leg instead of LIVEC-H30/H30B; those two legs launched by hand 08:08Z (S/judge7065/flowq2_g150_h30.log) → pooled_band.py flowq2_g150_hr when done. flow216_g70 pooled: REJECT −331 (t −1.86). The trend across arms: smaller sigma = candidates closer to B.
Adjustments (all unattended):
- Remote GPU 0: ~/queue_gpu0.sh → flow218 (sigma 0.005, seed 324, 1,000 gens; started 08:09Z pid 1433843) then flow219 (sigma 0.01 + weight-decay 1e-4, seed 325, 1,000 gens). Log ~/queue_gpu0.log.
- Remote GPU 1 queue unchanged in order (flowq2 running, then q3 lr 0.001, q4, q5 wd 1e-4, q6) but the two not-yet-started variants rewritten: flowq4 = crop-mix sigma 0.005 (stage_cd4 now CROP_DAY_ON=False, init pad7065, seed 321), flowq6 = sigma 0.01 + lr 0.001 (seed 323). Crop-day gain-4 and sigma 0.04 dropped.
- Local: tree216 set CROP_DAY_ON=False (applies to flowl3 lr 0.001 and later; flowl2 sigma 0.01 running keeps its loaded module); S/localarm/queue_local2.sh runs flowl4 (sigma 0.005, seed 333) after the first queue ends. flowl4 was started once by mistake (empty pid) and killed within a minute.
- Autojudge watcher restarted (pid 50103) with AJ_ARMS flow218, flow219, flowq2..q6 (WORKERS 6). Scripts copied to S/flow216/ and S/localarm/.
Status any time: `bash S/localarm/status.sh` (add ~/queue_gpu0.log by hand — script updated below).

## 2026-09-14 13:36Z — SHED-DEFICIT: forced-sale projection fix is exact and recovers zero units (band −30, t −1.23); shed-sizing family closed. SESSION PAUSED until the user resumes (≈ 09-16)

Report: docs/strategy/2026-09-14-shed-deficit.md; tools S/shed_deficit/; raws S/macro_exec/raw_sheddef_*.npz, S/shed_clip/raw_sd_*.npz. Paired CRN, theta B, 80 game-seats.
- SHED_DEFICIT_ON (plan.py:603, body :7548-7552, sd_yield = t_yield + 2·sd_w inside inflow): 12 ymg −4; 68 band −30 (t −1.23), margin −82 (t −2.60), their coins +52 (t +2.51), win 42.6 → 39.7 %, 2 flips to them. Clipped units 21.62 → 21.84 (+0.22): zero recovered. Identity OFF +0.
- Why: deficit is only an ask; the greedy spends it from spare = max(avail − s_qty, 0) (plan.py:7580), already empty (SHED-CLIP §4a); d15-28 already sell 0.73-0.87 of the dawn shed and the remainder is task-reserved feed/fert. The effect is +0.81 u of hour-0 stock dumped at the cheapest quote, feeding the pot, while what dies is tonight's inflow after the last lot (turn 18).
- Both planner-side repairs measured zero (SHED_OVERFLOW_ON +0.10 u, SHED_DEFICIT_ON −0.22 u). SHED_D29_ROW not built (bound 446 < bar before ~6 % throughput cost). Untested successors: a fourth afternoon lot turn (14 days, band bound 1,272), or not reserving stock the route never reaches.
- tests/test_shed_deficit.py 8 pass; OFF suite 56 pass.
- PAUSE: user ordered all work stopped after this close (limits end; resume Wed 2026-09-16). Monitor blyz0e31f stopped. Running unattended: flow216 (GPU 0), queue flowq1-q6 (GPU 1), local queue flowl1-l3, autojudge watcher. Status: `bash S/localarm/status.sh`.

## 2026-09-14 13:20Z — UNSUPERVISED SETUP until 2026-09-16 (Opus quota resets 09-15 22:00Z; user: "only important work and words")

User asked for continuous unsupervised training arms trying different variants to beat B, remote and local. Everything below runs without supervision; every candidate a remote arm nominates is judged locally by the autojudge (8 families, judge-7065 tree) and written to S/autojudge/verdicts.txt.

REMOTE user@remote-host (disk 18 GB free — candidates/logs are small):
- GPU 0: flow216 (pid 1393054), flow214 recipe minus --pinned-fixed-seed, crop-mix 7,020, seed 316, 30,000 gens, gate every 100 gens + every record; log ~/stage_flow214/artifacts/flow216/train.log.
- GPU 1: ~/queue_gpu1.sh (log ~/queue_gpu1.log) runs six 500-gen variants sequentially (≈ 10 h each): flowq1 crop-day gene CROP_DAY_GAIN 16 (stage_cd16, seed 318, init pad7065); flowq2 sigma 0.01 (seed 319); flowq3 lr 0.001 (320); flowq4 crop-day gain 4 (stage_cd4, 321); flowq5 weight-decay 1e-4 (322); flowq6 sigma 0.04 (323). q2/q3/q5/q6 on stage_flow214 (crop-mix). All redrawn episodes, --keep-candidates. Scripts ~/launch_flowqN.sh (sed of ~/launch_flow216.sh; copies in S/flow216/). flow217 (duplicate seed) killed 13:15Z.
- Kill: `ps -eo pid,cmd | grep "scripts/train.py --run"` then kill <pid>; kill the queue with the pid of `bash ~/queue_gpu1.sh`.
LOCAL (3070):
- S/localarm/queue_local.sh (log S/localarm/queue_local.log) runs flowl1 (sigma 0.02, seed 330) → flowl2 (sigma 0.01, 331) → flowl3 (lr 0.001, 332), 500 gens each, tree S/localarm/tree216 = git archive 08bee1a + MELON_GENE_ON/CROP_DAY_ON True + CROP_DAY_GAIN 16, init pad7065, chunk 4096, abs-pairs 32, gate workers 6; logs artifacts/flowlN/train.log. Local candidates are NOT auto-judged (watcher is remote-only): judge by hand with S/judge7065/judge_candidate.sh on artifacts/flowlN/cands/*.npy.
- Autojudge watcher started 13:19Z (S/autojudge/watch.pid) with AJ_ARMS = flow216 + flowq1..q6, KEEPCAND_STAGES incl. stage_cd16/stage_cd4, WORKERS=6; verdicts S/autojudge/verdicts.txt, log S/autojudge/watch.out. §115 promotion still by hand: pooled band ≥ +450, t ≥ 2 → hand the user file + md5.
- Monitor blyz0e31f (this session) polls remote gates, queue logs, local gates and verdicts every 15 min.
RESUME CHECKLIST (09-16): read S/autojudge/verdicts.txt and ~/queue_gpu1.log; judge any ACCEPTED/record candidates the watcher missed; SHED-DEFICIT (Opus, dispatched 13:20Z) is the one open research thread — its report lands in docs/strategy/2026-09-14-shed-deficit.md; if it reads ≥ +450 on the band it is the next engine candidate.

## 2026-09-14 13:17Z — SHED-CLIP: the shed clip is a real leak in the shipped agent: 21.6 u/game (68 band) ≈ 1,718 coins at dawn quotes, mostly nightfall d14-28, not day 29

Report: docs/strategy/2026-09-14-shed-clip.md; instrument + raws S/shed_clip/ (wrappers on units._apply_one / apply_units / eod.end_of_day / rollout._market_turn, no src edits; reproduces the stored smoke raw max|delta| 0 on 23/24 arrays).
- Theta B, shipped hr switches: 12 ymg 24.58 u/game-seat (DROP 2.67 + nightfall 21.92) = 1,816 coins (t 4.43); 68 band 21.62 u (6.25 + 15.37) = 1,718 coins (t 7.33); tape opponents lose 2.6-4.4 u. Nothing dies before d14; nightfall losses d14-28 (worst d16/d18/d26-28); the DROP loss is one event at h17-18 of d29 (52 % of band game-seats, worst board 33 u). Wheat is half the units; the expensive deaths are tomato/melon/wool.
- Mechanism: sim/units.py:86 room = max(SHED_CAPACITY − sum(shed), 0), :91 a DROP voids the whole hand whatever the shed took; eod.py:238-245 same nightly. Harvest never blocked (lands in the uncapped hand). plan.py's only guard is the forced sale (:7428-7465), gated off on the terminal day (:7452). Day 29: lot 1 clears the 91-u dawn shed by h2, then ten DROP_ON return legs pile 99.6 u back between h13 and h18 with no market row between turns 10 and 18. LOT-DEPTH's attribution to BANK_BEFORE_LOT_ON was wrong (bank_day = ~terminal, plan.py:7097).
- SHED_OVERFLOW_ON measured paired: inert (+0 ymg, +4 band, 0.10 u/board). Closed.
- Live term: the forced sale's projection excludes the watering bonus (plan.py:7438-7441 uses view.t_yield; :7621 already spells t_yield + 2*bl_w), so deficit is systematically too small. Bound ≤ 1,272 (band) / 1,686 (ymg) coins. Dispatched SHED-DEFICIT (default-off switch, paired). Weaker second: a d29-only sell row at turn ~15 (bound ~500-600).

## 2026-09-14 13:05Z — ROUTE-FREEFIRST: recovers 29 of the 266 hour-0/1 turns, worth nothing (band +23, t 0.18); morning-block family closed

Report: docs/strategy/2026-09-14-route-freefirst.md; tools S/route_freefirst/; raws S/macro_exec/raw_freefirst_{ymg,band}.npz, S/turns/raw_ff_*.npz. Paired CRN, sim only.
- Mechanism: route_split asks d_pick[e1]==0 (plan.py:8094), the per-day BUY-row question pushed onto a block; PLANT is the only op the row feeds (seed credited after turn 1). Widening the gate fires on 66/68 boards; h0-h1 PASS 266.3 → 237.0; whole-game PICKUPs unchanged; worked turns −9.4 (hires −25.9 unit-days).
- Paired: 12 ymg −46 coins / margin −759 (t −1.80), their coins +714; 68 band +23 (t 0.18), margin −79, their coins +102 (t 1.88), wins 29→28. TURNS priced 29 turns at +513; realised +23 (two-purse rule, eighth family).
- Why nothing: plan.py:7201 already credits every unit on a route_split day with the extra turn, so n_admit was sized as if it existed; delivering it finishes an over-admitted list earlier. The morning block is slack, not a constraint. With PRESTOCK-REPAIR this closes the hour-0/1 family; remaining half of TURNS' 695 is the smaller crew (labour family closed 09-11).
- Built default-off ROUTE_FREEFIRST_ON (plan.py:2377) + 6 tests (OFF digest vs pristine HEAD); 56 tests pass. Not dispatched (budget): exact labour credit at plan.py:7201 as an admission arm; the opponent-purse shift probe.

## 2026-09-14 12:45Z — flow216/flow217 alive: gate 1 = seed 57.3 %/+3,028 ACCEPTED on both (bar identical to flow214), gen 1 in 662 s

Both arms logged gen 1 (compile + first generation 662 s; ~70 s/gen expected after). Gate 1 on each: gen-0 record (the seed) 57.3 %/+3,028 on n=124 ACCEPTED as incumbent — byte-identical to flow214's, confirming the same tree, seed theta and gate field. gen-1 mean_win 0.023/0.022 = flow214's own gen-1 warm-up value (0.0195, then 0.05, 0.09 at gens 2-3), so nothing anomalous; under the re-drawn episodes mean_win is expected to sit near 0.5 and not climb (SIM-GATE-GAP) — the gate decides. Monitor bimyzltqm polls both logs every 600 s for gate lines and process death. First periodic gate at gen 100 ≈ 14:30Z.

## 2026-09-14 12:41Z — PRESTOCK-REPAIR: switch made legal, first real read is negative (band −326, t −1.92); the 266 idle turns are behind the seed row, not the assert

Report: docs/strategy/2026-09-14-prestock-repair.md; tools S/prestock/; raws S/macro_exec/raw_prestock_*.npz, S/turns/raw_pv2_ymg.npz. Sim-descriptive, paired CRN.

- Why the asserts exist: both subjects are hire_wide_early. plan.py:2584 — EARLY_SELL mode A gathers lot 1 into the free slots of the turn-1 BUY row while PRESTOCK moves the overflow HIRE row into turn 1 on exactly those days (two writers, one row); plan.py:8612 — OPEN_PUMP's sell-back leg is index 0 of the same row and pump/hire_wide_early are never None with the switches on, so it raised on day 0 of every game = the 3,000-coin VOID lines of 09-10. Minimal legal reconciliation: give up the wide day (rest = max(n_hire − MO, 0) = 0 for crews ≤ 10), pass hire_wide_early=None; ROUTE_BASE_PRE turns route_split off by its own gate so `early` applies once (the ROUTE_EARLY defect).
- Paired PRESTOCK_V2_ON: 12 ymg −789 (t −1.33); 68 band −326 (t −1.92), margin −355, wins 29→27, flips +2/−4 (TOPB2 −327, LIVE-C −326 t −3.05). V2+FARMER0 identical to V2 (FARMER0 live in the planner but never reaches a real board). Schedule-half-only arm byte-identical to OFF.
- Turns recovered: 2.6 of 266.3 (h1 PASS 236.3 → 233.7); worked turns +6.3 = +110 coins, paid for with +1,040 coins/game of extra wheat bought (145.7 → 171.9 units). Blocker: _buy_row_units (plan.py:3306) counts seeds, PRESTOCK_SEEDS is off and measured-rejected (−90,863), so the prestock can never seed; with ~wide (45.9 % of day-rows hire > 10) the reachable set is ≈ 0.3 day-rows/game.
- Built default-off: PRESTOCK_V2_ON / PRESTOCK_V2_FARMER0_ON / PRESTOCK_V2_BUY_ON (plan.py), rollout.py hooks; tests/test_prestock_v2.py 6 pass incl. whole-plan digest vs pristine HEAD archive; test_macro_exec + test_rebuy + test_prestock_v2 + test_lot_split = 50 pass. tests/test_route_split.py 2 failures are pre-existing at HEAD (verified on the pristine archive).
- Verdict: no engine leg for V2; it stays default-off as the family's legal read. The 266 turns: widen route_split's gate (plan.py:6907) so a block whose first op is not PLANT starts at TURN_BUY even on a seed-buying day (free_first exists at plan.py:8028) — no purchase, no purse. Dispatched as ROUTE-FREEFIRST. The smaller crew (351 turns) stays untouched (crew imposition lost −4,860 in MACRO-CHANNELS; labour family closed 09-11).

## 2026-09-14 12:39Z — LOT-DEPTH: lot-splitting lever real but ~10× smaller than bounded; best arm +69 coins (t 1.4) on 68 band boards; tight caps destroy units

Report: docs/strategy/2026-09-14-lot-depth.md; tools S/lot_depth/; raws S/macro_exec/raw_lotsplit*.npz. Sim-descriptive, paired CRN.

- Mechanism: day 29 is one lot because of `press` (sell.py:85-98), not a turn budget or cap: press·lot_index outweighs a curve worth < 2 coins/unit, so any press ≥ 1 gives 65/0/0 where press=0 gives 0/8/57 (+87 coins). A split within a turn is worth exactly 0 (one inventory path); the only gain is the town tick between lot turns 3/10/18 = +46..+163 coins on the whole liquidation. WHEAT-REBUY's −3.82/u day-29 gap is mostly the opponent's 101.8 units, not our walk. All nine products walk.
- Paired: cap 40 d29 = 12 ymg −2 / 68 band +69 (t 1.43), margin +109, 0 flips (TOPB2 +117 t 1.43, LIVE-C +1); cap 20 d29 +9; cap 10 d29 −481 (t −4.97); cap 20 all-season −427 (t −3.57); cap 40 all-season −21. Nothing near §115.
- New finding: cap 10 destroys 10.66 units/board on day 29 (t −7.86). Day 29 sells 171.9 units against a 90.8 dawn shed — over half the terminal sale is BANK_BEFORE_LOT_ON mid-day DROPs into a 100-cap shed, and deferring volume out of the early lot leaves no room for the deposit (engine clips it). An early lot is shed room, not just a price. Dispatched SHED-CLIP to measure engine-clipped deposits per game for B at OFF on every day.
- Built default-off: plan.LOT_SPLIT_ON/LOT_SPLIT_MAX/LOT_SPLIT_DAYS, plan._lot_split, one site before s_qty = sum(lots) so s_qty is conserved. OFF identity max |delta| 0 over 15 arrays × 31 snapshots × 2 seats × 12 boards. tests/test_lot_split.py 7 pass. Committed with only the LOT_SPLIT hunks of plan.py staged (PRESTOCK-REPAIR's PRESTOCK_V2 hunks stay in the working tree for its own close); test_lot_split re-run against the staged plan.py in a scratch copy: 7 pass.
- Not pursued: PRESS_SCALE sweep (ceiling +163 coins), too small for §115.

## 2026-09-14 12:30Z — flow214/flow215 killed; flow216 (GPU 0, seed 316) and flow217 (GPU 1, seed 317) launched = flow214 recipe minus --pinned-fixed-seed

Acting on SIM-GATE-GAP. flow214 (pid 1379036, 3 gates all below the seed, g130 −677 t −2.32) and flow215 (pid 1384994, 2 gates, −2,6xx) killed by PID at 12:28Z (SIGTERM then SIGKILL; both GPUs at 1 MiB afterwards). Staged ~/launch_flow216.sh and ~/launch_flow217.sh on the remote by sed from ~/launch_flow214.sh (copies in S/flow216/): exactly four edits each — --run, --seed 316/317, `--pinned-once --pinned-fixed-seed --shop-crn` → `--pinned-once --shop-crn`, log path (+ mkdir of artifacts/flow21N); same tree ~/stage_flow214 (git archive of the 7,020 crop-mix tree, MELON_GENE_ON=True), same seed theta flow193_g100_hr_pad7020.npy (= B byte-identical at zero cm/cb), same 153 pinned rungs, same 124-game win gate every 100 gens, --keep-candidates. Launched 12:29Z: flow216 pid 1393054 (GPU 0), flow217 pid 1393055 (GPU 1). Two seeds of one recipe = replication of the H1 test: with the pinned episodes re-drawn each generation, mean_win should stop climbing; the gate decides as before (bar = seed 57.3 %/+3,028 at gate 1). flow215's cd gene (H2: sigma×gain too large) is parked until the draw fix reads.

## 2026-09-14 12:28Z — SIM-GATE-GAP: flow214/flow215 in-sim gains are a fixed-draw artefact; gate candidates walk downhill monotonically

Report: docs/strategy/2026-09-14-sim-gate-gap.md; tools S/simgate/ (remote configs/logs/candidates mirrored under S/simgate/remote and S/simgate/cands).

- mean_win is the population win rate on 153 FROZEN games (one episode per pinned rung, seed word = blake2b(rung name), identical every generation: --pinned-once --pinned-fixed-seed, src/kagg3/es/train.py:1324-1347, :4543-4567). The trainer's own comment calls it a ladder-relative diagnostic near 0.5 that correlates −0.17 with strength (train.py:14-20). The coin yardstick on the same ladder is flat (abs 102,294 g10 → 103,163 g130) and hold ≡ abs to 0.006 % (the frozen seed makes both halves the same game), so nothing between gates can detect the drift.
- Gate ladder (paired, 62 boards): seed 57.3 %/+3,028; g10 −406 (t −1.71); g100 centre −494 (t −1.96); g130 −677 (t −2.32) while mean_win 0.568 → 0.593 → 0.611. flow215 the same, larger: −2,619 (t −7.95), −2,634 (t −5.75); its population never reaches the seed's level (mean_win 0.28-0.38) → sigma×gain too large for the cd block (H2).
- H1 (fixed-draw artefact, not strength) supported: the g100 candidate on its own 20 highest-weighted training opponents at a fresh engine seed = −139 (t −0.25), held-out TOPB2 −308 (t −0.48); not better even in-sample, so not class overfitting. Killed: win-quantisation/sigmoid saturation (the arm's own sigmoid(margin/scale) objective prefers the incumbent on the gate boards at every scale). Adam spreads the step: 4.4 % of the squared step at g100 is in the crop-mix block — these arms are a re-training of B (a measured local optimum), not a gene test. By g130 the candidate raises the opponent's coins (99,900 → 100,348).
- Flag change: S/flow214/launch_flow214_remote.sh:67 `--pinned-once --pinned-fixed-seed --shop-crn` → `--pinned-once --shop-crn` (re-draw each pinned rung's episode every generation; town stays pinned via --with-town; within-generation CRN untouched). If mean_win stops climbing under it, that is the confirmation.
- Lead decision: kill flow214 (pid 1379036) and flow215 (pid 1384994) — three and two gates respectively, all below the seed, in-sim metric shown uninformative; relaunch under the corrected draw (next entry).

## 2026-09-14 12:27Z — flow214 gate 3 (gen 138): gen-130 record 58.1 %/+2,351, rejected

flow214 gated its gen-130 in-sim record on the 124-game real gate: 58.1 % win / +2,351 margin vs seed 57.3 %/+3,028, rejected. First candidate above the seed on win rate, still 677 coins/game below on margin; the gate wants both (or a paired significance) — SIM-GATE-GAP is reading the gate rule in scripts/train.py and should quote it. flow214 candidates so far: g10 54.8/+2,621, g100 56.5/+2,534, g130 58.1/+2,351 — win rate rising, margin falling: the arm is trading big wins for narrow ones.

## 2026-09-14 12:15Z — TURNS: no turn sink; B is 695 worked crew-turns/game short of ymg_aq, 266 of them PASS at hours 0-1

Report: docs/strategy/2026-09-14-turns.md; tools + raws S/turns/. Sim-descriptive, 12 ymg_aq boards + 20-board band control.

- Turn economy is level: worked turns per grown unit sold B 4.89 vs ymg_aq 5.03; net-market coins per worked turn 17.52 vs 17.96; band control 4.86/4.82 and 18.37/18.10. The 1.59× "turns per sold unit" from HARVEST-AGE is an artefact: ymg_aq buys 1,171 of the 2,501 units it sells and a BUY costs zero crew turns.
- The gap is volume: 5,986 vs 6,682 worked turns/game = 695 turns ≈ 12,150 coins at B's own rate (sim margin -13,722). Where: PASS at hours 0-1 = 266 turns (4,665 coins; B h0 PASS 100 %, h1 PASS 236/270, h2 PICKUP 210 — ymg_aq PICKUPs at h0/h1, B does the same pickups one hour later; plan._routes ROUTE_BASE 2/3 and PRESTOCK_ON=False plan.py:2075); smaller crew 351 turns (6,142 coins; hire enumeration); PASS h2-19 86 turns; h20-23 not the difference.
- Water rule deterministic: tile planted today dies tonight unless watered today; watering tomato/strawberry never adds a unit. B's droppable waters 123/game vs ymg_aq 352 — B is tighter, no lever.
- Hands: d0-9 44.5 vs 52.3 hand-days, d10-19 parity, d20-29 106.6 vs 114.7; B turn-limited hours 4-12 (0-1 % PASS). Not cash-bound (41-78k at d20-28 vs a 371-1,094/day bill for +3 hands); 3 hands = 66 turns/day ≈ 1,150 coins vs 239-coin bill at d10 → the fib wage is ~5× underpriced against B's turn value; the binding thing is the hire enumeration's value model.
- Checks: reproduces REPLANT-SCOPE (184.2 PLANTs, 687/6,673 PASS); sim-side ymg_aq op budget matches the raw tape per class; net market B−ymg −15,515 vs top-5 ledger −15,483.
- Archive cross-check (agent-results rule): PRESTOCK_ON's only valid read is -334, t -0.21, n 24 (2026-09-09-switch-sweep.md:127); its later screens were VOID (seat crashed at import) because plan.py asserts against EARLY_SELL_ON=True and OPEN_PUMP_ON=True (2026-09-11-route-early-bug.md, 2026-09-14-open-lever-census.md item 6); never repaired. TURNS prices the hour-0/1 pass independently at +4,665. Dispatched PRESTOCK-REPAIR: lift the asserts legally, farmer block at turn 0, paired CRN 12 ymg + 68 band with the S/turns PASS instrument.

## 2026-09-14 12:11Z — AUTOJUDGE-WIRE: watcher re-pointed at judge-7065 + 8 families; not started

Report: docs/strategy/2026-09-14-autojudge-wire.md. S/autojudge/audit_candidate.py gains TOPB3R9 as an INFORMATIONAL family (prints PASS INFO / INFO-SKIP, never sets failed; rc unchanged on three old labels). S/autojudge/watch.sh: JUDGE_TREE/JUDGE_SWITCHES default to the judge-7065 worktree and the exact 6-item switch string of S/judge7065/judge_candidate.sh for 6789/7020/7065 thetas (6954 keeps its own pair; export both vars to reproduce the old 6,789 judge); TOPB3R9 leg after NEXTHIGH inside the caller's flock (run_r9.sh takes no lock, no nested flock); TOPB3R9 column + retention line + its own glut line, gate/promotion lines untouched; LEGS_ONLY=FAM,… subset mode; AJ_ARMS="arm stage;…" one-launch arm override; KEEPCAND_STAGES (stage_hr stage_flow214 stage_flow215) replaces the literal stage_hr test so --keep-candidates arms never judge best_abs.npy (the flow200 defect).
Receipts: bash -n clean; test_audit_candidate 7 pass; real TOPB3R9 leg on B pad7065 through the new path = S/lossflip/topb3r9_B7065wire.csv, md5 8292fb27… identical to topb3r9_B.csv (diff empty, ident 18), log shows MELON_GENE_ON/CROP_DAY_ON set and the judge-7065 plan.py.
Lead decision: watcher NOT started (watch.pid 56453 stale). No remote candidate has been ACCEPTED; the local CPU stays with TURNS and LOT-DEPTH. On an ACCEPTED gate I judge by hand with S/judge7065/fetch_flow215.sh + judge_candidate.sh. Start line if wanted: `AJ_ARMS="flow215 stage_flow215;flow214 stage_flow214" nohup setsid bash S/autojudge/watch.sh >> S/autojudge/watch.out 2>&1 &`. Caveat: AJ_ARMS does not persist; the ARMS array at watch.sh:66-80 still lists the old arms.

## 2026-09-14 12:10Z — flow215 gate 2 (gen 68): gen-60 in-sim record 43.5 %/+393, rejected

flow215 (cd gene, 7,065, seed 315) at gen 68 gated its gen-60 in-sim record candidate on the 124-game real gate: 43.5 %/+393 vs seed 57.3 %/+3,028, rejected. Worse than the gen-10 candidate (53.2 %/+409); the in-sim record is diverging from the real gate, the same pattern flow214 shows (mean_win 0.60 in sim, 56.5 % real). Next periodic gate at gen 100 (~12:45Z).

## 2026-09-14 12:09Z — WHEAT-REBUY: market re-buy is a zero-sum wash by construction; both executable arms lose and pay the opponent

Report: docs/strategy/2026-09-14-wheat-rebuy.md; tools S/rebuy/; raws S/macro_exec/raw_{rebuy20,rebuy40,macrorebuy,rebuy20_band,rebuy40_band,plate0_ident}.npz. Sim-descriptive, paired CRN, no engine game.

- Mechanism: one pot per town (state.py:65, market.py:590/684); WHEAT price = 25 + sqrt(10000 - inv). A BUY of n units followed by a SELL of n units receives exactly the same n table entries: round trip = +0 coins (wash_check.log, n = 20/40/100). Only escapes: town drift (+8..+28 coins per 40-unit overnight carry) and the cross (market.py:717-747), which pays the OPPONENT the undepressed quote (+34 to them per 40 units). The re-buy is never denial.
- Tape: ymg_aq buys 1,144.8 u/season @37.09 and sells 1,477.6 u @37.37; 872 bought units never fed, 642 bought and sold back within the same hour (buys on SHOP_SELL_INTERVAL ticks). Whole price gap ≈ 550 coins/board.
- Paired: rebuy20 / rebuy40 / MACRO "rebuy" on 12 ymg_aq = -2,275 / -2,544 / -2,404 coins (t -2.9..-3.2); on 68 band boards rebuy20 -1,043 (t -4.9, their coins +517 t 2.8), rebuy40 -1,997 (t -8.2, margin -3,811 t -13.4, their coins +1,815 t 6.8), 6-10 flips all to them. Market leg nets +153 coins for a season of churn; the loss is the shed (full at 100 by d15, eod harvest dump blocked) and d15 cash 7,376 -> 6,294.
- Build (all default-off, OFF path pinned): MACRO_MODE "rebuy" = site 9 (plan.py), helper _rebuy_extra, own-clock REBUY_ON/REBUY_N/REBUY_DAYS; extract.py emits buy_target/buy_hour (existing JSON keys byte-unchanged; plate0 re-run max |delta| 0). tests/test_rebuy.py 8 pass; test_macro_exec 29 pass. The tape's 22 buy hours are not emittable from B's turn rows (S/rebuy/PATCH_NEEDED.md).
- Verdict: the last untested ymg_aq channel loses. The imitation-channel family is exhausted (crew, herd, plate, land, calendar, sale clock, lots, dev, harvest age, late planting, wool, re-buy). Remaining thread from this report: lot depth — ymg_aq clears +0.99/u above the dawn quote, we clear -0.51/u (day-29 liquidation of 64.6 u into one lot at -3.82); bounded ~500 coins/board on wheat. Dispatched as LOT-DEPTH.

## 2026-09-14T09:25Z — TAPE-ARM: flow214 LAUNCHED on remote GPU 0; ladder snapshot 09:24Z: B 2715.1 rank 277, fifth 3004.3

**flow214 launched: YES.** pid 1379036 (started 2026-09-14 09:11:08Z), GPU 0 of 2 (RTX 3090), log `~/kagg3/artifacts/flow214/train.log` (= `~/stage_flow214/artifacts/flow214/train.log`). Progress at 09:24:35Z: gen 3, mean_win 0.0928, best 0.6541, 69.5 s/gen, rungs 153/157.
- Recipe = flow193 + the 6 ymg_aq town-pinned TOPB3 tapes (w2). Rungs: 85 @ w2 band/non-family, 20 @ w10.2 top-ten, 42 @ w4 LIVE-C, 6 @ w2 ymg_aq, 4 w0 archetypes = 157. 0 overlap with the 62 gate boards. DSM/Majkel excluded (desync until TAPE-PORT lands).
- Seed = raw B 7fcf3948… zero-padded to 7,020 (md5 e2fc35cb869a3e25418f6a5e889454f8), MELON_GENE_ON=True on the staged tree (cb live at sigma 0.02). Gate unchanged from flow193: `--real-gate-metric win`, 62 × 2 pinned seats every 100 gens, min-flips 5, keep-candidates.
- Staged tree = local master 076c195, NOT stage_hr (stage_hr has no cm/cb block; its leg20 metric and SEED_ROOM_PURSE_ON patches are absent by design; diff archived S/flow214/remote_diff.txt). Launcher S/flow214/launch_flow214_remote.sh (md5 af71fb47…). The pre-existing never-launched local S/flow214/launch_flow214.sh (3070 recipe) was restored to HEAD.
- LAYOUT NOTE: CROP-DAY is appending a `cd` block (7,020 → 7,065) in the working tree; flow214 candidates are 7,020 and must be judged with a tree whose layout still decodes 7,020 unchanged (the append guard must keep that true; verify before any judge).
- Fetch: `rsync -az user@remote-host:kagg3/artifacts/flow214/{best_abs.npy,real_gate_cand.npy} artifacts/kagg2_games/thetas/`. Judge = seven-family pinned tapes, §115.
- Report `docs/strategy/2026-09-14-flow214-launch.md`.

**Ladder snapshot 09:24Z** (`S/ladder2/snap_20260914T0924Z/`): B sub 56161192 = 2715.1, rank 277 (was 2767 / 165 on the 09-11 refresh), 432 games 273 W; last-40 17/40 vs mean opp 2750 (−28.6), last-100 50/100 vs 2724. hr sub 56143250 = 2618.6 (538 games). Fifth place 3004.3 (sub 56209748). Gap to fifth ≈ 290 rating ≈ 5,800 coins/game at the +100 ≈ +2,000 calibration.
## 2026-09-14T09:24Z — SEED-SCREEN closed: all three fitted seeds lose; no seed ES arm; hands gap is d10 only

**Verdict: FULL / CREW / CREW+HERD fitted thetas all lose vs B in the paired CRN sim. No ES arm from any of them. The crew "biggest they do / we don't" line was a measurement artefact: B already lands 261 hires a season vs ymg_aq's 278.**

| theta | ymg_aq (12 games) | band clone (68 games) |
|---|---|---|
| FULL (seed_ymg_aq.npy) | −80,122 (t −14.50, 0/12) | −82,954 (t −36.58, 0/68) |
| CREW (99 coords, g10/gb10) | −738 (t −1.11, 5/12) | −3,805 (t −6.94, 7/68) |
| CREW+HERD (198 coords, +g8/gb8) | −8,420 (t −5.38, 0/12) | −8,347 (t −12.21, 2/68) |

- Execution check (HIRE counter patched into the sim seat): B hires 4 d0 / 1 d1 / 5.5 d5 / 8.4 d10. MACRO-EXTRACT compared their *landed roster* to our *decoded ask*; `crew_target` is a floor/deferral, hire enumeration (HIRE_ROW_ON) prices hands on today's task gain. Corrected gap: d10 only (8.4 vs 11). Raising the ask changes landed hires by −3/season.
- FULL asks 10.2 hands at d10 and lands 5.25 (143/season), reaches their 19.2-tile wheat board with 20.2 idle tiles and 264 coins at d5: the FORWARD_ADMIT postmortem repeated with a fitted theta. CREW+HERD = a clean cow→sheep trade (wool +2.6k/+1.8k, milk −5.0k/−7.3k).
- Identity gate: same cross-tree drift as WHEAT-SLOPE §2 (−30/−293 coins vs raw_B.npz, worktree baselines); within-tree bit-equal, all Δ paired within run. EXEC-SCOPE's uncommitted edits inert (MACRO_EXEC_ON=False).
- Consequence: the seed arm is dead as planned (CREW / CREW+HERD). Everything now rides on the executor: (i) a day-indexed crop channel (CROP-DAY in flight), (ii) hire enumeration priced against the schedule, not today's derived tasks, (iii) sale/fertiliser/re-buy legs. Seeds are tested only after those land.
- Report `docs/strategy/2026-09-14-seed-screen.md`; tools/seeds `S/seed_screen/` (seed_CREW md5 504b30a2…, seed_CREWHERD md5 4d3a5790…).
## 2026-09-14T09:08Z — WHEAT-SLOPE closed: wheat gene reachable, moving it loses everywhere (family CLOSED)

**Verdict: cb[WHEAT] is ES-reachable (+8 d10 wheat tiles = 0.93 sd at sigma 0.02) and every move of it loses. 0 wins in 88 paired games over five z values. The −6.6k WHEAT ledger line is a conserved-tile trade, not a lever.**

- Reach: +1 wheat tile = 0.14–0.29 sd; +8 tiles = 0.93 sd (0.02) / 1.86 sd (0.01). Not gain-limited like melon.
- ymg_aq boards (6 × 2 seats, CRN): z=+0.01 Δ −11,699 (t −5.74, 0/12); z=+0.02 Δ −14,335 (t −6.99, 0/12). Wheat line closes (+6,872) but strawberry −11,885, melon −6,553, carrot −3,641 pay for it: tiles are conserved and a 105–167 coin/unit scarce row is traded for a 34–37 coin/unit commodity their 1,145-unit buy leg absorbs.
- Band clone (40 of 68 rows, time box): z=+0.02 Δ −26,075 (t −13.98, 0/40). Negative direction loses too (−10,632 / −44,568). Explains the W00/W01 rejections (band-only tapes, reach covered this direction).
- Caveats: switch inert (ON@z=0 bit-equal to OFF, 14 arrays); the 0-coin gate vs stored raw_B.npz fails because those baselines came from the 6,789-coordinate worktree (drift −30/−310 coins pooled, within-tree paired deltas unaffected). 28 band rows unrun (UNVERIFIED).
- Consequence for the seed path: a static crop mix cannot buy the top-five wheat line; the block programme (pure-wheat day next to pure-strawberry day) needs a day-indexed crop bias — see CROP-DAY dispatch below.
- Report `docs/strategy/2026-09-14-wheat-slope.md`; tools/data `S/wheat_slope/`.
## 2026-09-14T09:05Z — MACRO-EXTRACT closed: crew ramp and herd are expressible by theta; the crop programme is a capacity limit

- VERDICT: direct fit of all 7,020 coordinates (Adam, no sigma limit) on 180 ymg_aq dawns drives crew_target residual to 0.03 hands/day and the three animal_want channels to 0.03-0.07 (EXPRESSIBLE), but the five crops share ONE softmax over grow scores, so a block programme (d2 = 11 wheat/0 else, d3 = 6 strawberry) has no theta solution: wheat 70 % closed, strawberry/melon collapse to 0. That is a CAPACITY limit, not the step-size limit of melon-reachability §4. Fertiliser, sale day/hour/lot, market purchases have NO decoder channel.
- They do / we don't: 4 hands on d0 and 11 by d10 (all three teams; B decodes 0.0 hands d0-d5, 5.0 at d8); wheat standing board 16.5-19 tiles at d10 vs B's 9 (+1,145 re-bought units vs 141); broke on purpose through d10 (350-1,355 coins vs B 1,415/6,124) then 18.6-25.8k at d15 vs 7.8k.
- Missing Macro channels for the executor: sale day/hour/lot size, fertiliser application, product purchases, non-monotone per-day crew (logistic ramp cannot dip), day-indexed crop-mix bias, development above dev_frac*n_free.
- Seed S/macro_extract/seed_ymg_aq.npy md5 3b6040a6 (NO game played yet). 18 macro JSONs for all TOPB3 top-five seats in S/macro_extract/. Report docs/strategy/2026-09-14-macro-extract.md. UNVERIFIED: B's per-day hires/fertilise/sale lots (ledger snapshots dawns where the roster is empty). S/toptier_0911 is not in this tree (SpaTaro/Crop Dusta not extracted).
- Dispatched SEED-SCREEN: paired CRN sim of crew-only, crew+herd and full fits vs B on the 6 ymg_aq and 68 band boards.

## 2026-09-14T08:59Z — TAPE-FIX closed: hire-sticky replay lifts top-five retention; USER authorizes remote launches

- USER: "launch training yourself, permissions granted to upload training packages to remote, start, stop, and kill training process." (Kaggle uploads remain the user's.)
- VERDICT: the desync is a CASH SPIRAL after a refused day-1 HIRE (8 submitted / 3 landed; over-long hands lists are never rejected, kaggriculture.py:282/907), not an index misalignment; `_align` truncation was already correct. Fix = scripts/tape_opponent.py --hire-sticky / TAPE_HIRE_STICKY=1 (default OFF): re-issue owed HIREs behind the tape's market list, capped at the source roster, cleared at the day boundary. tests/test_tape_hire_sticky.py 11/11; flag-off control 36/36 coin-identical.
- Measured: TOPB3 retention Majkel1337 0.25->0.52, DSM 0.65->0.74, ymg_aq 1.02 identical; retained set 7->10 boards, B there -12,599 (t -5.54) -> -5,384 (t -1.24); NEXTHIGH ON = B -7 coins/board, 54/60 coin-identical. Five boards stay < 0.5; 108741964 regresses 0.75->0.40 (unexplained). The es.tape_actions SIM seat does not carry the reflex yet (TAPE-PORT dispatched). Re-cut packages before promoting (48 re-cuts predate two docstring corrections). Report docs/strategy/2026-09-14-tape-hire-fix.md; tools S/topb3/hirefix/.
- Dispatched: TAPE-ARM (flow214: B seed, MELON_GENE_ON, flow193 rung + the 6 ymg_aq pinned tapes, launched on the remote by me) and TAPE-PORT (hire-sticky reflex in the training sim seat).

## 2026-09-14T08:56Z — WOOL-MECH closed: not a sell defect; early sheep-days and care cadence, both unreachable

- VERDICT: B sells 100 % of its wool (0.00 unsold at d29, produced = sold 121.67); lot walk favours us (-0.31 c/u vs their -1.80). The -5,659 splits -2,460 volume and -3,199 price; the price half is sale-DAY MIX from ymg_aq owning 3 sheep at d1 to our 1 (d0-9 sheep-days 28.8 vs 10.5). 65 % of the volume gap is wool per sheep-day 0.930 vs 0.995/1.081 (same constant vs both classes): eod.refresh_animals pays 1 + care-bank per 3-day fire, ceiling 1.333, we run at 70 % -> a CARE+FEED hand-cadence effect, worth ~+9.3k UNVERIFIED (ignores own price impact).
- Reachability: sale timing has live coordinates hold[7]/press[7] but slope 0.079 day per sd at sigma 0.02 -> 12.7 sd per sale day, NOT REACHABLE; both HOLD perturbations lost (-13,934/-14,462 vs -13,722). Identity gate 0 coins. Correction: melon-reachability §8 is a day-0 plant gene, not a sell-day gene.
- Report docs/strategy/2026-09-14-wool-mechanism.md; tools S/wool_mech/. Consequence for the macro path: early animals (d0-d1) and hand cadence for care are macro channels the executor must carry; sell-side needs nothing.

## 2026-09-14T08:54Z — LEAD DECISION: tape-seeded initialisation, outcome-only promotion (user: "you the lead, so choose the best fast path")

- Diagnosis: nothing works NEAR B. B is a strict local optimum of a planner whose interface cannot express the top-five builds at training sigma (crop mix 70+ sd, mid-game herd 7-14 sd with zero gradient on head[6], wool sale day has no gene). The top five (ymg_aq 16-19 wheat tiles + day-0 wool, Crop Dusta 10 hands d10, zero idle turns) are different builds, not tuned B.
- Path chosen: (1) extract per-day macro trajectories (hires, animal buys, tiles per crop, sale lots/hours) from the top-five replays and fit a seed theta (gene ON) to them, reporting which channels the decoder can express; (2) build a macro-driven executor flag in plan.py so per-day targets override task-derived enumeration (the FORWARD_ADMIT postmortem: forced opening lost 94->26 % because hands/animals/tiles are bought together by the top and our enumeration prices hands on today's tasks); executability gate = our seat running ymg_aq's macro on its own boards must land within 20 % of ymg_aq's coins; (3) ES arm from the seed at a sigma matched to measured slopes, rungs = band + top-five tapes with the hire-robust replay; judge seven families, §115, hand file+md5 to the user.
- GOAL.md amended: tapes allowed as initialisation/macro targets only; promotion outcome-only. Streams dispatched: MACRO-EXTRACT, EXEC-SCOPE (plus TAPE-FIX, WOOL-MECH, WHEAT-SLOPE already running).

## 2026-09-14T08:41Z — HERD closed: mid-game herd growth (d3-d11) loses in every window and is unreachable by ES

- VERDICT: all 8 animal_want offset arms lose on 68 paired CRN boards (COW+1 d6-8 -1,009 t -3.22; COW+2&SHEEP+2 d6-10 -2,697 t -6.37; SHEEP+2 d6-8 inert -24), same sign on TOPB2 and LIVE-C, monotone in dose. Requests convert at 2-9 % on d3-d8 (cash-bound) and an unexecuted want still costs tiles (plant_total = n_dev - sum(animal_want), brain.py:992; +17.9 idle tiles at d10).
- More cows do pay fertilizer (+33…+766/board) but flood milk and hand wool/strawberry value to the opponent: the LOSS10 "fertilizer -7.3k with more cows" item is closed (right sign, two orders too small).
- Reachability: animal_count = qfloor(sig(head[6])*n_dev); B's share 0.043-0.073 gives 0 mid-game animals on 80/80 dawn states; one cow at d6-d8 needs 7-14 sd at sigma 0.01-0.02; the herd-mix block g8/gb8 has zero gradient on head[6]. Local-optimum result of 2026-09-11-integer-search §7 extends from d0-d2 to d3-d11.
- Report docs/strategy/2026-09-14-herd-growth-screen.md; tools S/herd/. Identity gate 0 coins on 68 boards. No engine leg, no finalist. Animal ACQUISITION line CLOSED; wool SELL side still open (WOOL-MECH).

## 2026-09-14T08:41Z — LEDGER-TOP5 closed: the top-five deficit is a d15-29 wheat/wool/strawberry loss, not the melon pot

- VERDICT: only the 6 ymg_aq boards of TOPB3 are measurable (sim = engine to <=96 coins, pooled -13,722 vs -13,751, 0-12); the DSM board collapses to 0.32 sim retention and Majkel1337 desyncs entirely -> DSM/Majkel halves UNVERIFIED until TAPE-FIX lands.
- Band shape vs ymg_aq (ours - theirs, net of purchases): d0-9 +800 / d10-14 -13,502 / d15-29 -2,780. The d10-14 pot deficit is SMALLER than vs the band clone (-20,017); the whole change is d15-29 (+15,516 vs clone -> -2,780). E-C answer: a second opponent class, not the clone at higher strength.
- Three lines: WHEAT -6,619 (their 16-19 wheat tiles vs our 8.5-9.5; the 42k buy leg is price-neutral churn), WOOL -5,659 (we hold MORE sheep at d20, 6.5 vs 5.8, yet sell 13 fewer units at 177 vs 202; same sign vs every class -> B-side defect), STRAWBERRY -3,131 (second strawberry-first grower denies our price 137 -> 105).
- Report docs/strategy/2026-09-14-top5-ledger.md; tools S/topledger3/. Caveat: TOPB2/LIVE-C vs TOPB3 are different board sets (board-confounded cross-set comparison).
- Next streams dispatched: WOOL-MECH (why B under-sells its own wool, sell-side only; HERD covers acquisition) and WHEAT-SLOPE (does the crop-mix gene carry a wheat-tile slope the ES could learn, paired sim vs ymg_aq and band boards).

## 2026-09-14T08:36Z — MELON-R follow-up closed: OFF-path equivalence re-verified against the true parent

- VERDICT: MELON_GENE_ON=False decodes byte-identically to the pre-switch decoder (529d33d^): 1,920 decodes per backend (12 thetas x 80 dawn states, both backends) hash to the same digest 3b4e978f…45f9b680. Gene tests 8/8 pass; the earlier 143 exit was a 900 s timeout, not a failure.
- Substantive findings unchanged (docs/strategy/2026-09-14-melon-reachability.md §2-§6): 2.05-nat first-tile boundary, 71/168 sd cm/cb barrier, slope table z=+0.01/+0.02. Sell-day gene NOT implemented. Melon stays CLOSED per MELON-M; no arm launched.

## 2026-09-14T08:33Z — MASTER fast-forwarded to 5999db0 (user rule: master = code we run and submit)

- `git checkout master && git merge --ff-only feature/h-checkpoint-continuation` succeeded after the drvfs index.lock cleared; master head = 5999db0, working branch is now master.
- Reproducibility check (done before the merge): submission/submission_flow193_g100_hr.tar.gz (md5 adf27cb0) contains theta.npy md5 7fcf3948 and kagg3 sources byte-identical to src/kagg3 at the ship commit (UPLOAD.md: b1bde4f; also identical at c0934af). The only src change since is the default-OFF MELON_GENE_ON switch (529d33d), which decodes B byte-identically.
- Rule going forward: all work continues on master; any future upload commits the ship tree + submission/ payload on master before the user uploads.

## Historical checkpoints

**Resumed at the user's request.** The shutdown state below is historical.
Read consensus §§133–151 and the [complete Flow215 judge](2026-09-12-flow215-g10-judge.md).
Flow215 w00 completed ten generations; its explicit centre then completed all
seven separate judge families with exit 0 and a fully passing coverage audit.
All seven margin means are negative; H30 -869 (t=-2.56), H30B -715 (t=-2.82)
cross the prospective continuation guards. **Do not launch w01 under the old
plan or rerun the completed judge.** Root judge session 96175 is terminal.
Both GPUs are idle after the deterministic control. B and submission payloads are unchanged.


**Latest update after 20:08Z overrides historical status below.**
The isolated sequential executor now passes 40 focused locked-engine cases
(root15056), 32 unchanged scripted DROP/PLACE cases (root78034), and exact
archived/loop/unrolled equality across all27 State fields on688 conservatively
disjoint recorded vectors (root82784 exit0,19:54:22–19:55:02Z). The31 excluded
vectors were selected by the frozen input-only rule, not output differences.
Root87739 independently recomputed selection, all81 raw arrays and file/array
hashes without executing the simulator; PASS. Disjoint receipt
`ef11aca023b860217806d5962726fa17dd371ab1ed9dbd191ecadd3600e237c6`.
See [correctness results](2026-09-12-unit-order-correctness.md).

Overlay `S/unitorder/units.py` SHA b5aeeb2ca2563f8af64c87ea0a811f852776c4153abd0d6b111419b7a99f1e07.
It carries each worker's tile/shed/inventory changes forward in engine order,
after one atomic planting validation. Both loop forms match; default is
provisional until GPU measurements. Only the isolated stage changes.

Next reviewed gate: [one unchanged wide-crew full-season node](2026-09-12-unit-order-season-plan.md),
seed1164543749, CPUcap1200+kill10. Root45712 completed exit0 at20:08:27Z,
166.655seconds. Root37824 and independent Sol review audited the saved evidence:
185 bound files exact, one named JUnit case, zero failures/errors/skips, both
source/engine markers. Execution receipt49679a194c3ca5413e69981f7c3d078c36969758a7979da669b4fc8d81b1f40c.
Outputs S/unitorder/wide_season_20260912.{log,xml,execution.json,root_audit.json}.
It covers29EOD+final partialday and>=12hands with explicit private state gaps.
The enhanced hourly game is COMPLETE: root82935 childexit0 at20:33:08Z after
265.103seconds/cap1200, helperPASS, peak16hands. Original launcherexit1 is
preserved: pure validator imported ops.py without its package context and failed.
No game was rerun. Reviewed adapterac4a283 runs only the unchanged saved-evidence
validator with proper import context. Root82857 exits0/PASS, and independent
Sol audit agrees:720 canonical states,719 both-seat actions,168 rawarrays,
31 exact direct/instrumented boundaries, all188 boundfiles unchanged.
Original executiona2e7e718 and receipt91416bc1 remain untouched; separate
`S/unitorder/enhanced_season_20260912.root_saved_audit.json` records the audit.
No local game or GPU job is running. [Complete result](2026-09-12-unit-order-enhanced-season-result.md).

**User steering: stay focused on top five.** Do not expand this into an open-ended
simulator project. The bounded route is one exact captured tape fidelity case,
then GPU performance/repeatability qualification, then a fresh bounded training
run and separate-family evaluation against B if the gates pass. A new diagnostic
must address a concrete observed blocker to that route. Do not rerun completed
tests or restore closed Flow215 training.
[Next exact tape design](2026-09-12-row58-tape-season-design.md) has independent
design agreement after clarifying the actual-engine eval seam and keeping
internal metrics separate from engine comparisons. Case is tapephysical0 versus zero
policyphysical1: inputseat0/tapectl[0,3] overrides candidate actions. The recorded
seat0 collisions are tape replay behavior, not candidate-generated/B evidence.
Implementation and independent review complete, frozen in commit74e6146.
Root17719 completed the one CPU tape case (cap1200+kill10), fresh output
`S/unitorder/row58_tape_season_20260912` and sibling log/execution receipt.
Helpere7309970, auditord8f8246d, launcher3d355f43, planf6158c62.
Pure tests root62258 exit0/twoPASS; frozen120-input preflight root45517PASS.
Terminal exit0 at21:07:05.971758Z after389.291277seconds; helperPASS and root
saved-evidence auditPASS, plus independent Sol saved-only auditPASS in4.7seconds.
All720 physical states,719 both-seat actions,118rawarrays and140boundinputs
match. Final money[141865,59347], day10[17396,2172], tape0/zero1 only.
Execution4570f980, receipta6ca8626, raw e0e9e6b8; no game rerun.
[Complete result](2026-09-12-row58-tape-season-result.md).
Next implement the [bounded GPU qualification design](2026-09-12-unit-order-gpu-design.md).
It measures both loop forms on992 and8192 evaluator rows, with exact output,
memory, cold/warm timing and repeatability gates; proposed budgets are explicit.
OFF is the intended fresh-training/shipped contract; current ON case is fidelity
and timing evidence only.
GPU helpers implemented and reviewed: commit e1ee159, with setup correction
e8b6405. The first launcher stopped at21:35:47Z before any GPU arm because
stage_hr/artifacts resolves to /home/user/kagg3/artifacts; its zero-arm refusal
and all original sidecars/bundle/manifest are preserved. No performance result
or threshold was discarded. Seven pure tests pass after the symlink regression.

**GPU qualification v2 is TERMINAL / REFUSED:** root SSH session98842 exit1 at
21:51:13Z after473.161s. Loop-1 helperPID1070516 completed exit0/PASS, but82
monitor gaps exceeded200ms (maximum0.248824s). Independent saved-only audit
reproduces the refusal. Remaining three arms never started; no variant qualifies.
Both GPUs observed idle afterward. Do not resume/retry this frozen protocol.
V2 manifest e696b0ee binds141files; helper2a6b649d, protocold7ca66f5,
launcheraba9ea6c. Remote bundle
/home/user/stage_hr/S/unitorder/gpu_qualification_20260913_v2_bundle;
canonical output /home/user/kagg3/artifacts/unitorder_gpu_20260913_v2,
also reachable through stage_hr/artifacts symlink. Wrapper sidecars live beside
that output. All raw outputs and sidecars downloaded unchanged to
S/unitorder/gpu_qualification_20260913_v2. Executionc79edd84, receipt5721927e,
rawa1379161, monitor4f3c3fae; [refused result](2026-09-13-unit-order-gpu-v2-result.md).
One-arm outputs/state/source checks pass, but its timings are diagnostic only.
Next repair the observed subprocess monitor overhead with persistent NVML;
review/freeze a new prospective protocol without waiving any qualification gate.
[V2 setup correction and execution plan](2026-09-13-unit-order-gpu-v2-plan.md).
No fresh training, optimizer update, promotion or upload has occurred.

**Latest: new prospective NVML qualification LIVE, root SSH session92254.**
Commit403a16d freezes persistent monitor a5ca2e61, adapterbce47f1d,
launcher81a52864 and manifest888b4e2f (155boundfiles/131unchanged arm inputs).
The original arm2a6b649d and protocold7ca66f5 are byte-exact. Independent Sol
static reviewPASS and root93408 fourteen pure testsPASS. NVML v2 allocated
memory preserves nvidia-smi idle semantics; reserved memory is recorded
separately, not counted as allocated. Original and corrected idle API proofs
are preserved. Every original qualification threshold remains unchanged.

New remote bundle:
/home/user/stage_hr/S/unitorder/gpu_qualification_nvml_20260913_bundle.
Bundle a1ff5d2d (2298448bytes), canonical output
/home/user/kagg3/artifacts/unitorder_gpu_nvml_20260913; wrapper sidecars beside
the output via stage_hr/artifacts symlink. All155hashes/canonical paths/idleGPU
verified22:11:54Z. Started22:12:07.740567Z. At22:30:29Z, loop-1 and unrolled-1
both completed child0/helper/outer armPASS. Loop peak4962MiB/maxgap0.057651s,
unrolled peak5030MiB/maxgap0.060532s. Both raw outputs SHAa1379161 exact.
Arm receipts161e5caf and8d26aa16. Unrolled-2 helperPID1099113 is now running;
its first73samples hadmaxgap0.052924s andzero gaps>200ms. Loop-2 has not started.
These are two completed arms, not complete qualification or a selected variant.
Observe the same root92254/process until terminal; no retries or duplicate arms.
Four fixed arms,900each/3660+kill10 outer. Prior v2 refusal remains closed and
contributes no arm to this execution. [Frozen plan](2026-09-13-unit-order-gpu-nvml-plan.md).

Shipped/OFF source contract is complete: helper9d25fe00, receipt3db9c2bc,
S/unitorder/shipped_source_contract_20260913.json. Of17shared package modules,
16are exact; replace only archive plan8044a3c6 with exact packagedplan19ad2816,
plus the selected units overlay. Seed-room symbol is absent, other four switches
True; main/theta are exact submitted B. Pure source check and saved-hash audit
PASS; no game/import/runtime equivalence claim or additional fidelity suite.
[Next OFF confirmation/training design](2026-09-13-unit-order-off-training-design.md)
requires an exact selected-source initialization match in the fresh trainer
before generation1, then a proposed10800sec cap for ten fresh generations fromB.
No OFF GPU confirmation or fresh training has started. Keep the route bounded
to qualification, shipped/OFF confirmation, training, and separate-family judge.

**OFF implementation prepared and reviewed, commitdbb1e73.** Helper26e118a5,
saved auditor/protocol836858b5, launcher3f91de4b, execution plan212e916d.
Root54160 eight pure testsPASS; independent Sol final static reviewPASS.
[One selected OFF execution plan](2026-09-13-unit-order-off-confirmation-plan.md).
It requires the completed qualification/root saved audit/first selected arm
receipt, exact ON-reference992/8192 inputs beforeOFF eval, exact packagedplan
plusunits, raw992leaves, and B in theta/best_abs_theta/pool[0]. No ON/OFF output
comparison. Canonical externaldata remains the frozen NVML bundle above,121files
(B+120tapes);135local arm inputs. One900secchild/960+kill10outer. No OFF manifest
has been generated and no OFF bundle transferred: both depend on qualification
selection and the independent saved audit. Do not launch the bare helper.

Sol /root/postlot_mechanism completed the bounded training draft: new
S/unitorder/train_off.py f65fcc9d and test_train_off.py05a233ae; three pure tests
PASS. These are unreviewed/unstaged drafts. /root/rotation_snapshot now has a
15minute independent static review task; root review is still required.
Do not stage or launch before those reviews and any concrete fixes.
The training guard must match OFF inputs/output and complete cold/post-B state
before allowing the real first generation. No training outer/manifest exists.

Latest ladder is the19:43 saved snapshot: B228games/162wins, rating2654.3704,
teamrank349; fifth3028.2 (displaygap373.9). Raw/summary/pacing audit PASS.
B and submitted payloads unchanged. No new training, promotion or upload.
Root owns Git index; preserve user replays/. Topfive remains unachieved.

**Historical update18:47Z:**
Complete unit-vector step707 check passed: root85369exit0 in25seconds, root69518
independent audit58arrays/13engine snapshots/invariants/source/input/B exact.
Sole discrepancy persists: unit7CARROT4archivevs5engine, otherbothseatpaths exact.
Receipt a3225703dbea67dd6c3d71acb85ade55f611ca3af4127af002946ae60d3af35a.
[Plan and completed result](2026-09-12-row58-full-unit-phase-plan.md).
No simulator rerun in root verification. Unitphaseonly; fullturn/terminalunvalued.

Two independent repair reviews agree on the [complete scalar fold design](2026-09-12-unit-order-repair-design.md).
Author next_lever owns new S/unitorder/units.py overlay; rotation_snapshot owns
new test_unit_order.py; postlot_mechanism reviews subtle semantic traps. Root
stager/run_staged_tests bind existing tests to an isolated archived source.
No amended kernel or new repair test suite has run. Next: code review and freeze
finite correctness cases, stage fresh source, root CPU tests with timeout; only
after all correctness gates should a separate performance protocol execute.
Root owns index. No production/reference/payload/training/promotion changes.

**Historical update18:36Z:**
All17 isolated collision groups have now executed once: root38344 exit0,
18:27:55Z–18:29:20Z, CPUcap180, frozen plan dfde64e/helper8894df8.
Root32623 found original serialized engine snapshots aliased later mutations;
preserve that refusal and original receipt. Separately reviewed engine-only
verifier root83044 exit0/cap60 reconstructs all68 controls exactly against3077
preserved raw arrays, all hashes/masks/invariants pass. No simulator rerun.
Final result16 matches/one difference: step707/day29h11 seat0tile80, unit4WATER
then unit7HARVEST; sequential harvest3CARROT versus parallel2. Unit7total5vs4.
Verification ce0d5966250eb30e45399f41016d81c0c3dde520474b60f627d0a07b76a6a2bc.
[Full result and evidence caveat](2026-09-12-row58-all17-result.md).
Original13 intermediate engine snapshots stay invalid; use raw evidence plus
new engine verification. Deep-copy mutable engine projections in future tools.
No complete-turn/terminal/B-policy/GPU-liveness causality claim. Two independent Sol reviews agree on one complete unit-vector step707 gate;
[prospective plan](2026-09-12-row58-full-unit-phase-plan.md), unimplemented/unrun.
Next: stage that helper and focused tests, independent code review, then one
root CPUcap180 call with strict both-seat/raw-state/action/inv_seq gates. No repair/training/promotion. Root owns Git index; goal remains active.

**Historical update18:25Z:**
The corrected trace root26261 completed exit0 at18:13:19Z in480seconds.
Direct and instrumented both match the frozen12-int32 target; root verified
719 ordered steps, all31 arrays,27 State schemas and complete source/input/tape
identity. Both GPUs idle and trace PIDs absent. Receipt
`d6afef93bc1fc57b1125d723440416b72a61e52dce1d295094c46ba254244a0e`.
[Complete trace result](2026-09-12-row58-trace-result.md), commit a69c6b5.

All17 collision groups are on seat0, with zero duplicate HARVEST groups.
The old HARVEST-only helper remains unexecuted and has no eligible case.
A new post-trace audit of every group is frozen in dfde64e:
[all17 plan](2026-09-12-row58-all17-plan.md). Two independent design reviews
agree; the new helper is under root and independent code review, unexecuted.
Root will run it once on CPU under timeout180+kill10 only after review/tests,
then audit all singleton/sequential controls and raw evidence before interpreting
matches or differences. No full-turn or terminal proof follows from this check.
Captured candidate theta differs from submitted B; do not call these B collisions.
Latest ladder remains18:08: B223/160wins,2656.69, teamrank339; fifth3022.9.
Root owns Git index; top-five goal remains active and unachieved.

**Historical update18:11Z:**
Root26261 remains live, instrumentedphase. Freshdirect undercuda,cpu completed
18:09:16.838Z and rootverified exact original12-int32 target/bothprioroutputs.
Directcheckpoint420a5e31edb65d8af485ff3d93c3934707f62ee42da7651297366ae60fb77fda,
CPU/GPUavailable, GPUdefault, correcthelper/env. No instrumentedresult yet.
Latestladder18:08 snapshotd128e28: B223/160wins, rating2656.69245,
teamrank339/display2656.6; fifth3022.9,gap366.3. Fiveadditionalgames/onewin
since17:05. hr332/208wins,2612.92018. All3publicresponses200, rawhash/summary
recomputed; original5secmonotonicguard used but oneUTCgap4.998759s, strictUTC
assertionnotpassed. Futurehelpermargin5.1seconds saved, no requestrepeated.
[Snapshot and pacing audit](2026-09-12-ladder-1808.md). Topfiveunachieved.

Corrected dual-platform row58 trace is LIVE root26261, started18:05:19Z,
timeout1065322/python1065323, cap900+kill10. ActualprocessGPUUUID maps tophysical
GPU1 GPU-<uuid>. Newhelper
3ff5f92df7d133aa111515bd7e338f5070f4cc32461ee629339a12e2e8dc7b2c
changes runtime initialization/guards/provenance only: JAX_PLATFORMS=cuda,cpu,
GPUdefault/CPUcallback available, strictCUDA1/cacheenv. Evaluator/source/input/
originaltarget719guards unchanged. Twoindependent reviews plus finalguardreview,
three inherited root tests pass; plan69d7cb5/launcher74335dc committedbeforelaunch.
All150remotehashes matched18:05:04Z, bothGPUsidle; currentmanifest
ac9502428aa38debbd36dd8d326f3e930526906e1ac090b4b758c8268d65d30b.
Remoteoutput artifacts/row58_trace_gpu_cpu_20260912 +sidecars. Observe samehandle,
no automaticretry/case substitution. Freshdirect must match originaltarget and
both priorcheckpoints under newruntime, instrumentedmustmatch+719steps before
interpretation. [Plan](2026-09-12-row58-gpu-cpu-plan.md).

Actual tinyGPU callback v2 root9461 PASS17:59:53Z (2s,cap60), all3callbacks/
93rawarrays exact and CPUresident, defaultGPU, direct/callback/fixedmath exact.
Receipt60d74c5996fa1ade03bbed20c57be24c451c52a80620c37d2aefc18920023a45;
rootaudit/all7remotehashes pass, fourpuretests. Firstprobe40549 also exactbytes
but originalNumPy-onlyguard refused actualCPUJAXarrays; preserveREFUSEDreceipt.
No game step in eitherprobe. [Evidence](2026-09-12-gpu-callback-compatibility.md).
Old CUDA-only failedattempts below remainunchanged. Eventchecker is still bound
to oldhelper and must be deliberately rebound/reviewed only aftervalidnewtrace;
no eventexecution or source repair yet. Agents idle, rootobserves/indexowner.

**Historical terminal CUDA-only state at17:46Z.**
The budget900 follow-up root57303 is **terminalexit1** at17:43:12Z after470s.
Direct checkpoint exact and byte-identical prior e38841aedd975f6198036ada089632130afcd961298248baf6165804e0d7c979.
Instrumented JAXdebugcallback failed: frozen `JAX_PLATFORMS=cuda` excludes the
CPU device required for callback dispatch. Zero trace steps, emptytraceNPZ,
invalidreceipt; no computedinstrumented result or collision evidence. Root
verified all8remote/local hashes; timeout1059692/python1059693 absent and both
GPUs1MiB. Receipt6815b48d2eac6fd0bb56a60df5c4a56d1f90a5598e1239464f96c8373c326299;
all evidence under `S/seedrank/row58_trace_budget900_20260912/`.
[Plan and failure](2026-09-12-row58-trace-budget900.md). This fixed execution plan
ends with no further retry/case substitution. The old300sec attempt is retained.

Conditional CPU event helper is reviewed and staged only, not executed:
`S/seedrank/row58_harvest_event.py`, SHA523a42c840261238b2c9850898063e99052f06d61763ecd0944f63e4b3234dab.
Five focused root tests pass and final independent review converged.
No validtrace means no eventrun. It retains
full descriptive census and firstduplicateHARVEST isolation, with raw/semantic
outputs, singleton+maskedsequential engine checks, precise inv_seq invariance,
strict source/input checks. FullturnUNVALUED, no terminalcausality claim.
[Conditional repair readiness](2026-09-12-unit-order-repair-readiness.md) records
two independent reviews: a complete unit-index action fold is the semantic
boundary, not HARVEST-only scatter repair; loopform/performance is unresolved.
No repair is implemented. Any future instrument design must prove actual GPU
callback compatibility before an expensive episode, preserving both failures.
The prior CPU-only smoke did not cover CUDA-only callback dispatch.

Root owns the Git index. The top-five goal remains active and unachieved.

Latest [17:05 ladder snapshot](2026-09-12-ladder-1705.md), commit57d330c:
B218 completed/159 wins, rating2668.8355, teamrank308; fifth3019.2,
displayed gap350.4. Three paced public requests all200; raw hashes and summary
independently reproduced. B last40W26/+52.32rating; hr328/205wins,
rating2604.8793,last40W17/-27.39rating. No pooling, import or upload.

The [first selected HARVEST fixture](2026-09-12-harvest-suffix-fixture.md)
is complete, root24343 exit0 cap180 after four root tests and independent review,
commit9887606. Fixed107764944/seat0/day8/seed1408844682, HIREhour11,
NORTH,NORTH,HARVEST12–14. All3WHEAT banked, nooverflow, hiringcost21.
All undeclared pre-EOD physical state exact, both seats. Crop removal changes
third town shop YARN_STORE to PET_CAFE through shared EOD RNG. This is physical
proof only; displaced future yield/prices/replanning/opponent impact unmeasured.
Receipt5c01725ac8e5aa73bdb87ebd8e5d0c7ed09225095342d04f3356481457951e54.
No full17/84-case campaign or performance pilot has launched.

**Fixed row58 trace is terminal and incomplete**, root39301 exit124,
started17:23:52Z, finished17:28:52Z at the original300second cap. Direct archived
12-int32 output exactly matches frozen row58. The instrumented phase timed out
before any traceNPZ or finalreceipt; no collision census/causal inference exists.
Directcheckpoint SHAe38841aedd975f6198036ada089632130afcd961298248baf6165804e0d7c979.
All six fetched remote/local file hashes match; root audit and logs/times/exit
are preserved in `S/seedrank/row58_trace_20260912/`. Timeout1057096 andpython1057097
are absent; both GPUs1MiB. Do not automatically retry or substitute another case.

Helper3fa9d8c, launcher/manifest6b6567e; three focused root tests and independent
final review pass. All141 remote inputs matched before the one GPU1 launch.
Direct identity is established; actual collision exposure and liveness cause
remain unresolved. Two independent reviews reconciled a conditional CPU fixture:
retain full descriptive event census; first supported duplicateHARVEST only,
allothergroupsUNVALUED; require every singleton and collision-only masked
sequential archived path equal lockedengine before comparing parallel result.
Semantic translation must preserve active fields and separately audit inactive
metadata. Fullturn gate additionally refuses atomicPLANT overdraw ambiguity.
**No trace means none of that postprocess can run.** Any new execution needs a
new concrete, reviewed plan accounting for measured compilation cost; no source
repair/population/training/promotion follows. [Evidence and conditional design](2026-09-12-row58-trace-plan.md).
All agents are now idle, root owns Git index; production/submittedB MD5 unchanged.

Exact row58 input capture root24129 is complete, not to rerun. Currentreceipt
84954905ab51606944cce39dd8f45508d42a7f89e1cd084a9b61c7d05ecd7473;
NPZ07454686620365bd8f06a0d6d0b2a5ef548bb1d91b87c0b087f4dbed7a096a49
under `S/seedrank/liveness_row58_inputs_20260912_root/`. Fixedrow58:
tape108100156,pair1,seat0,seed88567952,tape_ctl[0,3]. FullCLI inputtree exact
both previousGPUruns. No capture evaluation/population/update/checkpoint.

Liveness original51198 cached_repeat_mismatch (cached173elements/32rows,
retraced183/34). Deterministic13744 finished16:45:24Z exit0, three arrays exact;
flagged/unflaggedoriginal1161elements/221rows differ. Original population
comparison remains invalid. Root42447 constructed duplicateHARVEST fixture:
engine[3,0],archivedsim[3,3],singletoncontrol exact. Actual-tape exposure and
nondeterminism cause remain unresolved. [Evidence](2026-09-12-liveness-repeatability.md).

Static opportunity root54813 complete:84fundedrows,17selectedHARVEST routes,
67NO_RANKED_VISIT_FITS;35HARVEST/12WATER variants fit,5909ledgerentries,
2409nonpriority/unvalued. These alternatives are incompatible and not gain
counts. Firstselected exactfixture above is the only new executedroute.
[Funding/static evidence](2026-09-12-existing-assets-funding.md).

The original `S/snr/flow215_w00/g10/state.npz` SHA-256 is
`456b0b1934fad2ad904cd832bda1e8bddef69525fc46ea6f5bf2b6faacd2bf1e`.
Extracted centre `artifacts/kagg2_games/thetas/flow215_w00_g10s_hr.npy` MD5 is
`6585b78e3ed8bee29a3cfe59f717c3a3`. Final audit artifacts include exact metrics
and candidate/base CSV hashes. Production B remains
`7fcf39485bae65ee84171957c5843814`; top-five attainment is unverified.

Completed follow-up diagnostics:

- Root delayed-label retry **26093** completed exit 0 with all eight labels;
  all B own/opponent/margin values match the preserved ISEARCH simulator
  baseline exactly. Board deltas for the fixed day-5 compactness alternative:
  +626, +549, +144, -1777. No predictor or promotion evidence yet. See
  [validated labels](2026-09-12-planselect-day5-labels.md). Preserve its JSON,
  log, audit and dawn/day6 checkpoints; do not rerun the completed job.
- Seed-room engine pilot **036b2e1** completed on four H30 boards, both seats.
  OFF reproduces every main-judge field on 8/8 games. ON−OFF margin +41.5
  (board t=0.04); ON−B -1703.8 (t=-2.90). The source mismatch is real but
  supplies no demonstrated rescue. No full-family ON expansion or training
  extension is justified. See `S/flow215/seedroom-engine-pilot.md`.

The full thirty-tape H30-development labels and frozen calibration are now
**complete and refused**. Runner `2178a6d`, root session 1881, exited 0 at
15:01:46Z within 600 seconds; all sixty B terminal results exactly reproduce
the simulator baseline, and all eight original target rows remain identical.
Calibrator `5cfeb92`, root session 55291, exited 0; eleven focused tests pass
in agent and root runs, following seventeen pre-launch runner tests.

Frozen ridge gate margin **-130.25 per board (SE 110.77, t=-1.18)**; always
compact+1 **-192.00 (t=-1.14)**. Gate selects the alternative on 28/60 rows,
changing twenty plans. Hindsight maximum +187.63 is not a predictor result.
The predeclared continuation threshold fails: **no retuning and no held-out
engine pilot for this fixed day-5 selector**. H30B/NEXT were not used in fitting.
See [full result and artifact hashes](2026-09-12-planselect-all30-result.md).
Preserve all `day5_labels_all30*` / `day5_calibration_all30*` artifacts and
ignored checkpoints. Do not rerun either completed job. Those experiment
handles are terminal. The new paired GPU audit below is terminal and refused by its original ON reference. Two Sol agents completed bounded
read-only independent reviews of the missing existing-asset hiring census; no
census or new performance pilot has launched. Their scope was reconciled and the two-case fixture now passes; see
`2026-09-12-post-sale-existing-assets-review.md`. The liveness reproducibility diagnostic below is live on GPU1; all Sol agents
are idle, and root owns observation and the Git index.
No production change, promotion or upload follows. The old Flow215 continuation
and this selector are closed.

New work at 15:33Z: independent Sol reviews agree that the seed-room source
mismatch has not been measured across a perturbation population. Root froze
[a no-update audit](2026-09-12-seedroom-population-plan.md) in `dfeae9e` before
outcomes. Reviewed helpers `S/seedrank/` are committed as **8674216**, with six
focused tests passing in root's run. Root/independent review corrections are
complete. No population rollout has launched. The first CPU preflight, agent
session 9300, is terminal exit 124 with no receipt; timeout 240's TERM was caught
by the imported driver, so root verified and killed probe PID 44310. Preserve
`S/seedrank/preflight_timeout.json`; it is not a pass.

**Root CPU retry session 8537 is terminal exit 1.** It completed actual CLI
initialization, then failed before capture because the helper guarded a
nonexistent `Trainer.save`. No population rollout/update or receipt exists.
Preserve `S/seedrank/preflight_retry.log` and `preflight_guard_failure.json`.
Root fixed the guard to actual `apply_gradient`/`_snapshot` methods; the CLI
checkpoint block is unreachable after StopSetup unwinds the driver. Seven
focused tests pass, including the archived Trainer interface. Independent
review also agrees on symmetric JAX cache clearing after choosing the mode;
this prevents OFF from reusing ON initialization traces without changing RNG.

**Corrected root CPU capture session 2368 is terminal exit 0**, completed by
15:49:04Z under `timeout -k 10 900`. Actual CLI initialization and generation-0
capture pass: candidates 4096×6789, eps 2048×6789, 120 frozen tape episodes and
expander2/rusher2; no population rollout, optimizer mutation or checkpoint.
Receipt `S/seedrank/preflight_corrected/preflight.json` SHA-256
`d57363d528b0324c7e7a51cbcb0b8d5571476d19ddb42abe728dcbf30719c239`.
All seven focused tests pass; root rechecked both B MD5 values. No cached
liveness substitution was used. Reviewed fix/launcher commit **0be388c**.

All **133 updated remote input hashes matched** at 15:46:44Z (commit
**d2cb16a**), preserving the earlier 132-input manifest and sync receipt.
Launcher independently checks the CPU receipt against actual remote source,
manifest, B and ordered tape bytes, and verified both GPUs idle immediately
before starting. See `S/seedrank/remote_sync_reviewed.json` and launch receipt.

**Paired audit root SSH session 18616 is terminal**, finished **16:05:31Z**,
ON exit1 / OFF exit0. Both GPUs are idle and the original timeout/probe PIDs
1040190–1040193 are absent. No optimizer/update/checkpoint occurred.

ON failed its strict original-reference check: mean **0.6280547380447388**
versus **0.6280192732810974**, best exact. Raw outcomes differ by 36 half points
(equivalent to18 wins over507904 episodes). All paired input identities and
remote/local raw array hashes pass, but `compare.py` correctly refuses with
`valid:false`. **Do not interpret ON/OFF ranks, waive the expected score or
restart the pair.** Preserve `S/seedrank/seedrank_pair_20260912/` including its
large ignored arrays. See [reference failure](2026-09-12-seedroom-population-reference-failure.md).

Both current initialization probes ran ON before toggle/cache clear, yet their
rounded liveness rows differ19/124 (original versus currentON20/124). Root
reproduced this upstream numerical/process/device variation; exact mechanism
is unresolved. **ON-only liveness diagnostic is live: root SSH session51198**, started
**16:22:20Z**, GPU1 timeout/probe **1047223/1047224**, `timeout -k 10 900`.
Helper `S/seedrank/liveness_repro.py` committed **1ee5de8**, independently
reviewed; six focused root tests pass. All136 staged source/helper/input hashes
matched at16:21:53Z and both GPUs were idle before this single launch.
`S/seedrank/liveness_launch_receipt.json` preserves the launch. Remote output
`artifacts/seedrank_liveness_repro_20260912`, with adjacent `.log`, `.started`,
`.exit`, `.finished` files. Initial log is actual CLI initialization/original
liveness. Observe the same handle/PIDs, never restart on observation timeout.
No local CPU campaign process is live.

This captures exact raw992×12 initialization output/arguments, then repeats
cached and after JAX cache clear on the same device. ON stays true, no generation
population or optimizer is entered. Do not edit helper while live. After exit,
preserve/fetch outputs and verify all raw/input hashes before interpretation.
Even three identical calls prove only this initialization's same-process
repeatability; backend/persistent caches may survive, and the larger population
program remains unverified. The strict failed original-ON check stays failed.

The agreed hiring-review contract is now resolved. `S/hireasset/` stages actual
seeded-engine suffix fixtures for a PASS hand and one fixed productive WATER.
Independent review accepted the two-case plumbing and required additional
assertions/provenance, now addressed in v5 and committed **07f5e46**. Five focused
tests and an exact agent replay passed; **root tests8956 and replay37845 are terminal exit0** under cap180.
Root exactly reproduces v5 receipt SHA f0983ea1b86229918f10e6d7248c96c199de2ae0424fd14b75e681b111955ae8. Reserve/all-liability eligibility,
full B12 enumeration and other operation coverage remain pending; no funded
opportunity/census/pilot/performance claim exists. Seeded engine replay can
handle topology/RNG changes; static approximations cannot close those cases.
Root owns Git index; agents wait for explicit commit clearance.

Latest [16:00Z ladder snapshot](2026-09-12-ladder-1600.md), **c42d021**:
B211 completed/153 wins,2647.7103,teamrank349; fifth3025.8. Last40 B26wins,
+54.06rating. hr322/202wins,2605.3682,last40W18/−16.41rating. Exactly3paced
requests all200, no retries/import/upload; root verified hashes and summary.
Top five is unachieved. The following15:08 snapshot is historical.

Fresh [15:08Z ladder snapshot](2026-09-12-ladder-1508.md), commit `32ef9f9`:
B has 205 completed games, 149 wins, latest rating 2639.47 and team rank 362;
fifth place 3016.3. Last 40 B games: 26 wins, +54.16 rating. hr has 317 games,
201 wins, rating 2619.06 and last 40 rating -8.68. These are observed per-file
outcomes, not a forecast or pooled statistic. Three paced public requests
completed without 403/429; no replay import or submission followed.

The corpus now contains 175 fidelity-verified archives, 159 eligible tapes,
16 unchanged rejections and zero judge overlap. The immutable
`S/flow215/w01_manifest/` retains 90 launched tapes and adds 30 new ones; see
[successor staging](2026-09-12-flow215-w01-staging.md). Converted-checkpoint
loader checks, full CPU resume initialization and a guarded ten-additional-gen
launcher are implemented (84e773d, 762cc2b). Loader fixture tests passed, but
**actual w00 conversion, full resume initialization and successor launch have
not run**. The judged shipped-switch centre failed its continuation guards. Any
new rotating-support experiment needs a new concrete rationale and those
prerequisites; the old w01 continuation is closed. Apply the prospective
[continuation budget rule](2026-09-12-flow215-continuation-rule.md), recorded
before g10 outcomes (486aa01). Do not treat loader-unit proof as real Trainer
initialization.

Completed mechanism findings:

- [Fertilizer premise correction](2026-09-12-fertilizer-premise-correction.md):
  the original thirteen replays show early fertilizer quotes 77–100, never
  8–30. The old 1,915-coin allocation was gross revenue, not net arbitrage
  profit. This premise does not justify a storage-buy pilot (1186a27).
- [Public vacancy census](2026-09-12-forward-vacancy-public.md) finds no
  ten-day vacant targets in its six route opportunities. The fixed B12 cache
  includes ten earlier loss-selected replays; it is a convenience sample.
- [Post-sale hire census](2026-09-12-post-sale-hire-census.md) finds twelve early
  priority watering routes on seven episode-days. Other legal work remains
  unvalued; this is not a total labor-value ceiling (003a434). No new pilot.
- [Complete-plan selection review](2026-09-12-runtime-plan-selection.md)
  distinguishes an observation-only conditional selector from closed fixed
  offsets. Hindsight oracle variation does not establish a usable selector.
  [NumPy timing](2026-09-12-numpy-plan-timing.md) and
  [branch identity fixture](2026-09-12-planselect-branch-fixture.md) passed
  (d473668, 8a1ce68). Four builds take 364 ms median locally; offline B branches
  reproduce normal simulation exactly. Neither is a performance result.
  The bounded first-four-development-tapes season-end run timed out; its
  instrumented retry completed and validated all eight labels above. No
  successful learned selector has been established; the full development
  calibration above is now refused.

Local acquisition and cutting are complete. Root coordinates bounded Sol tasks.
Agents must obtain root's explicit index-free clearance before staging/committing.
Preserve all completed artifacts and use CPU local Python through `.venv/bin/python`.

## Historical shutdown checkpoint (12:09Z)

The user requested: save all work, stop agents, prepare continuation docs, and
continue after restarting the terminal. **All campaign processes are stopped.**
Do not restart anything until the user resumes. The top-five goal remains
unfinished; this shutdown is not a claim of completion or a research blocker.

## Goal and standing instructions

- Continuously improve the Kaggriculture agent toward **top five**, obeying the
  competition rules. Root coordinates **Sol subagents**, with bounded tasks and
  process timeouts. Do not pool evaluation-family statistics.
- Commit every completed code change with explanatory Git messages. Preserve
  experimental artifacts. There is no Git remote; Git is not a disk-loss backup.
- Use `JAX_PLATFORMS=cpu` for local Python. Do not modify reference engine or
  evaluation semantics, production `src/`, submitted payloads, or user `replays/`.
- Rules were checked in consensus §122. Public replay acquisition is permitted;
  stop at the first HTTP 403/429 and honor recorded endpoint cooldowns.
- Append `S/glut/verdicts.log` only using `echo ... >>`. No automatic watchers,
  loops, uploads or training should restart merely because a terminal opens.
- Codex auto review is enabled in `/root/.codex/config.toml`:
  `approvals_reviewer = "auto_review"`; TOML parsing was verified.

## Verified stopped state

- Sol agents `fresh_support`, `smoothie`, and `rotation` were explicitly stopped.
  A host process scan after their shutdown found no campaign process, including
  `on2b.py`, pilot, acquisition/cutter, trainer or auto-judge processes.
- Remote Flow213 training previously finished `done` / `EXIT=0`; trainer PID
  1027398 was absent. Both remote GPUs reported 1 MiB. No later remote launch
  occurred. Remote host: `user@remote-host`, tree `/home/user/stage_hr`.
- Root judge handle 39524 is terminal exit 0. Pilot child handle 75668 is terminal
  exit 1 from a post-run verifier bug; its games are complete (details below).
- Acquisition child handle 46143 was interrupted with KeyboardInterrupt. No
  download or cutting job followed it. Old handles are historical, not restart
  instructions; inspect actual processes before launching anything.
- A last seed-room diagnostic finished during shutdown. Root's scan initially
  saw group 7161 running `on2b.py`; by the targeted stop check its PID was absent.
  Both eight-row CSVs existed and were saved. An agent's earlier claim of no CSV
  was stale; use the saved evidence below.

## Completed findings

### Flow213 g10: no demonstrated improvement over B

Training completed ten generations. Archive:
`S/snr/flow213/state_g00010.npz`, SHA-256
`b05057206c1ddee5e6f5961a094cab49de625a033081fb84b57af6558347272b`.
Extracted theta: `artifacts/kagg2_games/thetas/flow213_g10s_hr.npy`, MD5
`7401152d1a73e4565571c02042d947e7`, 6,789 finite parameters.

Strict coverage audit validated all seven complete families against B:

| family | boards | margin delta | board t |
|---|---:|---:|---:|
| TOPB2 | 20 | -435 | -0.83 |
| H30 | 30 | -59 | -0.38 |
| H30B | 30 | +110 | +0.35 |
| LIVE62 | 62 | -299 | -1.62 |
| LOSS10 | 10 | -381 | -1.26 |
| NEXT14 | 14 | -284 | -0.50 |
| NEXTHIGH | 30 | -272 | -0.75 |

No promotion or automatic extension. See
`docs/strategy/2026-09-12-flow213-g10-judge.md` and
`S/autojudge/audit_candidate.py`; seven focused audit tests cover coverage
failures. Flow211/212 g20 were already refused by separate held-out screens;
do not repeat those completed checks.

### Post-sale seed hook: productive crops, adverse H30 result

Files are under `S/postlot/`; the hook is default-off and experimental.
The isolated tree is byte-identical to arms-next across 36 Python files and can
be verified/rebuilt with `S/postlot/stage_tree.py`.

Initial pilot plants all died at their first day boundary. The correction
reserves one additional idle turn and waters immediately after planting.
The full corrected `h30_water` run completed 60 games on 30 H30 boards:

- 44 injected crops were purchased, planted, watered, survived and harvested
  at yield six. Actual engine functionality is established.
- Margin versus B **-256.83**, SE 194.02, board t **-1.32**; own coins +134.87,
  opponent coins +391.70. Wins 63.3% to 60.0%; flips 0 wins / 2 losses. Twenty
  game margins are identical. This does not support promotion. H30B is unrun.
- The runner exited 1 only because four WATER actions at hour 23 were checked
  after day-end reset of `watered_today`. All four crops survived and were
  harvested. The verifier is now corrected; six focused evidence tests pass.
  Root checked all 44 purchase/plant transitions and the four reset cases.
- Preserve `S/postlot/pilot/h30_water.csv`, `debug_h30_water.jsonl`, its 60
  replays and log. The earlier tags `on` / `on_smoke` had a trace NameError and
  are invalid; `h30_final` was deliberately aborted before the watering fix.
- Compare by normalized `(seed, opponent tape, seat)`: the pilot writes absolute
  opponent paths, while `S/lossflip/sell5off_B_livech.csv` uses relative paths.
  A raw-string path comparison falsely reports zero matches.

Read `docs/strategy/2026-09-12-postlot-pilot.md`. Do not blindly launch H30B or
promote this implementation; the current result is adverse despite harvesting.

### ROTBAND: 58 selected episodes still need processing

At shutdown: **119 selected episodes**, **61 downloaded and fidelity-verified
archives**, **45 eligible tapes**, **16 retained provenance rejections**,
**zero windows**. The latest acquisition saved 58 additional selections before
interruption; they are neither downloaded nor cut. No 403/429 occurred during
that interrupted batch. All selections are atomically preserved in
`S/rotband/episodes.json` and `epseat.txt`.

Do not reacquire these selections. On resumption, process them first with the
existing downloader and checksum-skipping cutter, bounded to two workers.
If all 58 pass, eligible support becomes 103: at least 18 additional eligible
tapes are then needed for the normal builder's minimum pool of 121 and a real
120-tape window. More than 119 selected does not mean 119 eligible.

The picker enforces at least five seconds between every attempt, including
after ordinary errors. It supports `--max-requests`; the last batch was bounded
to 80, interrupted after 58 accepted requests. Preserve the existing stop
state in `S/rotband/http_stop.json`. The current 180-team list originally had
139 eligible targets; the cached leaderboard has 441 eligible distinct teams
if a later deterministic expansion is needed. Do not lower thresholds or use
any evaluation provenance to fill a window.

### Flow215 prerequisite and source snapshot

`S/flow215/dry_run.py` validates a real 120-tape window first, then initializes
the actual trainer on CPU with pop 8 / zero generations in a temporary cwd.
It checks 120 pinned + four carried episodes, 1,191 trainable genes, exact tape
identities and B theta. It has not initialized yet: the window is still absent.

The remote source enables `SEED_ROOM_PURSE_ON`; arms-next lacks that patch.
Use an actual training-source snapshot for the dry run. Root saved the original
archive inside the workspace at:

`S/flow215/remote_source_20260912T1202.tar`

SHA-256: `520619b2ab7c7395ffcd214e27b0d3b41c2b0f1a10e6394129fb7d2b20264169`.
The current extraction is `/tmp/flow215-stage-hr-20260912T1202`; if absent after
restart, restore from the workspace archive into a new temporary directory.
The archive is preserved locally and ignored by Git. See `S/flow215/DRY_RUN.md`.
Preserve the venv interpreter path; do not resolve its symlink to system Python.

Historical consensus §69 intentionally enabled seed-room for training while
leaving it OFF for shipped evaluation. B is invariant, but some perturbed
thetas are not. The final **four-board H30 diagnostic of Flow213 g10** did
finish: seed-room ON and OFF produced exactly identical own/opponent coins on
all eight games. Saved CSVs:
`S/seedroom/flow213_g10_False_pilot.csv` and
`S/seedroom/flow213_g10_True_pilot.csv`. This rules out an effect on those four
boards only; it does not establish invariance on every held-out family.

## Resume order

1. Read this file, the latest consensus sections, and `git status --short`.
   The only intended untracked item after shutdown is the user's `replays/`.
   Inspect actual local/remote processes before starting a job.
2. Process the 58 saved ROTBAND selections with bounded download/cutting and
   verification. Preserve all 61 old checksum records and the 16 exclusions.
3. Acquire the remaining eligible support through the normal endpoint, bounded
   and paced. Build real windows with the normal verifier, not a reduced size.
4. Once window 0 passes, run Flow215 static precheck and the actual-source CPU
   initialization; then verify/sync exact files and free GPU capacity before
   launching the already-staged ten-generation `flow215_w00` recipe. No GPU
   launch is authorized merely by the current incomplete manifest.
5. Judge its g10 centre on separate families; Flow215 keeps NEXT30 held out.
   There is no real-gate RECORD within ten generations, so archive/judge the
   centre explicitly. Later rotations require `rotate_checkpoint.py` and a
   fresh run directory; direct resume otherwise retains old tapes.
6. Reconsider the post-sale direction only with a concrete explanation for
   helping the opponent more than ourselves. No packaging or upload is ready.

Production B remains MD5 `7fcf39485bae65ee84171957c5843814`. No new submission
was uploaded, and top-five attainment has not been verified.

Latest saved code/evidence commits include 679c60c (watering boundary verifier)
and 3c2bc3d (interrupted selections and completed CSVs). Use `git log -5` for
the final documentation checkpoint commit.
