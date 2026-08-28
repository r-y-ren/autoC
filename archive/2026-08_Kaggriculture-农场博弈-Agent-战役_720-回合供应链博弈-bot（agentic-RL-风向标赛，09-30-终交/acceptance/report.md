---
competition_id: kaggle-kaggriculture
campaign: Kaggriculture 农场博弈 Agent 战役
blueprint_ref: 25d4900
generated_at: 2026-08-28 17:30
basis: {patterns_coverage: "kaggle-kaggriculture patterns（低置信·单届在赛）", run_ref: "run-1.json"}
---

# 作品分析报告：Kaggriculture 农场博弈 Agent

## 一、对照评审标准逐项自评

该赛为纯客观指标制（720 回合收益天梯）+ 复现性约束，无传统"评审标准"。按赛制特征对照：

| 赛制要求 | 作品对应点 | 证据 | 自评 |
|---|---|---|---|
| 官方引擎兼容 | vendored kaggle-environments 1.32.7+nodeps（引擎代码零修改） | metrics.software.engine | 强 |
| 本地可复现 | smoke_boot 自博弈冒烟 + requirements 锁定 | evidence/sw-boot.log、sw-deps.log | 强 |
| 工程质量 | 45/45 测试通过（收益模型单测+接口契约） | evidence/sw-test.log、metrics.tests_total | 强 |
| 方案可解释 | 报告 7 页（机制量化→基线→评估→迭代路线） | docs/report.pdf | 中 |
| 线上验证 | **未发生**——天梯未提交，线上指标全部如实为 null | metrics.boundary_note | 弱（人工项） |

## 二、赛点检查表核对

该赛 patterns 检查表要点 vs 现状：本地引擎复刻 ✓ / 提交预算"彩票"管理 → SOP 已列每日 ≤5 次纪律 ✓ / 验证 Episode 演练 ✓ / **Kaggle 报名与首提未完成 ✗（MANUAL 项）** / 开源时点策略（获奖前 CC0/MIT-0 要求）→ SOP 检查项已含 ⚠ 待提交时执行。

## 三、与历年获奖基准对比

patterns 覆盖为在赛首届（无往届）。参照同族 Kaggle agent 仿真赛模式（AIMO patterns"工程鲁棒性决胜"结论）：本作品采用启发式基线+评估基建先行、增强迭代（搜索/学习 A/B）后置的路线，与"先保正确性下限再拼差异化"的族内共识一致；线上未提交前无法验证真实天梯分位——**不宣称任何线上实力**。

## 四、人工测试项与遗留风险

| 项 | 内容 | 期限 |
|---|---|---|
| man-reg | Kaggle 报名（entry_deadline 官方数值缺失，第 0 天人工核对赛站锁定） | 尽早 |
| man-submit | 线上提交与天梯观察（按 docs/submit-sop.md 19 项检查单执行） | 终交 2026-09-30 |

风险：赛站关键日期（报名截止/终交）为单源或缺失——SOP 已列"第 0 天核对"缓解；策略迭代 m4 的"按评估器择优"依赖首轮线上反馈，存在时间窗风险（09-30 终交前需保留 ≥2 轮迭代窗口）。

## 五、人机分工记录（合规留痕，apply 模式）

AI（本框架）：KB 情报与模式归纳、方案报告、全部代码实现（收益模型/基线 bot/评估基建/测试）、编译与本地验证、提交 SOP 起草。
人工：赛队账号注册与报名、线上提交操作与天梯观察（每日提交决策）、策略方向的最终裁量。
申报附件：AI 使用声明与详情文档已随交付产出（apply 模式强制项），提交时按赛方模板誊入。

## 六、可复用资产清单

- 官方引擎 vendored 复刻路线（kaggle-environments 本地化，同族 Kaggle 仿真赛可直用）
- 评估基建骨架（对手池/Elo 六榜/复盘日志，40 局本地评估协议）
- submit-sop 19 项提交检查单（Kaggle 类通用，含开源时点与提交预算纪律）
- 报告模板实践：18 个数字键全文一致的回填流程（metrics 键→正文映射表）
