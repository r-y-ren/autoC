# BAND-GRAD: is the judge band-dependent? (analysis 2026-09-12, answering §92 / `2026-09-11-strategist-next.md` #1-#2)

Data-only. Script `S/bandgrad/bandgrad.py`, board-level rows `S/bandgrad/rows.csv`, machine output
`S/bandgrad/bandgrad.md`. No engine leg was run: every number below is a re-pairing of leg csvs we
already own.

## What was pooled

Both seats of a board are averaged into ONE observation (`2026-09-09-lottery-audit.md` s4.1);
win flips are still counted per game, the way the verdict lines print them.

| leg | csvs | boards | opponent rating (min–max, mean) | rating source |
|---|---|---|---|---|
| LIVE62 | `flow193_g100_hr_live62` / `g1000pair_hirerow_live62` | 62 | 1827–2070, 1992 | ListEpisodes sub 56098262, opponent `initialScore` (re-pulled 2026-09-12; `S/livewin/day.json` died in the reboot) |
| LOSS10 | `S/bloss/B.csv` / `S/bloss/hr.csv` | 10 | 2175–2381, 2263 | `S/bloss/rows.json` `opp_rate` |
| LIVEC-H30 (ids 43-72) | `flow193_g100_hr_livech` / `g1000pair_hr_livec` | 30 | 2440–2615, 2536 | `S/livec/provenance.txt` cut tables |
| LIVEC-H30B (ids 73-102) | `flow193_g100_hr_livech2` / `g1000pair_hr_livec` | 30 | 2519–2682, 2594 | `S/livec/rows_new3.json` |
| TOPB2 | `flow193_g100_hr_topb2` / `g1000pair_hr_topb2` | 20 | 2953–3081, 2989 | `S/topb2/chosen.json` (team LB score 2026-09-10) |

**152 boards, 304 games, rating span 1827–3081, ZERO boards dropped for a missing rating.**
The ES-record pair adds the same five legs for each of 19 `AUTOJUDGE-vsB` records (2,868 board rows).
`flow210_g10_hr` and `flow210_g10p_hr` are byte-identical csvs (same md5) — one record counted twice;
every conclusion below is unchanged if it is counted once.

---

## 1. B − hr, binned by opponent rating

| rating bin | boards | games | mean Δmargin | SE | t | win flips +/− | legs |
|---|---|---|---|---|---|---|---|
| <2200 | 64 | 128 | **+716** | 411 | +1.74 | +4/−8 | LIVE62, LOSS10 |
| 2200-2400 | 8 | 16 | **+501** | 590 | +0.85 | +1/−0 | LOSS10 |
| 2400-2600 | 41 | 82 | **+1,110** | 364 | +3.05 | +12/−4 | LIVEC-H30/H30B |
| 2600-2800 | 19 | 38 | **+450** | 562 | +0.80 | +0/−0 | LIVEC-H30/H30B |
| 2800-3000 | 14 | 28 | **+52** | 769 | +0.07 | +2/−0 | TOPB2 |
| 3000+ | 6 | 12 | **+2,888** | 1,191 | +2.42 | +1/−0 | TOPB2 |
| **ALL** | 152 | 304 | **+802** | 230 | **+3.48** | +20/−12 | |

Per leg: LIVE62 +644 (t +1.53) · LOSS10 +992 (t +1.69) · LIVEC-H30 +772 (t +1.77) ·
LIVEC-H30B +1,031 (t +2.37) · TOPB2 +903 (t +1.30). **B beats hr on all five legs.**

Slopes: pooled OLS **+36 coins per +100 rating (SE 65, t +0.56)**, Spearman ρ +0.044 (t +0.54).
TOPB2 dropped: +47 (t +0.54). Leg-level (n=5 legs, the only unconfounded between-band unit):
+20 (SE 22, t +0.93). Within-leg, where a leg spans ≥ 200 points: LIVE62 +86 (t +0.10),
LOSS10 −692 (t −0.73). **Flat everywhere.** Fitted line: +869 at 2550, +906 at 2650, +942 at 2750.

