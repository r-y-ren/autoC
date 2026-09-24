"""R15 参数扫描变体生成—骨架桩（fn-scaffold）。职责规约见 fn_docs/hybrid/responsibility.md 【R15 增补】。"""
def generate_mix_variants(swap_pairs, scales=(0.10,0.20,0.30), max_variants=16):
    """置换对×幅度展开→排程→可行性→变体 main 构建；全不可行→KILLED 依据。"""
    raise NotImplementedError("unimplemented:fn:generate_mix_variants")


def build_variant_schedule(pair, scale, base_schedule):
    """复用 giant_route gen_schedule：from 品产能窗 X% 迁 to 品的逐日排程。"""
    raise NotImplementedError("unimplemented:fn:build_variant_schedule")


def check_variant_feasibility(schedule):
    """孪生空跑逐日校验（劳动/现金/棚容/停时）。"""
    raise NotImplementedError("unimplemented:fn:check_variant_feasibility")


def build_variant_main(schedule, l3_base_path, out_path):
    """磁带产线事件手术产变体 main.py+diff 审计；手术超界即弃。"""
    raise NotImplementedError("unimplemented:fn:build_variant_main")
