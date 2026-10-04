# 60 — ACTION-RL: the residual head (MERGED into master 2026-09-19, manual lane)
**LAW (ACTIONRL5, 2026-09-19): sim `mwin` is NOT a gate.** flow254 climbed 0.826 → 0.918 in sim and *lost* real board wins
(94.6 → 89.3 %) out of sample. A checkpoint is promoted only on **OUT-OF-SAMPLE boards through `S/actionrl/gate.sh`** — BAND2 first
56 (`head -56 S/winjudge/band2_ids.txt`, disjoint from the training panel) — with **net board flips > 0**, `dTHEIRS ≤ 0` and t ≥ 3.
Coin alone is not enough: flow254 was gift-free at +646 coin and still −3 net flips, and the ladder pays **wins**.
**SELF-PLAY (ACTIONRL6):** a tape does not re-plan, so a head that beats tapes may only have learned to exploit a replay. New runs
seat a live opponent half the time: `--pool <npy,npy,…> --selfplay-frac 0.5`. The pool is **theta-only** (no head snapshots — seat 1
flies the plain planner by construction, `head.jax_fn` hands the second call of a dawn `head.noop_override`), the shipped centre is
always in it, and any member not 7,692 long or duplicate is SKIPPED and named at startup. `log.tsv` prices the halves apart:
`sp_win` (live opponent) vs `tape_win` (replay). **A run whose `tape_win` climbs while `sp_win` does not is flow254 again.**
ACTIONRL1 is an explicit **NO-GO on PPO**; the USER overrode it to build the stage, and no positive read is claimed. A fresh head
(`ZERO_BIAS` on each slot's no-op, `w3 = 0`) plans the shipped day **to the byte** — proved through the package, not asserted: the
identity tarball smokes 720 steps / 0 bad / 184,456 / 129,457, the shipped coins. PPO earns every departure from that.
## (a) Train — REMOTE GPU by default; `flow257_ppo_selfplay` is the live run (GPU0, pid 1804890, launched 2026-09-19 16:2xZ)
`flow257` = flow254's line **plus** `--pool S/alphafarm/theta_af3_20.npy,S/alphafarm/theta_af3_60.npy,S/alphafarm/theta_af3_120.npy --selfplay-frac 0.5`
(pool = 4 with the shipped centre; rsync the `theta_af3_*.npy` with the code). flow254 is done and NO-GO (ACTIONRL5).
**GPU LAW (user 09-19): use the GPU when possible.** Remote launch (stage once, then one line):
```bash
rsync -aR --exclude __pycache__ src S/actionrl S/drainpin S/winjudge/ship7692/theta7659.npy user@remote-host:~/stage_ppo/
sed 's/$/.npz/' S/actionrl/flow251_ids.txt > /tmp/ids.txt   # tapes the run needs (306)
ssh user@remote-host 'mkdir -p ~/stage_ppo/artifacts/tape_actions_town'
rsync -a --files-from=/tmp/ids.txt artifacts/tape_actions_town/ user@remote-host:~/stage_ppo/artifacts/tape_actions_town/
ssh user@remote-host 'cd ~/stage_ppo && setsid nohup env KAGG3_ROOT=$HOME/stage_ppo KAGG3_SRC=$HOME/stage_ppo/src KAGG3_ART=$HOME/stage_ppo/artifacts JAX_PLATFORMS=cuda CUDA_VISIBLE_DEVICES=0 \
  /home/user/kagg3/.venv/bin/python S/actionrl/ppo.py --run <run> --batch 512 --updates 2000 --ckpt-every 20 \
  --ent 0.001 --minibatches 4 --kl-target 0.01 --grad-clip 0.5 \
  --tape-dir $HOME/stage_ppo/artifacts/tape_actions_town --ids $HOME/stage_ppo/S/actionrl/flow251_ids.txt \
  > S/actionrl/<run>.log 2>&1 < /dev/null & echo pid $!'
```
Expected: `[actionrl] run=… batch=512` then ~10 min of XLA compile (GPU 0 %, ~800 MB), then `update` rows every ~3 s (GPU 100 %).
Status: `ssh user@remote-host 'cut -f1-16 ~/stage_ppo/S/actionrl/<run>/log.tsv | tail'`; checkpoints `~/stage_ppo/S/actionrl/<run>/head_*.npz`
— rsync them back before `gate.sh`. GPU1 is free for a second run (`CUDA_VISIBLE_DEVICES=1`). The LOCAL CPU line below is the fallback only.

The head, `ppo.py`, `gate.sh` and the spliced `plan.py` are on **master** now, so a NEW run starts here:
```bash
cd /mnt/e/_work/kaggriculture3                                   # master = the merged tree
nohup env KAGG3_ROOT=/mnt/e/_work/kaggriculture3 KAGG3_SRC=$PWD/src JAX_PLATFORMS=cpu \
  /mnt/e/_work/kaggriculture3/.venv/bin/python S/actionrl/ppo.py \
  --run <run> --batch 64 --updates 2000 --ckpt-every 20 \
  --ent 0.001 --minibatches 4 --kl-target 0.01 --grad-clip 0.5 \
  --tape-dir /mnt/e/_work/kaggriculture3/artifacts/tape_actions_town \
  --ids $PWD/S/actionrl/flow251_ids.txt > S/actionrl/<run>.log 2>&1 &
```
**`flow252_ppo` runs from `.claude/worktrees/actionrl` (pid 16600, launched 2026-09-19 12:15Z) and stays there** — that worktree is
*where flow252 is running now*, not where new work goes; its code is this same commit. Python already imported its
`S/actionrl/*.py` and the worktree's `src/kagg3`, so a merge does not touch the live process; equally, do NOT
`git checkout`/`reset` that worktree, and read its checkpoints and log at
`.claude/worktrees/actionrl/S/actionrl/flow252_ppo/`.
**What `flow251_ppo` died of (killed 12:14Z, pid 9267):** 4 full-batch epochs at a fixed 3e-4 with no trust region walked the head
to the UNIFORM policy — `entropy` 6.29 → 24.86 against a 27.30 ceiling (`sum_s log n_s` over the 18 slots), win 0.859 → 0.31-0.45,
margin +12,484 → −4,331 by u219. The four new flags are the trust region: **4 minibatches of 16 whole EPISODES × ≤ 4 epochs,
stopped the moment the k3 approx-KL to the sampling policy passes `--kl-target` 0.01**; **LR 3e-4 decayed linearly to 0** over
`--updates` plus a global **grad-norm clip 0.5**; advantages normalised per update; and `--ent 0.001`, because the entropy bonus is
a SUM over 18 slots (0.01 × 27.3 = 0.27 of pull at uniform, against a unit-normalised advantage — that bonus *is* the force
flow251 followed out). The `--ent` DEFAULT is still 0.01 so flow251's numbers stay reproducible; every new run passes 0.001
explicitly.
**REGRESSION GUARD** (`--guard-window 20 --guard-base 5 --guard-drop 0.15 --guard-keep 0.05 --guard-patience 20`): the loop keeps a
running mean win over the last 20 updates and `base_win` = the mean win of the first 5 (the identity head IS the shipped planner).
If the running mean sits below `base_win − 0.15` for 20 CONSECUTIVE updates it halves the LR, reloads the newest checkpoint whose
own window mean was ≥ `base_win − 0.05`, drops the Adam moments, and logs the event.
`flow251_ids.txt` = 56 hiband + 250 BAND250 ids, deduped, all 306 with a tape; ONE compile serves the panel (`tape_ctl` gathers the rung), so any `--ids` file swaps it free.
Shops are DRAWN (default); `--pinned-town` hands back the tapes' town and with it ALPHAPROBE3's 68 %-hindsight. `--resume <head_k.npz>` continues. The run eats the box (JAX
CPU, 12 threads, ~8 GB RSS at 306 tapes); prefix `taskset -c 0-3` to leave cores for a judge (≈ 3× slower). Remote (`user@remote-host`, **check what ES holds first**): the same line with `JAX_PLATFORMS=cuda` and batch 256-512, after rsyncing the worktree and `artifacts/tape_actions_town`.
**PYTHONPATH LAW:** never set `PYTHONPATH` in this lane — `KAGG3_SRC` goes to `sys.path[0]` so the worktree's spliced `plan.py`
traces; a stale `PYTHONPATH=/…/src` silently trains against master's planner.
## (b) Status
`<run dir>/log.tsv` — for flow252 that is `.claude/worktrees/actionrl/S/actionrl/flow252_ppo/log.tsv`:
`update games mean_reward win_rate mean_margin entropy loss vloss kl steps lr mwin sp_win tape_win sp_n sec hist`
(columns 13-15 are new in ACTIONRL6; `sec` moved 13 → 16, so old `cut -f1-13` becomes `-f1-16`).
`mean_margin` is the honest number (`mean_reward` mixes in the ±1 win); `hist` = per-slot action counts, 18 `;`-groups, and its
no-op column is the first diagnostic; `vloss` and stdout's `V|sd` say whether the GAE(λ=0.95, γ=1) baseline is alive.
**The DIVERGING signal is now one grep, not a squint at the win column:**
```bash
grep -a '^#GUARD' .claude/worktrees/actionrl/S/actionrl/flow252_ppo/log.tsv   # base_win once, then one line per rewind
# #GUARD  diverging  u<k>  mwin 0.41  base 0.83  lr0 1.500e-04  reload head_120.npz
```
A `diverging` line means the head has been ≥ 0.15 win below the shipped planner for 20 straight updates and the run has rewound
itself; **two of them is the run telling you PPO is not finding anything — stop it** rather than watching the LR halve again.
Between rewinds, read `kl` (should sit near but under 0.01) and `steps` (16 = all 4 epochs ran, < 16 = the KL stop fired, which is
healthy) — and `entropy` against the 27.30 uniform ceiling, which is the number flow251 climbed.
## (c) Gate a checkpoint — the greedy NUMPY head on the real engine, i.e. exactly what the package flies
Gate from **master** (the merged tree), pointing at the run dir that owns the checkpoint — `CK` below is the worktree for flow251:
```bash
cd /mnt/e/_work/kaggriculture3
CK=/mnt/e/_work/kaggriculture3/.claude/worktrees/actionrl/S/actionrl/flow252_ppo
WORKERS=2 N=8  bash S/actionrl/gate.sh $CK/head_20.npz     # smoke, proves the path
WORKERS=2 N=56 bash S/actionrl/gate.sh $CK/head_500.npz    # the real HIBAND read
KAGG3_RESIDUAL_HEAD_PY=$PWD/S/actionrl/head.py WORKERS=2 \
  SW_EXTRA=",RESIDUAL_ON=True,RESIDUAL_HEAD=$CK/head_500.npz" \
  bash S/winjudge/judge.sh res_500 /mnt/e/_work/kaggriculture3/S/winjudge/ship7692/theta7659.npy
```
Default `LEGS` is the POOLED278 pair read. Promotion needs §115b (+450, t ≥ 3) gift-free, not the hiband smoke — **and the
OUT-OF-SAMPLE leg first**: `head -56 S/winjudge/band2_ids.txt > /tmp/oos.txt` and gate on those 56 with net flips > 0 (the LAW at
the top of this file). A hiband number on the training panel is in-sample and says nothing (ACTIONRL5: +1,438 in sample, −3 net
flips out of it).
## (d) Ship
`.venv/bin/python scripts/package_submission.py --theta <theta.npy> --residual $CK/head_<k>.npz --out dist/<name>.tar.gz`
ships `head.py` → `core/residual_head.py` + `residual_head.npz` and sets `RESIDUAL_ON` in `main.py`. WITHOUT `--residual` the tarball is byte-identical to a pre-flag build
(md5 `3fb11573…` on `theta7659`). Always `bash S/widepickship/run_smoke.sh <tarball>`: 720 steps, 0 bad, no jax, `kagg3` loaded from the archive.
## (e) Games to signal, and when to stop
ACTIONRL1 §4: 1e6-1e7 dawn-steps = **33 k-333 k games**. Measured 18-32 s/update at batch 64 = **133-218 games/min**, flow251 itself ~22 s = ~175/min, after a one-off
250-700 s compile: 33 k ≈ **3-4 h**, 128 k (the 2,000-update target) ≈ **12-16 h**, 333 k ≈ **31-42 h**. A gate costs 56 engine games (~5 min at WORKERS=4), POOLED278 ~24 min.
**KILL RULE:** if by update 500 (32 k games, ~4 h) the argmax head has still not left the no-op — `hist` no-op column ~100 %, or
an `N=56` gate coin-identical to `ship7692` — STOP the run. A head that cannot leave the frozen planner has learned nothing, and
ACTIONRL1's five quantity-family rejections remain the prior it has to beat.
## (f) ACTIONRL6 read — `sp_win` vs `tape_win` on flow257, u0-u6 (identity head, nothing trained yet)
`sp_win` 0.17-0.18 against a live seat vs `tape_win` 0.80-0.83 against a replay, same head, same boards: the 0.66 gap IS
ACTIONRL5's lost board wins. ~0.15 of the self-play number is the sampler (`ZERO_BIAS 4.0` = ~13 %/slot/dawn off the no-op; the
CPU smoke puts a pure-sampling head at 0.125-0.25 vs the shipped planner), so **≈ 0.15 is the self-play baseline PPO must lift**,
not 0.5. The guard's `base_win` (0.4918) is the MIXED win: on a self-play run it is half a replay number, a divergence tripwire
only and never a read.
## (g) flow257_ppo_selfplay FINISHED (2,000 updates, ~1 h 50 m on GPU0, no `#GUARD diverging`) — checkpoints local
`S/actionrl/flow257_ppo_selfplay/` (100 × `head_*.npz`, gitignored, rsynced back; `log.tsv` committed). PPO **did** lift the live
seat: `sp_win` 0.175 → 0.371 (u200) → 0.438 (u400) → 0.492 (u600) → 0.562 (u800), then a **plateau at 0.54-0.58 from u800 to
u1999**; `tape_win` sat at 0.88-0.95 throughout, so the replay column was saturated almost from the start and carried no gradient —
the self-play half is where the run actually learned. Entropy 6.28 → 4.16 at u200 (it SHARPENED first, unlike flow251/254) → back
up through 10 at **u945** → 13.07 at u1999.
**Gate candidates, in the order to spend engine games on them** (LAW at the top of this file: BAND2 first 56, out of sample, net
flips > 0, dTHEIRS ≤ 0, t ≥ 3):
* `head_940` — best 20-update `sp_win` window that is still **pre-entropy-10** (mean 0.5629, ent 9.61). ACTIONRL5's analogue.
* `head_2000` — final (window 0.5822); on flow254 the FINAL checkpoint was the one that read positive out of sample, not the
  pre-entropy-10 pick, so this is not the second choice by default.
