# autoC — 竞赛情报与作品生成 Agent 框架：结构设计

> 版本 v0.9（2026-08-27）｜本版只定**结构层**：平台选型、循环骨架、阶段定义、目录与文件契约、行为治理。
> v0.9 变更：T3-c 能力完善——S-13 ocr_pdf（扫描件解析，实测消化 cumcm 待办并升级 verified）；winners/patterns 解构管线（模板+章程契约+CUMCM 首样板）；文档链冒烟（typst/marp 模板原样编译通过）；双频慢循环（K-08 深度评估+周六 cron）；E-09…E-12 登记；D5 裁决（零新增 MCP、RSSHub 缓判、tools/ 落位纪律、S-13 编号）。
> v0.8 变更：T2.1 修复轮——审查实测确认的 5 缺陷修复（跑批记录多行丢行 / pending_agent 绕归档闸门 / tag 先于 commit / cmd 超时崩溃及孤儿进程劫持管道 / suggested_fields 循环变量泄漏）+ 2 语义裁决（仅 fail 计入 retry；候选队列生命周期：processed/ + .rejections.yaml 台账 + stars 翻倍重评）+ retry.max 单一事实来源（budget.yaml）+ 三套新回归测试。
> v0.7 变更：T2 落地——S-02…S-06 脚本、K-01…K-07 技能、H-03 会话播报；K-03 前置项裁决（metrics 分片制已实现并 L2 强制；角色身份级守卫评估后不引入，理由见 §6.2 处置记录）；验收清单新增可选 cmd 字段。
> v0.6 变更：T2 开工校准——①残留 `.zcode/subagents/` 全部修正为 `.zcode/agents/`；②Hardware 更名 Hardware Agent 并按 D2 裁决标注 CLI 路线；③§6.2 如实区分"L1 角色软边界 / L2 阶段硬边界"，角色身份级守卫与 metrics 并发风险列为 K-03 前置评估项。
> v0.5 变更：按 Phase 0 实测校准——钩子注册落点为 `.zcode/config.json`（`hooks.events`，需 `enabled: true`）、子 agent 目录暂定 `.zcode/agents/`（首个章程编写时经 Settings → Subagents 实测确认）。
> 各模块细节（信源清单、schema 字段、验收清单条目等）在逐模块讨论后补充为独立模块文档，本文不展开。

---

## 1. 平台选型：当前客户端 + artifact-driven

**结论：v1 直接在当前客户端（ZCode 工作区）构建，不引入 LangGraph。**

核心理由：

1. **难点在节点能力，不在图编排。** 本项目真正难的是异构信源解析、完整软件工程、成套文档生成——依赖的是浏览器自动化、document-skills、Bash 沙箱、CUA、子 agent、cron 这些能力，客户端已全部具备；在 LangGraph 中这些需要全部自建。
2. **人工闸门免费。** 决策确认在会话客户端中是原生 human-in-the-loop；LangGraph 需额外构建交互界面（CLI/Web UI）。
3. **文件系统即状态存储。** 阶段间只通过文件契约交接：断点续跑 = 检查文件存在性；审计 = git diff。这替代了图框架的 checkpointing 卖点。

**迁移条件**（满足任一条再评估 LangGraph）：

- 产品化 / 多用户 / 服务器无人值守运行
- 收集规模大到需要程序化重试、预算控制与 LangSmith 级观测
- 流程结构本身需要频繁重构

**迁移成本控制**：坚持"skill 承载流程、文件契约承载交接"两条纪律。满足后，未来迁移 = 把 skill 包成节点、把文件契约变成 state schema，属于机械操作。

---

## 2. 总体结构：两条循环，不是一条直线

