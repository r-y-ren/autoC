# batches.md —— 批次表（待办导航）
> fn-implement 独占更新。▶ = 下一批要完成的任务；未经批间门批准不得增删批次内容。
> 2026-10-05 用户预授权冲刺（"全批次自动进行，结束后直接 fn-analyze+remote-compute，允许提交"）——批间门不停人，核验照跑照贴，评审照派，报告照发。

| 批次 | 函数/任务清单 | 验收点 | 注 |
|---|---|---|---|
| B1✅ | shared×6: play_local_match, load_agent_callable, assert_no_network, write_runs_jsonl, index_source_anchors, render_dossier_md | shared 全 wired：random vs first 真局跑通落 runs/ | 底座批 |
| B2✅ | R1+R3: summarize_pool, run_judge_pool, serialize_episode, record_episode, first_divergence, diff_episode | smoke_judge 入口绿（自镜像 h2h 0.35-0.65 n≥20）+ record/diff 闭环测试 | W1 里程碑主体 |
| B3✅ | R2+R5: probe_engine_facts, build_engine_dossier, parse_observation, greedy_priority, load_default_deck, guard_rails, seed_agent | T1/T2 产出+seed_agent 对 random≥0.9/first≥0.95+无网络静态检查绿 | guard_rails 提前（seed_agent 依赖）；本批完=W1 波门五查 |
| B4✅ | R4: validate_bundle_structure, sandbox_selfplay_once, count_daily_quota, pack_submission | pack_check 入口绿+submission.tar.gz 产出；**首次提交天梯（用户已授权）** | W2 里程碑 m1 起点 |
| B5✅ | R6: kaggle_cli_pull, dedup_register, fetch_episodes | mock 测试绿+提交后拉 ≥1 条真实 episode 入 references/episodes/ | 依赖 B4 提交产生对局 |
| B6✅ | R7[P1]: extract_behavior_features, cluster_prototypes, build_counter_matrix, cluster_opponents | 合成集≥50 局聚类稳定重跑测试绿；有真实回放则真跑 | W3 里程碑 m2 起点 |
| B7✅ | R8[P1]: filter_high_scores, aggregate_state_action, measure_alignment, emit_asset_spec, mine_assets | 生成器复跑同输出+血统表测试绿 | |
| ▶ B8 | R9a: observe_opponent, decide_tempo, schedule_resources, follow_asset_table, assemble_agent_v2 | 五层装配测试绿+对 random/first 不低于种子件 | guard_rails 已于 B3 |
| B9 | R9b: ab_pair_configs, net_delta_j, pooled_winrate, append_registry_row, run_ab_judgment | A/B 判决全链测试绿（台账行含 net_delta_J/pooled_winrate） | |
| B10 | R10-R12: collect_runs_shards, validate_ladder_readback, prepare_metrics_shards, load_pyxis_env, gsk_judge_smoke, build_gsk_prestudy, check_competition_page, probe_gsk_launch | gsk_prestudy_check 入口绿+probe not-live 落 runs | m4 预研包；全批完→fn-analyze |

## 变更记录（计划层事件：签名微调、需求变更往返、放弃等）
| 日期 | 事件 | 说明 |
|---|---|---|
| 2026-10-05 | 批次计划立表（10 批） | 垂直切片：shared 底座→判决池→种子件→提交链→采集→资产→装配→判决→汇聚；guard_rails 自 B3 提前（seed_agent 终检依赖，调用方跨块） |

| 2026-10-05 | B1 评审采纳（结构性发现） | 引擎洗牌 RNG 在 libcg.so 无种子入口——play_local_match 的 seed 仅为 Python 层统计播种，**同种子不可复现**（评审实证）。口径变更：判决池/A-B 一律按局数收敛（n≥20 起判），不做种子配对等值断言；test_seat_swap 改统计口径。伴修：失败拍号补全扫描、write_runs_jsonl 去 default=str、render_dossier_md 四级守卫 |
| 2026-10-05 | B2 评审采纳 | ①stdout 改受测体视角 self_winrate（原锚视角+vs 措辞致结论写反，勘误见 history）；②debug=False 树外改动补登记（d665ad3e 时点 36+1 非 37 绿，seat_swap 断言修复随 B3）；③n_anchor<1 校验补齐。**垫片说明**：蓝图 software/ 字面 cmd 不建垫片（用户 fn-grill 裁决 fn_work 入口等价执行），W1 波门以 fn_work/entries/smoke_judge.py 等价跑 sw-boot |