## 2. ES records − B, binned by opponent rating (19 records pooled)

| rating bin | boards | mean Δmargin | SE | t | win flips +/− | legs |
|---|---|---|---|---|---|---|
| <2200 | 1212 | −424 | 77 | −5.53 | +106/−74 (**+32**) | LIVE62, LOSS10 |
| 2200-2400 | 136 | −255 | 143 | −1.79 | +16/−6 (+10) | LOSS10 |
| 2400-2600 | 779 | −539 | 67 | −8.02 | +28/−116 (−88) | LIVEC |
| 2600-2800 | 361 | +49 | 120 | +0.41 | +2/−14 (−12) | LIVEC |
| 2800-3000 | 266 | −291 | 156 | −1.86 | +0/−15 (−15) | TOPB2 |
| 3000+ | 114 | **−2,991** | 318 | −9.41 | +2/−35 (−33) | TOPB2 |
| **ALL** | 2868 | −477 | 46 | −10.35 | +154/−260 (−106) | |

Per leg (board level): LIVE62 −400 (t −5.10) · LOSS10 −457 (t −3.49) · LIVEC-H30 −537 (t −7.03) ·
LIVEC-H30B −169 (t −1.83) · TOPB2 −1,101 (t −6.96). **Not monotone in rating** — the second-highest
band (H30B, mean 2594) is the *least* negative leg of the five.

| estimator | slope per +100 rating | SE | t |
|---|---|---|---|
| pooled board level | −42 | 13 | −3.28 |
| **pooled, TOPB2 dropped (1827-2682)** | **+16** | 17 | **+0.94** |
| record-level cells (n=93) | −59 | 14 | −4.07 |
| board level, record fixed effect | −42 | 13 | −3.29 |
| **board level, record × leg fixed effect (within-leg variation only)** | **−111** | 96 | **−1.16** |
| leg level (n=5 legs) | −59 | 41 | −1.43 |

The whole "gradient" is the TOPB2 leg, and inside TOPB2 it is three tapes: the within-leg slope is
−3,022/100 (t −7.78) over a 128-point span, leave-one-board-out swings it −3,769…−2,123, and dropping
the two worst boards (107460230 Otter Vibe @3032, mean record Δ −7,746; 107465299 SpaTaro @3081,
−3,643) leaves −1,611.

**What a win flip is worth on each leg** (a record's mean Δmargin regressed on its net game flips):

| leg | base win % | share of boards with abs(base margin) < 3,000 | board SD of Δ | coins per net flip | t |
|---|---|---|---|---|---|
| LIVE62 | 85.5 % | 0.26 | 2,692 | +62 | +3.18 |
| LOSS10 | 10.0 % | 0.30 | 1,704 | +154 | +2.18 |
| LIVEC-H30 | 63.3 % | 0.30 | 1,824 | +2 | +0.05 |
| LIVEC-H30B | 83.3 % | 0.20 | 2,206 | +85 | +2.99 |
| TOPB2 | 30.0 % | 0.35 | 3,082 | +89 | +1.19 |

A LIVE62 flip buys **62 coins**. Nine of 19 records gain net wins on LIVE62 — and **eight of those
nine have a NEGATIVE LIVE62 Δmargin** (pooled −400, t −5.10). The LIVE62 "gains" are near-tie coin
flips on the leg with the highest base win rate; the coins move the other way.

---

## The three answers

**(i) Does B − hr fall with opponent rating? No — it is flat and positive everywhere.**
Slope +36 coins per +100 rating (SE 65, t +0.56; Spearman ρ +0.044); leg-level +20 (t +0.93); no
within-leg slope anywhere. B leads hr on all five legs (+644…+1,031) and by +802 coins pooled
(SE 230, t +3.48). The fitted line predicts **+869 / +906 / +942 coins at 2550 / 2650 / 2750**, and
that is not an extrapolation: LIVE-C 43-102 already reaches 2682, and its **37 boards inside
2550-2750 give B − hr = +1,104 (SE 400, t +2.76)**. The premise of strategist item #1 — "nobody has
ever measured us at 2550-2750" — is false for the judge (it is true only of the Kaggle ladder, where
matchmaking caps the pool). **The incumbent and seed choices were not made on the wrong band.**

