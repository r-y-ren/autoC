---
id: jia2025DistributionallyRobustOptimization
name: UAV-HAP 分层空中 MEC 的 CVaR 分布鲁棒优化
field: [空中边缘计算, 分布鲁棒优化, 资源分配]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 参数不确定性下的机会约束建模经 CVaR 转分布鲁棒约束再重写 MISOCP，配原始分解与二元鲸鱼优化的完整求解链，是数模含不确定参数优化题的进阶武器，鲁棒性对照实验设计也可直接借鉴
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 「UAV 灵活接入 + HAP 稳定算力」的分层空中算力架构是低空经济/空天地一体化申报的架构亮点，CSI 误差鲁棒性论证能显著提升方案可信度
    reuse_cost: 低
sources:
  - paper_title: "Distributionally Robust Optimization for Aerial Multi-Access Edge Computing via Cooperation of UAVs and HAPs"
    doi: 10.1109/TMC.2025.3571023
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# UAV-HAP 分层空中 MEC 的 CVaR 分布鲁棒优化

## 单行摘要

构建高空平台 HAP 与多 UAV 协同的分层空中 MEC 体系（HAP 提供稳定大容量算力、UAV 提供灵活近端接入），把 CSI 估计误差引起的约束不确定性经 CVaR 机制转化为分布鲁棒约束，将带机会约束的能耗最小化 MINLP 重写为 MISOCP，再用原始分解与二元鲸鱼优化算法求解，得到不确定环境下近最优且更稳健的部署与资源配置方案。

## 方法快照

- 分层架构：HAP 高空固定提供上层稳定算力，UAV 作近端空中 MEC 节点接入地面用户；任务经 G2U 链路进入 UAV 后按资源状况在 UAV/HAP 侧分层执行。
- 决策耦合：UAV 部署（加权 K-means 预优化）、用户关联、二元卸载决策、通信与计算资源分配放在同一层级模型。
- 鲁棒化链路：机会约束 MINLP → CVaR 分布鲁棒约束 → MISOCP；primal decomposition 拆成连续与离散子问题，二元鲸鱼优化算法解离散卸载与关联决策。
- 验证：合成空中 MEC 场景数值仿真，鲁棒性评估设计较完整；平台/硬件/代码形态未公开。

## 比赛映射要点

- 数模：凡题面带「参数不确定/估计误差」的优化题，机会约束 + CVaR + 可凸重写的三段式处理是超越确定性模型的差异化写法，且实验可做「确定性 vs 鲁棒」对照。
- 双创申报：分层空中算力（临近空间 + 低空）的架构叙事在低空经济与应急通信申报中辨识度高。

## 关联概念
- 高空平台（HAP）
- 分布鲁棒优化（DRO）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Jia2025_UAV与HAP协同空中MEC的分布鲁棒优化`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `jia2025DistributionallyRobustOptimization` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16），页内容与 bib 条目相符。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 承自 vault 页自评（artifact_availability: unknown，故 runnable 如实标 false）；能耗节省幅度等数字如需引用请以论文原文复核。
