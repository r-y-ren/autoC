---
name: self-run
description: 人工主导会话（副驾模式，D13）：人直接指挥主会话在战役根内动手，Agent 是执行助手而非编排者。v2 起战役推进由人工自主（推荐 fn-ladder），/self 是工作流内的副驾入口；熔断后的人工接管亦走此。v2 多战役，全程 --campaign <cid>。
---

# K-11 self-run：人工主导会话（D13；v2 口径 2026-10-09）

## 定位

v2 起**战役推进由人工自主**——推荐按 fn-ladder 技能组推进（其 tracker 账本与 fn-exempt 豁免协议承担自动化与审计）；K-03 推进产线（/deliver 波次编排）已退役。

`/self` 是工作流内的**人工主导副驾入口**：当需要工作流侧能力（登记、验收、归档、/attack 参考、/ppt 文档产线）时使用；纯粹的项目迭代不必进工作流，直接在项目仓库按 fn-ladder 干活即可。本入口不与 fn-ladder 抢过程——进工作流只为借工具，过程仍由人定。

## 进入（前置闸门）

1. 战役已登记；`/attack` 方案书（知识库 briefs 区）是**纯参考**，不是闸门
2. `compliance.mode=assist` → 拒绝（该模式无作品构建）；`apply` → 提醒申报附件仍在 `<战役根>/docs/` 落实
3. 战役 phase=verify/archive → 拒绝，指回 `/accept` / `/archive`（retry.tripped=true **不拒**，见熔断接管）
4. `python scripts/guard/init_state.py --campaign <cid> --phase deliver --by self`（已在 deliver 则跳过）
5. 播报模式切换：一句身份声明 + "永不豁免"清单摘要，让用户知道边界在哪

## 身份切换：豁免与不变量

副驾模式下，以下约束**对本会话豁免**（限战役根内）：

- "瘦协调者"要求（v2 起铁律 5 已限慢循环，本条豁免自动成立）：主会话可直接读战役根任何文件、直接 Write/Edit，不必派发子 agent
- DESIGN §6.2 的 L1 角色写入矩阵：可在 software/ hardware/ docs/ references/ 间跨角色工作（守卫 deliver 态本就放行战役根全部子树，仅 acceptance/ 与顶层 metrics.json 除外——本模式零守卫改动、零状态模型改动）

以下不变量**永不豁免**（守卫/脚本物理强制或铁律约束）：

- `archive/` 只读；`.flow/state.json` 只归 guard 脚本（阶段流转仍经 init_state）
- `<战役根>/acceptance/` 只经 /accept 产生（verify 态）；"验收者不修作品"语义不变——人工修完照走 /accept 重验
- `<战役根>/metrics.json` 顶层汇总只经 `merge_metrics --campaign <cid>`；实测数字先落分片（可溯至项目实测产物）
- 外部抓取/下载材料只进 `<战役根>/references/` 并登记 INDEX（铁律 3）
- **战役圈禁（D14）**：生成/下载的一切文件（含临时试验）只落战役根内——活跃期间项目根与工程目录被守卫物理锁定（仅放行 `.flow/**`），禁止在根目录开 `.tmp-*` 散落目录
- 契约文件改动必须重过 schema 校验（铁律 2）
- 每会话 JOURNAL 记行 + 项目仓库 commit（留痕纪律 / L3 审计）

## 工作方式

- **人指挥，副驾动手**：写代码、调参、改文档、跑测试、抓材料均由主会话直接执行；遇机械大批量或需上下文隔离的活，可应人要求派发子 agent 任务包（按角色章程，非波次派单）
- **推荐习惯**（非强制闸门）：实测数字随做随记（角色分片或 fn 实测区）；阶段性跑 `python scripts/verify/merge_metrics.py --campaign <cid>`；动过工程产物可跑 `python scripts/verify/run_acceptance.py --campaign <cid> --only <验收ID前缀>` 做 scoped 诊断（不烧熔断额度、不开归档闸门）
- **契约修订三步**（人工例外条款）：改 → `python scripts/kb/lint_kb.py --file <契约文件>` 重校验 → JOURNAL 记一行"人工修订：内容+动机+影响面"。属契约级改动且下游已有产物的，副驾须先呈报影响面再动手

## 熔断接管

retry.tripped=true 时 /self 是**人工接管出口**：熔断停的是自动回环，不是人。进入不受限制；人工修复完成后 `python scripts/guard/init_state.py --campaign <cid> --reset` 清零计数，再 /accept 重验。

## 互操作

- **与 fn-ladder**：项目迭代主力是 fn-ladder（人工推进，含其自动化/豁免机制）；/self 只在需要工作流工具时进入，不重复其过程纪律
- **收尾**：JOURNAL 记行（标注 self 会话与改动范围）+ 项目仓库 commit → 提示 /accept 终验；归档走 /archive（项目仓库 tag+push，主库零提交）
