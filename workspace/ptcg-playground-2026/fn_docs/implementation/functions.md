# functions.md —— 函数级实现清单（唯一状态真值）
> fn-implement 独占更新。**代码是真值，本表只是导航。**
> **改任何状态前必须先跑核验命令、在对话中贴出输出，绿了才许改。**

| 函数 | 批次 | 状态(日期) | 核验命令+摘要 | commit |
|---|---|---|---|---|
| play_local_match | B1 | wired 10-05 | pytest tests/shared → 16 passed（含真局/席位对换/bo1）；b1-smoke 真局落 runs | d76114cc |
| load_agent_callable | B1 | tested 10-05 | pytest -k load_agent → 4 passed | d76114cc |
| assert_no_network | B1 | tested 10-05 | pytest -k assert_no_network → 4 passed | d76114cc |
| write_runs_jsonl | B1 | tested 10-05 | pytest -k write_runs → passed（reload 环境变量隔离） | d76114cc |
| index_source_anchors | B1 | tested 10-05 | pytest -k index_source → 2 passed | d76114cc |
| render_dossier_md | B1 | tested 10-05 | pytest -k render_dossier → 2 passed（六问+四级断言） | d76114cc |
| summarize_pool | B2 | tested 10-05 | 上游覆盖: test_run_judge_pool | — |
| run_judge_pool | B2 | wired 10-05 | pytest -k run_judge_pool + entries/smoke_judge 实跑 40 局（自镜像 h2h 0.6∈[0.35,0.65]） | 见B2 commit |
| serialize_episode | B2 | tested 10-05 | 上游覆盖: test_record_episode | — |
| record_episode | B2 | wired 10-05 | pytest -k record_episode（真局落盘回读+失败标记） | 见B2 commit |
| first_divergence | B2 | tested 10-05 | 上游覆盖: test_diff_episode（纯函数 4 例） | — |
| diff_episode | B2 | wired 10-05 | pytest -k diff_episode（自对拍一致+篡改定位+破损行号） | 见B2 commit |
| probe_engine_facts | B3 | tested 10-05 | 上游覆盖: test_build_engine_dossier（三实验实证：非法判负/同种子不可复现/None 观测） | 见B3 commit |
| build_engine_dossier | B3 | wired 10-05 | pytest + 真跑：docs/methodology/t1+t2 产出（六问行号+受控实验证据节） | 见B3 commit |
| parse_observation | B3 | tested 10-05 | 上游覆盖: test_seed_agent（None/缺段/满段） | 见B3 commit |
| greedy_priority | B3 | tested 10-05 | test_seed_agent v5 语义+血统表含 v1-v5 迭代链 | 见B3 commit |
| load_default_deck | B3 | tested 10-05 | deck.csv 60 行纯数字（引擎源直读） | 见B3 commit |
| guard_rails | B3 | tested 10-05 | 上游覆盖: test_seed_agent（越界/去重/minCount 补足/兜底） | 见B3 commit |
| seed_agent | B3 | wired 10-05 | 锚定标门槛 v2：vs random 0.82/vs first 0.52（60 局）通过；**61 卡字面量 bug 被测试逮住修复**（[3]*34→33） | 见B3 commit |
| validate_bundle_structure | B4 | tested 10-05 | 上游覆盖: test_pack_submission（好/嵌套包） | 见B4/B5 commit |
| sandbox_selfplay_once | B4 | tested 10-05 | 真包解包装载自对弈 OK | 见B4/B5 commit |
| count_daily_quota | B4 | tested 10-05 | 5 限/记账/破损容错 | 见B4/B5 commit |
| pack_submission | B4 | wired 10-05 | entries 等价+真打包双 OK（配额 1/5）；提交 403=账号未接规则（用户动作项） | 见B4/B5 commit |
| kaggle_cli_pull | B5 | tested 10-05 | 上游覆盖: test_fetch_episodes（mock） | 见B4/B5 commit |
| dedup_register | B5 | tested 10-05 | 去重+INDEX 登记行 | 见B4/B5 commit |
| fetch_episodes | B5 | wired 10-05 | mock 流水线绿（失败隔离+seen 持久化）；真实拉取待规则接受 | 见B4/B5 commit |
| extract_behavior_features | B6 | tested 10-05 | 上游覆盖: test_cluster_opponents（first/random 双席真回放） | 见B6/B7 commit |
| cluster_prototypes | B6 | tested 10-05 | 上游覆盖（K∈2-5 简化轮廓，稳定性±1 断言） | 见B6/B7 commit |
| build_counter_matrix | B6 | tested 10-05 | 上游覆盖（CSV 产出断言） | 见B6/B7 commit |
| cluster_opponents | B6 | wired 10-05 | 12 局 first-vs-random 真回放聚出 ≥2 原型+稳定重跑+矩阵/原型卡产出 | 见B6/B7 commit |
| filter_high_scores | B7 | tested 10-05 | 决出局+分位+快胜排序断言 | 见B6/B7 commit |
| aggregate_state_action | B7 | tested 10-05 | 状态键-动作签名计数断言 | 见B6/B7 commit |
| measure_alignment | B7 | tested 10-05 | 上游覆盖: test_mine_assets 端到端 | 见B6/B7 commit |
| emit_asset_spec | B7 | tested 10-05 | T3 硬字段/血统表/可复跑断言 | 见B6/B7 commit |
| mine_assets | B7 | wired 10-05 | 8 局真回放端到端：规格书可复跑同输出+方向性标注正确 | 见B6/B7 commit |
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
