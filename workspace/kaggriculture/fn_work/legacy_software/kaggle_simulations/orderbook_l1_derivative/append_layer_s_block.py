"""append_layer_s_block（R10 L1）：把 layer_s_block 源码注入 L1 副本尾部并过四条校验。"""


def inject(main_path) -> dict:
    """追加尾块并校验：py_compile/AST 可解析/末 callable=_cxs_agent/diff 仅尾部追加；任一红即抛。"""
    raise NotImplementedError("unimplemented:fn:append_layer_s_block")
