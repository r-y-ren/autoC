# 责任文档：kaggriculture 战役工程库重构（fn_work/ 重建）

> 本文档由 fn-divide 产出与独占更新；**fn-implement 只读**。实现期发现结构性变化（函数增/删/拆/并/职责或调用关系变化）时，必须回到本阶段修改本文档。进度与状态见 implementation.md（fn-implement 建立）。
> 上游：fn_docs/requirements.md（R1-R20，验收方式唯一来源）；行为全景：behavior_inventory.md；安全网：snapshot_tests/。
> 时序约束（继承 requirements 范围外）：①09-30 终交收口前旧树（software/ 现役链+验收引用路径+工件）零字节变更；②一切产物只落战役根内；③fn_work/ 新结构生长不触碰旧树；④真正的战后动作：旧树整体删除（fn-close 验收后）、active_candidate 降级（R21）、蓝图修订（R17）。
>
> **函数总数预警（fn-divide 规程）**：本划分共 13 个顶层功能块 + 约 32 个二级函数 + 2 个共享函数 ≈ 47 个函数，超过 20 的预警线。收缩方案=**四波实施**（见下），每波函数数 ≤20；矩阵全覆盖无波外需求。实现按波推进，波内函数才进 fn-scaffold 定桩。

## 实施波序（收缩方案）

| 波 | 范围 | 顶层块 | 需求 |
|---|---|---|---|
| W1 评估修复层 | 快照反例修复+安全网迁移 | run_official_bench / robust_selection / guard_replay_profile_engine / migrate_snapshot_suite | R1(判据) R2 R3 R5 |
| W2 基线与数据层 | 机器无关+最小集+路径变量化 | portable_test_baseline / package_minimal_repro_set / discover_campaign_roots(共享) | R6 R19 R20 |
| W3 契约与结构分层 | 单源化+归档+降级+归位 | unify_contract_sources / archive_forensic_assets / relocate_library_modules / downgrade_dormant_assets | R8 R9 R10(死码不迁) R11 R12 R13 R14 R15 |
| W4 文档与治理层 | 双源归源+留档+文档一致 | record_governance_dispositions / sync_documentation / run_submission_agent(注释修正收尾) | R1(主体) R4 R7 R16 R17 R18 R21 |

（W4 含 run_submission_agent 的整体迁移；其死码剔除随迁移完成=R10。若按波推进，W1-W3 均不依赖 W4，可先行。）

## 结构概览（纯结构，不带职责）

- run_submission_agent ← R1, R10
  - load_agent_modules
  - observe_opponent_state
  - decide_macro_mode
  - build_mission_pack
  - solve_worker_routes
  - execute_along_route
  - plan_market_orders
  - run_dawn_planner
  - record_shadow_telemetry
- robust_selection ← R3
  - aggregate_scores
  - break_ties_by_identity
- run_official_bench ← R2
  - rollout_with_replay_opponent
  - evaluate_plan_portfolio
  - recalculate_affected_history
- guard_replay_profile_engine ← R5
  - fingerprint_engine_constants
- migrate_snapshot_suite ← R1
  - refresh_frozen_values
- portable_test_baseline ← R6
  - regenerate_artifacts_lf
  - relax_platform_assertions
  - declare_machine_context
- package_minimal_repro_set ← R19
  - collect_gate_golden_files
  - enforce_size_budget
  - declare_local_corpus_dependencies
- unify_contract_sources ← R8, R9
  - merge_abnormal_reason
  - single_opponent_roster
  - assert_bots_constants_match_wheel
- archive_forensic_assets ← R11, R12
  - partition_script_tiers
  - archive_bc_models
- relocate_library_modules ← R15
  - scan_for_library_misplacement
- downgrade_dormant_assets ← R13, R14
  - prune_mainline_import_graph
- sync_documentation ← R7, R16, R18
  - fix_bc_track_records
  - retire_codemap_with_errata
  - codify_probes_policy
- record_governance_dispositions ← R4, R17, R21
  - write_dual_source_provenance
  - declare_blueprint_cmd_invalidation
  - demote_active_candidate_ledger
- （共享）discover_campaign_roots
- （共享）run_equivalence_gate

## 需求覆盖矩阵（非功能约束不进矩阵，fn-close 终检对照 requirements 非功能节）

