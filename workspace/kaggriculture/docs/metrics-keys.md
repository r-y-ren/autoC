# 战役 II 审计修订版 metrics 键清单（m2a/m2b/m2c/m3）

> 用途：这是 document 第一波大纲包中的 software -> document 接口提案。software 须在对应里程碑实测并写入 `workspace/software/metrics.json`，document 在 m3 只消费 `workspace/metrics.json` 合并后的稳定值。
> 对齐依据：`workspace/blueprint.md` 的 m2a/m2b/m2c/m3 与自动验收项、`workspace/strategy.md` 的证据边界，以及当前 `workspace/software/exports/schema.json` v1.1。
> 当前接口状态：schema v1.1 尚未定义本清单中的身份、种子域、AB/BA、异常局、一次性 holdout、语义校验与原子发布字段。以下键须由 software 扩展 export schema、生产器和 merge 投影后才能成为可引用事实；document 不单方面造值。

## 1. 总体数据纪律

1. 对外性能数字只可引用 `workspace/metrics.json` 中已经合并的实测键，格式为 `metrics.software.<key>` 或 `metrics.document.<key>`；表格或紧邻正文必须标出来源键名。
2. 每个分片键沿用 `{ "value": ..., "unit": ..., "method": ... }` 包装。未运行、运行失败、身份不匹配、语义校验失败或正式发布失败时，`value` 必须为 `null`，不得用 `0`、空数组、空对象或推算值冒充实测。
3. quick、dev、exploratory、失败运行只能形成隔离产物，不得覆盖正式 export，也不得进入确认性指标。自定义子集只能标为 exploratory，不能产生 PASS。
4. m2a 与 m2b 不得出现任何 holdout 种子清单、局数、战绩、区间、评级或运行结果。第 5 节列出的 16 个确认性键在 m2c 正式发布前一律为 `null`。
5. m2c 结果只对运行前冻结的候选 SHA-256 有效。候选文件变化后，旧 holdout 结果必须标记失效，不得继续调参后复用同一 holdout。
6. 旧 `m2_elo_ratings_full_pool` / `m2_matchup_win_rates` 只能作为固定 p0、开发种子复用、顺序敏感 Elo 的历史开发基线；不得与新 holdout 并列成确认性结论，更不得外推天梯、名次或获奖概率。
7. Elo 是顺序敏感指标，m2c 仅可放在附录。主结论必须使用逐对 W/L/T、AB/BA 座位分层、Wilson 区间和顺序无关统计。

## 2. 通用对象约定

下列对象字段是键值内部的最小语义要求，不是额外的顶层 metrics 键。

| 对象 | 最小字段 |
|---|---|
| 候选身份 | `candidate_path`, `sha256`, `git_ref`, `git_dirty`, `captured_at` |
| 输入身份 | `engine_hash`, `config_hash`, `opponent_pool_hash`, `required_opponents_hash`, `schema_hash` |
| 种子域 | `development`, `regression`, `holdout`；各域含 `manifest_hash`, `count`, `classification`，并给出两两 `overlap_count` |
| 赛程 | `expected_games`, `actual_games`, `expected_pairs`, `actual_pairs`, `complete` |
| 座位拆分 | `ab_expected`, `ab_actual`, `ba_expected`, `ba_actual`, `missing_mirrors`, `symmetric` |
| 异常摘要 | `total`, `non_done`, `invalid`, `timeout`, `contract_failure`, `other` |
| W/L/T | `W`, `L`, `T`, `games`，并满足 `W + L + T == games` |
| Wilson 区间 | `confidence`, `tie_policy`, `estimate`, `lower`, `upper`, `games` |
| 发布记录 | `publish_attempted`, `published`, `atomic_replace`, `official_path`, `official_sha256`, `prior_official_preserved_on_failure` |

## 3. m2a 评估加固键（16 个）

