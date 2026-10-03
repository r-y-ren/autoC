"""Audit all round-10 first-eight-world screens against identical V9 cases."""

import json
from pathlib import Path

from compare_round8 import compare, read


ROOT = Path(__file__).resolve().parent
BASELINE = read([ROOT / "results/round10_v9_development.json"])
SCREENS = [
    "credit_flush",
    "ongoing_flush",
    "crop_flush",
    "crop_safe",
    "no_final_reorder",
    "market_early",
    "tomato_value",
    "post_slack_reorder",
    "post_slack_gated",
    "double_inside",
    "exact_sell",
    "opening_cash_v2",
    "crop_portfolio_v2",
    "arlene_benchmark",
]


def main() -> None:
    report = {"screen_worlds": 8, "confirmation_used": False,
              "comparison_family": "exploratory, selected/adapted on development worlds",
              "screens": {}}
    for name in SCREENS:
        path = ROOT / f"results/round10_{name}_screen.json"
        if not path.with_suffix(".jsonl").exists():
            continue
        candidate = read([path])
        keys = BASELINE.keys() & candidate.keys()
        base = {key: BASELINE[key] for key in keys}
        new = {key: candidate[key] for key in keys}
        paired = compare(base, new, familywise_candidates=len(SCREENS))
        paired["base_points"] = sum(row["points"] for row in base.values()) / len(base)
        paired["new_points"] = sum(row["points"] for row in new.values()) / len(new)
        paired["different_final_shops"] = sum(base[key]["shops"] != new[key]["shops"] for key in keys)
        report["screens"][name] = paired
    destination = ROOT / "results/round10_all_screens.json"
    destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
    for name, row in report["screens"].items():
        print(name, "valid", row["paired_games"], "invalid", row["invalid_pairs"],
              "points", round(row["new_points"], 6),
              "paired_gain", round(row["metrics"]["points_change"]["mean"], 6),
              "margin_gain", round(row["metrics"]["margin_change"]["mean"], 2),
              "shop_diff", row["different_final_shops"])


if __name__ == "__main__":
    main()
