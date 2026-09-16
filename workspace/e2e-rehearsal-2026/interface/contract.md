# 接口契约：software ↔ document（e2e-rehearsal-2026）

> 冻结自票 01 的真实 CLI 实测输出（2026-09-16），票 02 产物。报告侧只许消费本文件冻结的名字与路径；键名/形状变更必须回本文件改并同步 CLI、metrics 分片与测试（三者逐键对齐）。
> 蓝图依据：`blueprint.md` interface_contracts[0]（between: [software, document], contract_file: interface/contract.md）。

## 1. 契约范围

- **software 侧产物（m1，已冻结）**：`software/stats_cli.py`、`software/tests/`、`references/data/sample.csv`、`software/metrics.json`、`software/check_report.py`。
- **document 侧消费（m2，票 04）**：撰写 `docs/report.typ` → 编译为 `docs/report.pdf`；报告中一切数字只引 `metrics.software.*` 键（即本契约 §3 的分片键）。

## 2. 统计 JSON 形状（stats_cli stdout，冻结）

命令：`python software/stats_cli.py --csv references/data/sample.csv [--check]`

```json
{
  "source": "sample.csv",
  "rows": 6,
  "cols": 3,
  "columns": ["name", "score", "hours"],
  "numeric_columns": ["score", "hours"],
  "numeric": {
    "score": {"count": 6, "mean": 88.0, "max": 95.0},
    "hours": {"count": 6, "mean": 5.5, "max": 8.0}
  }
}
```

- 键语义：`rows`=数据行数（不含表头）；`cols`=表头列数；`columns`=表头列名序；`numeric_columns`=数值列名序（该列所有非空单元格均可解析为有限浮点且至少一个非空值）；`numeric.<col>`：`count`=非缺失值个数，`mean`=均值，`max`=最大值（空单元格视为缺失，不参与）。
- 退出码：正常输出=0；输入异常（文件缺失/空文件/仅表头/行列不齐/读取失败）或 `--check` 自检不过（如无数值列）=非 0，报因于 stderr。
- 以上即 a1 验收口径（蓝图 checklist a1 的 cmd 原文：`python .../software/stats_cli.py --csv .../references/data/sample.csv --check`）。

## 3. metrics 分片键清单（software/metrics.json，冻结）

分片为**扁平键**（顶层即指标，`_meta` 仅载测量方法，不承载报告数字）。顶层 `metrics.json`（战役根）由 `scripts/verify/merge_metrics.py` 汇总生成（角色禁写），合并后同一数字的规范引用形为 `metrics.software.<键>`。

| 键 | 实测值 | 单位 | 含义 |
|---|---|---|---|
| `rows` | 6 | 行 | 样例数据行数（不含表头） |
| `cols` | 3 | 列 | 样例数据列数 |
| `score_count` | 6 | 个 | score 列非缺失观测数 |
| `score_mean` | 88.0 | 分 | score 列均值 |
| `score_max` | 95.0 | 分 | score 列最大值 |
| `hours_count` | 6 | 个 | hours 列非缺失观测数 |
| `hours_mean` | 5.5 | 小时 | hours 列均值 |
| `hours_max` | 8.0 | 小时 | hours 列最大值 |

测量方法：`python software/stats_cli.py --csv references/data/sample.csv --check` 于战役根实测（2026-09-16），数字与 CLI stdout 逐键一致（数据纪律：无编造/估计）。**报告所需数字已全部入片，m2 不得引用片外实测数字。**

## 4. 报告消费路径与引用语法（check_report.py 的扫描依据）

1. **加载**：`docs/report.typ` 中以 Typst 标准库读分片，变量名必须为 `metrics`：
   ```typst
   #let metrics = json("../../software/metrics.json")
   ```
   （直接读 software 分片；顶层汇总 `metrics.json` 是脚本生成物，document 勿手写。）
2. **引用**（两种规范形，`<键>` ∈ §3 键清单，`metrics.` 前缀不得用于其他对象）：
   - 取值形：`metrics.rows`、`metrics.score_mean` …（经上式变量）；
   - 规范注释/文本形：`metrics.software.rows` …（与合并后引用形一致）。
   - 扫描细则：核验器扫描前先剥离 `json("…")` 路径字面量（加载行文件名 `metrics.json` 不算键引用）；`metrics.<键>` 的键后不得紧跟 `.` 或词字符（裸写 `metrics.software` 属前缀误用，会被判失败）。
3. **硬性要求**：`report.typ` 中至少出现 1 个上述引用；任一引用的 `<键>` 不在 `software/metrics.json` 顶层键中 → a3 核验失败。
4. **数字纪律**：报告正文中一切实测数字只能来自 §3 键（展示格式化如保留位数属呈现层，不改变来源键）。

## 5. Typst → PDF 唯一编译通道

```bash
~/.venvs/autoc/bin/python -c "import typst; typst.compile('docs/report.typ', output='docs/report.pdf')"
```

- 仅此通道（宿主 venv 的 typst 包）；工程自身零第三方依赖（纯 Python stdlib），typst 不进工程 import 面。在战役根执行，产物落 `docs/report.pdf`。

## 6. a3 核验器：software/check_report.py

命令（蓝图 a3 cmd 原文，无参数，路径按战役根默认解析）：

```bash
python software/check_report.py
```

- 核验内容：① `docs/report.pdf` 存在；② `docs/report.typ` 存在且按 §4 语法扫描出 ≥1 个 metrics 键引用；③ 每个被引用键均存在于 `software/metrics.json` 顶层键。
- 退出码：全部通过=0；任一不满足=1；参数/文件读写异常=2。诊断信息输出到 stderr。
- 调试参数（供测试夹具用，不改变默认行为）：`--pdf` / `--typ` / `--metrics` 覆盖三个默认路径。

## 7. 交付物路径一览

| 角色 | 路径（相对战役根） | 说明 |
|---|---|---|
| software | `software/stats_cli.py` | 统计 CLI（a1） |
| software | `software/tests/` | unittest 测试集（a2） |
| software | `software/metrics.json` | 实测指标分片（§3） |
| software | `software/check_report.py` | a3 核验器（§6） |
| 共用 | `references/data/sample.csv` | 样例数据（INDEX 已登记：rehearsal://self-generated，2026-09-16） |
| document | `docs/report.typ` → `docs/report.pdf` | m2 产物（票 04），经 §5 通道编译 |
