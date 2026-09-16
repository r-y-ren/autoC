---
id: tong2023EnergyefficientUAVNOMAAided
name: 能效优先的UAV-NOMA海量连接覆盖
field: [UAV 通信覆盖, NOMA, 能效优化]
published: 2023-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: Science China Information Sciences
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: Dinkelbach 处理能效分式目标 + BCD 在轨迹与功率间交替更新 + 地面预编码单独优化的三段套路，是「比值目标 + 多变量耦合」类数模题的标准工具箱，MATLAB+CVX 工具链披露完整
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 「覆盖增益与飞行能耗绑定设计」的联合优化建模可直接迁移到基站/设施部署与资源复用类赛题，NOMA 功率域复用思想可类比多租户资源共享
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 广域覆盖 + 海量连接（农业物联网/低空经济补点）的空地协同组网方案支撑点，UAV-BS 服务边缘、G-BS 服务中心的分层覆盖叙事清晰
    reuse_cost: 低
sources:
  - paper_title: "Energy-Efficient UAV-NOMA Aided Wireless Coverage with Massive Connections"
    doi: 10.1007/s11432-023-3821-3
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 能效优先的UAV-NOMA海量连接覆盖

## 单行摘要

把 UAV-BS + 地面基站（G-BS）+ NOMA 组合成面向海量连接的无线覆盖方案：UAV-BS 主攻小区边缘用户、G-BS 服务中心区域，NOMA 以功率域复用 + SIC 解码在相同资源块内支撑更多连接。优化目标是系统能效最大化（而非单纯速率），约束含 UAV 飞行动力学、用户平均吞吐与功率预算——用 Dinkelbach 方法处理分式目标，将问题拆为轨迹优化与功率分配两个凸子问题以 BCD 交替求解，并单独优化 G-BS 预编码以降低地面侧功耗，使 UAV 不只是空中补点，而是与地面网络联合组织的覆盖能力。

## 方法快照

- 架构：地面层（G-BS 中心覆盖 + 预编码）+ 空中层（UAV-BS 边缘增强）+ 多址层（NOMA 功率域复用）。
- 目标：能效最大化，约束飞行动力学、平均吞吐与功率预算；海量连接来自资源块复用而非加频谱。
- 求解：Dinkelbach（分式目标）→ 轨迹/功率两子问题 BCD 交替 → G-BS 预编码单独优化。
- 核心论点：NOMA+UAV 的价值在于把覆盖设计与能耗设计绑定，而非多连几个用户。
- 验证：MATLAB + CVX 数值仿真（合成蜂窝覆盖场景）；代码与仿真配置未披露，复现性 medium。

## 比赛映射要点

- 数模：通信/覆盖/资源类题中「能效 = 总速率 / 总能耗」的分式目标出现频率极高，Dinkelbach + 交替优化的写法可直接搬进论文求解章节，且能对比「不联合优化」基线论证收益。
- 黑客松：设施选址 + 服务分组 + 资源复用类题可复用「空中补点 + 地面主覆盖」的分层建模与能效导向评价。
- 双创申报：农业物联网广域覆盖、低空经济通信补点等组网方案的技术支撑点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Tong2023_面向海量连接的能效UAV-NOMA无线覆盖`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `tong2023EnergyefficientUAVNOMAAided` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2023），按 2023-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、工具链已披露但代码未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
