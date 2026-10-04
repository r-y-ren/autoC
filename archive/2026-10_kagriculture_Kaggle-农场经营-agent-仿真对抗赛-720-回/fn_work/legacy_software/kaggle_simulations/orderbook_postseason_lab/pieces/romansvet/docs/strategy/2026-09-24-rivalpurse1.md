# RIVALPURSE1 (2026-09-24, 21:22-23:30Z) — head_940 rival-purse input fixed + PPO fine-tune: NO SHIP

## 1. Dead features (3 real engine games, reacting V56, LIVE250 dev 0-2, actTimeout 600, 180 dawn calls, `S/rivalpurse1/v56.py` RP_DUMP)
The 3 dump games reproduce master byte-exact (76,210/74,683, 60,295/61,743, 86,919/82,392 = DRIPSELL1 dev_off rows 0-2).
Constant at every dawn of all 3 games (64-vector layout: day, money, opp_money, crop×5, animal×3, n_free, shed×12, seeds×5, mkt_inv×9, price×9, shops×8, opp_commit×9):

| idx | feature | value | cause |
|---|---|---|---|
| **2** | **rival purse** | **0** | **BUG (never wired):** `_residual_features` reads `view.opp_money`, which `agent/parse.py` AND `sim/rollout.day_view` fill only under `SELL_SLOT_MIRROR_GATE_ON` (False). The true purse sits in `view.program_opp_money` (always filled, 59..73,489 in the dump). Train and serve both saw 0, so head_940 was trained blind, not mis-served. |
| 21-23 | shed GOOSE/COW/SHEEP | 0 | structural: animals go to tiles, never to the shed. Harmless (0 in train and serve). |
| 26-28 | seeds TOMATO/STRAWBERRY/MELON | 0 | behavioural: premium seeds are bought and planted the same day, so the dawn count is 0. Not a bug. |
| 54 | shops YARN_STORE | 0 | the 3 towns never drew one; live on other towns. Not a bug. |

## 2. Fix (commit on branch rivalpurse1)
`plan.RESIDUAL_RIVAL_PURSE_ON` (default False = shipped, byte-identical): feature 2 reads `view.program_opp_money`. Count/order unchanged,
head_940 loads as is. `S/actionrl/ppo.py`: `KAGG3_PPO_SW_EXTRA` env applies extra switches after `SW` (unset = identical).
Test `tests/test_rivalpurse1.py` (OFF → 0, ON → purse/1e4, other 63 untouched). Harness `S/rivalpurse1/`: `v56.sh` (dev 0-99 / held-out 150-249),
`tape.sh` (band tapes dev50), `eng.sh`/`eng.py` (ENGINE faithful-59), `pair.py`/`tpair.py`. Master baselines = DRIPSELL1 OFF csvs (only
`route_nn.py` changed since, default OFF) + own faithful master run (9-50, = ENGCHECK).

