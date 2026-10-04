# PIPELINE — the operator manual

## Training protocol (read first, 2026-09-27)
Enforced laws, arm table, per-upload re-sync checklist: **docs/TRAINING-PROTOCOL.md**. Trainers run only on
master src and tune only shipped parameter files. STATUS: `bash S/pipeline/stage_check.sh` (TREE PASS = on master).
PACKAGE: `python scripts/package_submission.py --out <path>` defaults to the shipped theta + head + ESWORK theta [PKGFIX1];
pass `--theta` / `--residual` only for the file a candidate changes.

Every script here wraps a tool that already produced a number in the ledger.

## 0. Start here — day one, in order

```bash
cd /mnt/e/_work/kaggriculture3
bash S/pipeline/00_env.sh                          # 1. can the box run?  ~1 min, any FAIL: fix first
bash S/pipeline/11_train_status.sh flow250_clone   # 2. what are the trainers doing?  read-only
bash S/pipeline/11_train_status.sh flow249_clone   #    (the PPO run's log is read by hand -- §2)
CYCLES=4 GENS=15 WHERE=remote FITNESS=clone WORKERS=4 bash S/pipeline/loop.sh   # 3. start and leave
bash S/pipeline/40_livewatch.sh                    # 4. has the ladder moved under us?  every few h
# 5. ONLY when loop.sh stops with *** SHIP BAR PASSED ***:
bash S/pipeline/30_ship.sh S/pipeline/SHIP-READY.npy <run>   # builds + smokes; never uploads
#    then UPLOAD TWICE back to back  <- the two-slot law, §4
#    then bash S/pipeline/35_buildstory.sh <LABEL> "<verdict>"
#    then edit tests/_pin.py: SHIPPED = <the ff commit of the ship tree>
#    then bash S/ship/sync_master.sh <ship-commit> <tarball> <sub-id>
```

`loop.sh` runs unattended and stops on its own when a candidate clears the ship
bar, because uploading is a human step. To look in: `11_train_status.sh <run>`
and `column -t -s $'\t' S/pipeline/ledger.tsv`. Weekly, or when `40_livewatch.sh`
shows a new top-10 id or ENGINE-class losses: `05_refresh_opponents.sh 10`.

## 1. State of play (2026-09-19, 11:15Z)

Two live submissions: **56421514** (`res940_vpost`: res940 +
`MELONVETO_POST_ON`) and **56370365** (res940). This is the live A/B; the two
packages differ only by that switch. **56335778** theta-only was replaced and
is inactive.

**What wins.** The ESR body (OPEN_PUMP + TAIL_FILL + BANK_BEFORE_LOT + HIRE_ROW
+ the ENDROUTE/ENDROUTE2/SPLIT/ROW2 family), the FT2 fertilizer engine (§115b,
+2,845), WIDE_PICK and WIDE_PICK_FREE (POOLED278 +117 t 3.14), the herd.
**What loses**: (a) melon first-mover rent, a flat tax on d0 melon boards — our
own melon plate pays the rival +15.4k in price; (b) the high-band tail — vs
≥2,700 seats we are −11.3k on PRICE and −11.6k on VOLUME, all d10-19, because we
under-request (hires, seed, wheat). Roster-and-ask, not schedule.
**Closed axes** — no reopening without a new mechanism; each has a dated doc in
`docs/strategy/` and a `BUILD-STORY.md` entry: sell timing (day, hour, order,
spread, projection, lot depth, terminal days) · plan/board selection · opening
imitation (MIRROROPEN −15,335, SCRIPTOPEN −16,182) · crop mix and tile
reallocation (CARROTBID −7,208) · herd-first splits · early-ramp planting ×1.5 ·
forward hiring · idle ops · pump window and the third d29 row · fertilizer denial
· ES-from-FT2 on every mask (ESJUDGE 4-10) · head-only ES (ALPHAFARM4) ·
rollout/MPC planning · the d0 melon plate vs a reactive seat (MELONGENES1) ·
per-day sale quotas (SELLSPREAD1) · a goose floor (GEESE1) · `WHEAT_LATE_ASK`
(WHEATLATE1). PPO action-RL is ACTIONRL1's explicit NO-GO, overridden by the
USER and now running as `flow251_ppo` — no read is claimed.

