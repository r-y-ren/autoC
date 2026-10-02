# SELFPLAY1 (2026-09-26): self-play RL practice guide + diagnosis of RLLOSS1 (`S/rlloss1/ppo_loss.py`)

Why this exists: every PPO retrain since head_940 moves the head (KL .2-.7, 60-88 % of dawns differ) but flips no boards and gifts the rival (Δtheirs t 2-4).
We compared the trainer with published self-play recipes. Research only: no training runs and no src/ edits.

## §1 Practice summary (sources)
- **AlphaStar league** (Vinyals et al., Nature 2019; the mini-AlphaStar re-implementation arxiv 2104.06890 §League). Three roles.
  Main agents: 35 % pure self-play, 50 % PFSP over all past players, 15 % PFSP over forgotten mains and exploiters.
  PFSP weight is f_hard(x) = (1-x)^p (p=2), where x = P(we beat opponent), so games go to opponents we still lose to.
  The alternative weight f_var = x(1-x) favours even matches. Main exploiters play only the current main; if their win rate vs it is < 0.1, they switch to its past checkpoints under f_var.
  A snapshot joins the league when its win rate vs the league is > 0.7 or after a fixed step budget. Exploiters then reset to the supervised init.
  Lesson: the learner never trains only against itself or only against one fixed opponent.
