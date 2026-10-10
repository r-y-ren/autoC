# contest-compass — 竞赛情报与参考方案工作区（v2）

面向**学科竞赛**（挑战杯/互联网+/大创/数模）与**编程/黑客松**（ACM/Kaggle/黑客松）两大类的工作区。
**v2 边界（2026-10-09 起）**：工作流**不指挥战役推进**——作品与项目迭代由**人工按
[fn-ladder](~/.zcode/cli/plugins/cache/fn-ladder) 技能组自主推进**（其 tracker 账本与 fn-exempt
豁免协议承担自动化与审计）；工作流提供四样东西：**KB 自动化**、**参考方案供给（/attack）**、
**文档产线（/ppt 两段式）**、**登记与归档支持**。

| 交付物 | 位置 | 生成方式 |
|---|---|---|
| ① 赛事知识库（名单/规则/获奖解构/模式库） | `kb/competitions/` | **全自动**，增量维护 |
| ② 前沿科技库（技术卡片 + 同族综述） | `kb/tech/` | **全自动**，增量维护 |
| ③ 参考方案书（赛事/方案/技术栈三节，纯参考） | `kb/briefs/` | `/attack` 生成，**不影响推进** |
| ④ 文档产线（答辩 PPT 两段式、报告） | 模板资产 + 取材器 | `/ppt` 生成，数字逐项可溯 |
| ⑤ 战役作品（代码/文档/实测） | `workspace/<cid>/` **独立 git 仓库** | 人工按 fn-ladder 推进 |

深入文档：[DESIGN.md](docs/DESIGN.md)（结构设计）｜[CAPABILITIES.md](docs/CAPABILITIES.md)（能力登记）｜
[ENVIRONMENT.md](docs/ENVIRONMENT.md)（工具链）｜[AGENTS.md](AGENTS.md)（全局铁律与 v2 运行边界）｜
[repo-split-handoff.md](docs/repo-split-handoff.md)（多库布局与两机交接）

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

多库布局（git 拆分后）：主库只装工作流；各战役/产物在 `r-y-ren/contest-compass-*` 系列独立仓库。
新机器接手：`python scripts/maint/repo_split.py adopt`（见交接清单）；新战役登记后立即
`python scripts/maint/repo_split.py bootstrap --path workspace/<cid> --push` 建项目库。

可选工具链（对应类型作品启用时才需要）：marp-cli + typst（文档/PPT）、PlatformIO + KiCad +
OpenSCAD + wokwi-cli（硬件）、Tesseract（OCR）。gh 已登录则 GitHub 信源自动启用。

## 二、日常使用（人类视角）

| 命令 | 什么时候用 | 会发生什么 |
|---|---|---|
| `/status` | 随时 | 状态卡：登记战役/归档态势/最近日志 |
| `/discover <方向描述>` | 想启用一个**新方向** | 全自动冷启动：赛事名单 → 首批条目 → 锚点回填 → 方向全景报告 |
| `/kb-sync` | 手动补一次增量（cron 之外的补偿入口） | 轻量增量：拉候选 → 分片入库 → lint → 索引 |
| `/attack [赛事ID或方向]` | **想打比赛、要参考方案** | 对比矩阵 + 三节方案书落 `kb/briefs/`（纯参考；`--to` 可复制进项目） |
| `/accept <战役id>` | 项目要终检（可选工具） | 执行验收清单（cmd 自动执行+取证），失败开单回人工修复（熔断按战役独立；人工修复后复位清零再重验） |
| `/ppt <战役id>` | 验收通过后、归档前（可选） | 两段式：取材器+模板自动出初稿（数字带来源）→ 精修可选（ppt-master / 人工改稿 / edit-native） |
| `/archive <战役id>` | 验收通过后 | 固化进 archive/（项目仓库 tag+push，主库零提交）并注销 |

**项目迭代不走工作流**：直接在项目仓库按 fn-ladder 干活（fn-grill → fn-divide → fn-scaffold →
fn-implement → fn-close；自动化与豁免走 fn-exempt 记账）。`/deliver` 推进产线已于 v2 **退役**。

**读知识库的正确姿势**：人不逐条读 `kb/`（那是 agent 的检索界面）——读 `export/digest-*.md`
方向情报简报；`kb/INDEX.md` 是总索引；参考方案书在 `kb/briefs/`。

## 三、慢循环（全自动，无需人管）

- **单一 cron**：每 3 天 09:00 全量深度跑批＝增量拉取 → 候选分片入库 → 老化重验 → 隔离处置 →
  winners/patterns 解构 → 综述必查 → lint → 索引重建 → 简报刷新 → git push 备份 → 收尾断言。
- 留痕三件：`kb/INDEX.md` 跑批表（append-only，含成本列）、`workspace/JOURNAL.md`、git log。
- 新方向入口唯一：`/discover`（自动建 `config/directions/<方向>.yaml` + 首跑 + 锚点回填）。

