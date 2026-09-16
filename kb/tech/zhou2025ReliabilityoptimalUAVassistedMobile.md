---
id: zhou2025ReliabilityoptimalUAVassistedMobile
name: 面向可靠性的UAV辅助MEC联合资源与运动优化
field: [UAV 辅助边缘计算, 无线可靠性建模]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 把任务成功率（LoS/NLoS 随机转移下的闭式可靠性表达式）而非平均速率设为优化目标，再用增广拉格朗日解非凸联合优化——数模赛题中"无人机辅助通信/卸载成功率最大化"类问题的差异化建模与求解模板
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 数据传输调度 + UAV 运动控制 + 带宽/功率分配的联合决策组件，可直接迁移到无人机应急通信、配送调度类赛题的算法层
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业田间数据回传的可靠性保障论据（空中 cloudlet 中继 + 可靠性优先设计），TMC 2025 文献背书用于申报书技术方案章节
    reuse_cost: 低
sources:
  - paper_title: Reliability-Optimal UAV-assisted Mobile Edge Computing：Joint Resource Allocation, Data Transmission Scheduling and Motion Control
    doi: 10.1109/TMC.2024.3521934
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 面向可靠性的UAV辅助MEC联合资源与运动优化

## 单行摘要

论文从随机建模角度重新定义 UAV-assisted MEC 的通信可靠性：A2G 链路会随 UAV 运动在 LoS/NLoS 之间随机切换，作者推导包含转移概率、数据装载、带宽、功率、计算时间与 UAV 运动状态的闭式可靠性表达式，并以系统可靠性最大化为目标，用增广拉格朗日法联合求解加速度控制、数据调度与带宽/功率/时间分配。

## 方法快照

- 建模视角：把"任务能否可靠卸载成功"（通信成功概率）作为系统级目标，替代平均速率/时延——指出固定 LoS 或固定 NLoS 假设都会高估稳定性。
- 可靠性表达式：LoS/NLoS 条件概率、数据分片量、带宽、功率、计算时间与 UAV 运动状态的闭式函数。
- 联合优化：决策变量覆盖 UAV 轨迹/加速度、用户数据调度、带宽、功率、时间分配；约束含截止期、运动学边界、能量自给。
- 求解：增广拉格朗日把强非凸问题转为序列无约束子问题迭代求解。
- 验证：MATLAB + SUMO，Bologna 城市真实交通流驱动移动性（比纯合成轨迹更接近部署），论文自报结果为仿真数据。

## 比赛映射要点

- 数模：随机信道下的"可靠性/成功率"目标函数写法是区别于常规吞吐量优化的加分建模点；增广拉格朗日是处理多约束非凸优化的经典可复用求解器。
- 黑客松：面向无人机应急通信/配送题，"调度+轨迹+资源"联合决策骨架可直接改造。
- 双创：智慧农业数据回传可信保障的技术支撑，引用门槛低（建模思路可整段迁移到申报书）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhou2025_可靠性最优的UAV辅助移动边缘计算`（venue_tier/evidence_tier/paper_role/reproducibility_level 自页 frontmatter 迁移）。
- bib 回填：citekey `zhou2025ReliabilityoptimalUAVassistedMobile` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）；bib 标题原文含 ASCII 冒号，frontmatter 按本跑批 YAML 约定改全角冒号写入，特此留痕。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation/trace_driven、复现性 medium、无开源说明）承自 vault 页自评，如需引用请以论文原文复核。