| 唯一键 | 类型 / 未测规则 | 用途与最小内容 | 验收对齐 |
|---|---|---|---|
| `metrics.software.m2a_test_summary` | object；未跑 `null` | 全软件测试的总数、通过、失败和命令；method 明列双座位、隔离、fail-closed、门禁、原子发布、统计边界与验收夹具覆盖 | m2a-test |
| `metrics.software.m2a_smoke_summary` | object；未跑 `null` | 短局与完整局自博弈、contract verdict、异常数；只有全部完成才可 PASS | m2a-smoke |
| `metrics.software.evaluation_candidate_identity` | object；未捕获 `null` | 本次评估候选身份；正式 gate 和 export 必须使用同一 SHA-256 | m2a-gate-contract / m2c-identity |
| `metrics.software.evaluation_input_hashes` | object；未捕获 `null` | 引擎、配置、对手池、必测对手清单与 schema 输入哈希 | m2a-gate-contract / m2c-identity |
| `metrics.software.evaluation_seed_domains` | object；未定义 `null` | 开发、回归、holdout 域的分类、manifest hash 与数量；m2a/m2b 的 holdout 子对象必须 `null` | m2a-test / m2c-identity |
| `metrics.software.evaluation_seed_domain_isolation` | object；未验 `null` | 域间交集计数、禁用种子检查及 verdict；开发/回归与 holdout 交集必须为零 | m2a-test / m2c-identity |
| `metrics.software.evaluation_schedule` | object；未跑 `null` | 正式 gate 的 expected/actual games、pairs、必测对手和完整性 | m2a-gate-contract |
| `metrics.software.evaluation_seat_split` | object；未跑 `null` | 正式 gate 的 AB/BA expected/actual、缺失镜像与对称 verdict | m2a-test / m2a-gate-contract |
| `metrics.software.evaluation_abnormal_summary` | object；未跑 `null` | 非 DONE、INVALID、超时、contract 失败等分项计数；成功正式批次要求 total 为零 | m2a-test / m2a-gate-contract |
| `metrics.software.evaluation_fail_closed` | object；未验 `null` | 注入异常时整批失败、禁止统计和禁止发布的断言结果 | m2a-test / m2a-gate-contract |
| `metrics.software.evaluation_gate_completeness` | object；未验 `null` | gate/guard 必测对手、种子、双座位和局数完整；缺一项均不可 PASS | m2a-gate-contract |
| `metrics.software.evaluation_run_class` | enum；未分类 `null` | 仅允许 `quick`, `development`, `exploratory`, `gate`, `official_holdout`；只有完整 gate/official 可产生正式 verdict | m2a-gate-contract / m2a-export-safety |
| `metrics.software.official_export_validation` | object；未验 `null` | `schema_pass`, `semantic_pass`, `cross_field_pass`, errors 与 validator identity | m2a-export-safety / m2c-identity |
| `metrics.software.official_export_publish` | object；未发布 `null` | 临时文件到正式 export 的原子替换证据；失败时旧正式文件保持不变 | m2a-export-safety |
| `metrics.software.statistical_boundary_test_summary` | object；未跑 `null` | t 区间/Wilson 的小样本、零方差、空样本和边界夹具结果 | m2a-test |
| `metrics.software.acceptance_fixture_test_summary` | object；未跑 `null` | `run-N` 解析夹具的 case 数、通过数和失败数，防止把运行编号误作断言结果 | m2a-test |

## 4. m2b 策略修复与冻结键（4 个）

| 唯一键 | 类型 / 未测规则 | 用途与最小内容 | 验收对齐 |
|---|---|---|---|
| `metrics.software.strategy_repair_test_summary` | object；未跑 `null` | 指定策略回归测试的总数、通过、失败、命令与测试文件哈希 | m2b-strategy |
| `metrics.software.strategy_repair_checks` | object；未跑 `null` | 分项 verdict：末日零资本支出、末日现收可变现或跳过、购买按观察确认、shed 库存预留、订单数量严格正数 | m2b-strategy |
| `metrics.software.development_gate_summary` | object；未跑 `null` | 完整开发门的候选 SHA-256、gate/guard 清单、expected/actual games、AB/BA split、异常计数与 verdict | m2b-dev-gate |
| `metrics.software.frozen_candidate_identity` | object；未冻结 `null` | 开发门通过后冻结的候选身份；其 SHA-256 是 m2c 唯一允许的运行前身份 | m2b-dev-gate / m2c-holdout |

## 5. m2c 一次性 holdout 与确认性键（17 个）

以下键中，前 16 个在 m2a/m2b 以及 m2c 正式发布前必须为 `null`。不得提前生成种子、填入预期战绩或以开发结果占位。最后一个历史基线状态键不是 holdout 数值，可在 m2a 起写入，但其来源必须指向既有实测键。

