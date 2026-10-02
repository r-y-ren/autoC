# TRAINREVIEW1 (2026-09-29 09:28-10:28Z): why every training line was flat or lost, and what to change

Read-only audit for the 09:28Z user order ("free GPUs ... analyze the training setup, ES theta, RL head, HRM/RLM"). Nothing launched or killed.
Numbers and their sources: `S/trainreview1/audit.md`. ESBAND2 statistics: `S/trainreview1/es_stats.py` -> `logs/es_stats.txt`.

## Verdict
- **No training line ever optimised the thing we lose.** ES used open-loop tapes, PPO used V56/V57 scripts plus 57-71 % self-play, BC used teacher tokens. The reacting programme rival exists only since 09-28, and it has never been a fitness.
- **Its win term is useless as a reward.** PFS beats the reacting judge rival 79/80 (ctrl, margin +34.7k), 75/80 (g0capsfix, +25.0k) and 80/80 (big, +45.8k).
  - So a closed-loop reward must be OWN coins (dours vs flood), with a margin >= 0 guard vs g0capsfix.
  - Margin alone rewards denial, and denial does not transfer live (PRICEFAITH1, PRICEGAP1).
- **The GPUs are not the binding resource for any PFS-based body.** PFS runs in Python at 5.5-8.75 s per game per core, on 8 remote cores.
  - In the CPU judge, the clone rival's numpy forward takes ~50-60 % of the time (170 s vs PFS 110-175 s per 20-game batch).
  - The GPU can take that forward, a 2x gain. It can also run JAX bodies at 1.4-2.5 games/s, but every JAX body today is 31k behind PFS.
- **The capacity and the architecture were never the limit.** The limits were:
  - the objective;
  - the reach of the action space: the RL head cannot act on d0, where invariant 2 locates the gap;
  - the search dimension vs population size.

## 1. ES (theta7659, ESBAND2)
- **What theta parameterises.** 7,692 floats. 6,779 live genes feed brain.decide:
  - the per-product encoder (grow/sell scores = the crop and animal mix, genes 0-2497);
  - the global trunk;
  - the macro head gb2: land bias, animal sharpness, dev_frac, animal share, crop sharpness;
  - the aux land/dev heads, the drain features, the crew and animal-mix heads, and the production-forecast / forward-value heads.
- **The decode quantises (`_qfloor`, largest remainder).** One gene at +1 sigma (0.002) moves 0/4 seats. A full +1 sigma draw moves 69/71 seats and costs -3 flips.
  - So the landscape is flat per gene and chaotic jointly. At this sigma the ES "gradient" is the sign of plan re-rolls, not a slope.
- **Recipe.**
  - Population: 16 antithetic candidates on one 71-seat half; 1,298 episodes and 3,085 s per generation.
  - Fitness: 1.5 x flip + dmargin/1000, share-weighted MELON .565 / V .348 / ZERO .087, paired vs theta7659 on the recorded TAPE seats (open loop).
  - Accept: on 142 band seats + dev20.
  - Dimension vs samples: 16 samples in 6,779 dimensions give a gradient-estimate cosine of ~0.05 even without noise.
- **Noise vs step.**
  - Within a generation, the member net sd is 1.55 flips per 71 seats.
  - Step candidates on 142 seats: mean -1.31 flips, sd 2.66, best +3.
  - Step F: mean -0.175, sd 0.435 (the mean is t -2.7 BELOW the base). The max of 45 iid draws from that spread would be ~+0.78; the best F is 0.355.
- **ESBAND2 trajectory (36-h run).**
  - 45 generations over 38.6 h, 2 accepts (g12 F +0.284, g18 F +0.355).
  - The best is W 91 -> 94 on tapes (+3 of 142), with dours -14 (t -0.14) and dtheirs -244 (t -2.31): tape denial.
  - **Since g18: 27 generations and 23.7 h with no gain.** All 27 steps score below the centre (mean F -0.095 vs 0.355), and frac_pos fell from 0.21 to 0.04.
  - **FLAT.** It trains against tapes, which FIRELIVE1 and REACTCLONE1 showed do not transfer: the tape read overstated the fire 9x with the wrong sign.
  - Cost on the local box: 2 workers (pids 25258/25261, nice 19), ~2.4 cores and 11.8 GB RSS, while the box sat at load 37.
  - Recommendation for the owner: judge cand_g018 closed loop once (`judge.sh --rival g0capsfix`, ~13 min), then stop it. Not done here, per the kill ban.
