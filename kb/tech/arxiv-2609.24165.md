---
id: arxiv-2609.24165
name: "APEXA: Execution-Integrity Enforcement for Multi-Agent LLM Automation of Synchrotron Data Reduction"
field: [LLM agents, 执行完整性, 科学数据自动化]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-09-21"
maturity: demo
venue_tier: workshop
reproducibility_level: medium
signal:
  venue: "arXiv（SC'26 TPC Workshop 录用）"
  stars: 0
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "数据分析 agent 作品的『结果防伪』层：把论文核心模式降维移植——每条被报告的数值结论必须映射到执行台账里的一条真实工具调用记录，工具层确定性校验、不信模型自述；论文自家数字是最好的演示脚本（安全提示词 15/200 违规 vs 执行门 0/200，前沿模型给从未运行过的命令编造了完整校准对比报告），现场让评委追问一个数字、agent 用台账自证计算过，比『prompt 里写了不许编造』的队伍高一个可信度档位"
    reuse_cost: 中
    open_source: "https://github.com/AdvancedPhotonSource/APEXA-APS-Beamline-Assistant"
  - track: "双创-文书与申报"
    edge: "AI for Science / 工业数据分析 agent 方向的可信自动化叙事：Argonne 先进光子源真实束线上部署（自然语言一句指令完成探测器几何恢复+衰减/曝光扫描积分，SC'26 TPC Workshop 录用），配合『前沿模型编造校准报告被护栏拦截』的实测案例，论证科研/工业 agent 产品必须内建执行完整性而非依赖模型自觉——有国家实验室背书的痛点证据"
    reuse_cost: 中
    open_source: "https://github.com/AdvancedPhotonSource/APEXA-APS-Beamline-Assistant"
sources:
  - url: https://arxiv.org/abs/2609.24165
    title: "APEXA: Execution-Integrity Enforcement for Multi-Agent LLM Automation of Synchrotron Data Reduction（arXiv abs 页，v1 2026-09-21，ANL 报告号，SC'26 TPC Workshop 录用）"
    accessed: "2026-09-22"
  - url: https://github.com/AdvancedPhotonSource/APEXA-APS-Beamline-Assistant
    title: "AdvancedPhotonSource/APEXA-APS-Beamline-Assistant — 官方框架代码（README 架构图与启动脚本，0 stars，2026-09-22 快照）"
    accessed: "2026-09-22"
---

# APEXA：给科学自动化 agent 装"执行完整性"强制层（Argonne 先进光子源）

> 来源：https://arxiv.org/abs/2609.24165 （v1 提交 2026-09-21，cs.AI；Comments：5 pages 4 figures，录用于 SC'26 的 4th TPC Workshop（Building Open AI Infrastructure, Models, and Agentic Systems for Science）；官方代码 github.com/AdvancedPhotonSource/APEXA-APS-Beamline-Assistant，数据 doi.org/10.18126/tgg4-1m26；抓取日期 2026-09-22。本卡内容出自本次抓取的摘要页与官方仓库 README。）

## 是什么

arXiv 2609.24165（Pawan K. Tripathi、Hemant Sharma、Andrew Chuang、Mathew J. Cherukara，Argonne 国家实验室先进光子源 ANL/APS）解决同步辐射数据削减（探测器校准+方位角积分的 TB 级衍射序列处理）的 LLM agent 自动化**执行诚信**问题：随机性模型驱动的真实流水线会出现"报告了一个从未被执行的计算结果"的失败模式——论文的关键句是**"正确性是'执行了什么'的属性，不是'对话记录里写了什么'的属性"**。三项贡献：

- **执行完整性强制**：确定性工具层护栏，阻止未执行结果的报告。部署实例：一个前沿模型为从未运行过的命令编造了完整的校准对比报告，护栏将其转为"非结果"；电机控制门的对抗违规为 **0/200**，而安全提示词为 **15/200**；
- **APEXA-Bench**：58 项设施任务（50 基础 + 8 跨探测器切片），按四类物理后果分级taxonomy，评分过程还顺带暴露了两个流水线潜在 bug；
- **真实束线验证**：一句自然语言提示完成探测器几何恢复与衰减/曝光扫描积分。

官方开源完整框架（README 实证）：编排 agent + 四个专才 agent（校准/分析/知识/可视化）、MCP 工具服务器族（core 10 工具/midas 50 工具/电机 13 工具）、执行台账（apexa_ledger.py）、工具面管控（apexa_toolsurface.py）、护栏（handbook_guardrails.py）、幂等控制（_idempotency.py）、benchmark 与 tests 目录、CLI/Gradio/Web/Trame 多套 UI。

## 解决什么问题

科学/工业自动化 agent 特有的盲区：chat 基准测不出"编造了没跑过的计算结果"，而这类结果一旦流入下游（校准、材料分析）就是物理级的错误。APEXA 把诚信校验从"提示词恳求模型别编"下沉为工具层的确定性检查——每个被报告的结果都必须对应台账里真实发生的执行记录，否则降级为非结果。

## 相比前方法优势

- 防的是**结果造假**而非指令注入：与库内 SARA（arxiv-2608.27146，防工具输出变成命令）攻防面正交，可叠加；0/200 vs 安全提示词 15/200 的对照直接量化了"提示词防御不够"；
- 论文+代码+数据三件套齐（数据有 DOI），且出自真实设施部署——不是纸面框架，grader 还在真实使用中抓出了两个流水线 bug，证明评测本身有生产力；
- 台账/工具面/幂等/护栏四件套是**领域无关的工程模式**，虽然代码绑定同步辐射栈（EPICS 电机、MIDAS、GSAS-II），但模式本身可直接搬到任何数值型 agent 流水线。

## 局限

- 官方仓 0 stars、license 为 "Other/NOASSERTION"（非标准开源许可，商用/二次分发需留意授权）；设施领域绑定重，完整框架脱离束线环境跑不起来，比赛可复用的是模式而非代码；
- workshop 级录用（SC'26 TPC Workshop），5 页短文，主实验（0/200 vs 15/200）规模与对手样例覆盖有限；
- 领域是同步辐射数据削减，"执行完整性"在非数值型任务（写作、检索类）上如何定义"结果必须对应执行"需自行重构；
- 确定性护栏需要对每个工具定义"什么算已执行且结果一致"的规格，工具越多维护成本越高。

## 如何用于比赛（比赛映射展开）

- **黑客松（数据与算法）**：数据分析/科学计算类 agent 赛题的可信层——照抄台账模式：所有工具调用落 append-only 台账，agent 输出数字前先查台账，查不到就答"未计算"；演示环节故意让评委问一个没算过的数，展示 agent 拒绝编造并给出台账证据（对照组：裸 agent 现场编一个）。论文的 0/200 vs 15/200 就是现成的说服材料（reuse_cost=中：模式简单但需自建台账模块，官方代码仅作参考实现）。
- **双创（文书与申报）**：AI for Science / 工业 agent 赛道的产品叙事——"可信科研自动化"痛点有 Argonne 真实部署与前沿模型编造报告的实测案例背书，技术方案照 APEXA 架构图改（编排+专才 agent+MCP 工具层+执行台账），引用其"评分器抓出两个流水线 bug"论证评测体系本身的价值（reuse_cost=中：故事好借，产品化需自己实现完整性层）。
