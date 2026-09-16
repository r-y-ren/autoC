# 线上采样台账（sampling）

发射快照仍是 `../roundN_ledger.json`（提交当下的 PENDING 记录，不回写）。
官方回放的完成态写在本目录 `roundN_sampling.json`。

规则：

1. 本地 quickwin / 同族自对局只做灾难诊断，不能当下一轮上线或改旋钮的理由。
2. 提交后必须用 Kaggle CLI 拉公开回放，再 `sync_online_probe.py ingest`。
3. `status` 必须是 `COMPLETE`；`replays_are_local_selfplay` 必须为 false。
4. 下一轮改参/提交前跑 `sync_online_probe.py gate`；round ≥20 缺采样即 fail-closed。

原始回放落在 gitignored 的 `references/data/online-replays/roundN/`。
