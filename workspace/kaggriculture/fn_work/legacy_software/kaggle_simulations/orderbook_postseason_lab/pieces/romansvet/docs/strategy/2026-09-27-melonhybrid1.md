# MELONHYBRID1 (2026-09-27 20:24Z-21:30Z): does V56's d0 melon plate carry its MELON-seat edge? No, its body does. Hybrid (b) is dead on both families

**Verdict: the plate does not carry the edge (step 3 not triggered, no src change).** Hybrid (b) plays V56's exact d0 plate, then hands over to the PFS body from d1.
- **MELON seats:** it goes **9/51**, against V56 31/51 and PFS 14/51.
  - vs PFS: flips +5/−10.
  - vs V56: flips +1/−23. Δours +203 (t 0.1), **Δtheirs +24,376 (t 11.2)**.
- **Our purse is the same under both bodies.** The plate plus the PFS body earns what the V56 body earns. The whole MELON edge is what the V56 **body** takes from the rival from d1 on.
- **Handover cause:** V56's d0 leaves the farm with no cash, which starves the PFS body of labour and herd.
  - Cash at d1 h0 is **18 coins**, against 214 for PFS's own d0.
  - PFS then makes 0 hires on d1 and **19.6 hires over d1-9**, against 51.0 for V56 and 32.5 for PFS.
  - One of V56's two opening sheep **escapes, unfed 2 days, in 49/51 seats**. V56 and PFS lose none.
  - The herd at d10 is 2.6 cows / 1.7 sheep / 0.2 geese, against V56's 7.0 / 5.2 / 0.7.
  - With that herd we put 72 fewer MILK units and 155 fewer FERT units into the shared books than V56 does. The rival's MILK / STRAWBERRY / WOOL / FERT prices rise and it takes **+25.7k**.
- **Fixability:** the handover is only fixable by porting V56's d1-9 cash engine (445 u of wheat bought from the book, 51 hires d1-9, herd 4 → 13 by d10). That engine *is* the V56 body, not a handover patch.

## Harness
- **Runner:** `S/melonhybrid1/hybrid.py` is a copy of `S/bandfamily1/hybrid.py` on the same S/bandleg1 harness. That means BAND142 tapes, the original seat, pinned seed and town, SAFETY_S 1e9, REPAIR_MS 1e7 and actTimeout 600. Our side is master src = vrp12_pfs.
- **Modes are fixed, not gated:**
  - `off`: PFS on every step.
  - `v0pfs`: the V56 kernel `S/v56leg/main.py` plays d0, then PFS from d1 h0. This is hybrid (b)'s body.
  - `v56all`: the V56 kernel on every step.
- **Replays:** kept in `gz/<arm>/` (not committed).
- **Fidelity:**
  - Controls on 2 MELON seats (highfrequencyf, kuengo): `off` = pfv1 2/2 and `v56all` = bandfamily1 v56 2/2, byte-identical.
  - The full `v56all` MELON run reproduces bandfamily1 `res/v56.csv` **51/51**.
  - The 6 V trace seats reproduce `res/v0.csv` / `v56.csv` / `pfv1.csv` 6/6 for each body.
  - Every trace re-application ends on the replay rewards: 18/18 V and 153/153 MELON.
  - PFS MELON replays come from `S/melonaudit1/gz`, which matches pfv1 51/51.
- **Trace:** `trace.py` re-applies every step with the pinned engine, using the S/melonwin1 `_commit_unit` hook. It logs every market unit (seat, step, op, item, price) and, at each h0, our cash, hires_today, hands and tiles. `tracetab.py` builds the tables.