| 需求 | 顶层函数 |
|---|---|
| R1 | run_submission_agent；migrate_snapshot_suite（行为判据） |
| R2 | run_official_bench |
| R3 | robust_selection |
| R4 | record_governance_dispositions |
| R5 | guard_replay_profile_engine |
| R6 | portable_test_baseline |
| R7 | sync_documentation |
| R8 | unify_contract_sources |
| R9 | unify_contract_sources |
| R10 | run_submission_agent（死码不迁+stage 显式化） |
| R11 | archive_forensic_assets |
| R12 | archive_forensic_assets |
| R13 | downgrade_dormant_assets |
| R14 | downgrade_dormant_assets |
| R15 | relocate_library_modules |
| R16 | sync_documentation |
| R17 | record_governance_dispositions |
| R18 | sync_documentation |
| R19 | package_minimal_repro_set |
| R20 | discover_campaign_roots（共享，全库受益）+ portable_test_baseline |

## 共享函数（shared/：多顶层共用；矩阵挂全部受益需求）

- **discover_campaign_roots**（调用方：全部含路径操作的功能块）← R20 [新增]
  - 职责：程序化发现战役根/仓根/软件根（目录特征过滤：含 blueprint.md+software+fn_docs 者=战役根），返回各根路径对象；取代一切字面 `workspace/kag…` 路径与"仓根 CWD 假设"；任何调用点不得拼接字面战役名。
  - 签名意图：输入: 起点路径（默认按 __file__ 上溯）/ 输出: 含 campaign_root/repo_root/software_root 的具名结构 / 错误: 找不到特征目录时抛带排查提示的 RootDiscoveryError（fail-closed，不猜）。
  - tested 策略：自有单测。
  - 核验命令：测试: 任意 CWD 下 pytest/门禁通过（继承 R20 验收）；新结构树 grep 字面战役路径零命中（豁免：旧树对接适配层、fn_docs 记录）。
- **run_equivalence_gate**（调用方：run_submission_agent, migrate_snapshot_suite）← R1 [新增]
  - 职责：等价判据执行器——封装"黄金哈希复验 + 快照套件复跑 + 旗关等价探针"三件的调用与结果汇总，输出单页裁决（pass/fail+逐项数值）。只编排不实现判据本体。
  - 签名意图：输入: 目标 agent 装载路径 + 判据选项集 / 输出: 裁决结构（逐项 name/passed/value）/ 错误: 任一判据不可执行即整体 fail（fail-closed）。
  - tested 策略：自有单测（对旧代码跑=全 pass 基线）。
  - 核验命令：测试: 对旧树执行输出全 pass（继承 R1 验收：快照 62P+4xf 口径）。

## 功能块 run_submission_agent ← R1, R10

（块引言：现役提交链 bot 的等价迁移——把 kaggle_simulations/agent/ 十模块+planner/六模块迁入 fn_work/ 新包，行为以 snapshot_tests/test_agent_characterization.py 冻结值与旗关黄金哈希为逐字节判据；R10 的 9 处死码**不迁**（清单见 requirements R10），stage_* 四键显式化为保留轴并在包文档标注；R20 注释漂移 3 处（main"九模块"头注、strategy ANTICIPATED 注释、_decide_mode docstring 死门）在迁移副本中修正。装载语义红线：装载窗内急切导入 planner、sys.path 腰带保留、exec 拓扑序与 build MODULE_ORDER 逐字一致、身份链 sha 随迁移重新登记。）

