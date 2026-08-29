---
competition_id: kaggle-kaggriculture
campaign: Kaggriculture 农场博弈 Agent 战役 II（审计修订版）
blueprint_ref: b7664d2
generated_at: 2026-08-29 11:15
basis: {patterns_coverage: "低置信度；无 winner-derived 样本", run_ref: "run-13.json"}
---

# Kaggriculture 审计修订最终验收分析

本轮 `13` 项 agent/automatic 验收均为 pass，完整软件套件与验收夹具也均通过。总结果仍为 `pending_manual`，唯一原因是 `man-reg`、`man-submit`、`man-final` 尚待人工执行；retry 为 `0/3`，熔断未触发。状态证据：`workspace/acceptance/run-13.json`；软件套件证据：`workspace/acceptance/evidence/m2a-test.log`。上述验收项计数与 retry 属于 run-13 流程状态；作品性能数字均在下文逐项引用 `workspace/metrics.json` 精确键。

## 一、对照评审标准逐项自评

| 标准 | 作品对应点 | 证据 | 自评 |
|---|---|---|---|
| 可运行性与规则契约 | stdlib-only bot 已完成官方引擎短局、完整回合自博弈、双方座位及 replay/contract smoke；当前完整软件套件与验收夹具均通过。 | `workspace/acceptance/evidence/m2a-smoke.log`；`workspace/acceptance/evidence/m2a-test.log` | 强 |
| 策略正确性 | 末日无无效资本支出、末日现收处置、购买观察确认、shed 库存预留、正数量订单和跨局隔离均为 true；定向策略套件 `35/35` 通过。 | `workspace/metrics.json#/software/metrics/strategy_repair_checks/value`；`workspace/metrics.json#/software/metrics/strategy_repair_test_summary/value`；`workspace/acceptance/evidence/m2b-strategy.log` | 强 |
| 评估保真与完整性 | 一次性 holdout 预期/实际为 `576/576`，AB/BA 为 `288/288`，缺失镜像 `0`，异常局 `0`，完整性为 true。 | `workspace/metrics.json#/software/metrics/holdout_schedule/value`；`workspace/metrics.json#/software/metrics/holdout_seat_split/value`；`workspace/metrics.json#/software/metrics/holdout_abnormal_summary/value`；`workspace/metrics.json#/software/metrics/holdout_integrity_pass/value`；`workspace/acceptance/evidence/m2c-holdout.log` | 强 |
| 候选身份与可追溯性 | 冻结候选 SHA-256 为 `7c482921857562e6b7cd58a3ac4bde358981c180cc233ad3913948e5fcafa66a`；holdout 前、中、后身份一致且校验通过，正式 export 可追到 schema 与确认性 JSON Pointer。 | `workspace/metrics.json#/software/metrics/m2b_candidate_sha256/value`；`workspace/metrics.json#/software/metrics/holdout_candidate_hash_match/value`；`workspace/metrics.json#/software/metrics/confirmatory_export_traceability/value`；`workspace/acceptance/evidence/m2c-identity.log` | 强 |
| 本地确认性表现 | 冻结候选在本地研究对手池的确认集共 `128` 局，记录为 `119W-9L-0T`，score rate 为 `0.929688`，Wilson 区间为 `[0.8718, 0.9626]`；按 `(opponent, seed)` 聚合 AB/BA 的顺序无关估计为 `0.929688`，区间为 `[0.867281, 0.992094]`。 | `workspace/metrics.json#/software/metrics/confirmatory_overall_record/value`；`workspace/metrics.json#/software/metrics/confirmatory_order_independent_statistics/value` | 强，但只适用于本地对手池 |
| 文档可审计性 | 当前报告为 `5` 页、引用 `32` 个唯一 metrics 键；悬空键、未标键性能数字及禁止外推命中均为 `0`。指定视觉 judge 已检查 `5/5` 页，视觉缺陷为 `0`；当前 PDF SHA-256 为 `7baa5bf1d6145db5a546a58e99e2be4dbc83b2754529096dcd456c04f9d89153`。 | `workspace/metrics.json#/document/metrics/report_pages/value`；`workspace/metrics.json#/document/metrics/report_metric_key_references/value`；`workspace/metrics.json#/document/metrics/report_dangling_metric_keys/value`；`workspace/metrics.json#/document/metrics/report_unkeyed_performance_numbers/value`；`workspace/metrics.json#/document/metrics/report_prohibited_extrapolation_hits/value`；`workspace/metrics.json#/document/metrics/report_visual_pages_checked/value`；`workspace/metrics.json#/document/metrics/report_visual_defects/value`；`workspace/acceptance/evidence/doc-visual-13-01.log`；`workspace/acceptance/evidence/doc-visual-13-02.png` 至 `doc-visual-13-06.png` | 强 |
| 线上竞争力与交付闭环 | 线上对局、线上 skill rating、线上反馈校准和最终提交 commits 仍为 null；尚无真实线上结果可用于评价。 | `workspace/metrics.json#/software/unmeasured/online_ladder_games/value`；`workspace/metrics.json#/software/unmeasured/online_skill_rating/value`；`workspace/metrics.json#/software/unmeasured/online_feedback_calibration/value`；`workspace/metrics.json#/software/unmeasured/final_submission_commits/value` | 弱，待人工闭环 |