| 唯一键 | 类型 / 未测规则 | 用途与最小内容 | 验收对齐 |
|---|---|---|---|
| `metrics.software.holdout_protocol` | object；发布前 `null` | 系统随机源说明、生成时点、运行前冻结规则、揭晓规则、一次性规则和 invalidation policy | m2c-holdout |
| `metrics.software.holdout_seed_manifest` | object；发布前 `null` | 运行后公开的种子清单、数量、manifest SHA-256 与生成记录；不得包含 101-104、201-208 | m2c-holdout / m2c-identity |
| `metrics.software.holdout_candidate_hash_match` | object；发布前 `null` | 运行前 hash、冻结 hash、运行后 hash 及三者一致 verdict | m2c-holdout / m2c-identity |
| `metrics.software.holdout_seed_domain_isolation` | object；发布前 `null` | holdout 与开发/回归/历史已用种子的交集计数及 verdict | m2c-holdout / m2c-identity |
| `metrics.software.holdout_run_status` | object；发布前 `null` | `attempt_index`, `started_at`, `completed_at`, `published`, `invalidated`, `invalidation_reason`；有效结果只允许一次 published attempt | m2c-holdout |
| `metrics.software.holdout_schedule` | object；发布前 `null` | 全池确认矩阵的 expected/actual games 与 pairs、完整性；不得从自定义子集推导 | m2c-holdout / m2c-identity |
| `metrics.software.holdout_seat_split` | object；发布前 `null` | AB/BA expected/actual、缺失镜像、逐 `(pair, seed)` 对称性 | m2c-holdout / m2c-identity |
| `metrics.software.holdout_abnormal_summary` | object；发布前 `null` | 确认批次异常分项计数；任何非零使整批无效且确认性统计保持 `null` | m2c-holdout / m2c-identity |
| `metrics.software.holdout_integrity_pass` | boolean；发布前 `null` | 身份、种子隔离、完整赛程、双座位、零异常和一次性约束的合取 verdict | m2c-holdout / m2c-identity |
| `metrics.software.confirmatory_overall_record` | W/L/T object；发布前 `null` | 冻结候选在完整 holdout 全池上的合并 W/L/T，不以单一胜率替代原始计数 | m2c-holdout / m2c-metrics |
| `metrics.software.confirmatory_pair_records` | array；发布前 `null` | 每个对手逐对 W/L/T、games、seed count；pair 集必须等于赛程契约 | m2c-holdout / m2c-metrics |
| `metrics.software.confirmatory_seat_records` | object；发布前 `null` | AB 与 BA 分层 W/L/T，以及按对手的座位拆分；两层之和等于 overall | m2c-holdout / m2c-metrics |
| `metrics.software.confirmatory_wilson_intervals` | object/array；发布前 `null` | overall 与逐对 Wilson 区间；明确置信水平和 tie policy，并能回算到 W/L/T | m2c-holdout / m2c-metrics |
| `metrics.software.confirmatory_order_independent_statistics` | object；发布前 `null` | 顺序无关 Bradley-Terry 或预注册配对统计的 method、输入 hash、estimate、interval、fit status；不得混入顺序敏感 Elo | m2c-holdout / m2c-metrics |
| `metrics.software.confirmatory_elo_appendix` | object；发布前 `null` | 如保留 Elo，只记录 order、k、start、table 和 `descriptive_only: true`，仅供附录 | m2c-metrics / m3-redocument |
| `metrics.software.confirmatory_export_traceability` | object；发布前 `null` | metrics 各确认性键到正式 export JSON Pointer、export SHA-256 与 merge source 的映射 | m2c-metrics |
| `metrics.software.historical_m2_baseline_status` | object；未登记 `null` | 指向既有 `m2_elo_ratings_full_pool` / `m2_matchup_win_rates`，标记 `classification: historical_development_baseline`, `confirmatory_eligible: false`, `fixed_p0: true`, `seed_reuse: true`, `elo_order_sensitive: true` | m3-redocument / doc-consistency |

## 6. m3 document 验收键（13 个）

这些键由 document 写入 `workspace/document/metrics.json`；报告中的软件性能结论仍只来自 `metrics.software.*`。当前已有的编译/页数键可沿用，但 m3 必须在重写后重新实测，不能复用旧 PDF 的结果。

