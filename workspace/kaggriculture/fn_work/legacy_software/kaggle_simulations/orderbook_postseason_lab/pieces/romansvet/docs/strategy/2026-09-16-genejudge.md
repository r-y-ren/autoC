# GENEJUDGE — what the trained switch-gene block decodes, and what it is worth

**2026-09-16 · branch `genejudge` @ `c34afec` (the SHIPPED FT2 package) · box 19:40–20:30Z**
Candidates `S/genejudge/cands/{g00090,g00100}_record.npy`: the gen-90 / gen-100 records of the
remote ES arm `flow220_sw` (`--train-only sw,swb`, sigma 0.02, seat = the 44 fresh 09-16 clone tapes
of `S/v45leg2/ids.txt`). 7,395 floats = B **byte for byte** (`max|Δ| = 0.0` vs `B_sw0.npy` over all
7,065 head params) plus a trained 330-param `sw`/`swb` block; the two records differ by
`max|Δ| 0.0199` and decode the *same* flip pattern, so only `g00100` was judged.

## VERDICT
1. **NOT inert** — the block decodes 2.6 flips per decision on out-of-sample boards.
2. It is **2 static switch flips + a day window + one genuinely state-conditional flip**, and the
   static pair is a string the campaign has already priced as a loss.
3. §115b **REJECT** — POOLED180 **+188, t +1.23** (169 boards, se 152); in-band 48 −20; net flips 0.

## 1. DECODE (`S/genejudge/decode.py` → `S/genejudge/decode.csv`)
2,400 recorded real hour-0 observations (`tests/data/trajectory_obs.npz`, 40 seeds x 30 days x 2
seats = **80 games**), recorded long before the arm's tapes existed. `z = gh @ sw + swb`,
`flip = round(8 z) > 0`, so the threshold is **z ≥ 0.0625**; the zero block (`B_sw0`) decodes
`z == 0.0` on 2,400/2,400 — every switch at its module default, as `2026-09-16-geneswitch.md` §2 says.

| switch | shipped | g00100 z range | days flipped | games flipped | kind |
|---|---|---|---:|---:|---|
| `FEED_MANDATORY_ON` | True | −0.359 … +0.134 | 11.6 % | 100 % | **day window** (days 1-4) |
| `SURVIVAL_WATER_ON` | True | −0.427 … +0.162 | 36.2 % | 100 % | **day window** (days 0-11) |
| `FERT_VOLUME_ON` | False | **+0.154 … +0.438** | **100 %** | **100 %** | **STATIC ON** |
| `SHED_DEFICIT_ON` | False | **+0.133 … +0.518** | **100 %** | **100 %** | **STATIC ON** |
| `WHEAT_VOLUME_ON` | False | −0.374 … +0.154 | 15.1 % | 67.5 % | **state-conditional** |

The other five (`ANIMAL_DEFER_ON`, `CARE_HOLD_ON`, `CREW_PUSH_COST_ON`, `LATE_STRAW_CAP_ON`,
`ENDGAME_TOMATO_ON`) never flip: their `z` maxima are −0.007 … −0.053, all below the threshold.

`g00090` reproduces the table to within a point (8.3 / 35.0 / 100 / 100 / 13.9 %): same five
switches, same three kinds, same five never touched. Flip % by day, the three non-static ones:

    FEED_MANDATORY_ON    0 100 100  72  72   2   0 ... 0
    SURVIVAL_WATER_ON  100 100 100 100 100 100 100 100 100 100 28 60 0 ... 0
    WHEAT_VOLUME_ON      0 0 0 0 0 0 10 8 55 15 25 42 20 0 15 25 45 30 50 25 38 12 15 10 8 0 2 0 2 0

So of 2.6 flips a decision **two are a constant switch string**, two are a *calendar* (both survival
gates off for the opening) a `day <` constant expresses just as well, and only `WHEAT_VOLUME_ON` uses
the per-board freedom the layer was built for — the one thing `2026-09-16-switchvec.md` says a gene
can add over a static string.

## 2. WHAT THAT STRING IS WORTH BY PRIOR READ
`S/switchvec/factors.md` excluded all five, with reasons: `FERT_VOLUME_ON` and `WHEAT_VOLUME_ON` sit
in the **hard-reject** list (`|Δ| > 2,000`, the −10.5k group), `SHED_DEFICIT_ON` reads **−30 t −1.23**,
`FEED_MANDATORY_ON` / `SURVIVAL_WATER_ON` were "too large to flip (survival / structural)". The arm
walked to a vector whose static part is priced as a loss; its defence is the three conditional flips.

