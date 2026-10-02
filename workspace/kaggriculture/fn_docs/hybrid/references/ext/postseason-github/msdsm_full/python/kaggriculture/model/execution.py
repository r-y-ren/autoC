"""Explicit, serializable numerical paths; CPU inference retains the dense FP32 path."""

from functools import partial


def forward_options(variant: str, *, platform: str = "gpu") -> dict:
    if variant not in ("baseline", "latest", "selected"):
        raise ValueError(f"unknown execution variant: {variant}")
    if variant == "baseline" or platform == "cpu":
        return {}
    if platform != "gpu":
        raise ValueError(f"unsupported execution platform: {platform}")
    from kaggriculture.model.kernels.selective_attention import fused_selective_attention

    options = {
        "partition_kernel": partial(fused_selective_attention, block=64, precompute_delta=True, compact_upstream=True),
        "remat_ffn_activation": True,
    }
    if variant == "selected":
        from kaggriculture.model.kernels.selective_attention import fused_selected_attention

        options.update(
            prune_final_queries=True,
            selected_partition_kernel=partial(
                fused_selected_attention, block=64, precompute_delta=True, compact_upstream=True
            ),
        )
    return options
