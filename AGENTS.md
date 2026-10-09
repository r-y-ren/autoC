# autoC 全局纪律（AGENTS.md）

本文件对本仓库内所有会话与子 agent 生效。结构设计见 `docs/DESIGN.md`，两者冲突时以本文的"铁律"为准。

## 身份与地图

本仓库是"竞赛情报与作品生成 Agent 框架"的工作区：慢循环维护两座知识库（`kb/`），快循环按战役交付作品（`workspace/` → `archive/`）。

| 分区 | 职责 | 写入规则 |
|---|---|---|
| `.zcode/` | 客户端原生配置（钩子/技能/子agent） | 随工程演进 |
| `.flow/` | 运行时状态（gitignore） | **仅脚本可写** |
| `config/` | 静态配置与契约 Schema | 全局 idle 且无活跃战役可改（D14 圈禁） |
| `scripts/` | 确定性脚本（kb/guard/verify） | 全局 idle 且无活跃战役可改（D14 圈禁） |
| `kb/` | 知识库（清洗后的轻量 Markdown） | collect 态经跑批写入 |
| `workspace/` | 多战役容器（每战役 `workspace/<cid>/` 子目录，独立阶段与熔断；**每战役独立 git**，见下方仓库布局） | 按各战役阶段/角色受限（最长 root 匹配） |
| `export/` | KB 交付导出层（S-15 纯投影，D6；独立 git） | 脚本生成，人读 |
| `archive/` | 历史作品库（归档目录携带自身 `.git` 与 `archive/…` tag） | **永远只读**（主库不收归档提交） |

**仓库布局（2026-10-09 git 拆分，spec r-y-ren/autoC#2）**：主库只跟踪流程面（`.zcode/`、`config/`、`scripts/`、`kb/` 清洗层、`docs/`、本文件）；`workspace/<cid>/`、`export/`、`kb/raw/`、`archive/<归档名>/` 各带**独立 git 与 GitHub 远程**（`r-y-ren/autoC-*` 系列），产物提交一律落所属项目仓库，主库仅在工作流面变更时 commit。大文件维持本机留存不入库（继承既有忽略口径）；第二台机器经 `python scripts/maint/repo_split.py adopt` 收敛项目库（保留本机未跟踪大件）。

## 六条铁律

1. **引用纪律**：KB 中的一切分析必须基于本次实抓的文档，逐条携带 `来源 URL + 抓取日期`。禁止凭模型记忆撰写获奖分析或赛事信息。唯一受控例外（2026-09-16 引入）：vault-distill 一次性提炼跑批的产物卡允许 sources 使用 paper-distill 形态（论文标题 + `distilled_from` + `distilled_date`，DOI/URL 尽力从 Zotero bib 回填）——该放宽仅限此跑批，不得泛化到常规采集与建卡。
2. **契约纪律**：`<战役根>/blueprint.md`、KB 条目、验收记录必须通过 `config/templates/*.schema.json` 校验；蓝图未过校验不得请求用户确认。
3. **写入纪律**：尊重 `scripts/guard/guard_path.py` 的**阶段级**写入策略与角色写入矩阵（DESIGN.md §6.2；角色目录级边界属 L1 软约束；多战役按最长 root 匹配路由到所属战役的阶段）。被守卫阻断时，修正自己的目标路径，不要绕道 Bash 写入来规避——Bash 写入同样会被 git 审计（L3）追责（拆分后口径：主库审计流程面，各项目库审计产物面，写入哪个分区由哪个仓库记账）。`archive/` 与 `.flow/state.json` 对 agent 永远只读；`workspace/<未登记id>/` 不得创建（战役登记只能经 `init_state --campaign`）。战役中抓取/下载的外部参考资料与数据（规则、数据集、第三方包、情报摘要）**只能**放该战役 `references/` 对应子目录并在其 INDEX.md 登记来源，禁止散落到工程目录。**战役圈禁（D14）**：战役生成/下载的一切文件（代码、数据、工件、临时文件）只许落在所属战役根 `workspace/<cid>/` 内，**禁止在项目根或工程目录生成/下载战役相关文件**——任一战役活跃期间（decide/deliver/verify/archive）守卫对工程面与项目根物理锁定（仅放行 `.flow/**`），绕道 Bash 亦会被 L3 审计追责（按所在仓库记账）。
4. **数据纪律**：对外文档中的一切性能数字只能来自所属战役 `<战役根>/metrics.json` 的实测值，禁止编造或"合理估计"数字。
5. **上下文纪律**：主会话是瘦协调者——只读 `kb/INDEX.md` 与各契约文件，不整读 `kb/raw/` 与条目正文；收集/分析任务按条目分片派发子 agent；子 agent 返回结构化结论而非原始转储。
6. **阶段纪律**：每完成一个阶段在所属战役 `JOURNAL.md` 记录一行，并在**项目仓库** git commit + 立即 push（主库不为阶段提交）；阶段流转只能经 `init_state.py`（战役级流转带 `--campaign <cid>`；熔断计数为战役级，各战役独立）；验收-修复回环超过 `retry.max` 次必须熔断升级人工，不得继续重试。