## 3. JUDGE — the candidate as a THETA arm on the shipped FT2 package
Identical tree, identical module defaults, identical switch string; **only the theta differs**
(`g00100_record.npy`, zero-padded 7,395 → 7,428 by `policy.unpack`) against
`artifacts/kagg2_games/thetas/flow193_g100_hr.npy`. The block IS live in the engine: **44 of 44**
ENG22 rows differ from the control. The baseline was not re-run — `git diff 9a9c435..c34afec -- src`
is **empty**, so this tree's `src` is byte-identical to the PUMPCLIP2 tree, whose `pc2_pair` rows are
byte-identical to the banked `ft2_*` (re-verified: `diff ft2_eng22.csv pc2_pair_eng22.csv` = 0 lines).
**No leakage:** `comm -12` of `S/v45leg2/ids.txt` against the `S/band180`, `S/livec`, `S/nextband`,
`S/eng22` and `S/v45leg` id lists is **0 on every one** — V45LEG is the same post-09-15 clone class as
the training tapes, not the same boards.

| leg | boards | rows | Δmargin | sd | se | t | flips W-L |
|---|---:|---:|---:|---:|---:|---:|---:|
| LIVEC-H30 | 30 | 60 | +387 | 1831 | 334 | +1.16 | 0-2 |
| LIVEC-H30B | 30 | 60 | −69 | 2471 | 451 | −0.15 | 0-0 |
| NEXT30 | 30 | 60 | +773 | 1294 | 236 | +3.27 | 2-0 |
| POOLED BAND (90) | 90 | 180 | +364 | 1936 | 204 | +1.78 | 2-2 |
| BAND180 | 79 | 158 | −12 | 2024 | 228 | −0.05 | 0-0 |
| **POOLED180** | **169** | **338** | **+188** | 1980 | **152** | **+1.23** | 2-2 |
| of which in-band 48 (opp ≥ 2300) | 48 | 96 | −20 | 2040 | 294 | −0.07 | 0-0 |

Informational, out of pool: **ENG22 −182** se 534 t −0.34 (2-0); **V45LEG +228** se 266 t +0.86 (0-0).

**§115b REJECT: +188 against a +450 / t 3.00 bar.** Net flips 0, the 2300+ in-band 48 is −20, the 79
fresh BAND180 boards are −12, and the single positive leg (NEXT30 +773 t +3.27) is one third of the
pool against two flat ones — the shape of noise, not of a lever. **One surprise:** a *wash*, not the
−10.5k the static `FERT_VOLUME_ON` read predicts. Either that read does not survive the FT2 package
or the conditional flips pay for it; +188 t 1.23 cannot separate them, and neither changes the verdict.

## 4. REPRODUCE
    git -C /mnt/e/_work/kaggriculture3-genejudge rev-parse --short HEAD    # c34afec, clean
    .venv/bin/python S/genejudge/decode.py                                 # §1, writes decode.csv
    WORKERS=2 bash S/genejudge/run_all.sh eng22 gj_g100 S/genejudge/cands/g00100_record.npy
    WORKERS=2 bash S/genejudge/run_all.sh pool  gj_g100 S/genejudge/cands/g00100_record.npy
    WORKERS=2 bash S/genejudge/run_all.sh v45   gj_g100 S/genejudge/cands/g00100_record.npy
    .venv/bin/python S/pumpclip/incr.py        gj_g100 pc2_pair     # POOLED180 + in-band 48
    .venv/bin/python S/pumpclip2/cheap_incr.py gj_g100 pc2_pair     # ENG22 + V45LEG

Switch string = the FT2 package (`S/pumpclip2/run_all.sh`'s `CB`), `JAX_PLATFORMS=cpu`, WORKERS=2.
Controls `S/lossflip/{pc2_pair_*,nextband_pc2_pair}.csv` were **not overwritten**; the arm writes
`gj_g100_*`. Candidates, `B_sw0` and `index.jsonl` are committed under `S/genejudge/cands/`.

## 5. READING IT
The arm's own acceptance record is a **2-game in-sample** margin (`index.jsonl`: 19,415 → 20,086 over
gens 0-100, every gen after 0 `rejected` by its own bar) — not a read, hence this leg. Settled:
(1) **the block decodes, and decodes hard** — 330 trained params move 5 of 10 switches and `z` reaches
±0.5 against a 0.0625 threshold, so the deadband is no barrier at sigma 0.02 and the arm can drive a
gene to a constant over every board it will ever see; (2) **most of what it bought is a static switch
string** whose price SWITCHVEC already knows, leaving `WHEAT_VOLUME_ON` at 15 % of days as the layer's
one genuine addition; (3) `--train-only sw,swb` is a 10-bit search with a **2-game fitness** — the fix
is a fitness with boards (the `S/judge7065` bar), not a wider block. No follow-on arm is cut.
