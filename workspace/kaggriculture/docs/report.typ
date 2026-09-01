// Kaggriculture 战役 III（线上反馈重构版）报告 — m5 成稿 (document/m5-redocument)
// 数据纪律: 全部现行性能数字在编译时从 ../metrics.json 读取并经 m()/um() 键引用渲染;
// round-2 未发生的线上子字段经 .at(key, default: none) 如实渲染为 null; 大纲版占位符已全部替换。
#let data = json("../metrics.json")
#let software = data.at("software")
#let m(key) = software.at("metrics").at(key).at("value")
#let um(key) = software.at("unmeasured").at(key).at("value")
#let fmt(value) = if value == none { "null" } else if type(value) == bool { if value { "true" } else { "false" } } else { str(value) }
#let source(key) = text(size: 8pt, fill: rgb("#555555"), [ #raw("metrics.software." + key)])
#let usource(key) = text(size: 8pt, fill: rgb("#555555"), [ #raw("metrics.software.unmeasured." + key)])
#let record(value) = [#fmt(value.at("W"))W-#fmt(value.at("L"))L-#fmt(value.at("T"))T]
#let wl(value) = [#fmt(value.at("wins"))W-#fmt(value.at("losses"))L-#fmt(value.at("ties"))T]
#let hash64(value) = [#raw(value.slice(0, 32))#linebreak()#raw(value.slice(32, 64))]

// ---- 战役 II（前代）证据变量 ----
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

// ---- 战役 III 证据变量 ----
#let corpus_bytes = m("m1_download_bytes")
#let corpus_gb = str(calc.round(corpus_bytes / 1000000000.0, digits: 2))
#let byband = m("m1_corpus_by_band")
#let opps = m("m2_online_style_opponents")
#let cert = m("m2_opponent_pool_certification")
#let reqopp = m("m2_gate_required_opponents")
#let opps_tests = m("m2_opponent_unit_tests_summary")
#let caps = m("m3_strategy_capability_checks")
#let regr = m("m3_strategy_regression_summary")
#let m3gate = m("m3_development_gate_summary")
#let m3frozen = m("m3_frozen_candidate_identity")
#let m4protocol = m("m4_holdout_protocol")
#let m4seeds = m("m4_holdout_seed_manifest")
#let m4hash = m("m4_holdout_candidate_hash_match")
#let m4iso = m("m4_holdout_seed_domain_isolation")
#let m4run = m("m4_holdout_run_status")
#let m4sched = m("m4_holdout_schedule")
#let m4split = m("m4_holdout_seat_split")
#let m4abn = m("m4_holdout_abnormal_summary")
#let m4overall = m("m4_confirmatory_overall_record")
#let m4pairs = m("m4_confirmatory_pair_records")
#let m4seats = m("m4_confirmatory_seat_records")
#let m4wilson = m("m4_confirmatory_wilson_intervals")
#let m4paired = m("m4_confirmatory_order_independent_statistics")
#let m4trace = m("m4_confirmatory_export_traceability")
#let m4ptr = m4trace.at("json_pointers")
#let m4elo = m("m4_confirmatory_elo_appendix")
#let m4elo_sub = m4elo.at("table").find(t => t.at("name") == "submission")
#let r2 = um("online_feedback_calibration")
#let p_near = m4pairs.find(p => p.at("opponent") == "near_band_diversified")
#let p_tpl = m4pairs.find(p => p.at("opponent") == "template_wheat")
#let p_crop = m4pairs.find(p => p.at("opponent") == "crop_rotator")
#let p_sf = m4pairs.find(p => p.at("opponent") == "self_feed_ranch")

#set document(
  title: "Kaggriculture 农场博弈 Agent 战役 III：线上反馈重构报告（m5 成稿）",
  author: "autoC Kaggriculture 项目组",
  description: "round-1 线上复盘、回放画像与对手池、市场自适应候选与一次性 holdout v2 的成稿报告",
)
#set page(paper: "a4", margin: 2.1cm)
#set text(lang: "zh", region: "cn", size: 10.5pt, font: ("Libertinus Serif", "Microsoft YaHei"))
#set heading(numbering: "1.1")
#set par(justify: true, leading: 0.82em)
#show heading.where(level: 1): it => { v(0.55em); it; v(0.25em) }

#align(center)[
  #v(1.0em)
  #text(size: 20pt, weight: "bold")[Kaggriculture 农场博弈 Agent 战役 III]
  #v(0.35em)
  #text(size: 14pt)[线上反馈重构报告（m5 成稿）]
  #v(0.35em)
  #text(size: 10pt, fill: gray)[document m5-redocument 成稿包 | 全部性能数字经 metrics 键引用渲染 | 数据源: workspace/kaggriculture/metrics.json]
]

= 摘要

本报告是战役 III（线上反馈重构版）的 m5 成稿版。战役 II 建立的证据链——候选身份冻结、开发/确认种子隔离、AB/BA 双座位、异常 fail-closed、正式 export 原子发布与一次性独立 holdout——被战役 III 整体继承, 并扩展到画像驱动的线上风格对手池。第一轮线上反馈（依赖真实线上提交, 人工执行）在公共天梯留下 #fmt(um("online_ladder_games")) 局台账战绩 #fmt(r2.at("round1_public_record")), 其失利回放复盘产生的失败模式清单驱动了本战役的语料、对手池与候选重构。#usource("online_ladder_games") #usource("online_feedback_calibration")

回放语料与画像管线落地官方 episodes 语料 #fmt(m("m1_corpus_episodes_total")) 局（异常剔除 #fmt(m("m1_corpus_abnormal_excluded")) 局）、画像档案 #fmt(m("m1_profiles_generated")) 份, 原始回放字节量 #fmt(corpus_bytes)（合 #corpus_gb GB）, 构建耗时 #fmt(m("m1_corpus_runtime_seconds")) 秒。#source("m1_corpus_episodes_total") #source("m1_corpus_abnormal_excluded") #source("m1_profiles_generated") #source("m1_download_bytes") #source("m1_corpus_runtime_seconds")

四个画像参数化线上风格对手全部通过冻结弱池认证（各 #fmt(cert.at("online_style").at("crop_rotator").at("games")) 局 #record(cert.at("online_style").at("crop_rotator"))）, 门禁必测名单由 #fmt(reqopp.at("before").len()) 个扩至 #fmt(reqopp.at("after").len()) 个（旧成员全保留）, 契约检查通过, 对手单测 #fmt(opps_tests.at("total")) 项与全量测试 #fmt(opps_tests.at("full_suite_total")) 项全部通过。#source("m2_online_style_opponents") #source("m2_opponent_pool_certification") #source("m2_gate_required_opponents") #source("m2_gate_contract_check_pass") #source("m2_opponent_unit_tests_summary")

