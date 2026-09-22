# v48_hybrid v4 — P1 旗关变体包（--p1 off，轻量轮门禁已跑：FAIL）

> v4 = `python build.py --p1 off`（P1 中期卖单层零接线，P2/P3 保留）。
> 本目录产物由 `tmp/build_v4.py` 驱动 build.py 原函数确定性生成（build.py
> 旗关模式默认只落 `tmp/main_p011.py`，故由驱动脚本产最终包）；基底与
> `patches/*.py` 只读未改，v48_hybrid/ 既有件零改动。

## 身份链

| 件 | sha256 | 字节 |
|---|---|---|
| 基底 `../../v48_derivative/main.py` | `dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a` | 107,008 |
| `v4/main.py`（基底逐字前缀 + P2/P3 追加块） | `6266e765b5a4ce46bb8b3aa8404dfbd7df55e20ef3c9284fca06e95fd5b241d5` | 126,668 |
| `v4/submission.tar.gz`（单成员 main.py，确定性 tar） | `05ef4e204f4438ee8ba0d05272f606fab4e761487b446b2425d2626b6e18968f` | 94,642 |
| P1 源 `patches/midgame_sell_layer.py`（未内嵌，sha 登记溯源） | `1b9f235e9824c6b0c38c362ca53133869be1dcd126fe6bf7fd33dcfcd4de9f94` | 23,676 |

- 零接线字节级自证：v4 文本中 P1 接线 token（`v48h.p1_midgame_sell_layer`
  / `_v48h_p1_apply` / `_v48h_p1_defer` / `apply_to_market_orders` /
  `should_defer_to_tape`）计数 **0/0/0/0/0**；blob 只内嵌 P2/P3 源
  （与 `patches/` 逐字节一致，P1 模块零内嵌）；P2/P3 token 在场=接线真实。
- 确定性：CLI 子进程构建 == 进程内 `build_once`（sha 同）；双跑构建/双次
  打包逐字节一致；tar 单成员 main.py 内容逐字节回读一致。
- 开关：`P1_ON=False P2_ON=True P3_ON=True`。

## 门禁（轻量轮 2026-09-22）——总体 **FAIL**（如实）

| 门 | 结果 | 数字 |
|---|---|---|
| launch fourgate | **PASS** | 装载语义（干净 -I，named==last，stdlib 扫描空）/ 双席自打 2 局（seeds 101/102）双 DONE 720 回合 max 4.2ms/步 / 确定性 seed101 重跑流哈希一致 / 94,642B ≤ 100MB |
| h2h vs 纯 v48 | **FAIL** | 8 局（seeds 101/102/202/203 × AB/BA）**0-8-0**，非平局=行为不≡v48；margin -1,044 ~ -29,551/局（席位镜像确定性） |
| patch_safety 等价面 | **FAIL** | 4 种子（11/22/33/47）真引擎+孪生动作流均分叉（24/126/38/175 步）；0 局"零触发等价" |
| patch_safety 保险面 | **PASS** | 构造双死价局（MILK=88/WOOL=85×持续帧）经 v4 注册 P2 模块实弹：激活后 BUY_ANIMAL 全删、BUILD_PASTURE→PASS、其余原样、健康市场零触发；patches 单测 14/14 |
| panel | **FAIL** | 4 局合成语料 global ratio **0.971688** <0.98；逐局 0.9736/0.9992/0.9901/0.8680（seed47 席位1 低至 0.715） |

**差分定位（根因）**：P1 旗关后接线置 `_v48h_defer_frame = False`（P3
无门控）。P3 的 d10-12 里程碑窗口在**纯 v48 磁带轨迹本身**判偏离（seeds
11/22/33 step252 `money` 地板、seed47 step240 `cow_herd`）→ 推迟非紧急
卖单（首个分叉=step252 v48 的 `SELL MELON 6` 被 v4 延迟）→ 与 v48 行为
分叉。P3 里程碑表按 P1 在位经济标定，v48 自身磁带在其下读作"偏离"。
P2 全程零触发（归因遥测 p2=0，4 局皆 P3 单因）。**结论：当前接线下
v4（P2/P3 保留）行为级 ≠ 纯 v48**，"行为级≡纯 v48" 仅在 P3 亦关（或
P3 获得 defer 谓词/按 v48 磁带重标定里程碑）时成立——待用户裁决。

## 提交（人工执行；门禁 FAIL，未获裁决勿提交）

```bash
cd /mnt/data/Code/autoC/workspace/kaggriculture/software/kaggle_simulations/v48_hybrid/v4
kaggle competitions submit -c kaggriculture -f submission.tar.gz -m "public derivative with economic-guard layers (v4: market layer off per online forensics)"
```

- slug `kaggriculture` 由 build.py `extract_slug()` 从
  `software/scripts/sync_online_probe.py` 程序化提取。
- 描述文案（-m）：`public derivative with economic-guard layers (v4: market layer off per online forensics)`。

## 目录内容

- `main.py` / `submission.tar.gz` — v4 交付件（上表 sha）
- `build_manifest.json` — 身份链/零接线/门禁回填（FAIL 如实）
- 门禁产物：`../tmp/probes_v4/{v4_smoke,gates_v4,panel_v4}.json`
- 驱动/门禁脚本（临时，不入库语义）：`../tmp/{build_v4,fourgate_v4,gates_v4,panel_v4}.py`
