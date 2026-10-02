# AUTOJUDGE-WIRE — the watcher and the audit now know the 8th family and the 7,065 tree

Built 2026-09-14 11:58–12:20Z from `master` HEAD **d9b0ddb**. Closes the two gaps listed as
caveats in `docs/strategy/2026-09-14-judge7065.md` §6 (audit has 7 families, watcher still points
at the 6,789 tree with a 4-item switch string). Nothing was committed — the lead commits.

**Not started.** No watcher was launched; no leg longer than 90 s was run. The start commands are
in §5, unexecuted.

---

## 1. What changed

### `S/autojudge/audit_candidate.py` (8th family, informational)

| line | change |
|---|---|
| `:20-25` | `BASE_FAMILIES` gains `("TOPB3R9", "topb3r9_{name}.csv", "topb3r9_B.csv", None, 9)` — same 5-tuple shape as the other seven (label, candidate csv fmt, base csv relative to `S/lossflip`, id subset, expected boards). 9 boards = 18 rows. |
| `:27-29` | new `INFORMATIONAL = ("TOPB3R9",)` — the only member. |
| `:83` | family order comment; the assembly `(*BASE_FAMILIES[:5], next_row, *BASE_FAMILIES[5:])` is unchanged and now yields TOPB2, LIVEC-H30, LIVEC-H30B, LIVE62, LOSS10, NEXT30, NEXTHIGH, **TOPB3R9** — the same order as `S/judge7065/judge_candidate.sh:56-63`. |
| `:92-98` | an informational family prints `PASS INFO …` / `INFO-SKIP <reason>` and **never sets `failed`**, so the exit code is bit-for-bit what it was for every label judged before the family existed. LOSS10 / NEXTHIGH keep their old hard-failure semantics — only TOPB3R9 is informational. |

The §115 pooled band is computed in `S/judge7065/pooled_band.py`, which already listed TOPB3R9
under `INFO` (`pooled_band.py:42-46`); `audit_candidate.py` has no promotion logic at all, so
there was nothing to veto-proof beyond the exit code.

### `S/autojudge/watch.sh` (7,065 tree by default, 8th leg, subset mode)

| line | change |
|---|---|
| `:17-25` | USAGE/ENV header for `LEGS_ONLY`, `JUDGE_TREE`, `JUDGE_SWITCHES`. |
| `:60-63` | header paragraph: TOPB3R9 is the 8th leg and is INFORMATIONAL like LOSS10/NEXT30/NEXTHIGH. |
| `:74`, `:76` | `V=${AJ_VERDICTS:-…}`, `GLUT=${AJ_GLUT:-…}` — like the existing `AJ_LOCK`, they keep a dry run off the live ledgers. Defaults unchanged. |
| `:94-97` | `AJ_ARMS="<arm> <stage>;<arm> <stage>"` overrides the hard-coded `ARMS` array for one launch, so a new arm needs no edit of the file. Unset = the file's list. |
| `:99-106` | `KEEPCAND_STAGES` + `keeps_cands()`. The record path used to be the literal test `stage = stage_hr` (`:640`, `:669`); flow214/flow215 run out of `~/stage_flow214` / `~/stage_flow215` **with `--keep-candidates`**, so that test would have sent them down `judge_one` → `best_abs.npy` = the seat (memory *autojudge --judge defect*, the 2026-09-11 flow200 g30 incident). Default list = `stage_hr stage_flow214 stage_flow215`; anything else keeps the old ACCEPT-only `best_abs.npy` path, so no existing arm changes. |
| `:145-149` | `BASEB_TOPB3R9=$S/lossflip/topb3r9_B.csv` — the family's only base (no `hr` run exists, so the column is always "vs B", like LOSS10's). |
| `:158-183` | the judge tree/switches are now **parameters with judge-7065 defaults** (§2). |
| `:186-198` | `worktree_for` / `switches_for`: `6789|7020|7065` → `$JUDGE_TREE` / `$JUDGE_SWITCHES`; `6954` → its own pair (that layout is not a prefix of 7,065). |
| `:213-218` | `leg_enabled()` + `LEGS_ONLY` — the watch.sh twin of `judge_candidate.sh --only`. |
| `:363` | a `LEGS_ONLY` run always enters the leg section (`rerun=1`) and logs the subset. |
| `:371,375,380,385,390,405,420,433` | each of the 8 legs is now `if ! leg_enabled <FAM>; then log skip; elif <old condition>; then …` — the old condition, and therefore the old behaviour with `LEGS_ONLY` unset, is untouched. |
| `:425-437` | **the TOPB3R9 leg**, after NEXTHIGH, exactly as `2026-09-14-topb3r9-leg.md` §5 specifies: skip test = row count, `rm -f` the stale csv, `WORKERS=$WORKERS bash $S/topb3/run_r9.sh "$name" "$wt" "$th" "$sw"`, failure = one FAILED line. |
| `:466-479` | the TOPB3R9 column: one `TOPB3R9 (vs B)` line, one `TOPB3R9 retention` line (`S/topb3/retention.py` — a candidate that hires differently desyncs a tape B kept), and its own `AUTOJUDGE-TOPB3R9` line in `S/glut/verdicts.log`, shaped like LOSS10's. The `AUTOJUDGE` / `AUTOJUDGE-vsB` lines are **not** touched. |

