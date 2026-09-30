# godv7 外部件血统记录（flexonafft 重打包 · leoprovorov god's-mode v7）

## 件对象

- 名称: godv7（本战役代号）；notebook 标题 "Kaggriculture | Multi-Route Farming Agent"
- 来源 URL: https://www.kaggle.com/code/flexonafft/kaggriculture-multi-route-farming-agent
- 抓取日期: **2026-09-30**（`kaggle kernels pull` 于 2026-09-30T16:39Z / 2026-10-01 00:39 CST，CLI 2.2.4）
- kernel 元数据（`kaggle kernels list` + `kaggle kernels pull -m` 实查）: author=Igor Zharov（flexonafft），
  lastRunTime=2026-09-30 11:40:14，totalVotes=123，id_no=129367546（public notebook，competition_sources=[kaggriculture]）
- 拉取物: `kaggriculture-multi-route-farming-agent.ipynb`，sha256 `4ce77b8e00a3100e18813d5d2bbe548d2c622ff3bf6ef2255b398c30dcb8ecc7`，882916 B（2 cell）
- 定性: 公开件重打包（Apache-2.0 声明）；本次仅作**对手池实测**，不入产线、不在线提交
- 归档文件清单: `SHA256SUMS.txt`（全件）+ `kernel-metadata.json`（-m 拉取）+ `LICENSE.txt`/`NOTICE.txt`
  （**抽出件非随包**：Apache-2.0 全文与署名自 `agent/base_agent.py` 注释头原样抽出，供合规包引用）

## 上游血统（notebook cell 0 自述 + base_agent.py 头部）

- 上游原件: Aleksei Provorov（leoprovorov）`god-s-mode-hacked-stores`，pinned `scriptVersionId=351167531`
  （https://www.kaggle.com/code/leoprovorov/god-s-mode-hacked-stores?scriptVersionId=351167531）
- 上游自报公开分: **2604.3**（该存档版"observed public score"，cell 0 自报；**未复核，不引作实测数**）
- 重打包自述: "The four executable Python files retain their original SHA-256 digests. Only the
  notebook presentation and archive filename have changed."（flexonafft 只改 notebook 装裱与归档名，四件 py 保真）
- base_agent.py 系谱头部自述: "public V39 (Apache-2.0) plus the v9 layers RACEPX gate, RACE,
  COURIER, CARROT and HERD"；署名保留 thomastschinkel、yhay81、destbreso、aurax7、tetsutani、
  prvsiyan、Dmitrii Gluzdov、Ahmed Berat Ozer（Apache-2.0 衍生，NOTICES 在文件头）

## 载荷与解码（extract_manifest.json 为准）

- cell1 `PAYLOAD_B85`：lzma+base85 单体重载，内嵌 4 py + 2 html；每个文件带 notebook 内嵌
  `EXPECTED_SHA256` 自校验
- 解码方式: 外部离线解码（ast 抽字面量→b85decode→lzma.decompress；**未执行 notebook cell**），
  六件 sha256 逐一与内嵌期望值比对全绿（见 `extract_manifest.json`）
- 零修改: `agent/` 下各件与载荷字节一致，直接当对手跑

| 文件 | sha256 | 字节 | 行数 |
|---|---|---|---|
| agent/main.py | f9588c469d2c1829e46593faeab7efe088a70f6c77d04a78800217350c812ae5 | 358 | 14 |
| agent/base_agent.py | 177d78bdf00aa96579d98052558e18cd3081d29f855c8a6f20a2bbfebcdbda11 | 860103 | 5874 |
| agent/shop_predictor.py | 900b30017b3c97b07d2d4490aca88fabbc419bb9bfd2acb35c73aced8f1fe2ac | 11585 | 282 |
| agent/shop_overlay.py | f4a5d2ecae74a008eba992ca1a9aa0bf8789adc826d8783afd399c8006a4f436 | 13773 | 354 |
| agent/field-shops.html | 847602adebb1381ba0d16a64a5faab35fe997c5870c55b6247e9b49111b64746 | 52553 | （可视化资产，运行时不引用） |
| agent/field-worlds.html | 530ce60e53d5780b9c0bda3945abaf25645b373832b8448af4a7fd0016ed04e5 | 2276701 | （可视化资产，运行时不引用） |

## 入口与机制（一句话）

- 入口: `main.py` 末 callable `agent(observation, configuration=None)`（官方 last-callable 语义；
  `GodModeShopOverlay(base_agent.agent)` 包装，`agent.telemetry` 有遥测）
- 机制: 多路由农事日程磁带（base_agent=公开 V39 系谱+RACEPX/RACE/COURIER/CARROT/HERD 分层尾补）
  + "黑店"预测（shop_predictor 从 hour-23/hour-0 观测过滤 RNG 种子后验→预测未来商店进货）
  + 商店覆盖层改卖单；纯标准库，无网络/文件写；`os.environ["V92_SELL_LIB"]` 仅可选读环境变量

## 执行纪律（本次实测）

- 仅在 bwrap 沙箱内执行（根只读+/tmp 与 lab 目录可写+断网）；不执行任何非测试用途路径；
  **绝不在线提交**（notebook 的打包/submit 流程不运行）
- 只作对手件：装载走外部 harness 适配层 `orderbook_godv7_lab/judge_godv7.py`
  （sys.modules 清 base_agent/shop_* 后按 last-callable 装载=每局全新命名空间，对齐官方逐局隔离语义）

## 引用它的产物/任务

- `fn_work/legacy_software/kaggle_simulations/orderbook_godv7_lab/evidence/godv7_arena.json`
  （godv7 竞技池实测面板与判决，2026-09-30）
