---
id: wan2025MultimodalScaleNormalization
name: 视觉雷达融合UAV定位尺度归一化
field: [多模态感知, 无人机定位, 小目标检测]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 距离感知图像切片 + 跨模态尺度归一化是可直接移植的预处理组件——小目标检测 / 多传感器融合类数据赛题（150m 到 1300m 尺度剧烈变化）中，比单纯换检测器更能稳住远距离定位精度，训练栈为开源的 MMDetection + YOLOv5
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空经济热点的「低空无人机探测定位」方案技术支撑点（相控阵雷达 + 可见光融合的实测系统与自建数据集，CCF-A 实测验证），适配安防巡护、农情空域监测类项目申报
    reuse_cost: 低
sources:
  - paper_title: "A Multimodal Scale Normalization Framework for Vision-Radar Small UAV Positioning"
    doi: 10.1109/TMC.2025.3549620
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 视觉雷达融合UAV定位尺度归一化

## 单行摘要

面向远距离小型 UAV 精确定位，提出视觉-雷达多模态尺度归一化框架：把「目标越远视觉尺度越小、雷达与视觉表征存在模态差异」建模为跨模态尺度漂移问题，先按目标距离自适应切分图像以保住远距小目标可分辨区域，再对视觉与雷达分支分别做尺度归一化，最后经模态融合网络联合定位——在 150m 至 1300m 尺度剧烈变化的实测平台上显著提升小目标定位稳定性。

## 方法快照

- 感知配置：相控阵雷达 + 海康威视 DS-2DC4223IW-D 可见光摄像头 + 旋转台，单 GPU 工作站训练。
- 第一步 距离感知切片：按目标距离自适应切分图像，避免远距离小目标被背景淹没。
- 第二步 多模态尺度归一化：视觉与雷达表征在不同观测距离下对齐尺度，削弱跨模态尺度漂移。
- 第三步 融合定位：归一化后特征经模态融合网络联合输出检测与定位（训练栈 MMDetection、YOLOv5）。
- 验证：field_test 实测 + 自建视觉-雷达定位数据集；数据集与训练代码未公开。

## 比赛映射要点

- 黑客松/数据赛：小目标检测、多模态融合类赛题中「尺度归一化 + 距离感知切片」是低侵入预处理组件，可叠加在任意检测器（YOLO 系）之上做消融对比，形成差异化点。
- 双创申报：低空经济 / 无人机反制 / 农情空域监测类项目的技术方案背书——CCF-A 级实测系统证明「雷达 + 视觉融合探测小型 UAV」工程可行。

## 关联概念
- 视觉雷达融合定位

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wan2025_视觉雷达融合的小型UAV定位尺度归一化框架`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `wan2025MultimodalScaleNormalization` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 与 field_test/自采数据验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
