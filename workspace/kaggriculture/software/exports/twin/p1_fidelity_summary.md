# P1 孪生保真台账（twin_fidelity）

- 生成：2026-09-19T03:47:15+0800  模式：`smoke`  门墙钟：854 ms
- 指纹链：wheel `kaggle_environments-1.32.7+nodeps-py3-none-any.whl`
  - wheel sha256 `be693e837bcb0f81bad7d6509f2737f29986fe66b12296e9990b0aa88f287465`
  - kaggriculture.py sha256 `bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e`
  - kaggriculture.json sha256 `a82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867`
- 判据：全程走子逐步逐位比对 + 中间步注入重演终局资金逐位相等（型别敏感，float 位型 hex 复核）。

## 结论

- 语料：184 局可用，抽样 2 局 x 2 步点（抽样种子 20260919，早/中/晚窗 [(24, 240), (240, 480), (480, 690)]）。
- 全程走子逐位一致：2/2 局（100.00%），累计逐步比对 1438 个步点。
- 终局重演逐位一致：4/4 步点（100.00%）。
- **总体：PASS**（通过 2/2 局）。

## 基准（本地实测，Python 3.14.7）


## 失败归因

- 无失败例。

## 方法

- 判据与口径细节见 `exports/probes/twin_fidelity/fidelity_report.json`（gitignored）
  与 `scripts/twin_fidelity.py`（验收命令：`python workspace/kaggriculture/software/scripts/twin_fidelity.py --mode official`）。
- 孪生实现：`software/kaggle_simulations/agent/planner/twin.py`（stdlib-only；vendored 引擎指纹 fail-closed 校验；解释器零修改）。