综合判断：作品在本地可执行性、评估治理、候选冻结、确认性统计和文档审计上达到强证据水平；线上提交与反馈尚未发生，因此最终验收只能维持 `pending_manual`，不能据此声称天梯名次、获奖概率或人工项完成。

## 二、赛点检查表核对

- [x] **完整回合与 contract 红线**：smoke 覆盖短局、完整回合、双方状态及 replay round-trip，结果 pass。证据：`workspace/acceptance/evidence/m2a-smoke.log`。
- [x] **终局策略红线**：末日资本支出、现收变现、购买确认、库存预留和正数量订单检查均为 true。来源键：`workspace/metrics.json#/software/metrics/strategy_repair_checks/value`。
- [x] **冻结身份**：候选 SHA-256 为 `7c482921857562e6b7cd58a3ac4bde358981c180cc233ad3913948e5fcafa66a`，holdout 身份匹配为 true。来源键：`workspace/metrics.json#/software/metrics/frozen_candidate_identity/value`；`workspace/metrics.json#/software/metrics/holdout_candidate_hash_match/value`。
- [x] **开发集与确认集隔离**：历史种子重叠计数为 `0`，隔离判定为 true；holdout 标记为 one-time，候选变化会使结果失效。来源键：`workspace/metrics.json#/software/metrics/holdout_seed_domain_isolation/value`；`workspace/metrics.json#/software/metrics/holdout_protocol/value`。
- [x] **AB/BA 完整矩阵**：正式矩阵 `576/576`，AB/BA `288/288`，缺失镜像 `0`。来源键：`workspace/metrics.json#/software/metrics/holdout_schedule/value`；`workspace/metrics.json#/software/metrics/holdout_seat_split/value`。
- [x] **异常 fail-closed 与门禁不可绕过**：异常局为 `0`；生产契约检查拒绝缺对手、单座位、异常状态、畸形 tie、种子域不一致及 exploratory 冒充正式 PASS。来源键：`workspace/metrics.json#/software/metrics/holdout_abnormal_summary/value`；`workspace/metrics.json#/software/metrics/m2a_gate_contract_check_pass/value`；证据：`workspace/acceptance/evidence/m2a-gate-contract.log`。
- [x] **正式 export 事务安全**：schema、语义、路径别名、replay 与发布事务检查通过。来源键：`workspace/metrics.json#/software/metrics/m2a_export_safety_check_pass/value`；证据：`workspace/acceptance/evidence/m2a-export-safety.log`。
- [x] **确认性统计边界**：主结论采用逐对 W/L/T、座位分层、Wilson 区间与顺序无关配对估计；Elo 仅作描述性附录。来源键：`workspace/metrics.json#/software/metrics/confirmatory_pair_records/value`；`workspace/metrics.json#/software/metrics/confirmatory_seat_records/value`；`workspace/metrics.json#/software/metrics/confirmatory_wilson_intervals/value`；`workspace/metrics.json#/software/metrics/confirmatory_order_independent_statistics/value`；`workspace/metrics.json#/software/metrics/confirmatory_elo_appendix/value`。
- [x] **LLM A/B 条件契约**：环境未配置完整 `KG_LLM_*`，真实 A/B 胜率与预算闸命中保持 null；本地 provider、逐局 budget、fallback 和 real-A/B 边界测试通过，且没有外部调用。来源键：`workspace/metrics.json#/software/unmeasured/llm_ab_win_rate/value`；`workspace/metrics.json#/software/unmeasured/llm_ab_budget_gate_hits/value`；`workspace/metrics.json#/software/metrics/m2a_llm_null_effective_calls/value`；`workspace/metrics.json#/software/metrics/m2a_llm_null_fallback_count/value`；证据：`workspace/acceptance/evidence/m2-ab-13-01.log`。
- [x] **文档一致性与视觉检查**：编译与一致性检查退出码均为 `0`，指定 judge 对当前 PDF 的全部 `5` 页完成复核。来源键：`workspace/metrics.json#/document/metrics/report_compile_exit_code/value`；`workspace/metrics.json#/document/metrics/report_consistency_check_exit_code/value`；`workspace/metrics.json#/document/metrics/report_visual_pages_checked/value`；证据：`workspace/acceptance/evidence/doc-consistency.log`、`workspace/acceptance/evidence/doc-visual-13-01.log`。
- [ ] **报名状态终验**：`man-reg` 待人工复核账号仍在队。
- [ ] **真实线上提交与反馈**：`man-submit` 待人工执行；线上相关值目前均为 null。来源键：`workspace/metrics.json#/software/unmeasured/online_ladder_games/value`；`workspace/metrics.json#/software/unmeasured/online_feedback_calibration/value`。
- [ ] **截止前最终锁定**：`man-final` 待人工锁定并回填最终提交身份；当前值为 null。来源键：`workspace/metrics.json#/software/unmeasured/final_submission_commits/value`。

