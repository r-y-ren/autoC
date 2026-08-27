---
id: tianchi-ijcai18-alimama-cvr
name: IJCAI-18 阿里妈妈搜索广告转化预测（Alimama International Advertising Algorithm Competition）
tier: 编程/黑客松
directions:
  - 黑客松与数据竞赛
status: ended
organizer: 阿里妈妈 × IJCAI-18 × 阿里云天池平台联合举办（天池协议署名 Alibaba Cloud Computing Ltd）
award_levels:
  - name: 决赛一等奖（冠军）
    count_or_ratio: 1 名
    note: 2018 届=DOG（花志祥，京东尚科；天池代号 plants）；总奖池 $37000，分档金额待核验
  - name: 决赛二等奖（亚军）
    count_or_ratio: 1 名
    note: 2018 届=蓝鲸烧香队（周耀、李智、郭鹏博）
  - name: 决赛三等奖（季军）
    count_or_ratio: 1 名
    note: 2018 届=躺分队（陈波成、罗宾理、吴昊；全学生队）
  - name: 创新奖
    count_or_ratio: 2 名
    note: 表彰方法新颖性（2018 届=序列化行为特征设计、end2end 深度学习）
key_dates:
  "赛事周期":
    date: 2018-02 至 2018-05（天池用户协议原文 "from February to May 2018"）
    verified: true
  "决赛答辩与放榜":
    date: 2018 年 6 月上旬（雷锋网 2018-06-19 报道"近日落下帷幕"；决赛答辩于杭州举行）
    verified: false
deliverables:
  - 线上提交预测结果（两阶段：初赛预测第 8 天全天、复赛预测第 8 天下午；logloss 评估）
  - 决赛现场答辩（评奖=复赛成绩+答辩表现）
ai_policy:
  summary: >-
    抓取材料中无 AI 工具使用条款（2018 年赛前 LLM 时代，信息页与用户协议均无此类规定）。天池用户协议 Article 3 约定：竞赛结果 IP 归参赛者保留、提交物须原创、结果限非营利用途（学术研究除外）、向 Alibaba 授予免费不可撤销许可（含商业开发与衍生数据集）；Article 5 主办方保留修改规则/更换评测数据/调整赛程权利。对当代复刻作品含义：可自由使用 AI 辅助，但须叠加本框架"AI 辅助原创"披露，且数据（已沉淀为天池数据集 147588）使用须遵守脱敏数据边界。
  url: https://tianchi.aliyun.com/competition/entrance/231647/rank
  checked: "2026-08-28"
credibility: 交叉验证
last_verified: "2026-08-28"
sources:
  - url: https://tianchi.aliyun.com/competition/entrance/231647/information
    title: 天池官方赛题与数据页（任务定义/logloss 评估/5 表数据结构/final.zip 143.23MB）
    accessed: "2026-08-28"
  - url: https://tianchi.aliyun.com/competition/entrance/231647/rank
    title: 天池官方排行榜页元数据（Bonus $37000/Team 5205/Ended/用户协议英文条款）
    accessed: "2026-08-28"
  - url: https://zhuanlan.zhihu.com/p/40631601
    title: 新智元决赛报道（官方名次/评委名单与讲评/冠军与创新奖方案综述）
    accessed: "2026-08-28"
  - url: https://cloud.tencent.com/developer/article/1166758
    title: 雷锋网 AI 研习社 Top3 方案（腾讯云转载，2018-06-19）
    accessed: "2026-08-28"
  - url: https://www.leiphone.com/category/yanxishe/GdVhajX7Lchr24WF.html
    title: 亚军全方案自述长文（雷锋网，队员笔名 BRYAN/桑楡/李困困）
    accessed: "2026-08-28"
  - url: https://github.com/plantsgo/ijcai-2018
    title: 冠军开源仓库（Graft Learning + Sample Embedding README）
    accessed: "2026-08-28"
  - url: https://github.com/luoda888/2018-IJCAI-top3
    title: 季军开源仓库（特征工程/模型清单/答辩材料原件）
    accessed: "2026-08-28"
