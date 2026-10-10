---
id: arxiv-2610.11164
name: "RideBench: A Large-Scale Exogenous-Aware Benchmark for Ride-Hailing Time Series Forecasting（滴滴网约车外生感知预测基准）"
field: [时序预测, 外生变量建模, 基准数据集]
directions: [数模与时序预测]
published: "2026-10-08"
maturity: demo
venue_tier: arXiv
signal:
  venue: arXiv
  stars: 4
  runnable: true
competition_fit:
  - track: "数模-预测与评估"
    edge: "出行需求预测类赛题（网约车/共享单车/公交调度需求预测）的练手与自评环境：数据自带三大外生场景旋钮（天气扰动/节假日效应/大型事件冲击）恰是此类赛题的难度设计要素，可直接拿来复现实验、预演回答卷里的场景分情景分析；8 周前瞻 2,688 步的长程任务对应赛题'多周调度规划'设定；基准结论（外生变量对周前瞻明确有益、扰动致模式变化仍是短板、点误差/趋势/近期精度难兼得）可作答卷模型选型与误差分析章节的论证框架"
    reuse_cost: "低"
    open_source: "官方 harness github.com/ACAT-SCUT/ridebench（2026-10-10 API 实抓：4 stars、2026-10-09 推送、含 datasets/ridebench/scripts/run_results 完整结构与 uv.lock 锁定环境），数据经滴滴开放平台 outreach.didichuxing.com/opendata/datasets 发布（README 载明渠道，申请流程未逐页核验）"
  - track: "黑客松-数据与算法"
    edge: "出行/需求类数据黑客松的基准级起点数据集：四年×200 区域×半小时粒度（14,025,600 记录、9 个内生目标）足够支撑多区域共享模型与异质性分析，chronological 划分与全预测窗落区协议可直接照搬防泄漏"
    reuse_cost: "低"
sources:
  - url: https://arxiv.org/abs/2610.11164
    title: "RideBench: A Large-Scale Exogenous-Aware Benchmark for Ride-Hailing Time Series Forecasting (arXiv:2610.11164, 摘要页实抓)"
    accessed: "2026-10-10"
  - url: https://github.com/ACAT-SCUT/ridebench
    title: "ACAT-SCUT/ridebench 官方仓（README 与目录结构实抓：数据规格/任务协议/30+ 方法清单）"
    accessed: "2026-10-10"
---

# RideBench：外生感知的网约车时序预测大规模基准

## 是什么

Shengsheng Lin、Jing Hu、Zhengyang Hu 等 11 人（2026-10-08 提交 arXiv:2610.11164，cs.LG，v1；作者谱系此前产出 SegRNN/SparseTSF/CycleNet/TQNet——README 自述）发布的双件套：**Ride-Hailing 数据集**（滴滴 marketplace 数据合成的网约车时序，200 个空间区域×连续 4 年×半小时粒度=14,025,600 条记录，9 个匿名化内生目标变量+连续天气影响因子+节假日（公历/传统/西方节日）+两类大型事件冲击+半小时/星期日历协变量）与 **RideBench 基准**（30+ 方法统一评测：内生专用/外生感知/基础模型三类）。

## 解决什么问题

真实网约车预测需要同时应对规律周期、外生扰动与跨区域异质性，并支撑多周规划；既有研究缺少带受控外生场景的大规模公开数据，导致"外生变量到底帮多少、扰动鲁棒性短板在哪"无法系统量化。

## 任务协议与实证结论

- **两任务**：常规周前瞻（输入 4 周 1,344 步 → 预测 336 步）与长程 8 周前瞻（输入 14 周 4,704 步 → 预测 2,688 步）；时间序划分（前三年训练/次半年验证/末半年测试），样本整窗落入分区，可训练模型跨区域池化训练共享全局模型；
- **结论**（摘要页+README 实抓）：外生变量对周前瞻预测明确有益；但现有模型仍难完整捕捉扰动诱发的模式变化；没有任何模型能同时做到低点误差、准确趋势与可靠的近期预测——与真实业务需求存在错配。

## 局限（如实标注）

- 数据为**合成数据集**（区域与变量匿名化、经变换保留预测相关模式以脱敏），非原始运营数据，结论外推到真实平台需谨慎；
- 官方仓 4 stars 新仓（2026-08-21 建、2026-10-09 推送；arXiv 候选 stars 不设门槛，快照如实记录）；数据在滴滴开放平台发布、README 载明渠道但本次未逐页核验申请流程；
- 覆盖 30+ 方法（含 TSFM）但摘要层未给具体排名数字，引用结论需回论文正文表。

## 如何用于比赛

1. **需求预测类赛题的标准训练场（数模-预测与评估，主用）**：赛前用该数据+官方 harness 完整走一遍"基线→外生感知→TSFM 对比"，其任务协议（多区域池化、chronological 划分、场景分情景评测）与绝大多数需求预测赛题同构，考场上按已验证管线换数据即可；
2. **答卷论证框架**：三大外生场景分情景误差分解 + "点误差/趋势/近期精度不可兼得"的权衡分析，直接构成误差分析章节骨架，并支撑'为什么选带协变量的模型'的选型论证；
3. **长程规划题**：8 周前瞻 2,688 步任务与"多周调度规划"类赛题对齐，可选作长程建模方法（含 TSFM）的压测台；
4. **技术脉络定位**：库内需求预测卡现有 ReasonCast（arxiv-2608.15291，agentic 方法卡）——本卡为**基准/数据层**卡，与方法层互补；与已拒 arxiv-2609.16415（TSFM 行人客流评测、无码）的本质区别在官方 harness+公开数据双落地。