市场自适应候选在含线上风格对手的完整开发门 #fmt(m3gate.at("actual_games")) 局中取得 #wl(m3gate.at("candidate_record"))（异常 #fmt(m3gate.at("abnormal_games")) 局）, 冻结身份 SHA-256 为 #hash64(m3frozen.at("sha256"))。#source("m3_development_gate_summary") #source("m3_frozen_candidate_identity")

一次性 holdout v2（attempt #fmt(m4run.at("index"))）与全部 #fmt(m4iso.at("historical_count")) 个历史种子零交集, 全池 #fmt(m4sched.at("actual_games")) 局零异常; 确认子集 #fmt(m4overall.at("games")) 局战绩 #record(m4overall), score #fmt(m4overall.at("score_rate")), Wilson 95% 区间 [#fmt(m4overall.at("wilson95").at(0)), #fmt(m4overall.at("wilson95").at(1))]; 顺序无关成对估计 #fmt(m4paired.at("estimate")), Student-t 区间 [#fmt(m4paired.at("ci95").at(0)), #fmt(m4paired.at("ci95").at(1))]。#source("m4_holdout_run_status") #source("m4_holdout_seed_domain_isolation") #source("m4_holdout_schedule") #source("m4_holdout_abnormal_summary") #source("m4_confirmatory_overall_record") #source("m4_confirmatory_order_independent_statistics")

上述本地结果绑定固定的本地 8 对手池, 不外推为天梯实力、名次或获奖结论。逐对记录中 near_band_diversified #record(p_near) 与 template_wheat #record(p_tpl) 如实列为本候选在当前固定对手池上的短板。round-2 线上提交尚未发生, 对应 unmeasured 子字段保持 null 如实渲染（见第 6、9 章）。前代 holdout 总体 score（#fmt(overall.at("score_rate"))）保留为前代候选（SHA 前缀 #raw(m("m2b_candidate_sha256").slice(0, 8))）在固定对手池上的历史实测结论, 受固定对手池分布偏移、不外推新候选限制约束（第 5 章）。#source("confirmatory_overall_record") #source("m2b_candidate_sha256")

= 战役定位与范围

== 交付定位

战役 III 的目标是把第一轮线上反馈转化为可验证的重构: 回放语料与画像管线、线上风格对手池、市场自适应候选引擎、一次性独立 holdout v2 与提交 SOP v4。可交付对象保持 stdlib-only、离线自包含 bot 与完整证据链; 本波（m5）交付成稿包——本报告成稿、SOP v4 完整手册（`workspace/kaggriculture/docs/sop-v4.md`）与 document 分片 metrics。账号报名、线上提交、Validation Episode 检查、round-2 采样与最终版本选择仍由队伍人工执行, 本报告不把流程约束写成已执行事实。

== 证据边界

战役 II 确认结果绑定前代候选 #raw(m("m2b_candidate_sha256")), holdout 运行前、中、后哈希一致性判定为 #fmt(hash_match.at("pass")); 战役 III 确认结果绑定候选 #hash64(m3frozen.at("sha256")), m4 holdout 的 frozen/before/after 一致性判定为 #fmt(m4hash.at("pass"))。两代确认互不迁移: 任何策略或候选字节变化都构成新候选, 旧确认结果与旧 holdout 种子不得为新候选背书或复用。#source("m2b_candidate_sha256") #source("holdout_candidate_hash_match") #source("m3_frozen_candidate_identity") #source("m4_holdout_candidate_hash_match")

两代 holdout 种子均已在运行完成后公开: 战役 II 清单哈希 #raw(seed_manifest.at("sha256")), 战役 III 清单哈希 #raw(m4seeds.at("sha256"))。公开后的这些种子不得再用于新的独立 holdout; 新候选必须冻结新身份并使用新的独立确认种子。#source("holdout_seed_manifest") #source("m4_holdout_seed_manifest")

历史披露(仅此一处): 1500.8 / 36-0 属于固定 p0; 复用开发种子; 顺序敏感 Elo; 非确认性; 不可外推线上。该记录仅用于说明战役 II 审计为何重开, 不参与本报告主结论。#source("m2_elo_ratings_full_pool")

== 禁止外推

本报告不把本地 holdout 等同于线上对手分布, 不对竞赛名次、奖项结果或线上能力作结论。第一轮线上证据样本极小且对手分布未知, 只用于失败模式复盘与画像设计输入; round-2 尚未发生, `unmeasured.online_*` 的 round-2 子字段保持未回填。LLM 真实 A/B 未发生, 对应值保持 #fmt(um("llm_ab_win_rate")); 预算闸真实触发值保持 #fmt(um("llm_ab_budget_gate_hits"))。#usource("llm_ab_win_rate") #usource("llm_ab_budget_gate_hits")

= 方法与选型

== 候选身份锁定

// CHECK:METHOD_IDENTITY
战役 II: 开发门候选 SHA 与冻结 SHA 均为 #raw(gate.at("candidate_sha256")), holdout 三点哈希由正式 export 记录, 一致性判定 #fmt(hash_match.at("pass"))。战役 III: 开发门候选 SHA 为 #raw(m3gate.at("candidate_sha256")), 冻结身份含 manifest 与快照（#raw(m3frozen.at("manifest")), 快照解码哈希 #raw(m3frozen.at("decoded_sha256"))）, m4 holdout 一致性判定 #fmt(m4hash.at("pass"))。#source("development_gate_summary") #source("frozen_candidate_identity") #source("holdout_candidate_hash_match") #source("m3_development_gate_summary") #source("m3_frozen_candidate_identity") #source("m4_holdout_candidate_hash_match")

== 种子域与一次性规则

// CHECK:METHOD_SEEDS
战役 II 协议记录 one_time=#fmt(protocol.at("one_time")), candidate_change_invalidates=#fmt(protocol.at("candidate_change_invalidates")), seed_count=#fmt(protocol.at("seed_count")), 与历史种子交集 #fmt(m("holdout_seed_domain_isolation").at("overlap_count")), 隔离判定 #fmt(m("holdout_seed_domain_isolation").at("pass"))。战役 III 的 m4 协议同构: one_time=#fmt(m4protocol.at("one_time")), seed_count=#fmt(m4protocol.at("seed_count")), 历史种子排除清单规模扩至 #fmt(m4protocol.at("historical_seed_exclusion_count"))（覆盖战役 II 登记的开发/回归种子、已公布 holdout 种子与线上实测 episode 对应 seed）, 交集计数 #fmt(m4iso.at("overlap_count")), 隔离判定 #fmt(m4iso.at("pass"))。#source("holdout_protocol") #source("holdout_seed_domain_isolation") #source("m4_holdout_protocol") #source("m4_holdout_seed_domain_isolation")

