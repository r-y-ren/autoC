---
id: nguyen2024DilemmaReliabilitySecurity
name: UAV能量采集中继的可靠性-安全性双目标优化
field: [UAV 通信, 物理层安全, 多目标优化]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Journal on Selected Areas in Communications
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 把"可靠性 vs 安全性"写成可解析的双目标规划并给出 OP/IP 闭式近似，再用 NSGA-II 搜 Pareto 前沿——这套"双目标冲突建模 + NSGA-II 折中"模板可直接迁移到任何存在两个此消彼长指标的评估决策赛题
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: NSGA-II 是现成可插拔组件（pymoo 等库即用），适合算法赛里出现多目标权衡（成本 vs 覆盖、精度 vs 召回）时快速搭出 Pareto 分析亮点
    reuse_cost: 低
  - track: 双创-文书与申报
    edge: 智慧农业无人机中继/能量采集通信方案的技术支撑点——"提升链路可靠性的同时正面管理窃听暴露面"可写成低空农业网络的可靠安全协同设计叙事
    reuse_cost: 低
sources:
  - paper_title: On the Dilemma of Reliability or Security in Unmanned Aerial Vehicle Communications Assisted by Energy Harvesting Relaying
    doi: 10.1109/JSAC.2023.3322756
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# UAV能量采集中继的可靠性-安全性双目标优化

## 单行摘要

针对 power beacon 供能的中继辅助 UAV-地面通信系统，推导中断概率（OP，可靠性）与截获概率（IP，安全性）的精确/闭式近似表达式，证明能量采集、友好干扰与双跳中继会同时作用于主链路与窃听链路、两指标存在结构性冲突，进而以 UAV 位置与时间切换比（TS ratio）为决策变量构造双目标优化问题（MOOP），用 NSGA-II 搜索 Pareto 折中解——同时压低 OP 与 IP，而非只优化单一指标。

## 方法快照

- 三阶段链路建模：阶段一能量采集；阶段二 UAV→中继传输（窃听者尝试截获）；阶段三中继转发、power beacon 持续发射人工噪声压制窃听。
- 解析分析：OP 与 IP 的精确表达式 + 闭式近似，显式刻画 EH、人工噪声与双跳中继对主/窃链路的共同影响。
- 双目标优化：联合最小化 OP 与 IP；决策变量为 UAV 空间位置与 TS 比。
- 求解：NSGA-II 搜索次优 Pareto 前沿，输出"可靠性-安全性"折中曲线供系统设计取舍。

## 比赛映射要点

- 数模评估/决策题：任何"两个指标互斥"的赛题（可靠性 vs 风险、成本 vs 覆盖）都可套用"指标闭式/仿真建模 → 双目标规划 → NSGA-II 出 Pareto 前沿 → 前沿上做方案选择"的完整论证链，比单目标加权更有说服力。
- 黑客松算法题：NSGA-II 组件即插即用，多目标权衡场景可快速落地并可视化 Pareto 前沿作为演示亮点。
- 双创申报：智慧农业低空网络（植保/巡检无人机中继）的通信方案叙事——可靠性提升不能以安全裸奔为代价，本文提供量化权衡依据。

## 关联概念
- 可靠性-安全性权衡

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Nguyen2024_可靠性与安全性的两难协同`（frontmatter venue_tier/evidence_tier/paper_role/reproducibility_level 已映射到本卡 4 枚举字段）。
- bib 回填：citekey `nguyen2024DilemmaReliabilitySecurity` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；验证类信息（theory+simulation、synthetic 场景、复现性 medium、无开源）承自 vault 页自评，如需引用请以论文原文复核。
