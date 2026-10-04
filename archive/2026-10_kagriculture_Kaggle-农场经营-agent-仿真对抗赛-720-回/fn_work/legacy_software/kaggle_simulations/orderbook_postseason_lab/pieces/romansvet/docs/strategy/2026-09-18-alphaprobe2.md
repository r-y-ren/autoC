# ALPHAPROBE2 — the shop-CRN objection is VOID on our boards; the shop LOTTERY is the real wall

2026-09-18, branch `alphafarm`. `S/alphafarm/search_probe.py` (+ `report.py`), rows `run12nc_* / run12dt_* /
run12b_nc_*`. With [[alphaprobe]], [[mpcfeas]], [[planselect]], [[tape-fidelity]].

## 1. The objection, and why it is void
[[alphaprobe]] ran every rollout with `shop_crn=True` — the sim-only device that moves the 3-daily shop draw off the
weed cursor `2*used` onto a constant, so candidates that plant differently still unlock the same shops. The charge:
+2,912 was measured in a world the engine does not run. Added `--shop-crn 0/1` (default **0** = the engine program);
re-asserted the K=1 zero-jitter check on 2 boards under it — **PASS to the coin, both purses**. Re-ran the SAME 12
boards, everything else identical: **`run12nc` is byte-identical to `run12`** — every dawn row, every purse, paired
per-board difference exactly **0.0 on 12/12**. Cause, `sim/rollout.py:333-343` → `sim/eod.py:198-205`: `TAPE_DIR` is
`artifacts/tape_actions_town`, so `run_day` hands the tape's **recorded town** to `unlock_shop`, which replaces the
word draw outright. On a pinned-town board the shop schedule is a property of the BOARD, identical for every
candidate, before `--shop-crn` is consulted — the flag is dead code there. ALPHAPROBE's table stands unchanged:
pooled **+2,912, se 479, t 6.07, Δtheirs −245, oracle +2,766, 12/12 up, cand-0 0.725**.

## 2. The test that actually bites — `--drawn-town 1`
New flag: drop the recording, so the shop comes off the `2*used` cursor and the candidate's own tile count re-rolls
every later shop — the [[mpcfeas]] lottery, live, inside the selection.
| condition | Δmargin | se | t | Δours | Δtheirs | oracle | up | Σ in-sample dawn gain | transfer | corr(A,or) | sd(Δ) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pinned (`run12nc` = `run12`) | **+2,912** | 479 | **6.07** | +2,667 | −245 | +2,766 | 12/12 | +2,849 | **1.02** | **0.988** | 1,661 |
| drawn (`run12dt`) | +1,209 | 5,953 | **0.20** | −3,160 | −4,370 | **+22,658** | 6/12 | +15,365 | **0.08** | 0.046 | 20,622 |

Paired `dt − nc` −1,703 ± 5,971 (t −0.29), per-board swings ±20-33k = the [[shop-lottery]] ±25k noise, and the
[[planselect]] signature to the letter. Caveat, a real one: a drawn town also breaks the *opponent* (it replays
actions for shops that never unlock — why pinned-town boards exist, [[tape-fidelity]]), part of why both purses
fall. So `run12dt` does not price the search; it prices what a candidate-dependent shop draw does to a selection.

## 3. Fresh boards, still pinned — `run12b_nc`
Boards 7-12 of each class (`--board-skip 6`), engine-faithful, never run before: **+1,829, se 477, t 3.84, Δours
+1,608, Δtheirs −222, 11/12 up**, cand-0 0.767; engine tail +1,680 t 1.93 (theirs **+521**), BAND250 +1,979 t 4.08
(theirs −964). Oracle +2,483 vs held-out +1,829 = 1.36× hindsight, small against the drawn-town 19×; in-sample
+2,435 → 0.75 transfer. **All 24 boards: +2,371, se 349, t 6.79, Δours +2,138, Δtheirs −233, 23/24 up, oracle
+2,624** — the honest central estimate for the search is ≈ **+2,400/board**, not +2,900.

## 4. Verdict — GO, narrowed
* The `shop_crn` charge against [[alphaprobe]] is **VOID**, proven byte for byte, not argued: every number in that
  doc was already produced by the engine's own shop program on the judge's own board.
* **New and binding:** dawn-by-dawn selection is well-posed only while the shop schedule is *candidate-independent*.
  Pinning it is what makes +2,371 measurable; letting the candidate re-roll it destroys the signal (t 0.20) and
  fabricates an oracle (+22,658) — the law that killed [[mpcfeas]] and [[planselect]].
* Consequence: **online rollout search can never ride in the submission.** ALPHAFARM's only live path is offline
  distillation — labels harvested on pinned-town boards, a reactive policy shipped and judged by the ordinary §115b
  legs, which are pinned-town themselves. Tasks 3-4 (`soft_decide.py`, `ei_train.py`) are unchanged.
* Haircut on 24 boards: +2,371 → **+710…+1,420**, above the §115b +450 bar; the fresh engine six gift +521, so the
  "drop any label with `d_theirs > 0`" rule stays mandatory at distillation.
* Not done: the real-engine replay of chain A's macros — low value, the injection being a policy-side change under
  `brain.decide`, the seam [[essim]] certifies, and §2 answers its fidelity question.
