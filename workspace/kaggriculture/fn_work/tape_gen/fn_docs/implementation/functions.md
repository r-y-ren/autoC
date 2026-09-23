# functions.md —— 函数级实现清单（唯一状态真值）
> 改状态前先跑核验、贴输出，绿了才许改。

| 函数 | 批次 | 状态(日期) | 核验命令+摘要 | commit |
|---|---|---|---|---|
| load_replay_corpus | T1 | done 2026-09-22 | `python -m pytest tests/mine_trajectories -q`（14 passed）；真实语料 182 局装载（full 182+projection 14 全被 full 压制去重），corpus_hash=7a77a51a…；缺目录 fail-closed/projection 可选 | — |
| extract_and_filter_seats | T1 | done 2026-09-22 | 同上；364 席：保留 162/剔我方 185+克隆 17+其他 0；本队名实测=renyxin；克隆判定 turns1-51 sha256 对 routes.json 六路由（合并 1 签名）；独立复核 3 克隆匹配+2 保留不匹配+1 席全流 719 步逐字节一致 | — |
| mine_trajectories | T1 | done 2026-09-22 | 同上；corpus/trajectory_store.jsonl（364 行，18.8MB）+mining_summary.json+filter_audit.md（12 局抽查）落盘；双跑（含异目录）逐字节一致，store sha=2e337c72… | — |
| elect_backbone | T2 | stub 2026-09-23 | — | — |
| fork_routes_on_events | T2 | stub 2026-09-23 | — | — |
| verify_replay_fidelity | T2 | stub 2026-09-23 | — | — |
| build_route_library | T2 | stub 2026-09-23 | — | — |
| apply_market_edit_operators | T2 | stub 2026-09-23 | — | — |
| assert_farmer_stream_identity | T2 | stub 2026-09-23 | — | — |
| derive_market_variants | T2 | stub 2026-09-23 | — | — |
| define_config_space | T3 | stub 2026-09-23 | — | — |
| evaluate_ablation_tree | T3 | stub 2026-09-23 | — | — |
| search_reflector_configs | T3 | stub 2026-09-23 | — | — |
| split_train_holdout | T3 | stub 2026-09-23 | — | — |
| rank_candidates_seated | T3 | stub 2026-09-23 | — | — |
| select_on_holdout | T3 | stub 2026-09-23 | — | — |
| build_candidate_package | T4 | stub 2026-09-23 | — | — |
| run_m1_m2_gates | T4 | stub 2026-09-23 | — | — |
| assemble_and_gate | T4 | stub 2026-09-23 | — | — |
| run_pipeline | T4 | stub 2026-09-23 | — | — |
