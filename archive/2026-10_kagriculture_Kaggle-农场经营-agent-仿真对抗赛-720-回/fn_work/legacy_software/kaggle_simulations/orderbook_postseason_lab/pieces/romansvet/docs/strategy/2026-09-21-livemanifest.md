# LIVEMANIFEST — exact-board ACTIONRL lanes (2026-09-21)

`S/actionrl/live_manifest.py` makes LIVE250 the board authority for both
trainers.  The ordered id list is joined by episode key to opponent seat,
LIVESEED sidecar, pinned town, and opponent action tape.  The fixed
chronological split is games 0–149 train, 150–199 development, and 200–249
sealed.  Original seat is retained; neither trainer invents weather seeds,
towns, tape seats, or mirrored games in manifest mode.

The portable form is optional:

```bash
.venv/bin/python S/actionrl/live_manifest.py \
  S/actionrl/live250_ids.txt /tmp/live250.tsv
```

The commands below use the canonical id file directly.  Stage code, manifest
companions, theta/head, and the 250 pinned tapes once, following the relative
path convention in `S/pipeline/60_actionrl.md`:

```bash
cd /mnt/e/_work/kaggriculture3
rsync -aR --exclude __pycache__ \
  src S/actionrl/ppo.py S/actionrl/es_head.py S/actionrl/head.py \
  S/actionrl/live_manifest.py S/actionrl/live250_ids.txt \
  S/actionrl/flow257_ppo_selfplay/head_940.npz \
  S/band3/live250_epseat.txt S/band3/live250_epseat.txt.seeds \
  S/winjudge/town_live250.json S/winjudge/ship7692/theta7659.npy \
  user@remote-host:~/stage_livemanifest/
sed 's/$/.npz/' S/actionrl/live250_ids.txt > /tmp/live250_npz.txt
ssh user@remote-host 'mkdir -p ~/stage_livemanifest/artifacts/tape_actions_town'
rsync -a --files-from=/tmp/live250_npz.txt artifacts/tape_actions_town/ \
  user@remote-host:~/stage_livemanifest/artifacts/tape_actions_town/
```

GPU0 — PPO proposal lane, resumed from `head_940`.  The reference arm and
opponent head are the same incumbent.  Every 50 updates an ARGMAX candidate
vs-incumbent development read is appended to the run's `log.jsonl`; it never
ships a checkpoint.

```bash
ssh user@remote-host 'cd ~/stage_livemanifest && setsid nohup env \
  KAGG3_ROOT=$HOME/stage_livemanifest \
  KAGG3_SRC=$HOME/stage_livemanifest/src \
  KAGG3_ART=$HOME/stage_livemanifest/artifacts \
  JAX_PLATFORMS=cuda CUDA_VISIBLE_DEVICES=0 \
  /home/user/kagg3/.venv/bin/python S/actionrl/ppo.py \
  --run flow_livemanifest_ppo --batch 512 --updates 2000 --ckpt-every 20 \
  --resume S/actionrl/flow257_ppo_selfplay/head_940.npz \
  --opponent-head S/actionrl/flow257_ppo_selfplay/head_940.npz \
  --win-reference S/actionrl/flow257_ppo_selfplay/head_940.npz \
  --adaptive-gift --gift-budget 0 --dev-gate-every 50 \
  --ent 0.001 --minibatches 4 --kl-target 0.01 --grad-clip 0.5 \
  --live-manifest S/actionrl/live250_ids.txt --live-split train \
  > S/actionrl/flow_livemanifest_ppo.stdout 2>&1 & echo pid $!'
```

GPU1 — exact-board greedy ES control.  Fitness is uniform per train board,
uses paired delta-win, rejects mean positive `delta_theirs`, and lets only a
bounded margin term break ties.

```bash
ssh user@remote-host 'cd ~/stage_livemanifest && setsid nohup env \
  KAGG3_ROOT=$HOME/stage_livemanifest \
  KAGG3_SRC=$HOME/stage_livemanifest/src \
  KAGG3_ART=$HOME/stage_livemanifest/artifacts \
  JAX_PLATFORMS=cuda CUDA_VISIBLE_DEVICES=1 \
  /home/user/kagg3/.venv/bin/python S/actionrl/es_head.py \
  --run flow_livemanifest_es --gens 20 --pairs 16 --ckpt-every 5 \
  --incumbent S/actionrl/flow257_ppo_selfplay/head_940.npz \
  --opponent-head S/actionrl/flow257_ppo_selfplay/head_940.npz \
  --live-manifest S/actionrl/live250_ids.txt --live-split train \
  > S/actionrl/flow_livemanifest_es.stdout 2>&1 & echo pid $!'
```

The development read is the only selection signal during these launches.  The
sealed 50 rows are not loaded into either fitness panel and remain untouched
until one candidate has been frozen.