```
[慢循环·常驻]  cron 定时 ──► Competition Scraper & Frontier Hunter 并发
                                │ 增量写入（merge，非重写）
                                ├──► KB-1 目标赛事名单与标杆解构库（交付物 1）
                                └──► KB-2 前沿科技资产库（交付物 2）
                                ▼
                          linter 校验 ──不合格──► kb/quarantine/ 隔离区待修
                                │ 合格
                                ▼
                          changelog + git commit

[快循环·按需]  用户指定方向
                    │
                    ▼
              强制先拉一次 KB 增量（保证决策基于最新信息）
                    │
                    ▼
              Strategy Agent：建议赛道对比矩阵 + "一鱼多吃"路线 + ★作品蓝图
                    │（蓝图 = workspace/blueprint.md，须通过 blueprint.schema.json 校验）
              [用户确认蓝图] ◄── 全流程唯一人工闸门
                    │
                    ▼
              Coordinator 按蓝图并发分发（文件契约为唯一交接物）：
              ├── Software Agent ─► workspace/software/ ─► 编码 + 沙箱测试 ─► metrics 分片 ─┐
              ├── Hardware Agent（CLI 路线）──► workspace/hardware/ ─► PlatformIO / Wokwi 验证 ─► metrics 分片 ─┤(并行)
              └── (汇合点) merge_metrics.py 汇总 ─► Document Agent ◄── 消费工程产物 + metrics 汇总 ─► 报告 + 答辩 PPT
                    │
              [验收节点] ──不通过──► 失败工单路由回责任 agent 修复（唯一回路边，带熔断）
                    │ 通过
                    ▼
              [交付归档] archive_campaign.py：workspace/ ─► archive/<YYYY-MM_赛事_主题>/（只读 + git tag）
```

**结构要点（四条骨架纪律）：**

1. **两条循环**：KB 是常驻资产（cron 定时增量维护），攻坚是按需战役；快循环启动前强制刷新一次，两条循环靠文件系统解耦。
2. **唯一人工闸门确认的是蓝图级文档**：跨 agent 接口契约（固件协议、数据格式、目录布局）必须在并发分发前钉死。选赛事与定方案在一次确认中合并覆盖。
3. **验收-修复节点**位于工程交付与归档之间：验收清单不过 = 未完成；失败项带证据路由回责任 agent；**重试超限触发熔断**，停机升级人工，防止回路边死循环。
4. **Agent 编排，脚本跑紧循环**：确定性循环（API 拉取、去重、编译测试、验收执行、归档）写成脚本由 agent 调用；agent 只做判断密集环节。

---

## 3. 阶段结构定义

### 3.1 慢循环：知识库维护（全自动）

- **触发**：cron（D7 合并节奏：每 3 天一次全量深度跑批=增量+深度）＋ 快循环启动时强制刷新；K-01 保留为手动轻量补偿入口（/kb-sync）
- **执行**：Scraper 与 Hunter 两个后台子 agent 并发；方向级信源配置在 `config/directions/`
- **写入语义**：条目级增量 merge（`last_verified` + 来源记录），绝不整体重写；原始快照落 `kb/raw/`（不进 git 主干）
- **质量闸**：lint_kb 校验 frontmatter/引用完整性（schema 在 `config/templates/`）→ 不合格进 quarantine；所有分析基于本次实抓文档、逐条带引用 URL + 抓取日期
- **候选队列生命周期（T2.1 裁决）**：活跃队列 = `kb/raw/candidates/*.yaml`（仅顶层），K-01 消费完毕移入 `candidates/processed/`（不参与下轮去重）；Hunter 拒绝的候选记入 `kb/tech/.rejections.yaml` 台账（id/reason/stars/decided），sync_tech 对台账候选去重、**stars 达快照 ×2 自动放行重评**（科技信号随时间增长的核心场景）
- **产物**：KB-1（赛事信息 + 历年获奖解构 + 模式库）、KB-2（技术卡片：是什么/用途/优势/成熟度/比赛映射）、聚合索引 `kb/INDEX.md`
- **交付形式（D6）**：源库（kb/）面向 agent 检索；人读交付物为 `export/digest-*.md` 方向情报简报——S-15 从条目层纯投影生成（只重组不新增事实），每 3 天跑批末尾刷新草稿、当月最后一次跑批（下一次跨月）自动转正式版

### 3.2 决策阶段（交互）

