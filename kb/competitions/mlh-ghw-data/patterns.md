---
competition_id: mlh-ghw-data
last_verified: 2026-08-28
coverage: []            # 赛事未开（2026-09-11~09-17，upcoming）且为积分制（无获奖名单层）——无任何届次获奖数据；本文件全部为官方页面与规则文本反推
confidence: 低           # 官方三源 + 规则全文直抓（信源等级高），但积分制无获奖层、挑战清单未发布——模式层零实证，综合如实取低
sources:
  - url: https://events.mlh.com/events/14416-global-hack-week-data
    title: "GHW: Data 注册页（积分制/挑战三类/高阶挑战口径/参与对象——一手依据）"
    accessed: "2026-08-28"
  - url: https://ghw.mlh.com/events/data-week
    title: "GHW Data Week 专题页（免费宣言/技能主线 SQL·数据库·可视化）"
    accessed: "2026-08-28"
  - url: https://github.com/MLH/mlh-hackathon-rules/blob/master/Rules.md
    title: "MLH 官方 Hackathon Rules（评审四等权与'明示不评'清单/工作期与代码复用边界/AI 条款核对）"
    accessed: "2026-08-28"
  - url: https://www.mlh.com/seasons/2027/events
    title: "MLH 2027 赛季日历（GHW: Data 条目时间互证）"
    accessed: "2026-08-28"
---

# MLH Global Hack Week: Data Week 2026 模式库（patterns）

> 本文件是 KB-1 条目的解构总结层：供 K-02 赛道评分（"获奖模式重叠"维度）、验收分析报告与赛点检查表消费。
> **轻 量 赛 事 声 明**：GHW 为挑战积分制（social/technical/design 三类 + 直播签到），无现金奖池、无传统获奖名单层（快照：`kb/raw/mlh-ghw-data/2026-event-pages.md`，2026-08-28 实抓）。本文件为官方规则文本反推，对 K-02"获奖模式重叠"维度贡献低（meta 已注）；六节结构保持完整以备 09-17 收官后按实证刷新。

## 一、评审偏好（从章程/评委讲评/获奖名单可观察到的取向）

- **一手（MLH 规则全文）**：项目类评审四等权——Technology / Design / Completion / Learning；**明示不评**：代码质量、演讲质量、创意原创性、实际用处。对"完成度与学习"的制度性偏重是该规则体系最独特的取向。
- **口径映射声明（推断，标注）**：上述四维属 MLH hackathon 项目评审规则；GHW Data 的实际"得分口径"是挑战积分（注册页原文：完成挑战 earn experience points + 每次直播签到 1 分），非项目评审——两者不能直接等同，本文件按"挑战完成口径"为主、"四维规则"为项目类挑战的参照框架处理。
- **一手（注册页）**：挑战从社交帖级到 "building a project and creating a full demo video" 级——高阶挑战的完整口径 = 完整项目 + full demo 视频。
- **一手（专题页）**：技能主线为 SQL / 数据库实现 / 数据可视化（"job ready technical skills"）——挑战主题围绕数据工程基础而非前沿模型。

## 二、方法论分布（获奖作品的方法/方案套路）

| 模式 | 出现频次/占比 | 代表年份与条目 | 可迁移性 |
|---|---|---|---|
| （空表） | 不可用 | 不可用 | 不可用 |

**声明**：积分制无获奖名单层，且赛事未开——方法论分布层为零，不可统计亦不可推断；GHW 系列历届是否公布优秀项目展示尚待实证（meta 待核验 3）。**刷新触发**：2026-09-17 收官后，若官方公布挑战榜/优秀项目（ghw.mlh.io/challenges 与 Devpost 惯例渠道）则补抓回填；否则本节长期保持空表。

## 三、往届差异化点（什么样的作品拿到了最高奖）

- 本赛制**无"最高奖"概念**（积分兑 MLH 周边 swag，注册页原文）——传统差异化分析不适用。
- 可证的结构性观察（注册页原文）：得分阶梯 = social 帖 < technical 构建 < design 挑战 < "完整项目 + full demo 视频"（高阶）——在本赛制内"拿到高分"的路径是把挑战做成完整项目并配完整 demo 视频。

## 四、反面观察（常见失分模式，若有依据）

- **一手红线（MLH 规则原文）**：All work on a project should be done at the hackathon——不可复用既有代码（想法可延续）；允许第三方库/框架/开源代码；赛前开源以供赛中使用"违反规则精神"（against the spirit of the rules）。
- **AI 条款（一手，全文核对 2026-08-28）**：规则无任何 AI/generative AI/LLM 限制或授权条款——无 AI 相关失分红线，也无常设署名义务（与 Devpost 系署名条款不同，注意区分平台）。
- 周边兑现：积分奖励需在 hackp.ac/address 提交邮寄地址（注册页原文）；未载截止时间，如实记录。

## 五、赛点检查表（评审标准 → 可执行检查项）

- [ ] 若走高阶挑战：按"完整项目 + full demo 视频"口径交付（注册页原文），不为攒分做成半成品
- [ ] 全部工作在活动周内完成（09-11~09-17 EDT）；既有代码零复用，依赖走第三方库/开源许可
- [ ] 积分双通道都走：每日 Twitch 直播签到（1 分/次）+ Discord mini-events 参与
- [ ] 挑战类型三线布局：social / technical / design 各有产出（对应积分三类）
- [ ] 周边兑换地址提交（hackp.ac/address）
- [ ] AI 工具自由使用（规则无限制条款），人机分工记录按本框架合规底线自愿留存

## 六、对本框架的启示（喂给 K-02 / 验收报告）

- 方向契合：数据主题（SQL/数据库/可视化）与我方画像直接对口；免费 + 全程线上 + 无门槛——定位为**技能练兵场与低成本作品试验田**，不作 K-02 得分来源（无获奖层，"获奖模式重叠"按空值处理）。
- 产出沉淀：挑战产物（数据可视化/数据库小项目/demo 视频）可作后续黑客松的素材储备与技能证明；规则文本未载 IP/成果转让条款（如实：未见≠不存在，用前不复核不扩散该判断）。
- 机会成本：09-11~09-17 与 lablab 赛期（09-01~09-30）重叠——参与方式宜为碎片化积分挑战，不挤占主线作品窗口。
- 刷新触发：09-11 开幕后补抓挑战清单与积分细则（惯例临赛在 ghw.mlh.io/challenges 与 Devpost 发布，meta 待核验 2）+ 收官后优秀项目实证核查。
