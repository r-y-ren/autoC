# active_candidate 降级处置记录（R17/R21）

## 现状快照

- 读取时点: 2026-09-21（记录生成时实测读取）
- schema_version: 1.0
- working: v14.3-sellrace-working（status=development，sha256=f1f46638b8b7…）
- last_promoted_frozen: v72-frozen（status=frozen，sha256=c44e2b254686…）
- published_holdout: published（attempt 5）
- online_submission_refs: []（空=无在册线上引用）
- 时代定性: v72 时代（在役身份链 working+promoted 冻结态并存；online_refs 空=无在册线上引用）

## 降级预案（战后执行）

- 动作: 降级 active_candidate.json 为历史台账（historical ledger）
- 前置条件: 终局收口（2026-09-30）完成之后；收口前物理动作被时点闸拒绝
- 1. 收口后读取在册 active_candidate.json，整体收进 historical 键（不删字段，可回滚）
- 2. schema_version 追加 -historical 后缀，登记 demoted_at 与 demote_reason
- 3. 新立（或移交）战后现役身份链载体，旧台账只读留档
- 边界: 不现在补记、不现在降级——避免动在役身份链（R17 明文）

## 时点闸（fail-closed 断言）

- 闸日: 2026-09-30（终局收口日）；裁决时钟 now=2026-09-22（阶段=pre-closeout）。
- 语义: 收口前（now<=闸日，含收口日当日）物理降级动作一律拒绝（DemotionGateError），只许产出本记录；收口后（now>闸日）方许执行。
- 本次裁决: physical_action=record-only（未请求物理动作，纯记录态）

## 记录元信息

- 生成器: fn_work/src/record_governance_dispositions/demote_active_candidate_ledger.py（record_governance_dispositions 编排叶）
- 台账归宿: software/active_candidate.json（在役身份链，收口前零写入）。
