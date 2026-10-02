# Independent verification — planner finding 1, "land price is missing from its utility comparison"

Scope: one claim from `docs/2026-09-10-planner-findings.md` (row 1) and
`docs/reviews/planner-2026-09-10/REVIEW.md` §2. Read-only on every worktree `src/`;
probes ran in memory against `.claude/worktrees/ship-pair` (the reviewed tree). 2026-09-10.

**Verdict: PARTLY CONFIRMED — literally true of the code, fully compensated by the trained gene,
and the practical implication is already refuted by three paired arms.**

## 1. Source: where land is decided, and what the comparison contains

| Site | File:line | What it is |
|---|---|---|
| Gene decode | `.claude/worktrees/ship-pair/src/kagg3/core/brain.py:896-898` | `land_frac = _qfloor(tanh(head[1] + aux[1]*afford) * 256)`; `land_bias = (land_price * land_frac) // 256` |
| Clip | `brain.py:640` `LAND_BIAS_STEPS = 256`; `tanh` tail ⇒ `land_frac ∈ [-256, 255]` | so `land_bias ∈ [-land_price, +land_price·255/256]` |
| Brain-side predicate | `brain.py:913` `land_ok = (land_bias > -land_price) & (nquad < 4) & (money >= land_cost)` | tile-count prediction only; not the purchase |
| Value | `plan.py:5374-5376` `land_value = BUD.marginal_gain(..., money - land_gap, BUD.LAND_LISTS)` | |
| **The purchase** | **`plan.py:5384-5386`** `buy_land = (nquad<4) & (~terminal) & (money>=land_gap) & (money>=land_cost//LAND_OWN_DEN) & (land_value + macro.land_bias > 0)` | |
| What `marginal_gain` returns | `budget.py:94-143`, accumulator `gain + (v_next - c_next)` | net coins of the *seed/animal* candidates the 25 new tiles admit — a profit, but only over seed/animal cost |

