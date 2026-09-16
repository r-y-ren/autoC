---
id: guo2024JointOptimizationTrajectory
name: 多UAV主动窃听的干扰功率与轨迹联合优化
field: [物理层安全, 协同干扰, 强化学习]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 「内层逐状态解析最优功率 + 外层 RL 学轨迹、并证明解耦不损整体最优性」是处理连续耦合决策的通用套路，可迁移到分配+时序机动类复合算法题
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: MDP 序贯决策建模 + 内层凸/解析求解的组合是「资源投放+机动决策」类赛题的可复用求解模板，且自带最优性论证便于论文写作
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 植保无人机数据链安全申报的威胁模型素材：论文站在合法监视方，反窃听/抗干扰的防御论证可反向引用其干扰-轨迹耦合结论
    reuse_cost: 中
sources:
  - paper_title: "Joint Optimization of Trajectory and Jamming Power for Multiple UAV-Aided Proactive Eavesdropping"
    doi: 10.1109/TMC.2023.3311484
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 多UAV主动窃听的干扰功率与轨迹联合优化

## 单行摘要

面向合法监视方借助多 UAV 监听多条可疑通信链路的主动窃听问题，将其建模为 MDP 并采用两阶段解耦：每个状态先用非学习方法解析求最优干扰功率（压制可疑链路容量），再用强化学习只优化窃听 UAV 的飞行轨迹（增强监听信道），并证明该解耦不破坏整体最优性——降低学习难度的同时保留最优性分析。

## 方法快照

- 场景结构：协同干扰 UAV 发射干扰压制可疑链路，窃听 UAV 靠机动提升监听质量；「安全」站在监视者一侧而非通信者一侧，多链路多机协同。
- 建模：动态链路状态下的时序决策，自然适配 MDP；端到端 RL 直接学习满足监视约束的干扰功率较困难。
- 两阶段解耦：内层逐状态解析最优干扰功率分配；外层在固定功率最优响应下用 RL 学习飞行轨迹动作（编队安全距离约束内）。
- 求解与验证：TensorFlow + CVX，数值仿真为主，开源未说明。

## 比赛映射要点

- 黑客松：解耦范式（能闭式解的子问题不进学习器、RL 只学剩余动作、附最优性论证）可直接搬到「连续资源投放+离散/时序机动」的复合算法题，比端到端 RL 更稳更可解释。
- 数模：同样的两阶段结构适合「干扰资源分配+无人机调度」式决策优化赛题，内层解析解+外层学习/搜索的组合在论文里容易讲清机理。
- 双创申报：农业无人机数据链安全章节可将其作为威胁模型与对抗基线引用（站在攻击/监听视角推防御需求），素材稀缺、辨识度高。

## 溯源说明

- 提炼来源：my_LLM_valut wiki 页 `Guo2024_多UAV辅助主动窃听的轨迹与干扰功率联合优化`；citekey `guo2024JointOptimizationTrajectory`。
- bib 回填：标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性 medium 承自 vault 页自评（TensorFlow/CVX 线索、数值仿真为主、开源未说明）；如需引用请以论文原文复核。