- **输入**：用户方向 + 团队画像 `config/profile.yaml` + `kb/INDEX.md`
- **输出**（Strategy Agent 产出两份待确认文档）：
  1. `workspace/strategy.md`：建议赛道对比矩阵（时间窗 × 技术契合度 × 通吃度 × 画像匹配 × 竞争密度）+ "一鱼多吃"复投路线
  2. `workspace/blueprint.md`：作品蓝图（范围 / 技术栈，引用 KB-2 卡片 / 跨 agent 接口契约 / 里程碑 / 验收清单 / 合规检查），**须通过 blueprint.schema.json 校验方可提交确认**
- **用户确认蓝图**后进入交付；不认可则改蓝图再确认（闸门可重复，但同一时刻只有一个）

### 3.3 工程交付（全自动）

- Coordinator（主 agent）按蓝图拆解为**任务包**，每个任务包 = 输入契约 + 输出契约 + 验收标准
- **并发**：Software 与 Hardware 子 agent 并行；Document Agent 在汇合点后启动（消费前两者落盘的产物文件）
- 各角色在各自 `workspace/<role>/` 目录内工作，Bash 沙箱内自验（编译 / 测试 / 仿真）
- **实测数据契约（分片制）**：各工程角色只写自己的 `workspace/<role>/metrics.json` 分片（实测值+测量方法）；`scripts/verify/merge_metrics.py` 确定性汇总为顶层 `workspace/metrics.json`（命名空间 `metrics.<role>.<键>`，角色禁写，守卫已拦）。Document Agent 引用的一切性能数字**只能来自汇总文件**，禁止自行编造

### 3.4 验收-修复节点（全自动，可升级人工）

- `scripts/verify/run_acceptance.py` 逐项执行蓝图验收清单（**带 cmd 的项自动执行并存证据，超时记为 fail 并杀整棵进程树**；执行前先汇总 metrics 分片），产物写入 `workspace/acceptance/`：
  - 软件：一键启动、测试全过、browser-use 实测取证（截图/录屏）、真实数据端到端
  - 硬件：仿真（Wokwi）通过、设计文件/BOM/固件齐备；**物理项列为人工测试项**移交用户
  - 文档：结构完整性、数字与 metrics.json 一致性、格式校验
- 失败项**带失败证据**生成失败工单，路由回责任 agent 修复后重跑；`.flow/state.json` 记录重试计数（**仅 fail 计数**——pending 是等待而非失败重试，T2.1 裁决；retry.max 单一事实来源为 budget.yaml），**超限熔断**升级人工
- 通过后生成分析报告（对照该赛评审标准自评 + 历年获奖基准对比）

### 3.5 归档

- `scripts/verify/archive_campaign.py`：workspace/ 整体移入 `archive/<YYYY-MM_赛事_主题>/`，脚本内完成 **git add → commit → tag**（commit 先于 tag，tag 快照才含归档内容）+ 只读锁，**归档后不可变**
- 归档内容：攻略、蓝图、作品本体（software/hardware/docs）、验收记录、分析报告、人机分工记录（合规留痕）
- 归档是**脚本动作**而非 agent 行为；workspace/ 随之清空，可开启下一战役

---

## 4. 目录结构与文件契约（artifact-driven 的核心）

