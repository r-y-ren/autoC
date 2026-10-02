# Did any local leg ever predict a Kaggle outcome? (2026-09-09)

Data-only. Sources: `S/glut/verdicts.log`, memory `kagg3-optimisation-log` / `kaggle-episode-api`,
`docs/strategy/2026-09-05-build-story.md`, `2026-09-08-how-we-built-the-agent.md`,
`2026-09-09-judge-calibration.md`, `2026-09-09-loss12-se.md`, `2026-09-09-loss20-leg.md`.
One live read: Kaggle `GetLeaderboard` (competition 147734), 2026-09-09 — team TEAM_ID,
sub **56098262, rank 1254 / 8379, score 1957.3**.
`S` = `/tmp/claude-0/-mnt-e--work-kaggriculture3/8b388b22-9a4b-4bf0-8e3e-dc4aac1d5f04/scratchpad`.

## 1. The uploads

Ratings restart on every resubmission and the opponent pool drifts daily, so only the
**settled** level is comparable, and only loosely.

| sub | theta | up | local read at promotion | Kaggle settle |
|---|---|---|---|---|
| 55884330 | flow38_g25 | 08-30 | 4-opp panel 88.1 % / +11,223 (n=624), +2,118/g t 9.9 | peak 1799 → ~1600 |
| 55890731 | flow38_g25_HORIZON | 08-30 | same family | 60W-24L 71.4 %, 1797 (starved) |
| 55909963 | flow49b_g450 | 08-31 | — | 1655, 69 % |
| 55919021 | flow51_g900 | 08-31 | — | 1601 (sidelined) |
| 55924626 | (unconfirmed) | 08-31 | — | 83W-56L 59.7 %, **1790.8**, rank 900 |
| 55935357 | flow54_g700 | 09-01 | — | 53W-41L 56.4 %, 1676.8 |
| 55957863 | flow58_g450 | 09-02 | — | 1574.4, rank 1345 |
| 55966718 | flow58_g450_split | 09-02 | — | 1696.5, rank 1075 |
| 55974820 | stack | 09-03 | 4-opp n=768 +2,184 t 5.1, win 61.5→70.3 %; 20-tape panel +1,405 t 4.9 | ~54 %, rank 1006 |
| 55981305 | earlysell | 09-03 | same stack read + EARLY_SELL A | 50W-39L, 1680, rank 1188 |
| 56006782 | flow58_g450_pump | 09-04 | panel24 64→87 %, +20.5k; top10 42 % | 62W-25L, **~1996**, rank ~745 |
| 56013041 | slot0 | 09-04 | pump moved to index 0 (no paired legs) | 100W-90L 52.6 %, peak 2047, **1983** |
| 56028553 | flow102_g280 | 09-05 | **top10 pooled 1,280 bd +7.6 pts (+3,240/g, t 5.2 & 3.1 on two bases); band6 pooled 288 bd LEVEL (−0.3 pts, +1.06k)**; flood6/jesse4/today41 did not exist yet | 177W-173L 50.6 %, **1718**, rank 1388 |
| 56098262 | flow135_g350 | 09-11* | **band6@1 +32.3 / top10 +34.7 / band6@2 +36.4 / flood6 +25.0 / jesse4 +36.7 / today41 +34.3; pooled 1,904 bd 52.6→86.8 % (+34.2 pts, +9,095/g, t 21.4)**; h2h vs g200 +6.4 pts t 3.0; no held-out pinned read (it *is* the lossflip base) | peak **2144** (ATH), settle **1957.3** rank 1254/8379, ~52 % |

\* log clock; it is the most recent upload.

Uploads with ≥ 3 legs recorded: **exactly one** (56098262). With ≥ 2 paired legs: **two**.
Everything before 09-05 used panel24 / 4-opp / 20-tape sets that are not the same legs.

## 2. Ranking the legs against Kaggle — not computable

A Spearman over uploads needs n ≥ 3 upload-level pairs of (leg delta, settled-rating delta).
We have **n = 1** for band6/flood6/jesse4/today41 and **n = 2** for top10.
No ρ is reported here, because none can be honestly computed. The only comparable statement
is a 2-point sign check:

| upload | leg reads | Kaggle settled Δ vs its predecessor | leg verdict |
|---|---|---|---|
| 56028553 flow102_g280 | top10 **+7.6 pts** t 5.2/3.1; band6 level | 1983 → 1718 = **−265** | top10 WRONG |
| 56098262 flow135_g350 | all six legs up, pooled **+34.2 pts** t 21.4 | 1718 → 1957 = **+239**, but the account already settled at 1996 / 1983 on 09-04 with no ES theta | recovery only; **level vs the ceiling** |

The 09-11 09:05Z verdict line records the falsification directly: *"paired open-loop tapes of the
same opponents give g350 ≈ 62 % (8 tapes), live is 3/13 ≈ 23 % against the same band (p < 0.01)."*

## 3. Answer

**No local read has ever predicted a Kaggle improvement that materialised as a new settled level.**
The account has been pinned at **1,957–1,996** since 2026-09-04, when a hand lever (the wheat pump,
56006782) first reached it. The +34.2-pt / t 21.4 / 1,904-board read on flow135_g350 bought a new
*peak* (2144) and recovered the 265 points flow102_g280 had lost — and then settled at 1957.3, i.e.
back on the same wall, 26–39 points **below** the 09-04 pair. Local 86.8 % vs live ~52 %: the drawn
legs overstate the live win rate by ~34 points.

