# guojichuangxin2026 决策纪要（decide 阶段）

> 战役：安航云盾——乡村物流无人机主动安全保障平台；赛事：中国国际大学生创新大赛 2026 高教主赛道·创意组（新工科/低空经济），已报名（报名截止 2026-09-25 已过，人员/组别/类别/名称不可改）。三级赛制：校级初赛 → 省级复赛 → 总决赛 2026-11。校赛材料截止日期待用户补充——按"尽快"节奏执行。

## 入口与定位（2026-10-03）

- `/deliver` 前置闸门拒（无 blueprint.md）→ 战役经 `init_state --campaign guojichuangxin2026 --phase decide` 登记，本会话按 fn-grill 做需求打磨。
- 与隔壁 `workspace/chuangxin2026`（禾策，同一用户任队长的另一项目）为**同赛事两个项目**；用户同意相互借力（当前明确项：SDR/GNU Radio 技术栈与频谱数据复用——见 frontier-tech.md T3）。

## 两轮拷问决策表

| 决策点 | 结论 |
|---|---|
| 战役定位 | 材料冲刺 + 演示级原型（校赛/省赛材料与答辩证据优先） |
| 实飞硬件 | 先仿真雏形+验证，出成果后向导师申请采购/借用（演示级不含实飞） |
| 演示场景（三） | ①低电量+逆风渐进 ②电机故障突发 ③SDR 频谱干扰联动 |
| 前沿补强（采纳三项） | T1 共形预测校准层；T2 DroneMA 式链路一致性检测；T3 SDR 频谱感知站（详见 strategy/frontier-tech.md） |
| 未采纳（存档） | 深度相机备降点评估（二期）、AHFFA/ASSUME 学术纵深包（引用级） |
| 技术栈 | Python 3.11+：pymavlink/MAVSDK-Python + PyTorch + FastAPI/WebSocket；PX4 SITL（Gazebo 主，SIH 备）；边缘=借用 Jetson Orin NX（Python 起步，TensorRT 后置）；训练=RTX 4070 笔记本 |
| 地面平台形态 | 本地 Web（FastAPI+浏览器，单机一键启动） |
| 错误处理/日志 | 降级不中断（质量掩码+分支关闭）；JSON 行日志，运行目录含配置+种子+原始流 |

## 产物指引

| 文件 | 内容 |
|---|---|
| `strategy/README.md` | 产品功能说明（零术语，队员向） |
| `strategy/requirements.md` | 需求文档（R1–R8 含验收方式、术语表、范围外） |
| `strategy/frontier-tech.md` | 前沿技术补强方案（T1/T2/T3+演示地基事实+未采纳存档+合规注记，全部带源） |

## 风险与合规注记

1. 校赛截止日期未定——排期按"尽快"，用户补日期后回填。
2. 一人两队长：KB 未载限报条款，建议与校创新创业学院核实（不阻塞）。
3. 数字纪律：材料数字只出自 metrics 实测；论文数字标注"论文报告值"。
4. AI 辅助原创：AI 产出由团队消化改写，人机分工记录归档保留。

## 下一步

- 用户确认本纪要与 strategy/ 三份产物 → `/attack` 生成 blueprint（把 R1–R8+三场景+metrics 键清单固化为里程碑）→ `/deliver` 交付。
- 修订则直接指出要改的条目，本阶段（decide）可改。
