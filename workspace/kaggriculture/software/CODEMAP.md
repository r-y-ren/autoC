# CODEMAP — 代码目录分类地图（2026-09-21）

> 范围：`workspace/kaggriculture/software/`。本文是**分类索引**：每个代码文件的用途一行。
> 整理纪律：现役提交链（`kaggle_simulations/agent/`）与验收命令引用路径（`tests/`、`scripts/`）为**冻结面**——物理搬移会打断 build.py 路径、身份链与 blueprint 验收命令，故本波整理以本文的分类地图落地，破坏性搬移留赛后。

## A. 现役提交链（冻结面，线上 v14.x 候选本体）

| 文件/目录 | 作用 |
|---|---|
| `kaggle_simulations/agent/main.py` | 薄装载器：官方 get_last_callable 语义下按拓扑序 exec src 九模块+planner/；装载窗口内急切导入 planner.runtime（P4.1 接合修复）；sha 即候选身份锚 |
| `kaggle_simulations/agent/src/constants.py` | 引擎常量镜像+全部旋钮+PLANNER_ENABLED 总旗+PLANNER_OVERRIDES 寄存器+_plan_knob 惰性读取（29+ 键） |
| `kaggle_simulations/agent/src/entry.py` | agent() 主入口：黎明 DTSP 钩子、fail-open 三道（异常/覆盖恢复/指纹不符→当局纯 v13.8 语义）、遥测接线 |
| `kaggle_simulations/agent/src/observer.py` | 对手供给四通道估计器（市场库存差/价格反解/钱账/tile 记账），est_* getter |
| `kaggle_simulations/agent/src/strategy.py` | L1 宏观策略：模式决策 _decide_mode（11 激活门槛已旋钮化）、d6 五问、阶段窗、cash gate |
| `kaggle_simulations/agent/src/mission.py` | L2 任务包：D1-D4 死线分级、deps、场景标签、capacity 前馈 |
| `kaggle_simulations/agent/src/solver.py` | L3 路线求解：EDF×密度×老化最近邻+2-opt 抛光+喂食腿+逐站 ETA 重验 |
| `kaggle_simulations/agent/src/executor.py` | L4 执行器：沿线行走+到站动作+REPLAN 旗+d29 模板 |
| `kaggle_simulations/agent/src/market.py` | 市场层：黎明卖出计划器（吸收表×曲线投影×批次）、买畜/饲料门（钱包门已 _plan_knob 化）、干扰载体、committed_spend |
| `kaggle_simulations/agent/src/telemetry.py` | 遥测：mission/资金/行为计数/轨迹 trace（进程内） |
| `kaggle_simulations/agent/src/wave.py` | v15 波次日历剧本（休眠：WAVE_ENABLED=False）——d0 花到 ≤$600 开局、d6 毛 flush→地+牛、d10 瓜 flush→地+crew12、首店身份路由；仅被 DTSP 三选一消费 |
| `kaggle_simulations/agent/src/_archive_header.py` | 候选档案头（谱系与纪律声明，逐字保留） |
| `kaggle_simulations/agent/planner/twin.py` | 数字孪生引擎：官方回放任意步重建状态+interpreter 直驱（184 局官方回放 100% 逐位保真；0.054ms/步；fail-closed 指纹链） |
| `kaggle_simulations/agent/planner/plans.py` | 计划空间：PlanSpec/枚举 R1-R8 过滤（帽 111）/投影器（P2.6 校准）/plan_to_knob_overrides（54 键面） |
| `kaggle_simulations/agent/planner/opponents.py` | 对手模型集 Ω=4：被动外推/悲观成交/winner_balanced/wheat_suppressor |
| `kaggle_simulations/agent/planner/select.py` | 鲁棒选择器：trimmed-mean 等聚合+identity 近平 tie-break（τ=0.5%） |
| `kaggle_simulations/agent/planner/runtime.py` | DTSP 运行时：短地平线阶梯（K=6×H=1d 默认）、时间治理器（0.85s 帽）、接合遥测 |
| `kaggle_simulations/agent/planner/wave_script.py` | WaveCandidate：把波次剧本段作为 DTSP 三选一候选的桥接层 |
| `kaggle_simulations/agent/build.py` | 确定性打包器：main+src+planner 定拓扑序/零时间戳/--check 逐字节复验 |
| `kaggle_simulations/agent/submission.tar.gz` | 当前登记包（pkg.3-wave，b1f582ff，v14.3-sellrace 语义） |

## B. 引擎与评估基建（kgenv/ = 自研库）

