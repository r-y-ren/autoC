# BANDREJUDGE1 (2026-09-27 19:18Z-21:45Z): rejected near-miss arms re-judged on the 142-seat BAND leg over PFS -> NONE passes GATE2

**Verdict: NO SHIP CANDIDATE.** None of the 7 arms passes GATE2 (branch A or B) on BAND142, so no BAND-HOLD run was triggered. The MELON cell moves by at most +1 flip, and that flip is always the same near-tie board (hamedvakili, −702 → +261/+981). The only arm that adds MELON coins is NONV4-a2 (MELON Δours +2,668, t 2.6), and it loses 2 flips net and pays the rival +1,533.

| arm | cell | seats run | flips MELON / V / ZERO / OTHER (net) | Δours (t) | Δtheirs (t) | MELON Δtheirs (t) | GATE2 A: BAND soft Δθ (SE) z | GATE2 B: pooled soft t (legs) | hard Δθ (SE) | HOLD | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| a NONV4-a2 (d2 gate, +2 sheep d2-5) | a | 51 MELON = full cell (gated) | −2 / 0 / 0 / 0 (+1/−3 = **−2**) | +958 (2.53) | +550 (1.65) | +1,533 (1.67) | +2.0 (8.1) z 0.25 | +0.82 (band+pool+tapes, mixed base) | −11 (10) | not run | **gift / no move**: FAIL (A, B, gift on pool leg) |
| b MELONCOUNTER2-Cf (carrot far) | b | 36/51 MELON, **killed** | +1 (+2/−1) | −353 (−0.55) | +1,730 (**2.16**) | +1,730 (2.16) | −11.0 (7.1) z −1.55 | −1.53 (band only) | +8 (14) | not run | **gift**: KILL rule (MELON Δtheirs t ≥ 2) |
| c CARE_FED_ON | c | 44/51 MELON (partial, time box) | −1 / – / – / – (+0/−1) | −370 (−1.65) | −285 (−3.50) | −285 (−3.50) | −0.1 (1.6) z −0.04 | −0.04 (band only) | −7 (6) | not run | **own-purse loss / no move**: FAIL |
| d NONV_WOOL_CARE | d | 0 (budget) | – | – | – | – | – | – | – | – | **not run** |
| e MELONVETO_POST_ON (K 60) | e | 51 MELON (partial) | +1 / – / – / – (+1/−0) | +32 (0.36) | +5 (0.09) | +5 (0.09) | +0.3 (1.2) z 0.22 | +0.21 (band only) | +6 (6) | not run | **no move**: FAIL (flip = hamedvakili near-tie) |
| f VRPREPAIR1 (100,4) = `route_vrp.REPAIR_LAST_DAY` 20→29 | f | **142 = full** | +1 / 0 / 0 / 0 (+1/−0 = **+1**) | +39 (0.86) | +23 (1.22) | −1 (−0.02) | **−0.03** (1.2) z −0.03 | +7.45 (band + VRPREPAIR1 dev/held/FRESH/tapes, mixed base) | +6 (5) | not run | **no move**: FAIL (B: BAND soft Δθ < 0 by 0.03) |
| g ESSHIP1-h (= PFS + CARE_RIDE + SLIVER, g30 theta) | = BANDSTACK1-c | 142 (not rerun) | 0 / −2 / +1 / 0 (+2/−3 = −1) | −261 (−2.52) | −195 (−2.94) | – | +1 (3) | +0.15 (band only) | −4 (8) | not run | **own-purse loss**: FAIL (BANDSTACK1) |

## Method
- **Bed:** S/bandleg1 142 tape seats on the orig seat, real engine, with the ml1leg harness: SAFETY_S 1e9, REPAIR_MS 1e7, actTimeout 600, head_940, theta7659. Runner `S/bandrejudge1/leg.py` is S/bandleg1/leg.py plus `rv.NAME=val` switch items, which set `kagg3.agent.route_vrp` attributes after the init. Two workers under nice.
- **Base:** PFS = `S/bandleg1/res/pfv1.csv`.
  - **BASE tree:** a scratch copy of selfplay1 src 49e7f654 (plan.py dd26f0da = vrp12_pfs). `identb` replays 2/2 seats byte-identical to pfv1 (tape_highfrequencyf 103,709/86,194 and tape_team 151,182/135,790).
  - **PORT tree:** BASE plus OFF-default ports, committed on branch `bandrejudge1` (02a20f5b): `CARE_FED_ON` (careaudit1 3dc3fcf1), `NONV_WOOL_CARE` (nonv4), and `HERD_ADD_COW/SHEEP/DAYS` (HERDVRP1/NONV4) with a second latch `ENGINE_GATE2_*`. NONV4-a2 used the single ENGINE_GATE, which the shipped M20z latch now owns, so a2 rides the second latch and M20z stays intact. `identp`, with all ports OFF, is 2/2 identical to pfv1.
- **(a) is gated.** The latch fires on rival d2 MELON 1..10, and that is exactly the 51 MELON seats (pfv1 `opp_d2_melon`). The other 91 seats are base by construction.
  - The gate fires as intended: our d10 sheep go 3.33 → 3.98 per game.
