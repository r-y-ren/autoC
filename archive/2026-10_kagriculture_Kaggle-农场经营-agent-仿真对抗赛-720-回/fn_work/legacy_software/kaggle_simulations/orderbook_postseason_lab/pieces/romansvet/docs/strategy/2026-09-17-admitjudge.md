# ADMITJUDGE — POOLED180 on ADMIT_SLACK_ON over the shipped FT2 package

2026-09-16 22:11–22:50Z, branch `admitjudge` off master `6b81daf`, one frozen
worktree `/mnt/e/_work/kaggriculture3-admitjudge` for BOTH arms, theta
`flow193_g100_hr.npy`, WORKERS=3. Judge of `2026-09-17-admitslack.md` (ENG22
kill gate pooled **+357 se 138 t +2.59**, V45 null). No training, no upload.

## 1. VERDICT — §115b REJECT

`ADMIT_SLACK_ON` does not survive the 169-board promotion band. The ENG22
signal (+357, t 2.59, 44 engine-tape games) does **not** transfer: on the judge
band the increment over FT2 is **+41/board, t +0.78** — a null, an order of
magnitude under the +450 bar and a quarter of the ENG22 effect. The
in-band-48 subset (tiers A–D, opponents ≥ 2300) is **negative**.

| leg | boards | rows | Δ margin | sd | se | t | W | L | net |
|---|---|---|---|---|---|---|---|---|---|
| LIVEC-H30 | 30 | 60 | +97 | 385 | 70 | +1.38 | 0 | 0 | +0 |
| LIVEC-H30B | 30 | 60 | −64 | 522 | 95 | −0.67 | 0 | 0 | +0 |
| NEXT30 | 30 | 60 | +182 | 779 | 142 | +1.28 | 0 | 2 | −2 |
| **POOLED BAND (90)** | 90 | 180 | **+72** | 587 | 62 | **+1.15** | 0 | 2 | −2 |
| **BAND180** | 79 | 158 | **+6** | 784 | 88 | **+0.07** | 0 | 0 | +0 |
| **POOLED180** | **169** | **338** | **+41** | 685 | **53** | **+0.78** | 0 | 2 | **−2** |
| of which in-band | 48 | 96 | −63 | 738 | 107 | −0.59 | 0 | 0 | +0 |

Bar: Δ ≥ +450 **and** t ≥ 3.00 on the increment. **REJECT** (+41 / t 0.78).

## 2. Two purses and the win rate

`S/admitjudge/purses.py` splits the paired margin over all 338 rows:

| | n | Δ | se | t |
|---|---|---|---|---|
| OUR purse | 338 | **+21.1** | 35.8 | +0.59 |
| THEIR purse | 338 | **−19.7** | 13.8 | −1.43 |

Board win rate **85.2 % → 84.6 %**, flips **0 W / 2 L**. The *sign* of the
ENG22 finding survives — the lever still takes marginally more off the other
seat than it adds to ours (theirs is the larger |t|) — but at ~1/8 the ENG22
size on either purse, it buys nothing against the clone band. This is the
ENG22-vs-band split seen all campaign: the admission budget binds against the
fertilizer ENGINE class, not against the open-loop clones that make up the
judge band, and the promotion statistic is the clone band.

## 3. Tree check — OFF-identity holds

```
diff <(tail -n +2 S/lossflip/ft2_band180.csv) <(tail -n +2 S/lossflip/as_ft2_band180.csv)
```
**silent, 0 differing rows.** The FT2 arm re-cut on `6b81daf` reproduces the
`9a9c435` shipped-package band180 csv byte for byte: master's module defaults
have NOT drifted from the shipped package across ROUTEEFF / EVESTOCK /
ROUTEORDER / ADMITSLACK (all merged OFF), and the `as_ft2` re-cut is a clean
control rather than a second baseline.

## 4. Disposition

`ADMIT_SLACK_ON` stays **False** (module default). The switch is correct and
its mechanism is measured on both ends (`2026-09-17-admitslack.md` §2); it is
simply not worth coins against this band. The ADMISSION family's remaining
value is the ENG22-only read, so the family is CLOSED at §115b like the rest
of the dawn family. The next volume channel remains the block ASSIGNMENT
(`_cut`, ROUTEORDER §5) — the 86 % of `mid_move` no visiting-order change can
reach.

## 5. Repro

```
bash S/admitjudge/run_all.sh                       # WORKERS=3, ~39 min, log S/admitjudge/logs/ENG
.venv/bin/python S/pumpclip/incr.py as_on as_ft2   # the §115b increment table
.venv/bin/python S/admitjudge/purses.py as_on as_ft2
```
Labels: `as_on` = FT2 + `ADMIT_SLACK_ON=True`, `as_ft2` = FT2. Csvs in
`S/lossflip/` (gitignored).
