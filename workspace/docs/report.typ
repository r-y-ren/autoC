// Kaggriculture 战役 III（线上反馈重构版）报告 — 第 1 波大纲版 (document/wave-1)
// 数据纪律: 所有现行性能值均在编译时从 ../metrics.json 读取; 战役 III 未实测数字一律使用中文占位符,
// 不新增 m()/um() 对尚不存在键的引用; 键需求清单见同目录 metrics-keys-r3.md。
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
  title: "Kaggriculture 农场博弈 Agent 战役 III：线上反馈重构报告（第 1 波大纲版）",
  author: "autoC Kaggriculture 项目组",
  description: "round-1 线上反馈复盘、回放画像与对手池、市场自适应候选与一次性 holdout v2 的大纲版报告",
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
  #text(size: 14pt)[线上反馈重构报告（第 1 波大纲版）]
  #v(0.35em)
  #text(size: 10pt, fill: gray)[document wave-1 大纲包 | 未回填数字以「待 mN 实测」占位 | 数据源: workspace/metrics.json]
]

= 摘要

本报告是战役 III（线上反馈重构版）的第 1 波大纲版。战役 II 建立的证据链——候选身份冻结、开发/确认种子隔离、AB/BA 双座位、异常 fail-closed、正式 export 原子发布与一次性独立 holdout——作为基线资产整体保留。前代冻结候选 SHA-256 为 #raw(frozen.at("sha256")); 该身份通过开发门后用于唯一已发布且未失效的 holdout。#source("frozen_candidate_identity") #source("holdout_run_status")

开发门完成 #fmt(gate.at("actual_games")) 局, 战绩 #record(gate.at("record")); 策略修复定向测试 #fmt(repair.at("passed"))/#fmt(repair.at("total")) 通过。#source("development_gate_summary") #source("strategy_repair_test_summary")

正式全矩阵预期/实际均为 #fmt(schedule.at("expected_games"))/#fmt(schedule.at("actual_games")), AB/BA 为 #fmt(seat_split.at("ab_games"))/#fmt(seat_split.at("ba_games")), 缺失镜像 #fmt(seat_split.at("missing_mirrors")), 异常局 #fmt(abnormal.at("abnormal_games"))。#source("holdout_schedule") #source("holdout_seat_split") #source("holdout_abnormal_summary")

冻结候选在确认子集共 #fmt(overall.at("games")) 局, 战绩 #record(overall), score #fmt(overall.at("score_rate")), Wilson 区间 [#fmt(overall.at("wilson95").at(0)), #fmt(overall.at("wilson95").at(1))]。以每个 (opponent, seed) 的 AB/BA 成对得分为单位, #fmt(paired.at("unit_count")) 个单位的估计为 #fmt(paired.at("estimate")), Student-t 区间 [#fmt(paired.at("ci95").at(0)), #fmt(paired.at("ci95").at(1))]。#source("confirmatory_overall_record") #source("confirmatory_order_independent_statistics")

这些结果仅描述本地官方引擎和既定对手池。线上指标只以真实提交证据回填（对局 #fmt(um("online_ladder_games"))、skill rating #fmt(um("online_skill_rating")) 与反馈台账 #fmt(um("online_feedback_calibration").at("round1_public_record"))），不由本地结果代填。#usource("online_ladder_games") #usource("online_skill_rating") #usource("online_feedback_calibration")

本版新增: 第 6 章以第一轮真实线上证据复盘公共局与失败模式; 第 7 章给出战役 III m1-m5 波次大纲; 第 8 章给出提交 SOP v4 要点。以上章节的未回填数字一律使用中文占位符（如「待 m4 实测」）, 不新增对尚不存在 metrics 键的引用; 键需求清单见 `metrics-keys-r3.md`, SOP 大纲见 `sop-v4-outline.md`。第 5 章战役 II holdout 结论仅对前代冻结候选有效, 不得外推到战役 III 新候选。

= 战役定位与范围