```
autoC/
├── .zcode/                      # 客户端原生配置层（原生感知，不自造平行概念）
│   ├── agents/                  # 角色章程 = 子 agent 定义（目录名待首个章程编写时实测确认）
│   ├── skills/                  # SOP 纯函数技能（blueprint-gen / lint / marp-deck / typst-report 等）
│   └── config.json              # hooks.events 注册（enabled:true；PreToolUse 路径守卫，M0 已实测格式）
├── .flow/                       # 运行时状态（gitignore；守卫/脚本动态读写）
│   └── state.json               # 当前阶段、允许写根、重试计数与熔断状态
├── config/                      # 静态配置与契约规范中枢
│   ├── profile.yaml             # 团队画像（技术栈、算力设备、参赛历史）
│   ├── budget.yaml              # 跑批预算与限速策略
│   ├── directions/              # 方向采集配置（信源订阅、关注关键词）
│   └── templates/               # 模板 + JSON Schema（防幻觉规范，校验唯一来源）
│       ├── blueprint.schema.json
│       ├── kb-meta.schema.json / tech-card.schema.json / acceptance.schema.json
│       ├── presentation.marp.md
│       └── report_template.typ
├── scripts/                     # 确定性脚本与工具链
│   ├── kb/                      # sync_competitions / sync_tech / lint_kb / 索引构建
│   ├── guard/                   # guard_path.py（L2 写入拦截；state 缺失时 fail-closed）
│   └── verify/                  # run_acceptance.py / archive_campaign.py
├── kb/                          # 沉淀知识库（交付物 1 & 2，清洗后的轻量 Markdown）
│   ├── INDEX.md                 # 两库聚合全景索引（瘦协调者的唯一入口）
│   ├── competitions/            # KB-1：每赛一目录（meta / winners / patterns）
│   ├── tech/                    # KB-2：技术卡片（规范化 ID 命名）
│   ├── quarantine/              # linter 不合格条目
│   └── raw/                     # 原始快照与 PDF（gitignore 默认排除，需要审计留痕时切 LFS）
├── workspace/                   # 当前战役活跃开发区（动态；v1 单战役约束）
│   ├── strategy.md              # 决策阶段输出（对比矩阵 + 一鱼多吃路线）
│   ├── blueprint.md             # ★ 唯一蓝图契约（schema 校验后方可确认）
│   ├── JOURNAL.md               # 阶段流转日志（随 git 提交，状态可审计）
│   ├── metrics.json             # 分片汇总生成物（merge_metrics.py 产出；角色禁写，分片在各角色目录）
│   ├── software/                # Software Agent：代码 + 沙箱测试
│   ├── hardware/                # Hardware Agent：BOM / 引脚表 / 固件
│   ├── docs/                    # Document Agent：报告 + PPT 源码（Marp/Typst）
│   └── acceptance/              # 验收角色：执行记录 / 失败工单 / 分析报告
├── export/                      # KB 交付导出层（D6：条目层纯投影，读者=团队自用）
│   └── digest-<方向>-<YYYY-MM>.md  # 方向情报简报（S-15 生成；周更草稿，月末周六转正式版）
├── archive/                     # 历史作品库（交付物 3，归档后只读，带 git tag）
│   └── 2026-08_挑战杯_智能巡检/
├── AGENTS.md                    # 全局纪律与行为红线
└── README.md
```

**分层意图**：原生配置（.zcode/）／运行时状态（.flow/，不入库）／静态配置与契约（config/）／确定性脚本（scripts/）／沉淀知识（kb/）／活跃开发区（workspace/）／固化归档（archive/）——七区各态隔离，守卫规则与分区一一对应。

**关键文件契约（阶段间唯一交接物）：**

| 交接 | 契约文件 |
|---|---|
| 慢循环 → 决策 | `kb/INDEX.md` |
| 决策 → 交付 | `workspace/blueprint.md`（含接口契约 + 验收清单，schema 校验通过） |
| 工程内部（角色间） | `workspace/<role>/` 产物目录 + `workspace/metrics.json` |
| 交付 → 验收 | 蓝图验收清单 × `workspace/` 实际产物 |
| 验收 → 归档 | `workspace/acceptance/`（全项通过记录 + 分析报告） |

**v1 约束**：单一 workspace/ + 单一 state.json 隐含"同时只有一个活跃战役"；战役实践上串行，故接受此简化。并行战役的扩展路径：workspace/\<campaign\>/ 参数化 + state.json 携带战役 ID。

---

## 5. 组件 → 客户端机制映射

