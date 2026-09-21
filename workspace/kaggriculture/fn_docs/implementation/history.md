# history.md —— 历史表（已完成批次队列，只追加不删改）
> fn-implement 独占更新。每批次完成后尾部追加留痕。

| 完成日期 | 批次 | 任务/函数清单（含操作与来源说明） | 验收摘要 |
|---|---|---|---|
| 2026-09-21 | B1 | discover_campaign_roots, run_equivalence_gate（shared 基座） | 两函数 wired：roots 特征发现 8 测绿（三根/CWD 无关/fail-closed/零字面路径）；等价门旧树基线 pass（62P+4xf 实跑 36.8s）；全套件 60P |
| 2026-09-21 | B2 | aggregate_scores（值序裁切修复）, break_ties_by_identity（语义随迁）, robust_selection（顶层接线） | 26 passed；差分=仅 R3 修复增量；评审见 B2 报告 |
