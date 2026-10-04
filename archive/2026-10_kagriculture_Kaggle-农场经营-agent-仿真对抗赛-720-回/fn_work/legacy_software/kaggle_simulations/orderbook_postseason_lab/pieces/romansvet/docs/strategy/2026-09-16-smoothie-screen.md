# SMOOTHIE (census direction #3 / E-B): the pre-GPU sim screen

Agent run 2026-09-15 22:48Z–23:48Z. Falsifier asked for by
`docs/strategy/2026-09-14-open-lever-census.md:205-211`: before any GPU, screen a hand-set
theta whose `press3` / `grow_mult3` move OPPOSITE to B's measured smoothie response. GO only
if a variant shows ≥ +400 coins on SMOOTHIE_SHOP boards without losing ≥ that elsewhere.

Reference theta B = `flow193_g100_hr` = `submission/theta.npy` (6,789 floats, identical
decode to `S/judge7065/flow193_g100_hr_pad7020.npy`).

## 1. What "move press3 / grow_mult3" can even mean

**There is no per-product theta coordinate.** `press = h @ w3 + b3` with `b3` a *scalar*
(`src/kagg3/core/policy.py:319` `("w3", (N_ENC_HID, 1)), ("b3", (1,))`), and
`grow = (h @ w2 + b2)[:,0]` shares `w2`/`b2` across all nine products
(`policy.py:700-716`, `forward`). Products differ only through the per-product row of `h`.
Decode (`src/kagg3/core/brain.py:1161-1162`):

```
press     = floor(_BASE * relu(tanh(out.gate)))            # gate = (h @ w3 + b3)[:,0]
grow_mult = floor(min(softplus(grow)/softplus(0), GROW_MAX) * GROW_ONE)
```

So "move `press3` and `grow_mult3`" is a **direction in theta space**, not a coordinate edit.
The directions here were taken by autodiff of those two decoded quantities on real
observations (`tests/data/trajectory_obs.npz`, 40 seeds x 30 days x 2 seats = 2,400
`PolicyObs`, the same file `S/smoothie/probe_decode.py` uses), then solved for the
**minimum-norm** theta step that hits a target change in the d15-29 window means and leaves
the other eight products' means where they are (Jacobian J of the 18 window-mean raw outputs,
step `J^T (J J^T + lam I)^-1 target`, relinearised 3x). Tools: `S/smoothie/mkthetas2.py`
(Jacobian solve), `S/smoothie/mkthetas3.py` (contrast basis + dose line search),
`S/smoothie/mkfinal.py` (writes the four thetas + `S/smoothie/decode.txt`).

**B's response reproduced on the obs file** (d>=15, split by `shops[SMOOTHIE]>0`; SMOOTHIE is
shop index 6 of the sorted `spec.SHOP_NAMES`, `src/kagg3/spec.py:172-174`):
B holds strawberry harder and presses it less exactly as
`docs/strategy/2026-09-12-band-winloss-ledger.md:186-205` measured in play —
`press3` 12.37 (non-smoothie) -> **2.51** (smoothie), `grow_mult3` 944.6 -> **1006.1**.

## 2. Decode table (`S/smoothie/decode.txt`)

Means over the d15-29 window observations; `press_oth`/`gm_oth` are the other eight products
(the collateral the min-norm step is trying not to move). Every variant's decoded integers
differ from B's by 5-84 units, i.e. the gene-slope rule is satisfied by construction.

