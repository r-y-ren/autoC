# kaggriculture

Our agent for Kaggle's [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture/overview)
simulation competition, with the full record of how it was built.

The agent peaked at a rating of 2,858 and finished the submission period at 2,230
(rank 330 of 10,246, provisional until the final evaluation ends). It is not a
winning solution. The value of this repository is the exact simulator, the
evaluation method, and a build log in which about 190 experiments are rejected
with numbers and a mechanism-level reason.

Start with the write-up: [`docs/strategy/2026-10-01-kaggle-writeup.md`](docs/strategy/2026-10-01-kaggle-writeup.md).

## What the agent is

The submission is pure numpy plus one small C kernel. It is deterministic and
plays a full 720-step game without errors.

| Layer | Where | What it does |
|---|---|---|
| Policy | `core/policy.py`, `core/brain.py`, `submission/theta.npy` | A ~7.7k-float network, trained by OpenAI-ES, read once per in-game day. It sets the day's targets: crew, plantings, animals, forward buys, fertilizer deferral. |
| Day planner | `core/plan.py` | About 15.8k lines. Turns the targets into the engine's action rows. Written against an array module, so the JAX trainer and the numpy submission run the same code. |
| Residual head | `core/residual_head.py`, `submission/residual_head.npz` | A PPO head trained in self-play that adjusts the planner's choices. |
| Crew router | `agent/route_vrp.py`, `agent/route_vrp_c.c` | A vehicle-routing search at dawn that assigns tiles to workers and saves hires. |
| Price projector | `core/projector.py`, `agent/tell.py`, `core/opp_supply/` | Classifies the rival's family from its first-hour cash and uses that family's supply curve when projecting prices. |
| Simulator | `sim/` | A JAX re-implementation of the environment, checked field by field against `kaggle_environments`. Training only. |
| Trainer | `es/` | OpenAI-ES with common random numbers and antithetic sampling. Training only. |

Features are `NAME_ON` switches in `plan.py`. Most default to off: a rejected
feature stays in the code without changing shipped behaviour.

## Layout

```
src/kagg3/        the library: spec, core, agent, sim, es
submission/       the final upload, unpacked (main.py + kagg3/ + weights)
scripts/          train, package, evaluate, replay tools
tests/            the test suite (see "What is not included")
S/pipeline/       the train / judge / ship / watch wrappers we used
artifacts/        opponent supply curves, plus an early ES champion (not the shipped weights)
docs/             design notes, planner designs, pipeline guide
docs/strategy/    the build story and ~1,150 dated working notes
```

## Run it

Tested with Python 3.11 and `kaggle-environments==1.32.7`.

```bash
uv venv --python 3.11 && uv pip install -e '.[dev,cpu]'
```

Play one game against the built-in starter agent:

```python
from kaggle_environments import make

env = make("kaggriculture", configuration={"seed": 20260821})
env.run(["submission/main.py", "starter"])
print([a["reward"] for a in env.steps[-1]])   # [135888.0, 3697.0]
```

Rebuild the submission archive from source:

```bash
python scripts/package_submission.py        # -> dist/submission.tar.gz
```

The archive is byte-reproducible. Built from this tree it has md5
`1133b789592a586aaecb9683c56ea3c3`, which is the file we uploaded last.

Run the release-gate tests:

```bash
pytest tests/test_submission_runs.py tests/test_gates.py
```

In this repository that gives 15 passed and 2 failed. The two failures need a
directory that is not included (see below).

## Reading the docs

- [`docs/strategy/2026-10-01-kaggle-writeup.md`](docs/strategy/2026-10-01-kaggle-writeup.md):
  the short version. Architecture, judging method, timeline, where we got stuck.
- [`docs/strategy/BUILD-STORY.md`](docs/strategy/BUILD-STORY.md): the long
  version. Every ship and every rejection, in order, with numbers.
- [`docs/DESIGN.md`](docs/DESIGN.md): simulator and policy design decisions.
- [`docs/PIPELINE.md`](docs/PIPELINE.md): how the train / judge / ship / watch
  loop was run.
- [`GOAL.md`](GOAL.md): the original goal. It says "no hand-written strategy".
  That stopped being true early on, and the document is kept as history.
- `docs/strategy/`: dated working notes, one per experiment. They are unedited.
  They use internal names for experiments and refer to many directories under
  `S/` that are not in this repository.

## What is not included

This is a cleaned export of a private working repository, published as a single
commit.

- **Experiment directories.** The original had about 800 directories under `S/`
  with results, logs and scratch scripts. Only `S/pipeline/` is here.
- **Opponent data.** Replays, action tapes cut from other teams' games,
  leaderboard snapshots and copies of other competitors' notebook agents are
  left out. `scripts/make_tape_actions.py` and `scripts/tape_opponent.py`
  rebuild tapes from replays you download yourself.
- **Old packages.** Earlier submission tarballs are left out. `submission/` is
  the final one.
- **Git history.** Many tests pin behaviour against earlier commits with
  `git archive` (`tests/_pin.py`). Those commits do not exist here, so these
  tests fail. Tests that read `S/` or the tapes fail too. The suite is included
  as documentation of what was checked.

Personal details were replaced with placeholders: `remote-host` for the
training machine, `/home/user` for home paths, and `OurTeam` for our team name.
Scripts that take `--ours` default to `"OurTeam"`; pass your own team name when
reading your replays.

## How this was built

Most of the code and experiments were produced with AI coding agents (Claude
Code): one time-boxed agent per mechanism, run in parallel, each ending in a
written result. A second model reviewed results. A human set direction, made the
ship decisions and did every upload. The working notes are the output of that
process.

## Licence

Apache License 2.0. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

`agent/v56kernel.py` is third-party code from the public "V56" Kaggle notebook
lineage, also Apache-2.0, with its attribution notices kept in the file. It is
part of the uploaded package, but its trigger never fires in the final configuration.
The simulator re-implements the Kaggriculture environment from
`kaggle-environments` (Apache-2.0).