种子只有在运行完成后公开。两代公开清单都是既有证据的一部分, 不再具备新独立确认集资格。

== AB/BA 与完整矩阵

// CHECK:METHOD_ABBA
每个候选-对手-种子组合均以 AB/BA 镜像执行。战役 II 正式矩阵实际 #fmt(schedule.at("actual_games")) 局（AB #fmt(seat_split.at("ab_games")) / BA #fmt(seat_split.at("ba_games")), 缺失镜像 #fmt(seat_split.at("missing_mirrors"))）; 战役 III m4 正式矩阵实际 #fmt(m4sched.at("actual_games")) 局（AB #fmt(m4split.at("ab_games")) / BA #fmt(m4split.at("ba_games")), 缺失镜像 #fmt(m4split.at("missing_mirrors"))）。#source("holdout_schedule") #source("holdout_seat_split") #source("m4_holdout_schedule") #source("m4_holdout_seat_split")

== 异常关闭与原子发布

// CHECK:METHOD_FAIL_CLOSED
生产契约检查判定为 #fmt(m("m2a_gate_contract_check_pass")); 它覆盖缺失必测对手、单座位、INVALID、畸形 tie、种子域不符和 exploratory 冒充正式 PASS 的拒绝路径。战役 III 在扩至 #fmt(reqopp.at("after").len()) 对手的必测名单上重跑同族检查, 判定为 #fmt(m("m2_gate_contract_check_pass"))（含缺对手赛程与单座位赛程的拒绝复验, 以及战役 II 冻结 export 的 official 模式复验）。#source("m2a_gate_contract_check_pass") #source("m2_gate_contract_check_pass") #source("m2_gate_required_opponents")

// CHECK:METHOD_ATOMIC
export 安全检查判定为 #fmt(m("m2a_export_safety_check_pass")); 正式结果只在 schema、语义和跨字段验证完成后发布, 开发或失败产物不得覆盖正式 export。#source("m2a_export_safety_check_pass")

= 战役 II 四阶段波次执行记录

== m2a: 评估器加固

完整软件测试通过 #fmt(m("m2a_tests_passed"))/#fmt(m("m2a_tests_total")); 生产 gate 契约与 export 安全检查分别为 #fmt(m("m2a_gate_contract_check_pass")) 和 #fmt(m("m2a_export_safety_check_pass"))。修复前的一次开发门已明确 invalidated=#fmt(m("m2a_complete_gate_invalidated")), 不再作为合入证据。#source("m2a_tests_passed") #source("m2a_tests_total") #source("m2a_gate_contract_check_pass") #source("m2a_export_safety_check_pass") #source("m2a_complete_gate_invalidated")

== m2b: 策略修复与冻结

定向策略/契约测试通过 #fmt(repair.at("passed"))/#fmt(repair.at("total")), failed=#fmt(repair.at("failed"))。检查项记录末日零资本支出=#fmt(repair_checks.at("terminal_day_no_capex"))、末日现收处置=#fmt(repair_checks.at("terminal_day_liquidation"))、购买观察确认=#fmt(repair_checks.at("purchase_confirmation"))、shed 库存预留=#fmt(repair_checks.at("shed_reservation"))、严格正数量=#fmt(repair_checks.at("positive_quantities"))。#source("strategy_repair_test_summary") #source("strategy_repair_checks")

完整开发门 expected/actual 为 #fmt(gate.at("expected_games"))/#fmt(gate.at("actual_games")), AB/BA 为 #fmt(gate.at("ab_games"))/#fmt(gate.at("ba_games")), 异常 #fmt(gate.at("abnormal_games")), 战绩 #record(gate.at("record")), formal_pass=#fmt(gate.at("formal_pass"))。通过后冻结候选 SHA-256 为 #raw(frozen.at("sha256"))。#source("development_gate_summary") #source("frozen_candidate_identity")

== m2c: 一次性独立 holdout

唯一记录的 attempt index 为 #fmt(run_status.at("index")), 状态 #fmt(run_status.at("status")), published=#fmt(run_status.at("published")), invalidated=#fmt(run_status.at("invalidated"))。正式全矩阵 expected/actual 为 #fmt(schedule.at("expected_games"))/#fmt(schedule.at("actual_games")), 完整性合取判定为 #fmt(m("holdout_integrity_pass"))。#source("holdout_run_status") #source("holdout_schedule") #source("holdout_integrity_pass")

本阶段只发布既有 attempt 的结果。验证动作可以重读并校验正式文件, 但不得重跑、重抽或替换该 holdout。

== m3: 文档重生成（战役 II 收尾）

战役 II 收尾版只消费合并后的 metrics, 将旧开发 Elo 降为历史披露, 将主结论改为逐对 W/L/T、座位拆分、Wilson 区间和顺序无关成对统计。线上与真实 LLM A/B 的未测键继续显示 null。

= 战役 II 实测结果（绑定前代冻结候选）

本章全部数字来自战役 II 正式 export, 绑定前代冻结候选 SHA-256 #raw(m("m2b_candidate_sha256"))。本章总体战绩与 score（#record(overall), #fmt(overall.at("score_rate"))）是前代候选在战役 II 固定对手池上的一次性 holdout 实测历史结论: 固定对手池分布偏移、不外推新候选、不外推线上, 也不得迁移到战役 III 冻结候选（#raw(m3frozen.at("sha256").slice(0, 8))…）; 战役 III 的现行结论以第 8 章为准。#source("m2b_candidate_sha256") #source("confirmatory_overall_record") #source("m3_frozen_candidate_identity")

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

== 线上反馈与未回填项