- **(b) runs on its own tree.** MELON_COUNTER exists only on branch meloncounter1 4575e8d2 (vrp7-era). Its relay/ESWORK coupling is too deep to port in budget, so Cf ran on that tree paired against its own OFF base `../bandleg1/res/tfoff.csv`, the same as BANDLEG1's Tf (3').
  - `boff` replays 1/1 tfoff seats exactly.
- **(f) on the current base.** REPAIR is already ON with LD20 (vrp5), so VRPREPAIR1 (100,4) (every day, REPAIR_MS 100, EJECT_K 4) is `rv.REPAIR_LAST_DAY=29`.
  - Caveat: its V-leg pairs in S/gate2/pairs (VRPREPAIR1) measure repair vs no repair, which is about 2× the LD20→LD29 increment (VRPREPAIR3). Pooled soft t 7.45 therefore overstates branch B. B fails on the BAND sign regardless.
- **(g) is not rerun.** ESSHIP1-h is vrp8_jit + CARE_RIDE + SLIVER + g30. On today's base (vrp10_esw = vrp8_jit + g30, plus PFS) that config is exactly BANDSTACK1 cell c, so the GATE2 rescore row BANDSTACK1-c is its BAND verdict.
- **Order and kill rule.** Arms were queued a, b, e, c, d, f, running the MELON half first. At 20:25Z f was moved ahead of c/d: it is the GATE2 top re-judge candidate (V soft t 7.63), and c/d had the lowest MELON prior (CARE_RIDE superset; BANDSTACK1-b own-purse −3.3 t).
  - A cell was killed at MELON Δtheirs t ≥ 2. Ungated cells with only MELON seats are PARTIAL: unrun seats count as 0 change in Δθ.
- **Scoring:** `score.py` uses the GATE2 lib (`S/gate2/g2lib.py`, s 3,000).
  - A = BAND soft family Δθ z ≥ 1.96.
  - B = pooled soft t ≥ 2 over BAND plus the arm's existing V-leg pairs, and BAND soft Δθ ≥ 0.
  - It also applies the leg guard and the gift rule. Per-leg rows are in `score.txt`.

## Reading
- **NONV4-a2 is the only MELON-coin mover, and it gifts.** +2 sheep on d2-5 do reach the pasture (d10 +0.65 head). MELON Δours is +2,668 (t 2.6), but Δtheirs is +1,533 (t 1.7) and flips are +1/−3.
  - The one up flip is smackaveli (−18.3k → +57.2k), the known re-derive board.
  - The three downs are leaveyou (+817 → −1,549), smackaveli@113329149 (+146 → −1,702) and liminhai (+727 → −12,292).
  - This is the HERDVRP1/NONV4 herd gift again, now on the band.
- **Cf is the Tf mechanism, and it gifts on the band too.** MELON Δtheirs is +1,730 (t 2.16) after 36 seats, and the flips are 2 noise boards up and tineshagent (+10.4k) down.
- **CARE_FED_ON repeats CARE_RIDE's band profile** (BANDSTACK1-b) on 44 MELON seats: own purse −370 (t −1.65), rival −285 (t −3.5), 0 up / 1 down flip. It is denial that does not convert into wins.
- **MELONVETO_POST is inert on MELON rivals** (Δours +32, Δtheirs +5). Its one flip is hamedvakili.
- **VRPREPAIR LD29 is a ±40-coin effect on the band:**
  - 37/142 seats are byte-identical.
  - Family soft Δw/100 is MELON −0.11, V +0.16, ZERO +1.35.
  - The one flip is hamedvakili.
  - Its V-leg strength does not transfer to the band.
- **The MELON cell stays within −2..+1 of PFS's 14-37 under every arm, as in BANDSTACK1.** No parked switch reaches it; the gap is not a rejected-arm backlog.

## Commands
```
cd S/bandrejudge1
./run.sh identb; ./run.sh b; ./run.sh boff; ./run.sh identp      # replay checks + Cf (killed at 36)
./queue.sh     (boff, identp, then a e c d f MELON halves; stopped at 20:25Z after e) ; ./queue2.sh  (f MELON, f V,ZERO,OTHER, c MELON; c stopped at 21:33Z time box)
python3 score.py > score.txt     # -> res/score.tsv, pairs/<cell>__band.tsv
# HOLD (only if a cell passes): ./run.sh fhold ; python3 ../bandhold1/pair_hold.py res/fhold.csv
```
Trees: BASE = selfplay1 49e7f654 src copy; PORT = branch `bandrejudge1` 02a20f5b src (plan.py cde262ff, runtime.py 29f6a766); MC = /mnt/e/_work/kagg3_wt_meloncounter1/src.

## Files
S/bandrejudge1/: run.sh, queue.sh, queue2.sh, leg.py, score.py, score.txt, ident_labels.txt, checkpoint.txt, res/{identb,identp,boff,a,b,c,e,f}.csv + logs, res/score.tsv, pairs/*.tsv.