== 交付定位

战役 III 的目标是用第一轮线上反馈驱动重构: 回放语料与画像管线、线上风格对手池、市场自适应候选引擎、一次性独立 holdout v2 与提交 SOP v4。可交付对象保持 stdlib-only、离线自包含 bot 与完整证据链; 本波交付大纲包（本报告 + metrics 键需求清单 + SOP v4 大纲）, 成稿在 m5 波次回填。账号报名、线上提交、Validation Episode 检查与最终版本选择仍由队伍人工执行。

== 证据边界

确认结果绑定候选 #raw(m("m2b_candidate_sha256")), 且 holdout 运行前、中、后的哈希一致性判定为 #fmt(hash_match.at("pass"))。#source("m2b_candidate_sha256") #source("holdout_candidate_hash_match")

holdout 种子现已公开, 清单哈希为 #raw(seed_manifest.at("sha256"))。公开后的这些种子不得再用于新的独立 holdout; 任何策略或候选字节变化都必须冻结新身份并使用新的独立确认种子。#source("holdout_seed_manifest") #source("holdout_protocol")

历史披露(仅此一处): 1500.8 / 36-0 属于固定 p0; 复用开发种子; 顺序敏感 Elo; 非确认性; 不可外推线上。该记录仅用于说明审计为何重开, 不参与本报告主结论。#source("m2_elo_ratings_full_pool")

战役 III 的任何策略或候选字节变化都构成新候选; 战役 II 的确认结果与 holdout 种子不得迁移或复用于新候选, 新候选必须建立新的冻结身份和新的独立确认种子。

== 禁止外推

本报告不把本地 holdout 等同于线上对手分布, 不对竞赛名次、奖项结果或线上能力作结论。LLM 真实 A/B 未发生, 对应值保持 #fmt(um("llm_ab_win_rate")); 预算闸真实触发值保持 #fmt(um("llm_ab_budget_gate_hits"))。#usource("llm_ab_win_rate") #usource("llm_ab_budget_gate_hits")

第一轮线上证据样本极小且对手分布未知, 只用于失败模式复盘与画像设计输入, 不外推为任何线上实力、名次或获奖结论。

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

= 战役 II 四阶段波次执行记录

== m2a: 评估器加固

完整软件测试通过 #fmt(m("m2a_tests_passed"))/#fmt(m("m2a_tests_total")); 生产 gate 契约与 export 安全检查分别为 #fmt(m("m2a_gate_contract_check_pass")) 和 #fmt(m("m2a_export_safety_check_pass"))。修复前的一次开发门已明确 invalidated=#fmt(m("m2a_complete_gate_invalidated")), 不再作为合入证据。#source("m2a_tests_passed") #source("m2a_tests_total") #source("m2a_gate_contract_check_pass") #source("m2a_export_safety_check_pass") #source("m2a_complete_gate_invalidated")

== m2b: 策略修复与冻结

定向策略/契约测试通过 #fmt(repair.at("passed"))/#fmt(repair.at("total")), failed=#fmt(repair.at("failed"))。检查项记录末日零资本支出=#fmt(repair_checks.at("terminal_day_no_capex"))、末日现收处置=#fmt(repair_checks.at("terminal_day_liquidation"))、购买观察确认=#fmt(repair_checks.at("purchase_confirmation"))、shed 库存预留=#fmt(repair_checks.at("shed_reservation"))、严格正数量=#fmt(repair_checks.at("positive_quantities"))。#source("strategy_repair_test_summary") #source("strategy_repair_checks")

完整开发门 expected/actual 为 #fmt(gate.at("expected_games"))/#fmt(gate.at("actual_games")), AB/BA 为 #fmt(gate.at("ab_games"))/#fmt(gate.at("ba_games")), 异常 #fmt(gate.at("abnormal_games")), 战绩 #record(gate.at("record")), formal_pass=#fmt(gate.at("formal_pass"))。通过后冻结候选 SHA-256 为 #raw(frozen.at("sha256"))。#source("development_gate_summary") #source("frozen_candidate_identity")

