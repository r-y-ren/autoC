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
| collect_gate_golden_files | B7 | stub 2026-09-21 | — | — |
| enforce_size_budget | B7 | stub 2026-09-21 | — | — |
| declare_local_corpus_dependencies | B7 | stub 2026-09-21 | — | — |
| package_minimal_repro_set | B7 | stub 2026-09-21 | — | — |
| merge_abnormal_reason | B8 | stub 2026-09-21 | — | — |
| single_opponent_roster | B8 | stub 2026-09-21 | — | — |
| assert_bots_constants_match_wheel | B8 | stub 2026-09-21 | — | — |
| unify_contract_sources | B8 | stub 2026-09-21 | — | — |
| partition_script_tiers | B9 | stub 2026-09-21 | — | — |
| archive_bc_models | B9 | stub 2026-09-21 | — | — |
| archive_forensic_assets | B9 | stub 2026-09-21 | — | — |
| scan_for_library_misplacement | B10 | stub 2026-09-21 | — | — |
| relocate_library_modules | B10 | stub 2026-09-21 | — | — |
| prune_mainline_import_graph | B11 | stub 2026-09-21 | — | — |
| downgrade_dormant_assets | B11 | stub 2026-09-21 | — | — |
| observe_opponent_state | B12 | stub 2026-09-21 | — | — |
| decide_macro_mode | B12 | stub 2026-09-21 | — | — |
| build_mission_pack | B12 | stub 2026-09-21 | — | — |
| solve_worker_routes | B12 | stub 2026-09-21 | — | — |
| execute_along_route | B12 | stub 2026-09-21 | — | — |
| load_agent_modules | B13 | stub 2026-09-21 | — | — |
| plan_market_orders | B13 | stub 2026-09-21 | — | — |
| run_dawn_planner | B13 | stub 2026-09-21 | — | — |
| record_shadow_telemetry | B13 | stub 2026-09-21 | — | — |
| run_submission_agent | B13 | stub 2026-09-21 | — | — |
| fix_bc_track_records | B14 | stub 2026-09-21 | — | — |
| retire_codemap_with_errata | B14 | stub 2026-09-21 | — | — |
| codify_probes_policy | B14 | stub 2026-09-21 | — | — |
| sync_documentation | B14 | stub 2026-09-21 | — | — |
| write_dual_source_provenance | B15 | stub 2026-09-21 | — | — |
| declare_blueprint_cmd_invalidation | B15 | stub 2026-09-21 | — | — |
| demote_active_candidate_ledger | B15 | stub 2026-09-21 | — | — |
| record_governance_dispositions | B15 | stub 2026-09-21 | — | — |
