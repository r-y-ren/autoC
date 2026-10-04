# exports/probes 入库策略（R18 显式化）

> 生成：fn_work/src/sync_documentation/codify_probes_policy.py（B14，2026-09-22T02:35:35+08:00）。
> 适用面：software/exports/probes/**（旧树只读——.gitignore 的物理修正战后套用）。

## 策略规则

- P1 结论 .md 全入库：exports/probes/** 下的评估摘要/勘误/法证结论（*.md）一律 git 入库
- P2 数据中间物 gitignore：JSON 产物/引擎缓存/回放大文件等数据中间物不入库
- P3 引擎与源数据归 references/data（既有大文件规则，本策略不改其归宿）

## 现存摘要一致性核对

| # | 摘要（战役根相对） | 入库 | bytes |
|---|---|---|---:|
| 1 | software/exports/probes/planner_bench/round23_loss_forensics.md | 是 | 17142 |
| 2 | software/exports/probes/planner_bench/round24_loss_forensics.md | 是 | 22739 |
| 3 | software/exports/probes/planner_bench/v31_pressure_calibration_summary.md | 是 | 6475 |
| 4 | software/exports/probes/planner_bench/v3_readmission_summary.md | 是 | 3775 |
| 5 | software/exports/probes/v143_sellrace/v143_sellrace_summary.md | 是 | 7526 |
| 6 | software/exports/probes/v15_ignition/v15_ignition_summary.md | 是 | 4614 |

- **现存态**：6 份结论摘要全部 git 在册（P1 现存态一致；规则面缺口见下）。
- **数据中间物**：4 件在盘未跟踪（如 twin_fidelity/engine_cache）——P2 一致。

## 不一致清单（规则面缺口，旧树冻结故登记待战后）

- .gitignore 模式 ['workspace/kaggriculture/software/exports/probes/*', '!workspace/kaggriculture/software/exports/probes/README.md'] 仅回白 README.md——未来新增结论 .md 将被忽略（git check-ignore 实证 exit 0），与 P1『结论 .md 全入库』不一致

## 战后动作

- postwar_action: 战后把 exports/probes 白名单补为 !**/*.md（或目录级规则），套用前新增摘要须手工 git add -f
