# FERT_VOLUME on candidate B: the paired ENGINE judge

Agent, 75-min box, 2026-09-11.  Escalated by `docs/strategy/2026-09-11-fertcow-screen.md` §5
(consensus §53): the CPU sim screen put `FERT_VOLUME_ON` 2/1 above B on both frozen board files, and the
pre-registered answer to that was **exactly one paired engine judge, four legs vs B, on the shipped `hr`
composition — not a promotion**.  This is that judge.

## 1. Method

* **Theta is B in every game**: `artifacts/kagg2_games/thetas/flow193_g100_hr.npy` (candidate B, LIVE sub
  56161192).  **The switch string is the arm.**
* Base string (shipped `hr`): `OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True`.
* Arms: `fv_marg21` = BASE + `FERT_VOLUME_ON=True,FERT_VOLUME_MODE=marginal,FERT_VOLUME_NUM=2,FERT_VOLUME_DEN=1`;
  `fv_spot21` = the same with `FERT_VOLUME_MODE=spot`.
* Runner `S/fertcow/engine.sh` (adapted from `S/esm/sweep.sh` / `S/pump/sweep_b.sh`): the judge's own four leg
  runners under `fv_` names so the csvs never collide with the auto-judge's, on a **copy of the `arms-next`
  worktree** (`/root/wt_fertcow`, `cp -a`), constants moved by `S/drainpin/on2b.py` `setattr` — **no tree was
  edited, `git diff --stat -- src/` is empty.**  `WORKERS=5`, `JAX_PLATFORMS=cpu` (the 3070 is running the E3
  one-step sweep).
* None of the four runners takes the judge lock in its own header, so **each single runner call is wrapped in
  one `flock -w 1800 /root/kagg3_judge.lock`** (ext4, never nested, never around `S/autojudge/watch.sh`).
* Legs and their base csvs (all written under the same `hr` string, so the pairing is exact):
  TOPB2 40 games / 20 boards `S/lossflip/flow193_g100_hr_topb2.csv`; LIVEC-H30 (ids 43-72) 60/30 `_livech.csv`;
  LIVEC-H30B (ids 73-102) 60/30 `_livech2.csv`; LIVE62 124/62 `_live62.csv`.
  Pairing `.venv/bin/python S/bank/paired.py <base> <arm>`, ALL line, `t` on **boards** (seat-averaged).

NOTE on the flip columns: `W`/`L` count **games**, and every board is played from both seats; on these legs
the two mirrored games are byte-identical, so a board that changes side shows up as `2`.  The flipped-board
census below reads the csvs directly and reports **boards**.

## 2. Arm 1 — `fv_marg21` (mode `marginal`, 2/1)

`ALL` lines (`S/fertcow/engine.out`; cols `n winOFF winON d sd t dours dtheirs W L = boards t_rows`):

| leg | n | win OFF → ON | **Δmargin** | sd | **t (boards)** | Δ ours | Δ theirs | W/L/= | boards |
|---|---|---|---|---|---|---|---|---|---|
| TOPB2 | 40 | 32.5 % → 32.5 % | **+376** | 1,347 | **+1.37** | +196 | −180 | 0/0/0 | 20 |
| LIVEC-H30 (43-72) | 60 | 63.3 % → **66.7 %** | **+502** | 1,004 | **+2.77** | −109 | −611 | 2/0/0 | 30 |
| LIVEC-H30B (73-102) | 60 | 83.3 % → **80.0 %** | **+940** | 1,315 | **+3.97** | +363 | −577 | 0/2/2 | 30 |
| LIVE62 | 124 | 85.5 % → **87.1 %** | **+816** | 1,350 | **+4.81** | +282 | −534 | 2/0/0 | 62 |

**Flipped-board census** (csv diff, boards not games): TOPB2 none; LIVEC-H30 **+1 board won** (tape 107475310,
both seats, +376 us / −1,596 them); LIVEC-H30B **−1 board lost** (tape 107573857, both seats, −1,179 us /
−776 them); LIVE62 **+1 board won** (tape 107109832).  **Net +1 board over 142 boards.**

**Two-purse.** Every leg is denial-led: Δtheirs is −180 / −611 / −577 / −534 while Δours is +196 / −109 /
+363 / +282.  On LIVEC-H30 the whole gain is denial (our own purse is *down* 109 and we still gain 502 of
margin).  Board census (boards, not rows): **denial share |Δtheirs| / (|Δours| + |Δtheirs|) = 48 % TOPB2,
85 % LIVEC-H30, 61 % LIVEC-H30B, 65 % LIVE62**, with *their* purse down on 11/20, 27/30, 26/30 and 52/62
boards — broad, not a lottery.  Pooled over the 60 LIVE-C hold-out boards the split is **+127 ours / −594
theirs = 82 % denial**, i.e. **more** denial-led than the screen's 72 %, not less.  This is the same
fertilizer-pool mechanism the screen named: fertilizer has no town
drain, so units we do not burn on tiles are sold into the shared pool and walk the clone's quote down.

