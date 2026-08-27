---
competition_id: devpost-revenuecat-shipaton-2026
last_verified: 2026-08-28
coverage: []
confidence: 低
sources:
  - url: https://revenuecat-shipaton-2026.devpost.com/rules
    title: "Official Rules §6（17 组评审标准与权重全表——本文件一/四/五节的一手依据）"
    accessed: "2026-08-28"
---

# RevenueCat Shipaton 2026 模式库（patterns）

> coverage 为空（未放榜，2026-10-21 公布）：第一版仅沉淀官方一手评审标准与赛制机制。confidence 低 = 无获奖样本，非信源可疑。

## 一、评审偏好（从章程/评委讲评/获奖名单可观察到的取向）

- **一手证据（rules §6 直抓）**：Grand Prize 是"营收驱动"评审——收入 Top25 初筛 → "Early & Effective Release 15% + Growth by numbers 85%（Downloads/Revenue/Retention，前 30 天）" 定 5 强 → 主办方定冠军。**早上架（8 月初）+ 前 30 天增长数据是决定性权重**。
- 品类奖评审权重呈三类取向（一手）：
  - 数据派：Most Viral（增长率 40%）、Idea to Income（收入 30%）、Growth Loop（可测影响 30%）；
  - 体验派：Design（视觉 50%）、Best Game（好玩 40%）、Peace（有效性 50%）；
  - 工程派：Kotlin（跨平台覆盖 40% + KMP 用法 30%）、Funnel Vision（Stripe 集成质量 50%）。
- 视频纪律（一手）："judges are not required to watch beyond two minutes"——2 分钟硬上限。
- 平台合规即门槛（一手）：真实上架 + 可从美国访问 + 商店 ToS 合规，违者 DQ。

## 二、方法论分布（获奖作品的方法/方案套路）

- 无本届数据。预期回填轴（下轮验证）：首发定价/促销策略（IAP 结构）、Retention 前 30 天运营、KMP 跨端交付效率、AI 辅助开发痕迹（Replit 品类）。

## 三、往届差异化点（什么样的作品拿到了最高奖）

- 无数据（2025 届名单未抓，独立赛站；见 meta 待核清单）。机制级预判（非实录）：Grand Prize 形态决定"能拿最高奖的作品"= 8 月初即首发 + 快速收入验证的 App，而非纯创意 demo。

## 四、反面观察（常见失分模式，若有依据）

- **规则红线（rules 直抓）**：旧 App 更新提交（非全新首发）不合规；一提交报多品类（Next Gen 除外）；demo 视频超 2 分钟评委可不看；提交包缺任一要件（图标/截图/试用码）不完整；俄/古巴/伊朗/朝等地区选手无资格。
- 商店 ToS 违规直接 DQ（含商店政策类风险——如类目合规、支付绕过）。
- 未集成 RevenueCat SDK（或未跑 IAP/广告）即不满足参赛资格（机制推论）。

## 五、赛点检查表（评审标准 → 可执行检查项）

- [ ] 首发上架落在 2026-08-01~09-30 窗口内，且为全新 App（非更新）
- [ ] 至少一个 IAP 经 RevenueCat SDK 管理（或 RevenueCat Ads 投放）
- [ ] 美国 App Store/Play/Galaxy Store 可检索可下载；IAP 试用/兑换码随提交包提供
- [ ] demo 视频 ≤2 分钟且前 30 秒讲清价值主张（评委可在 2 分钟处停止观看）
- [ ] 图标 1024×1024、截图 1179×2556 无设备框——提交要件逐项核对
- [ ] Grand Prize 路线：早上架 + 前 30 天下载/收入/留存数据留痕（App Store Connect / Play Console 截图归档）
- [ ] 品类选择单一（Next Gen 可叠加）；#BuildInPublic 路线：持续社媒更新留痕
- [ ] 商店 ToS 合规自查（支付/隐私/类目）

## 六、对本框架的启示（喂给 K-02 / 验收报告）

- 方向契合：**"真实上架 + 收入验证"是对我方作品工程完成度的最高强度检验**；窗口开放中（首发+提交至 09-30），但需 30 天内完成从开发到上架全链路（苹果审核周期风险须预留）——建议作为快循环"可交付性试金石"而非轻量参赛。
- AI 政策零限制且 Replit 品类正面鼓励 prompt→上架——"AI 辅助原创"合规栈成本为零；合规重心全在商店侧（类目/支付/隐私政策）。
- 评审数据留痕（下载/收入/留存）要求作品自带可量化增长叙事——策略阶段即应设计增长钩子（推荐计划/社媒），对应 Growth Loop 与 Most Viral 两品类。
