# 接口契约：software ↔ document（chuangxin2026）

> 蓝图 interface_contracts 指向本文件；并发分发前修订钉死，变更须在 JOURNAL 留痕。

## 1. 数据流（software → document）

| 交付物 | 来源 | 格式 | 消费方 |
|---|---|---|---|
| 性能数字 | `workspace/chuangxin2026/metrics.json`（merge_metrics 唯一入口） | JSON 键值 | 计划书 §技术方案、PPT 指标页 |
| 截图素材 | `workspace/chuangxin2026/software/exports/shots/` | PNG（命名 `m<里程碑>-<功能>.png`） | 计划书、PPT |
| 评测表 | `software/scripts/eval_forecast.py` / `eval_agent.py` stdout JSON | JSON | 计划书附录 |

## 2. 硬约束

1. document 角色**只允许**消费上表路径的数字/素材；对外文档出现任何表外数字 = 验收失败（铁律 4）。
2. metrics 键清单在 m0 里程碑冻结：`forecast_{品类}_mape`、`forecast_{品类}_coverage90`、`agent_e2e_pass_rate`、`sim_steps_total`（增删须 JOURNAL 留痕）。
3. 计划书/PPT 源文件放 `workspace/chuangxin2026/docs/`，构建入口 `docs/build.py`（m3 交付可编译产物）。

## 3. 变更流程

software 改 metrics 键或素材路径 → 修改本文件 → `lint_kb.py --file workspace/chuangxin2026/blueprint.md` 复验 → JOURNAL 记一行。
