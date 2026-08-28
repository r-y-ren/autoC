---
id: gh-memovai_mimimodel
name: "MimiModel: $5 ESP32-S3 上的全离线工具调用 LLM 引擎（单文件 C）"
field: [on-device inference, LLM agents]
directions: [黑客松与数据竞赛]
published: "2026-08-16"
maturity: demo
signal:
  venue: GitHub
  stars: 89
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "硬件/嵌入式黑客松的『拔网线』卖点：工具调用 LLM 完全跑在 $5 ESP32-S3（无 Linux/无 Python/无网络），断网可用+数据不出设备是隐私叙事的实体证明；13.7MB 权重常驻 flash 永不进 RAM 的原位解码工程（Walsh-Hadamard 恒等式解 CQ 2-bit）自带可讲的技术深度；MIT + 完整烧录配方，BOM 只要 $5"
    reuse_cost: "中"
    open_source: "https://github.com/memovai/mimimodel（MIT；权重为 HuggingFace Cactus-Compute/needle2）"
sources:
  - url: https://github.com/memovai/mimimodel
    title: "memovai/mimimodel: Tool calling LLM on a $5 chip"
    accessed: "2026-08-28"
  - url: https://raw.githubusercontent.com/memovai/mimimodel/main/README.md
    title: "README 全文（引擎原理/基准/烧录配方/局限自述）"
    accessed: "2026-08-28"
---

# MimiModel：$5 微控制器上的全离线工具调用 LLM 引擎

## 是什么

memovai 于 2026-08-16 开源的单文件 C99 推理引擎（约 2000 行，除 libm 零依赖；89 star/8 fork，API 实查 2026-08-28）：在 ESP32-S3（240MHz Xtensa LX7、16MB flash、8MB PSRAM，约 $5）上运行 Cactus Compute 的 Needle 2——45M 参数工具调用模型，CQ 2-bit 量化后 13.7MB 权重内存映射常驻 flash、永不载入 RAM（README 实抓 2026-08-28）。核心技巧：CQ 量化矩阵存为共享球面码本的 2-bit 索引 + 每 128 元素组一个 fp16 L2 范数，利用 (unit·H)·x ≡ unit·(H·x)（H 为 Walsh–Hadamard 矩阵）每 token 只对激活做一次快速 WHT（896 次加法），矩阵乘变成直接读 flash 字节的码本加权点积——模型加载 48ms。注意力取 160 前缀 sink + 最近 256 窗口，int8 KV 共 416 行。实测：google/mobile-actions 961 例严格口径 69.6%，与官方引擎 2.0.2 同输入 69.2% 打平；速度 2.11 tok/s prefill / 1.73 tok/s decode，固定单工具冷启动 32.8s、前缀缓存命中后 14.9s。宿主 CLI（Python）保持串口连接以复用 KV 前缀缓存；工具 schema 以 JSON 运行时导入，改工具不用重刷固件。

## 解决什么问题

无网络/无云依赖场景下"语言模型控制设备"的落地：Cactus 官方引擎在此硬件不可用（计算核为预编译二进制、开源 kernel 只针对 ARM NEON，docs/how-it-fails.md 有源码级拆解），ESP32 又没有 Linux/Python 运行时、RAM 装不下权重——本项目证明"语言理解 + 工具选择"这一层可以下沉到 $5 微控制器且精度不输官方引擎。

## 相比前方法优势

- 相比云端 LLM + 设备执行：断网可用、数据不出设备、零 API 成本——作者诚实标注代价是比云 API 慢数倍；
- 相比官方 Cactus 引擎：绕开两个 Xtensa 阻塞（预编译二进制、NEON-only kernel），纯 flash 原位解码免去每 token 展开 13.7MB（512KB SRAM 根本放不下），严格分数反超官方 0.4pp；
- 相比树莓派级"小型 LLM"方案：$5 BOM、无操作系统、秒级加载，把"设备内置 NLU"的成本下限拉到玩具级硬件。

## 局限（如实标注）

- 速度硬伤：decode 1.73 tok/s，一条工具指令热缓存也要约 15s——只适合离散设备命令，不适合对话或高频控制（作者自述"比云 API 慢数倍"）；
- 只懂英文；对无关输入会硬调工具（作者自述"你说 hello 它也会调工具"）；与官方引擎分数打平但 name/error 分布仍有差异（作者自述）；
- 工具表受 180-token 检索预算约束（捆绑三工具 profile 以内），更大的工具集会改变有效前缀、破坏缓存命中；
- 工程链路长：ESP-IDF v5.5+ 构建 + 烧录 13.7MB 权重到指定分区，且有已知的分区表踩坑——SPIFFS 分区压到权重区会首启自动格式化、静默读出 0xFFFF 变 NaN（作者自述为此赔了一个下午）；
- 依赖第三方生态：模型规格（.cact）与权重（HuggingFace Cactus-Compute/needle2）不在本仓库控制内；项目年轻（创建 2026-08-16，08-22 后无推送，API 实查 2026-08-28）。

## 如何用于比赛

1. **硬件/嵌入式黑客松（主用）**：做"离线优先"智能硬件作品——语音/文本指令控制家电、无网环境巡检、传感器节点本地决策——"拔掉网线照样听懂指令"是评审看得见的演示，$5 BOM 让"可量产"叙事成立；on-device inference 主题黑客松可直接复用其"精度对齐官方引擎"的实测口径（961 例、严格评分）做技术可信度证据。reuse_cost 中：板子便宜，但必须赛前完成 ESP-IDF 环境搭建与烧录演练（约半天）。
2. **演示型组件复用**：其"一次生成跑任何工具表"的运行时 schema 导入设计，适合作为赛品中"本地指令理解模块"的黑盒组件——输出工具调用 JSON、执行层自己写。
