# -*- coding: utf-8 -*-
"""orderbook_surge_lab —— R14 surge 日卖时判决实验（两阶段全量版，离线判决不开刀）。

结构（fn_docs/hybrid/responsibility.md 【R14 增补】）：
  run_judgment（CLI 编排）
    ├─ corpus_select            （corpus.py，Phase A/B 共用）
    ├─ phase_a_attribution      （phase_a.py）
    │   ├─ daily_netflow_decompose / mark_surge_days / classify_surge_composition
    ├─ phase_b_four_arm_replay  （phase_b.py）
    │   ├─ build_treatment_arm / apply_surge_day_sells
    │   ├─ replay_dual_seat / compare_action_stream
    └─ judge_verdicts           （judge.py）

产物全落本包 evidence/（judgment.json + phase_a_full.json）；零改动既有目录与
在飞件；不上线不提交。
"""
