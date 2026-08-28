---
id: arxiv-2608.24022
name: "What Guides the Agent? Adjudicating Unauthorized Behavior via Localizing Behavior-Guiding Instructions（AttnLocate）"
field: [LLM agents, agent 安全, 可解释性]
directions: [黑客松与数据竞赛]
published: "2026-08-25"
maturity: paper
signal:
  venue: "arXiv v1（cs.CR/cs.AI，页内无 venue/comments 标注）"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "agent 行为审计/注入取证赛题的方法论蓝本：不判'输入是否含恶意'，而是定位'哪段上下文实际引导了这次工具调用'——把行为归因变成注意力矩阵激活轨迹上的 1-D span 检测，再按片段提供方（provider）权限裁决调用是否越权。开源权重模型（Qwen/Llama 系）黑客松环境可实现；论文口径 mean IoU 0.743 / AUROC 0.956、跨未见模型迁移、换策略免重训，可直接当评测叙事骨架"
    reuse_cost: 高
    open_source: "无（arXiv 页未附仓库链接；2026-08-28 实抓确认）"
sources:
  - url: https://arxiv.org/abs/2608.24022
    title: "What Guides the Agent? Adjudicating Unauthorized Behavior via Localizing Behavior-Guiding Instructions"
    accessed: "2026-08-28"
---

# AttnLocate：用注意力定位行为引导指令来裁决 agent 越权行为

> 来源：https://arxiv.org/abs/2608.24022 （arXiv v1 提交于 2026-08-25 03:24:53 UTC，作者 Yichao Gao、Yumo Zhang、Yunhao Yao、Haohua Du、Puhan Luo、Ruiqi Li、Zhiqiang Wang，cs.CR/cs.AI；抓取日期 2026-08-28）

## 是什么

arXiv 2608.24022 提出运行时框架 **AttnLocate**——对 agent 上下文中"真正影响了工具调用决策"的片段做细粒度定位（以下均来自本次实抓的摘要页）：

- **问题重构**：把"定位行为引导指令"表述为注意力矩阵激活轨迹上的**目标检测问题**；多头多层注意力聚合出 token 级特征，用 **1-D U-Net + 免锚框检测头**输出影响 span；
- **裁决逻辑**：定位出 span 后，按各 span 的**提供方权限（authority of the span's provider）**裁决该次恶意调用——即"引导这次调用的是谁塞进来的内容"；
- **评测口径**：10 种 agent 配置 × 5 个 LLM 家族，覆盖间接提示注入与工具投毒（tool poisoning）；mean IoU 0.743，平均 AUROC 0.956，TPR 0.934 @ FPR 0.067；
- **迁移性**：对未见过的模型可迁移，安全策略变更无需重训。

## 解决什么问题

接外部资源的 LLM agent 里，不可信外部数据可能在推理时被动态解析为行为引导指令（注入攻击），颠覆 agent 决策；既有防御聚焦静态检测或隔离恶意内容，回答不了"这次可疑调用究竟被哪段上下文驱动"——事后审计与责任归因缺工具。

## 相比前方法优势

- **归因而非分类**：输出"哪段内容引导了行为 + 其提供方是否有权"，支持事后裁决与追责，而不只是入站内容的恶意二分类；
- **与策略解耦**：判定依据是提供方权限，改安全策略不用重训检测器；
- **跨模型泛化**：在未见模型上保持性能（论文口径），缓解逐模型重训成本；
- 指标体系完整（span 级 IoU + 裁决级 AUROC/TPR@FPR），评测口径可直接搬用。

## 局限

- **无公开实现**：arXiv 页无代码仓库（runnable=false），页内无 comments/venue，未过评审；
- **白盒门槛**：方法依赖模型内部注意力矩阵，API-only 模型（GPT/Claude 等）拿不到激活轨迹，只适用于可取内部信息的开源权重模型——这直接限定赛场技术选型；
- **训练成本**：1-D U-Net 检测器需要自建"激活轨迹 + 影响 span 标注"数据集训练，黑客松时限内完整复现不现实（reuse_cost=高）；演示级可行的是降级替代——注意力聚合/归因代理（如 rollout 类加权）+ 阈值切 span + 同一套提供方权限裁决；
- IoU 0.743 意味着 span 边界仍含误差，"0.743 的定位精度支撑权限裁决"在安全关键场景需谨慎表述。

## 如何用于比赛（比赛映射展开）

- **黑客松-数据与算法**：agent 安全/审计主题（注入取证、agent 行为合规审计）作品的方法论核心或对照基线：
  1. **完整路线**（赛后/长周期）：开源模型取注意力轨迹 → 训练 span 检测器 → 提供方权限裁决，评测用论文的 IoU/AUROC 双层口径；
  2. **周末降级路线**：注意力归因代理（多层均值/rollout 加权）定位高贡献片段 + 权限表裁决 + 调用拦截，保住"可归因、可审计"的差异化叙事；
- **演示亮点**：现场注入一段恶意指令，系统高亮"就是这段上下文引导了这次工具调用"并给出提供方权限结论——比黑盒拦截更有解释力的展示；
- **风险自担**：所有数字引用注明论文口径（铁律 4），自家实现的 IoU/AUROC 需自建小评测集实测。
