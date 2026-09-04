---
campaign:
  competition_id: cy-innovation-2026
  name: 禾策——面向小农户的种养经营 AI 决策助手（暂定名，团队可改）
  theme: 高教主赛道·"人工智能+"类·本科生创意组（报名截止 2026-09-25 12:00）

scope:
  deliverables:
    - 报名信息包（截止后不可改项：组别/类别/名称先钉死，成员按 3-15 人注册）
    - 项目计划书（PDF，按学生操作手册格式细则微调；细则在手前按校赛通用结构）
    - 路演 PPT（校赛/省赛答辩口径，中英文任一）
    - 可运行原型 v1：经营仿真环境 + 农产品价格/产量时序预测引擎 + 可解释决策代理看板（一键启动）
    - 评测报告页：预测精度 vs naive 基线、决策建议质量案例集（数字全部出自战役 metrics.json）
  out_of_scope:
    - 硬件农机/具身设备/传感器部署（差异化在决策软件，且预算 1000 元约束）
    - 真实生产环境部署与真实农户付费转化（创意组：未注册、原型阶段）
    - 工商注册（创意组资格红线：通知发布前未注册）
    - kaggriculture Kaggle 作品直接包装参赛（十不准合规边界：问题定义/技术核心/落地场景必须实质差异）

tech_stack:
  - name: 经营仿真环境（种养结构/现金流/市场行情离散事件仿真，方法论复用团队自研农场 agent 战役）
    kb_tech_ids: [arxiv-2609.01126]
    rationale: 用免泄漏在线评测协议（01126）做仿真-决策全链路验证规范，支撑"项目创新"维度的可信度论证
    reuse_cost: 低
  - name: 农产品价格/产量/气象时序预测引擎（含概率区间输出）
    kb_tech_ids: [arxiv-2609.03937, arxiv-2609.02093, arxiv-2609.02068]
    rationale: RATL 检索残差修正（免重训适配分布漂移）+ CoSPOT 在线预测（CIKM 2026 官方仓）+ DynG-Diff 概率区间——差异化=以"区间+可解释"支撑"何时卖"决策而非单点预测展示
    reuse_cost: 中
  - name: 可解释决策代理（量化内核 + LLM 建议编排，LLM 被门控）
    kb_tech_ids: [arxiv-2609.04159, arxiv-2609.03340, arxiv-2609.03383, arxiv-2609.03923]
    rationale: SENTINEL-RL 架构范式（LLM 仅叙事、被确定性内核门控）正面回应评审对 AI 幻觉的质疑；PlanFence 防计划-执行漂移；TIGPO 支撑长程经营规划；03923 的校准协议用于建议质量评测
    reuse_cost: 中
  - name: 农技/政策知识库（RAG）
    kb_tech_ids: ["_surveys/RAG族"]
    rationale: 按 RAG 族 survey 的选型结论落地轻量知识检索（农时/农技/补贴政策问答），增强决策建议的领域可信度
    reuse_cost: 低

interface_contracts:
  - between: [software, document]
    contract_file: workspace/chuangxin2026/contracts/sw-doc-interface.md

milestones:
  - id: m0-skeleton
    task: 工程骨架（仓库结构/一键启动冒烟/接口契约实体化/计划书大纲与 metrics 键清单）；同周完成组队与报名系统信息录入
    owner_role: software
    depends_on: []
  - id: m1-vertical
    task: 端到端竖切——仿真环境最小闭环 + 单品类价格预测（vs naive 基线）+ 决策看板原型页
    owner_role: software
    depends_on: [m0-skeleton]
  - id: m2-full
    task: 全量实现——多品类预测（区间输出）+ 决策代理（量化内核+门控 LLM）+ RAG 知识库 + 评测协议落地
    owner_role: software
    depends_on: [m1-vertical]
  - id: m3-polish
    task: 计划书成稿（消费 metrics 稳定值）、路演 PPT、答辩模拟（人工项）；格式细则按学生操作手册微调
    owner_role: document
    depends_on: [m2-full]

acceptance:
  checklist:
    - {id: sw-boot, category: software, item: 一键启动冒烟通过（仿真+预测+看板三件套起服务）, method: 自动,
       cmd: "python workspace/chuangxin2026/software/smoke_boot.py"}
    - {id: sw-test, category: software, item: 测试套件全过, method: 自动,
       cmd: "python -m pytest workspace/chuangxin2026/software/tests -q"}
    - {id: sw-forecast, category: software, item: 预测引擎公开数据集评测完成且优于 naive 基线（指标入 metrics.json）, method: 自动,
       cmd: "python workspace/chuangxin2026/software/scripts/eval_forecast.py"}
    - {id: sw-agent, category: software, item: 决策代理端到端用例（输入行情→输出带区间与依据的建议）通过, method: 自动,
       cmd: "python workspace/chuangxin2026/software/scripts/eval_agent.py"}
    - {id: doc-compile, category: document, item: 计划书 PDF 与路演 PPT 编译通过, method: 自动,
       cmd: "python workspace/chuangxin2026/docs/build.py"}
    - {id: doc-numbers, category: document, item: 计划书/PPT 中全部性能数字与 metrics.json 一致, method: 自动,
       cmd: "python scripts/kb/lint_kb.py --file workspace/chuangxin2026/docs/plan.md"}
    - {id: man-interview, category: manual, item: 真实经营主体/校内基地场景访谈 ≥1 次并留痕（产业价值证据）, method: 人工手册}
    - {id: man-rehearsal, category: manual, item: 答辩模拟 ≥1 次并按反馈迭代 PPT, method: 人工手册}

compliance:
  ai_policy_reviewed: true
  mode: assist
  policy_basis: >-
    "不准将核心工作外包代做。商业计划书、技术文档等核心参赛材料必须由团队成员独立完成。严禁委托第三方机构或个人进行'代工'包装或撰写。"（附件8《参赛学生"十不准"》之五）
    +"若项目材料存在弄虚作假、抄袭剽窃等违规情况，则一票否决"（评审规则必要条件）。
    来源：cy-innovation-2026 条目 ai_policy，2026-09-04 核对；官方文件无 AI 专项条款
  notes: AI 仅作辅助（代码脚手架/资料检索/语言润色），核心创意、决策与文本由团队独立完成并保留人机分工记录；创意组资格红线=通知发布前未注册工商、全员全日制在校
---

# 蓝图：禾策——小农户种养经营 AI 决策助手（创意组原型）

# 正文（人读）

## 选型依据摘要

见 strategy.md 六节（大显身手信号 9/9 命中；金奖先例 知耘 2025 #41 / 智绘农稷 2024 #34 实证"AI+农业"评委认可度；差异化钉死在"经营决策大脑"软件闭环，与无人农机互补不撞车）。

## 里程碑展开

- m0（第 1 周）：报名组队是关键路径——截止后不可改项（组别/类别/名称）先在报名系统钉死；工程侧只做骨架与冒烟。
- m1（第 2 周）：竖切一条线：公开数据集（农产品批发价格）→ 预测 → 看板展示。此后所有迭代都在真实数据流上。
- m2（第 3 周）：多品类 + 区间预测 + 决策代理 + RAG；评测协议（01126）全链路落地，metrics 开始积累。
- m3（第 4 周）：文档冲刺，计划书按评审权重组织叙事（个人成长 30 → 以"团队 20 轮生产迭代的真实工程史"为主轴），数字全部回填 metrics.json。

## 风险与缓解

见 strategy.md 第五节（时间窗/同质竞争/资产复用合规/材料细则/数据可得性五项，各附缓解）。