== m2c: 一次性独立 holdout

唯一记录的 attempt index 为 #fmt(run_status.at("index")), 状态 #fmt(run_status.at("status")), published=#fmt(run_status.at("published")), invalidated=#fmt(run_status.at("invalidated"))。正式全矩阵 expected/actual 为 #fmt(schedule.at("expected_games"))/#fmt(schedule.at("actual_games")), 完整性合取判定为 #fmt(m("holdout_integrity_pass"))。#source("holdout_run_status") #source("holdout_schedule") #source("holdout_integrity_pass")

本阶段只发布既有 attempt 的结果。验证动作可以重读并校验正式文件, 但不得重跑、重抽或替换该 holdout。

== m3: 文档重生成

战役 II 收尾版只消费合并后的 metrics, 将旧开发 Elo 降为历史披露, 将主结论改为逐对 W/L/T、座位拆分、Wilson 区间和顺序无关成对统计。线上与真实 LLM A/B 的未测键继续显示 null。

= 战役 II 实测结果（绑定前代冻结候选）

本章全部数字来自战役 II 正式 export, 绑定前代冻结候选 SHA-256 #raw(m("m2b_candidate_sha256"))。战役 III 新候选冻结身份「待 m3 实测」; 在新候选形成并完成新的独立确认之前, 本章战绩、区间与完整性判定不得外推、不得迁移到战役 III 新候选。#source("m2b_candidate_sha256")

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
  [线上对局], [#fmt(um("online_ladder_games"))], [依赖真实线上提交, 已按第一轮实测回填],
  [线上 skill rating], [#fmt(um("online_skill_rating"))], [依赖真实线上提交与平台计分],
  [线上反馈校准], [#fmt(um("online_feedback_calibration").at("round1_public_record"))], [第一轮失败模式台账见 exports/online/],
  [最终提交 commits], [#fmt(um("final_submission_commits"))], [人工终交锁定尚未回填],
)
#usource("online_ladder_games") #usource("online_skill_rating") #usource("online_feedback_calibration") #usource("final_submission_commits")

= 战役 III 线上反馈复盘（round-1）

本章数字均为线上实测回填（依赖真实线上提交与平台回放, 人工执行）; 样本极小, 全章不外推。

== 公共局战绩与平台评分

第一轮提交（依赖真实线上提交, 人工执行）在公共天梯完成 #fmt(um("online_ladder_games")) 局, 台账战绩 #fmt(um("online_feedback_calibration").at("round1_public_record")), 平台 skill rating 为 #fmt(um("online_skill_rating"))。逐局台账与分析文件路径由键内字段给出: #raw(um("online_feedback_calibration").at("ledger")) 与 #raw(um("online_feedback_calibration").at("analysis"))。#usource("online_ladder_games") #usource("online_skill_rating") #usource("online_feedback_calibration")

== 失败模式清单（FM-O1..O4）

对第一轮公共局失利的回放复盘产生失败模式清单: #fmt(um("online_feedback_calibration").at("loss_failure_modes").join("；"))。这些失败模式构成本轮画像驱动重构的直接输入: 失败模式先行, 再定义画像维度, 经跨局复核后参数化线上风格对手, 最终进入门禁与候选重构; 该链路详见第七章。#usource("online_feedback_calibration")

== 榜单与分布快照（占位）

全榜排名与队伍总数快照当前没有 metrics 键, 本版不写数: 占位「待 m1 实测」（建议键 `m1_round1_ladder_context`, 定义见 `metrics-keys-r3.md`）。该快照只用作画像分层抽样（top-20 / top-100 / 500-900 近段）的设计输入, 不外推名次或对手分布结论。

== 复盘进入战役 III 的链路

复盘结论按固定链路进入工程: 失败模式清单先行, 再定义画像维度（资金曲线、畜群轨迹、作物轮替、雇佣强度、外购饲料、卖出价格门控、终局行为）, 经跨局复核后参数化线上风格对手, 最终进入门禁与候选重构。同选手不少于 3 局一致才可作为对手参数依据; 单局结论一律标 exploratory。

= 战役 III 波次大纲（第 1 波占位版）

以下各节为大纲占位: 所有性能与统计数字须待对应里程碑实测并经 merge_metrics 合并后, 于 m5 成稿回填; 当前一律以中文占位符标注, 不新增 `m()`/`um()` 对尚不存在键的引用。各键定义见 `metrics-keys-r3.md`。

== m1: 回放语料与画像（待 m1 实测）

- 官方 episodes index 解析与按需下载: 原始回放仅落 gitignored 数据目录, 仅小体积画像档案入库。
- 语料完整性校验: 双方 DONE、720 步完整性与异常局剔除留痕; 入库局数与剔除局数「待 m1 实测」。
- 逐局结构化画像: 资金曲线、畜群轨迹、作物轮替、雇佣强度、外购饲料、卖出价格分布与终局抛售构成。
- 分层画像档案: top-20、top-100、500-900 近段三档; 每档案携带数据集 URL 与抓取日期; 档案数与覆盖局数「待 m1 实测」。
- 跨局复核: 同选手不少于 3 局一致才进入对手池参数; 复核统计「待 m1 实测」。

== m2: 线上风格对手池（待 m2 实测）

- 依据复核后的画像参数实现 2-4 个显式风格 bot（候选: 作物轮作 bot、重劳动麦作 bot、混合畜群 bot、终局囤倾 bot）; 对手清单与画像参数来源「待 m2 实测」。
- 经 `check_opponent_strength` 对冻结弱池认证, 强度不低于 50%（蓝图契约阈值）才入库; 认证局数与战绩「待 m2 实测」。
- 纳入 run_eval 对手池与完整门禁必测名单; 旧池成员全部保留, 防能力回退。

== m3: 市场自适应候选（待 m3 实测）

- 作物轮作主引擎: 按实时价格在麦、草莓、西瓜、胡萝卜间轮换地块。
- 小规模混合畜群（羊为主）与常态外购饲料（带价格护栏）。
- 劳动扩容至画像实证强度; 第三象限扩张; 终局囤积-倾销与末日停喂。
- 保留 m2b 全部修复（末日零 capex、末日现收处置、购买观察确认、shed 预留、正数量订单、跨座位跨局隔离）与既有测试; 新增策略回归测试。
- 在含线上风格对手的新完整开发门通过后冻结候选与 SHA-256; 冻结身份「待 m3 实测」。

== m4: 一次性 holdout v2（待 m4 实测）

- 系统随机全新种子, 与全部历史种子无交集: 战役 II 已登记历史开发/回归种子 #fmt(m("holdout_seed_domain_isolation").at("historical_count")) 个、已公布 holdout 种子 #fmt(protocol.at("seed_count")) 个, 线上实测 episode 对应 seed 一并排除; 交集计数必须为 0。#source("holdout_seed_domain_isolation") #source("holdout_protocol")
- 全池 AB/BA 双座位、运行前候选哈希锁定、异常 fail-closed、语义校验通过后原子发布; 结果无论好坏如实入 metrics。
- 逐对 W/L/T、座位分层、Wilson 区间与顺序无关统计「待 m4 实测」。

== m5: 文档与 SOP v4 重生成

- 基于新 metrics 重生成本报告成稿与 SOP v4; 战役 II holdout 结论保留前代候选标注并紧邻限制说明; 不把本地 holdout 外推为线上实力。

= 提交 SOP v4 要点（大纲引用）

本节只收录操作约束要点; 完整手册大纲见 `sop-v4-outline.md`, 成稿随 m5 发布。以下均为流程约束, 不是已执行声明。

== 天梯采样-回拉-复盘循环

- 每日提交至多 5 次; 每候选至多 2 次/日; 提交前核对当日额度与「最近 2 次提交」跟踪。
- Validation Episode 返回 Error 即停当日提交并上报; 不得用连续重试掩盖错误。
- 每次提交后回拉不少于 3 局公共天梯回放完成复盘, 更新失败模式台账并滚动更新画像档案; 复盘产出按第 6 章链路进入对手池参数与新候选规则。

== 止损线与转备选

- 新候选线上公共局累计不少于 6 局且胜率低于 50% 时, 禁止继续本方向调参, 转备选方向接力; 触发条件与触发动作记录入台账（建议键位见 `metrics-keys-r3.md`）。
- 止损是资源分配决策, 不外推为任何线上实力、名次或获奖结论。

= 合规与人机分工

== 合规边界

提交 bot 保持离线、自包含和 stdlib-only; 外部 LLM 不是线上运行依赖。回放画像与线上复盘只用于离线设计, 提交 bot 不依赖外部数据集、LLM 或网络 API。正式结论只消费身份匹配、完整矩阵、零异常且已发布的 export。账号报名、提交、Validation Episode 检查、提交额度管理和最终锁定均由队伍人工执行, 本报告不把流程约束写成已完成事实。

== 人机分工概要

AI 辅助完成评估器加固、策略修复、测试与本地证据生成, 并依据 metrics 重写文档; 战役 III 中另承担语料画像、线上风格对手实现、候选重构与大纲文档。人工负责规则复核、候选裁决、Kaggle 账号操作、线上反馈解释、是否形成新候选以及最终签字。详细留痕见附录 A。

= 遗留与可复用资产

// CHECK:LIMITATIONS
== 局限

- 当前确认集对手来自既定本地池, 不能覆盖未知线上策略分布。
- holdout 种子已公开, 只能复核既有证据, 不得再作为新独立确认集。#source("holdout_seed_manifest")
- 任何策略变化都会使旧候选身份与确认结果不再适用于新候选。#source("holdout_protocol")
- 线上指标按第一轮真实提交证据回填, 但样本极小且对手分布未知; 真实 LLM A/B 仍为 null, 不以本地管道自检或 holdout 代替。#usource("online_ladder_games") #usource("online_skill_rating") #usource("llm_ab_win_rate")
- 本版为大纲版: 战役 III 各波次数尚未实测, 相关数字以中文占位符标注（见第 7 章）, 不以任何估计值顶替。

== 可复用资产

可复用资产包括: 候选 SHA 与冻结清单、AB/BA 调度、种子域隔离、异常 fail-closed、正式 export 事务发布、确认统计到 JSON Pointer 的追溯映射, 以及“新候选必须配新独立确认种子”的治理规则。战役 III 在其上追加: 带来源标注的回放画像档案、线上风格对手池、round-2 天梯采样-回拉-复盘循环与止损线。

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
  [回放语料与画像], [解析 index、下载、画像提取与完整性校验（待 m1 实测）], [抽查档案来源标注并裁决画像可用性],
  [线上风格对手池], [实现风格 bot 并执行认证（待 m2 实测）], [审阅画像参数并裁决对手入库],
  [候选重构], [实现轮作、畜群、饲料、劳动、象限与终局能力及回归测试（待 m3 实测）], [审阅行为变化并批准新候选冻结],
  [线上反馈复盘], [整理台账与失败模式清单, 维护采样额度台账], [提交、回拉回放、复盘解释与止损裁决],
  [文档], [仅从 metrics 生成报告与 SOP v3 及本版大纲], [事实核对、审读与签字],
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

正式证据的唯一数据入口是 `workspace/metrics.json`; 其映射同时给出 export SHA、schema 和各确认性对象的 JSON Pointer, 从而避免从日志或旧报告手工抄值。战役 III 新增键位的需求清单见 `metrics-keys-r3.md`; 在对应键进入 metrics 之前, 本报告只用占位符标注, 不预填任何数值。
