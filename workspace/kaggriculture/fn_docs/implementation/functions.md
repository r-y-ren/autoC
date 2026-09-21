# functions.md —— 函数级实现清单（唯一状态真值）
> fn-implement 独占更新。**代码是真值，本表只是导航。**
> **改任何状态前必须先跑核验命令、在对话中贴出输出，绿了才许改。**
> 核验命令来源：fn_docs/responsibility.md 各函数核验命令字段（继承 requirements 验收）。

| 函数 | 批次 | 状态(日期) | 核验命令+摘要 | commit |
|---|---|---|---|---|
| discover_campaign_roots | B1 | wired 2026-09-21 | pytest tests/shared/test_discover_campaign_roots.py → 8 passed（真实树三根/CWD 无关/四类 fail-closed/零字面路径）；全套件 57P | 16c9ebd |
| run_equivalence_gate | B1 | wired 2026-09-21 | pytest tests/shared/test_run_equivalence_gate.py → 3 passed in 36.79s（旧树默认判据 62P+4xf 实跑 pass；未知判据 fail-closed；裁决键完整） | 19ce465 |
| aggregate_scores | B2 | wired 2026-09-21 | pytest test_aggregate_scores → 12 passed（值序反例 65.0/22.5/55.0/62.5、对照旧名序值失效、trim 边界、旗面不变） | f64015a |
| break_ties_by_identity | B2 | wired 2026-09-21 | pytest test_break_ties_by_identity → 9 passed（0.4%切/0.6%不切/边界==gate 不切；对旧 robust_select 32 点网格差分零不匹配） | 3366285 |
| robust_selection | B2 | wired 2026-09-21 | pytest tests/robust_selection → 26 passed（端到端值序修复生效+K1 守成+注记结构；对旧码差分=仅 R3 修复增量） | 43258a4 |
| rollout_with_replay_opponent | B3 | wired 2026-09-21 | pytest test_rollout… → 10 passed（R2 反例 me_seat=1→[3000.0,1570.0]、me_seat=0 双通道一致、指纹 fail-closed） | bf61656 |
| evaluate_plan_portfolio | B3 | wired 2026-09-21 | pytest test_evaluate… → 6 passed（seated 透传/聚合委托 robust_selection/枚举帽/真引擎 me_seat=1 端到端） | bf3995a |
| recalculate_affected_history | B3 | wired 2026-09-21 | pytest test_recalculate… → 3 passed；真实台账已落盘（G1 五条全 SKIP=replay_data_missing，主力机回填前提已注明） | 9dd79b7 |
| run_official_bench | B3 | wired 2026-09-21 | pytest tests/run_official_bench → 32 passed（双口径裁决结构+offset 分解+异常局 fail-closed+oracle 归因；全套件 110P） | ba686fd |
| fingerprint_engine_constants | B4 | wired 2026-09-21 | pytest test_fingerprint… → 17 passed 之一（16 键集提取/确定性/三类篡改变指纹/wheel 交叉 14 键/登记 roundtrip） | 192b310 |
| guard_replay_profile_engine | B4 | wired 2026-09-21 | pytest tests/guard_replay_profile_engine → 17 passed（双重门：登记指纹+wheel 真值，绕过式改动仍红；skip 仅测试注入） | 0f07e98 |
| refresh_frozen_values | B5 | wired 2026-09-21 | pytest test_refresh_frozen… → 13 passed 之一（22 条锚定编辑表白名单、越界零写入、双口径注记 13 处） | cfd9a25 |
| migrate_snapshot_suite | B5 | wired 2026-09-21 | fn_work/tests/snapshot → 66 passed（R2/R3 反例全转常规 PASSED+零 xfail 残留+其余冻结值逐字节不变）；旧套件 62P+4xf 不动 | 1e0821a |
| regenerate_artifacts_lf | B6 | wired 2026-09-21 | 28 passed 之一（5 集合 100 条目 LF 重建+79 双 sha 登记+打包件 3 不重建登记） | 0b9dab2 |
| relax_platform_assertions | B6 | wired 2026-09-21 | 28 passed 之一（双平台断言工具+三类检出器；fn_work/tests 59 文件 0 命中） | 1deed88 |
| declare_machine_context | B6 | wired 2026-09-21 | 28 passed 之一（machine_context.md 渲染：历史口径/本机实测/skip 清单/双兼容策略） | 19154ce |
| portable_test_baseline | B6 | wired 2026-09-21 | 顶层实跑 verdict=pass：fn_work 全套件 226 passed/148.78s+checks 全真 | 2c9a677 |
| collect_gate_golden_files | B7 | wired 2026-09-21 | 25 passed 之一（四类收集/缺失登记回填/未知类 fail-closed） | 5adfd38 |
| enforce_size_budget | B7 | wired 2026-09-21 | 25 passed 之一（预算 2MiB/10MiB 定桩，超标逐件拒） | 56db9e2 |
| declare_local_corpus_dependencies | B7 | wired 2026-09-21 | 25 passed 之一（G23+skip 清单源，逐条带来源+日期） | 179b5a1 |
| package_minimal_repro_set | B7 | wired 2026-09-21；补丁 2026-09-22 | 实跑 ok=True complete=False（6/4，84,570B）；补丁=去自指字段+战役相对路径，双跑逐字节一致（06e4f32） | 46257f2+06e4f32 |
| merge_abnormal_reason | B8 | wired 2026-09-21 | 33 passed 之一（arena/eval 并集语义单源+24 例 battery） | 636f5fe |
| single_opponent_roster | B8 | wired 2026-09-21 | 33 passed 之一（11 对手池+网格真值，8 站点等值断言） | 766840f |
| assert_bots_constants_match_wheel | B8 | wired 2026-09-21 | 33 passed 之一（五文件常量对 wheel 逐条目全等，漂移抛） | 9223fed |
| unify_contract_sources | B8 | wired 2026-09-21 | 顶层实跑 ok=True（三叶+等值断言集，strict 缺省 fail） | a96e6a4 |
| partition_script_tiers | B9 | wired 2026-09-22 | 14 passed 之一（26 件具名三档+未分类 fail-closed） | 3f8a87c |
| archive_bc_models | B9 | wired 2026-09-22 | 14 passed 之一（models 5 件 419,149B 登记，registry-only） | 7a6b137 |
| archive_forensic_assets | B9 | wired 2026-09-22 | 顶层实跑 PASS（三档 5/3/18、探针 5/5、import 面零命中、v143 前置满足、out_of_scope 30 登记） | dcfc0e6 |
| scan_for_library_misplacement | B10 | wired 2026-09-22 | 7 passed 之一（无入口库件检出，容忍点前缀/动态装载形态） | f741948 |
| relocate_library_modules | B10 | wired 2026-09-22 | 顶层实跑 PASS（旧树扫描 56 件检出恰 market_ledger；库位副本 sha 等价+回探链通；注册表含战后 git mv 方案） | f8676c2 |
| prune_mainline_import_graph | B11 | wired 2026-09-22 | 14 passed 之一（AST 构图+相对导入解析+违例清单） | 0ce39db |
| downgrade_dormant_assets | B11 | wired 2026-09-22；补丁同日 | 顶层实跑 PASS（…）；补丁=注册表路径战役相对化（c5c89e3） | 736138b+c5c89e3 |
| observe_opponent_state | B12 | wired 2026-09-22 | 41 passed 之一（迁移副本 sha 登记+等值抽查；详见 B12 报告） | 7d68322 |
| decide_macro_mode | B12 | wired 2026-09-22 | 41 passed 之一（迁移副本 sha 登记+等值抽查；详见 B12 报告） | 7d68322 |
| build_mission_pack | B12 | wired 2026-09-22 | 41 passed 之一（迁移副本 sha 登记+等值抽查；详见 B12 报告） | 7d68322 |
| solve_worker_routes | B12 | wired 2026-09-22 | 41 passed 之一（迁移副本 sha 登记+等值抽查；详见 B12 报告） | 7d68322 |
| execute_along_route | B12 | wired 2026-09-22 | 41 passed 之一（迁移副本 sha 登记+等值抽查；详见 B12 报告） | 7d68322 |
| load_agent_modules | B13 | wired 2026-09-22 | 73 passed 之一（_MODULE_ORDER 逐字 ast 钉住+装载窗急切导入+sys.path 腰带） | 3820855 |
| plan_market_orders | B13 | wired 2026-09-22 | 73 passed 之一（market 迁移剥 _note_buys） | 3820855 |
| run_dawn_planner | B13 | wired 2026-09-22 | 73 passed 之一（runtime 迁移 4 处适配登记；select 提供者=robust_selection 值序版） | 3820855 |
| record_shadow_telemetry | B13 | wired 2026-09-22 | 73 passed 之一（零剥离逐字节） | 3820855 |
| run_submission_agent | B13 | wired 2026-09-22 | 顶层：等价门 overall=pass；旗关整局逐字节复现；snapshot 双目标 71 passed | 3820855 |
| fix_bc_track_records | B14 | wired 2026-09-22 | 21 passed 之一（9 处修正副本+diff 注册，台账锚定 fail-closed） | edcb993 |
| retire_codemap_with_errata | B14 | wired 2026-09-22 | 21 passed 之一（4 勘误实证+退役标记） | edcb993 |
| codify_probes_policy | B14 | wired 2026-09-22 | 21 passed 之一（6 摘要核对全过；不一致 1=.gitignore 白名单缺口入 postwar） | edcb993 |
| sync_documentation | B14 | wired 2026-09-22 | 顶层实跑 PASS（8/8 对账：#1-7 锚 README v1+#8 锚勘误） | edcb993 |
| write_dual_source_provenance | B15 | wired 2026-09-22 | 18 passed 之一（双源记录+单源断言扫描：11 目标/残留 2=旧树两记录文件战后统一） | 83880f2 |
| declare_blueprint_cmd_invalidation | B15 | wired 2026-09-22 | 18 passed 之一（失效判据反向校验） | 83880f2 |
| demote_active_candidate_ledger | B15 | wired 2026-09-22 | 18 passed 之一（时点闸：≤09-30 只记录，物理降级拒绝） | 83880f2 |
| record_governance_dispositions | B15 | wired 2026-09-22 | 顶层实跑 schema_valid=True（三叶汇编落盘） | 83880f2 |
