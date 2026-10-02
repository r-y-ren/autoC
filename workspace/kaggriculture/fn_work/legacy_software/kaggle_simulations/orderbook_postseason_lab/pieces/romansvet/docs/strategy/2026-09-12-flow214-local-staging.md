# flow214 — flow213's recipe staged on the local RTX 3070 (2026-09-12)

Staged, **not launched**. `S/flow214/launch_flow214.sh` + `S/flow214/precheck.sh` +
`S/flow214/README.md`. The coordinator launches; the one-line command is at the bottom.

## 1. Recipe — flow213, unchanged

Seed theta candidate **B** (`artifacts/kagg2_games/thetas/flow193_g100_hr.npy`, md5 `7fcf3948`,
byte-identical to `submission/theta.npy`). Band-only objective: the 85-tape w2 floor, LIVEC42 w4,
**BAND40 w4**, NEXT30 w10.2, the 39 top-ten/LOSS10/TOP50 ids at 0 — 236 pinned rungs against
`--episodes 240` (236 × 1 episode + 4 carried for self-play). `--train-only gp,dh,ds,g5,gb5,b1`,
i.e. the **press head w3/b3 pinned** (§117): measured in the staged tree,
`train_mask × live_mask` = **1,126** trained genes of 5,997 live (the pre-pin list
`gp,dh,ds,g5,gb5,w3,b3,b1` gives 1,191, matching flow213's header). sgd, lr 1.8e-4, sigma 0.01,
wd 4e-7, `--restart-sigma-on-stall 150`, `--arch-frac 0.9`, `--margin-scale 3000`,
`--pinned-once --pinned-fixed-seed --shop-crn`, `--real-gate-every 100` over the same 62
opponents, `--keep-candidates`, `--seed 309` — the same CRN draw as flow209/211/212/213.

The press-pin edit **had** landed in `S/flow213/launch_flow213.sh` at the time of derivation
(file mtime 2026-09-12T07:14Z), so flow214 carries the pinned list, not the older one.

## 2. The tree (why a new one was needed)

`S/localarm/tree` was already byte-identical to the host `~/stage_hr` in `scripts/train.py`
(`c8c22fb8`) and `src/kagg3/es/train.py` (`c9325713`, the leg-family gate) — but its
`src/kagg3/core/plan.py` was `6c7b7fe6` (master), **missing the seed-room switch**, while the host
has `790d53ed`. Per-file md5 over all 65 `.py` in `src/` + `scripts/`: that one file was the only
difference (the rest of the diff was locale sort order).

`/root/tree_local214` = a copy of `S/localarm/tree` + `S/seedroom/plan.patch` (`patch -p3`, four
hunks at offset +26) + `SEED_ROOM_PURSE_ON = True`. The result hashes **`790d53ed`** — the host's
byte-for-byte. So a flow214 record decodes exactly like a flow211/212/213 record and the shared
judge legs mean the same thing. The launcher refuses to start if either hash drifts
(`STRICT_TREE=1`).

## 3. Memory arithmetic for 8 GB

Card: 8,192 MiB, ~740 MiB permanently held by the Windows-side ollama/Xwayland contexts.

Measured on this card (`S/localarm/gpumem_8192.log`, the flow189 dry runs): the evaluator holds
**two chunk-sized buffers at ~256 KiB/row** — the log steps by two clean +2,048 MiB jumps at
`--chunk 8192` — so

```
JAX ≈ 680 MiB base + 2 × chunk × 256 KiB
  chunk 8192 → 4,776 MiB  (observed: 6,059 MiB total incl. ollama, "JAX ~4.88 GB")   → flow189 DIED at the abs probe
  chunk 4096 → 2,728 MiB  (ran flow194/flow198 for days)                              → CHOSEN
```

The abs probe is **one unsplit jit call** of `2 × abs_pairs × rungs` rows
(`src/kagg3/es/train.py:5511`, `limit = max(chunk, total)` — `--chunk` cannot split the base
block, which is exactly the chunk-independent OOM flow189 hit):

```
rungs = 236 tapes + 4 archetypes      = 240
abs_pairs 32 → 2 × 32 × 240 = 15,360 rows ≈ 3,840 MiB   ← chosen
abs_pairs 45 (flow213, 24 GB card)   = 21,600 rows ≈ 5,400 MiB   → does not fit here
abs_pairs 24 (fallback)              = 11,520 rows ≈ 2,880 MiB
peak during the probe ≈ 740 (ollama) + 680 (JAX base) + 3,840 = 5,260 MiB of 8,192
```

A live reading refines the base: a 2026-09-12T04:5xZ smoke of this exact argument list sat at
**2,122 MiB total** (≈1,380 MiB of JAX) once the 236 rung tables were resident, before any eval
chunk. Redo the sum with the measured base: main loop 740 + 1,380 + 2,048 = **4,168 MiB**, probe
peak 740 + 1,380 + 3,840 = **5,960 MiB** of 8,192 — ~2.2 GB of headroom, and the arithmetic that
would have failed is `--abs-pairs 45` (740 + 1,380 + 5,400 = 7,520, i.e. inside the driver's own
overhead). The precheck prints the measured peak from a 5 s `nvidia-smi` sampler.

The peak only holds if the main loop's buffers are handed back before the probe, which is what
`XLA_PYTHON_CLIENT_ALLOCATOR=platform` (+ `PREALLOCATE=false`) does — the same pair that made
flow198 survive this probe at 9,664 rows. `XLA_PYTHON_CLIENT_MEM_FRACTION=0.78` is set as the cap
that binds only if someone drops back to the BFC allocator (0.78 × 8,192 = 6,390 MiB).
`ABS_PAIRS=24` is the documented fallback if the probe ever OOMs.

**pop is not memory-bound.** The pop-dependent state is the perturbation block, pop × d =
2048 × 6,789 × 4 B = **53 MiB** (d = 6,789 from the theta file). pop is bound by wall clock:

| | rows/gen | s/gen on this card (780 rows/s) |
|---|---|---|
| pop 1024 | 245,760 | ~315 s (5.3 min) |
| **pop 2048 (chosen)** | **491,520** | **~630 s (10.5 min)** |
| pop 4096 (remote) | 983,040 | ~1,260 s (21 min) |

780 rows/s is measured, not assumed: flow198 ran 512 × 160 = 81,920 rows in 105 s/gen at
`--chunk 4096` on this card. The often-quoted "local is 3-4× slower" is wrong — the flow198 header
measured **1.85×** at an identical shape (101.5 s local vs 55 s on an idle 3090), and the two
remote arms currently log **690-717 s/gen** (pop 4096 × 200) because they share the box. So
**pop 2048 gives the local arm the same ~10.5 min/gen cadence as flow211/flow212**, at half their
population (P/(P+d_train) = 2048/3174 = 0.65 of the remote's 0.78, §72's dimension limit).
Gen 1 additionally carries the XLA compile (~430 s on this card, flow198 gen 1 443 s), and the
gen-0 gate leg ~210 s. `POP=1024` is the env override if a g10 read is wanted inside the hour.

Reads: g10 at ~1 h 55 m, g20 at ~3 h 40 m, g30 at ~5 h 25 m after launch.

## 4. Tapes and the town registry

All **236** pinned-town tapes exist locally in `artifacts/tape_actions_town/` (0 missing), as do
all 62 `--real-gate-opponent` packages.

Registry coverage of the 236 rungs + 62 gate opponents:

| registry | rows | rungs missing | gate missing |
|---|---|---|---|
| `artifacts/town_schedules.json` | 538 | 70 | 0 |
| `S/band2100p/town_schedules.json` | 612 | 40 (the BAND40 towns) | 0 |
| **`S/band40/town_schedules.json`** | **630** | **0** | **0** |

`S/band40/` is a superset of `artifacts/town_schedules.json` and agrees with `S/band2100p/` on
every shared key (it lacks only `band2100p`'s later NEXTHIGH rows, which are not flow214 rungs).
**No shared file was rewritten**: the 630-row file was copied to
`artifacts/flow214/town_schedules.json` (md5 `1d079d85`) and `--real-gate-pinned` points there.
The launcher refuses to start without it.

## 5. Precheck

`bash S/flow214/precheck.sh` → `S/flow214/precheck.log`. Steps: (1) banner
`236 pinned rungs x 1 episode + 4 episodes carried` + the rung/episode arithmetic, (2) the abs-probe
row and memory arithmetic against the 8 GB ceiling, (3) all 236 tapes + all 62 gate opponents,
(4) the registry covers every rung and every gate opponent, (5) the trained-gene mask (must be
1,126), (6) a **CPU** `--gens 0` dry run of the real argument list (`JAX_PLATFORMS=cpu`, the GPU is
never touched), (7) a **real GPU smoke**: `--gens 1 --pop 64 --abs-every 1` with the gate dropped,
which compiles the production `--chunk 4096` main loop *and* the full 15,360-row abs probe (the
probe is pop-independent, so the smoke's peak is the arm's peak to within the 53 MiB perturbation
block), samples `nvidia-smi` every 5 s for the peak, and releases the card.

Results (this staging run, 2026-09-12T04:52Z): **steps 1-5 PASS** — 236 rungs, `--episodes 240`,
probe peak ~5,260 MiB < 8,192 (measured base puts it at ~5,960), 236/236 tapes, 62/62 opponents,
registry 0 missing, **d_train 1,126**. Steps 6-7 take ~13 min (tape load on CPU) and ~20 min; they
were relaunched detached and `S/flow214/precheck.log` carries their verdict and the measured GPU
peak. **Read `=== flow214 precheck PASS ===` before launching** — while the smoke holds the card
the arm's own guard will refuse the launch anyway (a safe failure, not a broken recipe).

One harness bug was found and fixed by the first run: `SMOKE=1` dropped the gate array but left
`--keep-candidates`, and `scripts/train.py` refuses that pair apart ("it keeps the thetas the gate
is handed"). The launcher now drops both under `SMOKE=1` (`KEEP_ARGS`), and the launched arm always
carries `--real-gate … --keep-candidates`. The failed run is otherwise evidence *for* the staging:
it got all the way through setup and printed the trainer's own banner,
`pinned-once: 236 pinned rungs x 1 episode + 4 episodes carried`, with
`pinned-fixed-seed: 236 pinned rung(s) on their own fixed board`.

## 6. Judge path for a LOCAL arm

`S/autojudge/watch.sh`'s `ARMS` entries are `flowNNN stage_hr` — it fetches records over ssh and
never sees a local run. flow194/flow198 were judged **by path** instead, and flow214 is judged the
same way:

```
cp artifacts/flow214/cands/g00010_record.npy artifacts/kagg2_games/thetas/flow214_g10_hr.npy
bash S/autojudge/watch.sh --legs flow214_g10_hr \
     /mnt/e/_work/kaggriculture3/artifacts/kagg2_games/thetas/flow214_g10_hr.npy
```

(`--legs` takes `/root/kagg3_judge.lock` itself — never wrap it in a second `flock`.) Unattended:
`nohup bash S/localarm/judge_local.sh flow214 &` works unmodified, because
`S/localarm/tree/artifacts` is a symlink to the repo's `artifacts/`, so the tailer's
`…/tree/artifacts/flow214/real_gate.log` is the live run's.

Centre reads (§107) need two env values and **no edit to `S/snr/`**: drop the local checkpoint as
`S/snr/flow214/state_latest.npz` (which `keep_state.sh` adopts before it scps anything), then
`LAUNCHER=S/flow214/launch_flow214.sh SKIP_FETCH=1 S/snr/centre_read.sh flow214 <gen>`. Full
recipe in `S/flow214/README.md`.

## 7. Launch line (coordinator)

```
cd /mnt/e/_work/kaggriculture3 && nohup setsid bash S/flow214/launch_flow214.sh >> artifacts/flow214/launch.out 2>&1 &
```

The launcher refuses if: the card holds > 1,024 MiB, another `scripts/train.py` is on the box, the
tree hashes drift from the host, `SEED_ROOM_PURSE_ON` is not `True`, the seed theta or the registry
is missing, `artifacts/flow214/train.log` already exists, a rung id is duplicated between the
inherited / NEXT / BAND lists, or the pinned rungs exceed `--episodes − 2`.
