// Kaggriculture 战役 II 审计修订报告 (m3-redocument)
// 数据纪律: 所有现行性能值均在编译时从 ../metrics.json 读取。
#let data = json("../metrics.json")
#let software = data.at("software")
#let m(key) = software.at("metrics").at(key).at("value")
#let um(key) = software.at("unmeasured").at(key).at("value")
#let fmt(value) = if value == none { "null" } else if type(value) == bool { if value { "true" } else { "false" } } else { str(value) }
#let source(key) = text(size: 8pt, fill: rgb("#555555"), [来源键: #raw("metrics.software." + key)])
#let usource(key) = text(size: 8pt, fill: rgb("#555555"), [来源键: #raw("metrics.software.unmeasured." + key)])
#let record(value) = [#fmt(value.at("W"))W-#fmt(value.at("L"))L-#fmt(value.at("T"))T]
#let hash64(value) = [#raw(value.slice(0, 32))#linebreak()#raw(value.slice(32, 64))]

#let frozen = m("frozen_candidate_identity")
#let gate = m("development_gate_summary")
#let repair = m("strategy_repair_test_summary")
#let repair_checks = m("strategy_repair_checks")
#let protocol = m("holdout_protocol")
#let seed_manifest = m("holdout_seed_manifest")
#let hash_match = m("holdout_candidate_hash_match")
#let run_status = m("holdout_run_status")
#let schedule = m("holdout_schedule")
#let seat_split = m("holdout_seat_split")
#let abnormal = m("holdout_abnormal_summary")
#let overall = m("confirmatory_overall_record")
#let pairs = m("confirmatory_pair_records")
#let seats = m("confirmatory_seat_records")
#let wilson = m("confirmatory_wilson_intervals")
#let paired = m("confirmatory_order_independent_statistics")
#let trace = m("confirmatory_export_traceability")
#let pointers = trace.at("json_pointers")
#let elo = m("confirmatory_elo_appendix")

#set document(
  title: "Kaggriculture 农场博弈 Agent 战役 II：评估可信度重建与一次性确认报告",
  author: "autoC Kaggriculture 项目组",
  description: "冻结候选、AB/BA 双座位与一次性独立 holdout 的审计修订报告",
)
#set page(paper: "a4", margin: 2.1cm)
#set text(lang: "zh", region: "cn", size: 10.5pt, font: ("Libertinus Serif", "Microsoft YaHei"))
#set heading(numbering: "1.1")
#set par(justify: true, leading: 0.82em)
#show heading.where(level: 1): it => { v(0.55em); it; v(0.25em) }

#align(center)[
  #v(1.0em)
  #text(size: 20pt, weight: "bold")[Kaggriculture 农场博弈 Agent 战役 II]
  #v(0.35em)
  #text(size: 14pt)[评估可信度重建与一次性确认报告]
  #v(0.35em)
  #text(size: 10pt, fill: gray)[m3-redocument 审计修订版 | 数据源: workspace/metrics.json]
]

= 摘要

本报告替代旧 m3-polish 结论, 以候选身份冻结、开发/确认种子隔离、AB/BA 双座位、异常 fail-closed、正式 export 原子发布和一次性独立 holdout 组成证据链。冻结候选 SHA-256 为 #raw(frozen.at("sha256")); 该身份通过开发门后用于唯一已发布且未失效的 holdout。#source("frozen_candidate_identity") #source("holdout_run_status")

开发门完成 #fmt(gate.at("actual_games")) 局, 战绩 #record(gate.at("record")); 策略修复定向测试 #fmt(repair.at("passed"))/#fmt(repair.at("total")) 通过。#source("development_gate_summary") #source("strategy_repair_test_summary")

正式全矩阵预期/实际均为 #fmt(schedule.at("expected_games"))/#fmt(schedule.at("actual_games")), AB/BA 为 #fmt(seat_split.at("ab_games"))/#fmt(seat_split.at("ba_games")), 缺失镜像 #fmt(seat_split.at("missing_mirrors")), 异常局 #fmt(abnormal.at("abnormal_games"))。#source("holdout_schedule") #source("holdout_seat_split") #source("holdout_abnormal_summary")

