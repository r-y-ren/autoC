# SHIPSLIVER1 (2026-09-26 09:20Z–11:30Z): ship legs for SLIVER_ON (same/k2/wheat) vs the vrp7 config — NO SHIP (held100 fails)

Branch `shipsliver1` (worktree `/mnt/e/_work/kagg3_wt_shipsliver1`, from selfplay1 `aded4b9c`). Runs were local, with at most 3-4
worker processes (3 after the coordinator's 10:35Z note) at a local load of 25-58. They ran in `/root/stage_shipsliver1`, which is
`git archive aded4b9c` plus the gitignored LIVE250/tape data copied from the main checkout. Its `src` has route_vrp
`SAFETY_S 1e9` and `REPAIR_MS 1e7` in both arms, and `src_live` is the untouched tree used for the clock check. head_940 is
769ff15e and theta7659 is 94a8ffd2. `S/pool2/restore_tapes.sh` was not needed, because no bank agent that uses actions.json is
in these legs; the tape and faithful legs were not run.

**Arms.** Base is the vrp7 config: selfplay1 plan + `EMPTY_ROUTE_UNHIRE_ON` + M20z (`S/vloss1/vleg.py` BASE string). The arm is
base + `SLIVER_ON=True`, whose defaults are SLIVER_MODE same, K 2, CROP WHEAT, days 10-26.

## Determinism: base rows reused
The local harness reproduces the remote rows byte-exactly, so the base arm was not rerun.
- **V56 legs.** Base on dev 0-9, held 100-109 and FRESH 0-9 equals LABOUR1's `ua`/`uaL`/`uaF` rows (the vrp6 arm) on **30/30** games.
  M20z does not fire vs V56 (SHIPNV1). Those rows (`S/shipsliver1/base_labour1/`) are therefore the vrp7 base for dev100, held100
  and FRESH300.
- **VLOSSBED.** Local base 3/3 and sliver 3/3 equal VLOSS1's remote rows, so VLOSS1's `base.csv` (100 games) and `sliver.csv`
  (39 contested games) are reused, and only the 61 non-contested sliver games were run.

## Legs (sliver vs vrp7 base, paired)
| leg | n | W | flips | **net** | Δours (t) | Δtheirs (t) | Δmargin (t) | bar |
|---|---|---|---|---|---|---|---|---|
| VLOSSBED full (CHA22 + herd-safe × dev 0-24 × 2 seats) | 100 | 86 → 90 | +4/−0 | **+4** | +445 (5.84) | +74 (1.02) | +371 (4.72) | pass |
| dev100 (LIVE250 0-99, reacting V56) | 100 | 88 → 90 | +2/−0 | **+2** | +255 (3.77) | +74 (1.02) | +180 (1.80) | pass |
| **held100** (100-199) | 100 | 86 → 86 | +2/−2 | **0** | +263 (3.40) | **+119 (2.26)** | +144 (1.52) | **FAIL** (net < +1 and Δtheirs t ≥ 2) |
| dev+held 200 | 200 | 174 → 176 | +4/−2 | +2 | +259 (5.05) | +97 (2.16) | +162 (2.35) | |
| FRESH300, boards 0-49 only (= held 100-149, see note) | 50 | 43 → 42 | +1/−2 | −1 | +353 (3.23) | +292 (4.66) | +61 (0.45) | stopped |
| FRESH 50-299, band tapes dev50, faithful-59 | – | | | | | | | not run (held100 already fails) |

- **Flips.**
  - Bed: herd_saf@9 and @16, each on both seats. These are the same 2 boards as VLOSS1; the 61 non-contested games add no flip and no loss.
  - dev: 16 (as in SLIVER1) and 79.
  - held, up: 106 (−145 → +972) and 195 (−110 → +80).
  - held, down: 128 (+3,082 → −477) and 138 (+436 → −361).
- **FRESH300 overlaps held100.** `S/knobv56/screen_fresh.py` builds FRESH300 as live355 minus LIVE250 0-99 and 150-249, so its
  first 50 boards are LIVE250 100-149. The FRESH 0-49 chunk reproduces held 100-149 row for row. It is not independent evidence, and
  FRESH starts at −1 with Δtheirs t 4.66 on that slice.
- **Why held fails.** Held 100-149 alone shows Δtheirs +292 (t 4.66). The same-tile wheat fills add own wheat that V56 answers,
  the same reaction that closed ROUTEFILL1, RELAYFILL1 and TOMATOFILL1, only smaller. On dev the reaction is +74 (t 1.02). Over 200
  boards it is +97 (t 2.16).
- **Small-gains route.** It needs Δtheirs t < 2 on every leg, so held100 (t 2.26) fails it too.

## Clock (paired, live deadline; `timing.sh`, `tpair.py`)
dev 0-9 was run in both arms at the same time on `src_live` (SAFETY_S 0.75, REPAIR_MS 100), 300 paired dawns, at load 26-33.
- **Paired ratio, sliver/base:** median **1.044**, total-time ratio 1.054, p99 ratio 0.990.
- **Absolute, noted at load 26-33:** p50 0.189 vs 0.208 s and p99 0.683 vs 0.676 s. Max was 1.945 (base) vs 1.668 s, and dawns
  over 0.65 s were 13 vs 15. The base arm exceeds 0.75 s at this load as well.
- The absolute check at low load was not rerun, because the switch does not ship.

## LATE_ASK_FLOOR 0.8 crash (VLOSS1 NEEDS_FIX): found and fixed (harness-only), legs not run
`S/shipsliver1/askrepro.py` builds our in-process agent (NONV1 `_init` + vrp7 config + `LATE_ASK_FLOOR=0.8`) and calls it on the
step-0 obs.
- **Outside the engine's module swap it works**, which matches LABOUR1's clean sim measurement.
- **Inside `eval_vs_baselines._vendored_imports`** (which is how every reacting/NONV/VLOSS leg plays our seat), `plan._late_ask_floor`
  raises `ModuleNotFoundError: No module named 'kagg3'` on every turn. The cause is its call-time `from . import brain as _B`: the
  harness hides `kagg3` while the game runs, so the agent never acts, and the seat ends at 3,000 coins.
- **A packaged submission would not crash,** because `kagg3/core/brain.py` is in the tarball and importable.
- **Fix (`src/kagg3/core/plan.py`).**
  - `brain` is bound once at the bottom of the module (`from . import brain as _BRAIN`), which is safe with the brain→plan cycle in
    either import order.
  - `_late_ask_floor` and the `ENGINE_GATE_SET` `brain.` branch now use `_BRAIN`, which also removes a lazy import in the same class.
  - After the fix, step 0 under `_vendored_imports` acts (BUY_PRODUCT WHEAT 53 + 3 HIRE); without it, it raises.
- **Tests:** `tests/test_labour1.py` + `tests/test_engine_gate.py` give 11 passed and 1 failed. The failure is the pre-existing
  stale-mock `test_runtime_latch` (SHIPNV1: it also fails on vrp6).

## Verdict
**NO SHIP.**
- SLIVER_ON (same/k2/wheat) passes VLOSSBED at full 100 (+4, gift-free) and dev100 (+2, gift-free, Δours t 3.77).
- It fails held100: net 0 with Δtheirs t 2.26. That rules out both the flip bar and the gift-free small-gains route.
- The bed's +4 is 2 boards × 2 mirror seats.
- No vrp8 package was built. SLIVER_ON stays OFF.
- The same-tile sliver joins the fill family (ROUTEFILL1, RELAYFILL1, TOMATOFILL1, SLIVER1): own volume earns about +250 per game, and V56's reaction takes about a third to all of it.

Files: `S/shipsliver1/` (leg/queue/bed/timing lanes, pair.py, bedpair.py, tpair.py, askrepro.py, out/, bed/, base_labour1/, done.txt).