**Composition / `HIRE_ROW`.** The 2026-09-10 closure was specifically *"composed with `HIRE_ROW` it drops 3-4
live boards"*.  That effect is **reproduced but much smaller here**: exactly **one** LIVEC-H30B board is
dropped (83.3 % → 80.0 % on 30 boards), against **+1** on LIVEC-H30 and **+1** on LIVE62.  It is no longer a
3-4 board leak, but it is not zero, and it is the reason the largest-Δ leg is the one leg whose win rate falls.

**Pooled LIVE-C hold-out** (`S/fertcow/pool_livec.py`, the 60 boards the screen's `boards.json` actually
covers): `fv_marg21` **+721 coins/board, sd 1,166, t 4.79 — but wins EXACTLY level, 44/60 → 44/60.**

### Verdict, arm 1: **NOT PASS — strong positive that misses two clauses**

* Δmargin > 0 on **all four** legs ✓, three of them at t 2.8-4.8 ✓ — so this is emphatically **not LEVEL**.
* TOPB2 is **t 1.37 < 1.5** ✗ — the top tier still does not confirm it, exactly as the screen warned (fertcow-screen §5, caveat 3).
* LIVEC-H30B **loses 2 games = 1 board** (W 0 / L 2) ✗ under the literal "W < L by more than 1" rule; in the
  honest unit it is one board, and the net over all four legs is **+1 board**.

**Mechanism check (engine telemetry, per game vs B).**  `fv_marg21` plays **fewer moves** — −29.3 TOPB2,
−3.7 LIVEC-H30, −23.2 LIVEC-H30B, −9.4 LIVE62 — with `noops`, `quads` and `move_turns` unchanged and
**`unsold` flat (−1.2 … +0.1)**.  So the removed moves are FERTILIZE applications and the units they freed are
*sold*, not stranded in the shed.  That is the opposite of the `EARLY_SELL_MODE=B` failure mode logged at
14:17Z (unsold 7.7 → 90.4), and it is the direct engine confirmation of the screen's premise.

## 3. Arm 2 — `fv_spot21` (mode `spot`, 2/1)

| leg | n | win OFF → ON | **Δmargin** | sd | **t (boards)** | Δ ours | Δ theirs | W/L/= | boards |
|---|---|---|---|---|---|---|---|---|---|
| TOPB2 | 40 | 32.5 % → 32.5 % | **+466** | 1,952 | **+1.15** | +87 | −379 | 0/0/0 | 20 |
| LIVEC-H30 (43-72) | 60 | 63.3 % → **66.7 %** | **+397** | 1,145 | **+1.92** | −117 | −513 | 2/0/0 | 30 |
| LIVEC-H30B (73-102) | 60 | 83.3 % → 83.3 % | **+1,141** | 1,183 | **+5.32** | +479 | −662 | 2/2/0 | 30 |
| LIVE62 | 124 | 85.5 % → 85.5 % | **+836** | 1,234 | **+5.40** | +275 | −561 | 2/2/0 | 62 |

**Pooled LIVE-C hold-out (60 boards): +769, sd 1,205, t 4.94, wins 44/60 → 45/60 (+1 board).**

**Flipped-board census:** TOPB2 none; LIVEC-H30 **+1** (tape 107475310 — the same board arm 1 gains);
LIVEC-H30B **+1 / −1** (gains 107620742, loses **107573857 — the same board arm 1 loses**); LIVE62 +1/−1.
**Net +3 W / −2 L boards over 142.**  That one recurring casualty, 107573857, is mode-independent: it is the
`HIRE_ROW` composition leak of the 2026-09-10 closure, now down to a single hold-out board.

**Two-purse / mechanism:** denial share 81 % TOPB2, 81 % LIVEC-H30, 58 % LIVEC-H30B, 67 % LIVE62;
`dmoves` −28.8 / −10.3 / −22.6 / −14.4 per game with `unsold` flat (−1.2 … +0.8) — same signature as arm 1.

### Verdict, arm 2: **NOT PASS — the cleaner of the two arms**

* Δmargin > 0 on all four legs ✓, two of them at t 5.3-5.4 ✓; **no leg loses net flips** (0/0, 2/0, 2/2, 2/2) ✓;
  at least one LIVE-C leg at t ≥ 1.5 ✓ (both).
* **TOPB2 t 1.15 < 1.5** ✗ — the single clause it misses, and the same one arm 1 misses.
* Read the PASS rule as "Δ > 0 on all four *and* one LIVE-C leg at t ≥ 1.5 *and* no flip loss" (i.e. the
  t ≥ 1.5 requirement attaching only to the LIVE-C leg) and **`fv_spot21` passes and `fv_marg21` does not**.
  Under the strict reading (TOPB2 itself at t ≥ 1.5) **neither arm passes.**  Either way `spot` > `marginal`
  here, which **inverts the screen's ordering** (the screen put `marg21` ahead on LIVE-C win rate).

