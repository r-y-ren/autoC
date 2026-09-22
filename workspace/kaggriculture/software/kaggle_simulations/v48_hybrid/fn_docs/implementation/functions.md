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
