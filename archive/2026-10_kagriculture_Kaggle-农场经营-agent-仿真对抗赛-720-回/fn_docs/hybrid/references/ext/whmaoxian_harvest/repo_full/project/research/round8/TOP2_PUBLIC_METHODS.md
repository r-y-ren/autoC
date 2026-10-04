# DSM / Vadim：公开方法与源码证据核查

核查时间：2026-09-22 17:27–17:39（Asia/Shanghai）。本项只有公开资料读取；没有运行比赛、读取 confirmation 结果、改变候选或提交文件。

## 结论

**本次没有取得 DSM 或 Vadim Vasilenko 本人公开发布的 Kaggriculture 算法说明、训练流程或完整代理源码。** 这表示“在下面明确列出的公开检索范围内没有找到”，不能扩大为“他们肯定从未公开任何方法”。

确实找到 DSM 成员 masspeaks 本人在本赛题发表的一篇讨论，但内容是提醒参赛者防范冒充工作人员索取代码，并非方法分享。先前对两队生产布局、调度、市场行为的分析，仍属于我们对公开回放的观察与重构。`round8_top2_dsm_compact.py` 是我们的回放重构代理，不能称为“DSM 原代码”，其本地胜负也不能替代对 DSM 实际在线代理的胜负。

## 先核准身份

团队身份来自本轮此前保存的官方排行榜快照 `research/round8/leaderboard.json`，账号显示名与 ID 再由本次官方公开 Profile 接口确认。这里不宣称该快照仍代表即时名次。