- **OpenAI Five** (arxiv 1912.06680, §3.2 and App. N). Self-play is 80 % latest vs latest and 20 % past versions.
  Past versions are sampled by softmax over a quality score q_i. The current agent is added to the pool every 10 iterations at q = max. When the learner wins, q_i -= η/(N p_i) with η = 0.01.
  Reward is zero-sum symmetrised (the enemy team's reward is subtracted) and normalised by a running std, not a per-batch std.
  Batch is 1-3 M timesteps per optimiser step. Entropy 0.01→0.001, lr 5e-5→5e-6, clip 0.2, GAE λ 0.95, staleness ≤ 1 version.
  Batch 983 k gave 2.5× the speed of 123 k. "Surgery" keeps behaviour identical when the network changes.
- **PFSP/FSP/PSRO/NeuPL/regret families** (survey arxiv 2408.01072).
  Vanilla self-play cycles in non-transitive games. FSP/PFSP keeps a growing pool. PSRO/NeuPL add best responses to a meta-Nash mixture.
  R-NaD/DeepNash and (Deep)CFR target Nash in imperfect-information zero-sum games. Their per-infoset regret machinery does not fit a 30-dawn × 18-slot residual on a simulator: use it as theory, not as the recipe.
- **Competitive-PPO failure modes** (Territory Paint Wars, arxiv 2604.04983). With pure self-play, win rate vs held-out opponents fell 73.5 %→21.6 % while self-play win rate stayed ~50 % ("undetectable via self-play metrics").
  Replacing 20 % of episodes with a fixed off-population opponent restored 77.1 %. GAE λ 0.95 and a ±1 terminal win term were needed; a runaway reward scale broke training.
- **Kaggle sim winner** (Lux AI 2021 Toad Brigade, github.com/IsaiahPressman/Kaggle_Lux_AI_2021). IMPALA + UPGO + TD(λ).
  A KL term to a FROZEN TEACHER stabilises self-play and stops strategy cycling. Shaped reward was used only for the first 20 M steps, then sparse ±1 win/loss.
  Bigger nets were distilled from smaller teachers.
- **Recent (2025-26)**. League racing (arxiv 2605.22748): 75 % from its own checkpoint history (power-law, recency-biased), 25 % from a fixed diverse league.
  ShuttleArena (arxiv 2608.25246): broader opponent sampling delays saturation. "GAE falls short in imperfect-info self-play" (arxiv 2605.19235): sampled-action variance is large even with a perfect critic, so average over actions / expected-SARSA.
  Kaggle Lux S2 PPO self-play thread: kaggle.com/competitions/lux-ai-season-2/discussion/406791.
Common knobs: opponents = latest self + recency-weighted past pool + a fixed diverse anchor set (≥ 20 %).
Terminal ±1 win reward, with shaped/margin terms annealed away. Reward normalised by a RUNNING std. Big batches (10^5-10^6 steps).
Entropy ~1e-2→1e-3. Checkpoint to the pool every ~10 iterations or at a > 0.7 win rate vs the pool. Judge with a rating (TrueSkill/Elo) vs a FIXED reference set, never with self-play win rate.

## §2 Recipe for OUR game (RLFAST1)
- **Objective = P(win)**, which is zero-sum even though coins are general-sum.
  Per-game reward r = +1 win / −1 loss (tie 0), plus β·tanh(margin/6000) with β = 0.3 annealed to 0.1 after 20k games. The margin term only breaks ties in the credit signal.
  Normalise by a running std over the last ~20k games. Never normalise per batch, and never clip away the win term.
- **Variance control (the biggest lever here).** Shop lottery: any tile change re-rolls later shops (±25k).
  Use GROUP rollouts: K = 8 sampled rollouts per board with common random numbers (same seed/seat/town; shop CRN ON in training). Advantage = r − mean_group(r), i.e. a GRPO-style per-board baseline, plus the value head for per-dawn credit.
  Do not compare against a single greedy baseline sample.
- **Opponent mix (per game).**
  40 % latest checkpoint (self-play, mirrored seats).
  20 % past own checkpoints, PFSP f_hard = (1-x)^2 over the pool.
  30 % V-family / reacting pool (V48, V56, V57, S/pool1 36 agents + S/pool2 kernels), PFSP-weighted so V-late-volume losers get most of the games.
  10 % fixed anchors (head_940 seat, tape seats) as the anti-overfit mixture.
  No single scripted rival over 15 % of games.
- **League.** Add a snapshot every 10 updates, or when its win rate vs the pool is ≥ 0.6. Initial q = max; OpenAI-Five q-update with η = 0.01. Cap the pool at 30 by evicting the lowest q.
  Optionally run 1 main exploiter vs the current main with a periodic reset to head_940, to expose gifts before they ship.
- **Batch/optimiser.** ≥ 256 games (32 boards × K 8) = 7,680 dawns per update; minibatches of ≥ 64 games; 4 epochs; clip 0.2.
  lr 1e-4→3e-5 (warm start). Entropy 0.01→0.001. KL target 0.02-0.03, measured on the FULL batch after each epoch (not per 6-game minibatch).
  Add a KL-to-head_940 teacher term (coef 0.1, annealed) instead of relying on ZERO_BIAS 4.0. Use zero bias 1.5 plus the teacher KL.
- **Budget.** head_940 took ≈ 480k episodes, RLLOSS1 1,440 (0.3 %). Do not judge before 50k games (≈ 200 updates). Plan for 150-250k.
  With fast rollouts at ~20 games/s that is ~2-3 h on one GPU. Without that speed, do not run.
- **Acceptance (valley crossing).** No gate-driven rollback of the LEARNER.
  Gates every 20 updates only CHECKPOINT candidates. The learner keeps going unless it COLLAPSES: win rate vs the anchor set drops > 3 SE on two consecutive gates, or entropy is < 20 % of its start.
  Candidate selection at the end = the best checkpoint by pool rating.
- **Gate.** Greedy AND T = 1 sampled play vs (a) dev/held LIVE250 boards, paired vs head_940, and (b) the reacting pool (POOL1/2) + V56/V57, ≥ 300 boards.
  Report net flips with a McNemar SE and Δtheirs t. Ship bar = the usual 5 legs, gift-free (Δtheirs t < 2).
  Check the train↔eval match: the gate uses the same argmax head the file agent flies. If greedy ≠ sampled by more than 3 flips/100, train at T = 0.5 or distil the argmax.

## §3 Ranked diagnosis of `S/rlloss1/ppo_loss.py` ("moves but never wins")
1. **Reward = shop-lottery noise vs a one-sample greedy baseline.** L87 `crn=False` and L280-283: `dm = margin − m0[pick]`, where m0 is ONE greedy run (L113-118).
   A changed tile re-rolls later shops (±25k, memory "shop lottery"). Sampled play is also not greedy, so dm is mostly re-roll noise.
   24 games give maybe 1-2 real flips vs clip ±3 (±9,000 coins) of noise, so the gradient chases lucky re-rolls, which are often rival-favourable prices. Result: gifts.
2. **Per-batch std normalisation + margin-dominated reward kills the win signal.** L282-283: the win bonus (2,500/3,000 = 0.83) sits inside a ±3 clip and is then z-scored over 24 games. L286 z-scores the advantage again.
   With 0-2 flips per batch, the win term's weight is noise-scale. The objective becomes relative margin, not P(win).
3. **Fixed single scripted rival + deterministic boards = over-fitting.** L94 `P7.Pool(... KAGG3_V56 ...)`: every game is vs V56-in-sim on 500 frozen boards. The gate (L167-175) is also V56 only.
   The literature's collapse mode (2604.04983: 73 %→22 % off-pool) matches Δtheirs t 2-4: the head learns V56-sim-specific market moves that raise the rival's purse.
4. **Batch 100-300× too small, KL stop on 6-game minibatches.** L77 E = 24, L198 4 minibatches (6 games), L303 stops at the first minibatch KL > 0.01. The KL estimate from 180 dawns is noisy, so steps are near-random.
   Yet greedy drift is large (60-88 % dawns) because the argmax of 18 near-tied residual slots flips on tiny logit moves once they leave ZERO_BIAS.
5. **Train on sampled, gate on greedy.** L276 samples (T = 1, boosted temp L271-274); L168 gates greedy.
   The sampled-policy improvement does not carry over to the argmax. There is no greedy-consistent objective and no teacher-KL.
6. **Monotone accept + rollback blocks valley crossing and is noise-triggered.** L232 accepts only when held score ≥ best (46 boards, SD ≫ effect). L239-241 rolls back at dev net ≤ −3, about 1 SE of flip noise on 100 boards.
   lr halves with Adam reset, so the learner is repeatedly reset to head_940.
7. **Budget 0.3 % of head_940's** (60-80 updates × 24 = 1,440-1,920 games vs 480k). Nothing in the literature learns anything at that budget.
8. **Loss-only curriculum distribution shift** (L152-165, 75 % loss/close boards). This is fine as PFSP-like weighting, but with no self/past-self games it trains a best response to V56 on 108 boards.
9. **Action-space ceiling (lower likelihood, not excluded).** An 18-slot daily-ask residual may not reach the d20-29 volume mechanism. BESTRESP6 found a +953 robust oracle that is "unlearnable". RLFAST1's wide caps partly test this.

## §4 RLFAST1 checklist (must hold before any run is read)
1. Reward: terminal ±1 win (tie 0) + ≤ 0.3·tanh(margin/6000), running-std normalised. No per-batch z-score and no clip that caps the win term.
2. Variance: K ≥ 8 CRN rollouts per board, group-relative baseline (plus value head). Never a single greedy-baseline sample.
3. Opponents: ≥ 40 % latest self (mirrored seats), ≥ 20 % PFSP past checkpoints (1-x)^2, ≥ 30 % V-family/reacting pool PFSP, ≥ 10 % fixed anchors. No single rival > 15 %.
4. League: snapshot every 10 updates or at ≥ 0.6 win rate vs pool; OpenAI-Five q-scores (η 0.01); pool cap 30.
5. Batch ≥ 256 games/update, minibatch ≥ 64 games, KL target 0.02-0.03 on the full batch, entropy 0.01→0.001, lr 1e-4→3e-5.
6. Teacher-KL to head_940 (coef 0.1, annealed) replaces the 4.0 zero bias. Log greedy-vs-sampled flip gap every gate; if > 3/100, lower T or distil the argmax.
7. No learner rollback on gate noise. Rollback only on collapse (> 3 SE drop vs anchors on 2 consecutive gates or entropy < 20 % of start). Gates only checkpoint.
8. Budget: no verdict before 50k games; plan 150k+. Throughput ≥ 20 games/s measured before launch.
9. Gate = greedy file-agent argmax on ≥ 300 boards vs reacting pool + V56/V57 + LIVE250 held, paired vs head_940. Report net flips ± McNemar SE and Δtheirs t (gift < 2).
10. Metric of progress = rating vs a FIXED reference set (head_940, V56, V57, POOL1 sample), logged every gate. Self-play win rate is never a progress metric.
