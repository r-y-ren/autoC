# 战役 III（线上反馈重构版）metrics 键需求清单（m1-m5 与 online_*）

> 用途：这是 document 第 1 波大纲包中的 software -> document 接口提案。software 须在对应里程碑实测并写入分片 metrics，document 在 m5 成稿时只消费 `workspace/metrics.json` 合并后的稳定值。
> 对齐依据：`workspace/blueprint.md` 战役 III 的 m1-m5 里程碑与自动/人工验收项（m1-tests/m1-corpus/m1-smoke/m2-pool/m2-gate/m2-ab/m3-strategy/m3-dev-gate/m4-holdout/m4-identity/m4-metrics/doc-*/man-submit-r2/man-final）。
> 当前接口状态：本清单所有 m1_*/m2_*/m3_*/m4_* 键均不存在于当前 `workspace/metrics.json`；报告大纲版因此只用中文占位符，不引用任何未落地键。键落地（schema 扩展、生产器、merge 投影）由 software 负责；document 不单方面造值。

## 1. 总体数据纪律（引用纪律）

1. 对外性能数字只可引用 `workspace/metrics.json` 已合并的实测键，格式 `metrics.software.<key>`；表格或紧邻正文标出来源键名。
2. 分片键沿用 `{ "value": ..., "unit": ..., "method": ... }` 包装；未运行、运行失败、身份不匹配或正式发布失败时 `value` 必须为 `null`，不得以 0、空集或推算值冒充实测。
3. 画像与语料类键的每个数字必须能追溯到正式产物：官方数据集 URL + 抓取日期 + 档案哈希（蓝图 m1 契约）；无法追溯的统计不得入键。
4. 单局结论一律标 exploratory；只有同选手不少于 3 局一致的跨局复核结论才可进入对手池参数键。
5. quick/dev/exploratory/失败运行只形成隔离产物，不得覆盖正式 export，也不得进入 m4_* 确认性键。
6. m4_* 确认性键在正式发布前一律 `null`；结果无论好坏如实写入，禁止重抽、择优或替换。
7. unmeasured.online_* 只由真实线上证据回填（round-2 沿用 round-1 的回填通道与台账纪律）；本地 holdout、画像统计或 SOP 通路自检不得代填。

## 2. 命名占用与去重

- 战役 II 已占用前缀：`m1_tests_total`、`m1_tests_passed`、`m1_elo_ratings_full_pool`、`m1_eval_*`、`m1_matchup_*`、`m1_submission_margin_vs_pool`（战役 II m1）；`m2_submission_engine`、`m2_iteration_gate_log`、`m2_elo_ratings_full_pool`、`m2_matchup_win_rates`、`m2_probe_record`、`m2_tests_*` 等（战役 II m2）；`m2a_*`、`m2b_*`。
- 无占用：`m3_*`、`m4_*` 顶层前缀当前空闲。
- 建议：战役 III m1/m2 新键一律使用本清单新名，不复用战役 II 同名键位；若 m1-tests 验收需要记录测试计数，建议新增 `m1_tests_r3_total` / `m1_tests_r3_passed`，或由 software 裁决“最近一次覆盖”语义并在 JOURNAL 留痕。document 侧只要求零悬空键，不强制其一。

## 3. m1_*：回放语料与画像统计键（8 个）

