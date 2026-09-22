# v48_hybrid — v48 混合候选提交包（方案甲，assemble_package 产物）

> 本目录产物全部由 `python build.py` 确定性生成（零时间戳/固定序，双跑逐字节一致）；`python audit_base.py` 为基底五区零改动分区审计。基底 `../v48_derivative/main.py` 与 `patches/*.py` 只读不改。

## 身份链（identity chain）

| 件 | sha256 | 字节 |
|---|---|---|
| 基底 `../v48_derivative/main.py` | `dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a` | 107008 |
| P1 `patches/midgame_sell_layer.py` | `1b9f235e9824c6b0c38c362ca53133869be1dcd126fe6bf7fd33dcfcd4de9f94` | 23676 |
| P2 `patches/economic_guard.py` | `e7206b734451cb08a5d9cbbba5f4cf16a88f17dfcf8a3b34cd1f99201ad98713` | 10168 |
| P3 `patches/milestone_monitor.py` | `b0ef3c90380d9de079a6efb0d90462546336e196bd12732ddbb7287f5b0d6caf` | 16760 |
| 混合 `main.py`（基底逐字前缀 + 追加块） | `1d6cdb26d2f379402b069ec517de7bf3c6712df6a658a31875a26e2a951235c1` | 139494 |
| `submission.tar.gz`（单成员 main.py，确定性 tar） | `ad14c9e668a9e6dc62ed178aa3059d016b0d6d28aa0b4754b5bc2a2b93415772` | 103997 |

开关状态：`P1_ON=True P2_ON=True P3_ON=True`（提交构建全开；旗关重建=对应补丁零接线，字节级验证见 `build_manifest.json` 的 `flag_off_zero_wiring`）

## 仲裁次序（追加块内统一实现）

终局清仓 > 反克隆抢卖 > P3 卖单时点调整 > P1 中期卖单接管 > 剧本默认；P2 在策略步返回前否决产线步骤（market `BUY_ANIMAL` 删除、farmer/hands `BUILD_PASTURE`→`PASS`，唯一碰产线的补丁）。补丁异常一律回退该补丁未应用的 v48 原生动作；基底 except 兜底逐字保留。

## 提交（人工执行；蓝图 out_of_scope）

```bash
cd /mnt/data/Code/autoC/workspace/kaggriculture/software/kaggle_simulations/v48_hybrid
kaggle competitions submit -c kaggriculture -f submission.tar.gz -m "public derivative with modifications (market/economic-guard layers)"
```

- slug `kaggriculture` 由 build.py 从 `software/scripts/sync_online_probe.py` 程序化提取（`"competition": "kaggriculture"`）。
- 描述文案（`-m`）：public derivative with modifications (market/economic-guard layers)
- 提交预算：每日≤5、每候选≤2、Error 即停（继承 SOP）。

## 门禁结果（F3 verify_offline_gates 回填；此处为占位）

| 门 | 判据 | 结果 | 数字 |
|---|---|---|---|
| h2h | seated ≥16 局 vs 纯 v48 互胜 ≥0.65 | PENDING | — |
| panel | 孪生 d0 反事实资金 ratio ≥0.98 | PENDING | — |
| zero-new-anomalies | 全 DONE 且异常集对照纯 v48 零新增 | PENDING | — |
| launch fourgate | 装载语义/双席自打 DONE/确定性/体积身份链 | PENDING | — |

本批次（F2）冒烟已执行：官方装载语义（干净 -I 子进程 get_last_callable 复刻）、vendored 引擎双席自打 ≥2 局 DONE、确定性双跑逐字节——数字见批次报告与 `tmp/` 探针产物。

## 目录结构

- `main.py` — 基底逐字前缀 + 追加块（三补丁 blob + 仲裁接线 + 入口）
- `submission.tar.gz` — 提交包（单成员 main.py，mtime=0/uid=gid=0/mode 0644，gzip mtime=0）
- `build_manifest.json` — 基底 sha/混合 main sha/包 sha/补丁清单/开关状态/零接线验证/门禁占位
- `build.py` / `audit_base.py` — 装配器与分区审计（确定性，可复跑）
- `patches/` — 三补丁叶与其测试（F1 产物，只读）
- `tmp/` — 冒烟/诊断临时产物（不入库语义，旗关诊断件亦落此）
