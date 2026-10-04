# Amey-Thakur write-up provenance（teardown-wave1/amey-thakur/）

- 来源：GitHub 仓 `Amey-Thakur/KAGGLE-COMPETITIONS` 子目录 `Competitions/Kaggriculture/`（URL 自上轮 Brave 存档 `../monitor-round2-github/w_brave.html` 正则派生，存 `../urls_amey.txt`）
- 抓取方式：raw.githubusercontent.com 原文件直拉 + GitHub contents/git-trees API；抓取时间 **2026-10-03 06:04–06:07 UTC**
- **许可（CC-BY-4.0，可直接引用，须署名）**：仓根 `LICENSE` = Creative Commons Attribution 4.0 International（"Copyright (c) 2026 Amey Thakur"，全文存本目录 `LICENSE.txt`）；GitHub API license 检出 `spdx_id=CC-BY-4.0`。
  **混态警示**：①仓根另有 `LICENSE-MIT`；②本 README 徽章印 "License: Apache_2.0"（模板徽章，与其仓根 LICENSE 不一致）。裁定：**正文按 CC-BY-4.0+署名归档引用**（GitHub 自动检出+LICENSE 文件双证）；notebooks 代码许可见 Apache-2.0 徽章与 MIT 文件并存，**搬运/衍生代码前需向作者确证**——本轮只全文归档+摘引，不搬运再分发代码本体以外的用途。
- 署名（CC-BY-4.0 要求）：© 2026 Amey Thakur（Kaggle: ameythakur20；ORCID 0000-0001-5644-1575）
- 仓元数据：repo pushed_at **2026-09-06T02:16:51Z**（早于赛末——**该 write-up 系赛前发布，非赛后复盘**）；recursive tree 仅 237 项（`truncated=false`）但不含 Competitions/Kaggriculture 路径（tree 快照口径 vs contents API 口径差异，以 contents API 为准，`dir_contents.txt` 佐证 3 文件在册）

## 文件清单

| 文件 | 内容 | 校验 |
|---|---|---|
| `README.md` | write-up 全文（问题表述/畜牧经济学/市场优先级与 front-running/架构五子系统/V115 基准表） | SHA256SUMS.txt |
| `kaggriculture-premium-first-market-agent.ipynb` | notebook 1（19 cells，88,895 字节） | SHA256SUMS.txt |
| `kaggriculture-deterministic-farm-planning-agent.ipynb` | notebook 2（15 cells，36,586 字节） | SHA256SUMS.txt |
| `LICENSE.txt` | 仓根 CC-BY-4.0 许可全文 | SHA256SUMS.txt |
| `tree_all.txt` / `dir_contents.txt` | 仓树与目录列表（API） | SHA256SUMS.txt |

## 自报数字（全部未复核；终榜至 10-14 未出）

- Bronze medal 徽章（**终榜未出，待核**）
- V115 Grandmaster 对 5 公开基线基准表：Soil-Remembers-Rain V26-H 5-0/+10,421.60、Moon-V113 4-1/+5,848.60、Kaito-V41 10-0/+8,334.90、Tetsutani-Adaptive 9-1/+3,878.20、Starter 10-0/+177,807.00（表头口径"Win Rate"列实为 champion 胜率，100%=V115 全胜）
- 经济学公式：8 牛×11 周期×$160=$14,080/周期簇；4 羊×8 周期×$200=$6,400；8C4S 毛 $96,000/净 $88,400