| 唯一键 | 类型 / 未测规则 | 定义与数据来源约束 | 验收对齐 |
|---|---|---|---|
| `metrics.software.m1_replay_corpus_summary` | object；未跑 `null` | 官方 episodes index 快照与按需下载统计：index 来源 URL 与抓取日期、下载分片数、入库局数、异常局剔除数及逐条剔除原因留痕；数字只能来自正式语料产物 | m1-corpus |
| `metrics.software.m1_corpus_integrity_pass` | boolean；未跑 `null` | `corpus_integrity.py --mode official` 通过判定：档案含数据集 URL 与抓取日期、分层齐备、剔除留痕、跨局复核标注 | m1-corpus |
| `metrics.software.m1_profile_archive_inventory` | array；未产出 `null` | 分层画像档案清单（top-20 / top-100 / 500-900 近段）：每档案 ID、层、覆盖局数、同选手数、档案哈希、来源 URL、抓取日期、exploratory 标注 | m1-corpus |
| `metrics.software.m1_cross_review_summary` | object；未复核 `null` | 同选手不少于 3 局一致性复核统计：复核选手数、通过数、否决数；未通过者不得进入 `m2_online_style_opponents` 参数来源 | m1-corpus / m2-pool |
| `metrics.software.m1_profile_dimension_coverage` | object；未产出 `null` | 各画像维度（资金曲线、畜群轨迹、作物轮替、雇佣强度、外购饲料、卖出价格门控、终局行为）的逐局提取覆盖计数 | m1-tests |
| `metrics.software.m1_round1_ladder_context` | object；无快照 `null` | round-1 榜单上下文快照：全榜队伍数、我方名次、抓取时间、证据路径（页面/CLI 快照）；只作分层抽样设计输入，不作名次结论，不外推 | 报告第 6 章占位回填 |
| `metrics.software.m1_tests_r3_total` | integer；未跑 `null` | 战役 III 语料/画像/校验软件测试总数（命名避开战役 II `m1_tests_total`，见第 2 节） | m1-tests |
| `metrics.software.m1_tests_r3_passed` | integer；未跑 `null` | 战役 III 软件测试通过数 | m1-tests |

另：m1-smoke 验收（提交 bot 自博弈 contract 全绿）可沿用既有 `smoke_boot_pass` / `smoke_boot_runtime_seconds` 键位由本轮实测覆盖，或按第 2 节裁决；document 不强制新键。

## 4. m2_*：线上风格对手池认证键（5 个）

| 唯一键 | 类型 / 未测规则 | 定义与数据来源约束 | 验收对齐 |
|---|---|---|---|
| `metrics.software.m2_online_style_opponents` | array；未实现 `null` | 每个线上风格对手：名称、风格类型（作物轮作/重劳动麦作/混合畜群/终局囤倾等）、画像参数来源档案 ID（须为跨局复核通过档案）、实现文件 SHA-256 | m2-pool |
| `metrics.software.m2_opponent_pool_certification` | object；未认证 `null` | `check_opponent_strength` 认证结果：每对手对冻结弱池的认证局数、W/L/T 与是否达到蓝图契约阈值（不低于 50%）；未达标不入池 | m2-pool |
| `metrics.software.m2_gate_required_opponents` | object；未更新 `null` | 更新后完整门禁必测名单与哈希：旧池成员全保留 + 新对手全纳入；拒绝缺失必测对手的赛程 | m2-gate |
| `metrics.software.m2_gate_contract_check_pass` | boolean；未跑 `null` | `check_eval_contract.py --mode gate` 通过判定（完整门禁含全部新对手、双座位、拒绝异常赛程） | m2-gate |
| `metrics.software.m2_opponent_unit_tests_summary` | object；未跑 `null` | 对手单测总数/通过/失败与测试文件哈希 | m2-pool |

另：m2-ab 验收沿用既有 `llm_ab_harness_ready` / `llm_ab_win_rate` / `llm_ab_budget_gate_hits` nullable 键；未配置 `KG_LLM_*` 时保持 `null`，不新增键。

## 5. m3_*：开发门与候选冻结键（4 个）

| 唯一键 | 类型 / 未测规则 | 定义与数据来源约束 | 验收对齐 |
|---|---|---|---|
| `metrics.software.m3_strategy_capability_checks` | object；未跑 `null` | 分项能力 verdict：轮作触发、外购饲料护栏上下界、劳动扩容强度、第三象限扩张、终局囤积-倾销、末日停喂；并记录 m2b 修复项不回退判定 | m3-strategy |
| `metrics.software.m3_strategy_regression_summary` | object；未跑 `null` | 新增策略回归测试总数/通过/失败与测试文件哈希（与 m2b 既有测试不回退一并记录） | m3-strategy |
| `metrics.software.m3_development_gate_summary` | object；未跑 `null` | 含线上风格对手的完整开发门：候选 SHA-256、gate/guard 必测对手清单、expected/actual games、AB/BA split、异常计数、formal_pass | m3-dev-gate |
| `metrics.software.m3_frozen_candidate_identity` | object；未冻结 `null` | 战役 III 冻结候选身份（path、sha256、git_ref、manifest）；是 m4 holdout v2 唯一允许的运行前身份 | m3-dev-gate / m4-holdout |

## 6. m4_*：一次性 holdout v2 确认性统计键（16 个）

