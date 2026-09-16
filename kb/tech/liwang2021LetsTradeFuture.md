---
id: liwang2021LetsTradeFuture
name: CoDetect：隐私保护的UAV群协同异常检测
field: [协同异常检测, 隐私保护, 无人机集群安全]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: Science China Information Sciences
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 无人机集群可信自治的安全底座——Merkle 密钥链成员认证、自证/挑战/裁决的共识式协同异常检测与隐私保护三件套，支撑智慧农业集群管控与数据安全申报章节，且有 Pixhack V3+树莓派实机与 ALFA 公开数据集实验背书
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: 异常检测模型可用公开 ALFA 数据集（飞控故障 FDI/AD）复现，self-prove/challenge/commit 共识裁决流程可原型化为群内拜占庭节点识别 demo，对比 Tendermint/EPBFT 有现成基线
    reuse_cost: 中
sources:
  - paper_title: "CoDetect: Cooperative Anomaly Detection with Privacy Protection towards UAV Swarm"
    doi: 10.1007/s11432-023-3984-7
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# CoDetect：隐私保护的UAV群协同异常检测

## 单行摘要

面向远离地面站的 UAV 群自治安全问题，提出 CoDetect 框架，把三件事统一起来：注册阶段用 Merkle 树密钥链做远程成员认证（不依赖 GCS 实时参与）、任务中用自证/挑战/裁决的共识式协同流程识别与处置 Byzantine 异常节点、全程用多叉 Merkle 树组织带时间戳的飞行日志块以同时支撑完整性验证与隐私保护——异常检测从单点判别升级为群内轻量自治安全流程。

## 方法快照

- 成员认证：GCS 注册时为每个 UAV 分配身份与取自 Merkle 树的密钥链，任意节点可在远离 GCS 时验证他人身份合法性并保持匿名。
- 个体自检测：用 GCS 已认证 UAV 的飞行数据训练异常检测模型，节点自行判别硬件/系统异常，异常者按临时退出协议离群。
- 共识式协同裁决：对隐瞒异常的恶意节点走 inquiry → self-prove → challenge → commit 四段流程，群体计算证据达成共识后施罚；共识效率较 Tendermint/EPBFT 复现对比有约 40% 改进（同超时/迭代/节点比例/规模）。
- 隐私保护：传感器数据按时间戳组织成多叉 Merkle 树，篡改反馈到协同检测框架处理，覆盖外部窃听与内部恶意节点。
- 验证：simulation + prototype + emulation 混合；ALFA 公开数据集（飞控故障 FDI/AD）+ 真实 UAV 自采数据（Pixhack V3 飞控、UBLOX NEO-M8N GPS、树莓派 4B 经 MAVLink 采姿态角，16000 采样点检测 drift/step 两类故障）；HLPSL 做认证协议安全分析。

## 比赛映射要点

- 黑客松/算法赛：ALFA 数据集公开可得，异常检测模型可直接复现；四段共识裁决流程适合做拜占庭节点识别类原型，且 Tendermint/EPBFT 对照基线现成。
- 双创申报：智慧农业集群的「可信自治」叙事底座——成员准入、异常处置与数据隐私一体化的安全方案，实机与公开数据集双背书增强材料可信度。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Li2024_CoDetect隐私保护的UAV群协同异常检测`（4 枚举字段自该页 frontmatter 迁移）。
- citekey 错配（W1 协议处理）：分片 citekey `liwang2021LetsTradeFuture` 在 bib map 中对应另一篇论文（JSAC 2021 期货式资源交易机制），与页内容明显不符；经查该页 sources 指向的 raw/markdown 原文核对，实为 Li Teng 等（Xidian University）的 CoDetect 论文（Science China Information Sciences, 2024）。改按 bib map 中正确条目 `li2024CoDetectCooperativeAnomaly` 回填标题/venue/DOI/published；卡 id 与文件名仍保留分片 citekey 作为去重键。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 simulation+prototype+emulation 混合验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
