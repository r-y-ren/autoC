# KERNELBANK1 (2026-09-28): is V56 the only public kernel worth gating in?

Question: the KERNEL2 line hands our game to the public V56 kernel at d0 h1 on four rival-h1-cash vectors (26, 29, 2338, 2438) and is 0 or negative on 967 (real 938: DECEM / Mother-Goose / DSM / Vadim), 2464 (wheat-then-cow) and the rest. Does any other public pool kernel beat PFS on those vectors?

**Verdict: no. No kernel x vector reaches faithful net flips >= +2 on n >= 8. The best faithful result is +1 (v34 on 967, n4; v56all on 2438, n4), and no vector-level cell has n >= 8 faithful seats. V56 is the only kernel with a measured edge, and the vector lookup is closed.** Every kernel "wins" 12-21 of the 30 PFS-lost seats, but it does so by tape breakage. The mean dtheirs is -14k to -30k (t -3.8 to -4.9), and only 6-11 of the 30 seats keep the rival tape faithful. On those faithful seats the rival purse holds within 5 % of live, and there the kernels flip 0 or 1 seat.

## 1. Candidate kernels (S/pool1/bank, public score, family, licence)

Rule: the top 5 pool agents by public_score, one per code family (bank.tsv `family`), excluding F04_ahmedberatozer. F04 is V56's own family, which also holds its forks: v15stack, v57, herd_saf, clone_ra, pipe18 and others. All five have a permissive licence.

| run | kernel (bank dir) | public | family | licence |
|---|---|---|---|---|
| v38 | ahmedberatozer_kaggriculture_v38_smar | 2625.2 | F01 | Apache-2.0 (in-source header) |
| v34 | ahmedberatozer_kaggriculture_v34_obse | 2601.6 | F02 | Apache-2.0 (header) |
| cha22 | abhinav0370_cha22_agent | 2599.8 | F32 (jaccard 0.81 to V55) | Apache-2.0 (header) |
| v53 | ahmedberatozer_kaggriculture_v53_open | 2597.5 | F03 | Apache-2.0 (header) |
| v41 | ahmedberatozer_kaggriculture_v41_revi | 2586.4 | F05 | Apache-2.0 (header) |

Four of the five are older ahmedberatozer V-series code. To cover lineages outside that author, tier 2 adds the top families that are not ahmedberatozer:

| run | kernel | public | family | licence |
|---|---|---|---|---|
| ravi | ravi123a321at_177_180_fresh_top_30_v | 2517.1 | F07 | no in-source header; Kaggle public-notebook default Apache-2.0 |
| herdsafe3 | arsgorynich_herd_safe_v3_2452 | 2513.3 | POOL2 (Pipe-16 HybridOpening, V lineage) | Apache-2.0 (LICENSE.txt + NOTICE) |
| aurax7 | aurax7_kaggriculture_shop_rou | 2510.0 | F08 | Apache-2.0 (header) |
| reyhan | reyhanksatria_best_market_agent_high | 2497.9 | F09 | no header; Kaggle default Apache-2.0 |

There is also a reference arm, **v56all**: S/v56leg/main.py plays the whole game from h0, in the same mode as the candidates, so it is the like-for-like control.

## 2. Seats (select.py -> res/seats.tsv, res/boards.json)

- **Vector key.** Seats are keyed by the real rival h1 cash after our real PFS h0 (S/gatetable2/res/seats_real.tsv `real`). Key 967 = real 938, and 2464 and 2438 are as named.
- **Sources.**
  - band276: S/bandbank2/boards_band2.json, with base rows from pfs_band2.csv and base faithfulness from JC1 faith.seat.
  - toprival1: boards_new/rev.json, with base rows from res/off_*.csv and `faithful_base`.
  - topv56_1: S/melonswap1/boards_swap.json, with base rows from res/pfs.csv and `base_faithful`.
- **Filter.** Only seats where the PFS base is faithful are kept. PFS-lost seats come first; each episode is used once.
- **Pool sizes.** There are 53 base-faithful seats for 967, 15 for 2464 and 40 for 2438. The 10 taken per vector were all PFS losses, so the base is W 0/30.
- **Why the V56 faithful n was small (4/8/30).** GATETABLE2 counted a seat as faithful only when V56's replay was faithful too, and V56 breaks the tape. Base-faithful seats are plentiful.
- **Harness.** kb.py is S/bandgated1/hybrid.py with the V56 path replaced by any single-file kernel (KB_KERNEL) playing our seat every step from h0. The rest is the S/bandleg1 tape harness: live rival tape, original seat, pinned seed and town, actTimeout 600, master src vrp12_pfs.
- **Faithfulness.** pair.py counts a seat as faithful when the base is JC1-faithful and the arm passes JC1 faith.seat with the boards swapped in. Where no units were kept this is the cash proxy: rival purse >= 95 % of live. v56all on BAND142 seats uses the units basis from judgeclean1/res/units_sold.tsv.
- **Cross-check.** `python3 ../judgeclean1/pair_faith.py res/v38.csv res/v56all.csv` on the 12 BAND142 seats (res/pair_faith_jc1.txt) gives the same picture:
  - All seats: v38 +6 and v56all +5, both GATE2 A/B PASS.
  - Faithful seats: v38 +0 (soft t -1.35) and v56all +1 (n7). The breakage share of dtheirs is 108 % for v38 and 87 % for v56all.

