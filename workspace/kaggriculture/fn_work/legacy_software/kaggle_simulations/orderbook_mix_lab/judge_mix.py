"""R15 三出口判据—骨架桩（fn-scaffold）。职责规约见 fn_docs/hybrid/responsibility.md 【R15 增补】。"""
def judge_mix_verdicts(openloop_result, closedloop_result):
    """逐变体：≥2/3 翻正+胜局违例 ≤2+Δ 中位>0→开环 POSITIVE；+闭环互胜 ≥0.5→POSITIVE；整体三出口+敏感度。"""
    raise NotImplementedError("unimplemented:fn:judge_mix_verdicts")
