"""arena._abnormal_reason 与 eval_contract.game_abnormal_reason 合并为单一实现（字段集分叉对齐后取并集语义）。

上游: R8, R9（详见 fn_docs/responsibility.md）

实现要点（[改造]件，双源=旧树两实现，读旧码定真值）：
- 旧源 A = kgenv/arena.py:27 `_abnormal_reason(result)`：statuses 在场 +
  DONE/DONE + players 为 2 元列表 + rewards 为 2 元数值列表（拒绝 bool 与
  非有限值）+ contract_ok 严格 True + winner_label 与 rewards 推导一致。
- 旧源 B = kgenv/eval_contract.py:155 `game_abnormal_reason(game, *,
  require_export_fields, expected_domain, allowed_seeds)`：必填字段集
  （players/seed/seat/seed_domain/statuses/contract_ok/winner_label/rewards，
  导出面再含 p0/p1/winner/turns）+ players 两两互异 + 座位 AB/BA +
  p0/p1 与 players 一致 + winner 与 winner_label 一致 + 平局 rewards 必等 +
  seed_domain/seed 白名单两个可选判定面。
- 分叉面清单（union 语义取并集，即任一旧实现能判红即红）：
    1. players 两元素相同——仅 B 判（A 只查长度）；并集=判。
    2. rewards 为 bool——仅 A 判（True 是 int 子类，B 的 isinstance 放行）；并集=判。
    3. rewards 非有限（NaN/inf）——仅 A 显式判（B 仅经"平局 rewards 必等"
       对 NaN 间接判红，inf 完全漏判）；并集=显式判。
    4. 缺 seed/seat/seed_domain 等字段——仅 B 判（A 的字段面只有 statuses，
       且其"missing statuses"被 B 的必填字段检查包含）；并集=B 的完整必填集。
    5. require_export_fields/expected_domain/allowed_seeds 三个判定面——
       仅 B 有（A 无对应参数）；并集=保留为可选 kwarg，缺省关闭。
- 判定次序沿 B 骨架（B 是字段超集），rewards 校验点嫁接 A 的严格口径；
  理由串为合并后的新真值（旧两套理由串不保留一一对应，裁决口径以
  "None=正常 / 非 None=异常"为准，测试锚也只锚裁决不锚文案）。
- build_case_battery() 登记并集语义锚定用例集（正常/双源同判红/分叉面
  单源判红/导出面与 kwarg 面），叶测试与顶层 unify_contract_sources
  自检共用，不重复维护两份用例。

适配说明（旧树冻结——物理改线属战后，登记于此）：
- 战后 arena.py 的 `_abnormal_reason(result)` 改为
  `merge_abnormal_reason(result)` 的 re-export/委托（A 的调用面
  run_match/summarize_games 不带 kwarg，与缺省签名直接兼容）。
- 战后 eval_contract.py 的 `game_abnormal_reason(...)` 改为对本函数的
  委托（签名逐参一致，B 的调用面 assert_games_normal/validate_gate_run
  无感切换）；B 的理由串消费者（错误消息拼接）只消费非空性，无文案匹配。
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

__all__ = ["merge_abnormal_reason", "build_case_battery"]

# 必填字段集（并集口径）：B 的完整必填集已包含 A 的 statuses 在场检查。
_REQUIRED_FIELDS = ("players", "seed", "seat", "seed_domain", "statuses",
                    "contract_ok", "winner_label", "rewards")
_EXPORT_FIELDS = ("p0", "p1", "winner", "turns")
_SEAT_PROTOCOL = ("AB", "BA")


def merge_abnormal_reason(game: Dict[str, Any], *,
                          require_export_fields: bool = False,
                          expected_domain: Optional[str] = None,
                          allowed_seeds: Optional[set] = None
                          ) -> Optional[str]:
    """对局记录的异常局判定（arena/eval_contract 双实现的并集语义单源）。

    Args:
        game: 对局记录 dict（含 players/statuses/rewards/contract_ok/
            winner_label/seed/seat/seed_domain 等字段）。
        require_export_fields: 额外要求导出面字段（p0/p1/winner/turns）
            并校验其与 players/winner_label 的一致性（源 B 判定面）。
        expected_domain: 非 None 时要求 game["seed_domain"] 与之相等。
        allowed_seeds: 非 None 时要求 game["seed"] 落在集合内。

    Returns:
        异常理由串（新真值文案）；正常局返回 None。

    Raises:
        无——一切异常以理由串表达（与两旧实现一致，fail 表达在返回值）。
    """
    required = list(_REQUIRED_FIELDS)
    if require_export_fields:
        required.extend(_EXPORT_FIELDS)
    missing = [key for key in required if key not in game]
    if missing:
        return f"missing required game fields: {missing}"
    players = game["players"]
    if (not isinstance(players, list) or len(players) != 2
            or players[0] == players[1]):
        return f"invalid players {players!r}"
    if require_export_fields and [game["p0"], game["p1"]] != players:
        return "players do not match p0/p1"
    if game["seat"] not in _SEAT_PROTOCOL:
        return f"invalid seat {game['seat']!r}"
    if game["statuses"] != ["DONE", "DONE"]:
        return f"non-DONE statuses {game['statuses']!r}"
    if game["contract_ok"] is not True:
        return "contract_ok is not true"
    rewards = game["rewards"]
    if (not isinstance(rewards, list) or len(rewards) != 2 or
            any(isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(float(value)) for value in rewards)):
        # 并集口径：源 A 的严格数值面（拒 bool/非有限）+ 源 B 的结构面。
        return f"missing, invalid, or non-finite rewards {rewards!r}"
    expected_winner = (players[0] if rewards[0] > rewards[1] else
                       players[1] if rewards[1] > rewards[0] else None)
    if game["winner_label"] != expected_winner:
        return "winner_label is inconsistent with players/rewards"
    if require_export_fields and game["winner"] != expected_winner:
        return "winner is inconsistent with winner_label/rewards"
    if expected_winner is None and rewards[0] != rewards[1]:
        return "tie requires equal rewards"
    if expected_domain is not None and game["seed_domain"] != expected_domain:
        return "game seed_domain differs from top-level seed_domain"
    if allowed_seeds is not None and game["seed"] not in allowed_seeds:
        return "game seed is outside configured seed set"
    return None


# --------------------------------------------------------------------------- #
# 并集语义锚定用例集（叶测试与顶层自检共用）
# --------------------------------------------------------------------------- #
def _base_record() -> Dict[str, Any]:
    """完整并集字段面的正常局底稿（分叉面用例在其上做单点覆写）。"""
    return {
        "players": ["cand", "cow_baron"],
        "p0": "cand", "p1": "cow_baron",
        "seed": 101, "seat": "AB", "seed_domain": "development",
        "statuses": ["DONE", "DONE"],
        "contract_ok": True,
        "winner_label": "cand", "winner": "cand",
        "rewards": [2.0, 1.0],
        "turns": 720, "turns_played": 720,
    }


def build_case_battery() -> List[Dict[str, Any]]:
    """锚定用例集：每条 = {name, game(或 None), kwargs, kind}。

    kind 口径：
      "normal"        —— 两旧实现同判正常（merged 必 None）；
      "parity_red"    —— 两旧实现同判红（merged 必红）；
      "union_red"     —— 分叉面：恰一旧实现判红（merged 必红=并集）；
      "eval_kwarg"    —— 源 B kwarg 判定面（A 无此参数面，按 B 锚定；
                          merged 带同 kwarg 必红、不带 kwarg 必 None）；
      "export_only"   —— 仅 require_export_fields 下判红（两模式都锚定）。
    """
    battery: List[Dict[str, Any]] = []

    def case(name, kind, overrides=None, drop=(), **kwargs):
        game = _base_record()
        for key in drop:
            game.pop(key, None)
        if overrides:
            game.update(overrides)
        battery.append({"name": name, "game": game, "kwargs": kwargs,
                        "kind": kind})

    case("normal", "normal")
    case("tie_equal_rewards", "normal",
         {"rewards": [1.0, 1.0], "winner_label": None, "winner": None})

    case("missing_statuses", "parity_red", drop=("statuses",))
    case("non_done_statuses", "parity_red",
         {"statuses": ["INVALID", "DONE"]})
    case("players_not_list", "parity_red", {"players": "cand"})
    case("players_wrong_len", "parity_red", {"players": ["cand"]})
    case("rewards_wrong_len", "parity_red", {"rewards": [1.0]})
    case("rewards_non_numeric", "parity_red", {"rewards": ["2", 1.0]})
    case("rewards_nan", "parity_red", {"rewards": [float("nan"), 1.0]})
    case("contract_ok_false", "parity_red", {"contract_ok": False})
    case("contract_ok_string", "parity_red", {"contract_ok": "yes"})
    case("winner_label_inconsistent", "parity_red",
         {"winner_label": "cow_baron"})
    case("winner_label_missing", "parity_red", drop=("winner_label",))

    # ---- 分叉面（union_red：恰一旧实现判红） ----
    # 1) players 两元素相同：仅 B 判红。
    case("players_identical", "union_red",
         {"players": ["cand", "cand"], "p0": "cand", "p1": "cand",
          "rewards": [2.0, 1.0], "winner_label": "cand", "winner": "cand"})
    # 2) rewards 为 bool：仅 A 判红（B 的 isinstance 放行 bool）。
    case("rewards_bool", "union_red",
         {"rewards": [True, False]})
    # 3) rewards 非有限 inf：仅 A 显式判红（B 完全漏判，胜者推导照常成立）。
    case("rewards_inf", "union_red",
         {"rewards": [float("inf"), 1.0]})
    # 4) 缺 seed / seat / seed_domain：仅 B 判红（A 无此字段面）。
    case("missing_seed", "union_red", drop=("seed",))
    case("missing_seat", "union_red", drop=("seat",))
    case("missing_seed_domain", "union_red", drop=("seed_domain",))
    case("seat_invalid", "union_red", {"seat": "XX"})

    # ---- 源 B kwarg 判定面（A 无对应参数，按 B 锚定） ----
    case("seed_domain_mismatch", "eval_kwarg", expected_domain="holdout")
    case("seed_outside_allowed", "eval_kwarg", allowed_seeds={201, 202})

    # ---- 导出面（仅 require_export_fields 判红） ----
    case("export_p0_p1_mismatch", "export_only",
         {"p0": "cow_baron", "p1": "cand"})
    case("export_winner_mismatch", "export_only", {"winner": "cow_baron"})
    return battery