## 3. Kernel x vector (res/table.md)

Base = PFS rows, all 30 lost. The kill rule (stop after 10 seats if kernel W <= PFS W) never fired, because every kernel won >= 1 of its first 10 seats by breakage. The V56 (KERNEL2) column gives V56's h1-mode W on the same seats from GATETABLE2, counting all seats and then jointly-faithful seats. "h0 plants/buys" counts kernels whose h0 includes BUY_SEED or PLANT.

<!-- TABLE -->
| kernel | vector | n | W PFS->kernel | flips | dours (t) | dtheirs (t) | faithful n | W faith PFS->kernel | faith net flips | V56 (KERNEL2) W on same seats | h0 plants/buys |
|---|---|---|---|---|---|---|---|---|---|---|---|
| aurax7 | 967 | 10 | 0->4 | +4/-0 | +1,396 (+0.30) | -12,750 (-2.74) | 4 | 0->0 | +0 (+0/-0) | 7/10 (faith 0/2) | 0/10 |
| aurax7 | 2464 | 10 | 0->8 | +8/-0 | +27,254 (+2.63) | -47,874 (-3.49) | 1 | 0->0 | +0 (+0/-0) | 6/10 (faith 1/4) | 0/10 |
| aurax7 | 2438 | 10 | 0->9 | +9/-0 | +14,986 (+2.45) | -29,085 (-3.57) | 1 | 0->0 | +0 (+0/-0) | 6/10 (faith 3/6) | 0/10 |
| aurax7 | ALL | 30 | 0->21 | +21/-0 | +14,545 (+3.17) | -29,903 (-5.01) | 6 | 0->0 | +0 (+0/-0) | 19/30 (faith 4/12) | 0/30 |
| cha22 | 967 | 10 | 0->0 | +0/-0 | -9,325 (-4.54) | -5,155 (-2.07) | 6 | 0->0 | +0 (+0/-0) | 7/10 (faith 0/2) | 10/10 |
| cha22 | 2464 | 10 | 0->8 | +8/-0 | +27,572 (+2.61) | -49,292 (-3.89) | 0 | 0->0 | +0 (+0/-0) | 6/10 (faith 1/4) | 10/10 |
| cha22 | 2438 | 10 | 0->8 | +8/-0 | +18,565 (+2.27) | -34,225 (-3.03) | 1 | 0->0 | +0 (+0/-0) | 6/10 (faith 3/6) | 10/10 |
| cha22 | ALL | 30 | 0->16 | +16/-0 | +12,271 (+2.34) | -29,557 (-4.56) | 7 | 0->0 | +0 (+0/-0) | 19/30 (faith 4/12) | 30/30 |
| herdsafe3 | 967 | 10 | 0->0 | +0/-0 | -9,679 (-3.59) | -4,839 (-1.77) | 6 | 0->0 | +0 (+0/-0) | 7/10 (faith 0/2) | 10/10 |
| herdsafe3 | 2464 | 10 | 0->8 | +8/-0 | +28,646 (+2.66) | -48,568 (-3.79) | 0 | 0->0 | +0 (+0/-0) | 6/10 (faith 1/4) | 10/10 |
| herdsafe3 | 2438 | 10 | 0->8 | +8/-0 | +16,588 (+2.26) | -28,140 (-2.78) | 1 | 0->0 | +0 (+0/-0) | 6/10 (faith 3/6) | 10/10 |
| herdsafe3 | ALL | 30 | 0->16 | +16/-0 | +11,852 (+2.28) | -27,182 (-4.33) | 7 | 0->0 | +0 (+0/-0) | 19/30 (faith 4/12) | 30/30 |
| ravi | 967 | 10 | 0->4 | +4/-0 | -5,779 (-0.58) | -21,591 (-2.05) | 4 | 0->0 | +0 (+0/-0) | 7/10 (faith 0/2) | 10/10 |
| ravi | 2464 | 10 | 0->0 | +0/-0 | -27,684 (-8.51) | +6,425 (+2.34) | 8 | 0->0 | +0 (+0/-0) | 6/10 (faith 1/4) | 10/10 |
| ravi | 2438 | 10 | 0->3 | +3/-0 | -8,268 (-1.05) | -7,653 (-1.23) | 6 | 0->0 | +0 (+0/-0) | 6/10 (faith 3/6) | 10/10 |
| ravi | ALL | 30 | 0->7 | +7/-0 | -13,910 (-3.03) | -7,606 (-1.67) | 18 | 0->0 | +0 (+0/-0) | 19/30 (faith 4/12) | 30/30 |
| reyhan | 967 | 10 | 0->3 | +3/-0 | -2,267 (-0.20) | -12,526 (-1.16) | 6 | 0->1 | +1 (+1/-0) | 7/10 (faith 0/2) | 10/10 |
| reyhan | 2464 | 10 | 0->2 | +2/-0 | -13,550 (-3.46) | +232 (+0.04) | 7 | 0->0 | +0 (+0/-0) | 6/10 (faith 1/4) | 10/10 |
| reyhan | 2438 | 10 | 0->3 | +3/-0 | -7,893 (-0.54) | +1,619 (+0.18) | 7 | 0->0 | +0 (+0/-0) | 6/10 (faith 3/6) | 10/10 |
| reyhan | ALL | 30 | 0->8 | +8/-0 | -7,904 (-1.29) | -3,558 (-0.72) | 20 | 0->1 | +1 (+1/-0) | 19/30 (faith 4/12) | 30/30 |
| v34 | 967 | 10 | 0->6 | +6/-0 | +1,599 (+0.35) | -22,557 (-3.23) | 4 | 0->1 | +1 (+1/-0) | 7/10 (faith 0/2) | 0/10 |
| v34 | 2464 | 10 | 0->7 | +7/-0 | +25,520 (+2.44) | -44,720 (-3.48) | 1 | 0->0 | +0 (+0/-0) | 6/10 (faith 1/4) | 0/10 |
| v34 | 2438 | 10 | 0->4 | +4/-0 | +13,689 (+1.59) | -21,453 (-2.13) | 2 | 0->0 | +0 (+0/-0) | 6/10 (faith 3/6) | 0/10 |
| v34 | ALL | 30 | 0->17 | +17/-0 | +13,603 (+2.75) | -29,577 (-4.89) | 7 | 0->1 | +1 (+1/-0) | 19/30 (faith 4/12) | 0/30 |
| v38 | 967 | 10 | 0->3 | +3/-0 | -1,920 (-0.40) | -11,162 (-2.38) | 4 | 0->0 | +0 (+0/-0) | 7/10 (faith 0/2) | 0/10 |
| v38 | 2464 | 10 | 0->8 | +8/-0 | +26,720 (+2.61) | -44,576 (-3.46) | 1 | 0->0 | +0 (+0/-0) | 6/10 (faith 1/4) | 0/10 |
| v38 | 2438 | 10 | 0->7 | +7/-0 | +15,811 (+1.87) | -22,488 (-2.08) | 2 | 0->0 | +0 (+0/-0) | 6/10 (faith 3/6) | 0/10 |
| v38 | ALL | 30 | 0->18 | +18/-0 | +13,537 (+2.68) | -26,075 (-4.22) | 7 | 0->0 | +0 (+0/-0) | 19/30 (faith 4/12) | 0/30 |
| v41 | 967 | 10 | 0->4 | +4/-0 | +1,388 (+0.28) | -11,614 (-2.47) | 4 | 0->0 | +0 (+0/-0) | 7/10 (faith 0/2) | 0/10 |
| v41 | 2464 | 10 | 0->8 | +8/-0 | +27,776 (+2.65) | -46,988 (-3.41) | 1 | 0->0 | +0 (+0/-0) | 6/10 (faith 1/4) | 0/10 |
| v41 | 2438 | 10 | 0->9 | +9/-0 | +14,447 (+2.32) | -28,890 (-3.55) | 1 | 0->0 | +0 (+0/-0) | 6/10 (faith 3/6) | 0/10 |
| v41 | ALL | 30 | 0->21 | +21/-0 | +14,537 (+3.10) | -29,164 (-4.86) | 6 | 0->0 | +0 (+0/-0) | 19/30 (faith 4/12) | 0/30 |
| v53 | 967 | 10 | 0->0 | +0/-0 | -10,316 (-3.92) | -4,476 (-1.64) | 6 | 0->0 | +0 (+0/-0) | 7/10 (faith 0/2) | 0/10 |
| v53 | 2464 | 10 | 0->6 | +6/-0 | -880 (-0.34) | -17,622 (-3.90) | 2 | 0->0 | +0 (+0/-0) | 6/10 (faith 1/4) | 0/10 |
| v53 | 2438 | 10 | 0->6 | +6/-0 | +8,641 (+1.40) | -20,613 (-2.13) | 2 | 0->0 | +0 (+0/-0) | 6/10 (faith 3/6) | 0/10 |
| v53 | ALL | 30 | 0->12 | +12/-0 | -852 (-0.31) | -14,237 (-3.77) | 10 | 0->0 | +0 (+0/-0) | 19/30 (faith 4/12) | 0/30 |
| v56all | 967 | 10 | 0->0 | +0/-0 | -9,586 (-4.06) | -5,608 (-2.08) | 6 | 0->0 | +0 (+0/-0) | 7/10 (faith 0/2) | 10/10 |
| v56all | 2464 | 10 | 0->8 | +8/-0 | +28,682 (+2.68) | -48,522 (-3.78) | 1 | 0->0 | +0 (+0/-0) | 6/10 (faith 1/4) | 10/10 |
| v56all | 2438 | 10 | 0->7 | +7/-0 | +16,491 (+2.21) | -28,417 (-2.81) | 4 | 0->1 | +1 (+1/-0) | 6/10 (faith 3/6) | 10/10 |
| v56all | ALL | 30 | 0->15 | +15/-0 | +11,862 (+2.28) | -27,515 (-4.41) | 11 | 0->1 | +1 (+1/-0) | 19/30 (faith 4/12) | 30/30 |
<!-- /TABLE -->

