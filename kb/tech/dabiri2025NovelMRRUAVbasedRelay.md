---
id: dabiri2025NovelMRRUAVbasedRelay
name: MRR-UAV光网络编码双向中继
field: [自由空间光通信, UAV 中继, 网络编码]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: low
signal:
  venue: IEEE Journal on Selected Areas in Communications
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 无人机集群远距高带宽回传的技术选型论据——MRR 双向中继、AF/DF 中继与光学 IRS 三方案在角抖动、重量、功耗上的适用边界对比，可支撑低空经济/农业集群通信保障章节的方案论证与结论引用
    reuse_cost: 高
sources:
  - paper_title: "A Novel MRR-UAV-based Relay with Optical Network Coding: A Comparative Study with Optical IRS and Conventional UAV Relaying"
    doi: 10.1109/JSAC.2025.3543516
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# MRR-UAV光网络编码双向中继

## 单行摘要

面向 UAV 搭载自由空间光（FSO）中继时姿态抖动破坏光学对准的问题，提出基于 MRR（调制反射器）的双向中继拓扑：地面两端以双波长分别发送业务光与 interrogator 光，UAV 端透镜接收、探测后做 XOR 网络编码，再用单个 MRR 调制反射实现双向转发；并在统一误差模型下与 AF/DF 中继、光学 IRS 对比 BER、容量与实现复杂度，给出各自适用边界。

## 方法快照

- 问题定位：UAV 角抖动与指向误差是空中光链路的首要瓶颈；传统 AF/DF 功耗重量大，小型 IRS 对角度波动敏感。
- MRR 双向结构：大视场透镜接收 + 探测器得两路电信号 + XOR 检测 + 单 MRR 调制反射 interrogator 光，双向通信共享一个调制器。
- 性能分析：推导平均 BER 与容量闭式，讨论抖动、口径面积与功率分配下的性能交叉点。
- 复杂度对比：省去 AF/DF 的高功率放大与精密对准，避免小尺寸 IRS 的抖动脆弱性。
- 验证：数值仿真（合成参数），无公开代码与实验资产。

## 比赛映射要点

- 双创申报：本文是"论据型"支撑卡——申报书涉及无人机集群远距大带宽回传（低空经济、农业遥感数据回传）时，可直接引用其三方案对比结论做通信保障技术路线论证；硬件（MRR/透镜）专用性强，无可复用算法组件，勿在算法类赛题中引用。

## 关联概念
- 自由空间光通信（FSO）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Dabiri2025_MRR-UAV光网络编码中继与FSO对比研究`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `dabiri2025NovelMRRUAVbasedRelay` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 low 与 simulation/synthetic 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
