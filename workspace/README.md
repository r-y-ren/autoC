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

## 现役战役

| 战役 id | 战役根 | 阶段 |
|---|---|---|
| `kaggriculture` | `workspace/kaggriculture/` | 见 /status（当前 deliver） |

守卫按**最长 root 匹配**把写入路由到所属战役的阶段策略；`workspace/<未登记id>/` 一律拒写。
守卫策略与写入矩阵见 `scripts/guard/guard_path.py` 与 `docs/DESIGN.md` §6.2。
