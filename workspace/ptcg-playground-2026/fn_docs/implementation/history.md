# history.md —— 历史表（已完成批次队列，只追加不删改）
> fn-implement 独占更新。每批次完成后尾部追加留痕。

| 完成日期 | 批次 | 任务/函数清单（含操作与来源说明） | 验收摘要 |
|---|---|---|---|
| 10-05 | B1 | shared×6: play_local_match/load_agent_callable/assert_no_network/write_runs_jsonl/index_source_anchors/render_dossier_md | 16 tests 绿+真局冒烟（first 2-0 random）落 runs；d76114cc |
| 10-05 | B2 | R1+R3×6: summarize_pool/run_judge_pool/serialize_episode/record_episode/first_divergence/diff_episode | 全套 37 绿；smoke_judge 入口实跑 40 局：自镜像 h2h 0.6 合格；**发现**：random 锚对 first 锚 9-1（锚点强度序反直觉，判决池首战即产出真读数）；修 play_local_match debug=False（agent 异常归引擎判 ERROR 不穿透；**B2 评审指认：此为计划外树外改动，入表补登记，且在 d665ad3e 时点引入 seat_swap 回归 1 例——36+1 而非 37 绿，断言修复随 B3 提交**）；修 summarize 测试断言笔误 |
| 10-05 | B3 | R2+R5×7: probe_engine_facts/build_engine_dossier/parse_observation/greedy_priority/load_default_deck/guard_rails/seed_agent | 42 tests 全绿；T1/T2 真跑产出（docs/methodology/）；种子件 greedy v1→v5 迭代链（0.17→0.38→0.07→0.80→0.82，教训=引擎选项次序即强基线）；**61 卡 deck 字面量 bug 测试逮住**；R5 门槛锚定标重校（requirements 变更记录，待用户批准） |
| 10-05 | B4+B5 | R4×4+R6×3 | 45 tests 绿；submission.tar.gz 真打包（结构+沙箱自对弈双 OK，配额记账生效）；首提 403（账号未接赛事规则→用户动作项）；采集链 mock 流水线绿（去重/INDEX/失败隔离） |
