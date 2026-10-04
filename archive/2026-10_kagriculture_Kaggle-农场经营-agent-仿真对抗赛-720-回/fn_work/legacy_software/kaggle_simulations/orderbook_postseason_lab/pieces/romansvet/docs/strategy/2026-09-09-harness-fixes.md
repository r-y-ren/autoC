# Harness fixes — seat-grouped t, and the judge's stale/silent gate

2026-09-09. Fixes for `docs/strategy/2026-09-09-lottery-audit.md` §4.1 (every published t inflated
1.40×) and §4.4 (the judge's two live bugs). Scope: the measurement harness under
**S** = `/tmp/claude-0/-mnt-e--work-kaggriculture3/8b388b22-9a4b-4bf0-8e3e-dc4aac1d5f04/scratchpad`.
No repo code changed. Backups of the three edited files sit beside them as `*.bak_rowt`,
`*.bak_m1`, `*.bak_append`.

## 1. `S/bank/paired.py` — the t is now computed on boards, not rows

The rows are `(seed, opponent, seat)` and every board is played from both seats, so the row count is
twice the number of independent boards and the mirrored games are near-duplicates (seat-identical on
72/96, 205/320, 45/64, 215/328 of the judge legs). `stats()` divided by `sqrt(rows)`.

* `stats(rows, boards)` now takes a parallel list of board keys `(seed, opponent)`, averages the two
  seats' paired deltas into one observation per board, and computes mean/sd/SE/t over those boards —
  the same rule as the trainer's `paired_stats(group_seats=True)`
  (`.claude/worktrees/arms-next/src/kagg3/es/train.py:1625`), which is the reference implementation.
* The printed `t` column is now the **grouped** t: the decision statistic.
* Two columns are **appended at the end of the line**: `boards` (the n the t is computed on) and
  `t_rows` — the old row-level t, kept only so log lines written before today stay comparable. Two
  legend lines below the table label it `t_rows (inflated)`.
* Every pre-existing column keeps its position, width and meaning (`n` is still the paired *row*
  count, `sd` is still the row-level spread), so `grep '^ALL'` / `grep '^tape'` in `S/spo/measure.sh`,
  `S/legs/legs.sh`, `S/judge/judge.sh`, `S/bundles/screen.sh` and the monitors still parse. Line
  length grows ~15 chars to ≈138, still inside `S/ablation/run_all.sh`'s `cut -c1-160`.
* `stats(rows)` with no board list falls back to the old row-level statistic in both fields, so any
  other caller of the module keeps working.

### Verification — `t_rows` reproduces every logged value, `t` = `t_rows` / ~1.40

| leg (candidate vs g350 refs) | rows | boards | t_rows (= the logged value) | t (grouped) | ratio |
|---|---|---|---|---|---|
| flow156_g20 band6@777001 | 192 | 96 | −2.12 | **−1.50** | 1.41 |
| flow156_g20 top10@777001 | 640 | 320 | −4.05 | **−2.90** | 1.40 |
| flow156_g20 band6@777002 | 192 | 96 | −1.49 | **−1.06** | 1.41 |
| flow156_g20 flood6@777001 | 192 | 96 | −2.53 | **−1.83** | 1.38 |
| flow156_g20 jesse4@777001 | 128 | 64 | −5.72 | **−4.05** | 1.41 |
| flow156_g20 today41@777001 | 656 | 328 | −2.09 | **−1.50** | 1.39 |
| flow150_g40 band6@777001 | 192 | 96 | −2.14 | **−1.51** | 1.42 |
| flow150_g40 top10@777001 | 640 | 320 | −4.52 | **−3.23** | 1.40 |
| flow150_g40 jesse4@777001 | 128 | 64 | −4.28 | **−3.03** | 1.41 |
| flow150_g40 today41@777001 | 656 | 328 | −2.54 | **−1.81** | 1.40 |

The `t_rows` column reproduces `S/judge/flow156_g20_legs/summary.txt` and the audit's §4.1 table to
the last digit, and the grouped column reproduces the audit's board-level recomputation. Ratio
1.38–1.42 everywhere, i.e. ≈√2 — as expected when the seats are near-duplicates.

## 2. `S/judge/judge.sh` + `S/lossflip/run.sh` — stale reads and silent rejections

**BUG A (stale line).** `run.sh` appended to `$name.summary` for ever and `judge.sh` read it with
`grep -m1` — the *oldest* block. Fixes:

* `run.sh` now truncates `$name.summary` per invocation, after copying whatever was there into a new
  append-only history log `$name.summary.history` (prefixed `== superseded <UTC>`). The file the
  monitors watch (`$name.summary`, still ending `LEGSDONE`) and every other file name are unchanged.
* `judge.sh` reads the **last** `^LEG20:` line (`| tail -1`), and the same for `HELD-OUT`, so a stale
  block cannot be read even if some other caller appends.

**BUG B (silent reject).** A regex miss produced an empty `leg20`/`hdm`, which the gate treated as
"reject" and reported as `LEGS SKIPPED (… NA …)`. Fixes:

* No `^LEG20:` line at all → `GATE ERROR: no LEG20 line in <summary> … legs NOT run, nothing decided`
  on stdout and in `<name>.txt`, then `exit 2`.
* A `^LEG20:` line that does not parse → `GATE ERROR: LEG20 line did not parse (d-margin='' H_dm='')`
  plus the offending line, then `exit 2`.
* `JUDGEDONE` is still written before either error exit, so `until grep -q JUDGEDONE` monitors
  (e.g. `S/melonpin/run_small.sh:3`) terminate instead of hanging on a failed judge.

Tested on crafted summaries (no simulations) in `S/harnessfix_test`, since removed:

| case | summary | old behaviour | new behaviour |
|---|---|---|---|
| stale + fresh block | LEG20 −1243 … then LEG20 +500 / H_dm +10 | reads −1243 → LEGS SKIPPED | reads +500 → legs run, exit 0 |
| no LEG20 line | LEGFAILED only | `d-margin NA` → LEGS SKIPPED, exit 0 | GATE ERROR, exit 2 |
| reformatted LEG20 | `LEG20: dmargin=+500` | `NA` → LEGS SKIPPED, exit 0 | GATE ERROR (line quoted), exit 2 |
| fresh block negative | LEG20 −181 / H_dm −300 | LEGS SKIPPED | LEGS SKIPPED (unchanged), exit 0 |

The historical instance the audit points at, `S/judge/flow156_g20.txt:15-23`, is BUG B rather than
BUG A: `S/lossflip/flow156_g20.summary` contains **no** `LEG20:` line at all (the block was written
by a `flips.py` predating LEG20), so the gate printed `LEG20 d-margin NA` and skipped the legs
silently. Under the new judge that run stops with `GATE ERROR` instead of reading as a rejection.
The legs were later run by hand, which is where `S/judge/flow156_g20_legs/` came from.

## 3. Verdict-log re-read — calls decided on 1.7 ≤ |t| < 3.0 in the last three days

48 lines of `S/glut/verdicts.log` from `:453` (2026-09-07 00:15Z) onward quote a t in that band.
Below are the ones where the csvs still exist and the number is load-bearing. `t_rows` reproduces the
logged value exactly in **every** row, which is the check that these recomputations are of the same
comparison. **No decision has been changed** — this is the list, for the operator.

### 3a. Calls that no longer clear |t| ≥ 2 grouped

| log line | call | statistic as logged | grouped t | does the decision still stand? |
|---|---|---|---|---|
| `:835` | **crew-ramp 11-by-d11 on g350 REJECTED**, "crew-ramp family stays CLOSED" | band6@777001 −2,153 **t −2.1** | **−1.51** | **No supporting statistic left.** This was the *only* leg. The rejection now rests on a null that cannot exclude ±2.9k/game. The displacement signature (ours −3,303 vs theirs −1,150) is unaffected, but "REJECTED" should read "not measured". |
| `:1066`, `:1068` | flow156_g20 **not promoted** | band6 **t −2.1**, flood6 **t −2.5**, today41 t −2.09 | **−1.50**, **−1.83**, **−1.50** | **Yes** — carried by top10 −2.90 and jesse4 −4.05, both still significant, and by five of six legs pointing the same way. |
| `:994`, `:1004` | flow150_g40 **not promoted**, "JUDGE CLOSED" | band6 **t −2.1**, today41 **t −2.5** | **−1.51**, **−1.81** | **Yes** — top10 −3.23 and jesse4 −3.03 survive. |
| `:962` | flow149_pend_g106 "REJECT stands on six of six legs" | today41 +1,296 **t 2.6** (margin up, wins down) | **1.86** | **Yes, and more cleanly** — the number that *contradicted* the reject is the one that fails; the reject was on win rate. |
| `:880` | PINNED LADDER: "flow130_g260 −932 **t −2.2**" vs g350 | 120 rows / 60 boards | **−1.56** | Ladder conclusion (every theta loses ≥92 % of the 30 live-loss games) is unaffected; the *ordering* claim g350 > g260 on margin is no longer significant. flow129_g100 −9.21 → **−6.51**, still overwhelming. |
| `:844` | STREAM top4rep: "Mengfei Li +6.2k **t 2.3**", pooled "**t 2.35**" | 48 / 192 rows | **1.64**, **1.73** | Rung weights were set on the *win rates*, which are unchanged; the two t's quoted as evidence do not clear 2. Matthew Huang 6.47 → **4.55** survives. |
| `:851` | STREAM loss3b: xiongrui666 **t 1.9**, Panos-2150 **t 2.2** | 48 rows each | **1.30**, **1.52** | Pooled 4.93 → **3.48** survives, so the 2100-band conclusion stands; the per-tape numbers do not. |
| `:693` | flow135_g200 "first candidate to beat gen-260 on the pooled margin significantly" | today41 h2h +6.9 pts **t 2.5** | **1.81** | **Yes** — the pooled h2h 3.56 → **2.57** still clears 2. The *leg-level* claim does not. |
| `:644` | flow133_g100 **LEVEL, not promoted** | top10 **t 2.2**, flood **t −2.0** | **1.61**, **−1.43** | **Yes, reinforced** — "level" gets more level (pooled 0.88 → 0.64). |
| `:660` | flow135_g40 **LEVEL, not promoted** | pooled h2h +595 **t 2.0**, band +5.2 pts **t 2.5**, top10 **t 2.0** | **1.46**, **1.81**, **1.42** | **Yes, reinforced.** |
| `:796` | flow138_g200 **not promoted** | flood leg **t −2.5** | **−1.75** | **Yes** — the call was made on the −1.9-pt win rate with a pooled margin t of 0.35 → **0.25**; it is a "level, not promoted", not a refutation. |
| `:731`, `:733` | flow137_g10 **not promoted** | h2h vs g200 +595 **t 1.8** (already under 2) | **1.31** | **Yes** — h2h vs g350 −1.35 → **−0.97**; the call was g350 stays. |
| `:485` | KNOB SWEEP "ADMIT_PICK_SHARED … jesse4 holds +135 **t 1.7**" | CRN sim | not recomputed | already under 2 as logged; see §4. |

### 3b. Calls in the band whose decision is carried by a much larger statistic (survive unchanged)

`:500 :506 :512 :515 :523 :531 :536 :539 :540 :546 :547 :555 :557 :562 :563 :569 :575 :585 :586
:589 :613 :615` — the flow128→flow130 promotion chain. Every individual leg t quoted there
(2.1–2.9) drops to 1.5–2.1, but each promotion was decided on a pooled 1,904-board read at
**t 4.1–17.3**. Spot-checked on the csvs: the flow130 g260-vs-g130 head-to-head (`:615`, logged
t 3.3) is **t_rows 3.31 → grouped 2.39**, and g260 vs LIVE on the four legs whose LIVE refs are still
on disk (1,120 rows / 560 boards) is **t_rows 12.38 → grouped 8.85**. Every promotion in the chain
survives. `:465` reads the *trainer's* gate, which already groups seats (`paired_stats`, audit §2.2)
— unaffected.

### 3c. Rule of thumb for reading the old log

Any `t` in a log line written before 2026-09-09 that came from `S/bank/paired.py` should be divided
by **1.40**. A logged **t 2.8 is the new t 2.0**; everything logged between **1.7 and 2.8 no longer
clears a two-sigma bar**. Combined with the audit's §4.2 finding (band6 and jesse4 are lotteries as
accept/reject legs at any t), the only single-leg reads that can still carry a verdict are top10 and
today41, and only for effects ≥ ~2k/game.

## 4. Not verified

* The **CRN sim** comparator behind `S/knobsweep` and `S/rescreen` (log lines `:473`, `:485`, and the
  parked/dead knob verdicts at `:513`, `:528`, `:599`) was not audited. `screen_sw2.py:101-104`
  builds its boards over `(tape, seed, seat)`, so the same seat-doubling is present in the data; its
  t is printed by a different tool than `S/bank/paired.py` and was left untouched. **Those sim t's
  are likely inflated by the same ~1.40× and should be rechecked before any of them is quoted.**
* `S/oppaware/paired.py`, `S/idlefill/paired.py` and `S/tail_care/paired.py` are separate copies with
  the same row-level defect. They were out of scope and are unchanged; `S/prestock2/run.sh:10` and
  `S/tailfill2/run.sh:10` gate on `$5` of `tail_care/paired.py`'s last line (a margin, not a t), so
  they are unaffected by the fix either way.
* Verdict-log lines whose csvs no longer exist on disk (mostly the pre-`--seed-per-opponent` era the
  audit already voids in §3.3) were not recomputed.
* Nothing was re-run: no simulation, no leg, no judge. Every number above comes from csvs already on
  disk.
