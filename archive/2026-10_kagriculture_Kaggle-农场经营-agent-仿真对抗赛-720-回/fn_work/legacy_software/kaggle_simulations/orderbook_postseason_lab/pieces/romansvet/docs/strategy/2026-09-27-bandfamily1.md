# BANDFAMILY1 (2026-09-27 17:12Z-19:40Z): does a public V body out-rate PFS on the BAND leg?

**Verdict: NO.** No V kernel, the ENGINE port, or any runnable hybrid out-rates PFS (vrp12_pfs) on the 142-seat BAND leg.
- The strongest family on the band is **ours (PFS)**: W 91/142, V cell 70/81.
- V56/V57 beat PFS only in the MELON cell (31/51 vs 14/51), and that edge cannot be used:
  - It needs V56's own d0 melon plate. The rival's family is visible only at d1 h0.
  - On the non-collapsed seats it is denial on open-loop tapes: Δours +277, Δtheirs −9.8k.
- Part B was **not triggered** under the stated rule: the best V arm is −37 W and −35 θ vs PFS. Two gated hybrids were run anyway, and both lose.

## Harness
- **Band seats:** S/bandleg1 (boards_all.json): 142 tape seats at the original seat, pinned seed + town, actTimeout 600.
- **Kernel arms:** `S/bandfamily1/fam.py` = S/bandleg1/leg.py `job()` file-agent branch (the `fid` bed, which reproduced 96/96 live games exactly). The kernel main.py plays our seat.
- **ENGINE arm:** `S/bandfamily1/eng.py` runs the PROGFIX2 tree b7a98688 (worktree kagg3_wt_wateraudit). Setup is the IMIT recipe: tree LE.SWITCHES + head_940 + OVERFLOW_GUARD_V3 + PROGRAM_ENGINE_ON, with PROGRAM_HERD_MIDDAY at its default of on.
- **PFS rows:** S/bandleg1/res/pfv1.csv.
- **θ method:** `famsum.py` uses the Part C method of pair.py. It is the family-weighted Elo/400 MLE over vrp10's live games, with the per-family win-rate change applied at vrp10's band mix (MELON 26 / V 16 / ZERO 4). It is reported relative to PFS (PFS vs master = +36). SE comes from a 200× seat bootstrap.
- **Collapse:** the tape purse ends more than 25 % below its PFS purse. That means the open-loop tape broke.

## Part A: family strength on the band (our seat = the arm)
| arm | W | MELON W / margin | V W / margin | ZERO | OTHER | collapse | flips vs PFS | fam Δθ vs PFS (SE) | direct Δθ | excl. collapse |
|---|---|---|---|---|---|---|---|---|---|---|
| (1) PFS vrp12_pfs | **91** | 14/51 −6.6k | **70/81 +5.8k** | 5/7 +8.1k | 2/3 −3.5k | 0 | – | 0 | 0 | 0 |
| (2) V56 kernel (S/v56leg/main.py) | 54 | **31/51 +20.4k** | 22/81 −4.9k | 1/7 −7.1k | 0/3 −10.2k | 10 (all MELON) | +24/−61 = −37 | **−35 (31)** | −33 | −61 |
| (3) V57 kernel (v57_fund) | 54 | 31/51 +20.4k | 22/81 −4.8k | 1/7 | 0/3 | 10 | −37 | −35 (29) | −33 | −61 |
| (4) V38 kernel (v38_smar, bank public_score **2,625.2** = top of bank) | 31 | 25/51 +16.5k | 5/81 −6.4k | 1/7 | 0/3 | 10 | −60 | −105 (27) | −76 | −139 |
| (5) ENGINE port (PROGFIX2 IMIT) | 10 | 10/51 −6.7k | 0/81 −28.4k | 0/7 | 0/3 | 6 | −81 | −206 (20) | −166 | −230 |

- **V57 vs V56:** V57 plays within 184 coins of V56 on every seat (23/142 byte-identical), so it is the same body.
- **V56 vs PFS, pooled:** Δours −3.4k, Δtheirs −6.1k.
- **V56 vs PFS in the MELON cell:** Δours +7.6k, Δtheirs −19.4k (median −12.6k). With the 10 collapsed seats removed, V56 goes 21/41 vs PFS 11/41, at Δours +277 and Δtheirs −9.8k. The whole MELON edge is a price effect on a rival that cannot react (the same pattern as the MELONGENES1 finding that tapes overstate denial).
- **ENGINE port:** gifts +13k theirs and loses everywhere. This is consistent with PROGFIX2.

## Hybrids
| arm | what | seats run | result | fam Δθ vs PFS |
|---|---|---|---|---|
| oracle composite (NOT runnable) | MELON seats take V56's outcome, others PFS | 0 (recombination) | W 108; excluding collapse W 101 | +111 / +62 |
| d1 gate (runnable) | PFS plays d0; at the first d≥1 obs, rival melon 1..10 → V56 kernel for the rest (49 seats; the other 93 = PFS by construction) | 49 MELON | **+0/−13**, Δours **−80.4k** (t −30), Δtheirs +49.8k; MELON 1/51 | **−62** (direct −33) |
| V56 d0 + d1 gate (runnable; K=0 prefix) | V56 plays d0 always; MELON → V56 continues, else PFS from d1 | 54/81 V seats (stopped) | V seats **0/54 vs PFS 48/54** (−48 flips), Δours −9.1k, Δtheirs +23.3k | dead |

- **Control:** HY_MODE=off on 5 seats (3 MELON, 2 V) reproduces pfv1 exactly (5/5 byte-identical).
- **Why each hybrid fails:**
  - The V56 kernel cannot run a farm it did not open (d1 gate: our purse falls ~80k).
  - PFS cannot run V56's d0 opening (0/54 on V seats). This is the RLREVIEW1 prefix result (K2 4-55) again, now on the band.
- **The gate is dev-inert:** V56 dev boards show rival d1 melon 12, so the d1 gate never fires there. No dev leg was needed.

## Part C
- **(i) Does anything out-rate PFS?** No. Best V body: −35 θ (SE 31). Best runnable hybrid: −62 θ. The only positive number is the non-runnable family-oracle composite: +62 θ excluding collapse, all of it denial on open-loop tapes.
- **(ii) Ship path and licences:** not applicable, because there is no ship path. Kernel licences and the competition's public-code rule were not checked.
- **(iii) Strongest family on the band:** ours. PFS W 91/142 against V56's 54, V38's 31 and ENGINE's 10. The V bodies win only against MELON openers, and only with their own d0 plate. The top-10 edge (tuned V vs melon openers, TOP5VSV1) does not transfer as a kernel, a d1 hand-off or a d0 prefix.

## Files
- S/bandfamily1/: fam.py, eng.py, hybrid.py, famsum.py, composite.py, hysum.py, summary.txt, checkpoint.txt; res/{v56,v57,v38,eng,hy,hy_ctl,v0}.csv plus logs.
- Rerun:
  - `cd S/bandfamily1; nice python fam.py v56=S/v56leg/main.py -w 5`
  - `HY_MODE=gate python hybrid.py hy res/hy.csv melon -w 6`
  - `python3 famsum.py; python3 hysum.py`
  - ENGINE: from the kagg3_wt_wateraudit tree with KAGG3_SRC/PYTHONPATH=$PWD/src, run `python S/bandfamily1/eng.py res/eng.csv -w 6`.
