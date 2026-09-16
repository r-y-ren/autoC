---
id: li2025CooperativeNonorthogonalMultiple
name: 空地多UAV索引调制协作NOMA（MCU/MCCU-NOMA-IM）
field: [空地通信, 索引调制, 协作 NOMA]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 创新创业大赛]
venue_tier: unknown
evidence_tier: core
paper_role: anchor
reproducibility_level: low
signal:
  venue: IEEE Journal on Selected Areas in Communications
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 比特到调制符号/子载波激活模式/能量分配模式多维映射的组合编码设计，加分簇并行把协作时隙从随节点数线性增长压到 J+1，可迁移到带宽/时隙受限的多节点协作调度类赛题
    reuse_cost: 高
  - track: 双创-文书与申报
    edge: 农田多无人机数据回传频谱受限场景的低干扰高可靠链路方案亮点叙事（远端 UAV 可靠性 + 无需传统 SIC 的差异化卖点）
    reuse_cost: 低
sources:
  - paper_title: "Cooperative Non-Orthogonal Multiple Access with Index Modulation for Air-Ground Multi-UAV Networks"
    doi: 10.1109/JSAC.2024.3460050
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 空地多UAV索引调制协作NOMA（MCU/MCCU-NOMA-IM）

## 单行摘要

面向地面站与多 UAV 的空地网络，提出 MCU-NOMA-IM 及分簇增强版 MCCU-NOMA-IM：把不同 UAV 的比特分散映射到调制符号、子载波激活模式（SAP）与能量分配模式（EAP）多个独立维度，使各 UAV 信息无需传统 SIC 即可区分恢复，缓解多 UAV 场景的用户间干扰与 SIC 误差地板；近端 UAV 在合作阶段为远端 UAV 转发辅助信息，并推导了三/四 UAV 场景的 BER 上界。

## 方法快照

- 传输结构：广播阶段（地面站发 OFDM-IM 多维索引向量）+ 多时隙合作阶段（近端 UAV 重构辅助向量转发远端）。
- 多维索引调制：信息承载维度从 PSK/QAM 符号扩展到 SAP 与 EAP，用维度区分不同 UAV 数据，规避强干扰与 SIC 依赖。
- 检测流程：近端 UAV 先 ML 检测恢复索引与符号，再按已恢复信息生成合作向量辅助远端检测；远端 BER 由直达链路 + 合作链路共同决定。
- 分簇增强 MCCU-NOMA-IM：UAV 数量大时把距离相近者聚簇，J+1 时隙替代线性增长的合作时隙，压端到端时延。
- 理论分析：三/四 UAV 场景 BER 上界推导，Nakagami-m 信道、准静态 UAV 假设，数值仿真验证理论-仿真匹配。
- 验证：理论 + 数值仿真（合成场景），对比 MCU-NOMA 与 NC-MU-NOMA-IM，无实现栈与代码资产。

## 比赛映射要点

- 黑客松/算法赛：索引调制的「用激活模式本身携带信息」是组合编码思想的通用范本；分簇并行压缩协作时隙的机制可迁移到带宽/时隙受限的多节点任务协作与批处理调度类题。
- 双创申报：智慧农业低空网络（多机同时回传农田数据）频谱受限场景的通信方案亮点；注意复现成本高（物理层方案，reproducibility low），宜作叙事支撑而非实现组件。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Li2025_空地多UAV网络中基于索引调制的协作NOMA`（4 枚举字段自 vault 页 frontmatter 迁移）。
- venue_tier 说明：vault 页自评 Unknown，按跑批规则映射为 unknown；bib 回填 venue 为 IEEE JSAC，供后续 deep-sync 复核升级。
- bib 回填：citekey `li2025CooperativeNonorthogonalMultiple` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（low，理论推导完整但纯数值验证、无代码资产）；signal.runnable 如实标 false。
