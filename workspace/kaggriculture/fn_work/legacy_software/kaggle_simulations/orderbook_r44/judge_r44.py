# r44 判决线（三形态同局配对+单件消融+安慰剂；realized_price_stats 复用 judge_r26 不立桩）
def judge_r44(packages, corpus, config):
    """判决 v27：三形态 vs r40 同 seed 双席配对+消融（B 效应=AB vs A 边际）+安慰剂（B 单≡r40 逐字节；A 非触发拍零足迹）；判据=A 臂实现价≥0.80∧终局钱+2k~4k∧h2h≥0.55；B 臂等价面恒等∧AB 边际>0。输出: evidence JSON / 错误: 单局红计入不短路"""
    raise NotImplementedError("unimplemented:fn:judge_r44")
def pick_launch_form(evidence):
    """择优单发（用户裁决）：按判据达成数>h2h>实现价从 {A,B,AB} 取唯一发射形态+落选收档标记+计分对核对（第 2 发挤 r37 保 r40）。错误: 无形态达标→不选（全收档）"""
    raise NotImplementedError("unimplemented:fn:pick_launch_form")
