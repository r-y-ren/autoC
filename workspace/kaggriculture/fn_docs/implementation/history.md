# history.md —— 历史表（已完成批次队列，只追加不删改）
> fn-implement 独占更新。每批次完成后尾部追加留痕。

| 完成日期 | 批次 | 任务/函数清单（含操作与来源说明） | 验收摘要 |
|---|---|---|---|
| 2026-09-21 | B1 | discover_campaign_roots, run_equivalence_gate（shared 基座） | 两函数 wired：roots 特征发现 8 测绿（三根/CWD 无关/fail-closed/零字面路径）；等价门旧树基线 pass（62P+4xf 实跑 36.8s）；全套件 60P |
| 2026-09-21 | B2 | aggregate_scores（值序裁切修复）, break_ties_by_identity（语义随迁）, robust_selection（顶层接线） | 26 passed；差分=仅 R3 修复增量；评审见 B2 报告 |
| 2026-09-21 | B3 | rollout_with_replay_opponent（seated 通道，v143 骨架+twin 指纹链）, evaluate_plan_portfolio（聚合委托 robust_selection）, recalculate_affected_history（台账 5 条 SKIP=语料缺机，主力机回填）, run_official_bench（双口径裁决顶层） | 目录 32 passed；R2 反例 [3000.0,1570.0] 全链贯通；期间发现并修正快照套件整局冻结口径（时间治理器墙钟敏感→旗关面冻结） |
| 2026-09-21 | B4 | fingerprint_engine_constants（16 键集+wheel 交叉 14 键）, guard_replay_profile_engine（双重 fail-closed 门） | 17 passed；R5 修复落地 |
| 2026-09-21 | B5（W1 收口） | refresh_frozen_values（22 锚白名单+13 双口径注记）, migrate_snapshot_suite（迁移 66P 反例转常规） | W1 全收口：R2/R3 修复经安全网验证；旧套件原样 |
| 2026-09-21 | B6 | regenerate_artifacts_lf, relax_platform_assertions, declare_machine_context, portable_test_baseline | 28 passed+顶层实跑 pass（全套件 226P）；R6 修复落地（Windows 复检留边界登记） |
| 2026-09-21 | B7（W2 收口） | collect_gate_golden_files, enforce_size_budget, declare_local_corpus_dependencies, package_minimal_repro_set | 25 passed+实跑 ok（6 收集/4 缺失登记，预算 2M/10M，总量 84KB）；W2 全收口 |
| 2026-09-22 | B8 | merge_abnormal_reason（并集单源）, single_opponent_roster（8 站点等值）, assert_bots_constants_match_wheel（wheel 全等）, unify_contract_sources | 33 passed+顶层实跑 ok；R8/R9 修复落地（旧树物理改线战后） |
| 2026-09-22 | B9 | partition_script_tiers, archive_bc_models, archive_forensic_assets（+B7 应修补丁 p1） | 14 passed+顶层 PASS；R11/R12 注册表落地（物理搬移=战后执行清单） |
| 2026-09-22 | B10 | scan_for_library_misplacement, relocate_library_modules | 7 passed+实跑 PASS（检出恰 1 件；R15 注册落地） |
| 2026-09-22 | B11 | prune_mainline_import_graph, downgrade_dormant_assets | 14 passed+实跑 PASS（R13/R14 分区注册；W3 全收口） |
| 2026-09-22 | B12 | observe/decide/build_mission/solve/execute 五迁移件（+B11 注册表路径补丁 p1） | 41 passed；R10 剥离落地（solver 三件/mission all 支/stage 显式化/R20 注释修正）；sha 登记测试兼旧树冻结哨兵 |
| 2026-09-22 | B13 | load_agent_modules, plan_market_orders, run_dawn_planner, record_shadow_telemetry, run_submission_agent（+链基座 _exec_chain 七件+planner 四件迁移） | 73 passed+snapshot 71 双目标+等价门 pass——R1 主体收口：fn_work 链旗关整局逐字节复现旧冻结口径 |