- **What to change.**
  - Fitness: paired closed-loop OWN coins vs flood, margin >= 0 vs g0capsfix, accepted on held-out m76.
  - Genes: <= 200 decision-level numbers, not 6,779 trunk weights.
  - Sigma at the decode quantum.
  - Population >= 2x the dimension over the run (antithetic pairs; CRN is free because the judge is bit-exact).

## 2. RL head (head_940)
- **Structure.** MLP 64 -> 64 -> 64 -> 92 plus a value head; 14,365 params.
  - Inputs: 64 order-free scalars (day, both purses, own crop/animal counts, free tiles, shed, seeds, market inventory, prices, shops, opponent commitment). No history.
  - Outputs: 6 categoricals, applied as a clamped residual on brain.decide's macro once per dawn on **d1-29 only** (d0 is pinned):
    - d_plant 5 x 9 values (-4..+4);
    - d_animal 3 x 5 (-2..+2);
    - d_hire 5 (-2..+2);
    - hold 9 x 3 (x0, x0.5, x1).
- **PPO history.**
  - head_940 = flow257, 50 % self-play, pool 4, reward WIN + margin/1e4, ~68 games per update. Result: +312 coins/board (t 4.26), flips +0/-1.
  - RLFAST run2 followed the self-play guide: sign(m) + 0.3 tanh(m/6000), K 8 CRN groups, 320 games per update, teacher-KL, entropy 0.01 -> 0.001. Its opponent mix: self-play 57-71 %, V56/V57 scripts 19-21 %, no loss bank.
    - 61,440 games: V56 net -3 -> -1, slope +0.048 +/- 0.017 flips per 1k games, gift t 2.3-2.6, at 0.47 games/s.
- **Why flat.**
  1. Its rivals never included the programme family, the only family PFS loses to. Against V56, PFS wins 91 %, so 1.9-4.0 % of boards are discordant and the win term is sparse.
  2. The action space cannot reach the gap. d0 is pinned and a delta is at most 4 tiles, while the gap sits in the d0-9 purse and herd (invariants 2 and 6). BESTRESP6's +953 oracle was already "unlearnable".
  3. One terminal reward covers 29 decisions, at 0.47 games/s.
- **Could the reward be the closed-loop margin/win vs the reacting rival?**
  - Not the win term: it is near-saturated (PFS 75-80/80; 5 losses per 80 games is too sparse for a 16-candidate ES).
  - Not the margin: it pays denial (GUARD=0 gave own +4.7k closed loop and 0 on live27).
  - **The own-coin delta vs flood, with a margin guard, is the right reward.** The throughput is not there for PPO: PFS bodies give <= 2.5k games/h on 6 cores even with the GPU rival, so a 50k-game verdict takes 20+ h.
  - It is enough for ES on a few hundred head numbers (experiment 2, ESHEAD-CL).