### THE HEAD LAW (verified 2026-09-19 against the code and a real tarball smoke)

**The macro head lives ONLY in the alphafarm tree.** `git grep -ln mw2 -- src/`
on master is **EMPTY**; on `.claude/worktrees/alphafarm` it hits `core/policy.py`
(`("mw2", …)` in `SHAPES`) and `core/brain.py` (`macro_delta`). master's packaged
planner cannot read a head — it has no code that could. **The REALES line trains
that head**: `10_train_remote.sh` / `10b_train_local.sh` launch
`S/reales/reales_clone.py` with `--coords mw2,mb2`, and `coord_index()` masks
`PO.offset()` over the four contiguous groups **mw1@7692 mb1@9036 mw2@9052
mb2@9260** — 221 floats at 9,052..9,273. Everything outside the mask, the
package theta at 0..7,691 included, is **structurally frozen**: a REALES centre's
first 7,692 floats ARE the shipped theta, and never move on this line.

**So shipping a REALES win means shipping the alphafarm tree.** `30_ship.sh`
routes on length automatically — ≤ 7,692 → master, 9,273 → `$AF` — and that is a
**layout move**, not a packaging step: `N_PARAMS`, `tests/_pin.py`'s SHIPPED ref
and the ES baseline (`BASE=ship7692`) move together, so the script prints that
checklist whenever the layout differs from master's. A centre whose body prefix
equals the shipped theta **and** whose `mw2`/`mb2` are zero is inert either way
(`macro_delta` is exactly `0.0`): `30_ship.sh` refuses to build it for upload,
and allows it under `DRY=1` as the documented coin-exact self-test.

**Open axes.** (1) **REALES on the 221 `mw2,mb2` coords**, the line `loop.sh`
drives: trainer `reales_clone.py`, LIVE V48 clone in the opponent seat, TRAIN
`S/melongenes/hiband28_ids.txt` / HOLD `hiband28b_ids.txt`, `--assert-base
89.3,6762,101271` (g0 must reproduce the MELONGENES1 base to the coin or the run
is void), start centre `$AF/S/heades/centre9273.npy`; the tape trainer
`reales.py` is **legacy** (CLONEES1: −245/board vs the clone). (2) **Residual
action-RL**, merged into master behind `plan.RESIDUAL_ON` (OFF, byte-identical,
20 tests), runbook `60_actionrl.md`.

## 2. Open runs — do not disturb

| run | where | pid | log | stop rule |
|---|---|---|---|---|
| `flow249_clone` | LOCAL, 8 workers, from 09:20Z | **91616** | `.claude/worktrees/alphafarm/S/reales/flow249_clone/log.tsv` (+ `stdout.log`) | two cycles with no accept, or `hold_d ≤ 0` once hold has been read twice |
| `flow250_clone` | REMOTE `user@remote-host`, `~/stage_clone`, 8 workers, from 10:00Z | **1791886** | `~/stage_clone/S/reales/flow250_clone/log.tsv` | same |
| `flow251_ppo` | LOCAL, from `.claude/worktrees/actionrl` | **9267** | `.claude/worktrees/actionrl/S/actionrl/flow251_ppo/log.tsv` | **by update 500** (~32 k games, ~4 h): if the argmax head has not left the no-op — `hist` no-op column still ~100 %, or an `N=56` gate coin-identical to `ship7692` — STOP |

Both REALES runs print `[clonees] BASE CHECK … PASS` at g0, so the two boxes are
CRN-comparable; a generation is ~15 min remote, ~33 min local, and the box will
not take a third trainer. `11_train_status.sh <run>` reads any of them without
touching anything (for `flow251_ppo` it finds the pid but not the log).

