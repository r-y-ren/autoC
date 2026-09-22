---
id: arxiv-2609.21666
name: "Samsone：99M/134M/356M 三档开源小型音频语言模型（Interspeech 2026，checkpoint 可下载 + ExecuTorch 移动端 + Android 应用）"
field: [on-device inference, 音频理解, audio language model]
directions: [黑客松与数据竞赛]
published: "2026-09-18"
maturity: demo
venue_tier: CCF-C
reproducibility_level: high
signal:
  venue: "Interspeech 2026（arXiv Comments 注明录用；官方代码仓 SamsungLabs/samsone）"
  stars: 10
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "离线/隐私音频交互 demo 的现成引擎：134M 级模型服务端 uv sync 一条命令即用（checkpoint 首次调用自动从 GitHub Release 下载），且附 ExecuTorch 移动端 checkpoint 与 Android 应用代码——可做真机断网演示，相对『调 GPT-4o/Whisper API』的队伍形成离线可用+零 API 账单+音频不出设备三维硬差异，适配无网环境赛题（野外/应急/可穿戴/现场交互）与音频 caption/跨片段对比问答类交互"
    reuse_cost: 低
    open_source: "https://github.com/SamsungLabs/samsone（注意仓库本身无 LICENSE 文件，商用前需确认授权）"
sources:
  - url: https://arxiv.org/abs/2609.21666
    title: "Samsone: A Family of Open Small Audio Language Models for On-Device Inference（arXiv abs 页，v1 2026-09-18，Comments: Accepted for Interspeech 2026）"
    accessed: "2026-09-22"
  - url: https://github.com/SamsungLabs/samsone
    title: "SamsungLabs/samsone 官方仓（README：三档 checkpoint 释出清单/uv 安装/CLI 示例/Android 应用；API 元数据：10 stars/Python/2026-09-18 推送/license null）"
    accessed: "2026-09-22"
---

# Samsone：面向端侧推理的三档开源小型音频语言模型（Interspeech 2026）

> 来源：https://arxiv.org/abs/2609.21666 （v1 2026-09-18，eess.AS/cs.AI，作者 Piotr Masztalski、Michał K. Grzeszczyk、Olaf Sikorski，abs 页未列单位；Comments 注明 Interspeech 2026 录用，论文 CC BY 4.0）与官方代码仓 https://github.com/SamsungLabs/samsone （API 实查 2026-09-22：2026-02-06 创建、2026-09-18 推送、10 stars/2 forks、Python、无 LICENSE 文件）。本卡内容出自本次抓取的摘要页与官方仓 README。

## 是什么

Interspeech 2026 录用的小型音频语言模型（SALM）家族，官方仓挂 SamsungLabs 组织，三档规模：**Samsone-99M / 134M / 356M**。摘要口径：核心模型 Samsone-134M 自称在其 size class 多个基准上 SOTA，性能与更大的模型有竞争力；全程只用公开数据训练。释出物齐全（README 实抓）：三档服务端 PyTorch checkpoint（Python API 首次调用自动从 GitHub Release 下载到 `~/.cache/samsone`）、移动端 ExecuTorch checkpoint、训练/评测/导出代码与开源 Android 应用。用法：`uv sync` 安装后直接 `Samsone134M()(audio=..., prompt=...)`，每档模型一个 CLI 命令（如 `uv run samsone134M --audio a.wav b.wav --prompt "compare audio files"`）；支持单片段或多片段（多 clip 拼一次回答）。README 示例展示音频 caption 与跨片段对比问答（区分牛叫与水声的声学性质描述），并挂 MMAU 基准性能对比图。

## 解决什么问题

大型音频语言模型动辄数十亿参数，无法在手机/边缘设备执行；隐私保护与低延迟需求把注意力推向可端侧运行的 SALM。Samsone 提供"小而可用"的三档规模，并罕见地打通了**训 → 评 → 导出 → 移动端应用**的完整开源链，而不是只放权重。

## 相比前方法优势

- 相比闭源 API 音频理解（GPT-4o-audio、Gemini 等）：本地可跑、可离线、零边际调用成本、音频数据不出设备；
- 相比多数只放权重的开源 SALM：三档 size class 齐全便于按设备算力选型，且附 ExecuTorch 导出与 Android demo 应用——端侧部署路径现成，这是多数学术释出缺的一环；
- 相同 size class 内以公开数据训练（摘要口径），数据合规审计比爬数据训练的竞品友好。

## 局限（如实标注）

- **仓库无 LICENSE 文件**（2026-09-22 API 实查 license: null）：论文 CC BY 4.0 不等于代码授权，"open"口径与代码授权状态不一致，商用/二改前需向作者确认；
- 10 stars/2 forks，社区检验少（发布仅数日）；
- 摘要未给具体基准数值，"SOTA for its size class"与"competitive with much larger models"均为作者口径，MMAU 具体数字需读论文核实；134M 级与数十亿参数大模型存在代差，复杂音频推理不可期待；
- 能力范围是音频 caption / 音频问答级任务，摘要未宣称全谱 ASR/对话能力，选型前需按自己赛题实测；
- 仓内含 .gitmodules，从源完整复现训练需一并拉取子模块，训练复现成本高于推理复现。

## 如何用于比赛

**黑客松（数据与算法）**：无网/离线/隐私敏感赛题（野外作业、应急响应、医疗/车载等音频不出设备场景）的音频理解引擎。落地两档：服务端 demo 成本最低（uv sync + checkpoint 自动下载，CPU 可跑小档）；加分演示是 Android 真机断网端侧推理（官方 ExecuTorch checkpoint + 应用代码）。相对调用闭源 API 的队伍，差异化叙事是"离线可用 + 零 API 成本 + 隐私合规"三件套；也可作为 size class 对照基线引用其 MMAU 图说明选型理由。reuse_cost 低（推理侧），商用前先解决 LICENSE 确认。
