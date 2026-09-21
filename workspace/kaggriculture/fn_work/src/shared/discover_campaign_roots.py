"""程序化发现战役根/仓根/软件根（目录特征过滤：含 blueprint.md+software+fn_docs 者=战役根），返回 campaign_root/repo_root/software_root 具名结构，取代一切字面战役路径与"仓根 CWD 假设"，找不到特征目录即抛 RootDiscoveryError（fail-closed，不猜）。

上游: R20（详见 fn_docs/responsibility.md）
"""


def discover_campaign_roots(start_path=None) -> dict:
    raise NotImplementedError("unimplemented:fn:discover_campaign_roots")
