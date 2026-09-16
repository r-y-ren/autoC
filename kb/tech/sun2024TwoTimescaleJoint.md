---
id: sun2024TwoTimescaleJoint
name: TJCCT 双时间尺度无人机辅助MEC联合优化
field: [UAV 辅助 MEC, 双时间尺度优化, 匹配与定价]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE INFOCOM 2024 - IEEE Conference on Computer Communications
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 「快时间尺度价格激励资源分配 + 匹配式任务卸载，慢时间尺度凸优化轨迹控制」的双环解耦框架，是资源分配-激励机制-选址路径耦合类数模题的方法编排模板，三工具分工各有的放矢
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 定价机制显式写入供需反馈 + 稳定匹配决定卸载去向，两者实现成本都低，可快速搭出多服务器任务分配 demo
    reuse_cost: 低
  - track: 双创-文书与申报
    edge: 空地协同算力服务网络（MBS + 多 UAV 服务器）方案叙事，兼顾 QoE、能耗与截止期的效用设计可支撑低空经济类项目书
    reuse_cost: 低
sources:
  - paper_title: "A Two Time-Scale Joint Optimization Approach for UAV-assisted MEC"
    doi: 10.1109/INFOCOM52122.2024.10621095
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# TJCCT 双时间尺度无人机辅助MEC联合优化

## 单行摘要

面向地空协同的 UAV 辅助 MEC 网络，处理计算资源分配、任务卸载与 UAV 轨迹控制的跨层联合优化：用户移动与任务到达在快时间尺度变化，而轨迹调整与全局资源组织适合慢时间尺度处理。TJCCT 据此解耦——短时间尺度用价格激励分配 MEC 服务器计算资源（反映供需）并以匹配机制决定移动设备任务卸载去向，长时间尺度用凸优化更新 UAV 轨迹以适配全局负载，把快变业务响应与慢变飞行控制分开治理，兼顾时延、效用与能量约束。

## 方法快照

- 系统实体：移动设备（任务带大小/计算强度/截止期）、一座 MBS、四架 UAV MEC 服务器。
- 快时间尺度内环：价格激励资源分配（预算约束下的供需定价）+ 匹配式卸载（任务与服务器稳定匹配）。
- 慢时间尺度外环：每个较长控制周期用凸优化更新 UAV 轨迹，适配负载分布。
- 效用设计：综合 MD 与服务器两侧收益、QoE 与成本，而非单纯时延最小化。
- 方法论定位：把价格、匹配、凸优化三类工具按时间尺度分工编排，替代把全部变量塞给单一求解器。
- 验证：数值仿真（合成场景），未披露代码，复现性 medium。

## 比赛映射要点

- 数模：资源分配 + 激励 + 调度耦合类题（如共享算力/充电桩/无人机服务网络）可直接套「双时间尺度双环」叙事：内环定价+匹配、外环选址/轨迹，求解复杂度论证现成。
- 黑客松：拍卖/定价 + 稳定匹配组件实现成本低，适合快速原型多服务器任务分配系统。
- 双创申报：空地协同边缘算力、低空服务网络的系统架构图与效用-成本模型可直接迁移。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Sun2024_TJCCT双时间尺度UAV辅助MEC联合优化`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `sun2024TwoTimescaleJoint` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16；venue 为 INFOCOM 2024 会议）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、无代码资产披露）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