## 三、与历年获奖基准对比

该赛现有 patterns 置信度低，且没有 winner-derived 样本，因此历年获奖基准未建，无法进行获奖方案分布或名次门槛的量化对比。当前作品落在“启发式自主 agent + 可执行评估治理 + 一次性独立 holdout”的工程模式上；其差异化主要是把候选身份、种子隔离、AB/BA、异常 fail-closed、原子发布和 metrics-only 文档约束串成可审计链路，而不是声称复现了历届获奖套路。

本地确认集显示候选在研究对手池中的记录为 `119W-9L-0T`，Wilson 区间为 `[0.8718, 0.9626]`；这只能证明对该本地池的结果，不覆盖未知线上策略分布。来源键：`workspace/metrics.json#/software/metrics/confirmatory_overall_record/value`。

历史披露仅此一处：`1500.8 / 36-0` 来自固定 p0、复用开发种子且顺序敏感的 Elo 流，是非确认性的历史开发记录，也不是线上结果。该记录只解释本轮为何重做审计，不参与当前主结论。来源键：`workspace/metrics.json#/software/metrics/m2_elo_ratings_full_pool/value`。

竞争密度与真实线上能力目前不可判定：线上对局、线上 skill rating 与线上反馈校准均为 null。来源键：`workspace/metrics.json#/software/unmeasured/online_ladder_games/value`；`workspace/metrics.json#/software/unmeasured/online_skill_rating/value`；`workspace/metrics.json#/software/unmeasured/online_feedback_calibration/value`。因此本报告不主张天梯排名、获奖概率或本地结果向线上的外推。

## 四、人工测试项与遗留风险

当前结果为 `pending_manual`。以下 MANUAL_TEST 必须由参赛团队在 Kaggle 实际账号环境完成，并将时间、URL、账号/团队身份、结果截图或回执与候选身份一并留档；本报告不把这些项目视为已完成。

- **`man-reg`：报名与团队成员复核。** 登录实际参赛账号，打开竞赛与团队页面；确认 `userHasEntered=True`，并确认该账号当前仍在目标团队。留存同时可辨识账号、竞赛、URL、复核时间和团队状态的截图；若账号已退队、团队变化或页面无法确认，立即停止提交并升级人工处理。
- **`man-submit`：真实线上提交与反馈。** 严格按 SOP v3 对冻结候选 `7c482921857562e6b7cd58a3ac4bde358981c180cc233ad3913948e5fcafa66a` 制作提交，在 Kaggle 执行真实 online submission；记录提交回执、Validation Episode 状态、平台反馈、对应 commit/hash 和提交时间。候选身份来源键：`workspace/metrics.json#/software/metrics/m2b_candidate_sha256/value`。当前线上对局与反馈仍为 null，来源键：`workspace/metrics.json#/software/unmeasured/online_ladder_games/value`；`workspace/metrics.json#/software/unmeasured/online_feedback_calibration/value`。
- **`man-final`：截止前最终锁定。** 在赛事 deadline 前复核提交列表与 Validation Episode 状态，锁定平台规则要求跟踪的最新两份提交；逐份记录 commit/hash、候选 SHA、提交时间、平台状态和选择理由，并回填最终提交 commits。当前该字段为 null，来源键：`workspace/metrics.json#/software/unmeasured/final_submission_commits/value`。

遗留风险包括：本地对手池与线上分布不一致；真实平台运行环境、排队、Validation Episode 和反馈尚未实测；报名/团队状态可能在终验后变化；线上反馈若触发策略调整，旧候选身份及已公开 holdout 不得复用为新候选的确认性证据。one-time 与候选变化失效规则来源键：`workspace/metrics.json#/software/metrics/holdout_protocol/value`。

## 五、人机分工记录（合规留痕）

**AI 辅助范围**

