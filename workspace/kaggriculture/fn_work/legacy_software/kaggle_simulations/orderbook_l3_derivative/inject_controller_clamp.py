"""inject_controller_clamp（R13 L1）：基座中部受控手术——CARROT2 目标项钳制（fine/coarse）。"""
# CLAMP_HELPER_SRC 常量承载 _ca_future_plant_demand 源文本（独立可测，注入时随钳制插入基座）


def inject(base_main_path, mode="fine") -> dict:
    """行 4695 目标项替换+helper 插入；变更集恰{一 def+一表达式}；五区零改动断言。"""
    raise NotImplementedError("unimplemented:fn:inject_controller_clamp")