| theta | split | press3 | grow_mult3 | press_oth | gm_oth | \|dtheta\| |
|---|---|---:|---:|---:|---:|---:|
| B | win-smoo | 2.51 | 1006.1 | 47.78 | 494.5 | 0.0000 |
| B | win-nonsm | 12.37 | 944.6 | 46.84 | 493.5 | 0.0000 |
| B | all | 8.31 | 763.9 | 32.83 | 378.1 | 0.0000 |
| sm_opp1 | win-smoo | 22.79 | 991.3 | 48.13 | 494.5 | 0.3445 |
| sm_opp1 | win-nonsm | 43.57 | 921.8 | 46.83 | 493.8 | 0.3445 |
| sm_opp1 | all | 42.11 | 769.3 | 37.70 | 375.8 | 0.3445 |
| sm_opp2 | win-smoo | 43.88 | 975.2 | 50.13 | 494.7 | 0.5741 |
| sm_opp2 | win-nonsm | 65.46 | 905.2 | 48.42 | 494.4 | 0.5741 |
| sm_opp2 | all | 66.07 | 771.0 | 42.83 | 375.3 | 0.5741 |
| sm_cond | win-smoo | 15.78 | 921.7 | 49.63 | 494.6 | 0.5240 |
| sm_cond | win-nonsm | 7.64 | 953.5 | 48.58 | 494.0 | 0.5240 |
| sm_cond | all | 6.34 | 752.8 | 30.26 | 393.8 | 0.5240 |
| sm_with | win-smoo | 0.05 | 1016.0 | 49.09 | 495.5 | 0.3445 |
| sm_with | win-nonsm | 5.08 | 965.1 | 48.50 | 494.2 | 0.3445 |
| sm_with | all | 1.14 | 759.8 | 31.55 | 382.8 | 0.3445 |

Doses (vs B, window means): `sm_opp1` press3 **+20.3 / grow_mult3 −14.8** on smoothie obs;
`sm_opp2` **+41.4 / −30.9**; `sm_cond` **+13.3 / −84.4** on smoothie obs against
**−4.7 / +8.9** on non-smoothie obs (a genuinely shop-conditional flip, and the full dose the
census asked for on both coordinates); `sm_with` **−2.5 / +9.9** (control, B's own direction).
`grow_mult3` is stiff at B on the global step (`unit_ratio ≈ 1.0`, so 1 GROW_ONE unit of decode
is ~1.4e-3 of raw logit but every coordinate that reaches it also reaches the other products);
the contrast solve (`sm_cond`) is the one that lands the asked-for −50 and more.

## 3. Sim screen (`S/smoothie/screen.py` = `S/simscreen/screen.py` verbatim)

120 boards = the frozen LIVE-C hold-out list `S/simscreen/boards.json` (60 pinned-town tapes
x 1 seed x 2 seats), shipped `hr` switches, `shop_crn` on, 600 episodes, 498 s wall.
Split by SMOOTHIE_SHOP in the tape's pinned town (`artifacts/tape_actions_town/<id>.npz`
`town` array contains shop index 6): **74 smoothie / 46 non-smoothie boards**.
`dcoins` = paired Δ of our own d29 money, `dmargin` = paired Δ of (ours − theirs).

| theta | split | n | win% | margin | dcoins | **dmargin** | sd | t |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| B (ref) | smoothie | 74 | 64.9 | +3,793 | 0 | 0 | | |
| B (ref) | non-smoo | 46 | 82.6 | +7,669 | 0 | 0 | | |
| sm_opp1 | smoothie | 74 | 13.5 | −12,894 | −5,484 | **−16,687** | 5,955 | −24.10 |
| sm_opp1 | non-smoo | 46 | 32.6 | −5,634 | −4,611 | **−13,303** | 4,154 | −21.72 |
| sm_opp2 | smoothie | 74 | 6.8 | −14,634 | −6,899 | **−18,427** | 6,649 | −23.84 |
| sm_opp2 | non-smoo | 46 | 21.7 | −6,022 | −5,775 | **−13,691** | 4,905 | −18.93 |
| sm_cond | smoothie | 74 | 58.1 | +2,852 | −2,335 | **−942** | 3,960 | −2.05 |
| sm_cond | non-smoo | 46 | 69.6 | +5,761 | −1,917 | **−1,908** | 2,608 | −4.96 |
| sm_with | smoothie | 74 | 73.0 | +3,378 | +606 | **−415** | 3,456 | −1.03 |
| sm_with | non-smoo | 46 | 69.6 | +5,729 | −300 | **−1,941** | 2,842 | −4.63 |

Pooled rows: sm_opp1 −15,390 (t −30.3), sm_opp2 −16,611 (−28.2), sm_cond −1,312 (−4.08),
sm_with −1,000 (−3.31). Raw log `S/smoothie/screen_run.log`, per-board csv
`S/smoothie/smoothie_screen.csv`, split `S/smoothie/split.txt`.