* `head_1780` — best window of the whole run (0.5983) but at ent 12.83.
**Unread:** no checkpoint has been gated yet. The plateau from u800 is the honest stopping point — 1,200 updates of the run bought
~0.02 of `sp_win` and 4 points of entropy, so a shorter, lower-`--ent` rerun is the obvious next configuration if the gate is flat.

## (h) flow260_ppo_lossmix — LIVE-LOSS panel + warm start (ACTIONRL9, 2026-09-20, GPU1 pid 1823929)
`--ids S/actionrl/flow260_ids.txt` = flow251's 306 **plus the 112 lost live games** of subs 56370365 (30) and 56335778
(82), re-downloaded fresh and cut with `scripts/make_tape_actions.py --replay <raw>.json --with-town`; 0 of the 112 are
in `S/winjudge/band2_ids.txt`, so the OOS gate stays disjoint (`S/actionrl/flow260_excluded.txt` is empty).
**`--resume` IS the warm start** (`HEAD.load` into params, Adam moments zeroed, LR schedule restarted) — flow260 resumes
`flow257_ppo_selfplay/head_940.npz` at **`--lr 1e-4`** over 1,000 updates, everything else as (a).
Gate against **`head_940` as the incumbent**, not the identity head: `LEG=band2 N=56 WORKERS=2 bash S/actionrl/gate.sh <head_k.npz>`.
Full write-up: `docs/strategy/2026-09-20-actionrl9.md`.

