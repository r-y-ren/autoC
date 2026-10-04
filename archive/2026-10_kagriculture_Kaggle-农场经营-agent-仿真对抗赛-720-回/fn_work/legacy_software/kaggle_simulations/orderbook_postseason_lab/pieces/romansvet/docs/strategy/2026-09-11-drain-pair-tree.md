# drain-pair: the flow179 tree with the promoted pair ON

*2026-09-10. Prepared, not launched.*

flow179 trains in `drain-gene` (N_PARAMS 7053), the only tree that carries the
`winfirst` real-gate metric. The promoted pair — `TAIL_FILL_ON`,
`BANK_BEFORE_LOT_ON` (`docs/strategy/2026-09-10-ship-pair.md`) — was flipped on
`ship-pair`, off `arms-next` (6789). flow180 needs both, so the flip moves to a
tree of its own.

## 1. The branch

Worktree `.claude/worktrees/drain-pair`, new branch `drain-pair` off
`4a7a885` (the `drain-gene` worktree HEAD; there is no branch of that name —
that worktree is detached). Two cherry-picks, **both clean, zero conflicts**:

| picked | new hash | what |
|---|---|---|
| `eff3310` | `2acfe9a` | the flip: `plan.py` defaults + 5 pin-module fixtures |
| `b9b732b` | `36deffe` | the pair pinned off in 21 further digest modules |

`plan.py:1871 BANK_BEFORE_LOT_ON = True`, `plan.py:2615 TAIL_FILL_ON = True`.
`policy.N_PARAMS == 7053`, so the gene tail survived the picks intact.

## 2. Tests (the two the brief names, not the suite)

```
pytest -q -k "byte_identical or is_the_off_plan" tests/   43 passed, 1688 deselected
pytest -q tests/test_forward_gene.py                      19 passed
```

43/43 is the same digest surface the ship-pair doc closed, now closed in the
drain-gene planner too. Run with the repo venv (`.venv/bin/python`); the system
python has no jax and collection errors.

## 3. Remote stage

`user@remote-host:~/stage_drainpair/`, built the way `~/stage_draingene`
was: `rsync -a --delete --exclude __pycache__ --exclude .pytest_cache
src scripts tests vendor pyproject.toml`, then
`ln -sfn /home/user/stage_tape/artifacts ~/stage_drainpair/artifacts`.
**`artifacts` is a symlink and was never copied** — so the init theta
`artifacts/kagg2_games/thetas/flow172_g170c.npy` (27,284 B) is already there,
shared with every other stage.

Verified on the host, inside `~/kagg3/.venv`:

```
cd ~/stage_drainpair && PYTHONPATH=src python -c "import kagg3.core.plan as p; print(p.TAIL_FILL_ON, p.BANK_BEFORE_LOT_ON)"
True True
python scripts/train.py --help | grep -c winfirst   ->  7
```

## 4. The launch

`~/launch_flow180.sh` (md5 `e7298bf0c91c29720bb8ab87e8640f63`, copy at
`docs/strategy/2026-09-11-launch_flow180.sh`) is `launch_flow179.sh` with a new
header and, below the header, **exactly four changed lines**:
`cd ~/stage_drainpair`, `mkdir -p artifacts/flow180`, `--run flow180`, and the
two `artifacts/flow180/train.log` redirects. Every other option is byte-equal —
same init theta, same `--seed 270`, same 48-opponent `winfirst` gate. `bash -n`
clean locally and on the host.

```
sed -i 's/^CUDA_VISIBLE_DEVICES=0/CUDA_VISIBLE_DEVICES=<gpu>/' ~/launch_flow180.sh   # line 18
nohup bash ~/launch_flow180.sh &
```

The GPU is set *in the file* (line 18), not by an env prefix -- the inline
assignment on the `python` line wins over one. It is left at `0`, and **nothing
was launched.**