| 文件 | 作用 |
|---|---|
| `kgenv/engine.py` | 官方引擎装载/驱动封装（vendored 1.32.7 wheel） |
| `kgenv/gym_env.py` | gym 式环境封装（训练/批量对局用） |
| `kgenv/arena.py` | 本地竞技场：多 bot 循环赛 |
| `kgenv/elo.py` / `bradley_terry.py` | Elo 与 BT/Davidson 评级（顺序无关批量） |
| `kgenv/bots/` | 内置对手（baseline_wheat/cow_baron/starter 封装等） |
| `kgenv/economy.py` | 经济语义镜像（价格公式/棚容/城镇需求——market.py 消费） |
| `kgenv/replay_profile.py` / `dna_forensics.py` / `dna_integrity.py` | 回放画像与 DNA 法证（语料指纹/异常局检测） |
| `kgenv/online_probe.py` | 线上采样门 fail-closed 校验（禁本地自对局顶替） |
| `kgenv/eval_contract.py` / `holdout_contract.py` / `variance.py` / `regression.py` / `redlines.py` | 评估契约：AB/BA 对称、holdout 种子域隔离、方差门、回归门、红线清单 |
| `kgenv/candidate_identity.py` / `external_h2h_contract.py` | 候选身份链与外部黑盒 H2H 证据契约 |
| `vendor/kaggle_environments-1.32.7+nodeps-py3-none-any.whl` | 官方引擎 wheel（未改，WHEEL_PROVENANCE.md 记录来源与 sha） |
| `smoke_boot.py` | 四相冒烟：env 装载/提交自打/契约/gym |

## C. scripts/（57 个，按族分类）

**身份/门禁/评估族**

| 脚本 | 作用 |
|---|---|
| check_candidate_identity.py | 候选身份链校验（main sha/git ref/blob 三方一致） |
| check_eval_contract.py | 评估契约校验（official/dev：AB/BA、种子域、零异常局） |
| run_holdout.py | 一次性 holdout 运行/复验（--verify-published） |
| run_eval.py / iterate_gate.py | 本地评估矩阵与开发门 |
| ablate.py / quickwin_probe.py | 成对消融与单变量探针（本地=灾难诊断口径） |
| run_llm_ab.py | LLM 辅助决策 A/B（KG_LLM_* 完整配置才执行） |
| sync_online_probe.py | 线上采样闭环：list/fetch/ingest/gate/close（SOP 唯一门） |
| fit_bradley_terry.py | BT 拟合 |
| market_ledger.py / sell_plan_reconciliation.py | 官方逐件成交账本与卖计划对账 |
| kill_table.py | 杀伤表（干扰收益反解） |
| capacity_calibration.py | 容量定律系数定标 |

**回放取证族**

| 脚本 | 作用 |
|---|---|
| forensic_harvest.py | 官方回放限量抓取（episodes/replay 通道） |
| replay_deep_stats.py | 逐席深度画像（CARE/FEED/hires/畜群/象限/d12/d24） |
| corpus_build.py / corpus_fetch.py / corpus_integrity.py | 语料构建/抓取/完整性校验 |
| analyze_dna_forensics.py / check_dna_forensics.py | DNA 法证分析与校验 |
| observer_v0_validator.py | 观测器离线验证器（双席 private 真值口径） |
| analyze_failure_modes.py / verify_milk_economics.py / probe_v9_wheat_gate.py / r3_trajectory_probe.py / h2h_external_probe.py / check_opponent_strength.py / check_external_h2h.py | 历史法证/验证件（各代遗留，可复跑） |

**Track-B 门与法证族（2026-09-19/21 新增）**

| 脚本 | 作用 |
|---|---|
| twin_fidelity.py | 孪生保真门（--mode official/smoke；184 局逐位一致） |
| planner_offline_bench.py | DTSP 离线基准（14 局×42 注入双口径；可配置 Ω；注：rollout_with_replay_opponent 存在席位错位通道，me_seat=1 局数字需修正口径，见 JOURNAL 09-21 勘误） |
| planner_flagoff_golden.py | 旗关等价黄金基线（--emit/--check/--probe-on） |
| planner_calibration_suite.py | 投影器校准消融套件（C1-only oracle/聚合扫描/时点先验） |
| p41_official_load_probe.py | 官方装载语义探针（sys.path.pop 根因复现） |
| v3_readmission_suite.py | v3 复裁三判据套件 |
| v31_pressure_calibration.py | 压力自适应折扣校准（诚实 FAIL 留档） |
| v15_h2h_v48.py / v15_d0_counterfactual_giants.py / v15_regression_gate.py | v15 波次剧本三验证门 |
| v143_sellrace_gates.py | v14.3 售卖竞速门 |
| v48_derivative_launch_check.py / v48plus_launch_check.py / v48plus_ab_gate.py / v48plus_layer_ablation.py / v48plus_metrics.py | v48 衍生版与 v48+ 的发射/AB/消融/指标件 |
| round23_loss_forensics.py / round23_disaster_dtsp_probe.py / round23_dtsp_stepdiff_probe.py / round23_dtsp_engagement_probe.py | round-23 败局法证与接合判定四件 |
| round24_loss_forensics.py / round24_counterfactual_probe.py / round24_d0_counterfactual.py | round-24 败局法证与 d0 全季反事实协议 |
| sprintA_structure_probe.py / profile_v48_gap.py / m4_switchover_regression.py / solver_shadow_stats.py | 结构探针/v48 差距画像/M4 切换回归/求解器影子（历史在役） |

