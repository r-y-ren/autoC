# Codex blind review of the §85-§102 conclusion chain — 2026-09-12

**Reviewer:** `codex exec` (gpt-6-astra, `model_reasoning_effort = high`), read-only sandbox,
blind brief (question + absolute file pointers only, no verdicts and no prior docs of ours in the
prompt). Full transcript: `S/codex/review_20260912.txt` (6,639 lines; the final answer starts at the
`codex` marker near the end, tokens used 174,405).

Invocation (the one deviation from the dispatch: the arms-next worktree carries `src/` but **no**
`docs/`, so the working root is the repo, which *contains* the worktree; the brief pointed the
reviewer at `.claude/worktrees/arms-next/src/kagg3/` explicitly for every source check, and its
citations show it read the worktree tree, not the main checkout):

```
timeout 1500 codex exec -s read-only -C /mnt/e/_work/kaggriculture3 "$(cat brief_chain.md)" </dev/null
```

The brief gave it R1 (promotion only on paired real-engine legs), R2 (two-purse rule) and R3
(held-out pinned tapes; in-sample reads void) as *our* rules and asked it to find violations **in
either direction** — closing a family on a sim number counts the same as promoting on one.

Below: each objection verbatim as the reviewer wrote it, my own one-line check of the cited file,
and a verdict. Line numbers are as cited; I re-read every one of them.

---

## Objection 1 — VALID

> **1. The weakest link is closing an interface family using a simulator refusal and one frozen allocator.**
> Attacked claim: **"No engine legs spent."** Followed by **"SELL-TIMING FAMILY CLOSED."**
> (`docs/strategy/2026-09-10-consensus.md:760`)
> … "SELL5 establishes limited benefit **at B's existing parameters**, not a capacity ceiling. Its
> 3.6% utilisation comes from one game; the document then calls those 52 units the training ceiling.
> But allocation explicitly depends on trainable pressure and reservation values. Observed
> utilisation cannot bound utilisation after fitting." **Confidence: high.**

**Verification.** Both quotes are verbatim at `consensus.md:760`. `sell21-build.md:212-220` does say
in our own words *"An ES arm trained with `KAGG3_SELL21=1` would be the fair test"* and *"Variant (c)
is the only member of the family this measurement has not refuted"* — and §90 declined it.
`sell5-falsifier.md:168-171` confirms the utilisation figure comes from `lotprobe.py` on **one**
engine game (tape 107448662, seed 777001, theta B), and `:268-272` says outright that a sell/press
arm *"is training the genes that decline the rows"*.

**Verdict: VALID**, with one deduction: refusing SELL21 *on the screen* is rule-legal — §49/§50
licensed the screen as a refuser (`consensus.md:505-516`), the screen validates sign 6/6 vs the
engine, and t −8.9 is far past the ±400/board resolution. What does not follow from that refusal is
the **family closure**: one screened variant plus one engine null at frozen genes cannot retire a
variant the same document names as unrefuted, nor bound what the genes would do if trained under
five lots. The chain closed a family on evidence that refutes one member of it.

## Objection 2 — VALID (the strongest practical objection)

> **2. flow211's weight shift survives the falsification of its rationale without receiving a replacement causal test.**
> Attacked claim: **"22.7 points of objective mass are currently being spent for nothing"**
> (`docs/strategy/2026-09-11-toptier-overfit.md:150`)
> "No comparison varies top-ten weight while holding the other training conditions fixed. Neutral
> performance under substantial weight could mean that weight prevents larger deterioration. The
> report itself says the risk of cutting it cannot be resolved. … Moreover, the reported
> lower-versus-upper differences yield an approximate Welch contrast of only **t≈1.77** … separate
> t-values of 2.20 and 0.29 do not establish a significant difference between effects."
> **Confidence: high.**

