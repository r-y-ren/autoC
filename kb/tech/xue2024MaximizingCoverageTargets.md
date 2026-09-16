---
id: xue2024MaximizingCoverageTargets
name: MaxCov：WRSN 多充电器目标覆盖最大化调度
field: [无线可充电传感网, 充电调度, 目标覆盖]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: supporting
paper_role: supporting
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 覆盖优先级与补能调度的双层目标建模（目标覆盖不等于节点存活）适配传感网/设施维护类赛题，请求池-优先级-匹配的求解链路可直接复用
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: NP-hard 证明与请求分组（MaxCov-RG）在性能与实时性之间折中的思路，可用于多智能体任务分配题并在答辩时给出复杂度论证
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 农业物联网传感节点的无线补能维护方案支撑点——多充电主体协同保关键监测目标在线，替代单节点寿命最大化的粗放维护逻辑
    reuse_cost: 低
sources:
  - paper_title: "Towards Maximizing Coverage of Targets for WRSNs by Multiple Chargers Scheduling"
    doi: 10.1109/TMC.2024.3369054
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# MaxCov：WRSN 多充电器目标覆盖最大化调度

## 单行摘要

在多移动充电器 WRSN 的按需充电架构中，把"目标覆盖率（CoT）"而非"节点存活率"作为首要目标，提出 MaxCov（请求池-优先级-匹配）与 MaxCov-RG（请求分组协同）联合优化平均覆盖与能效。

## 方法快照

- 系统结构：静态可充电传感器 + 多个移动充电器 + 多基站；节点电量动态变化导致其不断离开或回到工作状态，网络拓扑持续演化。
- 目标重定义：CoT 是主评价指标，节点生存率降为支撑指标——"谁先被充电"直接改变目标覆盖质量而不只是设备寿命，这是与传充电调度研究的核心区别。
- MaxCov：构建充电请求池，按风险-收益比与路径成本计算请求优先级并做匹配，直接以目标覆盖为优化对象。
- MaxCov-RG：对请求分组后在组级别求解，在性能与实时性之间折中，降低计算复杂度并提升多充电器协同效率；问题被证明 NP-hard，并借助 M/M/n 与多个 M/M/1 队列对比论证多充电器协同优势。
- 验证：合成 WRSN 网络的数值仿真；平均覆盖率、覆盖率曲线、能效与节点生存率均优于对比基线；实现平台与开源情况未披露。

## 比赛映射要点

- 数模（数据分析与决策）：传感网维护、设施巡检类赛题中，"关键目标是否被持续覆盖"比"设备存活"更贴题的目标函数写法可直接借鉴；请求池化 + 优先级 + 匹配的三步求解链路是现成模板。
- 黑客松（数据与算法）：分组降复杂度的工程折中思路适用于多智能体任务分配题；NP-hard 归约与队列论对比分析可作为算法设计的论证素材。
- 双创（文书与申报）：农业物联网（土壤/气象传感节点）无线补能运维方案的技术支撑——多充电车或无人机协同充电，以保关键监测目标在线为优先承诺。

## 关联概念
- 无线可充电传感器网络（WRSN）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Xue2024_面向WRSN目标覆盖最大化的多充电器调度`（frontmatter venue_tier/evidence_tier/paper_role/reproducibility_level 已映射到本卡 4 枚举字段；该页为跨域参考——非 UAV-MEC 本体，但为"覆盖优先级 + 补能调度"提供建模参考）。
- bib 回填：citekey `xue2024MaximizingCoverageTargets` → 标题/venue/DOI 来自 vault 自带 Zotero bib（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；验证类信息（simulation、synthetic 数据、复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
