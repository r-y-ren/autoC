---
id: guo2025MightyLongrangeHighthroughput
name: Mighty：面向无人机的远距离高吞吐回散视频回传
field: [反向散射通信, 无人机系统, 跨层协同设计]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 植保/巡检无人机续航痛点（视频回传吃掉电池预算）的系统性解法：回散通信把机载发射与编码功耗卸载到地面，PCB 原型+DJI Mini2 实地对比在硬件类申报中差异化强
    reuse_cost: 高
  - track: 黑客松-数据与算法
    edge: 「机载轻、地面重」的跨层能耗卸载范式可迁移到低功耗边缘-云分工类系统题（弱算力端采集 + 地面端视频恢复/超分/插帧）
    reuse_cost: 高
sources:
  - paper_title: "Mighty: Towards Long-Range and High-Throughput Backscatter for Drones"
    doi: 10.1109/TMC.2024.3486993
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# Mighty：面向无人机的远距离高吞吐回散视频回传

## 单行摘要

Mighty 通过硬件-物理层-软件跨层协同，把无人机视频回传的机载功耗卸载到地面控制端：超低功耗环振回散无线电 + 频谱效率更高的非线性调制与多链路射频结构 + 绕过机载编码器的轻量视频链路（恢复/超分/插帧移到地面），在 PCB 原型上实现并经室内外实测（与 DJI Mini2 默认视频系统 head-to-head），展示低机载功耗下长距离高吞吐回传的可行性。

## 方法快照

- 硬件：超低功耗环振回散无线电，免除机载功放级发射负担。
- PHY：更高频谱效率的非线性调制 + 多链路射频架构，避免「低功耗换低吞吐」的常规回散短板。
- 软件：codec-bypassing 视频链路——机载只做轻量处理，视频恢复与智能增强全部移到地面端。
- 验证：PCB Mightyboard 原型 + 室内外 field study；对比 DJI Mini2 默认视频系统；证据含真实飞行测试，是本片中实测性最强的一篇。

## 比赛映射要点

- 双创申报：续航是植保/巡检无人机的核心痛点叙事，Mighty 给出「通信方式重塑视频流水线」的系统级答案；板级原型+实测数据在硬件类申报中比纯算法方案更具说服力，但涉及自定义射频硬件、复用成本高。
- 黑客松：能耗卸载范式（弱算力端只采不发、重处理放地面/云端）可迁移到低功耗物联网/边缘-云分工系统题，尤其视频类赛题。

## 溯源说明

- 提炼来源：my_LLM_valut wiki 页 `Guo2025_Mighty面向无人机的远距离高吞吐回散通信`；citekey `guo2025MightyLongrangeHighthroughput`。
- bib 回填：标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性 medium 承自 vault 页自评（板级原型+实测、MATLAB/PyTorch/DJI Mini2、开源未说明——自定义射频硬件本身抬高复用门槛）；如需引用请以论文原文复核。
