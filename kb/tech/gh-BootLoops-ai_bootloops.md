---
id: gh-BootLoops-ai_bootloops
name: "BootLoops 1.0：给 LLM Agent 用的可认证高精度计算工具箱（49 包自检 + agent 协议技能库）"
field: [LLM agents, scientific computing, 可信数值计算]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-10-01"
maturity: demo
reproducibility_level: high
signal:
  venue: GitHub
  stars: 168
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "物理/数学/数值密集型赛题（精确积分、贝叶斯模型比较、递推证明、枚举完备性）的防幻觉算错底座：clone 即用，MIT 零门槛，`python3 run_selftests.py` 一条命令验证 49 个工具包全部自检通过，笔记本+已有模型额度即可驱动；工具以 agent 视角写文档（做什么/何时用/输出什么含义/答案须过什么检验），任何 agent 框架可直接挂载。相比'让 LLM 直接算'的队伍，差异化是每个数字带可证明误差半径（ball arithmetic）甚至闭合形式证书——评委可现场复验"
    reuse_cost: "低"
    open_source: "https://github.com/BootLoops-ai/bootloops（MIT；文档 CC BY 4.0）"
  - track: "双创-文书与申报"
    edge: "'AI for Science / 可信科学计算'方向项目的技术底座与可信性协议素材：其 skills 库（planted-truth 阳性对照、独立路线交叉复现、整数关系纪律、溯源账本、'正对照必须能失败'的检验设计）是一套现成的'AI 结果可审计'方法论，可直接写进申报书的质量保障章节；工具箱本身可作产品原型的计算引擎层（reuse_cost=中：需要把科研工具链包装成领域产品）"
    reuse_cost: "中"
    open_source: "https://github.com/BootLoops-ai/bootloops（MIT；文档 CC BY 4.0）"
sources:
  - url: https://github.com/BootLoops-ai/bootloops
    title: "BootLoops-ai/bootloops — README（49 工具包、house engines、skills 协议库、run_selftests 自检流程，2026-10-03 raw 实抓）"
    accessed: "2026-10-03"
  - url: https://api.github.com/repos/BootLoops-ai/bootloops
    title: "GitHub API 仓库元数据（168 stars / 33 forks / Python / MIT / 创建于 2026-10-01 / topics: feynman-integrals, llm-agents, physics, scientific-computing，2026-10-03 快照）"
    accessed: "2026-10-03"
---

# BootLoops：让 LLM agent 拿到"算得对还自带证明"的科学计算仪器台

> 来源：https://github.com/BootLoops-ai/bootloops （README raw + GitHub API，2026-10-03 实抓；官网 bootloops.ai。本卡内容出自本次抓取。）

## 是什么

BootLoops-ai 组织 2026-10-01 开源的 **BootLoops 1.0**（MIT，Python，168 stars / 33 forks，2026-10-03 快照；两天内破 150 星，本批最强 GitHub 信号）：一个**为 LLM agent 驱动而造的高精度/精确科学计算 harness**。两部分构成：

- **工具箱**（`tools/` 下 49 个包，每包配 GUIDE.md，标注用途/验收门槛/验证类别）：数学物理前沿积分（多重参数积分，闭合形式或数百位认证数字，覆盖 polylog/椭圆/K3/Calabi-Yau 类）、带证明的递推关系（含证书，强到能证明某闭合形式不存在）、闭合形式贝叶斯证据积分（模型比较的边际似然，解析或认证数值求积而非采样）、以收敛方法替代蒙特卡洛（带认证误差界）、ball arithmetic 误差传播（每个值带可证明误差半径）、带完备性证书的穷举枚举、从公开文档从写并对照已发表输出验证的标准统计程序，以及领域代码库（JaCKandJill 贝叶斯系统发育、Mixalot 统计、Terrier 弦景观、Popcorn 群体遗传学）与 house engines（SOFIA.jl、Eichler.jl、Leviathan Landau 引擎；Kira/Blade/AMFlow.cpp 补丁分叉另仓）；
- **skills 协议库**（独立仓库，纯 markdown，任何 agent 框架可读）："做完"的定义——结果须在拟合未见的点上复现独立路线且阳性对照能失败、整数关系搜索前声明常数环、真实数据前先种已知答案（planted-truth）、溯源账本隔离曾喂拟合的 oracle、先小跑测时序，以及"与 agent 一起做证明/模拟审稿人/审计新颖性主张/核验文献"的重协议。

用法：clone 后把任意 agent 指进去，`python3 run_selftests.py --par 8` 数分钟内逐包自检（49 包绿灯，3 个因缺随仓数据报具名错误）。

## 解决什么问题

LLM 做定量科学时的两大不可信源：算术/数值错误不可检出、统计误差冒充确定结论。BootLoops 把"仪器"从模型外部补齐：计算交给认证工具（误差半径、证书、完备性证明随结果携带），行为交给协议（每类结果必须先过什么检验才可信），使"agent 算出的数"达到"有人需要信"的标准。

## 相比前方法优势

- 相比通用数学工具 MCP/代码解释器：不止"能算"，而是**结果带认证**（误差半径/证书/完备性证明），且协议层规定"何时可以信"——这是普通 sympy/numpy 封装没有的验证层；
- 模型无关：harness 独立于驱动它的模型，任何 agent 框架接入即可用，工具文档按 agent 视角写（何时用/输出含义/验收检验），挂载成本低；
- 相比库内科学计算类卡（如 RAGScope/科学问答 RAG 卡是检索层）：本卡是**执行层**的可信计算基建，互补不重叠；其 planted-truth/阳性对照协议与库内评测治理卡（tsfm-bench 的数据泄漏审计等）同属"防作弊验证"思想，可互引；
- 开源即跑：一条自检命令验证安装，笔记本级硬件要求。

## 局限

- 发布仅两天（2026-10-01 创建），无论文、无同行评审，成熟度凭自检与官网叙事背书；
- 工具谱系重心在数学物理（散射振幅出身的工具箱），"general purpose"的宣称对 ML/工程类赛题覆盖有限——统计程序包有，但深度学习/数据处理类工具缺席；
- 驱动仍需较强的底层模型（读懂工具文档、按协议规划验证路线），小模型上协议遵从性存疑；
- 3 个包需自备外部数据，部分 house engines 依赖 Julia 环境，安装面不完全零摩擦。

## 如何用于比赛（比赛映射展开）

- **黑客松（数据与算法）**：赛题一旦涉及"数值必须对"（物理仿真、优化下界、概率计算、组合枚举），两步走：把 bootloops clone 进工程，agent 读 tools/README 自选仪器；关键结果强制过其验收检验并展示误差半径/证书——答辩时"我们的数字每一个都带可证明误差界、评委可现场复验"是对"LLM 直算"队伍的碾压级差异化（reuse_cost=低，MIT，笔记本可跑）。
- **双创（文书与申报）**："AI+科学计算/科研助手"类项目的技术可信性章节可直接引其协议清单（阳性对照、独立路线复现、溯源账本）作为产品质量保障框架，并引 49 包自检的工程化程度佐证可行性；工具箱作引擎层原型，规避"从零造科学计算轮子"的申报硬伤（reuse_cost=中）。
