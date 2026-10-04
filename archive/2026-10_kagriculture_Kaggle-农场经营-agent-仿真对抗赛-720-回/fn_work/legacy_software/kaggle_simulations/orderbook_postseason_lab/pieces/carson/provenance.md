# provenance — carson（CarsonBurke/kaggriculture）

- **repo URL**: https://github.com/CarsonBurke/kaggriculture
- **commit sha**: `fbbf76f49fc833f5a444a6414a71c8e74d90c4f4`（HEAD，2026-10-01T23:35:15-07:00 "Update README with final run details and diagram"）
- **抓取时间**: 2026-10-02 12:06Z（git clone --depth 1，GitHub REST 11:0xZ 复核 license=MIT、pushed=2026-10-02T06:35:15Z）
- **许可**: MIT（仓内 LICENSE；`licenses/Apache-2.0.txt` 为第三方依赖许可留存）
- **自报声明**（README/docs/solution.md，抓取 2026-10-02，自报未复核）:
  - "The final submissions placed 12th of 10,246 teams on the public leaderboard."（自报 #12）
  - 产线：leaderboard replays → behavior cloning → self-play PPO → evaluation → submission
  - Rust 位级对齐仿真 `rust/kagg_env`（PyO3+Rayon，parity oracle 逐转移全公私字段对账）、LeJEPA 世界模型、联盟 PPO、集中式 critic、26 决策态 entity-attention 策略
  - 默认对手=public v27 agent（"the submission builder requires"）
- **装载形态**: **需权重（checkpoint）——仓内不带**。提交件=Python 神经推理包（`src/kaggriculture/`，54 模块）+ 训练 checkpoint；打包线 `scripts/build_submission.py --checkpoint runs/ppo/best.pt --output artifacts/submission.tar.gz`（README 步骤 5），仓内无任何 `.pt/.npz/.npy/.pth/.ckpt` 权重文件、无 `runs/`、无 `artifacts/`；`.lfsconfig` 仅排除 tensorboard 日志（results/tensorboard/* 为 LFS 指针，未拉取）。打包器另有 provenance/eval 证据硬门（"will not package a checkpoint unless its provenance and evaluation evidence match"）。运行依赖 kaggle-environments==1.32.7（torch 仅在 train extra）。
- **归档说明**: 本目录=仓库 shallow clone 原样归档（含 .git，300 文件）；判决 harness 侧无可装载入口（详见池测报告 UNRUNNABLE 判定）。
- clone HEAD: fbbf76f49fc833f5a444a6414a71c8e74d90c4f4（.git 已按嵌套仓纪律移除，源树全保留）
- 上游 LFS 件（results/tensorboard/*.tfevents 训练日志，.lfsconfig 指向）未随档：本地 clone 仅有指针无 LFS 对象，源在上游仓 CarsonBurke/kagriculture LFS 存储