## 人工主导会话（/self）

蓝图确认后的交付期有两条并行入口：`/deliver`（自动编排，K-03）与 `/self`（人工主导，K-11）。经 `/self` 进入的会话，主会话身份为**副驾**：铁律 5 的"瘦协调者"约束与 DESIGN.md §6.2 角色写入矩阵对该会话**限战役根内豁免**——可直接读写战役根任意子树、跨角色目录工作、不强制波次编排；蓝图可改，但**改必重过 schema 校验并在 JOURNAL 留痕**。其余铁律与 L2 物理边界一概不豁免（`archive/` 只读、`.flow/state.json` 只归脚本、`acceptance/` 只经 /accept、顶层 `metrics.json` 只经 merge_metrics、references/ 归宿、实测数字纪律）；终验仍走 /accept 全量清单。熔断后的人工接管亦走 /self。规程见 `.zcode/skills/self-run/SKILL.md`。PPT 阶段（/accept 通过后、/archive 前）的姊妹副驾入口为 `/ppt-self`（K-13，豁免限该战役 docs 子树）；正式答辩 PPT 唯一产线为 `/ppt`（K-12，Marp 仅波内草稿）。

## 多机协作（接力纪律，2026-09-16）

仓库由两台电脑接力维护；`.flow/state.json` 是本机文件，两机互不同步，交接以远程为唯一事实源：

- 开工前主库与当前在干的项目库分别 `git pull --rebase`；每完成一个阶段在**项目仓库** commit 后**立即 push**；`/archive` 的 `archive/…` tag 由脚本落项目仓库并自动 push（脚本 warn 时手动 `git push --tags` 补推），主库不收归档提交。
- 分工并行安全对：一台跑 KB 维护（collect 态写 `kb/**`）+ 一台做战役（写 `workspace/<cid>/**`）——子树不相交，允许同时开工；其余情形按接力处理。
- `kb-deep-sync` 的 cron 全局只在一台主力机启用；换主力机时迁移，间歇期用 `/kb-sync` 手动补偿。
- 契约变更（`config/templates/*.schema.json`、`.zcode/` 技能/子agent/命令、scripts 行为契约）时 bump `config/contract_version.yaml` 并随变更 commit+push；开工前跑 `python scripts/guard/contract_check.py`（本地 vs 上游版本，不一致即先 pull/push；多库拆分后"上游"仅指**主库**上游，契约版本只随主库走），SessionStart 播报契约版本与插件可用性，错配开机即见。
- `kb/inbox/` 为外来资料本机暂存区（gitignore，仅 README 入库）：消费发生在 kb-sync/kb-deep-sync 跑批内，消化产物才入库；跨机资料转移等本机跑批消化或走其他通道。

## 合规底线

每个赛事条目必须维护 `ai_policy` 字段；作品按"AI 辅助原创"标准产出并在归档时保留人机分工记录。禁止生成违反目标赛事规则的提交策略。

## 边界备忘

ACM 方向不承诺自动解题获奖（只出训练体系类蓝图）；硬件物理测试项列入人工测试项移交用户；挑战杯类二手信源分析必须标注信源等级，宁缺毋滥。