## D. tests/（53 个测试文件，基线 990 passed+2 skipped）

- **提交链契约**：test_agent_contract / test_candidate_identity / test_build_determinism / test_artifact_indexes / test_landing_w1
- **策略族**：test_strategy_m2 / m3 / mg / r3 / r4_p1 / r4_p2 / r4_p3 / r5；test_branch_w2 / test_p0_wave
- **调度器/市场**：test_scheduler_w2 / test_market_w2 / test_market_bilateral / test_market_budget / test_market_reconciliation_ledger / test_market_strategy_repairs / test_phase_d
- **观测器**：test_observer_w2
- **评估/评级/语料**：test_arena_elo / test_bradley_terry / test_bots_online_pool / test_bots_variants / test_ablate / test_eval_hardening / test_replay_corpus / test_replay_success / test_dna_forensics / test_external_h2h_contract
- **门禁**：test_regression_gate / test_variance_and_frozen_gate / test_holdout_contract / r4 / v6 / v7；test_redlines / test_activity_gate / test_online_probe_gate / test_economy
- **Track-B（孪生/规划器/接合/售卖）**：test_twin_fidelity / test_planner_contract / test_planner_flagoff_equiv / test_planner_calibration / test_p3_integration / test_p41_engagement_gate / test_wave_script / test_sellrace

## E. 线上提交工件（kaggle_simulations/ 除 agent/ 外）

| 目录/文件 | 作用 |
|---|---|
| `v48_derivative/` | **已上线**（ref 56400478）v48 公开衍生版包：逐字节=原作者公开发布工件（01de7c27）；launch_check 四门 |
| `v48plus/` | **封存备选**（四门全绿未发射）：V48+V50 经济层（COURIER+SHEDROOM），main eca5dea2/包 b5fc0ed7；build_manifest.json |
| `opponents/` | 本地陪练源码：v48_main.py（top-10 解码版）、v72_main.py（历史代）+PROVENANCE.md（来源与许可） |

## F. BC 轨（bc_track/，已弃牌、资产保留）

| 路径 | 作用 |
|---|---|
| `bc_track/scripts/harvest_top_replays.py` | top-30 队官方回放三级取证抓取 |
| `bc_track/scripts/extract_samples.py` | (obs 摘要, 动作) 样本抽取（bc-schema/1.1） |
| `bc_track/scripts/bc_schema.py` | 特征/动作 schema 单一契约（167 全局维+14 单位维 / 18op+12arg+14 桶） |
| `bc_track/scripts/train_bc.py` | 两解耦 MLP 训练（CPU 146s；条件掩码 CE） |
| `bc_track/scripts/bc_policy.py` | 纯 Python 前向策略（int8 量化权重） |
| `bc_track/scripts/bc_eval.py` | 评估闭环：孪生 d0 全季对回放对手+行为诊断（席位修正版） |
| `bc_track/scripts/bc_opening.py` / `bc_decode.py` / `bc_seed_stability.py` | 开局剧本先验 / 市场解码约束 / 种子稳定性 |
| `bc_track/models/bc_model_v1.py / v2.py` | 权重硬编码模型（v2=schema1.2 重训，op acc 49%） |
| `bc_track/issues/01-08` | 票单（01/02 完成，03 弃牌，04-07 未触发，08 收口） |

## G. 数据与产物（exports/，大文件多 gitignored）

| 子目录 | 作用 |
|---|---|
| `exports/online/` | 线上台账：round2-26 ledger/sampling/ledgers、sprint_forensics、index.json |
| `exports/probes/` | 实验探针产物（gitignored）：twin_fidelity / planner_bench / round23_forensics / v15_ignition / v143_sellrace / v48_launch / v48plus |
| `exports/twin/` | P1 孪生保真台账（入库） |
| `exports/candidates|ablations|holdout|external|replay_dna|replay_profiles` | 各代评估产物与语料画像 |
| `exports/intel/` | 早期情报摘要 |
| `active_candidate.json` | 候选身份登记（working/frozen 两段式） |
| `*_frozen_candidate.b64 + *_manifest.json` | 历史代冻结快照（m2b/m3/r3/r4/v6/v72） |
| `metrics.json` / `requirements.txt` | 软件侧 metrics 分片 / 评估环境依赖清单 |

## H. 整理纪律（为什么不做物理搬移）

1. `agent/` 是身份链锚（main sha 即候选身份）——移动即断链；
2. blueprint 验收命令以 `workspace/kaggriculture/software/tests`、`scripts/...` 字面路径执行——搬移即破坏验收；
3. 脚本间 import 以 `SOFTWARE` 根为基准（bench←twin/各方探针）——批量搬移需全链回归，冻结期（09-27 前）风险大于收益；
4. 建议：赛后归档时以本 CODEMAP 为蓝本做一次带全量回归的物理重组（届时 holdout/评估链一并退役可大幅瘦身）。
