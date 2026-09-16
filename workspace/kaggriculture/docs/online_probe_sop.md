# 线上探针 SOP（2026-09-04）

旧 SOP v4 已退役。本页只固化两件事：本地涨分不能当上线理由，以及提交后必须把官方回放拉回来。

## 1. 本地数字的身份

`quickwin_probe.py`、vendored 引擎自对局、同族 `run_eval` / `iterate_gate` 都是**灾难诊断**：

- 可以抓崩盘、饿逃、溢出、不确定性；
- 不可以当作强度、晋级或“该提交了”的证据。

round-19/20/21 的反例已经测过：本地 quickwin +1%～14% 仍提交，v13.7 本地 +1.23%（还披露 1 次饿逃），线上技能分 565.2→544.2。

## 2. 提交前

只允许这些本地门：单元/契约测试、身份链、`smoke_boot`、`build.py --check`。然后：

```bash
python workspace/kaggriculture/software/scripts/sync_online_probe.py gate
```

gate 不看 quickwin。它只问：当前最新发射轮（≥20）有没有官方 COMPLETE 采样、公开局够不够。过不了就停，不许改下一组旋钮，也不许再提交。

## 3. 提交后（固定步骤，不是可选项）

发射台账 `exports/online/roundN_ledger.json` 保持提交当下的快照，字段可以继续写 `PENDING`。完成态另写：

```text
exports/online/sampling/roundN_sampling.json
```

命令：

```bash
python workspace/kaggriculture/software/scripts/sync_online_probe.py close --round N
```

等价拆开：

```bash
kaggle competitions episodes <submission_id> --format json
kaggle competitions replay <episode_id> -p workspace/kaggriculture/references/data/online-replays/roundN
python workspace/kaggriculture/software/scripts/sync_online_probe.py ingest --round N
python workspace/kaggriculture/software/scripts/sync_online_probe.py gate
```

回放必须来自 Kaggle CLI。本地自对局顶替官方采样会被拒绝（`replays_are_local_selfplay` fail-closed）。token 过期就停，等重认证，不准拿 vendored 引擎自对局填台账。

## 4. 下一轮何时才能动代码

同时满足：

1. 本版公开回放已 ingest，sampling `status=COMPLETE`；
2. 最新一轮公开局 ≥3（止损/裁决仍按蓝图 ≥6 局看，3 局只是“看过回放再改”的下限）；
3. 下一刀旋钮必须引用这些官方局，而不是 quickwin 百分比。

比赛 bot 的种植/畜群参数不在本 SOP 里改。