- **run_submission_agent** [L0|改造]
  - 职责：官方装载语义下的单回合入口（原 main.py+entry.py 的 agent()）：obs→观察旁路→黎明 DTSP 钩子→宏计划→任务→四层求解→市场→雇工→排序→预算截断；整体 try/except PASS（fail-open 第一道）。与现役行为逐字节等价（判据=run_equivalence_gate 全 pass）。
  - 签名意图：输入: 官方 obs dict / 输出: 全部单位动作+市场订单 / 错误: 内部异常全吞并降级为 PASS（不许崩，线上语义）。
  - 调用方：Kaggle 官方装载（get_last_callable）。
  - tested 策略：上游覆盖: migrate_snapshot_suite。
  - 核验命令：上游覆盖: migrate_snapshot_suite（快照整局冻结值）。
  - **load_agent_modules** [L1|改造]
    - 职责：薄装载器——按固定拓扑序 exec 十模块+planner 进共享命名空间，装载窗内急切 import planner.runtime 存 DTSP_RUNTIME_MODULE，无条件 sys.path 腰带；重绑最后 callable=agent。死码支（_SELLRACE_SHIP 等）不迁。
    - 签名意图：输入: 包根路径 / 输出: 共享 globals+agent callable / 错误: 模块缺失/重名即抛（build precheck 同步收口）。
    - 调用方：run_submission_agent（装载期）。
    - tested 策略：自有单测（precheck 语义）+ 上游覆盖。
    - 核验命令：测试: 装载后 main sha 登记一致（继承 R1）。
  - **observe_opponent_state** [L1|改造]
    - 职责：对手供给四通道日账（精确流发布/残差降信/钱账分解/tile 记账）+est_* getter，按现状迁移；_opp_note_fills 仅离线语义保留。
    - 签名意图：输入: 单侧 obs/回合号 / 输出: 观察寄存器更新 / 错误: 通道失败降信不抛。
    - 调用方：run_submission_agent。
    - tested 策略：上游覆盖: run_submission_agent（既有 test_observer_w2 族随迁）。
    - 核验命令：上游覆盖: migrate_snapshot_suite。
  - **decide_macro_mode** [L1|改造]
    - 职责：L1 宏观三模式+WHEAT_FARM 关+_plan_rollout 偿付门+阶段寄存器（P0-P5/d1/d6/d10/d14/d22/fuse/backfill）+_field_alloc 分区轮作；stage_* 四键从"发射未接线"显式化为保留轴（文档标注，值面不变）；ANTICIPATED 注释漂移修正（行为不变）。
    - 签名意图：输入: 观察寄存器+现金/畜群/回合 / 输出: 模式+阶段旗组 / 错误: 无（纯函数语义）。
    - 调用方：run_submission_agent。
    - tested 策略：上游覆盖（test_strategy_m2/m3 族随迁）。
    - 核验命令：上游覆盖: migrate_snapshot_suite。
  - **build_mission_pack** [L1|改造]
    - 职责：L2 任务包（D1-D4 死线分级/deps/EOD 事件/容量前馈/mission_hash）+末日清算+黎明影子包，按现状迁移。
    - 签名意图：输入: 模式+实体状态 / 输出: 任务序列+影子包 / 错误: 无。
    - 调用方：run_submission_agent。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: migrate_snapshot_suite。
  - **solve_worker_routes** [L1|改造]
    - 职责：L3 路线求解（EDF+价值密度+2-opt 抛光+载货腿+D1 兜尾+自适应 REPLAN），按现状迁移；死件 _two_opt_segment/_dawn_crew_size/_schedule_units 及其测试不迁。
    - 签名意图：输入: 任务序列+工人状态+容量 / 输出: 逐工人路线 / 错误: 无解时 D1 兜尾。
    - 调用方：run_submission_agent。
    - tested 策略：上游覆盖（test_scheduler_w2 族随迁）。
    - 核验命令：上游覆盖: migrate_snapshot_suite。
  - **execute_along_route** [L1|改造]
    - 职责：L4 执行（沿线行走+到站动作+F4 跳过+D1/EOD 断言+幂等 REPLAN 门+d29 DROP→SELL），按现状迁移。
    - 签名意图：输入: 路线+实时 obs / 输出: 本回合单位动作 / 错误: 断言失败走 fail-open。
    - 调用方：run_submission_agent。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: migrate_snapshot_suite。
  - **plan_market_orders** [L1|改造]
    - 职责：市场层（引擎镜像定价/三门卖出/MK-3 批次/MK-5 载体/sellrace 前移旗关/买地饲料种子畜群四重门/committed_spend），按现状迁移；_note_buys 死 shim 不迁。
    - 签名意图：输入: 库存+价格投影+预算 / 输出: 市场订单集 / 错误: 预算超限截断不抛。
    - 调用方：run_submission_agent。
    - tested 策略：上游覆盖（test_market_* 族随迁）。
    - 核验命令：上游覆盖: migrate_snapshot_suite。
  - **run_dawn_planner** [L1|改造]
    - 职责：黎明 DTSP 钩子（预算治理→摘要→枚举≤120→投影×Ω4→robust_selection→rollout 阶梯→τ 双闸→注入/快照/幂等缓存；wave 候选恒排比较集首位），按现状迁移；fail-open 二三道（restore_pristine+sticky_off+指纹不符）语义不变。
    - 签名意图：输入: 黎明 obs+剩余预算 / 输出: 旋钮注入或显式跳过 / 错误: 三道 fail-open 全保留。
    - 调用方：run_submission_agent。
    - tested 策略：上游覆盖（test_planner_* 族随迁）。
    - 核验命令：上游覆盖: migrate_snapshot_suite + 旗关黄金哈希。
  - **record_shadow_telemetry** [L1|改造]
    - 职责：影子遥测+sink 注入（异常全吞旁路），按现状迁移。
    - 签名意图：输入: 任意遥测事件 / 输出: 寄存器追加 / 错误: 永不抛。
    - 调用方：run_submission_agent 全层。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: migrate_snapshot_suite。

