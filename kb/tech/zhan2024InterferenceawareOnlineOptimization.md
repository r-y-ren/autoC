---
id: zhan2024InterferenceawareOnlineOptimization
name: 能量约束蜂窝多UAV的干扰感知在线吞吐优化
field: [蜂窝连接无人机, 干扰管理, 凸优化]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 「滚动在线优化 + 交替优化 + 逐次凸近似（SCA）+ 精确罚函数」的完整求解工作流（MATLAB+CVX 披露）是数模连续优化与资源分配题的标准方法论模板，含无未来信息时的降复杂度 variant
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: max-min 公平吞吐目标 + 「轨迹本身就是干扰管理工具」的洞察，可差异化多机资源分配赛题的建模与求解，能量触发罚项保证可行性的技巧可直接移植
    reuse_cost: 中
sources:
  - paper_title: Interference-Aware Online Optimization for Cellular-Connected Multiple UAV Networks with Energy Constraints
    doi: 10.1109/TMC.2024.3438759
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 能量约束蜂窝多UAV的干扰感知在线吞吐优化

## 单行摘要

研究蜂窝连接多 UAV 上行通信的在线联合设计：在建筑遮挡、方向性天线与共信道强干扰下，协调多 UAV 的传输调度、功率控制与三维轨迹以最大化最小（max-min）吞吐并满足能量预算；给出两套方案——结合瞬时 CSI 与统计 CDI 的滚动优化，以及仅依赖当前 CSI、加入能量触发惩罚项的低复杂度方案，均经精确罚函数、交替优化与 SCA 求解。

## 方法快照

- 场景要点：UAV 的 LoS 优势与强上行互扰是同一枚硬币的两面；空地信道受建筑遮挡、天线方向图与小尺度衰落共同影响，几何距离不是唯一决定因素——「靠近基站不一定最优」。
- 在线方案 A（with CDI）：用当前瞬时 CSI 与未来时隙统计 CDI 做滚动优化。
- 在线方案 B（without CDI）：只用当前时隙 CSI，加入能量触发罚项保证 UAV 留有足速能量飞抵终点，复杂度更低。
- 求解结构：问题拆为功率与辅助变量、3D 轨迹、调度三类子问题，分别用 SCA、线性规划与精确罚函数处理，交替迭代。
- 关键洞察被证明：轨迹本身就是干扰管理工具，而不仅是覆盖或接入优化手段。
- 验证为 MATLAB R2022a + CVX 数值仿真（ITU 建筑统计模型），报告了在线求解运行时间，具备一定工程可行性证据。

## 比赛映射要点

- 数模优化题：多变量耦合连续优化（轨迹+功率+调度）的「分解-交替-凸近似」求解流程与 MATLAB/CVX 实现路径可整体迁移；max-min 公平目标在资源公平分配题中直接可用。
- 黑客松/算法赛：多机通信/充电/带宽分配赛题可借用「能量触发罚项 + 终点可行性」约束处理技巧与干扰感知建模视角。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhan2024_能量约束蜂窝连接多UAV的干扰感知在线优化`（4 枚举字段承自页 frontmatter）。
- bib 回填：citekey `zhan2024InterferenceawareOnlineOptimization` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性 medium 承自 vault 页自评：平台与硬件披露较全但无开源代码说明，如需引用请以原文复核。
