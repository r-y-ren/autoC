# software/ —— 数据统计 CLI（e2e-rehearsal-2026 m1）

纯 Python stdlib（零第三方依赖），Python 3.8+。契约冻结见 `../interface/contract.md`。

## 一键命令

```bash
# a1：对样例 CSV 输出统计 JSON 并自检（退出码 0 = 过）
python software/stats_cli.py --csv references/data/sample.csv --check

# a2：全测试集（unittest discover）
python -m unittest discover -s software/tests -v

# a3：报告数字核验（需 m2 产出 docs/report.typ + docs/report.pdf；W1 期间退出码 1 属预期）
python software/check_report.py
```

（在战役根 `workspace/e2e-rehearsal-2026/` 下执行；蓝图验收 cmd 为上述命令的绝对路径形态。）

## 文件

| 文件 | 职责 |
|---|---|
| `stats_cli.py` | 读 CSV → 统计 JSON（rows/cols/数值列 count+mean+max）；`--check` 自检退出码 |
| `check_report.py` | a3 核验器：report.pdf 存在 + report.typ 引用的 metrics 键全部命中 `software/metrics.json` |
| `metrics.json` | 实测指标分片（stats_cli 于 `references/data/sample.csv` 实测；文档侧经 `metrics.software.<键>` 引用） |
| `tests/` | unittest 测试集（外部行为：进程边界 + 公共函数两接缝） |

## 实测数字（2026-09-16）

`rows=6`，`cols=3`，`score`: mean 88.0 / max 95.0 / count 6，`hours`: mean 5.5 / max 8.0 / count 6 —— 全部来自 `metrics.json`（实测值，测量方法见其 `_meta`）。