**Instrument check.** The screen reproduces the covariate the whole direction rests on: B is
+3,793 / 64.9 % on smoothie boards against +7,669 / 82.6 % without one (Δ −3,876), the same
sign and about half the size of the ledger's −8,339 / 80.0 %→41.7 %
(`2026-09-12-band-winloss-ledger.md:110-116`). So the boards that carry the alleged pool are
present in the screen, and the screen is a valid instrument for this question.

## 4. Verdict: **NO-GO** — the +475…+975 is cross-sectional selection

Bar (census §4 E-B): ≥ **+400** on smoothie boards without losing that much elsewhere.
Best smoothie-split result of any variant is **−415** (t −1.03), and that is the *control*
that moves WITH B's response; every theta that moves in the prescribed OPPOSITE direction is
worse on smoothie boards than on non-smoothie ones:

* The **dose-response runs the wrong way.** sm_opp1 → sm_opp2 doubles the opposite move and
  the smoothie-board margin goes −16,687 → −18,427. If the ledger's displacement story were
  causal, more of the opposite move should have recovered coins on exactly these boards.
* The **shop-conditional variant is the clean test** — it applies the opposite response only
  where the sink exists, at the full asked-for dose (press3 +13.3, grow_mult3 −84.4, with
  non-smoothie obs held at −4.7 / +8.9) and leaves the other eight products alone. It is
  **−942 on smoothie boards (t −2.05)** and −1,908 elsewhere. The lever the census wants an
  arm to *learn* was hand-set in the correct direction and it lost on its own stratum.
* The one positive number in the table is sm_with's **+606 own coins** on smoothie boards —
  and its *margin* there is −415: holding strawberry harder on a smoothie town does put coins
  in our purse, it just puts at least as many in the clone's (the shop drains the market either
  way). That is the two-purse rule biting the ledger's counterfactual exactly as
  `counterfactuals-overstate` predicts.

This is the outcome the census itself flagged as the live possibility ("cross-section =
selection; +700 is a ceiling on where to look, not a predicted gain",
`2026-09-10-consensus.md:960`). **No GPU arm.** `S/smoothie/launch_flowsm1.sh` was NOT
written — the falsifier fired. Direction #3 joins §124 (the hand guard) as measured-out: the
hand-coded guard was engine-refused and the response itself now screens negative on the
stratum it was aimed at, in both the unconditional and the shop-conditional form.

Residual caveats, stated so a future arm knows what was *not* shown: (i) these are hand steps
of ‖dθ‖ 0.34-0.57 from B along a Jacobian-minimum-norm direction, not a trained policy — ES
could in principle find a smoothie-conditional response that also pays for itself elsewhere,
but the falsifier's whole point was that the cross-sectional pool should have shown up as a
reachable gain here and it did not; (ii) `press` is a violently sensitive global lever
(press_oth +0.4 → −13k margin), which is itself an argument against the census's "never pin
`press`" note being worth a dedicated arm; (iii) sim, not engine (ρ 0.77; here the pooled
effects are −1k to −16k, far outside the screen's resolution, so an engine leg would not
change the sign).

## 5. Commands

```bash
export JAX_PLATFORMS=cpu
.venv/bin/python S/smoothie/mkthetas2.py     # Jacobian min-norm directions (writes sm_*.npy)
.venv/bin/python S/smoothie/mkthetas3.py     # contrast basis + dose line search
.venv/bin/python S/smoothie/mkfinal.py       # final 4 thetas + S/smoothie/decode.txt
.venv/bin/python S/smoothie/screen.py --ref submission/theta.npy \
  --thetas S/smoothie/sm_opp1.npy S/smoothie/sm_opp2.npy S/smoothie/sm_cond.npy \
           S/smoothie/sm_with.npy \
  --boards 120 --board-file /mnt/e/_work/kaggriculture3/S/simscreen/boards.json \
  --tag smoothie_screen                      # 600 episodes, 498 s, 4 CPU threads
.venv/bin/python S/smoothie/split.py S/smoothie/smoothie_screen.csv
```

`mkfinal.py` OVERWRITES `sm_opp1.npy` (mkthetas2 writes the k=1 direction there, mkfinal the
k=3 dose), so re-run `mkthetas2.py` before `mkfinal.py` or read the frozen k=1 directions
`S/smoothie/dir_glob.npy` / `dir_cond.npy` instead. The four screened thetas as played are
`S/smoothie/sm_{opp1,opp2,cond,with}.npy` (6,789 floats each).