冻结候选在确认子集共 #fmt(overall.at("games")) 局, 战绩 #record(overall), score #fmt(overall.at("score_rate")), Wilson 区间 [#fmt(overall.at("wilson95").at(0)), #fmt(overall.at("wilson95").at(1))]。以每个 (opponent, seed) 的 AB/BA 成对得分为单位, #fmt(paired.at("unit_count")) 个单位的估计为 #fmt(paired.at("estimate")), Student-t 区间 [#fmt(paired.at("ci95").at(0)), #fmt(paired.at("ci95").at(1))]。#source("confirmatory_overall_record") #source("confirmatory_order_independent_statistics")

这些结果仅描述本地官方引擎和既定对手池。线上对局、线上 rating 与线上反馈校准仍显示为 #fmt(um("online_ladder_games")) / #fmt(um("online_skill_rating")) / #fmt(um("online_feedback_calibration")), 不由本地结果代填。#usource("online_ladder_games") #usource("online_skill_rating") #usource("online_feedback_calibration")

= 战役定位与范围

== 交付定位

本轮目标不是继续追逐单一开发集分数, 而是重建可审计评估流程并为一个冻结候选形成一次性确认记录。可交付对象包括 stdlib-only bot、冻结身份、完整开发门、已发布正式 export、确认性统计、本报告与 SOP v3。账号操作、线上提交和最终版本选择仍由队伍人工执行。

== 证据边界

确认结果绑定候选 #raw(m("m2b_candidate_sha256")), 且 holdout 运行前、中、后的哈希一致性判定为 #fmt(hash_match.at("pass"))。#source("m2b_candidate_sha256") #source("holdout_candidate_hash_match")

holdout 种子现已公开, 清单哈希为 #raw(seed_manifest.at("sha256"))。公开后的这些种子不得再用于新的独立 holdout; 任何策略或候选字节变化都必须冻结新身份并使用新的独立确认种子。#source("holdout_seed_manifest") #source("holdout_protocol")

历史披露(仅此一处): 1500.8 / 36-0 属于固定 p0; 复用开发种子; 顺序敏感 Elo; 非确认性; 不可外推线上。该记录仅用于说明审计为何重开, 不参与本报告主结论。#source("m2_elo_ratings_full_pool")

== 禁止外推

本报告不把本地 holdout 等同于线上对手分布, 不对竞赛名次、奖项结果或线上能力作结论。LLM 真实 A/B 未发生, 对应值保持 #fmt(um("llm_ab_win_rate")); 预算闸真实触发值保持 #fmt(um("llm_ab_budget_gate_hits"))。#usource("llm_ab_win_rate") #usource("llm_ab_budget_gate_hits")

= 方法与选型

== 候选身份锁定

// CHECK:METHOD_IDENTITY
候选路径、SHA-256、git ref 与冻结清单由 `frozen_candidate_identity` 给出。开发门候选 SHA 与冻结 SHA 均为 #raw(gate.at("candidate_sha256")), holdout 的 frozen/before/after 三个值均由正式 export 记录, 一致性判定为 #fmt(hash_match.at("pass"))。#source("development_gate_summary") #source("frozen_candidate_identity") #source("holdout_candidate_hash_match")

== 种子域与一次性规则

// CHECK:METHOD_SEEDS
正式协议记录 one_time=#fmt(protocol.at("one_time")), candidate_change_invalidates=#fmt(protocol.at("candidate_change_invalidates")), seed_count=#fmt(protocol.at("seed_count")); holdout 与历史已用种子的交集计数为 #fmt(m("holdout_seed_domain_isolation").at("overlap_count")), 隔离判定为 #fmt(m("holdout_seed_domain_isolation").at("pass"))。#source("holdout_protocol") #source("holdout_seed_domain_isolation")

