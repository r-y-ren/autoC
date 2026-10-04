# destbreso-xray 外部件血统记录（X-ray your agent，诊断工具向）

## 件对象

- 名称: destbreso-xray（本战役代号）；notebook 标题 "X-ray your agent"
- 来源 URL: https://www.kaggle.com/code/destbreso/x-ray-your-agent
- ref: `destbreso/x-ray-your-agent`
- 拉取时间: **2026-10-02 10:39 UTC**（`kaggle kernels pull … --metadata`，CLI 2.2.4）
- kernel 元数据（pull -m 实查）: author=destbreso，id_no=**132616249**，is_private=false，
  enable_internet=true，keywords=[scheduled]，competition_sources=[kaggriculture]，
  dataset_sources=[]；**scriptVersionId**: CLI 不暴露（同 leoprovorov-iaf-final 说明），
  以 id_no + SHA 内容锚代替
- 拉取时榜面读数: totalVotes 52（收官登记 52 @09-30 23:31）；lastRunTime
  2026-10-01 22:57:56（截止后例行重跑，`scheduled` 日更件）
- 拉取物: `x-ray-your-agent.ipynb`，sha256
  `3ca5da4f9d0b3be8f6e141e92be24f38a36a69e52067e9a850dc2e098b66f2df`，98,686 B，41 cell
- **内容锚定（重要）**: 该 SHA 与 /home/renyxin/fn28_cache/nb/x-ray-your-agent.ipynb
  （2026-09-28 12:18 我方拉取）**逐字节相同** → 收官 run（09-30 23:01 登记）与截止后 run
  （10-01 22:57）均为**纯重跑，无内容增量**；本件自 09-25 起内容未变
- 定性: 公开诊断工具（对任意 submission 出 X-ray 报告），scheduled 日更；
  本次仅作**方法拆解**，不入产线、不在线提交
- 归档文件清单: `SHA256SUMS.txt`（全件）+ `kernel-metadata.json`（-m 拉取）+ 本文件

## 许可

- notebook 本文: **未附 SPDX/许可证声明**（Kaggle notebook 默认版权）；作者在 cell 0 明示
  开放姿态——"fork it and put your own id in the next cell to x-ray yourself"（邀请 fork 自用）
- 引用的第三方资产（件内标注）: georgymarin/kaggriculture-episodes 数据集（爬虫端点出处，
  cell 0/40 致谢）；destbreso/kaggriculture-benchmark-matchups 数据集（45k 对局重放，
  件外标注 **CC0**，见 georgymarin 件 cell 6 转述）
- 代码迁移注意: 公开端点（EpisodeService/ListEpisodes、kaggleusercontent 回放 CDN、
  LeaderboardService/GetLeaderboard）为 Kaggle 非公开 API 形态，可能随时变更（cell 3 自带
  ladder-climb fallback）；移植代码需保留该 fallback 纪律

## 本次实抓纪律

- 结论口径=本次拉取 ipynb 全文（41 cell 逐格读毕）；件内所有校准数字（53.8% 步行占比、
  490 seat-seasons 用工共识、2026-08-30 宏观基准、2026-09-10 d18 番茄普查、2026-09-04
  语言指纹锚等）均为作者**自报**；本次未运行（运行需逐局拉取 ~25MB 公开回放，且比赛已截止、
  实时榜语义已死，运行不产生新结论）
