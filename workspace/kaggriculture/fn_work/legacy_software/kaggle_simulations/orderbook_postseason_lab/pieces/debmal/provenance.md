# provenance — debmal（debmalyaroy/kaggriculture）

- **repo URL**: https://github.com/debmalyaroy/kaggriculture
- **commit sha**: `c681c269d9713de082468271b056cf410e246dc9`（HEAD，2026-10-01T13:22:27+05:30 "Kaggriculture: agents, engine ports and tooling (final state after the competition)"）
- **抓取时间**: 2026-10-02 12:06Z（git clone --depth 1，GitHub REST 11:0xZ 复核 license=MIT、pushed=2026-10-01T07:52:38Z）
- **许可**: MIT（仓内 LICENSE）
- **自报声明**（README.md/docs/history/submission.md，抓取 2026-10-02，自报未复核）:
  - 终件=Rust "route + layers" v63.x：v63.14_rl_f898（Kaggle submission 56718979，自报 41W/12L/1D）+ v63.16_rl_f898（56720196，自报 53W/11L）；v63.17 "built, not submittable (deadline passed)"
  - 形态=按世界录制的 top-player route + chassis 修复守卫 + 反应层链（sale timing/races/endgame/economy，agent.json 管理器配置）
  - 竞赛口径自述：5 提交/日、仅最新 2 席计终榜、Validation Episode 自对局、Rating 只计 W/L、提交上限 100MiB、资源 1.6 vCPU/6.5GiB RAM、actTimeout 1.0s、remainingOverageTime 60s
- **装载形态**: **Rust 编译件+配置包——仓内缺件**。提交 tarball=`main.py`（= `kaggle/submission/main_config.py` stdio 桥）+ `agent-stdio`（Linux x86_64 musl 静态二进制，`cargo build --release` 产）+ `agent.json`（v63 候选配置）+ `base/routes.json + router.json`（首拍 ~4.8MB route 表装载）+ `fallback.py`（Python v61.1 同策略兜底）。README 明言 "The repository ships **no data** (replays, tapes, route tables, weights, builds)"；`configs/route_tables/` 仅 70B/476B/35B 的 refit 小 JSON 非 route 表；`configs/agents/` 仅 v61.x/c4/newchassis 无 v63 候选 agent.json；`agents/` 仅 v1_heuristic.py。编译链：crates/{agent,engine,runner,policy,…} + rustengine/（cargo 1.98.1 在位）。
- **归档说明**: 本目录=仓库 shallow clone 原样归档（含 .git，1,097 文件）；判决 harness 侧编译/装载尝试见池测报告（UNRUNNABLE 判定）。
- clone HEAD: c681c269d9713de082468271b056cf410e246dc9（.git 已按嵌套仓纪律移除，源树全保留）
