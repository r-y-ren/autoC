# functions.md —— 函数级实现清单（唯一状态真值）
> fn-implement 独占更新。**代码是真值，本表只是导航。**
> **改任何状态前必须先跑核验命令、在对话中贴出输出，绿了才许改。**

| 函数 | 批次 | 状态(日期) | 核验命令+摘要 | commit |
|---|---|---|---|---|
| play_local_match | B1 | stub 10-05 | 待: pytest -k play_local_match | — |
| load_agent_callable | B1 | stub 10-05 | 待: pytest -k load_agent_callable | — |
| assert_no_network | B1 | stub 10-05 | 待: pytest -k assert_no_network | — |
| write_runs_jsonl | B1 | stub 10-05 | 待: pytest -k write_runs_jsonl | — |
| index_source_anchors | B1 | stub 10-05 | 待: pytest -k index_source_anchors | — |
| render_dossier_md | B1 | stub 10-05 | 待: pytest -k render_dossier_md | — |
| summarize_pool | B2 | stub 10-05 | 待: pytest -k summarize_pool（上游覆盖） | — |
| run_judge_pool | B2 | stub 10-05 | 待: pytest -k run_judge_pool + entries/smoke_judge.py 实跑 | — |
| serialize_episode | B2 | stub 10-05 | 待: pytest -k record_episode（上游覆盖） | — |
| record_episode | B2 | stub 10-05 | 待: pytest -k record_episode | — |
| first_divergence | B2 | stub 10-05 | 待: pytest -k diff_episode（上游覆盖） | — |
| diff_episode | B2 | stub 10-05 | 待: pytest -k diff_episode | — |
| probe_engine_facts | B3 | stub 10-05 | 待: pytest -k build_engine_dossier（上游覆盖） | — |
| build_engine_dossier | B3 | stub 10-05 | 待: pytest -k build_engine_dossier | — |
| parse_observation | B3 | stub 10-05 | 待: pytest -k seed_agent（上游覆盖） | — |
| greedy_priority | B3 | stub 10-05 | 待: pytest -k seed_agent（上游覆盖） | — |
| load_default_deck | B3 | stub 10-05 | 待: pack 流（上游覆盖） | — |
| guard_rails | B3 | stub 10-05 | 待: pytest -k guard（跨块调用：seed_agent/assemble_agent_v2） | — |
| seed_agent | B3 | stub 10-05 | 待: pytest -k seed_agent（胜率门槛+None 防御+无网络） | — |
| validate_bundle_structure | B4 | stub 10-05 | 待: pytest -k pack_submission（上游覆盖） | — |
| sandbox_selfplay_once | B4 | stub 10-05 | 待: pytest -k pack_submission（上游覆盖） | — |
| count_daily_quota | B4 | stub 10-05 | 待: pytest -k pack_submission（上游覆盖） | — |
| pack_submission | B4 | stub 10-05 | 待: entries/pack_check.py 实跑绿 | — |
| kaggle_cli_pull | B5 | stub 10-05 | 待: pytest -k fetch_episodes（上游覆盖） | — |
| dedup_register | B5 | stub 10-05 | 待: pytest -k fetch_episodes（上游覆盖） | — |
| fetch_episodes | B5 | stub 10-05 | 待: pytest -k fetch_episodes + 真实拉取 | — |
| extract_behavior_features | B6 | stub 10-05 | 待: pytest -k cluster_opponents（上游覆盖） | — |
| cluster_prototypes | B6 | stub 10-05 | 待: pytest -k cluster_opponents（上游覆盖） | — |
| build_counter_matrix | B6 | stub 10-05 | 待: pytest -k cluster_opponents（上游覆盖） | — |
| cluster_opponents | B6 | stub 10-05 | 待: pytest -k cluster_opponents | — |
| filter_high_scores | B7 | stub 10-05 | 待: pytest -k mine_assets（上游覆盖） | — |
| aggregate_state_action | B7 | stub 10-05 | 待: pytest -k mine_assets（上游覆盖） | — |
| measure_alignment | B7 | stub 10-05 | 待: pytest -k mine_assets（上游覆盖） | — |
| emit_asset_spec | B7 | stub 10-05 | 待: pytest -k mine_assets（上游覆盖） | — |
| mine_assets | B7 | stub 10-05 | 待: pytest -k mine_assets | — |
| observe_opponent | B8 | stub 10-05 | 待: pytest -k assemble_agent_v2（上游覆盖） | — |
| decide_tempo | B8 | stub 10-05 | 待: pytest -k assemble_agent_v2（上游覆盖） | — |
| schedule_resources | B8 | stub 10-05 | 待: pytest -k assemble_agent_v2（上游覆盖） | — |
| follow_asset_table | B8 | stub 10-05 | 待: pytest -k assemble_agent_v2（上游覆盖） | — |
| assemble_agent_v2 | B8 | stub 10-05 | 待: pytest -k assemble_agent_v2 | — |
| ab_pair_configs | B9 | stub 10-05 | 待: pytest -k run_ab_judgment（上游覆盖） | — |
| net_delta_j | B9 | stub 10-05 | 待: pytest -k run_ab_judgment（上游覆盖） | — |
| pooled_winrate | B9 | stub 10-05 | 待: pytest -k run_ab_judgment（上游覆盖） | — |
| append_registry_row | B9 | stub 10-05 | 待: pytest -k run_ab_judgment（上游覆盖） | — |
| run_ab_judgment | B9 | stub 10-05 | 待: pytest -k run_ab_judgment | — |
| collect_runs_shards | B10 | stub 10-05 | 待: pytest -k prepare_metrics_shards（上游覆盖） | — |
| validate_ladder_readback | B10 | stub 10-05 | 待: pytest -k prepare_metrics_shards（上游覆盖） | — |
| prepare_metrics_shards | B10 | stub 10-05 | 待: pytest -k prepare_metrics_shards | — |
| load_pyxis_env | B10 | stub 10-05 | 待: pytest -k gsk（上游覆盖） | — |
| gsk_judge_smoke | B10 | stub 10-05 | 待: pytest -k gsk（上游覆盖） | — |
| build_gsk_prestudy | B10 | stub 10-05 | 待: entries/gsk_prestudy_check.py 实跑绿 | — |
| check_competition_page | B10 | stub 10-05 | 待: pytest -k probe（上游覆盖） | — |
| probe_gsk_launch | B10 | stub 10-05 | 待: pytest -k probe_gsk_launch | — |
