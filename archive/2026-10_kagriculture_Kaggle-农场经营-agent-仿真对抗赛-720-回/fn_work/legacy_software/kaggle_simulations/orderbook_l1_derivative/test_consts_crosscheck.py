"""test_consts_crosscheck：FIRST_HARVEST_STEPS 对 vendored wheel 现值交叉校验（R9/bots 常数看护先例）。

性质：wheel 的 CROPS["*"]["first_yield_day"] 或 turnsPerDay 默认值一旦变化，
本文件变红——layer_s_block 的转录表即失真，须按新真值人工重转录。
来源：本机 vendored kaggle_environments 1.32.7+nodeps（user site-packages），
  envs/kaggriculture/kaggriculture.py 模块 CROPS + kaggriculture.json configuration；
首次转录/抓取日期：2026-09-23。
"""

import json
import os

import pytest

import layer_s_block


def _wheel_facts():
    """读 vendored wheel 的 (CROPS 表, turnsPerDay 默认值)。wheel 不可用→skip（无对物可校）。"""
    try:
        from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    except Exception as exc:
        pytest.skip(f"vendored kaggle_environments 不可用，无从交叉校验: {exc!r}")
    try:
        with open(
            os.path.join(os.path.dirname(engine.__file__), "kaggriculture.json"),
            "r",
            encoding="utf-8",
        ) as fh:
            turns_per_day = int(json.load(fh)["configuration"]["turnsPerDay"]["default"])
    except Exception as exc:
        pytest.skip(f"vendored kaggriculture.json 解析失败: {exc!r}")
    return engine.CROPS, turns_per_day


def test_first_harvest_steps_keys_match_wheel():
    crops, _ = _wheel_facts()
    assert set(layer_s_block.FIRST_HARVEST_STEPS) == set(crops)


def test_first_harvest_steps_values_match_wheel():
    # 转录式：FIRST_HARVEST_STEPS[crop] == CROPS[crop]["first_yield_day"] * turnsPerDay
    crops, turns_per_day = _wheel_facts()
    for crop, info in crops.items():
        expect = int(info["first_yield_day"]) * turns_per_day
        got = layer_s_block.FIRST_HARVEST_STEPS[crop]
        assert got == expect, (
            f"{crop}: 转录值 {got} != wheel 现值 first_yield_day="
            f"{info['first_yield_day']}*turnsPerDay({turns_per_day})={expect}"
        )
