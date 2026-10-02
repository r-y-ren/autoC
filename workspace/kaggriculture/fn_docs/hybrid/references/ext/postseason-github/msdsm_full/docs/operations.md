# Containers and optional Kubernetes deployment

## Contents

- [Local container](#local-container)
- [Kaggle packaging](#kaggle-packaging)
- [Kubernetes template](#kubernetes-template)

## Local container

The Dockerfile installs the Python package, builds the Rust extension and compiles the C++ search library. It contains no credentials or reference to a private image registry.

```bash
docker build -t kaggriculture-training .
docker run --rm --gpus all --shm-size=8g \
  -v "$PWD/models:/work/models" -v "$PWD/runs:/work/runs" \
  kaggriculture-training \
  python scripts/train_ppo.py --config configs/ppo.json \
  --bc-checkpoint /work/models/initial-policy.pkl \
  --output-dir /work/runs/ppo --max-env-steps 100000000
```

`models/initial-policy.pkl` is an artifact you prepare with BC/critic fitting or export from a trusted checkpoint. The image does not contain trained weights. The host must provide compatible NVIDIA drivers for GPU training.

Build a CPU-only dependency set using:

```bash
docker build --build-arg PYTHON_EXTRAS=data -t kaggriculture-cpu .
```

## Kaggle packaging

For a Linux x86-64 planner from a development machine of another architecture:

```bash
docker build --platform linux/amd64 --build-arg PYTHON_EXTRAS=data \
  -t kaggriculture-kaggle .
mkdir -p artifacts
docker run --rm \
  -v "$PWD/models:/work/models:ro" -v "$PWD/artifacts:/work/artifacts" \
  kaggriculture-kaggle \
  python scripts/package_submission.py \
  --checkpoint /work/models/final-a.pkl \
  --agent-config configs/agent_a.json \
  --output /work/artifacts/agent-a.tar.gz
```

The resulting archive contains `main.py`, `agent.json`, `model_jax.pkl`, the Python package, a file manifest, and Agent A's search library. Runtime dependencies such as JAX must be available in the target Kaggle environment, as in the original submitted bundles. There is no runtime download or compilation.

A rebuilt planner uses the same source and compiler flags for numerical operations, but does not include the original profile-guided build profile. No claim of identical search timing is made for a new binary.

## Kubernetes template

[`k8s/ppo-job.yaml.template`](../k8s/ppo-job.yaml.template) is a single-GPU Job using an existing PVC. The user supplies all infrastructure choices:

```bash
export NAMESPACE=training
export TRAINING_IMAGE=registry.example.com/your-project/kaggriculture:latest
export WORK_PVC=training-work
mkdir -p artifacts
envsubst '${NAMESPACE} ${TRAINING_IMAGE} ${WORK_PVC}' \
  < k8s/ppo-job.yaml.template > artifacts/ppo-job.yaml
```

Inspect the rendered file and use your own Kubernetes configuration to deploy it. The template does not select or modify a context, create a namespace or PVC, mount credentials, specify a machine pool, or submit itself.

The mounted PVC should contain `models/initial-policy.pkl`; checkpoints and metrics are written under `runs/ppo`. Resource sizes and PPO rollout dimensions are examples to adjust for your hardware. Starting a new run and resuming a run are explicit choices: add the appropriate `--resume` checkpoint argument to resume.
