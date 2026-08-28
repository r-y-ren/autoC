# 框架级信源目录（方向冷启动的弹药库，K-09 消费）

> 用途：`/discover <方向>` 时按本目录展开搜索分片。每条信源标注类型/覆盖/抓取方式/信源等级。
> URL 以**实抓验证**为准（本目录只承诺入口检索式，不承诺 URL 永久有效）；失效信源在跑批记录中记待办。
> 合规底线：只抓公开页，不注册、不登录、不绕墙（AGENTS.md 铁律 1）。

## ⚠ SPA 站点清单与预抓规则（P1 机制，源于 2026-08-27 Nova 失真快照事故）

以下站点为纯 JS 渲染，子 agent 的 WebFetch 只能拿到空壳，**搜索快照转引已被实证会引入编造内容**：

| SPA 站点 | 涉及方向 |
|---|---|
| devpost.com（含各赛事子域） | 黑客松类 |
| kaggle.com（列表与详情页） | 黑客松类 |
| tianchi.aliyun.com（详情页；注意连续抓取会串页污染） | 黑客松类 |
| heywhale.com（页面 SPA；公开 API 可直用） | 黑客松类 |
| lablab.ai | 黑客松类 |

**规则**：上表站点的页面事实，由**主会话用 browser-use 预抓快照**落 `kb/raw/<id>/` 后交给分片消费；
分片在无本地快照时只能把搜索结果当**线索**，必须上报请求预抓——不得将搜索快照作为唯一事实源写入条目。


## 学科竞赛类（tier=学科竞赛）

| 信源 | 类型 | 覆盖 | 抓取方式 | 信源等级 |
|---|---|---|---|---|
| 中国大学生在线（dxs.moe.gov.cn） | 教育部官方平台 | 挑战杯/数模/互联网+等国赛通知、论文展示 | WebFetch/固定栏目 | 官方 |
| 挑战杯官网（tiaozhanbei.net） | 官方 | 挑战杯/创青春：章程/名单/作品库 | WebFetch + WebSearch 定位 | 官方 |
| 中国国际大学生创新大赛服务网（cy.ncss.cn） | 官方 | 互联网+（现名）：通知/项目库/金奖名单 | WebFetch | 官方 |
| 国家级大创计划平台（检索式："国家级大学生创新创业训练计划 年度立项 名单"） | 官方 | 大创立项名单/结题要求 | WebSearch 定位后 WebFetch | 官方 |
| 赛氪（saikr.com） | 聚合 | 全类赛事通知/名单（部分为官方合作渠道） | WebFetch | 聚合（官方合作可升半级） |
| 各赛官网（数模 mcm.edu.cn / COMAP / mathorcup.org 已实证） | 官方 | 单赛全量信息 | sync_competitions 锚点 | 官方 |
| 高校教务/学院转发页 | 二手 | 通知佐证 | WebSearch | 二手·降级 |

> ⚠ 公众号是挑战杯/互联网+类的主发布渠道之一——RSSHub 引入条件 = 该类方向启用时（D5/D7 判定链）。

## 编程/黑客松类（tier=编程/黑客松）

| 信源 | 类型 | 覆盖 | 抓取方式 | 信源等级 |
|---|---|---|---|---|
| Kaggle（kaggle.com/competitions） | 官方 | 数据竞赛：在赛/往赛/奖金/评测指标 | WebFetch（页面公开；API 需 key=E-08 可选）；**SPA 绕行**：官方内容接口 `kaggle.com/api/i/competitions.PageService/ListPages?competitionId=<id>` 匿名可访问，赛 ID 从 SSR 壳 og:image URL 提取，可取 rules/evaluation/timeline/prizes 全文（2026-08-28 分片 A 实证；Timeline 页 deadline 偶为模板变量需回退渲染抓取） | 官方 |
| devpost（devpost.com/hackathons） | 实例平台 | 全球黑客松：赛程/获奖项目+代码+评委评语公开 | WebFetch（JS 渲染页用 browser-use） | 平台一手 |
| MLH（mlh.io/seasons） | 组织方 | 北美黑客松季历 | WebFetch | 平台一手 |
| 阿里天池（tianchi.aliyun.com/competition） | 官方 | 国内数据竞赛：赛题/奖金/榜单 | WebFetch（公开页） | 官方 |
| 和鲸社区（heywhale.com）/ Datawhale 赛事页 | 社区 | 国内数据赛事/学习赛聚合 | WebFetch | 社区·降级 |
| CSDN/知乎赛题解析 | 二手 | 往届方案解读 | WebSearch | 二手·降级（仅佐证） |

## 前沿科技（KB-2，全方向共用）

| 信源 | 状态 |
|---|---|
| arXiv API（cat+abs 收紧查询） | ✅ 已实证（sync_tech） |
| GitHub 搜索（gh CLI，已登录） | ✅ 已启用 |
| HuggingFace Papers（/api/daily_papers，免鉴权） | ✅ 已接入（sync_tech，方向 yaml 显式开启；upvotes≥门槛+关键词过滤；与 arXiv 共用 arxiv-* ID 自然去重）⚠ 本机网络当前直连/镜像均超时→按设计告警跳过，网络恢复或配代理（api 条目 base:）即自动生效 |
| ~~Papers with Code~~ | ❌ 已关站（2025-07，Meta 与 HF 合作收尾，域名重定向 HF Trending Papers；2026-05 在 HF 重启为 PapersWithCode 新版）——不再作独立信源，功能经 HF Papers 覆盖 |
