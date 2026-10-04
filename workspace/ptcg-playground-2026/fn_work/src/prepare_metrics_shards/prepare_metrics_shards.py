"""编排分片：runs 归集+回读校验→全局 merge_metrics 消费目录（R10）"""


def prepare_metrics_shards(runs_dir: str, readback_file: str) -> str:
    raise NotImplementedError("unimplemented:fn:prepare_metrics_shards")