## 功能块 robust_selection ← R3

（块引言：planner/select.py 的鲁棒选择层修复——aggregate_scores 从名字序裁切改值序裁切，悲观模型（pessimistic_fill）在投影段恢复效力；identity tie-break（τ=0.5%）不变。修复判据=snapshot_tests/test_counterexample_r3.py 三条 strict xfail 转为 XPASS。）

- **robust_selection** [L0|改造]
  - 职责：对计划×对手模型的分数矩阵做鲁棒聚合与选择（argmax+identity 近平 tie-break），修复值序裁切。
  - 签名意图：输入: {plan: {opponent: score}}+tie 阈值 / 输出: 最优计划+聚合明细 / 错误: 空输入抛。
  - 调用方：run_dawn_planner（投影段）。
  - tested 策略：自有单测。
  - 核验命令：测试: snapshot_tests/test_counterexample_r3.py（迁移后期望 XPASS：值序 62.5 等）+ test_planner_select_characterization.py 对照冻结值更新为值序并留双口径注记（继承 R3 验收=快照反例）。
  - **aggregate_scores** [L1|改造]
    - 职责：逐计划聚合对手分数——按**分数值序**排序后裁切 trim 端点再聚合（原实现按字典序，wheat_suppressor/winner_balanced 恒被裁的缺陷修复）；聚合量（trimmed mean 等）与旗面不变。
    - 签名意图：输入: 对手名→分数 dict + trim 参数 / 输出: 聚合值 / 错误: 空集抛。
    - 调用方：robust_selection。
    - tested 策略：自有单测（反例集直测）。
    - 核验命令：测试: 值序反例（62.5/22.5/55.0）通过且名字序旧值（35.0）失败（继承 R3）。
  - **break_ties_by_identity** [L1|改造]
    - 职责：聚合值差 <τ(0.5%) 时优先选 identity 近平计划，按现状迁移（行为不变）。
    - 签名意图：输入: 聚合结果+identity 标记 / 输出: 决胜计划 / 错误: 无。
    - 调用方：robust_selection。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: robust_selection（K1 边际 1.5<5.0 冻结语义）。

## 功能块 run_official_bench ← R2

（块引言：DTSP 离线基准 harness 的席位修复——seated rollout（v143_sellrace_gates.py:91-116 参照）上提为唯一通道，8 处错位内联同构统一；受影响历史数字重算入台账（双口径并列：错位口径历史值/seated 口径重算值），范围=behavior_inventory G1 所列（v3 复裁 b=5/9·c=7/13、v48+ 巨人门、round24_d0 等）。修复判据=test_counterexample_r2 XPASS。）