种子只有在运行完成后公开。当前公开清单是既有证据的一部分, 不再具备新独立确认集资格。后续若策略变化, 只能建立新候选、新清单和新的一次性确认记录。

== AB/BA 与完整矩阵

// CHECK:METHOD_ABBA
每个候选-对手-种子组合均以 AB/BA 镜像执行。正式矩阵实际局数为 #fmt(schedule.at("actual_games")), 其中 AB #fmt(seat_split.at("ab_games")) 局、BA #fmt(seat_split.at("ba_games")) 局, 缺失镜像 #fmt(seat_split.at("missing_mirrors"))。#source("holdout_schedule") #source("holdout_seat_split")

== 异常关闭与原子发布

// CHECK:METHOD_FAIL_CLOSED
生产契约检查判定为 #fmt(m("m2a_gate_contract_check_pass")); 它覆盖缺失必测对手、单座位、INVALID、畸形 tie、种子域不符和 exploratory 冒充正式 PASS 的拒绝路径。#source("m2a_gate_contract_check_pass")

// CHECK:METHOD_ATOMIC
export 安全检查判定为 #fmt(m("m2a_export_safety_check_pass")); 正式结果只在 schema、语义和跨字段验证完成后发布, 开发或失败产物不得覆盖正式 export。#source("m2a_export_safety_check_pass")

= 四阶段波次执行记录

== m2a: 评估器加固

完整软件测试通过 #fmt(m("m2a_tests_passed"))/#fmt(m("m2a_tests_total")); 生产 gate 契约与 export 安全检查分别为 #fmt(m("m2a_gate_contract_check_pass")) 和 #fmt(m("m2a_export_safety_check_pass"))。修复前的一次开发门已明确 invalidated=#fmt(m("m2a_complete_gate_invalidated")), 不再作为合入证据。#source("m2a_tests_passed") #source("m2a_tests_total") #source("m2a_gate_contract_check_pass") #source("m2a_export_safety_check_pass") #source("m2a_complete_gate_invalidated")

== m2b: 策略修复与冻结

定向策略/契约测试通过 #fmt(repair.at("passed"))/#fmt(repair.at("total")), failed=#fmt(repair.at("failed"))。检查项记录末日零资本支出=#fmt(repair_checks.at("terminal_day_no_capex"))、末日现收处置=#fmt(repair_checks.at("terminal_day_liquidation"))、购买观察确认=#fmt(repair_checks.at("purchase_confirmation"))、shed 库存预留=#fmt(repair_checks.at("shed_reservation"))、严格正数量=#fmt(repair_checks.at("positive_quantities"))。#source("strategy_repair_test_summary") #source("strategy_repair_checks")

完整开发门 expected/actual 为 #fmt(gate.at("expected_games"))/#fmt(gate.at("actual_games")), AB/BA 为 #fmt(gate.at("ab_games"))/#fmt(gate.at("ba_games")), 异常 #fmt(gate.at("abnormal_games")), 战绩 #record(gate.at("record")), formal_pass=#fmt(gate.at("formal_pass"))。通过后冻结候选 SHA-256 为 #raw(frozen.at("sha256"))。#source("development_gate_summary") #source("frozen_candidate_identity")

== m2c: 一次性独立 holdout

唯一记录的 attempt index 为 #fmt(run_status.at("index")), 状态 #fmt(run_status.at("status")), published=#fmt(run_status.at("published")), invalidated=#fmt(run_status.at("invalidated"))。正式全矩阵 expected/actual 为 #fmt(schedule.at("expected_games"))/#fmt(schedule.at("actual_games")), 完整性合取判定为 #fmt(m("holdout_integrity_pass"))。#source("holdout_run_status") #source("holdout_schedule") #source("holdout_integrity_pass")

本阶段只发布既有 attempt 的结果。验证动作可以重读并校验正式文件, 但不得重跑、重抽或替换该 holdout。

== m3: 文档重生成

本版只消费合并后的 metrics, 将旧开发 Elo 降为历史披露, 将主结论改为逐对 W/L/T、座位拆分、Wilson 区间和顺序无关成对统计。线上与真实 LLM A/B 的未测键继续显示 null。