语义对齐战役 II 的 holdout/confirmatory 键族，但全部使用 `m4_` 前缀独立建档；正式发布前一律 `null`。种子域约束：与全部历史种子（战役 II 登记的开发/回归历史种子、已公布 holdout 种子、线上实测 episode 对应 seed）交集必须为 0。

| 唯一键 | 类型 / 未测规则 | 定义与数据来源约束 | 验收对齐 |
|---|---|---|---|
| `metrics.software.m4_holdout_protocol` | object；发布前 `null` | 系统随机源说明、生成时点、运行前冻结规则、一次性规则、invalidation policy、排除清单 | m4-holdout |
| `metrics.software.m4_holdout_seed_manifest` | object；发布前 `null` | 运行后公开的种子清单、数量、manifest SHA-256；禁止包含任何历史种子 | m4-holdout / m4-identity |
| `metrics.software.m4_holdout_seed_domain_isolation` | object；发布前 `null` | 与全部历史种子的交集计数（必须为 0）与 verdict | m4-identity |
| `metrics.software.m4_holdout_candidate_hash_match` | object；发布前 `null` | 运行前 hash、冻结 hash、运行后 hash 及一致 verdict | m4-identity |
| `metrics.software.m4_holdout_run_status` | object；发布前 `null` | attempt index、started/completed、published、invalidated；有效结果只允许一次 published attempt | m4-holdout |
| `metrics.software.m4_holdout_schedule` | object；发布前 `null` | 全池（含线上风格对手）确认矩阵 expected/actual games 与 pairs、完整性 | m4-identity |
| `metrics.software.m4_holdout_seat_split` | object；发布前 `null` | AB/BA expected/actual、缺失镜像、逐 (pair, seed) 对称性 | m4-identity |
| `metrics.software.m4_holdout_abnormal_summary` | object；发布前 `null` | 异常分项计数；任何非零使整批无效且确认性统计保持 `null` | m4-identity |
| `metrics.software.m4_holdout_integrity_pass` | boolean；发布前 `null` | 身份、种子隔离、完整赛程、双座位、零异常、一次性约束的合取 verdict | m4-holdout |
| `metrics.software.m4_confirmatory_overall_record` | W/L/T object；发布前 `null` | 冻结候选在 holdout v2 全池的合并 W/L/T 与 score | m4-holdout / m4-metrics |
| `metrics.software.m4_confirmatory_pair_records` | array；发布前 `null` | 逐对 W/L/T、games、seed count；pair 集必须等于赛程契约（含新线上风格对手） | m4-metrics |
| `metrics.software.m4_confirmatory_seat_records` | object；发布前 `null` | AB/BA 分层 W/L/T；两层之和等于 overall | m4-metrics |
| `metrics.software.m4_confirmatory_wilson_intervals` | object/array；发布前 `null` | overall 与逐对 Wilson 区间；明确置信水平与 tie policy，可回算到 W/L/T | m4-metrics |
| `metrics.software.m4_confirmatory_order_independent_statistics` | object；发布前 `null` | 顺序无关成对统计的 method、输入 hash、estimate、interval、fit status | m4-metrics |
| `metrics.software.m4_confirmatory_elo_appendix` | object；发布前 `null` | 如保留 Elo：order/k/start/table 与 `descriptive_only: true`，仅附录 | m4-metrics |
| `metrics.software.m4_confirmatory_export_traceability` | object；发布前 `null` | 各 m4 确认性键到正式 export JSON Pointer、export SHA-256 与 merge source 的映射 | m4-metrics / m4-identity |

## 7. unmeasured.online_*：round-2 键位沿用（不新增顶层键）

| 沿用键 | round-2 回填约束 | 对接验收 |
|---|---|---|
| `metrics.software.unmeasured.online_ladder_games` | round-2 公共天梯累计局数；episode 级台账（提交 ID、episode ID、EPISODE_TYPE），排除 VALIDATION 自博弈；只在真实线上证据存在后更新 | man-submit-r2 |
| `metrics.software.unmeasured.online_skill_rating` | 最近一次平台 publicScore 快照 + 读取时间（CLI/页面证据）；样本极小，不作分布结论 | man-submit-r2 |
| `metrics.software.unmeasured.online_feedback_calibration` | value 扩展子字段：`round2_public_record`、`round2_sampling_ledger`（每日 ≤5 次、每候选 ≤2 次/日的额度使用与 Validation 状态台账）、`round2_pullback_reviews`（每轮回拉 ≥3 局公共回放清单与复盘结论）、`stop_loss_status`（公共局累计 ≥6 局且胜率 <50% 的判定与触发动作） | man-submit-r2 / SOP v4 |
| `metrics.software.unmeasured.final_submission_commits` | man-final 执行后回填最近 2 份提交 commit/hash 与 Validation Episode 状态；此前保持 `null` | man-final |