**The land price is genuinely absent from the value comparison.** `land_gap` is subtracted from the
*purse* passed to `marginal_gain` (line 5375); that constrains which candidates are affordable, it
does not subtract 1,000 coins from the returned gain. The in-source rebuttal at `plan.py:5377-5379`
("the comparison is to zero and not to `land_cost` — charging the price twice is the old bug in
reverse") is **wrong on its own terms** for the quantity `marginal_gain` returns. The review's
structural reading is correct.

**But the price-scaled gene is a deliberate compensator, documented at the site.** `plan.py:5347-5350`:
"`land_bias` is scaled to `land_cost` precisely so a gene that has learned 'land displaces too much
early' can demand up to a full quadrant price of margin before the purchase clears." And
`brain.py:884-891`: "saturated negative it demands a full price of margin." At `land_frac = -256`,
`land_bias = -land_price` exactly, and the gate `land_value + land_bias > 0` **is algebraically
`land_value > land_price`** — i.e. exactly the fix the finding proposes. The defect is real only for
an untrained (zero-bias) policy.

`ship-pair` vs the currently shipped `ship-pair-hr`: `brain.py` and `budget.py` are md5-identical;
`plan.py` differs (hire-row switch) but lines 5320-5400 — the whole land block — are **byte-identical**.
The finding applies unchanged to the live file.

## 2. Reproduction (ship-pair tree, in memory, `_board(day=27)` + `_wheat(26)`)

Probe reproduced **exactly**: `land_cost 1000, land_gap 1000, land_value 34, money 9981`,
`buy_land = 1` at `land_bias = 0`, `n_free` 25 → 50. The review's "1,000 coins for 34 coins of
modeled profit" is confirmed to the coin.

Bias sweep on that same state (this is the new measurement):

| `land_bias` | −1001 | −1000 | −999 | −500 | **−34** | **−33** | 0 | +500 |
|---|---|---|---|---|---|---|---|---|
| `buy_land` | 0 | 0 | 0 | 0 | **0** | **1** | 1 | 1 |

The flip is at `land_bias > -land_value`, i.e. anything at or below −34 already refuses this
quadrant. The proposed fix (charge the full 1,000) is 29× stricter than needed to flip this probe.

**Trained decode on that state** (`brain.decide`, opponent mirrored — see assumptions):

| theta | d27 q1 | d6 q1 | d0 q1 (3k) | d10 q2 | d15 q3 |
|---|---|---|---|---|---|
| `flow172_g940` | **−1000 (−256/256)** | −997 | −969 | **−2000 (−256)** | **−4000 (−256)** |
| `flow172_g1000` | **−1000 (−256/256)** | −985 | −942 | **−2000** | **−4000** |
| `flow135_g350` | −961 (−246) | −618 | −950 | −1930 | −4000 |

On the review's own probe state the shipped theta decodes to **exactly −land_price**. The trained
decision on that state is therefore `34 > 1000` → **does not buy**. The zero-bias probe measures the
initialisation, not the shipped agent.

This also explains the review's scope line without any new measurement: "none of the eight land
purchases in the four instrumented games had `land_value < land_cost`" is not an independent
observation — with `land_bias = -land_price` it is an **algebraic identity** of the gate. 8/8 had to pass.

## 3. Scope: is the proposed fix already covered by paired reads?

Yes, on the loosening side; the archive is unambiguous.

- `docs/strategy/2026-09-10-planner-wall-audit.md:20,32-41` — `land_bias` decodes to exactly
  −`land_price` on **27 of 30 days in all 7 lineage thetas**; ES slope on land 6.9 % of decisions,
  zero after d10; quad 4 never bought; byte-identical from `flow135_g350` to `g1000` (~900 gens).
  Wall audit B (`-B.md`) independently: "exactly −land_price on 30-71 % of days; zero-gradient
  half-space." Consensus `2026-09-10-consensus.md:56` records agreement, and line 66 records the
  outcome: "the wall audit's items are walls of the optimum, not planner defects."
- `S/glut/verdicts.log`, three paired arms, all **DEAD**:
  - `LAND_BIAS_ZERO_ON` (force bias 0 — literally the "buggy" comparison): TOPB −16,640 t −9.4
    (12 drops); LIVE55 34.5 → **15.5 %**, −8,148 t −9.3.
  - `LAND_BIAS_FLOOR 0.1` (demand only 10 % of price): TOPB −16.7k (12 drops); LIVE55 34.5 → **17.3 %**,
    −8,056 t −9.2.
  - `ZERO + LAND_VETO_MIN_DAY=2` (lift the veto only after d1): TOPB **−6,217** t −6.8 (12 drops).
  Verdict recorded 10:29Z: "LAND FAMILY CLOSED FOR GOOD; the wall-audit land item is a false positive
  as a lever (the gene is at the optimum's edge)."

So: **every arm that moves the gate toward "no price charge" loses heavily and paired.** The finding's
implication ("subtract the full land cost and recalibrate the bias") points the *opposite* way from
those arms, and there the archive is silent. Two residuals remain genuinely untested:

1. **A stricter gate.** Implemented naively as `land_value - land_cost + land_bias > 0` with the
   trained bias unchanged, this is a *double* charge (`land_value > 2·land_price`) and would refuse
   the quad-2 d5 / quad-3 d10 purchases the shipped file still makes. Never measured paired. Prior is
   poor but not zero: the unpaired diagnostic in the wall audit went the other way (`bias:=0` →
   121k → 159k own coins on one board), and all three paired loosening arms lost, which is weak
   evidence that *less* land is not free either.
2. **Reparameterisation, not relocation.** Charging the price explicitly *and* re-centring the gene
   so the decision boundary is unchanged is a **no-op at inference by construction** — its only value
   is that it moves the trained optimum off the ±256 clip and restores a two-sided ES gradient. The
   build for this exists and was never judged: `LAND_FRAC_SOFT_ON`
   (`.claude/worktrees/land-veto/src/kagg3/core/brain.py:902-904`, `plan.py:232-240`), explicitly
   marked "For a *training* arm only". It is the one surviving form of finding 1 — and it is a
   training-arm question, not an inference lever.

## 4. Verdict and the test I would run

**PARTLY.** Literally true as written about the code path (the price is absent from
`land_value + land_bias > 0`, and the source comment defending it is incorrect). **True-but-compensated**
in the shipped agent: the gene is scaled to `land_price` by design and decodes to exactly
−`land_price`, so the trained comparison already *is* the proposed break-even. The finding's evidence
(zero bias) describes the initialisation; its scope sentence (8/8 purchases passed) is an identity,
not a corroboration.

**Would acting on it move paired win rate on S/livec (72 boards / 144 games)?** Very unlikely as an
inference change — the correct-and-recalibrated version is a no-op by construction, and the only
direction it can actually move the gate (stricter) is bounded by a gene already at its strict clip
while the three measured loosenings all lost double digits of win rate.

Paired test if run anyway (order: cheap tier first, stop on the first negative):
```
S/topb2/run.sh landcharge .claude/worktrees/land-veto \
  artifacts/kagg2_games/thetas/flow172_g1000_pad6954.npy "OPEN_PUMP_ON=True,HIRE_ROW_ON=True,<charge switch>"
S/livec/run.sh  landcharge <same>      # 72 boards, both seats, --seed-per-opponent
S/live62/run.sh landcharge <same>      # 62 live boards, LIVE55 held-out rule line
```
Baselines are the `g940pair` / `g1000pair_hr` CSVs already in `S/lossflip/`; `S/bank/paired.py`
prints the ALL line. A price charge needs a *new* switch in the `land-veto` tree (the three existing
switches only loosen); that build is not justified by this verification.

## Dead ends recorded

- Reading `money - land_gap` in `marginal_gain` as "the price is already charged" — it is not; it is a
  budget constraint. The source comment at `plan.py:5377-5379` is the dead end, and the review is right.
- Treating "8/8 purchases passed break-even" as evidence about behaviour — it is forced by
  `land_bias = -land_price`.
- Expecting `LAND_FRAC_SOFT_ON` to be an inference lever: at 255/256 it *loosens* the gate by
  `land_price/256`, the same direction as the FLOOR 0.1 arm that lost −16.7k on TOPB.

## Assumptions

- The trained decode used a `PolicyObs` built to mirror the review's `_board(day=27)` fixture with an
  identical opponent board and purse; `head[1]`'s inputs include opponent features, so a different
  opponent state could move the d0/d6 non-saturated readings. It cannot move the d27/q2/q3 rows —
  those are at the clip, where the decode is constant.
- Engine time used: in-memory `build_day` probes only (~4 min). No paired legs were run; §3 relies on
  the archived paired reads rather than re-measuring them, per the standing archive rule.
