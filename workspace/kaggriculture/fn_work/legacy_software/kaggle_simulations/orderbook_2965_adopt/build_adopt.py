def build_2965_adopt():
    """编排：fetch→merge→constants→audit→双件确定性打包+manifest（sha 链沿 r30 格式）。"""
    raise NotImplementedError("unimplemented:fn:build_2965_adopt")


def fetch_2965_source(kernel_slug):
    """拉取/解码 2965 公开件源+sha 登记；失败重试。"""
    raise NotImplementedError("unimplemented:fn:fetch_2965_source")


def merge_increments(l3_main_path, src2965_path, out_path):
    """三增量 AST 受控移植+移除 layer S 尾块（EXP402 替代）→r34a；变更集白名单审计。"""
    raise NotImplementedError("unimplemented:fn:merge_increments")


def apply_2965_constants(r34a_main_path, out_path):
    """layer-D 三常数恰三处替换（3/−5/20）→r34b。"""
    raise NotImplementedError("unimplemented:fn:apply_2965_constants")


def audit_diff_vs_2965(r34a_path, r34b_path, src2965_path):
    """双件对原件逐字节差异归因；白名单外差异=红。"""
    raise NotImplementedError("unimplemented:fn:audit_diff_vs_2965")
