# history.md —— 历史表（已完成批次队列，只追加不删改）
> fn-implement 独占更新。每批次完成后尾部追加留痕。

| 完成日期 | 批次 | 任务/函数清单（含操作与来源说明） | 验收摘要 |
|---|---|---|---|
| 10-05 | B1 | shared×6: play_local_match/load_agent_callable/assert_no_network/write_runs_jsonl/index_source_anchors/render_dossier_md | 16 tests 绿+真局冒烟（first 2-0 random）落 runs；d76114cc |
| 10-05 | B2 | R1+R3×6: summarize_pool/run_judge_pool/serialize_episode/record_episode/first_divergence/diff_episode | 全套 37 绿；smoke_judge 入口实跑 40 局：自镜像 h2h 0.6 合格；**发现**：random 锚对 first 锚 9-1（锚点强度序反直觉，判决池首战即产出真读数）；修 play_local_match debug=False（agent 异常归引擎判 ERROR 不穿透）；修 summarize 测试断言笔误 |