- **run_official_bench** [L0|改造]
  - 职责：离线基准主流程（14 局×注入点×双口径裁决：主口径 DTSP≥反应式、参考口径 history 代差修正），rollout 全部经 seated 通道。
  - 签名意图：输入: 注入集配置+对手模型集+me_seat 说明 / 输出: 逐局终局资金+双口径裁决 JSON / 错误: 引擎异常 fail-closed 记异常局。
  - 调用方：评估操作者（CLI）。
  - tested 策略：自有单测。
  - 核验命令：测试: snapshot_tests/test_counterexample_r2.py XPASS（seated=[3000.0,1570.0] 真值通道）（继承 R2）。
  - **rollout_with_replay_opponent** [L1|改造]
    - 职责：从回放任意步以**显式 me_seat** 重建双席状态并推演——我方动作注入 me_seat 席、对手动作注入对席（修复原恒 seat0 注入）；幂等/指纹校验语义保留。
    - 签名意图：输入: 回放+注入点+我方 callable+me_seat / 输出: 双席终局资金（序=seat0,seat1，与我方席位解耦） / 错误: 回放缺失/指纹不符抛。
    - 调用方：run_official_bench。
    - tested 策略：自有单测（me_seat∈{0,1} 差分）。
    - 核验命令：测试: 合成回放 me_seat=1 通道=[3000.0,1570.0]（继承 R2 快照反例）。
  - **evaluate_plan_portfolio** [L1|改造]
    - 职责：计划枚举×对手模型集的评估编排（枚举≤帽/投影/rollout 调用/聚合委托 robust_selection），按现状迁移、rollout 换 seated 通道。
    - 签名意图：输入: 计划空间+Ω+注入点 / 输出: 逐计划聚合分 / 错误: 无。
    - 调用方：run_official_bench。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: run_official_bench。
  - **recalculate_affected_history** [L1|新增]
    - 职责：对 G1 所列受影响历史结论用 seated 通道重算，产出 fn_docs/recalculation_ledger.md（台账）：每条含局号/口径（错位历史值 vs seated 重算值）/结论是否翻转；不修改既有 JOURNAL（台账并列留痕）。
    - 签名意图：输入: 受影响结论清单 / 输出: 台账文件+逐条翻转标记 / 错误: 单条重算失败记 SKIP 留因，不中断整批。
    - 调用方：评估操作者（一次性，W1 收口跑）。
    - tested 策略：自有单测（台账 schema）。
    - 核验命令：测试: 台账存在+键完整（继承 R2"重算留档"验收）。

## 功能块 guard_replay_profile_engine ← R5

（块引言：replay_profile.py 内嵌 ~1050 行手写引擎的指纹看护——对 vendored wheel 提取的常量集做 sha256 断言，语义漂移即红；选定断言方案（twin 通道改造为备选不进树）。）

- **guard_replay_profile_engine** [L0|新增]
  - 职责：入口校验器——装载 replay_profile 引擎前提取其常量集（价格公式/棚容/城镇需求等）计算指纹，与登记值比对。
  - 签名意图：输入: 无（模块装载时自检）/ 输出: 通过或 raise / 错误: 指纹不符→fail-closed 抛 EngineFingerprintError。
  - 调用方：replay_profile 消费者（corpus/画像/法证件）。
  - tested 策略：自有单测。
  - 核验命令：测试: 篡改常量→红；正常→绿（继承 R5）。
  - **fingerprint_engine_constants** [L1|新增]
    - 职责：常量集提取与指纹计算+登记值维护（升版 wheel 时显式重登记流程）。
    - 签名意图：输入: 引擎常量源 / 输出: sha256 指纹 / 错误: 提取失败抛。
    - 调用方：guard_replay_profile_engine。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: guard_replay_profile_engine。

## 功能块 migrate_snapshot_suite ← R1

（块引言：快照安全网迁移中枢——snapshot_tests/ 迁入 fn_work/tests/ 并成为重构 tested 判据；绿门=全绿且 R2/R3 反例 XPASS（strict xfail 转 XPASS 时套件翻红=迁移时点信号）。除 R2/R3 修复影响的冻结值外，一切冻结值逐字节不动。）

- **migrate_snapshot_suite** [L0|改造]
  - 职责：迁移编排——复制九文件、修正 import 根（经 discover_campaign_roots）、跑绿门、出具迁移裁决。
  - 签名意图：输入: 源套件路径+目标 / 输出: 裁决（passed/xpassed/xfail 残留清单） / 错误: 任一反例仍 xfail→迁移不通过。
  - 调用方：重构操作者（W1 收口）。
  - tested 策略：自有单测。
  - 核验命令：测试: fn_work/tests 全绿+两反例 XPASS（继承 R1/R2/R3）。
  - **refresh_frozen_values** [L1|改造]
    - 职责：仅更新受 R2/R3 修复影响的冻结值（select 名字序→值序、bench 错位→seated），每处更新留双口径注记（旧值/新值/原因）；其余冻结值（agent 整局、评级、契约）零改动。
    - 签名意图：输入: 修复影响清单 / 输出: 更新后测试文件+变更注记 / 错误: 影响清单外冻结值变动即失败。
    - 调用方：migrate_snapshot_suite。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: migrate_snapshot_suite。