## 四、战役与项目（v2：人工推进）

```
/attack ──► kb/briefs/ 三节方案书（纯参考，不影响推进）
                     │  你取用参考
                     ▼
        项目仓库 workspace/<cid>/  ──► 人工按 fn-ladder 迭代（tracker+fn-exempt）
                     │
                     ▼
        /accept 可选终检 ──► /ppt 两段式产稿 ──► /archive 固化（项目仓库 tag+push）
```

**登记与归档记账**（工作流侧仅存的战役事务）：

```bash
# 新战役：登记 + 建项目库（bootstrap 入清单并 push）
python scripts/guard/init_state.py --campaign newcup-2026 --phase deliver
python scripts/maint/repo_split.py --remote-base https://github.com/r-y-ren bootstrap --path workspace/newcup-2026 --push

# 终检与归档（可选；均带 --campaign）
python scripts/verify/run_acceptance.py --campaign newcup-2026
python scripts/verify/archive_campaign.py --campaign newcup-2026
```

- **阶段流转必须带 `--campaign`**；单战役可省（自动选中），多战役并存必须显式。
- **三个在役战役登记冻结**（2026-10-09）：推进/验收状态不再维护，归档支持保留。
- 战役 id 规则：小写字母数字连字符；战役目录只能经 `init_state --campaign` 创建。

## 五、配置速查（`config/`）

| 文件 | 管什么 | 何时改 |
|---|---|---|
| `directions/<方向>.yaml` | 方向的关键词/信源锚点/技术雷达 fields | `/discover` 自动建 |
| `budget.yaml` | 并发/配额/重试/熔断阈值 | 调跑批节奏时 |
| `profile.yaml` | 团队画像 | 队伍情况变化时 |
| `repo_split_repos.json` | 多库清单（新机器 adopt 的事实源） | bootstrap 自动追加 |
| `templates/` | Schema 与文档模板（含 PPT 资产层 `templates/ppt/`） | 模板是反幻觉契约：走模板变更，不许绕过 |

## 六、治理速览（为什么会拒绝你）

- **六阶段**：`idle/collect/decide/deliver/verify/archive`——写入路径守卫按阶段拦截；
  `archive/` 与 `.flow/state.json` 永远只读；阶段只能经 `init_state.py` 流转。
- **三层防线**：角色章程（软）→ 守卫+Schema 硬校验 → git 审计兜底（主库审计流程面、项目库审计产物面）。
- **引用纪律**：KB 一切分析基于本次实抓、逐条带 URL+日期；方案书纯参考、不得充当推进契约；
  实测数字须可溯至项目实测产物。
- **流程面纪律**：`.zcode/`、`config/`、`scripts/`、`docs/`、AGENTS.md 变更必须独立成提交，禁止夹带于战役提交。

## 七、故障排查

| 症状 | 处置 |
|---|---|
| 写文件被 `[guard_path] 阻断` | 阶段不对——看 `/status`；或路径本就只读 |
| 条目进了 `kb/quarantine/` | 看 `.reason` 文件修复后重写（勿手工移回） |
| 验收重试超限熔断 | 停止重试升级人工——看 `workspace/<cid>/acceptance/` 证据，人工修复后 `init_state --campaign <cid> --reset` |
| cron 跑批疑似没动 | 查 `workspace/JOURNAL.md` 与 `kb/INDEX.md` 跑批表末行（warn 行说明原因） |
| 想看某事实的依据 | 条目 frontmatter `sources` 逐条带 URL+抓取日期；快照在 `kb/raw/<id>/` |

## 八、测试与维护

```bash
python scripts/guard/test_guard.py                 # 守卫回归
python scripts/kb/test_lint.py && python scripts/kb/test_index.py && python scripts/kb/test_inbox.py
python scripts/verify/test_acceptance.py           # 验收器回归
python scripts/verify/test_archive.py              # 归档闸门回归
python scripts/maint/test_repo_split.py            # 拆分迁移器回归
python scripts/maint/test_doc_lint.py              # 文档一致性检查器回归
python scripts/ppt/test_collect_deck_material.py   # PPT 取材器+装配回归（含 e2e）
python scripts/kb/lint_kb.py                       # 全量契约校验
python scripts/maint/doc_lint.py                   # 工作流文档一致性（R1-R4）
```

## 九、项目状态（2026-10-10）

- ✅ v1 时代：契约/编排/跑批/能力补全/硬件工具链/内容框架全量落地；两次 git 拆分（产物出主库 + v2 瘦身）
- 📈 运营中：双方向知识库（34 赛事条目 + 301 技术卡）由 cron 每 3 天自主生长；多库远程
  [r-y-ren/contest-compass](https://github.com/r-y-ren/contest-compass) 系列
- 🧭 v2 边界：推进归人工（fn-ladder）；工作流管 KB + 参考供给 + 文档产线 + 登记/归档记账
