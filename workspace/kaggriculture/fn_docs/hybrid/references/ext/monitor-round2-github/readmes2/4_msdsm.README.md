# Kaggriculture: behavior cloning, self-play PPO and heuristics

Source code for a [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture) solution built by alternating replay imitation and self-play reinforcement learning. A shared Transformer chooses unit actions and market orders; rules prevent resource conflicts and wasted inventory.

The two final agents use the same **12-block, 10.23M-parameter architecture**, with different weights and controllers:

| Agent | Neural training | Inference |
| --- | --- | --- |
| **A** | Repeated BC → PPO stages | Confidence-ordered action repair, storage rules, and a search controller on the final day |
| **B** | Additional PPO with sequential action masks | The same conditional masks during training and inference; neural policy throughout the game |

The source also includes Net2Net depth growth and architecture presets for the parallel 20M family. Checkpoints, replay datasets and compiled binaries are supplied separately by the user.

**1. Training loop — BC, self-play PPO and heuristic refinement**

![BC, PPO and heuristic refinement form an iterative training loop](docs/images/overview.png)

<details>
<summary>2. Training history — chronological stages, data and environment steps</summary>

![Detailed training chronology](docs/images/training_detail.png)

</details>

<details>
<summary>3. Architecture and inference — neural network and rule-based action patches</summary>

![Network architecture and heuristic controllers](docs/images/model_detail.png)

</details>

## Contents

