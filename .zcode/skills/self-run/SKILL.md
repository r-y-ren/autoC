---
name: self-run
description: 人工主导交付会话（副驾模式，D13）：蓝图确认后由人直接指挥主会话在战役根内动手，Agent 是执行助手而非编排者。用户执行 /self 进入时使用；熔断后的人工接管亦走此入口。v2 多战役，全程 --campaign <cid>。
---

# K-11 self-run：人工主导交付会话（D13，2026-09-02）

## 定位

`/deliver` 与 `/self` 是蓝图确认后的**姊妹入口**：同处 deliver 阶段、共享同一套 L2 守卫边界与验收出口，只差"谁在干活"。

| | /deliver（K-03） | /self（K-11） |
|---|---|---|
| 主会话身份 | 编排者（瘦协调者，派发子 agent） | **副驾**（直接读写战役根，听人指挥） |
| 推进结构 | 波次拓扑分层 + 波门五查 | 人定粒度与顺序，无强制波门 |
| 蓝图 | 禁改（问题回 /attack 重新确认） | 可改（改必校验 + 留痕 + 影响评估） |

两者可随时互换续跑（见互操作）；终验一律走 /accept 全量清单。

## 进入（前置闸门）

1. 战役已登记；`<战役根>/blueprint.md` 存在且过 schema 校验（缺失/不过 → 指 `/attack`）
2. `compliance.mode=assist` → 拒绝（该模式无作品构建）；`apply` → 提醒申报附件仍在 `<战役根>/docs/` 落实
3. 战役 phase=verify/archive → 拒绝，指回 `/accept` / `/archive`（retry.tripped=true **不拒**，见熔断接管）
4. `python scripts/guard/init_state.py --campaign <cid> --phase deliver --by self`（已在 deliver 则跳过）
5. **确认语义**：执行 /self 即视为用户对该蓝图的人工确认（此后蓝图改动属"人工修订"，不再回 /attack 重新呈报）
6. 播报模式切换：一句身份声明 + "永不豁免"清单摘要，让用户知道边界在哪

## 身份切换：豁免与不变量

副驾模式下，以下约束**对本会话豁免**（限战役根内）：

- 铁律 5 的"瘦协调者"要求：主会话可直接读战役根任何文件、直接 Write/Edit，不必派发子 agent
- DESIGN §6.2 的 L1 角色写入矩阵：可在 software/ hardware/ docs/ references/ 间跨角色工作（守卫 deliver 态本就放行战役根全部子树，仅 acceptance/ 与顶层 metrics.json 除外——本模式零守卫改动、零状态模型改动）
- K-03 的波次编排与波门五查：不强制分层、不强制并行派发、不强制波门节奏

以下不变量**永不豁免**（守卫/脚本物理强制或铁律约束）：

- `archive/` 只读；`.flow/state.json` 只归 guard 脚本（阶段流转仍经 init_state）
- `<战役根>/acceptance/` 只经 /accept 产生（verify 态）；"验收者不修作品"语义不变——人工修完照走 /accept 重验
- `<战役根>/metrics.json` 顶层汇总只经 `merge_metrics --campaign <cid>`；实测数字先落角色分片（铁律 4）
- 外部抓取/下载材料只进 `<战役根>/references/` 并登记 INDEX（铁律 3）
- **战役圈禁（D14）**：生成/下载的一切文件（含临时试验）只落战役根内——活跃期间项目根与工程目录被守卫物理锁定（仅放行 `.flow/**`），临时试验放 `references/digests/` 或角色目录，禁止在根目录开 `.tmp-*` 散落目录
- 蓝图等契约文件改动必须重过 schema 校验（铁律 2）
- 每会话 JOURNAL 记行 + 项目仓库 commit（铁律 6 / L3 审计）

## 工作方式

- **人指挥，副驾动手**：写代码、调参、改文档、跑测试、抓材料均由主会话直接执行；遇机械大批量或需上下文隔离的活，可应人要求按 K-03 章程派单个角色任务包（副驾不排斥按需派发）
- **推荐习惯**（非强制闸门）：角色分片 metrics 随做随记；阶段性跑 `python scripts/verify/merge_metrics.py --campaign <cid>`；动过工程产物可跑 `python scripts/verify/run_acceptance.py --campaign <cid> --only <验收ID前缀>` 做 scoped 诊断（不烧熔断额度、不开归档闸门）
- **蓝图修订三步**（人工例外条款）：改 → `python scripts/kb/lint_kb.py --file <战役根>/blueprint.md` 重校验 → JOURNAL 记一行"人工修订：内容+动机+影响面"。属契约级改动（接口/目录/验收线）且下游已有产物的，副驾须先呈报影响面再动手

## 熔断接管

retry.tripped=true 时 /self 是**人工接管出口**：熔断停的是自动回环，不是人。进入不受限制；人工修复完成后 `python scripts/guard/init_state.py --campaign <cid> --reset` 清零计数，再 /accept 重验。

## 互操作

- **self → deliver**：新会话 /deliver 按蓝图波次续跑；波门会重查该波可编译/测试/验收左移，天然兜住人工改动的回归
- **deliver → self**：自动交付任意断点可转人工（直接 /self 进入；波门断点状态查 JOURNAL）
- **收尾**：JOURNAL 记行（标注 self 会话与改动范围）+ 项目仓库 commit → 提示 /accept；阶段停留在 deliver，由 /accept 切 verify