**Gate/promotion logic is unchanged.** `judged_already()` still means the four paired legs; the
`case "$a_topb2$a_livec$a_livech2$a_live62" in *FAILED*` return at the end of `run_legs` still
reads only those four; no branch anywhere reads the TOPB3R9 result.

**Lock discipline.** The TOPB3R9 leg runs inside the same `flock 9` the caller already holds
(`:643`, `:650`, `:669`, `:670`); `S/topb3/run_r9.sh` takes no lock of its own (`grep -n flock` on all four
informational runners: nothing), so there is no nested flock — the 2026-09-10 deadlock cannot
recur. Lock file is still `${AJ_LOCK:-/root/kagg3_judge.lock}`, on ext4.

Backup of the pre-wire file: `S/autojudge/watch.sh.bak_20260914T120121Z_prewire`.

## 2. The env defaults

| var | default | notes |
|---|---|---|
| `JUDGE_TREE` | `.claude/worktrees/judge-7065` | the tree `judge_candidate.sh:22` uses |
| `JUDGE_SWITCHES` | `OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True,brain.MELON_GENE_ON=True,brain.CROP_DAY_ON=True` | byte-equal to `judge_candidate.sh:23` |
| `JUDGE_TREE_6954` / `JUDGE_SWITCHES_6954` | `slope-repair` + the `brain.PLANT_FLOOR_ON` string | the old 6,954 pair, unchanged |
| `KEEPCAND_STAGES` | `stage_hr stage_flow214 stage_flow215` | stages judged from `cands/gNNNNN_record.npy` |
| `AJ_ARMS` | unset (= the `ARMS` array in the file) | `"flow215 stage_flow215;flow214 stage_flow214"` |
| `LEGS_ONLY` | unset (= all 8 legs) | `TOPB2 LIVEC LIVEC-H30B LIVE62 LOSS10 NEXT30 NEXTHIGH TOPB3R9` |
| `AJ_LOCK` / `AJ_VERDICTS` / `AJ_GLUT` | `/root/kagg3_judge.lock`, `S/autojudge/verdicts.txt`, `S/glut/verdicts.log` | a dry run overrides all three |

For a **6,789** theta the two gene slots are zero by construction (`policy.unpack` zero-pads
anything shorter than `N_PARAMS`, `policy.py:582`), so the ON branches add `exp(0)=1` / `+0.0` for
*any* 6,789 candidate, not just B — the switch string needs no per-arm branching. What does change
for a 6,789 arm is the **tree**: judge-7065 is HEAD `1d4e7e8`, arms-next is older. Cross-tree
identity is demonstrated on two full legs (TOPB3R9 and LOSS10, `2026-09-14-judge7065.md` §3, plus
§3.4 below), and every switch added since is default-off; if the lead wants a 6,789 arm judged in
the old tree anyway, export the pair:

    JUDGE_TREE=/mnt/e/_work/kaggriculture3/.claude/worktrees/arms-next \
    JUDGE_SWITCHES=OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True \
    bash S/autojudge/watch.sh --legs <name> <theta.npy>

## 3. Receipts (all dry, all ≤ 90 s)

**3.1 `bash -n`** — `S/autojudge/watch.sh`, `S/topb3/run_r9.sh`, `S/judge7065/judge_candidate.sh`:
all clean. `S/autojudge/test_audit_candidate.py`: **7 passed**.

**3.2 audit output is unchanged except the new row.** `HEAD:S/autojudge/audit_candidate.py` vs the
edited file, same label, same cwd:

