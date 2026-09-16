---
id: li2025DroneMADroneMobility
name: DroneMA：移动性一致性驱动的无人机AI欺骗检测
field: [无人机安全, 时间序列异常检测, 物理层鉴别]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE INFOCOM 2025 - IEEE Conference on Computer Communications
  runnable: false
competition_fit:
  - track: Kaggle-竞赛
    edge: Z-score 标准化→R2D-GRU 跨序列趋势预测→IQR 自适应阈值的仅正样本异常检测模板，直接适配时序异常检测类赛题（无需攻击/异常样本即可训练）
    reuse_cost: 低
  - track: 数模-预测与评估
    edge: 用「RSSI 预测距离趋势与真实距离序列的一致性」做数据可信性评估的范式，可迁移到传感器数据可信评估与数据质量判别类题
    reuse_cost: 低
  - track: 双创-文书与申报
    edge: 现成硬件（Pixhawk + Jetson Nano）实时反欺骗的低成本无人机安全方案支撑点，适配智慧农业无人机作业安全叙事
    reuse_cost: 低
sources:
  - paper_title: "DroneMA: Drone Mobility Alignment Countering AI-based Spoofing Attacks"
    doi: 10.1109/INFOCOM55648.2025.11044631
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# DroneMA：移动性一致性驱动的无人机AI欺骗检测

## 单行摘要

针对生成式 AI 驱动的物理层欺骗攻击，提出 DroneMA：利用合法 GCS 与攻击者相对无人机运动关系不同导致 RSSI 时序趋势不同的观察，把欺骗检测转化为「RSSI 推断距离趋势是否与真实运动一致」的序列异常检测问题——Z-score 标准化后用 R2D-GRU 从 RSSI 预测距离序列，再以 IQR 自适应阈值对预测与真实距离的相关性做异常判断，仅用正样本即可在现成飞控链路上实时运行。

## 方法快照

- 问题转化：传统 CSI/RF 指纹鉴别在机动、低资源无人机上不稳健且难敌 AI 伪造特征；DroneMA 改用通信（RSSI）与感知（GPS 距离）的跨模态一致性作安全锚点。
- 检测管线：滑动窗口采集 RSSI 与距离序列 → Z-score 消除漂移与增益噪声 → R2D-GRU 从标准化 RSSI 预测标准化距离 → 预测距离与真实距离的相关性 + IQR 自适应阈值判定异常。
- 关键设计：只依赖正样本的 one-class 检测（攻击样本难以穷举），轻量到可在机载端持续运行；连续异常触发返航/切换链路等应急动作。
- 验证：Pixhawk 6c mini + Jetson Nano + MAVLink 真实飞行数据，三类真实飞行情境平均准确率约 92.78%，未开源。

## 比赛映射要点

- Kaggle/数据竞赛：跨序列一致性预测 + IQR 阈值是即插即用的时序异常检测组件，不需要异常标签，特别适合异常样本稀缺的赛题；相比直接上分类器有「无监督 + 可解释」双重卖点。
- 数模评估题：「预测趋势 vs 实测趋势一致性」可迁移到传感器数据可信性/异常数据识别类题（如数据污染、设备故障检测）。
- 双创申报：低成本无人机安全防护方案（现成硬件、毫秒级实时、可解释检测依据）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Li2025_DroneMA基于移动性对齐的无人机AI欺骗检测`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `li2025DroneMADroneMobility` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，真实飞行验证、硬件清单齐全但未开源）；signal.runnable 如实标 false。
