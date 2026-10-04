# MELONDETECT1 (2026-09-28, 09:02-10:40Z): a tile detector of the rival's d0 melon plate for the KERNEL2 gate

USER order: "melon detector instead of cash fingerprints - do it". Question: can the V56 kernel's fire decision read what the rival
DOES on day 0 (its melon plate) instead of the exact h1-cash whitelist 26|29|2338|2438 (v3, live vrp15_k2fire)?
**Verdict: NO SHIP. The plate cannot replace the cash gate with the current kernel.** Every tile-gated arm is below v3 (+22 band) or
fails GATE2; the only passing tile arm outside v3's own whitelist is a veto on v2 (+37) that is dominated by v2 itself (+43).
No package built (the condition "best arm PASSES with more band flips than v3" is not met by any grid arm).

## 1. What the observation shows (S/melondetect1/obs.md, obsprobe*.py on 58-83 live games)
- The rival's farm is public: `farms[q].tiles` (PLANT kind + crop + planted_day, animals), money, farmer, hands, hires_today,
  unlocked_quadrants. Its shed/seeds/orders are private; seed buys do not move the public market inventory.
- **Step 1: 0 melon tiles on every live seat.** h0 only buys and hires (hands hired at h0 are visible at step 1).
- Plates are planted d0 h5..h20: first step with >= 4 melon = MELON family median 13 (6..33), V family median 11. Complete at our d1
  dawn (step 24): **MELON 3-9 melon (27/29 at 6-7), V family 11-12 melon, ZERO 0.** The V family (our lineage + public V notebooks)
  plants the BIGGER plate, so plate size alone fires on V; the h1 cash pre-filter (<= 2,550) is what keeps V out.
- The faithful59 ENGINE tapes (v2's misfires) also show 5-7 melon at step 24; band "MELON" seats that V56 wins include 0-5-melon
  rivals (pico, ebi, tineshagent, snorlax, readyornothere): the plate does not mark where V56 wins or loses.
- **Handoff after step 1 was measured, not assumed:** the kernel's INHERIT rewrite exists only for step 1 (V56 is a per-step tape
  chassis). Handing it PFS's d0 farm at step 24 (fresh kernel state) collapses every fired seat to 2-33k coins (smoke 5/5, run A
  108/108 band fired seats, own coins -41k..-135k vs base; e.g. sidazuo 21,754 vs 133,231, unreal 22,765 vs 181,155). A d1 handoff would need a full-day inherit
  rewrite (tiles/hands/animals re-mapped onto the tape), not buildable here.

