---
id: arxiv-2609.03923
name: "Speak for Me: Giving LLMs the Situational Awareness to Participate in a Meeting"
field: [LLM agents, 多智能体协作, 对话系统]
directions: [黑客松与数据竞赛]
published: "2026-09-03"
maturity: paper
signal:
  venue: "arXiv v1（2026-09-03 提交，cs.AI + cs.CL；Comments 标注 EMNLP 2026 Main 录用；摘要页无代码仓库链接）"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "meeting-assistant/协作工具类黑客松（devpost/MLH 常见赛道）的产品级架构与评测模板：'替缺席者参会'是评委秒懂的产品形态；CAPA 六模块（感知-预测-决策-生成-双裁判-重校准）全为 LLM API 编排层、零训练、单机可跑；EMNLP 2026 Main 录用是现成背书；其 episode 级 whether/when/what 评测协议 + 经人工校准的 LLM judge（Cohen's kappa=0.71）可直接搬作作品评测设计——解比赛作品'没有像样评测'的通病；消融结论'结构化会议状态是关闭识别缺口的关键杠杆、堆原始上下文无效'是现成答辩论点"
    reuse_cost: 低
sources:
  - url: https://arxiv.org/abs/2609.03923
    title: "Speak for Me: Giving LLMs the Situational Awareness to Participate in a Meeting"
    accessed: "2026-09-04"
---

# Speak for Me：让 LLM 拥有参与会议所需的态势感知

> 来源：https://arxiv.org/abs/2609.03923 （arXiv v1 提交于 2026-09-03，主分类 cs.AI 交叉 cs.CL，作者 Khan、Kirstein、Ruas、Gipp；Comments 字段标注 EMNLP 2026 Main 录用；摘要页未附代码链接）；抓取日期 2026-09-04

## 是什么

**在线会议委托**（online meeting delegation）场景的 agent 架构 CAPA（Collaborative Agent Predictive Architecture）：LLM agent 代表缺席者参会，核心难点是**识别何时该发言**（以下均来自本次抓取的摘要页）。架构六个模块构成闭环：

1. **Perceiver**：逐轮更新会议状态（结构化追踪立场 stance、覆盖 coverage、发言权 floor）；
2. **Predictor**：预测对话如何继续；
3. **Controller**：决定是否发言、呈现缺席者的哪个命题；
4. **Generator**：以参与者的风格措辞；
5. **两个 judge**：将预测与动作对照下一轮实测打分；
6. **Recalibrator**：依裁决更新会议状态。

## 解决什么问题

纯提示词（prompt-only）的委托 agent 在 AMI 语料上错失缺席者 **51.4%** 的发言机会——缺乏结构化方式追踪立场、议题覆盖与发言权，就识别不到该贡献的时刻。CAPA 用"感知-预测-行动-裁决-重校准"闭环把"何时说话"变成有状态可追踪的决策。

实测（137 场 AMI 会议，episode 级评测围绕缺席者真实"想法单元"评 whether/when/what）：沉默率 51.4% → **2.5%**；credited recovery 26.1 → **52.2**（翻倍）；幻觉率 **0.6%**；失败模式从**遗漏**转为**选择**。评测方法上，schema 约束的 LLM judge 与人工标注达 Cohen's kappa=0.71。消融显示：**结构化会议状态**是关闭"识别缺口"的关键杠杆，堆原始上下文无法弥合差距。

## 相比前方法优势

- **从"生成得好"转向"时机对"**：先行工作聚焦发言质量，本文指出委托场景的第一性失败是不发言/错时机，并给出针对性架构；
- **闭环自评**：judge 对比预测与实测、Recalibrator 回写状态，agent 在会中持续修正而非静态提示；
- **评测协议可复用**：episode 级 whether/when/what + 校准过的 LLM judge，本身就是一套可直接照搬的 agent 评测设计（kappa=0.71 是校准证据）；
- **顶会录用**（EMNLP 2026 Main）背书方法学。

## 局限

- **无开源实现**：摘要页无代码链接，maturity 如实标 paper、runnable=false（六模块编排需按论文描述自建）；
- **语料域限制**：实验在 AMI 会议语料上，中文/其他会议形态需自建评测验证迁移性；
- **LLM judge 依赖**：评测用 LLM 打分，虽经人工校准，作品引用时仍须自做人工抽验；
- 论文数字（51.4%、2.5% 等）绑定其模型与协议，作品不得直接引用（铁律 4）。

## 如何用于比赛（比赛映射展开）

- **黑客松-数据与算法（会议助手/远程协作/无障碍工具主题）**：作品做成"数字代身替你开会"——现场 demo 让评审指定一个"缺席者画像"，agent 实时参会并在正确时机替其发言，产品冲击力直观；六模块全部可用普通 LLM API 搭建，比赛周期内可完成；
- **评测章节直接复用论文协议**：whether/when/what 三口径 + LLM judge（附 kappa 校准流程），比赛队临时发问卷的评测有说服力得多；
- **答辩差异化**：引用消融结论反驳"上更大上下文/更强模型就行"的质疑——识别缺口是架构问题不是规模问题；
- **复用成本评估：低**——零训练、AMI 语料公开、单会话编排即可 demo；主要成本是会议状态的 schema 设计与调参。