| label | old rows / rc | new rows / rc |
|---|---|---|
| `crop_mix_C_seed313` (7 csvs, no topb3r9) | 7 PASS lines, **rc 0** | the *same 7 lines byte for byte* + `TOPB3R9      INFO-SKIP missing …/topb3r9_crop_mix_C_seed313.csv (informational leg: not counted, no veto)`, **rc 0** |
| `flow193_g100_hr` (4 csvs) | 4 PASS + 3 FAIL, **rc 1** | same 7 lines + `TOPB3R9 INFO-SKIP …`, **rc 1** |
| `B7065id` (loss10 + topb3r9 only) | 1 PASS + 6 FAIL, **rc 1** | same 7 lines + `TOPB3R9      PASS INFO rows=18 boards=9 ours=+0 theirs=+0 margin=+0 t=+nan flips=0/0 ident=18`, **rc 1** |

The informational row never moves the exit code: rc is identical in all three.

**3.3 width → tree/switches, through the new `watch.sh`** (`LEGSOFF=1 … --legs`, ~1 s each, on a
test lock and test verdict file):

    wiretest_flow193_g100_hr_pad7065  (7065 params) -> worktree .../judge-7065, switches …,brain.MELON_GENE_ON=True,brain.CROP_DAY_ON=True
    wiretest_flow193_g100_hr_pad7020  (7020 params) -> worktree .../judge-7065, switches …,brain.MELON_GENE_ON=True,brain.CROP_DAY_ON=True
    wiretest_flow193_g100_hr          (6789 params) -> worktree .../judge-7065, switches …,brain.MELON_GENE_ON=True,brain.CROP_DAY_ON=True
    wiretest_oldpath (JUDGE_TREE/JUDGE_SWITCHES exported, 6789) -> worktree .../arms-next, switches OPEN_PUMP_ON=True,TAIL_FILL_ON=True,BANK_BEFORE_LOT_ON=True,HIRE_ROW_ON=True

The 7,020 file is not padded (`policy.unpack` zero-pads; `2026-09-14-judge7065.md` §4).

**3.4 IDENTITY — one real leg through the new path, 90 s.**

    WORKERS=4 LEGS_ONLY=TOPB3R9 AJ_LOCK=/root/kagg3_judge_wire.lock AJ_VERDICTS=… AJ_GLUT=… \
      bash S/autojudge/watch.sh --legs B7065wire artifacts/kagg2_games/thetas/flow193_g100_hr_pad7065.npy

    12:05:01Z B7065wire theta …/flow193_g100_hr_pad7065.npy (7065 params) -> worktree …/judge-7065, switches …
    12:05:01Z B7065wire LEGS_ONLY=TOPB3R9 -- subset run, only these legs are started
    12:05:01Z B7065wire TOPB2/LIVEC/LIVEC-H30B/LIVE62/LOSS10/NEXT30/NEXTHIGH skip (LEGS_ONLY)
    12:06:30Z B7065wire TOPB3R9 (vs B) ALL 18 22.2% 22.2% 0 0 nan 0 0 0 0 18 9 nan
    12:06:31Z B7065wire TOPB3R9 retention … RETAINED(>=0.85) boards 9 games 18 win 22.2% mean margin -7139 sd 13324 t -1.61 | PAIRED on 9 fidelity-retained boards: d/board +0 sd 0 t +nan

    md5  8292fb275cd1b44b09c8d6518204a882  S/lossflip/topb3r9_B.csv
    md5  8292fb275cd1b44b09c8d6518204a882  S/lossflip/topb3r9_B7065wire.csv     <- diff EMPTY

The leg's own log `S/topb3/logs_r9/B7065wire.log` shows `set kagg3.core.brain MELON_GENE_ON True`
/ `CROP_DAY_ON True` and `plan: …/.claude/worktrees/judge-7065/src/kagg3/core/plan.py`, i.e. the
watcher really used the new tree and the new switch string. `audit_candidate.py B7065wire` then
prints `TOPB3R9 PASS INFO rows=18 boards=9 … ident=18`. This is the §3 identity of
`2026-09-14-judge7065.md` reproduced *through `watch.sh`* instead of by hand.