## 4. Screen vs engine

The CPU sim screen predicted **TOPB2 +378 (marg) / +441 (spot)** and **LIVE-C +901 / +941**.  The engine, on
the same boards, returns **TOPB2 +376 / +466** and **LIVE-C (60 hold-out boards pooled) +721 / +769**.

| family | arm | screen Δ | engine Δ | error | per-board sign agreement | Spearman |
|---|---|---|---|---|---|---|
| TOPB2 (20 tapes) | `marg21` | +378 | **+376** | **2 coins** | 19/20 | 0.92 |
| TOPB2 (20 tapes) | `spot21` | +441 | **+466** | 25 coins | 19/20 | 0.82 |
| LIVE-C (60 boards) | `marg21` | +901 | **+721** | −180 (−20 %) | 46/60 | 0.71 |
| LIVE-C (60 boards) | `spot21` | +941 | **+769** | −172 (−18 %) | 49/60 | 0.76 |

**The screen is right about the margin and wrong about the wins.**  On TOPB2 it reproduces the engine to 2 and
25 coins with 19/20 tapes agreeing in sign — the calibration published at 14:46Z (≤ 45 coins, ρ 0.94) holds on
a *switch* arm as well as on theta arms, which is new: nothing had yet tested the screen on a constant change
rather than a weight change.  On LIVE-C it is ~20 % optimistic in magnitude and noticeably weaker per board
(ρ 0.71-0.76, 46-49/60 signs), but the sign and the ordering of the two arms survive.  Where it **fails** is
the win rate: the screen showed LIVE-C **71.7 % → 78.3 % / 76.7 %** (88/32 boards), and the engine's own
hold-out win rate moves **44/60 → 44/60** (`marg21`, exactly level) and **44/60 → 45/60** (`spot21`, +1
board).  The screen's headline "wins are NOT level here — that is what differs from the 2026-09-10 read"
(fertcow-screen §4) **does not survive the engine**: the wins *are* level, and the 2026-09-10 denial signature
— margin up, wins level, opponent's purse doing the work — is exactly what the engine reproduces.  Use of the
screen is unchanged: rank and refuse, never promote.

## 5. What to do with it

1. **Do not promote on this evidence.**  Both arms are **denial-led** (58-85 % of every leg's Δ is the
   opponent's purse falling) against **open-loop pinned tapes that cannot re-time their fertilizer sales**.
   The memory rule `counterfactuals-overstate` / the two-purse rule says exactly this class of edge does not
   transfer to a reactive opponent — and the ladder band we are trying to beat is the open-loop clone, so it
   *should* transfer to them, but the **top tier (TOPB2) is the family that decides above 2,800 and it is
   t 1.15-1.37, i.e. unconfirmed** for the third time (2026-09-09 +636 t 1.50, 2026-09-10 level on TOPB,
   today +376/+466).
2. **The 2026-09-10 closure is downgraded, not overturned.**  "Composed with `HIRE_ROW` it drops 3-4 live
   boards" is now **one** board (107573857) on 142, and that board is lost by both modes.  The reason to keep
   the switch closed as a *package* candidate is therefore no longer the board leak — it is the flat TOPB2.
3. **If it is escalated again, escalate `fv_spot21`, not `fv_marg21`** (bigger pooled LIVE-C, bigger LIVE62,
   no leg losing flips), and escalate it as a **second seed on TOPB2 only** — 20 boards at sd 1,952 is the
   whole of the uncertainty, and a second TOPB2 seed costs ~4 minutes of judge lock.  That is the single
   cheapest experiment that would move either arm across the bar.
4. Nothing here changes the live submission: candidate B ships unchanged (sub 56161192).

## 6. Provenance

* Runner `S/fertcow/engine.sh`, pooling helper `S/fertcow/pool_livec.py`, raw ALL lines `S/fertcow/engine.out`.
* Per-game rows `S/lossflip/fv_{marg21,spot21}_{topb2,livech,livech2,live62}.csv`; leg logs
  `S/topb2/fv_*.log`, `S/livec/fv_*_holdout*.log`, `S/live62/fv_*.log`.
* Worktree copy `/root/wt_fertcow` (`cp -a` of `.claude/worktrees/arms-next`, HEAD 45f8217).
* **No `src/` change** (`git diff --stat -- src/` empty), no GPU (the 3070 is on `S/onestep`), `WORKERS=5`,
  `JAX_PLATFORMS=cpu`.  **No VOID line on any pairing; minimum `moves` per row 2,729-2,767**, so no arm hit
  the refused-switch trap logged at 14:17Z.
* Verdict lines appended to `S/glut/verdicts.log` (`FERTVOL-ENGINE fv_marg21`, `FERTVOL-ENGINE fv_spot21`).