## 功能块 portable_test_baseline ← R6

（块引言：测试基线机器无关化——LF 重建索引/打包工件、Windows-only 断言双平台化、机器语境声明；仓外 .gitattributes 不可加（范围外），一切靠工件+测试双兼容。）

- **portable_test_baseline** [L0|新增]
  - 职责：基线无关化入口——工件重建、断言修正、语境声明三件编排。
  - 签名意图：输入: 无（CLI）/ 输出: 重建后工件+声明文档 / 错误: 重建后主力机基线回退即失败。
  - 调用方：重构操作者（W2）。
  - tested 策略：自有单测。
  - 核验命令：fresh Linux clone 0 环境性失败 + Windows 主力机基线不回退（继承 R6）。
  - **regenerate_artifacts_lf** [L1|新增]
    - 职责：以 LF 重新生成 index.json 类工件与打包件并重算登记 sha（消除 CRLF 变体双值）。
    - 签名意图：输入: 工件源 / 输出: LF 工件+新 sha 登记 / 错误: 生成不确定即失败。
    - 调用方：portable_test_baseline。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: portable_test_baseline。
  - **relax_platform_assertions** [L1|改造]
    - 职责：修正 2 处 Windows-only 断言（normcase 大小写折叠、Path("C:/…").is_absolute）为双平台语义。
    - 签名意图：输入: 测试源 / 输出: 平台无关断言 / 错误: 无。
    - 调用方：portable_test_baseline。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: portable_test_baseline。
  - **declare_machine_context** [L1|新增]
    - 职责：基线机器语境声明（"990+2 仅主力机"历史口径与通用口径并列、数据依赖项显式 skip 标注缺什么）。
    - 签名意图：输入: 基线运行记录 / 输出: 声明文档 / 错误: 无。
    - 调用方：portable_test_baseline。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: portable_test_baseline。

## 功能块 package_minimal_repro_set ← R19

（块引言：最小可复算集入库——golden JSON/灾难局回放/语料 manifest+样例/对手池种子定义收集入库；体积预算在 fn-scaffold 定桩时定死；其余 ~GB 语料本机保存+依赖清单声明。）

- **package_minimal_repro_set** [L0|新增]
  - 职责：入库编排——收集、预算裁剪、清单生成。
  - 签名意图：输入: 最小集清单+预算 / 输出: 入库文件集+清单 / 错误: 超预算即失败（不许静默截断）。
  - 调用方：重构操作者（W2）。
  - tested 策略：自有单测。
  - 核验命令：fresh clone+最小集跑通：黄金复验/灾难局接合/孪生 smoke/快照全量（继承 R19）。
  - **collect_gate_golden_files** [L1|新增]
    - 职责：定位并收集四类最小集文件（golden/灾难局/manifest+样例/种子定义）。
    - 签名意图：输入: 类别清单 / 输出: 文件集+逐件来源登记 / 错误: 任一类缺失即失败。
    - 调用方：package_minimal_repro_set。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖。
  - **enforce_size_budget** [L1|新增]
    - 职责：单件与总量体积预算断言。
    - 签名意图：输入: 文件集+预算 / 输出: 通过或逐件超标清单 / 错误: 超标抛。
    - 调用方：package_minimal_repro_set。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖。
  - **declare_local_corpus_dependencies** [L1|新增]
    - 职责：非入库语料的依赖声明（哪些结论依赖主力机语料、如何补齐）。
    - 签名意图：输入: 依赖扫描 / 输出: 声明文档 / 错误: 无。
    - 调用方：package_minimal_repro_set。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖。

## 功能块 unify_contract_sources ← R8, R9

（块引言：契约单源化——异常局判定双校验器合并、对手名册 5 处+REQUIRED_OPPONENTS 网格收敛单源、bots 手抄常量对 wheel 断言。）

