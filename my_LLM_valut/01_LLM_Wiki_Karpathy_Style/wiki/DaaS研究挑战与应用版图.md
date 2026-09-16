---
tags: [主题, DaaS, 综述, 研究挑战]
created: 2026-04-07
updated: 2026-04-09
sources:
  - ../raw/markdown/hamdi2025DroneasaserviceResearchChallenges.md
  - ../raw/markdown/alkouz2022InflightEnergydrivenComposition.md
  - ../raw/markdown/li2025UAVassistedMicroserviceMobile.md
  - ../raw/markdown/rizvi2025MonitoringInterdroneService.md
  - ../raw/markdown/roy2025ServHUServiceHandoff.md
  - ../raw/markdown/xu2024HolisticHybridService.md
  - ../raw/markdown/xu2025WindawareServiceProvisioning.md

---

# DaaS研究挑战与应用版图

## 主题概览
这条分支把 DaaS 组织成一张很清晰的三维地图：功能版图、研究任务版图和应用域版图。它的价值不在于给出某个最优算法，而在于告诉我们“服务化无人机系统真正要研究哪些层面”，以及这些层面如何落到可执行的服务组合上。

## 功能版图
- 感知：多光谱、热红外、LiDAR、污染传感等能力以服务形式输出。
- 巡检：把感知和云/边计算结合起来，形成实时检查、诊断和处置服务。
- 配送：将包裹、急救物资、教材、食品等交付任务包装为带 QoS 的服务。
- 娱乐：灯光秀、竞速、沉浸式互动等场景强调群体编排与用户体验。
- 影像：航拍、直播、跟拍和媒体生产强调稳定性、合规性和人机交互。
- 通信：把无人机作为空中通信平台，为灾后或偏远区域提供临时覆盖。

## 应用域版图
- 非商业域：应急响应、公共安全、城市规划、医疗与辅助技术。
- 商业域：电商、农业与食品、媒体、旅游与娱乐。
- 这说明 DaaS 不是单一配送问题，而是一个横跨公共服务与商业服务的平台型系统。

## 研究挑战版图
- 通信与数据管理：多层 IoT 环境中的实时数据处理与高效传输。
- 环境不确定性预测：天气、能见度、温度与风场影响路径、时延和可达性。
- 成本估计：成本受 QoS、环境、维护、生命周期和调度优先级共同影响。
- 用户控制管理：隐私、监管、个性化 QoS 和用户信任问题。
- 安全保障：硬件故障、软件错误、用户误用和极端环境下的服务失效。
- 调度：实时请求、动态重分配和利润导向的服务编排。
- 能耗优化：飞行、计算、通信与环境条件共同决定服务持续能力。
- 选择与组合：单服务不足时需要多服务拼接，同时还要处理不确定性与法规。
- 群智感知：多无人机数据采集下的带宽、能量和可靠性问题。
- 网络安全：GPS spoofing、hijacking、de-authentication 等攻击。
- 无人机群即服务：群体路径规划、避碰与机间通信。
- 人机交互：语音、手势、多模态接口以及 3D 空间中的可用性设计。

## 从挑战地图到可执行实例
- [[Alkouz2022_飞行中能量驱动的无人机群服务组合]] 把 DaaS 中“服务选择与组合”具体化为可求解问题。
- 它说明 DaaS 不只是概念 taxonomy，还可以进一步落到任务分配、能量共享和群体执行链条的联合优化。
- 这让 DaaS 分支和当前 UAC 研究库里的[[多无人机协同]]、[[服务放置]]开始产生更实质的交叉。
- [[Li2025_灾后医疗救援的UAV辅助微服务MEC架构]] 进一步说明，DaaS 可以与微服务 MEC 融合，进入灾后医疗等高时效服务场景。
- [[Roy2025_Serv-HU面向UaaS的服务接力机制]] 把“多服务商之间如何不断档交付”写成平台机制设计问题。
- [[Rizvi2025_面向韧性运行的无人机间服务干扰监测]] 和 [[Xu2025_多包裹无人机配送的风感知服务供给策略]] 则分别把运行韧性与风场环境约束接到 DaaS 分支上。
- [[Xu2024_MEC无人机末端配送的整体混合服务选择]] 则把静态组合和动态重选一起带进服务选择主线。

## 对当前 UAC 研究库的启发
- 它提醒我们，不要把问题只写成“卸载 + 轨迹 + 资源”三件套；一旦系统面向真实服务交付，还要写清服务角色、用户控制和交付约束。
- 它把“服务选择与组合”抬升为核心问题，这对你未来做系统级问题定义很有启发。
- 它把 swarm、cybersecurity、HDI 和 cost estimation 放进同一张图里，有助于发现当前 UAC 语料尚未系统覆盖的方向。
- 它特别适合在综述或开题中作为“邻近范式”，帮助说明为什么需要从性能优化走向服务系统设计。
- Batch_09 的价值在于把 DaaS 从“概念与挑战图”继续推进到“连续交付、韧性监测、环境感知供给和微服务编排”四类可执行机制。
- 这意味着你后面写服务系统时，可以把 DaaS 不仅当作背景范式，也当作问题构造来源。


## 相关页面
- [[无人机即服务（DaaS）]]
- [[服务化无人机三层架构模型]]
- [[无人机即服务（DaaS）与空中计算的关系]]
- [[Alkouz2022_飞行中能量驱动的无人机群服务组合]]
- [[Li2025_灾后医疗救援的UAV辅助微服务MEC架构]]
- [[Rizvi2025_面向韧性运行的无人机间服务干扰监测]]
- [[Roy2025_Serv-HU面向UaaS的服务接力机制]]
- [[Xu2024_MEC无人机末端配送的整体混合服务选择]]
- [[Xu2025_多包裹无人机配送的风感知服务供给策略]]
- [[安全与服务保障]]
- [[多无人机协同]]
- [[空中计算]]

## 来源
- [Hamdi2025 原文](../raw/markdown/hamdi2025DroneasaserviceResearchChallenges.md)
- [Alkouz2022 原文](../raw/markdown/alkouz2022InflightEnergydrivenComposition.md)
- [Li2025 Microservice MEC 原文](../raw/markdown/li2025UAVassistedMicroserviceMobile.md)
- [Rizvi2025 原文](../raw/markdown/rizvi2025MonitoringInterdroneService.md)
- [Roy2025 原文](../raw/markdown/roy2025ServHUServiceHandoff.md)
- [Xu2024 H2S2 原文](../raw/markdown/xu2024HolisticHybridService.md)
- [Xu2025 原文](../raw/markdown/xu2025WindawareServiceProvisioning.md)
