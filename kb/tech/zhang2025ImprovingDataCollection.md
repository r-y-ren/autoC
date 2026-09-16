---
id: zhang2025ImprovingDataCollection
name: 定向性感知链路模型驱动的UAV-LoRa数据采集（annulus+PreLoRa）
field: [UAV 辅助数据采集, LoRa, 实测链路建模]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Networking
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: "农田 LoRa 传感 + 无人机巡田采集是智慧农业物联网的经典架构，'头顶数据采集空洞'的实测反直觉洞察（越近不一定越好）可直接转化为产品链路设计差异化点，全套硬件清单（SX1262/SX1301/RPi）可估成本"
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: "实测驱动的链路现象建模（环带模型）+ 预测驻留窗口的主动发送调度（SF/时段/包长切换 + SF backoff 抗冲突），适用于 LPWAN/低功耗广域数据采集类赛题，比通用距离感知自适应速率方案更有辨识度"
    reuse_cost: 中
sources:
  - paper_title: "Improving Data Collection Efficiency of UAV-assisted LoRa Networks via Directivity-Aware Link Model"
    doi: 10.1109/TON.2025.3559889
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 定向性感知链路模型驱动的UAV-LoRa数据采集（annulus+PreLoRa）

## 单行摘要

通过野外实测发现 UAV-LoRa 空地链路存在"头顶数据采集空洞"：收发天线主辐射方向失配导致 UAV 越靠近节点链路反而越差。据此提出 annulus model 把空地链路质量表示为与相对位置有关的环带结构，并设计 PreLoRa 机制——网关预测 UAV 在各配置区域的驻留时长，提前下发最优发送计划，节点主动在最佳窗口切换 SF/时段/包长上传，多节点场景叠加 SF backoff 缓解并发冲突，显著提升短驻留时间内的可靠上传量。

## 方法快照

- 核心发现：空地链路质量不随距离单调改善，定向性失配使"看起来最近、实际最差"的位置浪费上传机会——从"距离感知"升级到"定向性感知"。
- 链路模型：annulus model 将直向性损耗映射为空间环带，参数由网关持续更新的 RSS/SNR 估计在线维护。
- 协议设计：PreLoRa 基于模型预测未来 ping 周期的发送计划并下发；节点按预测飞行状态切换最优 SF、发送时段与包长；多节点用 SF backoff 抗冲突。
- 系统目标：短驻留窗口内的可靠上传总量最大化，而非单包成功率。
- 实验证据：prototype + field_test，自采数据，硬件链完整（STM32 Nucleo-64、Semtech SX1262 节点、Z410 UAV、Raspberry Pi 4B + SX1301 网关），工程证据层强；代码未开源。

## 比赛映射要点

- 黑客松/数据赛：LPWAN/无人机数据采集类题目可直接引用"定向性空洞"现象做系统设计论证；"预测窗口 + 主动调度配置"的思路可迁移到任何移动采集器 + 低功耗节点的场景。
- 双创申报：智慧农业物联网（农田传感 + 无人机巡田回收数据）是现成落地方向，实测背书与完整 BOM 清单支撑可行性与成本章节。

## 关联概念
- 定向性感知空地链路模型

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhang2025_基于定向性感知链路模型的UAV-LoRa高效数据采集`（4 枚举字段自 vault 页 frontmatter 迁移，reproducibility_level=medium）。
- bib 回填：citekey `zhang2025ImprovingDataCollection` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，硬件链路完整披露但无开源代码）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