**(ii) "Records lose on TOPB2, gain on LIVE62" is a leg artefact plus one genuine top-tier
penalty — not a rating gradient.** Three reasons: (a) the leg means are not monotone in rating
(H30B at 2594 is the least negative leg of five); (b) with TOPB2 removed the slope over 1827-2682 is
+16 per 100 (t +0.94) — exactly zero — and the within-leg (record × leg FE) slope is −111 (t −1.16);
(c) the LIVE62 "gains" are win flips worth 62 coins each on a leg where the base already wins 85.5 %
and a quarter of boards sit inside ±3k, and 8 of the 9 gaining records have *negative* LIVE62 coins.
What is real is narrower and points the other way from the strategist's reading: records are
genuinely worse against the very top tapes (3000+ bin −2,991, t −9.41), concentrated on three
episodes. **That is a reason to keep the TOPB2 clause, not to demote it** — it is the only leg whose
signal is not a near-tie lottery (SD 3,082 per board but effect −1,101, t −6.96 on 380 rows).
Corollary for GATE-vs-LADDER (#2): the "TOPB2-refused, live-band-positive" records do not exist as a
class — of 19 records, **zero** gain net wins on TOPB2 and none has a positive Δmargin on both LIVE62
and TOPB2; uploading one would be uploading a record that is negative in coins on every leg.

**(iii) What NEXT30 should be expected to show.** Taking B − hr on our 60 boards between 2400 and
2800 as the prior (+901 coins, board SD 2,370): a fresh 30-board paired leg has SE ≈ 433, so the
expected t is **+2.08**, P(clear the pre-registered |t| ≥ 1.5 bar in B's favour) ≈ **0.72**,
P(the hr ≥ B verdict that would declare the judge band-dependent) ≈ **0.000**, P(inconclusive)
≈ 0.28. NEXT60: expected t +2.95, P(pass) 0.93. So NEXT30 is a ~72 %-power confirmation of something
four legs already say at t +3.48 — its main value is the 0.28 chance of an inconclusive read, which
would cost a day and change nothing. **Pre-commit to the extension to 60 before running it, or spend
the hours elsewhere.**

## Caveats

1. **Confounding.** Opponent identity, leg, board set, seat pairing and rating are one variable:
   each leg is one narrow rating band (spans 128–243 points). The pooled slope is therefore a
   five-point between-leg comparison dressed as n=152/2,868; the honest units are the leg-level
   regressions (n=5) and the within-leg slopes, both reported and both null for B − hr.
2. **Rating vintage.** TOPB2 ratings are the tape owner's *leaderboard score on 2026-09-10*, not the
   rating at episode time; LIVE-C and LIVE62 ratings are the opponent's `initialScore`/`updatedScore`
   in the episode that was cut (2026-09-10 and 2026-09-08/09 respectively); LOSS10 is `opp_rate` at
   cut time (2026-09-11). Ratings drift by tens of points a day, which blurs bins but cannot create
   the 1,000-point gaps between legs.
3. **LIVE62 is not perfectly held out**: 7 of its 62 ids are training rungs
   (`2026-09-09-judge-live55.md`). Dropping them cannot rescue the LIVE62 win-flip reading, which is
   contradicted by its own coins.
4. **The LOSS10 leg is loss-selected** (B's own ten ladder losses; base win rate 10 %), so its win
   flips are one-directional by construction — it is used here for its rating coverage (2175-2381),
   not as evidence of strength.
5. **19 records, one duplicate** (`flow210_g10_hr` = `flow210_g10p_hr`, identical csvs), and all 19
   are 10-200-gen records of six arms — a narrow, correlated sample of directions.
