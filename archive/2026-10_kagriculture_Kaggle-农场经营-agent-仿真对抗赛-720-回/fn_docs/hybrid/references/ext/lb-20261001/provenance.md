# ext/lb-20261001 —— 2026-09-30T17:41:44Z 公榜 CSV 归档 provenance

- 抓取命令（2026-09-30 17:41 UTC，kaggle CLI 2.2.4，在本目录内执行）：
  `kaggle competitions leaderboard -c kaggriculture --download`
- 产物：`kaggriculture.zip`（328,835B）→ 解压 `kaggriculture-publicleaderboard-2026-09-30T17:41:44.csv`（727,579B，10,221 数据行 + 表头）
- 列：`Rank,TeamId,TeamName,LastSubmissionDate,Score,SubmissionCount,TeamMemberUserNames`（utf-8-sig 带 BOM）
- 来源页：https://www.kaggle.com/competitions/kaggriculture/leaderboard （快照时戳以 Kaggle 生成文件名为准：2026-09-30T17:41:44Z）

## SHA256（2026-09-30 17:46 UTC 本目录执行 sha256sum）

```
0ffb161c2a4b73188d1c6eb85bc9c211269cdec1867eecbce1a1b93b10f3e597  kaggriculture.zip
c712f0b84f666fa3bfda03863be0f65c15351e71e968e1e56a677d7036685515  kaggriculture-publicleaderboard-2026-09-30T17:41:44.csv
```

## 用途

终窗 sweep6 对比基线（vs 2026-09-30T16:11:16Z 快照，仅 6 行留存于 `../2026-10-01-final-window-sweep.md` §1）与同门作者榜位映射（TeamMemberUserNames 列）。分析报告：`../2026-10-01-lb-sweep6.md`。
