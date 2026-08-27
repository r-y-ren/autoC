# autoC — 竞赛情报与作品生成 Agent 框架·使用手册

面向**学科竞赛**（挑战杯/互联网+/大创/数模）与**编程/黑客松**（ACM/Kaggle/黑客松）两大类的自动化工作区：
自动收集你指定方向的赛事情报、解构历年获奖作品、追踪前沿科技；在你确认方向后，全自动产出
攻略 + 完整作品 + 分析报告。

| 交付物 | 位置 | 生成方式 |
|---|---|---|
| ① 赛事知识库（名单/规则/获奖解构/模式库） | `kb/competitions/` | **全自动**，增量维护（不重新生成） |
| ② 前沿科技库（技术卡片：用途/优势/比赛映射 + 同族综述） | `kb/tech/` | **全自动**，增量维护 |
| ③ 指定作品库（攻略/作品/分析报告，每场战役一套） | `workspace/` → `archive/` | 用户确认方向后**全自动**，归档不可变 |

深入文档：[DESIGN.md](docs/DESIGN.md)（结构设计）｜[CAPABILITIES.md](docs/CAPABILITIES.md)（能力登记与 D1–D10 裁决）｜[ENVIRONMENT.md](docs/ENVIRONMENT.md)（工具链版本）｜[AGENTS.md](AGENTS.md)（全局铁律）

---

## 一、首次使用（环境准备）

```bash
# 1. 依赖（系统 Python 3.14，一次性）
python -m pip install pyyaml jsonschema pypdfium2 pdfplumber pillow

# 2. 守卫引导（.flow/ 不入库；缺状态时写入守卫 fail-closed 全只读，必须先跑这步）
python scripts/guard/init_state.py

# 3. 自检（应全绿）
python scripts/guard/test_guard.py && python scripts/kb/lint_kb.py
```

可选工具链（对应类型作品启用时才需要，均已在 ENVIRONMENT.md 登记版本与路径）：
marp-cli + typst（文档/PPT）、PlatformIO + KiCad + OpenSCAD + wokwi-cli（硬件）、Tesseract（扫描件 OCR）。
gh 已登录则 GitHub 信源自动启用；WOKWI_CLI_TOKEN 已配置则固件仿真断言可用。

## 二、日常使用（人类视角）

**你只需要记住六个斜杠命令：**

| 命令 | 什么时候用 | 会发生什么 |
|---|---|---|
| `/status` | 随时 | 状态卡：当前阶段/战役/重试计数/最近日志 |
| `/discover <方向描述>` | 想启用一个**新方向**（如"挑战杯类创新创业"） | 全自动冷启动：搜索该方向赛事名单 → 建首批条目（≤8 条）→ 回填信源锚点 → 产出方向全景报告。全程无需确认 |
| `/kb-sync` | 想手动补一次增量（cron 之外的补偿入口） | 轻量增量：拉候选 → 分片入库 → lint → 索引 |
| `/attack [赛事ID或方向]` | **想打比赛了**——指定比赛，或省略参数直接问建议 | 见下文快循环详解 |
| `/accept` | 交付完成后（或 campaign 提示时） | 执行蓝图验收清单，失败自动开单修复回环 |
| `/archive` | 验收通过后 | workspace 固化进 archive/（git tag），工作区复位 |

**读知识库的正确姿势**：人不逐条读 `kb/`（那是 agent 的检索界面）——读 `export/digest-<方向>-<月>.md`
方向情报简报（每 3 天自动刷新，月末转正式版）：赛事日历倒计时、技术雷达速览、模式库要点、合规提醒。
`kb/INDEX.md` 是总索引；`kb/README.md` 是库结构导览。

## 三、慢循环（全自动，无需人管）

- **单一 cron**：每 3 天 09:00 全量深度跑批（K-08 流程）＝增量拉取（arXiv+gh+锚点）→ 候选分片入库
  → 老化条目重验（>12 天）→ 拒绝台账复核 → 隔离区处置 → winners/patterns 解构推进（配额 1 年份片/轮）
  → `_surveys` 综述必查 → 结构 WARN 消化 → lint → 索引重建 → 简报刷新 → **git push 自动备份** → 收尾断言。
- 全过程留三条审计痕迹：`kb/INDEX.md` 跑批表（append-only，含成本列）、`workspace/JOURNAL.md`、git log。
- 无人值守自愈设计：跑前预检（git 干净/阶段正确）、跑后断言（阶段回 idle/登记齐全），异常记 warn 行不静默。
- 新方向的进入方式只有一条：`/discover`（自动建 `config/directions/<方向>.yaml` + 首跑 + 锚点回填）。

## 四、快循环（战役，一次确认后全自动）

```
/attack ──► 刷新KB ──► K-02 决策 ──► ★你确认蓝图（全流程唯一人工闸门）
                                          │
              ┌───────────────────────────┤
              ▼                           ▼
        并发交付 K-03                （不认可则改蓝图再确认）
        software ∥ hardware
              ──► metrics 汇总 ──► document（报告/PPT）
              ──► /accept K-04：断言式验收（cmd 自动执行+browser-use 取证）
                    │失败→工单路由回责任角色修复→重验（仅 fail 计数，≥3 熔断升级人工）
                    │通过
                    ▼
              /archive K-05：archive/<YYYY-MM_赛事_主题>/ + git tag，workspace 复位
```