**3.5 command equality with `judge_candidate.sh`.** For a `flow214_*` / `flow215_*` label the
watcher's 8 invocations are the same commands as `judge_candidate.sh:56-63`: `run_legs` picks
`livec/run_holdout.sh` + `run_holdout2.sh` (the `flow2[0-9][0-9]*` case at `:341`), `NEXT30` with
`FIRST=0 IDS=$S/nextband/ids.txt` (the `flow211|flow212|flow213` exception does not match), and
`topb3/run_r9.sh "$name" "$wt" "$th" "$sw"` last. Only the wrappers differ (`WORKERS=…` prefix vs
`env WORKERS=…`), and both pass identical `$wt` / `$sw`.

**3.6 `AJ_ARMS` / `keeps_cands` unit check** (the two snippets, run standalone):
`AJ_ARMS="flow215 stage_flow215;flow214 stage_flow214"` → `ARMS[0]="flow215 stage_flow215"`,
`ARMS[1]="flow214 stage_flow214"`, count 2. `keeps_cands`: `stage_hr`, `stage_flow214`,
`stage_flow215` → record path; `stage_leg20`, `stage_flow21` → `best_abs` path (no prefix
false-positive).

## 4. Files touched

* `S/autojudge/audit_candidate.py` (+13 lines)
* `S/autojudge/watch.sh` (+70 lines; backup `…/watch.sh.bak_20260914T120121Z_prewire`)
* `docs/strategy/2026-09-14-autojudge-wire.md` (this file)
* receipt artifact: `S/lossflip/topb3r9_B7065wire.csv` (byte-identical to `topb3r9_B.csv`),
  `S/topb3/logs_r9/B7065wire.log`

Nothing under `src/`, `scripts/`, `tests/`, `S/macro_exec/`, `S/rebuy/`, `S/turns/`,
`S/judge7065/` was touched.

## 5. Starting the watcher (NOT started)

No watcher is running (`S/autojudge/watch.pid` holds a stale 56453; `ps` shows no `watch.sh`).
Both arms are `--keep-candidates`, so each record is judged from `cands/gNNNNN_record.npy`
automatically ~7 min after it lands.

Both arms, one watcher (WORKERS=8, ~35-45 min of legs per record):

    cd /mnt/e/_work/kaggriculture3 && \
    AJ_ARMS="flow215 stage_flow215;flow214 stage_flow214" \
    nohup setsid bash S/autojudge/watch.sh >> S/autojudge/watch.out 2>&1 &

flow215 only:

    cd /mnt/e/_work/kaggriculture3 && \
    AJ_ARMS="flow215 stage_flow215" \
    nohup setsid bash S/autojudge/watch.sh >> S/autojudge/watch.out 2>&1 &

flow214 only:

    cd /mnt/e/_work/kaggriculture3 && \
    AJ_ARMS="flow214 stage_flow214" \
    nohup setsid bash S/autojudge/watch.sh >> S/autojudge/watch.out 2>&1 &

Judging one theta already on disk (no ssh at all), e.g. a fetched flow215 candidate:

    nohup setsid bash S/autojudge/watch.sh --legs flow215_g100_hr \
      /mnt/e/_work/kaggriculture3/artifacts/kagg2_games/thetas/flow215/real_gate_cand.npy &

Killing it (unchanged): `P=$(cat S/autojudge/watch.pid); kill -TERM -$P`.

## 6. Caveats

* The watcher's own arm list in the file still names the retired flow187…flow213 arms; `AJ_ARMS`
  is the intended way in, and it does not persist across launches. If flow214/flow215 become the
  standing arms, the lead should replace the `ARMS` array (`watch.sh:66-80`).
* `--judge <arm> <gen> <stage>` now takes the record path for the two new stages as well, which is
  the correct fetch for them, but the 2026-09-11 warning still stands for any stage **not** in
  `KEEPCAND_STAGES`: it fetches `best_abs.npy`, which for a keep-candidates arm is the seat.
* `LEGS_ONLY` bypasses the `judged_already` skip on purpose (a subset run is explicit). It does not
  delete existing csvs except the one the named leg is about to rewrite.
* Every arm — including the 6,789 ones still in the `ARMS` array — now judges in the judge-7065
  tree by default. That is deliberate (one tree for all widths), and the identity evidence is two
  byte-identical legs; a leg-by-leg identity sweep across all eight families was not run.
* The TOPB3R9 retention line is logged, not gated: a board under 0.85 retention under the candidate
  is unreadable, and the judge still has to look at it by eye (as `judge_candidate.sh` does).
