# mqingcs 上游依赖归档（degnonguidi/best-agent-ranking kernel output）

## 用途

`monitor-round2-probe` 包（mqingcs/kaggressulture-two-policy-source，Apache-2.0）的
last_dance_56720309 / observed_56713902 两策略运行时经 `publication_assets.value()` 解析
上游常量：**不执行**上游文件，只按 `dependency_spec.json` 的 characters+prefix 在
`main.py` 的 AST 字符串常量（>1024 字符）中匹配（README「Run」节明示流程）。

## 拉取记录（实抓）

- 拉取时间：2026-10-03T06:05:55Z（本机 UTC；CLI 输出时间 14:06 本地=06:06Z）
- 命令：`kaggle kernels output degnonguidi/best-agent-ranking -p kernel_output`
- 元数据（`kaggle kernels pull --metadata`，2026-10-03T06:07Z）：kernel id
  `degnonguidi/best-agent-ranking`（id_no 134618884），public notebook，
  language python，无 GPU/TPU，enable_internet=true，competition_sources=["kaggriculture"]，
  docker `gcr.io/kaggle-images/python@sha256:dafd4ce5668bbf1ad422e4c109e0f18c9623c3a7c7f48b0235f13142755c40b9`
- 状态：`KernelWorkerStatus.COMPLETE`（kaggle kernels status，2026-10-03T06:07Z）
- 产物（kernel_output/）：
  - `main.py` 1,026,965 B，sha256
    `a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab`
  - `submission.tar.gz` 628,543 B（未解包未执行）
  - `best-agent-ranking.log`（kernel 运行日志；其 stdout 自报
    "main.py 1,026,965 bytes sha256 a16e0e9b40c48997..."，与本次下载件哈希一致=版本同一性证据）

## dependency_spec 匹配核验（2026-10-03T06:06Z 实测）

AST 解析（不执行）得 >1024 字符字符串常量 5 个，长度集合
{1823, 12009, 22861, 94490, 553065}。逐条 spec 匹配：

| spec 键 | characters | prefix 匹配数 | 结果 |
|---|---|---|---|
| observed_56713902_001_002 | 94490 | 1 | UNIQUE-OK |
| observed_56713902_001_006 | 553065 | 1 | UNIQUE-OK |
| last_dance_56720309_014 | 94490 | 1 | UNIQUE-OK |
| last_dance_56720309_018 | 553065 | 1 | UNIQUE-OK |

结论：当前线上版本 kernel output 与包内 dependency_spec 完全匹配（无 missing/ambiguous），
`KAGGRICULTURE_UPSTREAM_MAIN` 指向本目录 `kernel_output/main.py` 即可装载 last_dance 全链。

## 版本限界

- Kaggle CLI 的 kernels output 只取最新版本快照；kernel 若后续被作者重跑且常量变更，
  本归档为可复现锚点（以 sha256 为准）。
- `policy_parameters.json` 已含 6 键（含 last_dance_56720309_015/_020 与 observed 4 键）；
  `observed_56713902_009_010` 既不在参数包也不在 dependency_spec → observed_56713902_009.py
  装载必触发 FileNotFoundError（缺授权任务库分支），符合 README 预期（私有任务库未随包，
  预期 UNRUNNABLE）。