## (i) Two flags added by ACTIONRL10 (2026-09-20) — price the gift, and seat the clone
**`--paired-baseline LAMBDA`** (absent = OFF, and OFF the reward is flow257/260's byte-identical
`win + margin/1e4`). ON, every episode is rolled a SECOND time on the same board — same weather words,
same shop draw, same seat-1 theta, same tape rung, same `ctl` — with the head off on both seats
(`head.noop_override` = the shipped planner), giving `(ours0, theirs0)`; the reward becomes
`win + ((ours - ours0) - LAMBDA*(theirs - theirs0))/1e4`. That is the head's own causal effect on EACH
purse. **LAMBDA = 1.0 is the CRN control variate, not a new objective** — the coin term is then exactly
`margin - margin0` and `margin0` is policy-independent, so it buys variance (board margins swing ±20k, a
head move is worth hundreds) and nothing else. The gift TAX is `LAMBDA > 1`: it is the price of the
rival's coin in ours, and flow260 (ours +594 / theirs +963 on the live gate) is the argument that the
price is above 1. Baseline for the WHOLE panel, tape half
included: a tape replays fixed actions but the coins they earn move with the book we move. Costs one
extra sim per episode (no gradient, no features) — ~2× the update's rollout time.
New `log.tsv` columns `d_ours` `d_theirs` (batch means) between `sp_n` and `sec`, so status reads are
now `cut -f1-18`. Sanity: `--resume` a SATURATED no-op head (`b3[noop]=60`, i.e. `p(noop)=1`, not the
`ZERO_BIAS=4.0` init which still samples off-noop) must print `d_ours 0.0 d_theirs 0.0` and
`reward == win` exactly.
**`--pool` clone members** — `S/actionrl/pool/clone_m*.npy` are theta7659 with `cd[MELON, bucket 0]`
raised (`brain.CROP_DAY_ON` is in the shipped switch string, `CROP_DAY_GAIN=64`), which is the only
theta-reachable way to seat a RE-PLANNING opponent that opens on the BAND clone's melon plate — the
plate is `plan.MELON_PLATE_TILES`, a module switch read at trace time, so it cannot vary per episode
inside one compiled program and cannot be a pool member. `S/actionrl/pool/build_clone.py` is the
builder and prints the measured opening plate of each.
`flow261_ppo_gift` (GPU1, pid 1826730, 2026-09-20 11:19Z) is the first arm: `--resume head_940.npz
--lr 1e-4 --paired-baseline 1.0 --selfplay-frac 0.8 --pool <af3×3 + clone_m{4,8,10}> --batch 512
--updates 1500 --ids flow251_ids.txt`. 10.7 s/update (5.7 without the pairing). At u0 `head_940` reads
`d_ours +1469 / d_theirs +944` — flow260's gate gift reproduced inside the trainer.
Full write-up `docs/strategy/2026-09-20-actionrl10.md`.