## 2. Detector (branch `melondetect1` from kernel2v3 63f74064; default OFF)
Switches in `core/plan.py`, logic in `agent/runtime.Runtime._kernel2` + `runtime.kernel2_rival_melon(obs)`:
- `KERNEL2_FIRE_MODE` = `cash` (default: the v3/v2 step-1 latch, byte-identical) | `melon` | `either` | `veto`
- `KERNEL2_MELON_MIN` (6), `KERNEL2_GATE_STEP` (24), `KERNEL2_MELON_CASH_MAX` (2550); `KERNEL2_ZERO_CASH` honoured in every mode.
- melon: h1 cash <= MELON_CASH_MAX and not ZERO_CASH -> wait (PFS plays); at the first turn with step >= GATE_STEP the kernel takes
  the farm iff the rival shows >= MELON_MIN melon tiles, else PFS for the game. either: a FIRE_CASH-listed h1 value fires at step 1
  (INHERIT, = v3), the rest go through melon. veto: step-1 fire on h1 <= MELON_CASH_MAX not ZERO_CASH (v2's rule, no whitelist),
  hand-back to PFS at GATE_STEP when the rival shows < MELON_MIN melon (ZERO_BACK mechanics).
- tests/test_melondetect1.py (9 tests: defaults, counter, melon/either/veto/cash latches, and an OFF decode of the live vrp15
  package vs the same package + this runtime/plan change on 3 live vrp15 games x 30 turns, byte-identical) + test_kernel2_fire.py:
  15 passed. Judge rows log `opp_mel_s24, opp_plants_s24, opp_first_mel4/6/8, opp_hands_s1, opp_mel_s1` (S/melondetect1/md_leg.py).

## 3. Grid (named up front, S/melondetect1/grid.md) and exact scoring
Gate step 24 (the first step the plate is complete on every MELON seat). One sim run A (melon, MIN 4, gate 24) on every cash-eligible
seat (band 120, faithful59 41, pool 8, tapes 1; dev/self/clone/held/fresh300 have 0 eligible seats -> byte-identical base) gives every
melon/either arm exactly: until step 24 the game is PFS's in every arm, so a fired seat's game does not depend on MIN; unfired seats
reproduced the base rows 100 % (e.g. highfrequencyf 103,709/86,194 = the band_MELON control); 6 seats replayed twice, identical.
Run B (veto MIN 6) on the 35 eligible seats with run-A plate < 6 (faithful 11, band 24). Selection: S/melondetect1/rescore_md.py ->
res/runs/<arm>/judge.md (ja_judge.py --final), res/summary.md.

| arm | band fired MELON/V/ZERO/OTHER | band W 155 -> | flips | band soft t | faithful59 flips | A (band dtheta z) | B pooled soft t | guard | gift (react dtheirs t) | JC1 breakage | GATE2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| m4 | 100/7/0/1 | 132 | +1/-24 = -23 | -6.15 | -10 | -54.0 | -7.58 | FAIL (pool, faithful, band) | +1.93 | no | FAIL |
| m6 | 89/7/0/1 | 135 | +1/-21 = -20 | -5.78 | -8 | -35.3 | -6.96 | FAIL (pool, faithful, band) | +1.93 | no | FAIL |
| m8 | 5/6/0/1 | 153 | +0/-2 = -2 | -2.35 | 0 | -2.02 | -2.96 | FAIL (pool, band) | +1.93 | no | FAIL |
| e4 | 101/7/0/1 | 162 | +23/-16 = +7 | +0.79 | -8 | +0.94 | -1.18 | FAIL (faithful) | +1.21 | no | FAIL |
| e6 | 94/7/0/1 | 165 | +23/-13 = +10 | +1.26 | -6 | +1.41 | -0.34 | FAIL (faithful) | +1.21 | no | FAIL |
| **e8** | 57/7/0/1 | 175 | +23/-3 = **+20** | +4.19 | -2 | +4.55 | +2.91 | OK | +1.21 | no | **PASS** (< v3) |
| v4 (extra) | 107/7/5/1 | 192 | +44/-7 = **+37** | +6.05 | -1 | +6.01 | +5.04 | OK | -1.54 | TRIGGERED (A holds) | **PASS** (< v2) |
| v6 (extra) | 107/7/5/1 | 184 | +39/-10 = +29 | +4.75 | -4 | +4.64 | +3.45 | FAIL (faithful) | -1.54 | TRIGGERED | FAIL |
| ref v3 (live) | whitelist | 177 | +22 | | -2 | | | OK | | | PASS |
| ref v2 (vrp14) | h1 <= 2550 - ZERO | 198 | +43 | +6.92 | -1 | +6.70 | +5.79 | OK | -1.54 | TRIGGERED (A holds) | PASS |

Best 2 grid arms by band flips = e8, e6 (9-leg rows in res/runs/e8|e6/judge.md): e8 pool -4 (the 8 reacting 12-melon pool seats fire
late and collapse; v3 0), faithful59 -2, all other legs byte-identical; e6 faithful59 -6 (ENGINE tapes carry 5-7 melon). fresh300
fired 0/300 for every arm (no fresh rival shows h1 <= 2,550). Live fire share proxy (83 live games, our obs): m4/m6/e4/e6/v4/v6 39.8 %
(v2 41.0 %), m8 7.2 %, e8 21.7 %, v3 18.1 %.

## 4. Why it fails and the robustness argument
- A fire trigger must act at step 1 (INHERIT); the plate appears at step 5..24; a later handoff collapses the kernel (run A: every late
  fire -41k..-135k own coins). So "melon" and the melon part of "either" can only lose; e8 is v3 minus the losses of its 57-18 late
  fires, not a new signal.
- As a veto the plate is a real, fingerprint-free structural tell, but the veto has nothing to act with: handing V56's d0 farm back to
  PFS loses 20 of the 23 band veto seats run (15 of them v2 wins; v4 -6 flips vs v2, v6 -14), as ZEROGATE1 found on ZERO. The low-plate rivals are exactly
  where V56 (step-1 fire) wins.
- So the fingerprint's weakness (exact values move on a resubmission) cannot be fixed by tiles with the current kernel. The robust
  alternatives are the wide cash rule itself (v2/v4g families: h1 <= 2,550 minus exclusions, which a resubmission only moves within
  the band) or a kernel that can inherit at d1 dawn.

## 5. Next (not done)
- A d1-dawn INHERIT for V56 (re-map its d1 tape onto PFS's farm) is the only way a tile tell can gate the kernel; size: days, and it
  would have to beat the collapse measured here by ~90k coins/seat.
- The plate SIZE separates V (11-12) from MELON (3-9) at d1 dawn; combined with a working late handoff it would remove the cash
  pre-filter too.

## Commands
```
bash S/melondetect1/run_smoke.sh; bash S/melondetect1/run_a.sh; bash S/melondetect1/run_b.sh     # sims (2 workers, nice 10)
.venv/bin/python S/melondetect1/rescore_md.py                                                   # all 8 arms, 9 legs, GATE2
KAGG3_SRC=/mnt/e/_work/kagg3_wt_melondetect1/src .venv/bin/python -m pytest tests/test_melondetect1.py tests/test_kernel2_fire.py
python3 S/melondetect1/obsprobe.py 200; python3 S/melondetect1/obsprobe2.py                     # obs facts
```