#table(
  columns: (2.7fr, 1.0fr, 2.5fr),
  align: horizon,
  table.header([*指标*], [*值*], [*含义*]),
  [round-1 线上对局], [#fmt(um("online_ladder_games"))], [依赖真实线上提交, 已按第一轮实测回填],
  [round-1 平台 skill rating], [#fmt(um("online_skill_rating"))], [依赖真实线上提交与平台计分],
  [round-1 反馈校准], [#fmt(r2.at("round1_public_record"))], [第一轮失败模式台账见 exports/online/],
  [round-2 公共战绩], [#fmt(r2.at("round2_public_record", default: none))], [round-2 尚未发生, 如实保持 null],
  [round-2 采样台账], [#fmt(r2.at("round2_sampling_ledger", default: none))], [同上, 见 SOP v4 第 4 节],
  [round-2 回拉复盘], [#fmt(r2.at("round2_pullback_reviews", default: none))], [同上, 见 SOP v4 第 6 节],
  [止损状态], [#fmt(r2.at("stop_loss_status", default: none))], [同上, 见 SOP v4 第 7 节],
  [最终提交 commits], [#fmt(um("final_submission_commits"))], [人工终交锁定尚未回填],
)
#usource("online_ladder_games") #usource("online_skill_rating") #usource("online_feedback_calibration") #usource("final_submission_commits")

= 战役 III 线上反馈复盘（round-1）

// CHECK:R3_ROUND1
本章数字均为线上实测回填（依赖真实线上提交与平台回放, 人工执行）; 样本极小, 全章不外推。

== 公共局战绩与平台评分

第一轮提交（依赖真实线上提交, 人工执行）在公共天梯完成 #fmt(um("online_ladder_games")) 局, 台账战绩 #fmt(r2.at("round1_public_record")), 平台 skill rating 快照为 #fmt(um("online_skill_rating"))。逐局台账与分析文件路径由键内字段给出: #raw(r2.at("ledger")) 与 #raw(r2.at("analysis"))。#usource("online_ladder_games") #usource("online_skill_rating") #usource("online_feedback_calibration")

== 失败模式清单（FM-O1..O4）

对第一轮公共局失利的回放复盘产生失败模式清单: #fmt(r2.at("loss_failure_modes").join("；"))。胜方呈现多元化经济结构, 与我方单一畜群结构形成对照; 这些失败模式构成本轮画像驱动重构的直接输入。#usource("online_feedback_calibration")

== 语料分层与画像输入

分层抽样以 2026-08-29 公共榜单为设计输入, 落地为四档语料: top-20 档 #fmt(byband.at("top20")) 局、top-100 档 #fmt(byband.at("top100")) 局、500-900 近段 #fmt(byband.at("band_500_900")) 局、我方基线 #fmt(byband.at("baseline")) 局（单局可同时计入多档）。全榜排名与队伍总数快照没有 metrics 键, 本版不写数; 该快照只用作抽样设计输入, 不作名次结论。#source("m1_corpus_by_band")

== 复盘进入战役 III 的链路

复盘结论按固定链路进入工程: 失败模式清单先行, 再定义画像维度（资金曲线、畜群轨迹、作物轮替、雇佣强度、外购饲料、卖出价格门控、终局行为）, 经跨局复核后参数化线上风格对手, 最终进入门禁与候选重构。同选手不少于 3 局一致才可作为对手参数依据; 单局结论一律标 exploratory。

= 战役 III 波次执行记录

本章记录 m1-m4 四个里程碑的实测落地; 全部数字经 metrics 键引用渲染, 无占位符残留。

== m1: 回放语料与画像

// CHECK:R3_M1_CORPUS
官方 episodes index 解析与按需下载落地: 入库 #fmt(m("m1_corpus_episodes_total")) 局, 完整性校验（双方 DONE、720 步）后异常剔除 #fmt(m("m1_corpus_abnormal_excluded")) 局, 逐局结构化画像 #fmt(m("m1_profiles_generated")) 份（每局两座位各一份）, 原始回放字节量 #fmt(corpus_bytes)（合 #corpus_gb GB, 原始回放仅落 gitignored 数据目录）, 构建耗时 #fmt(m("m1_corpus_runtime_seconds")) 秒。分层构成见第 6.3 节。#source("m1_corpus_episodes_total") #source("m1_corpus_abnormal_excluded") #source("m1_profiles_generated") #source("m1_download_bytes") #source("m1_corpus_runtime_seconds")

画像层面对强段与基线的结构性差异形成多项一致发现: 强段雇佣强度更高、终局抛售占比更高、作物收入结构更多元、外购饲料与卖出价格门控更精细。带数字的参数依据只经 `m2_online_style_opponents` 键的 param_basis 字段进入本文（见 7.2 节）, 本节不另行罗列未经键化的数字。

== m2: 线上风格对手池

// CHECK:R3_M2_POOL
依据跨局复核后的画像参数实现四个线上风格对手（主打 bot 只用同选手不少于 3 局一致发现; near_band_diversified 显式 exploratory）:

#let o0 = opps.at(0)
#let o1 = opps.at(1)
#let o2 = opps.at(2)
#let o3 = opps.at(3)
- *#fmt(o0.at("name"))* — 原型 #fmt(o0.at("prototype")); 画像档案 #fmt(o0.at("profile_archives").len()) 份; exploratory=#fmt(o0.at("exploratory_params"))
- *#fmt(o1.at("name"))* — 原型 #fmt(o1.at("prototype")); 画像档案 #fmt(o1.at("profile_archives").len()) 份; exploratory=#fmt(o1.at("exploratory_params"))
- *#fmt(o2.at("name"))* — 原型 #fmt(o2.at("prototype")); 画像档案 #fmt(o2.at("profile_archives").len()) 份; exploratory=#fmt(o2.at("exploratory_params"))
- *#fmt(o3.at("name"))* — 原型 #fmt(o3.at("prototype")); 画像档案 #fmt(o3.at("profile_archives").len()) 份; exploratory=#fmt(o3.at("exploratory_params"))

#text(size: 8.5pt, fill: rgb("#555555"))[参数依据（键内 param_basis 字段）: #fmt(o0.at("param_basis"))；#fmt(o1.at("param_basis"))；#fmt(o2.at("param_basis"))；#fmt(o3.at("param_basis"))]
#source("m2_online_style_opponents")

认证（对冻结弱池, 阈值 #fmt(cert.at("threshold"))）: 四个线上风格对手与三个强族对手全部达标, threshold_met_by_all=#fmt(cert.at("threshold_met_by_all"))。#source("m2_opponent_pool_certification")

#table(
  columns: (1.7fr, 0.7fr, 1.1fr, 0.9fr, 1.6fr),
  align: horizon,
  table.header([*对手*], [*games*], [*W-L-T*], [*win_rate*], [*vs greedy_carrot 均差*]),
  [#fmt(o0.at("name"))], [#fmt(cert.at("online_style").at("crop_rotator").at("games"))], [#record(cert.at("online_style").at("crop_rotator"))], [#fmt(cert.at("online_style").at("crop_rotator").at("win_rate"))], [#fmt(cert.at("online_style").at("crop_rotator").at("vs_greedy_carrot").at("avg_margin"))],
  [#fmt(o1.at("name"))], [#fmt(cert.at("online_style").at("template_wheat").at("games"))], [#record(cert.at("online_style").at("template_wheat"))], [#fmt(cert.at("online_style").at("template_wheat").at("win_rate"))], [#fmt(cert.at("online_style").at("template_wheat").at("vs_greedy_carrot").at("avg_margin"))],
  [#fmt(o2.at("name"))], [#fmt(cert.at("online_style").at("self_feed_ranch").at("games"))], [#record(cert.at("online_style").at("self_feed_ranch"))], [#fmt(cert.at("online_style").at("self_feed_ranch").at("win_rate"))], [#fmt(cert.at("online_style").at("self_feed_ranch").at("vs_greedy_carrot").at("avg_margin"))],
  [#fmt(o3.at("name"))], [#fmt(cert.at("online_style").at("near_band_diversified").at("games"))], [#record(cert.at("online_style").at("near_band_diversified"))], [#fmt(cert.at("online_style").at("near_band_diversified").at("win_rate"))], [#fmt(cert.at("online_style").at("near_band_diversified").at("vs_greedy_carrot").at("avg_margin"))],
  [#fmt(m("m2_opponent_pool_certification").at("strong_family_recertified").at("cow_baron").at("games"))#text(size: 8pt)[（强族复认证）]], [—], [#record(m("m2_opponent_pool_certification").at("strong_family_recertified").at("cow_baron"))], [#fmt(m("m2_opponent_pool_certification").at("strong_family_recertified").at("cow_baron").at("win_rate"))], [—],
)
#source("m2_opponent_pool_certification")

门禁必测名单由 #fmt(reqopp.at("before").len()) 个（#fmt(reqopp.at("before").join(", "))）扩至 #fmt(reqopp.at("after").len()) 个（新增 #fmt(reqopp.at("new_members_added").join(", "))）, 旧成员全保留（old_members_retained=#fmt(reqopp.at("old_members_retained"))）, 名单哈希 #hash64(reqopp.at("required_list_sha256")), 完整门预期 #fmt(reqopp.at("gate_games_expected")) 局; 缺失必测对手与单座位赛程均被契约检查拒绝（missing_opponent_schedule_rejected=#fmt(reqopp.at("missing_opponent_schedule_rejected"))）。对手单测 #fmt(opps_tests.at("passed"))/#fmt(opps_tests.at("total")), 全量测试 #fmt(opps_tests.at("full_suite_passed"))/#fmt(opps_tests.at("full_suite_total")); 覆盖面: #fmt(opps_tests.at("coverage").join("；"))。#source("m2_gate_required_opponents") #source("m2_opponent_unit_tests_summary")

== m3: 市场自适应候选与冻结

// CHECK:R3_M3_CANDIDATE
候选引擎按画像发现重构: 轮作触发与价格下限、外购饲料护栏、劳动扩容强度、第三象限扩张、终局囤积-倾销与末日停喂、死价格冻结泛化, 并保留 m2b 全部修复不回退。分项能力回归判定:

#table(
  columns: (2.4fr, 1.0fr, 0.8fr),
  align: horizon,
  table.header([*能力组（键内字段）*], [*verdict*], [*tests*]),
  [rotation_trigger_and_price_floors], [#fmt(caps.at("rotation_trigger_and_price_floors").at("verdict"))], [#fmt(caps.at("rotation_trigger_and_price_floors").at("tests"))],
  [external_feed_guardrail], [#fmt(caps.at("external_feed_guardrail").at("verdict"))], [#fmt(caps.at("external_feed_guardrail").at("tests"))],
  [labour_expansion_intensity], [#fmt(caps.at("labour_expansion_intensity").at("verdict"))], [#fmt(caps.at("labour_expansion_intensity").at("tests"))],
  [third_quadrant_expansion], [#fmt(caps.at("third_quadrant_expansion").at("verdict"))], [#fmt(caps.at("third_quadrant_expansion").at("tests"))],
  [endgame_hoard_dump_and_stop_feed], [#fmt(caps.at("endgame_hoard_dump_and_stop_feed").at("verdict"))], [#fmt(caps.at("endgame_hoard_dump_and_stop_feed").at("tests"))],
  [dead_price_freeze_generalized], [#fmt(caps.at("dead_price_freeze_generalized").at("verdict"))], [#fmt(caps.at("dead_price_freeze_generalized").at("tests"))],
  [m2b_fixes_no_regression], [#fmt(caps.at("m2b_fixes_no_regression").at("verdict"))], [#fmt(caps.at("m2b_fixes_no_regression").at("tests"))],
)
#source("m3_strategy_capability_checks")

策略回归: m3 新增测试 #fmt(regr.at("m3_tests_passed"))/#fmt(regr.at("m3_tests_total")), m2b 保留测试 #fmt(regr.at("m2b_preserved_tests_passed"))/#fmt(regr.at("m2b_preserved_tests_total")), 完整套件 #fmt(regr.at("complete_suite_passed"))/#fmt(regr.at("complete_suite_total"))。#source("m3_strategy_regression_summary")

完整开发门（#fmt(m3gate.at("required_opponents").len()) 必测对手 x seeds #fmt(m3gate.at("seeds").map(s => str(s)).join("-")) x AB/BA = #fmt(m3gate.at("actual_games")) 局, expected #fmt(m3gate.at("expected_games"))）: 战绩 #wl(m3gate.at("candidate_record")), AB/BA #fmt(m3gate.at("seat_split").at("AB"))/#fmt(m3gate.at("seat_split").at("BA")), 异常 #fmt(m3gate.at("abnormal_games")), formal_pass=#fmt(m3gate.at("formal_pass")), 耗时 #fmt(m3gate.at("elapsed_seconds")) 秒。逐对开发门记录:

#table(
  columns: (1.7fr, 1.0fr, 0.9fr, 1.3fr),
  align: horizon,
  table.header([*opponent*], [*W-L-T*], [*win_rate*], [*avg_margin*]),
  [cow_baron], [#wl(m3gate.at("per_opponent").at("cow_baron"))], [#fmt(m3gate.at("per_opponent").at("cow_baron").at("win_rate"))], [#fmt(m3gate.at("per_opponent").at("cow_baron").at("avg_margin"))],
  [melon_hoarder], [#wl(m3gate.at("per_opponent").at("melon_hoarder"))], [#fmt(m3gate.at("per_opponent").at("melon_hoarder").at("win_rate"))], [#fmt(m3gate.at("per_opponent").at("melon_hoarder").at("avg_margin"))],
  [expansionist], [#wl(m3gate.at("per_opponent").at("expansionist"))], [#fmt(m3gate.at("per_opponent").at("expansionist").at("win_rate"))], [#fmt(m3gate.at("per_opponent").at("expansionist").at("avg_margin"))],
  [baseline_wheat], [#wl(m3gate.at("per_opponent").at("baseline_wheat"))], [#fmt(m3gate.at("per_opponent").at("baseline_wheat").at("win_rate"))], [#fmt(m3gate.at("per_opponent").at("baseline_wheat").at("avg_margin"))],
  [crop_rotator], [#wl(m3gate.at("per_opponent").at("crop_rotator"))], [#fmt(m3gate.at("per_opponent").at("crop_rotator").at("win_rate"))], [#fmt(m3gate.at("per_opponent").at("crop_rotator").at("avg_margin"))],
  [template_wheat], [#wl(m3gate.at("per_opponent").at("template_wheat"))], [#fmt(m3gate.at("per_opponent").at("template_wheat").at("win_rate"))], [#fmt(m3gate.at("per_opponent").at("template_wheat").at("avg_margin"))],
  [self_feed_ranch], [#wl(m3gate.at("per_opponent").at("self_feed_ranch"))], [#fmt(m3gate.at("per_opponent").at("self_feed_ranch").at("win_rate"))], [#fmt(m3gate.at("per_opponent").at("self_feed_ranch").at("avg_margin"))],
  [near_band_diversified], [#wl(m3gate.at("per_opponent").at("near_band_diversified"))], [#fmt(m3gate.at("per_opponent").at("near_band_diversified").at("win_rate"))], [#fmt(m3gate.at("per_opponent").at("near_band_diversified").at("avg_margin"))],
)
#source("m3_development_gate_summary")

开发门内 self_feed_ranch 与 near_band_diversified 已接近持平, 该信号在 m4 holdout 中进一步显现（第 8 章）。通过后冻结候选身份: 路径 #raw(m3frozen.at("path")), SHA-256 #hash64(m3frozen.at("sha256")), git ref #raw(m3frozen.at("git_ref")), manifest #raw(m3frozen.at("manifest"))（SHA-256 #hash64(m3frozen.at("manifest_sha256"))）, 快照 #raw(m3frozen.at("snapshot"))。#source("m3_frozen_candidate_identity")

== m4: 一次性独立 holdout v2

// CHECK:R3_M4_PROTOCOL
m4 协议: one_time=#fmt(m4protocol.at("one_time")), candidate_change_invalidates=#fmt(m4protocol.at("candidate_change_invalidates")), seed_count=#fmt(m4protocol.at("seed_count")), 历史种子排除清单 #fmt(m4protocol.at("historical_seed_exclusion_count")) 个; 种子在冻结后生成、运行完成后公开, manifest SHA-256 为 #raw(m4seeds.at("sha256"))（attempt #raw(m4seeds.at("attempt_id"))）, 与历史种子交集 #fmt(m4iso.at("overlap_count")), 隔离判定 #fmt(m4iso.at("pass"))。候选哈希三点一致判定 #fmt(m4hash.at("pass"))。#source("m4_holdout_protocol") #source("m4_holdout_seed_manifest") #source("m4_holdout_seed_domain_isolation") #source("m4_holdout_candidate_hash_match")

运行状态: attempt index #fmt(m4run.at("index")), status=#fmt(m4run.at("status")), published=#fmt(m4run.at("published")), invalidated=#fmt(m4run.at("invalidated")); 此前 attempt #fmt(m4run.at("prior_attempt_index")) 的证据保留于 #raw(m4run.at("prior_attempt_evidence"))。运行工作区状态与输入闭包哈希由键内 worktree_state 注记（边界外零改动）。完整矩阵 expected/actual #fmt(m4sched.at("expected_games"))/#fmt(m4sched.at("actual_games")), AB/BA #fmt(m4split.at("ab_games"))/#fmt(m4split.at("ba_games"))（缺失镜像 #fmt(m4split.at("missing_mirrors"))）, 异常局 #fmt(m4abn.at("abnormal_games")), 完整性合取判定 #fmt(m("m4_holdout_integrity_pass"))。#source("m4_holdout_run_status") #source("m4_holdout_schedule") #source("m4_holdout_seat_split") #source("m4_holdout_abnormal_summary") #source("m4_holdout_integrity_pass")

= 战役 III 实测结果（m4 holdout v2, 绑定 m3 冻结候选）

本章数字绑定战役 III 冻结候选 SHA-256 #hash64(m3frozen.at("sha256")), 对手池为 m2 扩展后的 #fmt(m3gate.at("required_opponents").len()) 个必测对手。全部结论仅在本地官方引擎与该固定对手池上成立, 不外推为天梯实力、名次或获奖结论。#source("m3_frozen_candidate_identity") #source("m3_development_gate_summary")

== 总体与区间

// CHECK:R3_RESULT_OVERALL
冻结候选确认战绩为 #record(m4overall), games=#fmt(m4overall.at("games")), score=#fmt(m4overall.at("score_rate"))。#source("m4_confirmatory_overall_record")

// CHECK:R3_RESULT_INTERVALS
#table(
  columns: (2.2fr, 1.2fr, 2.3fr),
  align: horizon,
  table.header([*统计量*], [*估计*], [*区间*]),
  [逐局 score 的 Wilson 区间], [#fmt(m4overall.at("score_rate"))], [[#fmt(m4wilson.at("overall").at(0)), #fmt(m4wilson.at("overall").at(1))]],
  [每 (opponent, seed) AB/BA 成对均值; unit=#fmt(m4paired.at("unit_count"))], [#fmt(m4paired.at("estimate"))], [[#fmt(m4paired.at("ci95").at(0)), #fmt(m4paired.at("ci95").at(1))]],
)
#source("m4_confirmatory_wilson_intervals") #source("m4_confirmatory_order_independent_statistics")

Wilson 方法为 #fmt(m4wilson.at("method")), confidence=#fmt(m4wilson.at("confidence")); 成对统计方法为 #fmt(m4paired.at("method")), order_independent=#fmt(m4paired.at("order_independent")), fit_status=#fmt(m4paired.at("fit_status"))。#source("m4_confirmatory_wilson_intervals") #source("m4_confirmatory_order_independent_statistics")

== 对手记录

// CHECK:R3_RESULT_PAIRS
#table(
  columns: (1.6fr, 0.7fr, 0.9fr, 0.9fr, 1.5fr),
  align: horizon,
  table.header([*opponent*], [*games*], [*W-L-T*], [*score*], [*Wilson interval*]),
  [#fmt(m4pairs.at(0).at("opponent"))], [#fmt(m4pairs.at(0).at("games"))], [#record(m4pairs.at(0))], [#fmt(m4pairs.at(0).at("score_rate"))], [[#fmt(m4pairs.at(0).at("wilson95").at(0)), #fmt(m4pairs.at(0).at("wilson95").at(1))]],
  [#fmt(m4pairs.at(1).at("opponent"))], [#fmt(m4pairs.at(1).at("games"))], [#record(m4pairs.at(1))], [#fmt(m4pairs.at(1).at("score_rate"))], [[#fmt(m4pairs.at(1).at("wilson95").at(0)), #fmt(m4pairs.at(1).at("wilson95").at(1))]],
  [#fmt(m4pairs.at(2).at("opponent"))], [#fmt(m4pairs.at(2).at("games"))], [#record(m4pairs.at(2))], [#fmt(m4pairs.at(2).at("score_rate"))], [[#fmt(m4pairs.at(2).at("wilson95").at(0)), #fmt(m4pairs.at(2).at("wilson95").at(1))]],
  [#fmt(m4pairs.at(3).at("opponent"))], [#fmt(m4pairs.at(3).at("games"))], [#record(m4pairs.at(3))], [#fmt(m4pairs.at(3).at("score_rate"))], [[#fmt(m4pairs.at(3).at("wilson95").at(0)), #fmt(m4pairs.at(3).at("wilson95").at(1))]],
  [#fmt(m4pairs.at(4).at("opponent"))], [#fmt(m4pairs.at(4).at("games"))], [#record(m4pairs.at(4))], [#fmt(m4pairs.at(4).at("score_rate"))], [[#fmt(m4pairs.at(4).at("wilson95").at(0)), #fmt(m4pairs.at(4).at("wilson95").at(1))]],
  [#fmt(m4pairs.at(5).at("opponent"))], [#fmt(m4pairs.at(5).at("games"))], [#record(m4pairs.at(5))], [#fmt(m4pairs.at(5).at("score_rate"))], [[#fmt(m4pairs.at(5).at("wilson95").at(0)), #fmt(m4pairs.at(5).at("wilson95").at(1))]],
  [#fmt(m4pairs.at(6).at("opponent"))], [#fmt(m4pairs.at(6).at("games"))], [#record(m4pairs.at(6))], [#fmt(m4pairs.at(6).at("score_rate"))], [[#fmt(m4pairs.at(6).at("wilson95").at(0)), #fmt(m4pairs.at(6).at("wilson95").at(1))]],
  [#fmt(m4pairs.at(7).at("opponent"))], [#fmt(m4pairs.at(7).at("games"))], [#record(m4pairs.at(7))], [#fmt(m4pairs.at(7).at("score_rate"))], [[#fmt(m4pairs.at(7).at("wilson95").at(0)), #fmt(m4pairs.at(7).at("wilson95").at(1))]],
)
#source("m4_confirmatory_pair_records")

// CHECK:R3_BOUNDARY
逐对记录如实呈现: 对 cow_baron、melon_hoarder、expansionist、baseline_wheat 四对全胜（各 #fmt(m4pairs.at(3).at("games")) 局）, crop_rotator #record(p_crop), self_feed_ranch #record(p_sf); near_band_diversified #record(p_near) 胜负各半、template_wheat #record(p_tpl) 接近持平, 如实列为本候选在当前固定对手池上的短板, 是 round-2 复盘与候选迭代的首要输入。本章全部数字不外推为天梯实力、名次或获奖结论。

与前代总体 score（#fmt(overall.at("score_rate"))）的对照仅作审计叙事: 两代数字分别绑定不同候选与不同固定对手池（战役 II 池不含线上风格对手）, 对手池分布偏移使二者不构成跨池可比的能力结论, 互不外推、互不迁移。#source("confirmatory_overall_record")

== 座位记录

// CHECK:R3_RESULT_SEATS
#table(
  columns: (0.8fr, 0.9fr, 1.2fr, 1.0fr, 1.8fr),
  align: horizon,
  table.header([*seat*], [*games*], [*W-L-T*], [*score*], [*Wilson interval*]),
  [AB], [#fmt(m4seats.at("AB").at("games"))], [#record(m4seats.at("AB"))], [#fmt(m4seats.at("AB").at("score_rate"))], [[#fmt(m4seats.at("AB").at("wilson95").at(0)), #fmt(m4seats.at("AB").at("wilson95").at(1))]],
  [BA], [#fmt(m4seats.at("BA").at("games"))], [#record(m4seats.at("BA"))], [#fmt(m4seats.at("BA").at("score_rate"))], [[#fmt(m4seats.at("BA").at("wilson95").at(0)), #fmt(m4seats.at("BA").at("wilson95").at(1))]],
)
#source("m4_confirmatory_seat_records")

== 描述性 Elo 附录（不用于主结论）

该对象角色标签为 #fmt(m4elo.at("role")), order_sensitive=#fmt(m4elo.at("order_sensitive")), k=#fmt(m4elo.at("k")), start=#fmt(m4elo.at("start")); 候选条目 rating #fmt(m4elo_sub.at("rating"))（played #fmt(m4elo_sub.at("played"))）。由于对局输入顺序影响更新轨迹, 该表不用于候选确认、版本门槛或任何线上推断。#source("m4_confirmatory_elo_appendix")

= 提交 SOP v4 要点

本节只收录操作约束要点; 完整手册见 `workspace/kaggriculture/docs/sop-v4.md`（V4-01..V4-44 检查项成稿）。以下均为流程约束, 不是已执行声明; 额度与阈值（每日提交 ≤5 次、每候选 ≤2 次/日、每轮回拉 ≥3 局、公共局累计 ≥6 局且胜率低于 50%）是蓝图契约常量, 不是实测数字。

== 权威身份门

SOP v4 以战役 III 冻结候选 SHA（前缀 #raw(m3frozen.at("sha256").slice(0, 8))）与 m4 正式 export 身份（schema #fmt(m4trace.at("validated_schema")), SHA-256 #hash64(m4trace.at("export_sha256"))）为提交前检查门的权威值, 从 metrics 读取、不以旧报告抄值; 战役 II 身份整段降级为历史记录, 不得为新候选背书。#source("m3_frozen_candidate_identity") #source("m4_confirmatory_export_traceability")

== round-2 天梯采样-回拉-复盘循环

- 每日提交至多 5 次; 每候选至多 2 次/日; 提交前核对当日额度与「最近 2 次提交」跟踪, 新提交不得无意覆盖应保留版本。
- Validation Episode 返回 Error 即停当日提交并上报, 不得以连续重试掩盖错误。
- 每次提交后回拉不少于 3 局公共天梯回放完成复盘, 更新失败模式台账（延续 FM-O 编号族）并滚动更新画像档案; 复盘产出按第 6 章链路进入对手池参数与新候选规则。
- 台账逐次对接 `unmeasured.online_feedback_calibration` 的 round-2 子字段; 当前这些子字段保持 null（依赖真实线上提交, 人工执行）。

== 止损线与转备选

- 触发条件: 新候选线上公共局累计不少于 6 局且胜率低于 50%; 触发后禁止继续本方向调参, 转备选方向接力, 判定与动作记录入 stop_loss_status 子字段并上报队伍。
- 止损是资源分配决策, 不外推为任何线上实力、名次或获奖结论。

= 合规与人机分工

== 合规边界

提交 bot 保持离线、自包含和 stdlib-only; 外部 LLM 不是线上运行依赖。回放画像与线上复盘只用于离线设计, 提交 bot 不依赖外部数据集、LLM 或网络 API。正式结论只消费身份匹配、完整矩阵、零异常且已发布的 export。账号报名、提交、Validation Episode 检查、round-2 采样、提交额度管理和最终锁定均由队伍人工执行, 本报告不把流程约束写成已完成事实。

== 人机分工概要

AI 辅助完成评估器加固、策略修复、测试与本地证据生成, 并依据 metrics 重写文档; 战役 III 中另承担语料画像、线上风格对手实现、候选重构与本成稿文档。人工负责规则复核、候选裁决、Kaggle 账号操作、线上反馈解释、round-2 采样与止损裁决以及最终签字。详细留痕见附录 A。

= 遗留与可复用资产

// CHECK:LIMITATIONS
== 局限

- 当前确认集对手来自既定本地 8 对手池, 不能覆盖未知线上策略分布; near_band_diversified 与 template_wheat 两对短板如实保留（第 8 章）。#source("m4_confirmatory_pair_records")
- 两代 holdout 种子均已公开, 只能复核既有证据, 不得再作为新独立确认集。#source("holdout_seed_manifest") #source("m4_holdout_seed_manifest")
- 任何策略变化都会使旧候选身份与确认结果不再适用于新候选。#source("m4_holdout_protocol")
- round-2 线上提交尚未发生, `unmeasured.online_*` 的 round-2 子字段与最终提交 commits 保持 null, 不以本地管道自检或 holdout 代替。#usource("online_ladder_games") #usource("online_skill_rating") #usource("final_submission_commits")
- 真实 LLM A/B 仍未发生, 对应键保持 null。#usource("llm_ab_win_rate")
- 全榜排名与队伍总数快照没有 metrics 键, 本版不写数（第 6.3 节）。

== 可复用资产

可复用资产包括: 候选 SHA 与冻结清单（manifest + 字节级快照）、AB/BA 调度、种子域隔离、异常 fail-closed、正式 export 事务发布、确认统计到 JSON Pointer 的追溯映射, 以及「新候选必须配新独立确认种子」的治理规则。战役 III 在其上追加: 带来源标注的回放画像档案、画像参数化线上风格对手池、必测名单哈希门, 以及 round-2 天梯采样-回拉-复盘循环与止损线（SOP v4）。

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
  [候选冻结], [记录战役 II/III SHA 与 git ref], [确认该身份对应拟提交版本],
  [一次性确认], [执行既定协议并发布战役 II attempt #fmt(run_status.at("index")) 与战役 III attempt #fmt(m4run.at("index"))], [确认不重跑、不重抽、不择优替换],
  [回放语料与画像], [解析 index、下载 #fmt(corpus_bytes) 字节、画像提取 #fmt(m("m1_profiles_generated")) 份与完整性校验], [抽查档案来源标注并裁决画像可用性],
  [线上风格对手池], [实现 #fmt(opps.len()) 个风格 bot 并执行弱池认证与 #fmt(opps_tests.at("total")) 项单测], [审阅画像参数并裁决对手入库],
  [候选重构], [实现轮作、畜群、饲料、劳动、象限与终局能力及 #fmt(regr.at("complete_suite_total")) 项套件], [审阅行为变化并批准新候选冻结],
  [线上反馈复盘], [整理 round-1 台账与 FM-O 清单, 维护 round-2 采样额度台账接口], [提交、回拉回放、复盘解释与止损裁决],
  [文档], [仅从 metrics 生成报告成稿与 SOP v4], [事实核对、审读与签字],
  [线上操作], [不登录、不提交、不代填未发生值], [报名、提交、反馈回填和终交锁定],
)
]
#source("m2a_gate_contract_check_pass") #source("m2a_export_safety_check_pass") #source("strategy_repair_test_summary") #source("frozen_candidate_identity") #source("holdout_run_status") #source("m1_profiles_generated") #source("m2_online_style_opponents") #source("m2_opponent_unit_tests_summary") #source("m3_strategy_regression_summary")

= 附录 B: 证据追溯与描述性 Elo

// CHECK:TRACEABILITY
== 正式 export 追溯（两代）

#text(size: 9pt)[
#table(
  columns: (1.8fr, 3.8fr),
  align: horizon,
  inset: 4pt,
  table.header([*项目*], [*metrics 读取值*]),
  [战役 II 正式 export], [#raw(trace.at("source"))],
  [战役 II export SHA-256], [#hash64(trace.at("export_sha256"))],
  [战役 II validated schema], [#fmt(trace.at("validated_schema"))],
  [战役 II 候选身份], [#hash64(frozen.at("sha256"))],
  [战役 II 确认总体 Pointer], [#raw(pointers.at("confirmatory_overall_record"))],
  [战役 II 逐对/座位/Wilson/成对/Elo Pointer], [#raw(pointers.at("confirmatory_pair_records")); #raw(pointers.at("confirmatory_seat_records")); #raw(pointers.at("confirmatory_wilson_intervals")); #raw(pointers.at("confirmatory_order_independent_statistics")); #raw(pointers.at("confirmatory_elo_appendix"))],
  [战役 III 正式 export], [#raw(m4trace.at("source"))],
  [战役 III export SHA-256], [#hash64(m4trace.at("export_sha256"))],
  [战役 III validated schema], [#fmt(m4trace.at("validated_schema"))],
  [战役 III 候选身份], [#hash64(m3frozen.at("sha256"))],
  [战役 III 确认总体 Pointer], [#raw(m4ptr.at("m4_confirmatory_overall_record"))],
  [战役 III 逐对/座位/Wilson/成对/Elo Pointer], [#raw(m4ptr.at("m4_confirmatory_pair_records")); #raw(m4ptr.at("m4_confirmatory_seat_records")); #raw(m4ptr.at("m4_confirmatory_wilson_intervals")); #raw(m4ptr.at("m4_confirmatory_order_independent_statistics")); #raw(m4ptr.at("m4_confirmatory_elo_appendix"))],
)
]
#source("confirmatory_export_traceability") #source("m4_confirmatory_export_traceability")

== 描述性 Elo 附录（战役 II, 不用于主结论）

战役 II 该对象角色标签为 #fmt(elo.at("role")), order_sensitive=#fmt(elo.at("order_sensitive")), k=#fmt(elo.at("k")), start=#fmt(elo.at("start"))。它只保留为复核 export 的描述性产物; 由于对局输入顺序会影响更新轨迹, 不用于候选确认、版本门槛或任何线上推断。#source("confirmatory_elo_appendix")

正式证据的唯一数据入口是 `workspace/kaggriculture/metrics.json`; 其映射同时给出两代 export SHA、schema 和各确认性对象的 JSON Pointer, 避免从日志或旧报告手工抄值。文档侧的核对入口为 `m("confirmatory_export_traceability")` 与 `m("m4_confirmatory_export_traceability")` 两个键; 战役 III 新增键的需求与回填对照见 `metrics-keys-r3.md`。