Reading:
- **967 (DECEM / MG / DSM / Vadim), all seats.**
  - The V56-lineage h0 kernels (cha22, v53, herdsafe3, v56all) win 0/10, with dours -9..-10k (t -3.6..-4.5).
  - The wheat-pump V-series kernels v34 (6/10) and v38/v41 (3-4/10) win only by breaking the tape: dtheirs -11..-23k.
- **967, faithful seats (n 4-9).** 0 flips, except v34 +1 (n4).
- **2464.** Every market-only-h0 kernel (V-series, cha22, herdsafe3, aurax7, v56all) wins 6-8/10 on all seats with dtheirs -18..-49k. Its faithful n is 0-2, and no kernel flips a faithful seat.
- **2438 (control).** The market-only-h0 kernels win 4-9/10 on all seats, again by breakage. The faithful n is 1-4 with 0 flips, except v56all +1 (n4). On the same 10 seats, V56 KERNEL2 (h1 mode) holds 3/6 jointly-faithful wins. No candidate reaches V56's measured bar of +5 on n30 faithful.
- **ravi.** The first pass scored a passive 3,000 on every seat. The kernel's last callable, `_kaggle_submission_entrypoint(obs)`, takes one argument and was called with (obs, config). kb.py now applies the engine's arity rule, and that invalid pass is kept only as res/ravi_arity_broken.csv.txt. For the rerun and the reyhan and aurax7 status, see §5.
- **reyhan and ravi (tier 2, full h0 opening: 5 HIRE + cows/sheep + 7 wheat + 12 melon seeds).** These are the only bodies that mostly keep the rival tape faithful: reyhan 20/30, ravi 10/16. reyhan: faithful 967 n6 +1, 2464 n7 0, 2438 n7 0; all-seat W 8/30, dours -7.9k (t -1.3). ravi: faithful 18/30, the only cell with n >= 8 is 2464 n8 at net 0; dours -13.9k (t -3.0). Being faithful exposes them as weaker than PFS on purse, not stronger.