**四种典型用法：**

1. **问建议**（没想好打什么）：直接 `/attack`——产出四块固定格式：六维矩阵（每格一句证据+证据强度）、
   大显身手信号行（近 90 天 KB-2 新卡 × 该赛 patterns 的命中）、一鱼多吃路线图、**明确推荐第一名+理由**。
   数据不足的维度会如实降权告知，不硬推。
2. **指定比赛**：`/attack cumcm`——跳过矩阵直接进蓝图。
3. **确认时看什么**：strategy.md（攻略六节）+ blueprint 要点（范围/技术选型/接口契约/验收清单/合规模式）。
4. **合规模式**（蓝图必带，schema 硬校验）：`prep` 赛前范本级（默认，数模类必须）/ `apply` 申报制参赛型
   （AI 政策允许范围内构建，申报附件强制进交付）/ `assist` 赛中支持型（零介入，不会启动作品构建）。

**作品质量底线**（写进验收默认线，不达不通过）：软件"完整可实用"四标准（可运行/可验证/可维护/可交付——
交付物逐项对齐赛方清单）；硬件编译+仿真断言过、物理项列 MANUAL_TEST 移交人工；文档数字只能引 metrics.json。

## 五、配置速查（`config/`）

| 文件 | 管什么 | 何时改 |
|---|---|---|
| `directions/<方向>.yaml` | 方向的关键词/信源锚点/技术雷达 fields | `/discover` 自动建；锚点跑批自动回填 |
| `budget.yaml` | 并发/配额/重试/**熔断阈值**——数字唯一事实源 | 调跑批节奏时（改动会体现在下轮成本观测） |
| `profile.yaml` | 团队画像（技能/算力/设备/时间/历史） | 队伍情况变化时 |
| `sources/catalog.md` | 框架级信源目录 + **SPA 站点清单与预抓规则** | 发现新信源时 |
| `templates/` | 15 件 Schema 与文档模板（蓝图/攻略/分析报告/winners/patterns/survey/验收 cmd/CUMCM 论文/BP 骨架…） | 模板是反幻觉契约：要改结构走模板变更，不许绕过 |

## 六、治理速览（为什么会拒绝你）

- **六阶段**：`idle/collect/decide/deliver/verify/archive`——写入路径守卫按阶段拦截（Write/Edit 钩子），
  `archive/` 与 `.flow/state.json` 永远只读；阶段只能经 `init_state.py` 流转。
- **三层防线**：角色章程（软）→ 守卫+Schema 硬校验 → git 审计兜底。
- **引用纪律**：KB 一切分析基于本次实抓、逐条带 URL+日期；搜索快照禁作唯一事实源（SPA 站点走主会话预抓）。

## 七、故障排查

| 症状 | 处置 |
|---|---|
| 写文件被 `[guard_path] 阻断` | 阶段不对——看 `/status`；该动作应在对应阶段做，或路径本就只读 |
| 条目进了 `kb/quarantine/` | 看 `.reason` 文件修复后重写（勿手工移回）；下轮跑批也会处置 |
| 验收重试 ≥3 触发熔断 | 自动停止重试升级人工——看 `workspace/acceptance/` 失败证据与工单，人工决策后 `init_state --reset` |
| cron 跑批疑似没动 | 查 `workspace/JOURNAL.md` 末行与 `kb/INDEX.md` 跑批表末行（warn 行会说明原因）；预检失败会如实记录 |
| 想看某事实的依据 | 条目 frontmatter `sources` 逐条带 URL+抓取日期；快照在 `kb/raw/<id>/` |

## 八、测试与维护

```bash
python scripts/guard/test_guard.py        # 守卫回归（16 用例）
python scripts/kb/test_lint.py            # lint 回归（12）
python scripts/kb/test_index.py           # 索引 append-only 回归
python scripts/verify/test_acceptance.py  # 验收器回归（6）
python scripts/verify/test_archive.py     # 归档闸门回归（4）
python scripts/kb/lint_kb.py              # 全量契约校验（含正文层结构 WARN）
python scripts/kb/lint_kb.py --structure  # 只看正文层结构
```

## 九、项目状态（2026-08-28）

- ✅ Phase 0 / T1 契约 / T2 编排与脚本 / T2.1 修复轮 / T3-a 首次真实跑批 / T3-c 能力补全（OCR·patterns·文档链）
  / T3-d 硬件工具链 / T3-e profile+Wokwi 断言 / T4 内容框架（批次1 框架件 + 批次2 黑客松方向泛化实证）
  / T4.1 工作流完善 / T4.2 第三类细节（D10 四裁决）/ T4.3 改进轮（远程备份·结构 lint·成本观测）
- 📈 运营中：双方向知识库（11 赛事条目 + 6 技术卡）由 cron 每 3 天自主生长；远程 [r-y-ren/autoC](https://github.com/r-y-ren/autoC) 自动备份
- ⏸ 按裁定暂缓：快循环整链真实执行（`/attack` 待命）；按需触发：RSSHub（挑战杯方向）、Kaggle API、wokwi-mcp（首个硬件蓝图）
