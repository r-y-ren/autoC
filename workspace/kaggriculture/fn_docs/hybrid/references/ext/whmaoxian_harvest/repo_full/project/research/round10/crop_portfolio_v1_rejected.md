# 禁止将 round10_crop_portfolio.py v1 用于策略比较或提交

v1 SHA256 `1021b964f0c4d7752df38b30b4ea7457dc064ef229f6af93be2828be83185ddb` 接到了 V9 最后一层之前的 `agent` 别名，遗漏 `round9_slack_agent`。官方开发世界 `1193292362` 双席两场均显示“选择 0 株却输冻结 V9 735 分”，证明其并非保留 V9 原动作的有效对照。保留文件仅用于追溯这次集成错误。

修正版为 `experiments/round10_crop_portfolio_v2.py`，SHA256 `9a982d7e340f3ca2714f10203e8e11ec54024f2fc3856cc4718737c7efa4ed23`；无操作双席烟测与 V9 两场同分。后续只评 v2。