| 骨架组件 | 当前客户端机制 |
|---|---|
| Scraper & Hunter 并发 | `.zcode/agents/` 章程 + 后台子 agent 并行 + 紧循环脚本 |
| KB 增量调度 | Cron → `scripts/kb/` |
| Strategy Agent | 主 agent + `.zcode/skills/`，读 `kb/INDEX.md` |
| 用户确认蓝图 | 会话交互（原生 human-in-the-loop） |
| Coordinator | 主 agent 把蓝图拆为任务包 |
| Software Agent + 沙箱 | 子 agent + Bash 工作区（workspace/software/） |
| Hardware Agent（CLI 路线，D2 裁决） | PlatformIO / kicad-cli / Wokwi（Bash 调用） |
| Document Agent | Marp / Typst 模板（config/templates/）+ document-skills 兜底（严格 .pptx 需求） |
| 验收执行器 | `scripts/verify/run_acceptance.py` + browser-use 实测取证 |
| 归档 | `scripts/verify/archive_campaign.py` + git tag |
| 契约校验 | `config/templates/*.schema.json` + linter |

---

## 6. Agent 行为治理：上下文隔离与职责边界

原则：**隔离靠结构（新上下文 + 文件交接），边界靠三层防线（章程·软 → 钩子与 Schema·硬 → git·审计兜底）**。不把提示词自觉作为唯一手段。

### 6.1 上下文隔离（防干扰）

1. **一阶段一子 agent，上下文用完即弃**：每阶段在独立子 agent 中执行（全新上下文），阶段间只通过文件契约交接；主会话只做调度与闸门。上一阶段的噪声物理上进不了下一阶段。
2. **瘦协调者**：主会话只读索引与结论（`kb/INDEX.md` / 摘要 / 状态文件），永不读 `kb/raw/`；子 agent 只返回结构化结论，不返回原始转储。
3. **分片粒度**：收集/分析类子 agent 按条目分片（一个比赛、一篇获奖论文 = 一个子 agent），不按整库分片，防止单上下文被噪声淹没。
4. **状态外置**：运行时状态落 `.flow/state.json`（gitignore）；阶段流转日志落 `workspace/JOURNAL.md`（提交入库，可审计）。会话压缩或每阶段换新会话执行均不丢状态（斜杠命令天然支持换会话重启）。

### 6.2 职责边界（防越界）：三层防线

- **L1 软边界——角色章程（.zcode/agents/）**：每角色一份（职责 / 输入输出契约 / 禁止清单）；Coordinator 按名派发。角色目录级的写入边界（如"Software 不得写 workspace/hardware/"）目前由**章程约定 + git 审计发现**保障，不是物理强制。
- **L2 阶段级硬边界——写入路径守卫 + 契约 Schema 校验**：
  - PreToolUse 钩子（`.zcode/config.json` → `hooks.events` → `scripts/guard/guard_path.py`，matcher 为 `Write|Edit|ApplyPatch`）执行的是**阶段级**写入控制：collect 放行整个 kb/、deliver 放行 workspace/（acceptance/ 除外）、verify 仅放行 acceptance/——**不识别调用者角色**。越界即阻断并说明原因；**state 缺失时 fail-closed**（全只读，仅放行 .flow/ 自身）。
  - 契约文件（blueprint / KB 条目 / 验收清单）必须通过 `config/templates/*.schema.json` 校验：蓝图不过校验不得进入确认闸门；KB 条目不过校验进 quarantine。
  - PostToolUse 钩子对 kb/ 契约文件即时校验（仅四类目标：`<id>/meta.md`、`kb/tech/<id>.md`、`blueprint.md`、`acceptance/*.json`；winners/patterns/raw 等正文文件明确跳过）。
- **L3 审计兜底——git**：每阶段一个 commit（阶段日志见 workspace/JOURNAL.md），越界改动必然暴露于 diff，可精确回滚（覆盖钩子未拦截的路径，如经 Bash 的写操作）。

**流程规则：验收 agent 只开失败工单，不亲手修作品**——修复路由回责任 agent，避免裁判兼运动员。

**角色写入矩阵（L1 章程依据；守卫物理执行的是其中的阶段级子集）：**