---

# IJCAI-18 阿里妈妈搜索广告转化预测

以下正文基于 2026-08-28 实抓（来源编号对应 frontmatter `sources`；快照存于 `kb/raw/tianchi-ijcai18-alimama-cvr/`：information-231647、rank-231647、top3-tencentcloud、github-top3-readme 及 leiphone/zhihu 转述要点见 winners 文件 sources）。

## 定位与价值

- 历史标杆赛（2018，已结束）：阿里妈妈首次公开脱敏线上数据（用户属性/点击曝光/广告商品/上下文/店铺 5 表）做搜索广告 CVR 预估 P(conversion=1|query, user, ad, context, shop)，logloss 评估，线上赛制不设线下赛（来源[1]）。
- 本条目对框架的核心价值是 patterns 素材：公开获奖方案完整度极高的天池经典赛——冠/亚/季军方案均有参赛者一手材料（GitHub×2 + 授权转载长文），已解构至 `winners/2018.md`，模式提炼至 `patterns.md`。

## 规模与结构

- 规模口径三方不一：天池页 Team=5205（来源[2]）；雷锋网"5204 支队伍参赛"（来源[4]）；新智元"50 多个国家 6000+ 选手 5300+ 队伍"（来源[3]）——均如实记录，官方口径以天池页为准但差 1~100 支，不裁决。
- 赛制两阶段（来源[1][3]）：初赛=日常转化率预估（用前 7 天预测第 8 天）；复赛=特殊日期转化率预估（前 7 天+第 8 天上午预测第 8 天下午，目标日为大促型异常流量）。
- 决赛：8 支队伍现场答辩（全部中国队伍），评出一/二/三等奖各 1、创新奖 2（来源[3]）。

## 结果（2018 届）

- 一等奖 DOG（花志祥，京东尚科，天池代号 plants）——嫁接学习（Graft Learning）+ Sample Embedding，核心代码一页（来源[3] + GitHub[6]）。
- 二等奖 蓝鲸烧香队（周耀、李智、郭鹏博，IJCAI-17 冠军团队）——特征群海量工程+多模型融合（来源[3] + 雷锋网长文[5]）。
- 三等奖 躺分队（陈波成/罗宾理/吴昊，前三中唯一全学生队）——异常流量特征工程+四训练集划分（来源[3][4] + GitHub[7]）。
- 逐条深构（骨架/亮点/不足与可改进点/可迁移性）见 `winners/2018.md`。

## 数据资产

- 数据已沉淀为天池公开数据集 147588（来源[1] 页面下载入口指向），可复用于教学/复刻；final 轮数据 final.zip（csv，143.23 MB，来源[1]）。

## 信源与核验说明

- 官方一手[1][2]（天池页面，经渲染抓取；rank 页表格明细未渲染成功，队伍/分数明细缺）+ 媒体二手两路独立（新智元[3]、雷锋网系[4][5]，名次交叉一致）+ 参赛者一手 GitHub[6][7]。整体取"交叉验证"。
- 天池为 SPA 站点：information 页首次缓存模式只得空壳，no_cache 渲染抓取成功；rank 页榜单表未随渲染输出——官方获奖公告原文待主会话 browser-use 预抓复核（记入待办）。

## 待办

1. 天池官方获奖公告/决赛榜单页（含各队复赛 logloss 分数、单项奖金分档）未能直抓，待主会话 browser-use 预抓 `tianchi.aliyun.com/competition/entrance/231647`（rank/notice/forum）后补验 winners 名单数据节。
2. 决赛答辩日精确日期（媒体报道口径 6 月上旬，另有至顶网 2018-06-06 报道线索但其站反爬未能直抓）待第二源核验。
3. 队员真名↔笔名映射（BRYAN/桑楡/李困困 ↔ 周耀/李智/郭鹏博）未逐一核实。
4. 决赛 8 队中未获奖 5 支名单未获取（低优先级）。