**Verification.** Quote verbatim at `toptier-overfit.md:150`; the same section at `:154-158` does say
*"The risk that cutting it enlarges the −1,274 held-out loss cannot be resolved here"* and
*"the TOPB2 damage tracks **step size and subspace**, not top-ten weight"*. The Welch contrast
reproduces: from `nextband.md:96-98` (lower +1,377 sd 2,344 n 14; upper +102 sd 1,410 n 16) the
difference is +1,275, SE 719, **t 1.77** — the two halves are not distinguishable, so §96's
*"B's edge decays … and by 2700 it is gone"* (`nextband.md:137-139`) is an underpowered null (the
upper half's own 95 % interval is roughly ±700 coins), and that null is the stated argument for
re-pointing 38 % of the objective.

**Verdict: VALID.** Three findings of our own reinforce it and were not in the reviewer's list:
(a) the staged recipe overshoots its own design — `strategist-next.md:72` specified *"top-ten
37.2 → ~15 %, 2550-2800 0 → ~20 %"*, the staged arm is top-ten **10 %**, NEXT30 **38.2 %**
(`flow211-staging.md` §2); (b) promotion is decided by TOPB2 / LIVEC-H30 / LIVEC-H30B / LIVE62
(`S/autojudge/watch.sh:39`) and the band column is explicitly informational (`:319`), so flow211
cannot be promoted on the hypothesis it is built to test, while it cuts the objective mass on the
one promotion leg where records already lose −1,274; (c) `band-gradient.md:118-124` pre-computed
NEXT30 as a **72 %-power confirmation of something four legs already say at t +3.48** and wrote
*"spend the hours elsewhere"* — the chain ran it anyway and then promoted its byproduct to the
heaviest rung family.

## Objection 3 — VALID on the statistics, PARTLY on the seed

> **3. The "not memorisation" test changes the training conditions and exaggerates its independent sample size.**
> Attacked claim: **"Memorising a training game's shop draw would show up as an in-sample gain; there
> is none to find."** (`docs/strategy/2026-09-11-toptier-overfit.md:123`)
> "The purported in-sample leg uses seed base 300777601, whereas training uses a hash of the tape
> name. … The pooled inference treats four records on each of twenty boards as eighty observations.
> My read-only recalculation from the published rows, averaging records within each board, changes
> held-out **SE 348→621 and t −3.66→−2.05**." **Confidence: high.**

**Verification.** Quote verbatim at `toptier-overfit.md:123`; `S/topb2/run_insample.sh:15` is
`SB=300777601` (a fixed seed base) while `es/train.py:1316-1331` seeds every pinned rung from
`pinned_seed_word(name)`, a blake2b of the ladder label — different random conditions, so the leg
measures *familiar opponents*, not *training trajectories*. The pseudo-replication is real: the
pooled row at `toptier-overfit.md:44` is labelled **"pooled, 80 board-cells"** = 4 records × 20
tapes, i.e. four correlated reads of the same 20 boards treated as independent; our own
`S/bank/paired.py:1-8` docstring already warns that dividing by √rows when the evidence is boards
*"inflated every published t by ~1.40x"*. I did not re-derive the reviewer's −2.05 from the raw
rows, but the per-record SEs (493-825, `:40-43`) make a record-level SE of 348 impossible unless the
records are independent, which they are not.

**Verdict: VALID** on the pooled t (the held-out effect is real; its significance is overstated —
read it as ≈ −1,274 at t ≈ −2, not t −3.7). **PARTLY** on the seed point: caveat 1 (`:170-172`) and
caveat 3 (`:178`) already flag the objective/coins distinction and the non-independence of the 20
rungs, so the doc half-registered the limitation; what it then asserted at `:123` went further than
its own caveats allow. The reviewer's third sub-claim — that the *"shop re-roll"* caveat (`:174-177`)
is inconsistent with town pinning because `scripts/town_inject.py:134` overwrites the unlocked shops
— is **INVALID as stated**: `town_inject` overrides the *town list* at the end-of-day refresh; the
per-empty-tile shop draw is the separate ±25k lottery of the shop-lottery memory, so the caveat is
correct.

## Objection 4 — VALID (decisive, and it is a source error)

> **4. "No open knob" rests on a false reading of the network and an unjustified "mistake-free" classification.**
> Attacked claim: **"Nothing in the ES's 1,191 trained genes touches the opening, hiring, tile mix or
> animal schedule"** (`docs/strategy/2026-09-11-nextband-anatomy.md:190`)
> "False in source: `b1` and `dh` alter the shared encoder; `gp` alters the global hidden state, which
> feeds development, crew, hiring, and other heads. Fixed output weights do not freeze outputs when
> their inputs change. … Its arithmetic also breaks: 14 changes/240 decisions is **0.058**, not
> **0.6**, changes per board-day." **Confidence: high.**

**Verification.** Quote verbatim at `nextband-anatomy.md:190`, and the source contradicts it on one
screen: `policy.py:635` is `pre = (x @ p.w1 + p.b1) + drain_feat @ p.dh` (b1 and dh move the shared
encoder), `:643-644` feed `press` (w3/b3) into `summary`, `:646` is
`gpre = (glob_feat @ p.g1 + p.gb1) + summary.reshape(N_PROD_SUMMARY) @ p.gp`, and `:648-650` take
`gh = tanh(gpre)` straight into `crew`, `head`, `prio`, `lots` — i.e. **every** block in the
train-only list reaches the head that sizes the crew, the land bias and the animal share. The same
paragraph also lists `g5`/`gb5` = `land_afford`/`free_urgency`, which are land knobs. The
arithmetic error is confirmed: `g10-decode-diff.md:75` reports 14 knob-changes over 240 decisions
(0.058/board-day) while `:141` projects from *"~0.6 coarse knob-changes per board-day per 10
generations"* — a clean factor of ten, and the g30 prediction of *"15-20 % of board-days"* rests on
it. §93's own decode already shows a crew_target 11→12 and an animal_want swap (`:76-78`), which alone
falsifies the anatomy sentence.

**Verdict: VALID.** §99's "no open knob" conclusion and its recommendation to judge on the upper
half are both built on a false statement about what the trained subspace can move. The g30 reading
rule (§93) should be re-derived at the measured rate.

## Objection 5 — VALID on the inference, PARTLY on the t-statistic

> **5. The timing ledger repeatedly converts an optimistic estimate into an exclusion proof.**
> Attacked claim: **"read it as 'their window choice is worth at most zero to them'."**
> (`docs/strategy/2026-09-11-timing-prize.md:173`)
> "An upward-biased estimate of the gain from replacing their schedule does **not** prove that
> replacement helps. The true gain can be negative. Consequently, 'None of the opponent's edge is
> window selection' does not follow. … And SELL21's −8.87 screen statistic counts mirrored seats
> separately, contrary to the campaign's own board-level rule." **Confidence: high.**

**Verification.** Quote verbatim at `timing-prize.md:173-175`, including *"None of the opponent's
edge is window selection."* The logic is inverted exactly as claimed: +3,288 is an **upper bound**
on what our schedule would pay them, and an upper bound above zero says nothing about whether the
true number is below zero — if it is, their windows *are* worth something. `timing-prize.md:63-66`
concedes *"the opponent's revenue change is ignored entirely"* in the primary ledger, and `:91-93`'s
"94 % selection" is 2,806/2,988, a wins/losses ratio, not a selection estimate. On the screen
statistic: `S/sell21/pair.py:16-20` divides by √rows over both seats, and `S/bank/paired.py:1-8`
states the resulting inflation is ~1.40×, so t −8.87 is honestly ≈ −6.3.

**Verdict: VALID** on the exclusion inference — §89's headline *"the exclusion framing of §85/§88 is
an accounting artefact"* is carried by a bound that cannot support it, and the same ledger was then
used *for* SELL21 (§89) and *against* the family (§90). **PARTLY** on the t: the inflation is real
and known, but §50 already sets the refusal bar at board-level |t| ≳ 2.5, which −6.3 still clears,
so the SELL21 refusal itself survives.

---

## Ranked experiments (reviewer's, re-ordered, with the cheapest falsifier for each)

Ranking criterion: information per GPU-hour against 11 days and two cards, with the flow211 slot as
the thing at stake. 1-4 are the reviewer's; 5 is ours, added because it is the only one that attacks
the campaign-level fact that 0 of 19 records has ever beaten B.

| # | experiment | cost | cheapest falsifier |
|---|---|---|---|
| **1** | **Objective ablation before flow211 gets days.** At B, on one perturbation draw, build four directions: NEXT weight in/out × top-ten kept/cut; repeat on a second draw. Judge both directions and B on the *same* held-out panel (NEXT14 + TOPB2). | ~0.4 GPU-h of rollout + 204 engine games | The new-objective direction fails to beat the old one on the common panel ⇒ decline the long run (without declaring the band family impossible). |
| **2** | **Repair the band comparison on existing checkpoints.** Run one pre-registered flow209 and one flow210 checkpoint on NEXT14, then keep those ids/seeds for flow211 instead of comparing flow209's NEXT30 column with flow211's NEXT14 column. | 56 engine games, 0 GPU-h | Checkpoint ordering reverses on the common panel ⇒ B-vs-hr band ordering does not extrapolate to the arms, and §96's licence for flow211 is void. |
| **3** | **The unrefuted sell-timing member.** Variant (c): keep a token lot at turn 18 (denial preserved), move only the marginal late WOOL/MILK units to turn 21. B vs split, paired, both purses priced. | 120 engine games (180 with full SELL21 as a third arm), 0 GPU-h | A reproducible negative paired margin for the split ⇒ the family closure is earned rather than assumed. |
| **4** | **Separate training-seed overfit from opponent transfer.** Replay B and `flow209_g10` on the 20 training tapes at their *actual* `pinned_seed_word` seeds, reporting raw margin and the training sigmoid. | 80 engine games, 0 GPU-h | An advantage confined to the training seeds ⇒ §101's "not memorisation" is overturned (diagnostic only; R3 forbids promoting on it). |
| **5** | **(ours) Step-size ladder on directions we already own.** §101 says the TOPB2 damage tracks step size and subspace, not rung mix; take the flow205/206/209 g10 directions and judge α·d at α ∈ {0.25, 0.5, 1} on TOPB2 + LIVEC-H30. | ~240 engine games, 0 GPU-h | Damage at α 0.25 is not ≈ 0.25× the damage at α 1 ⇒ the loss is curvature, not step length, and the lr/subspace recipe (not the objective) is what must change. |

Reading of the set: **1 and 2 are strictly cheaper than the arm they gate and both are prerequisites
for reading flow211 at all.** Under 11 days, spending ~half a GPU-hour plus 260 engine games to
decide whether the 38 % re-point is worth a multi-day arm dominates launching the arm and finding
out at g100.

## What the chain got right (the reviewer's calibration section, verbatim)

> SELL5's byte-identical OFF controls and paired engine evaluation support refusing immediate
> promotion of that implementation. The allocation audit correctly distinguishes episode count from
> objective weight. Section 102 genuinely addresses probe size, seed alignment, and direct NEXT30
> judging contamination. Those are useful controls; they do not validate the broader closures or
> establish flow211's opportunity cost.

Two of our own additions to that list, both checked: §94's mechanism is exactly right
(`es/train.py:4547-4551` is the "every rung pinned ⇒ residual is self-play" branch, so `arch_frac`
is never read), and the §100/§102 fix set is real (the abs probe *is* one unsplit
`max(chunk, total)` call at `es/train.py:5510`).

## Findings of our own the reviewer did not raise

1. **SELL5 is not "level" — it is positive and negligible.** The three paired legs are +35 (SE 28),
   +44 (SE 20), +52 (SE 38) (`sell5-falsifier.md:146-148`); inverse-variance pooled that is
   **+42.7 coins, SE 15.0, t 2.85**. The right sentence is "reproducibly positive at ~0.03 % of a
   game", not "LEVEL"; nothing about the decision changes, but the family was closed with the wrong
   word.
2. **The design drift in flow211** (20 % → 38.2 % band weight, §92 → §98) was never re-argued.
3. **flow211's hypothesis is unpromotable by construction** (`watch.sh:39` vs `:319`).