= 实测结果

== 身份与完整性

#table(
  columns: (2.2fr, 2.8fr),
  align: horizon,
  table.header([*审计项*], [*结果*]),
  [冻结候选 SHA-256], [#hash64(frozen.at("sha256"))],
  [holdout 哈希一致], [#fmt(hash_match.at("pass"))],
  [发布 attempt], [index=#fmt(run_status.at("index")); status=#fmt(run_status.at("status")); invalidated=#fmt(run_status.at("invalidated"))],
  [完整矩阵 expected/actual], [#fmt(schedule.at("expected_games")) / #fmt(schedule.at("actual_games"))],
  [AB/BA; missing mirrors], [#fmt(seat_split.at("ab_games")) / #fmt(seat_split.at("ba_games")); #fmt(seat_split.at("missing_mirrors"))],
  [异常局; integrity], [#fmt(abnormal.at("abnormal_games")); #fmt(m("holdout_integrity_pass"))],
)
#source("frozen_candidate_identity") #source("holdout_candidate_hash_match") #source("holdout_run_status") #source("holdout_schedule") #source("holdout_seat_split") #source("holdout_abnormal_summary") #source("holdout_integrity_pass")

== 总体与区间

// CHECK:RESULT_OVERALL
冻结候选确认战绩为 #record(overall), games=#fmt(overall.at("games")), score=#fmt(overall.at("score_rate"))。#source("confirmatory_overall_record")

// CHECK:RESULT_INTERVALS
#table(
  columns: (2.2fr, 1.2fr, 2.3fr),
  align: horizon,
  table.header([*统计量*], [*估计*], [*区间*]),
  [逐局 score 的 Wilson 区间], [#fmt(overall.at("score_rate"))], [[#fmt(wilson.at("overall").at(0)), #fmt(wilson.at("overall").at(1))]],
  [每 (opponent, seed) AB/BA 成对均值; unit=#fmt(paired.at("unit_count"))], [#fmt(paired.at("estimate"))], [[#fmt(paired.at("ci95").at(0)), #fmt(paired.at("ci95").at(1))]],
)
#source("confirmatory_wilson_intervals") #source("confirmatory_order_independent_statistics")

Wilson 方法为 #fmt(wilson.at("method")), confidence=#fmt(wilson.at("confidence")); 成对统计方法为 #fmt(paired.at("method")), order_independent=#fmt(paired.at("order_independent")), fit_status=#fmt(paired.at("fit_status"))。#source("confirmatory_wilson_intervals") #source("confirmatory_order_independent_statistics")

== 对手记录

// CHECK:RESULT_PAIRS
#table(
  columns: (1.6fr, 0.7fr, 0.9fr, 0.9fr, 1.5fr),
  align: horizon,
  table.header([*opponent*], [*games*], [*W-L-T*], [*score*], [*Wilson interval*]),
  [#fmt(pairs.at(0).at("opponent"))], [#fmt(pairs.at(0).at("games"))], [#record(pairs.at(0))], [#fmt(pairs.at(0).at("score_rate"))], [[#fmt(pairs.at(0).at("wilson95").at(0)), #fmt(pairs.at(0).at("wilson95").at(1))]],
  [#fmt(pairs.at(1).at("opponent"))], [#fmt(pairs.at(1).at("games"))], [#record(pairs.at(1))], [#fmt(pairs.at(1).at("score_rate"))], [[#fmt(pairs.at(1).at("wilson95").at(0)), #fmt(pairs.at(1).at("wilson95").at(1))]],
  [#fmt(pairs.at(2).at("opponent"))], [#fmt(pairs.at(2).at("games"))], [#record(pairs.at(2))], [#fmt(pairs.at(2).at("score_rate"))], [[#fmt(pairs.at(2).at("wilson95").at(0)), #fmt(pairs.at(2).at("wilson95").at(1))]],
  [#fmt(pairs.at(3).at("opponent"))], [#fmt(pairs.at(3).at("games"))], [#record(pairs.at(3))], [#fmt(pairs.at(3).at("score_rate"))], [[#fmt(pairs.at(3).at("wilson95").at(0)), #fmt(pairs.at(3).at("wilson95").at(1))]],
  [#fmt(pairs.at(4).at("opponent"))], [#fmt(pairs.at(4).at("games"))], [#record(pairs.at(4))], [#fmt(pairs.at(4).at("score_rate"))], [[#fmt(pairs.at(4).at("wilson95").at(0)), #fmt(pairs.at(4).at("wilson95").at(1))]],
  [#fmt(pairs.at(5).at("opponent"))], [#fmt(pairs.at(5).at("games"))], [#record(pairs.at(5))], [#fmt(pairs.at(5).at("score_rate"))], [[#fmt(pairs.at(5).at("wilson95").at(0)), #fmt(pairs.at(5).at("wilson95").at(1))]],
  [#fmt(pairs.at(6).at("opponent"))], [#fmt(pairs.at(6).at("games"))], [#record(pairs.at(6))], [#fmt(pairs.at(6).at("score_rate"))], [[#fmt(pairs.at(6).at("wilson95").at(0)), #fmt(pairs.at(6).at("wilson95").at(1))]],
  [#fmt(pairs.at(7).at("opponent"))], [#fmt(pairs.at(7).at("games"))], [#record(pairs.at(7))], [#fmt(pairs.at(7).at("score_rate"))], [[#fmt(pairs.at(7).at("wilson95").at(0)), #fmt(pairs.at(7).at("wilson95").at(1))]],
)
#source("confirmatory_pair_records")

== 座位记录

// CHECK:RESULT_SEATS
#table(
  columns: (0.8fr, 0.9fr, 1.2fr, 1.0fr, 1.8fr),
  align: horizon,
  table.header([*seat*], [*games*], [*W-L-T*], [*score*], [*Wilson interval*]),
  [AB], [#fmt(seats.at("AB").at("games"))], [#record(seats.at("AB"))], [#fmt(seats.at("AB").at("score_rate"))], [[#fmt(seats.at("AB").at("wilson95").at(0)), #fmt(seats.at("AB").at("wilson95").at(1))]],
  [BA], [#fmt(seats.at("BA").at("games"))], [#record(seats.at("BA"))], [#fmt(seats.at("BA").at("score_rate"))], [[#fmt(seats.at("BA").at("wilson95").at(0)), #fmt(seats.at("BA").at("wilson95").at(1))]],
)
#source("confirmatory_seat_records")

== 未测线上项

#table(
  columns: (2.7fr, 1.0fr, 2.5fr),
  align: horizon,
  table.header([*指标*], [*值*], [*含义*]),
  [线上对局], [#fmt(um("online_ladder_games"))], [尚无真实线上提交证据],
  [线上 skill rating], [#fmt(um("online_skill_rating"))], [依赖真实线上提交],
  [线上反馈校准], [#fmt(um("online_feedback_calibration"))], [尚未形成新证据],
  [最终提交 commits], [#fmt(um("final_submission_commits"))], [人工终交锁定尚未回填],
)
#usource("online_ladder_games") #usource("online_skill_rating") #usource("online_feedback_calibration") #usource("final_submission_commits")

= 合规与人机分工

== 合规边界

提交 bot 保持离线、自包含和 stdlib-only; 外部 LLM 不是线上运行依赖。正式结论只消费身份匹配、完整矩阵、零异常且已发布的 export。账号报名、提交、Validation Episode 检查、提交额度管理和最终锁定均由队伍人工执行, 本报告不把流程约束写成已完成事实。

== 人机分工概要

AI 辅助完成评估器加固、策略修复、测试与本地证据生成, 并依据 metrics 重写文档。人工负责规则复核、候选裁决、Kaggle 账号操作、线上反馈解释、是否形成新候选以及最终签字。详细留痕见附录 A。

= 遗留与可复用资产

// CHECK:LIMITATIONS
== 局限

- 当前确认集对手来自既定本地池, 不能覆盖未知线上策略分布。
- holdout 种子已公开, 只能复核既有证据, 不得再作为新独立确认集。#source("holdout_seed_manifest")
- 任何策略变化都会使旧候选身份与确认结果不再适用于新候选。#source("holdout_protocol")
- 线上指标与真实 LLM A/B 仍为 null, 不以本地管道自检或 holdout 代替。#usource("online_ladder_games") #usource("online_skill_rating") #usource("llm_ab_win_rate")

== 可复用资产

可复用资产包括: 候选 SHA 与冻结清单、AB/BA 调度、种子域隔离、异常 fail-closed、正式 export 事务发布、确认统计到 JSON Pointer 的追溯映射, 以及“新候选必须配新独立确认种子”的治理规则。

= 附录 A: 人机分工记录

// CHECK:HUMAN_AI
#text(size: 9pt)[
#table(
  columns: (1.2fr, 2.5fr, 2.5fr),
  align: horizon,
  inset: 4pt,
  table.header([*环节*], [*AI 辅助*], [*人工责任*]),
  [评估治理], [实现并验证双座位、隔离、fail-closed 与 export 安全检查], [审阅规则边界并裁决证据是否可用],
  [策略修复], [执行定向测试 #fmt(repair.at("passed"))/#fmt(repair.at("total")), 记录检查项], [审阅行为变化并批准冻结],
  [候选冻结], [记录 SHA #hash64(frozen.at("sha256")) 与 git ref], [确认该身份对应拟提交版本],
  [一次性确认], [执行既定协议并发布 attempt #fmt(run_status.at("index"))], [确认不重跑、不重抽、不择优替换],
  [文档], [仅从 metrics 生成报告与 SOP v3], [事实核对、审读与签字],
  [线上操作], [不登录、不提交、不代填未发生值], [报名、提交、反馈回填和终交锁定],
)
]
#source("m2a_gate_contract_check_pass") #source("m2a_export_safety_check_pass") #source("strategy_repair_test_summary") #source("frozen_candidate_identity") #source("holdout_run_status")

= 附录 B: 证据追溯与描述性 Elo

// CHECK:TRACEABILITY
== 正式 export 追溯

#text(size: 9pt)[
#table(
  columns: (1.8fr, 3.8fr),
  align: horizon,
  inset: 4pt,
  table.header([*项目*], [*metrics 读取值*]),
  [正式 export], [#raw(trace.at("source"))],
  [export SHA-256], [#hash64(trace.at("export_sha256"))],
  [validated schema], [#fmt(trace.at("validated_schema"))],
  [候选身份], [#hash64(frozen.at("sha256"))],
  [确认总体 JSON Pointer], [#raw(pointers.at("confirmatory_overall_record"))],
  [逐对记录 JSON Pointer], [#raw(pointers.at("confirmatory_pair_records"))],
  [座位记录 JSON Pointer], [#raw(pointers.at("confirmatory_seat_records"))],
  [Wilson JSON Pointer], [#raw(pointers.at("confirmatory_wilson_intervals"))],
  [成对统计 JSON Pointer], [#raw(pointers.at("confirmatory_order_independent_statistics"))],
  [Elo JSON Pointer], [#raw(pointers.at("confirmatory_elo_appendix"))],
)
]
#source("confirmatory_export_traceability") #source("frozen_candidate_identity")

== 描述性 Elo 附录(不用于主结论)

该对象的角色标签为 #fmt(elo.at("role")), order_sensitive=#fmt(elo.at("order_sensitive")), k=#fmt(elo.at("k")), start=#fmt(elo.at("start"))。它只保留为复核 export 的描述性产物; 由于对局输入顺序会影响更新轨迹, 不用于候选确认、线上推断或版本门槛。#source("confirmatory_elo_appendix")

正式证据的唯一数据入口是 `workspace/metrics.json`; 其映射同时给出 export SHA、schema 和各确认性对象的 JSON Pointer, 从而避免从日志或旧报告手工抄值。