## (j) ACTIONRL12 — win-only reward on hard boards (`flow265_winonly`, GPU1 pid 1843859, 2026-09-20)
**`--margin-weight W`** (default 1.0 = every earlier run byte for byte) scales the whole COIN term of the
reward — the paired `d_ours - LAMBDA*d_theirs` under `--paired-baseline`, the raw `margin` without it — so
**`W = 0` is the WIN term `+-1` and nothing else**. Every arm flow260-263 had sim `mwin` flat 0.72-0.78
while margin moved by thousands: the gradient was the coin's, and the ladder pays `P(win)`.
**`--hard-boards P`** (default 0 = the old uniform board draw, RNG stream included) runs ONE head-off pass
(the `--paired-baseline` program, head off on both seats, chunked at exactly `--batch` so it reuses that
program's compile) over the tape rungs, scores each board's head-off win rate `p0` over `HARD_K = 4`
weather draws, and samples boards with weight `max(P, 4 p0 (1-p0))`: 1.0 at a coin flip, `P` at a board the
shipped planner always wins or always loses — which under a win-only reward returns the same `+-1` whatever
the head does. Nothing is excluded. Summary once as a `#HARD` row in `log.tsv` (`grep -a '^#HARD'`);
**log columns unchanged**, so `cut -f1-18` still reads.
With `W = 0` do **not** pass `--paired-baseline`: it cannot reach the reward and costs 2x rollout time
(10.7 vs 5.7 s/update). `d_ours`/`d_theirs` then log as 0.0 and the gift is read at the gate, as always.
Launch line, pid, gate commands and the WIDE-from-scratch argument: `docs/strategy/2026-09-20-actionrl12.md`.