## 8. m5 document 键沿用

`metrics.document.*` 的 13 个既有键（report_compile_exit_code / report_compile_seconds / report_pages / report_consistency_check_exit_code / report_metric_key_references / report_dangling_metric_keys / report_unkeyed_performance_numbers / report_historical_baseline_disclosures / report_prohibited_extrapolation_hits / report_visual_pages_checked / report_visual_defects / report_human_ai_appendix_present / report_rewrite_mapping_coverage）在 m5 成稿后重新实测覆盖，不沿用本大纲版 PDF 的旧值。

## 9. 报告占位符 → 键回填映射（m5 执行）

| 报告占位（章节） | 目标键 | 回填波次 |
|---|---|---|
| 「待 m1 实测」入库局数/剔除局数/档案数/覆盖局数/复核统计（第 7 章 m1 节） | `m1_replay_corpus_summary`, `m1_profile_archive_inventory`, `m1_cross_review_summary`, `m1_profile_dimension_coverage` | m1 |
| 「待 m1 实测」榜单快照（第 6 章） | `m1_round1_ladder_context` | m1 |
| 「待 m2 实测」对手清单/画像参数来源/认证局数与战绩（第 7 章 m2 节） | `m2_online_style_opponents`, `m2_opponent_pool_certification` | m2 |
| 「待 m3 实测」冻结身份（第 5/7 章） | `m3_frozen_candidate_identity`, `m3_development_gate_summary` | m3 |
| 「待 m4 实测」种子数/赛程/逐对与区间（第 7 章 m4 节） | 第 6 节全部 `m4_*` 键 | m4 |
| 止损触发记录（第 8 章台账引用） | `unmeasured.online_feedback_calibration` 扩展子字段 | round-2 人工回填 |

回填时旧结论纪律不变：第 5 章战役 II 数字继续绑定前代候选 SHA（`m2b_candidate_sha256`），m4 结论只对 `m3_frozen_candidate_identity` 有效，二者互不外推。

## 10. 验收覆盖矩阵

| 蓝图验收 | 键证据组 |
|---|---|
| m1-tests | `m1_tests_r3_*`, `m1_profile_dimension_coverage` |
| m1-corpus | `m1_replay_corpus_summary`, `m1_corpus_integrity_pass`, `m1_profile_archive_inventory`, `m1_cross_review_summary` |
| m1-smoke | 沿用 `smoke_boot_*`（按第 2 节裁决） |
| m2-pool | `m2_online_style_opponents`, `m2_opponent_pool_certification`, `m2_opponent_unit_tests_summary` |
| m2-gate | `m2_gate_required_opponents`, `m2_gate_contract_check_pass` |
| m2-ab | 沿用 `llm_ab_*` nullable 键 |
| m3-strategy | `m3_strategy_capability_checks`, `m3_strategy_regression_summary` |
| m3-dev-gate | `m3_development_gate_summary`, `m3_frozen_candidate_identity` |
| m4-holdout / m4-identity / m4-metrics | 第 6 节 16 键 |
| doc-compile / doc-consistency / doc-visual | 第 8 节 document 键（m5 重测） |
| man-submit-r2 / man-final | 第 7 节 unmeasured.online_* 沿用键 |

人工验收不由本清单制造完成值；对应键在人工动作发生前保持 `null`。

## 11. 本清单自检口径

- software 新键定义：33 个（m1 8 + m2 5 + m3 4 + m4 16）。
- unmeasured.online_* 沿用键：4 个（子字段扩展，不新增顶层键）。
- document m5 沿用键：13 个（重新实测）。
- 报告占位符回填映射：6 行；蓝图自动验收覆盖 13 项 + 人工 2 项仅保留接口。
- 命名冲突检查：33 个新键与当前 `workspace/metrics.json` 既有键零重名（`m1_tests_r3_*` 显式避开战役 II `m1_tests_*`）。