**What a positive result looks like.** *REALES* `log.tsv` is `gen secs
train_mean_d train_best_d trial_d accept cum_train_d cwin twin dwin hold_d
hold_dtheirs head_l2 sigma games`; the two columns that matter are **`hold_d`
> 0** (held-out margin, read at g1 then every 5 gens, `+nan` on the gens that
did not read it) and **`cwin` rising** (clone-seat wins out of the 28-board
panel). `train_*` overfits, and a frozen centre reprints its own `hold_d` — not
a second measurement. **Buy a judge leg only when `hold_d` > 0 AND the centre
md5 moved.** *PPO* `log.tsv` is `update games mean_reward win_rate mean_margin
entropy loss vloss sec hist`: the head must **leave the no-op** (`hist` = 18
`;`-separated per-slot histograms, each no-op column falling off ~100 %) **and
`win_rate` must rise** with it; `mean_margin` is the honest coin number
(`mean_reward` mixes in the ±1 win) and `vloss` / stdout's `V|sd` say whether
the GAE baseline is alive. A head that never leaves the frozen planner has
learned nothing; one that left it everywhere is entropy-collapsed. **Never
`kill $(pgrep -f X)`** — it matches the shell running it and kills your own
session (exit 144); read a literal PID above and type `kill <n>`.

## 3. The steps, with the decision rule for each

The last column is what the step has been **run** as; UNVERIFIED = read and
reasoned about, never executed end to end, so its first run is an experiment.