| 唯一键 | 未测规则 | 用途 | 验收对齐 |
|---|---|---|---|
| `metrics.document.report_compile_exit_code` | 未编译 `null` | m3 新报告编译退出码 | doc-compile |
| `metrics.document.report_compile_seconds` | 未编译 `null` | m3 成功编译墙钟耗时 | doc-compile |
| `metrics.document.report_pages` | 未生成 `null` | m3 PDF 实际页数 | doc-compile / doc-visual |
| `metrics.document.report_consistency_check_exit_code` | 未检查 `null` | `check_report_metrics.py` 退出码 | doc-consistency |
| `metrics.document.report_metric_key_references` | 未检查 `null` | 报告中唯一 metrics 键引用数 | doc-consistency |
| `metrics.document.report_dangling_metric_keys` | 未检查 `null` | 引用但未在合并 metrics 中解析的键数，验收要求为零 | doc-consistency |
| `metrics.document.report_unkeyed_performance_numbers` | 未检查 `null` | 无紧邻 metrics 键来源的性能数字命中数，验收要求为零 | doc-consistency |
| `metrics.document.report_historical_baseline_disclosures` | 未检查 `null` | 旧开发基线每次出现时紧邻限制说明的检查记录 | doc-consistency |
| `metrics.document.report_prohibited_extrapolation_hits` | 未检查 `null` | 天梯实力、名次或获奖外推命中数，验收要求为零 | doc-consistency |
| `metrics.document.report_visual_pages_checked` | 未视觉验收 `null` | 实际逐页检查页数，须等于 PDF 页数 | doc-visual |
| `metrics.document.report_visual_defects` | 未视觉验收 `null` | 溢出、重叠、断页、不可读图表的缺陷计数与页码 | doc-visual |
| `metrics.document.report_human_ai_appendix_present` | 未检查 `null` | 人机分工附录存在且非空的布尔检查 | m3-redocument / 合规留痕 |
| `metrics.document.report_rewrite_mapping_coverage` | 未检查 `null` | 第 8 节各重写目标均已落到报告的覆盖记录 | m3-redocument |

## 7. 既有键的保留与降格

| 既有键 | m3 处理 |
|---|---|
| `metrics.software.m2_elo_ratings_full_pool` | 仅作为历史开发基线数值来源；每次出现必须同时引用 `historical_m2_baseline_status` 并紧邻披露固定 p0、开发种子复用和顺序敏感限制 |
| `metrics.software.m2_matchup_win_rates` | 仅作为历史开发基线 matchup 来源，不得称为 holdout 或确认性结果 |
| `metrics.software.llm_ab_win_rate` / `llm_ab_budget_gate_hits` | 未配置 `KG_LLM_*` 或未执行真实 A/B 时继续为 `null`；NullProvider 通路测试不能替代真实 A/B |
| `metrics.software.online_ladder_games` / `online_skill_rating` / `online_feedback_calibration` | 人工线上步骤未发生时继续为 `null`；本地 holdout 不得回填这些键 |
| `metrics.software.final_submission_commits` | man-final 未执行时继续为 `null` |

## 8. report.typ 章节重写映射（m3 执行）

本波只定义映射，不改 `report.typ`。m3 保留现有主结构和附录框架，在原章节内重写，不凭空新增性能结论。