## 3. BC clone (r5a3)
- **Architecture (model3, 3,514,886 params).** A per-unit ego 19x19 crop (both farms' 28 planes + self + 2 coordination planes):
  - conv 48-64-64 -> 256, joined with global 154 -> 128 and a unit vector of 121 (own previous token + earlier units' tokens this step);
  - -> token 44 -> qty 45;
  - a market head of 21 keys x 45 quantity classes;
  - units decoded sequentially within a step.
  - **Context = one step.** The only memory is the unit's own previous token. There is no day plan and no price or purchase history.
- **Data and loss.** 3,116 top-team seat-episodes (warm r5a2), 30k steps (725 s on GPU0). Loss CE(token) + CE(qty) + 3 x CE(market), AdamW 1e-3 cosine.
- **Held-out accuracy rose while coins fell.**
  - r5b had the best held-out scores (.8655 / .9288 / .5244) and went -4 flips, dours -3.1k (t -2.6).
  - 4x batch: own -3,719 +/- 592, below r5a3 in 15/16 checkpoints, already by 2,500 steps.
- **Why.** Token accuracy weights ~14k unit decisions per game equally, but the coins sit in a few hundred plan-level choices.
  - The labels are a 4-team mixture, and the argmax of a mixture is none of the teams.
  - A Markov net cannot carry the programme's day plan, so its first plan error puts it off-manifold, where it executes 22 % fewer units.
  - Result: -22.9k vs its own teacher, and PFS - r5a3 = 31.0k closed loop. Three ExIt rounds lost -3.0k to -13.5k.
- **DAgger needs an expert that labels arbitrary states.**
  - For the programme: none exists (tapes only).
  - For PFS: the Python planner can label them, but it is STATEFUL. The Runtime builds the day plan at hour 0 and keeps a planted[30x5] ledger, an overflow ledger and a VRP fill.
    - So its labels are consistent only at DAY granularity: roll the learner in to dawn d, then PFS plays day d.
    - A Markov student cannot see PFS's hidden day plan. **It must be given PFS's dawn macro/plan targets as input.**
  - Label cost = PFS's own cost (~7 core-s per game): about 2 core-h per 1,000 games. Training 30k steps takes ~12 min on GPU0.

## 4. HRM and RLM
| reading | addresses our failure? | cost | EV by 09-30 12:00Z |
|---|---|---|---|
| **HRM = Hierarchical Reasoning Model** (Sapient 2025, arXiv 2506.21734): two coupled recurrent modules (slow H, fast L), 1-step gradient, ACT halting; 27M params trained on ~1k supervised puzzles | Only "missing history", and only for the clone. Covariate shift, the teacher mixture and the objective remain; ARC Prize's ablation credits the outer refinement loop, not the hierarchy | 6-10 h engineering (recurrent state in the fast-env harness + truncated-BPTT BC) + 2-4 h training | **0**: the clone is 31k behind PFS. The best in-rollout bound (BCBODY11, +8.6k on 14 % of samples) leaves it >= 22k behind |
| **HRL = daily-plan module over an hourly controller** | PFS already IS this: brain.decide (daily macro) -> plan.build_day / route_vrp (hourly), and head_940 is the daily-level learner. What failed is the high level's training signal | 0 new | = experiments 1-2. Its one real use: condition DAGGER1's hourly student on PFS's dawn plan |
| **RLM = Recursive Language Model** (Zhang & Khattab 2025: an LLM recursing over its context in a REPL) / recursive refinement nets (TRM 2025) | No: an LLM cannot run 720 steps in a Kaggle agent; TRM is the HRM verdict | n/a | **0** |
| **RLM = model-based RL with the exact env as the model** | Yes: this is the real lever. The bit-exact env + reacting rival = a planning model; it was used as a JUDGE only, never as the optimiser's fitness | Offline = experiments 1-2. Online (decision-time rollouts) is infeasible: a PFS + clone-rival rollout costs ~15 CPU-s (7 s PFS + 8.5 s rival), so 20 d0 rollouts take ~300 s against the 60 s overage | = experiments 1-2 |
| **Reward learning (IRL from 6,553 programme seat-episodes)** | Would fix the objective in principle | Needs an RL optimiser at >= 50k games | **0** by the deadline |

## 5. Ranked GPU experiments that can yield a judged body by 09-30 12:00Z
**Shared prerequisite (1-2 h): RCGPU-PFS.**
- Move the rival's forward in the lockstep judge (S/judgerival1/rcr.py / reactclone1 rc.py path) to GPU1, using the rcgpu JAX forward.
  - It is bit-exact: jax-GPU = numpy = the kaggle engine, 719/719 actions (BCSIM1).
- Keep PFS on 4-6 remote CPU workers.
- Expected speed: ~0.4-0.7 games/s (80 games in 2-3 min) vs 0.11 games/s today.
- Gate: 8 games identical to judge.sh rows.
- The remote cores are shared with MELONPRE1, DRAWREACT2 and VID, so the rates below assume 4 workers.

| # | experiment | hypothesis | exact change | data / compute | wall | proving read | stop rule | P(pass) |
|---|---|---|---|---|---|---|---|---|
| 1 | **CLSEARCH1**: joint closed-loop search over PFS's d1-9 knobs, with d0 frozen (invariant 2) | Every d1-9 knob was probed one axis at a time; no joint search on a reacting fitness exists (BRAINSTORM1 candidate 5) | Integer vector over the existing switches: HERD_PLAN floors d5/d9, feed-first reserve, sheep-first order, animal-buy day (BRAINSTORM2's switches), LAND_DAY Q3, CROP_DAY, fertilizer bar + gb2[1,5,6,7] / gb5[1,2] biases at +/-1 quantum. Successive halving: ~120 cells x 8 games -> top 16 x 80 -> top 3 x 152 held-out | ~3,000 games (960 + 1,280 + 456 + 240 flood) | 2 h build + ~2-3 h search on shared CPUs | same as 1 | rung B: no cell with m40 own >= +1.5k and margin >= 0 -> NONE | ~5-10 % (depends on BRAINSTORM2's switches existing) |
| 2 | **ESHEAD-CL**: closed-loop ES on head_940's output biases, by day window | head_940 is a good structure trained against the wrong rivals; it already has d_animal / d_hire / d_plant on d1-9 (the BRAINSTORM2 open line). Prior art against it: ESHEAD flow267/268 searched the same b3 (74 effective dimensions) for 150 generations on 80 % tapes / 20 % head_940 and stayed flat (BAND2 +46 t 1.40, fresh BAND3 +15 t 0.32). New here: the reacting programme rival, the own-coin fitness and the d1-9 window | `S/actionrl/head.py numpy_fn`: optional `b3w` [2, 92] added to b3 for d1-9 / d10-29 (absent = byte-identical). Genes = 184, init 0, sigma 0.5 logit (the no-op bias is 4.0) | Candidate = an npz via RESIDUAL_HEAD. 8 antithetic pairs x 40 games (20 m40 boards x 2 seats, alternating halves) = 640 games per gen, ~25 min. Fitness = paired own vs flood + 0.5 x margin vs g0capsfix | 2 h build + ~14 h = ~30 gens | Best centre on m76 held-out (152 games): own >= +2k (t >= 3) AND margin >= 0 vs g0capsfix, flood dours >= 0, then live27 faithful dours >= 0 | 10 gens with no m40 centre gain > +1k, or frac_pos < 0.1 for 5 gens -> CLOSED | ~3-5 % |
| 3 | **DAGGER1** (running in parallel): distil PFS into a JAX student by day-granular DAgger with the Python planner as the expert, then ES/PPO on the GPU vs the reacting rival with an own-coin objective and a loss bank | A GPU-speed PFS makes RL throughput real. The closed-loop JAX-vs-JAX lane measures 0.27 games/s (80 games in 5 min); BCSIM1 measured 1.4 games/s at N=256. That is ~15-70k games in 14 h, i.e. at most RLFAST's flat 61k | Student = model3 + PFS's dawn macro/plan targets as global input (hidden plan state). Roll the learner in to dawn d; a fresh PFS Runtime (planted ledger rebuilt from the tiles' planted_day) plays day d, and its actions are the labels. Pin SAFETY_S 1e9 / REPAIR_MS 1e7, because the router's wall-clock budgets otherwise make the labels non-deterministic. 3-4 rounds | ~1k games (~2 core-h) of PFS labels per round, 12-min trains on GPU0, rcgpu judge 80 games in 5 min | Stage 1 ~6-8 h to a parity read; stage 2 ~14 h | Stage 1: student within 2k of PFS closed loop on m40 (the BC line's best ratio was 0.852 = -15k+). Stage 2: same bar as 1 | Stage 1 parity worse than -5k after 3 rounds -> stop before RL | **<= 2-3 %** by the deadline (P(parity by ~17Z) ~25 % x P(RL gain >= +2k in ~14 h) ~10 %). An investment with no ship value before 09-30 12:00Z |

- **Order:** RCGPU-PFS first. CLSEARCH1 then runs as soon as BRAINSTORM2's d1-9 switches exist. ESHEAD-CL needs no planner switch and fills the CPU workers until then. Both use the GPU1 rival forward.
- DAGGER1 keeps GPU0. Its PFS labelling must be capped at 2 CPU workers, or it starves experiments 1 and 2: PFS is the CPU bottleneck in all three.
- Filler (not top 3): closed-loop reads of ESBAND2's cand_g018 / g039 / g045 (3 x 13 min CPU), P ~2 %.

## 6. What to stop and what to change, per line
- **ES:** change the fitness to closed-loop own coins with a margin guard, the genes to <= 200 decision-level numbers at the decode quantum, and the population to >= 2x the dimension over the run. ESBAND2 as run is flat. Read cand_g018 closed loop once, then stop it (the owner's call).
- **RL head:** keep head_940. Retune it only by ES on its day-windowed output biases (ESHEAD-CL). A PPO verdict (>= 50k games) is not reachable by 09-30 12:00Z at PFS-body throughput.
- **BC clone:** stays CLOSED (BCBODY11). The only BC that can still be built by the deadline is the distillation of PFS (DAGGER1), with the dawn plan as input.
- **Architecture (HRM/RLM):** no new architecture addresses covariate shift, the tape/V56 objective or the saturated win term. The exact env is already the model; use it as the optimiser's fitness.

## Files
- `S/trainreview1/audit.md`: the numbers ledger with sources.
- `S/trainreview1/es_stats.py` and `logs/es_stats.txt`: the ESBAND2 trajectory statistics.
- `logs/esband2_ps.txt`: the ESBAND2 process cost.
- `logs/param_counts.txt` and `logs/head_shapes.txt`: r5a3 and head_940 sizes.
- `logs/remote_status.txt`: remote GPUs and CPUs at 09:31Z.
- `checkpoint.txt`.