- [Setup](#setup)
- [Repository layout](#repository-layout)
- [Training workflow](#training-workflow)
- [Build an agent archive](#build-an-agent-archive)
- [Evaluation and small checks](#evaluation-and-small-checks)
- [Containers and Kubernetes](#containers-and-kubernetes)
- [Team contributions](#team-contributions)
- [Method and source notes](#method-and-source-notes)

## Setup

Use Python 3.12 or later. The neural implementation is JAX; the batched training environment is Rust. Search-based teachers and Agent A additionally use a C++17 planner.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[data,dev]"
```

For NVIDIA GPU training, install the CUDA extra instead:

```bash
python -m pip install -e ".[gpu,data,dev]"
```

Build the Rust environment for PPO and critic warmup. This requires [Rust 1.88+](https://blog.rust-lang.org/2025/06/26/Rust-1.88.0/) and a C/C++ toolchain:

```bash
python -m pip install ./native/engine
```

Build the search library when generating heuristic replays or using Agent A:

```bash
python scripts/build_search.py
```

This builds for the current machine. A Kaggle archive containing the planner needs a **Linux x86-64** library; use the container instructions below when developing on another platform.

The competition rules are pinned to `kaggle-environments==1.32.7`; the included Rust engine is `kagg-engine==0.3.24`. JAX and Optax are pinned to the versions used by the final training source. Inference uses FP32 on CPU.

## Repository layout

```text
configs/                         Model, BC, PPO, critic and final-agent presets
python/kaggriculture/
  observations/                  Typed tokens and opponent-inventory tracking
  model/                         Transformer, attention kernels and Net2Net growth
  actions/                       Action vocabulary, quantities and conditional masks
  data/                          Replay labels, dataset batches and heuristic self-play
  training/                      BC, critic fitting, PPO, rollouts and checkpoints
  agents/                        Greedy inference and the two final controllers
  heuristics/                    Unit-action repair, storage sales and search handoff
  search/                        Python planner wrapper, C++ search and local rules
python/main.py                   Kaggle entry point copied into generated archives
native/engine/                   Rust batch environment and Python extension
scripts/                         Data, training, evaluation and packaging commands
k8s/                             Generic manifest template
docs/                            Method, training history and operation notes
tests/                           Small CPU smoke checks
```

All commands below run from this repository root. JSON presets provide defaults; explicit command-line arguments override them. Paths in configurations are relative to the working directory.

## Training workflow

The public package uses the final observation and action schema for new runs. The [historical lineage](docs/training-lineage.md) records the competition's earlier stages, dataset sizes, and retained PPO experience. It is not a claim that every historical dataset or checkpoint is included here.

Prepare a cache from your public-replay manifests, optionally mixed with heuristic self-play. See [data preparation](docs/data.md) for the manifest format, episode-based holdouts, and all three synthetic shop scenarios.

```bash
# Random weights. A six-block bootstrap preset is also available.
python scripts/init_model.py --config configs/model/10m.json --output models/random.pkl

# Replay imitation. --initial also accepts an existing full PPO checkpoint.
python scripts/train_bc.py --config configs/bc.json \
  --initial models/random.pkl --cache data/mixed-cache --output runs/bc

# Fit only the critic while keeping the actor and shared trunk fixed.
python scripts/warmup_critic.py --config configs/critic.json \
  --policy runs/bc/final_student_jax.pkl --output runs/critic

# Current-policy self-play from the fitted model.
python scripts/train_ppo.py --config configs/ppo.json \
  --bc-checkpoint runs/critic/policy_with_critic.pkl \
  --output-dir runs/ppo --max-env-steps 100000000
```

`configs/ppo.json` is a **single-device example with 64 games per rollout**, preserving the main loss settings. It is not the changing, heterogeneous GPU allocation used during the competition. Rollout collection uses both seats; the teacher is the KL reference. The example keeps that reference fixed. The package also retains checkpoint and last-best-reference primitives for custom training schedules.

Continue PPO with the same initial policy and configuration:

```bash
python scripts/train_ppo.py --config configs/ppo.json \
  --bc-checkpoint runs/critic/policy_with_critic.pkl \
  --resume runs/ppo/latest_jax.pkl --output-dir runs/ppo \
  --max-env-steps 200000000
```

For another BC → PPO cycle, pass the PPO checkpoint as BC's `--initial`, use the new replay cache, fit its critic, and start a new PPO run. BC starts a fresh optimizer; PPO resume restores its optimizer, RNG and seed cursor.

To adapt a saved policy with Agent B's sequential masks while retaining the PPO state:

```bash
python scripts/train_ppo.py --config configs/ppo.json \
  --bc-checkpoint runs/critic/policy_with_critic.pkl \
  --resume runs/ppo/latest_jax.pkl --output-dir runs/rule-aware \
  --enable-sequential-masks --max-env-steps 210000000
```

Grow a 12-block policy into a 24-block policy, then run BC and/or PPO on the result:

```bash
python scripts/grow_model.py runs/ppo/policy_latest_jax.pkl models/grown-20m.pkl --layers 24
```

For a full PPO checkpoint at an optimizer-update boundary, `--preserve-optimizer` also grows the optimizer state. Starting a fresh PPO run from an exported policy uses fresh optimizer state. See [training and checkpoints](docs/training.md) for these distinctions and resource settings.

## Build an agent archive

Choose a checkpoint whose training matches the requested inference mode:

```bash
python scripts/package_submission.py \
  --checkpoint runs/ppo/policy_latest_jax.pkl \
  --agent-config configs/agent_a.json \
  --output artifacts/agent-a.tar.gz

python scripts/package_submission.py \
  --checkpoint runs/rule-aware/policy_latest_jax.pkl \
  --agent-config configs/agent_b.json \
  --output artifacts/agent-b.tar.gz
```

The packager checks the checkpoint's mask setting, writes a self-contained entry point, exports neural parameters, and records file hashes. Agent A includes the compiled search library; Agent B does not. These commands create local files only.

Use `scripts/export_policy.py CHECKPOINT OUTPUT` to extract parameters from a full training checkpoint. `--sequential-masks` changes the action-selection configuration for a new adaptation stage; it does not train or reproduce Agent B's weights. Load only trusted pickle checkpoints.

## Evaluation and small checks

The included smoke checks exercise configuration, a tiny random model, function-preserving depth growth and both action controllers. They do not train a model or play complete games:

```bash
python tests/test_smoke.py
```

For an explicit local match after unpacking two archives:

```bash
python scripts/evaluate.py artifacts/agent-a/main.py artifacts/agent-b/main.py \
  --games 2 --seed 0 --output artifacts/evaluation.json
```

Each agent runs in a separate process. Every seed is played with both seat assignments. Use this evaluator for compatibility and outcome checks; it does not reproduce Kaggle's container scheduling or time accounting exactly.

## Containers and Kubernetes

```bash
docker build -t kaggriculture-training .
```

The image builds both the Rust engine and the search library. CPU-only images can use `--build-arg PYTHON_EXTRAS=data`. See [container and Kubernetes notes](docs/operations.md) for mounted data, packaging and the optional Job template.

The template contains placeholders for the image, namespace and existing PVC. It has no cluster context, organization-specific registry, machine selector, credential or deployment automation.

## Team contributions

| GitHub | Contribution |
| --- | --- |
| [@morim3](https://github.com/morim3) | Neural network architecture and the 10M model line, testing the hypothesis that more self-play games lead to stronger agents. |
| [@msdsm](https://github.com/msdsm) | The 20M model line, testing the hypothesis that more parameters lead to stronger agents. |
| [@BergBuch](https://github.com/BergBuch) | Development of a strong heuristic planner. |
| [@qistripute](https://github.com/qistripute) | Rule-based action patches and replay analysis, identifying weaknesses in our evolving strategies and suggesting improvements. |

## Method and source notes

- [Training lineage and environment-step totals](docs/training-lineage.md)
- [Replay preparation and heuristic teacher data](docs/data.md)
- [Network and final-agent behavior](docs/architecture.md)
- [Training settings and checkpoint semantics](docs/training.md)
- [Source provenance](docs/source-provenance.json) and [third-party notices](THIRD_PARTY_NOTICES.md)

The organization into Python, native code, presets, scripts and documentation was informed by the [Orbit Wars solution repository](https://github.com/IsaiahPressman/kaggle-orbit-wars). The algorithms here are the Kaggriculture team's own training and submitted-agent implementations, reorganized into one package. Infrastructure-specific launchers and experiment-management scripts are replaced by explicit local commands and a generic deployment template.
