# functions.md —— 函数级实现清单（唯一状态真值）
> fn-implement 独占更新。**代码是真值，本表只是导航。**
> **改任何状态前必须先跑核验命令、在对话中贴出输出，绿了才许改。**
> 核验命令来源：fn_docs/responsibility.md 各函数核验命令字段（继承 requirements 验收）。

| 函数 | 批次 | 状态(日期) | 核验命令+摘要 | commit |
|---|---|---|---|---|
| discover_campaign_roots | B1 | wired 2026-09-21 | pytest tests/shared/test_discover_campaign_roots.py → 8 passed（真实树三根/CWD 无关/四类 fail-closed/零字面路径）；全套件 57P | 16c9ebd |
| run_equivalence_gate | B1 | wired 2026-09-21 | pytest tests/shared/test_run_equivalence_gate.py → 3 passed in 36.79s（旧树默认判据 62P+4xf 实跑 pass；未知判据 fail-closed；裁决键完整） | 19ce465 |
| aggregate_scores | B2 | stub 2026-09-21 | — | — |
| break_ties_by_identity | B2 | stub 2026-09-21 | — | — |
| robust_selection | B2 | stub 2026-09-21 | — | — |
| rollout_with_replay_opponent | B3 | stub 2026-09-21 | — | — |
| evaluate_plan_portfolio | B3 | stub 2026-09-21 | — | — |
| recalculate_affected_history | B3 | stub 2026-09-21 | — | — |
| run_official_bench | B3 | stub 2026-09-21 | — | — |
| fingerprint_engine_constants | B4 | stub 2026-09-21 | — | — |
| guard_replay_profile_engine | B4 | stub 2026-09-21 | — | — |
| refresh_frozen_values | B5 | stub 2026-09-21 | — | — |
| migrate_snapshot_suite | B5 | stub 2026-09-21 | — | — |
| regenerate_artifacts_lf | B6 | stub 2026-09-21 | — | — |
| relax_platform_assertions | B6 | stub 2026-09-21 | — | — |
| declare_machine_context | B6 | stub 2026-09-21 | — | — |
| portable_test_baseline | B6 | stub 2026-09-21 | — | — |
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