| script | what it does | the decision it feeds | state (2026-09-19) |
|---|---|---|---|
| `00_env.sh` | venv, JAX, both layouts (master 7,692 / alphafarm 9,273), ssh, package md5, `tests/_pin.py` SHIPPED ref, git clean | any FAIL: fix before starting | **VERIFIED** 10:32Z — 8 PASS, 0 FAIL, counted the 2 live remote REALES |
| `05_refresh_opponents.sh [N]` | ladder + our episodes → pick ≥2,700 opponents the panel lacks → replays → tapes → `LEGS=fresh` | a band we lose hard and did not carry = a NEW class | **VERIFIED END TO END** 10:22-10:30Z — 5 boards (2,804-2,864) cut and verified, registry 941 → 946, `LEGS=fresh` banked `S/lossflip/ship7692_fresh.csv`. Found one bug: the banking label must be `ship7692` |
| `10_train_remote.sh <run> <centre> [σ] [floor]` | stages the self-contained clone tree to the remote and launches REALES exactly as `2026-09-19-reales5.md` did | ~15 min/gen | **VERIFIED** 10:24Z `DRYRUN=1` (line matches flow250's launch field for field) and 10:26Z `SMOKE=1` (real 1-board probe on the host: centre wins 1/1 train, 1/1 hold). The rsync half is UNVERIFIED **by choice** — it will not stage over a live run |
| `10b_train_local.sh` | the same on this box, 8 workers | only when the box is otherwise idle | **VERIFIED `DRYRUN=1`** 10:58Z. Had a real bug: the two-run cap counted `ps -eo args` matches and hit its own wrapper, refusing every invocation; it now filters on `comm`. A live launch is UNVERIFIED **by choice** — flow249 owns the cores |
| `11_train_status.sh <run>` | `log.tsv` tail, the `hold_d` column, checkpoints, literal kill PIDs | **buy a judge leg only when `hold_d` > 0 AND the centre md5 moved** | **VERIFIED** 10:25-10:31Z on both live runs. Had a real bug — the PID list matched the `ssh` wrapper that launched the remote run, so "TO KILL" offered you your own session |
| `20_judge.sh <label> <centre>` | POOLED278 + BAND2 → POOLED511, plus HIBAND, all vs `ship7692` | prints the bar, exits non-zero on REJECT | **VERIFIED (reader chain)** 10:52-10:57Z — `SMOKE=2` ran the whole three-leg path and both reports and `verdict.py`; read `POOLED511 +0 t +nan`, the documented tie-to-the-coin self-test. The **full 511-board** read is still **UNVERIFIED** (~90 min, box loaded) |
| `25_clone_leg.sh <label> <theta>` | the same boards with the LIVE V48 clone answering back | mandatory for anything touching the opening or the book | **VERIFIED** 10:22-10:41Z — base rows banked (56 boards, 112 rows), then the Δ path on a 12-id prefix. Had a hard bug: it padded a 9,273 centre with master's `pad_theta.py`; it now pads with `$TREE`'s own |
| `26_selfplay_leg.sh <label> <theta>` | the current best PACKAGE seated live as the opponent | regression check only, never a rating forecast | **VERIFIED** (previous session, `S/pipeline/logs/selfsmoke*.self.log`); not re-run since |
| `30_ship.sh <theta> <label>` | routes the tree by layout, builds `dist/…tar.gz`, smokes it, prints the layout-move checklist + pin + BUILD-STORY + upload steps | the upload itself is yours | **VERIFIED `DRY=1`** 11:07-11:12Z on **both routes after the merges**: 7,692 theta → master, 24 files, md5 `377f4a72`; 9,273 centre → auto-routed to `$AF`, 24 files, md5 `68a519cd`, `N_PARAMS 9273` inside the archive. Both smoke **720 steps / 0 bad on both seeds at 184,456 / 129,457** — the shipped coins to the unit. The inert-centre refusal and the layout checklist both fire |
| `35_buildstory.sh <LABEL> "<verdict>"` | appends the `## LABEL` paragraph to `BUILD-STORY.md` and the row to `S/buildstory/index.tsv` (prose on stdin) | the standing rule: EVERY ship and EVERY reject | **VERIFIED** — it wrote this session's own entries |
| `40_livewatch.sh` | fetch → rows → an → getrep → d2gate | has the ladder moved under us? | **PARTLY VERIFIED** — `an.py`'s rewrite is VERIFIED (trajectories are `_traj(sub, rows)`, re-run it reproduces 56329775 at 2,857.7 over 165 games). The full wrapper is UNVERIFIED — `getrep.py` pulls ~32 MB per new loss |
| `50_new_switch.md` | how to add a free float and judge it | read before touching `src/` | doc |
| `60_actionrl.md` | the residual-head lane, **merged into master** 2026-09-19 | a USER-authorised override of ACTIONRL1's NO-GO | **RUNNING, NOT READ** — `flow251_ppo` is in flight; the branch proved the identity head is coin-exact through the package, and **no positive read is claimed**. The gate has never been run from master |

**The bars.** `20_judge.sh` ends with a `--- SHIP BAR on POOLED511 ---` block
and a `VERDICT:`. **SHIP bar**: `Δtheirs ≤ 0` **and** pooled `t ≥ 3` **and** net
board flips `> 0`. **PROMOTE bar** (internal to the loop; a centre is not an
upload): `Δtheirs ≤ 0`, `t ≥ 2`, net flips `≥ 0`. `30_ship.sh` must show **720 steps / 0 bad** on both seeds, and at the shipped
centre the coins are **seed 20260821 → 184,456** and **seed 7 → 129,457**
(`theirs` is 3,000 both times: the smoke's opponent is `pass`). If it does not,
do not upload. Rehearse with `DRY=1 OUT=<scratch>/x.tar.gz`. `20_judge.sh
SMOKE=<n>` prints leg names reading `POOLED278`/`POOLED511` — the BASE pool
size, not the board count; the `bds` column is what paired.

**GATE2 (proposed 2026-09-27; docs/strategy/2026-09-27-gate2.md).** It replaces the per-leg flip bar of TRAINING-PROTOCOL §1.7 once the user adopts it. Until then §1.7 is the operative bar.

**Legs.** Every leg is paired per board against the live package:
- BAND: the 142 banked band seats; grow to ≥ 284 with both seats, then BANDBANK2.
- dev100, held100, FRESH300, tapes50, faithful59.

**Metric.** Soft win w(m) = 1/(1+e^(−m/3000)) of the margin m = ours − theirs; Δw = w(arm) − w(base). Both seats of one tape or bed opponent form one cluster.

**PASS iff all three hold:**
1. Either branch:
   - **A.** BAND family soft Δθ (the BANDLEG1 Part C family formula fed per-family mean Δw) ≥ 1.96 × SE, the SE from a seat bootstrap within family.
   - **B.** Pooled soft-win t ≥ 2 over all legs, BAND included, and BAND family soft Δθ ≥ 0.
2. Guard: no leg with n ≥ 20 has soft-win t ≤ −2.
3. Gift rule: not (Δtheirs t ≥ +2 and soft-win t < 2), both pooled over the reacting legs dev/held/FRESH/pool.

Hard flips, hard family Δθ and Δmargin are reported with bootstrap SE and have no threshold.

**Operating characteristics** (power model, BAND142 / 284):

| arm | BAND142 | BAND284 |
|---|---|---|
| null | 0.038 | 0.044 |
| true +2 flips/100 on every leg | 0.93 | 0.97 |
| +2 on BAND only | 0.42 | 0.61 (0.76 at 426) |

The old flip bar gives null 0.016 and +2/100 0.34.

**How to run it.**
1. Write the candidate's pairs as `S/gate2/pairs/<ARM>__<leg>.tsv`. The header is `key ours_b theirs_b ours_a theirs_a [fam]`, with leg ∈ dev held fresh tapes faithful band bed pool. BAND keys are the BANDLEG1 labels, so fam is filled automatically.
2. Run `python3 S/gate2/rescore.py > S/gate2/rescore.txt`. The arm's row carries the GATE2 verdict.

A `*` verdict means no BAND rows, so the arm is not shippable until BAND has been run.

**Ship note: KERNEL2 candidates + JUDGEALL1 (2026-09-28).** Full GATE2 for any KERNEL2-style switch string in one command:
`bash S/judgeall1/judgeall.sh <label> <worktree> "<switches>" 3` -> `S/judgeall1/runs/<label>/judge.md` (9 legs, A/B/guard/gift; `JA_CONTINUE=1` resumes).
A whitelist variant of a judged run is re-scored without games: `bash S/v3branch1/run.sh rescore` (v3 row = v2 row iff the rival's real h1 is listed).
Candidates, both GATE2 PASS, NOT uploaded: v3 `dist/vrp15_k2fire.tar.gz` md5 1929f224 (FIRE_CASH=26|29|2338|2438, band +22, recommended) and
v2 `dist/vrp14_k2real.tar.gz` md5 233430d3 (ZERO_CASH exclusion, band +43). Upload at most ONE (FIFO): docs/strategy/2026-09-28-decision-brief.md.

**§ BAND3 / per-seat.** Run `LEG=band3 N=120 gate.sh`, then
`report_band3.py <cand> a8_940b3` and `report_perseat.py <cand> <base> <leg>`.
Incumbent labels are `a8_257_940b2` / `a8_940b3`; head-off labels are
`ship7692b2` / `ship7692b3`.

**§ Exact-seed live replay.** `S/band3/dl.sh` writes each downloaded
`info.seed` to `<EPSEAT>.seeds` as `episode seed`.  Pass an ids file containing
`episode seed` rows to `S/actionrl/gate.sh`, set `SEEDS_SOURCE` to a separate
sidecar, or leave the downloader sidecar next to `IDS_SOURCE`; the gate carries
it to `judge.sh`, which uses `eval_vs_baselines.py --seed-file` in place of the
synthetic `--seed-per-opponent` ladder.  Seeds are joined by episode id, so
reordering or selecting ids cannot silently attach one board's seed to another.
Example: `IDS_SOURCE=S/band3/live32_epseat.txt SEEDS_SOURCE=S/band3/live32_epseat.txt.seeds N=32 LEG=band3 ... gate.sh <head>`.

## 4. Rules of the road

**TWO-PURSE RULE.** Only paired runs count and both purses are read: an arm that
adds coins to our purse and more to theirs is a gift — hence Δtheirs in every
report. **A TAPE CANNOT RE-PLAN**: the same arm read +10,448 against a board's
recording and −15,451 against the exact V48 clone on the same pinned town, so
anything moving the opening or the order book is judged on `25_clone_leg.sh`.
**MARGIN IS NOT RATING.** The ladder is Bradley-Terry over board WINS: a pooled
margin at t 2.5 with net flips +1 at signp 1.000 bought nothing, and a flip
census on 278 boards can invert on the next 233 — check both cells.
**σ FLOOR LAW.** Always pass `--sigma-floor`; flow245 inherited the 0.01 default
and spent seven generations unable to take the shorter step. **WORKERS**: at most
two worker processes on this box, `JAX_PLATFORMS=cpu` always (the GPU is shared),
and the remote host caps at two REALES runs.
**PYTHONPATH LAW.** `PYTHONPATH=<tree>/src`, the tree being the one whose
`policy.N_PARAMS` matches the theta (master 7,692, alphafarm 9,273). `tree_for`
in `_common.sh` is the router; `20_judge.sh` and `30_ship.sh` use it and print
the tree they picked. The action-RL lane **inverts** this: never set
`PYTHONPATH` there — `KAGG3_SRC` goes to `sys.path[0]`.
**NEVER `pytest -q tests`** — it OOMs the box. Named files only, and
`tests/_pin.py` has no test functions: run the files that import it. **MASTER =
the latest upload + production code**, kept true after an upload by
`bash S/ship/sync_master.sh <ship-commit> <tarball> <sub-id>`; never a bare
`git stash`. **BUILD-STORY at every ship AND every reject** — an unrecorded
reject gets re-explored. **THE TWO-SLOT LAW**: Kaggle keeps only the newest two
submissions active, so uploading one retires the older — today 56329775, our
best agent at 2,858. Upload twice back-to-back, or hold.

## 5. Troubleshooting

**`GetEpisodeReplay` 404** — dead. Replays come from
`kaggleusercontent.com/episodes/<id>.json` (~32 MB), which `S/livewatch8/getrep.py`
and `S/hiband/dl.sh` use; `ListEpisodes` and `GetLeaderboard` (competitionId
147734) still work, credential-free. **"where is the hiband report?"** — in the
tree `judge.sh` ran in, `<tree>/S/winjudge/logs/<label>.report.log`, which for a
9,273 centre is the alphafarm worktree; leg CSVs always land in the shared
`S/lossflip/` (why labels pool across trees) and `20_judge.sh` tees copies into
`S/pipeline/logs/`.
**A packaged opponent scores exactly 3,000** — its starting purse: it never
acted. `main.py` does `sys.path.insert(0, dirname(abspath(__file__)))`, `abspath`
does not resolve symlinks, so symlinking only `main.py` puts an empty dir on
`sys.path`. Symlink the whole package directory; `26_selfplay_leg.sh` exits 3 on
that signature. Related: `eval_vs_baselines.py` hides this repo's `kagg3` for one
game, so TWO packaged agents share that slot and the second runs the first's
planner — rename `kagg3` inside the second package.
**A rebuild does not reproduce the shipped md5** — expected and measured: the
same theta from HEAD gives a different md5 and the **identical coins**, because
HEAD carries OFF/zero module defaults the ship tree did not (`HERD_TILT`,
`WHEAT_LATE_ASK`, `GEESE_TARGET`, `RESIDUAL_ON`, …). **Judge a rebuild by the
smoke coins, never the md5**; `git archive <ship commit> src` reproduces a past
package exactly.
**`REFUSE: theta is 9273 long, this tree's layout is 7692`** — the padder was
master's, the tree is alphafarm's; both checkouts have `pad_theta.py` and each
refuses a theta longer than its own `N_PARAMS`, so call
`$TREE/S/winjudge/pad_theta.py`. **A paired report printing `t +nan` and `+0/-0`
flips** means the two thetas play the board identically, so every difference and
the standard error are zero: a tie to the coin, and the self-test of the padded
shipped centre, of `loop.sh`'s reduced cycle and of `26_selfplay_leg.sh`.
**Base rows for a leg are missing** — every report opens
`S/lossflip/<BASE>_<leg>.csv` with `BASE=ship7692`, so a base is banked by
running `judge.sh` under the label **`ship7692`**; `ship7692_fresh` lands at
`ship7692_fresh_fresh.csv` and the pairing silently reports no base. **"TOWN
REGISTRY MISSING" / "TAPE MISSING"** — the id is not pinned and an unpinned id
must not be judged (WINRATE2 law): rebuild the leg with
`05_refresh_opponents.sh`, or drop the id.

**The reduced cycle** trains nothing and judges an existing centre, exercising
the centre pick, judge, verdict, promote, SHIP-READY and the ledger row in
~15 min. `IDS_HIBAND` must be a **prefix** of `hiband_ids.txt`, because
`--seed-per-opponent` draws seed(board i) from the id's position: a prefix keeps
the banked base's seeds, a reordering is a different board set.
```
CYCLES=1 JUDGE_ONLY=.claude/worktrees/alphafarm/S/heades/centre9273.npy \
  LEGS_ONLY=hiband IDS_HIBAND=$PWD/S/pipeline/logs/hiband12_ids.txt \
  CLONE=0 SELF=0 WORKERS=2 bash S/pipeline/loop.sh
```
