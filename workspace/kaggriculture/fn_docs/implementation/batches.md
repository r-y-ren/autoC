# batches.md —— 批次表（待办导航）
> fn-implement 独占更新。▶ = 下一批要完成的任务；未经批间门批准不得增删批次内容。
> 波序对齐 responsibility.md 四波（W1 评估修复 → W2 基线数据 → W3 契约结构 → W4 文档治理+bot 整体迁移）；唯一波间依赖：B9 的 v143 归档前置 B3（bench 吸收 seated 完成）。
> 旧树冻结纪律：一切实现只落 fn_work/ 与 fn_docs/implementation/；[改造] 件的修复发生在 fn_work 副本，旧树零字节变更直至战后 fn-close。

| 批次 | 函数/任务清单 | 验收点 | 注 |
|---|---|---|---|
| ▶ B3 | run_official_bench 子树: rollout_with_replay_opponent, evaluate_plan_portfolio, recalculate_affected_history, run_official_bench | 顶层 wired + 合成回放 me_seat=1 通道=[3000.0,1570.0] + 重算台账落盘 | W1；R2 修复；台账=fn_docs/recalculation_ledger.md |
| B4 | guard_replay_profile_engine 子树: fingerprint_engine_constants, guard_replay_profile_engine | 顶层 wired + 篡改常量红/正常绿 | W1；R5 |
| B5 | migrate_snapshot_suite 子树: refresh_frozen_values, migrate_snapshot_suite | 快照套件迁入 fn_work/tests 全绿 + R2/R3 反例 XPASS | W1 收口；R1 判据中枢 |
| B6 | portable_test_baseline 子树: regenerate_artifacts_lf, relax_platform_assertions, declare_machine_context, portable_test_baseline | 顶层 wired + fresh 语义验证（本 Linux 机 0 环境性失败） | W2；R6 |
| B7 | package_minimal_repro_set 子树: collect_gate_golden_files, enforce_size_budget, declare_local_corpus_dependencies, package_minimal_repro_set | 顶层 wired + 最小集清单+预算断言实跑 | W2；R19；体积预算定桩随批 |
| B8 | unify_contract_sources 子树: merge_abnormal_reason, single_opponent_roster, assert_bots_constants_match_wheel, unify_contract_sources | 顶层 wired + 单点 grep 断言 + 篡改红测试 | W3；R8/R9 |
| B9 | archive_forensic_assets 子树: partition_script_tiers, archive_bc_models, archive_forensic_assets | 归档区落位 + 主线 import 断言 + 保留档可跑 | W3；R11/R12；前置 B3 |
| B10 | relocate_library_modules 子树: scan_for_library_misplacement, relocate_library_modules | 顶层 wired + 库件误置扫描绿 | W3；R15 |
| B11 | downgrade_dormant_assets 子树: prune_mainline_import_graph, downgrade_dormant_assets | 主线 import 图断言绿 | W3；R13/R14 |
| B12 | run_submission_agent 下半（迁移核心 5 件）: observe_opponent_state, decide_macro_mode, build_mission_pack, solve_worker_routes, execute_along_route | 五件 implemented+tested（对旧模块语义随迁测试绿） | W4；子树 10 函数超 8 上限切半；死码不迁（R10） |
| B13 | run_submission_agent 上半: load_agent_modules, plan_market_orders, run_dawn_planner, record_shadow_telemetry, run_submission_agent | 顶层 wired=agent 整链实跑 + run_equivalence_gate 全 pass（快照整局冻结值+黄金哈希） | W4 收口；R1 主体 |
| B14 | sync_documentation 子树: fix_bc_track_records, retire_codemap_with_errata, codify_probes_policy, sync_documentation | 顶层 wired + gap_table §一清单对账清零 | W4；R7/R16/R18 |
| B15 | record_governance_dispositions 子树: write_dual_source_provenance, declare_blueprint_cmd_invalidation, demote_active_candidate_ledger, record_governance_dispositions | 顶层 wired + 处置记录键完整 | W4；R4/R17/R21（R21 物理动作留时点闸） |

## 变更记录（计划层事件：签名微调、需求变更往返、放弃等）
| 日期 | 事件 | 说明 |
|---|---|---|
| 2026-09-21 | 快照套件口径修正（B3 期发现） | 根因=planner-on 整局含时间治理器（0.85s 帽读真实墙钟）→负载抖动跨决策边界即漂移（实测两跑 [81108,70273]/[78199,63920]）；整局逐位冻结改旗关面（三遍逐字节一致 [59730.0,59835.0]），planner-on 改 DONE/零异常/engaged 冒烟；旧 planner-on 冻结值文件头留档已废；门默认口径 62P+4xf 不变（commit dfcf476） |
| 2026-09-21 | B2 签名登记 | robust_select→robust_selection（对齐责任文档命名）；返回结构 dict{best,ranking,strategy,tie_break,aggregates}（旧码同构） |
| 2026-09-21 | 批次计划建立 | 15 批（B1 共享基座 → B15 治理层）；波序对齐 responsibility.md 四波；run_submission_agent 因 10 函数超 8 切 B12/B13 两批 |
