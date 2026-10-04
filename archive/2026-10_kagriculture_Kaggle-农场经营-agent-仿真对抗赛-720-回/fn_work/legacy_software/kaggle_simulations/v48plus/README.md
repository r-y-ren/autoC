# v48plus — V48 解码真源码 + V50 经济层（独立赛道）

v48 公开衍生版（线上 56400478，在跑资产）的**改进包**：以
`references/data/intel-notebooks/v48build/main.py`（sha256 `dadee25a…`，
与 `software/kaggle_simulations/v48_derivative/main.py` 逐字节一致）为
base 逐字保留，追加 V49/V50 公开 notebook 中的经济层手工移植（COURIER /
CAPHARV / SHEDROOM 三层，纯追加，不改动 base 任何一行）。stdlib-only。

## 一键构建

```bash
python software/kaggle_simulations/v48plus/build_v48plus.py
```

- 产物：`main.py` + `submission.tar.gz` + `build_manifest.json`
- 确定性：双次构建/双次打包字节一致（脚本自证），tar 口径
  mtime=0 / uid=gid=0 / mode 0644 / gzip mtime=0

## 一键验证

```bash
# 发射四件套（官方装载语义 / 720 回合短局实测 / 动作流确定性 / 包体）
python software/scripts/v48plus_launch_check.py

# 孪生 A/B 门（h2h 16 局 + 多样对手面板 + 9 巨人局 d0 反事实）
python software/scripts/v48plus_ab_gate.py

# 层消融（诊断用）
python software/scripts/v48plus_layer_ablation.py --seeds 101,102
```

结果落在 `software/exports/probes/v48plus/`。

## 层说明（移植范围与理由）

| 上游层 | 出处 | 本包 | 理由 |
|---|---|---|---|
| COURIER | V49 §v9 COURIER（The 2945 Farm） | 移植 | 纯 obs+动作叠加，底座无关 |
| SHEDROOM | V49 §SHEDROOM | 移植 | 同上（projected_shed 用本底座 v19_terminal） |
| CAPHARV | V49 §CAPHARV | 移植后移除 | 本底座六路线磁带已在 cap 前收割：全部跟踪局 0 次触发（层消融证据），属死代码，不入 shipping build |
| weedlag | V50 §weedlag | 无需移植 | 本底座已有等价物 `scripts.v22_weed_repair`（同 8 步回放，覆盖 BUILD_PASTURE/PLANT；BUILD_COOP 不在其列，残留缺口极小不处理） |
| v233x day-11 yarn commit | V50 §v233x | 未移植 | 本底座无 V233 六羊项目（yarn 路线 d7-d9 已放羊、d11 已买地），无加速对象 |
| CARROT/CARROT2/HERD/HERD2/COWSWAP/FERT/ORDERPRI2 | V49 | 未移植 | 依赖上游闭环 chassis（`_IMPL.chassis`）/作物模拟钩子，移植=重写已验证路线，非经济层叠加 |

引擎机制依据（vendored kaggriculture.py 实测）：黎明重置（farmer 回棚、
hands 全裁、库存自动入棚）、单位动作先于市场（DROP+SELL 同步生效）、
午夜溢出丢弃、照顾加成（fed+cared 每日 +1 pending_care_bonus，生产夜
1+bonus、封顶 max_held：羊 6 毛/牛 6 奶/鹅 4 蛋）。

## 上游来源与许可

- V48: Ahmed Berat Ozer, "Kaggriculture V48 — Clear the Queue"（Apache-2.0，
  notebook 拉回 2026-09-20，notebook 内嵌源 sha `4b540288…`；本包 base 为其
  提交包解码真源码 `dadee25a…`）
- V49: "kaggriculture-v49-funded-sale-timing-and-worker"（agent sha
  `ed89be8c…`，The 2945 Farm 经济层，Thomas Tschinkel v9/4 公开层）
- V50: "kaggriculture-v50-early-yarn-commit"（agent sha `044a2660…`）
- 2945 机制: Thomas Tschinkel, "The 2945 Farm"（公开 notebook，Apache-2.0）

本目录内 `main.py`/`submission.tar.gz` 为构建产物；源头 =
`v48plus_layers.py` + references 内 base。合规：全部基于公开发布代码
（host 明示 "Anything freely and publicly available is fair use"，
见 references/digests/web-comp-intel-2026-09-19.md §3）。
