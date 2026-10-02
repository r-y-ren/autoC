# leoprovorov-iaf-final 外部件血统记录（冰火系列收官篇）

## 件对象

- 名称: leoprovorov-iaf-final（本战役代号）；notebook 标题 "❄️🔥 A Song of Ice and Fire | Final Update"
- 来源 URL: https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-final-update
- ref: `leoprovorov/a-song-of-ice-and-fire-final-update`
- 拉取时间: **2026-10-02 10:39 UTC**（`kaggle kernels pull … --metadata`，CLI 2.2.4）
- kernel 元数据（pull -m 实查）: author=AlekseiProvorov（Aleksei Provorov），id_no=**134330479**，
  is_private=false，enable_internet=true，competition_sources=[kaggriculture]，
  dataset_sources=[leoprovorov/a-song-of-ice-and-fire-interactive-dashboards]；
  **scriptVersionId**: CLI `kernels pull/list` 不暴露该字段（GetKernel RPC 对本机 token 返回
  PERMISSION_DENIED）——以 id_no + 拉取时 lastRunTime 代替版本锚；件内无 pinned 版本 URL。
- 拉取时榜面读数: totalVotes **109**（2026-10-02 18:5x CST list；收官登记 103 @09-30 23:31）；
  lastRunTime 2026-09-30 23:15:01（=收官冲刺登记的 run，拉取后未再变 run 戳）
- 拉取物: `a-song-of-ice-and-fire-final-update.ipynb`，sha256
  `e4e83741123cdaa56438424800a741e773994fb3e218aaa6f77f7c2b6684bf38`，912,579 B，23 cell
  （cell 22=872KB base64 agent 载荷，构建 submission.tar.gz）
- 定性: 冰火系列 Part 3 收官篇=研究文章+交互仪表盘+可复现 agent 构建三合一；
  本次仅作**情报拆解**，不入产线、不在线提交
- 归档文件清单: `SHA256SUMS.txt`（全件）+ `kernel-metadata.json`（-m 拉取）+ 本文件

## 内容版本锚（cell 19 自述）

- 末格提交件版本: **MarketShock-M1-WR1K**（"MarketShock-M1 with one audited day-21 local
  watering repair and exact parent pass-through everywhere else"；= flexonafft v106 打包的
  同源件，见 2026-09-30-kaggle-sweep3）
- 分析部分"unchanged"自述：cell 19 明言 "The original analysis below is unchanged"；
  配套仪表盘数据集三文件 creationDate=2026-09-20 → **分析数据窗约止 2026-09-20**
- 配套数据集 leoprovorov/a-song-of-ice-and-fire-interactive-dashboards **仍公开可下载**
  （ice-fire-1-action-overlay.html 1,163,361B / ice-fire-2-divergence.html 611,064B /
  ice-fire-3-worlds.html 1,839,649B，2026-09-20 创建）

## 许可

- notebook 本文（分析 markdown+仪表盘代码）: **未附 SPDX/许可证声明**（Kaggle notebook 默认
  版权；方法口径可引用，代码照抄需自行斟酌）
- agent 载荷内各件: Apache-2.0 系谱（cell 19 Credits 自述）——router_parent.py/actions.json
  = Yusuke Hayashi `yhay81/shop-router-0909` v3（其上署名 aurax7 Reactive Router）；
  planner 血统 = Thomas Tschinkel public state router（Apache-2.0）；unit_model.py =
  kaggle-environments 1.32.7 抽取（Apache-2.0）；LICENSE.txt/NOTICE.txt 随 submission 打包

## 本次实抓纪律

- 全部结论出自本次拉取 ipynb 原文（cell 序号可溯）；数字均为作者**自报**（写死在 markdown），
  本次未运行其分析代码复核（运行需配套数据集渲染仪表盘，不产生新数字）
