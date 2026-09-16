---
id: zhou2025LLMQLLLMenhancedQlearning
name: LLM-QL：LLM增强Q学习的多无人机并行调度
field: [大语言模型, 强化学习, 无人机调度]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Knowledge and Data Engineering
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: LLM 出启发式、Q-learning 出决策的架构规避了 LLM 直接求解组合优化的不稳定——prompt 化问题建模 + 启发式引导探索 + 幻觉扰动鲁棒性分析（页内记录 ChatGPT-4o）是调度/路径类赛题的即插即用加速组件
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 卡车-多无人机协同配送 mFSTSP 是数模常见题型，LLM 启发式引导 + RL 奖励修正的求解管线可作超越纯启发式/纯 RL 基线的差异化方案；Seattle 真实城市数据 + 合成 mFSTP 数据的双轨评测设计可参照
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 农产品/农资无人机配送调度的智能化叙事支撑——"LLM 赋能组合优化"作为申报书技术亮点的当前热点表述
    reuse_cost: 低
sources:
  - paper_title: "LLM-QL：A LLM-enhanced Q-learning Approach for Scheduling Multiple Parallel Drones"
    doi: 10.1109/TKDE.2025.3579386
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# LLM-QL：LLM增强Q学习的多无人机并行调度

## 单行摘要

面向卡车-多无人机协同配送的 mFSTSP 问题（卡车负责携带、回收与补能无人机，目标最小化总完成时间），提出 LLM-QL：把问题约束与状态组织成 prompt 喂给 LLM 生成启发式项，用于缩小 Q-learning 的无效探索区域，再由奖励驱动持续修正策略——在大规模调度环境中提升总完成时间、运行时间与 UAV 利用率。

## 方法快照

- 核心定位：LLM 不直接输出调度，而是充当强化学习前端的启发式生成器——既利用 LLM 的全局语义组织能力，又保留 RL 长期迭代纠错的稳定性。
- 管线四步：mFSTSP 状态/约束/目标 prompt 化 → LLM 生成启发式项或中间变量缩小探索区域 → Q-learning 依靠奖励学习修正启发式偏差 → 分析启发式幻觉带来的扰动并验证系统可在有限时间内重新收敛。
- 评测：Seattle city dataset（trace-driven）+ 合成 mFSTSP 数据集双轨；指标为总完成时间、运行时间、UAV 利用率与鲁棒性；页内记录使用 ChatGPT-4o（复现 medium）。
- 缺口：完整代码与调用设置未给出，仅明确了 LLM 版本。

## 比赛映射要点

- 算法赛：LLM 辅助探索的架构可直接迁移到 VRP/调度/组合优化类题目，幻觉鲁棒性分析降低落地风险。
- 数模赛：卡车-无人机配送题型匹配度高，LLM+RL 管线是相对纯启发式/纯 RL 的差异化求解方案。
- 双创申报：物流/配送智能化技术亮点素材。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhou2025_LLM增强Q学习的多并行无人机调度`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `zhou2025LLMQLLLMenhancedQlearning` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）；bib 标题含 ASCII 冒号（LLM-QL 后），已改全角写入 paper_title 并在此留痕。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真 + trace 驱动验证、完整代码未给出）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