Reads that predicted improvements which did NOT materialise:

* **flow102_g280** — pooled top10 +7.6 pts on 1,280 paired boards, replicated on two independent
  base sets (t 5.2 and 3.1), band6 level. This is *precisely the shape of tonight's proposed rule*,
  and it is the worst upload of the campaign: −265 rating, 50.6 % at settle, rank 1388.
* **flow135_g350** — every one of six legs up, t 3.4–13.5, pooled t 21.4. Live: level with the
  09-04 ceiling.
* **flow129_g40/g100/g180, flow130_g130/g260, flow133_g100, flow134_g40** — +8.4 to +25.6 pooled
  pts at t 3.4–16.8, all "PROMOTED / HANDED TO USER". **None was ever uploaded**, so they are not
  evidence in either direction; they only show how cheaply the drawn legs manufacture t ≥ 4.

The judge-calibration note is consistent with this from the other side: the drawn legs rank
near-neighbour arms *against each other* at ρ 0.83–0.95, i.e. internal consistency, and the pinned
held-out judge has **zero demonstrated true positives** over 7 arms.

## 4. What this implies for tonight's rule

**(a) A pooled top10+today41 pass at grouped |t| ≥ 2 is not sufficient.** Its one historical
instance is a false positive that cost 265 rating points, and both legs are open-loop drawn-board
tapes — the population the tape-fidelity note and the 09-11 09:05Z measurement both say overstate
us against the 2,000+ band. Keep them as a **non-regression floor** (veto if a big leg is down),
never as the promotion evidence. `band6`/`jesse4` never rejecting alone is right and unaffected.

**(b) The fresh-loss leg is the better *candidate* predictor, on mechanism, not on evidence.**
LOSS12/LOSS20 are pinned-town tapes cut from the live losses of the live theta: they replay the
real game to the coin, are drawn from the population that actually decides our rating, and are
uncontaminated (verified against every `launch_flow*.sh`, `heldout_ids.txt`, `leg_family.py`).
That is the only external-validity mechanism any leg has. But it has **zero upload-level
evidence** — no upload has ever been promoted on it — and two structural defects:
its base is 0/24 (all losses), so **no candidate can ever drop a game** and the statistic is
one-sided; and two of the twelve tapes (107088554, 107095149) are not byte-exact vs Kaggle and
carry −5.9k / −5.8k of pull and the largest cross-candidate swing (sd 5,572 / range 14,020).

**(c) The n it needs.** Pinned tapes are deterministic (per-tape sd 0, one tape sd 64), so
**extra seeds buy nothing — only more tapes raise n.** With the median per-board sd of 5,716
coins measured over the seven flow166/167 candidates (range 4,006–6,814):

| n boards | min effect detectable at \|t\| ≥ 2 |
|---|---|
| 12 (LOSS12) | 3,300 coins/board |
| **20 (LOSS20)** | **2,556** |
| 40 | 1,808 |
| 60 | 1,476 |
| 100 | 1,143 |
| 120 | 1,044 |

LOSS20 at n = 20 therefore only resolves a step of **≥ ~2,500 coins/board** — which is exactly the
size of the best candidate seen (flow167_g150 +2,555, t 2.05 at n = 12). To hold a ≥ +1,000
coins/board step at |t| ≥ 2 needs **~120–130 boards** (≈ 240–260 games). At the current cut rate
(~15–25 fresh tapes/day) that is 5–8 days of losses alone, or ~3 days if fresh **wins** are cut too
— which would also restore the drop side and fix the one-sidedness for free.

**Recommended rule for tonight**

1. **Screen (necessary, not sufficient):** LOSS20 d-margin > 0 with the two non-byte-exact tapes
   (107088554, 107095149) excluded, and seat-grouped |t| ≥ 2 on the remaining ~18 boards.
   Add a sign check: **≥ 15 of 20 boards positive** (one-sided p = 0.021; 14/20 is p = 0.058 and
   13/20 is p = 0.13 — do not accept those as evidence).
2. **Floor:** no drawn leg down by more than noise (the existing band6/jesse4-never-reject-alone
   convention stays); the melon-family catastrophe check stays.
3. **Head-to-head, not vs an old base:** a resubmission restarts the rating and costs ~150 games of
   re-climb, and the ceiling is ~1,980. Promote only on a paired win over the **current live**
   theta (flow135_g350) on the fresh-loss set — beating a stale base is what produced flow102_g280.
4. **Do not treat a large pooled drawn-leg t as evidence of a Kaggle step.** Both times it has been
   tested it did not deliver one. State the pooled read, then decide on (1)–(3).
5. **Power the leg before trusting it as a gate:** cut fresh wins as well as losses and grow the
   pinned fresh set toward ~120 boards. Until then LOSS20 is a screen, not a gate — the same
   status the judge-calibration note gives LEG20.

## Caveats

* Every rating comparison crosses a restart and ~4–6 days of opponent drift; the settled levels
  above are not paired measurements and should be read to ±50 rating points at best.
* n = 1 upload with the full six-leg read and n = 2 with any comparable leg. Nothing here has
  the power to *reject* the drawn legs; it only records that they have never been vindicated.
* The 09-04 ceiling (1996 / 1983) was itself reached by hand levers (pump, slot0), which is why
  "flow135_g350 beat its predecessor" is not the same claim as "the legs predicted an improvement".
