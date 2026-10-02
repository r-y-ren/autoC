# -*- coding: utf-8 -*-
"""orderbook_p4up_lab —— P4 判决尺升级：destbreso X-ray 六判据 + leoprovorov p25 磁带长度表（工具级）。

责任口径（P3 判决尺升级，2026-10-02）：
- 六判据（GLOBAL vs WITHIN-WORLD / 血缘谱镜像线 / 收敛三件套 / 语言指纹三分 /
  crater 卖压 / 热图半分相关闸）= destbreso《x-ray your agent》13 节诊断 harness 的
  工具级移植（cell 13-27/32-37，MIT/CC0 状态见其 provenance.md：无许可证声明、
  作者明示 fork 自用）；判据定义可引用，代码为忠实移植改写（纯 stdlib、去绘图、
  数值口径不动）。
- leoprovorov《A Song of Ice and Fire | Final Update》cell 16 ROWS p10/p25/p50
  11 队硬数据 → data/opponents_baseline.json（对手画像基线，判决分层用）；
  D(t)/p_q 公式见 divergence.py（cell 11/17 数学区口径）。
- x-ray 自校准数字（53.8% unit-turn、490 seat-seasons、08-30 #1 形状、语言指纹
  校准锚、盲测 7/7）一律标"自报"，只入 CRITERIA_SPEC 注记，不作我方读数。
- 只落本目录（新增文件+测试+样例输出）；不改既有 judge/实验室文件；不 commit；
  不在线提交；阈值随判声明纪律（"a verdict quoted without its threshold is not
  a verdict"，cell 33）在每条判据输出里强制携带 threshold 字段。

输入模型：records.EpisodeRecord（回放全流 720 拍 或 feats-band day0 片段）；
adapters 提供 replay blob（kaggle-environments JSON）与 feats-band 行两个入口。
"""
