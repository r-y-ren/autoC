# LOSS12: the sim does NOT equal the engine — 2026-09-09

Resolves the `flow166_g50` discrepancy: the ENGINE loss12 leg reads **d-margin +722/game
(+4/−0 flips)**, the SIM (`S/g50anat`, `S/simprobe`'s LOSS12 column) reads **+6/game**.

Data only, no new sim run. Working files: `S/loss12val/{cmp.py,table.txt,fidelity.txt,stack.txt,fam.txt,caps.txt}`.

## Verdict

**The sim's LOSS12 column is NOT trustworthy.** Two independent defects, one small, one fatal.

### 1. Seed mapping — real, but small (2 of 12 tapes)

`S/loss12/run.sh` hands the engine only the twelve ids, so `--seed-per-opponent` draws
`777001 + 1000003*(i+1)` off the **index in that 12-item list** (0…11).
`S/simprobe/probe.py` and `S/g50anat/anat.py` derive the seed from `PANEL_IX` — the index in
`sorted(glob(panel_opp_town/opponent_tape_*/main.py))`, i.e. **161…172** of 177.
All twelve seeds differ (e.g. 107056463: engine 4,674,845 vs sim 1,894,255,280).
`S/lossflip/run.sh` passes the FULL panel, so `PANEL_IX` is correct for held42 / leg20 / family —
loss12 is the only set with its own list.

On a pinned town the seed only moves the end-of-day shop draw, so this is mostly harmless:
engine-vs-engine, loss12-list seeds vs panel seeds, same theta and tree,
**mean |d margin| 293, max 1,990, 2 of 12 tapes > 500** (107056463 +1,990, 107067869 −1,228).

### 2. Sim fidelity — fatal on 4 of 12 tapes

Same theta (`flow166_g50`), same worktree (`arms-next`), same knobs, **same seeds**
(engine full-panel `S/lossflip/flow166_g50.csv` vs `S/g50anat/anat.npz` rec, 2-seat mean):

| tape | eng margin | sim margin | d |
|---|---|---|---|
| 107056463 | −8,260 | −8,191 | −69 |
| 107067869 | −8,942 | −8,942 | 0 |
| 107068399 | +1,060 | +1,021 | +39 |
| 107070717 | −7,252 | −7,288 | +36 |
| **107072760** | **+3,098** | **+10,378** | **−7,280** |
| 107079367 | −15,237 | −15,237 | 0 |
| 107081922 | −9,631 | −9,638 | +7 |
| 107088554 | −6,452 | −6,394 | −58 |
| **107090008** | **−8,300** | **−1,556** | **−6,744** |
| **107089992** | **−3,532** | **+3,978** | **−7,510** |
| 107092814 | −2,438 | −2,396 | −42 |
| **107095149** | **−23,310** | **−16,755** | **−6,555** |

mean |d margin| **2,362**, max **7,510**, 4 tapes > 500, 8 tapes ≤ 100.
Pooled the sim is **+2,348/game optimistic** (engine −7,433, sim −5,085).

Signature on the four: the sim's OPPONENT purse is 2.8–5.9k **low** (107072760 +5,932,
107089992 +4,978, 107090008 +2,805) and/or our purse 1.3–5.9k **high** (107095149 +5,890) —
the tape seat under-plays in the sim and we take the pot it drops. It is **not** a level offset
that cancels in a delta: the same four tapes miss by different amounts under the base theta
(107089992 −5,597 ours / +1,917 theirs at base vs −2,531 / +4,978 at g50), which is exactly how
a +722 engine delta becomes a +6 sim delta.

Control: on the 10 family tapes, same comparison, **mean |d margin| 17, max 173, 0 tapes > 500** —
9 of 10 coin-exact. The sim is faithful there and broken only on the loss12 cut.

Not the cause: **stack composition** (61-tape `simprobe` base vs 22-tape `anat` stack, identical
tree/theta/seed → **0 coins** on all 44 boards, bit-identical); **the 2 non-byte-exact tapes**
(107088554 is one of the 4 best matches at 58 coins; 107095149 is bad, but so are three tapes
verified byte-exact); **the gene-padded init theta / worktree** (`flow135_g350` 4,980 vs
`flow135_g350_gpfwdfv_gb028` 6,789 agree to ≤ 60 coins on the 8 clean tapes); **tape provenance**
(each `tape_actions_town/<id>.npz` was cut within seconds of its `panel_opp_town` package).
Also noted: `probe.py` writes the TAPE's seat in the `seat` column while the engine writes ours,
so seat-dependent rows come out label-swapped (107056463, 107067869) — cosmetic, but it makes
per-row diffs look like disagreements when the pair is identical.

## Fix

1. **Do not read LOSS12 out of `S/simprobe` or `S/g50anat` until 107072760, 107089992,
   107090008 and 107095149 are re-cut or dropped.** Delete the LOSS12 column from
   `docs/strategy/2026-09-09-simprobe.md`'s template, or restrict it to the 8 clean ids
   (mean |d margin| 31, max 69) where it is worth reading.
2. **Seed mapping**: give `probe.py` / `anat.py` a per-SET index. `PANEL_IX` is right for
   held42 / leg20 / family (full-panel engine list) and wrong for loss12, whose index must be
   its position in `S/loss12/ids.txt`. Until then loss12 sim rows pair with nothing.
3. **Root cause of the 4-tape gap is still open** — the recorded action arrays are
   `mop (30,24,10)` / `uop (30,17,24)`; the 10-row market cap saturates on every tape including
   the clean ones, so the truncation hypothesis is unproven. Re-cut the four tapes and re-diff.
4. The **engine** loss12 leg (+722, +4/−0) stands: 10 of its 12 tapes reproduce Kaggle to the
   coin, and it is the judge. The sim's +6 is an artifact.
