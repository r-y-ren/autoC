# 第 11 轮「战之野」赛场协议

这是后续迭代的评测设施，不是新参赛智能体，也不代表线上分数。`arena_round11.py` 复用已验证的 `league_round9.run_job`，每局都由本地 Kaggle 官方 `kaggle-environments==1.32.7` 引擎完整运行 720 步。V9 原件与第 10 轮文件均不改动。

## 赛场封存

- 2026-09-23 已先生成 `league_seeds.json`：开发 24 个世界、确认 48 个、备用 48 个，三个集合互不重合，也与第 8、9、10 轮联赛清单中共 340 个旧世界不重合。种子文件 SHA256 为 `4a4cff07c6ae9bda2c875db14b9980f4838fae4870837a6d70ff4db81151bb7e`。这些世界在任何第 11 轮候选跑分前固定。
- 核心对手：V9 原件 `self_v9`、Frontier、Master 和本地 DSM 代理。各核心文件的 SHA256 写死于赛场脚本并在建清单时核对；每局启动前再次核对候选和对手源码。**DSM 代理是公开信息构造的本地代理，绝非 DSM 的私有提交。**
- 每个世界对每个对手各跑候选和冻结 V9 基线、各坐两个席位。默认开发轮为 `24 × 4 × 2 × 2 = 384` 局；确认和备用各 768 局。结果逐局追加至 `results/round11/<名称>-<分组>.jsonl`，同名清单固定种子、源码 SHA、引擎版本、坐席和对手。失败、未满 720 步、异常日志、异常遥测或非有限分数都使局无效，不能晋级。恢复执行时核对每一行的任务 ID 和来源。
- 通过 `--extra-opponent FAMILY=path/to/main.py` 可加入新公开对手，单独报告其家族成绩。额外家族只用于诊断，不能通过增添弱对手提高核心晋级分；核心家族、V9 参照组及其文件路径不接受替换。
- 开发集 V9 基线逐局存入 `results/round11/baseline_cache_v2/`。缓存键锁定官方引擎版本、720 步、种子与席位、对手和 V9 的路径与源码 SHA，以及官方对局执行器和本赛场脚本 SHA。仅通过完整结果校验的局可缓存；读取时再次验证源码字节、结果、校验和。后续不同候选共用同一 192 局开发基线，确认集与备用集绝不读取或写入此缓存。`--dry-run` 会显示缓存命中数及仍需运行的局数，发现损坏缓存会直接拒绝而非悄悄重赛。

## 顺序与晋级

1. 在**开发集**先作小规模机制筛选，再用全部 24 个世界比较具体候选和 V9。任一世界的两个席位算同一个样本；对一个对手家族含多个文件的情况，先在世界内平均，再给 Frontier、Master、DSM 代理三家族等权。报告同时列出每家族胜／负／平、平均与中位金币差、与 V9 同世界同坐席的胜点和金币差。
2. 只有开发集完整、所有局有效、核心家族等权配对胜点增益为正、对 V9 直接交手至少拿到 0.5 胜点的候选，才能执行 `freeze`。此命令只允许在一个 `run-name` 下冻结一个候选与对手清单，记录开发赛场清单和逐局账本的 SHA。冻结后不再按确认集改策略。
3. **确认集默认封锁。**只有显式 `--unlock-confirmation`，且源码、对手、冻结开发证据完全匹配时才能运行；确认集必须一次按全部 48 个世界评估。通过标准：所有对局有效；48 个世界中三大核心家族的配对样本完整；按世界重采样的核心胜点增益 95% 区间下界大于零；三大家族各自平均增益均不低于 −0.05；对 V9 的直接胜点不低于 0.5。备用集还需显式 `--unlock-reserve`，并先通过完整确认集。
4. 线上提交和 Kaggle 动态积分另行验证。即使通过本地门槛，也只代表相对于这些固定代理和这个引擎版本的稳健改进；不能推出能击败 DSM／Vadim 私有版本，也不能预测 3000 分。

V9 自对弈通常大量平局；一个候选若只把这些平局打破，胜点可能上升而对多种生产路线无改进。因此 V9 只作为**退步否决项**，不进入正向核心晋级分。公开录像用于提出机制假说和定位失败，不拿录像里的已知种子做晋级测试、不照抄动作序列或识别对手开局签名。官方引擎和公开代理可能共享代码谱系，哪怕三个家族均提升也不能当成三个独立证据源；在线下发现反例后，应寻找机制失效原因并在新的前瞻性种子上再验证，不能回头反复调确认集。

## 使用

在比赛目录内使用项目虚拟环境：

```powershell
.venv/Scripts/python.exe arena_round11.py smoke
.venv/Scripts/python.exe arena_round11.py run --candidate experiments/your_candidate.py --run-name crop-value-v1 --count 8
.venv/Scripts/python.exe arena_round11.py run --candidate experiments/your_candidate.py --run-name crop-value-v1
.venv/Scripts/python.exe arena_round11.py freeze --run-name crop-value-v1
.venv/Scripts/python.exe arena_round11.py run --candidate experiments/your_candidate.py --run-name crop-value-v1 --split confirmation --unlock-confirmation
.venv/Scripts/python.exe arena_round11.py report --run-name crop-value-v1 --split confirmation
```

第一条只核对 120 个种子、源码清单、384 个开发任务 ID 与默认确认封锁；**不运行智能体对局**。候选继续修改时须改 `run-name`，避免旧结果与新源码混用。若源码、赛场脚本或种子清单变化，恢复命令会拒绝既有同名结果。