- **unify_contract_sources** [L0|改造]
  - 职责：单源化编排与一致性测试收口。
  - 签名意图：输入: 无（重构期一次性）/ 输出: 单源模块+一致性测试 / 错误: 双源残留即失败。
  - 调用方：评估链（arena/eval_contract/iterate_gate/check_eval_contract）。
  - tested 策略：自有单测。
  - 核验命令：单点定义 grep 断言+改一处全链生效一致性测试（继承 R8）。
  - **merge_abnormal_reason** [L1|改造]
    - 职责：arena._abnormal_reason 与 eval_contract.game_abnormal_reason 合并为单一实现（字段集分叉对齐后取并集语义）。
    - 签名意图：输入: 对局记录 / 输出: 异常理由或 None / 错误: 无。
    - 调用方：unify_contract_sources（arena/eval_contract 双消费）。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: unify_contract_sources。
  - **single_opponent_roster** [L1|改造]
    - 职责：对手名册单源（11 对手池+网格口径），bots/__init__×2、STANDARD_MATRIX_ORDER、EXPECTED_ELO_ORDER、holdout_matrix_order、REQUIRED_OPPONENTS 全部改为引用。
    - 签名意图：输入: 无（常量模块）/ 输出: 名册真值 / 错误: 无。
    - 调用方：unify_contract_sources 全消费点。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖: unify_contract_sources。
  - **assert_bots_constants_match_wheel** [L1|新增]
    - 职责：bots 五文件 CROPS_INFO/ANIMALS_INFO 与 vendored wheel 常量交叉断言（篡改即红）。
    - 签名意图：输入: 无（测试）/ 输出: 断言结果 / 错误: 不一致抛。
    - 调用方：unify_contract_sources（测试面）。
    - tested 策略：自有单测。
    - 核验命令：篡改变红/正常绿（继承 R9）。

## 功能块 archive_forensic_assets ← R11, R12

（块引言：脚本三档分层落地——归档档移归档区（round23×4/round24×3/v15×3/v143/v3/v31/calibration/v48plus 消融 2+1/profile_v48_gap ≈19 件+bc models 416KB）；保留档 5 件与工具箱档 3 件留主线；**v143 归档前置=run_official_bench 已吸收 seated 实现**（W3 依赖 W1）。）

- **archive_forensic_assets** [L0|新增]
  - 职责：归档编排——三档清单核验、归档区落位、主线清理。
  - 签名意图：输入: 三档清单 / 输出: 归档区+主线残留断言通过 / 错误: v143 未吸收即拒绝归档 v143。
  - 调用方：重构操作者（W3）。
  - tested 策略：自有单测。
  - 核验命令：归档件不在主线 import 路径（grep）+保留档逐件可跑（继承 R11）。
  - **partition_script_tiers** [L1|新增]
    - 职责：按 requirements R11 清单把 57 脚本分三档并产出迁移映射。
    - 签名意图：输入: 脚本清单 / 输出: {保留,工具箱,归档} 映射 / 错误: 未分类件即失败。
    - 调用方：archive_forensic_assets。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖。
  - **archive_bc_models** [L1|新增]
    - 职责：bc models 416KB 权重件移证据归档区+清单登记（R12）。
    - 签名意图：输入: models 目录 / 输出: 归档登记 / 错误: 无。
    - 调用方：archive_forensic_assets。
    - tested 策略：上游覆盖。
    - 核验命令：新结构代码树 grep 零命中（继承 R12）。

## 功能块 relocate_library_modules ← R15

- **relocate_library_modules** [L0|改造]
  - 职责：market_ledger 从 scripts/ 归位库区，import 链更新。
  - 签名意图：输入: 无（重构期一次性）/ 输出: 新库位+更新后 import / 错误: 断链即失败。
  - 调用方：sell_plan_reconciliation 等消费者。
  - tested 策略：自有单测。
  - 核验命令：scripts/ 无无入口库件扫描断言+全量测试绿（继承 R15）。
  - **scan_for_library_misplacement** [L1|新增]
    - 职责：扫描 scripts/ 检出无 main/argparse 的库件（防复发）。
    - 签名意图：输入: 目录 / 输出: 库件清单 / 错误: 无。
    - 调用方：relocate_library_modules（+常驻测试）。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖。

## 功能块 downgrade_dormant_assets ← R13, R14

- **downgrade_dormant_assets** [L0|新增]
  - 职责：gym_env/llm_provider 移实验区（dormant 标注）；economy/redlines 移测试资产区；主线 import 图断言收口。
  - 签名意图：输入: 无（重构期一次性）/ 输出: 分区后布局 / 错误: 主线依赖残留即失败。
  - 调用方：重构操作者（W3）。
  - tested 策略：自有单测。
  - 核验命令：主线 import 图不含四件+冒烟显式引用实验区（继承 R13/R14）。
  - **prune_mainline_import_graph** [L1|新增]
    - 职责：解析新结构 import 图并断言主线不依赖实验区/测试资产区。
    - 签名意图：输入: 布局根 / 输出: import 图+违例清单 / 错误: 违例抛。
    - 调用方：downgrade_dormant_assets（+常驻测试）。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖。

