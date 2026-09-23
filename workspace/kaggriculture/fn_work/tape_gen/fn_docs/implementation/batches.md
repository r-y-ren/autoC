# batches.md —— 批次表
> tape_gen 梯（档位：子代理批式连推+批间评审；FAIL 即停待裁决）。

| 批次 | 函数清单 | 验收点 |
|---|---|---|
| ▶ T2 | elect_backbone, fork_routes_on_events, verify_replay_fidelity, build_route_library, apply_market_edit_operators, assert_farmer_stream_identity, derive_market_variants | 路由库回放金标准逐字节+变体 farmer 流逐字节 |
| T3 | define_config_space, evaluate_ablation_tree, search_reflector_configs, split_train_holdout, rank_candidates_seated, select_on_holdout | 消融账本+留出分离（对手不相交）+seated 适应度表 |
| T4 | build_candidate_package, run_m1_m2_gates, assemble_and_gate, run_pipeline | 候选包四门+M1（≥0.45）+管线双跑一致 |

## 变更记录
| 日期 | 事件 | 说明 |
|---|---|---|
| 2026-09-23 | 批次计划建立 | 四批 20 函数对齐 responsibility.md |
