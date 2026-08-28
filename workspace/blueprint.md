---
campaign:
  competition_id: cumcm
  name: CUMCM 2026 冲奖工具链与实战体系
  theme: 预测与评估方法论武装（数模方向·本科组，2026-09-10~13 赛窗）

scope:
  deliverables:
    - 时序预测方法库（workspace/software/：DNBNet/AsyTO 一键基线群 + 共形预测区间 + 数据清洗底座，内置样例端到端跑通）
    - 评估与可视化框架（Beyond-MSE 双口径评估 + 图表自动产出，输出走 exports 契约 JSON）
    - CUMCM 论文编译链（workspace/docs/report.typ：摘要页/匿名合规/正文 30 页结构/AI 工具使用声明页，基于 K-04 格式规范模板）
    - 赛中 72 小时 SOP 手册（选题决策树×patterns 评审导向 + 时间轴 + 提交核查单）与 2025 真题计时演练报告
  out_of_scope:
    - 赛中实时解题与论文生成（独立作答红线，见 compliance.notes）
    - 报名/缴费/作品提交等操作（队伍经学校教务与 cumcm.cnki.net 人工完成）
    - 获奖结果承诺
    - 硬件类交付（本战役无 hardware 里程碑）
    - RSNA/agent 线作品（属备选与支线，不在本战役范围）

tech_stack:
  - name: 时序预测方法库（主力基线群）
    kb_tech_ids: [arxiv-2608.17284, arxiv-2608.16098, arxiv-2608.25128]
    rationale: DNBNet（不规则时序去偏，有官方代码）直击 2025C 类时点判定题型；AsyTO 轻量档适配全队无云算力（RTX 4070 8GB）；Context Routing 实证结论指导多模态特征取舍
    reuse_cost: 中
  - name: 评估与不确定性框架
    kb_tech_ids: [arxiv-2608.17293, arxiv-2608.17333]
    rationale: Beyond-MSE 双口径评估对应评奖标准"结果的正确性"的量化呈现；SPACE 共形区间升级"假设的合理性"论证——两卡均可方法论级落地，无重训练依赖
    reuse_cost: 低
  - name: 情景增强备选模块（赛题命中才启用）
    kb_tech_ids: [arxiv-2608.17164, arxiv-2608.23855]
    rationale: SCENARIODIFF/ICI-Time 面向文本+数值事件驱动题；栈重（LLM+扩散/跨模态），仅当赛题命中时按 SOP 决策树启用
    reuse_cost: 高

interface_contracts:
  - between: [software, document]
    contract_file: workspace/software/exports/schema.json

milestones:
  - id: m1
    task: 方法库骨架与 DNBNet/AsyTO 基线跑通（含样例数据与一键 CLI）
    owner_role: software
    depends_on: []
  - id: m2
    task: 评估框架与 exports 导出契约落地（双口径指标 + 图表）
    owner_role: software
    depends_on: [m1]
  - id: m3
    task: 论文编译链与 AI 工具使用声明模板（typst，格式规范 2026 修订稿对齐）
    owner_role: document
    depends_on: [m2]
  - id: m4
    task: 2025 真题全流程计时演练（缩时版）与复盘报告
    owner_role: software
    depends_on: [m1, m2, m3]
  - id: m5
    task: 72h SOP 手册与可复用资产清单定稿（含 MCM/ICM 2027 复用指引）
    owner_role: document
    depends_on: [m4]

acceptance:
  checklist:
    - {id: sw-deps, category: software, item: 依赖锁定安装通过, method: 自动,
       cmd: "python -m pip install -q -r workspace/software/requirements.txt"}
    - {id: sw-boot, category: software, item: 方法库一键冒烟（内置样例端到端基线）, method: 自动,
       cmd: "python workspace/software/smoke_boot.py"}
    - {id: sw-test, category: software, item: 测试套件全过, method: 自动,
       cmd: "python -m pytest workspace/software/tests -q"}
    - {id: doc-compile, category: document, item: 论文链编译通过（含摘要页/AI 声明页）, method: 自动,
       cmd: "typst compile workspace/docs/report.typ workspace/docs/report.pdf"}
    - {id: man-sim, category: manual, item: 2025 真题计时演练由队伍实际执行并记录, method: 人工手册}
    - {id: man-reg, category: manual, item: 赛区报名完成性核查（09-07 20:00 前，经学校教务）, method: 人工手册}

compliance:
  ai_policy_reviewed: true
  mode: prep
  policy_basis: >-
    《全国大学生数学建模竞赛人工智能工具使用规定（2026年试行）》（mcm.edu.cn，2026-08-27 实抓）：
    "参赛队可以使用但不要求必须使用，须遵循公开透明原则，确保核心建模与分析由参赛队主导，并对AI生成内容
    逐项人工审查与核实"；"隐瞒使用、虚假声明或把未审查AI内容直接当核心成果提交的，取消评奖资格"。
    另《参赛规则（2026年修订稿）》第5条："竞赛期间必须独立完成，严禁与队外任何人（含指导教师）交流讨论赛题"。
  notes: >-
    prep 边界：本战役只交付赛前资产（工具链/SOP/演练）。赛中（09-10 18:00 ~ 09-13 20:00）不得运行
    本框架的编排/交付流程——独立作答纪律与人主导红线双重约束。赛中 AI 使用由队伍按 2026 试行规定
    自行申报（论文 AI 声明 + 支撑材料 AI 工具使用详情.pdf）。

---

# 正文（人读）

## 选型依据摘要

- 主推 cumcm：时间窗 13 天最优区 + patterns 23/23 全量武装 + 画像 M 奖已验证（详见 workspace/strategy.md 六维矩阵与大显身手信号）。
- 方法库以"有代码/轻量/方法论级"三档组合：DNBNet（官方代码，可直接跑）→ AsyTO（无代码但线性代数结构透明，数天自实现）→ 评估双卡（纯方法论落地，零训练成本）；SCENARIODIFF/ICI-Time 为情景题备选，栈重不预投入。
- 论文链复用 K-04 已挂的 report-cumcm.typ 格式规范模板（2026 修订稿实抓结构化），把"摘要页第一页/匿名/30 页上限/AI 声明位置"做成编译期约束而非人工记忆。

## 里程碑展开

m1-m2（软件主体）并发于 m3 前半（文档可先行搭骨架）；m4 演练是全链路验收的实战版（真题数据走方法库→评估→论文链全流程计时）；m5 收口 SOP 并沉淀 MCM/ICM 2027-01 复用指引（一鱼多吃终点）。

## 风险与缓解

1. 赛题不命中时序方向 → 方法库含清洗/回归通用底座 + SOP 选题决策树（patterns 评审导向：假设合理性优先）。
2. 报名时点（09-07 截止经学校）→ man-reg 验收项 + 建议用户即刻确认学校报名进度。
3. 赛中合规 → prep 模式硬边界，见 compliance.notes；SOP 手册内嵌"赛中禁用清单"一页。
4. 数字纪律：演练报告与 SOP 中一切性能数字只能来自 workspace/metrics.json 实测。