## 1. Hybrid (b) on the 51 BAND142 MELON seats, paired (`res/v0pfs_melon.csv`, `res/sum_v0pfs_melon.md`)
| seats (rival d0-9 melon plate) | n | **hybrid W** | PFS W | V56 W | flips vs PFS | Δours vs PFS (t) | Δtheirs vs PFS (t) | flips vs V56 | Δours vs V56 (t) | Δtheirs vs V56 (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| MELON all | 51 | **9** | 14 | 31 | +5/−10 = −5 | +7,847 (3.3) | +5,025 (1.3) | +1/−23 | +203 (0.1) | **+24,376 (11.2)** |
| plate ≤ 8 | 5 | 1 | 5 | 3 | −4 | −4,290 | +17,450 | +1/−3 | +5,057 | +28,659 |
| plate 9-11 | 21 | 5 | 7 | 13 | −2 | +11,606 (2.7) | −988 | +0/−8 | +3,199 | +23,757 (8.0) |
| plate ≥ 12 | 25 | 3 | 2 | 15 | +1 | +7,116 (2.5) | +7,591 | +0/−12 | −3,285 | +24,039 (7.0) |

- **W-L:** hybrid 9-42, V56 kernel 31-20, PFS 14-37.
- **Collapse:** in 6/51 seats the rival's purse ends more than 25 % below PFS's (open-loop tape breakage), against 10/51 for V56.
- **Together with bandfamily1:** hybrid (b) is V 0/54 (PFS 48/54) and MELON 9/51 (PFS 14/51), so it is worse than PFS in both cells.
- **The plate carries none of V56's W edge.**
  - In the ≥ 12 stratum V56 wins 15, the hybrid 3.
  - That stratum is 1-23 under PFS (MELONWIN1). There V56's edge is entirely the d1+ body.

## 2. The handover, traced
### 2a. Six V seats, day × body (mean; bodies hy = V56 d0 + PFS / V56 = V56 continuing / PFS). `res/trace6_tables.md`
Seats: richard6969_113251221, offhand_114127228, pensukesan_114164108, qq_113248648, arsekkat_113239492, trantrikien239_113289898. They were chosen to span hybrid Δtheirs +8.0k..+31.8k.

Finals: ours hy 89,659 / V56 89,823 / PFS 98,909; theirs **115,997** / 93,797 / 94,984.

| day | our melon u sold (hy / V56 / PFS) | rival melon u sold | melon quote h0 | our cash h0 | our hires | our sales coins | rival sales coins |
|---|---|---|---|---|---|---|---|
| 1 | 0 / 0 / 0 | 0 / 0 / 0 | 256 / 256 / 256 | **6 / 6 / 179** | **0 / 2 / 1** | 0 / 266 / 0 | 300 / 299 / 300 |
| 2 | 0 / 0 / 0 | 0 / 0 / 0 | 260 | 6 / 92 / 91 | 1 / 4 / 2 | 396 / 475 / 592 | 550 / 551 / 550 |
| 3 | 0 / 0 / 0 | 0 / 0 / 0 | 262 | 401 / 264 / 626 | 1 / 5 / 4 | 292 / 451 / 580 | 586 / 584 / 596 |
| 4 | 0 / 0 / 0 | 0 / 0 / 0 | 264 | 506 / 262 / 675 | 2 / 4 / 4 | 287 / 563 / 1,355 | 631 / 626 / 624 |
| 5 | 0 / 0 / 0 | 0 / 0 / 0 | 266 | 465 / 608 / 1,390 | 1 / 4 / 4 | 856 / 524 / 1,852 | 528 / 524 / 520 |
| 6 | 0 / 0 / 0 | 0 / 0 / 0 | 267 | 1,287 / 726 / 972 | 3 / 7 / 4 | 277 / 3,283 / 631 | 3,582 / 3,504 / 3,555 |
| 7 | 0 / 0 / 0 | 0 / 0 / 0 | 268 | 287 / 892 / 736 | 2 / 7 / 5 | 1,296 / 745 / 1,860 | 792 / 772 / 760 |
| 8 | 0 / 0 / 0 | 0 / 0 / 0 | 269 | 1,343 / 426 / 2,147 | 5 / 8 / 6 | 761 / 2,832 / 1,291 | 3,374 / 3,260 / 3,333 |
| 9 | 0 / 0 / 0 | 0 / 0 / 0 | 270 | 586 / 1,148 / 1,844 | 3 / 8 / 6 | 2,664 / 2,553 / 5,105 | 2,851 / 2,658 / 2,771 |
| 10 | **0 / 60 / 0** | 61 / 61 / 61 | 271 | 2,959 / 2,034 / 6,132 | 6 / 11 / 7 | 1,403 / 15,493 / 2,199 | 18,107 / 16,092 / 17,849 |
| 11 | **66 / 12 / 0** | 10 / 10 / 10 | 225 / 129 / 225 | 2,343 / 14,902 / 4,366 | 4 / 10 / 8 | 11,665 / 4,019 / 2,771 | 5,104 / 3,858 / 4,804 |
| 12 | 0 / 0 / 0 | 0 / 0 / 0 | 93 / 78 / 215 | 12,519 / 14,111 / 5,828 | 8 / 9 / 10 | 400 / 4,675 / 247 | 4,527 / 4,042 / 4,190 |

Hires d1-9: hy **18.5** / V56 49.3 / PFS 35.7. Herd at d10 (cow / sheep / goose): hy **2.3 / 1.2 / 0** / V56 6.3 / 4.5 / 0.7 / PFS 6.3 / 3.3 / 2.2.

**Where the rival's +22.8k (hy − V56) comes from.** On these 6 seats the rival's units match across bodies to within 1.5 %, so it is essentially all **price**:

| rival product | hy − V56 | hy − PFS | rival realised price (hy / V56 / PFS) | our units into that book (hy / V56 / PFS) |
|---|---|---|---|---|
| MILK | **+8,633** | +10,246 | 133 / 88 / 79 | 102 / 172 / 174 |
| WOOL | +5,050 | +93 | 150 / 114 / 149 | 112 / 128 / 110 |
| FERTILIZER | +4,600 | +3,299 | 63 / 49 / 53 (and fert buys 55 / 38 / 43) | 125 / 305 / 199 |
| MELON | +3,102 | −111 | 238 / 196 / 240 | 141 / 72 / 90 (hy sells d11, after the rival's d10 line; V56 books d10 first) |
| STRAWBERRY | +1,570 | +7,106 | 133 / 126 / 101 | – |
| all | **+22,800** | +21,711 | – | – |

### 2b. The same trace on all 51 MELON seats (`res/trace_melon_tables.md`; PFS = S/melonaudit1 replays)
Finals: ours hy 109,517 / V56 109,314 / PFS 101,671; theirs **113,306** / 88,930 / 108,281.
- **Opening state:**
  - Cash at d1 h0: 18 / 18 / 214.
  - Hires d1: **0.0** / 2.9 / 1.0. Hires d1-9: **19.6** / 51.0 / 32.5.
  - An opening sheep escapes by d3 in **49/51** seats for the hybrid, 0/51 for V56 and 0/51 for PFS.
  - Herd at d10: **2.6 / 1.7 / 0.2** vs V56 7.0 / 5.2 / 0.7 vs PFS 6.1 / 3.3 / 1.5.
- **Rival hy − V56 = +25.7k.** By product: MILK **+11.0k** (price 178 vs 129, units 168 vs 147), STRAWBERRY +4.7k, WOOL +4.2k, FERT +4.0k, EGG +1.1k, MELON +0.7k.
  - The rival's melon price is 167 vs 164. On MELON openers our d11 dump still lands inside the rival's d10-19 melon line, so melon timing is not the MELON-seat gap.
  - Here the rival's units also move, not only its prices. That is the compound effect of V56's denial on a cash-tight rival.
- **Our volume into the shared books (hy / V56):** MILK 137 / 209, FERT 181 / 336, WHEAT 334 / 654, STRAWBERRY 219 / 247.
  - V56 also buys 445 u of wheat from the book (hy 88, PFS 135). This is its d1-9 cash and feed engine.
- **The V56 MELON edge vs PFS, for reference:** rival −20.5k = MELON −5.7k (V56 books d10 ahead: rival melon price 164 vs 220), WOOL −5.5k, MILK −3.3k, FERT −2.5k, STRAWBERRY −1.6k, EGG −1.4k.
  - This is the same same-window denial that MELONSWAP1 found for top MELON bodies.

### Handover cause (named)
1. **Cash starvation.** V56's d0 spends the purse to about 18 coins: 12 melon + 8 wheat seeds, 2 cows, 2 sheep, 5 hires. PFS's d1 planner then makes 0 hires. V56 funds d1 from shed-wheat sales (+296 coins d1) and keeps hiring 3-5 per day.
2. **Opening-herd escape.** PFS's feed rule lets one of V56's two sheep go unfed for 2 days (engine `_daily_refresh_animals`: `consecutive_unfed >= 2` → escape) in 49/51 seats.
3. **Herd never catches up.** PFS's d1-9 animal buys stall on cash. The herd sits at 4.5 animals at d10 vs V56's 12.9, which is 72 fewer MILK and 155 fewer FERT units into the shared books.
4. **Late melon (V seats only):** PFS holds the harvest until dusk and sells d11, after a V rival's d10 line. The rival gets +3.1k.

**Why no fix was built:** step 3 was gated on the plate carrying the edge, and it does not.
- A minimal PFS patch is not enough to close the gap. Feeding the sheep and one d1 hire would address items 1-2, which are worth one animal.
- The gap is items 3-4: V56's d1-9 herd and wheat engine plus d10 booking. That engine is the V56 body.
- The V56 body itself cannot be gated in: rival family is visible only at d1, the d1 gate hands a PFS-opened farm to the kernel (dours −80k, BANDFAMILY1), and V56 on V seats is 22/81.

## 4. Rules check: V56 kernel licence
`S/v56leg/main.py` states **Apache-2.0** explicitly in its header, with the full licence text and notices retained.
- **Lineage:** public V39 plus layers by thomastschinkel, yhay81 (shop-router-0908/0909/0911), destbreso, aurax7, tetsutani, prvsiyan, Dmitrii Gluzdov and Ahmed Berat Ozer (v25-v31 / EXP-149..173).
- **Obligations if reused:** Apache-2.0 would allow reuse with attribution and the licence text retained, and the competition's public-code rule would still apply.
- **Moot here:** nothing ships from this stream, neither their file nor a d0 opening pattern.

## Commands (S/melonhybrid1/run.sh)
```
cd S/melonhybrid1
bash run.sh ctl          # fidelity: off = pfv1, v56all = bandfamily1 v56 (2 MELON seats, byte-identical)
bash run.sh melon        # (1) HY_MODE=v0pfs hybrid.py v0pfs res/v0pfs_melon.csv fam:MELON -w 2   (~18 min)
python3 sumup.py res/v0pfs_melon.csv > res/sum_v0pfs_melon.md
bash run.sh trace        # (2) 6 V seats x {v0pfs, v56all, off}, kept replays -> trace.py -> res/trace6.tsv.gz, tracetab.py -> res/trace6_tables.md
bash run.sh melontrace   # (2b) v56all on 51 MELON (kept replays), PFS = melonaudit1 gz, trace -> res/trace_melon.tsv.gz / res/trace_melon_tables.md
```

## Files
- **S/melonhybrid1/:** hybrid.py, trace.py, tracetab.py, sumup.py, run.sh, checkpoint.txt.
- **res/:**
  - v0pfs_melon.csv (51), v56all_melon.csv (51), ctl_off.csv, ctl_v56.csv, tr_{v0pfs,v56all,off}.csv (6 V seats);
  - sum_v0pfs_melon.md;
  - trace6.tsv.gz, trace6_tables.md, trace_melon.tsv.gz, trace_melon_tables.md;
  - logs.
- **Not committed:** replays in gz/.
