# workspace/ —— 多战役容器（v2，2026-09-01）

**每个战役一个子目录** `workspace/<战役id>/`；多战役可并行（各自独立阶段与熔断计数）。
（`kaggriculture` 于 2026-09-01 从平铺布局迁入本结构，历史冻结证据的规范路径字符串经兼容层保持可验证。）

## 战役生命周期

```
init_state --campaign <cid> --phase decide    # 登记（自动建骨架）→ strategy-gen 产出 strategy/blueprint
  → 用户确认蓝图 → --phase deliver           # campaign-run 波次交付
  → --phase verify                            # accept-run 验收-修复回环
  → archive_campaign --campaign <cid>         # 归档移入 archive/ 并注销（--close）
```

## 单战役目录结构（workspace/<cid>/）

| 文件/目录 | 归属角色 | 说明 |
|---|---|---|
| `strategy.md` | Strategy | 对比矩阵 + 一鱼多吃路线（decide 态可写） |
| `blueprint.md` | Strategy | ★ 唯一蓝图契约，须过 blueprint.schema.json 校验 |
| `JOURNAL.md` | 协调者 | 本战役阶段流转日志（提交入库，可审计） |
| `metrics.json` | merge_metrics.py | 分片汇总生成物（角色禁写；分片在各角色目录下） |
| `software/` | Software | 代码 + 沙箱测试 + metrics 分片 |
| `hardware/` | Hardware | BOM / 引脚表 / 固件 + metrics 分片 |
| `docs/` | Document | 报告（Typst）+ PPT（Marp）源码 |
| `references/` | 抓取材料的角色 | ★ 外部参考资料/数据/第三方包的**唯一归宿**（rules/data/code/digests，登记见其 INDEX.md） |
| `acceptance/` | 验收 | 执行记录 / 失败工单 / 分析报告（交付期只读） |

## 多战役并行操作流程

各战役阶段、熔断计数、JOURNAL、metrics 完全独立；所有阶段流转与 verify 命令带 `--campaign <cid>`：

| 操作 | 命令 |
|---|---|
| 开新战役（建骨架，不影响在役战役） | `python scripts/guard/init_state.py --campaign <cid> --phase decide` |
| 阶段流转（某战役） | `python scripts/guard/init_state.py --campaign <cid> --phase deliver\|verify\|idle` |
| 指标汇总（某战役） | `python scripts/verify/merge_metrics.py --campaign <cid>` |
| 验收（某战役，retry 按战役计数） | `python scripts/verify/run_acceptance.py --campaign <cid>` |
| 归档（单战役，注销后其余不动） | `python scripts/verify/archive_campaign.py --campaign <cid>` |
| 注销战役（归档脚本自动调用） | `python scripts/guard/init_state.py --campaign <cid> --close` |
| 查看全局+各战役状态 | `/status`（会话启动时自动播报一行） |

单战役仓库可省 `--campaign`（自动选中唯一战役）；**两战役及以上并存时必须显式指定**。
全局阶段只有 `idle|collect`（慢循环用）；战役 id 规则 `^[a-z0-9][a-z0-9-]{0,31}$`，
不得占用 software/hardware/docs 等保留名。慢循环（/kb-sync、/discover）可与任何战役阶段并行。

## 现役战役

| 战役 id | 战役根 | 阶段 |
|---|---|---|
| `kaggriculture` | `workspace/kaggriculture/` | 见 /status（结构迁移后休眠于 idle） |

守卫按**最长 root 匹配**把写入路由到所属战役的阶段策略；`workspace/<未登记id>/` 一律拒写。
守卫策略与写入矩阵见 `scripts/guard/guard_path.py` 与 `docs/DESIGN.md` §6.2。
