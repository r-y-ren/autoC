# 蓝图（workspace/blueprint.md）骨架——frontmatter 须过 blueprint.schema.json，不过不得呈报确认

> 用法：复制本骨架填充；`?` 处必填；注释行删除。验收清单默认线按作品类型抄默认项（"完整可实用"的四标准是硬约束）。

---
campaign:
  competition_id: ?            # KB-1 条目 ID（strategy 呈报的推荐或用户指定）
  name: ?
  theme: ?                     # 本届主题/赛道

scope:
  deliverables: [?]            # 逐项对齐该赛 meta.deliverables（赛方要什么就交什么）
  out_of_scope: [?]            # 显式排除项，防范围失控

tech_stack:
  - name: ?
    kb_tech_ids: [?]           # 每项选型必须引用 KB-2 卡片 ID（禁凭印象）
    rationale: ?               # 差异化逻辑（与大显身手信号呼应）
    reuse_cost: 低|中|高

interface_contracts:           # 并发分发前钉死；软件↔硬件协议、document 消费路径
  - between: [software, hardware]
    contract_file: workspace/?

milestones:
  # ── 里程碑分层模板（D12 波次化，可直接抄改）──
  # K-03 按 depends_on 拓扑分层成波；轻蓝图推荐四阶段依赖链（大结构默认化）：
  #   骨架层 → 竖切层 → 完整层 → 打磨层；重蓝图按需加层（如评估层/集成层）
  - id: m0-skeleton          # 骨架层：可编译空壳 + 接口契约实体化 + 报告大纲
    task: 工程骨架与接口契约落地（仓库结构/CI 冒烟/报告大纲与 metrics 键清单）
    owner_role: software
    depends_on: []
  - id: m1-vertical          # 竖切层：端到端最小可运行（walking skeleton）
    task: 核心功能一条线打通（最小数据流 + smoke_boot 可跑）
    owner_role: software
    depends_on: [m0-skeleton]
  - id: m2-full              # 完整层：全量功能 + metrics 开始积累真实数据
    task: 按范围全量实现 + 测试套件齐备
    owner_role: software
    depends_on: [m1-vertical]
  - id: m3-polish            # 打磨层：集成/性能/边界 + 文档成稿（数字回填）
    task: 跨角色集成与打磨、报告/PPT 成稿（消费 merge_metrics 稳定值）
    owner_role: document
    depends_on: [m2-full]
  # 验收项 id 建议带里程碑前缀（如 m0-、sw-），便于波门 --only 左移检查

acceptance:
  checklist:
    # ── 软件类默认线（完整可实用：可运行/可验证/可维护/可交付）──
    - {id: sw-boot, category: software, item: 一键启动冒烟通过, method: 自动,
       cmd: "python workspace/software/smoke_boot.py"}
    - {id: sw-test, category: software, item: 测试套件全过, method: 自动,
       cmd: "python -m pytest workspace/software/tests -q"}
    # ── 文档类默认线 ──
    - {id: doc-compile, category: document, item: 报告/PPT 编译通过, method: 自动, cmd: ?}
    # ── 硬件类默认线（物理项一律 manual）──
    - {id: hw-fw, category: hardware, item: 固件编译通过, method: 自动,
       cmd: "python3 -m platformio run -d workspace/hardware/firmware"}
    # ── 人工项示例 ──
    - {id: man-1, category: manual, item: 物理装配与实测, method: 人工手册}

compliance:
  ai_policy_reviewed: true|false
  mode: prep|apply|assist      # 三分硬校验（见 strategy-template 第五节判定规则）
  policy_basis: ?              # 该赛 ai_policy 原文关键句摘引（apply/assist 必填，schema 强制）
  notes: ?
---

# 正文（人读）

## 选型依据摘要 / 里程碑展开 / 风险与缓解
（正文自由；一切数字在验收时只能来自 metrics.json）