- 协助检索并整理赛事规则、工程约束与审计问题，生成评估治理、策略修复、测试和文档草稿。
- 实现并执行 AB/BA 调度、种子域隔离、异常 fail-closed、候选身份检查、正式 export 事务发布、统计汇总和 metrics 引用检查。
- 协助编写 bot、回归测试、报告与 SOP，并基于实际日志和 `workspace/metrics.json` 整理证据；不为缺失的线上结果生成替代值。
- 在 `m2-ab` 验收中只执行本地无网络的 provider/budget/fallback 边界核验；有效外部 LLM 调用为 `0`，真实 A/B 指标保持 null。来源键：`workspace/metrics.json#/software/metrics/m2a_llm_null_effective_calls/value`；`workspace/metrics.json#/software/unmeasured/llm_ab_win_rate/value`；证据：`workspace/acceptance/evidence/m2-ab-13-01.log`。

**人工责任**

- 人工审阅赛事规则、AI 政策、策略方向、风险边界与冻结决策，决定证据是否足以进入交付。
- 人工确认 Kaggle 账号、报名与团队状态；执行真实线上提交，解释线上反馈，决定是否形成新候选。
- 人工在 deadline 前完成最终提交选择、签字与留档，并确保任何候选变化都触发新身份和新的独立确认流程。
- 人工对最终对外表述负责，不得把本地 holdout、描述性 Elo 或未发生的 LLM/线上指标改写为天梯或获奖结论。

**声明落点**

作品报告附录已保留非空人机分工说明，来源键：`workspace/metrics.json#/document/metrics/report_human_ai_appendix_present/value`。归档时应同时保留本节、报告附录、候选 manifest、验收记录、人工截图/回执和最终提交映射，形成“AI 辅助原创、人工决策与提交”的可追溯记录。

## 六、可复用资产清单

- **冻结候选与身份清单**：stdlib-only Kaggle agent、冻结 manifest、候选 SHA/git ref/snapshot 关系；可复用于需要提交包身份锁定的 agent 赛。来源键：`workspace/metrics.json#/software/metrics/m2b_frozen_manifest/value`；`workspace/metrics.json#/software/metrics/frozen_candidate_identity/value`。
- **AB/BA 评估框架**：按 pair/seed 生成镜像座位，检查预期局数、缺失镜像和异常局；可迁移到双边博弈或座位敏感评测。来源键：`workspace/metrics.json#/software/metrics/holdout_schedule/value`；`workspace/metrics.json#/software/metrics/holdout_seat_split/value`。
- **一次性 holdout 协议**：冻结后随机生成、历史种子排除、公开后不可刷新、候选变化即失效；可用于防调参泄漏的确认性评估。来源键：`workspace/metrics.json#/software/metrics/holdout_protocol/value`；`workspace/metrics.json#/software/metrics/holdout_seed_manifest/value`；`workspace/metrics.json#/software/metrics/holdout_seed_domain_isolation/value`。
- **fail-closed 与原子发布门**：生产契约验证、schema/语义交叉检查、quick/dev/失败产物隔离及正式 export 事务发布；可复用于模型评测和数据竞赛证据发布。来源键：`workspace/metrics.json#/software/metrics/m2a_gate_contract_check_pass/value`；`workspace/metrics.json#/software/metrics/m2a_export_safety_check_pass/value`。
- **确认性统计与追溯映射**：逐对 W/L/T、座位分层、Wilson 区间、顺序无关配对估计及正式 export JSON Pointer；可作为后续 agent 评测模板。来源键：`workspace/metrics.json#/software/metrics/confirmatory_wilson_intervals/value`；`workspace/metrics.json#/software/metrics/confirmatory_order_independent_statistics/value`；`workspace/metrics.json#/software/metrics/confirmatory_export_traceability/value`。
- **metrics-only 文档管线**：Typst 报告、指标键检查、禁止外推扫描、视觉验收和人机分工附录；可复用于需要数字溯源的交付文档。来源键：`workspace/metrics.json#/document/metrics/report_metric_key_references/value`；`workspace/metrics.json#/document/metrics/report_dangling_metric_keys/value`；`workspace/metrics.json#/document/metrics/report_prohibited_extrapolation_hits/value`；`workspace/metrics.json#/document/metrics/report_human_ai_appendix_present/value`。
- **条件式 LLM A/B harness**：完整配置才允许真实 A/B，逐局重建 provider/budget，未配置时保持 null 并验证 fallback；可复用于可选外部模型路径。来源键：`workspace/metrics.json#/software/metrics/llm_ab_harness_ready/value`；`workspace/metrics.json#/software/unmeasured/llm_ab_win_rate/value`；`workspace/metrics.json#/software/unmeasured/llm_ab_budget_gate_hits/value`。
- **人工提交 SOP v3**：把报名复核、真实提交、Validation Episode、线上反馈和最终锁定明确留给人工；线上未测字段持续保持 null，避免自动化伪造完成态。来源键：`workspace/metrics.json#/software/unmeasured/online_ladder_games/value`；`workspace/metrics.json#/software/unmeasured/online_feedback_calibration/value`；`workspace/metrics.json#/software/unmeasured/final_submission_commits/value`。
