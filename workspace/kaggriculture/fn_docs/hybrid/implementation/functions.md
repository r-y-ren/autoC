# functions.md —— 函数级实现清单（补登版）
> 2026-09-23 补登（fn-review 审计 Important 项对账修正）：本梯 F1-F3 压缩执行未留三文档，现按 commit 80b68e2 与 gates_report.json 回溯登记。代码与门禁台账为真值，本表为导航。
> 改状态前先跑核验、贴输出，绿了才许改。

| 函数 | 批次 | 状态(日期) | 核验命令+摘要 | commit |
|---|---|---|---|---|
| apply_midgame_sell_layer | F1 | wired 09-22；v2 09-22；v3 09-23 FAIL 已回退 | 27 passed（v2：tape 透传/day≥13/只补发/N=3 前瞻/基底日历重推导一致性） | 80b68e2 |
| apply_economic_guard | F1 | wired 09-22 | 14 passed（90/90/30+4 帧+day≥10 窄化；未触发同对象返回） | 80b68e2 |
| apply_milestone_monitor | F1 | wired 09-22 | 33 passed（d10-12 里程碑表/只动卖单缝/异常回退） | 80b68e2 |
| load_v48_base | F2 | wired 09-22 | audit_base PASS（前缀逐字+五零改动区分区+三注入点唯一） | 80b68e2 |
| assemble_package | F2 | wired 09-22 | 双跑逐字节一致；旗关零接线字节级；发射四门全绿 | 80b68e2 |
| run_h2h_gate | F3 | wired 09-22 | v1 0-16 → v2 4W-4L-8T 互胜 0.25（FAIL 结构性）；AB/BA 显式席位 | 80b68e2 |
| run_panel_gate | F3 | wired 09-22 | 合成语料 6 局 seated ratio 0.9994 PASS（官方语料=主力机补测） | 80b68e2 |
| check_zero_new_anomalies | F3 | wired 09-22 | kinds=[] 新增=[] PASS | 80b68e2 |
| run_launch_fourgate | F3 | wired 09-22 | 装载 719 obs 零失配/双席 DONE×2/确定性/stdlib | 80b68e2 |
| test_guard_inactive_equivalence | F3 | wired 09-22 | p000 逐字节 4/4；全开≡p100 4/4 | 80b68e2 |
| test_trigger_coverage | F3 | wired 09-22 | 触发面用例齐（v2 后 p2/p3 有效触发 0——正常局零动作实证） | 80b68e2 |
| estimate_lead_margin | F4 | wired 09-25 | patches 113P 之一（三态 basis：farms_money_direct 直读实测/代理/None） | (本批) |
| plan_protective_sells | F4 | wired 09-25 | patches 113P 之一（717-718 让位/帽 4/时点 6,12,18/异常原单） | (本批) |
| build_lead_protection | F4 | wired 09-25 | patches 113P 之一（day≥24 且 lead≥3000 门；未触发原对象） | (本批) |
| assemble_lead_protection_build | F4 | wired 09-25 | v5 包 20421986…/95,489B；四门绿；P4-off 对照≡v4b 逐字节 | (本批) |
| run_replay_gate | F4 | wired 09-25 | 真实跑 0/14（判据 ≥7/14 FAIL；8/14 重演=原值逐位=P4 零足迹自证；EOD 变体仍 0/14） | (本批) |
| run_equivalence_face | F4 | wired 09-25 | 8/8 逐字节一致（构造 4+真实 4） | (本批) |
| run_launch_recheck | F4 | wired 09-25 | 四门真复跑+patches 113P | (本批) |
| verify_lead_protection | F4 | wired 09-25 | 总裁决 FAIL（重演门）落 gates/out/lead_protection_verdict.json | (本批) |
| build_lead_protection | F5 | wired-v2 09-25 | 触发并集+峰寄存器（56 测之一）；v5 重建 042f84f0… | (本批) |
| run_replay_gate | F5 | wired-v2 09-25 | **双臂对照 28 重演：wins 0/14，Δ 正1/负4/零9（净-2642）=杠杆符号确证为负** | (本批) |
| verify_lead_protection | F5 | FAIL-v2 09-25 | gates/out/lead_protection_v2_verdict.json=FAIL；等价面 8/8+四门绿（实现无瑕） | (本批) |
| generate_giant_schedule | G1 | wired 09-23 | 排程 17羊6牛/SE d13/可行性 1 轮 0 违规/收入峰 13634@d17（favorable 情景） | (本批) |
| perform_tape_surgery | G2/G2b | wired 09-23 | 三面重生成（产线 858+卖 723+移动 180 路由日）；v6b 5a532201 四门绿 | (本批) |
| assemble_v6_build | G2/G2b | wired 09-23 | v6 da844619（中间产物）/v6b 5a532201 | (本批) |
| verify_structure_gates | G3 | FAIL 09-23 | 五线 1/5：h2h 0-16（-150k 级）/巨人 0-9/回归 8/8 翻负/四门过/经济面 16-37% | (本批) |
| _cxs_harvest_completable | S1 | tested 09-23 | pytest -k harvest + crosscheck → 6 passed；常数转录 WHEAT/CARROT=48,TOMATO=192,STRAW/MELON=240 | (本批) |
| _cxs_completable_plant_demand | S1 | stub 09-23 | — | — |
| _cxs_seed_surplus | S1 | stub 09-23 | — | — |
| _cxs_seed_truncate | S1 | stub 09-23 | — | — |
| _cxs_agent | S1 | stub 09-23 | — | — |
| append_layer_s_block | S2 | stub 09-23 | — | — |
| build_layer_s_candidate | S2 | stub 09-23 | — | — |
| replay_action_diff | S3 | stub 09-23 | — | — |
| precision_subset_check | S3 | stub 09-23 | — | — |
| constructed_invariant_cases | S3 | stub 09-23 | — | — |
| gate_equivalence_precision | S3 | stub 09-23 | — | — |
| gate_h2h_vs_verbatim | S3 | stub 09-23 | — | — |
| gate_lineage_strength | S3 | stub 09-23 | — | — |
| gate_launch_fourgate_l1 | S3 | stub 09-23 | — | — |
| verify_layer_s_gates | S3 | stub 09-23 | — | — |
