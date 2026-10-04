# Training and checkpoint semantics

## Contents

- [Behavior cloning](#behavior-cloning)
- [Critic fitting](#critic-fitting)
- [Self-play PPO](#self-play-ppo)
- [Environment steps](#environment-steps)
- [Checkpoints and growth](#checkpoints-and-growth)

## Behavior cloning

`scripts/train_bc.py` runs the final replay-only objective:

```text
L = CE_unit + CE_market
    - beta_unit * H_unit - beta_market * H_market
    + alpha * (KL(initial || current)_unit + KL(initial || current)_market)
```

The final-stage defaults are `beta_unit=beta_market=0.10`, `alpha=0.05`, two epochs, learning rate `1e-4`, Adam epsilon `1e-5`, and gradient-norm clipping at 5. Cross-entropy uses valid teacher labels. Entropy and KL use active units and all ten market slots, even where an individual teacher label is ignored. The initial teacher stays frozen; BC does not train the value head.

The trainer uses one local device per process. `--batch-per-gpu` is the per-process batch; the name is retained for the GPU training interface. A single CPU device is also supported for small development inputs with `--compute-dtype float32`. Production BC loads the feature cache into host memory.

For multi-process BC, set `KAGGRICULTURE_PROCESS_COUNT`, `KAGGRICULTURE_PROCESS_INDEX` and `KAGGRICULTURE_COORDINATOR` before launching each process. The coordinator is a user-supplied `host:port`. Initialization occurs before JAX device discovery. This package does not provision those processes.

BC writes `latest_bc_state.pkl`, `final_student_jax.pkl`, optional per-epoch policies, metrics and a receipt. Reusing the same output directory resumes at an epoch boundary after checking the initial-policy and dataset hashes and the regularization settings.

## Critic fitting

`scripts/warmup_critic.py` collects fresh self-play from a fixed policy, caches the global-token features, and trains only the critic. The actor and Transformer trunk remain fixed. Training and validation game seeds are disjoint.

The example uses 64 training games per iteration, 16 validation games, GAE with `gamma=1` and `lambda=0.97`, learning rate `1e-4`, and patience eight. The historical adopted warmup stopped after 17 iterations and selected iteration nine. A new run is evaluated independently and need not stop at those same counts.

The command saves the best critic and `policy_with_critic.pkl`, which can initialize PPO directly. It verifies that the actor hash is unchanged. The separate critic artifact is also compatible with PPO's `--initial-critic-checkpoint` option when paired with its original policy.

The PPO command defaults to zero in-process value warmup because the explicit critic-fitting stage implements the adopted frozen-actor procedure. The retained `--value-warmup-max-updates` option enables an older full-model value-only warmup; its gradients also reach the shared trunk.

## Self-play PPO

The current neural policy plays both seats. Teacher weights are used for regularization; this is not a rollout batch consisting only of games against the teacher.

| Setting | Public default |
| --- | --- |
| Reward | Terminal win / draw / loss: `+1 / 0 / -1` |
| Discount / GAE | `gamma=1`, `lambda=0.97` |
| PPO clipping | `0.2` |
| Epochs over each rollout | `1` |
| Value objective | Huber, weight `2` |
| Teacher regularizer | `KL(teacher || policy)`, coefficient `0.2` |
| Unit / market entropy coefficients | `0.0015` each |
| Optimizer | Adam, epsilon `1e-5`, gradient-norm clip `5` |
| Base learning rate | `5e-5` |
| LR schedule | 240 optimizer-step warmup; 150,000-step linear decay; minimum multiplier `0.25` |
| Training precision | BF16 activations with FP32 numerical paths where required |
| Rollout example | 64 complete games, both seats |

The summed unit and market log probabilities form the joint action probability. Minibatches preserve paired seats for the zero-sum critic. The trainer retains gradients across microbatches to process full-game segments without placing the entire rollout on the GPU at once.

The public launcher supports a single host with one or multiple local devices. Set `--data-parallel-devices N`, and optionally `--data-parallel-rollout`, for local data parallelism. Keep these relationships valid:

- `inference_batch_size = 2 * games`.
- `games` is divisible by `segments_per_minibatch`.
- Every microbatch and per-device shard contains complete seat pairs.

The competition additionally used elastic multi-host scheduling and mixed GPU types. The public commands retain the model, objective, masks and numerical primitives; the original cluster scheduler and environment-specific launchers are not included. The included preset makes no throughput or convergence guarantee on a different GPU arrangement.

For Agent B, `--enable-sequential-masks` enables the same sequential masks in sampling and log-probability recomputation. When used with `--resume`, this permitted mask transition retains the optimizer and seed cursor. Other model changes still fail resume validation. The competition subsequently varied learning rate and teacher KL; its final KL-free portion was only two updates. The public preset does not silently recreate those manual scheduling changes.

## Environment steps

One decision by either player is one environment step. A complete training game contains 719 decisions per seat:

```text
1 game = 719 × 2 = 1,438 env steps
64 games in the example rollout = 92,032 env steps
```

The PPO JSONL metrics record `rollout_env_steps` and cumulative `env_steps`. The cumulative value starts at the first PPO rollout in that run, excluding critic fitting, and survives normal resume. It does not include ancestors when starting a fresh run from exported weights.

`--max-env-steps` stops after a complete PPO update. It can exceed the requested budget by less than one rollout. Resuming with a larger budget continues from the saved cursor. `--max-inner-updates` provides a separate total update limit; whichever stopping condition is reached first ends the run.

Older full checkpoints without `ppo_seed_start` begin the public env-step counter at the resumed seed cursor. Historical lineage totals are reconstructed separately and should not be inferred from that newly initialized counter.

## Checkpoints and growth

| File | Contents / purpose |
| --- | --- |
| `latest_bc_state.pkl` | BC parameters, optimizer state and completed epoch |
| `final_student_jax.pkl` | Policy parameters after BC |
| `critic_best_jax.pkl` | Best critic combined with the frozen actor, plus source-policy identity |
| `policy_with_critic.pkl` | Inference-compatible parameters after critic fitting |
| `latest_jax.pkl` | Full PPO state, optimizer, reference policy, RNG and seed cursor |
| `policy_latest_jax.pkl` | PPO parameters for inference or a fresh training stage |

Checkpoint writes are atomic. Full checkpoints are tied to their initial-policy hash and training configuration; replacing a file with a different starting policy does not silently resume the old run. Keep the original initial-policy file when resuming.

Net2Net depth growth inserts blocks whose attention and FFN output projections are zero. Existing blocks keep their parameters and order, so the initial grown network computes the same policy. The standard tool grows depth at fixed width and FFN size. `--preserve-optimizer` additionally grows a full checkpoint's reference policy and zero-initializes the new optimizer entries while preserving existing moments and counters. It requires an empty gradient-accumulation boundary.

The separate 29-block / FFN-1,072 preset describes the further-grown branch's architecture. The depth-only CLI does not perform that branch's FFN-width migration.

All pickle files are local trusted artifacts. Weights, replay data and optimizer state are ignored by Git and are not part of this source release.
