# haodou_v94 原始拉取物 provenance（ext/haodou_v94/）

- 来源 URL：https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger
- 抓取方式：`kaggle kernels pull haodou092/kaggriculture-harvest-ledger -p /tmp/v94_pull`（含 -m 取 kernel-metadata.json）
- 抓取日期：2026-09-30（本地落盘时间戳 10-01 00:37，为时区显示差；kernels list 实测 lastRunTime=2026-09-30 15:56:57.750000，与任务描述"09-30 15:56 run"一致）
- 自报版本号：**V94**（notebook markdown 首行 "Kaggriculture V94 — Verified Spatial Mirror Gate"；自报为"final selected agent"定稿件）
- kernel id：haodou092/kaggriculture-harvest-ledger（id_no 131331249，public，python notebook）

## 文件清单与 SHA-256（见 SHA256SUMS.txt）

| 文件 | SHA-256 | 说明 |
|---|---|---|
| kaggriculture-harvest-ledger.ipynb | aaca2038dfa72440c45cd8704b0ca101e6ebcaecb726b50a0ebded29c4b03596 | 原始拉取 notebook（2 cells：markdown 自述 + 自解包代码） |
| kernel-metadata.json | 71a1aa19482920ed324fbcbb04e2dd62830b490db977305a268bfd22e9410d44 | kaggle CLI -m 拉取元数据 |
| main.py | 531a423a43184bc5864714189595ec1dbbe3c873de48691b0ebd32fa0a2359bb | 从 notebook PACKED_FILES 解包（base85+lzma），与内嵌 EXPECTED_SHA256 一致 |
| LICENSE.txt | cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30 | Apache-2.0（随包） |
| NOTICE.txt | b42b73b176af1dd8bd5ab2c72acae57ff1577cf172bbbafdb302c59c10135128 | 上游署名（guruprasaathas111 Master Engine V4 直系 + V81 镜像门本地改动声明） |

## 版本谱系（本次 diff 实测，见 evidence/v94_arena.json）

- V82 本体（我方留存件 `fn_work/legacy_software/kaggle_simulations/orderbook_haodou_adopt/submission.tar.gz`，main.py SHA bdb821178ca73c0e8480f06c1887e20921caea0438398a5edb68bd9ad20b1de8，run 2026-09-28T02:23Z）→ V94（SHA 531a423a…）行级 diff 仅 2 处改动块：
  1. **+Spatial Mirror Gate**（_s738_advance 内，main.py V94 行 7518-7529）：双农场 shape 指纹（tiles(kind,crop,animal)/unlocked_quadrants/farmer/hands）全同且 |money 差| ≤250 时 look 4→7（七拍提前卖窗），否则维持 _S738_LOOK=4 保守视界。
  2. **−PET_CAFE 胡萝卜倾斜**（V82 行 10138-10158 的 pet_any_demand_agent 壳：day10-23 已揭示 PET_CAFE 时 _CA_MARGIN -15→-22）整块删除。
- 生产策略保留声明属实：除上述 2 处外 main.py 逐字节一致（diff 总输出 37 行，全为这两 hunk）。
- 注意：V94 实际是"回滚 V82 的 PET_CAFE 局部实验 + 复装 V81 镜像门"，与 V81 NOTICE（_S738_LOOK=4 默认、镜像门后切 7）自述吻合。

## 自报战绩（自报口径，未迁移验证）

markdown 自述：V81 血脉在 32 局近期实榜对手动作流筛 24W8L、独立 24 局高带确认集 17W1T6L（合计 41.5/56 分最佳）、最终 32 局动态双席测试 28W4L 无崩溃；选择准则=胜/负/平分优先→灾难败计数→硬币边际三级诊断；声称零隐藏信息/对手身份/回放指纹。历史判决背景：我方实证"镜像提前卖"−80k 为负（六连败教训：自报≠可迁移）。
