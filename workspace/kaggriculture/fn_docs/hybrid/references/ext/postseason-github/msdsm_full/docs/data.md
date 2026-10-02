# Replay preparation and heuristic teachers

## Contents

- [Public replays](#public-replays)
- [Label construction](#label-construction)
- [Heuristic self-play](#heuristic-self-play)
- [Mixed cache](#mixed-cache)

## Public replays

Supply downloaded replays locally. No credentials or replay datasets are included, and the preparation commands make no API calls.

Create a JSONL index with one row per teacher seat. Paths are relative to the index file. A single game can contribute two rows when both players are teachers:

```json
{"path":"replays/game-1.json.gz","episode_id":1,"seat":0,"submission_id":11111111}
{"path":"replays/game-1.json.gz","episode_id":1,"seat":1,"submission_id":22222222}
```

The replay must be the full JSON object with `module_version: "1.32.7"` and 720 recorded states. The index names the intended teacher explicitly; it does not guess a teacher from the winner or leaderboard position. Uncompressed `.json` and compressed `.json.gz` input are accepted.

```bash
python scripts/index_replays.py data/teacher-seats.jsonl --output data/replays
python scripts/prepare_replays.py \
  --manifest data/replays/11111111/manifest.json \
  --manifest data/replays/22222222/manifest.json \
  --cache data/public-cache --workers 4
```

`prepare_replays.py` verifies the replay SHA256 and game length. It emits compressed feature/label arrays and an `index.json` describing each trajectory. An optional repeated `--submission ID` restricts allowed teacher submissions.

Validation uses an episode hash and approximately 10% of public games. Both seats of a game receive the same split. Duplicate episode/seat rows across teacher manifests are deduplicated.

## Label construction

Each `observation[t]` is paired with the recorded `action[t+1]`, yielding 719 decisions per full teacher trajectory. Unit and market labels exclude invalid or unexecuted actions using the pinned rule resolver. SELL labels use the executed absolute quantity, from 1 through 100, rather than the requested quantity.

The opponent-inventory tracker advances through observations with the teacher's previous action, so cached input matches inference. Padding labels use `-100` and are ignored by cross-entropy. Entropy and teacher KL still apply to real units and all ten market slots at those observations.

The cache contains `features[719,264,124]` and `labels[719,30]` for each trajectory. Each label row contains up to 20 unit labels and ten market labels. These large generated files belong under the ignored root `data/` directory.

## Heuristic self-play

The targeted scenarios were chosen after inspecting policies trained with BC and PPO and observing weaknesses in tomato-heavy and highly skewed shop configurations. We improved the heuristic planner in response, generated demonstrations for these cases, then mixed them into the next BC stage alongside public replays. Standard-shop games were included as a third group. This data-generation role is separate from the heuristic corrections and search used at inference.

Compile the planner, then generate the three shop scenarios:

```bash
python scripts/build_search.py
python scripts/collect_search_replays.py --output data/search-selfplay \
  --per-group 100 --workers 4 --seed-start 51010000
```

This is an explicit data-generation job and can take substantial time. It is not run by setup, packaging or smoke checks.

| Group | Games in the final BC recipe | Shop distribution |
| --- | ---: | --- |
| `normal` | 100 | Standard distribution |
| `tomato` | 100 | At least two tomato-related shops |
| `extreme` | 100 | At least three shops of the same type |

Each game is heuristic-versus-heuristic and contributes both seats. Shop overrides are applied at the normal unlock schedule for teacher generation only. Evaluation uses the standard environment distribution. The collector keeps separate agent state for each seat and writes provenance and checksums with the replay files.

## Mixed cache

Combine public data with both seats of the synthetic games:

```bash
python scripts/mix_replays.py --public-cache data/public-cache \
  --selfplay data/search-selfplay --output data/mixed-cache \
  --holdout-per-group 10 --workers 4
```

Synthetic holdouts are chosen by an episode/seed hash: ten complete games per group in the final recipe, with both seats held out together. The mixer checks unique synthetic seeds and the shop-stratum constraints. Smaller collections are supported when each group still has training games after its requested holdout.

The final competition BC cache contained 849 public teacher trajectories and 600 synthetic trajectories: **1,449 trajectories total**, including validation. The released commands can build the same type of dataset; the historical replay files themselves are not bundled.
