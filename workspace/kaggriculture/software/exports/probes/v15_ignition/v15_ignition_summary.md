# v15「点火重构」M-A..M-E 实测总结（2026-09-20）

剧本引擎与验证门的完整实测记录。JSON 原始产物在同目录（gitignore，本地留存）：
`v15_h2h_v48_v15_shipped.json` / `v15_h2h_v48_v15_forced.json` /
`v15_h2h_v48_flagoff_v138.json` / `v15_d0_counterfactual_giants.json` /
`v15_regression_gate.json`。Durable 键 = software/metrics.json `p15v15_*`。

## 交付物

- `kaggle_simulations/agent/src/wave.py`：M-A 波次剧本引擎（旗关零足迹，
  `PLANNER_OVERRIDES.wave_mode` 总闸 + globals().get 钩子死路模式）。
- `kaggle_simulations/agent/planner/wave_script.py`：M-C 剧本候选
  （WAVE|v15|ignition；rollout 比较集首位；τ 闸沿用）。
- M-B 市场结构（src/market.py + src/entry.py）：同回合 SELL 影响分排序
  （q×(p−p_after)）、d29 终局 (1+对手exposure)×glut×价×log(1+q) 全量排序、
  flush 日 SELL 先于 BUY 融资。
- 消费点：strategy._macro_plan/_crew_target/_field_alloc、market._market_orders、
  entry.agent（全部旗关等价，`planner_flagoff_golden.py` 6/6 逐字节）。
- 验证脚本：`scripts/v15_h2h_v48.py` / `scripts/v15_d0_counterfactual_giants.py`
  / `scripts/v15_regression_gate.py`。
- 包：layout pkg.3-wave（+src/wave.py +planner/wave_script.py），199,575 B，
  sha256 8bc419dc…14aaa74（见 commit B 登记）。

## M-E 门禁实测（全部 2026-09-20 本机，官方 1.32.7 vendored 引擎）

| 门 | 判据 | 实测 | 判定 |
|---|---|---|---|
| E4 旗关等价 | golden 6/6 逐字节 | 6/6 OK（seeds 11..69） | **PASS** |
| E5 冒烟 | smoke 4 相 | PASS 47.8s | **PASS** |
| E5 打包 | build --check | OK deterministic | **PASS** |
| E5 全测 | pytest 基线 | 955 passed+2 skipped（红=登记前身份链 20 项预期态+打包 1 项，登记后复验绿） | **PASS（登记后）** |
| E1 v48 h2h | 16 局：收窄 ≤-20k 或有胜局；0-16 不许复现 | shipped 0-16 均值 -84,743 / forced 0-16 -83,580 / 旗关基线 0-16 -88,043；点火中位 13 vs v48 的 10 | **FAIL** |
| E2 9 巨人反事实 | G1 点火≤12 ≥5/9；G2 挽回≥10% ≥5/9；G3 翻盘 ≥2 | G1 m5k 2/9、G1b 资产口径 2/9；G2 5/9；G3 1 | **FAIL**（G2 单项过） |
| E3 回归 | 塌方 ≤2/26；escape/overflow 0 | pool 32 局 0 败 0 契约违；注入塌方 wave 4/26（base 5/26）；escape 77（base 104）；满棚警戒 24（base 17）；净差 -38.4k/26 局 | **FAIL（字面门）** |

## 归因（诚实）

1. **点火时点差是表症**：v15 wave 把我方 m5k 点火稳定在 d13（base d13-18 中
   若干局提前到 d13），v48 稳定 d10——但 h2h 终局差 84.7k 中，点火差只贡献
   3 天的复利头部；**day-11 后经济规模差是主导**（v48 同种子终局 110-176k vs
   我方 31-77k）。
2. **公开谱系的结构性未解**：fresh-sweep digest——2945 Farm（公开最高
   2944.7）对当期 top-10 七队 0-36，"day-10 前领先、day-11 后全崩"，作者自述
   未解。v48 范式的可移植层（日历事件/flush/卖序/crew 阶梯）已全部并入 v15，
   仍不足以跨越该断层。
3. **m5k 现金口径 vs 剧本教义的度量张力**：剧本把 d6/d10 现金即刻换成地/畜
   （v48 教义），m5k 现金穿越日被设计性推迟；资产口径（herd≥11∧quads≥2）
   同样未进 ≤12（2/9）——我方四层手的 herd 采购节奏（pace+钱包门）比 v48
   的 719 步剧本慢。
4. **剧本候选在 rollout 仲裁中实际全选**：shipped 与 forced 16 局逐字节一致
   → 黎明三选一在实测中每黎明选中 WAVE（rollout 段剧本候选排首位恒被评估，
   τ 闸未拦截）。

## 两轮反事实修正（各带测试，教训内嵌代码注释）

1. crew 阶梯改"只抬不缩"（首跑把 native d1-9 的 7-8 人压到 5-6 → 浇水饿荒
   → 瓜 flush 全灭，melon 70/96 教科书复现）。
2. 瓜帽不缩（首跑 melon_total_cap 12→7 砍半瓜 flush）、买地日程不接管
   （native B2 本就 d1 起步，v48 的 d6/d10 地日程对我方是推迟）。
3. 买畜波次三闸（feed/cash/棚位 88）：饿逃=死损非零成本；一次 5 头=+10 棚位
   是 105375966 注入塌方的机制。

## 对协调者的发射建议

**v15 不建议作为 round-26 发射候选**（E1/E2/E3 均未过字面门；v14.2-dtsp
仍为注册基线）。剧本引擎保留为基础设施 + 对 v48 的本地回归基准；下一杠杆
建议按 fresh-sweep §6：售卖竞速层（前插+对手队列情景搜索）与 day-11 后
经济规模（CARE 覆盖/畜群结构），而非继续调点火日历。