| 队伍 | 公开账号 | 用户 ID | 核查入口 |
|---|---|---:|---|
| Vadim Vasilenko；teamId 16770421 | vadimvasilenko | 28274680 | [主页](https://www.kaggle.com/vadimvasilenko) · [Code](https://www.kaggle.com/vadimvasilenko/code) · [Discussion](https://www.kaggle.com/vadimvasilenko/discussion) |
| DSM；teamId 16732748 | denden12（队长） | 2024292 | [主页](https://www.kaggle.com/denden12) · [Code](https://www.kaggle.com/denden12/code) · [Discussion](https://www.kaggle.com/denden12/discussion) |
| DSM | shimishige，显示名 shige | 5486027 | [主页](https://www.kaggle.com/shimishige) · [Code](https://www.kaggle.com/shimishige/code) · [Discussion](https://www.kaggle.com/shimishige/discussion) |
| DSM | masspeaks | 23924550 | [主页](https://www.kaggle.com/masspeaks) · [Code](https://www.kaggle.com/masspeaks/code) · [Discussion](https://www.kaggle.com/masspeaks/discussion) |

DSM 是三人团队，不是一个名为 DSM 的个人账号。搜索得到的 Vadim Timakin、Vadim Irtlach、Vadim Borisov 等其他人均排除，不能借同名结果推断 Vadim Vasilenko 的方法。

## 直接一手讨论

官方赛事元数据返回 competitionId `147734`、forumId `11548702`。对[本赛题 Discussion](https://www.kaggle.com/competitions/kaggriculture/discussion)的公开主题接口读取 11 页，得到 **203 个唯一主帖**，与该次接口报告总数 203 相符。逐项检查 `authorUser.id`，上述四个账号只有以下一篇主帖匹配。

| 作者 | 日期 | 精确来源 | 读到的内容 | 对算法证据的意义 |
|---|---|---|---|---|
| masspeaks，DSM 成员 | 2026-09-19 | [Scam alert: fake “Kaggle Staff” account asking Kaggriculture participants for their code](https://www.kaggle.com/competitions/kaggriculture/discussion/742035) | 作者提醒有人冒充工作人员要求交出完整提交代码；正文和已返回的三条评论均不介绍农业策略、优化器或训练过程。 | 能证明该成员确实发表过本赛题讨论；**不是方法帖，也没有公开代理源码链接**。作者关于团队代码的陈述不能证明其具体算法。 |

此外，在本赛题主题搜索中查询 `denden12`、`shimishige`、`masspeaks`、`vadimvasilenko`、`DSM`、`Vadim`；仅 `masspeaks` 返回上述同一主帖，其余没有返回主题。搜索引擎也查询了队名、全名、四个账号与 `kaggriculture` 的组合，没有取得额外可归属于这两队的一手方法来源。

**范围限制：** 203 个主帖的作者已核对，但没有逐条爬取每篇帖子下全部历史回复。主题搜索也不应当作所有回复都被索引的保证。不能据此断言 DSM 成员在任何评论中都没有讲过技术细节。

## Code 与个人页核查

通过公开前端的 `kernels.KernelsService/ListKernels` 读取匿名可见代码条目，并核对返回条目的作者 ID、标题及关联比赛，而非只凭搜索摘要判断。

| 账号 | Profile 的代码计数 | 本次返回的唯一条目 | 与 Kaggriculture 关联的返回条目 |
|---|---:|---:|---:|
| vadimvasilenko | 0 | 0 | 0 |
| denden12 | 3 | 3 | 0 |
| shimishige | 14 | 9 | 0 |
| masspeaks | 0 | 0 | 0 |

返回的 denden12 条目为 [GOLF_compress_ALL](https://www.kaggle.com/code/denden12/golf-compress-all)、[R2-cup-EDA](https://www.kaggle.com/code/denden12/r2-cup-eda)、[RKCup#1 fastText + SWEM + LightGBM](https://www.kaggle.com/code/denden12/rkcup-1-fasttext-swem-lightgbm-ver)，关联 Code Golf / RKCup，不能作为本赛题的算法证据。

shige 返回的九个条目关联 ShiggleCup-1st/2nd/3rd 和 Data Analysis Contest 2022；完整 URL 清单保存在 `top2_public_methods/summary.json`。**这里存在明确覆盖缺口：个人页计数为 14，匿名清单只返回 9，page 0 与 page 1 返回相同内容，继续读取 page 2 没有新条目。** 没有把重复页计为新条目，也没有把这个接口的 `totalCount: 0` 当作真实代码总数。不能称其所有公开 Code 已完整列举。

Profile 还分别返回 Vadim / denden12 / shige / masspeaks 的 Writeups 计数为 0 / 2 / 1 / 1；未完整展开这些独立 Writeups，所以不据此作不存在的绝对判断。能从搜索确认的 [15th Place Solution](https://www.kaggle.com/competitions/google-code-golf-2025/writeups/15th-place-solution)包含 denden12 作为共同作者，但对象是 2025 Code Golf，不是 Kaggriculture。shige 在 [PTCG 讨论 724094](https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/724094) 对规则型方法的说明同样属于另一个比赛，不能移花接木成 DSM 的本赛题实现。

## 访问方式、限制与可复查记录

- 搜索工具打开多数个人 Code / Discussion 页时只返回空动态页面，部分页面直接报告不可访问。普通 HTTP 访问主页获得的是页面外壳，不足以判断代码或帖子是否存在。
- `/api/v1/kernels/list` 的四次匿名请求均返回 HTTP 401。没有使用或索取凭据。当前没有可用浏览器供动态页面读取。
- 随后静态读取主页引用的公开站点脚本，确认公开读取接口名称；公开 Profile、主题和 Code 前端接口匿名返回 HTTP 200。仅发送查询请求，没有登录、发帖、联系作者或读取私有提交。
- Profile / DiscussionCounts 的 protobuf JSON 会省略零值。本次从同一公开客户端的响应默认值定义确认了这些字段默认值为零，避免把“字段缺失”直接误当成计数零。不同 Profile 与 DiscussionCounts 统计口径出现差异，报告未把它们混用为已阅读帖数。
- 没有找到两队在本赛题公开的策略源码，因此没有新增策略源码下载、解码或执行；也没有根据此次资料改动候选。

所有响应及精简摘要保存在 `research/round8/top2_public_methods/`：

| 证据 | 文件 |
|---|---|
| 身份、可见 Code URL、计数与限制汇总 | `summary.json` |
| 203 主题扫描、请求参数与匹配作者 | `competition_topic_audit.json`、`competition_topics_page1.json` 至 `page11.json` |
| 本赛题账号/队名搜索 | `topic_search_requests.json`、`competition_search_*.json` |
| masspeaks 主帖及评论原始响应 | `topic_742035.json` |
| 四个账号 Profile 与讨论计数 | `*_GetProfile.json`、`*_GetUserDiscussionCounts.json`、`public_profile_requests.json` |
| Code 请求与返回条目 | `kernel_requests.json`、`*_ListKernels_page*.json` |
| HTTP / 动态页面访问限制 | `requests.json`、`*_profile.html` |
| 公开接口名称、客户端零值默认定义的来源 | `api_discovery.json`、`kaggle-public-app.js` |
| 本次文件哈希清单 | `evidence_manifest.json` |

精确公开 API 地址：

- `https://www.kaggle.com/api/i/users.ProfileService/GetProfile`，请求 `{"userName":"对应账号"}`。
- `https://www.kaggle.com/api/i/users.ProfileService/GetUserDiscussionCounts`，同上。
- `https://www.kaggle.com/api/i/kernels.KernelsService/ListKernels`，完整查询体见 `kernel_requests.json`。
- `https://www.kaggle.com/api/i/discussions.DiscussionsService/GetTopicListByForumId`，请求包含 `forumId:11548702`、`page`、`searchQuery`。
- `https://www.kaggle.com/api/i/discussions.DiscussionsService/GetForumTopicById`，请求 `{"forumTopicId":742035,"includeComments":true}`。

## 对最终研究表述的约束

可以写：“我们研究了 DSM / Vadim 的公开比赛回放，并构造可执行重构对手以暴露自身弱点；另从有明确来源和归属的其他公开 Notebook 复用了组件。”

不能写：“拿到了 DSM / Vadim 的代码”“复现了作者算法”“作者使用强化学习/搜索/固定脚本”“已经证明能击败真实第一、第二名”。具体生产和交易机制只能标注为**回放中的可观察行为**；路由选择、优化目标、训练与适应方式仍是我们尚未确认的作者内部实现。
