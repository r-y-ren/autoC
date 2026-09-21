"""快照安全网迁移编排：复制九文件、修正 import 根（经 discover_campaign_roots）、跑绿门、出具迁移裁决（任一反例仍 xfail 即不通过）。

上游: R1（详见 fn_docs/responsibility.md）
"""


def migrate_snapshot_suite(source_suite, target) -> dict:
    raise NotImplementedError("unimplemented:fn:migrate_snapshot_suite")