| 当前章节 | m3 重写目标 | 主要键来源 |
|---|---|---|
| 摘要 | 从“旧 m2 已收口”改为“评估可信度重建 -> 策略修复 -> 冻结候选一次性确认”；主结论只取确认性统计 | `confirmatory_overall_record`, `confirmatory_wilson_intervals`, `confirmatory_order_independent_statistics` |
| 战役定位与范围 | 明确本地 holdout 不是天梯，线上/获奖不外推；旧结果降格 | `historical_m2_baseline_status`, online nullable keys |
| 方法与选型 / 软件-文档契约 | 改写为候选身份、种子域、AB/BA、异常 fail-closed、完整门与原子发布证据链 | m2a identity/schedule/validation/publish 键 |
| 四阶段执行记录 - m2a | 记录评估器加固、统计边界与验收夹具修复，不引用 holdout 数值 | 第 3 节 m2a 键 |
| 四阶段执行记录 - m2b | 记录五项策略修复、完整开发门和候选冻结，不引用 holdout 数值 | 第 4 节 m2b 键 |
| 四阶段执行记录 - m2c | 记录一次性协议、运行前后 hash、公开种子、完整性与发布状态 | `holdout_protocol` 至 `holdout_integrity_pass` |
| 实测结果 | 先列身份/完整性，再列逐对与座位 W/L/T、Wilson 和顺序无关统计；Elo 移至描述性附录 | 第 5 节确认性键 |
| 旧 m2 结果段 | 不删除历史记录，但重写为固定 p0 开发基线，限制说明与数值紧邻 | 既有 m2 键 + `historical_m2_baseline_status` |
| A/B 与线上段 | 未发生继续显示 `null`，不得把通路自检或本地 holdout 写成真实 A/B/天梯结果 | 第 7 节 nullable 键 |
| 合规与人机分工 / 附录 A | 保留 AI 辅助原创与人工报名、提交、终交裁量；补本轮评估治理和文档重写留痕 | `report_human_ai_appendix_present` |
| 遗留与可复用资产 | 写明同族对手分布偏差、一次性 holdout 不可复用、线上仍待人工校准 | holdout integrity 与 online nullable 键 |
| 附录 B / 证据索引 | 增加正式 export hash、schema/语义校验、merge traceability；Elo 若出现只在此标 descriptive | `official_export_validation`, `official_export_publish`, `confirmatory_export_traceability`, `confirmatory_elo_appendix` |

## 9. 验收覆盖矩阵

| 蓝图自动验收 | 键证据组 | 大纲状态 |
|---|---|---|
| m2a-test | m2a 测试、座位、隔离、异常、统计边界、夹具 | 已定义 |
| m2a-smoke | m2a smoke 与异常摘要 | 已定义 |
| m2a-gate-contract | run class、赛程、座位、完整门、fail-closed | 已定义 |
| m2a-export-safety | schema/语义校验与原子发布 | 已定义 |
| m2b-strategy | 策略测试与五项分解检查 | 已定义 |
| m2b-dev-gate | 完整开发门与冻结候选身份 | 已定义 |
| m2c-holdout | 一次性协议、种子清单、身份匹配、完整性 | 已定义 |
| m2c-identity | 候选/输入身份、种子域、expected/actual、AB/BA、零异常、跨字段语义 | 已定义 |
| m2c-metrics | 确认性统计到正式 export 的逐键追溯 | 已定义 |
| m2-ab | 沿用既有 nullable 键；未配置时保持 `null` | 已定义边界 |
| doc-compile | 编译、耗时、页数 | 已定义 |
| doc-consistency | 键解析、无来源数字、基线披露、禁止外推 | 已定义 |
| doc-visual | 逐页检查与缺陷记录 | 已定义 |

人工验收 `man-reg`、`man-submit`、`man-final` 不由本大纲制造完成值；只沿用对应 nullable 键并在人工动作发生后回填。

## 10. software 接口待落地点

1. 将当前 `workspace/software/exports/schema.json` 从 v1.1 扩展到覆盖第 2-5 节对象，并对 expected/actual、W/L/T 总和、AB/BA 镜像、异常为零、hash 一致性做跨字段语义校验。
2. 明确 software export 字段到 `workspace/software/metrics.json` 顶层键的确定性投影；确认性键必须携带 JSON Pointer 与 export SHA-256。
3. 明确一次性 holdout 状态文件/发布记录的权威接口。document 需要 `attempt_index`、冻结 hash、公开 seed manifest hash 和 invalidation 状态，但不指定 software 的内部文件布局。
4. `check_report_metrics.py` 尚需在 m3 前确认能识别对象型来源、nullable 值、历史基线紧邻披露和禁止外推规则；本角色此波不修改该脚本。

## 11. 本大纲自检口径

- software 唯一键定义：37 个（m2a 16 + m2b 4 + m2c 17）。
- m2a/m2b 阶段必须为 `null` 的确认性 holdout 键：16 个。
- document m3 验收键定义：13 个。
- 报告重写映射：12 项。
- 蓝图自动验收覆盖：13 项；人工验收 3 项仅保留接口，不伪造完成状态。
- 同一注册表内无重复全限定键名；Markdown 标题层级、表头和代码标记由本波自检。
