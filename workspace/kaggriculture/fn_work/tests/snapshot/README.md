# snapshot_tests/ —— 旧代码行为基线快照安全网（fn-ladder 阶段四）

> 建立于 2026-09-21（Linux/Python 3.14.7/pytest 9.1.1）。上游需求：
> `fn_docs/requirements.md`（R1 行为基线保持 / R2 席位错位修复 /
> R3 trimmed_mean 值序修复）。本套件对**旧代码**（software/ 全树，
> 只读）跑绿即构成 R1 安全网；两个反例文件在旧代码上以 strict xfail
> 形式"预期失败"，R2/R3 修复后 XPASS 会把套件顶红——那不是回归，
> 是"缺陷已修、该迁移了"的信号（见迁移约定）。

## 运行

```bash
# 从仓库根（<仓根>）
python -m pytest workspace/kaggriculture/snapshot_tests -q
```

- 依赖：本机已装 Python 3.14 + pytest 9.1.1 + kaggle_environments
  1.32.7（site-packages，与 vendored wheel 同版）；无网络、无 kaggle
  CLI、无 gitignored 语料依赖。
- 时长：本机约 38s（大头 = 现役 agent 自博弈完整一局 ~35s；三遍实测
  37.3-37.8s，PYTHONHASHSEED 1/7/99 各一遍全绿）。
- 运行期副作用：`__pycache__` 与 twin 引擎缓存
  `software/exports/probes/twin_fidelity/engine_cache/`（gitignored，
  与既有 software/tests 同款副作用）；不写 software/ 任何受控文件。

## 绿门定义

**全绿** = `pytest -q` 退出码 0：全部普通测试通过，且
`test_counterexample_r2.py` 与 `test_counterexample_r3.py` 中的全部
strict xfail 用例恰好 XFAIL（`XFAIL` 计为绿；出现 `XPASS` 或 `FAILED`
即红）。验收口径：连跑三遍全绿无 flake（本机 2026-09-21 三遍通过）。

## 套件地图（文件 → 钉住的 requirements 条目）

| 文件 | 钉什么 | 关键冻结值 |
|---|---|---|
| `conftest.py` | sys.path 装配（software/ + scripts/，与 software/tests/conftest.py 同法） | — |
| `test_agent_characterization.py` | **R1**（行为清单 §1 提交链）：main.py 装载的现役 agent（DTSP 开）经 kgenv.engine 自博弈整局的完成契约/终局资金/四天动作哈希/活性摘要 | seed=20260921；rewards `[75708.0, 66284.0]`；winner 0；non-PASS `[671, 679]`；d0/d6/d10/d24 双席动作 sha256 ×8（文件内字面量） |
| `test_planner_select_characterization.py` | **R1**（select.py 现行名字序裁切 + 聚合/平票/K1 守成全语义）：aggregate_scores/robust_select 固定分数字典逐值固化 | Ω=4 真名集（wheat_suppressor<winner_balanced<passive<pessimistic）；CASE_A trimmed=35.0（值序应 65.0）；悲观零效应对 60.0/60.0；K1 边际 1.5<5.0 → identity |
| `test_counterexample_r3.py` | **R3 快照反例**：名字序裁切 ≠ 值序裁切的分数集，断言值序正确结果（strict xfail）；对照断言固化名字序当前行为（保绿） | 值序正确值 65.0 / 22.5 / 55.0→62.5（悲观恢复效力）；现行值 35.0 / 60.0 / 60.0==60.0 |
| `test_counterexample_r2.py` | **R2 快照反例**：合成回放 me_seat=1 注入局，bench 恒 mine→seat0 vs v143 seated 按席位注入 | 回放真值 `[3000.0, 1570.0]`；seated 复现之；bench 错位输出 `[1570.0, 3000.0]`（互换伪影）；me_seat=0 两通道逐字节同 |
| `test_kgenv_rating_snapshots.py` | **R1**（行为清单 §2 评级面）：Elo 顺序敏感双冻结值；BT 批量顺序无关（两排列全等）+ 输出 sha256；Wilson/t/margin_stats | elo 两序 `alice 1215.263693206478 / 1215.2976013366472`；BT sha `4e230dd2…7489`；wilson(3,4)=(0.3006,0.9544) |
| `test_online_probe_gate_rules.py` | **R1**（线上台账门 fail-closed）：自对局源拒/零对局拒/缺 COMPLETE 采样拒/PENDING 拒/ref 不匹配拒/合法布局过 | 合法 payload record `3W-0L`、public_games=3；拒绝理由串逐条匹配 |
| `test_eval_contract_rules.py` | **R1**（评估契约族）：种子域隔离拒重叠、AB/BA 调度冻结、5 代历史种子黑名单（19/38/46/54/62）published 命中拒、异常局判定理由、canonical_sha256 | 调度 4 行字面量；黑名单尺寸链；`canonical_sha256({"b":1,"a":2})=d3626ac3…a772` |

## 迁移约定（fn_work/ 时期）

1. 套件整体迁入 `fn_work/tests/`（conftest 的 sys.path 指向新结构树根）。
2. **期望 R2/R3 反例 XPASS**：两文件里的 strict xfail 用例变 XPASS 会把
   套件顶红——此时把对应 xfail 装饰器删除、断言转正，并把
   `test_counterexample_r2.py` 的 bench 冻结值 `[1570.0, 3000.0]` 更新为
   seated 口径 `[3000.0, 1570.0]`；把 `test_counterexample_r3.py` 与
   `test_planner_select_characterization.py` 的"现行值/零效力"冻结值
   按值序裁切重算更新（35.0→65.0 一类）。
3. `test_agent_characterization.py` 的冻结值**不得变**（R1：重构前后
   行为逐字节不变）；若在新结构上变红，即重构改变了现役行为，须回溯
   修新结构而不是改冻结值。
4. 已知边界：DTSP 黎明规划带 0.85s 墙钟预算帽，极端慢机可能触发截断
   使 agent 冻结值漂移（本机三遍稳定；换机复跑验证即可区分）。