| 角色 | 允许写 | 禁止触碰 |
|---|---|---|
| Scraper | kb/competitions/、kb/raw/ | kb/tech/、workspace/、archive/ |
| Hunter | kb/tech/、kb/raw/ | kb/competitions/、workspace/、archive/ |
| Strategy | workspace/{strategy.md, blueprint.md} | kb/ 正文（只读）、workspace/ 其余子目录 |
| Software | workspace/software/、workspace/metrics.json（工程实测） | kb/、blueprint、其他角色目录 |
| Hardware | workspace/hardware/ | 同上 |
| Document | workspace/docs/（性能数字仅可引 metrics.json） | 一切代码与设计文件 |
| 验收 | workspace/acceptance/ | 不直接修任何作品文件 |

（交付阶段 kb/ 对所有角色只读；archive/ 仅 `archive_campaign.py` 可写。）

**已知边界与处置记录（K-03 前置项，T2 已裁决落地）：**

1. **角色身份级守卫——评估后不引入（v1）**：钩子负载不含调用者身份，全局 `active_role` 又会破坏 software/hardware 的并发派发。同阶段跨角色越界的保障维持 L1 章程 + L3 git 审计；唯一存在真实写冲突的文件已由下条消除，其余目录冲突风险随分片制大幅降低。
2. **metrics.json 并发覆盖风险——已解决（分片制）**：角色只写 `workspace/<role>/metrics.json` 分片，`scripts/verify/merge_metrics.py` 确定性汇总为顶层 `workspace/metrics.json`（`metrics.<role>.<键>` 命名空间）。守卫在 deliver 阶段对该生成物拒写（该文件的 L2 强制已生效）；software/hardware/document 三份章程已同步，回归用例已固化。

### 6.3 客户端自定义能力使用清单

| 机制 | 用途 |
|---|---|
| AGENTS.md | 全局铁律（引用纪律 / 契约纪律 / 合规纪律） |
| .zcode/agents/ | 角色章程（L1 软边界，见 §6.2） |
| .zcode/skills/ | SOP 纯函数技能（blueprint-gen / lint / marp-deck 等） |
| .zcode/config.json → hooks | 写入路径守卫（PreToolUse，process 型；Phase 0 已注册并冒烟验证） |
| 斜杠命令 | 阶段入口、换会话重启阶段 |
| 子 agent | 上下文隔离与并发 |
| cron | KB 定时增量调度 |
| git | 审计与回滚 |
| config/templates/ | 契约 Schema 与模板（校验唯一来源） |

---

## 7. 结构性边界备忘（影响结构的能力事实）

- **ACM 不承诺自动解题获奖** → 该方向在决策阶段只产出训练体系类蓝图（题解引擎/模板库/训练计划的重定位）
- **硬件物理装配与实测为人工环节** → 验收清单显式区分"agent 可验证项"与"人工测试项"
- **挑战杯类获奖作品正文稀缺** → KB-1 分析深度分级、标注信源等级，宁缺毋滥
- **各赛事 AI 使用政策不一**（美赛/Kaggle 等已有明确要求）→ 每个赛事条目维护 AI 政策字段，合规检查为蓝图必含章节

---

## 8. 待确认（清理于 2026-08-27 · T3-c）

1. ✅ 试点方向——部分落地：数模与时序预测已启用并完成首跑（6 卡 + 3 条目）；黑客松方向待启用
2. ✅ `config/profile.yaml`——已关闭（2026-08-27 用户口述、经确认落盘：3 人 CS 全栈队、RTX 4070 Laptop、ESP32/LattePanda/PIC18F、周投入高强度、预算 ~1000 元；美赛 M 奖 + 蓝桥杯国三等历史）
3. ⏸ 公众号信源策略——缓判（D5：挑战杯/创新创业类方向启用时再裁决，RSSHub 落 tools/ 本机跑）
4. ✅ 跑批预算上限——已关闭（T3-a 实测校准进 budget.yaml）
5. ⏸ ACM"训练系统"重定位——维持 §7 边界备忘
6. ✅ v1 单战役约束——已关闭（T3-a/T2 实践接受）
