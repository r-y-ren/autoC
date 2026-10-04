# 治理处置记录汇编（record_governance_dispositions · R4/R17/R21）

本汇编索引三件处置记录；各记录事实与判据见其正文。

| 处置 | 记录文件（fn_docs/） | 需求 | 要点 |
|---|---|---|---|
| dual_source_provenance | provenance_dadee25a.md | R4 | dadee25a 双源血统（kaitofukami 08-31 首拉 + ahmedberatozer 09-20 拉回，原创归属两账号间未定）+ 全库单源断言扫描清单 |
| blueprint_cmd_invalidation | blueprint_cmd_invalidation.md | R17 | 蓝图 2 条失效验收 cmd（docs/report.typ、docs/check_report_metrics.py 不存在）+ 09-01 后 /accept 静默事实；处置=战后经 /attack 修订 |
| active_candidate_demotion | active_candidate_disposition.md | R17/R21 | active_candidate 现状快照（v72 时代/online_refs 空）+ 战后降级预案+ 时点闸（2026-09-30 收口前只许记录，物理动作拒绝） |

## 记录 schema 校验

| 记录 | 存在 | 必需标记数 | 缺失 |
|---|---|---|---|
| provenance_dadee25a.md | True | 5 | 无 |
| blueprint_cmd_invalidation.md | True | 4 | 无 |
| active_candidate_disposition.md | True | 4 | 无 |

## 编排元信息

- 生成器: fn_work/src/record_governance_dispositions/record_governance_dispositions.py（W4 治理处置编排）
- 编排语义: 只产记录不改物理面（旧树冻结；蓝图修订战后 /attack；台账降级战后受时点闸）。