## 3. Gate table (paired vs master, TWO-PURSE; ckpt = rp1_a update k, head_940 + fixed input)
| ckpt | leg | W-L master→new | flips | Δours (t) | Δtheirs (t) |
|---|---|---|---|---|---|
| head_940 + fix (no training) | V56 dev100 | 69-31 → 73-27 | +4/−0 = **+4** | −53 (−1.14) | −37 (−0.87) |
| head_940 + fix | V56 held-out100 | 72-28 → 71-29 | +1/−2 = **−1** | −0 (0.00) | −5 (−0.15) |
| head_940 + fix | band tapes dev50 (100 seat-games) | 74-26 → 74-26 | +4/−4 = 0 | +464 (1.19) | −21 (−0.48) |
| head_940 + fix | ENGINE faithful-59 | 9-50 → 9-50 | 0 | −65 (−0.96) | +3 (0.07) |
| rp1_a u200 | V56 dev100 | 69-31 → 68-32 | +0/−1 = −1 | −36 (−0.81) | −19 (−0.32) |
| rp1_a u360 | V56 dev100 | 69-31 → 67-33 | +1/−3 = −2 | −63 (−1.44) | +34 (0.59) |
| rp1_a u580 | V56 dev100 | 69-31 → 72-28 | +6/−3 = **+3** | −92 (−1.54) | −106 (−1.45) |
| rp1_a u580 | V56 held-out100 | 72-28 → 68-32 | +1/−5 = **−4** | +27 (0.32) | **+159 (2.51)** |
| rp1_a u580 | band tapes dev50 | 74-26 → 78-22 | +4/−0 = +4 | +605 (1.57) | −10 (−0.12) |
| rp1_a u580 | ENGINE faithful-59 | 9-50 → 9-50 | 0 | +15 (0.10) | +198 (2.06) |
| rp1_a u600 | V56 dev100 | 69-31 → 70-30 | +5/−4 = +1 | −260 (−3.58) | +1 (0.01) |
| rp1_a u900 | V56 dev100 | 69-31 → 70-30 | +5/−4 = +1 | −146 (−1.74) | +0.22 (0.00) |
| rp1_a u1100 | V56 dev100 | 69-31 → 67-33 | +3/−5 = −2 | −147 (−1.69) | +115 (1.46) |
| rp1_a u1200 | V56 dev100 | 69-31 → 67-33 | +2/−4 = −2 | −177 (−2.07) | +147 (1.93) |

**Verdict: NO SHIP.** The fixed input alone moves head_940 on ~80 % of boards but nets +4 dev / −1 held-out / 0 tapes / 0 faithful
(noise). PPO fine-tune (u580 the only dev pass) fails held-out −4 with a gift t 2.5; later checkpoints drift to −2 dev with gifts
rising (Δtheirs +115..+147). Sim self-play win (20-update window) dropped 0.56 → 0.505 at u0-20 when the head first saw a real purse,
recovered to 0.54-0.56 by u580 and stayed flat to u1380 (entropy 9.6 → 13.1): the sim objective (tapes + theta pool) has no gradient
toward the V56 wins the labels found. The rival-purse channel is now wired and available (switch) for any future head/trainer
(BESTRESP3's rich-input residual already reads it via `program_features[64]`).

## 4. Remote state
`user@remote-host:~/stage_rivalpurse1` (src + S/actionrl + pool thetas + head_940; tapes symlinked to ~/stage_ppo). Run `rp1_a`
(GPU1, pid 2022500, `--resume head_940 --lr 1e-4 --updates 1500 --ckpt-every 20`, pool af3_20/60/120, selfplay 0.5,
`KAGG3_PPO_SW_EXTRA=RESIDUAL_RIVAL_PURSE_ON=True`) **KILLED 23:26Z at u1383** (time-box, negative trend); verified gone, GPU1 free.
69 checkpoints in `~/stage_rivalpurse1/S/actionrl/rp1_a/head_*.npz`; log copied to `S/rivalpurse1/rp1_a_log.tsv`.
Resume: same launch line (`S/pipeline/60_actionrl.md` §a) with `--resume ~/stage_rivalpurse1/S/actionrl/rp1_a/head_1380.npz`.
Local gate heads `S/rivalpurse1/heads/` (gitignored): head_940 md5 769ff15e…, rp1_a_580 md5 61adf242…. No local processes left.
Gate a checkpoint: `WORKERS=4 bash S/rivalpurse1/v56.sh <arm> 0 100 dev <head.npz> RESIDUAL_RIVAL_PURSE_ON=True` then
`python S/rivalpurse1/pair.py S/rivalpurse1/dev_master.csv S/rivalpurse1/dev_<arm>.csv` (held-out: `150 100 ho`, `ho_master.csv`).

## 5. Left
Not tried: training with the fixed input against the reacting V56 itself (the sim has no V56; only the engine-side DAgger/search
lanes of BESTRESP2/3 see it). rp1_a u700-1380 ungated except 900/1100/1200.