## 功能块 sync_documentation ← R7, R16, R18

- **sync_documentation** [L0|改造]
  - 职责：文档层一致性收口编排（bc 记录修正/CODEMAP 勘误退役/probes 策略显式化）。
  - 签名意图：输入: 无（重构期一次性）/ 输出: 更新后文档集 / 错误: 对账失败即失败。
  - 调用方：重构操作者（W4）。
  - tested 策略：自有单测（对账脚本）。
  - 核验命令：gap_table §一清单逐项清零（继承 R16）。
  - **fix_bc_track_records** [L1|改造]
    - 职责：bc_track/README 复现命令路径修正；issues/03/08/04-07 票面状态与 JOURNAL 对齐。
    - 签名意图：输入: JOURNAL 台账 / 输出: 修正后 README+票面 / 错误: 无。
    - 调用方：sync_documentation。
    - tested 策略：上游覆盖。
    - 核验命令：复现命令逐条可 cd+票账一致（继承 R7）。
  - **retire_codemap_with_errata** [L1|新增]
    - 职责：CODEMAP 4 失准处勘误记录后随新结构落地退役（新结构以 responsibility.md+包文档替代）。
    - 签名意图：输入: 勘误清单 / 输出: 勘误记录+退役标记 / 错误: 无。
    - 调用方：sync_documentation。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖（继承 R16/R19-勘误部分）。
  - **codify_probes_policy** [L1|新增]
    - 职责：exports/probes 策略显式化（结论 .md 全入库、数据中间物 gitignore）+现存 6 份摘要一致性核对。
    - 签名意图：输入: probes 现状 / 输出: 策略文档+核对结果 / 错误: 不一致清单非空即失败。
    - 调用方：sync_documentation。
    - tested 策略：上游覆盖。
    - 核验命令：上游覆盖（继承 R18）。

## 功能块 record_governance_dispositions ← R4, R17, R21

- **record_governance_dispositions** [L0|新增]
  - 职责：治理处置记录编排（双源归源/蓝图失效声明/active_candidate 降级）。
  - 签名意图：输入: 处置清单 / 输出: fn_docs 处置记录 / 错误: 无。
  - 调用方：重构操作者（W4）。
  - tested 策略：自有单测（记录 schema）。
  - 核验命令：处置记录存在+键完整（继承 R4/R17/R21 验收）。
  - **write_dual_source_provenance** [L1|新增]
    - 职责：dadee25a 双源血统记录（kaitofukami 08-31 首拉+ahmedberatozer 09-20 拉回，各自日期/sha/许可现状，原创归属标"两账号间未定"）；全库对外引用处去单源断言（旧树 PROVENANCE/v48plus README 的物理统一=迁移副本中执行，旧树战后）。
    - 签名意图：输入: 两源证据 / 输出: 统一血统记录 / 错误: 证据缺失即失败。
    - 调用方：record_governance_dispositions。
    - tested 策略：上游覆盖。
    - 核验命令：fn_docs 记录含两源+未定声明+grep 无单源断言残留（继承 R4）。
  - **declare_blueprint_cmd_invalidation** [L1|新增]
    - 职责：蓝图 2 条失效验收 cmd 的留档声明（指向不存在文件+09-01 后 /accept 静默事实）；物理修订=战后 /attack，本函数只声明。
    - 签名意图：输入: 蓝图 cmd 清单 / 输出: 失效声明文档 / 错误: 无。
    - 调用方：record_governance_dispositions。
    - tested 策略：上游覆盖。
    - 核验命令：声明存在（继承 R17）。
  - **demote_active_candidate_ledger** [L1|新增]
    - 职责：active_candidate.json 降级历史台账的处置记录（动作本身=09-30 收口后执行，本函数产出记录与时点闸）。
    - 签名意图：输入: 现状快照 / 输出: 降级预案记录 / 错误: 时点未到即拒绝执行动作（只许记录）。
    - 调用方：record_governance_dispositions。
    - tested 策略：上游覆盖。
    - 核验命令：预案记录存在+时点闸断言（继承 R21）。