## 4. Inherit-mode question

No kernel qualifies, so this is moot. For the record, reyhan and ravi open with a full h0 (hires, animals, seed buys; reyhan also BUILD_PASTURE), so they could not inherit PFS's h0. aurax7 (BUY/SELL WHEAT) and herdsafe3 (wheat pump + 1 wheat seed) are market-only. So is every tier-1 candidate, a wheat pump:
- v38, v34 and v41: BUY/SELL WHEAT.
- cha22 and v56all: BUY_PRODUCT WHEAT plus 1 wheat seed.
- v53: BUY 7 / SELL 2.

None hires or plants at h0. Any of them could therefore be handed the game at h1 after PFS's real h0, the way KERNEL2 inherits (v56h1m relabel), without losing an h0 plant.

## 5. Status / completeness

Complete: v38, v34, cha22, v53, v41 (tier 1, 30/30 seats each), v56all (reference, 30/30), herdsafe3, aurax7, reyhan (30/30),
ravi 30/30 after the arity fix. Kill rule never fired (all PFS W = 0 on the chosen seats, every
kernel won >= 1 of its first 10 by breakage). Incident: the first chain (`run.sh all`) died after v38 because run.sh was edited while bash was
reading it; the remaining kernels ran through chain.sh (same `run.sh k` commands).

Re-run: `bash S/kernelbank1/run.sh select`, then `bash S/kernelbank1/run.sh k <name> <bank dir>` per kernel (or S/kernelbank1/chain.sh), then `bash S/kernelbank1/mkdoc.sh`. Replays are in S/kernelbank1/gz/<arm>/.
