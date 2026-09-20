---
id: arxiv-2609.02783
name: "EarlyEval：agent 评测省钱器（早期结果预测+置信早停，HF 112 赞）"
field: [LLM agent, 评测提效, 早停预测]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-09-01"
maturity: demo
venue_tier: arXiv
reproducibility_level: high
signal:
  venue: "HuggingFace Papers（upvotes 112，2026-09-20 候选队列实抓）+ GitHub inphotoo/earlyeval（9 stars，MIT，2026-09-20 API 实抓；论文 Comments 自述 code+data）"
  stars: 9
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "agent 类黑客松 48 小时迭代中评测是最大隐性开销（前沿模型过一遍 agentic benchmark 数百至上千美元）：EarlyEval 用 LightGBM 成功/失败双分类器盯中间行为特征，任一分类器过校准阈值即终止——三基准（SWE-bench Verified/TerminalBench/Toolathlon）实测省 13-26% agent 步数、至多 44.1% input token 与 29.4% output token，预测精度 89-97%，resolve 率平均扰动仅 1-2pp；MIT 代码直接接进自家 agent 的评测循环，省下的预算换更多轮 prompt/架构迭代，这是同类参赛队伍少有的工程杠杆"
    reuse_cost: 低
    open_source: "https://github.com/inphotoo/earlyeval（MIT，论文 comment 自述 code+data）"
  - track: "双创-文书与申报"
    edge: "『AI+』项目申报书的单位经济学论据：引其量化数字（评测 token 成本可压 44%、精度 89-97%）支撑 agent 产品的成本可控性与迭代效率叙事，比空谈『降本增效』有出处"
    reuse_cost: 低
sources:
  - url: https://arxiv.org/abs/2609.02783
    title: "EarlyEval: Cheaper Agent Evaluation via Early Outcome Prediction（arXiv export API 实抓：2026-09-01，Comments『Code and data available at https://github.com/inphotoo/earlyeval』；LightGBM 双分类器/三基准/13-26% 步数/44.1% input+29.4% output token/89-97% 精度/1-2pp 扰动均出自摘要原文）"
    accessed: "2026-09-20"
  - url: https://huggingface.co/papers/2609.02783
    title: "HuggingFace Papers 页（候选队列实抓 2026-09-20：upvotes 112，为本批候选最高社区信号）"
    accessed: "2026-09-20"
  - url: https://github.com/inphotoo/earlyeval
    title: "inphotoo/earlyeval 仓库实抓（GitHub API 2026-09-20：9 stars，MIT）"
    accessed: "2026-09-20"
---

# EarlyEval：在 agent 跑完之前就预言它会不会失败

> 来源：https://arxiv.org/abs/2609.02783 （arXiv export API 实抓，抓取日期 2026-09-20；HF upvotes 与仓库元数据同日实抓。以下分析基于本次抓取的摘要原文）

## 是什么

评测提效框架（摘要口径）：LLM agent 评测贵在"每个任务都要跑到底"——此前基准蒸馏只减任务数，不减单任务执行成本。EarlyEval 换一条互补轴：**agent 的最终结局往往在其中间行为里早已显形**。实现为轻量框架：训练一对 LightGBM 成功/失败分类器（特征含行为、文本、参考解特征），agent 运行中任一分类器越过校准置信阈值即提前终止。三个基准（SWE-bench Verified、TerminalBench、Toolathlon）上：消除 13-26% 的 agent 步数、至多 44.1% input token 与 29.4% output token，预测精度 89-97%，对每个 agent 的 resolve 率平均只扰动 1-2 个百分点。代码与数据开源（MIT，github.com/inphotoo/earlyeval，9 stars，2026-09-20 实抓）。

## 解决什么问题

agent 开发的迭代循环被评测成本卡死：每次改一版 scaffold 都要全量跑基准。EarlyEval 把"失败 agent 白跑到最后"的钱省下来，且与任务削减类方法正交可叠加。

## 相比前方法优势

- **单任务内省成本**，与基准蒸馏（减任务数）互补而非竞争；
- **白盒特征 + 浅层模型**（LightGBM）：不是再调一个 LLM 当裁判（那本身烧钱），训练与推理开销都可忽略；
- **校准阈值**控制误杀率：resolve 率扰动 1-2pp 的代价换 13-26% 步数/44% token 的节省，账算得过来；
- 三基准三域验证而非单榜。

## 局限

- 仓库仅 9 stars（2026-09-20 实抓），早期项目，工程打磨度未知；
- 三基准均为软件工程/工具使用域（SWE/Terminal/Tool），对数据科学类 agent（Kaggle agent、数据分析 agent）未验证——迁移前需自标一批成功/失败轨迹重训分类器；
- 分类器需各 agent/各基准单独校准，冷启动需要一轮标注投入；
- 本卡止于摘要层，特征清单与阈值校准细节未读正文。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：黑客松-数据与算法（agent 类赛题迭代评测）；双创-文书与申报（成本论据）。
- **打法**：
  (a) **接入自评循环**：黑客松/Kaggle agent 赛题里，把 EarlyEval 挂在自己的评测脚本前——轨迹特征喂 LightGBM，低置信成功的运行提前砍掉，同样的 API 预算多跑 1/3 轮迭代；
  (b) **申报书数字**：44.1% input token / 89-97% 精度 / 1-2pp 扰动三组数字直接支撑"评测成本可控"段落；
  (c) **反向用法**：早停分类器本身就是"运行时失败预警"，可包装成作品的自我监控亮点。
- **成本**：reuse_cost=低——MIT 代码可得；主要工作量是把特征抽取对齐到自家 agent 轨迹格式并重训 LightGBM（小时级）。
