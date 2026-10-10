---
id: arxiv-2610.11794
name: "Memento 3: 反思规则书——冻结 LLM 经可执行世界模型做递归自我改进（ARC-AGI-3 全清）"
field: [LLM agents, 世界模型, 持续学习]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-10-08"
maturity: paper
venue_tier: arXiv
reproducibility_level: low
signal:
  venue: "arXiv"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "交互游戏/多回合 agent 赛题的跨回合学习叙事：ARC-AGI-3 的 25 个公开游戏免费可玩，『规则书世界模型』是最小可实现模式——LLM 把环境规律写成自然语言规则书→编译成可执行代码预测下一步→cell 级重放对不上就拒收更新，玩得越久规则越准而非每回合从零试错；论文口径全清 25 关且仅用 44% 人类动作数，『我们的 agent 会自己总结环境规律』相比普通 ReAct 玩家在评审处是稀缺演示"
    reuse_cost: 高
    open_source: "无官方代码（abs 页无链接；检索未见 Memento 3 专属公开仓，2026-10-10）；环境侧可借开源 arc-3-agents（astroseger）或 PrimeIntellect arc-agi-3-prime-agent 搭建"
  - track: "双创-文书与申报"
    edge: "自适应 agent 产品的低成本技术路线：『冻结大模型 + 外置可验证世界模型』不改参数就让产品随使用持续变准——规则书显式可审计（区别于黑盒微调）、cell 级重放验证给更新上了质量门，申报书里是『持续学习但不失控』的完整论证链；ARC-AGI-3 全清 + 44% 人类动作数（注明 arXiv 预印本作者自报）可作可行性数字"
    reuse_cost: 中
    open_source: "无官方代码；方法叙述 arXiv:2610.11794，设计模式（规则书→编译→重放验证）可直接转译为产品架构"
sources:
  - url: https://arxiv.org/abs/2610.11794
    title: "Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks（arXiv abs 页，v1 2026-10-08，Haoyu Zhao/Zhengxu Yu/Zhiyuan He/Meng Fang/Rasul Tutunov/Haitham Bou-Ammar/Jun Wang，无 Comments 无代码链接）"
    accessed: "2026-10-10"
---

# Memento 3：冻结 LLM 靠"反思规则书"递归自我改进，ARC-AGI-3 全清 25 关

> 来源：https://arxiv.org/abs/2610.11794 （v1 提交 2026-10-08，2,034 KB，Haoyu Zhao、Zhengxu Yu、Zhiyuan He、Meng Fang、Rasul Tutunov、Haitham Bou-Ammar、Jun Wang；abs 页未列机构、无 Comments、无代码/项目链接，2026-10-10 实抓）。本卡内容出自本次抓取的摘要页；补充检索（2026-10-10）确认暂无 Memento 3 官方公开仓，第三方报道（aicoder 等检索摘要）称作者群属 UCL 与华为诺亚方舟，abs 页未证实，如实存疑。

## 是什么

Memento 3（Memento 系列续作）让**冻结的 LLM agent 持续学习显式世界模型**：世界知识维护为自然语言"规则书"（rulebook），规则书**编译成可执行代码**用于预测与规划；每次更新须通过双重验证才被接受——LLM 判断新规则忠实于现有规则书，且 **cell 级精确重放（cell-exact replay）能复现观测到的状态转移**。LLM 参数全程不动，摘要称这是通向递归自我改进（RSI）的 **model-based 路线**；另有 population 扩展并行维护多个世界模型。结果（摘要自报）：

- **ARC-AGI-3：清完全部 25 个公开游戏关卡，mean RHAE 100.0**，仅用 **44% 的人类动作数**；
- Atari Pong 案例研究：从交互中学到的**反馈控制器**在三种不同开局下 **21:0** 获胜，无需进一步调用 LLM——即学到的规则书编译体可脱离大模型自主运行。

## 解决什么问题

agent 进入陌生环境要从有限观测推断世界如何运转，并随新证据修正理解——但有限观测支持多个"都能解释过去、对未来预测不同"的世界模型，且靠微调注入经验成本高、不可审计。Memento 3 把"世界观"外置为**显式、可编辑、可执行验证**的规则书：模型冻结（省钱稳定），经验全部沉淀在规则书里，且每条更新都有重放验证这道质量门。

## 相比前方法优势

- **显式可审计**：世界模型是自然语言规则书 + 可执行代码，人可读、可改、可回滚，区别于隐式参数记忆与黑盒微调；
- **更新有验证门槛**：cell-exact replay 复现观测转移才收——给"世界模型幻觉污染"上了一道机制性防线，这是多数 memory/经验沉淀类 agent 方案没有的；
- **推理期零模型依赖的潜力**：Pong 案例显示编译后的控制器可独立运行，暗示热路径可以不付 LLM 推理成本；
- **结果口径强**：ARC-AGI-3（交互式推理基准）全清 + 动作数仅为人类 44%，在该基准属头部表现（作者自报口径）。

## 局限（如实标注）

- **无官方代码**：abs 页无链接，检索未见 Memento 3 专属公开仓（前代 Memento 有开源仓，本代代码释出状态待跟踪）；复现=从零实现规则书循环+编译+重放验证（reuse_cost 高）；
- v1 预印本无 venue，ARC-AGI-3/RHAE/Pong 全部作者自报，评测细节（游戏交互预算、判分实现）未读全文不背书；
- "全清 25 关"与 44% 动作数的效果归因未拆解：摘要称有 rulebook 与 population 扩展的针对性对比，但单模型 vs 全配置的贡献占比需读全文；
- rulebook 编译依赖强代码能力的 LLM，模型档位与成本未在摘要披露；
- 验证域为游戏类（ARC-AGI-3/Atari），向真实业务环境（网页操作/数据管线）外推未证；"递归自我改进"叙事的安全边界论文摘要未涉及。

## 如何用于比赛（比赛映射展开）

1. **黑客松-数据与算法（游戏/交互 agent 赛题）**：ARC-AGI-3 公开游戏环境免费可接入（开源 arc-3-agents、arc-agi-3-prime-agent 等第三方仓可搭环境）。可实现的降配版方法链：每回合让 LLM 把新观察写成/修订规则条目 → 规则编译成简单预测函数 → 下一回合拿预测对实测，对不上拒收该条——不需要复刻论文的完整 RSI 机制，就能做出"agent 玩得越久越懂规则"的可视化演示（规则书条数与预测命中率曲线）。相比裸 ReAct 玩家是清晰的差异化卖点。reuse_cost 高：方法自实现 + 环境搭建双成本，赛期需控范围（1-2 个游戏做深）。
2. **双创-文书与申报（自适应 agent 产品）**：技术方案叙事——"冻结大模型 + 外置世界模型"回答持续学习类产品的两个申报痛点：数据飞轮要不要微调（不用，规则书沉淀）、学习能力会不会失控（显式规则 + 重放验证 + 人工可审计）。可行性数字引 ARC-AGI-3 全清与 44% 人类动作数，注明 arXiv 预印本作者自报。reuse_cost 中：设计模式直接转译为产品架构语言，不需复现。
