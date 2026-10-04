# v48_hybrid v4b — P1/P3 双旗关变体包（--p1 off --p3 off，轻量轮门禁已跑：**PASS**）

> v4b = `python build.py --p1 off --p3 off`（P1 中期卖单层与 P3 里程碑层
> 双旗关零接线，P2 死价保险保留）。v4 轮门禁 FAIL 根因 = P1 旗关使 P3
> 失去门控（defer 探针属 P1），P3 里程碑表把纯 v48 磁带轨迹本身判偏离
> （首分叉 step252，4/4 种子 P3 单因，P2 全程零触发）——v4b 将 P1/P3
> 同关，行为级 ≡ 纯 v48 + P2 保险。本目录产物由 `tmp/build_v4b.py` 驱动
> build.py 原函数确定性生成（build.py 旗关模式默认只落
> `tmp/main_p010.py`，故由驱动脚本产最终包）；基底与 `patches/*.py`
> 只读未改，v48_hybrid/ 既有件零改动。

## 身份链

| 件 | sha256 | 字节 |
|---|---|---|
| 基底 `../../v48_derivative/main.py` | `dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a` | 107,008 |
| `v4b/main.py`（基底逐字前缀 + P2 追加块） | `8bbd25467b4c0fc40c20996ed703a498b1a575bc4a2cfa524fe92ce1236c7e1a` | 116,499 |
| `v4b/submission.tar.gz`（单成员 main.py，确定性 tar） | `b5141af72a9da368b34815a2bac1bc462a9e3a62b7ea31d36c048bd68e74d198` | 87,657 |
| P1 源 `patches/midgame_sell_layer.py`（未内嵌，sha 登记溯源） | `1b9f235e9824c6b0c38c362ca53133869be1dcd126fe6bf7fd33dcfcd4de9f94` | 23,676 |
| P2 源 `patches/economic_guard.py`（内嵌，blob==源逐字节） | `e7206b734451cb08a5d9cbbba5f4cf16a88f17dfcf8a3b34cd1f99201ad98713` | 10,168 |
| P3 源 `patches/milestone_monitor.py`（未内嵌，sha 登记溯源） | `b0ef3c90380d9de079a6efb0d90462546336e196bd12732ddbb7287f5b0d6caf` | 16,760 |

- 零接线字节级自证：v4b 文本中 P1+P3 接线 token（P1：`v48h.p1_midgame_sell_layer`
  / `_v48h_p1_apply` / `_v48h_p1_defer` / `apply_to_market_orders` /
  `should_defer_to_tape`；P3：`v48h.p3_milestone_monitor` / `_v48h_p3_assess` /
  `_v48h_p3_adjust_timing` / `_v48h_p3_sell_timing` /
  `assess_milestone_deviation` / `adjust_sell_timing` /
  `_V48H_TURNS_PER_DAY`）计数 **全零**；blob 只内嵌 P2 源（与
  `patches/economic_guard.py` 逐字节一致，P1/P3 模块零内嵌）；P2 token
  在场（3/2/1）=接线真实；P1/P3 模块在装载实例中零注册。
- 确定性：CLI 子进程构建 == 进程内 `build_once`（sha 同）；双跑构建/双次
  打包逐字节一致；tar 单成员 main.py 内容逐字节回读一致。
- 开关：`P1_ON=False P2_ON=True P3_ON=False`。

## 门禁（轻量轮 2026-09-22）——总体 **PASS**（全为构造性 PASS）

| 门 | 结果 | 数字 |
|---|---|---|
| launch fourgate | **PASS** | 装载语义（干净 -I，named==last `_v48hybrid_entrypoint`，mismatch=0，stdlib 扫描空）/ 双席自打 2 局（seeds 101/102）双 DONE 720 回合 max 3.34ms/步 / 确定性 seed101 重跑流哈希逐字节一致 / 87,657B ≤ 100MB；交叉核验：v4b 自打终局 vs 纯 v48 自打基线 seeds 101/102 **逐位相等**（92750/86550；对照 v4 轮 96018/86863 不等） |
| h2h vs 纯 v48 | **PASS** | 8 局（seeds 101/102/202/203 × AB/BA）**8/8 平局**，全 DONE，且每局完整动作流 sha256 == 同种子纯 v48 自打动作流（`all_stream_identical=True` ×8，构造性身份证明） |
| patch_safety 等价面 | **PASS** | 4 种子（11/22/33/47）真引擎+孪生动作流**逐字节一致**（differing_steps=0 ×8 通道），P2 零触发（p2_veto=0 ×4），classification 全部 `equivalent_zero_trigger`（对照 v4 轮 4/4 分叉 24/126/38/175 步） |
| patch_safety 保险面 | **PASS** | 构造双死价局（MILK=88/WOOL=85 持续 4 帧激活）经 v4b 装载注册的 `v48h.p2_economic_guard` 实弹：激活后 BUY_ANIMAL 全删、BUILD_PASTURE→PASS、其余原样、健康市场零触发（same-object noop）；P1/P3 模块零注册；patches 单测 14/14 |
| panel | **PASS** | 4 局合成语料 global ratio **1.000000** ≥0.98；逐局 1.0/1.0/1.0/1.0，8 席位资金全部逐位相等（按构造：行为级≡纯 v48 + P2 零触发） |

**结论**：v4b（P1/P3 双旗关、P2 保险保留）行为级 ≡ 纯 v48——h2h 全平局
+ 动作流逐字节身份、等价面零分叉、panel ratio=1.0 三面构造性证明；
P2 死价保险双面验证（线上轨迹零误触发 + 双死价局实弹否决）。

## 提交（人工执行）

```bash
cd /mnt/data/Code/autoC/workspace/kaggriculture/software/kaggle_simulations/v48_hybrid/v4b
kaggle competitions submit -c kaggriculture -f submission.tar.gz -m "public derivative with economic-guard layer (v4b: market/milestone layers off per online forensics; dead-price guard retained)"
```

- slug `kaggriculture` 由 build.py `extract_slug()` 从
  `software/scripts/sync_online_probe.py` 程序化提取。
- 描述文案（`-m`）：`public derivative with economic-guard layer (v4b: market/milestone layers off per online forensics; dead-price guard retained)`。

## 目录内容

- `main.py` / `submission.tar.gz` — v4b 交付件（上表 sha）
- `build_manifest.json` — 身份链/双旗零接线/门禁回填（PASS）
- 门禁产物：`../tmp/probes_v4b/{v4b_smoke,gates_v4b,panel_v4b}.json`
- 驱动/门禁脚本（临时，不入库语义）：`../tmp/{build_v4b,fourgate_v4b,gates_v4b,panel_v4b}.py`
