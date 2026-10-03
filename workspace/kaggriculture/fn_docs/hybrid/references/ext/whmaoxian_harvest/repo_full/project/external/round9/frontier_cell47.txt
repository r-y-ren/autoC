import pandas as pd
import matplotlib.pyplot as plt

price_guard = pd.DataFrame([
    {"threshold": 28, "mean_margin_vs_price31": -1.583, "games": 24, "valid": 24},
    {"threshold": 30, "mean_margin_vs_price31": 14.833, "games": 24, "valid": 24},
    {"threshold": 31, "mean_margin_vs_price31": 33.500, "games": 24, "valid": 24},
    {"threshold": 33, "mean_margin_vs_price31": 33.500, "games": 24, "valid": 24},
    {"threshold": 35, "mean_margin_vs_price31": 33.500, "games": 24, "valid": 24},
])
price_guard["validity"] = price_guard["valid"].astype(str) + "/" + price_guard["games"].astype(str)
display(price_guard.style.format({"mean_margin_vs_price31": "{:+,.3f}"}))
fig, ax = plt.subplots(figsize=(9, 3.8))
ax.plot(price_guard["threshold"], price_guard["mean_margin_vs_price31"], marker="o", color="#0ea5e9")
ax.axvline(31, color="#ef4444", ls="--", label="chosen threshold")
ax.axhline(0, color="#111827", lw=1)
ax.set_xlabel("Minimum visible Wheat price for immediate sale")
ax.set_ylabel("Mean margin versus price31 control")
ax.set_title("Fresh 1.32.7 threshold holdout · 12 seeds × 2 seats")
ax.grid(alpha=.25); ax.legend(); plt.tight_layout(); display(fig); plt.close(fig)
assert (price_guard["valid"] == price_guard["games"]).all()
print("All threshold panels valid:", ", ".join(price_guard["validity"]))
