# v10 修改程序：资料驱动的类差修复（2026-08-31）

依据: exports/intel/source_map.md + H2H 行为画像（本文件 §1）。核验日期 2026-08-31。

## 1. 行为画像：7 万缺口定位（scripts/profile_v48_gap.py，seed 101/102）

同土地（3 象限，解锁日差 1 天）、同雇佣（265 vs 282）、双方零外购肥料：

| 维度 | 我方 | v48 | 倍数 |
|---|---|---|---|
| 草莓收入 | 15.1k / 27.7k | 60.0k / 103.8k | 3-4x |
| 肥料转卖 | 5.0k / 5.2k | 25.7k / 25.4k | 5x |
| 牛奶收入 | 7.5k / 10.1k | 23.0k / 26.0k | 3x |
| 小麦收入 | 4.3k / 5.7k | 16.0k / 16.2k | 3.5x |
| 蜜瓜收入 | 13.3k / 14.3k | 16.4k / 16.1k | 1.2x |
| 畜群终局 | 8牛2羊 + **5空栏** | 11牛4羊（15/15满栏） | — |
| tile-day 草莓占比 | 0.37 | 0.49 | — |
| 终局清算增益 | 6.2k / 7.6k | 17.7k / 21.0k | 3x |

结论：差距不在扩张速度（土地/雇佣持平），在**畜群满栏率、粪肥货币化、草莓单位产量执行**三个结构项。v48 即 boatlee"8C/4S premium market lead"同型的高产路线活体。

## 2. 引擎实锤（kaggriculture.py 1.32.7，line 431-444）

- 肥效：`bonus = 2 if fertilized else 1`，**只作用于浇水日且在奖励窗内**（`window_start=(max_yield_day+1)//2 .. max_yield_day`）；施肥无即时产量。
- 作物窗：WHEAT window age 2-4（age-2 施肥=3/3 完美）；CARROT 2-3（完美）；MELON 6-12（**age-2 施肥覆盖 2-4=0 重叠，100% 浪费**）。
- 我方旧代码在 age 2 给 MELON 施 premium(v=190) → 机械确定性浪费，且挤占草莓的稀缺肥源。

## 3. 已实施：M-A 施肥时机修正（a93022c6）

- 改动: 一年一次性作物施肥年龄 `age == (max_yield_day+1)//2`（引擎窗口起点），premium_boost 收窄为 STRAWBERRY 专属；wheat/carrot 行为不变（窗口起点恰为 2）。
- 测试: 598 绿（含 test_fert_value_gate_keeps_premium_boosts_only）。
- dev 域配对门（vs r3_frozen，176 局）: **57W-31L 净 +84,028**，pool_wr 0.975 worst 0.75 disaster 0.0114 → **NOT MERGEABLE**（pool_wr 对 1.0 的单格差触发；worst/disaster 均优于或近于冠军）。
- 裁读: +84k 是近几波最强正净差，但按纪律与 FM-E1/v9.1 教训（本地配对正差不保证线上迁移），不升格、留候选线，reg 域数据补齐后与 fork 裁决一并定夺。

## 4. 待实施程序（按确定性排序，全部自研实现、行为引用合规）

- **M-B 畜群满栏**: `_herd_target` 上限 17 实际只到 10（5 空栏）。目标: 建栏即补栏至 13-15（参照公开行为 band，非抄码）。风险: FM-R5-1 dear-feed 螺旋 → 需配套外部小麦 feed 门（v48 买 105u 外饲同时卖 16k 小麦收入）。
- **M-C 粪肥货币化**: 产出 ~10u/日 vs 出售 ~5k/季。改 collect 优先级 + 超出田间需求即售（保留 M-A 释放的肥源）。
- **M-D 草莓产量执行**: tile-day 占比相近但收入 3x 差 → 排查我方浇水覆盖/售时（v7-R finished-crop 停浇策略是否过早停产）。
- 定位工具: `scripts/profile_v48_gap.py`（画像）、`scripts/h2h_external_probe.py`（16 局/候选 H2H）、opponents/ 目录（v48 + v72 锚点，PROVENANCE.md 含许可红线：只作陪练，字节永不入提交路径）。
