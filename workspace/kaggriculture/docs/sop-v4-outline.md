# Kaggriculture 提交 SOP v4 大纲（第 1 波）

> 状态：大纲版，随战役 III m5 波次成稿；基于 `workspace/docs/submit-sop.md`（SOP v3）结构演进。
> 本文件只定章节结构、条款主题与数据接口，不写检查项成稿，不制造任何“已执行”状态。
> 依据：`workspace/blueprint.md` m5 任务与 man-submit-r2 / man-final 验收；键位见 `metrics-keys-r3.md` 第 7 节。
> 常量声明：本文中的额度与阈值（每日 ≤5 次、每候选 ≤2 次/日、每轮回拉 ≥3 局、公共局累计 ≥6 局且胜率 <50%）是蓝图契约常量，不是实测数字。

## 变更摘要（v3 → v4）

1. 权威身份切换：从战役 II 冻结候选（`frozen_candidate_identity`，sha 前缀 7c482921）切换为战役 III `m3_frozen_candidate_identity` 与 m4 holdout v2 正式 export；旧身份整段降级为历史记录并保留“不得引用旧确认为新候选背书”的限制。
2. 新增第 6 节“回拉与复盘循环”：把“提交-回拉-复盘”固化为每轮必做的循环协议。
3. 新增第 7 节“止损线与转备选”：写明触发条件、触发动作与记录键位。
4. 第 4 节并入 round-2 天梯采样协议核心条款（额度、Error 即停、最近 2 次跟踪）。
5. 其余各节沿用 v3 条款主题，身份与路径指向更新。

## 0. 权威身份与正式产物（改写 v3 第 0 节）

- 数据源：`metrics.software.m3_frozen_candidate_identity` + `metrics.software.m4_confirmatory_export_traceability`；从 metrics 读身份，不从旧报告或终端历史抄值。
- 计划检查项主题：候选文件 SHA-256 复核、正式 export SHA-256 复核、git ref 一致、任一不一致立即停止且不得以重跑 holdout“修复”。
- 历史身份段：战役 II 冻结候选与其 export 保留为历史记录，仅供审计，不得为新候选背书。

## 1. 已发布 holdout 保护门（沿用 v3 第 1 节，扩展适用范围）

- 战役 II holdout 与战役 III holdout v2 均只允许 verify-only（`run_holdout.py --verify-published --require-frozen` 类接口，以 m4 实际脚本为准）。
- 禁止创建新 attempt、重抽种子、重放择优、删除失败 attempt、覆盖正式 export。
- 新候选不得引用任一旧确认；候选变更即作废旧确认的适用性。

## 2. 正式 export 检查（沿用 v3 第 2 节）

- `check_eval_contract.py --mode official` 类接口对 m4 export 做 schema、语义与跨字段验证（以 m4 实际命令为准）。
- 核对 `m4_confirmatory_export_traceability` 的 export SHA、schema 与 JSON Pointer 映射。
- 不得用 merge_metrics 掩盖 export 错误。

## 3. 提交前候选检查（沿用 v3 第 3 节 + 对手池扩展）

- 冻结身份复核、smoke 与全量测试（含线上风格对手单测）、stdlib-only 与离线自主运行确认、台账登记。
- 新增主题：确认对手池与门禁必测名单为 m2 更新后的版本（`m2_gate_required_opponents`）。

## 4. 人工线上提交与 round-2 天梯采样协议（v4 核心改写）

- 账号与团队规则确认；AI 不代操作账号。
- 采样额度：每日提交至多 5 次；每候选至多 2 次/日；提交前核对当日计数与“最近 2 次提交”跟踪，新提交不得无意覆盖应保留版本。
- Error 即停：Validation Episode 返回 Error 即停止当日提交并上报，不得连续重试掩盖错误。
- 台账：逐次记录提交序号、candidate SHA、Validation 状态与是否保留；对接 `online_feedback_calibration` 扩展子字段 `round2_sampling_ledger`。

## 5. 竞赛运行约束（沿用 v3 第 5 节）

- 额度台账、最近 2 次提交状态、终交前逐条人工确认；未看到赛站记录前不标记已执行。

## 6. 回拉与复盘循环（v4 新增）

- 每次提交后回拉不少于 3 局公共天梯回放完成复盘（episode 级清单入台账，对接 `round2_pullback_reviews`）。
- 复盘产出：失败模式台账更新（延续 FM-O 编号族）、画像档案滚动更新（携带来源 URL 与抓取日期）、是否触发新候选的判定。
- 跨局复核纪律：同选手不少于 3 局一致才可更新对手池参数；单局结论一律标 exploratory。
- 复盘产生的任何策略变化走 v3 第 6 节规则：新候选、新 SHA、新独立确认种子（对应 m4 流程）。

## 7. 止损线与转备选（v4 新增）

- 触发条件：新候选线上公共局累计不少于 6 局且胜率低于 50%。
- 触发动作：停止本方向调参；转备选方向接力；触发判定与动作记录入 `stop_loss_status` 子字段并上报队伍。
- 边界声明：止损是资源分配决策，不得写成对线上实力、名次或获奖的结论。

## 8. 终交锁定（沿用 v3 第 7 节）

- 09-30 前人工核对最近 2 份提交的提交 ID、candidate SHA、git ref 与 Validation Episode 状态并锁定。
- 回填 `unmeasured.final_submission_commits`（回填前保持 null）；操作人/复核人/日期台账签字，AI 不代签；锁定后不再实验性提交。

## 9. 停止条件（v3 扩展）

出现以下任一情况立即停止并上报：

- 候选 SHA 或 export SHA 与第 0 节不一致；
- verify-only 检查试图启动新对局或改变 attempt 状态；
- schema、语义、跨字段、完整矩阵、AB/BA 或异常检查失败；
- 已变化候选仍试图引用旧 holdout/旧确认；
- Validation Error 后仍被要求继续提交，或当日额度/最近 2 次状态无法确认；
- 止损线已触发但未执行转备选动作；
- 线上结果尚未产生却要求填写非 null 线上指标。

## 与 metrics 键的对接（成稿时落检查项引用）

| SOP 环节 | 键位 |
|---|---|
| 0 身份 | `m3_frozen_candidate_identity`, `m4_confirmatory_export_traceability` |
| 1-2 holdout/export 保护 | `m4_holdout_run_status`, `m4_holdout_integrity_pass` |
| 3 提交前检查 | `m2_gate_required_opponents`, smoke/测试键 |
| 4 采样额度台账 | `unmeasured.online_feedback_calibration.round2_sampling_ledger` |
| 6 回拉复盘 | `unmeasured.online_feedback_calibration.round2_pullback_reviews` |
| 7 止损 | `unmeasured.online_feedback_calibration.stop_loss_status` |
| 8 终交 | `unmeasured.final_submission_commits`, `unmeasured.online_skill_rating` |

## 大纲自检

- 节数：10（v3 的 8 节 + 新增 2 节，停止条件独立成节沿用 v3 形态）。
- 新增章节：第 6 节回拉与复盘循环、第 7 节止损线与转备选。
- 检查项编号：成稿时以 V4-01 起连续编号；本大纲只列主题不预分编号。
- 一切额度与阈值为蓝图契约常量；一切线上数值待人工执行后经 unmeasured 键回填，本大纲不预填。
